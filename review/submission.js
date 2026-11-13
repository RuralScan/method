/* GitHub supplies the author's identity and the public issue receipt. */
(() => {
  const dialog = document.getElementById('finding-submission');
  const form = dialog.querySelector('form');
  const verdict = form.elements.verdict;
  const reason = form.elements.reason;
  const fixtureIds = {T4:'test_bench_terrace', 'T3/T6':'test_hazard_scorecard'};

  document.addEventListener('click', event => {
    const trigger = event.target.closest('.finding-submit');
    if (!trigger) return;
    form.reset();
    form.dataset.finding = trigger.dataset.finding;
    form.dataset.revision = trigger.dataset.revision;
    form.dataset.lane = trigger.dataset.lane;
    dialog.querySelector('output').textContent = trigger.dataset.lane + ' · ' + trigger.dataset.finding;
    const codes = [...new Set([..._VF_RC_PASSED, ..._VF_RC_FLAGGED])];
    reason.replaceChildren(new Option('Choose a reason', ''), ...codes.map(c => new Option(c.replaceAll('_',' '), c)));
    reason.required = false;
    dialog.showModal();
  });
  verdict.addEventListener('change', () => { reason.required = verdict.value === 'reject'; });
  dialog.querySelector('[data-cancel]').addEventListener('click', () => dialog.close());
  form.addEventListener('submit', event => {
    event.preventDefault();
    const {finding, revision, lane} = form.dataset;
    const test = fixtureIds[lane] === finding;
    const record = {kind:'vote', lane, revision, test, payload:{evidence_id:finding,
      decision:verdict.value, reason:reason.value, note:form.elements.note.value}};
    const params = new URLSearchParams({
      title:(test ? 'TEST · ' : '') + lane + ' · finding review · ' + finding,
      body:'RuralScan submission v1\n' + JSON.stringify(record)
    });
    location.assign('https://github.com/RuralScan/evidence/issues/new?' + params);
  });
})();
