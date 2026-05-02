/* CEC English Camp · auth-nav (v3 simple)
 * <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
 * <script src="/assets/auth-nav.js?v=4"></script>
 */
(function () {
  'use strict';

  var URL = 'https://rzlqlokqplhyntuirsmd.supabase.co';
  var KEY = 'sb_publishable_A4HJDb41-YeAMIaRnB8KeQ_ssECgA6q';

  // ── CSS 주입 ──
  var css = document.createElement('style');
  css.textContent =
    '.cec-user{position:relative;margin-left:10px;font-family:inherit}' +
    '.cec-user-btn{background:rgba(0,188,212,.12);border:1px solid #00bcd4;color:#00bcd4;' +
      'font-size:.9rem;font-weight:700;padding:8px 14px 8px 12px;border-radius:50px;cursor:pointer;' +
      'display:flex;align-items:center;gap:7px;font-family:inherit;line-height:1;' +
      'transition:background .2s,transform .15s}' +
    '.cec-user-btn:hover{background:rgba(0,188,212,.22);transform:translateY(-1px)}' +
    '.cec-user-name{max-width:120px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}' +
    '.cec-user-arrow{font-size:.7rem;opacity:.75}' +
    '.cec-user-menu{display:none;position:absolute;top:calc(100% + 8px);right:0;' +
      'background:#080808;border:1px solid rgba(0,188,212,.3);border-radius:10px;' +
      'min-width:140px;overflow:hidden;box-shadow:0 16px 48px rgba(0,0,0,.7);z-index:99999}' +
    '.cec-user.open .cec-user-menu{display:block}' +
    '.cec-user-menu a{display:block;padding:11px 18px;color:#00bcd4;text-decoration:none;' +
      'font-size:.9rem;font-weight:600;font-family:inherit}' +
    '.cec-user-menu a:hover{background:rgba(0,188,212,.1);color:#4dd0e1}';
  document.head.appendChild(css);

  function start() {
    if (!window.supabase) { console.error('[auth-nav] supabase-js 미로드'); return; }
    var sb = window.supabase.createClient(URL, KEY);

    var nav = document.querySelector('nav');
    var reg = document.querySelector('.nav-register');
    if (!nav) return;

    // 위젯 생성 — nav 맨 끝
    var widget = document.createElement('div');
    widget.className = 'cec-user';
    widget.style.display = 'none';
    widget.innerHTML =
      '<button type="button" class="cec-user-btn">' +
        '<span>👤</span>' +
        '<span class="cec-user-name">사용자</span>' +
        '<span class="cec-user-arrow">▾</span>' +
      '</button>' +
      '<div class="cec-user-menu">' +
        '<a href="#" class="cec-logout">로그아웃</a>' +
      '</div>';
    nav.appendChild(widget);

    function render(session) {
      if (session && session.user) {
        var u = session.user;
        var name = (u.user_metadata && (u.user_metadata.name || u.user_metadata.full_name))
                || (u.email ? u.email.split('@')[0] : '사용자');
        widget.querySelector('.cec-user-name').textContent = name;
        widget.style.display = 'inline-block';
        if (reg) reg.style.display = 'none';
      } else {
        widget.style.display = 'none';
        if (reg) reg.style.display = '';
      }
    }

    // 초기 세션
    sb.auth.getSession().then(function (r) { render(r.data ? r.data.session : null); });

    // 변경 이벤트
    sb.auth.onAuthStateChange(function (_e, session) { render(session); });

    // 드롭다운 토글
    widget.querySelector('.cec-user-btn').addEventListener('click', function (e) {
      e.preventDefault(); e.stopPropagation();
      widget.classList.toggle('open');
    });
    document.addEventListener('click', function (e) {
      if (!widget.contains(e.target)) widget.classList.remove('open');
    });

    // 로그아웃 — Supabase 세션 + 무료체험 쿠키 동시 정리
    widget.querySelector('.cec-logout').addEventListener('click', async function (e) {
      e.preventDefault();
      await sb.auth.signOut();
      document.cookie = 'cec_trial=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/';
      document.cookie = 'cec_trial_name=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/';
      document.cookie = 'cec_trial_expires=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/';
      location.href = '/';
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start);
  } else {
    start();
  }
})();
