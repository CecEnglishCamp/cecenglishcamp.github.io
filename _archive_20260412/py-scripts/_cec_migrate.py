#!/usr/bin/env python3
"""CEC: Replace Open WebUI with ChatGPT split-screen practice button."""
import os, re, sys, glob, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ── Snippets ──
CSS_SNIPPET = """
/* ── ChatGPT 회화 연습 버튼 ── */
.chatgpt-practice-section {
  margin: 40px auto 20px;
  max-width: 860px;
  padding: 0 20px;
}
.chatgpt-practice-wrap {
  background: linear-gradient(135deg, #050e1f, #0a1628);
  border: 2px solid rgba(0,210,255,0.4);
  border-radius: 20px;
  padding: 32px 28px;
  text-align: center;
  position: relative;
  overflow: hidden;
}
.chatgpt-practice-wrap::before {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse at 50% 0%,
    rgba(0,210,255,0.07) 0%, transparent 60%);
  pointer-events: none;
}
.chatgpt-practice-title {
  font-size: 1.2rem;
  font-weight: 700;
  color: #fff;
  margin-bottom: 8px;
}
.chatgpt-practice-desc {
  color: #6a8fad;
  font-size: 0.88rem;
  line-height: 1.7;
  margin-bottom: 24px;
}
.chatgpt-practice-desc strong { color: #00d2ff; }
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
  transition: transform 0.2s, box-shadow 0.2s;
  font-family: inherit;
}
.chatgpt-launch-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 0 50px rgba(0,210,255,0.5);
}
.chatgpt-practice-note {
  margin-top: 12px;
  font-size: 0.75rem;
  color: #3a5a7a;
}
"""

HTML_SNIPPET = """
<div class="chatgpt-practice-section">
  <div class="chatgpt-practice-wrap">
    <div class="chatgpt-practice-title">🎉 수업 완료! 이제 회화 연습!</div>
    <div class="chatgpt-practice-desc">
      오늘 배운 내용을 보면서 <strong>ChatGPT</strong>와 영어로 대화해보세요!<br>
      <strong>왼쪽</strong>엔 오늘 수업, <strong>오른쪽</strong>엔 ChatGPT가 열립니다.
    </div>
    <button class="chatgpt-launch-btn" onclick="launchChatGPTPractice()">
      🎙️ ChatGPT 회화 연습 시작
    </button>
    <div class="chatgpt-practice-note">※ 처음 한 번만 팝업 허용이 필요합니다</div>
  </div>
</div>

<script>
function getCampType() {
  var path = window.location.pathname;
  if (path.includes('camp-b') ||
      path.includes('/m1/') || path.includes('/m2/') || path.includes('/m3/') ||
      path.includes('/g1/') || path.includes('/g2/') || path.includes('/g3/')) return 'b';
  if (path.includes('camp-c') || path.includes('mom-teacher')) return 'c';
  return 'a';
}

function launchChatGPTPractice() {
  // 단어 자동 수집
  var words = [];
  document.querySelectorAll(
    '.word-en, .vocab-en, .key-word, [class*="word-en"], [class*="vocab"]'
  ).forEach(function(el) {
    var t = el.textContent.trim();
    if (t && t.length < 30) words.push(t);
  });

  // 본문 첫 문장
  var storyEl = document.querySelector(
    '.story-content.active p, .reading-text p, .story p'
  );
  var firstLine = storyEl
    ? storyEl.textContent.substring(0, 80) + '...'
    : '';

  var summary = [
    '[' + document.title + ']',
    words.length ? '배운 단어: ' + words.slice(0,8).join(', ') : '',
    firstLine ? '오늘 이야기: ' + firstLine : '',
    '위 내용으로 영어 회화 연습을 도와주세요!'
  ].filter(Boolean).join('\\n');

  var camp = getCampType();

  // cec_guide.html 경로: GitHub Pages 루트
  var depth = (window.location.pathname.match(/\\//g) || []).length - 1;
  var prefix = depth <= 1 ? '' : '../'.repeat(depth - 1);

  var guideUrl = prefix + 'cec_guide.html'
    + '?camp=' + camp
    + '&url=' + encodeURIComponent(window.location.href)
    + '&summary=' + encodeURIComponent(summary);

  window.location.href = guideUrl;
}
</script>
"""

# ── Exclusion check ──
EXCLUDE_KEYWORDS = ['grammar', 'gram', 'prestep', 'index', 'guide']

def should_exclude(filepath):
    basename = os.path.basename(filepath).lower()
    for kw in EXCLUDE_KEYWORDS:
        if kw in basename:
            return True
    return False

def already_has_button(content):
    return 'launchChatGPTPractice' in content or 'chatgpt-launch-btn' in content

