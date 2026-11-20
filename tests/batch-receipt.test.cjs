const {test} = require('node:test');
const assert = require('node:assert/strict');
const {chunks, receiptBody, prepare, matches, history, pending, remember, maxBytes} = require('../review/batch-receipt.js');

const vote = {reviewer:'fixture-reader', decision:'hold', reason:'',
  note:'Check "site",\nthen page 3', revision:'a'.repeat(40), lane:'M2b', evidence_id:'wet-1'};
const decode = rows => JSON.parse(receiptBody(rows).split('\n')[1]);

test('one mixed receipt preserves per-finding lane, CSV quoting, author and pin', () => {
  const rows = [vote,{...vote,evidence_id:'wet-2',lane:'T4'},{...vote,evidence_id:'wet-3',lane:'T3/T6'}];
  assert.deepEqual(chunks(rows),[rows]);
  const entry = decode(rows);
  assert.equal(entry.test,false);
  assert.equal(entry.kind,'csv');
  assert.equal(entry.lane,'Mixed');
  assert.equal(entry.revision,vote.revision);
  assert.match(entry.payload,/^lane,evidence_id,reviewer,decision,reason,note\n"M2b","wet-1","fixture-reader","hold","","Check ""site"",\nthen page 3"/);
  assert.equal(decode([vote]).lane,'M2b');
});

test('different register revisions and synthetic fixture receipts remain separate', () => {
  const rows = [vote,{...vote,revision:'b'.repeat(40)},{...vote,evidence_id:'test_operational_risk'}];
  const groups=chunks(rows);
  assert.equal(groups.length,3);
  assert.deepEqual(groups.map(r=>decode(r).test),[false,false,true]);
});

test('large multibyte notes split without dropping votes at the public receipt size limit', () => {
  const rows=Array.from({length:400},(_,i)=>({...vote,evidence_id:'wet-'+i,note:'水'.repeat(1000)}));
  const groups=chunks(rows);
  assert(groups.length>1);
  assert.deepEqual(groups.flat(),rows);
  for (const group of groups) assert(Buffer.byteLength(receiptBody(group))<=maxBytes);
});

function storage() {
  const disk={}; Object.defineProperties(disk,{getItem:{value:k=>disk[k]??null},setItem:{value:(k,v)=>disk[k]=v}}); return disk;
}
test('small batch is prefilled; large batch downloads one bound CSV without copy/paste',async()=>{
  const small=await prepare([vote]);
  assert.equal(small.attachment,false); assert.equal(new URL(small.url).searchParams.get('body'),small.body);
  assert.match(small.body,/already included/);
  const rows=Array.from({length:90},(_,i)=>({...vote,evidence_id:'wet-'+i,note:'Which source page? '.repeat(20)}));
  assert.equal(chunks(rows).length,1);
  const large=await prepare(rows);assert.equal(large.attachment,true);assert(large.url.length<6000);
  assert.match(large.body,/Attach/);assert(!large.body.includes(large.csv));
  assert.equal(large.meta.bytes,Buffer.byteLength(large.csv));
  assert.equal(large.meta.sha256,require('node:crypto').createHash('sha256').update(large.csv).digest('hex'));
});
test('receipts require matching account, pin, content and attachment; drafts survive changed edits and retries',async()=>{
  const large=await prepare([{...vote,note:'水'.repeat(1000)}]);assert(large.attachment);
  const receipt={number:123,user:{login:vote.reviewer},body:large.body+'\n['+large.filename+'](https://github.com/user-attachments/files/1/'+large.filename+')'};
  assert(matches(receipt,large));
  assert(!matches({...receipt,body:large.body},large));
  assert(!matches({...receipt,user:{login:'another-reviewer'}},large));
  assert(!matches({...receipt,body:receipt.body.replace(large.meta.sha256,'0'.repeat(64))},large));
  assert(!matches({...receipt,pull_request:{}},large));
  const disk=storage();await remember(disk,receipt,large);await remember(disk,receipt,large);
  const saved=history(disk,vote.reviewer);assert.equal(saved.length,1);assert.deepEqual(saved[0].rows,large.rows);
  assert.equal(pending(large.rows,saved).length,0);
  assert.equal(pending([{...large.rows[0],note:'New question'}],saved).length,1);
  assert.equal(pending(large.rows,history(disk,'another-reviewer')).length,1);
  await assert.rejects(remember({setItem:()=>{throw Error('QuotaExceeded');}},receipt,large),/QuotaExceeded/);
  assert.equal(pending(large.rows,[]).length,1);
});
test('old inline receipts remain discoverable; unsafe note markup stays encoded',async()=>{
  const p=await prepare([{...vote,note:'</details> <!-- --> <script>alert(1)</script>'}]);
  assert(!p.body.includes('<script>'));
  const issue={user:{login:vote.reviewer},body:p.legacy,number:5};
  assert(matches(issue,p));
});
