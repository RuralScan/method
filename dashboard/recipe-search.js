/* Load the evidence catalogue after the reader asks for a search. */
(() => {
  const form = document.getElementById("evidence-search");
  const results = document.getElementById("evidence-results");
  const status = document.getElementById("evidence-status");
  const retry = document.getElementById("evidence-retry");
  if (!form) return;
  let catalogue;
  let sequence = 0;

  async function search(event, retryExact = false) {
    event?.preventDefault();
    const request = ++sequence;
    const term = form.elements.q.value.toLowerCase().trim();
    results.replaceChildren();
    retry.hidden = true;
    if (!term) {
      status.textContent = "Enter a source, variable or identifier.";
      form.elements.q.focus();
      return;
    }
    status.textContent = "Searching this edition…";
    try {
      if (!catalogue) {
        const response = await fetch("recipe-catalogue.json");
        if (!response.ok) throw new Error("Catalogue unavailable");
        catalogue = await response.json();
      }
      if (request !== sequence) return;
      const items = catalogue.filter(item => item.search.includes(term));
      if (retryExact) {
        const exact = items.filter(item => item.id.toLowerCase() === term);
        if (exact.length === 1) {
          location.assign(exact[0].path);
          return;
        }
      }
      const page = items.slice(0, 40);
      status.textContent = items.length > page.length
        ? `Showing the first 40 of ${items.length.toLocaleString()} matches. Refine your search for more detail.`
        : `${items.length.toLocaleString()} ${items.length === 1 ? "match" : "matches"}.`;
      for (const item of page) {
        const li = document.createElement("li");
        const a = document.createElement("a");
        a.href = item.path;
        a.textContent = item.label;
        li.append(a);
        results.append(li);
      }
    } catch {
      if (request !== sequence) return;
      status.textContent = "The catalogue could not be loaded. Retry this search or open the portable workbook.";
      retry.hidden = false;
    }
  }
  form.addEventListener("submit", search);
  retry.addEventListener("click", event => search(event, true));
  // A reader can submit the native form before its deferred script loads.
  const query = new URLSearchParams(location.search).get("q");
  if (query) {
    form.elements.q.value = query;
    search();
  }
})();
