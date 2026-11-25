# COORDINATION — shared task board

Format: each task lists status, owner session, and files it touches.
Statuses: `unclaimed` · `in progress` · `done` · `needs review` (published on the Flagged for Review page; does not block).

Session ID used below: `3c3c3c5e` (branch `arena/3c3c3c5e-chinafun3`).
Note: the branch-naming convention `session-<id>/<task>` conflicts with the platform rule to work only on the assigned branch; this session follows the assigned branch.

## Task board

| ID | Task | Status | Owner | Files touched |
|---|---|---|---|---|
| T0 | Repo review + irregularities | done | 3c3c3c5e | `README.md`, `docs/data/irregularities.json`, `docs/repo-review.html` |
| T1 | Entry rules + 2027 holiday calendar | done | 3c3c3c5e | `docs/data/entry.json`, `docs/data/calendar.json`, `docs/entry-and-calendar.html` |
| T2 | Michelin restaurants — Shanghai cluster | done (partial, see log) | 3c3c3c5e | `docs/data/michelin.json`, `docs/michelin-shanghai.html` |
| T3 | Hotels (price / location / amenities) | needs review (blocked by data access) | 3c3c3c5e | `docs/data/hotels.json`, `docs/hotels.html` |
| T4 | Activities (hours, tickets, social links) | done (partial, see log) | 3c3c3c5e | `docs/data/activities.json`, `docs/activities.html` |
| T5 | Questions, suggestions, flagged review | done | 3c3c3c5e | `docs/data/questions.json`, `docs/data/suggestions.json`, `docs/review.html` |
| T6 | Site shell, landing page, executive summary | done | 3c3c3c5e | `docs/index.html`, `docs/assets/*`, `docs/.nojekyll` |
| T7 | Integration: merge, re-verify, publish Pages | in progress | 3c3c3c5e | `docs/**`, `COORDINATION.md` |

Shared outputs (`docs/index.html` navigation, combined data) are owned by T7 (integration).

## Log

- **2026-11-25 · 3c3c3c5e** — Read COORDINATION.md (did not exist) and created it. Claimed T0–T7 above; this session is the only active session on the repo, so no conflicts occurred.
- **Sources consulted (all retrieved 2026-11-25):**
  - State Council General Office notice on 2027 holidays (gov.cn, 国办发明电〔2026〕10号): https://www.gov.cn/zhengce/content/202611/content_7085101.htm
  - NIA — Visa-Free Transit Policies (57 countries incl. US; 65 ports; 10 days): https://en.nia.gov.cn/n147418/n147463/c183412/content.html
  - NIA — Regional Visa-Free Entry Policies (Hainan 30-day list includes US): https://en.nia.gov.cn/n147418/n147463/c180637/content.html
  - MICHELIN Guide press release, Shanghai/Jiangsu/Zhejiang 2026 (10 Apr 2026): https://www.michelin.com/en/publications/products-and-services/michelin-guide-shanghai-jiangsu-zhejiang
  - Shanghai Museum official notice (25 Aug 2025): https://www.shanghaimuseum.net/mu/frontend/pg/m/article/id/I00004797
  - Yu Garden official visitor information: https://www.yugarden.com.cn/page/articleView/message.html
- **Verification performed:** holiday dates and make-up days were checked against the gov.cn text; weekdays were checked with `date` (2027-02-15 is a Monday; 2027-02-14 is a Sunday, matching the official make-up day). Michelin star status was checked against the official press release text. Shanghai Museum and Yu Garden hours were checked against their own sites.
- **Could not verify (blocked):** michelin.com restaurant pages (`guide.michelin.com`) returned fetch errors; hotel booking sites are outside the sandbox's allowed hosts, so Feb 2027 room rates cannot be checked from here; social-media accounts were not searched exhaustively.
- **Irregularities:** see `docs/repo-review.html` and `docs/data/irregularities.json` (T0).
- **Handoff:** none needed.
- **Build and checks (T6/T7):** site is static HTML/CSS/JS in `docs/` (no build step). Checks run: every internal `href` and `data-src` resolves; all 8 JSON files parse; `app.js` passes a syntax check; the renderer was run against every data file in a headless DOM (row and unverified counts matched the data). Local server tested with HTTP 200 on all pages and data files. No broken internal links.
- **Task results:** T1 — 2027 holiday dates verified against the gov.cn notice; 15 Feb 2027 = Monday. T2 — 16 starred Shanghai restaurants verified against the official release; 64 unverified cells (hours, prices, social links, guide links) left blank. T4 — Shanghai Museum and Yu Garden verified against official sites; ticket/social blanks flagged. T3 — no hotel rows; room/price data not reachable. T5 — 11 questions, 8 suggestions (none implemented).
