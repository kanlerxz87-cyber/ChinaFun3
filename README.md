# China, for two

An evidence-led, mobile-friendly static trip-planning dashboard for two adults traveling between **15 February and 23 March 2027**.

**Site:** https://kanlerxz87-cyber.github.io/ChinaFun3/

## Pages

- Overview / executive summary
- Four hotel candidates
- Seven MICHELIN dining records with separate starred, Bib Gourmand and Selected labels
- Five activities
- Proposed seven-night itinerary
- Six dated Peninsula hotel searches and transparent seven-night calculations
- Decision questions and optional locally saved suggestion reviews
- Flagged for Review (13 open research issues)
- Official-source register, media links and method

## Important boundaries

This is a research snapshot dated **25 November 2026**, not a booking service or a completed cheapest-trip optimization. No reservations, payments or inquiries using traveler details were made.

The six Peninsula searches provide real official nightly inputs, with a published surcharge used to calculate seven-night totals. They are **not final checkout quotations**. Three other hotel totals, timed public-transport coverage ranks, strict private-bathroom confirmations and several future schedules remain unverified. Unknown data is null, not fabricated or zero. See [verification audit](research/verification.md) and [release notes](research/release.md).

The preferred 15–18 February window is shorter than one week. The proposed 15–22 February stay is an explicitly labeled interpretation, not a confirmed traveler choice.

## Development

Runtime: plain HTML/CSS/JavaScript, no CDN assets, no backend and no framework. Python 3 generates the static pages. Node dependencies are only for browser testing.

```sh
python scripts/build.py
python -m unittest discover -s tests -v
python -m http.server 3000 --bind 0.0.0.0
```

Optional browser tests (with the server already running):

```sh
npm ci
npm run test:browser
```

The test browser comes from the npm-packaged `@sparticuz/chromium`; no external browser download is needed. Browser screenshots/reports are ignored in `test-results/`.

## Editing research

`data/trip.json` is the published dataset. `scripts/seed_data.py` is its editorial seed, containing source transcription and clearly labeled follow-up checks; rerun it only intentionally when updating facts. Then run `python scripts/build.py` to regenerate pages and `data/hotels.csv`. Never edit generated HTML as the primary source.

Each factual row needs official source IDs. Social media is an inspiration layer only, not evidence for current prices, hours or Michelin awards. Changing a field requires checking its official source and updating its evidence note/date. Recommendations are clearly distinguished from confirmed facts.

Local shortlist/suggestion preferences stay in browser localStorage; export is optional. No analytics, advertising, embedded social trackers or data collection.

## Coordination and deployment

Read [COORDINATION.md](COORDINATION.md) before changing files. This Arena session uses fixed branch `arena/a9dba5c2-chinafun3`; no alternative branch is created. Repository-generated HTML is committed so GitHub Pages can publish directly from the working branch's root with `.nojekyll`. CI validates the build and tests; it does not claim to reverify third-party travel facts.
