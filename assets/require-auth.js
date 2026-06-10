/* CEC English Camp · 콘텐츠 페이지 로그인 게이트
 * 사용:
 *   <script src="/assets/require-auth.js?v=8"></script>
 *   (supabase-js 미로드 시 자동 동적 로드)
 *
 * 우선순위 (v=8):
 *   [/space-camp/ 경로]  ← Space Camp 전용 강화 게이트
 *     1. 미로그인 → /login.html?next=현재경로
 *     2. 로그인 + (구독자(plan_type 있고 canceled_at 없음) 또는 space_camp_access=true) → 통과
 *     3. 그 외(무료 계정 등) → /space-camp-lock.html 로 이동
 *   [그 외 일반 콘텐츠]
 *     1. Supabase 로그인 세션 → 통과
 *     2. 무료체험 쿠키(cec_trial) → week01/ep01 만 허용, 이후는 /payment/
 *     3. 둘 다 없으면 → /login.html?next=현재경로
 */
(function () {
  // 항상 정식 도메인(cecenglishcamp.com)에서 동작 — 로그인 세션이 도메인별로 분리돼 생기는 로그인 루프 방지
  var _H = location.hostname;
  if (_H === 'cecenglishcamp.github.io' || _H === 'www.cecenglishcamp.com') {
    location.replace('https://cecenglishcamp.com' + location.pathname + location.search + location.hash);
    return;
  }
  function getCookie(name) {
    var match = document.cookie.match(new RegExp('(?:^|;\\s*)' + name + '=([^;]+)'));
    return match ? match[1] : null;
  }
  function gotoLogin() {
    var next = encodeURIComponent(location.pathname + location.search);
    window.location.replace('/login.html?next=' + next);
  }

  function checkAccess() {
    var SUPABASE_URL = 'https://rzlqlokqplhyntuirsmd.supabase.co';
    var SUPABASE_KEY = 'sb_publishable_A4HJDb41-YeAMIaRnB8KeQ_ssECgA6q';
    var sb = window.supabase.createClient(SUPABASE_URL, SUPABASE_KEY);
    var isSpaceCamp = location.pathname.indexOf('/space-camp/') === 0;

    // onAuthStateChange: INITIAL_SESSION은 클라이언트 생성 직후 즉시 발행
    // → localStorage 세션 있으면 session 객체 포함, 없으면 null
    // SIGNED_IN: OAuth 코드 교환 완료 후 발행 (login.html에서 처리 후 여기 도달 시 INITIAL_SESSION에 이미 세션 있음)
    var _authSub = sb.auth.onAuthStateChange(function (event, session) {
      if (event !== 'INITIAL_SESSION' && event !== 'SIGNED_IN') return;
      _authSub.data.subscription.unsubscribe(); // 한 번만 실행

      // ── 관리자 계정: 체크 없이 모든 페이지 즉시 통과 ──
      if (session && session.user && session.user.email === 'cecenglishcamp@gmail.com') {
        return;
      }

      // ── Space Camp 전용 게이트 ──
      if (isSpaceCamp) {
        if (!session) { gotoLogin(); return; }
        sb.from('households')
          .select('space_camp_access,plan_type,canceled_at')
          .eq('auth_user_id', session.user.id)
          .maybeSingle()
          .then(function (r) {
            // 설정 오류(예: space_camp_access 컬럼 미생성)로 쿼리가 실패하면
            // 로그인 사용자를 막지 않고 통과시킨다(잠금 루프 방지). SQL 적용 후 정상 판별.
            if (r && r.error) { return; }
            var h = r && r.data;
            var paidSub = h && !!h.plan_type && !h.canceled_at;       // $40 등 활성 구독자
            var hasSpaceCamp = h && h.space_camp_access === true;       // $99 Space Camp 결제자
            if (paidSub || hasSpaceCamp) return;                       // 통과
            window.location.replace('/space-camp-lock.html');          // 권한 없음
          })
          .catch(function () { window.location.replace('/space-camp-lock.html'); });
        return;
      }

      // ── 일반 콘텐츠 게이트 (기존 동작) ──
      if (session) return; // 로그인 → 통과

      var trialToken = getCookie('cec_trial');
      if (trialToken) {
        var path = location.pathname;
        var weekMatch = path.match(/week(\d+)/);
        if (weekMatch && parseInt(weekMatch[1], 10) > 1) { window.location.replace('/payment/'); return; }
        var epMatch = path.match(/ep(\d+)/);
        if (epMatch && parseInt(epMatch[1], 10) > 1) { window.location.replace('/payment/'); return; }
        return; // week01/ep01 → 통과
      }

      gotoLogin();
    });
  }

  if (window.supabase) {
    checkAccess();
  } else {
    var script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2';
    script.onload = function () { checkAccess(); };
    document.head.appendChild(script);
  }
})();
