const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const code = fs.readFileSync(path.join(__dirname, '..', 'review/workspace.js'), 'utf8');

function setup(table='T4-suitability') {
  const c = {
    _vfScope:{nbs:'wetland_management',table,round:'all',access:'all'},
    reviewData:{registers:{SRC_source_register:[
      {source_id:'open',access_status:'open',extraction_run_id:'original'},
      {source_id:'closed',access_status:'restricted',extraction_run_id:'round2_grey'},
    ]},membership:{T3:[],T6:[]},formerly_cited:{T3:{},T6:{}}},
    document:{getElementById:()=>({addEventListener(){}})},
    DashboardPriority:{matches:()=>true,needsAttention:()=>false,leaveFocus:()=>{c._vfPriorityEvidence='';}},
    renderVfWorklist:()=>{}, vfHasAnswerForReview:()=>false, vfClarificationsFor:()=>[],
  };
  c.window = c; vm.createContext(c);
  for (const name of ['vfFilterState','vfShortcutFilters','vfShortcutSelected','vfWriteFilters','vfShortcut',
    'vfSetFilter','vfReviewQueue','vfSimpleQueue','vfFollowUpMatch','vfMatchesFilters','vfShowPersonalHistory',
    'vfIsSiteObservation','_vfInScope','_vfRoundMap','_vfRoundKey','_vfSrcOAMap','_vfIsOA','_vfTabular']) {
    const start=code.indexOf('  function '+name+'(');assert.notEqual(start,-1,name);
    vm.runInContext(code.slice(start,code.indexOf('\n  function ',start+1)),c);
  }
  vm.runInContext(fs.readFileSync(path.join(__dirname,'..','dashboard-tables.js'),'utf8'),c);
  function row(id, role, options={}) {
    return {origin:'passed',verdict:'pass',me:false,other:false,myDec:'',meApplied:false,dropped:false,
      ...options, ev:{evidence_id:id,source_id:'open',nbs_id:'wetland_management',use_role:role,
        quote:'synthetic evidence',_reviewQueue:'first',...options.ev}};
  }
  const rows=[];
  for(const [lane,role] of [['T3','effect_claim'],['T4-suitability','structural_suitability'],['T6','effect_claim'],['M2b','operational_risk']]) {
    const make=(id,options)=>row(lane+'_'+id,role,options);
    const laneRows=[make('first'),make('flagged',{origin:'flagged',verdict:'unsupported'}),
      make('other',{other:true,ev:{_reviewQueue:'recorded'}}),
      make('mine',{me:true,meApplied:true,myDec:'ok',ev:{source_id:'closed',_reviewQueue:'recorded'}}),
      make('conflict',{me:true,other:true,meApplied:true,myDec:'ok',origin:'flagged',verdict:'mismatch',ev:{source_id:'closed',_reviewQueue:'unresolved',_reviewConflict:true}}),
      make('drop',{me:true,meApplied:true,myDec:'drop',dropped:true,ev:{source_id:'closed',review_state:'dropped',_reviewQueue:'dropped'}}),
      make('reopened'),make('held',{me:true,meApplied:true,myDec:'flag',ev:{source_id:'closed',_reviewQueue:'unresolved'}}),
      make('pendingDrop',{me:true,meApplied:false,myDec:'drop',ev:{source_id:'closed'}})];
    rows.push(...laneRows);
    if(c.reviewData.membership[lane])c.reviewData.membership[lane]=laneRows.map(r=>r.ev.evidence_id);
  }
  const ids = overrides => rows.filter(u=>c._vfInScope(u.ev,true)&&c.vfMatchesFilters(u,overrides)).map(u=>u.ev.evidence_id.replace(table+'_',''));
  return {c,rows,ids};
}

