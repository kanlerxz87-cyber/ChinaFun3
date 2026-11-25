# COORDINATION — ChinaFun3 Trip Planning

Session ID: `session-7449eccd` (branch `arena/7449eccd-chinafun3`)
Last updated: 2026-11-25 (round 2)

## Task board

| ID | Task | Status | Owner | Files touched |
|----|------|--------|-------|---------------|
| T1 | Repo review + COORDINATION setup | done | session-7449eccd | COORDINATION.md, README.md |
| T2 | Research: Michelin clusters (Shanghai/Beijing/Guangzhou-Shenzhen) from guide.michelin.com | done | session-7449eccd | data/michelin.json, michelin.html |
| T3 | Research: Hotels (queen+, private bath) + 7-night pricing methodology | done | session-7449eccd | data/hotels.json, hotels.html |
| T4 | Research: Activities within 1h + hours + social links | done | session-7449eccd | data/activities.json, activities.html |
| T5 | Research: Dates (CNY 2027), weather, transit, booking windows | done | session-7449eccd | pricing.html |
| T6 | Build GitHub Pages site (landing + subpages, mobile-friendly dashboard) | in progress | session-7449eccd | index.html, *.html, assets/* |
| T7 | Verification pass: every row has official source or flagged unverified | in progress | session-7449eccd | verification.html, flagged.html |
| T8 | Final integration + Pages publish + broken-link check | unclaimed | — | all |

## Rules followed
- No manual input requested; all work done autonomously.
- Every table row links to an official source. Unconfirmed values left blank + flagged **Unverified**.
- No inferred prices. Hotel 7-night totals for Feb 2027 are dynamic (require live booking search) — flagged unverified with direct official booking links.
- Only Taian Table price is from the restaurant's official FAQ (verified). Other restaurant prices from secondary sources are labelled as such, not presented as official.
- Parallel sessions: claim by writing session ID here, commit+push immediately, keep scopes non-overlapping, `git pull --rebase` before push.

## Sources & verification log
- Michelin Shanghai|Jiangsu|Zhejiang 2026 (official, 2026-04-09): https://guide.michelin.com/en/article/michelin-guide-ceremony/michelin-guide-shanghai-jiangsu-zhejiang — 409 restaurants, 77 starred (1×3★, 14×2★, 62×1★); Shanghai 156 restaurants.
- Taian Table official page (3★, Changning, ¥¥¥¥): https://guide.michelin.com/en/shanghai-municipality/shanghai/restaurant/taian-table
- Taian Table official FAQ prices ¥2,588 (10-course) / ¥2,888 (12-course): https://sh.taian-table.cn/faq/
- Grand Hyatt Shanghai official rooms (1 Queen Bed, 2 Queen Beds, private bath/tub): https://www.hyatt.com/grand-hyatt/en-US/shagh-grand-hyatt-shanghai/rooms
- Waldorf Astoria Shanghai on the Bund official rooms (Double Queen Deluxe etc.): https://www.hilton.com/en/hotels/shawawa-waldorf-astoria-shanghai-on-the-bund/rooms/
- Fairmont Peace Hotel official rooms (Fairmont Queen Queen, marble bathroom): https://www.fairmont.com/en/hotels/shanghai/fairmont-peace-hotel/rooms/DBCMV.room.html
- Bvlgari Hotel Shanghai official (82 rooms, Bao Li Xuan on site): https://www.bulgarihotels.com/en-US/shanghai
- Peninsula Shanghai official rooms/suites: https://www.peninsula.com/en/shanghai/luxury-hotel-room-suite-types/the-palace-suite
- Shanghai Museum official hours 9:00–17:00, closed Mon (except holidays): https://www.shanghaimuseum.net/mu/frontend/pg/m/article/id/I00004797
- CNY 2027: Sat Feb 6, 2027; holiday Feb 5–13 (State Council notice via secondary summaries — flagged for gov.cn re-check).

## Irregularities flagged
- Four Seasons Shanghai (new, Huaihai Zhong Rd) is announced for 2027 opening — NOT bookable as an existing hotel for Feb 2027; excluded from ranking, listed as flagged.
- Ultraviolet by Paul Pairet (formerly 3★ Shanghai) closed 29 Mar 2025 — removed from all lists.
- Hotel nightly rates for Feb 2027 are not published on static official pages; 7-night totals left blank/unverified.
- Restaurant opening hours are not consistently published on Michelin pages; left blank/unverified where not on official restaurant site.
- Social links: only URLs returned by web search are used; platform search URLs are provided where no direct post URL was verified.

## Handoff log
- 2026-11-25 session-7449eccd claimed T1–T7 on branch arena/7449eccd-chinafun3.

## Round 2 findings (session-7449eccd)

### Corrections made against the first draft
- Waldorf Astoria Shanghai on the Bund does house a starred restaurant: **Ling Long (1★)** at 105, 1F, 2 Zhongshan Dong Yi Road — confirmed on https://guide.michelin.com/en/shanghai-municipality/shanghai/restaurant/ling-long-1209951. Hotel ranking updated.
- Fu He Hui district confirmed as **Changning** (1037 Yuyuan Road), phone +86 21 3980 9188.
- Fu He Hui hours confirmed daily 11:00-13:00 / 17:30-21:00 on its MICHELIN page.

### Restaurant pages read individually (address + phone + hours + official site where published)
- Taian Table (3★) — Changning, +86 173 0160 5350, sh.taian-table.cn
- Fu He Hui (2★) — 1037 Yuyuan Rd, Changning, +86 21 3980 9188, daily 11:00-13:00 & 17:30-21:00
- Bao Li Xuan (2★) — 3F Chamber of Commerce, Lane 108 N Shanxi Rd, Jingan, +86 21 3606 7788, bulgarihotels.com
- Canton 8 Huangpu (2★) — 63 Runan St, Huangpu, +86 21 6733 7123
- 8½ Otto e Mezzo Bombana (2★) — 6-7F Associate Mission Bldg, 169 Yuanmingyuan Rd, Huangpu, +86 21 6087 2890, Mon-Wed dinner only / Thu-Sun lunch+dinner
- T'ang Court (2★) — 5F Langham Xintiandi, 99 Madang Rd, Huangpu, +86 21 2330 2288
- Ji Pin Court (2★) — 3F 55 S Wulumuqi Rd, Xuhui, +86 21 6469 9969
- Tou Zao (2★) — Shanghai Centre 1376 W Nanjing Rd, Jingan, +86 191 2133 7327
- Amazing Chinese Cuisine Changning (2★) — B5 Villa 1665 Hongqiao Rd, +86 21 6262 5677, selectionbydu.com
- The House of Rong (2★) — 170 Nanyang Rd, Jingan, +86 21 6289 1717, xinrongji.com
- Imperial Treasure (2★) — L402-403 Yi Feng Galleria 99 E Beijing Rd, Huangpu, +86 21 5308 1188
- Da Vittorio (2★) — 3F N3 Bund Finance Centre 600 Zhongshan Dong Er Rd, Huangpu, +86 21 6330 2198, closed Mondays
- Jin Xuan (1★) — 53F Ritz-Carlton Pudong, 8 Century Ave, +86 21 2020 1717, 11:30-21:30/22:00
- Yi Long Court (1★) — 2F Peninsula Bund 32, +86 21 2327 6742, daily 11:30-14:30 & 18:00-22:30
- Yong Fu Huangpu (1★) — 11-12F Jin Jiang Hotel 59 S Maoming Rd, +86 21 3356 6777, daily 11:00-14:00 & 17:00-21:00
- Ling Long (1★) — 105 1F Waldorf Astoria, 2 Zhongshan Dong Yi Rd, +86 21 2329 0313, daily 16:00-01:00
- Fu 1015 (1★) — 1015 Yuyuan Rd, Changning, +86 21 5237 9778
- Fabula (1★) — 2-3F 720 Weihai Rd, Jing'an, +86 131 8434 3001, fabula.restaurant

### Coverage after round 2 (of 58 restaurant rows)
- address 19/58 · phone 18/58 · official site 14/58 · published hours 7/58 · verified price for two 1/58
- Remaining gaps stay blank + flagged; they are listed on flagged.html.

### Irregularity noted
- MICHELIN city page counters (1×3★, 11×2★, 38×1★ = 50) vs. the 2026 launch release figure of 12 two-star
  restaurants for the wider region. City-page counter is used; discrepancy documented.