# ── Open WebUI removal patterns ──
def remove_openwebui(content):
    """Remove Open WebUI buttons/links/sections from HTML content."""
    original = content

    # Remove <a> tags containing localhost:3001
    content = re.sub(
        r'<a[^>]*localhost:3001[^>]*>.*?</a>',
        '', content, flags=re.DOTALL | re.IGNORECASE
    )

    # Remove <button> tags containing localhost:3001 or Open WebUI
    content = re.sub(
        r'<button[^>]*onclick="[^"]*localhost:3001[^"]*"[^>]*>.*?</button>',
        '', content, flags=re.DOTALL | re.IGNORECASE
    )

    # Remove entire divs/sections that reference Open WebUI or localhost:3001
    # Pattern: div with class containing "webui" or "openwebui"
    content = re.sub(
        r'<div[^>]*(?:open-?webui|openwebui)[^>]*>.*?</div>',
        '', content, flags=re.DOTALL | re.IGNORECASE
    )

    # Remove script blocks that reference localhost:3001
    content = re.sub(
        r'<script>[^<]*localhost:3001[^<]*</script>',
        '', content, flags=re.DOTALL | re.IGNORECASE
    )

    # Remove inline onclick handlers with localhost:3001 (standalone links)
    content = re.sub(
        r'''<a[^>]*href=["'][^"']*localhost:3001[^"']*["'][^>]*>.*?</a>''',
        '', content, flags=re.DOTALL | re.IGNORECASE
    )

    # Remove any remaining lines with localhost:3001 that are link/button related
    lines = content.split('\n')
    cleaned = []
    skip_depth = 0
    for line in lines:
        stripped = line.strip()
        if skip_depth > 0:
            if '</div>' in stripped or '</section>' in stripped:
                skip_depth -= 1
            continue
        # Skip standalone lines referencing Open WebUI / localhost:3001
        if 'localhost:3001' in line and ('<a ' in line or '<button' in line or 'onclick' in line or 'href' in line):
            continue
        if 'Open WebUI' in line and ('<a ' in line or '<button' in line or '<div' in line):
            continue
        cleaned.append(line)
    content = '\n'.join(cleaned)

    # Clean up multiple blank lines
    content = re.sub(r'\n{3,}', '\n\n', content)

    return content

def insert_css(content, css):
    """Insert CSS before </style>."""
    # Find the last </style> tag
    idx = content.rfind('</style>')
    if idx == -1:
        return content
    return content[:idx] + css + '\n' + content[idx:]

def insert_html_js(content, html_js):
    """Insert HTML+JS before </body>."""
    idx = content.rfind('</body>')
    if idx == -1:
        return content
    return content[:idx] + html_js + '\n' + content[idx:]

def process_file(filepath, remove_webui=False):
    """Process a single HTML file. Returns: 'modified', 'skipped', or 'excluded'."""
    if should_exclude(filepath):
        return 'excluded'

    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    if already_has_button(content):
        return 'skipped'

    # Check it has </style> and </body>
    if '</style>' not in content or '</body>' not in content:
        return 'skipped'

    if remove_webui:
        content = remove_openwebui(content)

    content = insert_css(content, CSS_SNIPPET)
    content = insert_html_js(content, HTML_SNIPPET)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return 'modified'

def process_directory(directory, remove_webui=False, label=''):
    """Process all HTML files in a directory."""
    pattern = os.path.join(directory, '**', '*.html')
    files = glob.glob(pattern, recursive=True)

    results = {'modified': 0, 'skipped': 0, 'excluded': 0, 'total': len(files)}
    modified_files = []

    for f in sorted(files):
        result = process_file(f, remove_webui=remove_webui)
        results[result] += 1
        if result == 'modified':
            modified_files.append(os.path.relpath(f, directory))

    print(f"\n{'='*50}")
    print(f"{label}")
    print(f"{'='*50}")
    print(f"Total HTML files: {results['total']}")
    print(f"Modified:         {results['modified']}")
    print(f"Skipped (exists): {results['skipped']}")
    print(f"Excluded:         {results['excluded']}")
    if modified_files:
        print(f"\nModified files:")
        for mf in modified_files:
            print(f"  + {mf}")

    return results

# ── Main ──
if __name__ == '__main__':
    base = r'C:\Users\cecsu\cecenglishcamp.github.io'

    camp = sys.argv[1] if len(sys.argv) > 1 else 'all'

    if camp in ('camp-b', 'all'):
        process_directory(
            os.path.join(base, 'camp-b'),
            remove_webui=True,
            label='CAMP-B (Open WebUI 제거 + ChatGPT 추가)'
        )

    if camp in ('camp-a', 'all'):
        process_directory(
            os.path.join(base, 'camp-a', 'lessons'),
            remove_webui=False,
            label='CAMP-A (ChatGPT 추가)'
        )

    if camp in ('camp-c', 'all'):
        process_directory(
            os.path.join(base, 'camp-c'),
            remove_webui=False,
            label='CAMP-C (ChatGPT 추가)'
        )

    if camp in ('mom-teacher', 'all'):
        process_directory(
            os.path.join(base, 'mom-teacher'),
            remove_webui=False,
            label='MOM-TEACHER (ChatGPT 추가, camp=c)'
        )
