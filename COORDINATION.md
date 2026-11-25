# ChinaFun3 — Shared Task Coordination Board

> **Purpose:** Shared coordination log for verifying travel data, auditing sources, and building the ChinaFun3 Trip Planning GitHub Pages dashboard.
> **Branch Policy Note:** This Arena session is bound to branch `arena/256b850d-chinafun3` (branched from `main` at `fa1f9fa`). All commits and pushes from this session target `arena/256b850d-chinafun3`.
> **Verification Rule:** No cell or claim may be marked `verified` without direct confirmation from an official, trusted source (linked). Any unconfirmable field is left blank in tables and logged on the **Flagged for Review** page (`needs review` status does not block other work).

---

## Active Sessions

| Session ID | Branch | Started (UTC) | Scope | Status |
|---|---|---|---|---|
| `session-256b850d` | `arena/256b850d-chinafun3` | 2026-11-25 | Full initial build, verification, and integration (no other active sessions found in repo) | Active |

---

## Task Board

| Task ID | Task Description | Status | Owner Session | File Scope | Last Updated (UTC) |
|---|---|---|---|---|---|
| `T-00` | Repo audit & `COORDINATION.md` initialization | `done` | `session-256b850d` | `COORDINATION.md` | 2026-11-25 |
| `T-01` | Verify 2027 China travel calendar (Spring Festival / Lantern Festival, official public holidays, weather, booking windows) & city-level Michelin Guide China cluster counts | `done` | `session-256b850d` | `data/calendar-and-clusters.json` | 2026-11-25 |
| `T-02` | Research & verify Michelin-starred and Michelin Guide-listed restaurants (Shanghai & Beijing clusters), total pricing for 2 adults, hours/exceptions, official links, and social media links (YouTube/TikTok/Instagram) | `done` | `session-256b850d` | `data/restaurants.json` | 2026-11-25 |
| `T-03` | Research & verify hotels (private bath, queen+ bed, amenities, transit ≤1 hr to Michelin clusters), rank by Michelin reachability, verify 7-night pricing for Feb–Mar 2027 dates & optimal booking window | `done` | `session-256b850d` | `data/hotels.json` | 2026-11-25 |
| `T-04` | Research & verify activities & attractions within ≤1 hr transit of hotel clusters, official hours/exceptions, 2-adult admission prices, official links, and social media links | `done` | `session-256b850d` | `data/activities.json` | 2026-11-25 |
| `T-05` | Compile Executive Summary, Missing Info / Decision Questions & Discovery Plan, Site Improvement Suggestions, and Flagged for Review audit register | `done` | `session-256b850d` | `data/governance.json` | 2026-11-25 |
| `T-06` | Build mobile-friendly GitHub Pages dashboard (landing page + category subpages, searchable/filterable tables, zero broken links, line-by-line verification pass) | `in progress` | `session-256b850d` | `index.html`, `pages/*.html`, `assets/*`, `.nojekyll` | 2026-11-25 |
| `T-07` | Final integration audit, link & schema validation, live preview verification, and GitHub Pages publication | `unclaimed` | — | `README.md`, `COORDINATION.md`, site root | 2026-11-25 |

---

## Repo Audit Notes (`T-00`)

- **Initial Repo Inspection (2026-11-25):**
  - Only file present on `main` (`fa1f9fa`): `README.md` (`# ChinaFun3`).
  - No other branches, worktrees, or pull requests exist on `origin`.
  - GitHub Pages is currently configured in legacy mode serving `/` from `main` at `https://kanlerxz87-cyber.github.io/ChinaFun3/`.
- **Initial Prompt Irregularities Identified for Flagging:**
  1. **Date Duration Conflict:** Prompt states trip length should be *1–2 weeks* (and requests *7-night* hotel stay totals), while also stating *"Preferred vacation time is February 15 2027 to February 18 2027"* (which is only 3 nights / 4 days). Flagged for user clarification.
  2. **Destination City/Region Unspecified:** Prompt specifies *"China"* without specifying Mainland China vs. Hong Kong/Macau SARs, or single-city vs. multi-city itinerary.
  3. **2027 Lunar New Year / Spring Festival Overlap:** Must verify exact 2027 Chinese New Year & Lantern Festival dates relative to Feb 15 – Mar 23, 2027.

---

## Verification & Source Log

- **`T-01` Completed (`data/calendar-and-clusters.json`):**
  - Verified 2027 official public holiday schedule (Spring Festival Feb 5–13, make-up workdays Jan 31 & Feb 14, Qingming Apr 3–5) via Beijing Municipal Government (`english.beijing.gov.cn`), Lantern Festival (Feb 20, 2027), Beijing Two Sessions (early March) via State Council (`english.www.gov.cn`), NIA 240-hour visa-free transit (`en.nia.gov.cn`), and Shanghai/Beijing Feb–Mar climate normals (`climate-data.org`).
  - Verified all 10 active Mainland China MICHELIN Guide editions (Shanghai 156 / 51★, Beijing 107 / 33★, Guangzhou 117 / 20★, Chengdu 84 / 15★, Zhejiang/Hangzhou 142 / 13★, Jiangsu 111 / 9★, Shenzhen 59 / 7★, Fujian 96 / 7★, Hunan 61 / 4★ debut Nov 24, 2026, Tianjin 27 / 1★) plus Greater China SAR benchmarks (Hong Kong 219 / 77★, Macau 59 / 21★) directly from `guide.michelin.com` ceremony releases and `english.shanghai.gov.cn`.
  - Irregularities flagged: Shanghai live index shows 153 vs 156 at ceremony due to mid-year closures; Zhejiang/Hangzhou province-only Bib/Selected split left `null` because official tri-region release only published combined 409-restaurant Bib/Selected totals; exact 2027 Two Sessions closing date not yet officially published.
