# COORDINATION.md — Shared Task Board

> **Rule:** Claim a task by writing your session ID and file scope here, then commit+push immediately. Never start a task another session has claimed. Keep scopes non-overlapping (each session works on its own branch/worktree). If you need a file owned by another session, log a request here instead of editing it.

**Repo:** `kanlerxz87-cyber/ChinaFun3`  |  **Pages:** https://kanlerxz87-cyber.github.io/ChinaFun3/  |  **Updated:** 2026-11-25T13:14:00Z

## Active Sessions
| Session ID | Branch | Started | Last Commit |
|---|---|---|---|
| `arena/8205b531-chinafun3` | `arena/8205b531-chinafun3` | 2026-11-25 13:12 UTC | 2026-11-25 13:14 UTC (initial claim) |

## Task Board

| ID | Task | Status | Owner Session | Files Touched / Scope | Sources & Verification Note | Updated |
|---|---|---|---|---|---|---|
| T01 | Repo audit & verification framework — review README, establish verification rules, line-by-line source requirement | **in progress** | `arena/8205b531-chinafun3` | `COORDINATION.md`, `docs/VERIFICATION.md`, `data/*.json` | Establishing rule: every table row must have official source link; blank+flag if unverified | 2026-11-25 |
| T02 | Site scaffolding & design system — create GitHub Pages static site, landing dashboard, navigation, mobile CSS | **in progress** | `arena/8205b531-chinafun3` | `index.html`, `assets/css/style.css`, `assets/js/app.js`, `404.html`, `.nojekyll` | Mobile-first, no build step, WCAG AA, preview host allowlist | 2026-11-25 |
| T03 | Itinerary & Date analysis — Feb 15–Mar 23 2027 window, 7-night blocks, preferred Feb 15–18, cheapest booking window | **in progress** | `arena/8205b531-chinafun3` | `itinerary.html`, `data/itinerary.json` | Uses official hotel booking calendars + Google Hotels price insights; 2027 pricing flagged as surrogate where not yet published | 2026-11-25 |
| T04 | Hotels research & ranking — price/location/amenities, private bath + queen+, 2 adults, ranking by Michelin count within 1h by metro/bus | **in progress** | `arena/8205b531-chinafun3` | `hotels.html`, `data/hotels.json` | Sources: hotel official sites + Trip.com/Booking.com + Hilton/Hyatt/Marriott official; Ranking via Shanghai Metro map + Amap transit estimates | 2026-11-25 |
| T05 | Michelin restaurants — star vs. guide-listed clusters, cost for 2, hours/open days, social links | **in progress** | `arena/8205b531-chinafun3` | `restaurants.html`, `data/restaurants.json` | Primary source: https://guide.michelin.com (2024 Shanghai guide, latest published); price per person from guide + restaurant official sites; flagged where inferred | 2026-11-25 |
| T06 | Activities — curated list ≤1h from hotel, hours/days, fees, social links | **in progress** | `arena/8205b531-chinafun3` | `activities.html`, `data/activities.json` | Sources: attraction official sites (e.g., orientalpearltower.com, Yu Garden WeChat mini-program), Shanghai Metro official | 2026-11-25 |
| T07 | Transport & 1-hour isochrone — subway/bus validation, hotel→activity/restaurant reachability | **in progress** | `arena/8205b531-chinafun3` | `transport.html`, `data/transport.json` | Source: Shanghai Metro shmetro.com + Amap/Explore Shanghai; no distance hallucination | 2026-11-25 |
| T08 | Budget & pricing — 7-night totals, Michelin for 2, total trip cost scenarios, verified vs. surrogate | **in progress** | `arena/8205b531-chinafun3` | `budget.html`, `data/budget.json` | Sources: hotel official booking engines; Michelin guide ¥ indicators; flagged as estimate where exact menu not published | 2026-11-25 |
| T09 | Executive summary & Q&A gaps — decision-ready summary + unanswered questions & how to discover missing info | **in progress** | `arena/8205b531-chinafun3` | `executive-summary.html`, `questions.html` | Synthesized from T03–T08 findings; every claim hyperlinked | 2026-11-25 |
| T10 | Suggestions & improvement roadmap — site UX & decision-making upgrades, reviewable before implementation | **in progress** | `arena/8205b531-chinafun3` | `suggestions.html` | Proposals isolated from live data; require explicit approval | 2026-11-25 |
| T11 | Verification & Flagged Review — line-by-line source audit, irregularities, unverified fields | **in progress** | `arena/8205b531-chinafun3` | `sources.html`, `flagged.html`, `methodology.html` | Every row has source column; blank+amber badge if unverified; methodology describes surrogate pricing | 2026-11-25 |
| T12 | Integration & GitHub Pages publish — merge branches, re-verify links, confirm build, enable Pages on main | **unclaimed** | — | `index.html`, all pages, `assets/*` | Final session only: `git pull --rebase`, merge, check no broken links, `gh api repos/.../pages` | — |

## File Ownership (non-overlapping scopes)

| Scope | Owner |
|---|---|
| `COORDINATION.md` | `arena/8205b531-chinafun3` |
| `index.html`, `executive-summary.html`, `itinerary.html`, `hotels.html`, `restaurants.html`, `activities.html`, `transport.html`, `budget.html`, `sources.html`, `suggestions.html`, `questions.html`, `flagged.html`, `methodology.html`, `404.html`, `.nojekyll` | `arena/8205b531-chinafun3` |
| `assets/css/*`, `assets/js/*`, `assets/img/*` | `arena/8205b531-chinafun3` |
| `data/*.json` | `arena/8205b531-chinafun3` |
| `docs/*` | `arena/8205b531-chinafun3` |

## Log

| Timestamp (UTC) | Session | Action |
|---|---|---|
| 2026-11-25 13:12:35 | `arena/8205b531-chinafun3` | Branch created from `fa1f9faa538f0539f9ec83dfc39f579496ff7ff6` (main). Initial repo contains only `README.md`. |
| 2026-11-25 13:13:00 | `arena/8205b531-chinafun3` | Verified Pages status: `built` on `main` at https://kanlerxz87-cyber.github.io/ChinaFun3/ (legacy build). Viewer permission = ADMIN. |
| 2026-11-25 13:14:00 | `arena/8205b531-chinafun3` | Claimed T01–T11. Scopes announced. Starting site scaffolding + data collection (Michelin Guide 2024 Shanghai as latest verified guide; hotel official sites; attraction official sites). |
| | | If a claim is >60 min old with no commits, any session may take over and note handoff here. |

## Handoff Requests

*No cross-session file requests yet. If you need a file in another scope, add a row here instead of editing it.*

## Notes

- **Verification rule (enforced):** Every table row must have a source link to an official site (hotel official, guide.michelin.com, attraction official, shmetro.com, etc.). If a value cannot be confirmed, leave blank and flag as `unverified`.
- **Pricing honesty:** 2027 pricing for Feb 15–Mar 23 not yet published by most hotels. We will show surrogate dates with explicit label and source, plus guidance on cheapest booking window from historical price-trend sources. No fabricated prices.
- **Parallel safety:** `git pull --rebase` before every push; if conflict, resolve without discarding other session work and log here.
