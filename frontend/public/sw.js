// Minimal Service Worker for KrishiSampann PWA - No Caching
const CACHE_NAME = 'krishisampann-v1';

self.addEventListener('install', (event) => {
  console.log('Service Worker installed');
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  console.log('Service Worker activated');
  event.waitUntil(self.clients.claim());
});

self.addEventListener('fetch', (event) => {
  // Let all requests go through to the network
  // No caching, just pass through
  event.respondWith(fetch(event.request));
});

// Optional: Handle offline detection
self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});
