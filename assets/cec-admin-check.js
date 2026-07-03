/* CEC English Camp · Admin 계정 통과 공통 판정
 * 로그인된 사용자의 이메일이 Admin 이메일과 일치할 때만 true를 반환한다.
 * - 비로그인 사용자는 항상 false (URL 파라미터, 하드코딩 우회 없음)
 * - localStorage/sessionStorage 전체를 스캔하여 Supabase Auth 토큰을 찾는다.
 * - Admin 발견 시 cec_mom_trial_session을 자동 생성하여 Mom Teacher guard도 통과시킨다.
 *
 * 사용:
 *   <script src="/assets/cec-admin-check.js"></script>   ← guard 스크립트보다 먼저 로드
 *   if (window.CEC_AUTH.isCecAdminUser()) return;         // guard 안에서 맨 먼저 확인
 *   if (window.CEC_AUTH.ensureAdminTrialSession()) return; // Mom Teacher guard bridge
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

  // localStorage / sessionStorage 전체를 스캔하여 Supabase Auth 토큰 및
  // 모든 JSON에서 이메일을 찾는다.
  function deepScanEmail(storage) {
    try {
      for (var i = 0; i < storage.length; i++) {
        var key = storage.key(i);
        if (!key) continue;
        var raw = storage.getItem(key);
        if (!raw) continue;

        // Supabase Auth token 키 (sb-<project-ref>-auth-token)
        if (/^sb-.*-auth-token$/.test(key)) {
          try {
            var parsed = JSON.parse(raw);
            // supabase-js v2: {user:{email:...}}
            if (parsed && parsed.user && parsed.user.email) return parsed.user.email;
            // 다른 구조 탐색
            if (parsed && parsed.currentSession && parsed.currentSession.user && parsed.currentSession.user.email) return parsed.currentSession.user.email;
            if (parsed && parsed.session && parsed.session.user && parsed.session.user.email) return parsed.session.user.email;
            // 깊이 무관 email 탐색
            var found = findEmailDeep(parsed);
            if (found) return found;
          } catch (e) {}
        }

        // 모든 JSON 문자열에서 이메일 직접 탐색 (key 상관없이)
        try {
          if (raw.indexOf('cecenglishcamp@gmail.com') !== -1) {
            var parsed = JSON.parse(raw);
            var found = findEmailDeep(parsed);
            if (found) return found;
          }
        } catch (e) {}
      }
    } catch (e) {}
    return null;
  }

  // JSON 객체를 깊이 탐색하여 이메일 문자열 찾기
  function findEmailDeep(obj) {
    if (!obj || typeof obj !== 'object') return null;
    if (obj.email) return obj.email;
    if (obj.currentSession && obj.currentSession.user) {
      if (obj.currentSession.user.email) return obj.currentSession.user.email;
    }
    if (obj.session && obj.session.user) {
      if (obj.session.user.email) return obj.session.user.email;
    }
    if (obj.user && obj.user.email) return obj.user.email;
    // identities 배열 확인
    if (obj.identities && Array.isArray(obj.identities) && obj.identities[0]) {
      if (obj.identities[0].email) return obj.identities[0].email;
    }
    return null;
  }

  // 현재 로그인된 사용자의 이메일을 동기적으로 찾는다.
  function getLoggedInEmailSync() {
    // 1) localStorage 전체 스캔
    var email = deepScanEmail(localStorage);
    if (email) return email;

    // 2) sessionStorage 전체 스캔
    email = deepScanEmail(sessionStorage);
    if (email) return email;

    // 3) 기존 Mom Teacher trial session 확인
    try {
      var s = localStorage.getItem('cec_mom_trial_session');
      if (s) {
        var d = JSON.parse(s);
        if (d && d.email) return d.email;
      }
    } catch (e) {}

    return null;
  }

  function ensureAdminTrialSession() {
    var email = getLoggedInEmailSync();
    if (!isCecAdminEmail(email)) return false;

    // 이미 Mom Teacher trial session이 있고 유효하면 그대로
    try {
      var existing = localStorage.getItem('cec_mom_trial_session');
      if (existing) {
        var d = JSON.parse(existing);
        if (d && d.exp && Date.now() < d.exp) return true;
      }
    } catch (e) {}

    // Admin용 trial session 생성 (30일)
    var session = {
      email: 'cecenglishcamp@gmail.com',
      name: 'CEC Admin',
      role: 'admin',
      plan: 'admin',
      admin: true,
      trial: true,
      exp: Date.now() + 30 * 24 * 60 * 60 * 1000
    };
    localStorage.setItem('cec_mom_trial_session', JSON.stringify(session));
    return true;
  }

  function isCecAdminUser() {
    var email = getLoggedInEmailSync();
    return isCecAdminEmail(email);
  }

  window.CEC_AUTH = window.CEC_AUTH || {};
  window.CEC_AUTH.ADMIN_EMAILS = CEC_ADMIN_EMAILS;
  window.CEC_AUTH.normalizeEmail = normalizeEmail;
  window.CEC_AUTH.isCecAdminEmail = isCecAdminEmail;
  window.CEC_AUTH.isCecAdminUser = isCecAdminUser;
  window.CEC_AUTH.ensureAdminTrialSession = ensureAdminTrialSession;
})();
