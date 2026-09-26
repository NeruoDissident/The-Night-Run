/* Platform integration is optional: the same game also runs as a local HTML file. */
(function () {
  'use strict';
  let registration = null;
  let installPrompt = null;
  let updateRequested = false;
  const state = { offline: false, update: false, error: '', installed: false };
  const standalone = window.matchMedia('(display-mode: standalone)');
  function changed() {
    state.installed = standalone.matches || navigator.standalone === true;
    const label = document.getElementById('pwaStatus');
    if (label) label.textContent = state.error || (state.update ? 'UPDATE READY · OPEN INSTALL MENU' : state.offline ? 'READY TO PLAY OFFLINE' : location.protocol === 'file:' ? 'PORTABLE EDITION' : 'PREPARING OFFLINE PLAY…');
    window.dispatchEvent(new CustomEvent('night-run-platform', { detail: { ...state } }));
  }
  window.addEventListener('beforeinstallprompt', event => {
    event.preventDefault();
    installPrompt = event;
    changed();
  });
  window.addEventListener('appinstalled', () => { installPrompt = null; changed(); });
  standalone.addEventListener?.('change', changed);
  window.NightRunPWA = {
    getState: () => ({ ...state, canPrompt: !!installPrompt, hosted: /^https?:$/.test(location.protocol) }),
    async install() {
      if (!installPrompt) return false;
      const prompt = installPrompt;
      installPrompt = null;
      await prompt.prompt();
      const choice = await prompt.userChoice;
      if (choice.outcome === 'accepted') navigator.storage?.persist?.().catch(() => {});
      changed();
      return choice.outcome === 'accepted';
    },
    applyUpdate() {
      if (!registration?.waiting) return;
      window.dispatchEvent(new Event('night-run-save-request'));
      updateRequested = true;
      registration.waiting.postMessage({ type: 'APPLY_UPDATE' });
    }
  };
  changed();
  if (!('serviceWorker' in navigator) || !/^https?:$/.test(location.protocol)) return;
  if (!window.isSecureContext) { state.error = 'OFFLINE INSTALL REQUIRES HTTPS'; changed(); return; }
  navigator.serviceWorker.addEventListener('controllerchange', () => {
    if (updateRequested) location.reload();
  });
  function watch(worker) {
    worker?.addEventListener('statechange', () => {
      if (worker.state === 'installed' && navigator.serviceWorker.controller) {
        state.update = true;
        changed();
      }
    });
  }
  navigator.serviceWorker.register(new URL('sw.js', location.href), { scope: './', updateViaCache: 'none' }).then(async reg => {
    registration = reg;
    state.update = !!reg.waiting;
    watch(reg.installing);
    reg.addEventListener('updatefound', () => watch(reg.installing));
    await navigator.serviceWorker.ready;
    state.offline = true;
    changed();
  }).catch(async () => {
    // A previously installed app may reopen with no connection at all.
    try {
      registration = await navigator.serviceWorker.getRegistration(new URL('./', location.href));
      if (registration?.active) { state.offline = true; changed(); return; }
    } catch (_) { /* The portable game still works without browser storage. */ }
    state.error = 'ONLINE PLAY READY · OFFLINE STORAGE UNAVAILABLE';
    changed();
  });
})();
