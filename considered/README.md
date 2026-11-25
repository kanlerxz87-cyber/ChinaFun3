# China, considered · ChinaFun3

A mobile-friendly, source-linked travel planning dashboard for two adults, for a 1–2 week trip within **15 February–23 March 2027**.

**Site:** https://kanlerxz87-cyber.github.io/ChinaFun3/considered/

## What is delivered

Nine static pages: executive overview, hotel candidates, Michelin dining, activities, proposed itinerary, dates/costs, Flagged for Review, suggestions/questions, and source register. Searchable tables become labeled cards on phones. Dining distinction filters, print/PDF, and optional browser-local suggestion shortlists work without a backend. Findings are readable without JavaScript.

The research is a **bounded Shanghai baseline**, not a China-wide comparison or a final bookable vacation. Includes three hotel candidates, six Michelin restaurant entries (five starred, one Selected without a star), two Shanghai Museum branches, three date-specific official Langham search attempts, and a proposed 15–22 February itinerary. The preference 15–18 February alone is only three hotel nights.

## Critical limitations — do not treat these as solved

- No final tax-inclusive seven-night hotel quote; no verified cheapest stay week or best future booking day.
- No measured complete ≤60-minute public-transit hotel/restaurant matrix, so no invented ranking or reachable-restaurant counts.
- Some meal totals, social previews, hours, 2027 exceptions and personal travel-eligibility facts remain unknown.
- T’ang Court publishes CNY 888 lunch / CNY 2,288 all-day for two, including tax and service; not a guarantee of future price or availability.
- Radisson spa closure overlaps entire travel window. Schedule conflicts and website redirects are published on `review.html`.

Each table row has an official-source link. Missing factual values are `null`, rendered empty with an adjacent Unverified flag. Suggestions are proposals, not silently implemented future services. No reservations, payments, or automated monitoring.

## Source and verification files

- `research/data.json` — structured facts, source register and observed fields, checked 25 November 2026 UTC.
- `research/README.md` — repository audit, research scope, failed checks, exclusions and irregularities.
- `COORDINATION.md` — ownership, coordination log, test/deployment status.
- `scripts/build.py` — deterministic, dependency-free HTML generator.

## Develop / test

Python 3.10+ is sufficient for the site build and offline tests:

```sh
python3 scripts/build.py
python3 -m unittest discover -s tests -v
python3 -m http.server 8000 --bind 0.0.0.0
```

No runtime npm packages, API keys, remote fonts, analytics or external assets. All paths are relative for GitHub project Pages. Generated HTML is committed. `node --check assets/app.js` checks syntax.

Optional real-browser tests (Node 22+; dev dependencies only):

```sh
npm ci
# Start the Python server above in another process, then:
npm run test:browser
```

Browser tests exercise all nine pages at 390/768/1440px, viewport overflow, search/filter/no-results, suggestion persistence/reset, disclosure and runtime errors. The sandbox's CDN access prevented Playwright's usual browser download; Chromium was obtained through the npm package. Minimal Linux installations may need NSS libraries; the bundled `al2023.tar.br` can be inflated by `@sparticuz/chromium` (the test harness does this) if those libraries are absent. Screenshots are scratch artifacts under ignored `.cache/`.

Offline tests check all internal links/anchors and official-source presence per row, schema, null-value safeguards, calendar arithmetic, and reproducible generation. They do not prove external future availability or a complete live-link crawl.

## Publication

GitHub Pages remains on the existing `main` branch at root. The settings API denied updates (HTTP 403). This independent dashboard lives under `considered/` and is integrated through a pull request from the fixed session branch; no direct push to main. Root and docs dashboards from parallel sessions are preserved unchanged and not endorsed as verified by this snapshot. Build/test commands are run from the repository root; they target considered/ only. The verification workflow checks the additional dashboard, not the other sessions’ datasets.

## Parallel publication

The repository was empty at initial inspection; concurrent sessions published root and docs sites during this research. Their files have been preserved. This dashboard was relocated intact to considered/ to avoid overwriting their owned scopes. Research/source files remain at repository-root research/. The original session board is archived as considered/COORDINATION-session.md; the current merged board is ../COORDINATION.md.
