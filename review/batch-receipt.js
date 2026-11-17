/* Wire format consumed by RuralScan/evidence workflows/submissions/intake.py. */
const BatchReceipt = (() => {
  const fixtures = {T4:'test_bench_terrace', 'T3/T6':'test_hazard_scorecard', M2b:'test_operational_risk'};
  const header = 'RuralScan submission v1\n';
  const size = str => new TextEncoder().encode(str).length;
  function receiptBody(rows) {
    const lanes = new Set(rows.map(r => r.lane));
    const lane = lanes.size === 1 ? rows[0].lane : 'Mixed';
    const fields = ['evidence_id','reviewer','decision','reason','note'];
    if (lane === 'Mixed') fields.unshift('lane');
    const cell = v => '"' + v.replaceAll('"','""') + '"';
    const csv = [fields.join(','), ...rows.map(row => fields.map(f => cell(row[f])).join(','))].join('\n');
    return header + JSON.stringify({kind:'csv',lane,revision:rows[0].revision,
      test:rows[0].evidence_id === fixtures[rows[0].lane],payload:csv});
  }
  function chunks(rows) {
    const groups = new Map();
    for (const r of rows) {
      const group = r.revision + '/' + (r.evidence_id === fixtures[r.lane]);
      if (!groups.has(group)) groups.set(group,[[]]);
      const batches = groups.get(group);
      if (size(receiptBody([...batches.at(-1),r])) > 65000 && batches.at(-1).length) batches.push([]);
      batches.at(-1).push(r);
    }
    return [...groups.values()].flat();
  }
  return {receiptBody, chunks, fixtures, header};
})();
if (typeof module !== 'undefined') module.exports = BatchReceipt;
