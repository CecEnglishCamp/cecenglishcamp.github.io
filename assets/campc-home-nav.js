/* CEC Camp C · 수업 화면 'Back to Camp C Home' 버튼 (2026-11-26)
 * security.js 가 Camp C 수업 페이지(/camp-c/epNN.html)에서만 불러옴. 페이지 HTML 은 고치지 않음.
 *   - 위: 고정(sticky) 상단 띠 안에 한 줄 → 스크롤해도 늘 보임(모바일 포함)
 *   - 아래: 수업 내용 맨 끝에 큰 버튼(모바일에서는 가로 전체, 높이 48px 이상)
 *   - 기존 상단 'Camp C · 한국주부 영어교실' 글자 링크도 사이트 첫 화면(/) 대신 Camp C 첫 화면으로
 * 같은 사이트 안 일반 링크라 로그인·진도·XP 는 그대로(새로고침과 같음).
 */
(function () {
  'use strict';
  var HOME = '/camp-c/';
  var LABEL = 'Back to Camp C Home';
  if (!/^\/camp-c\/ep\d+\.html$/.test(location.pathname)) return;
  if (window.__cecCampcHomeNav) return;
  window.__cecCampcHomeNav = true;

  function css() {
    if (document.getElementById('cec-campc-home-css')) return;
    var s = document.createElement('style');
    s.id = 'cec-campc-home-css';
    s.textContent =
      '.cec-ch-top{display:flex;justify-content:flex-start;max-width:860px;margin:0 auto;padding:0 20px 8px}' +
      '.cec-ch-bar{position:sticky;top:0;z-index:100;background:#0f1f4a;padding:8px 16px}' +
      '.cec-ch-bar .cec-ch-top{padding:0}' +
      '.cec-ch-link{display:inline-flex;align-items:center;gap:6px;min-height:36px;padding:6px 14px;border-radius:999px;' +
      'background:rgba(255,255,255,0.14);border:1px solid rgba(255,255,255,0.35);color:#fff;font-weight:800;font-size:13px;' +
      'text-decoration:none;font-family:system-ui,-apple-system,"Segoe UI",sans-serif;letter-spacing:.2px;line-height:1.2}' +
      '.cec-ch-link:hover,.cec-ch-link:focus-visible{background:rgba(255,255,255,0.26);outline:2px solid #fbbf24;outline-offset:2px}' +
      '.cec-ch-bottom{display:flex;justify-content:center;margin:18px auto 28px;padding:0 16px;max-width:860px}' +
      '.cec-ch-bottom .cec-ch-link{min-height:50px;padding:12px 28px;font-size:16px;background:#1e3a8a;border-color:#1e3a8a;' +
      'box-shadow:0 4px 18px rgba(15,31,74,0.25)}' +
      '.cec-ch-bottom .cec-ch-link:hover,.cec-ch-bottom .cec-ch-link:focus-visible{background:#1d4ed8}' +
      // 휴대폰: 기존 로고 두 줄(작은 소개 글)이 58px 띠 밖으로 넘쳐 버튼과 겹침 → 이 페이지들에서만 작은 소개 글을 숨김(로고는 띠 안 두 줄)
      '@media(max-width:560px){.top-banner .logo-campc{display:none}' +
      '.cec-ch-top{padding:0 12px 8px}.cec-ch-link{font-size:14px;min-height:40px}' +
      '.cec-ch-bottom .cec-ch-link{width:100%;justify-content:center}}';
    (document.head || document.documentElement).appendChild(s);
  }

  function link(where) {
    var a = document.createElement('a');
    a.href = HOME;
    a.className = 'cec-ch-link';
    a.setAttribute('data-cec-campc-home', where);
    a.setAttribute('aria-label', LABEL);
    a.innerHTML = '<span aria-hidden="true">🏠</span><span></span>';
    a.lastChild.textContent = LABEL;
    return a;
  }

  function init() {
    if (document.querySelector('[data-cec-campc-home]')) return;
    css();
    // 위
    var top = document.createElement('div');
    top.className = 'cec-ch-top';
    top.appendChild(link('top'));
    var banner = document.querySelector('nav.top-banner');
    if (banner) {
      banner.appendChild(top);
      var mid = banner.querySelector('a.banner-mid');
      if (mid && mid.getAttribute('href') === '/') mid.setAttribute('href', HOME);
    } else {
      var bar = document.createElement('nav');
      bar.className = 'cec-ch-bar';
      bar.setAttribute('aria-label', 'Camp C');
      bar.appendChild(top);
      document.body.insertBefore(bar, document.body.firstChild);
    }
    // 아래
    var bottom = document.createElement('nav');
    bottom.className = 'cec-ch-bottom';
    bottom.setAttribute('aria-label', 'Camp C');
    bottom.appendChild(link('bottom'));
    // 수업 내용의 맨 끝(.main, ep120 은 .container) — 에피소드 이동 칸 뒤에도 '수업 완료' 칸 등이 이어지므로 맨 끝에 둠
    var box = document.querySelector('.main') || document.querySelector('.container');
    if (box) box.appendChild(bottom);
    else document.body.appendChild(bottom);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
