# ChinaFun3 — China trip planning

Planning site and data for a 2-adult trip to China (window: 15 Feb – 23 Mar 2027).

- **Live site:** GitHub Pages from the repo root on `main`; the root `index.html` forwards to `docs/index.html` (Pages source is set to `/`, and changing it needs admin rights).
- **Data:** `docs/data/*.json` — every table row carries an official source link, or is flagged *Unverified* and left blank.
- **Pages:** Home (dashboard + executive summary), Entry & calendar, Michelin (Shanghai), Hotels, Activities, Questions & suggestions, Repo review.
- **Coordination:** `COORDINATION.md` is the shared task board, with sources, verification notes and irregularities per task.

Run locally: `cd docs && python3 -m http.server 8080` then open http://localhost:8080 (the pages load JSON, so open them over HTTP, not as files).
