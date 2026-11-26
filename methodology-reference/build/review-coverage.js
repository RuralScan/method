/* Read-only explorer. Selection changes no evidence or review decisions. */
(function () {
  'use strict';
  const matchStatus = (value, state) => state === 'all' ||
    (state === 'retained' ? value !== 'rejected' :
      state === 'awaiting' ? ['pending', 'held'].includes(value) : value === state);
  function select(data, filters) {
    let ids = null;
    if (filters.node) {
      const scope = data.scopes[filters.node];
      if (!scope) return [];
      ids = new Set(filters.relation === 'broader' ? scope.broader_evidence_ids :
        filters.relation === 'legacy' ? scope.legacy_scope_evidence_ids :
          [...scope.direct_evidence_ids, ...scope.descendant_evidence_ids]);
    } else if (filters.relation !== 'included') return [];
    const term = (filters.q || '').trim().toLowerCase();
    return data.findings.filter(f => (!ids || ids.has(f.evidence_id)) &&
      f.lanes.includes(filters.lane) && matchStatus(f.status, filters.state) &&
      (!term || [f.evidence_id, f.source_id, f.citation, f.variable].join(' ').toLowerCase().includes(term)))
      .sort((a, b) => a.evidence_id.localeCompare(b.evidence_id));
  }
  const sourceCount = findings => new Set(findings.map(f => f.source_id)).size;
  if (typeof module !== 'undefined') module.exports = { select, matchStatus, sourceCount };
  if (typeof document === 'undefined') return;
  const root = document.getElementById('coverage-browser');
  if (!root) return;
  const form = document.getElementById('coverage-filters');
  const status = document.getElementById('coverage-status');
  const el = (tag, text) => {
    const node = document.createElement(tag);
    if (text !== undefined) node.textContent = text;
    return node;
  };
  fetch('data/review-findings.json').then(response => {
    if (!response.ok) throw new Error('Snapshot unavailable');
    return response.json();
  }).then(data => {
    const label = key => {
      const node = data.nodes[key];
      if (node.level === 'practice') return node.label.replaceAll('_', ' ');
      return node.nbs_id.replaceAll('_', ' ') + ' · ' + node.level.replaceAll('_', ' ') + ' · ' +
        node.label.split('__').pop().replaceAll('_', ' ');
    };
    for (const key of Object.keys(data.nodes).sort((a, b) => label(a).localeCompare(label(b)))) {
      const option = el('option', label(key)); option.value = key;
      form.elements.node.append(option);
    }
    const defaults = { node: '', lane: 'all', state: 'retained', relation: 'included', q: '' };
    const readURL = () => {
      const params = new URLSearchParams(location.search);
      for (const name of Object.keys(defaults)) {
        const control = form.elements[name];
        const value = params.get(name) || defaults[name];
        control.value = control.tagName === 'SELECT' && ![...control.options].some(o => o.value === value) ? defaults[name] : value;
      }
    };
    let offset = 0;
    const limit = 50;
    function render(updateURL = false) {
      const filters = Object.fromEntries(new FormData(form));
      if (updateURL) history.replaceState(null, '', '?' + new URLSearchParams(filters));
      const results = select(data, filters);
      const c = { reviewed_kept: 0, pending: 0, held: 0, rejected: 0 };
      for (const f of results) c[f.status]++;
      status.textContent = `${results.length.toLocaleString()} findings from ${sourceCount(results).toLocaleString()} source records in this view · ${c.reviewed_kept} reviewed and kept · ${c.pending} pending · ${c.held} held · ${c.rejected} rejected`;
      document.getElementById('coverage-scope-note').textContent = filters.relation === 'broader' ?
        'Broader context is not assigned to this child and is not added to its total.' : filters.relation === 'legacy' ?
          'Earlier family scopes need source-scope review before reassignment. Existing IDs and decisions are preserved.' :
          'Unique findings at this scope and its children. Pending and held findings remain visible; scope does not imply synthesis approval.';
      const box = document.getElementById('coverage-results'); box.replaceChildren();
      if (!results.length) box.append(el('p', filters.relation !== 'included' && !filters.node ?
        'Choose a practice or more specific scope to inspect its broader or earlier-scope evidence.' :
        'No findings match these filters. Try Total retained, another lane or Broader context.'));
      else {
        const wrapper = el('div'); wrapper.className = 'tablewrap';
        const table = el('table');
        table.append(el('caption', 'Table 1. Findings matching your filters'));
        const head = el('thead'), tr = el('tr');
        for (const title of ['Finding and variable', 'Source', 'Recorded scope', 'Review status']) {
          const th = el('th', title); th.scope = 'col'; tr.append(th);
        }
        head.append(tr); table.append(head);
        const tbody = el('tbody');
        for (const f of results.slice(offset, offset + limit)) {
          const row = el('tr'), finding = el('td'), a = el('a', f.evidence_id);
          a.href = f.url; finding.append(a, el('br'), el('small', f.variable.replaceAll('_', ' ')));
          row.append(finding, el('td', f.citation), el('td', label(f.node)), el('td', data.metadata.states[f.status]));
          tbody.append(row);
        }
        table.append(tbody); wrapper.append(table); box.append(wrapper);
      }
      document.getElementById('coverage-page').textContent = results.length ? `${offset + 1}–${Math.min(offset + limit, results.length)} of ${results.length}` : '0 findings';
      document.getElementById('coverage-prev').disabled = offset === 0;
      document.getElementById('coverage-next').disabled = offset + limit >= results.length;
    }
    form.addEventListener('submit', event => event.preventDefault());
    form.addEventListener('input', () => { offset = 0; render(true); });
    form.addEventListener('reset', event => {
      event.preventDefault();
      for (const [key, value] of Object.entries(defaults)) form.elements[key].value = value;
      offset = 0; render(true);
    });
    document.getElementById('coverage-prev').addEventListener('click', () => { offset = Math.max(0, offset - limit); render(); });
    document.getElementById('coverage-next').addEventListener('click', () => { offset += limit; render(); });
    addEventListener('popstate', () => { readURL(); offset = 0; render(); });
    readURL(); render();
  }).catch(() => {
    status.textContent = 'Could not load the pinned snapshot. Reload or download the finding data below. No review decisions were changed.';
    form.hidden = true;
    document.querySelector('.coverage-pagination').hidden = true;
  });
})();
