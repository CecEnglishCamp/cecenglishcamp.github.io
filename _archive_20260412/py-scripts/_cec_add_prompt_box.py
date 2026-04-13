#!/usr/bin/env python3
"""Add prompt copy box to ChatGPT practice sections in all camps."""
import sys, io, glob, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

EXCLUDE_KEYWORDS = ['grammar', 'gram', 'prestep', 'index', 'guide']

def should_exclude(filepath):
    basename = os.path.basename(filepath).lower()
    return any(kw in basename for kw in EXCLUDE_KEYWORDS)

# ── CSS to add ──
PROMPT_CSS = """
/* ── Prompt Copy Box ── */
.prompt-box {
  background: rgba(0,210,255,0.06);
  border: 1px solid rgba(0,210,255,0.25);
  border-radius: 14px;
  padding: 16px 20px;
  margin-bottom: 20px;
  text-align: left;
}
.prompt-label {
  font-size: 0.75rem;
  color: #00d2ff;
  font-weight: 700;
  margin-bottom: 10px;
  letter-spacing: 1px;
}
.prompt-text {
  font-size: 0.82rem;
  color: #8ab0c8;
  line-height: 1.7;
  white-space: pre-line;
  margin-bottom: 14px;
}
.copy-btn {
  background: linear-gradient(135deg, #00d2ff, #0055ff);
  color: #fff;
  border: none;
  border-radius: 50px;
  padding: 10px 24px;
  font-size: 0.9rem;
  font-weight: 700;
  cursor: pointer;
  font-family: inherit;
  transition: transform 0.15s;
}
.copy-btn:hover { transform: scale(1.03); }
.copy-done {
  margin-top: 10px;
  color: #00e88a;
  font-size: 0.85rem;
  font-weight: 700;
}
"""

PROMPT_HTML = """<div class="prompt-box" id="promptBox">
      <div class="prompt-label">📋 오늘 학습 요약 (ChatGPT에 붙여넣기용)</div>
      <div class="prompt-text" id="promptText"></div>
      <button class="copy-btn" onclick="copyPrompt()">📋 프롬프트 복사하기</button>
      <div class="copy-done" id="copyDone" style="display:none">✅ 복사됐어요! ChatGPT에서 Ctrl+V 하세요!</div>
    </div>"""

# New JS functions to replace existing launchChatGPTPractice
NEW_JS = """
function buildSummary() {
  var words = [];
  document.querySelectorAll(
    '.word-en, .vocab-en, .key-word, .key-expression, .expression-en'
  ).forEach(function(el) {
    var t = el.textContent.trim();
    if (t && t.length < 30) words.push(t);
  });
  var storyEl = document.querySelector(
    '.story-content.active p, .reading-text p, .story p, .story-content p, .dialogue p'
  );
  var firstLine = storyEl
    ? storyEl.textContent.substring(0, 80) + '...' : '';
  return [
    '[' + document.title + ']',
    words.length ? '배운 단어: ' + words.slice(0,8).join(', ') : '',
    firstLine ? '오늘 이야기: ' + firstLine : '',
    '위 내용으로 영어 회화 연습을 도와주세요!'
  ].filter(Boolean).join('\\n');
}

function copyPrompt() {
  var summary = buildSummary();
  document.getElementById('promptText').textContent = summary;
  navigator.clipboard.writeText(summary).then(function() {
    document.getElementById('copyDone').style.display = 'block';
    setTimeout(function() {
      document.getElementById('copyDone').style.display = 'none';
    }, 3000);
  });
}

function launchChatGPTPractice() {
  var summary = buildSummary();
  document.getElementById('promptText').textContent = summary;
  var camp = getCampType();
  var guideUrl = 'https://cecenglishcamp.github.io/cec_guide.html'
    + '?camp=' + camp
    + '&url=' + encodeURIComponent(window.location.href)
    + '&summary=' + encodeURIComponent(summary);
  window.location.href = guideUrl;
}

window.addEventListener('load', function() {
  var el = document.getElementById('promptText');
  if (el) el.textContent = buildSummary();
});
"""


