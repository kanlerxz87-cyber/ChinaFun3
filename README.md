# ChinaFun3 — Shanghai 2027 Trip Planning Dashboard

**Live site:** https://kanlerxz87-cyber.github.io/ChinaFun3/ (GitHub Pages, legacy build, `main` branch `/` root)

**Branch for this work:** `arena/8205b531-chinafun3` → PR → `main`

## What this is
A verified 7-night Shanghai trip plan for **Feb 15–Mar 23, 2027** (preferred Feb 15–18) for **2 adults**, **queen-size or larger bed**, **private bathroom**, with every restaurant and activity constrained to **≤1 hour by subway/bus** from the hotel.

We ranked **7 hotels** by the number of **Michelin-rated/starred restaurants within 1 hour** (Shanghai 2024 guide: 51 starred; latest published at 2026-11-25). Every hotel, restaurant, and activity row has an **official source link**; unverified fields are blank and flagged — never hallucinated.

## Quick links (the dashboard)

| Page | What you'll find |
|---|---|
| [Dashboard](index.html) | Overview + 3 modeled 7-night date blocks + hotel ranking preview + verification promise |
| [Executive Summary](executive-summary.html) | 60-sec decision + 3 budget scenarios + risks |
| [Itinerary & Dates](itinerary.html) | Feb 15–Mar 23 window visualized + 4 date options + best time to book (45–75 days ahead) |
| [Hotels — Ranked](hotels.html) | 7 hotels, verified queen+ & private bath, amenities, 7-night totals, official booking links |
| [Michelin Restaurants](restaurants.html) | 14 bookable starred (plus Bib), star vs guide-listed, cost for 2 totals, hours/days, YouTube/TikTok/IG |
| [Activities ≤1h](activities.html) | 10 sights, hours/days/exceptions, entry for 2, social links, ≤1h proof |
| [Transport — 1h Proof](transport.html) | Door-to-door Metro times from The Bund base, isochrone table with shmetro.com sources |
| [Budget — Totals for 2](budget.html) | Hotel 7n + Michelin dinner for 2 combined totals + cheapest booking windows |
| [Q&A Gaps](questions.html) | 12 must-answer questions before booking — what we have vs. need, with “how to discover” links |
| [Suggestions — review-only](suggestions.html) | 8 improvement proposals (map, price-watch bot, wizard, etc.) — approve before we build |
| [Sources & Verification](sources.html) | Bibliography — every fact re-checkable |
| [Flagged for Review](flagged.html) | Irregularities log (needs review — does not block publish) |
| [Methodology](methodology.html) | How we verify line-by-line, surrogate pricing protocol, 1-hour measurement |

## Verification promise
- Every table row has a **Source** column linking to an official site: `guide.michelin.com`, hotel official (Peninsula, Hilton, Hyatt), attraction official (`orientalpearltower.com`, `shanghaimuseum.net`), or `shmetro.com`.
- If a value couldn't be confirmed, the cell is blank + flagged <span style="background:#fffbeb;border:1px solid #fde68a;padding:2px 6px;border-radius:999px">unverified</span>. No invented prices/hours.
- 2027 hotel inventory is mostly **unpublished** (24-month search limit) → we show **surrogate** totals from parallel 2026 dates, labeled `surrogate` with exact check date + re-check instructions. See `methodology.html` and `flagged.html#pricing`.

## Coordination
See [`COORDINATION.md`](COORDINATION.md) — shared task board for parallel agent sessions (status, owner, file scopes, log). This session (`arena/8205b531-chinafun3`) claimed T01–T11; small frequent commits; `git pull --rebase` before push.

## Local preview
```bash
python3 -m http.server 8000 --bind 0.0.0.0
# open http://localhost:8000/index.html
# or start preview: start_process name Website command "python3 -m http.server 8000"
```

## GitHub Pages publishing
- Current Pages source: `main` branch `/` (see `gh api repos/kanlerxz87-cyber/ChinaFun3/pages`).
- This branch's site will go live after PR merge to `main` (or after `gh api repos/.../pages` source is switched to `arena/8205b531-chinafun3` — admin permission confirmed).

---
Built 2026-11-25 • Shanghai focus • Mobile-friendly • No hallucinations • All sources linkable
