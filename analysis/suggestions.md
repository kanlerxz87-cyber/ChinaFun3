# Suggestions for Improving Decision Quality

**Status:** Suggestions only — no changes implemented without user review.  
**Session:** c8dcd263

## 1. Resolve Decision-Critical Inputs First

| Suggestion | Why | Expected outcome | Effort |
|---|---|---|---|
| Confirm destination city (Shanghai proposed) | All data depends on city | Prevents wasted research | Low |
| Confirm exact dates and trip length (7 nights Feb 15-22 2027 proposed) | Pricing/availability/hours depend on dates | Enables real quotes | Low |
| Set budget ceiling (total and/or nightly) | Needed to rank hotels meaningfully | Narrows options | Low |
| Define "Michelin rated" scope | Starred vs Bib Gourmand vs Selected changes ranking | Clear restaurant universe | Low |

## 2. Improve Pricing Verification

| Suggestion | Why | How | Priority |
|---|---|---|---|
| Capture date-stamped hotel quotes | 2027 pricing is currently unverified | For each candidate: check official hotel site + Booking + Trip.com for same room/cancellation; save screenshot/PDF and URL with access date | Critical |
| Track price changes over 2-4 weeks | "Best time to book" is unknown | Set price alerts (Google Hotels, Kayak, Hopper if used) and log observed prices/date | High |
| Confirm total 7-night price including taxes/fees | Nightly "from" rates often exclude taxes/service fees | Record total checkout price, currency, cancellation policy, breakfast inclusion | Critical |
| Confirm restaurant per-couple cost | Michelin ¥ symbol is coarse | Check official menus/tasting menu prices; record date; convert to CNY/USD with date-stamped FX rate | High |

## 3. Improve Location/Transit Accuracy

| Suggestion | Why | How | Priority |
|---|---|---|---|
| Verify <=1hr subway/bus claim per hotel-restaurant pair | Estimates may be wrong at peak times | Use Amap or Google Maps transit directions for departure time (e.g., 18:00 weekday) and record route/duration | High |
| Map Michelin clusters visually | Easier decision-making | Add map layer with hotel pins and restaurant pins; color by star/distinction | Medium |
| Include walking time to nearest metro | Last-mile affects 1-hour rule | Record nearest station, line, walking minutes from official map/hotel page | Medium |

## 4. Improve Data Completeness

| Suggestion | Why | How | Priority |
|---|---|---|---|
| Collect official hours/open days for every venue | User requested; many missing | Visit each restaurant/activity official site or Michelin page; record regular hours + holiday exceptions | High |
| Collect official social links for every venue | User requested YouTube/TikTok/Instagram where possible | Search "[venue] official Instagram/TikTok/YouTube"; verify account authenticity; prefer official website links | Medium |
| Add reservation links/policies | Michelin restaurants often require reservations | Capture official reservation channel (phone, website, Michelin/partner) | Medium |
| Add activity options | Activities unspecified in request | Propose 5-8 Shanghai activities near cluster with official links, hours, cost, transit time | High |

## 5. Improve Site / UX

| Suggestion | Why | How | Priority |
|---|---|---|---|
| Add filters/sort on tables | Easier mobile decision-making | Client-side sort by price, stars, transit time, district | Medium |
| Add "Verified/Unverified" badges | Prevents trust errors | Color-coded status column + legend on every page | High (partially planned) |
| Add comparison view for 2-3 hotels | Supports final choice | Side-by-side cards with key metrics | Medium |
| Add print/PDF export | Useful for travel | Simple print CSS | Low |
| Add date-stamped "last verified" per row | Data stales quickly | Include `verified_on` field in data model | High |

## 6. Governance / Verification

| Suggestion | Why | How | Priority |
|---|---|---|---|
| Run a final integration verification pass | Multiple sessions/edits may introduce errors | Check every row has source link; re-open links; confirm no hallucinated values | Critical |
| Add CI link checker | Broken links degrade trust | GitHub Actions link checker on PRs | Medium |
| Keep raw source snapshots | Pages change | Save archived URLs/screenshots in `research/snapshots/` when possible | Medium |
| Separate "fact" vs "estimate" columns | Avoids mixing verified and inferred data | Never place estimate in a verified fact column; label explicitly | Critical |