for(const lane of ['T3','T4-suitability','T6','M2b']) {
  test(lane+': original shortcuts select the same sidebar filters and exact prospective counts',()=>{
    const {c,ids}=setup(lane);
    const expected={todo:['first','flagged','other','reopened'],flagged:['flagged'],passed:['first','other','reopened'],
      second:['other'],kept:['mine','conflict'],queried:['held'],dropped:['drop','pendingDrop'],mine:['mine','conflict','drop','held','pendingDrop'],
      conflict:['conflict'],answers:[]};
    for(const [key,want] of Object.entries(expected)) {
      const preview=ids(c.vfShortcutFilters(key));
      c.vfShortcut(key);
      assert.deepEqual(ids(),want,key);assert.deepEqual(ids(),preview,key+' count');
      assert.ok(c.vfShortcutSelected(key));
      for(const [axis,value] of Object.entries(c.vfShortcutFilters(key)))assert.equal(c.vfFilterState()[axis],value);
    }
    c.vfShortcut('flagged');c.vfSetFilter('me','any');
    assert.deepEqual(ids(),['flagged','conflict']);assert.equal(c._vfAxOrigin,'flagged');
    assert.equal(c.vfShortcutSelected('flagged'),false);
    c.vfSetFilter('me','no');assert.ok(c.vfShortcutSelected('flagged'));
    c.vfShortcut('todo');c.vfSetFilter('other','yes');
    assert.deepEqual(ids(),['other']);assert.ok(c.vfShortcutSelected('second'));
  });
  test(lane+': every sidebar candidate count equals selection without changing other axes',()=>{
    const {c,ids}=setup(lane);
    for(const shortcut of ['todo','mine','queried','conflict']) {
      for(const [axis,values] of Object.entries({status:['active','dropped','any'],origin:['any','flagged','passed'],me:['any','no','yes'],other:['any','no','yes'],call:['all','ok','query','drop'],followup:['all','answers','waiting','conflict','requested'],verdict:['all','mismatch','unsupported'],tables:[false,true]})) {
        for(const value of values) {
          c.vfShortcut(shortcut);const before=c.vfFilterState();const candidate=ids({[axis]:value});
          c.vfSetFilter(axis,value);assert.deepEqual(ids(),candidate,shortcut+' / '+axis+' / '+value);
          for(const key of Object.keys(before))if(key!==axis)assert.equal(c.vfFilterState()[key],before[key],key+' preserved');
        }
      }
    }
  });
}

test('round, access, search and selected task refine shortcuts rather than get reset',()=>{
  const {c,ids}=setup();c._vfScope.round='round2';c._vfScope.access='restricted';c._vfSearch='held';
  c.vfShortcut('mine');assert.deepEqual(ids(),['held']);
  assert.equal(c._vfScope.round,'round2');assert.equal(c._vfScope.access,'restricted');assert.equal(c._vfSearch,'held');
  c.DashboardPriority.matches=ev=>ev.evidence_id.endsWith('_mine');assert.deepEqual(ids(),[]);
  c.DashboardPriority.matches=()=>true;c._vfSearch='';
  assert.deepEqual(ids({round:'round1'}),[]);
  assert.deepEqual(ids({round:'round2'}),['mine','conflict','drop','held','pendingDrop']);
});

test('answered questions and requested rechecks are explicit; they cannot bypass Reviewed by me',()=>{
  const {c,ids}=setup();c.vfHasAnswerForReview=id=>id.endsWith('_held');
  c.DashboardPriority.needsAttention=ev=>ev.evidence_id.endsWith('_mine');
  c.vfShortcut('todo');assert.deepEqual(ids(),['first','flagged','other','reopened']);
  c.vfShortcut('answers');assert.deepEqual(ids(),['held']);assert.equal(c._vfAxMe,'any');
  c.vfSetFilter('me','no');assert.deepEqual(ids(),[]);
  c.vfShortcut('requested');assert.deepEqual(ids(),['mine']);assert.equal(c._vfFollowUp,'requested');
  c.vfSetFilter('me','no');assert.deepEqual(ids(),[]);
  c.vfShortcut('waiting');assert.deepEqual(ids(),[]);
  c.vfHasAnswerForReview=()=>false;assert.deepEqual(ids(),['held']);
});

