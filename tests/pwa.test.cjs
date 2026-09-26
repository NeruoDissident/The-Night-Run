/* Exercise the shipped worker itself, including offline navigation and safe updates. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const source = fs.readFileSync(path.join(__dirname, '../sw.js'), 'utf8');

function workerHarness(scope) {
  const handlers = {};
  const cacheStore = new Map();
  const state = { network: 'online', skipped: false, claimed: false, requests: [] };
  const caches = {
    async open(name) {
      if (!cacheStore.has(name)) cacheStore.set(name, new Map());
      const entries = cacheStore.get(name);
      return {
        async addAll(paths) { for (const p of paths) { const url = new URL(p, scope).href; state.requests.push(url); entries.set(url, new Response('cached:' + url)); } },
        async match(request) { return entries.get(typeof request === 'string' ? request : request.url)?.clone(); }
      };
    },
    async keys() { return [...cacheStore.keys()]; },
    async delete(name) { return cacheStore.delete(name); }
  };
  const self = {
    registration: { scope }, location: new URL(scope + 'sw.js'),
    clients: { async claim() { state.claimed = true; } },
    skipWaiting() { state.skipped = true; },
    addEventListener(type, handler) { handlers[type] = handler; }
  };
  vm.runInNewContext(source, { self, caches, URL, Set, fetch: async request => {
    if (state.network === 'offline') throw new TypeError('Network unavailable');
    return new Response('live:' + request.url, { status: state.network === 'server-error' ? 503 : 200 });
  } });
  return { state, caches, cacheStore, async event(type, data = {}) {
    let work, response;
    handlers[type]({ ...data, waitUntil(p) { work = p; }, respondWith(p) { response = p; } });
    if (work) await work;
    return response ? await response : undefined;
  } };
}

(async () => {
  let checks = 0;
  const ok = name => { checks++; console.log('PASS ' + name); };
  for (const scope of ['https://example.test/', 'https://neruodissident.github.io/The-Night-Run/']) {
    const h = workerHarness(scope);
    await h.event('install');
    assert.ok(h.state.requests.every(url => url.startsWith(scope)));
    assert.ok(h.state.requests.includes(scope + 'index.html'));
    assert.ok(h.state.requests.includes(scope + 'apple-touch-icon.png'));
    assert.equal(h.state.skipped, false);
    ok('Install caches the complete app inside ' + new URL(scope).pathname);
    const request = { url: scope, mode: 'navigate', method: 'GET' };
    assert.equal(await (await h.event('fetch', { request })).text(), 'live:' + scope);
    ok('Online navigation gets the current game');
    h.state.network = 'offline';
    assert.equal(await (await h.event('fetch', { request })).text(), 'cached:' + scope + 'index.html');
    ok('Offline launch falls back to the installed game');
    h.state.network = 'server-error';
    assert.equal(await (await h.event('fetch', { request })).text(), 'cached:' + scope + 'index.html');
    ok('Server errors still allow offline play');
    h.state.network = 'offline';
    const icon = { url: scope + 'icons/icon-192.png', mode: 'cors', method: 'GET' };
    assert.equal(await (await h.event('fetch', { request: icon })).text(), 'cached:' + icon.url);
    ok('App icons are available offline');
    assert.equal(await h.event('fetch', { request: { url: 'https://other.test/', mode: 'navigate', method: 'GET' } }), undefined);
    assert.equal(await h.event('fetch', { request: { url: scope, mode: 'cors', method: 'POST' } }), undefined);
    ok('Unrelated origins and non-GET requests are untouched');
    await h.caches.open('other-game:saved-assets');
    await h.caches.open('night-run:' + scope + ':old-build');
    await h.event('activate');
    assert.ok(h.state.claimed);
    assert.ok(h.cacheStore.has('other-game:saved-assets'));
    assert.ok(!h.cacheStore.has('night-run:' + scope + ':old-build'));
    ok('Activation removes only obsolete Night Run caches for this scope');
    await h.event('message', { data: { type: 'UNRELATED_MESSAGE' } });
    assert.equal(h.state.skipped, false);
    await h.event('message', { data: { type: 'APPLY_UPDATE' } });
    assert.equal(h.state.skipped, true);
    ok('An update waits until the player requests it');
  }
  console.log(`\n${checks} PWA worker checks passed.`);
})().catch(err => { console.error(err); process.exitCode = 1; });
