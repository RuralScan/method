// Native links provide shareable records. Keep the activation point across Back/Forward.
const focusKey = "ruralscan-focus:" + location.pathname + location.search;
document.addEventListener("click", event => {
  const link = event.target.closest("a[href]");
  if (!link) return;
  try { sessionStorage.setItem(focusKey, String(Array.from(document.links).indexOf(link))); } catch {}
});
window.addEventListener("pageshow", event => {
  if (!event.persisted && performance.getEntriesByType("navigation")[0]?.type !== "back_forward") return;
  try {
    const saved = sessionStorage.getItem(focusKey);
    const link = saved === null ? null : document.links[Number(saved)];
    if (link) {
      for (let node = link.parentElement; node; node = node.parentElement) {
        if (node.tagName === "DETAILS") node.open = true;
      }
      link.focus({preventScroll:true});
      const bounds = link.getBoundingClientRect();
      if (bounds.top < document.querySelector(".bar").getBoundingClientRect().bottom || bounds.bottom > innerHeight)
        link.scrollIntoView({block:"center"});
    }
  } catch {}
});
const filter = document.querySelector("[data-filter]");
filter?.addEventListener("input", () => {
  const term = filter.value.toLowerCase().trim();
  for (const item of document.querySelectorAll("[data-filter-item]"))
    item.hidden = !item.textContent.toLowerCase().includes(term);
});
