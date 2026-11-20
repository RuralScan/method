/* GitHub authenticates the voter. Drafts stay local until a public receipt is created. */
(() => {
  const byId = id => document.getElementById(id);
  const dialog = byId('finding-submission');
  const batch = byId('review-batch');
  const form = dialog.querySelector('form');
  const {verdict, reason, note} = form.elements;
  const {fixtures, header, chunks, receiptBody} = BatchReceipt;
  const store = VoteDrafts.store(localStorage);
  const reviewer = () => (window._vfReviewer || '').trim();
  const key = VoteDrafts.key;
  const inbox = 'https://github.com/RuralScan/evidence/issues/new?';
  const action = (label, fn) => {
    const button = document.createElement('button');
    button.type = 'button'; button.textContent = label; button.addEventListener('click', fn);
    return button;
  };
  function drafts() {
    return BatchReceipt.pending(store.list(reviewer()), BatchReceipt.history(localStorage,reviewer()));
  }
  function refresh() {
    const count = drafts().length;
    byId('review-batch-count').textContent = count;
    for (const node of document.querySelectorAll('[data-review-batch-count]')) node.textContent = count;
    if (byId('vf-pending-count')) byId('vf-pending-count').textContent = reviewer() ? (count ? count + (count === 1 ? ' decision' : ' decisions') + ' saved on this device — not submitted yet' : 'No unsubmitted decisions on this device') : 'Choose your reviewer name to start.';
  }
  let appliedJournal={};
  function receiptFor(row) {
    if (!row) return null;
    const item=BatchReceipt.history(localStorage,row.reviewer).find(r=>r.rows.some(old=>JSON.stringify(old)===JSON.stringify(row)));
    if (!item) return null;
    const applied=appliedJournal[String(item.number)];
    return {...item, applied:applied?.digest===item.digest && applied.actor?.toLowerCase()===item.reviewer.toLowerCase()};
  }
  function label(id, revision) {
    const saved = localStorage.getItem(key({reviewer:reviewer(), revision, evidence_id:id}));
    return saved ? 'Edit saved decision' : 'Review finding';
  }
  window.ReviewBatch = {refresh, label, drafts, get:id => store.get({reviewer:reviewer(), revision:reviewData.registerRevision, evidence_id:id}),
    receipt:receiptFor,
    pending:revision => store.pending(reviewer(), revision),
    save:row => { store.save({...row, reviewer:reviewer()}); refresh(); },
    remove:row => { store.remove({...row, reviewer:reviewer()}); refresh(); },
    open:() => { showBatches(); batch.showModal(); checkReceipts(); }};
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
    try { store.save(draft); }
    catch (error) { dialog.querySelector('output').textContent = error.message; return; }
    dialog.close(); refresh();
    for (const button of document.querySelectorAll('.finding-submit')) {
      if (button.dataset.finding === finding) button.textContent = 'Edit saved decision';
    }
    byId('review-batch-status').textContent = finding + ' saved to your batch.';
  });

  let csvUrls = [], rendering = 0, checking = false, checkedAt = 0;
  const message = text => { byId('review-batch-message').textContent=text; };
  function download(prepared) {
    const a=document.createElement('a');
    a.href=URL.createObjectURL(new Blob([prepared.csv],{type:'text/csv;charset=utf-8'}));
    csvUrls.push(a.href); a.download=prepared.filename; a.click();
  }
  async function showBatches() {
    const generation=++rendering;
    csvUrls.forEach(url=>URL.revokeObjectURL(url)); csvUrls=[];
    const host=byId('review-batch-groups'); host.replaceChildren();
    const rows=drafts();
    byId('review-batch-owner').textContent=reviewer() ? reviewer()+' · '+rows.length+' decisions ready to submit' : 'Choose your reviewer name to start.';
    byId('review-batch-message').textContent='';
    try {
      for (const group of chunks(rows)) {
        const prepared=await BatchReceipt.prepare(group);
        if (generation!==rendering) return;
        const section=document.createElement('section'); section.className='review-submit-card';
        const title=document.createElement('h3'); title.textContent=group.length+' decisions';
        const summary=document.createElement('p');
        summary.textContent=['approve','reject','hold'].map(v=>group.filter(r=>r.decision===v).length+' '+({approve:'Keep',reject:'Drop',hold:'Query'})[v]).join(' · ');
        const help=document.createElement('p'); help.className='review-submit-instruction';
        help.textContent=prepared.attachment
          ? 'Open submission downloads your CSV and opens GitHub. Attach that file, wait for upload to finish, then click Create.'
          : 'Your decisions are already included. Open submission, then click Create on GitHub.';
        const open=document.createElement('a'); open.className='review-submit-primary';
        open.href=prepared.url; open.target='_blank'; open.rel='noopener'; open.textContent='Open submission';
        open.addEventListener('click',()=>{
          if (prepared.attachment) download(prepared);
          message('Finish on GitHub, then return here. Your decisions stay saved until we find the matching submission.');
        });
        const actions=document.createElement('div'); actions.className='review-submit-actions';
        actions.append(open,action(prepared.attachment?'Download CSV again':'Download a CSV copy',()=>download(prepared)));
        const details=document.createElement('details'), label=document.createElement('summary'), list=document.createElement('ul');
        label.textContent='Check decisions · '+group.map(r=>r.lane).filter((v,i,a)=>a.indexOf(v)===i).join(', ')+' · revision '+group[0].revision.slice(0,8);
        for(const row of group){
          const li=document.createElement('li'); li.textContent=row.evidence_id+' · '+({approve:'Keep',reject:'Drop',hold:'Query'})[row.decision]+(row.note?' · '+row.note:'')+' ';
          li.append(action('Remove',()=>{store.remove(row);refresh();showBatches();}));list.append(li);
        }
        details.append(label,list);section.append(title,summary,help,actions,details);host.append(section);
      }
      renderHistory();
      if (!rows.length && BatchReceipt.history(localStorage,reviewer()).length) document.querySelector('.review-submission-history').open=true;
    } catch(error){message(error.message);}
  }
  function renderHistory(journal=appliedJournal) {
    appliedJournal=journal;
    const host=byId('review-batch-history');host.replaceChildren();
    for(const item of BatchReceipt.history(localStorage,reviewer())){
      const applied=journal[String(item.number)];
      const done=applied?.digest===item.digest && applied.actor?.toLowerCase()===item.reviewer.toLowerCase();
      const p=document.createElement('p'), link=document.createElement('a');
      link.href=item.url;link.target='_blank';link.rel='noopener';link.textContent='Submission #'+item.number;
      p.append(link,' · '+item.rows.length+' decisions · '+(done?'Applied':'Submitted · awaiting validation and processing'));
      host.append(p);
    }
  }
  async function checkReceipts(force=false) {
    if(checking || !reviewer() || (!force && Date.now()-checkedAt<3000))return;
    checking=true;checkedAt=Date.now();
    const actor=reviewer();
    const status=byId('review-check-submissions');status.disabled=true;
    try {
      const groups=await Promise.all(chunks(drafts()).map(BatchReceipt.prepare));
      let matched=0;
      if(groups.length){
        for(let page=1;page<=3;page++){
          const res=await fetch('https://api.github.com/repos/RuralScan/evidence/issues?state=all&sort=created&direction=desc&per_page=100&creator='+encodeURIComponent(actor)+'&page='+page,{cache:'no-store'});
          if(!res.ok)throw Error('Could not check GitHub submissions. Your decisions remain saved; try Check submissions again.');
          const issues=await res.json();
          for(const group of [...groups]){
            const issue=issues.find(i=>BatchReceipt.matches(i,group));
            if(issue){await BatchReceipt.remember(localStorage,issue,group);groups.splice(groups.indexOf(group),1);matched++;}
          }
          if(!groups.length||issues.length<100)break;
        }
      }
      if(actor!==reviewer())return;
      refresh();await showBatches();
      if(matched)message('Submission found. Decisions are saved here while validation and register processing finish.');
      else if(groups.length && force)message('No matching submission yet. Finish creating it on GitHub, then check again. Decisions remain saved.');
      try {
        const res=await fetch('https://raw.githubusercontent.com/RuralScan/evidence/main/registers/applied-receipts.json',{cache:'no-store'});
        if(res.ok && actor===reviewer())renderHistory(await res.json());
      } catch { /* Receipt links remain usable when the register cannot be reached. */ }
    } catch(error){message(error.message);}
    finally {checking=false;status.disabled=false;}
  }
  byId('review-submit-all').addEventListener('click',()=>ReviewBatch.open());
  byId('review-check-submissions').addEventListener('click',()=>checkReceipts(true));
  window.addEventListener('focus',()=>{if(batch.open)checkReceipts();});
  document.addEventListener('visibilitychange',()=>{if(!document.hidden&&batch.open)checkReceipts();});
  batch.querySelector('[data-close]').addEventListener('click',()=>batch.close());
  batch.addEventListener('close',()=>{if(typeof renderVfWorklist==='function')renderVfWorklist();for(const b of document.querySelectorAll('.finding-submit'))b.textContent=label(b.dataset.finding,b.dataset.revision);});
})();
