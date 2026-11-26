/* Shared read-only view of pinned pending candidates. No scientific evaluation or writes. */
(function () {
  'use strict';
  const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const words = value => String(value === 'ai' ? 'aridity index' : value ?? '').replace(/^.*__/, '').replaceAll('_', ' ').replace(/\bfmnr\b/g, 'FMNR').replace(/\banr\b/g, 'ANR');
  const num = value => value == null ? 'Unknown / not assigned' : Number(value).toLocaleString('en', {maximumFractionDigits: 4});
  const safeUrl = url => { try { const u = new URL(url); return ['https:', 'http:'].includes(u.protocol) ? u.href : ''; } catch (_) { return ''; } };
  const link = (url, label) => safeUrl(url) ? `<a href="${esc(safeUrl(url))}" target="_blank" rel="noopener noreferrer">${esc(label)}</a>` : esc(label);
  const details = (title, body) => `<details><summary>${esc(title)}</summary>${body}</details>`;
  const para = value => `<p>${esc(value)}</p>`;
  const table = (caption, headings, rows) => `<div class="ovr-table"><table><caption>${esc(caption)}</caption><thead><tr>${headings.map(h => `<th scope="col">${esc(h)}</th>`).join('')}</tr></thead><tbody>${rows.map(row => `<tr>${row.map(cell => `<td>${esc(cell)}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`;
  function validate(model) {
    if (model.format !== 'ruralscan.override-review.v1' || !/^[a-f0-9]{40}$/.test(model.revision) || model.activate !== false || model.runtime_implemented !== false || model.scientific_acceptance !== 'pending' || !Array.isArray(model.records) || !model.records.length) throw Error('Unsupported review snapshot');
    const ids = new Set();
    for (const item of model.records) {
      const r = item.candidate;
      if (!r || r.status !== 'pending' || r.activate !== false || r.format !== 'ruralscan.t4-profile-candidate.v1' || ids.has(r.id) || !/^[a-z0-9_-]+$/.test(r.id) || !Array.isArray(r.profile?.scope) || !r.profile.scope.length || !['composite_scoping','precomputed_unit_index'].includes(r.profile.type)) throw Error('Snapshot contains an unsupported or non-pending candidate');
      ids.add(r.id);
    }
    return model;
  }
  function select(model, practice = '', family = '', id = '') {
    return model.records.filter(({candidate:r}) => (!id || r.id === id) && r.profile.scope.some(s => (!practice || s.nbs_id === practice) && (!family || s.family_id === family)));
  }
  function expression(node) {
    return node.kind === 'minimum' ? `minimum(${node.children.map(expression).join(', ')})` : `${words(node.input)} support`;
  }
  function curve(item, p, index) {
    const pts = item.points, lo = pts[0][0], hi = pts[pts.length-1][0];
    const x = v => 48 + (v-lo)/(hi-lo)*350, y = v => 140-v*110;
    const path = pts.map(([a,b], i) => `${i?'L':'M'}${x(a).toFixed(2)},${y(b).toFixed(2)}`).join(' ');
    const title = `${words(item.input)} membership — pending`;
    const unit = p.inputs[item.input].unit;
    return `<figure class="ovr-curve"><svg viewBox="0 0 440 192" role="img" aria-label="${esc(title)}"><title>${esc(title)}</title><path class="ovr-axis" d="M48 30V140H398"/><text x="36" y="35" text-anchor="end">1</text><text x="36" y="145" text-anchor="end">0</text><path class="ovr-line" d="${path}"/>${[[item.x20,.2],[item.x80,.8]].map(([a,b]) => `<circle cx="${x(a)}" cy="${y(b)}" r="4"/><text x="${x(a)}" y="${y(b)-10}" text-anchor="middle">${num(a)} → ${b}</text>`).join('')}<text x="48" y="160">${num(lo)}</text><text x="398" y="160" text-anchor="end">${num(hi)}</text><text x="223" y="184" text-anchor="middle">${esc(words(item.input))} (${esc(unit)})</text></svg><figcaption>Figure ${index+1}. ${esc(title)}. Displayed range is not an exclusion range.</figcaption></figure>`;
  }
  function renderCard(item, model) {
    const r = item.candidate, p = r.profile, j = r.justification;
    const source = `https://github.com/RuralScan/evidence/blob/${model.revision}/suitability/overrides/candidates/${r.id}.json`;
    const scope = table('Declared intervention scope', ['Practice','Family','Subpractice','Pathway'], p.scope.map(s => [words(s.nbs_id), words(s.family_id), s.subpractice_ids.map(words).join(', '), s.pathways ? s.pathways.map(words).join(', ') : 'No pathway predicate declared']));
    const inputs = table('Proposed inputs and bindings', ['Input','Canonical variable','Dataset release','Unit'], Object.entries(p.inputs).map(([k,v]) => [words(k),v.variable,v.dataset_id,v.unit]));
    let relationship;
    if (p.type === 'composite_scoping') {
      relationship = `<p class="ovr-formula">${esc(expression(p.score))}</p><p>Membership describes climatic limitation, not establishment probability or an area fraction. The continuous curve and separate screens serve different purposes.</p><div class="ovr-curves">${item.curves.map((c,i) => curve(c,p,i)).join('')}</div>`;
      relationship += table('Separate exclusion screens', ['Screen','Condition','Mapped water may bypass this screen'], p.screens.map(s => [words(s.id), `${words(s.input)} ${{lt:'<',le:'≤',gt:'>',ge:'≥'}[s.operator]} ${s.threshold} ${p.inputs[s.input].unit}`, s.water_bypass ? 'Conditional pathway only; no score or automatic hectares' : 'No']));
      relationship += `<p>Combined-score cutoff: ${p.combined_score_cutoff === null ? 'none' : esc(p.combined_score_cutoff)}. Criterion weight: ${p.weight === null ? 'not assigned' : esc(p.weight)}.</p>`;
      relationship += details('Exact thermal derivation and missing-state policy', `<pre>${esc(JSON.stringify({thermal_season:p.thermal_season,water_policy:p.water_policy,missing:p.missing},null,2))}</pre><p>Missing climate remains unknown. A known independent exclusion stays visible. Retention-only parklands and mismatched pathways receive no inherited recruitment exclusion.</p>`);
    } else {
      relationship = `<p class="ovr-formula">Score = native ${esc(p.score_input)} where ${esc(p.area_input)} &gt; 0</p><p>Keep the source score unchanged. Support polygons are not restoration footprints. Zero modelled area and missing coverage have different meanings.</p><p>Source area conversion: ${esc(p.area_to_hectares)} hectares per km². Allocation policy: ${esc(words(p.area_policy))}. No score-weighted hectares or polygon-area proration.</p>`;
    }
    const examples = model.examples.filter(e => e.candidate_id === r.id).map(e => {
      const v = e.result;
      return details(e.id === 'mangrove-partial-unit' ? 'Worked example: synthetic partial unit' : 'Worked example: selected climate reference', `<p>${e.id === 'mangrove-partial-unit' ? 'Synthetic arithmetic only; not a mapped restoration unit.' : 'Selected contradiction check; host/legal context unresolved. Not global validation or site eligibility.'}</p>${table('Reference-evaluator output', ['State','Score','Point estimate (ha)','Lower allocation bound (ha)','Upper allocation bound (ha)'], [[words(v.state),num(v.score),num(v.area_ha),num(v.area_lower_ha),num(v.area_upper_ha)]])}<pre>${esc(JSON.stringify(e.inputs,null,2))}</pre>`);
    }).join('');
    const evidence = r.evidence_refs.map(ref => `<li>${link(ref.url,ref.citation)}<p><strong>Locator:</strong> ${esc(ref.locator)}</p><p><strong>Role:</strong> ${esc(ref.claim_role)}</p><p><strong>Source status at this pin:</strong> ${esc(words(ref.admission_status))}</p><code>${esc(ref.source_id)}</code></li>`).join('');
    return `<article class="ovr-card" id="rule-${esc(r.id)}"><h3>${esc(words(p.scope[0].family_id))} · ${p.type === 'composite_scoping' ? 'Climate proposal' : 'Restoration index proposal'}</h3><p class="ovr-id">${esc(r.id)}</p><dl class="ovr-lifecycle"><div><dt>Rule</dt><dd>Pending</dd></div><div><dt>Scientific acceptance</dt><dd>Pending</dd></div><div><dt>Reference implementation</dt><dd>Implemented for review</dd></div><div><dt>Runtime activation</dt><dd>Inactive · unimplemented</dd></div></dl>${para(j.rationale)}${scope}${details('Evidence and source locators', '<p>Source admission is separate from finding Keep and relationship acceptance. These references are not invented Evidence Register units.</p><ul class="ovr-sources">'+evidence+'</ul>')}${details('Mechanism and justification', '<h4>What the sources report</h4>'+para(j.source_relationship)+'<h4>Mechanism interpretation</h4>'+para(j.mechanism)+'<h4>Analyst choices and transfer</h4>'+para(j.analyst_choices)+para(j.transfer_limits))}${details('Quantitative relationship and separate screens',relationship)}${examples}${details('Dataset bindings and area accounting',inputs+para(j.binding)+'<h4>Area accounting</h4>'+para(j.area_accounting))}${details('Replacements, dependencies and remaining approval',para(j.replacement_policy)+para(j.approval_remaining)+'<p>No accepted replacement or activation receipt is recorded in this pending candidate. Exact replacement fingerprints and dependencies must be settled in the official proposal route; source Keep and software tests cannot supply them.</p>')}<p>${link(source,'Exact candidate and revision history')} · <a href="#overrides/${esc(r.id)}">Link to this rule</a></p><details><summary>Exact profile and candidate fingerprint</summary><p>Candidate SHA-256: <code>${esc(item.sha256)}</code></p><pre>${esc(JSON.stringify(p,null,2))}</pre></details></article>`;
  }
  function routeId(hash) { return hash.startsWith('#overrides/') ? hash.slice(11) : ''; }
  async function mount(root) {
    try {
      const response = await fetch(new URL(root.dataset.source, document.baseURI));
      if (!response.ok) throw Error('Snapshot unavailable');
      const model = validate(await response.json());
      const practices = [...new Set(model.records.flatMap(i => i.candidate.profile.scope.map(s => s.nbs_id)))].sort();
      root.innerHTML = `<p class="ovr-notice"><strong>Pending proposals · inactive.</strong> Read source evidence, mechanism and authored policy choices separately. This pinned review snapshot does not change maps or approve relationships.</p><p>${link(model.summary_url,'Scientific review summary')} · ${link(model.source_csv,'Authoritative CSV')} · <a href="${esc(root.dataset.source)}">Download review snapshot</a><br><small>Evidence revision: <code>${esc(model.revision)}</code>. Source/finding status may have changed since this snapshot.</small></p><div class="ovr-filters"><label>Practice<select data-practice><option value="">All practices</option>${practices.map(p => `<option value="${esc(p)}">${esc(words(p))}</option>`).join('')}</select></label><label>Family<select data-family></select></label><a href="#overrides">Show all rules</a></div><p data-count role="status"></p><div data-cards></div>`;
      const practice = root.querySelector('[data-practice]'), family = root.querySelector('[data-family]');
      function families() {
        const fs = [...new Set(model.records.flatMap(i => i.candidate.profile.scope.filter(s => !practice.value || s.nbs_id === practice.value).map(s => s.family_id)))].sort();
        family.innerHTML = '<option value="">All families</option>'+fs.map(f => `<option value="${esc(f)}">${esc(words(f))}</option>`).join('');
      }
      function render() {
        const id = routeId(location.hash);
        if (id) { practice.value=''; families(); }
        const items = select(model, practice.value, family.value, id);
        root.querySelector('[data-count]').textContent = `${items.length} pending rule${items.length === 1 ? '' : 's'} · no active relationships`;
        root.querySelector('[data-cards]').innerHTML = items.map(i => renderCard(i,model)).join('') || '<p>No matching pending rule in this snapshot.</p>';
      }
      function filter() { if (routeId(location.hash)) history.replaceState(null,'','#overrides'); render(); }
      practice.addEventListener('change',()=>{families();filter();}); family.addEventListener('change',filter);
      window.addEventListener('hashchange',()=>{if(location.hash === '#overrides'){practice.value='';families();}render();});
      families();render();
    } catch (error) { root.innerHTML='<p role="alert">Pending rule snapshot unavailable or unsupported. No active rule is inferred. Reload to retry.</p>'; }
  }
  const api={validate,select,renderCard,expression,routeId,safeUrl};
  if(typeof module!=='undefined') module.exports=api;
  if(typeof document!=='undefined') { const start=()=>document.querySelectorAll('[data-override-review]').forEach(mount); if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',start);else start(); }
})();
