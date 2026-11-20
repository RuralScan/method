const {test}=require('node:test');
const assert=require('node:assert/strict');
const vm=require('node:vm');
const fs=require('node:fs');
const source=fs.readFileSync(require('node:path').join(__dirname,'../review/inline-review.js'),'utf8');
function card(receipt){
  const context=vm.createContext({window:{_vfReviewer:'fixture-reader'},VoteDrafts:{key:()=> 'key'},
    ReviewBatch:{get:()=>({decision:'approve',reason:'',note:''}),receipt:()=>receipt},
    document:{addEventListener(){}},vfEsc:String,_VF_RC_PASSED:[],_VF_RC_FLAGGED:[],_VF_RC_DESC:{}});
  vm.runInContext(source,context);return vm.runInContext("InlineReview.html('fixture-wetland','T4','a'.repeat(40))",context);
}
test('submitted cards show receipt status and cannot imply local undo withdraws a submitted vote',()=>{
  const submitted=card({number:12,url:'https://github.com/RuralScan/evidence/issues/12',applied:false});
  assert.match(submitted,/Submitted · awaiting validation and processing/);
  assert.match(submitted,/data-undo hidden/);assert(!submitted.includes('not submitted'));
  assert.match(card({number:12,url:'https://github.com/RuralScan/evidence/issues/12',applied:true}),/· Applied/);
  const draft=card(null);assert.match(draft,/not submitted/);assert(!draft.includes('data-undo hidden'));
});
