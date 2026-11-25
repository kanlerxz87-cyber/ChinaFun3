# COORDINATION.md

Shared task board for parallel agent sessions.  
**Rule:** claim before starting, keep scopes non-overlapping, commit/push claims immediately, never mark verified without an official source link.

## Session Registry

| Session ID | Branch | Status | Last update (UTC) | Notes |
|---|---|---|---|---|
| c8dcd263 | arena/c8dcd263-chinafun3 | active | 2026-11-25T00:30:00Z | Created initial draft: research log, data, analysis, static GitHub Pages site. Many requested fields remain unverified/partial; see flags. |

## Task Board

| Task | Status | Owner | Files/scope | Started (UTC) | Updated (UTC) | Notes |
|---|---|---|---|---|---|---|
| T1 Repo review & baseline audit | done | c8dcd263 | `README.md`, `COORDINATION.md` | 2026-11-25T00:00:00Z | 2026-11-25T00:30:00Z | Repo was near-empty (README only). No prior code/data/site. Created structure and docs. |
| T2 Research: destination, hotels, Michelin restaurants, activities, transport, pricing | in_progress | c8dcd263 | `data/`, `research/` | 2026-11-25T00:00:00Z | 2026-11-25T00:30:00Z | Partial verified data collected from MICHELIN official pages and hotel official/booking refs. 2027 date-specific pricing, full hours/social/transit verification incomplete. |
| T3 Analysis: executive summary, questions, suggestions, decision gaps | done | c8dcd263 | `analysis/`, `plan.html` | 2026-11-25T00:00:00Z | 2026-11-25T00:30:00Z | Executive summary, questions/gaps, assumptions, suggestions documented. |
| T4 GitHub Pages site build | in_progress | c8dcd263 | `index.html`, `hotels.html`, `restaurants.html`, `activities.html`, `plan.html`, `sources.html`, `assets/`, `.nojekyll` | 2026-11-25T00:00:00Z | 2026-11-25T00:30:00Z | Static mobile-friendly dashboard created; local link check passed. Data completeness/verification still partial. |
| T5 Verification & integration | needs_review | c8dcd263 | all owned files | 2026-11-25T00:00:00Z | 2026-11-25T00:30:00Z | Partial verification complete. Not all requested rows/fields verified; flagged items must be reviewed before booking/publishing as final. |

## Handoff / Conflict Log

| Time (UTC) | Session | Event | Details |
|---|---|---|---|
| 2026-11-25T00:00:00Z | c8dcd263 | Initialized coordination | Created COORDINATION.md; claimed T1-T5 on arena/c8dcd263-chinafun3. |
| 2026-11-25T00:30:00Z | c8dcd263 | Draft deliverables pushed | Added research/data/analysis/static site. Remaining gaps flagged in F1-F6. |

## Verification Log

| Item | Source checked | Result | Session | Time (UTC) |
|---|---|---|---|---|
| MICHELIN Shanghai restaurant counts/filters | https://guide.michelin.com/en/cn/shanghai-municipality/shanghai/restaurants ; https://guide.michelin.com/en/cn/shanghai-municipality/shanghai/restaurants/all-starred | Verified listing shows 153 total; filters 1x3*,11x2*,38x1*,33 Bib,70 Selected (accessed 2026-11-25) | c8dcd263 | 2026-11-25T00:30:00Z |
| 2026 MICHELIN Shanghai/Jiangsu/Zhejiang announcement | https://guide.michelin.com/en/article/michelin-guide-ceremony/michelin-guide-shanghai-jiangsu-zhejiang | Verified announcement date 2026-04-09 and Shanghai promotions/new stars named in article | c8dcd263 | 2026-11-25T00:30:00Z |
| Da Vittorio details | https://guide.michelin.com/en/shanghai-municipality/shanghai/restaurant/da-vittorio-570570 | Verified 2*, address, phone, website, hours Tue-Sun 12:00-13:30/18:00-21:30, Mon closed | c8dcd263 | 2026-11-25T00:30:00Z |
| Lao Zheng Xing details | https://guide.michelin.com/us/en/shanghai-municipality/shanghai/restaurant/lao-zheng-xing-huangpu | Verified 1*, address, phone, price ¥¥ | c8dcd263 | 2026-11-25T00:30:00Z |
| Ren He Guan (Xuhui) details | https://guide.michelin.com/en/shanghai-municipality/shanghai/restaurant/ren-he-guan-zhaojiabang-road | Verified 1*, address, phone, price ¥¥ | c8dcd263 | 2026-11-25T00:30:00Z |
| Fu 1015 details | https://guide.michelin.com/en/shanghai-municipality/shanghai/restaurant/fu-1015 | Verified 1*, address, phone, price ¥¥¥¥ | c8dcd263 | 2026-11-25T00:30:00Z |
| Hotel 7-night pricing 2027-02-15→22 | Booking/Trip snippets; no official date-stamped checkout quote | Unverified - indicative only | c8dcd263 | 2026-11-25T00:30:00Z |
| Local site links | `python3` local href existence check | Passed (`OK`) for local links in *.html | c8dcd263 | 2026-11-25T00:30:00Z |

## Irregularities / Flagged for Review

| ID | Item | Issue | Severity | Source | Status |
|---|---|---|---|---|---|
| F1 | Hotel 7-night totals for 2027-02-15→22 | No date-stamped checkout quote confirmed; indicative nightly rates not booking quotes. | High | S8-S11 | needs review |
| F2 | Cheapest upcoming time to book | No definitive official/verifiable source; requires price tracking method. | High | N/A | needs review |
| F3 | Restaurant hours/social/couple-cost completeness | Most venues missing verified hours, official social links, exact per-couple menu pricing. | High | S4-S7 | needs review |
| F4 | Transit <=1hr claim | Transit times are estimates; not route-verified at travel time. | Medium | N/A | needs review |
| F5 | Destination/date conflict in request | "1-2 weeks" conflicts with "preferred Feb 15–18 2027"; city unspecified. Draft assumes Shanghai + 7 nights 2027-02-15→22. | Medium | User request | needs review |
| F6 | Activities unspecified | Activities proposed, not user-selected; details unverified. | Medium | S12-S14 | needs review |
