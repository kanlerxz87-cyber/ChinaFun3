# COORDINATION — ChinaFun3 Trip Planning (Shared Task Board)

Session ID for this branch: `69c89392` (branch `arena/69c89392-chinafun3`)
Rule: claim before editing, commit+push claim immediately, non-overlapping scopes, small frequent commits, `git pull --rebase` before push.

| Task ID | Task | Status | Owner Session | Files Touched | Sources / Verification | Irregularities |
|---|---|---|---|---|---|---|
| T1 | Michelin China data (Shanghai-Jiangsu-Zhejiang 2026, Beijing 2025, Guangzhou-Shenzhen 2026) | done | 69c89392 | `data/restaurants.csv`, `data/restaurants.json`, `pages/restaurants.html` | guide.michelin.com 2026 regional edition; michelin.com Beijing 2025; Guangzhou/Shenzhen 2026 release | 2027 guide not yet published — Feb 2027 stars unverified; Ultraviolet closed 29 Mar 2025 per secondary source, needs official re-check |
| T2 | Hotels Shanghai (queen+, private bath, 7-night pricing methodology) | done | 69c89392 | `data/hotels.csv`, `data/hotels.json`, `pages/hotels.html` | Official hotel sites (Hilton, Hyatt, Peninsula) for room types; pricing left blank/unverified — Feb 2027 rates not bookable at research date | No live Feb 2027 pricing available; do not infer |
| T3 | Activities within 1h (Shanghai Museum, Yu Garden, Oriental Pearl, Disneyland, Bund) | done | 69c89392 | `data/activities.csv`, `data/activities.json`, `pages/activities.html` | shanghaimuseum.net official hours; Yu Garden official notices via secondary; shanghaidisneyresort.com; shmetro.com | Oriental Pearl hours conflict across secondary sources — flagged unverified, check official |
| T4 | Site build (GitHub Pages dashboard, mobile-friendly) | done | 69c89392 | `index.html`, `pages/*.html`, `assets/*` | Build check + link check | — |
| T5 | Verification pass (every row source link or blank+unverified) | unclaimed | — | `pages/verification.html`, `pages/suggestions.html` | Line-by-line review | Visa-free expires 31 Dec 2026 — 2027 entry unverified |

## Log
- 2026-11-25: Session 69c89392 created board, claimed T1–T4 (single-session build; T5 left unclaimed for independent review). No other sessions active at creation.
- 2026-11-25: Session 69c89392 completed T1–T4: data/*.csv+json (23 restaurants, 5 hotels, 5 activities), 7-page static site, link check passed (0 broken internal links), all pages HTTP 200. T1–T4 marked done below. T5 remains unclaimed for independent review.
