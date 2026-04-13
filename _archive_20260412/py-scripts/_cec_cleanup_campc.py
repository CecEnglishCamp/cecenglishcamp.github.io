#!/usr/bin/env python3
import sys, io, re, glob, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

folder = r'C:\Users\cecsu\cecenglishcamp.github.io\camp-c'
fixed = 0

for fpath in sorted(glob.glob(os.path.join(folder, '**', '*.html'), recursive=True)):
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    original = content

    # ① 구버전 practice-wrap CSS/HTML/JS 완전 제거
    # Old CSS block
    content = re.sub(
        r'/\*\s*──\s*프롬프트.*?\*/\s*\.practice-wrap\s*\{.*?\.launch-note\s*\{[^}]*\}',
        '',
        content,
        flags=re.DOTALL
    )
    content = re.sub(
        r'\.practice-wrap\s*\{.*?\.launch-note\s*\{[^}]*\}',
        '',
        content,
        flags=re.DOTALL
    )

    # Old HTML block
    content = re.sub(
        r'<!--\s*프롬프트[^>]*-->\s*<div class="practice-wrap">.*?</div>\s*</div>\s*</div>',
        '',
        content,
        flags=re.DOTALL
    )
    content = re.sub(
        r'<div class="practice-wrap">.*?</div>\s*</div>\s*</div>',
        '',
        content,
        flags=re.DOTALL
    )

    # Old JS block (getCampType/buildSummary/copyPrompt/launchChatGPTPractice)
    content = re.sub(
        r'<script>\s*function getCampType\(\).*?</script>',
        '',
        content,
        flags=re.DOTALL
    )

    # ② 구버전 loose text/buttons 제거
    # chatgpt-launch-btn outside pw-wrap
    content = re.sub(
        r'\s*<button[^>]*class="chatgpt-launch-btn"[^>]*>.*?</button>',
        '',
        content,
        flags=re.DOTALL
    )
    # chatgpt-practice-note
    content = re.sub(
        r'\s*<div[^>]*class="chatgpt-practice-note"[^>]*>.*?</div>',
        '',
        content,
        flags=re.DOTALL
    )
    # launch-note outside pw-wrap (but not inside pw-launch)
    # leave this alone - it's part of pw-wrap

    # ③ pw-wrap 위치 확인: </body> 바로 앞으로 이동
    pw_match = re.search(
        r'(<style>\s*\.pw-wrap.*?</style>\s*<div class="pw-wrap">.*?</div>\s*</div>\s*</div>\s*<script>\s*function pwBuild.*?</script>)',
        content,
        flags=re.DOTALL
    )
    if pw_match:
        pw_block = pw_match.group(1)
        body_idx = content.rfind('</body>')
        pw_end = pw_match.end()
        # Check if there's significant content between pw_block end and </body>
        between = content[pw_end:body_idx].strip()
        # Remove empty style tags and whitespace
        between_clean = re.sub(r'</?style[^>]*>', '', between).strip()
        if len(between_clean) > 5:
            # pw-wrap is not right before </body>, move it
            content = content.replace(pw_block, '')
            content = content.replace('</body>', pw_block + '\n</body>')

    # ④ 빈 <style></style> 태그 제거
    content = re.sub(r'<style>\s*</style>', '', content)

    # ⑤ 과도한 빈 줄 정리
    content = re.sub(r'\n{4,}', '\n\n', content)

    if content != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        fixed += 1

print(f'Fixed: {fixed}')
