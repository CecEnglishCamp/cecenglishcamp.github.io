/* CEC English Camp · 캠프 링크 게이트
 * Library/Grammar 페이지(공개)에서 보호 캠프(/camp-a, /camp-b, /camp-c,
 * /essay-camp, /mom-teacher)로 향하는 링크 클릭 시 인증 확인.
 * 무료체험 쿠키(cec_trial) 또는 Supabase 세션이 있으면 통과,
 * 둘 다 없으면 /login.html?next=링크 로 이동.
 */
(function () {
  if (!window.supabase) return;

  function getCookie(name) {
    var m = document.cookie.match(new RegExp('(?:^|;\\s*)' + name + '=([^;]+)'));
    return m ? m[1] : null;
  }

  var SUPABASE_URL = 'https://rzlqlokqplhyntuirsmd.supabase.co';
  var SUPABASE_KEY = 'sb_publishable_A4HJDb41-YeAMIaRnB8KeQ_ssECgA6q';
  var sb = window.supabase.createClient(SUPABASE_URL, SUPABASE_KEY);

  var sessionPromise = sb.auth.getSession().then(function (r) {
    return !!(r && r.data && r.data.session);
  }).catch(function () { return false; });

  var GATED = /^\/(camp-a|camp-b|camp-c|essay-camp|mom-teacher)(\/|$)/;

  document.addEventListener('click', function (e) {
    var a = e.target && e.target.closest ? e.target.closest('a[href]') : null;
    if (!a) return;
    var href = a.getAttribute('href');
    if (!href || !GATED.test(href)) return;

    // 무료체험 쿠키 보유 시 즉시 통과 (week 제한은 require-auth.js가 처리)
    if (getCookie('cec_trial')) return;

    // 세션 비동기 확인
    e.preventDefault();
    sessionPromise.then(function (ok) {
      if (ok) {
        window.location.href = href;
      } else {
        window.location.href = '/login.html?next=' + encodeURIComponent(href);
      }
    });
  }, true);
})();
