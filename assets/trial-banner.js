/* CEC English Camp · 무료체험 사용자 환영 배너
 * cec_trial 쿠키 보유 + 비로그인 상태일 때만 상단 고정 배너 표시
 * (이름 + 남은 일수)
 *
 * 사용:
 *   <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
 *   <script src="/assets/trial-banner.js?v=2"></script>
 *
 * 우선순위:
 *   - 쿠키 없음 → 즉시 종료
 *   - Supabase 로그인 세션 있음 → 배너 숨김 (회원/관리자에게는 안내 불필요)
 *   - 쿠키 있고 세션 없음 → 배너 표시
 */
(function() {
  function getCookie(name) {
    var match = document.cookie.match(new RegExp('(?:^|;\\s*)' + name + '=([^;]+)'));
    return match ? decodeURIComponent(match[1]) : null;
  }

  var trial = getCookie('cec_trial');
  if (!trial) return;

  function showBanner() {
    var name = getCookie('cec_trial_name') || '';
    var expires = getCookie('cec_trial_expires');
    var daysLeft = 7;
    if (expires) {
      var diff = new Date(expires) - new Date();
      daysLeft = Math.max(0, Math.ceil(diff / (1000 * 60 * 60 * 24)));
    }

    var banner = document.createElement('div');
    banner.id = 'cec-trial-banner';
    banner.style.cssText = [
      'position:fixed', 'top:0', 'left:0', 'right:0', 'z-index:99999',
      'background:#c9a84c', 'color:#0a1628',
      'display:flex', 'align-items:center', 'justify-content:center',
      'gap:16px', 'padding:8px 20px',
      'font-size:13px', 'font-weight:600',
      'box-shadow:0 2px 8px rgba(0,0,0,0.2)'
    ].join(';');

    var nameText = name ? name + '님, ' : '';
    banner.innerHTML =
      '🎉 ' + nameText + '무료체험 중 · <span style="color:#0a1628;font-weight:700">' + daysLeft + '일 남았습니다</span>' +
      ' &nbsp;|&nbsp; ' +
      '<a href="/free-trial/" style="color:#0a1628;text-decoration:underline;font-weight:700">플랜 보기 →</a>' +
      '<span onclick="this.parentElement.remove()" style="margin-left:16px;cursor:pointer;opacity:0.6">✕</span>';

    document.body.insertBefore(banner, document.body.firstChild);
    document.body.style.paddingTop = '40px';
  }

  // Supabase 로드되어 있으면 세션 확인 후 분기, 아니면 그냥 표시
  if (window.supabase) {
    var SUPABASE_URL = 'https://rzlqlokqplhyntuirsmd.supabase.co';
    var SUPABASE_KEY = 'sb_publishable_A4HJDb41-YeAMIaRnB8KeQ_ssECgA6q';
    var sb = window.supabase.createClient(SUPABASE_URL, SUPABASE_KEY);
    sb.auth.getSession().then(function (result) {
      var session = result && result.data && result.data.session;
      if (!session) showBanner();
    }).catch(function () {
      showBanner();
    });
  } else {
    showBanner();
  }
})();
