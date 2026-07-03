/* CEC English Camp · Admin 계정 통과 공통 판정
 * 로그인된 사용자의 이메일이 Admin 이메일과 일치할 때만 true를 반환한다.
 * - 비로그인 사용자는 항상 false (URL 파라미터, 하드코딩 우회 없음)
 * - localStorage만 동기적으로 읽으므로 네트워크 요청 없이 즉시 사용 가능
 *   (trial-dashboard.html 등 "깜빡임 방지용" 동기 게이트 스크립트에서 그대로 사용)
 *
 * 사용:
 *   <script src="/assets/cec-admin-check.js"></script>   ← guard 스크립트보다 먼저 로드
 *   if (window.CEC_AUTH.isCecAdminUser()) return;         // guard 안에서 맨 먼저 확인
 */
(function () {
  'use strict';

  var CEC_ADMIN_EMAILS = ['cecenglishcamp@gmail.com'];

  function normalizeEmail(email) {
    return String(email || '').trim().toLowerCase();
  }

  function isCecAdminEmail(email) {
    return CEC_ADMIN_EMAILS.indexOf(normalizeEmail(email)) !== -1;
  }

  // 현재 로그인된 사용자의 이메일을 동기적으로 찾는다.
  // 1) 메인 사이트 로그인(Supabase Auth) 세션 — supabase-js v2가 기본으로 localStorage에
  //    'sb-<project-ref>-auth-token' 키로 저장하는 세션 JSON을 직접 읽는다.
  // 2) Mom Teacher 무료체험 로그인(cec_mom_trial_session) 세션
  function getLoggedInEmailSync() {
    try {
      for (var i = 0; i < localStorage.length; i++) {
        var key = localStorage.key(i);
        if (key && /^sb-.*-auth-token$/.test(key)) {
          var raw = localStorage.getItem(key);
          if (!raw) continue;
          var parsed = JSON.parse(raw);
          var email = parsed && parsed.user && parsed.user.email;
          if (email) return email;
        }
      }
    } catch (e) { /* 세션 파싱 실패 → admin 아님으로 취급 */ }

    try {
      var s = localStorage.getItem('cec_mom_trial_session');
      if (s) {
        var d = JSON.parse(s);
        if (d && d.email) return d.email;
      }
    } catch (e) { /* 세션 파싱 실패 → admin 아님으로 취급 */ }

    return null;
  }

  function isCecAdminUser() {
    return isCecAdminEmail(getLoggedInEmailSync());
  }

  window.CEC_AUTH = window.CEC_AUTH || {};
  window.CEC_AUTH.ADMIN_EMAILS = CEC_ADMIN_EMAILS;
  window.CEC_AUTH.normalizeEmail = normalizeEmail;
  window.CEC_AUTH.isCecAdminEmail = isCecAdminEmail;
  window.CEC_AUTH.isCecAdminUser = isCecAdminUser;
})();
