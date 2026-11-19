/* Methodology is home; explicit evidence and finding routes keep their workspace. */
(function () {
  'use strict';
  function destination(href) {
    const previous = new URL(href);
    const methodPages = {'#overview': 'index.html', '#methods': 'method.html',
      '#methods/rural': 'method.html', '#methods/evidence': 'evidence-methods.html',
      '#methods/search': 'ch-discovery.html'};
    const legacy = Boolean(previous.hash) || previous.searchParams.has('edition-section')
      || previous.searchParams.has('edition-fallback');
    const methodPage = methodPages[previous.hash];
    const target = new URL(methodPage ? 'reference/' + methodPage : legacy ? 'dashboard.html' : 'reference/index.html', previous);
    target.search = previous.search;
    target.hash = methodPage ? '' : previous.hash;
    return target.href;
  }
  if (typeof module !== 'undefined') module.exports = {destination};
  else { const target = destination(location.href); if (target !== location.href) location.replace(target); }
})();
