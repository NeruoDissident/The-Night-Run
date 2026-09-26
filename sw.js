/* Build-generated, scope-isolated offline cache. Does not contain saved games. */
'use strict';
const PREFIX = 'night-run:' + self.registration.scope + ':';
const CACHE = PREFIX + 'b6a941681f7db4ca';
const ASSETS = ["./index.html", "./manifest.webmanifest", "./apple-touch-icon.png", "./icons/favicon-32.png", "./icons/icon-192.png", "./icons/icon-512.png", "./icons/icon-maskable-512.png", "./icons/logo.svg"];
const ROOT = new URL('./', self.registration.scope).href;
const INDEX = new URL('index.html', ROOT).href;
const ALLOWED = new Set(ASSETS.map(path => new URL(path, ROOT).href));

self.addEventListener('install', event => {
  event.waitUntil(caches.open(CACHE).then(cache => cache.addAll(ASSETS)));
  // Updates wait for an explicit player action. Never reload a run in progress.
});
self.addEventListener('activate', event => {
  event.waitUntil((async () => {
    for (const name of await caches.keys()) {
      if (name.startsWith(PREFIX) && name !== CACHE) await caches.delete(name);
    }
    await self.clients.claim();
  })());
});
self.addEventListener('message', event => {
  if (event.data?.type === 'APPLY_UPDATE') self.skipWaiting();
});
self.addEventListener('fetch', event => {
  const request = event.request;
  const url = new URL(request.url);
  if (request.method !== 'GET' || url.origin !== self.location.origin || !url.href.startsWith(ROOT)) return;
  if (request.mode === 'navigate' && (url.pathname === new URL(ROOT).pathname || url.pathname === new URL(INDEX).pathname)) {
    event.respondWith((async () => {
      try {
        const response = await fetch(request);
        if (response.ok) return response;
      } catch (_) { /* The installed copy works without a network. */ }
      return (await caches.open(CACHE)).match(INDEX);
    })());
    return;
  }
  url.search = '';
  if (ALLOWED.has(url.href)) {
    event.respondWith((async () => {
      const cached = await (await caches.open(CACHE)).match(url.href);
      return cached || fetch(request);
    })());
  }
});
