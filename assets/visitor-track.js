// CEC English Camp — 방문자 행동 추적 v2
// 추적 항목: 페이지뷰, 체류시간, 이탈페이지, 영상재생, 수료증발급
(function () {
  var SUPA_URL = 'https://rzlqlokqplhyntuirsmd.supabase.co';
  var SUPA_KEY = 'sb_publishable_A4HJDb41-YeAMIaRnB8KeQ_ssECgA6q';
  var PAGE_START = Date.now();

  function track(type, extra) {
    try {
      var payload = Object.assign({
        type: type,
        url: location.pathname,
        referrer: document.referrer || null,
        user_agent: navigator.userAgent,
        created_at: new Date().toISOString()
      }, extra || {});
      fetch(SUPA_URL + '/rest/v1/visit_logs', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'apikey': SUPA_KEY,
          'Authorization': 'Bearer ' + SUPA_KEY,
          'Prefer': 'return=minimal'
        },
        body: JSON.stringify(payload),
        keepalive: true
      }).catch(function(){});
    } catch(e) {}
  }

  // 1. 페이지뷰
  function init() {
    track('pageview');

    // 2. 체류시간 + 이탈페이지 (페이지 떠날 때)
    window.addEventListener('beforeunload', function() {
      var seconds = Math.round((Date.now() - PAGE_START) / 1000);
      track('pageleave', { duration_seconds: seconds });
    });

    // 3. 영상 재생 감지 (openVideo 함수 후킹)
    if (typeof window.openVideo === 'function') {
      var _orig = window.openVideo;
      window.openVideo = function(vid) {
        track('video_play', { video_id: vid });
        return _orig.apply(this, arguments);
      };
    } else {
      // openVideo가 나중에 정의되는 경우 대비
      Object.defineProperty(window, 'openVideo', {
        configurable: true,
        set: function(fn) {
          var wrapped = function(vid) {
            track('video_play', { video_id: vid });
            return fn.apply(this, arguments);
          };
          Object.defineProperty(window, 'openVideo', { value: wrapped, writable: true, configurable: true });
        }
      });
    }

    // 4. 수료증 발급 감지 (certificate.html의 generateCert 후킹)
    if (location.pathname.includes('certificate')) {
      var _gen = window.generateCert;
      if (typeof _gen === 'function') {
        window.generateCert = function() {
          var name = document.getElementById('inp-name') ? document.getElementById('inp-name').value : '';
          track('certificate_issued', { student_name: name });
          return _gen.apply(this, arguments);
        };
      } else {
        Object.defineProperty(window, 'generateCert', {
          configurable: true,
          set: function(fn) {
            var wrapped = function() {
              var name = document.getElementById('inp-name') ? document.getElementById('inp-name').value : '';
              track('certificate_issued', { student_name: name });
              return fn.apply(this, arguments);
            };
            Object.defineProperty(window, 'generateCert', { value: wrapped, writable: true, configurable: true });
          }
        });
      }
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
