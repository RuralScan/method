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
  results.focus = () => { results.focused = true; };
  results.scrollIntoView = () => { results.scrolled = true; };
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
  assert.match(html, /<small>1 finding<\/small>/);
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
  assert.match(results.innerHTML, /No tasks match/);
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

test('shared addressed requests leave active priorities, stay in history, and changed inputs return', () => {
  const {context,api} = setup();
  for (const r of context.reviewData.review_priorities) if(r.batch_id==='mixed') {
    r.status='addressed';r.history=[{actor:'fixture',date:'2026-11-17',action:'addressed',reason:'Correction applied <checked>',receipt:501,current:true}];
  }
  api.choose('high');
  assert.equal(api.matches({evidence_id:'wet-op'}),false);
  assert.doesNotMatch(api.controls(),/data-batch="mixed"/);
  assert.match(api.badge({evidence_id:'wet-op'}),/Earlier review priority/);
  const history=api.card({evidence_id:'wet-op'});
  assert.match(history,/Request addressed/);
  assert.match(history,/Correction applied &lt;checked&gt;/);
  assert.match(history,/issues\/501/);
  api.setView('history');
  assert.equal(api.matches({evidence_id:'wet-op'}),true);
  assert.match(api.controls(),/data-batch="mixed"/);
  for(const r of context.reviewData.review_priorities) if(r.batch_id==='mixed')r.status='recheck';
  api.setView('attention');
  assert.equal(api.matches({evidence_id:'wet-op'}),true);
});


test('selected active requests remain reviewable after an earlier finding decision', () => {
  const {context,api} = setup();
  const html=fs.readFileSync(path.join(__dirname,'..','dashboard.html'),'utf8');
  vm.runInContext(html.match(/  function vfSimpleMatch\(u,view\)\{[\s\S]*?\n  \}/)[0],context);
  context.vfHasAnswerForReview=()=>false;context.vfClarificationsFor=()=>[];
  const unit={ev:{evidence_id:'wet-op',_reviewQueue:'recorded'},me:true,meApplied:true};
  assert.equal(context.vfSimpleMatch(unit,'todo'),false);
  api.choose('mixed');
  assert.equal(context.vfSimpleMatch(unit,'todo'),true);
  assert.equal(context.vfSimpleMatch({...unit,dropped:true},'todo'),true);
  assert.equal(context.vfSimpleMatch({...unit,formerlyCited:true},'todo'),true);
  assert.equal(context.vfSimpleMatch({...unit,meApplied:false},'todo'),false);
  assert.equal(context.vfSimpleMatch(unit,'mine'),true);
  assert.equal(context.vfSimpleMatch({...unit,me:false},'mine'),false);
  for(const r of context.reviewData.review_priorities)if(r.evidence_id==='wet-op')r.status='addressed';
  assert.equal(context.vfSimpleMatch(unit,'todo'),false);
  for(const r of context.reviewData.review_priorities)if(r.evidence_id==='wet-op')r.status='recheck';
  assert.equal(context.vfSimpleMatch(unit,'todo'),true);
});


test('task pages stay bounded, search resets paging, and opening moves to findings without voting', () => {
  const {context,api,results}=setup();
  for(let i=0;i<14;i++) context.reviewData.review_priorities.push({batch_id:'extra-'+i,batch_label:'Extra task '+i,evidence_id:'wet-op',status:'active'});
  let html=api.controls();
  assert.equal((html.match(/aria-label="Open findings:/g)||[]).length,6);
  assert.match(html,/Read the requested check/);
  assert.match(html,/Next tasks/);
  api.turnPage(1);
  assert.match(results.innerHTML,/Tasks 7–12 of 15/);
  api.filterSets('Extra task 13',false);
  assert.match(results.innerHTML,/Open findings: Extra task 13/);
  assert.doesNotMatch(results.innerHTML,/Previous tasks/);
  const data=JSON.stringify(context.reviewData),scope=JSON.stringify(context._vfScope);
  api.openTask('extra-13');
  assert.equal(context._vfPriority,'extra-13');
  assert.equal(context._vfSimpleView,'mine');
  assert.equal(JSON.stringify(context._vfScope),scope);
  assert.equal(JSON.stringify(context.reviewData),data);
  assert.equal(results.scrolled,true);assert.equal(results.focused,true);
});
