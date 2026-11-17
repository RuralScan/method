/* Keep existing root bookmarks intact while Methodology becomes the home page. */
(function () {
  'use strict';
  function destination(href) {
    const previous = new URL(href);
    const legacy = Boolean(previous.hash) || previous.searchParams.has('edition-section')
      || previous.searchParams.has('edition-fallback');
    const target = new URL(legacy ? 'dashboard.html' : 'reference/index.html', previous);
    target.search = previous.search;
    target.hash = previous.hash;
    return target.href;
  }
  if (typeof module !== 'undefined') module.exports = {destination};
  else location.replace(destination(location.href));
})();
