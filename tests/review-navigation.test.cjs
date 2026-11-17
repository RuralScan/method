const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');

function setup() {
  const ev = [
    {evidence_id:'wet-op', nbs_id:'wetland_management', use_role:'operational_risk'},
    {evidence_id:'wet-effect', nbs_id:'wetland_management', use_role:'effect_claim'},
    {evidence_id:'wet-site', nbs_id:'wetland_management', use_role:'structural_suitability'},
    {evidence_id:'forest-op', nbs_id:'forest_restoration', use_role:'operational_risk'},
  ];
  const notes = [
    ['mixed','Cross-practice checks','wet-op'], ['mixed','Cross-practice checks','forest-op'],
    ['wet-t3','Hazard checks','wet-effect'], ['wet-t6','Scorecard checks','wet-effect'],
    ['wet-t4','Source checks <draft>','wet-site'], ['forest','Forest checks','forest-op'],
    ['mixed','Cross-practice checks','wet-op'], // duplicated requests count one finding
  ].map(([batch_id,batch_label,evidence_id]) => ({batch_id,batch_label,evidence_id,priority:'high'}));
  const results = {};
  const context = {
    reviewData: {registers:{EV_evidence_register:ev}, review_priorities:notes,
      membership:{T3:['wet-effect'],T6:['wet-effect']}, formerly_cited:{T3:{},T6:{}}},
    _vfScope:{nbs:'wetland_management',table:'M2b',family:'peatland'}, _vfSimpleView:'mine',
    _vfR2T:{operational_risk:'T4',structural_suitability:'T4-suitability',effect_claim:'T3'},
    document:{getElementById:() => results,querySelector:() => null},
    history:{replaceState:(_,__,hash) => { context.hash = hash; }},
    renderVfWorklist:() => {}, vfSimpleQueue:view => { context._vfSimpleView = view; },
    DashboardShell:{openReviewQueue:() => {}}, vfNotice:() => {},
  };
  results.addEventListener = () => {};
  context.window = context;
  vm.createContext(context);
  for (const file of ['dashboard-tables.js','dashboard-priority.js']) {
    vm.runInContext(fs.readFileSync(path.join(__dirname,'..',file),'utf8'),context);
  }
  return {context, api:context.DashboardPriority, results};
}

test('review sets match practice and actual table membership; duplicate requests count once', () => {
  const {context,api} = setup();
  let html = api.controls();
  assert.match(html, /Cross-practice checks<\/span><small>1 finding in this view/);
  assert.doesNotMatch(html, /data-batch="(?:wet-t3|wet-t6|wet-t4|forest)"/);
  for (const [table,id] of [['T3','wet-t3'],['T6','wet-t6'],['T4-suitability','wet-t4']]) {
    context._vfScope.table = table;
    html = api.controls();
    assert.ok(html.includes('data-batch="'+id+'"'));
    assert.ok(!html.includes('data-batch="forest"'));
    assert.ok(!html.includes('data-batch="mixed"'));
  }
  assert.match(html, /Source checks &lt;draft&gt;/);
});

test('search and explicit all-sets browsing expose hidden sets without changing queue scope', () => {
  const {context,api,results} = setup();
  const scope = context._vfScope;
  api.filterSets('FOREST', false);
  assert.match(results.innerHTML, /No review sets match/);
  api.filterSets('FOREST', true);
  assert.match(results.innerHTML, /data-batch="forest"/);
  assert.doesNotMatch(results.innerHTML, /data-batch="wet-t4"/);
  assert.equal(context._vfScope, scope);
  api.choose('forest');
  assert.equal(context._vfScope.nbs, 'forest_restoration');
  assert.equal(context._vfScope.table, 'M2b');
  assert.equal(context.hash, '#review-priority=forest');
});

test('choosing and clearing a scoped set preserve reviewer filters and My reviewed', () => {
  const {context,api} = setup();
  const before = JSON.stringify(context._vfScope);
  api.choose('mixed');
  assert.equal(JSON.stringify(context._vfScope), before);
  assert.equal(context._vfSimpleView, 'mine');
  assert.equal(api.matches({evidence_id:'wet-op'}),true);
  assert.equal(api.matches({evidence_id:'wet-site'}),false);
  api.choose('all');
  assert.equal(context._vfSimpleView, 'mine');
  assert.equal(api.matches({evidence_id:'wet-site'}),true);
});

test('legacy batch links still open full sets; direct findings can return to scoped queue without priorities', () => {
  const {context,api} = setup();
  assert.equal(api.openFromHash('#review-priority=mixed'),true);
  assert.equal(context._vfScope.nbs,'all');
  assert.equal(context._vfScope.table,'M2b');
  context.reviewData.review_priorities = [];
  context._vfScope = {nbs:'wetland_management',table:'M2b'};
  context._vfPriorityEvidence = 'wet-op';
  assert.match(api.controls(), /Back to queue/);
  api.backToQueue();
  assert.equal(context._vfPriorityEvidence,'');
  assert.equal(context._vfPriority,'all');
  assert.equal(context._vfScope.nbs,'wetland_management');
  assert.equal(context._vfScope.table,'M2b');
  assert.equal(context._vfSimpleView,'todo');
});
