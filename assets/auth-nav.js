/* CEC English Camp · 공용 nav 인증 위젯
 * 사용: <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
 *       <script src="/assets/auth-nav.js" defer></script>
 *
 * 로그인 안 됨 → .nav-register Register 버튼 그대로
 * 로그인 됨   → Register 숨기고 👤 [이름] ▾ 드롭다운 표시 (내 정보 / 로그아웃)
 */
(function () {
  'use strict';

  var SUPABASE_URL = 'https://rzlqlokqplhyntuirsmd.supabase.co';
  var SUPABASE_KEY = 'sb_publishable_A4HJDb41-YeAMIaRnB8KeQ_ssECgA6q';

  function init() {
    if (!window.supabase) {
      console.warn('[auth-nav] supabase-js 미로드 — script src 순서 확인');
      return;
    }
    var sb = window.supabase.createClient(SUPABASE_URL, SUPABASE_KEY);
    window.__cecSb = sb;

    injectStyles();
    var widget = injectMarkup();
    if (!widget) return;

    function refresh(session) {
      var reg = document.querySelector('.nav-register');
      if (session && session.user) {
        var u = session.user;
        var name =
          (u.user_metadata && (u.user_metadata.name || u.user_metadata.full_name)) ||
          (u.email ? u.email.split('@')[0] : '사용자');
        widget.querySelector('.nav-user-name').textContent = name;
        widget.style.display = '';
        if (reg) reg.style.display = 'none';
      } else {
        widget.style.display = 'none';
        if (reg) reg.style.display = '';
      }
    }

    sb.auth.getSession().then(function (r) { refresh(r.data ? r.data.session : null); });
    sb.auth.onAuthStateChange(function (_event, session) { refresh(session); });

    // 드롭다운 클릭 토글 (모바일 hover 안 됨 보완)
    widget.querySelector('.nav-user-btn').addEventListener('click', function (e) {
      e.preventDefault(); e.stopPropagation();
      widget.classList.toggle('open');
    });
    document.addEventListener('click', function (e) {
      if (!widget.contains(e.target)) widget.classList.remove('open');
    });

    // 로그아웃
    widget.querySelector('[data-action="signout"]').addEventListener('click', async function (e) {
      e.preventDefault();
      await sb.auth.signOut();
      location.href = '/';
    });
  }

  function injectStyles() {
    if (document.getElementById('cec-auth-nav-styles')) return;
    var s = document.createElement('style');
    s.id = 'cec-auth-nav-styles';
    s.textContent =
      '.nav-user{position:relative;display:none;font-family:inherit}' +
      '.nav-user-btn{background:rgba(0,188,212,.10);border:1px solid rgba(0,188,212,.32);color:#00bcd4;font-size:.88rem;font-weight:700;padding:8px 14px 8px 12px;border-radius:50px;cursor:pointer;display:flex;align-items:center;gap:6px;font-family:inherit;line-height:1;transition:background .2s,border-color .2s}' +
      '.nav-user-btn:hover{background:rgba(0,188,212,.18);border-color:rgba(0,188,212,.5)}' +
      '.nav-user-avatar{font-size:1.05rem}' +
      '.nav-user-name{max-width:120px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}' +
      '.nav-user-arrow{font-size:.65rem;opacity:.7}' +
      '.nav-user-menu{display:none;position:absolute;top:calc(100% + 8px);right:0;background:#080808;border:1px solid rgba(0,188,212,.22);border-radius:10px;min-width:170px;overflow:hidden;box-shadow:0 16px 48px rgba(0,0,0,.7);z-index:1100}' +
      '.nav-user.open .nav-user-menu{display:block}' +
      '.nav-user-menu a{display:block;padding:10px 18px;color:#00bcd4;text-decoration:none;font-size:.9rem;font-weight:500;transition:background .15s,color .15s;cursor:pointer}' +
      '.nav-user-menu a:hover{background:rgba(0,188,212,.08);color:#4dd0e1}' +
      '.nav-user-menu a + a{border-top:1px solid rgba(0,188,212,.1)}' +
      '@media(max-width:900px){.nav-user-name{max-width:80px}}';
    document.head.appendChild(s);
  }

  function injectMarkup() {
    var reg = document.querySelector('.nav-register');
    var host = reg ? reg.parentNode : null;
    if (!host) {
      // nav-register가 없는 페이지(예: library/) — 우측 상단 fixed 위젯으로
      var nav = document.querySelector('nav, header.topbar, header.site-header');
      host = nav || document.body;
    }
    var w = document.createElement('div');
    w.className = 'nav-user';
    w.id = 'navUserWidget';
    w.innerHTML =
      '<button type="button" class="nav-user-btn" aria-label="사용자 메뉴">' +
        '<span class="nav-user-avatar">👤</span>' +
        '<span class="nav-user-name">사용자</span>' +
        '<span class="nav-user-arrow">▾</span>' +
      '</button>' +
      '<div class="nav-user-menu">' +
        '<a href="/profile.html">내 정보</a>' +
        '<a href="#" data-action="signout">로그아웃</a>' +
      '</div>';
    if (reg) {
      host.insertBefore(w, reg);   // Register 바로 앞
    } else {
      // fallback: 페이지 우상단 fixed
      w.style.cssText = 'position:fixed;top:14px;right:18px;z-index:1100';
      host.appendChild(w);
    }
    return w;
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
