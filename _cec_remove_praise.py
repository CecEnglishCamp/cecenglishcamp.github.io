#!/usr/bin/env python3
"""Remove AI praise sections, Robo AI cards, and praise popups from camp-a lessons."""
import sys, io, glob, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

TARGETS = [
    'AI 선생님한테 칭찬',
    'AI 선생님과 대화하기',
    'AI PRAISE',
    'Robo AI에게 오늘 배운 거 자랑하기',
    'Robo AI에게',
]

def remove_praise_sections(content):
    """Remove AI praise card sections, praise popups, and related CSS."""
    lines = content.split('\n')
    result = []
    skip_depth = 0
    skip_until_close = None
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # ── Skip: card section containing AI PRAISE / Robo AI ──
        # Detect start of a card div that contains target text
        if skip_depth == 0 and '<div class="card">' in stripped:
            # Look ahead to see if this card contains target text
            lookahead = '\n'.join(lines[i:i+30])
            is_target = any(t in lookahead for t in TARGETS)
            if is_target:
                # Count div depth to find matching close
                depth = 0
                j = i
                while j < len(lines):
                    depth += lines[j].count('<div')
                    depth -= lines[j].count('</div')
                    if depth <= 0:
                        break
                    j += 1
                # Skip lines i through j (inclusive)
                i = j + 1
                continue

        # ── Skip: section containing "I learned" text box ──
        if skip_depth == 0 and 'I learned' in stripped and ('<div' in stripped or '<p' in stripped):
            # Look for containing div and skip it
            if '<div' in stripped:
                depth = 0
                j = i
                while j < len(lines):
                    depth += lines[j].count('<div')
                    depth -= lines[j].count('</div')
                    if depth <= 0:
                        break
                    j += 1
                i = j + 1
                continue

        # ── Skip: praise popup divs ──
        if 'class="praise-bg"' in stripped or 'id="pbg"' in stripped:
            # Single line or multi-line div
            depth = 0
            j = i
            while j < len(lines):
                depth += lines[j].count('<div')
                depth -= lines[j].count('</div')
                if depth <= 0:
                    break
                j += 1
            i = j + 1
            continue

        if ('class="praise"' in stripped or 'id="pop"' in stripped) and 'praise-bg' not in stripped and 'practice' not in stripped:
            depth = 0
            j = i
            while j < len(lines):
                depth += lines[j].count('<div')
                depth -= lines[j].count('</div')
                if depth <= 0:
                    break
                j += 1
            i = j + 1
            continue

        # ── Skip: divs with robo-chat class ──
        if 'robo-chat' in stripped and '<div' in stripped:
            depth = 0
            j = i
            while j < len(lines):
                depth += lines[j].count('<div')
                depth -= lines[j].count('</div')
                if depth <= 0:
                    break
                j += 1
            i = j + 1
            continue

        result.append(line)
        i += 1

    content = '\n'.join(result)

    # ── Remove praise CSS rules ──
    # Remove .praise-bg, .praise (but not .chatgpt-practice), .praise-icon, .praise-t, .praise-s
    # These are typically multi-line CSS blocks
    css_patterns = [
        r'/\*\s*=+\s*PRAISE\s*POPUP\s*=+\s*\*/',  # comment header
        r'\.praise-bg\{[^}]*\}',
        r'\.praise-bg\.on\{[^}]*\}',
        r'\.praise\{[^}]*\}',
        r'\.praise\.on\{[^}]*\}',
        r'\.praise-icon\{[^}]*\}',
        r'\.praise-t\{[^}]*\}',
        r'\.praise-s\{[^}]*\}',
    ]
    for pat in css_patterns:
        content = re.sub(pat, '', content, flags=re.DOTALL)

    # Also handle multi-line CSS blocks
    css_ml_patterns = [
        r'/\*\s*=+\s*PRAISE\s*POPUP\s*=+\s*\*/',
        r'\.praise-bg\s*\{[^}]*\}',
        r'\.praise-bg\.on\s*\{[^}]*\}',
        r'\.praise\s*\{[^}]*\}',
        r'\.praise\.on\s*\{[^}]*\}',
        r'\.praise-icon\s*\{[^}]*\}',
        r'\.praise-t\s*\{[^}]*\}',
        r'\.praise-s\s*\{[^}]*\}',
    ]
    for pat in css_ml_patterns:
        content = re.sub(pat, '', content, flags=re.DOTALL)

    # Remove .ai-card CSS (the card inside the praise section, not header btn)
    content = re.sub(r'\.ai-card\s*\{[^}]*\}', '', content, flags=re.DOTALL)
    content = re.sub(r'\.ai-title\s*\{[^}]*\}', '', content, flags=re.DOTALL)
    content = re.sub(r'\.ai-desc\s*\{[^}]*\}', '', content, flags=re.DOTALL)
    content = re.sub(r'\.ai-btn\s*\{[^}]*\}', '', content, flags=re.DOTALL)
    content = re.sub(r'\.ai-btn:hover\s*\{[^}]*\}', '', content, flags=re.DOTALL)

    # Clean up excessive blank lines
    content = re.sub(r'\n{3,}', '\n\n', content)

    return content


base = r'C:\Users\cecsu\cecenglishcamp.github.io\camp-a\lessons'
files = glob.glob(os.path.join(base, '**', '*.html'), recursive=True)
modified = 0

for f in sorted(files):
    with open(f, 'r', encoding='utf-8', errors='ignore') as fh:
        original = fh.read()

    # Check if file has any target content
    has_target = any(t in original for t in TARGETS + ['praise-bg', 'robo-chat'])
    if not has_target:
        continue

    cleaned = remove_praise_sections(original)
    if cleaned != original:
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(cleaned)
        rel = os.path.relpath(f, base)
        print(f'  Cleaned: {rel}')
        modified += 1

print(f'\nTotal cleaned: {modified}')
