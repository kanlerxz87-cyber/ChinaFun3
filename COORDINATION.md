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


## Session arena-8725551a — parallel handoff and non-overlapping addition

- Initial claim 102fd5b was made when this branch and origin/main had only the original README. Research checkpoint 6a50fca and dashboard f6397e9 were committed/pushed on arena/8725551a-chinafun3. No claims were visible at initial inspection.
- Before publication, fetched main and discovered concurrent merged work from sessions 8205b531 and 3c3c3c5e at fd670ae. Stopped root integration immediately. Began merge of origin/main; add/add conflicts in shared root pages and coordination, plus README content conflict. No automatic overwrite and no work discarded.
- Resolution: keep the other sessions' root HTML, data/, docs/, assets/css/ and assets/js/ byte-for-byte as origin/main. Preserve this session's full dashboard under **considered/**, its README and original log under considered/README.md and considered/COORDINATION-session.md. Preserve both original boards and logs above; append this handoff. Root README receives only a new link/summary section. Unique research/, scripts/, tests/, package*.json and .github/workflows/verify.yml belong to this session. Generator and tests are scoped to considered/ only.
- This session does not claim or modify the other owners' root navigation or data. Integration request: root-site owner may add an optional link to considered/index.html after review. No root-nav change is needed to publish a directly addressable subsite.
- Scope/state: bounded official-source research DONE; standalone dashboard DONE; unresolved travel decisions NEEDS REVIEW on considered/review.html; final non-overlapping integration and Pages publish DONE (PR #5, deployment confirmed below). Root and docs claims above remain intact. Existing dashboards' factual claims are preserved, not automatically endorsed or reverified by this session.
- Evidence: research/data.json (primary source URLs and observed fields, 2026-11-25), research/README.md (irregularities). Eight offline tests and 27 real-browser page/viewport checks passed before relocation; rerunning at considered/ before publication. No final seven-night hotel totals, no verified cheapest period, no measured one-hour transit ranking. Never inferred these missing values.
- Pages settings PUT returned HTTP 403 (integration lacks settings-write permission). Existing source is main /. Plan: publish additional considered/ path through explicit PR merge into existing Pages source; no direct push or checkout of main.
- Relocation verification complete: eight offline tests and all 27 browser page/viewport checks passed at /considered/. Root overlapping HTML compares byte-for-byte equal to origin/main. Full repository HTML relative-file link scan (excluding dependencies/cache) found no missing relative file references; this is not a factual re-verification of retained root/docs content. Independent dashboard review now also flags the retained dashboards as not independently reverified (R13; China-wide scope R14).
- Push synchronization note: plain `git pull --rebase` after the integration merge attempted to flatten the other sessions' merge ancestry and raised a COORDINATION add/add conflict. Stopped and aborted that rebase; no resolution/discard applied. `git pull --rebase=merges origin arena/8725551a-chinafun3` then completed successfully, preserving merge topology and all boards. Use merge-preserving rebase for subsequent pushes on this integration branch.
- CI caught one relocation oversight: the JavaScript syntax step still pointed to deleted assets/app.js. Corrected workflow, npm test and subsite README to considered/assets/app.js; offline content tests were already passing. No factual source or prior-owner file changed.

- Completion: PR #5 merged 2026-11-25T13:27:49Z, main merge commit 62a8a24da14acbb573269ba84a1efbc877255722. Verification check passed. Pages run 45623839028 completed successfully (build + deploy + report); Pages API reports built with no error for that commit. Public fetch of https://kanlerxz87-cyber.github.io/ChinaFun3/considered/ returned the new executive dashboard successfully. No reservations or payments made. Research gaps remain needs review; publication is complete.
