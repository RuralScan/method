/* Review triage only. No register, decision, approval or runtime writes. */
(function () {
  'use strict';
  const esc = value => String(value == null ? '' : value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const rows = () => (typeof reviewData !== 'undefined' && reviewData && reviewData.review_priorities) || [];
  const evidence = () => [...(reviewData.registers.EV_evidence_register || []), ...(reviewData._evDropped || [])];
  const notes = id => rows().filter(r => r.evidence_id === id);
  const selected = () => window._vfPriority || 'all';
  const batchRoute = id => '#review-priority=' + encodeURIComponent(id);
  const cardRoute = id => '#review-evidence=' + encodeURIComponent(id);
  function sourceLocation(row) {
    return String(row.page || '').trim() ? 'PDF p' + esc(row.page) : 'Source location: ' + esc(row.source_locator);
  }
  function matches(ev) {
    if (window._vfPriorityEvidence && ev.evidence_id !== window._vfPriorityEvidence) return false;
    const value = selected();
    return value === 'all' || notes(ev.evidence_id).some(r => value === 'high' ? r.priority === 'high' : r.batch_id === value);
  }
  function scopeFor(units) {
    const practices = [...new Set(units.map(e => e.nbs_id))];
    const tables = [...new Set(units.map(e => e.use_role === 'operational_risk' ? 'M2b' : _vfR2T[e.use_role]))];
    window._vfScope = {nbs: practices.length === 1 ? practices[0] : 'all', table: tables.length === 1 ? tables[0] : 'all', family: 'all', source: 'all', access: 'all', claimScope: 'all', observations: 'show', round: 'all', sourceId: '', section: ''};
    window._vfSearch = ''; window._vfMode = 'review';
  }
  function set(value) {
    window._vfPriorityEvidence = '';
    window._vfPriority = value;
    if (value !== 'all') {
      const ids = new Set(rows().filter(r => value === 'high' ? r.priority === 'high' : r.batch_id === value).map(r => r.evidence_id));
      scopeFor(evidence().filter(e => ids.has(e.evidence_id)));
      vfSimpleQueue('todo');
    } else renderVfWorklist();
    history.replaceState(null, '', route());
  }
  function route() {
    return window._vfPriorityEvidence ? cardRoute(window._vfPriorityEvidence) : selected() !== 'all' ? batchRoute(selected()) : DashboardTables.route((window._vfScope || {}).table);
  }
  function leaveFocus() {
    window._vfPriorityEvidence = '';
    history.replaceState(null, '', route());
  }
  function openFromHash(hash) {
    const table = DashboardTables.tableFromRoute(hash);
    if (table) {
      if (!reviewData) return true;
      scopeFor([]);
      window._vfPriorityEvidence = '';
      window._vfPriority = 'all';
      window._vfScope.table = table;
      window._vfScope.observations = table === 'M2b' ? 'show' : 'hide';
      window.DashboardShell.openReviewQueue();
      vfSimpleQueue('todo');
      history.replaceState(null, '', hash);
      document.getElementById('review-queue').scrollIntoView({block: 'start'});
      return true;
    }
    const match = /^#review-(priority|evidence)=(.*)$/.exec(hash);
    if (!match) return false;
    if (typeof reviewData === 'undefined' || !reviewData) return true;
    let value; try { value = decodeURIComponent(match[2]); } catch (_) { return true; }
    const unit = match[1] === 'evidence' && evidence().find(e => e.evidence_id === value);
    if (match[1] === 'priority' && value !== 'high' && !rows().some(r => r.batch_id === value) || match[1] === 'evidence' && !unit) {
      window.DashboardShell.openReviewQueue();
      vfNotice('This review link is not present in the current dashboard build.', true);
      return true;
    }
    window.DashboardShell.openReviewQueue();
    if (unit) {
      scopeFor([unit]);
      window._vfPriority = 'all'; window._vfPriorityEvidence = value;
      vfSimpleQueue('advanced');
      window._vfAxStatus = 'any';
      renderVfWorklist();
      const card = Array.from(document.querySelectorAll('#vf-cards [data-vfeid]')).find(el => el.dataset.vfeid === value);
      if (card) { if (card.tagName === 'DETAILS') card.open = true; card.scrollIntoView({block: 'start'}); }
    } else set(value);
    history.replaceState(null, '', hash);
    return true;
  }
  let setSearch = '', allSets = false, pickerScope = '';
  function catalog() {
    const byId = new Map(evidence().map(ev => [ev.evidence_id, ev]));
    const batches = new Map();
    const scope = window._vfScope || {};
    for (const row of rows()) {
      if (!batches.has(row.batch_id)) batches.set(row.batch_id, {id:row.batch_id, label:row.batch_label, ids:new Set(), scoped:new Set()});
      const batch = batches.get(row.batch_id), ev = byId.get(row.evidence_id);
      batch.ids.add(row.evidence_id);
      if (ev && (!scope.nbs || scope.nbs === 'all' || ev.nbs_id === scope.nbs)
          && DashboardTables.matches(ev, scope.table, true)) batch.scoped.add(row.evidence_id);
    }
    return [...batches.values()];
  }
  function setList() {
    const query = setSearch.trim().toLowerCase();
    const batches = catalog().filter(b => (allSets || b.scoped.size) && (!query || b.label.toLowerCase().includes(query)));
    return '<p class="vf-set-count" role="status">'+batches.length+(batches.length===1?' review set':' review sets')+(allSets?' across all practices and evidence types':' for this practice and evidence type')+'</p>'
      + (batches.length ? '<ul class="vf-set-list">'+batches.map(b => '<li><button type="button" data-batch="'+esc(b.id)+'" onclick="DashboardPriority.choose(this.dataset.batch)"'
        +(selected()===b.id?' aria-current="true"':'')+'><span>'+esc(b.label)+'</span><small>'+(allSets?b.ids.size:b.scoped.size)+((allSets?b.ids.size:b.scoped.size)===1?' finding':' findings')
        +(allSets?' · opens full set':' in this view')+'</small></button></li>').join('')+'</ul>'
        : '<p class="vf-set-empty">'+(query?'No review sets match your search.':'No review sets for this practice and evidence type.')+' You can review the queue without choosing a set.</p>');
  }
  function filterSets(value, includeAll) {
    setSearch = value; allSets = includeAll;
    document.getElementById('vf-set-results').innerHTML = setList();
  }
  function choose(value) {
    const expandScope = allSets && value !== 'all' && value !== 'high';
    setSearch = ''; allSets = false;
    if (expandScope) set(value);
    else {
      window._vfPriorityEvidence = '';
      window._vfPriority = value;
      renderVfWorklist();
      history.replaceState(null, '', route());
    }
    document.querySelector('.vf-selected-set button, .vf-review-sets > summary')?.focus({preventScroll:true});
  }
  function backToQueue() {
    window._vfPriorityEvidence = ''; window._vfPriority = 'all';
    vfSimpleQueue('todo');
    history.replaceState(null, '', route());
    document.querySelector('#vf-verdict-filters button')?.focus({preventScroll:true});
  }
  function controls() {
    const scope = window._vfScope || {};
    const scopeKey = [scope.nbs,scope.table].join('/');
    if (pickerScope !== scopeKey) { setSearch = ''; allSets = false; pickerScope = scopeKey; }
    const current = selected(), focused = window._vfPriorityEvidence;
    const batchRows = rows().filter(r => r.batch_id === current);
    const label = current === 'high' ? 'High priority' : batchRows[0]?.batch_label || current;
    const focus = focused ? '<div class="vf-single-finding"><span><strong>Single finding</strong> · Opened from a direct link</span><button type="button" class="pill-btn" onclick="DashboardPriority.backToQueue()">Back to queue</button></div>' : '';
    if (!rows().length) return focus;
    return focus + '<section class="vf-priority-controls" aria-label="Review focus">'
      + (current !== 'all' ? '<div class="vf-selected-set"><span>Review set: <strong>'+esc(label)+'</strong></span><button type="button" class="pill-btn" onclick="DashboardPriority.choose(\'all\')">Clear review set</button></div>' : '')
      + '<details class="vf-review-sets"><summary>Choose a review set <span>Optional</span></summary><div class="vf-set-browser">'
      + '<p>Review sets group findings that need a particular check. You can also work straight through the queue.</p>'
      + '<div class="vf-set-tools"><label for="vf-set-search">Find a review set</label><input id="vf-set-search" type="search" placeholder="e.g. rating checks or source checks" value="'+esc(setSearch)+'" oninput="DashboardPriority.filterSets(this.value,document.getElementById(\'vf-all-sets\').checked)">'
      + '<label class="vf-set-toggle"><input id="vf-all-sets" type="checkbox"'+(allSets?' checked':'')+' onchange="DashboardPriority.filterSets(document.getElementById(\'vf-set-search\').value,this.checked)"> Include other practices and evidence types</label></div>'
      + '<button type="button" class="pill-btn" onclick="DashboardPriority.choose(\'high\')">High priority in this view</button>'
      + '<div id="vf-set-results">'+setList()+'</div>'
      + '<p class="vf-set-help">Counts include reviewed findings. Queue tabs and other filters still apply. Choosing a set does not change any review decisions.</p>'
      + (batchRows.length ? '<details class="vf-set-records"><summary>Finding links for selected set ('+new Set(batchRows.map(r=>r.evidence_id)).size+')</summary><ul>'+[...new Map(batchRows.map(r=>[r.evidence_id,r])).values()].map(r=>'<li><a href="'+cardRoute(r.evidence_id)+'">'+esc(r.evidence_id)+'</a> · '+esc(r.source_id)+' · '+sourceLocation(r)+'</li>').join('')+'</ul></details>' : '')
      + '</div></details></section>';
  }
  function badge(ev) {
    const list = notes(ev.evidence_id);
    if (!list.length) return '';
    return '<span style="font-size:11px;border:1px solid var(--accent-amber);color:var(--accent-amber);padding:2px 6px;border-radius:4px">'+(list.some(r=>r.priority==='high')?'High review priority':'Review priority')+'</span>';
  }
  function fieldLabel(path) {
    const names = {observed_min:'Observed minimum', observed_max:'Observed maximum', observed_classes:'Observed classes'};
    const words = key => key.replace(/_/g, ' ').replace(/^./, c => c.toUpperCase());
    if (path[0] === 'relationship' && path.length === 2 && names[path[1]]) return names[path[1]];
    return path.map(words).join(' · ');
  }
  function fieldValue(change, side) {
    if (!Object.hasOwn(change, side)) return '<em>Not recorded</em>';
    const value = change[side];
    const text = typeof value === 'number' ? value.toLocaleString('en-US', {maximumSignificantDigits:21})
      : typeof value === 'string' ? value : JSON.stringify(value, null, 2);
    return esc(text) + (change[side + '_unit'] ? ' '+esc(change[side + '_unit']) : '');
  }
  function correction(event) {
    const rows = event.changes.map(change => '<tr><th scope="row">'+esc(fieldLabel(change.path))+'</th><td>'
      +fieldValue(change,'before')+'</td><td>'+fieldValue(change,'after')+'</td></tr>');
    return '<p>'+esc(event.date)+' · <a href="https://github.com/RuralScan/evidence/issues/'+encodeURIComponent(event.receipt)+'">Receipt #'
      +esc(event.receipt)+'</a></p><table><thead><tr><th scope="col">Field</th><th scope="col">Before</th>'
      +'<th scope="col">After</th></tr></thead><tbody>'+rows.join('')+'</tbody></table>';
  }
  function card(ev) {
    const history = reviewData.corrections?.[ev.evidence_id] || [];
    const latest = history.at(-1);
    const earlier = history.slice(0,-1).reverse();
    const pending = ev.review_state !== 'dropped' && ev.reviewer_ok !== true && ev.reviewer_ok !== 'true';
    const applied = latest ? '<section class="vf-applied-correction" aria-label="Applied correction"><strong>Correction applied</strong>'
      +correction(latest)+'<p>This correction reopened the finding for source review.'
      +(pending?' Check the changed fields against the source.':'')+'</p>'
      +(earlier.length ? '<details><summary>Earlier corrections ('+earlier.length+')</summary>'+earlier.map(correction).join('')+'</details>' : '')
      +'</section>' : '';
    return applied + notes(ev.evidence_id).map(r => {
      const reference = '<a href="'+cardRoute(ev.evidence_id)+'">Link to this evidence card</a> · <a href="'+batchRoute(r.batch_id)+'">Open priority batch</a>';
      if (!r.reason && !r.decision_needed) return '<p>'+esc(r.batch_label)+' · <a href="'+batchRoute(r.batch_id)+'">Open priority batch</a></p>';
      const original = '<b>'+esc(r.batch_label)+'</b>'+(r.requested_by?' · requested by '+esc(r.requested_by):'')+(r.requested_date?' · '+esc(r.requested_date):'')
        +(r.context_changed?'<p>Evidence changed since this request.</p>':'')
        +'<p><b>Why prioritized:</b> '+esc(r.reason)+'</p><p><b>Decision needed:</b> '+esc(r.decision_needed)+'</p>';
      const older = latest && r.requested_date && r.requested_date < latest.date;
      return '<section class="vf-priority-note" style="margin:10px 0;padding:12px;border-left:3px solid var(--accent-amber);font-size:12px;line-height:1.6">'
        +(older ? '<details><summary>Original review request · before this correction</summary>'+original+'</details>'
          +'<p>Check any remaining questions in the original request.</p>' : original)
        +'<details><summary>Request reference and links</summary><p>Source '+esc(r.source_id)+' · '+sourceLocation(r)+'</p>'
        +(r.mapping_id?'<p>Mapping: '+esc(r.mapping_id)+'</p>':'')+reference+'</details>'
        +(ev.use_role==='structural_suitability'?'<p>Keep confirms the extraction. Changing a live mapping requires a separate reviewed change.</p>':'')+'</section>';
    }).join('');
  }
  window.DashboardPriority = {matches, set, route, leaveFocus, openFromHash, controls, badge, card, filterSets, choose, backToQueue};
})();
