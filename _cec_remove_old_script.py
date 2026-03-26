#!/usr/bin/env python3
"""Remove old chatgpt-practice-section HTML + getCampType/launchChatGPTPractice script blocks."""
import sys, io, re, glob, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

folder = 'camp-c'
fixed = 0

for fpath in sorted(glob.glob(os.path.join(folder, '**', '*.html'), recursive=True)):
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    original = content

    # Remove old chatgpt-practice-section HTML
    content = re.sub(
        r'<div class="chatgpt-practice-section">.*?</div>\s*</div>',
        '', content, flags=re.DOTALL
    )

    # Remove old script block with getCampType + launchChatGPTPractice
    content = re.sub(
        r'<script>\s*\n?function getCampType\(\).*?</script>',
        '', content, flags=re.DOTALL
    )

    # Remove old CSS for chatgpt-practice classes
    content = re.sub(
        r'/\*\s*──\s*ChatGPT.*?\*/.*?\.chatgpt-practice-note\s*\{[^}]*\}',
        '', content, flags=re.DOTALL
    )
    content = re.sub(
        r'\.chatgpt-practice-section\s*\{.*?\.chatgpt-practice-note\s*\{[^}]*\}',
        '', content, flags=re.DOTALL
    )

    # Clean up
    content = re.sub(r'\n{4,}', '\n\n', content)

    if content != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        fixed += 1

print(f'Fixed: {fixed}')
