#!/usr/bin/env python3
import sys, io, re, glob, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

INJECT = r'''
<style>
.pw-wrap{max-width:860px;margin:40px auto;padding:0 20px;display:flex;flex-direction:column;gap:16px;}
.pw-prompt{background:#f0faf5;border-radius:20px;border:2px solid #6ee7b7;padding:24px 28px;}
.pw-header{display:flex;align-items:center;gap:10px;margin-bottom:16px;}
.pw-header img{width:36px;height:36px;border-radius:50%;object-fit:cover;}
.pw-header-t{font-size:14px;font-weight:700;color:#065f46;}
.pw-header-s{font-size:11px;color:#6b7280;margin-top:1px;}
.pw-body{background:#fff;border:1px solid #a7f3d0;border-radius:12px;padding:16px 18px;font-size:13px;color:#374151;line-height:1.85;white-space:pre-line;margin-bottom:16px;min-height:60px;}
.pw-copy{width:100%;padding:14px;background:#059669;color:#fff;border:none;border-radius:12px;font-size:15px;font-weight:700;cursor:pointer;font-family:inherit;}
.pw-ok{display:none;margin-top:10px;color:#059669;font-size:13px;font-weight:700;text-align:center;}
.pw-launch{background:#f5f3ff;border-radius:20px;border:2px solid #c4b5fd;padding:24px 28px;text-align:center;}
.pw-launch-title{font-size:16px;font-weight:700;color:#4c1d95;margin-bottom:6px;}
.pw-launch-desc{font-size:13px;color:#6b7280;line-height:1.7;margin-bottom:20px;}
.pw-launch-desc strong{color:#7c3aed;}
.pw-btn{display:inline-flex;align-items:center;gap:10px;padding:16px 40px;background:linear-gradient(135deg,#2563eb,#7c3aed);color:#fff;border:none;border-radius:50px;font-size:16px;font-weight:700;cursor:pointer;font-family:inherit;}
.pw-note{margin-top:10px;font-size:12px;color:#9ca3af;}
</style>
<div class="pw-wrap">
  <div class="pw-prompt">
    <div class="pw-header">
      <img src="https://pub-a418b5aad0bd4c3fb41cf7159403fc12.r2.dev/robo_jump.gif" alt="Robo">
      <div><div class="pw-header-t">AI 튜터 빅스와 영어 연습</div>
      <div class="pw-header-s">오늘 배운 내용을 ChatGPT에 붙여넣으세요</div></div>
    </div>
    <div class="pw-body" id="pwBody"></div>
    <button class="pw-copy" onclick="pwCopy()">📋 프롬프트 복사하기</button>
    <div class="pw-ok" id="pwOk">✅ 복사됐어요! ChatGPT에서 Ctrl+V 하세요!</div>
  </div>
  <div class="pw-launch">
    <div style="font-size:20px;margin-bottom:6px;">🎉</div>
    <div class="pw-launch-title">수업 완료! 이제 회화 연습!</div>
    <div class="pw-launch-desc">오늘 배운 내용을 보면서 <strong>ChatGPT</strong>와 대화해보세요!<br>
    <strong>왼쪽</strong>엔 오늘 수업, <strong>오른쪽</strong>엔 ChatGPT가 열립니다.</div>
    <button class="pw-btn" onclick="pwLaunch()">🎙️ ChatGPT 회화 연습 시작</button>
    <div class="pw-note">※ 처음 한 번만 팝업 허용이 필요합니다</div>
  </div>
</div>
<script>
function pwBuild(){
  var w=[];
  document.querySelectorAll('.key-expression,.expression-en,.vocab-en,.v-eng,.word-en,.key-word')
    .forEach(function(e){var t=e.textContent.trim();if(t&&t.length<40)w.push(t);});
  var s=document.querySelector('.story-en,.dialogue p,.story-content p,.ep-story p');
  var st=s?s.textContent.replace(/\s+/g,' ').trim().substring(0,100)+'...':'';
  return ['안녕! 나는 CEC English Camp 학생이야.',
    '오늘 '+document.title+' 을 공부했어.','',
    '📚 오늘 배운 내용:',
    w.length?'- 표현/단어: '+w.slice(0,8).join(', '):'',
    st?'- 내용: '+st:'','',
    '[할 것 - 5분] 오늘 배운 표현으로 짧은 대화를 도와줘.',
    '[할 것 - 10분] 오늘 상황과 비슷한 롤플레이를 해줘.',
    '[할 것 - 5분] 내가 말하는 영어를 듣고 자연스럽게 대화해줘.'
  ].filter(Boolean).join('\n');
}
function pwCopy(){
  navigator.clipboard.writeText(pwBuild()).then(function(){
    var e=document.getElementById('pwOk');
    if(e){e.style.display='block';setTimeout(function(){e.style.display='none';},3000);}
  });
}
function pwLaunch(){
  window.location.href='https://cecenglishcamp.github.io/cec_guide.html'
    +'?camp=c&url='+encodeURIComponent(window.location.href)
    +'&summary='+encodeURIComponent(pwBuild());
}
window.addEventListener('load',function(){
  var e=document.getElementById('pwBody');
  if(e)e.textContent=pwBuild();
});
</script>'''

folder = r'C:\Users\cecsu\cecenglishcamp.github.io\camp-c'
fixed = 0

for fpath in sorted(glob.glob(os.path.join(folder, '**', '*.html'), recursive=True)):
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    original = content

    # ── 모든 구버전 코드 제거 ──
    # pw-wrap CSS+HTML+JS blocks
    content = re.sub(r'<style>\s*\n?\.pw-wrap\{.*?</script>', '', content, flags=re.DOTALL)
    content = re.sub(r'<style>\s*\n?\.pw-wrap\s*\{.*?</script>', '', content, flags=re.DOTALL)
    # practice-wrap CSS+HTML+JS blocks
    content = re.sub(r'<style>\s*\n?\.practice-wrap\s*\{.*?</script>', '', content, flags=re.DOTALL)
    # chatgpt-practice sections
    content = re.sub(r'<div[^>]*class="chatgpt-practice[^"]*"[^>]*>.*?</div>\s*</div>', '', content, flags=re.DOTALL)
    # Standalone pw- blocks (no <style> wrapper)
    content = re.sub(r'<div class="pw-wrap">.*?</div>\s*</div>\s*</div>', '', content, flags=re.DOTALL)
    content = re.sub(r'<script>\s*\n?function pwBuild.*?</script>', '', content, flags=re.DOTALL)
    # Old getCampType/buildSummary scripts
    content = re.sub(r'<script>\s*\n?function getCampType\(\).*?</script>', '', content, flags=re.DOTALL)
    # Orphaned style blocks with pw- or practice-wrap
    content = re.sub(r'<style>[^<]*\.pw-[^<]*</style>', '', content, flags=re.DOTALL)
    content = re.sub(r'<style>[^<]*\.practice-wrap[^<]*</style>', '', content, flags=re.DOTALL)
    # Empty style tags
    content = re.sub(r'<style>\s*</style>', '', content)
    # Excess blank lines
    content = re.sub(r'\n{4,}', '\n\n', content)

    # ── </body> 앞에 새 코드 삽입 ──
    if '</body>' in content and 'pwBuild' not in content:
        content = content.replace('</body>', INJECT + '\n</body>', 1)

    if content != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        fixed += 1

print(f'Fixed: {fixed}')
