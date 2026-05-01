/* CEC English Camp · 콘텐츠 페이지 로그인 게이트
 * 사용:
 *   <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
 *   <script src="/assets/require-auth.js?v=3"></script>
 *
 * 통과 조건:
 *   - 무료체험 쿠키(cec_trial) 보유 시 → week01a/b/c (또는 week 패턴 없는 인덱스) 만 허용,
 *     week02 이상은 /free-trial/?locked=true 로 리다이렉트
 *   - 쿠키 없으면 Supabase 세션 확인, 미로그인 시 /login.html?next=현재경로 로 리다이렉트
 */
(function () {
  if (!window.supabase) { console.error('[require-auth] supabase-js 미로드'); return; }

  function getCookie(name) {
    var match = document.cookie.match(new RegExp('(?:^|;\\s*)' + name + '=([^;]+)'));
    return match ? match[1] : null;
  }

  var trialToken = getCookie('cec_trial');

  if (trialToken) {
    // 무료체험 쿠키 있음 → 1주차만 허용
    var path = location.pathname;
    var weekMatch = path.match(/week(\d+)/);
    if (weekMatch) {
      var weekNum = parseInt(weekMatch[1], 10);
      if (weekNum > 1) {
        window.location.replace('/free-trial/?locked=true');
        return;
      }
    }
    // 1주차 또는 인덱스 페이지 → 통과
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
