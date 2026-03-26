#!/usr/bin/env python3
import sys, io, re, glob, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

folder = r'C:\Users\cecsu\cecenglishcamp.github.io\camp-c'
fixed = 0

for fpath in sorted(glob.glob(os.path.join(folder, '**', '*.html'), recursive=True)):
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    original = content

    content = re.sub(
        r'(</style>\s*)(</div>\s*)(<style>\s*\.pw-wrap)',
        r'\1\3',
        content,
        flags=re.DOTALL
    )

    if content != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        fixed += 1
        print(f'  Fixed: {os.path.relpath(fpath, folder)}')

print(f'Total: {fixed}')
