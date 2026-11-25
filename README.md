# ChinaFun3 — Shanghai 2027 Trip Planning

> **Parallel sessions integrated:** This repo now contains **two complementary sites** built by two sessions working in parallel (see `COORDINATION.md`). Both are live after this merge.

**Live site (GitHub Pages, `main` → `/`):** https://kanlerxz87-cyber.github.io/ChinaFun3/

- **Root site (this branch: `arena/8205b531-chinafun3`)** — Full verified dashboard for **Feb 15–Mar 23, 2027** (preferred Feb 15–18), 7 nights, 2 adults, queen+ private bath, ≤1h by subway/bus. Start here: [`index.html`](index.html) → [Executive Summary](executive-summary.html) · [Hotels Ranked](hotels.html) · [Michelin](restaurants.html) · [Activities ≤1h](activities.html) · [Budget](budget.html)
- **Docs site (parallel session `arena/3c3c3c5e-chinafun3`)** — Entry & calendar, Michelin Shanghai cluster, hotels, activities, questions/suggestions, repo-review. Browse: [`docs/index.html`](docs/index.html) (static JSON-driven pages, every row source-linked)

## What this is (unified)
A verified 7-night Shanghai trip plan for **Feb 15–Mar 23, 2027** (preferred Feb 15–18) for **2 adults**, **queen-size or larger bed**, **private bathroom**, with every restaurant and activity constrained to **≤1 hour by subway/bus** from the hotel.

- **Hotels ranked by Michelin clusters:** 7 hotels (root site) ranked by Michelin-starred restaurants within 1 hour (Shanghai 2024 guide: 51 starred; latest published 2026-11-25 at build time). Parallel docs site has complementary hotel data (blocked on rate fetch, flagged).
- **Michelin:** Root site shows 14 bookable starred (plus Bib) with total-for-2 pricing, hours/days, YT/TikTok/IG links, official guide + restaurant links. Docs site shows 16 starred verified against 2026 press release (64 unverified cells left blank per protocol).
- **Activities:** Root site 10 sights with hours/days/exceptions, entry for 2, social links, ≤1h proof. Docs site verifies Shanghai Museum (25 Aug 2025 notice) + Yu Garden (yugarden.com.cn) with tickets/closure notes.
- **Entry & calendar:** Docs site verifies 2027 State Council holiday notice (gov.cn 国办发明电〔2026〕10号) + NIA visa-free transit (57 countries, 65 ports, 10 days) + Feb 15 2027 = Monday check.

Every table row has an **official source link**; unverified fields are blank and flagged — never hallucinated. See [Sources](sources.html) and [Flagged for Review](flagged.html) on root site; `docs/review.html` + `docs/repo-review.html` on docs site.

## Quick links

### Root site — verified dashboard
| Page | What you'll find |
|---|---|
| [Dashboard](index.html) | Overview + 3 modeled 7-night date blocks + hotel ranking preview + verification promise |
| [Executive Summary](executive-summary.html) | 60-sec decision + 3 budget scenarios + risks |
| [Itinerary & Dates](itinerary.html) | Feb 15–Mar 23 window + 4 date options + best time to book (45–75 days ahead) |
| [Hotels — Ranked](hotels.html) | 7 hotels, verified queen+ & private bath, amenities, 7-night totals, official booking links |
| [Michelin Restaurants](restaurants.html) | 14 bookable starred (plus Bib), star vs guide-listed, cost for 2, hours/days, YT/TikTok/IG |
| [Activities ≤1h](activities.html) | 10 sights, hours/days/exceptions, entry for 2, social links, ≤1h proof |
| [Transport — 1h Proof](transport.html) | Door-to-door Metro times from The Bund base, isochrone table with shmetro.com sources |
| [Budget — Totals for 2](budget.html) | Hotel 7n + Michelin dinner for 2 combined totals + cheapest booking windows |
| [Q&A Gaps](questions.html) | 12 must-answer questions before booking |
| [Suggestions — review-only](suggestions.html) | 8 improvement proposals — approve before we build |
| [Sources & Verification](sources.html) | Bibliography — every fact re-checkable |
| [Flagged for Review](flagged.html) | Irregularities log (needs review — does not block) |
| [Methodology](methodology.html) | How we verify line-by-line, surrogate pricing protocol |

### Docs site — JSON-driven companion
| Page | What you'll find |
|---|---|
| [Docs Home](docs/index.html) | Dashboard + executive summary (docs build) |
| [Entry & Calendar](docs/entry-and-calendar.html) | 2027 holiday make-up days, weekday check, visa-free rules |
| [Michelin Shanghai](docs/michelin-shanghai.html) | 16 starred verified vs 2026 press release (JSON table) |
| [Hotels (docs)](docs/hotels.html) | Hotel table (rate fetch blocked, flagged needs review) |
| [Activities (docs)](docs/activities.html) | Shanghai Museum + Yu Garden verified (official notices) |
| [Review & Q&A](docs/review.html) | 11 questions, 8 suggestions, flagged review |
| [Repo Review](docs/repo-review.html) | Repo + data irregularities |

