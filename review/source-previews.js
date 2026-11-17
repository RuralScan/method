/* Load provenance-matched crops and passages from the same revision as the queue. */
const SourcePreviews = (() => {
  const indexes = new Map();
  const files = new Map();
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
  function localPDF(host, ev, src, page) {
    const names = [ev.source_id+'.pdf', (src.library_path || '').split('/').pop()];
    const show = () => {
      const file = names.map(n => files.get(n)).find(Boolean);
      if (!file) return false;
      const frame = tag('iframe'); frame.title='Local source PDF';
      const words=(ev.quote || '').trim().split(/\s+/).slice(0,8).join(' ');
      frame.src=file+'#page='+page+(words ? '&search='+encodeURIComponent(words) : '');
      host.replaceChildren(tag('p','Your local source · PDF page '+page),frame);
      return true;
    };
    if (show()) return;
    const label = tag('label','Preview library PDFs from this device ');
    const input = tag('input'); input.type='file'; input.accept='.pdf'; input.multiple=true;
    input.addEventListener('change',() => {
      for (const f of input.files) {
        if (!f.name.toLowerCase().endsWith('.pdf')) continue;
        if (files.has(f.name)) URL.revokeObjectURL(files.get(f.name));
        files.set(f.name,URL.createObjectURL(f));
      }
      if (!show()) hint.textContent='Choose '+names.filter(Boolean).join(' or ')+'.';
    });
    const hint = tag('small','Select multiple acquired PDFs once. They stay on this device.');
    label.append(input); host.append(label,hint);
  }
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
    if (!item && page) { const local=tag('div'); host.append(local); localPDF(local,ev,src,page); }
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
