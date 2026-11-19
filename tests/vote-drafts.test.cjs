const {test} = require('node:test');
const assert = require('node:assert/strict');
const {store, key} = require('../review/vote-drafts.js');
const {chunks, receiptBody} = require('../review/batch-receipt.js');
function storage() {
  const result = {};
  Object.defineProperties(result, {
    getItem:{value:k=>result[k] ?? null}, setItem:{value:(k,v)=>{result[k]=v;}}, removeItem:{value:k=>{delete result[k];}}
  });
  return result;
}
const row = {evidence_id:'fixture-wetland', reviewer:'fixture-reader', revision:'a'.repeat(40), lane:'T4', decision:'approve', reason:'', note:''};

test('pre-existing dialog drafts survive and inline edits stay scoped to reviewer, finding and pin', () => {
  const disk = storage(); disk.setItem(key(row),JSON.stringify(row));
  const votes=store(disk);
  const other={...row,reviewer:'second-reader'}, earlier={...row,revision:'b'.repeat(40)};
  votes.save(other); votes.save(earlier);
  votes.save({...row,decision:'reject',reason:'wrong_variable',note:'Wrong variable in quote'});
  assert.equal(votes.get(row).decision,'reject');
  assert.deepEqual(votes.get(other),other); assert.deepEqual(votes.get(earlier),earlier);
  assert.equal(store(disk).list('FIXTURE-READER').length,2);
  assert.deepEqual(votes.pending('fixture-reader',row.revision),{'fixture-wetland':'drop'});
  votes.remove(row); assert.equal(votes.list('fixture-reader').length,1); assert.deepEqual(votes.get(other),other);
});
test('a drop needs a reason and a query needs text; invalid edits preserve saved decision', () => {
  const votes=store(storage()); votes.save(row);
  assert.throws(()=>votes.save({...row,decision:'reject'}),/reason/);
  assert.throws(()=>votes.save({...row,decision:'hold',note:'  '}),/question/);
  assert.throws(()=>votes.save({...row,reviewer:''}),/reviewer/);
  assert.throws(()=>votes.save({...row,revision:'unknown'}),/revision/);
  assert.deepEqual(votes.get(row),row);
  votes.save({...row,decision:'hold',note:'Which rainfall band?'});
  assert.deepEqual(votes.pending(row.reviewer,row.revision),{'fixture-wetland':'flag'});
});
test('all four review queues share one batch; analytical lanes and older pins remain separate', () => {
  const votes=store(storage());
  for (const [id,lane] of [['t3','T3/T6'],['t4','T4'],['t6','T3/T6'],['m2b','M2b']]) votes.save({...row,evidence_id:id,lane});
  votes.save({...row,evidence_id:'old-pin',revision:'b'.repeat(40)});
  const groups=chunks(votes.list(row.reviewer)); assert.equal(groups.length,2);
  const current=groups.find(g=>g[0].revision===row.revision);
  const receipt=JSON.parse(receiptBody(current).split('\n')[1]);
  assert.equal(receipt.lane,'Mixed'); assert.equal(current.length,4); assert.equal(receipt.revision,row.revision);
  assert.match(receipt.payload,/"T3\/T6","t3"/); assert.match(receipt.payload,/"T3\/T6","t6"/);
  assert.match(receipt.payload,/"T4","t4"/); assert.match(receipt.payload,/"M2b","m2b"/);
});
test('corrupt unrelated browser entries are retained and do not erase valid drafts', () => {
  const disk=storage(), votes=store(disk); votes.save(row);
  const corrupt='ruralscan.vote.v1/fixture-reader/broken'; disk.setItem(corrupt,'{'); disk.setItem('vfDecisions','legacy audit only');
  assert.deepEqual(votes.list(row.reviewer),[row]);
  assert.equal(disk.getItem(corrupt),'{'); assert.equal(disk.getItem('vfDecisions'),'legacy audit only');
});
test('storage failure is visible and never claims success or alters existing draft', () => {
  const disk=storage(); disk.setItem(key(row),JSON.stringify(row));
  const votes=store({getItem:disk.getItem,setItem:()=>{throw new Error('QuotaExceededError');}});
  assert.throws(()=>votes.save({...row,note:'new'}),/QuotaExceededError/);
  assert.deepEqual(votes.get(row),row);
});
