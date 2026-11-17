const {test} = require('node:test');
const assert = require('node:assert/strict');
const {chunks,header} = require('../review/priority-receipt.js');
const row = {batch_id:'wetland',evidence_id:'ev',request_sha256:'a'.repeat(64),basis_sha256:'b'.repeat(64),last_receipt:null};
const revision='c'.repeat(40);

test('priority receipt carries exact targets and reason, without a claimed voter or finding decision',()=>{
  const [result]=chunks([row,row],revision,'addressed','Applied in receipt #29.');
  const entry=JSON.parse(result.body.slice(header.length));
  assert.equal(result.count,1);assert.equal(entry.kind,'priority');assert.equal(entry.action,'addressed');
  assert.deepEqual(entry.targets,[row]);assert.equal(entry.reason,'Applied in receipt #29.');
  assert(!Object.hasOwn(entry,'reviewer'));assert(!Object.hasOwn(entry,'decision'));
  for(const action of ['approve','drop','hold'])assert.throws(()=>chunks([row],revision,action,'reason'));
  assert.throws(()=>chunks([row],revision,'restore',' '));
});

test('large sets split losslessly under GitHub size limits and stale metadata is refused',()=>{
  const rows=Array.from({length:650},(_,i)=>({...row,evidence_id:'ev_'+i,last_receipt:123}));
  const result=chunks(rows,revision,'deprioritize','Checked request. '.repeat(90));
  assert(result.length>1);
  assert.deepEqual(result.flatMap(r=>JSON.parse(r.body.slice(header.length)).targets),rows);
  assert(result.every(r=>new TextEncoder().encode(r.body).length<=60000));
  assert.throws(()=>chunks([{batch_id:'legacy',evidence_id:'ev'}],revision,'restore','Recheck this.'));
});
