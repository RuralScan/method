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
  const statusLabels = {active:'Needs attention', recheck:'Changed — recheck', reviewed:'Review recorded', excluded:'Excluded finding', addressed:'Request addressed', deprioritized:'Deprioritized'};
  const priorityView = () => window._vfPriorityView || 'attention';
  const viewLabels = {attention:'Needs attention', settled:'Reviewed / excluded', history:'Addressed / deprioritized', all:'All requests'};
  function visibleRequest(row) {
    const status = row.status || 'active', view = priorityView();
    return view === 'all' || (view === 'settled' ? ['reviewed','excluded'].includes(status)
      : view === 'history' ? ['addressed','deprioritized'].includes(status) : ['active','recheck'].includes(status));
  }
  function needsAttention(ev) {
    return selected() !== 'all' && priorityView() === 'attention' && notes(ev.evidence_id).some(r =>
      ['active','recheck'].includes(r.status || 'active') && (selected() === 'high' ? r.priority === 'high' : r.batch_id === selected()));
  }
  function matches(ev) {
    if (window._vfPriorityEvidence && ev.evidence_id !== window._vfPriorityEvidence) return false;
    const value = selected();
    return value === 'all' || notes(ev.evidence_id).some(r => visibleRequest(r) && (value === 'high' ? r.priority === 'high' : r.batch_id === value));
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
      const ids = new Set(rows().filter(r => value === 'high' ? visibleRequest(r) && r.priority === 'high' : r.batch_id === value).map(r => r.evidence_id));
      scopeFor(evidence().filter(e => ids.has(e.evidence_id)));
      if (priorityView() === 'attention') vfSimpleQueue('todo');
      else { window._vfAxStatus = 'any'; window._vfSimpleView = 'advanced'; renderVfWorklist(); }
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
  let setSearch = '', allSets = false, pickerScope = '', taskPage = 0;
  const pageSize = 6;
  function catalog() {
    const byId = new Map(evidence().map(ev => [ev.evidence_id, ev]));
    const batches = new Map();
    const scope = window._vfScope || {};
    for (const row of rows()) {
      if (!batches.has(row.batch_id)) batches.set(row.batch_id, {id:row.batch_id, label:row.batch_label, ids:new Set(), scoped:new Set(), total:new Set(), scopedTotal:new Set()});
      const batch = batches.get(row.batch_id), ev = byId.get(row.evidence_id);
      batch.total.add(row.evidence_id);
      if (visibleRequest(row)) batch.ids.add(row.evidence_id);
      if (ev && (!scope.nbs || scope.nbs === 'all' || ev.nbs_id === scope.nbs)
          && DashboardTables.matches(ev, scope.table, true)) {
        batch.scopedTotal.add(row.evidence_id);
        if (visibleRequest(row)) batch.scoped.add(row.evidence_id);
      }
    }
    return [...batches.values()];
  }
  function taskHint(id) {
    const hints = {
      t4_wetland_live_mapping_review_20261105: 'Check source evidence behind the current wetland suitability rules.',
      t4_mapped_claims_20261106: 'Check findings used in suitability rules against their sources.',
      t4_source_checked_20261106: 'Compare extracted values and their context with the source passage.',
      t4_species_crop_20261106: 'Check crop or species claims within their stated scope.',
      t4_held_parked_20261106: 'Read earlier holds and reasons before deciding whether another check is needed.',
      't4_limits_2026-11-10': 'Check whether the cited source supports each numerical cutoff.',
      'ocr_check_2026-11-07': 'Compare extracted table text with the original PDF.',
      'direction_audit_2026-10-23': 'Check the reported direction of the effect against the source.'
    };
    if (hints[id]) return hints[id];
    if (id.startsWith('ratings_')) return 'Check findings behind ratings. Follow the review question on each card.';
    if (id.startsWith('effects_')) return 'Check reported effects against the cited source passages.';
    return 'Read the requested check on each finding, then compare it with the source.';
  }
  function setList() {
    const query = setSearch.trim().toLowerCase();
    const batches = catalog().filter(b => (allSets ? b.ids.size : b.scoped.size) &&
      (!query || (b.label+' '+taskHint(b.id)).toLowerCase().includes(query)));
    taskPage = Math.min(taskPage, Math.max(0,Math.ceil(batches.length/pageSize)-1));
    const start = taskPage*pageSize, shown = batches.slice(start,start+pageSize);
    const count = b => {
      const n = allSets?b.ids.size:b.scoped.size, total = allSets?b.total.size:b.scopedTotal.size;
      return n+(n===total?'':' of '+total)+' finding'+(total===1?'':'s');
    };
    return '<p class="vf-set-count" role="status">'+(batches.length>pageSize ? 'Tasks '+(start+1)+'–'+(start+shown.length)+' of '+batches.length : batches.length+(batches.length===1?' task':' tasks'))
      +(allSets?' across all practices and evidence types':' for the practice and evidence type above')+'</p>'
      + (shown.length ? '<ul class="vf-set-list">'+shown.map(b => '<li><button type="button" data-batch="'+esc(b.id)+'" onclick="DashboardPriority.openTask(this.dataset.batch)" aria-label="Open findings: '+esc(b.label)+'"'
        +(selected()===b.id?' aria-current="true"':'')+'><strong>'+esc(b.label)+'</strong><span class="vf-task-hint">'+esc(taskHint(b.id))+'</span><span class="vf-task-bottom"><small>'+count(b)+'</small><span class="vf-task-open">Open findings →</span></span></button></li>').join('')+'</ul>'
        : '<p class="vf-set-empty">'+(query?'No tasks match your search.':'No tasks match this status. Choose All requests to see earlier work.')+' You can still review the findings below.</p>')
      + (batches.length>pageSize ? '<nav class="vf-task-pages" aria-label="Review task pages"><button type="button" class="pill-btn" onclick="DashboardPriority.turnPage(-1)"'+(taskPage===0?' disabled':'')+'>Previous tasks</button><span>Page '+(taskPage+1)+' of '+Math.ceil(batches.length/pageSize)+'</span><button type="button" class="pill-btn" onclick="DashboardPriority.turnPage(1)"'+(start+pageSize>=batches.length?' disabled':'')+'>Next tasks</button></nav>' : '');
  }
  function filterSets(value, includeAll) {
    setSearch = value; allSets = includeAll; taskPage = 0;
    document.getElementById('vf-set-results').innerHTML = setList();
  }
  function turnPage(delta) {
    taskPage = Math.max(0,taskPage+delta);
    document.getElementById('vf-set-results').innerHTML = setList();
    document.querySelector('.vf-set-list button')?.focus({preventScroll:true});
  }
  function goToFindings() {
    const cards = document.getElementById('vf-cards');
    cards?.scrollIntoView({block:'start'});
    cards?.focus({preventScroll:true});
  }
  function openTask(value) { choose(value); goToFindings(); }
  function setView(value) {
    window._vfPriorityView = value; taskPage = 0;
    if (selected() !== 'all') {
      if (value === 'attention' && window._vfSimpleView === 'advanced') window._vfSimpleView = 'todo';
      else if (value !== 'attention') { window._vfSimpleView = 'advanced'; window._vfAxStatus = 'any'; }
    }
    renderVfWorklist();
    const picker = document.querySelector('.vf-review-sets');
    if (picker) picker.open = true;
    document.getElementById('vf-set-status')?.focus();
  }
  function choose(value) {
    const expandScope = allSets && value !== 'all' && value !== 'high';
    setSearch = ''; allSets = false; taskPage = 0;
    if (expandScope) set(value);
    else {
      window._vfPriorityEvidence = '';
      window._vfPriority = value;
      if (value !== 'all' && priorityView() !== 'attention') { window._vfSimpleView = 'advanced'; window._vfAxStatus = 'any'; }
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
    if (pickerScope !== scopeKey) { setSearch = ''; allSets = false; taskPage = 0; pickerScope = scopeKey; }
    const current = selected(), focused = window._vfPriorityEvidence;
    const batchRows = rows().filter(r => r.batch_id === current);
    const label = current === 'high' ? 'High priority' : batchRows[0]?.batch_label || current;
    const focus = focused ? '<div class="vf-single-finding"><span><strong>Single finding</strong> · Opened from a direct link</span><button type="button" class="pill-btn" onclick="DashboardPriority.backToQueue()">Back to queue</button></div>' : '';
    if (!rows().length) return focus;
    return focus + '<section class="vf-priority-controls" aria-label="Review tasks">'
      + (current !== 'all' ? '<div class="vf-selected-set"><div class="vf-task-current"><span>Working on <strong>'+esc(label)+'</strong></span><small>'+esc(viewLabels[priorityView()])+' · Open each finding, read its source, then choose Keep, Drop or Query.</small></div><div class="vf-task-actions"><button type="button" class="pill-btn vf-task-primary" onclick="DashboardPriority.goToFindings()">Go to findings ↓</button>'+(current !== 'high' && reviewData.priority_requests ? '<button type="button" class="pill-btn" data-batch="'+esc(current)+'" title="Change shared task status for the team; a reason is required. Finding decisions stay unchanged." onclick="PriorityStatus.open(this.dataset.batch)">Mark done / set aside</button>' : '')+'<button type="button" class="pill-btn" onclick="DashboardPriority.choose(\'all\')">All findings</button></div></div>' : '')
      + '<details class="vf-review-sets"><summary>Choose a review task <span>Optional</span></summary><div class="vf-set-browser">'
      + '<p class="vf-task-intro">Choose <strong>Open findings</strong> on a task below. Then compare each finding with its source and save your decision.</p>'
      + '<div class="vf-set-tools"><label for="vf-set-status">Show<select id="vf-set-status" onchange="DashboardPriority.setView(this.value)">'+Object.entries(viewLabels).map(([value,label])=>'<option value="'+value+'"'+(priorityView()===value?' selected':'')+'>'+esc(label)+'</option>').join('')+'</select></label><label for="vf-set-search">Find a task<input id="vf-set-search" type="search" placeholder="Search tasks, e.g. source checks" value="'+esc(setSearch)+'" oninput="DashboardPriority.filterSets(this.value,document.getElementById(\'vf-all-sets\').checked)"></label>'
      + '<div class="vf-task-scope"><label class="vf-set-toggle"><input id="vf-all-sets" type="checkbox"'+(allSets?' checked':'')+' onchange="DashboardPriority.filterSets(document.getElementById(\'vf-set-search\').value,this.checked)"> Browse all practices and types</label><button type="button" class="pill-btn" onclick="DashboardPriority.openTask(\'high\')">Open high-priority findings</button></div></div>'
      + '<div id="vf-set-results">'+setList()+'</div>'
      + '<p class="vf-set-help">Earlier work is under Reviewed / excluded or Addressed / deprioritized. Opening a task does not record a review.</p>'
      + (batchRows.length ? '<details class="vf-set-records"><summary>Direct links for this task ('+new Set(batchRows.map(r=>r.evidence_id)).size+')</summary><ul>'+[...new Map(batchRows.map(r=>[r.evidence_id,r])).values()].map(r=>'<li><a href="'+cardRoute(r.evidence_id)+'">'+esc(r.evidence_id)+'</a> · '+esc(r.source_id)+' · '+sourceLocation(r)+'</li>').join('')+'</ul></details>' : '')
      + '</div></details></section>';
  }

  function badge(ev) {
    const all = notes(ev.evidence_id), list = all.filter(r => ['active','recheck'].includes(r.status || 'active'));
    if (all.length && !list.length) return '<span class="vf-priority-history">Earlier review priority</span>';
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

      const original = '<b>'+esc(r.batch_label)+'</b>'+(r.requested_by?' · requested by '+esc(r.requested_by):'')+(r.requested_date?' · '+esc(r.requested_date):'')
        +(r.context_changed?'<p>Evidence changed since this request.</p>':'')
        +(r.reason?'<p><b>Why prioritized:</b> '+esc(r.reason)+'</p>':'')+(r.decision_needed?'<p><b>Decision needed:</b> '+esc(r.decision_needed)+'</p>':'');
      const older = latest && r.requested_date && r.requested_date < latest.date;
      const settled = !['active','recheck'].includes(r.status || 'active');
      const history = r.history || [], last = history.at(-1);
      const trail = history.length ? '<details><summary>Team priority history</summary>'+history.slice().reverse().map(h => '<p>'+esc(h.date)+' · '+esc(h.actor)+' · '+esc(h.action)+' · <a href="https://github.com/RuralScan/evidence/issues/'+encodeURIComponent(h.receipt)+'">Receipt #'+esc(h.receipt)+'</a><br>'+esc(h.reason)+(h.current?'':'<br>Inputs changed since this action.')+'</p>').join('')+'</details>' : '';
      const action = r.request_sha256 ? '<button type="button" class="pill-btn" data-batch="'+esc(r.batch_id)+'" data-evidence="'+esc(r.evidence_id)+'" onclick="PriorityStatus.open(this.dataset.batch,this.dataset.evidence)">Change task status</button>' : '';
      const state = '<p class="vf-priority-state"><strong>'+esc(statusLabels[r.status] || 'Needs attention')+'</strong>'+action+'</p>'
        +(last ? '<p>'+esc(last.reason)+(last.current?'':'<br>Inputs changed; this request needs another look.')+'</p>' : '');
      return '<section class="vf-priority-note" style="margin:10px 0;padding:12px;border-left:3px solid var(--accent-amber);font-size:12px;line-height:1.6">'
        +(r.decision_needed && !settled && !older ? '<p><b>Review question:</b> '+esc(r.decision_needed)+'</p>' : '')
        +'<details><summary>Review request and history · '+esc(statusLabels[r.status] || 'Needs attention')+'</summary>'+state+(settled ? '<details><summary>Earlier review request</summary>'+original+'</details>' : older ? '<details><summary>Original review request · before this correction</summary>'+original+'</details>'
          +'<p>Check any remaining questions in the original request.</p>' : original)
        +'<details><summary>Request reference and links</summary><p>Source '+esc(r.source_id)+' · '+sourceLocation(r)+'</p>'
        +(r.mapping_id?'<p>Mapping: '+esc(r.mapping_id)+'</p>':'')+reference+'</details>'+trail
        +(ev.use_role==='structural_suitability'?'<p>Keep confirms the extraction. Changing a live mapping requires a separate reviewed change.</p>':'')+'</details></section>';
    }).join('');
  }
  window.DashboardPriority = {matches, set, route, leaveFocus, openFromHash, controls, badge, card, filterSets, choose, backToQueue, visibleRequest, needsAttention, setView, turnPage, openTask, goToFindings};
})();
