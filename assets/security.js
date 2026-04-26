/* CEC English Camp · 사이트 보안/저작권 모듈
 * 사용: <script src="/assets/security.js"></script>
 *
 * 1) 우클릭 방지 (마우스 컨텍스트 메뉴)
 * 2) 텍스트 선택 방지 (form 입력 요소는 예외)
 * 3) 키보드 단축키 차단 (Ctrl+C/S/P/U, F12)
 * 4) 워터마크 (우측 하단 고정)
 * 5) 저작권 푸터 (페이지 하단)
 *
 * ⚠️ 클라이언트 사이드 보호 — dev tools/view-source 등으로 우회 가능. UX 마찰 목적.
 */
(function () {
  'use strict';

  // ── 1) 우클릭 방지 ────────────────────────────────────
  document.addEventListener('contextmenu', function (e) { e.preventDefault(); });

  // ── 2) 텍스트 선택 방지 (input/textarea/contenteditable는 예외) ──
  function disableSelect() {
    if (!document.body) return;
    var st = document.body.style;
    st.userSelect = 'none';
    st.webkitUserSelect = 'none';
    st.MozUserSelect = 'none';
    st.msUserSelect = 'none';
    if (!document.getElementById('cec-sec-select-css')) {
      var css = document.createElement('style');
      css.id = 'cec-sec-select-css';
      css.textContent =
        'input,textarea,select,[contenteditable="true"]{' +
          '-webkit-user-select:text!important;-moz-user-select:text!important;' +
          '-ms-user-select:text!important;user-select:text!important' +
        '}';
      document.head.appendChild(css);
    }
  }

  // ── 3) 키보드 단축키 차단 ────────────────────────────
  document.addEventListener('keydown', function (e) {
    if (e.key === 'F12') { e.preventDefault(); return; }
    var k = (e.key || '').toLowerCase();
    if ((e.ctrlKey || e.metaKey) && (k === 'c' || k === 's' || k === 'p' || k === 'u')) {
      // form input에 포커스 중이면 ctrl+c는 허용 (사용자 자기 입력 복사)
      if (k === 'c') {
        var el = document.activeElement;
        if (el && (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA' || el.isContentEditable)) return;
      }
      e.preventDefault();
    }
  });

  // ── 4) 워터마크 + 5) 저작권 푸터 ─────────────────────
  function injectChrome() {
    if (!document.body) return;

    // 워터마크
    if (!document.getElementById('cec-watermark')) {
      var wm = document.createElement('div');
      wm.id = 'cec-watermark';
      wm.textContent = '© CEC English Camp';
      wm.style.cssText =
        'position:fixed;bottom:14px;right:18px;z-index:99998;pointer-events:none;' +
        'background:rgba(0,0,0,.55);color:rgba(255,255,255,.72);' +
        'font-size:.7rem;letter-spacing:.5px;font-family:system-ui,sans-serif;' +
        'padding:5px 11px;border-radius:6px;' +
        'backdrop-filter:blur(4px);-webkit-backdrop-filter:blur(4px);' +
        'border:1px solid rgba(255,255,255,.08);' +
        'user-select:none;-webkit-user-select:none';
      document.body.appendChild(wm);
    }

    // 저작권 푸터
    if (!document.getElementById('cec-copyright-footer')) {
      var ft = document.createElement('div');
      ft.id = 'cec-copyright-footer';
      ft.textContent = '© 2026 CEC English Camp. All rights reserved. 무단복제 금지.';
      ft.style.cssText =
        'text-align:center;padding:18px 16px 22px;margin-top:30px;' +
        'font-size:.72rem;color:rgba(150,150,150,.6);' +
        'font-family:system-ui,sans-serif;letter-spacing:.3px;' +
        'border-top:1px solid rgba(255,255,255,.06);' +
        'background:rgba(0,0,0,.25);' +
        'user-select:none;-webkit-user-select:none';
      document.body.appendChild(ft);
    }
  }

  function init() {
    disableSelect();
    injectChrome();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
