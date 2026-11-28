(function () {
  "use strict";

  // 1. Mobile Navigation Drawer Toggle
  var navToggle = document.getElementById("nav-toggle");
  var mainNav = document.getElementById("main-nav");
  if (navToggle && mainNav) {
    navToggle.addEventListener("click", function () {
      var isOpen = mainNav.classList.toggle("open");
      navToggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
    });
  }

  // 2. Generic Table Filter Handler (Hotels & Restaurants)
  function initTableFilter(containerId, tableId, countId, searchId) {
    var bar = document.getElementById(containerId);
    var table = document.getElementById(tableId);
    var countEl = document.getElementById(countId);
    var searchEl = searchId ? document.getElementById(searchId) : null;
    if (!bar || !table) return;

    var buttons = Array.prototype.slice.call(bar.querySelectorAll(".filter-btn"));
    var rows = Array.prototype.slice.call(table.querySelectorAll("tbody tr"));
    var activeTag = "all";

    function applyFilter() {
      var query = searchEl ? searchEl.value.trim().toLowerCase() : "";
      var shown = 0;
      rows.forEach(function (row) {
        var tags = (row.getAttribute("data-tags") || "").split(/\s+/);
        var text = row.textContent.toLowerCase();
        var tagMatch = activeTag === "all" || tags.indexOf(activeTag) !== -1;
        var searchMatch = !query || text.indexOf(query) !== -1;
        if (tagMatch && searchMatch) {
          row.style.display = "";
          shown += 1;
        } else {
          row.style.display = "none";
        }
      });
      if (countEl) {
        countEl.textContent = "Showing " + shown + " of " + rows.length + " shortlisted properties";
      }
    }

    buttons.forEach(function (btn) {
      btn.addEventListener("click", function () {
        buttons.forEach(function (b) {
          b.classList.remove("active");
        });
        btn.classList.add("active");
        activeTag = btn.getAttribute("data-filter") || "all";
        applyFilter();
      });
    });

    if (searchEl) {
      searchEl.addEventListener("input", applyFilter);
    }

    applyFilter();
  }

  initTableFilter("hotel-filters", "hotels-table", "hotel-count", null);
  initTableFilter("restaurant-filters", "restaurants-table", "restaurant-count", "restaurant-search");

  // 3. Interactive Verified Couple Budget Calculator
  var hotelSel = document.getElementById("calc-hotel");
  var visaSel = document.getElementById("calc-visa");
  var diningSel = document.getElementById("calc-dining");
  var actSel = document.getElementById("calc-activities");
  var outBox = document.getElementById("calc-result");

  if (hotelSel && visaSel && diningSel && actSel && outBox) {
    function updateBudget() {
      var hotelUsd = parseFloat(hotelSel.value || "0");
      var hasVisaExample = visaSel.value !== "";
      var visaUsd = hasVisaExample ? parseFloat(visaSel.value) : 0;
      var diningCny = parseFloat(diningSel.value || "0");
      var actCny = parseFloat(actSel.value || "0");
      var totalCny = diningCny + actCny;
      var approxCnyInUsd = totalCny / 7.24;
      var subtotalUsd = hotelUsd + visaUsd + approxCnyInUsd;
      var visaLine = hasVisaExample
        ? "Conditional example (not traveler-specific): " + visaSel.options[visaSel.selectedIndex].text
        : "Not included — passport nationality, visa status, and route are unknown";
      var subtotalLabel = hasVisaExample
        ? "Illustrative subtotal including the selected conditional visa example"
        : "Observed subtotal before visa / entry costs and airfare";

      outBox.innerHTML =
        "<strong>Dated hotel quote snapshot:</strong> $" +
        hotelUsd.toFixed(2) +
        " USD (7 nights; checked 2026-11-26)<br>" +
        "<strong>Visa / entry scenario:</strong> " + visaLine + "<br>" +
        "<strong>Published CNY on-ground bundle (menus + transit + tickets):</strong> CNY " +
        totalCny.toFixed(2) +
        " (about $" +
        approxCnyInUsd.toFixed(0) +
        " USD at the indicative 7.24 CNY/USD rate)<br>" +
        "<strong>" + subtotalLabel + ":</strong> about $" +
        subtotalUsd.toFixed(0) +
        " USD for two <span class='muted-note'>This is not a complete trip budget: airfare, unknown visa/entry costs when not selected, unpriced à la carte/3★ balances, and rate changes are excluded. See Flags F06, F17, and F18.</span>";
    }

    [hotelSel, visaSel, diningSel, actSel].forEach(function (el) {
      el.addEventListener("change", updateBudget);
    });
    updateBudget();
  }
})();
