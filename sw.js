// CEC English Camp - Service Worker
const CACHE = 'cec-v1';
const PRECACHE = [
  '/',
  '/camp-a/',
  '/camp-b/',
  '/camp-c/',
  '/speaking/',
  '/mom-teacher/',
  '/grammar-camp/',
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
  // Only cache GET requests
  if (e.request.method !== 'GET') return;

  // Skip cross-origin requests (R2 CDN, Google Fonts, ngrok API)
  const url = new URL(e.request.url);
  if (url.origin !== location.origin) return;

  // Network-first for HTML (fresh content when online)
  if (e.request.headers.get('accept')?.includes('text/html')) {
    e.respondWith(
      fetch(e.request)
        .then(res => {
          const clone = res.clone();
          caches.open(CACHE).then(c => c.put(e.request, clone));
          return res;
        })
        .catch(() => caches.match(e.request))
    );
    return;
  }

  // Cache-first for assets (CSS, JS, images)
  e.respondWith(
    caches.match(e.request).then(r =>
      r || fetch(e.request).then(res => {
        const clone = res.clone();
        caches.open(CACHE).then(c => c.put(e.request, clone));
        return res;
      })
    )
  );
});
