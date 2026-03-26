#!/usr/bin/env python3
"""Remove Open WebUI references from camp-b files that already have ChatGPT button."""
import os, re, sys, glob, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

EXCLUDE_KEYWORDS = ['grammar', 'gram', 'prestep', 'index', 'guide']

def should_exclude(filepath):
    basename = os.path.basename(filepath).lower()
    return any(kw in basename for kw in EXCLUDE_KEYWORDS)

def remove_openwebui(content):
    """Remove Open WebUI buttons/links/sections."""
    # Remove <a> tags with localhost:3001
    content = re.sub(
        r'<a\s[^>]*localhost:3001[^>]*>.*?</a>',
        '', content, flags=re.DOTALL | re.IGNORECASE
    )
    # Remove onclick with localhost:3001
    content = re.sub(
        r'<button[^>]*onclick="[^"]*localhost:3001[^"]*"[^>]*>.*?</button>',
        '', content, flags=re.DOTALL | re.IGNORECASE
    )
    # Remove lines referencing localhost:3001 in links/buttons
    lines = content.split('\n')
    cleaned = []
    for line in lines:
        if 'localhost:3001' in line and any(tag in line for tag in ['<a ', '<button', 'onclick', 'href=', 'window.open']):
            continue
        if 'Open WebUI' in line and any(tag in line for tag in ['<a ', '<button', '<div', '<span', '<p']):
            continue
        cleaned.append(line)
    content = '\n'.join(cleaned)
    content = re.sub(r'\n{3,}', '\n\n', content)
    return content

base = r'C:\Users\cecsu\cecenglishcamp.github.io\camp-b'
files = glob.glob(os.path.join(base, '**', '*.html'), recursive=True)
modified = 0

for f in sorted(files):
    if should_exclude(f):
        continue
    with open(f, 'r', encoding='utf-8', errors='ignore') as fh:
        original = fh.read()
    if 'localhost:3001' not in original and 'Open WebUI' not in original:
        continue
    cleaned = remove_openwebui(original)
    if cleaned != original:
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(cleaned)
        rel = os.path.relpath(f, base)
        print(f"  Cleaned: {rel}")
        modified += 1

print(f"\nTotal cleaned: {modified}")
