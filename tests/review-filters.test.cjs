const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');

// Exercise the functions used by the actual queue, rather than a duplicate filter model.
const html = fs.readFileSync(path.join(__dirname, '..', 'review/workspace.js'), 'utf8');
function setup() {
  const c = {
    _vfSimpleView:'todo', _vfAxStatus:'active', _vfAxOrigin:'any', _vfAxMe:'any', _vfAxOther:'any',
    _vfScope:{nbs:'wetland_management',table:'T4-suitability',round:'all',access:'all'},
    _vfMyCall:'all', _vfReconcile:'all', _vfVerdictFilter:'all',
    reviewData:{registers:{SRC_source_register:[
      {source_id:'open',access_status:'open',extraction_run_id:'original'},
      {source_id:'closed',access_status:'restricted',extraction_run_id:'round2_grey'},
    ]}},
    DashboardPriority:{matches:()=>true,needsAttention:()=>false},
    DashboardTables:{matches:()=>true}, vfHasAnswerForReview:()=>false, vfClarificationsFor:()=>[],
  };
  c.window = c; vm.createContext(c);
  for (const name of ['vfSimpleMatch','vfMatchesFilters','vfIsSiteObservation','_vfInScope',
    '_vfRoundMap','_vfRoundKey','_vfSrcOAMap','_vfIsOA','_vfTabular']) {
    const start = html.indexOf('  function '+name+'(');
    assert.notEqual(start,-1,name);
    const end = html.indexOf('\n  function ',start+1);
    vm.runInContext(html.slice(start,end),c);
  }
  function row(id, options={}) {
    return {origin:'passed',verdict:'pass',me:false,other:false,myDec:'',meApplied:false,dropped:false,
      ...options, ev:{evidence_id:id,source_id:'open',nbs_id:'wetland_management',use_role:'structural_suitability',
        quote:'synthetic evidence',_reviewQueue:'first',...options.ev}};
  }
  const rows = [row('first'), row('flagged',{origin:'flagged',verdict:'unsupported'}),
    row('other',{other:true,ev:{_reviewQueue:'recorded'}}),
    row('mine',{me:true,meApplied:true,myDec:'ok',ev:{source_id:'closed',_reviewQueue:'recorded'}}),
    row('conflict',{me:true,other:true,meApplied:true,myDec:'ok',origin:'flagged',verdict:'mismatch',ev:{source_id:'closed',_reviewQueue:'unresolved',_reviewConflict:true}}),
    row('drop',{me:true,meApplied:true,myDec:'drop',dropped:true,ev:{source_id:'closed',review_state:'dropped',_reviewQueue:'dropped'}}),
    row('reopened'), row('held',{me:true,meApplied:true,myDec:'flag',ev:{source_id:'closed',_reviewQueue:'unresolved'}})];
  const ids = overrides => rows.filter(u=>c._vfInScope(u.ev,true)&&c.vfMatchesFilters(u,overrides)).map(u=>u.ev.evidence_id);
  return {c,rows,ids};
}

test('status candidates use the custom view that clicking selects, even from an empty To review queue',()=>{
  const {c,ids}=setup();
  assert.deepEqual(ids(),['first','flagged','conflict','reopened']);
  assert.deepEqual(ids({view:'advanced',status:'dropped'}),['drop']);
  assert.equal(ids({view:'advanced',status:'active'}).length,7);
  assert.equal(ids({view:'advanced',status:'any'}).length,8);
  c._vfSearch='mine';
  assert.deepEqual(ids(),[]);
  assert.deepEqual(ids({view:'advanced',me:'yes'}),['mine']);
});

test('origin, own review and other-reviewer axes compose without losing committed history',()=>{
  const {ids}=setup();
  assert.deepEqual(ids({view:'advanced',origin:'flagged'}),['flagged','conflict']);
  assert.equal(ids({view:'advanced',origin:'passed'}).length,5);
  assert.deepEqual(ids({view:'advanced',me:'yes'}),['mine','conflict','held']);
  assert.deepEqual(ids({view:'advanced',me:'no',other:'yes'}),['other']);
  assert.deepEqual(ids({view:'advanced',me:'yes',other:'yes'}),['conflict']);
});

test('round counts retain queue, reviewer, search and priority filters',()=>{
  const {c,ids}=setup();
  assert.deepEqual(ids({round:'round1'}),['first','flagged','reopened']);
  assert.deepEqual(ids({round:'round2'}),['conflict']);
  c._vfSimpleView='advanced'; c._vfAxMe='yes';
  assert.deepEqual(ids({round:'round1'}),[]);
  assert.deepEqual(ids({round:'round2'}),['mine','conflict','held']);
  c._vfScope.round='round1';
  assert.deepEqual(ids({round:'round2'}),['mine','conflict','held']);
  c._vfSearch='held';
  assert.deepEqual(ids({round:'round2'}),['held']);
  c.DashboardPriority.matches=ev=>ev.evidence_id==='mine';
  assert.deepEqual(ids({round:'round2'}),[]);
});

test('access combines with history status and search round',()=>{
  const {c,ids}=setup();
  c._vfScope.access='oa';
  assert.deepEqual(ids(),['first','flagged','reopened']);
  c._vfScope.access='restricted';
  assert.deepEqual(ids(),['conflict']);
  assert.deepEqual(ids({view:'advanced',status:'dropped'}),['drop']);
  assert.deepEqual(ids({view:'advanced',status:'dropped',round:'round1'}),[]);
});

test('committed conflicts work without a local decisions store; stale verdict does not hide passed evidence',()=>{
  const {c,ids}=setup();
  c._vfAllReviews={};
  assert.deepEqual(ids({view:'advanced',verdict:'conflict'}),['conflict']);
  assert.equal(ids({view:'advanced',origin:'passed',verdict:'unsupported'}).length,5);
  c._vfMyCall='query';
  assert.deepEqual(ids({view:'advanced',me:'yes'}),['held']);
});

test('former table citations stay in dropped/all history and My reviewed, not active queue',()=>{
  const {c,rows,ids}=setup(); rows.find(r=>r.ev.evidence_id==='drop').formerlyCited=true;
  assert.deepEqual(ids({view:'advanced',status:'dropped'}),['drop']);
  assert.ok(ids({view:'advanced',status:'any'}).includes('drop'));
  assert.ok(ids({view:'mine'}).includes('drop'));
  assert.ok(!ids().includes('drop'));
});
