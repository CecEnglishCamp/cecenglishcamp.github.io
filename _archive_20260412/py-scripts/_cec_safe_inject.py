#!/usr/bin/env python3
"""Safe inject: ONLY append pw_inject.html before </body>. Never modify existing code."""
import sys, io, glob, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('pw_inject.html', 'r', encoding='utf-8') as f:
    INJECT = f.read()

folder = r'C:\Users\cecsu\cecenglishcamp.github.io\camp-c'
injected = 0
skipped = 0

for fpath in sorted(glob.glob(os.path.join(folder, '**', '*.html'), recursive=True)):
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Already has pw-wrap? SKIP
    if 'pw-wrap' in content or 'pwBuild' in content:
        skipped += 1
        continue

    # No </body>? SKIP
    if '</body>' not in content:
        skipped += 1
        continue

    # ONLY insert before </body>, touch nothing else
    content = content.replace('</body>', INJECT + '\n</body>', 1)

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)
    injected += 1

print(f'Injected: {injected}, Skipped: {skipped}')
