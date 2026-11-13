/* Read-only views over the evidence and recipe rows shipped with this dashboard. */
(() => {
  'use strict';
  const tables = [
    {id: 'T3', hash: '#review-t3', key: 'T3_nbs_hazard_farming', description: 'Findings cited in T3 hazard ratings. Check what the source says about the hazard, practice and farming system.'},
    {id: 'T4-suitability', hash: '#review-t4', description: 'Structural suitability findings. Check the site condition, threshold and units against the source.'},
    {id: 'T6', hash: '#review-t6', key: 'T6_nbs_scorecard', description: 'Findings cited in T6 scorecard ratings. Check the reported effect and the conditions under which it applies.'}
  ];
  const compiled = new WeakMap();
  function matches(ev, table, includeHistory = false) {
    if (!table || table === 'all') return true;
    if (table === 'T4-suitability') return ev.use_role === 'structural_suitability';
    if (table !== 'T3' && table !== 'T6') return _vfR2T[ev.use_role] === table;
    const recipes = reviewData.recipes;
    if (reviewData.membership) {
      if (!compiled.has(reviewData)) {
        const groups = {};
        for (const id of ['T3', 'T6']) {
          groups[id] = new Set(reviewData.membership[id]);
          groups[id + '-former'] = new Set(Object.keys(reviewData.formerly_cited[id]));
        }
        compiled.set(reviewData, groups);
      }
      const groups = compiled.get(reviewData);
      return groups[table].has(ev.evidence_id) || (includeHistory && groups[table + '-former'].has(ev.evidence_id));
    }
    if (!compiled.has(recipes)) {
      const sets = {};
      for (const {id, key} of tables.filter(t => t.key)) {
        sets[id] = new Set(Object.values(recipes).flatMap(recipe =>
          (recipe[key] || []).flatMap(row => row.evidence_ids || [])));
      }
      compiled.set(recipes, sets);
    }
    return compiled.get(recipes)[table].has(ev.evidence_id);
  }
  function describe(id) {
    const table = tables.find(t => t.id === id);
    document.getElementById('review-table-description').textContent = table?.description || 'Choose a table to open its findings, then check the quoted passage on each evidence card.';
    for (const a of document.querySelectorAll('.review-start nav a')) {
      if (a.hash === table?.hash) a.setAttribute('aria-current', 'true');
      else a.removeAttribute('aria-current');
    }
  }
  let batches;
  function ciatUrl(id) {
    if (!batches) batches = JSON.parse(document.getElementById('ciat-review-batches')?.textContent || '{}');
    const base = 'https://ciat.github.io/nbs_ruralscan/';
    if (batches[id]) return base + 'review.html?' + new URLSearchParams({batch: batches[id], unit: id});
    return base + 'dashboard.html#review-evidence=' + encodeURIComponent(id);
  }
  let ratingReviews;
  function ratingStatus(id) {
    if (!ratingReviews) ratingReviews = JSON.parse(document.getElementById('live-t3-reviews')?.textContent || '{}');
    const review = ratingReviews[id];
    if (review?.provisional) {
      return '<p><strong>Provisional.</strong> ' + review.unresolved + (review.unresolved === 1 ?
        ' finding that sets this rating is held or unreviewed.' : ' findings that set this rating are held or unreviewed.') + '</p>';
    }
    if (review?.coverage === 'assessed') return '<p>All findings identified as setting this rating have been checked for outstanding review. None are held or unreviewed.</p>';
    return '<p>Review coverage is incomplete for this rating. Its provisional status is unknown.</p>';
  }
  const pretty = text => String(text ?? '').replace(/_/g, ' ').replace(/^\w/, c => c.toUpperCase());
  const lensNames = {asset_threat: 'Threat to the investment', livelihood_mitigation: 'Livelihood risk mitigation'};
  const esc = value => vfEsc(String(value ?? ''));
  const select = id => document.getElementById('hazard-' + id);
  function choose(id, options) {
    const el = select(id), previous = el.value;
    el.replaceChildren(...options.map(([value, label]) => new Option(label, value)));
    if (options.some(([value]) => value === previous)) el.value = previous;
    return el.value;
  }
  function scope(row) {
    return [row.suitability_family_id ? familyDisplayName(row.suitability_family_id) : 'Whole practice',
      row.scope_type ? pretty(row.scope_type) + ' · ' + pretty(row.scope_id) : '',
      row.farming_system === 'all' ? 'All farming systems' : pretty(row.farming_system)].filter(Boolean).join(' · ');
  }
  function scopeOrder(row) {
    return Number(Boolean(row.suitability_family_id || row.scope_type)) * 2 + Number(row.farming_system !== 'all');
  }
  function showHazards() {
    if (!dashboardData) return;
    const recipes = dashboardData.recipes;
    const practices = Object.entries(recipes).filter(([, recipe]) => recipe.T3_nbs_hazard_farming?.length);
    if (!practices.length) { select('rating').textContent = 'No hazard ratings in this edition.'; return; }
    const practice = choose('practice', practices.map(([id, recipe]) => [id, recipe.T0_nbs_registry?.[0]?.nbs_name || pretty(id)]));
    const rows = recipes[practice].T3_nbs_hazard_farming;
    const hazard = choose('type', [...new Set(rows.map(r => r.hazard_type))].sort().map(id => [id, pretty(id)]));
    const hazardRows = rows.filter(r => r.hazard_type === hazard);
    const lens = choose('lens', [...new Set(hazardRows.map(r => r.risk_role))].sort().reverse().map(id => [id, lensNames[id] || pretty(id)]));
    const choices = hazardRows.filter(r => r.risk_role === lens).sort((a,b) => scopeOrder(a) - scopeOrder(b) || scope(a).localeCompare(scope(b)));
    const id = choose('scope', choices.map(r => [r.record_id, scope(r)]));
    const row = choices.find(r => r.record_id === id);
    const findings = new Map([...dashboardData.registers.EV_evidence_register, ...(dashboardData._evDropped || [])].map(e => [e.evidence_id, e]));
    const sources = new Map(dashboardData.registers.SRC_source_register.map(s => [s.source_id, s]));
    const ids = row.evidence_ids || [];
    function cited(text) {
      return esc(text).replace(/\[(ev_[^\]]+)\]/g, (full, group) => {
        const links = group.split(/,\s*/).map(id => {
          const n = ids.indexOf(id);
          return n < 0 ? id : '<a href="#review-evidence=' + encodeURIComponent(id) + '" aria-label="Review finding ' + (n+1) + '">' + (n+1) + '</a>';
        });
        return '[' + links.join(', ') + ']';
      });
    }
    const list = ids.map(id => {
      const ev = findings.get(id);
      if (!ev) return '<li>' + esc(id) + ' · Finding unavailable in this snapshot</li>';
      const source = sources.get(ev.source_id);
      const locator = ev.page ? ' · p. ' + esc(ev.page) : ev.locator ? ' · ' + esc(ev.locator) : '';
      return '<li><a href="#review-evidence=' + encodeURIComponent(id) + '">' + esc(source?.citation || ev.source_id) + locator + '</a></li>';
    }).join('');
    const rating = lens === 'asset_threat' ? row.asset_sensitivity : row.mitigation_potential;
    select('rating').innerHTML = '<p class="hazard-result"><strong>' + (lens === 'asset_threat' ? 'Asset sensitivity' : 'Mitigation potential') +
      ' · ' + esc(pretty(rating) || 'No rating recorded') + '</strong><span>Confidence · ' + esc(pretty(row.confidence) || 'Unreported') + '</span></p>' +
      ratingStatus(row.record_id) +
      (row.mitigation_mechanism ? '<p>' + cited(row.mitigation_mechanism) + '</p>' : '') +
      (row.caveats ? '<details><summary>Limitations and applicability</summary><p>' + cited(row.caveats) + '</p></details>' : '') +
      '<details><summary>Source findings (' + ids.length + ')</summary><ol>' + list + '</ol></details><p><a href="#review-t3">Open T3 review queue</a></p>';
  }
  document.getElementById('hazard-panel').addEventListener('change', showHazards);
  window.DashboardTables = {
    matches, describe, showHazards, ciatUrl,
    route: id => tables.find(t => t.id === id)?.hash || '#review-queue',
    tableFromRoute: hash => tables.find(t => t.hash === hash)?.id
  };
})();
