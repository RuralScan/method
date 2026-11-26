const test = require('node:test');
const assert = require('node:assert/strict');
const view = require('./override-review.js');
function model() {
  return {format:'ruralscan.override-review.v1',revision:'a'.repeat(40),activate:false,runtime_implemented:false,scientific_acceptance:'pending',examples:[{id:'mangrove-partial-unit',candidate_id:'shared',inputs:{},result:{state:'partial_unit',score:0,area_ha:null,area_lower_ha:0,area_upper_ha:100}}],records:[{sha256:'b'.repeat(64),curves:[],candidate:{id:'shared',format:'ruralscan.t4-profile-candidate.v1',status:'pending',activate:false,evidence_refs:[{url:'javascript:alert(1)',citation:'<script>unsafe</script>',locator:'page 1'}],justification:{rationale:'<img src=x onerror=alert(1)>'},profile:{type:'precomputed_unit_index',scope:[{nbs_id:'one',family_id:'first',subpractice_ids:[]},{nbs_id:'two',family_id:'second',subpractice_ids:[]}],inputs:{},score_input:'native',area_input:'restorable_km2',area_to_hectares:100,area_policy:'bounds'}}}]};
}
test('scope filters match one declared scope without duplicating multi-practice rules',()=>{
  const m=view.validate(model());
  assert.equal(view.select(m).length,1);
  assert.equal(view.select(m,'two','second').length,1);
  assert.equal(view.select(m,'one','second').length,0);
  assert.equal(view.select(m,'','','missing').length,0);
});
test('active, accepted, duplicate and unsupported candidates fail closed',()=>{
  for (const mutate of [m=>m.activate=true,m=>m.runtime_implemented=true,m=>m.records[0].candidate.status='accepted',m=>m.records[0].candidate.activate=true,m=>m.records.push(m.records[0]),m=>m.records[0].candidate.profile.type='new_kind']) {
    const m=model(); mutate(m); assert.throws(()=>view.validate(m));
  }
});
test('missing point estimate remains unknown while true zero remains zero',()=>{
  const m=model(), html=view.renderCard(m.records[0],m);
  assert.match(html,/<td>0<\/td><td>Unknown \/ not assigned<\/td><td>0<\/td><td>100<\/td>/);
  assert.match(html,/Inactive · unimplemented/);
  assert.match(html,/Source admission is separate from finding Keep/);
  assert.doesNotMatch(html,/<button|<form/);
});
test('source text is escaped and unsafe source URLs cannot become links',()=>{
  const m=model(), html=view.renderCard(m.records[0],m);
  assert.match(html,/&lt;script&gt;unsafe/);
  assert.doesNotMatch(html,/<img|<script|href="javascript:/);
  assert.equal(view.safeUrl('javascript:alert(1)'),'');
  assert.equal(view.safeUrl('https://example.org/paper'),'https://example.org/paper');
});
test('candidate deep links retain the complete identifier and minimum nesting',()=>{
  assert.equal(view.routeId('#overrides/shared'),'shared');
  assert.equal(view.routeId('#evidence'),'');
  assert.equal(view.expression({kind:'minimum',children:[{kind:'logistic',input:'aridity'},{kind:'minimum',children:[{kind:'logistic',input:'thermal_mean'},{kind:'logistic',input:'thermal_days'}]}]}),'minimum(aridity support, minimum(thermal mean support, thermal days support))');
});