def process_camp_a_and_mom(filepath):
    """Add prompt box to camp-a / mom-teacher files that already have ChatGPT button."""
    if should_exclude(filepath):
        return False

    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    if 'launchChatGPTPractice' not in content:
        return False
    if 'prompt-box' in content:
        return False  # already has it

    original = content

    # 1. Add CSS before </style>
    idx = content.rfind('</style>')
    if idx != -1:
        content = content[:idx] + PROMPT_CSS + content[idx:]

    # 2. Add prompt box HTML inside .chatgpt-practice-wrap, before the button
    content = content.replace(
        '<button class="chatgpt-launch-btn" onclick="launchChatGPTPractice()">',
        PROMPT_HTML + '\n    <button class="chatgpt-launch-btn" onclick="launchChatGPTPractice()">'
    )

    # 3. Replace the old launchChatGPTPractice function and related code
    # Remove old function block
    content = re.sub(
        r'function launchChatGPTPractice\(\)\{.*?\n\}',
        '', content, flags=re.DOTALL
    )
    # Also try multi-line version
    content = re.sub(
        r'function launchChatGPTPractice\(\)\s*\{[^}]*(?:\{[^}]*\}[^}]*)*\}',
        '', content, flags=re.DOTALL
    )

    # Remove old inline summary builders if present
    content = re.sub(
        r'function launchChatGPTPractice\(\).*?window\.location\.href\s*=\s*guideUrl;\s*\}',
        '', content, flags=re.DOTALL
    )

    # Insert new JS before </script> (the last one)
    last_script_close = content.rfind('</script>')
    if last_script_close != -1:
        content = content[:last_script_close] + NEW_JS + '\n' + content[last_script_close:]

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def process_camp_c(filepath):
    """Remove old ChatGPT buttons and add prompt box for camp-c files."""
    if should_exclude(filepath):
        return False

    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    if 'launchChatGPTPractice' not in content:
        return False
    if 'prompt-box' in content:
        return False

    original = content

    # 1. Remove old specific camp-c sections
    # "오늘 공부 완료!" sections
    content = re.sub(
        r'<div[^>]*>[^<]*오늘 공부 완료![^<]*</div>',
        '', content, flags=re.DOTALL
    )

    # "ChatGPT 선생님과 대화하기" buttons
    content = re.sub(
        r'<button[^>]*>[^<]*ChatGPT 선생님과 대화하기[^<]*</button>',
        '', content, flags=re.DOTALL
    )

    # "클릭하면 학습 내용이 복사되고" text
    content = re.sub(
        r'<[^>]*>[^<]*클릭하면 학습 내용이 복사되고[^<]*</[^>]*>',
        '', content, flags=re.DOTALL
    )

    # 2. Add CSS before </style>
    idx = content.rfind('</style>')
    if idx != -1:
        content = content[:idx] + PROMPT_CSS + content[idx:]

    # 3. Add prompt box before the chatgpt-launch-btn
    content = content.replace(
        '<button class="chatgpt-launch-btn" onclick="launchChatGPTPractice()">',
        PROMPT_HTML + '\n    <button class="chatgpt-launch-btn" onclick="launchChatGPTPractice()">'
    )

    # 4. Replace JS
    content = re.sub(
        r'function launchChatGPTPractice\(\)\{.*?\n\}',
        '', content, flags=re.DOTALL
    )
    content = re.sub(
        r'function launchChatGPTPractice\(\).*?window\.location\.href\s*=\s*guideUrl;\s*\}',
        '', content, flags=re.DOTALL
    )

    last_script_close = content.rfind('</script>')
    if last_script_close != -1:
        content = content[:last_script_close] + NEW_JS + '\n' + content[last_script_close:]

    content = re.sub(r'\n{3,}', '\n\n', content)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


# ── Main ──
base = r'C:\Users\cecsu\cecenglishcamp.github.io'

# STEP 2: Camp A
print("=== CAMP A ===")
count = 0
for f in sorted(glob.glob(os.path.join(base, 'camp-a', 'lessons', '**', '*.html'), recursive=True)):
    if process_camp_a_and_mom(f):
        count += 1
print(f"  Modified: {count} files")

# STEP 3: Camp C
print("\n=== CAMP C ===")
count = 0
for f in sorted(glob.glob(os.path.join(base, 'camp-c', '**', '*.html'), recursive=True)):
    if process_camp_c(f):
        count += 1
print(f"  Modified: {count} files")

# STEP 4: Mom Teacher
print("\n=== MOM TEACHER ===")
count = 0
for f in sorted(glob.glob(os.path.join(base, 'mom-teacher', '**', '*.html'), recursive=True)):
    if process_camp_a_and_mom(f):
        count += 1
print(f"  Modified: {count} files")
