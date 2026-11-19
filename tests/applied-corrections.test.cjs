const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');

function render(events, notes = []) {
  const reviewData = {review_priorities: notes, corrections: events && {fixture: events}};
  const context = {window: {}, reviewData};
  const code = fs.readFileSync(path.join(__dirname, '../review/priority.js'), 'utf8');
  vm.runInNewContext(code, context);
  return context.window.DashboardPriority.card({evidence_id:'fixture'});
}

test('an applied finding renders before and after without priority membership', () => {
  const html = render([{receipt:45, date:'2026-11-16', changes:[
    {path:['relationship','observed_max'], before:750, before_unit:'mm', after:1000, after_unit:'mm'},
    {path:['quote'], before:'Original quotation', after:'<img onerror=bad>'},
    {path:['locator'], before:'table 3'},
    {path:['context','source'], after:'0'},
  ]}]);
  for (const value of ['750 mm', '1,000 mm', 'Observed maximum', 'Original quotation', '&lt;img onerror=bad&gt;', 'table 3', 'Not recorded', 'Context · Source', '/issues/45']) {
    assert.ok(html.includes(value), value);
  }
  assert.doesNotMatch(html, /<img/);
});

test('latest correction leads, older corrections and original questions remain accessible', () => {
  const events = [4, 8].map(receipt => ({receipt, date:'2026-11-14', changes:[{path:['page'], before:1, after:2}]}));
  const notes = ['2026-11-06','2026-11-16'].map((requested_date, i) => ({
    evidence_id:'fixture', batch_id:'b', requested_date, decision_needed:'Question '+i
  }));
  const html = render(events, notes);
  assert.ok(html.indexOf('Receipt #8') < html.indexOf('Earlier corrections (1)'));
  assert.ok(html.indexOf('Earlier corrections (1)') < html.indexOf('Receipt #4'));
  assert.match(html, /Original review request · before this correction<\/summary>.*Question 0.*?<\/details>/);
  assert.ok(html.lastIndexOf('Question 1') > html.indexOf('Check any remaining questions'));
});

test('old queue snapshots and unaffected findings show no correction panel', () => {
  assert.equal(render(undefined), '');
  assert.equal(render([]), '');
});
