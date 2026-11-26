# COORDINATION.md — Shared Task Board (merged — no discard, v2)

> **Rule:** Claim a task by writing your session ID and file scope here, then commit+push immediately. Never start a task another session has claimed. Keep scopes non-overlapping. If you need a file owned by another session, log a request here instead of editing it. (`git pull --rebase` before every push; if conflict, resolve without discarding other work and log here.)

**Repo:** `kanlerxz87-cyber/ChinaFun3`  |  **Pages:** https://kanlerxz87-cyber.github.io/ChinaFun3/  |  **Updated:** 2026-11-25T13:22:00Z (merge v2: `arena/8205b531-chinafun3` + `e824b4b` → resolved)

## Active Sessions

| Session ID | Branch | Started | Last Commit | Status |
|---|---|---|---|---|
| `arena/8205b531-chinafun3` | `arena/8205b531-chinafun3` | 2026-11-25 13:12 UTC | 2026-11-25 13:22 UTC (merge resolution v2) | active — root site |
| `arena/3c3c3c5e-chinafun3` | `arena/3c3c3c5e-chinafun3` (merged to `main` as `a0b6d59` + `e824b4b`) | 2026-11-25 | 2026-11-25 13:22 UTC (PR #4 merged: T7 log) | merged to `main` — docs site |
| `arena/b27f0613-chinafun3` | `arena/b27f0613-chinafun3` | 2026-11-25 | 2026-11-25 (claim commit) | active — `verify/` re-verified dashboard |

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


## Session a9dba5c2 — isolated /for-two/ integration

- Initial claim f3f305e was committed/pushed on the fixed branch `arena/a9dba5c2-chinafun3` when only the original README was visible. Original complete board/log is preserved at `for-two/COORDINATION-session.md`.
- On publication check, fetched `origin/main` 62a8a24 and discovered the root, docs/ and considered/ owners. Claimed non-overlapping `for-two/**` plus unique `.github/workflows/validate.yml` in a4b942c and pushed immediately before relocating. Root README/navigation/data and other sessions’ build/research tools are not changed.
- Relocation committed as 10133ae. Merge of origin/main paused for COORDINATION add/add and README modify/delete conflicts. Resolution preserves origin/main’s full board above, appends this handoff, restores root README byte-for-byte from origin/main, and retains this session’s README/research/site/tests separately under for-two/. No session’s work was discarded.
- Scope: `for-two/**` (a9dba5c2 only); `.github/workflows/validate.yml` (a9dba5c2 only); root COORDINATION append-only. Existing scopes above remain unchanged. Root navigation-link request: owner may optionally link `for-two/index.html` after review.
- Research: **needs review** (published F01–F13; inherited dashboards also explicitly not reverified). Four hotel candidates, seven dining records, five activities, 51 evidence/media sources. Six official dated Peninsula quotes and surcharge arithmetic; four usable published couple meal totals. No inferred hotel price, private bathroom confirmation, timed transit rank or 2027 menu guarantee. Evidence in `for-two/data/trip.json`, audit at `for-two/research/verification.md`.
- Site/test implementation: **done**, publication integration **in progress**. Before relocation: 9 offline tests and 113 desktop/mobile/browser/accessibility checks passed. Re-running at /for-two/ before PR. No completion claim for other owners’ factual research.
- Direct Pages settings update denied HTTP 403. Existing main / publication is retained; plan is explicit PR merge from this branch, no direct push/checkout of main and no settings bypass.

### a9dba5c2 relocation verification complete

- **done**: isolated `/for-two/` build regenerated; 9 Python tests + 113 real-browser checks passed after relocation, including axe desktop/mobile and 320–1440px overflow checks. Combined repository scan: 40 tracked HTML files, zero missing relative-file targets. Existing other-owner files unchanged against main 62a8a24.
- **needs review**: F14 now published in `for-two/review.html`: preserved parallel dashboards are not independently reverified; do not combine their factual claims without official-source reconciliation. F01–F13 remain published research gaps, not deployment blockers.
- **in progress**: PR integration and actual Pages reachability verification. Evidence/results at `for-two/research/release.md`. Direct Pages update denial is not bypassed.

- Publication synchronization: PR #6 landed a completion note while PR #7 opened. Merged main c21b265, preserving that full board and appending this session’s log; no content or ownership lost.

### a9dba5c2 final handoff — 25 November 2026

- **done**: PR #7 merged at 13:32 UTC, merge e7c538fdec3a5451e8bc36dabdbc6b11a2244990. Both CI checks passed. GitHub Pages build/deploy run 45624561650 completed successfully for that exact commit. Published dashboard path: https://kanlerxz87-cyber.github.io/ChinaFun3/for-two/ .
- **needs review**: research F01–F14 remain published; no one-hour ranking, hotel checkout total, private-bathroom confirmation or complete China-wide cheapest-stay claim. Public-page fetch failed in this environment even after deployment; independent public HTTP/content verification is unconfirmed (github.io is not in sandbox allowlist). Local identical-subpath browser checks passed.
- **done**: conflict resolutions preserved both owners’ complete coordination logs and existing other-owner files. Final source/test/publication evidence: `for-two/research/verification.md`, `for-two/research/release.md`, `for-two/sources.html`. No bookings, messages to hotels or future monitoring were initiated. Optional root-nav link remains a request to the root owner, not an unauthorized edit.

---

## Session `arena/7449eccd-chinafun3` — plan site (`plan/**`), merged via PR #9

**Scope (non-overlapping):** `plan/**`, `data/dataset.py`, `generate.py`, `check_links.py`. No root-site,
`docs/**`, `for-two/**` or `considered/**` file was modified. The two shared files (`README.md`,
`COORDINATION.md`) were kept as `main`'s version with this section appended — nothing removed.

| ID | Task | Status | Owner | Files |
|---|---|---|---|---|
| U1 | Dataset + generator + link checker | **done** | `arena/7449eccd-chinafun3` | `data/dataset.py`, `generate.py`, `check_links.py` |
| U2 | Hotels ranked by in-building starred density | **done** | `arena/7449eccd-chinafun3` | `plan/hotels.html` |
| U3 | All 50 starred rows + Bib sample, star vs listed | **done** | `arena/7449eccd-chinafun3` | `plan/michelin.html` |
| U4 | Activities, dates/weather, booking calendar | **done** | `arena/7449eccd-chinafun3` | `plan/activities.html`, `plan/dates.html` |
| U5 | Open questions, suggestions, flagged, verification | **done** | `arena/7449eccd-chinafun3` | `plan/questions.html`, `plan/suggestions.html`, `plan/flagged.html`, `plan/verification.html` |
| U6 | Merge with `main` without discarding other sessions' work | **done** | `arena/7449eccd-chinafun3` | conflict resolved additively |

### Sources verified in this session
- MICHELIN Shanghai all-starred (50 entries) and Bib Gourmand lists: https://guide.michelin.com/en/cn/shanghai-municipality/shanghai/restaurants/all-starred
- 2026 selection announcement: https://guide.michelin.com/en/article/michelin-guide-ceremony/michelin-guide-shanghai-jiangsu-zhejiang
- Taian Table official FAQ pricing: https://sh.taian-table.cn/faq/
- Individual MICHELIN restaurant pages for 19 rows (address, phone, hours, official site) — each row on `plan/michelin.html` links its own page.
- Brand room pages: Peninsula, Bvlgari, Ritz-Carlton Pudong, Waldorf Astoria, Fairmont Peace, Grand Hyatt.
- Shanghai Museum hours notice; Shanghai Disneyland calendar; shmetro.com network facts.

### Irregularities logged (detail on `plan/flagged.html`)
- City page counter shows 1×3★ / 11×2★ / 38×1★ = 50, while the 2026 launch release reports 12 two-star across the
  wider region — discrepancy documented, city counter used.
- MICHELIN ¥¥¥¥ tiers are relative bands, never converted to currency.
- Peninsula structured-data "price range" is not a dated quote and is not used as a rate.
- Ultraviolet (closed 29 Mar 2025) and the not-yet-open Four Seasons Shanghai excluded.
- Feb-2027 room rates, 51 of 58 restaurant hour sets, 57 of 58 restaurant prices and all measured transit times
  remain **unverified and blank** by design.

### Merge notes
- `main` had advanced with PRs #1–#8 (root site + `docs/` + `for-two/` + `considered/`). Our site was relocated
  to `plan/` before merging so no other session's page names were contested; the merge then produced conflicts
  only in `README.md` and `COORDINATION.md`, resolved by keeping `main`'s text and appending this section.

### Round 3 (session `arena/7449eccd-chinafun3`) — post-publish verification

**Yu Garden resolved from the official site** (previously blank + flagged):
- Hours `09:00-16:30`, last entry `16:00`, garden cleared `16:30`; closed Mondays except national public holidays.
- Price is seasonal and February is **off-peak**: ¥30 adult (1 Dec-31 Mar) vs ¥40 peak (1 Apr-30 Jun, 1 Sep-30 Nov).
- Gates: north 168 Fuyou Road (groups + individuals), south 279 Yuyuan Old Street (individuals only); office 218 Anren Street, Huangpu; tel 021-63260830.
- Transport: Metro 10/14 Yuyuan Garden + bus 11/26/64/736/926/929/932/969/980/Fangchuan.
- Sources: https://www.yugarden.com.cn/page/articleView/message.html · https://www.yugarden.com.cn/page/articleView/traffic.html

**Irregularity caught:** every third-party guide consulted gave a different Yu Garden answer (08:30-17:00 vs
09:00-16:30; ¥30 / ¥40 / ¥50; "closed some Mondays" vs daily). Only the official page is used; the discrepancy is
documented on `plan/flagged.html` and `plan/verification.html` as evidence for the "official sources only" rule.

**Social accounts accepted (4, each tied to the venue):** Taian Table via chef Stefan Stiller's account (bio lists
TT Shanghai with three stars); Fu He Hui (bio states 2★ and 1037 Yuyuan Road); The Shanghai Museum; Shanghai
Disneyland park account (launch announced by the resort's verified X account).

**Build status:** `python3 generate.py` → 9 pages; `python3 check_links.py` → no broken internal links, no
malformed tables. Published at `/plan/` after PR #9 merged to `main`; Pages build `779e15f` reported `built`.

### Round 4 — duration options and a closing-day-aware skeleton
- Added a 7 / 10 / 14-night comparison to `plan/dates.html` (the brief allows 1-2 weeks inside 15 Feb-23 Mar 2027).
- Added a 7-night day skeleton derived **only** from verified closures: Yu Garden and Shanghai Museum (People's
  Square) shut Mondays, Shanghai Museum East shut Tuesdays, Da Vittorio shut Mondays, 8½ Otto e Mezzo lunch
  Thu-Sun only. Lantern Festival (20 Feb) is the anchor evening.
- Dashboard now links the itinerary directly.
- `python3 check_links.py` → 9 pages, no broken links, no malformed tables.

---

## Task Board — Session `arena/b27f0613-chinafun3` (scope: `verify/**` + append-only `COORDINATION.md` + `README.md` link section + new `.github/workflows/verify-dashboard.yml`)

| ID | Task | Status | Owner Session | Files Touched / Scope | Sources & Verification Note | Updated |
|---|---|---|---|---|---|---|
| V01 | Claim scope & fresh re-verification of Michelin 2026 Shanghai directory | **done** | `b27f0613` | `COORDINATION.md` | Full 50-restaurant starred directory scraped from guide.michelin.com all-starred listing (1×3★, 11×2★, 38×1★); cross-checked vs official 2026-04-09 press release (guide.michelin.com + webwire mirror) | 2026-11-25 |
| V02 | Hotel shortlist + live Feb 15–22 2027 rate verification | **done** | `b27f0613` | `verify/data/hotels.json` | 8 hotels; "starting at" USD rates for Feb 15–22 2027 pulled live from the MICHELIN Guide Hotels booking engine (official channel) 2026-11-25; Waldorf = sold out that window (flagged) | 2026-11-25 |
| V03 | Michelin restaurant deep verification (address/hours/website/phone) | **done** | `b27f0613` | `verify/data/restaurants.json` | 12 restaurant pages on guide.michelin.com verified (stars, address, district, band, phone, website); hours verified for 4 (T'ang Court via langhamhotels.com, Da Vittorio / Fu He Hui / Ling Long via guide pages) | 2026-11-25 |
| V04 | Activities with official hours/tickets/social links | **done** | `b27f0613` | `verify/data/activities.json` | Yu Garden (yugarden.com.cn) + Shanghai Museum (shanghaimuseum.net, 8 official socials) verified; Disney site verified but hours flagged; Bund/Oriental Pearl/Jing'an Temple flagged (official sites unreachable) | 2026-11-25 |
| V05 | Exact menu pricing | **done** | `b27f0613` | `verify/data/restaurants.json`, `verify/budget.html` | T'ang Court 2026 official menu PDF: ¥888 dim-sum lunch set for 2; ¥2,288 all-day set for 2 (incl. service + taxes) — exact totals for 2 | 2026-11-25 |
| V06 | Dashboard site build (mobile-friendly tables, 11 pages) | **done** | `b27f0613` | `verify/**`, `verify/scripts/build.py`, `verify/assets/*` | Generated from JSON; every table row has Source link or Unverified flag | 2026-11-25 |
| V07 | Verification tests + CI workflow | **done** | `b27f0613` | `verify/tests/test_site.py`, `.github/workflows/verify-dashboard.yml` (new file) | Row-source audit, link resolution, JSON schema, arithmetic checks | 2026-11-25 |
| V08 | Q&A gaps + suggestions section | **done** | `b27f0613` | `verify/questions.html`, `verify/suggestions.html` | Open questions list + decision-improvement suggestions with discovery actions | 2026-11-25 |
| V09 | Flagged-for-review irregularities | **done (needs review)** | `b27f0613` | `verify/data/flagged.json`, `verify/flagged.html` | 102 House discrepancy; press-release vs directory counts; hotel filter-count mismatch; shmetro unreachable (transit unverified); site-reachability gaps | 2026-11-25 |
| V10 | Publication (PR → main → Pages `/verify/`) | **in progress** | `b27f0613` | — | Pages source stays `main` `/`; subsite addressable at `/verify/` like `/considered/`, `/for-two/`, `/docs/` | 2026-11-25 |

## Log — Session `arena/b27f0613-chinafun3`

| Timestamp (UTC) | Session | Action |
|---|---|---|
| 2026-11-25 | `b27f0613` | Branch `arena/b27f0613-chinafun3` created from `45c6f11` (branch base). Fetched `origin/main` (a1598cf) and merged (fast-forward, no conflicts) to synchronize with all prior sessions' merged work (root, docs/, considered/, for-two/, plan/). No other session's files modified. |
| 2026-11-25 | `b27f0613` | Verified Pages: source `main` `/`, status `built`, live at https://kanlerxz87-cyber.github.io/ChinaFun3/. |
| 2026-11-25 | `b27f0613` | Claimed V01–V10. Scope announced: new `verify/**` only + append-only COORDINATION + README link section + new CI workflow file. |
| 2026-11-25 | `b27f0613` | Verified official sources: Michelin 2026 regional press release (guide.michelin.com, 2026-04-08/09), full 50-restaurant starred directory (guide.michelin.com), 38-hotel Shanghai directory, 12 restaurant pages, Langham/Peninsula official sites, Yu Garden, Shanghai Museum, Shanghai Disney Resort. Live Feb 15–22 2027 hotel rates from the MICHELIN Guide Hotels booking engine. T'ang Court 2026 menu PDF (exact ¥888 / ¥2,288 for-two totals). |
| 2026-11-25 | `b27f0613` | Built `verify/` dashboard (11 generated pages, JSON-driven, every row source-linked or flagged), offline tests, CI workflow. See `verify/verification.html` for the line-by-line log. |

### Current session claim — 2026-11-26

| Task | Status | Owner | Scope |
|---|---|---|---|
| Independent repository and publication audit; publish actionable verified findings | in progress | `arena/3f54228c-chinafun3` | `audit-2026-11-26/**`, append-only `COORDINATION.md` |

Existing session scopes are respected; requests for changes to their files will be logged rather than edited. The Arena-assigned branch is fixed for this session.

**Scope takeover request/claim:** The root-site owner `arena/8205b531-chinafun3` last recorded a commit on 2026-11-25, more than 60 minutes ago. In accordance with the stale-claim handoff rule, this session claims only `index.html` for a prominent link to the independent audit and caution about unverified legacy figures. Other root files remain untouched; requests for corrections are logged in the audit.

### Audit findings and handoff — 2026-11-26

- Task status: **needs review**; targeted audit completed, not a comprehensive line-by-line repository verification. Scope: `audit-2026-11-26/index.html`, root `index.html` (stale-owner handoff above), this append-only log.
- Checked the official [2026 MICHELIN announcement](https://guide.michelin.com/en/article/michelin-guide-ceremony/michelin-guide-shanghai-jiangsu-zhejiang) against the legacy claim that 2024 was the latest. Claim is contradicted. Requested correction to legacy `executive-summary.html`, `restaurants.html`, related data and all affected tables by their owner or an integration session.
- Checked the [dated Andaz booking page](https://guide.michelin.com/en/hotels-stays/shanghai/andaz-xintiandi-shanghai-6510?arr=2027-02-15&dep=2027-02-22&nA=2&nC=0&nR=1): $169 starting / $197 including taxes per night. Multiplying by seven is indicative, not a confirmed checkout quote or verified qualifying room. Legacy surrogate figures and one-hour counts need source-by-source review; request correction in `hotels.html` and associated data.
- Checked the [State Council holiday notice hosted by Wuhan district government](https://www.dxh.gov.cn/ZWGK/zc_zwgk/ZFWJ/TZGG/202611/t20261106_2875104.shtml). Social search links are not reviews; official hours, current meal totals, actual full transit routes, room-specific amenities and cheapest dates remain incomplete. Details published in audit flagged page.
- Verification: `python3 check_links.py` (nine plan pages), `npm test` (eight considered tests), and `python3 -m unittest discover -s verify/tests` (ten verify tests) passed. New page local links checked separately. These do not validate every repository page or external link, nor facts. ResourceWarnings in verify tests noted.
- PR #10 belongs to another active branch and has not been integrated or reviewed by this session. No other session's branch was merged or changed.

**Concurrent-session handoff:** After the above claim, GitHub showed active integration PR #16 (`arena/9ee6f5e0-chinafun3`, updated 2026-11-26) also owns `index.html` and is correcting legacy pages. Its claim was absent from this branch's board at the time of the handoff. To avoid overlapping work, this session relinquishes `index.html` and restores it to the branch base. Request to integration owner: include a prominent link to `audit-2026-11-26/` and retain the cautions that nightly starting rates times seven are not verified checkout totals, one-hour counts require individual measured routes, and search links are not reviews. PR #16 was reported conflicting by GitHub; its owner should resolve that conflict without discarding other work. A broad local scan of 61 HTML files found zero missing relative resources; this is not external-link verification.

---

## Task Board — Session `arena/9ee6f5e0-chinafun3` (FINAL INTEGRATION — scope: root site fixes + append-only `COORDINATION.md` + `README.md` integration section)

| ID | Task | Status | Owner Session | Files Touched / Scope | Sources & Verification Note | Updated |
|---|---|---|---|---|---|---|
| W01 | Claim integration scope & audit all sites vs requirements | **done** | `9ee6f5e0` | `COORDINATION.md` | Audit root/docs/considered/for-two/plan/verify vs brief; PR #10 divergence flagged | 2026-11-26 |
| W02 | Line-by-line official re-verification (Michelin 2026, CNY 2027, visa, Yu Garden, Museum, Taian price, Andaz rate) | **done** | `9ee6f5e0` | `COORDINATION.md`, `flagged.html` | guide.michelin.com (50 starred, Taian 3★ Changning), gov.cn 2027 notice, NIA 240h, yugarden.com.cn, shanghaimuseum.net, Michelin Hotels engine | 2026-11-26 |
| W03 | Fix root site outdated Michelin (2024→2026: 50 starred, Ultraviolet closed, Fu He Hui 2★, Taian district/price) | **done** | `9ee6f5e0` | `index.html`, `restaurants.html`, `executive-summary.html`, `sources.html`, `flagged.html`, `data/restaurants.json` | Official 2026 directory + Taian page + closure notice | 2026-11-26 |
| W04 | Fix activities (Yu Garden off-season ¥60/2, Museum last entry 15:00 + .cn domain) + add live 2027 hotel rates + subsite nav | **done** | `9ee6f5e0` | `activities.html`, `hotels.html`, `index.html`, `budget.html` | yugarden.com.cn, shanghaimuseum.net, Michelin Hotels engine (Andaz $169/$197) | 2026-11-26 |
| W05 | Re-verify combined data, run all tests, check links, mobile preview | **done** | `9ee6f5e0` | all | check_links.py, verify/tests, considered/tests, for-two tests | 2026-11-26 |
| W06 | PR from integration branch to main, merge, confirm Pages deploy, log PR link | **done** | `9ee6f5e0` | — | Pages source main /, status built | 2026-11-26 |

## Log — Session `arena/9ee6f5e0-chinafun3`

| Timestamp (UTC) | Session | Action |
|---|---|---|
| 2026-11-26 | `9ee6f5e0` | Branch `arena/9ee6f5e0-chinafun3` from `73a7acb` (main HEAD, Pages built). Audited root/docs/considered/for-two/plan/verify + open PR #10 (divergent from initial commit `fa1f9fa`, would delete all merged work — flagged, will NOT merge). Claimed W01–W06 as final integration (shared outputs per brief). |
| 2026-11-26 | `9ee6f5e0` | Official re-verification: Michelin all-starred directory = 50 (1×3★ Taian Table Changning, 11×2★, 38×1★) — root's 51/2×3★ is 2024-outdated; Ultraviolet closed 2025-03-29; Taian ¥2,588/¥2,888pp → ¥5,176–5,776/2; Andaz live $169/$197 Feb 15–22 2027 confirmed; Yu Garden off-season ¥30pp; Museum last entry 15:00 + domain → .cn 2027-01-01; CNY 2027 Feb 6, holiday Feb 5–13; NIA 240h/57/65. |
| 2026-11-26 | `9ee6f5e0` | W03/W04 fixes applied: root Michelin 2024→2026 (50 starred, Taian sole 3★ Changning ¥5,176–5,776/2, Ultraviolet CLOSED 2025-03-29, Fu He Hui 2★); Yu Garden ¥60/2 off-season; Museum last entry 15:00 + .cn domain; live Feb 15–22 2027 rates (Andaz $1,183) + subsite nav on index; flags F03 resolved, F12–F14 added; data/restaurants.json updated. Tests: check_links OK, verify 10/10, considered 8/8, all pages HTTP 200. |

## Session `arena/d4b2f26a-chinafun3` — Final Verification & Audit

- **Branch:** `arena/d4b2f26a-chinafun3` (from `main` `73a7acb`)
- **Timestamp:** 2026-11-26 UTC
- **Checks performed:**
  - `python3 check_links.py`: checked 9 pages, no problems found.
  - JSON validation across `data/*.json` and `docs/data/*.json`: all 11 JSON files parsed cleanly.
  - GitHub Pages status: `built` on `main` `/` at `https://kanlerxz87-cyber.github.io/ChinaFun3/`.
- **Status:** Done — no broken links or JSON errors found.
| 2026-11-26 | `9ee6f5e0` | W05/W06 done: re-verified combined data (check_links OK, verify 10/10, considered 8/8, all pages 200, mobile viewport+table-wrap). PR #16 https://github.com/kanlerxz87-cyber/ChinaFun3/pull/16 MERGED 2026-11-26T19:12:30Z (merge commit 0bbd4d5). Pages build `built` on main `/` — live at https://kanlerxz87-cyber.github.io/ChinaFun3/ (root + /docs/ + /considered/ + /for-two/ + /plan/ + /verify/). Merge conflict with PR #15 (d4b2f26a) in COORDINATION.md resolved keeping both boards, no discard. PR #10 NOT merged (divergent, would delete all work — F12). |

**2026-11-26 merge reconciliation:** Merged updated `origin/main` into this session branch; resolved the sole `COORDINATION.md` conflict by retaining both sessions’ complete appended boards and logs. No other content was discarded. PR #16 has since merged; previous requests concerning its pending state are historical.
