/* Remember a read-only PDF folder on this device. Never upload files or handles. */
(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.LocalLibrary = api.mount(root);
})(typeof window === 'undefined' ? null : window, function () {
  'use strict';
  const normalize = value => String(value || '').replace(/\\/g, '/').replace(/^\/+|\/+$/g, '').toLowerCase();
  function match(entries, ev, src) {
    const library = normalize(src.library_path);
    const names = [normalize(ev.source_id + '.pdf'), library.split('/').pop()].filter(Boolean);
    // Prefer the longest matching library suffix, not an arbitrary duplicate basename.
    if (library) {
      const parts = library.split('/');
      for (let i = 0; i < parts.length; i++) {
        const suffix = parts.slice(i).join('/');
        const found = entries.filter(e => normalize(e.path) === suffix || normalize(e.path).endsWith('/' + suffix));
        if (found.length) return found.length === 1 ? {entry: found[0]} : {status: 'ambiguous'};
      }
    }
    for (const name of names) {
      const found = entries.filter(e => normalize(e.path).split('/').pop() === name);
      if (found.length) return found.length === 1 ? {entry: found[0]} : {status: 'ambiguous'};
    }
    return {status: 'missing'};
  }
  function create({store, pick, createURL, revokeURL}) {
    let handle = null, entries = [], generation = 0, state = {status: 'empty', name: '', count: 0};
    const listeners = new Set(), urls = new Map();
    const emit = () => { for (const fn of listeners) fn({...state}); };
    const clearURLs = () => { for (const item of urls.values()) revokeURL(item.url); urls.clear(); };
    function set(next) { state = {...state, ...next}; emit(); }
    async function scan(folder, token) {
      const found = [];
      async function walk(dir, prefix) {
        for await (const entry of dir.values()) {
          if (token !== generation) return;
          const path = prefix + entry.name;
          if (entry.kind === 'directory') await walk(entry, path + '/');
          else if (/\.pdf$/i.test(entry.name)) found.push({path, handle: entry});
        }
      }
      await walk(folder, '');
      return found;
    }
    async function refresh() {
      if (!handle) return;
      const folder = handle, token = ++generation;
      clearURLs(); entries = [];
      set({status: 'loading', count: 0, error: ''});
      try {
        if (await folder.queryPermission({mode: 'read'}) !== 'granted') {
          if (token === generation) set({status: 'permission'});
          return;
        }
        const found = await scan(folder, token);
        if (token !== generation) return;
        entries = found;
        set({status: 'ready', count: entries.length});
      } catch (err) {
        if (token === generation) set({status: err.name === 'NotAllowedError' ? 'permission' : 'error', error: 'Folder unavailable. Check that it is on this device, then reconnect.'});
      }
    }
    const ready = (async () => {
      const token = generation;
      try {
        const saved = await store.get();
        if (token !== generation || !saved) return;
        handle = saved;
        set({name: saved.name, remembered: true});
        await refresh();
      } catch { set({error: 'Folder memory unavailable in this browser. You can still connect for this visit.'}); }
    })();
    async function connect() {
      // Call the picker directly from the click; awaits before it can lose user activation.
      let chosen;
      try { chosen = await pick({id: 'ruralscan-pdfs', mode: 'read', ...(handle ? {startIn: handle} : {})}); }
      catch (err) { if (err.name !== 'AbortError') set({error: 'Could not connect the folder. Try again in Chrome or Edge.'}); return; }
      ++generation; handle = chosen; entries = []; clearURLs();
      set({status: 'loading', count: 0, name: chosen.name, remembered: false, sessionOnly: false, error: ''});
      try { await store.set(chosen); state.remembered = true; }
      catch { state.remembered = false; }
      await refresh();
    }
    async function allow() {
      if (!handle) return;
      try {
        const permission = await handle.requestPermission({mode: 'read'});
        if (permission === 'granted') await refresh();
        else set({status: 'permission', error: 'Folder access was not granted. Click Reconnect PDF folder to try again.'});
      } catch { set({status: 'permission', error: 'Click Reconnect PDF folder again, or choose another folder under Folder options and help.'}); }
    }
    async function useFiles(files) {
      ++generation; handle = null; clearURLs();
      entries = Array.from(files).filter(f => /\.pdf$/i.test(f.name)).map(file => ({
        path: file.webkitRelativePath || file.name, handle: {getFile: async () => file}
      }));
      set({status: 'ready', name: files[0]?.webkitRelativePath?.split('/')[0] || 'Selected PDFs', count: entries.length, remembered: false, sessionOnly: true, error: ''});
      try { await store.remove(); } catch { /* File-input fallback has no persistent handle. */ }
    }
    async function disconnect() {
      ++generation; handle = null; entries = []; clearURLs();
      set({status: 'empty', name: '', count: 0, remembered: false, sessionOnly: false, error: ''});
      try { await store.remove(); }
      catch { set({error: 'Disconnected for this visit. Browser storage could not be cleared; remove site data to forget it permanently.'}); }
    }
    async function pdf(ev, src) {
      await ready;
      if (state.status !== 'ready') return {status: state.status};
      const token = generation, result = match(entries, ev, src);
      if (!result.entry) return result;
      try {
        const file = await result.entry.handle.getFile();
        // Names identify a candidate; reject non-PDF bytes and never claim quote verification.
        if (await file.slice(0, 5).text() !== '%PDF-') return {status: 'invalid'};
        if (token !== generation) return {status: 'changed'};
        const path = result.entry.path, old = urls.get(path);
        if (old && old.size === file.size && old.modified === file.lastModified) return {status: 'found', path, url: old.url};
        if (old) revokeURL(old.url);
        const url = createURL(file);
        urls.set(path, {url, size: file.size, modified: file.lastModified});
        return {status: 'found', path, url};
      } catch (err) { return {status: err.name === 'NotAllowedError' ? 'permission' : 'unavailable'}; }
    }
    return {ready, connect, allow, refresh, disconnect, useFiles, pdf,
      state: () => ({...state}), subscribe: fn => { listeners.add(fn); return () => listeners.delete(fn); }};
  }
  function browserStore(win) {
    const database = new Promise((resolve, reject) => {
      const request = win.indexedDB.open('ruralscan-local-library', 1);
      request.onupgradeneeded = () => request.result.createObjectStore('folders');
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
      request.onblocked = () => reject(Error('Folder storage is blocked'));
    });
    async function transaction(mode, action) {
      const db = await database;
      return new Promise((resolve, reject) => {
        const tx = db.transaction('folders', mode), request = action(tx.objectStore('folders'));
        tx.oncomplete = () => resolve(request.result);
        tx.onerror = () => reject(tx.error); tx.onabort = () => reject(tx.error);
      });
    }
    return {get: () => transaction('readonly', s => s.get('pdf-library')),
      set: h => transaction('readwrite', s => s.put(h, 'pdf-library')),
      remove: () => transaction('readwrite', s => s.delete('pdf-library'))};
  }
  function mount(win) {
    const supported = typeof win.showDirectoryPicker === 'function';
    const service = create({store: browserStore(win), pick: options => win.showDirectoryPicker(options),
      createURL: file => URL.createObjectURL(file), revokeURL: url => URL.revokeObjectURL(url)});
    const el = (name, text) => { const node = document.createElement(name); if (text) node.textContent = text; return node; };
    const panel = el('section'); panel.className = 'local-library-settings'; panel.setAttribute('aria-label', 'Source PDFs on this device');
    const toolbar = el('div'); toolbar.className = 'local-library-toolbar';
    const heading = el('div'), title = el('strong', 'Source PDFs'), subtitle = el('p');
    const status = el('p'), actions = el('div'), locations = el('div');
    status.setAttribute('role', 'status'); status.className = 'local-library-status';
    const help = el('details'), summary = el('summary', 'Help finding your folder'); help.className = 'local-library-help';
    const body = el('div');
    actions.className = 'local-library-actions'; locations.className = 'local-library-locations';
    const button = (text, fn) => { const b = el('button', text); b.type = 'button'; b.className = 'pill-btn'; b.onclick = fn; return b; };
    const input = el('input'); input.type = 'file'; input.multiple = true; input.accept = '.pdf'; input.setAttribute('webkitdirectory', ''); input.hidden = true;
    input.onchange = () => { if (input.files.length) service.useFiles(input.files); };
    const connect = button('Connect PDF folder', () => supported ? service.connect() : input.click());
    connect.classList.add('local-library-connect');
    const change = button('Change folder', () => supported ? service.connect() : input.click());
    const refresh = button('Refresh folder', () => service.refresh());
    const disconnect = button('Disconnect', () => service.disconnect());
    actions.append(refresh, change, disconnect);
    const steps = el('ol');
    steps.append(el('li', 'Click Connect PDF folder and choose your synced team PDF library.'), el('li', 'Select the folder and allow access. Subfolders are included.'));
    const permissionNote = el('p', 'A saved path is a location hint, not permission. Your browser needs you to select the folder once before this page can read its PDFs.');
    const privacy = el('p', supported ? 'PDFs stay on this device. Your browser remembers the folder and may ask to reconnect after a restart.' : 'PDFs stay on this device. Select the folder again after a reload, or use Chrome or Edge to remember it.');
    body.append(steps, permissionNote, privacy, actions); help.append(summary, body);
    heading.append(title, subtitle); toolbar.append(heading, connect); panel.append(toolbar, status, locations, help, input);
    const optional = el('details'), optionalTitle = el('summary', 'Optional: PDFs inside the dashboard');
    optional.className = 'local-library-optional';
    optional.append(optionalTitle, panel);
    document.getElementById('review-library-controls').append(optional);
    let presets = {};
    function showLocations() {
      locations.replaceChildren();
      const reviewer = (document.getElementById('vf-reviewer')?.value || '').toLowerCase();
      for (const item of presets[reviewer] || []) {
        const row = el('div'), path = el('code', item.path);
        const copy = button('Copy path', async () => {
          try { await navigator.clipboard.writeText(item.path); copy.textContent = 'Copied'; }
          catch { copy.textContent = 'Select and copy path above'; }
        });
        row.append(el('strong', item.label), path, copy); locations.append(row);
      }
      steps.firstElementChild.textContent = locations.childElementCount ? 'Copy the recommended path shown above, then click Connect PDF folder.' : 'Click Connect PDF folder and choose your synced team PDF library.';
      steps.lastElementChild.textContent = locations.childElementCount ? 'In the folder chooser, press ⌘⇧G on Mac and paste the path; on Windows, paste into the address bar. Select that folder and allow access. Subfolders are included.' : 'Select the folder and allow access. Subfolders are included.';
      locations.hidden = service.state().status === 'ready' || !locations.childElementCount;
    }
    fetch('review/library-locations.json').then(r => r.ok ? r.json() : {}).then(data => { presets = data; showLocations(); }).catch(() => {});
    document.getElementById('vf-reviewer').addEventListener('change', showLocations);
    help.addEventListener('toggle', () => { if (help.open) showLocations(); });
    function draw(state) {
      const connected = state.status === 'ready';
      optionalTitle.textContent = connected ? 'Local PDFs connected · ' + state.name : 'Optional: PDFs inside the dashboard';
      title.textContent = connected ? 'PDFs connected' : 'Local PDF preview';
      subtitle.textContent = connected ? state.name + ' · ' + state.count.toLocaleString() + (state.count === 1 ? ' PDF' : ' PDFs') :
        state.status === 'loading' ? 'Finding PDFs in ' + state.name + '…' :
        state.status === 'permission' ? state.name + ' needs your permission to reopen PDFs.' :
        'Use Open source on a finding to read it online. Connect a folder only if you want local PDFs displayed here.';
      connect.textContent = state.status === 'permission' ? 'Reconnect PDF folder' : state.status === 'loading' ? 'Connecting…' : 'Connect PDF folder';
      connect.onclick = () => state.status === 'permission' ? service.allow() : supported ? service.connect() : input.click();
      locations.hidden = connected || !locations.childElementCount;
      connect.hidden = connected;
      connect.disabled = state.status === 'loading';
      summary.textContent = connected || state.name ? 'Folder options and help' : 'Help finding your folder';
      steps.hidden = connected || state.status === 'permission';
      change.hidden = !state.name;
      refresh.hidden = !connected || state.sessionOnly;
      disconnect.hidden = !state.name;
      actions.hidden = !state.name;
      status.textContent = state.error || (connected && !state.count ? 'No PDFs found. Choose a folder containing your source PDFs.' :
        connected && !state.remembered ? 'Connected for this visit. Select the folder again after a reload.' :
        !supported && !connected ? 'This browser needs the folder again after each reload. Chrome or Edge can remember it.' : '');
      status.hidden = !status.textContent;
    }
    service.subscribe(draw); draw(service.state());
    return {...service, supported, openSettings() { optional.open = true; help.open = true; panel.scrollIntoView({block: 'center'}); summary.focus(); },
      connect: () => supported ? service.connect() : input.click()};
  }
  return {create, match, browserStore, mount};
});
