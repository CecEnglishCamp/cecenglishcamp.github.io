/* CEC English Camp · 콘텐츠 페이지 로그인 게이트
 * 사용:
 *   <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
 *   <script src="/assets/require-auth.js?v=1"></script>
 *
 * 비로그인 상태면 즉시 /login.html?next=현재경로 로 리다이렉트
 */
(function () {
  if (!window.supabase) { console.error('[require-auth] supabase-js 미로드'); return; }

  var SUPABASE_URL = 'https://rzlqlokqplhyntuirsmd.supabase.co';
  var SUPABASE_KEY = 'sb_publishable_A4HJDb41-YeAMIaRnB8KeQ_ssECgA6q';

  var sb = window.supabase.createClient(SUPABASE_URL, SUPABASE_KEY);

  sb.auth.getSession().then(function (result) {
    if (!result.data || !result.data.session) {
      var next = encodeURIComponent(location.pathname + location.search);
      window.location.replace('/login.html?next=' + next);
    }
  });
})();
