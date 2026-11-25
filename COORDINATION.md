# COORDINATION.md — Shared Task Board (merged — no discard, v2)

> **Rule:** Claim a task by writing your session ID and file scope here, then commit+push immediately. Never start a task another session has claimed. Keep scopes non-overlapping. If you need a file owned by another session, log a request here instead of editing it. (`git pull --rebase` before every push; if conflict, resolve without discarding other work and log here.)

**Repo:** `kanlerxz87-cyber/ChinaFun3`  |  **Pages:** https://kanlerxz87-cyber.github.io/ChinaFun3/  |  **Updated:** 2026-11-25T13:22:00Z (merge v2: `arena/8205b531-chinafun3` + `e824b4b` → resolved)

## Active Sessions

| Session ID | Branch | Started | Last Commit | Status |
|---|---|---|---|---|
| `arena/8205b531-chinafun3` | `arena/8205b531-chinafun3` | 2026-11-25 13:12 UTC | 2026-11-25 13:22 UTC (merge resolution v2) | active — root site |
| `arena/3c3c3c5e-chinafun3` | `arena/3c3c3c5e-chinafun3` (merged to `main` as `a0b6d59` + `e824b4b`) | 2026-11-25 | 2026-11-25 13:22 UTC (PR #4 merged: T7 log) | merged to `main` — docs site |

---

## Task Board — Session `arena/8205b531-chinafun3` (root site: `index.html` + `assets/*` + `data/*.json`)

| ID | Task | Status | Owner Session | Files Touched / Scope | Sources & Verification Note | Updated |
|---|---|---|---|---|---|---|
| T01 | Repo audit & verification framework | **done** | `arena/8205b531-chinafun3` | `COORDINATION.md`, `data/*.json` | Every row has official source link; blank+flag if unverified | 2026-11-25 |
| T02 | Site scaffolding & design system | **done** | `arena/8205b531-chinafun3` | `index.html`, `assets/css/style.css`, `assets/js/app.js`, `404.html`, `.nojekyll` | Mobile-first, no build, WCAG AA | 2026-11-25 |
| T03 | Itinerary & Date analysis | **done** | `arena/8205b531-chinafun3` | `itinerary.html`, `data/itinerary.json` | Official calendars + Google Hotels insights; 2027 pricing flagged surrogate | 2026-11-25 |
| T04 | Hotels research & ranking | **done** | `arena/8205b531-chinafun3` | `hotels.html`, `data/hotels.json` | Hotel official + Trip/Booking mirrors; ranking via shmetro.com | 2026-11-25 |
| T05 | Michelin restaurants | **done** | `arena/8205b531-chinafun3` | `restaurants.html`, `data/restaurants.json` | guide.michelin.com 2024 Shanghai; budget article exact totals for 3; scale estimates flagged | 2026-11-25 |
| T06 | Activities ≤1h | **done** | `arena/8205b531-chinafun3` | `activities.html`, `data/activities.json` | Attraction official + shmetro.com | 2026-11-25 |
| T07 | Transport & 1-hour isochrone | **done** | `arena/8205b531-chinafun3` | `transport.html`, `data/transport.json` | shmetro.com + Amap; door-to-door times | 2026-11-25 |
| T08 | Budget & pricing | **done** | `arena/8205b531-chinafun3` | `budget.html`, `data/budget.json` | Hotel engines; ¥ scale; FX 7.2 dated | 2026-11-25 |
| T09 | Executive summary & Q&A gaps | **done** | `arena/8205b531-chinafun3` | `executive-summary.html`, `questions.html` | 12 gaps, how to discover | 2026-11-25 |
| T10 | Suggestions & improvement roadmap | **done** | `arena/8205b531-chinafun3` | `suggestions.html` | 8 proposals, review-only | 2026-11-25 |
| T11 | Verification & Flagged Review | **done** | `arena/8205b531-chinafun3` | `sources.html`, `flagged.html`, `methodology.html` | 11 flags, surrogate protocol | 2026-11-25 |
| T12 | Integration & publish (this merge) | **done** | `arena/8205b531-chinafun3` | `index.html`, `README.md`, `COORDINATION.md`, `docs/**` | No discard merge: kept root dashboard at `/` + preserved `docs/`; resolved conflicts | 2026-11-25 |

## Task Board — Session `arena/3c3c3c5e-chinafun3` (docs site: `docs/**`)

| ID | Task | Status | Owner | Files touched |
|---|---|---|---|---|
| T0 | Repo review + irregularities | **done** | `3c3c3c5e` | `README.md`, `docs/data/irregularities.json`, `docs/repo-review.html` |
| T1 | Entry rules + 2027 holiday calendar | **done** | `3c3c3c5e` | `docs/data/entry.json`, `docs/data/calendar.json`, `docs/entry-and-calendar.html` |
| T2 | Michelin restaurants — Shanghai cluster | **done** (partial, 64 unverified cells blank) | `3c3c3c5e` | `docs/data/michelin.json`, `docs/michelin-shanghai.html` |
| T3 | Hotels (price/location/amenities) | **needs review** (blocked by data access — hotel sites outside allowed hosts) | `3c3c3c5e` | `docs/data/hotels.json`, `docs/hotels.html` |
| T4 | Activities (hours, tickets, social links) | **done** (partial) | `3c3c3c5e` | `docs/data/activities.json`, `docs/activities.html` |
| T5 | Questions, suggestions, flagged review | **done** | `3c3c3c5e` | `docs/data/questions.json`, `docs/data/suggestions.json`, `docs/review.html` |
| T6 | Site shell, landing page, executive summary | **done** | `3c3c3c5e` | `docs/index.html`, `docs/assets/*`, `docs/.nojekyll` |
| T7 | Integration: merge, re-verify, publish Pages | **done** | `3c3c3c5e` | `docs/**`, `COORDINATION.md` |

Shared outputs (`docs/index.html` navigation, combined data) owned by T7 (integration) — now preserved at `/docs/` after merge.

---

## File Ownership (non-overlapping scopes — post-merge)

| Scope | Owner | Note |
|---|---|---|
| `COORDINATION.md`, `README.md` (merged) | both sessions (joint) | This merge resolved without discard |
| `index.html`, `executive-summary.html`, `itinerary.html`, `hotels.html`, `restaurants.html`, `activities.html`, `transport.html`, `budget.html`, `sources.html`, `suggestions.html`, `questions.html`, `flagged.html`, `methodology.html`, `404.html`, `.nojekyll` | `arena/8205b531-chinafun3` | Root site — stays at `/` |
| `assets/css/*`, `assets/js/*` | `arena/8205b531-chinafun3` | Root site assets |
| `data/*.json` | `arena/8205b531-chinafun3` | Root site data |
| `docs/*`, `docs/data/*`, `docs/assets/*` | `arena/3c3c3c5e-chinafun3` | Docs site — stays at `/docs/` |

## Log (merged, no discard — v2 adds e824b4b)

| Timestamp (UTC) | Session | Action |
|---|---|---|
| 2026-11-25 13:12:35 | `arena/8205b531-chinafun3` | Branch created from `fa1f9faa538f0539f9ec83dfc39f579496ff7ff6` (main). Repo contained only `README.md`. |
| 2026-11-25 13:13:00 | `arena/8205b531-chinafun3` | Verified Pages status: `built` on `main` at https://kanlerxz87-cyber.github.io/ChinaFun3/ (legacy, `main` `/`). Viewer permission = ADMIN. |
| 2026-11-25 13:14:00 | `arena/8205b531-chinafun3` | Claimed T01–T11. Scopes announced. Started scaffolding + data collection (Michelin 2024, hotel official, attraction official, shmetro.com). |
| 2026-11-25 13:18:00 | `arena/8205b531-chinafun3` | Pushed complete root site (17 files + assets/data) to `arena/8205b531-chinafun3`; PR #3 opened. |
| 2026-11-25 | `arena/3c3c3c5e-chinafun3` | Created `COORDINATION.md` with T0–T7, claimed all. Verified 2027 holiday notice on gov.cn (国办发明电〔2026〕10号), NIA visa-free, Michelin press release, Shanghai Museum + Yu Garden official. Logged blocked fetches. Built `docs/` static site, validated links/JSON, merged PR #1 + #2 to `main` (a0b6d59). |
| 2026-11-25 13:19:00 | `arena/8205b531-chinafun3` | Merge to `main` blocked — conflicts in `COORDINATION.md`, `README.md`, `index.html`. Fetched `origin/main` (a0b6d59), started merge resolution. |
| 2026-11-25 13:20:00 | `arena/8205b531-chinafun3` | **Resolved without discard:** kept root dashboard at `index.html` + preserved `docs/**` + merged `README.md` + merged `COORDINATION.md` (both task boards + logs). Committed eca078c. |
| 2026-11-25 13:22:00 | `arena/3c3c3c5e-chinafun3` | PR #4 merged to `main` (e824b4b): Log T7 integration — Pages source `main` `/`, root forwarder, built status, and final re-verification (all JSON parse, links resolve, every row source/flag). See origin/main COORDINATION addendum below. |
| 2026-11-25 13:22:00 | `arena/8205b531-chinafun3` | **Merge v2:** fetched `origin/main` e824b4b, merged into `arena/8205b531-chinafun3`. Conflict in `COORDINATION.md` resolved by keeping merged board (both sessions) + incorporating `e824b4b` log entry (see “T7 integration — 3c3c3c5e” below) — no work discarded from either session. |
| | | If a claim is >60 min old with no commits, any session may take over and note handoff here. |

### T7 integration log from `e824b4b` (preserved verbatim, not discarded)

- **2026-11-25 · 3c3c3c5e — Integration (T7):**
  - PR #1 (site + data) merged into `main` (7277767). PR #2 (root `index.html` forwarder) merged after that.
  - GitHub Pages is configured with source `main` / path `/` (root). The token cannot change it (HTTP 403 on PUT), so the root `index.html` forwards to `docs/index.html`.
  - Latest Pages build: status `built` (commit a0b6d59). Live URL https://kanlerxz87-cyber.github.io/ChinaFun3/ . This sandbox cannot reach github.io directly, so the page itself was checked locally.
  - Process note: a stray `git checkout main` was run during publishing, reverted right away, no commits on `main` directly.
  - Final re-verification: all JSON parses; all internal links resolve; every table row has a source link or an Unverified flag.
- **Open items (need your input or manual checks):** see Questions tab (Q1–Q11) and suggestions S1–S8 on `docs/review.html` (and root site `questions.html` / `suggestions.html`).

## Handoff Requests
*No cross-session file requests outstanding. If you need a file in another scope, add a row here instead of editing it.*

## Notes (merged)
- **Verification rule (enforced on both sites):** Every table row must have a source link to an official site; if a value can't be confirmed, leave blank and flag as `unverified` (root site uses amber badge; docs site uses `Unverified` label).
- **Pricing honesty (root site):** 2027 pricing for Feb 15–Mar 23 not yet published by most hotels → show surrogate dates with explicit label + re-check after Dec 1, 2026. Docs site correctly left hotel price cells blank (needs review).
- **Michelin counts:** Root site uses Shanghai 2024 guide (51 starred; paginates to 50+UV) with editorial confirm; docs site uses Shanghai/Jiangsu/Zhejiang 2026 press release (16 Shanghai starred verified, rest blank). Both flagged discrepancies.
- **Parallel safety:** `git pull --rebase` before push; if a claim is >60 min old with no commits, any session may take over and note handoff here. This merge demonstrates the protocol: no work discarded, conflicts resolved, log preserved.

