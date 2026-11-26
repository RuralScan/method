const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const path=require('node:path');
const {destination}=require('../home-route.js');
function setup(hash) {
  const nodes={};
  const node=id=>nodes[id]||(nodes[id]={hidden:false,querySelectorAll(){return [];},click(){this.clicked=true;},classList:{toggle(){}},scrollIntoView(){}});
  const context={location:{hash},history:{replaceState(a,b,h){context.location.hash=h;}},ReviewWorkspace:{onTab(){}},document:{body:{hasAttribute(){return false;}},readyState:'loading',addEventListener(){},getElementById:node,querySelector(){return null;},querySelectorAll(){return [];},documentElement:{style:{setProperty(){}}}}};
  context.window=context;
  vm.runInNewContext(fs.readFileSync(path.join(__dirname,'../dashboard-shell.js'),'utf8'),context);
  return {context,node};
}
test('override deep links open only pending view and survive tab restoration',()=>{
  for(const hash of ['#overrides','#overrides/tree-climate']){
    const {context,node}=setup(hash);context.DashboardShell.openFromHash();
    assert.equal(node('btn-interrogator').clicked,true);
    assert.equal(node('override-review-root').hidden,false);
    assert.equal(node('evidence-section-root').hidden,true);
    assert.equal(node('legacy-analysis-note').hidden,true);
    context.DashboardShell.onTab('tab-interrogator');
    assert.equal(context.location.hash,hash);
  }
});
test('findings and historical links remain separate',()=>{
  for(const [hash,panel] of [['#evidence','evidence-section-root'],['#relationships','relationship-review-root'],['#t4/old','query-explorer-panel']]){
    const {context,node}=setup(hash);context.DashboardShell.openFromHash();
    assert.equal(node(panel).hidden,false);
    assert.equal(node('override-review-root').hidden,true);
    assert.equal(context.location.hash,hash);
  }
});
test('root bookmarks preserve candidate identity and dashboard loads shared reference assets',()=>{
  assert.equal(destination('https://ruralscan.github.io/method/#overrides/tree-climate'),'https://ruralscan.github.io/method/dashboard.html#overrides/tree-climate');
  const html=fs.readFileSync(path.join(__dirname,'../dashboard.html'),'utf8');
  for(const s of ['reference/override-review.css','reference/override-review.js','data-source="reference/data/t4-overrides.json"','data-query-view="overrides"','reference/ch-t4-overrides.html'])assert.ok(html.includes(s),s);
});