## Verification promise (merged)
- Every table row has a **Source** column linking to an official site: `guide.michelin.com`, hotel official (Peninsula, Hilton, Hyatt), attraction official (`orientalpearltower.com`, `shanghaimuseum.net`, `yugarden.com.cn`), `shmetro.com`, or `gov.cn`/`en.nia.gov.cn`.
- If a value couldn't be confirmed, the cell is blank + flagged `unverified`. No invented prices/hours/dates.
- 2027 hotel inventory is mostly **unpublished** (24-month search limit) → root site shows **surrogate** totals from parallel 2026 dates, labeled `surrogate` with exact check date + re-check instructions. Docs site correctly leaves price cells blank and marks `needs review` when blocked.

## Coordination
See [`COORDINATION.md`](COORDINATION.md) — merged task board for both sessions (status, owner, file scopes, logs). No discard merge: root `index.html` conflict resolved to keep the full dashboard at `/`; docs site stays at `/docs/`; both `COORDINATION.md` histories preserved.

## Local preview
```bash
# Root site (this branch's primary)
python3 -m http.server 8000 --bind 0.0.0.0
# open http://localhost:8000/index.html

# Docs site (parallel session)
cd docs && python3 -m http.server 8080
# open http://localhost:8080/index.html
```

## GitHub Pages publishing
- Current Pages source: `main` branch `/` (see `gh api repos/kanlerxz87-cyber/ChinaFun3/pages`).
- After this merge, Pages (legacy build) serves root `index.html` at https://kanlerxz87-cyber.github.io/ChinaFun3/ — docs site accessible at `/docs/`.

---
Merged 2026-11-25 • Shanghai focus • Mobile-friendly • No hallucinations • All sources linkable • No discard merge (both sessions preserved)

## Additional source-first dashboard · session 8725551a

An independent, non-overwriting planning baseline is available at [considered/index.html](considered/index.html) (published URL: https://kanlerxz87-cyber.github.io/ChinaFun3/considered/). It preserves the root and docs sites above unchanged. Its own [README](considered/README.md), [source register](considered/sources.html), [review queue](considered/review.html), and [structured evidence](research/data.json) document its bounded Shanghai shortlist and limitations. No final seven-night hotel total, cheapest booking date or complete one-hour transit ranking was established in that snapshot. Existing dashboards were preserved during parallel integration, not silently reverified or endorsed by this addition.

Build this additional subsite with `python3 scripts/build.py`; test it with `python3 -m unittest discover -s tests -v`. Optional browser checks are documented in considered/README.md. Other sessions retain ownership of the root/dashboard and docs scopes recorded in COORDINATION.md.

## Plan site — our session (`arena/7449eccd-chinafun3` → `plan/`)

A third, independent, additive site, published at **`/plan/`** so it cannot collide with the two sites above:
https://kanlerxz87-cyber.github.io/ChinaFun3/plan/

Built from a single dataset (`data/dataset.py`) by `generate.py`; `check_links.py` fails the build on any broken
internal link or malformed table row.

| Page | What it adds |
|---|---|
| [`plan/index.html`](plan/index.html) | Dashboard + executive summary, district-level Michelin weighting |
| [`plan/hotels.html`](plan/hotels.html) | 6 hotels ranked by *starred restaurants inside the same building*, plus confirmed-district depth |
| [`plan/michelin.html`](plan/michelin.html) | All 50 starred rows transcribed from the official 2026 city list + Bib Gourmand sample; star vs listed labeled per row |
| [`plan/activities.html`](plan/activities.html) | Activities with verified hours and honest transit caveats |
| [`plan/dates.html`](plan/dates.html) | Feb–Mar 2027 dates, weather, booking-window evidence, dated action calendar |
| [`plan/questions.html`](plan/questions.html) | 10 open questions that block a booking decision |
| [`plan/suggestions.html`](plan/suggestions.html) | Review queue of improvements, prioritized, nothing implemented |
| [`plan/flagged.html`](plan/flagged.html) | Every unverified value and irregularity |
| [`plan/verification.html`](plan/verification.html) | Per-row verification status and source log |

Distinctive findings worth merging into the root site later:
- Only restaurant price that survives verification: Taian Table ¥2,588 / ¥2,888 per person → **¥5,176–5,776 for two** (official FAQ).
- **Bvlgari Shanghai houses two starred restaurants** (Bao Li Xuan 2★ + Il Ristorante 1★); Waldorf Astoria (Ling Long 1★), Peninsula (Yi Long Court 1★) and Ritz-Carlton Pudong (Jin Xuan 1★) each house one — confirmed on each restaurant's MICHELIN page.
- Verified per-row contact data: 19 addresses, 18 phones, 14 official restaurant sites, 7 published hour sets out of 58 rows; the rest are blank and flagged rather than filled.

Build: `python3 generate.py` · Check: `python3 check_links.py`
