const CACHE_NAME = 'azab-color-picker-v1.0';
const urlsToCache = [
  '/color-picker',
  '/manifest.json',
  '/assets/img/icon-192.png'
];

self.addEventListener('install', event => {
  console.log('🔧 Installing Service Worker...');
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('📦 Caching app shell');
        return cache.addAll(urlsToCache);
      })
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        if (response) {
          console.log('📱 Loading from cache:', event.request.url);
          return response;
        }
        return fetch(event.request);
      })
  );
});
