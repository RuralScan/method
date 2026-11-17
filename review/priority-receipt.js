/* A priority receipt changes triage only; it is never a finding vote. */
(function(root) {
  'use strict';
  const header = 'RuralScan review priority v1\n';
  const fields = ['batch_id','evidence_id','request_sha256','basis_sha256','last_receipt'];
  function chunks(rows, revision, action, reason) {
    if (!/^[0-9a-f]{40}$/.test(revision) || !['addressed','deprioritize','restore'].includes(action)) throw Error('Choose a priority action for the current register revision.');
    if (reason.trim().length < 3 || reason.length > 2000 || reason.includes('\0')) throw Error('Enter a reason (3–2000 characters).');
    if (!rows.length) throw Error('No matching requests. Change the priority filter first.');
    const encode = targets => header + JSON.stringify({kind:'priority',revision,action,reason,targets});
    const groups = [[]], seen = new Set();
    for (const row of rows) {
      const key = JSON.stringify([row.batch_id,row.evidence_id]);
      if (seen.has(key)) continue;
      seen.add(key);
      if (!fields.every(k => Object.hasOwn(row,k))) throw Error('Reload the queue to get current priority records.');
      const target = Object.fromEntries(fields.map(k => [k,row[k]]));
      const candidate = [...groups.at(-1),target];
      if ((candidate.length > 500 || new TextEncoder().encode(encode(candidate)).length > 60000) && groups.at(-1).length) groups.push([]);
      groups.at(-1).push(target);
    }
    return groups.map(targets => ({count:targets.length,body:encode(targets)}));
  }
  const api = {header,chunks};
  if (typeof module !== 'undefined') module.exports = api;
  else root.PriorityReceipt = api;
})(typeof window === 'undefined' ? {} : window);
