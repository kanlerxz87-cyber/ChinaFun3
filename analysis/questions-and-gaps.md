# Questions, Information Gaps, and Answers Needed

**Purpose:** List what is known, unknown, and required before a final booking decision. No manual input is required from the user for this draft; unresolved items are flagged for review.

## A. Decision-Critical Questions

| ID | Question | Why it matters | Current known info | Missing info | Suggested way to discover | Priority |
|---|---|---|---|---|---|---|
| Q1 | Which city in China is the destination? | Hotels, restaurants, transport, and activities all depend on it. | User said "Trip Planning China" but no city named. | Confirmed city. | User confirms; if no response, default to Shanghai and mark as assumption. | Critical |
| Q2 | What is the actual trip length? | Conflicts: "1-2 weeks long" vs "Preferred vacation time is February 15 2027 to February 18 2027" (4 days). | Both statements present in request. | Intended check-in/check-out and total nights. | Propose 7 nights (2027-02-15 to 2027-02-22) covering preferred start; ask user to confirm. | Critical |
| Q3 | What is the hotel budget? | "Best hotels by price..." needs a ceiling/target. | No budget given. | Max nightly or max 7-night total in CNY/USD. | User provides budget; otherwise present 3 tiers (budget/mid/upscale) with verified/indicative pricing. | Critical |
| Q4 | What does "Michelin rated" include? | Affects restaurant count and hotel ranking. | Michelin has Stars, Bib Gourmand, Selected distinctions. | Include all Michelin Guide-listed restaurants or stars only? | Default: include Starred + Bib Gourmand + Selected but label distinction clearly; user confirms. | High |
| Q5 | What are the preferred activities? | "For the activites we plan to do..." but none specified. | No activities listed. | Activity types, must-see places, mobility constraints. | Propose top Shanghai activities near hotel cluster; user selects. | High |
| Q6 | What is the meal budget for Michelin dining? | "Cost... for a couple of 2 adults" varies widely (¥¥ to ¥¥¥¥). | Michelin price symbols available on some pages. | Per-meal/per-day budget, lunch vs dinner preference. | Use Michelin price bands and flag exact totals unverified; user sets cap. | High |
| Q7 | What booking channel and cancellation policy is required? | "Cheapest upcoming time to book" depends on refundable/non-refundable and channel. | No preference stated. | OTA vs official site, refundable vs prepaid, loyalty programs. | Compare official hotel site and major OTAs for same room/date/cancellation terms. | High |
| Q8 | Any dietary, accessibility, or visa/passport constraints? | Affects restaurant/hotel suitability. | Travelers are a couple of 2 adults; no other constraints given. | Allergies, dietary restrictions, mobility needs, passport/visa status. | User confirms; flag as unknown. | Medium |

## B. Information Gaps (Current Research)

| Gap ID | Gap | Impact | Current status | How to close |
|---|---|---|---|---|
| G1 | 2027-02-15 to 2027-02-22 hotel pricing not confirmed | Cannot claim "real verified pricing" for target dates | Unverified | Check Booking.com/Agoda/Trip.com/official hotel site for exact dates; capture date-stamped quote |
| G2 | "Cheapest upcoming time to book" not verifiable | User asked for it; no official source gives definitive answer | Unverified | Track prices over time with price alerts; compare refundable rate now vs historical trends; document method |
| G3 | Restaurant hours/open days incomplete | User asked for days/hours/exceptions | Partially verified (Da Vittorio hours from Michelin page) | Check each restaurant's official site/Google Business/Michelin page; confirm holiday exceptions |
| G4 | Exact per-couple restaurant pricing unavailable | User asked for exact or estimate range | Partially available (Michelin ¥ symbols) | Use restaurant menus/official sites where published; otherwise provide labeled estimate range |
| G5 | Transit time (<=1hr by subway/bus) not route-verified | Hotel ranking depends on it | Estimated from location knowledge | Verify each hotel-restaurant pair using Amap/Baidu Maps/Google Maps transit directions at typical dining time |
| G6 | Social media links (YouTube/TikTok/Instagram) for every restaurant/activity | User requested as many as possible | Not collected in this draft pass | Search official accounts per venue; only include verified official/recognizable links |
| G7 | Private bathroom / queen bed confirmation for each hotel candidate | Required amenity | Partially verified from listing text | Confirm on hotel official room page or booking room details for target room type |
| G8 | Activity list unspecified | "Activites we plan to do" unknown | No user-provided activities | Propose a default Shanghai itinerary near hotel cluster; mark as proposal |

## C. Assumptions Made in This Draft (Must Be Confirmed)

| Assumption | Rationale | Risk if wrong |
|---|---|---|
| Destination is Shanghai | Strong Michelin density, good transit, clear sources | Entire plan changes |
| 7 nights: 2027-02-15 check-in, 2027-02-22 check-out | Fits 1-2 week window and includes preferred start date | Dates/pricing/availability change |
| 2 adults, 1 room, queen bed+, private bathroom | Explicit in request | Room selection changes |
| "Michelin rated/star restaurants" includes Starred restaurants; Bib Gourmand/Selected listed separately with distinction | User wording ambiguous | Restaurant scope changes |
| Pricing shown as indicative where not date-confirmed | No reliable 2027 inventory source in-session | User may over/under-budget |
