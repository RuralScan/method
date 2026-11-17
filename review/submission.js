/* GitHub authenticates the voter. Drafts stay local until a public receipt is created. */
(() => {
  const byId = id => document.getElementById(id);
  const dialog = byId('finding-submission');
  const batch = byId('review-batch');
  const form = dialog.querySelector('form');
  const {verdict, reason, note} = form.elements;
  const {fixtures, header, chunks, receiptBody} = BatchReceipt;
  const prefix = 'ruralscan.vote.v1/';
  const reviewer = () => (window._vfReviewer || '').trim();
  const key = r => prefix + [r.reviewer.toLowerCase(),r.revision,r.evidence_id].map(encodeURIComponent).join('/');
  const inbox = 'https://github.com/RuralScan/evidence/issues/new?';
  const action = (label, fn) => {
    const button = document.createElement('button');
    button.type = 'button'; button.textContent = label; button.addEventListener('click', fn);
    return button;
  };
  function drafts() {
    const scope = prefix + encodeURIComponent(reviewer().toLowerCase()) + '/';
    return Object.keys(localStorage).filter(k => k.startsWith(scope)).sort().map(k => JSON.parse(localStorage.getItem(k)));
  }
  function refresh() {
    byId('review-batch-count').textContent = drafts().length;
  }
  function label(id, revision) {
    const saved = localStorage.getItem(key({reviewer:reviewer(), revision, evidence_id:id}));
    return saved ? 'Edit saved decision' : 'Review finding';
  }
  window.ReviewBatch = {refresh, label};
  window.addEventListener('storage', () => { refresh(); if (batch.open) showBatches(); });

  document.addEventListener('click', event => {
    const trigger = event.target.closest('.finding-submit');
    if (!trigger) return;
    form.reset();
    byId('batch-reviewer-label').hidden = Boolean(reviewer());
    form.elements.handle.value = reviewer();
    const {finding, revision, lane} = trigger.dataset;
    Object.assign(form.dataset, {finding, revision, lane});
    dialog.querySelector('output').textContent = lane + ' · ' + finding;
    const codes = [...new Set([..._VF_RC_PASSED, ..._VF_RC_FLAGGED])];
    reason.replaceChildren(new Option('Choose a reason', ''), ...codes.map(c => new Option(c.replaceAll('_',' '), c)));
    const saved = localStorage.getItem(key({reviewer:reviewer(), revision, evidence_id:finding}));
    if (saved) {
      const d = JSON.parse(saved); verdict.value = d.decision; reason.value = d.reason; note.value = d.note;
    }
    reason.required = verdict.value === 'reject';
    dialog.showModal();
  });
  verdict.addEventListener('change', () => { reason.required = verdict.value === 'reject'; });
  dialog.querySelector('[data-cancel]').addEventListener('click', () => dialog.close());
  form.addEventListener('submit', event => {
    event.preventDefault();
    const {finding, revision, lane} = form.dataset;
    const vote = {evidence_id:finding, decision:verdict.value, reason:reason.value, note:note.value};
    if (event.submitter?.value === 'single') {
      const test = finding === fixtures[lane];
      const body = header + JSON.stringify({kind:'vote', lane, revision, test, payload:vote});
      location.assign(inbox + new URLSearchParams({title:(test?'TEST · ':'')+lane+' · finding review · '+finding, body}));
      return;
    }
    if (!reviewer()) {
      const handle = form.elements.handle;
      if (!/^[a-z0-9](?:[a-z0-9-]{0,37}[a-z0-9])?$/i.test(handle.value.trim())) {
        handle.setCustomValidity('Enter your GitHub username for this batch.');
        handle.reportValidity();
        handle.setCustomValidity('');
        return;
      }
      setVfReviewer(handle.value.trim());
    }
    const draft = {...vote, reviewer:reviewer(), revision, lane};
    try { localStorage.setItem(key(draft), JSON.stringify(draft)); }
    catch { dialog.querySelector('output').textContent = 'Browser storage is full or unavailable. Use Submit this finding only.'; return; }
    dialog.close(); refresh();
    for (const button of document.querySelectorAll('.finding-submit')) {
      if (button.dataset.finding === finding) button.textContent = 'Edit saved decision';
    }
    byId('review-batch-status').textContent = finding + ' saved to your batch.';
  });

  function showBatches() {
    const host = byId('review-batch-groups'); host.replaceChildren();
    const rows = drafts();
    byId('review-batch-owner').textContent = rows.length ? reviewer() + ' · ' + rows.length + ' saved. Submit with this GitHub account.' :
      (reviewer() ? 'No saved decisions for '+reviewer()+'.' : 'Choose your reviewer name to start a batch.');
    byId('review-batch-message').textContent = '';
    for (const group of chunks(rows)) {
      const body = receiptBody(group);
      const title = 'Finding review batch · ' + group.length + ' · ' + group[0].reviewer;
      const section = document.createElement('section');
      const details = document.createElement('details'), summary = document.createElement('summary');
      summary.textContent = group.length + ' decisions · register ' + group[0].revision.slice(0,8);
      const list = document.createElement('ul');
      for (const row of group) {
        const li = document.createElement('li');
        li.append(row.lane+' · '+row.evidence_id+' · '+row.decision+(row.reason?' · '+row.reason:'')+(row.note?' · '+row.note:'')+' ',
          action('Remove from batch', () => { localStorage.removeItem(key(row)); refresh(); showBatches(); }));
        list.append(li);
      }
      details.append(summary,list); section.append(details);
      let href = inbox + new URLSearchParams({title,body});
      if (href.length > 6000) {
        href = inbox + new URLSearchParams({title});
        const help = document.createElement('p');
        help.textContent = 'Copy this batch, open GitHub, paste into the issue description and choose Create.';
        const payload = document.createElement('textarea');
        payload.readOnly = true; payload.value = body; payload.setAttribute('aria-label','Batch issue description');
        section.append(help,action('Copy batch',async () => {
          try { await navigator.clipboard.writeText(body); byId('review-batch-message').textContent='Batch copied.'; }
          catch { payload.focus(); payload.select(); byId('review-batch-message').textContent='Copy the selected description.'; }
        }),payload);
      }
      const open = document.createElement('a');
      open.href = href; open.target = '_blank'; open.rel = 'noopener'; open.textContent = 'Open batch in GitHub';
      const label = document.createElement('label');
      label.textContent = ' After creating the issue, enter its receipt number ';
      const input = document.createElement('input'); input.type='number'; input.min='1';
      label.append(input);
      section.append(open,label,action('Confirm receipt',async () => {
        const status = byId('review-batch-message');
        if (!/^[1-9]\d*$/.test(input.value)) { status.textContent='Enter the GitHub issue number.'; return; }
        try {
          const res = await fetch('https://api.github.com/repos/RuralScan/evidence/issues/'+input.value,{cache:'no-store'});
          if (!res.ok) throw Error('Receipt unavailable. Saved decisions retained.');
          const issue = await res.json();
          if (issue.pull_request || issue.user?.login?.toLowerCase() !== group[0].reviewer.toLowerCase() ||
              issue.body?.replaceAll('\r\n','\n').trim() !== body) throw Error('Receipt differs from this batch. Saved decisions retained.');
          for (const r of group) if (localStorage.getItem(key(r)) === JSON.stringify(r)) localStorage.removeItem(key(r));
          refresh(); showBatches(); status.textContent='Receipt #'+issue.number+' confirmed. Submitted decisions await register processing.';
        } catch (error) { status.textContent=error.message; }
      }));
      host.append(section);
    }
  }
  byId('review-submit-all').addEventListener('click',() => { showBatches(); batch.showModal(); });
  batch.querySelector('[data-close]').addEventListener('click',() => batch.close());
  batch.addEventListener('close',() => { for (const b of document.querySelectorAll('.finding-submit')) b.textContent=label(b.dataset.finding,b.dataset.revision); });
})();
