#!/usr/bin/env python3
"""Upgrade Camp A prompt sections to Camp B style."""
import sys, io, glob, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

EXCLUDE = ['grammar', 'gram', 'prestep', 'index', 'guide']

OLD_CSS_START = '/* ── ChatGPT 회화 연습 버튼 ── */'
OLD_CSS_START2 = '/* -- ChatGPT practice button -- */'
OLD_CSS_START3 = '/* -- ChatGPT practice -- */'
OLD_CSS_END_MARKERS = ['.copy-done {', '.copy-btn:hover']

NEW_CSS = """/* ── 프롬프트 + ChatGPT 연습 ── */
.practice-wrap {
  max-width: 860px;
  margin: 40px auto 40px;
  padding: 0 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}
.prompt-section {
  background: #1a2a1a;
  border: 1px solid rgba(0,200,80,0.3);
  border-radius: 16px;
  padding: 20px 24px;
}
.prompt-header {
  font-size: 1rem;
  font-weight: 700;
  color: #4ade80;
  margin-bottom: 14px;
  display: flex;
  align-items: center;
  gap: 8px;
}
.prompt-body {
  background: rgba(0,0,0,0.3);
  border-radius: 10px;
  padding: 14px 16px;
  font-size: 0.85rem;
  color: #a8c8a8;
  line-height: 1.8;
  white-space: pre-line;
  margin-bottom: 16px;
  min-height: 80px;
}
.copy-prompt-btn {
  background: #2d6a2d;
  color: #fff;
  border: none;
  border-radius: 50px;
  padding: 12px 28px;
  font-size: 0.95rem;
  font-weight: 700;
  cursor: pointer;
  font-family: inherit;
  transition: background 0.2s, transform 0.15s;
  width: 100%;
}
.copy-prompt-btn:hover {
  background: #3a8a3a;
  transform: translateY(-1px);
}
.copy-feedback {
  display: none;
  margin-top: 10px;
  color: #4ade80;
  font-size: 0.85rem;
  font-weight: 700;
  text-align: center;
}
.chatgpt-launch-wrap {
  background: linear-gradient(135deg, #050e1f, #0a1628);
  border: 2px solid rgba(0,210,255,0.4);
  border-radius: 20px;
  padding: 28px;
  text-align: center;
}
.launch-title {
  font-size: 1.2rem;
  font-weight: 700;
  color: #fff;
  margin-bottom: 8px;
}
.launch-desc {
  color: #6a8fad;
  font-size: 0.88rem;
  line-height: 1.7;
  margin-bottom: 20px;
}
.launch-desc strong { color: #00d2ff; }
.chatgpt-launch-btn {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  background: linear-gradient(135deg, #00d2ff, #0055ff);
  color: #fff;
  font-size: 1rem;
  font-weight: 700;
  padding: 16px 36px;
  border: none;
  border-radius: 50px;
  cursor: pointer;
  box-shadow: 0 0 30px rgba(0,210,255,0.3);
  transition: transform 0.2s;
  font-family: inherit;
}
.chatgpt-launch-btn:hover { transform: translateY(-2px); }
.launch-note {
  margin-top: 12px;
  font-size: 0.75rem;
  color: #3a5a7a;
}
"""

