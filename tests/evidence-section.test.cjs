const {test} = require('node:test');
const assert = require('node:assert/strict');
const {buildModel, parseCsv, zip, crc32} = require('../dashboard-evidence.js');

const source = {source_id: 's1', citation: 'Mekdaschi Studer, R.; Liniger, H. (2013). Water harvesting: guidelines to good practice.', url: 'https://example.org/wh', source_category: 'grey'};
const unit = (id, role, variable, relationship, extra = {}) => ({evidence_id: id, source_id: 's1', nbs_id: 'water_harvesting_conservation',
  suitability_family_id: 'water_harvesting__terracing', variable, use_role: role, relationship, quote: 'q', page: '129', locator_type: 'page', claim_basis: 'expert_assertion', ...extra});
const lookups = {
  vont: [{canonical_variable_id: 'annual_precipitation', label: 'Mean annual precipitation'}, {canonical_variable_id: 'crop_yield', label: 'Crop productivity / grain yield'}, {canonical_variable_id: 'erosion_hazard', label: 'Soil erosion hazard'}],
  fam: [{suitability_family_id: 'water_harvesting__terracing', nbs_id: 'water_harvesting_conservation', name: 'Bench terraces'}],
  sense: [{variable: 'crop_yield', positive_means: 'higher yield', negative_means: 'lower yield', high_is: 'good'}, {variable: 'erosion_hazard', positive_means: 'more erosion', negative_means: 'less erosion', high_is: 'bad'}],
};
const model = rows => buildModel({EV_evidence_register: rows, SRC_source_register: [source]}, lookups);
const one = row => model([row]).findings[0];

test('a reported range reads as a plain sentence and keeps the stored record', () => {
  const stored = '{"abs_min": 200, "abs_max": 600, "unit": "mm", "direction": "used in semi-arid rainfall"}';
  const f = one(unit('ev1', 'structural_suitability', 'annual_precipitation', stored));
  assert.equal(f.t, 'Reported range: mean annual precipitation 200 to 600 mm.');
  assert.deepEqual([f.r, f.lo, f.hi, f.u, f.pg, f.x], ['w', 200, 600, 'mm', 'p. 129', stored]);
});

test('direction is read on the variable as named: less erosion is a benefit, lower yield a harm', () => {
  const erosion = one(unit('ev2', 'nbs_effect', 'erosion_hazard', {direction: 'negative', metric: 'pct_change', magnitude: 43}));
  assert.deepEqual([erosion.t, erosion.g, erosion.pc, erosion.r], ['Less erosion by 43%.', 'Benefit', -43, 'd']);
  const crop = one(unit('ev3', 'nbs_effect', 'crop_yield', {direction: 'negative', metric: 'pct_change', magnitude: 9.5}));
  assert.deepEqual([crop.t, crop.g, crop.pc], ['Lower yield by 9.5%.', 'Harm', -9.5]);
});

test('an effect stated under a hazard answers the hazard-protection question, by hazard', () => {
  const f = one(unit('ev4', 'nbs_effect', 'crop_yield', {direction: 'positive', metric: 'narrative'}, {context: {hazard_type: 'drought', country: ['ETH']}}));
  assert.deepEqual([f.r, f.v, f.ov, f.g, f.c], ['p', 'hz:drought', 'crop_yield', 'Benefit', ['Ethiopia']]);
});

test('no direction is invented: operational findings carry no helps or hinders label, and gaps are stated', () => {
  const said = one(unit('ev5', 'operational_risk', 'labour_availability', {outcome_raw: 'rainy-season labour competition prevents terrace repair'}));
  assert.deepEqual([said.t, said.g], ['Rainy-season labour competition prevents terrace repair.', '']);
  const empty = one(unit('ev6', 'operational_risk', 'tenure_security', ''));
  assert.equal(empty.g, 'No summary');
  assert.match(empty.t, /no plain summary is recorded/);
});

test('dropped findings and non-evidence rows are left out; one family id spelling per practice', () => {
  const m = model([
    unit('keep', 'structural_suitability', 'annual_precipitation', {abs_min: 1, unit: 'mm'}, {suitability_family_id: 'water_harvesting__cross_family'}),
    unit('bare', 'structural_suitability', 'annual_precipitation', {abs_min: 1, unit: 'mm'}, {suitability_family_id: 'cross_family'}),
    unit('gone', 'structural_suitability', 'annual_precipitation', {abs_min: 1, unit: 'mm'}, {review_state: 'dropped'}),
    unit('data', 'dataset', 'annual_precipitation', {}),
  ]);
  assert.deepEqual(m.findings.map(f => [f.i, f.f]), [['keep', 'water_harvesting__cross_family'], ['bare', 'water_harvesting__cross_family']]);
  assert.equal(m.families.water_harvesting__cross_family.l, 'Across sub-practices');
  assert.equal(m.sources[0].s, 'Mekdaschi Studer et al. (2013)');
});

test('register files parse with quoted commas and line breaks', () => {
  assert.deepEqual(parseCsv('a,b\r\n"x, y","line 1\nline 2 ""quoted"""\r\n'), [{a: 'x, y', b: 'line 1\nline 2 "quoted"'}]);
});

test('the download is a valid stored zip', async () => {
  assert.equal(crc32(new TextEncoder().encode('123456789')), 0xCBF43926);
  const bytes = new Uint8Array(await zip([['findings.csv', 'a,b\r\n'], ['README.txt', 'é']]).arrayBuffer());
  const view = new DataView(bytes.buffer);
  assert.equal(view.getUint32(0, true), 0x04034b50);
  const end = bytes.length - 22;
  assert.equal(view.getUint32(end, true), 0x06054b50);
  assert.equal(view.getUint16(end + 10, true), 2);
  assert.equal(view.getUint32(view.getUint32(end + 16, true), true), 0x02014b50);
});
