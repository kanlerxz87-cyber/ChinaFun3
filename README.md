# ChinaFun3 — Trip Planning China (Feb–Mar 2027)

Verified, mobile-friendly trip planner for 2 adults: Shanghai base (densest Michelin cluster), 5 hotels ranked by 1-hour Michelin access, 23 Michelin restaurants, 5 activities ≤1h, 8 seven-night date options.

## Live site (GitHub Pages)
- Enable Pages: **Settings → Pages → Source: Deploy from branch → `arena/69c89392-chinafun3` → `/ (root)`** (or merge to `main` then select `main`).
- Pages: `index.html` (dashboard) · `pages/hotels.html` · `pages/restaurants.html` · `pages/activities.html` · `pages/itinerary.html` · `pages/verification.html` · `pages/suggestions.html`
- Data (single source of truth): `data/*.csv` + `data/*.json`

## Verification rule
Every row has an official source link. Unverifiable = blank + `Unverified`. No inferred prices, hours, or social links.

## Coordination
See [COORDINATION.md](COORDINATION.md). This session (69c89392) owns T1–T4; T5 is open for independent review.
