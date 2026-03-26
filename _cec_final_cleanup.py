#!/usr/bin/env python3
"""Final camp-c cleanup: remove remnant lines, preserve everything else."""
import sys, io, glob, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

REMNANT_MARKERS = ['오늘 공부 완료', 'ChatGPT 선생님과 대화하기', '클릭하면 학습 내용이 복사']
PROTECT = ['pw-wrap', 'pw-launch', 'pwBuild', 'pwCopy', 'pwLaunch']

folder = 'camp-c'
fixed = 0

for fpath in sorted(glob.glob(os.path.join(folder, '**', '*.html'), recursive=True)):
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    original = lines[:]
    new_lines = []

    for line in lines:
        # Check if this line has a remnant marker
        has_remnant = any(m in line for m in REMNANT_MARKERS)
        # Check if this line is inside pw-wrap (protected)
        is_protected = any(p in line for p in PROTECT)

        if has_remnant and not is_protected:
            # Skip this line (remove it)
            continue
        new_lines.append(line)

    if len(new_lines) != len(original):
        with open(fpath, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        removed = len(original) - len(new_lines)
        fixed += 1
        print(f'  {os.path.relpath(fpath, folder)}: {removed} lines removed')

print(f'\nTotal files fixed: {fixed}')
