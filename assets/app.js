/* ==========================================================================
   ChinaFun3 — Client Data Loader & Interactive UI Engine
   Dynamically renders verified JSON datasets with zero unverified guesses.
   ========================================================================== */

(function () {
  "use strict";

  const isSubpage = window.location.pathname.includes("/pages/");
  const ROOT = isSubpage ? ".." : ".";

  /* ---------- Utilities ---------- */
  function esc(value) {
    if (value === null || value === undefined) return "";
    return String(value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function safeUrl(url) {
    if (!url || typeof url !== "string") return "";
    const trimmed = url.trim();
    if (trimmed.startsWith("https://") || trimmed.startsWith("http://")) {
      return trimmed;
    }
    return "";
  }

  async function fetchJson(relPath) {
    const res = await fetch(`${ROOT}/${relPath}`, { cache: "no-cache" });
    if (!res.ok) throw new Error(`Failed to load ${relPath} (HTTP ${res.status})`);
    return res.json();
  }

  function blankOrVal(val, reviewNote) {
    if (val === null || val === undefined || val === "") {
      return `<span class="blank-cell" title="${esc(reviewNote || "Unverified in primary official sources — see Flagged for Review")}">—</span> <span class="badge badge-review">Needs review</span>`;
    }
    return esc(val);
  }

  function renderSocialLinks(links) {
    if (!Array.isArray(links) || links.length === 0) {
      return `<span class="text-muted text-sm">No verified social links</span>`;
    }
    return links
      .map((s) => {
        const href = safeUrl(s.url);
        if (!href) return "";
        return `<a class="btn btn-ghost" href="${esc(href)}" target="_blank" rel="noopener noreferrer">${esc(s.platform)}: ${esc(s.label)} ↗</a>`;
      })
      .join("");
  }

  /* ---------- Shared Header & Footer ---------- */
  function initShell(activePage) {
    const header = document.getElementById("site-header");
    if (header) {
      const navItems = [
        { key: "home", label: "Overview", href: `${ROOT}/index.html` },
        { key: "restaurants", label: "MICHELIN Dining", href: `${ROOT}/pages/restaurants.html` },
        { key: "hotels", label: "Hotels & Timing", href: `${ROOT}/pages/hotels.html` },
        { key: "activities", label: "Activities", href: `${ROOT}/pages/activities.html` },
        { key: "planning", label: "Planning & Roadmap", href: `${ROOT}/pages/planning.html` },
        { key: "review", label: "Flagged for Review", href: `${ROOT}/pages/review.html` }
      ];

      header.innerHTML = `
        <div class="container header-inner">
          <a class="brand" href="${ROOT}/index.html">
            <span class="brand-mark" aria-hidden="true">中</span>
            <span class="brand-text">
              <span class="brand-name">ChinaFun3</span>
              <span class="brand-tag">Feb–Mar 2027 · Verified MICHELIN Trip Planner</span>
            </span>
          </a>
          <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="primary-nav" id="nav-toggle-btn">
            Menu ☰
          </button>
          <ul class="nav-links" id="primary-nav">
            ${navItems
              .map(
                (n) =>
                  `<li><a href="${n.href}" ${n.key === activePage ? 'aria-current="page"' : ""}>${esc(n.label)}</a></li>`
              )
              .join("")}
          </ul>
        </div>
      `;

      const toggleBtn = document.getElementById("nav-toggle-btn");
      const navList = document.getElementById("primary-nav");
      if (toggleBtn && navList) {
        toggleBtn.addEventListener("click", () => {
          const isOpen = navList.classList.toggle("open");
          toggleBtn.setAttribute("aria-expanded", String(isOpen));
        });
      }
    }

    const footer = document.getElementById("site-footer");
    if (footer) {
      footer.innerHTML = `
        <div class="container">
          <div class="footer-grid">
            <div>
              <h3 class="footer-heading">ChinaFun3 Trip Planner</h3>
              <p style="margin:0;color:#b8b2a8;">
                Evidence-verified travel &amp; MICHELIN dining dashboard for 2 adults traveling to China between February 15 and March 23, 2027.
              </p>
            </div>
            <div>
              <h3 class="footer-heading">Dashboard Sections</h3>
              <ul class="footer-list">
                <li><a href="${ROOT}/index.html">Executive Summary &amp; Clusters</a></li>
                <li><a href="${ROOT}/pages/restaurants.html">MICHELIN Dining (29 Audited)</a></li>
                <li><a href="${ROOT}/pages/hotels.html">Hotels &amp; Booking Window (10 Ranked)</a></li>
                <li><a href="${ROOT}/pages/activities.html">Activities &amp; Landmarks (16 Verified)</a></li>
              </ul>
            </div>
            <div>
              <h3 class="footer-heading">Governance &amp; Transparency</h3>
              <ul class="footer-list">
                <li><a href="${ROOT}/pages/planning.html">Decision Questions &amp; Discovery Plan</a></li>
                <li><a href="${ROOT}/pages/review.html">Flagged for Review Audit Register</a></li>
                <li><a href="${ROOT}/COORDINATION.md">COORDINATION.md Source Log</a></li>
              </ul>
            </div>
          </div>
          <div class="footer-bottom">
            <span>Last primary verification pass: <strong>2026-11-25</strong> · All unverified prices/hours intentionally left blank (never estimated).</span>
            <span>Static JSON-driven site · GitHub Pages compatible</span>
          </div>
        </div>
      `;
    }

    initDriverModal();
  }

  /* ---------- Show Driver / Copy Address Modal ---------- */
  function initDriverModal() {
    if (document.getElementById("driver-modal")) return;
    const modal = document.createElement("div");
    modal.id = "driver-modal";
    modal.className = "modal-backdrop";
    modal.setAttribute("role", "dialog");
    modal.setAttribute("aria-modal", "true");
    modal.setAttribute("aria-labelledby", "driver-modal-title");
    modal.innerHTML = `
      <div class="modal-dialog">
        <div style="display:flex;justify-content:space-between;align-items:center;gap:12px;">
          <span class="badge badge-city">Taxi / DiDi / Concierge Card</span>
          <button type="button" class="btn btn-ghost" id="driver-modal-close">Close ✕</button>
        </div>
        <h3 class="modal-chinese" id="driver-modal-title"></h3>
        <div class="text-muted text-sm" id="driver-modal-en"></div>
        <div class="modal-addr" id="driver-modal-addr"></div>
        <div class="text-sm text-muted" id="driver-modal-metro"></div>
        <div class="btn-row mt-16">
          <button type="button" class="btn btn-primary" id="driver-modal-copy">Copy Address</button>
          <span id="driver-copy-status" class="text-sm" style="align-self:center;color:var(--emerald);font-weight:600;"></span>
        </div>
      </div>
    `;
    document.body.appendChild(modal);

    const closeBtn = document.getElementById("driver-modal-close");
    const copyBtn = document.getElementById("driver-modal-copy");
    const statusEl = document.getElementById("driver-copy-status");

    function close() {
      modal.classList.remove("open");
      statusEl.textContent = "";
    }

    closeBtn.addEventListener("click", close);
    modal.addEventListener("click", (e) => {
      if (e.target === modal) close();
    });
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && modal.classList.contains("open")) close();
    });

    copyBtn.addEventListener("click", async () => {
      const text = `${document.getElementById("driver-modal-title").textContent}\n${document.getElementById("driver-modal-addr").textContent}`;
      try {
        await navigator.clipboard.writeText(text);
        statusEl.textContent = "Copied!";
      } catch {
        statusEl.textContent = "Select & copy above";
      }
    });

    document.addEventListener("click", (e) => {
      const btn = e.target.closest(".btn-driver");
      if (!btn) return;
      document.getElementById("driver-modal-title").textContent = btn.dataset.zh || btn.dataset.en || "";
      document.getElementById("driver-modal-en").textContent = btn.dataset.en || "";
      document.getElementById("driver-modal-addr").textContent = btn.dataset.addr || "";
      document.getElementById("driver-modal-metro").textContent = btn.dataset.metro ? `Nearest Metro: ${btn.dataset.metro}` : "";
      statusEl.textContent = "";
      modal.classList.add("open");
    });
  }

  /* ========================================================================
     PAGE 1: OVERVIEW / EXECUTIVE SUMMARY (index.html)
     ======================================================================== */
  async function renderHome() {
    const [cal, gov] = await Promise.all([
      fetchJson("data/calendar-and-clusters.json"),
      fetchJson("data/governance.json")
    ]);

    const exec = gov.executiveSummary;

    // Itinerary cards
    const itinEl = document.getElementById("itinerary-options");
    if (itinEl) {
      itinEl.innerHTML = exec.recommendedItineraries
        .map(
          (opt, idx) => `
          <article class="card">
            <div class="card-meta-row">
              <span class="badge ${idx === 0 ? "badge-star" : idx === 1 ? "badge-verified" : "badge-review"}">${esc(opt.recommendedDates)}</span>
            </div>
            <h3 class="card-title">${esc(opt.option)}</h3>
            <p style="margin:0;color:var(--text-secondary);font-size:0.9rem;">${esc(opt.whyBest)}</p>
            <div class="spec-item">
              <span class="spec-label">Verified Anchor Hotels</span>
              <ul style="margin:4px 0 0;padding-left:18px;font-size:0.86rem;color:var(--text-primary);">
                ${opt.topHotelPicks.map((h) => `<li>${esc(h)}</li>`).join("")}
              </ul>
            </div>
          </article>
        `
        )
        .join("");
    }

    // Cost snapshot
    const costEl = document.getElementById("cost-snapshot");
    if (costEl) {
      costEl.innerHTML = exec.verifiedCostSnapshotForTwoAdults7Nights
        .map(
          (c) => `
          <article class="card">
            <h3 class="card-title">${esc(c.tier)}</h3>
            <div class="spec-list">
              <div class="spec-item">
                <span class="spec-label">Shanghai Hotel (7 Nights, 2 Adults, Incl. Tax)</span>
                <span class="spec-val num">${esc(c.shanghaiHotel7N)}</span>
              </div>
              <div class="spec-item">
                <span class="spec-label">Beijing Hotel (7 Nights, 2 Adults, Incl. Tax)</span>
                <span class="spec-val num">${esc(c.beijingHotel7N)}</span>
              </div>
              <div class="spec-item">
                <span class="spec-label">All 8 Audited Activities / City (Off-Season 2 Adults)</span>
                <span class="spec-val">${esc(c.activities8SitesCny)}</span>
              </div>
              <div class="spec-item">
                <span class="spec-label">Verified Official MICHELIN Menus (2 Adults)</span>
                <span class="spec-val">${esc(c.michelinDiningIllustrative)}</span>
              </div>
            </div>
          </article>
        `
        )
        .join("");
    }

    // Key takeaways
    const takeEl = document.getElementById("key-takeaways");
    if (takeEl) {
      takeEl.innerHTML = exec.keyBookingAndOperationalTakeaways
        .map((t) => `<li style="margin-bottom:8px;">${esc(t)}</li>`)
        .join("");
    }

    // 2027 Calendar table
    const calEl = document.getElementById("calendar-tbody");
    if (calEl) {
      calEl.innerHTML = cal.calendar2027
        .map(
          (ev) => `
          <tr>
            <td><strong>${esc(ev.event)}</strong></td>
            <td class="num">${esc(ev.dates)}</td>
            <td>${esc(ev.impact)}</td>
            <td><a href="${esc(safeUrl(ev.sourceUrl))}" target="_blank" rel="noopener noreferrer">${esc(ev.sourceName)} ↗</a></td>
          </tr>
        `
        )
        .join("");
    }

    // Climate cards
    const climEl = document.getElementById("climate-grid");
    if (climEl) {
      climEl.innerHTML = cal.climateNormals
        .map(
          (cl) => `
          <article class="card">
            <div class="card-meta-row">
              <span class="badge badge-city">${esc(cl.city)} Climate Normals</span>
            </div>
            <div class="grid-2" style="gap:10px;">
              <div class="spec-item" style="border-top:none;padding-top:0;">
                <span class="spec-label">February Avg (Low / High)</span>
                <span class="spec-val num">${esc(cl.febAvgC)}°C (${esc(cl.febLowHighC)}°C) · ${esc(cl.febRainMm)} mm rain</span>
              </div>
              <div class="spec-item" style="border-top:none;padding-top:0;">
                <span class="spec-label">March Avg (Low / High)</span>
                <span class="spec-val num">${esc(cl.marAvgC)}°C (${esc(cl.marLowHighC)}°C) · ${esc(cl.marRainMm)} mm rain</span>
              </div>
            </div>
            <p style="margin:0;font-size:0.88rem;color:var(--text-secondary);">${esc(cl.travelTakeaway)}</p>
            <a class="text-sm" href="${esc(safeUrl(cl.sourceUrl))}" target="_blank" rel="noopener noreferrer">Source: ${esc(cl.sourceName)} ↗</a>
          </article>
        `
        )
        .join("");
    }

    // 12 MICHELIN Clusters Table
    const clusterEl = document.getElementById("clusters-tbody");
    if (clusterEl) {
      clusterEl.innerHTML = cal.michelinClusters
        .map((c) => {
          const isDeepDive = c.selectedForDeepDive;
          return `
            <tr style="${isDeepDive ? "background:#fff9f9;" : ""}">
              <td class="num">#${esc(c.rank)}</td>
              <td>
                <strong>${esc(c.clusterName)}</strong>
                ${isDeepDive ? '<span class="badge badge-star" style="margin-left:6px;">Deep-Dive Hub</span>' : ""}
                <div class="text-muted text-sm">${esc(c.edition)} · ${esc(c.region)}</div>
              </td>
              <td class="num">${esc(c.totalListed)}</td>
              <td class="num">${esc(c.totalStarred)}★</td>
              <td class="num">${esc(c.threeStars)} / ${esc(c.twoStars)} / ${esc(c.oneStar)}</td>
              <td class="num">${c.bibGourmand !== null ? esc(c.bibGourmand) : '<span class="blank-cell">—</span>'}</td>
              <td class="num">${c.michelinSelected !== null ? esc(c.michelinSelected) : '<span class="blank-cell">—</span>'}</td>
              <td>
                <a href="${esc(safeUrl(c.sourceUrl))}" target="_blank" rel="noopener noreferrer">Official Release ↗</a>
              </td>
            </tr>
          `;
        })
        .join("");
    }
  }

  /* ========================================================================
     PAGE 2: MICHELIN RESTAURANTS (pages/restaurants.html)
     ======================================================================== */
  async function renderRestaurants() {
    const data = await fetchJson("data/restaurants.json");
    const list = data.restaurants;

    let state = {
      city: "ALL",
      category: "ALL", // ALL | STARRED | LISTED
      priceOnly: false,
      query: ""
    };

    const grid = document.getElementById("restaurants-grid");
    const countEl = document.getElementById("restaurants-count");
    const searchInput = document.getElementById("rest-search");
    const priceCheckbox = document.getElementById("rest-price-only");

    function badgeFor(r) {
      if (r.distinctionCategory === "MICHELIN Starred") {
        return `<span class="badge badge-star">★ ${esc(r.distinctionLabel)}</span>`;
      }
      if ((r.distinctionLabel || "").toLowerCase().includes("bib")) {
        return `<span class="badge badge-bib">${esc(r.distinctionLabel)} (Guide Listed)</span>`;
      }
      return `<span class="badge badge-selected">${esc(r.distinctionLabel)} (Guide Listed)</span>`;
    }

    function apply() {
      const q = state.query.trim().toLowerCase();
      const filtered = list.filter((r) => {
        if (state.city !== "ALL" && r.city !== state.city) return false;
        if (state.category === "STARRED" && r.distinctionCategory !== "MICHELIN Starred") return false;
        if (state.category === "LISTED" && r.distinctionCategory === "MICHELIN Starred") return false;
        if (state.priceOnly && !r.priceForTwoCny) return false;
        if (q) {
          const hay = `${r.name} ${r.city} ${r.district} ${r.cuisine} ${r.address} ${r.distinctionLabel}`.toLowerCase();
          if (!hay.includes(q)) return false;
        }
        return true;
      });

      const starredCount = filtered.filter((r) => r.distinctionCategory === "MICHELIN Starred").length;
      const listedCount = filtered.length - starredCount;
      if (countEl) {
        countEl.textContent = `Showing ${filtered.length} of ${list.length} audited venues (${starredCount} MICHELIN Starred · ${listedCount} MICHELIN Guide Listed)`;
      }

      if (!filtered.length) {
        grid.innerHTML = `<div class="loading-box">No restaurants match the current filters. Try clearing your search or toggling off "Official Menu Price Published".</div>`;
        return;
      }

      grid.innerHTML = filtered
        .map((r) => {
          const officialHref = safeUrl(r.officialWebsite);
          const michelinHref = safeUrl(r.michelinUrl);
          const priceHref = safeUrl(r.priceSourceUrl);
          const unverified = Array.isArray(r.unverifiedFields) && r.unverifiedFields.length > 0;

          return `
            <article class="card">
              <div class="card-meta-row">
                ${badgeFor(r)}
                <span class="badge badge-city">${esc(r.city)} · ${esc(r.district)}</span>
                <span class="badge badge-low">${esc(r.cuisine)} · ${esc(r.michelinPriceTier)}</span>
              </div>
              <div>
                <h3 class="card-title">${esc(r.name)}</h3>
                <p class="card-subtitle">${esc(r.nearestMetro ? `Metro: ${r.nearestMetro}` : "")} ${r.phone ? `· Tel: ${esc(r.phone)}` : ""}</p>
              </div>
              <div class="spec-list">
                <div class="spec-item">
                  <span class="spec-label">Official Verified Cost for 2 Adults (CNY)</span>
                  <span class="spec-val">
                    ${
                      r.priceForTwoCny
                        ? `${esc(r.priceForTwoCny)} ${priceHref ? `<a href="${esc(priceHref)}" target="_blank" rel="noopener noreferrer" class="text-sm">[Official Menu ↗]</a>` : ""}`
                        : `<span class="blank-cell">—</span> <span class="badge badge-review">Not published online — confirm when booking</span>`
                    }
                  </span>
                </div>
                <div class="spec-item">
                  <span class="spec-label">Days Open &amp; Hours</span>
                  <span class="spec-val">
                    ${
                      r.daysOpen || r.hours
                        ? `${r.daysOpen ? `<strong>${esc(r.daysOpen)}</strong>` : '<span class="blank-cell">Days unverified</span>'}${r.hours ? ` · ${esc(r.hours)}` : ' · <span class="blank-cell">Hours unverified</span>'}`
                        : `<span class="blank-cell">—</span> <span class="badge badge-review">Needs review</span>`
                    }
                  </span>
                </div>
                <div class="spec-item">
                  <span class="spec-label">Closure Exceptions &amp; Booking Notes</span>
                  <span class="spec-val">${esc(r.closureExceptions || "Check official venue before Lunar New Year tail (Feb 15–20).")}</span>
                </div>
                <div class="spec-item">
                  <span class="spec-label">Verbatim MICHELIN Address</span>
                  <span class="spec-val">${esc(r.address)}</span>
                </div>
              </div>
              <div class="btn-row">
                ${michelinHref ? `<a class="btn btn-primary" href="${esc(michelinHref)}" target="_blank" rel="noopener noreferrer">MICHELIN Guide ↗</a>` : ""}
                ${officialHref ? `<a class="btn btn-secondary" href="${esc(officialHref)}" target="_blank" rel="noopener noreferrer">Official Site ↗</a>` : ""}
                <button type="button" class="btn btn-ghost btn-driver" data-en="${esc(r.name)}" data-zh="${esc(r.name)}" data-addr="${esc(r.address)}" data-metro="${esc(r.nearestMetro || "")}">Show Address Card</button>
              </div>
              <div class="btn-row" style="border-top:1px solid var(--border-light);padding-top:10px;margin-top:4px;">
                ${renderSocialLinks(r.socialLinks)}
              </div>
              ${
                unverified
                  ? `<div class="text-sm text-muted">Audit fields flagged: <code>${esc(r.unverifiedFields.join(", "))}</code></div>`
                  : `<div class="text-sm" style="color:var(--emerald);font-weight:600;">✓ All core fields verified from primary sources</div>`
              }
            </article>
          `;
        })
        .join("");
    }

    document.querySelectorAll("[data-rest-city]").forEach((btn) => {
      btn.addEventListener("click", () => {
        document.querySelectorAll("[data-rest-city]").forEach((b) => b.classList.remove("active"));
        btn.classList.add("active");
        state.city = btn.dataset.restCity;
        apply();
      });
    });

    document.querySelectorAll("[data-rest-cat]").forEach((btn) => {
      btn.addEventListener("click", () => {
        document.querySelectorAll("[data-rest-cat]").forEach((b) => b.classList.remove("active"));
        btn.classList.add("active");
        state.category = btn.dataset.restCat;
        apply();
      });
    });

    if (searchInput) {
      searchInput.addEventListener("input", (e) => {
        state.query = e.target.value;
        apply();
      });
    }

    if (priceCheckbox) {
      priceCheckbox.addEventListener("change", (e) => {
        state.priceOnly = e.target.checked;
        apply();
      });
    }

    apply();
  }

  /* ========================================================================
     PAGE 3: HOTELS & BOOKING TIMING (pages/hotels.html)
     ======================================================================== */
  async function renderHotels() {
    const data = await fetchJson("data/hotels.json");
    const hotels = data.hotels;

    // Booking Window Benchmarks
    const benchEl = document.getElementById("booking-benchmarks");
    if (benchEl) {
      benchEl.innerHTML = data.cheapestBookingWindow.live2027WeeklyBenchmark
        .map((b) => {
          const maxVal = Math.max(...b.weeks.map((w) => w.total7NightUsdInclTax));
          return `
            <article class="card">
              <div class="card-meta-row">
                <span class="badge badge-city">${esc(b.city)}</span>
                <span class="badge badge-verified">Live 2027 Quotes (7 Nights, Incl. Tax)</span>
              </div>
              <h3 class="card-title">${esc(b.benchmarkHotel)}</h3>
              <p class="card-subtitle">${esc(b.roomType)}</p>
              <div class="mt-12">
                ${b.weeks
                  .map((w) => {
                    const pct = Math.round((w.total7NightUsdInclTax / maxVal) * 100);
                    const cls = w.vsCheapestPct === 0 ? "best" : w.vsCheapestPct > 25 ? "" : "warn";
                    return `
                      <div class="bar-row">
                        <div class="text-sm">
                          <strong>${esc(w.dates.replace("2027-", "").replace(" to 2027-", " → "))}</strong>
                          <div class="text-muted" style="font-size:11.5px;">${w.vsCheapestPct === 0 ? "Lowest verified" : `+${esc(w.vsCheapestPct)}% vs lowest`}</div>
                        </div>
                        <div class="bar-track" aria-hidden="true">
                          <div class="bar-fill ${cls}" style="width:${pct}%;"></div>
                        </div>
                        <div class="num" style="text-align:right;">
                          <a href="${esc(safeUrl(w.sourceUrl))}" target="_blank" rel="noopener noreferrer">US$${esc(w.total7NightUsdInclTax.toLocaleString())} ↗</a>
                        </div>
                      </div>
                    `;
                  })
                  .join("")}
              </div>
              <ul style="margin:8px 0 0;padding-left:18px;font-size:0.83rem;color:var(--text-secondary);">
                ${b.weeks.map((w) => `<li><strong>${esc(w.dates.slice(5, 10))}–${esc(w.dates.slice(19, 24))}:</strong> ${esc(w.context)}</li>`).join("")}
              </ul>
            </article>
          `;
        })
        .join("");
    }

    // Lead time study
    const leadEl = document.getElementById("lead-time-box");
    if (leadEl) {
      const g = data.cheapestBookingWindow.bookingLeadTimeGuidance;
      leadEl.innerHTML = `
        <h3 class="callout-title">Optimal Booking Timing Playbook · ${esc(g.sourceName)}</h3>
        <ul style="margin:6px 0 6px;padding-left:18px;font-size:0.9rem;color:var(--text-secondary);">
          ${g.keyFindings.map((f) => `<li style="margin-bottom:4px;">${esc(f)}</li>`).join("")}
        </ul>
        <a class="text-sm" href="${esc(safeUrl(g.sourceUrl))}" target="_blank" rel="noopener noreferrer">Read KAYAK May 2026 Hotel Booking Study ↗</a>
      `;
    }

    let state = { city: "ALL", sort: "rank" };
    const tableBody = document.getElementById("hotels-tbody");
    const cardsEl = document.getElementById("hotels-cards");
    const sortSelect = document.getElementById("hotel-sort");

    function apply() {
      let filtered = hotels.filter((h) => state.city === "ALL" || h.city === state.city);
      if (state.sort === "price-asc") {
        filtered = [...filtered].sort(
          (a, b) => a.pricing7NightsFeb22Mar1.lowestQueenKingUsdInclTax - b.pricing7NightsFeb22Mar1.lowestQueenKingUsdInclTax
        );
      } else if (state.sort === "price-desc") {
        filtered = [...filtered].sort(
          (a, b) => b.pricing7NightsFeb22Mar1.lowestQueenKingUsdInclTax - a.pricing7NightsFeb22Mar1.lowestQueenKingUsdInclTax
        );
      } else {
        filtered = [...filtered].sort((a, b) => {
          if (a.city !== b.city) return a.city === "Shanghai" ? -1 : 1;
          return a.cityRank - b.cityRank;
        });
      }

      if (tableBody) {
        tableBody.innerHTML = filtered
          .map((h) => {
            const p = h.pricing7NightsFeb22Mar1;
            const r = h.michelinReachability;
            return `
              <tr>
                <td class="num">${esc(h.city)} #${esc(h.cityRank)}</td>
                <td>
                  <strong>${esc(h.name)}</strong>
                  <div class="text-muted text-sm">${esc(h.district)} · ${esc(h.tier)}</div>
                </td>
                <td>
                  <strong>${esc(h.verifiedRoom.roomName)}</strong>
                  <div class="text-sm text-muted">${esc(h.verifiedRoom.sizeSqm)} m² · Private Bath ✓</div>
                </td>
                <td>
                  <strong>${esc(r.auditedWithin60Min)}/${esc(r.auditedTotalInCity)} ≤60 min</strong>
                  <div class="text-sm text-muted">${esc(r.auditedWithin30Min)} within 30 min · Max ${esc(r.maxDoorToDoorMin)} min</div>
                </td>
                <td class="num">
                  <strong>US$${esc(p.lowestQueenKingUsdInclTax.toLocaleString())}</strong>
                  ${p.officialDirectSynxisCnyPerNightExclTax ? `<div class="text-sm text-muted">Direct: CN¥${esc(p.officialDirectSynxisCnyPerNightExclTax.toLocaleString())}/nt excl. tax</div>` : ""}
                </td>
                <td>
                  <a href="${esc(safeUrl(p.liveQuoteUrl))}" target="_blank" rel="noopener noreferrer">Live Quote ↗</a><br/>
                  <a href="${esc(safeUrl(p.officialHotelUrl))}" target="_blank" rel="noopener noreferrer" class="text-sm">Official Specs ↗</a>
                </td>
              </tr>
            `;
          })
          .join("");
      }

      if (cardsEl) {
        cardsEl.innerHTML = filtered
          .map((h) => {
            const p = h.pricing7NightsFeb22Mar1;
            const r = h.michelinReachability;
            const m = h.nearestMetro;
            return `
              <article class="card">
                <div class="card-meta-row">
                  <span class="badge badge-star">${esc(h.city)} Rank #${esc(h.cityRank)}</span>
                  <span class="badge badge-verified">${esc(r.auditedWithin60Min)}/${esc(r.auditedTotalInCity)} Audited MICHELIN ≤60 min</span>
                  <span class="badge badge-city">Private Bath ✓ · ${esc(h.verifiedRoom.sizeSqm)} m²</span>
                </div>
                <div>
                  <h3 class="card-title">${esc(h.name)}</h3>
                  <p class="card-subtitle">${esc(h.chineseName)} · ${esc(h.tier)}</p>
                </div>
                <div class="callout callout-emerald" style="padding:12px 14px;">
                  <div class="callout-title">
                    7-Night Total (Feb 22 – Mar 1, 2027, 2 Adults, Incl. Taxes &amp; Fees):
                    <span class="num" style="color:var(--emerald);font-size:1.08rem;">US$${esc(p.lowestQueenKingUsdInclTax.toLocaleString())}</span>
                  </div>
                  <p>
                    ${esc(p.cancellationPolicy)} · With 2 daily breakfasts: <strong>US$${esc(p.breakfast2AdultsUsdInclTax.toLocaleString())}</strong>
                    ${p.officialDirectSynxisNote ? `<br/><strong>Official Direct SynXis:</strong> ${esc(p.officialDirectSynxisNote)}` : ""}
                  </p>
                </div>
                <div class="spec-list">
                  <div class="spec-item">
                    <span class="spec-label">Verified Bed &amp; Private Bathroom</span>
                    <span class="spec-val"><strong>${esc(h.verifiedRoom.roomName)}</strong> — ${esc(h.verifiedRoom.bedSpec)}. ${esc(h.verifiedRoom.bathroomDetails)}.</span>
                  </div>
                  <div class="spec-item">
                    <span class="spec-label">Nearest Metro Hub</span>
                    <span class="spec-val"><strong>${esc(m.station)}</strong> (${esc(m.lines.join(", "))}) — ${esc(m.walkMeters)}m / ~${esc(m.walkMinutes)} min walk</span>
                  </div>
                  <div class="spec-item">
                    <span class="spec-label">Door-to-Door MICHELIN Transit Times (${esc(r.auditedWithin30Min)} within 30 min)</span>
                    <ul style="margin:4px 0 0;padding-left:18px;font-size:0.84rem;color:var(--text-secondary);">
                      ${r.keyTransitExamples.map((ex) => `<li>${esc(ex)}</li>`).join("")}
                    </ul>
                  </div>
                  <div class="spec-item">
                    <span class="spec-label">Verified Amenities</span>
                    <ul class="pill-list mt-12" style="margin-top:4px;">
                      ${h.amenities.map((am) => `<li class="pill">${esc(am)}</li>`).join("")}
                    </ul>
                  </div>
                </div>
                <div class="btn-row">
                  <a class="btn btn-primary" href="${esc(safeUrl(p.liveQuoteUrl))}" target="_blank" rel="noopener noreferrer">Verify Live Feb 22–Mar 1 Rate ↗</a>
                  ${p.officialDirectBookingUrl ? `<a class="btn btn-secondary" href="${esc(safeUrl(p.officialDirectBookingUrl))}" target="_blank" rel="noopener noreferrer">Official Direct SynXis ↗</a>` : ""}
                  <a class="btn btn-secondary" href="${esc(safeUrl(p.officialHotelUrl))}" target="_blank" rel="noopener noreferrer">Official Hotel Specs ↗</a>
                  <button type="button" class="btn btn-ghost btn-driver" data-en="${esc(h.name)}" data-zh="${esc(h.chineseName)}" data-addr="${esc(h.address)}" data-metro="${esc(m.station)} (${esc(m.lines.join(", "))})">Show Driver (中文)</button>
                </div>
              </article>
            `;
          })
          .join("");
      }
    }

    document.querySelectorAll("[data-hotel-city]").forEach((btn) => {
      btn.addEventListener("click", () => {
        document.querySelectorAll("[data-hotel-city]").forEach((b) => b.classList.remove("active"));
        btn.classList.add("active");
        state.city = btn.dataset.hotelCity;
        apply();
      });
    });

    if (sortSelect) {
      sortSelect.addEventListener("change", (e) => {
        state.sort = e.target.value;
        apply();
      });
    }

    apply();
  }

  /* ========================================================================
     PAGE 4: ACTIVITIES & LANDMARKS (pages/activities.html)
     ======================================================================== */
  async function renderActivities() {
    const data = await fetchJson("data/activities.json");
    const acts = data.activities;

    let state = { city: "ALL", filter: "ALL", query: "" };
    const grid = document.getElementById("activities-grid");
    const countEl = document.getElementById("activities-count");
    const searchInput = document.getElementById("act-search");

    function isOpenMonday(a) {
      const txt = `${a.daysOpen} ${a.closureExceptions}`.toLowerCase();
      if (txt.includes("open daily") || txt.includes("open mondays") || txt.includes("monday – sunday") || txt.includes("wed–mon") || txt.includes("all day")) {
        return !txt.includes("closed mondays") || txt.includes("at least one branch is open every day");
      }
      return false;
    }

    function apply() {
      const q = state.query.trim().toLowerCase();
      const filtered = acts.filter((a) => {
        if (state.city !== "ALL" && a.city !== state.city) return false;
        if (state.filter === "MONDAY" && !isOpenMonday(a)) return false;
        if (state.filter === "FREE" && a.priceForTwoCny !== 0) return false;
        if (q) {
          const hay = `${a.name} ${a.chineseName} ${a.city} ${a.category} ${a.address} ${a.winterSuitability}`.toLowerCase();
          if (!hay.includes(q)) return false;
        }
        return true;
      });

      const shSum = filtered.filter((a) => a.city === "Shanghai").reduce((s, a) => s + (a.priceForTwoCny || 0), 0);
      const bjSum = filtered.filter((a) => a.city === "Beijing").reduce((s, a) => s + (a.priceForTwoCny || 0), 0);
      if (countEl) {
        countEl.textContent = `Showing ${filtered.length} of ${acts.length} activities · Filtered admission totals (2 adults, off-season): Shanghai CN¥${shSum} · Beijing CN¥${bjSum}`;
      }

      if (!filtered.length) {
        grid.innerHTML = `<div class="loading-box">No activities match the current filters.</div>`;
        return;
      }

      grid.innerHTML = filtered
        .map((a) => {
          const openMon = isOpenMonday(a);
          const over60 = a.maxTransitMin > 60;
          return `
            <article class="card">
              <div class="card-meta-row">
                <span class="badge badge-city">${esc(a.city)}</span>
                <span class="badge badge-low">${esc(a.category)}</span>
                ${openMon ? '<span class="badge badge-verified">Open Mondays ✓</span>' : '<span class="badge badge-high">Closed Mondays</span>'}
                ${over60 ? '<span class="badge badge-review">~60–70 min door-to-door (27 min HSR)</span>' : `<span class="badge badge-verified">≤${esc(a.maxTransitMin)} min transit</span>`}
              </div>
              <div>
                <h3 class="card-title">${esc(a.name)}</h3>
                <p class="card-subtitle">${esc(a.chineseName)}</p>
              </div>
              <div class="spec-list">
                <div class="spec-item">
                  <span class="spec-label">Verified Official Admission (2 Adults, Feb–Mar Off-Season)</span>
                  <span class="spec-val">
                    <strong class="num" style="font-size:1.02rem;color:var(--crimson);">${a.priceForTwoCny === 0 ? "FREE (CN¥0)" : `CN¥${esc(a.priceForTwoCny)}`}</strong>
                    — ${esc(a.priceBreakdown)}
                  </span>
                </div>
                <div class="spec-item">
                  <span class="spec-label">Opening Hours &amp; Closure Exceptions</span>
                  <span class="spec-val"><strong>${esc(a.daysOpen)}</strong> · ${esc(a.hours)}<br/><span class="text-muted">${esc(a.closureExceptions)}</span></span>
                </div>
                <div class="spec-item">
                  <span class="spec-label">Transit from Recommended Hotel Clusters</span>
                  <span class="spec-val">${esc(a.transitFromHotelCluster)}</span>
                </div>
                <div class="spec-item">
                  <span class="spec-label">Passport &amp; Booking Requirement</span>
                  <span class="spec-val">${esc(a.bookingRequirement)}</span>
                </div>
                <div class="spec-item">
                  <span class="spec-label">Late-Feb / March Weather Fit</span>
                  <span class="spec-val">${esc(a.winterSuitability)}</span>
                </div>
              </div>
              <div class="btn-row">
                <a class="btn btn-primary" href="${esc(safeUrl(a.officialUrl))}" target="_blank" rel="noopener noreferrer">Official Info ↗</a>
                ${a.officialGovReferenceUrl && a.officialGovReferenceUrl !== a.officialUrl ? `<a class="btn btn-secondary" href="${esc(safeUrl(a.officialGovReferenceUrl))}" target="_blank" rel="noopener noreferrer">Gov Reference ↗</a>` : ""}
                <button type="button" class="btn btn-ghost btn-driver" data-en="${esc(a.name)}" data-zh="${esc(a.chineseName)}" data-addr="${esc(a.address)}" data-metro="">Show Driver (中文)</button>
              </div>
              <div class="btn-row" style="border-top:1px solid var(--border-light);padding-top:10px;margin-top:4px;">
                ${renderSocialLinks(a.socialLinks)}
              </div>
              ${
                Array.isArray(a.unverifiedFields) && a.unverifiedFields.length > 0
                  ? `<div class="text-sm text-muted">Audit note: ${esc(a.unverifiedFields.join(" | "))}</div>`
                  : ""
              }
            </article>
          `;
        })
        .join("");
    }

    document.querySelectorAll("[data-act-city]").forEach((btn) => {
      btn.addEventListener("click", () => {
        document.querySelectorAll("[data-act-city]").forEach((b) => b.classList.remove("active"));
        btn.classList.add("active");
        state.city = btn.dataset.actCity;
        apply();
      });
    });

    document.querySelectorAll("[data-act-filter]").forEach((btn) => {
      btn.addEventListener("click", () => {
        document.querySelectorAll("[data-act-filter]").forEach((b) => b.classList.remove("active"));
        btn.classList.add("active");
        state.filter = btn.dataset.actFilter;
        apply();
      });
    });

    if (searchInput) {
      searchInput.addEventListener("input", (e) => {
        state.query = e.target.value;
        apply();
      });
    }

    apply();
  }

  /* ========================================================================
     PAGE 5: PLANNING, DECISION QUESTIONS & IMPROVEMENTS (pages/planning.html)
     ======================================================================== */
  async function renderPlanning() {
    const gov = await fetchJson("data/governance.json");

    const qEl = document.getElementById("decision-questions");
    if (qEl) {
      qEl.innerHTML = gov.missingInfoAndDiscovery.decisionQuestions
        .map((q) => {
          const sevCls = q.priority === "Critical" ? "badge-high" : q.priority === "High" ? "badge-medium" : "badge-low";
          return `
            <article class="card">
              <div class="card-meta-row">
                <span class="badge ${sevCls}">${esc(q.priority)} Priority</span>
                <span class="badge badge-city">${esc(q.id)}</span>
              </div>
              <h3 class="card-title">${esc(q.topic)}</h3>
              <p style="margin:0;font-weight:600;color:var(--text-primary);">${esc(q.question)}</p>
              <div class="spec-list">
                <div class="spec-item">
                  <span class="spec-label">Why It Changes Your Plan</span>
                  <span class="spec-val">${esc(q.impact)}</span>
                </div>
                <div class="spec-item">
                  <span class="spec-label">Current Planning Assumption</span>
                  <span class="spec-val">${esc(q.defaultAssumed)}</span>
                </div>
              </div>
            </article>
          `;
        })
        .join("");
    }

    const planEl = document.getElementById("discovery-plan");
    if (planEl) {
      planEl.innerHTML = gov.missingInfoAndDiscovery.discoveryPlan
        .map(
          (p) => `
          <article class="card">
            <div class="card-meta-row">
              <span class="badge badge-star">${esc(p.timeline)}</span>
            </div>
            <h3 class="card-title">${esc(p.phase)}</h3>
            <ul style="margin:4px 0 0;padding-left:18px;font-size:0.9rem;color:var(--text-secondary);">
              ${p.actions.map((act) => `<li style="margin-bottom:6px;">${esc(act)}</li>`).join("")}
            </ul>
          </article>
        `
        )
        .join("");
    }

    const impEl = document.getElementById("site-improvements");
    if (impEl) {
      impEl.innerHTML = gov.siteImprovements
        .map(
          (imp) => `
          <article class="card">
            <div class="card-meta-row">
              <span class="badge badge-city">${esc(imp.id)}</span>
              <span class="badge badge-verified">${esc(imp.priority)}</span>
            </div>
            <h3 class="card-title">${esc(imp.title)}</h3>
            <p style="margin:0;color:var(--text-secondary);font-size:0.9rem;">${esc(imp.description)}</p>
          </article>
        `
        )
        .join("");
    }
  }

  /* ========================================================================
     PAGE 6: FLAGGED FOR REVIEW AUDIT REGISTER (pages/review.html)
     ======================================================================== */
  async function renderReview() {
    const [gov, rest, act] = await Promise.all([
      fetchJson("data/governance.json"),
      fetchJson("data/restaurants.json"),
      fetchJson("data/activities.json")
    ]);

    let severityFilter = "ALL";
    const flagsEl = document.getElementById("flagged-list");

    function renderFlags() {
      const items = gov.flaggedForReview.filter((f) => severityFilter === "ALL" || f.severity === severityFilter);
      flagsEl.innerHTML = items
        .map((f) => {
          const cls = f.severity === "High" ? "badge-high" : f.severity === "Medium" ? "badge-medium" : "badge-low";
          return `
            <article class="card">
              <div class="card-meta-row">
                <span class="badge ${cls}">${esc(f.severity)} Severity</span>
                <span class="badge badge-city">${esc(f.id)} · ${esc(f.category)}</span>
                <span class="badge badge-review">${esc(f.status)}</span>
              </div>
              <h3 class="card-title">${esc(f.item)}</h3>
              <p style="margin:0;color:var(--text-secondary);font-size:0.9rem;">${esc(f.details)}</p>
            </article>
          `;
        })
        .join("");
    }

    document.querySelectorAll("[data-flag-sev]").forEach((btn) => {
      btn.addEventListener("click", () => {
        document.querySelectorAll("[data-flag-sev]").forEach((b) => b.classList.remove("active"));
        btn.classList.add("active");
        severityFilter = btn.dataset.flagSev;
        renderFlags();
      });
    });

    renderFlags();

    // Auto-generated live granular audit table of every unverified restaurant & activity field
    const granularTbody = document.getElementById("granular-audit-tbody");
    if (granularTbody) {
      const rows = [];
      rest.restaurants.forEach((r) => {
        if (Array.isArray(r.unverifiedFields) && r.unverifiedFields.length > 0) {
          rows.push({
            dataset: "MICHELIN Dining",
            city: r.city,
            item: `${r.name} (${r.distinctionLabel})`,
            fields: r.unverifiedFields.join(", "),
            url: r.michelinUrl
          });
        }
      });
      act.activities.forEach((a) => {
        if (Array.isArray(a.unverifiedFields) && a.unverifiedFields.length > 0) {
          rows.push({
            dataset: "Activities",
            city: a.city,
            item: a.name,
            fields: a.unverifiedFields.join(" | "),
            url: a.officialUrl
          });
        }
      });

      const countSpan = document.getElementById("granular-count");
      if (countSpan) countSpan.textContent = `${rows.length} individual records with blank/flagged fields`;

      granularTbody.innerHTML = rows
        .map(
          (row) => `
          <tr>
            <td><span class="badge badge-city">${esc(row.dataset)}</span></td>
            <td>${esc(row.city)}</td>
            <td><strong>${esc(row.item)}</strong></td>
            <td><span class="text-sm">${esc(row.fields)}</span></td>
            <td><a href="${esc(safeUrl(row.url))}" target="_blank" rel="noopener noreferrer">Official Link ↗</a></td>
          </tr>
        `
        )
        .join("");
    }
  }

  /* ---------- Bootstrap ---------- */
  document.addEventListener("DOMContentLoaded", async () => {
    const page = document.body.dataset.page || "home";
    initShell(page);

    try {
      if (page === "home") await renderHome();
      else if (page === "restaurants") await renderRestaurants();
      else if (page === "hotels") await renderHotels();
      else if (page === "activities") await renderActivities();
      else if (page === "planning") await renderPlanning();
      else if (page === "review") await renderReview();
    } catch (err) {
      console.error(err);
      const main = document.querySelector("main");
      if (main) {
        const alert = document.createElement("div");
        alert.className = "container section";
        alert.innerHTML = `<div class="callout callout-crimson"><h3 class="callout-title">Data Load Notice</h3><p>Could not load JSON dataset (${esc(err.message)}). If opening locally via <code>file://</code>, serve via a local HTTP server or GitHub Pages.</p></div>`;
        main.prepend(alert);
      }
    }
  });
})();
