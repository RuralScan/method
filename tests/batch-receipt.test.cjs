const {test} = require('node:test');
const assert = require('node:assert/strict');
const {chunks, receiptBody} = require('../review/batch-receipt.js');

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
  const rows=Array.from({length:100},(_,i)=>({...vote,evidence_id:'wet-'+i,note:'水'.repeat(1000)}));
  const groups=chunks(rows);
  assert(groups.length>1);
  assert.deepEqual(groups.flat(),rows);
  for (const group of groups) assert(Buffer.byteLength(receiptBody(group))<=65000);
});
