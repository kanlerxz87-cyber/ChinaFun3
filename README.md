# ChinaFun3 — Shanghai Trip Planning (Draft)

Verified-first trip planning workspace for a couple (2 adults) planning a Shanghai trip. This draft prioritizes official sources, flags unverified data, and avoids hallucinated values.

## Live Dashboard (GitHub Pages)

Static site files are in the repo root:

- [Overview](index.html)
- [Hotels](hotels.html)
- [Michelin Restaurants](restaurants.html)
- [Activities](activities.html)
- [Plan, Gaps & Suggestions](plan.html)
- [Sources & Verification](sources.html)

> Enable GitHub Pages for this repository (Settings → Pages → Deploy from branch, root) to publish the dashboard.

## Key Constraints (from request)

- Destination: China (Shanghai proposed; **unconfirmed**).
- Dates: between 2027-02-15 and 2027-03-23; preferred 2027-02-15 to 2027-02-18. Draft proposes **7 nights, 2027-02-15 check-in to 2027-02-22 check-out** (**unconfirmed**).
- Travelers: 2 adults; 1 room; private bathroom; queen bed or larger/equivalent.
- Hotel ranking: consider Michelin access within ~1 hour by subway/bus.
- Verification: official sources only; no hallucinations; unverified values left blank/flagged.

## Repository Layout

```text
.
├── COORDINATION.md              # Shared task board / verification log
├── README.md
├── index.html                   # Dashboard landing page
├── hotels.html                  # Hotel comparison table
├── restaurants.html             # Michelin restaurant table
├── activities.html              # Proposed activities table
├── plan.html                    # Executive summary, questions, gaps, suggestions
├── sources.html                 # Source log and flagged review items
├── assets/style.css             # Shared site styles
├── data/
│   ├── hotels.json
│   └── restaurants.json
├── research/
│   └── sources.md
└── analysis/
    ├── executive-summary.md
    ├── questions-and-gaps.md
    └── suggestions.md
```

## Verification Status

This is a **partially verified draft**. Confirmed items include MICHELIN Guide distinctions/details fetched from official MICHELIN pages on 2026-11-25. Unverified/high-risk items include:

- 7-night hotel totals for 2027-02-15→2027-02-22 (no date-stamped checkout quote).
- "Cheapest upcoming time to book" (no definitive official source).
- Complete hours/open days/exceptions for every venue.
- Exact per-couple restaurant menu totals (estimates labeled).
- Transit <=1 hour route verification at travel time.
- Official social links for every venue.
- Room-level amenity confirmation (private bathroom, queen+ bed).

See [sources.html](sources.html) and [COORDINATION.md](COORDINATION.md).
