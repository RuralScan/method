// Progressive enhancement only. Every page reads fully without this file.
(function () {
  // Bring the current section tab into view on narrow screens.
  var current = document.querySelector('.tabs a[aria-current]');
  if (current && current.scrollIntoView) {
    current.scrollIntoView({ block: 'nearest', inline: 'center' });
  }
  // Collapse the section contents on small screens so the page title is reachable.
  var side = document.querySelector('.side details');
  if (side && window.matchMedia('(max-width: 900px)').matches) {
    side.removeAttribute('open');
  }
  // Filter a table's rows as the reader types.
  document.querySelectorAll('input[data-filter]').forEach(function (input) {
    var table = document.getElementById(input.getAttribute('data-filter'));
    if (!table) return;
    var rows = Array.prototype.slice.call(table.tBodies[0].rows);
    var status = document.createElement('span');
    status.setAttribute('role', 'status');
    status.className = 'basis';
    status.style.marginLeft = '.6rem';
    input.insertAdjacentElement('afterend', status);
    input.addEventListener('input', function () {
      var terms = input.value.toLowerCase().split(/\s+/).filter(Boolean);
      var shown = 0;
      rows.forEach(function (row) {
        var text = row.textContent.toLowerCase();
        var match = terms.every(function (t) { return text.indexOf(t) !== -1; });
        row.hidden = !match;
        if (match) shown += 1;
      });
      status.textContent = terms.length ? shown + ' of ' + rows.length + ' shown' : '';
    });
  });
  // Open a collapsed block when a link targets something inside it.
  function reveal() {
    if (!location.hash) return;
    var target = document.getElementById(decodeURIComponent(location.hash.slice(1)));
    for (var el = target; el; el = el.parentElement) {
      if (el.tagName === 'DETAILS') el.open = true;
    }
    if (target && target.scrollIntoView) target.scrollIntoView();
  }
  window.addEventListener('hashchange', reveal);
  reveal();
})();
