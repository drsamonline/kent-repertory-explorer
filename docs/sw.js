/* Repertorium Publicum Explorer — offline cache.
 *
 * HTML is network-first, so a release lands on the next visit; the cache is
 * only the offline fallback. Assets are cache-first with a background refresh.
 * CACHE is bumped on every release, and the page prints a build stamp in its
 * footer so "am I on the new one?" is answerable from the page itself.
 *
 * Fixed: CORE listed './app.html', which does not exist here (the app is
 * ./play/index.html). addAll() rejected, the catch swallowed it, and nothing
 * was ever precached — so the offline promise was never kept. */
const CACHE = 'rpe-v5';
const CORE = [
  './',
  './index.html',
  './play/',
  './play/index.html',
  './manifest.webmanifest',
  './play/manifest.webmanifest',
  './assets/icon.svg',
  './assets/icon-192.png',
  './assets/icon-512.png'
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE)
      .then(c => Promise.allSettled(CORE.map(u => c.add(u))))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET' || new URL(req.url).origin !== location.origin) return;

  const isHTML = req.mode === 'navigate' || (req.headers.get('accept') || '').includes('text/html');
  if (isHTML) {
    e.respondWith(
      fetch(req)
        .then(r => { const cp = r.clone(); caches.open(CACHE).then(c => c.put(req, cp)); return r; })
        .catch(() => caches.match(req).then(r => r || caches.match('./index.html')))
    );
    return;
  }

  e.respondWith(
    caches.match(req).then(hit => {
      const net = fetch(req).then(res => {
        if (res && res.ok) { const cp = res.clone(); caches.open(CACHE).then(c => c.put(req, cp)); }
        return res;
      }).catch(() => hit);
      return hit || net;
    })
  );
});
