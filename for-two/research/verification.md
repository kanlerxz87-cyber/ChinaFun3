# Verification and scope audit

Research snapshot: **2026-11-25 UTC**. Travel dates are in China local time. Sources were checked using web search to discover URLs and `fetch_page` to inspect official page/PDF contents. The source register in [trip.json](../data/trip.json) records the checked claim, URL, method, date and limits; [Sources](../sources.html) renders it for manual review. Summaries are paraphrases, not full archived pages. Research has not been independently audited by a second human/session.

## What was actually done

- Inspected original repository: only an 11-byte README, no application, no data, no coordination board. Created the board, claimed scope, committed and pushed before implementing.
- Used the fixed Arena branch; no other session claim or integration branch was found. No other branch was created, switched to, merged into or pushed.
- Checked official Michelin 2026 regional releases for Shanghai and Guangzhou. Kept Shanghai/Guangzhou separate from regional totals and did not copy third-party aggregate prices.
- Read seven restaurant records against the official guide and/or operator. Found five starred restaurants, one Bib Gourmand and one Selected restaurant in this shortlist. It is **not** the complete Shanghai guide.
- Read official room pages for four hotels. Recorded king beds, room sizes when stated, bathroom fixtures and amenities. Did not turn implied bathroom privacy into an explicitly confirmed field.
- Queried Peninsula's official engine for **six** date windows, each seven nights, one room, two adults: 15–22 February, 22 February–1 March, 1–8 March, 8–15 March, 15–22 March and 16–23 March 2027.
- Accepted the **inputs** of CNY 2,465 or 2,805 average nightly for Deluxe King, A Gift for the New Year. Applied the hotel's published 16.6% surcharge transparently. Result: CNY 20,119.33 or 22,894.41 for seven nights. These are **calculated totals, not a captured checkout quotation or reserved price**.
- Found actual booking promotion 23 November–7 December in the current 2026 festive context, for January–March stays; engine says book before 8 Dec. 15% discount is for rooms; 20% is for suites. All sampled offer rates require full non-refundable prepayment and no amendments.
- Attempted Langham's official dated search: correct dates/occupancy but no priced room cards returned. This does not mean sold out.
- Attempted Marriott's official dated search: both CNY 7,755 and 6,650 seven-night totals appeared with ambiguous markup. Neither accepted as a verified comparable rate.
- No date-specific Bvlgari quote obtained; no hotel price invented from search-engine snippets, OTA “from” rates or annual averages.
- Checked four current restaurant menus with usable totals: T’ang Court CNY 888 / 2,288 for two; Bao Li Xuan autumn set CNY 3,576 food or 5,176 with pairing; Yi Long Court two set lunches CNY 788.22; Sir Elly’s two five-course menus CNY 3,003.62. Operator taxes/surcharges accounted for. None is confirmed for 2027 travel dates.
- Taian Menu 55 extracted base price missing: optional add-on amounts were not used as the meal total. Polux numeric dishes were visible, but full currency/tax treatment was not established in the inspected text, so no all-in couple total was asserted.
- Read five activity records from museums, city government or the experience operator. Distinguished the East and People's Square Shanghai Museum branches. Kept older Yuyuan night-tour pricing in explicitly historical notes, not the 2027 price field.
- Matched social media where possible. T’ang Court and Yi Long Court have related hotel profiles only, not verified restaurant-specific videos. Museum People's Square later acquired an exact-exhibition YouTube link. Every activity and restaurant has a media or related-profile link, but **not all are exact-product videos**. YouTube metadata was readable on several pages with playback errors. No claim that all videos play or that historic footage shows future conditions.
- Attempted Shanghai Metro official website; fetch failed. No hotel-door to venue-door timed itinerary was obtained. **Every transit duration and citywide one-hour coverage rank remains null.** Same-hotel venues are described separately, never counted as proof of a citywide transit radius.

## Line-by-line publication rules

1. Each hotel, restaurant, activity and quote row must reference at least one official source ID in `data/trip.json`.
2. Awards, prices, hours, room attributes and addresses must be supported by the checked claim. Media cannot support these facts.
3. Missing facts are null in JSON, empty in CSV, and blank-valued with a visible reason on the site. Null is never converted to zero, “free”, “sold out”, or a ranking.
4. Historical/current menu prices are distinguished from travel-date prices. All unknown `price2027` fields remain null.
5. Computed values are marked as computed; source inputs and arithmetic are retained.
6. Proposed dates, clusters, itinerary, prioritization and suggestions are editorial recommendations, not claims of provider availability.
7. Personal requirements come from [the user brief](request.md). Passport/nationality, budget, flight origin and dietary preferences cannot be inferred. No automated inquiry was sent using invented traveler details.
8. Official external URLs were checked via fetched contents, not an independent live browser crawl. This is **not** a guarantee of zero broken external links now or later. Internal links/assets are checked automatically; external failures/redirects are documented on [Flagged for Review](../review.html).

## Irregularities deliberately retained

See F01–F14 on [Flagged for Review](../review.html). Highlights:
- T’ang Court says both “daily” and “Off on Monday”.
- Langham Deluxe size: index 40–43 m²; detail 40 m² (detail used).
- Peninsula room page says two adults maximum; engine says sleeps three (two adults fits both, no third guest assumed).
- Yi Long Court old operator URL redirected to hotel home; canonical `/yi-long-court` subsequently found and checked.
- Guessed Michelin Da Vittorio Shanghai slug redirected to Italy; excluded rather than borrowing the Italian venue's three stars.
- Guessed Canton 8 / Mercato URLs failed; no unsupported record created.
- PuLi, Yu Garden direct domain, History Museum direct domain and Metro attempts failed. No operational claim inferred.
- Unmatched T’ang Court search results frequently concerned Hong Kong; rejected as Shanghai evidence.
- Dates fit a hotel-stay scenario, not necessarily door-to-door international travel. Preferred 15–18 February dates alone cannot satisfy the seven-night request.

## Tests

`npm test` checks source integrity, null handling, dates, arithmetic, classifications, HTML semantics and every local link/fragment/asset. `npm run test:browser` checks desktop/mobile layouts, navigation, filters, local review persistence, exports, no-JavaScript content and axe accessibility rules. Test results and publication evidence are recorded in `research/release.md` after running; tests do not verify external travel truth.

## What remains incomplete

An exhaustive China-wide city/hotel search; three accepted competing hotel prices; all 30 eligible seven-night date checks; a final checkout total; private-bathroom confirmation; one-hour transit ranking; a complete flight/meal/activity/transport budget; exact-venue media for two restaurants; date-valid 2027 menus, holidays and some opening hours; traveler-specific entry feasibility. These are visible research gaps, not fabricated completions. No future monitoring or follow-up service is running.

## Parallel integration boundary

After initial research, other sessions merged root, docs/ and considered/ dashboards. Their existing files are preserved byte-for-byte; this session’s complete deliverable is under /for-two/. The retained datasets were not independently source-audited by this session. F14 explicitly warns against treating preservation as factual endorsement. Build tools, test dependencies and source records for this dashboard are scoped to for-two/ only.
