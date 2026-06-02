/* CEC English Camp · visitor-track
 * 페이지 방문 기록을 Supabase visit_logs 테이블에 적재.
 * 사용: <script src="/assets/visitor-track.js?v=1" defer></script>
 * supabase-js 불필요 — REST 엔드포인트로 직접 INSERT.
 */
(function () {
  'use strict';

  var URL = 'https://rzlqlokqplhyntuirsmd.supabase.co';
  var KEY = 'sb_publishable_A4HJDb41-YeAMIaRnB8KeQ_ssECgA6q';

  function track() {
    try {
      var payload = {
        type: 'pageview',
        url: window.location.href,
        referrer: document.referrer || null,
        user_agent: navigator.userAgent || null
      };

      fetch(URL + '/rest/v1/visit_logs', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'apikey': KEY,
          'Authorization': 'Bearer ' + KEY,
          'Prefer': 'return=minimal'
        },
        body: JSON.stringify(payload),
        keepalive: true
      }).catch(function () { /* 네트워크 오류 무시 — 사용자 영향 없음 */ });
    } catch (e) {
      /* 어떤 오류도 페이지 동작에 영향 주지 않음 */
    }
  }

  // 페이지 로드 시 자동 실행
  if (document.readyState === 'complete' || document.readyState === 'interactive') {
    track();
  } else {
    window.addEventListener('DOMContentLoaded', track, { once: true });
  }
})();
