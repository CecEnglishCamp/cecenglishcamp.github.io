/* CEC English Camp · 공용 nav 인증 위젯
 * 사용 (둘 다 defer 없이 같은 순서로):
 *   <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
 *   <script src="/assets/auth-nav.js"></script>
 *
 * 로그인 안 됨 → .nav-register Register 버튼 그대로
 * 로그인 됨   → Register 숨기고 👤 [이름] ▾ 드롭다운 (내 정보 / 로그아웃)
 *
 * 디버그: window.__cecAuth.debug() — 현재 세션/위젯 상태 콘솔 출력
 */
(function () {
  'use strict';

  var SUPABASE_URL = 'https://rzlqlokqplhyntuirsmd.supabase.co';
  var SUPABASE_KEY = 'sb_publishable_A4HJDb41-YeAMIaRnB8KeQ_ssECgA6q';
  var TAG = '[auth-nav]';

  // supabase-js가 늦게 로드될 가능성 대비 — 최대 5초 retry
  function whenSupabaseReady(cb, retries) {
    if (window.supabase && window.supabase.createClient) return cb();
    if (retries === undefined) retries = 50;   // 50 × 100ms = 5s
    if (retries <= 0) {
      console.error(TAG, 'supabase-js 로드 실패 — CDN 차단/네트워크 확인. <script src="…@supabase/supabase-js@2"> 가 이 스크립트 앞에 있는지 확인.');
      return;
    }
    setTimeout(function () { whenSupabaseReady(cb, retries - 1); }, 100);
  }

  var sb;
  var widget;

  function init() {
    sb = window.supabase.createClient(SUPABASE_URL, SUPABASE_KEY, {
      auth: { persistSession: true, autoRefreshToken: true, detectSessionInUrl: true }
    });
    window.__cecSb = sb;

    injectStyles();
    widget = injectMarkup();
    if (!widget) {
      console.warn(TAG, '위젯 주입 실패 (host element 없음)');
      return;
    }

    sb.auth.getSession().then(function (r) {
      var s = r && r.data ? r.data.session : null;
      console.log(TAG, 'getSession:', s ? '✓ logged in (' + (s.user.email || s.user.id) + ')' : '✗ no session');
      refresh(s);
    }).catch(function (err) {
      console.error(TAG, 'getSession error:', err);
      refresh(null);
    });

    sb.auth.onAuthStateChange(function (event, session) {
      console.log(TAG, 'auth event:', event, session ? 'has session' : 'null');
      refresh(session);
    });

    bindWidgetEvents();
    window.__cecAuth = {
      sb: sb,
      widget: widget,
      debug: function () {
        sb.auth.getSession().then(function (r) {
          console.log(TAG, '=== DEBUG ===');
          console.log('  session :', r.data.session);
          console.log('  user    :', r.data.session ? r.data.session.user : null);
          console.log('  widget  :', widget);
          console.log('  display :', widget.style.display || '(default)');
          console.log('  reg btn :', document.querySelector('.nav-register'));
          console.log('  storage :', Object.keys(localStorage).filter(function(k){return k.indexOf('supabase') >= 0 || k.indexOf('sb-') >= 0;}));
        });
      }
    };
  }

  function refresh(session) {
    if (!widget) return;
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
    if (document.getElementById('navUserWidget')) return document.getElementById('navUserWidget');
    var reg = document.querySelector('.nav-register');
    var host = reg ? reg.parentNode : null;
    if (!host) {
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
    if (reg) host.insertBefore(w, reg);
    else { w.style.cssText = 'position:fixed;top:14px;right:18px;z-index:1100'; host.appendChild(w); }
    return w;
  }

  function bindWidgetEvents() {
    widget.querySelector('.nav-user-btn').addEventListener('click', function (e) {
      e.preventDefault(); e.stopPropagation();
      widget.classList.toggle('open');
    });
    document.addEventListener('click', function (e) {
      if (!widget.contains(e.target)) widget.classList.remove('open');
    });
    widget.querySelector('[data-action="signout"]').addEventListener('click', async function (e) {
      e.preventDefault();
      try { await sb.auth.signOut(); } catch (err) { console.error(TAG, 'signOut error:', err); }
      location.href = '/';
    });
  }

  function bootstrap() { whenSupabaseReady(init); }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', bootstrap);
  } else {
    bootstrap();
  }
})();
