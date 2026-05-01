/* CEC English Camp · 콘텐츠 페이지 로그인 게이트
 * 사용:
 *   <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
 *   <script src="/assets/require-auth.js?v=2"></script>
 *
 * 통과 조건: Supabase 세션 OR 무료체험 쿠키(cec_trial)
 * 둘 다 없으면 /login.html?next=현재경로 로 리다이렉트
 */
(function () {
  if (!window.supabase) { console.error('[require-auth] supabase-js 미로드'); return; }

  // 무료체험 쿠키 확인
  function getTrialCookie() {
    var match = document.cookie.match(/(?:^|;\s*)cec_trial=([^;]+)/);
    return match ? match[1] : null;
  }

  var trialToken = getTrialCookie();
  if (trialToken) {
    // 쿠키 있으면 통과 (무료체험 중)
    return;
  }

  // 쿠키 없으면 Supabase 세션 확인
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
