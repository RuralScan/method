/* Load provenance-matched crops and passages from the same revision as the queue. */
const SourcePreviews = (() => {
  const indexes = new Map();
  const localPanels = new Map();
  const root = pin => 'https://raw.githubusercontent.com/RuralScan/evidence/'+pin+'/publication/source-previews/';
  const tag = (name, text) => {
    const el = document.createElement(name);
    if (text) el.textContent = text;
    return el;
  };
  function link(label, href) {
    const el = tag('a',label); el.href=href; el.target='_blank'; el.rel='noopener'; return el;
  }
  async function signature(ev, src) {
    const values = ['source_id','page','locator_type','locator','quote','claim_basis'].map(k => ev[k]);
    values.push(...['url','library_path','access_status','license','doi'].map(k => src[k]));
    const bytes = new TextEncoder().encode(JSON.stringify(values.map(v => String(v || ''))));
    const hash = new Uint8Array(await crypto.subtle.digest('SHA-256',bytes));
    return Array.from(hash,b => b.toString(16).padStart(2,'0')).join('');
  }
  function loadIndex(pin) {
    if (!indexes.has(pin)) indexes.set(pin,fetch(root(pin)+'index.json').then(r => {
      if (!r.ok) throw Error('Preview index unavailable');
      return r.json();
    }).catch(err => { indexes.delete(pin); throw err; }));
    return indexes.get(pin);
  }
  async function localPDF(host, ev, src, page) {
    const request = {ev, src, page};
    localPanels.set(host, request);
    const result = await LocalLibrary.pdf(ev, src);
    if (!host.isConnected || localPanels.get(host) !== request) return;
    host.replaceChildren();
    if (result.status === 'found') {
      const frame = tag('iframe'); frame.title = 'Local source PDF';
      const words = (ev.quote || '').trim().split(/\s+/).slice(0,8).join(' ');
      frame.src = result.url + '#page=' + page + (words ? '&search=' + encodeURIComponent(words) : '');
      host.append(tag('p', 'Connected folder · ' + result.path + ' · PDF page ' + page),
        link('Open local PDF in a new tab', result.url + '#page=' + page), frame);
      return;
    }
    const messages = {
      loading: 'Reading connected PDF folder…',
      missing: 'PDF not found in the connected folder. Expected ' + ev.source_id + '.pdf or the registered library filename.',
      ambiguous: 'More than one PDF matches this source. Connect its specific subfolder so the correct file is unambiguous.',
      invalid: 'The matching file is not readable as a PDF. Check the local file.',
      unavailable: 'Could not read this PDF. Make it available offline in OneDrive, then refresh the folder.',
      permission: 'Your folder is remembered. Allow read access to show this PDF.',
      error: 'Connected folder is unavailable. Check its location or reconnect it.'
    };
    host.append(tag('p', messages[result.status] || 'Connect your PDF folder once to open matching sources at the cited page.'));
    const button = tag('button'); button.type = 'button'; button.className = 'pill-btn';
    const connected = LocalLibrary.state().status === 'ready';
    button.textContent = result.status === 'permission' ? 'Allow folder access' : connected ? 'Refresh folder' : 'Connect PDF folder';
    button.onclick = () => result.status === 'permission' ? LocalLibrary.allow() : connected ? LocalLibrary.refresh() : LocalLibrary.connect();
    button.disabled = result.status === 'loading';
    if (connected && LocalLibrary.state().sessionOnly) { button.textContent = 'Choose PDF folder'; button.onclick = () => LocalLibrary.connect(); }
    const settings = tag('button', 'Folder location / settings'); settings.type = 'button'; settings.className = 'pill-btn';
    settings.onclick = () => LocalLibrary.openSettings();
    host.append(button, ' ', settings);
  }
  LocalLibrary.subscribe(() => {
    for (const [host, item] of localPanels) {
      if (!host.isConnected) { localPanels.delete(host); continue; }
      localPDF(host, item.ev, item.src, item.page);
    }
  });
  async function render(panel) {
    const host = panel.querySelector('div');
    const pin = reviewData.registerRevision;
    const ev = [...reviewData.registers.EV_evidence_register,...(reviewData._evDropped || [])]
      .find(r => r.evidence_id === panel.dataset.preview);
    const src = ev && reviewData.registers.SRC_source_register.find(s => s.source_id === ev.source_id);
    if (!src || !pin) { host.textContent='Source record unavailable.'; return; }
    host.textContent='Loading source preview…';
    let item, unavailable=false;
    try {
      const index = await loadIndex(pin);
      const found = index[ev.evidence_id];
      if (found && found.key === await signature(ev,src)) item=found;
    } catch { unavailable=true; }
    host.replaceChildren();
    const page=item?.page || ev.page;
    const locator=page ? 'PDF page '+page : ev.locator || 'Source';
    host.append(tag('p',(src.citation || src.source_id)+' · '+locator));
    if (item?.match) {
      const excerpt = tag('blockquote');
      excerpt.append(item.before,tag('mark',item.match),item.after);
      host.append(tag('small',item.partial?'Matched part of the quotation':'Matched source passage'),excerpt);
    }
    if (item?.image && /^[a-f0-9]{64}\.webp$/.test(item.image)) {
      const imageURL=root(pin)+'pages/'+item.image;
      const fig=tag('figure'), img=tag('img');
      img.alt='Source region on PDF page '+page; img.src=imageURL;
      img.addEventListener('error',() => fig.replaceChildren(tag('p','Image unavailable. Open the cited source below.')));
      fig.append(img);
      for (const [x,y,w,h] of item.boxes || []) {
        const overlay=tag('i'); overlay.setAttribute('aria-hidden','true');
        Object.assign(overlay.style,{left:x*100+'%',top:y*100+'%',width:w*100+'%',height:h*100+'%'});
        fig.append(overlay);
      }
      host.append(fig,link('Open full-size source region',imageURL));
    }
    if (!item) host.append(tag('p',unavailable?'Could not load the preview index. Reopen this panel to retry.':
      'No verified public preview for this version of the finding.'));
    const sources=tag('p');
    if (!item && reviewData.legacyPreviews?.has(ev.evidence_id)) {
      if (window._cropSharePointMap?.[ev.evidence_id]) {
        sources.append(link('Open saved highlighted crop in team library',
          vfSharePointUrl(window._cropSharePointMap[ev.evidence_id])), ' ');
      } else if (window._cropManifest?.has(ev.evidence_id)) {
        const url='https://raw.githubusercontent.com/CIAT/nbs_ruralscan/'+reviewData.revision+
          '/docs/crops/'+encodeURIComponent(ev.evidence_id)+'.jpg';
        const figure=tag('figure'), img=tag('img');
        img.alt='Archived highlighted source region'; img.src=url;
        figure.append(img); host.append(figure);
      }
    }
    if (src.library_path) sources.append(link('Open team library · '+locator,
      vfSharePointUrl(src.library_path)+(page?'#page='+page:'')),' ');
    if (/^https?:\/\//i.test(src.url || '')) sources.append(link('Open original source',src.url));
    host.append(sources);
    if (!item && page) { const local=tag('div'); host.append(local); await localPDF(local,ev,src,page); }
    if (!unavailable) panel.dataset.loaded='1';
  }
  document.addEventListener('toggle',event => {
    const panel=event.target;
    if (panel.matches?.('details.source-preview') && panel.open && !panel.dataset.loaded) {
      render(panel).catch(() => { panel.querySelector('div').textContent='Preview unavailable. Reopen to retry.'; });
    }
  },true);
  return {card:id => '<details class="source-preview" data-preview="'+vfEsc(id)+'"><summary>View source preview</summary><div></div></details>'};
})();
