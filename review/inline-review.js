/* Familiar per-card controls, using the current RuralScan receipt store. No live writes. */
const InlineReview = (() => {
  const edits = new Map();
  const labels = {approve:'Keep', reject:'Drop', hold:'Query'};
  const owner = () => (window._vfReviewer || '').trim();
  const identity = (id, revision) => VoteDrafts.key({reviewer:owner(), evidence_id:id, revision});
  const codes = () => [...new Set([..._VF_RC_PASSED, ..._VF_RC_FLAGGED])];
  function html(id, lane, revision) {
    const saved = ReviewBatch.get(id);
    const receipt = ReviewBatch.receipt?.(saved);
    const values = edits.get(identity(id,revision)) || saved || {};
    return '<form class="inline-review" aria-label="Your decision for '+vfEsc(id)+'" data-finding="'+vfEsc(id)+'" data-lane="'+vfEsc(lane)+'" data-revision="'+vfEsc(revision)+'" data-reviewer="'+vfEsc(owner())+'">'
      +'<div class="inline-review-fields"><label>Reason<select name="reason"><option value="">Choose if needed · required for Drop</option>'
      +codes().map(c=>'<option value="'+vfEsc(c)+'" title="'+vfEsc(_VF_RC_DESC[c] || '')+'"'+(values.reason===c?' selected':'')+'>'+vfEsc(c.replaceAll('_',' '))+'</option>').join('')+'</select></label>'
      +'<label>Note / question<textarea name="note" rows="2" maxlength="1000" placeholder="Optional for Keep; write your question before Query">'+vfEsc(values.note || '')+'</textarea></label></div>'
      +'<div class="inline-review-actions"><strong>Your decision</strong>'
      +Object.entries(labels).map(([value,label])=>'<button type="button" data-decision="'+value+'" class="review-'+value+'" aria-pressed="'+(saved?.decision===value)+'">'+({approve:'✓ ',reject:'✕ ',hold:'? '})[value]+label+'</button>').join('')
      +'<button type="button" data-undo'+(!saved || receipt?' hidden':'')+'>Undo saved decision</button>'
      +'<output role="status">'+(receipt ? '<a href="'+vfEsc(receipt.url)+'" target="_blank" rel="noopener">Submission #'+receipt.number+'</a> · '+(receipt.applied?'Applied':'Submitted · awaiting validation and processing') : saved?'Saved on this device · '+labels[saved.decision]+' · not submitted':'Choose a decision to save it to your batch.')+'</output></div></form>';
  }
  function row(form, decision) {
    if (form.dataset.reviewer !== owner()) throw Error('Reviewer changed. Reopen this finding before saving.');
    return {evidence_id:form.dataset.finding, lane:form.dataset.lane, revision:form.dataset.revision,
      reviewer:owner(), decision, reason:form.elements.reason.value, note:form.elements.note.value};
  }
  function announce(form, message) { form.querySelector('output').textContent = message; }
  function save(form, decision) {
    try {
      const draft = row(form,decision);
      ReviewBatch.save(draft);
      edits.delete(identity(draft.evidence_id,draft.revision));
      const cards = _vfCardEls(), previous = cards.findIndex(c=>c.contains(form));
      renderVfWorklist();
      _vfSetFocus(Math.max(0, Math.min(previous, _vfCardEls().length-1)));
      document.getElementById('review-batch-status').textContent = labels[decision]+' saved · '+draft.evidence_id+'. Submit your batch when ready.';
    } catch (error) {
      announce(form, error.name === 'QuotaExceededError' || error.name === 'SecurityError' ?
        'Browser could not save this decision. Free browser storage or download a backup before retrying.' : error.message);
      if (!owner()) document.getElementById('vf-reviewer').focus();
      else if (decision==='reject' && !form.elements.reason.value) form.elements.reason.focus();
      else if (decision==='hold' && !form.elements.note.value.trim()) form.elements.note.focus();
    }
  }
  document.addEventListener('submit',event=>{ if(event.target.matches('.inline-review'))event.preventDefault(); });
  document.addEventListener('click',event=>{
    const button=event.target.closest('.inline-review button');
    if(!button)return;
    const form=button.closest('form');
    if(button.dataset.decision)save(form,button.dataset.decision);
    else if(button.hasAttribute('data-undo')) {
      try { ReviewBatch.remove(row(form,ReviewBatch.get(form.dataset.finding)?.decision)); edits.delete(identity(form.dataset.finding,form.dataset.revision)); renderVfWorklist(); }
      catch(error) { announce(form,error.message); }
    }
  });
  document.addEventListener('input',event=>{
    const form=event.target.closest('.inline-review'); if(!form)return;
    const saved=ReviewBatch.get(form.dataset.finding);
    try {
      const value=row(form,saved?.decision);
      edits.set(identity(value.evidence_id,value.revision),value);
      if(saved) { ReviewBatch.save(value); announce(form,'Saved note / reason updated · not submitted.'); }
      else announce(form,'Choose Keep, Drop or Query to save this note with your decision.');
    } catch(error) { announce(form,'Edits not saved: '+error.message); }
  });
  function key(card, value) {
    const form=card.querySelector('.inline-review'); if(!form)return;
    if(value==='q' && !form.elements.note.value.trim()) { form.elements.note.focus(); return; }
    save(form, {k:'approve',d:'reject',q:'hold'}[value]);
  }
  return {html, key};
})();