test('verdict filters never silently switch off for AI-passed origin',()=>{
  const {c,ids}=setup();c.vfShortcut('passed');c.vfSetFilter('verdict','unsupported');
  assert.deepEqual(ids(),[]);assert.equal(c._vfVerdictFilter,'unsupported');
  c.vfSetFilter('origin','flagged');assert.deepEqual(ids(),['flagged']);
});

test('former citations remain in personal/dropped history; archived ratings do not inflate refined findings',()=>{
  const {c,rows,ids}=setup();rows.find(r=>r.ev.evidence_id==='T4-suitability_drop').formerlyCited=true;
  c.vfShortcut('mine');assert.ok(ids().includes('drop'));assert.equal(c.vfShowPersonalHistory(),true);
  c.vfSetFilter('origin','passed');assert.equal(c.vfShowPersonalHistory(),false);
  c.vfShortcut('mine');c._vfScope.round='round2';assert.equal(c.vfShowPersonalHistory(),false);
  c.vfShortcut('todo');assert.ok(!ids().includes('drop'));
});

test('legacy finding route can show decided/dropped records; shortcuts leave focus but keep the task',()=>{
  const {c,ids}=setup();c._vfPriority='fixture-task';c._vfPriorityEvidence='T4-suitability_drop';
  c.vfSimpleQueue('advanced');assert.equal(c._vfPriorityEvidence,'T4-suitability_drop');assert.ok(ids().includes('drop'));
  c.vfShortcut('todo');assert.equal(c._vfPriorityEvidence,'');assert.equal(c._vfPriority,'fixture-task');
});


test('pending local responses leave answered/recheck work until submitted or undone',()=>{
  const {c,rows,ids}=setup();const row=rows.find(r=>r.ev.evidence_id==='T4-suitability_held');
  c.vfHasAnswerForReview=id=>id===row.ev.evidence_id;
  c.DashboardPriority.needsAttention=ev=>ev.evidence_id===row.ev.evidence_id;
  for(const key of ['answers','requested']) {
    row.meApplied=true;c.vfShortcut(key);assert.deepEqual(ids(),['held']);
    row.meApplied=false;assert.deepEqual(ids(),[]);
  }
});

test('feedback captures and restores the shared filters, search and task; old notes still open',()=>{
  const {c}=setup();const feedback=fs.readFileSync(path.join(__dirname,'..','dashboard-feedback.js'),'utf8');
  Object.assign(c,{page:'/dashboard.html',tabParam:()=> 'tab-qaqc',clean:s=>s,noteTab:()=> 'tab-qaqc',
    DashboardShell:{},setTimeout:()=>{},document:{
      getElementById:()=>({hidden:true}),querySelectorAll:()=>[],
      querySelector:sel=>sel==='.tab-btn.active'?{textContent:'Review'}:{dataset:{reviewView:'queue'},click(){}}
    }});
  for(const name of ['context','jump']) {
    const start=feedback.indexOf('  function '+name+'(');
    vm.runInContext(feedback.slice(start,feedback.indexOf('\n  function ',start+1)),c);
  }
  c.vfShortcut('second');c.vfSetFilter('origin','flagged');c._vfSearch='paper';c._vfPriority='task';c._vfPriorityView='history';
  const saved=c.context();const filters=JSON.stringify(c.vfFilterState());
  c.vfShortcut('mine');c._vfSearch='';c._vfPriority='all';c._vfPriorityView='attention';
  c.jump({page:c.page,context:saved});
  assert.equal(JSON.stringify(c.vfFilterState()),filters);assert.equal(c._vfSearch,'paper');
  assert.equal(c._vfPriority,'task');assert.equal(c._vfPriorityView,'history');
  c.jump({page:c.page,context:{scope:{view:'queue',reviewQueue:'mine'}}});
  assert.ok(c.vfShortcutSelected('mine'));
});
