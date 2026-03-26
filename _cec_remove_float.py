#!/usr/bin/env python3
import sys, io, re, glob, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

REMOVE = [
    r'🎉\s*수업 완료! 이제 회화 연습!\s*\n?',
    r'오늘 배운 내용을 보면서 <strong>ChatGPT</strong>와 대화해보세요!\s*<br>?\s*\n?',
    r'<strong>왼쪽</strong>엔 오늘 수업, <strong>오른쪽</strong>엔 ChatGPT가 열립니다\.\s*\n?',
    r'※ 처음 한 번만 팝업 허용이 필요합니다\s*\n?',
    r'<a[^>]*openChatGPT[^>]*>.*?</a>',
    r'<button[^>]*openChatGPT[^>]*>.*?</button>',
    r'<div class="chatgpt-section[^"]*"[^>]*>\s*</div>',
    r'<div class="completion[^"]*"[^>]*>\s*</div>',
]

folder = r'C:\Users\cecsu\cecenglishcamp.github.io\camp-c'
fixed = 0
for fpath in sorted(glob.glob(os.path.join(folder, '**', '*.html'), recursive=True)):
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    original = content
    for pat in REMOVE:
        content = re.sub(pat, '', content, flags=re.DOTALL)
    if content != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        fixed += 1
        print(f'  Fixed: {os.path.relpath(fpath, folder)}')
print(f'Total: {fixed}')
