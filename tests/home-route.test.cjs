const {test} = require('node:test');
const assert = require('node:assert/strict');
const {destination} = require('../home-route.js');
const root = 'https://ruralscan.github.io/method/';

test('bare root and index open Methodology while retaining ordinary query parameters', () => {
  for (const path of ['', 'index.html']) {
    assert.equal(destination(root+path),root+'reference/index.html');
    assert.equal(destination(root+path+'?utm_source=team'),root+'reference/index.html?utm_source=team');
  }
});

test('all existing root fragments preserve their exact finding, queue or source route', () => {
  for (const path of ['', 'index.html']) for (const hash of [
    '#review-queue','#review-t3','#review-t4','#review-t6','#review-m2b',
    '#review-evidence=ev_fr_precip_wocat1626_1',
    '#review-evidence=ev_wet_water_table_depth_brouwer26_1',
    '#review-priority=t4_wetland_live_mapping_review_20261105',
    '#source=paper%20with%20spaces','#methods/evidence','#overview','#unrecognised-old-fragment'
  ]) assert.equal(destination(root+path+'?keep=1'+hash),root+'dashboard.html?keep=1'+hash);
});

test('legacy section and fallback query links stay on the dashboard without redirect loops', () => {
  for (const query of ['?edition-section=review-queue','?edition-fallback=overview'])
    assert.equal(destination(root+query),root+'dashboard.html'+query);
  assert.equal(destination(root+'?next=https://example.org'),root+'reference/index.html?next=https://example.org');
});
