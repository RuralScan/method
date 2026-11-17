/* Prepare an authenticated team-priority receipt. No optimistic queue changes. */
(() => {
  'use strict';
  const dialog = document.createElement('dialog');
  dialog.id = 'priority-status'; dialog.setAttribute('aria-labelledby','priority-status-title');
  dialog.innerHTML = '<form><h2 id="priority-status-title">Update team priority</h2><p class="priority-targets"></p>'
    + '<p>Updates shared review priority only. Takes effect after the receipt is applied through a protected PR.</p>'
    + '<label>Action<select name="action" required><option value="">Choose…</option><option value="addressed">Addressed — request completed</option><option value="deprioritize">Deprioritize — keep for later</option><option value="restore">Restore — needs attention</option></select></label>'
    + '<label>Reason for the team<textarea name="reason" required minlength="3" maxlength="2000" rows="4" placeholder="What was addressed, superseded, or should wait? Include a receipt or change link when available."></textarea></label>'
    + '<p>Your signed-in GitHub account records the author. The reason is public.</p><button type="submit">Prepare GitHub receipt</button> <button type="button" class="priority-close">Cancel</button>'
    + '<output role="status"></output><div class="priority-receipts"></div></form>';
  document.body.append(dialog);
  const form = dialog.querySelector('form'), output = dialog.querySelector('output'), links = dialog.querySelector('.priority-receipts');
  let targets = [], revision = '';
  function open(batch, evidence) {
    const units = new Map([...(reviewData.registers.EV_evidence_register || []),...(reviewData._evDropped || [])].map(e => [e.evidence_id,e]));
    const scope = window._vfScope || {};
    targets = (reviewData.priority_requests || []).filter(r => r.batch_id === batch &&
      (evidence ? r.evidence_id === evidence : DashboardPriority.visibleRequest(r) &&
        (scope.nbs === 'all' || !scope.nbs || units.get(r.evidence_id)?.nbs_id === scope.nbs) &&
        units.has(r.evidence_id) && DashboardTables.matches(units.get(r.evidence_id),scope.table,true)));
    revision = reviewData.registerRevision;
    form.reset(); output.textContent = ''; links.replaceChildren();
    dialog.querySelector('.priority-targets').textContent = targets.length + ' review request'+(targets.length===1?'':'s')+' · '+(targets[0]?.batch_label || batch);
    if (!targets.length) output.textContent = 'No matching requests. Choose another priority filter or reload the queue.';
    dialog.showModal();
  }
  form.addEventListener('input',() => { links.replaceChildren(); output.textContent = ''; });
  form.addEventListener('submit',event => {
    event.preventDefault(); links.replaceChildren();
    try {
      const groups = PriorityReceipt.chunks(targets,revision,form.elements.action.value,form.elements.reason.value);
      output.textContent = 'Create '+groups.length+' GitHub receipt'+(groups.length===1?'':'s')+'. The team queue stays unchanged until application.';
      groups.forEach((group,i) => {
        const section = document.createElement('section'), link = document.createElement('a');
        const title = 'Review priority · '+form.elements.action.value+' · '+group.count+' request'+(group.count===1?'':'s');
        let url = 'https://github.com/RuralScan/evidence/issues/new?'+new URLSearchParams({title,body:group.body});
        if (url.length > 7500) {
          url = 'https://github.com/RuralScan/evidence/issues/new?'+new URLSearchParams({title});
          const label = document.createElement('label'), box = document.createElement('textarea');
          label.textContent = 'Copy this description into receipt '+(i+1)+' in GitHub';
          box.value = group.body; box.readOnly = true; box.rows = 5; label.append(box); section.append(label);
        }
        link.href = url; link.target = '_blank'; link.rel = 'noopener';
        link.textContent = 'Open GitHub receipt '+(i+1)+' · '+group.count+' request'+(group.count===1?'':'s'); section.append(link); links.append(section);
      });
    } catch(error) { output.textContent = error.message; }
  });
  dialog.querySelector('.priority-close').onclick = () => dialog.close();
  window.PriorityStatus = {open};
})();
