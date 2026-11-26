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
        countEl.textContent = "Showing " + shown + " of " + rows.length + " verified entries";
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
      var visaUsd = parseFloat(visaSel.value || "0");
      var diningCny = parseFloat(diningSel.value || "0");
      var actCny = parseFloat(actSel.value || "0");
      var totalCny = diningCny + actCny;
      var approxCnyInUsd = totalCny / 7.24;
      var combinedApproxUsd = hotelUsd + visaUsd + approxCnyInUsd;

      outBox.innerHTML =
        "<strong>Verified USD Components (Hotel + Visa):</strong> $" +
        (hotelUsd + visaUsd).toFixed(2) +
        " USD ($" +
        hotelUsd.toFixed(2) +
        " 7-night tax-incl. hotel + $" +
        visaUsd.toFixed(2) +
        " US entry pathway)<br>" +
        "<strong>Verified CNY On-Ground Bundle (Published Menus + Transit + Tickets):</strong> CNY " +
        totalCny.toFixed(2) +
        " (approx. $" +
        approxCnyInUsd.toFixed(0) +
        " USD at indicative 7.24 CNY/USD)<br>" +
        "<strong>Combined Verified Baseline for Two Travelers:</strong> ~$" +
        combinedApproxUsd.toFixed(0) +
        " USD <span class='muted-note'>Strictly excludes unverified international airfare and unpublished à la carte/3★ tasting balances (see Flagged F06/F10).</span>";
    }

    [hotelSel, visaSel, diningSel, actSel].forEach(function (el) {
      el.addEventListener("change", updateBudget);
    });
    updateBudget();
  }
})();
