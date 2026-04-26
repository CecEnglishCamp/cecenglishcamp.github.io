/* CEC English Camp · 공용 nav 인증 위젯 (v2 — 단순/강제 표시)
 * 사용:
 *   <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
 *   <script src="/assets/auth-nav.js?v=2"></script>
 */
(function () {
  'use strict';

  var URL = 'https://rzlqlokqplhyntuirsmd.supabase.co';
  var KEY = 'sb_publishable_A4HJDb41-YeAMIaRnB8KeQ_ssECgA6q';
  var TAG = '[auth-nav v2]';

  // ── inline style strings (CSS rule보다 우선, !important로 다른 규칙 차단) ──
  var STYLE_HIDDEN  = 'display:none !important';
  var STYLE_VISIBLE = 'position:relative;display:inline-flex !important;align-items:center;font-family:inherit;margin-left:8px';

  function ready(fn) {
    if (document.readyState !== 'loading') fn();
    else document.addEventListener('DOMContentLoaded', fn);
  }

  function waitForSupabase(cb, n) {
    if (window.supabase && window.supabase.createClient) return cb();
    n = (n || 0) + 1;
    if (n > 60) { console.error(TAG, 'supabase-js 로드 실패'); return; }
    setTimeout(function () { waitForSupabase(cb, n); }, 100);
  }

  function createWidget() {
    var existing = document.getElementById('cec-user-widget');
    if (existing) return existing;

    var w = document.createElement('div');
    w.id = 'cec-user-widget';
    w.setAttribute('style', STYLE_HIDDEN);   // 시작은 숨김
    w.innerHTML =
      '<button type="button" class="cec-btn" aria-label="사용자 메뉴" ' +
        'style="background:rgba(0,188,212,.12);border:1px solid #00bcd4;color:#00bcd4;' +
        'font-size:.9rem;font-weight:700;padding:8px 16px 8px 12px;border-radius:50px;cursor:pointer;' +
        'display:flex;align-items:center;gap:7px;font-family:inherit;line-height:1;' +
        'transition:background .2s">' +
        '<span style="font-size:1.05rem">👤</span>' +
        '<span class="cec-name" style="max-width:120px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">사용자</span>' +
        '<span style="font-size:.7rem;opacity:.75">▾</span>' +
      '</button>' +
      '<div class="cec-menu" ' +
        'style="display:none;position:absolute;top:calc(100% + 8px);right:0;background:#080808;' +
        'border:1px solid rgba(0,188,212,.3);border-radius:10px;min-width:170px;overflow:hidden;' +
        'box-shadow:0 16px 48px rgba(0,0,0,.7);z-index:99999">' +
        '<a href="/profile.html" ' +
          'style="display:block;padding:11px 18px;color:#00bcd4;text-decoration:none;' +
          'font-size:.9rem;font-weight:500;font-family:inherit">내 정보</a>' +
        '<a href="#" class="cec-logout" ' +
          'style="display:block;padding:11px 18px;color:#00bcd4;text-decoration:none;' +
          'font-size:.9rem;font-weight:500;font-family:inherit;border-top:1px solid rgba(0,188,212,.1)">' +
          '로그아웃</a>' +
      '</div>';

    // 삽입 위치: nav-register 앞 → 없으면 nav 끝
    var reg = document.querySelector('.nav-register');
    if (reg && reg.parentNode) {
      reg.parentNode.insertBefore(w, reg);
    } else {
      var nav = document.querySelector('nav, header.topbar, header.site-header');
      if (nav) nav.appendChild(w);
      else { w.setAttribute('style', STYLE_HIDDEN + ';position:fixed;top:14px;right:18px;z-index:1100'); document.body.appendChild(w); }
    }
    return w;
  }

  ready(function () {
    waitForSupabase(function () {
      var sb = window.supabase.createClient(URL, KEY, {
        auth: { persistSession: true, autoRefreshToken: true, detectSessionInUrl: true }
      });
      window.__cecSb = sb;

      var widget = createWidget();
      var btn = widget.querySelector('.cec-btn');
      var menu = widget.querySelector('.cec-menu');
      var nameEl = widget.querySelector('.cec-name');
      var logoutEl = widget.querySelector('.cec-logout');

      function show(name) {
        nameEl.textContent = name || '사용자';
        widget.setAttribute('style', STYLE_VISIBLE);
        var reg = document.querySelector('.nav-register');
        if (reg) reg.setAttribute('style', STYLE_HIDDEN);
        console.log(TAG, 'SHOW widget for:', name);
      }
      function hide() {
        widget.setAttribute('style', STYLE_HIDDEN);
        var reg = document.querySelector('.nav-register');
        if (reg) reg.removeAttribute('style');
        console.log(TAG, 'HIDE widget (logged out)');
      }

      function apply(session) {
        if (session && session.user) {
          var u = session.user;
          var name =
            (u.user_metadata && (u.user_metadata.name || u.user_metadata.full_name)) ||
            (u.email ? u.email.split('@')[0] : '사용자');
          show(name);
        } else {
          hide();
        }
      }

      // 초기 세션 + 변경 이벤트
      sb.auth.getSession().then(function (r) {
        var s = r && r.data ? r.data.session : null;
        console.log(TAG, 'getSession:', s ? '✓ ' + s.user.email : '✗ null');
        apply(s);
      }).catch(function (e) { console.error(TAG, 'getSession error:', e); apply(null); });

      sb.auth.onAuthStateChange(function (event, session) {
        console.log(TAG, 'onAuthStateChange:', event);
        apply(session);
      });

      // 드롭다운 토글
      btn.addEventListener('click', function (e) {
        e.preventDefault(); e.stopPropagation();
        var open = menu.style.display === 'block';
        menu.style.display = open ? 'none' : 'block';
      });
      document.addEventListener('click', function (e) {
        if (!widget.contains(e.target)) menu.style.display = 'none';
      });

      // 로그아웃
      logoutEl.addEventListener('click', async function (e) {
        e.preventDefault();
        console.log(TAG, 'signing out…');
        try { await sb.auth.signOut(); } catch (err) { console.error(TAG, 'signOut error:', err); }
        location.href = '/';
      });

      // 콘솔 디버그 헬퍼
      window.__cecAuth = {
        sb: sb, widget: widget,
        debug: function () {
          sb.auth.getSession().then(function (r) {
            console.log(TAG, '=== DEBUG ===');
            console.log('  session:', r.data.session);
            console.log('  user   :', r.data.session ? r.data.session.user : null);
            console.log('  widget style:', widget.getAttribute('style'));
            console.log('  reg btn:', document.querySelector('.nav-register'));
            console.log('  storage:', Object.keys(localStorage).filter(function(k){return k.indexOf('sb-')===0;}));
          });
        }
      };
    });
  });
})();
