// Progressive enhancement only. Every page reads fully without this file.
(function () {
  // Version selector: open the chosen version, and show this page as selected on return.
  var version = document.getElementById('dashboard-version');
  if (version) {
    version.addEventListener('change', function () {
      window.location.assign(version.value);
    });
    window.addEventListener('pageshow', function () {
      for (var i = 0; i < version.options.length; i += 1) {
        if (version.options[i].defaultSelected) version.selectedIndex = i;
      }
    });
  }
  // Theme: dark by default, as on the live dashboard. The button and its wording follow the visual
  // methodology's. The choice is remembered on this device.
  var toggle = document.getElementById('theme-toggle');
  if (toggle) {
    var root = document.documentElement;
    var show = function () {
      var dark = root.getAttribute('data-theme') !== 'light';
      toggle.setAttribute('aria-pressed', String(dark));
      toggle.querySelector('span').textContent = dark ? 'Light theme' : 'Dark theme';
      toggle.classList.toggle('is-dark', dark);
    };
    toggle.hidden = false;
    toggle.addEventListener('click', function () {
      var next = root.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
      root.setAttribute('data-theme', next);
      try { localStorage.setItem('reference-theme', next); } catch (e) { /* not stored; the page still switches */ }
      show();
    });
    show();
  }
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
  // Way back: a link to another page of this methodology remembers where it was followed from.
  // The page it opens then offers one link that returns to that spot.
  var KEY = 'methodology-return';
  var main = document.getElementById('main');
  function sectionAbove(node) {
    var heads = main ? main.querySelectorAll('h2[id], h3[id]') : [], found = null;
    for (var i = 0; i < heads.length; i++) {
      if (heads[i].compareDocumentPosition(node) & Node.DOCUMENT_POSITION_FOLLOWING) found = heads[i];
    }
    return found;
  }
  document.addEventListener('click', function (event) {
    var a = event.target.closest ? event.target.closest('main a[href]') : null;
    if (!a || a.classList.contains('wayback') || a.target === '_blank' || a.origin !== location.origin || a.pathname === location.pathname) return;
    var page = document.querySelector('main > h1'), head = sectionAbove(a);
    var home = /(\/|\/index\.html)$/.test(location.pathname);
    var label = (home ? 'Overview' : page ? page.textContent.trim() : document.title) + (head ? ': ' + head.textContent.trim().replace(/\s+/g, ' ') : '');
    try {
      sessionStorage.setItem(KEY, JSON.stringify({from: location.pathname + location.search, to: a.pathname, y: window.scrollY, label: label}));
    } catch (e) { /* not stored; the browser's Back button still returns to the same spot */ }
  });
  try {
    var saved = JSON.parse(sessionStorage.getItem(KEY) || 'null');
    if (saved && saved.to === location.pathname && main) {
      var back = document.createElement('a');
      back.className = 'wayback';
      back.href = saved.from;
      back.textContent = '\u2190 Back to ' + saved.label;
      back.addEventListener('click', function () {
        try { sessionStorage.setItem(KEY + '-y', JSON.stringify({page: saved.from, y: saved.y})); sessionStorage.removeItem(KEY); } catch (e) { /* plain link */ }
      });
      main.insertBefore(back, main.firstChild);
    }
    var spot = JSON.parse(sessionStorage.getItem(KEY + '-y') || 'null');
    if (spot) {
      sessionStorage.removeItem(KEY + '-y');
      if (spot.page === location.pathname + location.search) window.scrollTo(0, spot.y);
    }
  } catch (e) { /* no way-back link; nothing else depends on it */ }
})();
