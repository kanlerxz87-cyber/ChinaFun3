# ChinaFun3 — Shanghai trip plan (15–22 Feb 2027, 2 adults)

A verified, source-linked research site for a 7-night Shanghai trip built around MICHELIN dining:
hotels ranked by starred restaurants within reach, star vs. Guide-listed kept strictly separate,
costs for two adults, opening hours and closures, and an explicit list of what is still unverified.

**Live site:** https://kanlerxz87-cyber.github.io/ChinaFun3/

## Pages
| Page | Contents |
|---|---|
| `index.html` | Dashboard + executive summary |
| `hotels.html` | Hotel ranking, beds/baths, booking links |
| `michelin.html` | All 50 starred rows + Bib Gourmand sample, costs, hours, social links |
| `activities.html` | Activities with verified hours, transit notes, day trips |
| `dates.html` | Feb–Mar 2027 dates, weather, booking-window evidence + dated action calendar |
| `questions.html` | 10 open questions that block a booking decision |
| `suggestions.html` | Review queue of site improvements, with priority and effort |
| `flagged.html` | Every unverified value and irregularity |
| `verification.html` | Method + source log per row |

## How it is built
- `data/dataset.py` — the single source of truth. Empty strings mean **not verified**; nothing is estimated.
- `generate.py` — renders every page from the dataset. `python3 generate.py`
- `check_links.py` — fails if any internal link or table row is malformed. `python3 check_links.py`
- `COORDINATION.md` — shared task board, verification log and handoff notes for parallel sessions.

## Rules this repo follows
1. Every table row links to an official source.
2. A value is published only if it was read on that official page; otherwise it is blank and flagged.
3. Hotel rates are never estimated — February 2027 prices require the live booking engine, linked per row.
4. Starred vs. Bib Gourmand vs. Selected is labelled per restaurant, never merged.
5. Nothing is marked verified without the source link in the same row.

## Publishing
GitHub Pages serves the repository root of `main`. Changes land via pull request from the working branch.
