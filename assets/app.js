// ChinaFun3 Dashboard Interactivity (Mobile Nav + Table Filters)
document.addEventListener("DOMContentLoaded", () => {
  // Mobile navigation toggle
  const toggle = document.querySelector(".nav-toggle");
  const nav = document.querySelector(".site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", () => {
      const isOpen = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", String(isOpen));
    });
  }

  // Table category filtering
  const filterBars = document.querySelectorAll("[data-filter-table]");
  filterBars.forEach((bar) => {
    const tableId = bar.getAttribute("data-filter-table");
    const table = document.getElementById(tableId);
    if (!table) return;
    const buttons = bar.querySelectorAll(".filter-btn");
    const rows = table.querySelectorAll("tbody tr");

    buttons.forEach((btn) => {
      btn.addEventListener("click", () => {
        buttons.forEach((b) => b.classList.remove("active"));
        btn.classList.add("active");
        const filter = btn.getAttribute("data-filter");
        rows.forEach((row) => {
          const tags = (row.getAttribute("data-tags") || "").split(",");
          if (filter === "all" || tags.includes(filter)) {
            row.style.display = "";
          } else {
            row.style.display = "none";
          }
        });
      });
    });
  });
});
