/* Keep existing browser drafts readable; scope every edit to reviewer and revision. */
const VoteDrafts = (() => {
  const prefix = 'ruralscan.vote.v1/';
  const key = r => prefix + [r.reviewer.toLowerCase(), r.revision, r.evidence_id].map(encodeURIComponent).join('/');
  const legacyDecision = value => ({approve:'ok', reject:'drop', hold:'flag'})[value] || '';
  function validate(row) {
    if (!/^[a-z0-9](?:[a-z0-9-]{0,37}[a-z0-9])?$/i.test(row.reviewer || '')) throw Error('Choose your GitHub reviewer name above the queue first.');
    if (!/^[a-f0-9]{40}$/.test(row.revision || '') || !row.evidence_id || !['T4','T3/T6','M2b'].includes(row.lane)) throw Error('Finding revision unavailable. Reload the queue before reviewing.');
    if (!legacyDecision(row.decision)) throw Error('Choose Keep, Drop or Query.');
    if (row.decision === 'reject' && !row.reason?.trim()) throw Error('Choose a reason before Drop.');
    if (row.decision === 'hold' && !row.note?.trim()) throw Error('Write your question before Query.');
    if ((row.note || '').length > 1000) throw Error('Keep the note within 1,000 characters.');
    return row;
  }
  function store(storage) {
    const get = row => {
      try { return JSON.parse(storage.getItem(key(row)) || 'null'); } catch { return null; }
    };
    const list = reviewer => {
      if (!reviewer) return [];
      const scope = prefix + encodeURIComponent(reviewer.toLowerCase()) + '/';
      return Object.keys(storage).filter(k => k.startsWith(scope)).sort().flatMap(k => {
        try { const row = JSON.parse(storage.getItem(k)); return row && key(row) === k ? [row] : []; } catch { return []; }
      });
    };
    return {get, list, save(row) { validate(row); storage.setItem(key(row), JSON.stringify(row)); return row; },
      remove(row) { storage.removeItem(key(row)); },
      pending(reviewer, revision) { return Object.fromEntries(list(reviewer).filter(r => r.revision === revision).map(r => [r.evidence_id, legacyDecision(r.decision)])); }};
  }
  return {key, validate, store, legacyDecision};
})();
if (typeof module !== 'undefined') module.exports = VoteDrafts;
