// Verify every browser drill-down against the generated summary, including all scopes and lanes.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const { select, matchStatus } = require('./review-coverage.js');
const root = process.argv[2];
if (!root) throw Error('Pass the built reference directory');
const data = JSON.parse(fs.readFileSync(root + '/data/review-findings.json'));
const summary = JSON.parse(fs.readFileSync(root + '/data/review-coverage.json'));
assert(matchStatus('held', 'awaiting'));
assert(!matchStatus('held', 'reviewed_kept'));
assert(!matchStatus('rejected', 'retained'));
let assertions = 0;
for (const row of summary.rows) {
  const filters = { node: row.node, lane: row.lane, relation: row.relation, q: '' };
  const findings = select(data, { ...filters, state: 'all' });
  const counts = { reviewed_kept: 0, pending: 0, held: 0, rejected: 0 };
  for (const f of findings) counts[f.status]++;
  assert.equal(findings.length, row.registered_total);
  assert.equal(findings.length - counts.rejected, row.retained_total);
  assert.equal(counts.pending + counts.held, row.awaiting);
  for (const field of Object.keys(counts)) assert.equal(counts[field], row[field]);
  assertions += 7;
}
const sample = data.findings.find(f => f.status === 'pending');
assert(select(data, { node: '', lane: 'all', relation: 'included', state: 'pending', q: sample.evidence_id })
  .some(f => f.evidence_id === sample.evidence_id));
assert.equal(select(data, { node: 'missing', lane: 'all', relation: 'included', state: 'all' }).length, 0);
console.log(`${assertions} browser count assertions passed across ${summary.rows.length} scope/lane/relationship selections`);
