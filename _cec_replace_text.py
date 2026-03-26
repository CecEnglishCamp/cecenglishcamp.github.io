#!/usr/bin/env python3
"""Replace 'Open WebUI' text references with 'ChatGPT' in camp-b files."""
import os, glob, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

EXCLUDE_KEYWORDS = ['grammar', 'gram', 'prestep', 'index', 'guide']

def should_exclude(filepath):
    basename = os.path.basename(filepath).lower()
    return any(kw in basename for kw in EXCLUDE_KEYWORDS)

base = r'C:\Users\cecsu\cecenglishcamp.github.io\camp-b'
files = glob.glob(os.path.join(base, '**', '*.html'), recursive=True)
modified = 0

for f in sorted(files):
    if should_exclude(f):
        continue
    with open(f, 'r', encoding='utf-8', errors='ignore') as fh:
        content = fh.read()
    if 'Open WebUI' not in content:
        continue
    new_content = content.replace('Open WebUI', 'ChatGPT')
    if new_content != content:
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(new_content)
        rel = os.path.relpath(f, base)
        print(f"  Replaced: {rel}")
        modified += 1

print(f"\nTotal replaced: {modified}")
