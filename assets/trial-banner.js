/* CEC English Camp · 무료체험 사용자 환영 배너
 * cec_trial 쿠키 보유 사용자에게 상단 고정 배너 표시 (이름 + 남은 일수)
 * 사용:
 *   <script src="/assets/trial-banner.js?v=1"></script>
 */
(function() {
  function getCookie(name) {
    var match = document.cookie.match(new RegExp('(?:^|;\\s*)' + name + '=([^;]+)'));
    return match ? decodeURIComponent(match[1]) : null;
  }

  var trial = getCookie('cec_trial');
  if (!trial) return;

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

  // 배너 높이만큼 body 상단 패딩 추가
  document.body.style.paddingTop = '40px';
})();