- **`T-02` Completed (`data/restaurants.json`):**
  - Verified 29 individual restaurants (16 Shanghai, 13 Beijing) directly on `guide.michelin.com` (addresses, phone numbers, star vs. Bib Gourmand / Selected distinction, cuisines, ¥ price tier, and published hours).
  - Extracted exact 2026 official menu pricing & hours directly from primary restaurant websites/PDFs for `Taian Table`, `Bao Li Xuan`, `Da Vittorio`, `T'ang Court`, `Imperial Treasure`, `Yong Yi Ting`, `Jade on 36`, `Trb Hutong`, and `Fu Chun Ju` (plus hours/policy for `8 ½ Otto e Mezzo Bombana` and `Monsieur Dior`).
  - Verified YouTube, Instagram, and TikTok/Douyin URLs via direct search results (no guessed handles/links).
  - Unverified numeric prices/hours intentionally left `null` and logged in `unverifiedFields` for the Flagged for Review page. Note also: `King's Joy` dropped from 3★ to 2★ in the Oct 2026 Beijing 2027 Guide; `157 Shi Fang` relocated to IM Shanghai (1398 Kaixuan Rd); `No. 69 Fangzhuanchang Zhajiangmian` has official street address `1 Fangzhuanchang Hutong`.
- **`T-03` Completed (`data/hotels.json`):**
  - Verified 10 hotels (5 Shanghai, 5 Beijing) spanning value/midscale through ultra-luxury, all confirming private bathrooms, Queen/King bed dimensions, key amenities, and ≤1-hour door-to-door Metro reachability to 100% of audited Michelin restaurants (`16/16` Shanghai, `13/13` Beijing), cross-checked verbatim against `data/restaurants.json` distinctions.
  - Retrieved live tax-and-fee-inclusive 7-night quotes for `2027-02-22` to `2027-03-01` (2 adults, 1 room) via Trip.com for all 10 hotels, PLUS live official direct SynXis booking engine rates (`be.synxis.com`) for `The PuLi Hotel and Spa` (`CN¥2,533/nt excl. tax`) and `The PuXuan Hotel and Spa` (`CN¥2,468/nt excl. tax`, Stay 4 Pay 3 w/ breakfast).
  - Ran live 4-week 2027 benchmark pricing (`Feb 15–22`, `Feb 22–Mar 1`, `Mar 1–8`, `Mar 15–22`) on `Radisson Blu Shanghai New World` (US$1,061 → US$1,179 → US$1,543 → US$1,620), `Hilton Beijing Wangfujing` (US$1,317 → US$1,343 → US$1,343 → US$1,409+), and `Park Plaza Beijing Wangfujing` (US$955 flat), combined with KAYAK's May 6, 2026 hotel booking timing study (`kayak.co.uk/news/best-time-to-book-a-hotel/`). Direct brand SPA engines for IHG, Radisson, Hilton, and Shangri-La blocked/errored on automated rate scraping and are noted explicitly in `directOfficialRateNote`.
- **`T-04` Completed (`data/activities.json`):**
  - Verified 16 iconic activities & attractions (8 Shanghai, 8 Beijing) with official off-season winter (Dec–Mar / Nov–Mar) 2-adult CNY admission prices, exact opening hours, weekly Monday/Tuesday closure patterns, and passport/booking rules directly from primary municipal/venue portals (`yugarden.com.cn`, `shanghaimuseum.net`, `english.shanghai.gov.cn`, `meet-in-shanghai.net`, `westbund.com`, `english.beijing.gov.cn`).
  - Explicitly flagged nuances: `Badaling Great Wall` HSR train ride is only 20–27 min from Beijing North/Qinghe, but total door-to-door from downtown hotels is ~60–70 min incl. station security (flagged transparently); `West Bund Museum` rotating post-Feb 14, 2027 Centre Pompidou show fee and `Badaling` cable car fee left flagged rather than guessed. Verified YouTube/Instagram links attached only where directly verified.
- **`T-05` Completed (`data/governance.json`):**
  - Consolidated Executive Summary (3 itinerary options: 7-night Shanghai Feb 22–Mar 1, 14-night Dual-City Shanghai Feb 15–22 + Beijing Feb 22–Mar 1, and 3-night sprint if Feb 15–18 is hard-locked), verified 2-adult 7-night cost snapshots, 7 prioritized Missing Info / Decision Questions (`Q-01`–`Q-07`), 4-phase Discovery Plan, 5 high-impact Site Improvement Suggestions (`IMP-01`–`IMP-05`), and 10 comprehensive Flagged for Review audit entries (`FLG-01`–`FLG-10`) synced across all 4 upstream JSON files.

---

## Change Requests Across Scopes

*(None yet.)*
