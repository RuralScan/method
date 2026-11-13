(() => {
  const select = document.getElementById("dashboard-version");
  const note = document.getElementById("dashboard-version-note");
  if (!select || !note) return;
  const legacyViews = {
    "#overview": "index.html",
    "#progress": "progress.html",
    "#methods/rural": "methods.html",
    "#methods/evidence": "ai.html",
    "#methods/search": "searches.html",
    "#datasets": "table-T1.html"
  };
  select.addEventListener("change", () => {
    const option = select.selectedOptions[0];
    const url = new URL(option.value, document.baseURI);
    if (select.dataset.legacy && legacyViews[location.hash]) {
      url.pathname = url.pathname.replace(/index\.html$/, legacyViews[location.hash]);
    } else if (option.hasAttribute("data-match") && !url.hash) {
      url.hash = location.hash;
    }
    location.assign(url);
  });
  // Browsers can cache the control's last value when returning with Back.
  window.addEventListener("pageshow", () => {
    select.selectedIndex = Array.from(select.options).findIndex(option => option.defaultSelected);
  });
})();
