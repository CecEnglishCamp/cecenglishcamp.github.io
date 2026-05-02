/* CEC English Camp · Service Worker
 * 전략:
 *   - Cache First: 정적 자산 (CSS, JS, 이미지, 폰트)
 *   - Network First: HTML 페이지 (오프라인 시 캐시 → /offline.html 폴백)
 *   - Cross-origin (R2 CDN, Google Fonts 등) 은 통과 (브라우저 기본 처리)
 */
const CACHE = 'cec-pwa-v1';
const PRECACHE = [
  '/',
  '/index.html',
  '/offline.html',
  '/assets/require-auth.js',
  '/assets/trial-banner.js',
  '/favicon.ico',
  '/apple-touch-icon.png',
  '/manifest.json'
];

self.addEventListener('install', e => {
  self.skipWaiting();
  e.waitUntil(
    caches.open(CACHE).then(c =>
      Promise.all(
        PRECACHE.map(url =>
          c.add(url).catch(err => console.log('[SW] precache miss:', url))
        )
      )
    )
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  // GET 요청만 처리
  if (e.request.method !== 'GET') return;

  // Cross-origin 통과 (R2 CDN, Google Fonts, Supabase 등)
  const url = new URL(e.request.url);
  if (url.origin !== location.origin) return;

  const accept = e.request.headers.get('accept') || '';

  // ── HTML: Network First → 캐시 → /offline.html ──
  if (accept.includes('text/html')) {
    e.respondWith(
      fetch(e.request)
        .then(res => {
          const clone = res.clone();
          caches.open(CACHE).then(c => c.put(e.request, clone));
          return res;
        })
        .catch(() =>
          caches.match(e.request).then(cached => cached || caches.match('/offline.html'))
        )
    );
    return;
  }

  // ── 정적 자산: Cache First → Network → 실패 시 빈 응답 ──
  e.respondWith(
    caches.match(e.request).then(cached =>
      cached ||
      fetch(e.request)
        .then(res => {
          const clone = res.clone();
          caches.open(CACHE).then(c => c.put(e.request, clone));
          return res;
        })
        .catch(() => new Response('', { status: 503, statusText: 'offline' }))
    )
  );
});
