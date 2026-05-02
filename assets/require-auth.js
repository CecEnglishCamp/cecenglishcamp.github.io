/* CEC English Camp · 콘텐츠 페이지 로그인 게이트
 * 사용:
 *   <script src="/assets/require-auth.js?v=6"></script>
 *   (supabase-js 미로드 시 자동 동적 로드)
 *
 * 우선순위 (v=6):
 *   1. Supabase 로그인 세션 → 무조건 통과 (회원/관리자, week/ep 제한 없음)
 *   2. 무료체험 쿠키(cec_trial) → week01a/b/c · ep01 (또는 패턴 없는 인덱스) 만 허용
 *      week02+ / ep02+ 는 /free-trial/?locked=true 로 리다이렉트
 *   3. 둘 다 없으면 → /login.html?next=현재경로 로 리다이렉트
 */
(function () {
  function getCookie(name) {
    var match = document.cookie.match(new RegExp('(?:^|;\\s*)' + name + '=([^;]+)'));
    return match ? match[1] : null;
  }

  function checkAccess() {
    var SUPABASE_URL = 'https://rzlqlokqplhyntuirsmd.supabase.co';
    var SUPABASE_KEY = 'sb_publishable_A4HJDb41-YeAMIaRnB8KeQ_ssECgA6q';
    var sb = window.supabase.createClient(SUPABASE_URL, SUPABASE_KEY);

    sb.auth.getSession().then(function(result) {
      var session = result && result.data && result.data.session;
      if (session) return; // 로그인 → 통과

      var trialToken = getCookie('cec_trial');
      if (trialToken) {
        var path = location.pathname;
        var weekMatch = path.match(/week(\d+)/);
        if (weekMatch && parseInt(weekMatch[1], 10) > 1) {
          window.location.replace('/free-trial/?locked=true');
          return;
        }
        var epMatch = path.match(/ep(\d+)/);
        if (epMatch && parseInt(epMatch[1], 10) > 1) {
          window.location.replace('/free-trial/?locked=true');
          return;
        }
        return; // week01/ep01 → 통과
      }

      var next = encodeURIComponent(location.pathname + location.search);
      window.location.replace('/login.html?next=' + next);
    });
  }

  if (window.supabase) {
    checkAccess();
  } else {
    // supabase-js 동적 로드
    var script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2';
    script.onload = function() { checkAccess(); };
    document.head.appendChild(script);
  }
})();