NEW_HTML_JS = """<!-- 프롬프트 + ChatGPT 연습 섹션 -->
<div class="practice-wrap">

  <!-- 프롬프트 박스 -->
  <div class="prompt-section">
    <div class="prompt-header">🤖 AI 튜터 빅스와 영어 연습</div>
    <div class="prompt-body" id="promptBody"></div>
    <button class="copy-prompt-btn" onclick="copyPrompt()">📋 프롬프트 복사하기</button>
    <div class="copy-feedback" id="copyFeedback">✅ 복사됐어요! ChatGPT에서 Ctrl+V 하세요!</div>
  </div>

  <!-- ChatGPT 시작 버튼 -->
  <div class="chatgpt-launch-wrap">
    <div class="launch-title">🎉 수업 완료! 이제 회화 연습!</div>
    <div class="launch-desc">
      오늘 배운 내용을 보면서 <strong>ChatGPT</strong>와 영어로 대화해보세요!<br>
      <strong>왼쪽</strong>엔 오늘 수업, <strong>오른쪽</strong>엔 ChatGPT가 열립니다.
    </div>
    <button class="chatgpt-launch-btn" onclick="launchChatGPTPractice()">🎙️ ChatGPT 회화 연습 시작</button>
    <div class="launch-note">※ 처음 한 번만 팝업 허용이 필요합니다</div>
  </div>

</div>

<script>
function getCampType() {
  var path = window.location.pathname;
  if (path.includes('camp-b') || path.includes('/m1/') ||
      path.includes('/m2/') || path.includes('/m3/')) return 'b';
  if (path.includes('camp-c') || path.includes('mom-teacher')) return 'c';
  return 'a';
}

function buildSummary() {
  var words = [];
  document.querySelectorAll(
    '.v-eng, .word-en, .vocab-en, .key-word, .key-eng, .eng-word'
  ).forEach(function(el) {
    var t = el.textContent.trim();
    if (t && t.length < 40) words.push(t);
  });

  var storyEl = document.querySelector(
    '.story-en, .story-content.active p, .story-content p, .reading-text p, .story p'
  );
  var storyText = '';
  if (storyEl) {
    storyText = storyEl.textContent
      .replace(/\\s+/g, ' ').trim()
      .substring(0, 100) + '...';
  }

  var title = document.title;

  return [
    '안녕! 나는 CEC English Camp 학생이야.',
    '오늘 ' + title + ' 을 공부했어.',
    '',
    '📚 오늘 배운 내용:',
    words.length ? '- 단어: ' + words.slice(0,8).join(', ') : '',
    storyText ? '- 이야기: ' + storyText : '',
    '',
    '[할 것 - 5분] 오늘 배운 단어로 짧은 영어 문장 만드는 것을 도와줘.',
    '[할 것 - 10분] 이야기 내용으로 간단한 질문 5개 만들어줘.',
    '[할 것 - 5분] 내가 말하는 영어를 듣고 자연스럽게 대화해줘.'
  ].filter(function(l) { return l !== undefined; }).join('\\n');
}

function copyPrompt() {
  var summary = buildSummary();
  navigator.clipboard.writeText(summary).then(function() {
    var fb = document.getElementById('copyFeedback');
    if (fb) {
      fb.style.display = 'block';
      setTimeout(function() { fb.style.display = 'none'; }, 3000);
    }
  });
}

function launchChatGPTPractice() {
  var summary = buildSummary();
  var camp = getCampType();
  var guideUrl = 'https://cecenglishcamp.github.io/cec_guide.html'
    + '?camp=' + camp
    + '&url=' + encodeURIComponent(window.location.href)
    + '&summary=' + encodeURIComponent(summary);
  window.location.href = guideUrl;
}

window.addEventListener('load', function() {
  var el = document.getElementById('promptBody');
  if (el) el.textContent = buildSummary();
});
</script>
"""


def process_file(filepath):
    bn = os.path.basename(filepath).lower()
    if any(kw in bn for kw in EXCLUDE):
        return False

    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Skip if already upgraded (exact class, not substring of chatgpt-practice-wrap)
    if '"practice-wrap"' in content:
        return False
    # Must have old chatgpt section
    if 'chatgpt-practice-section' not in content and 'chatgpt-launch-btn' not in content:
        return False

    original = content

    # 1. Remove old CSS block
    for marker in [OLD_CSS_START, OLD_CSS_START2, OLD_CSS_START3]:
        idx = content.find(marker)
        if idx != -1:
            # Find end: look for </style> after this point
            end_style = content.find('</style>', idx)
            if end_style != -1:
                content = content[:idx] + NEW_CSS + content[end_style:]
            break

    # 2. Remove old HTML section (chatgpt-practice-section through its closing divs)
    content = re.sub(
        r'<div class="chatgpt-practice-section">.*?</div>\s*</div>',
        '', content, flags=re.DOTALL
    )

    # Remove the old script block with getCampType
    content = re.sub(
        r'<script>\s*\n?\s*function getCampType\(\).*?</script>',
        '', content, flags=re.DOTALL
    )

    # 3. Insert new HTML+JS before </body>
    idx = content.rfind('</body>')
    if idx != -1:
        content = content[:idx] + NEW_HTML_JS + '\n' + content[idx:]

    # Clean up excessive blank lines
    content = re.sub(r'\n{4,}', '\n\n', content)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


base = r'C:\Users\cecsu\cecenglishcamp.github.io\camp-a\lessons'
files = sorted(glob.glob(os.path.join(base, '**', '*.html'), recursive=True))
count = 0
for f in files:
    # Skip week01.html in grade3 (already done)
    if f.endswith('grade3\\week01.html') or f.endswith('grade3/week01.html'):
        continue
    if process_file(f):
        count += 1
        print(f'  + {os.path.relpath(f, base)}')

print(f'\nTotal modified: {count}')
