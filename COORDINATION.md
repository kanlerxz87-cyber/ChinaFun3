# COORDINATION — ChinaFun3 Trip Planning

Session ID: `session-7449eccd` (branch `arena/7449eccd-chinafun3`)
Last updated: 2026-11-25

## Task board

| ID | Task | Status | Owner | Files touched |
|----|------|--------|-------|---------------|
| T1 | Repo review + COORDINATION setup | done | session-7449eccd | COORDINATION.md, README.md |
| T2 | Research: Michelin clusters (Shanghai/Beijing/Guangzhou-Shenzhen) from guide.michelin.com | done | session-7449eccd | data/michelin.json, michelin.html |
| T3 | Research: Hotels (queen+, private bath) + 7-night pricing methodology | done | session-7449eccd | data/hotels.json, hotels.html |
| T4 | Research: Activities within 1h + hours + social links | done | session-7449eccd | data/activities.json, activities.html |
| T5 | Research: Dates (CNY 2027), weather, transit, booking windows | done | session-7449eccd | pricing.html |
| T6 | Build GitHub Pages site (landing + subpages, mobile-friendly dashboard) | in progress | session-7449eccd | index.html, *.html, assets/* |
| T7 | Verification pass: every row has official source or flagged unverified | in progress | session-7449eccd | verification.html, flagged.html |
| T8 | Final integration + Pages publish + broken-link check | unclaimed | — | all |

## Rules followed
- No manual input requested; all work done autonomously.
- Every table row links to an official source. Unconfirmed values left blank + flagged **Unverified**.
- No inferred prices. Hotel 7-night totals for Feb 2027 are dynamic (require live booking search) — flagged unverified with direct official booking links.
- Only Taian Table price is from the restaurant's official FAQ (verified). Other restaurant prices from secondary sources are labelled as such, not presented as official.
- Parallel sessions: claim by writing session ID here, commit+push immediately, keep scopes non-overlapping, `git pull --rebase` before push.

## Sources & verification log
- Michelin Shanghai|Jiangsu|Zhejiang 2026 (official, 2026-04-09): https://guide.michelin.com/en/article/michelin-guide-ceremony/michelin-guide-shanghai-jiangsu-zhejiang — 409 restaurants, 77 starred (1×3★, 14×2★, 62×1★); Shanghai 156 restaurants.
- Taian Table official page (3★, Changning, ¥¥¥¥): https://guide.michelin.com/en/shanghai-municipality/shanghai/restaurant/taian-table
- Taian Table official FAQ prices ¥2,588 (10-course) / ¥2,888 (12-course): https://sh.taian-table.cn/faq/
- Grand Hyatt Shanghai official rooms (1 Queen Bed, 2 Queen Beds, private bath/tub): https://www.hyatt.com/grand-hyatt/en-US/shagh-grand-hyatt-shanghai/rooms
- Waldorf Astoria Shanghai on the Bund official rooms (Double Queen Deluxe etc.): https://www.hilton.com/en/hotels/shawawa-waldorf-astoria-shanghai-on-the-bund/rooms/
- Fairmont Peace Hotel official rooms (Fairmont Queen Queen, marble bathroom): https://www.fairmont.com/en/hotels/shanghai/fairmont-peace-hotel/rooms/DBCMV.room.html
- Bvlgari Hotel Shanghai official (82 rooms, Bao Li Xuan on site): https://www.bulgarihotels.com/en-US/shanghai
- Peninsula Shanghai official rooms/suites: https://www.peninsula.com/en/shanghai/luxury-hotel-room-suite-types/the-palace-suite
- Shanghai Museum official hours 9:00–17:00, closed Mon (except holidays): https://www.shanghaimuseum.net/mu/frontend/pg/m/article/id/I00004797
- CNY 2027: Sat Feb 6, 2027; holiday Feb 5–13 (State Council notice via secondary summaries — flagged for gov.cn re-check).

## Irregularities flagged
- Four Seasons Shanghai (new, Huaihai Zhong Rd) is announced for 2027 opening — NOT bookable as an existing hotel for Feb 2027; excluded from ranking, listed as flagged.
- Ultraviolet by Paul Pairet (formerly 3★ Shanghai) closed 29 Mar 2025 — removed from all lists.
- Hotel nightly rates for Feb 2027 are not published on static official pages; 7-night totals left blank/unverified.
- Restaurant opening hours are not consistently published on Michelin pages; left blank/unverified where not on official restaurant site.
- Social links: only URLs returned by web search are used; platform search URLs are provided where no direct post URL was verified.

## Handoff log
- 2026-11-25 session-7449eccd claimed T1–T7 on branch arena/7449eccd-chinafun3.
