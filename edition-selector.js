(() => {
  const select = document.getElementById("dashboard-version");
  const note = document.getElementById("dashboard-version-note");
  if (!select || !note) return;

  // On narrow screens the historical source drawer otherwise covers the selector.
  if (select.dataset.legacy) {
    new ResizeObserver(([entry]) => {
      document.documentElement.style.setProperty("--edition-bar-height",
        entry.target.getBoundingClientRect().height + "px");
    }).observe(select.parentElement);
  }

  const url = new URL(location.href);
  const requested = url.searchParams.get("edition-section");
  if (requested) {
    const section = document.getElementById(requested);
    if (section) {
      url.searchParams.delete("edition-section");
      url.hash = encodeURIComponent(requested);
      location.replace(url);
    } else {
      note.textContent = "This section is unavailable in this edition. Showing the start of the same page.";
    }
  } else if (url.searchParams.get("edition-fallback") === "overview") {
    note.textContent = "This record or view is unavailable in this edition. Showing its overview.";
  }

  select.addEventListener("change", () => {
    const option = select.selectedOptions[0];
    const target = new URL(option.value, document.baseURI);
    let fragment;
    try { fragment = decodeURIComponent(location.hash.slice(1)); }
    catch { fragment = location.hash.slice(1); }

    if (select.dataset.legacy && option.dataset.edition) {
      const routes = JSON.parse(document.getElementById("legacy-version-routes").textContent);
      const page = routes[option.dataset.edition]["#" + fragment];
      if (typeof page === "string") target.pathname = target.pathname.replace(/index\.html$/, page);
      else if (fragment) target.searchParams.set("edition-fallback", "overview");
    } else if (option.hasAttribute("data-match") && (fragment || requested)) {
      // Resolve the fragment against the destination's actual DOM on arrival.
      target.searchParams.set("edition-section", fragment || requested);
    } else if (option.hasAttribute("data-fallback")) {
      target.searchParams.set("edition-fallback", "overview");
    }
    location.assign(target);
  });
  window.addEventListener("pageshow", () => {
    select.selectedIndex = Array.from(select.options).findIndex(option => option.defaultSelected);
  });
})();
