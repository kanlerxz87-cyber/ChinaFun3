# ChinaFun3 — Verified Feb–Mar 2027 China MICHELIN Trip Planner

An evidence-verified, mobile-friendly multi-page GitHub Pages travel dashboard built for **2 adults** planning a **1–2 week MICHELIN culinary & cultural trip to China** between **February 15 and March 23, 2027**.

> **Live GitHub Pages URL (after merging to `main`):** [`https://kanlerxz87-cyber.github.io/ChinaFun3/`](https://kanlerxz87-cyber.github.io/ChinaFun3/)

---

## Dashboard Pages

| Page | File | What's Inside |
|---|---|---|
| **Executive Summary & Overview** | `index.html` | Recommended 7-night & 14-night itineraries, verified 2-adult cost snapshots, 2027 official public holidays & NIA 240-hour visa-free transit rules, Feb–Mar climate normals, and all 12 active China & SAR MICHELIN Guide clusters ranked. |
| **MICHELIN Dining Directory** | `pages/restaurants.html` | 29 audited restaurants (**16 Shanghai**, **13 Beijing**) verified against `guide.michelin.com` and official venue menus. Strictly separates **MICHELIN Starred (3★/2★/1★)** from **MICHELIN Guide Listed (Bib Gourmand / Selected)**, with live city/distinction/price filters, verified social links, and bilingual address cards. |
| **Hotels & Booking Timing** | `pages/hotels.html` | 10 ranked hotels (**5 Shanghai**, **5 Beijing**) meeting all hard requirements (private en-suite bath, Queen/King bed, 100% ≤1-hr Metro reachability to audited MICHELIN restaurants), live verified **Feb 22–Mar 1, 2027** 7-night tax-inclusive totals, live 4-week seasonal price proof, and KAYAK May 2026 booking-timing guidance. |
| **Activities & Landmarks** | `pages/activities.html` | 16 verified attractions (**8 Shanghai**, **8 Beijing**) with official winter off-season (Feb–Mar) 2-adult admission totals, Monday-closure filter, passport/booking rules, transit times, and official municipal/museum references. |
| **Planning & Roadmap** | `pages/planning.html` | 7 prioritized Missing Info / Decision Questions (`Q-01`–`Q-07`), 4-phase Discovery & Booking Plan (Nov 2026 → Feb 2027), and v2 Site Improvement Backlog (`IMP-01`–`IMP-05`). |
| **Flagged for Review** | `pages/review.html` | Full transparency audit register (`FLG-01`–`FLG-10`) plus an auto-synced granular table of every unverified/blank restaurant and activity field across all datasets. |

---

## Verified Data Architecture (`/data`)

All dashboard views dynamically load static, schema-validated JSON datasets verified on **2026-11-25**:

- `data/calendar-and-clusters.json` — 2027 State Council holidays, Lantern Festival, Two Sessions window, 240-hr visa-free transit, climate normals, and all 12 active MICHELIN Guide China & SAR clusters.
- `data/restaurants.json` — 29 audited Shanghai & Beijing MICHELIN restaurants with verbatim official addresses, phones, official menu totals (where published), hours/exceptions, and verified social media URLs.
- `data/hotels.json` — 10 curated hotels with live Feb–Mar 2027 7-night quotes, direct SynXis rates (The PuLi & The PuXuan), 4-week seasonal benchmark pricing, and door-to-door MICHELIN transit breakdowns.
- `data/activities.json` — 16 verified attractions with official off-season 2-adult admission, weekly closures, and official municipal links.
- `data/governance.json` — Executive summary, decision questions, discovery timeline, site improvements, and audit flags.
- `COORDINATION.md` — Shared task board and full primary-source verification log.

---

## Verification & Zero-Guesswork Standard

- Every numeric price, schedule, address, and distinction is backed by a direct clickable primary source (`guide.michelin.com`, `english.beijing.gov.cn`, `english.shanghai.gov.cn`, `yugarden.com.cn`, `shanghaimuseum.net`, official restaurant menu PDFs, `be.synxis.com`, and live date-bound `trip.com` queries).
- Any field that could not be confirmed on an official primary source (such as non-published tasting menu prices or WeChat-only schedules) is intentionally left blank (`—`) and logged on `pages/review.html`.

---

## Local Preview

```bash
python3 -m http.server 8000 --bind 0.0.0.0
# Open http://localhost:8000/
```
