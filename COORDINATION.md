# ChinaFun3 — Shared Task Coordination Board

> **Purpose:** Shared coordination log for verifying travel data, auditing sources, and building the ChinaFun3 Trip Planning GitHub Pages dashboard.
> **Branch Policy Note:** This Arena session is bound to branch `arena/256b850d-chinafun3` (branched from `main` at `fa1f9fa`). All commits and pushes from this session target `arena/256b850d-chinafun3`.
> **Verification Rule:** No cell or claim may be marked `verified` without direct confirmation from an official, trusted source (linked). Any unconfirmable field is left blank in tables and logged on the **Flagged for Review** page (`needs review` status does not block other work).

---

## Active Sessions

| Session ID | Branch | Started (UTC) | Scope | Status |
|---|---|---|---|---|
| `session-256b850d` | `arena/256b850d-chinafun3` | 2026-11-25 | Full initial build, verification, and integration (no other active sessions found in repo) | Active |

---

## Task Board

| Task ID | Task Description | Status | Owner Session | File Scope | Last Updated (UTC) |
|---|---|---|---|---|---|
| `T-00` | Repo audit & `COORDINATION.md` initialization | `done` | `session-256b850d` | `COORDINATION.md` | 2026-11-25 |
| `T-01` | Verify 2027 China travel calendar (Spring Festival / Lantern Festival, official public holidays, weather, booking windows) & city-level Michelin Guide China cluster counts | `in progress` | `session-256b850d` | `data/calendar-and-clusters.json`, `docs/research-notes.md` | 2026-11-25 |
| `T-02` | Research & verify Michelin-starred and Michelin Guide-listed restaurants (Shanghai & Beijing clusters), total pricing for 2 adults, hours/exceptions, official links, and social media links (YouTube/TikTok/Instagram) | `in progress` | `session-256b850d` | `data/restaurants.json` | 2026-11-25 |
| `T-03` | Research & verify hotels (private bath, queen+ bed, amenities, transit ≤1 hr to Michelin clusters), rank by Michelin reachability, verify 7-night pricing for Feb–Mar 2027 dates & optimal booking window | `unclaimed` | — | `data/hotels.json` | 2026-11-25 |
| `T-04` | Research & verify activities & attractions within ≤1 hr transit of hotel clusters, official hours/exceptions, 2-adult admission prices, official links, and social media links | `unclaimed` | — | `data/activities.json` | 2026-11-25 |
| `T-05` | Compile Executive Summary, Missing Info / Decision Questions & Discovery Plan, Site Improvement Suggestions, and Flagged for Review audit register | `unclaimed` | — | `data/governance.json` | 2026-11-25 |
| `T-06` | Build mobile-friendly GitHub Pages dashboard (landing page + category subpages, searchable/filterable tables, zero broken links, line-by-line verification pass) | `unclaimed` | — | `index.html`, `pages/*.html`, `assets/*`, `.nojekyll` | 2026-11-25 |
| `T-07` | Final integration audit, link & schema validation, live preview verification, and GitHub Pages publication | `unclaimed` | — | `README.md`, `COORDINATION.md`, site root | 2026-11-25 |

---

## Repo Audit Notes (`T-00`)

- **Initial Repo Inspection (2026-11-25):**
  - Only file present on `main` (`fa1f9fa`): `README.md` (`# ChinaFun3`).
  - No other branches, worktrees, or pull requests exist on `origin`.
  - GitHub Pages is currently configured in legacy mode serving `/` from `main` at `https://kanlerxz87-cyber.github.io/ChinaFun3/`.
- **Initial Prompt Irregularities Identified for Flagging:**
  1. **Date Duration Conflict:** Prompt states trip length should be *1–2 weeks* (and requests *7-night* hotel stay totals), while also stating *"Preferred vacation time is February 15 2027 to February 18 2027"* (which is only 3 nights / 4 days). Flagged for user clarification.
  2. **Destination City/Region Unspecified:** Prompt specifies *"China"* without specifying Mainland China vs. Hong Kong/Macau SARs, or single-city vs. multi-city itinerary.
  3. **2027 Lunar New Year / Spring Festival Overlap:** Must verify exact 2027 Chinese New Year & Lantern Festival dates relative to Feb 15 – Mar 23, 2027.

---

## Verification & Source Log

*(Populated as each task completes.)*

---

## Change Requests Across Scopes

*(None yet.)*
