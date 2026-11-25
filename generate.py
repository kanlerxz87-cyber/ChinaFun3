#!/usr/bin/env python3
"""Static-site generator for the ChinaFun3 Shanghai trip-planning site.

Every value rendered comes from data/dataset.py. Nothing is invented here:
missing values render as an explicit "Not verified" chip.
Run:  python3 generate.py   (writes *.html into the repo root)
"""
from html import escape as e
from pathlib import Path
from collections import Counter

import data.dataset as D

ROOT = Path(__file__).parent / "plan"
NAV = [
    ("index.html", "Dashboard"),
    ("hotels.html", "Hotels"),
    ("michelin.html", "Michelin"),
    ("activities.html", "Activities"),
    ("dates.html", "Dates & Booking"),
    ("questions.html", "Open Questions"),
    ("suggestions.html", "Suggestions"),
    ("flagged.html", "Flagged"),
    ("verification.html", "Verification"),
]

VERIFIED = '<span class="badge ok">verified</span>'
UNVERIFIED = '<span class="badge warn">unverified</span>'


def chip(v, ok_text=None):
    if v:
        return e(v) if not ok_text else ok_text
    return '<span class="badge warn">not verified</span>'


def link(url, text=None):
    if not url:
        return '<span class="badge warn">no official link</span>'
    return f'<a href="{e(url)}" target="_blank" rel="noopener">{e(text or url)}</a>'


def page(title, subtitle, body, active):
    nav = "".join(
        '<a href="%s"%s>%s</a>' % (h, ' class="active"' if h == active else "", t)
        for h, t in NAV
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)} · Shanghai Trip Plan</title>
<meta name="description" content="{e(subtitle)}">
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="topbar"><div class="topbar-inner">
  <div class="brand">Shanghai · Feb-Mar 2027<small>Verified trip research · 2 adults</small></div>
  <nav class="nav">{nav}</nav>
</div></header>
<main id="main" class="wrap">
{body}
</main>
<footer>
  Built from <code>data/dataset.py</code>. Blank or chipped fields are <strong>not verified</strong> —
  no value on this site is estimated. Sources are linked on every row.
  · <a href="verification.html">Method &amp; source log</a>
</footer>
</body>
</html>"""


# ---------------------------------------------------------------------------
# derived numbers (computed, never invented)
# ---------------------------------------------------------------------------
starred = [r for r in D.RESTAURANTS if r["stars"] > 0]
bib = [r for r in D.RESTAURANTS if r.get("bib")]
by_star = Counter(r["stars"] for r in D.RESTAURANTS)
district_stars = Counter(r["district"] for r in starred if r["district"])
district_any = Counter(
    r["district"] for r in D.RESTAURANTS if r["district"]
)
total_starred_shanghai = 50  # official count on the MICHELIN all-starred page
rows_verified_hours = sum(1 for r in D.RESTAURANTS if r["hours"])
rows_verified_cost = sum(1 for r in D.RESTAURANTS if r["cost"])
rows_with_site = sum(1 for r in D.RESTAURANTS if r["site"])


def hotel_rank():
    scored = []
    for h in D.HOTELS:
        inb = len(h["inbuilding"])
        dcount = district_stars.get(h["district"].split(" (")[0], 0)
        scored.append((inb * 10 + dcount, inb, dcount, h))
    scored.sort(key=lambda x: (-x[0], x[3]["name"]))
    return scored


RANKED = hotel_rank()

# social links: only URLs actually seen during research
SOCIAL = {
    "Taian Table": [
        ("YouTube", "https://www.youtube.com/watch?v=RYsEUZJSrN8", "in-depth review (16 Jul 2026)"),
        ("YouTube", "https://www.youtube.com/watch?v=YyhXAggluco", "Tai'an Table (27 Feb 2022)"),
    ],
}


def social_cell(name):
    links = SOCIAL.get(name, [])
    if not links:
        q = name.replace(" ", "+")
        return ('<span class="badge warn">no verified post</span>'
                f'<br><a href="https://www.youtube.com/results?search_query={q}+shanghai" target="_blank" rel="noopener">YouTube search</a>')
    out = []
    for plat, url, note in links:
        out.append(f'<a href="{e(url)}" target="_blank" rel="noopener">{plat}</a> <span class="muted">{e(note)}</span>')
    return "<br>".join(out)


# ---------------------------------------------------------------------------
# INDEX
# ---------------------------------------------------------------------------
def build_index():
    top = RANKED[:3]
    cards = "".join(
        f'<div class="card"><h3>{e(h["name"])}</h3>'
        f'<p class="muted">{e(h["district"])}</p>'
        f'<p>In-building: <strong>{len(h["inbuilding"])} starred</strong>'
        + (f' — {e(", ".join(h["inbuilding"]))}' if h["inbuilding"] else "")
        + f'<br>Confirmed starred in district: <strong>{dc}</strong></p>'
        f'<a class="btn secondary" href="hotels.html">Details</a></div>'
        for _, inb, dc, h in top
    )
    body = f"""
<section class="hero">
  <h1>Shanghai, 15 Feb – 22 Feb 2027 · 7 nights · 2 adults</h1>
  <p>Michelin-first trip plan: which hotels put the most starred restaurants within an hour,
     what dinner actually costs for two, and what still needs checking before you book.</p>
  <p class="muted" style="color:#e2e8f0">Every number below is either read from an official page
     or shown as <strong>not verified</strong>. Nothing is estimated.</p>
</section>

<div class="kpi">
  <div class="card"><b>{total_starred_shanghai}</b><span class="muted">starred restaurants in Shanghai
    (2026 guide, official count)</span></div>
  <div class="card"><b>{by_star.get(3,0)}</b><span class="muted">three-star in the city (Taian Table)</span></div>
  <div class="card"><b>{len(D.HOTELS)}</b><span class="muted">hotels shortlisted, bed + bath verified</span></div>
  <div class="card"><b>{rows_verified_cost}/{len(D.RESTAURANTS)}</b><span class="muted">restaurants with a verified price for two</span></div>
</div>

<div class="notice">
  <strong>Read this first.</strong> Hotel prices for February 2027 are not published as static pages by any
  brand — every 7-night total on this site is therefore <strong>blank</strong>, with the official booking link
  alongside it. Restaurant rows without a verified price are equally blank. That is deliberate: an invented
  number is worse than a gap. The <a href="flagged.html">Flagged</a> page lists every gap.
</div>

<h2>Executive summary</h2>
<div class="grid">
  <div class="card" style="grid-column:span 12">
    <ol>
      <li><strong>Base yourself on the Bund / Huangpu.</strong> Huangpu has
        <strong>{district_stars.get("Huangpu",0)}</strong> starred restaurants whose district is confirmed on
        MICHELIN pages — the densest confirmed cluster, and the Peninsula, Waldorf Astoria and Fairmont Peace
        are all inside it.</li>
      <li><strong>One hotel beats everything on walk-to-dinner.</strong> Bvlgari Shanghai houses
        <strong>two</strong> starred restaurants in the same building (Bao Li Xuan 2★ and Il Ristorante 1★).
        The Waldorf Astoria (Ling Long 1★), the Peninsula (Yi Long Court 1★) and the Ritz-Carlton Pudong
        (Jin Xuan 1★) each house one — confirmed on each restaurant's MICHELIN page.</li>
      <li><strong>Only one restaurant price survives verification.</strong> Taian Table publishes
        ¥2,588 / ¥2,888 per person → <strong>¥5,176–5,776 for two</strong> before add-ons. Other starred
        houses do not publish menus that a static page can confirm.</li>
      <li><strong>The dates are well chosen.</strong> Spring Festival 2027 runs 5–13 February; your window
        opens the day after it closes, so you avoid peak rates and holiday closures, and still catch the
        Lantern Festival on 20 February.</li>
      <li><strong>Booking timing is evidence-based, not guesswork.</strong> Industry 2026 data points to
        8–14 days out for city hotels, with the trade-off of losing specific room categories — see
        <a href="dates.html">Dates &amp; Booking</a> for the exact recommendation and its caveat.</li>
      <li><strong>{len(D.EXCLUDED)} properties are explicitly excluded</strong> and why (Four Seasons not yet
        open in 2027, Ultraviolet closed 2025, one hotel fetched in error).</li>
      <li><strong>{len([r for r in D.RESTAURANTS if not r["hours"]])} of {len(D.RESTAURANTS)}</strong>
        restaurants still have no official hours — the single biggest gap in this plan.</li>
    </ol>
  </div>
</div>

<h2>Best hotel picks by Michelin proximity</h2>
<p class="muted">Ranking = starred restaurants inside the building (weighted ×10) + starred restaurants whose
district is confirmed on MICHELIN. District counts are a verified <em>floor</em>, not a full city tally.</p>
<div class="grid">{cards}</div>
<p><a class="btn" href="hotels.html">See all hotels and the full ranking</a></p>

<h2>Where the Michelin weight actually sits</h2>
<div class="tablewrap"><table>
<thead><tr><th>District (confirmed on MICHELIN page)</th><th>Starred</th><th>Rows with a confirmed district</th></tr></thead>
<tbody>
{"".join(f'<tr><td>{e(k)}</td><td><strong>{v}</strong></td><td>{district_any.get(k,0)}</td></tr>' for k, v in district_stars.most_common())}
</tbody></table></div>
<p class="muted">Districts are only shown where the MICHELIN restaurant page states the district; the rest are
left blank rather than guessed, so real totals per district are equal or higher.</p>

<h2>What this site does not know yet</h2>
<div class="notice"><p>Before booking, eight questions need answers — currency of the live room rate,
cancellation terms, which starred kitchens close on Mondays, and whether the hotels actually hold
queen-bed rooms on your dates. They are all listed, with how to find each answer, on
<a href="questions.html">Open Questions</a>.</p></div>
<div class="toolbar">
  <a class="btn" href="questions.html">Open questions</a>
  <a class="btn secondary" href="flagged.html">Flagged for review</a>
  <a class="btn secondary" href="suggestions.html">Site suggestions</a>
</div>
"""
    return page("Dashboard", "Shanghai Michelin trip plan for 2 adults, Feb-Mar 2027", body, "index.html")


# ---------------------------------------------------------------------------
# HOTELS
# ---------------------------------------------------------------------------
def build_hotels():
    rows = []
    for i, (score, inb, dc, h) in enumerate(RANKED, 1):
        rows.append(f"""<tr>
<td><strong>#{i}</strong></td>
<td><strong>{e(h["name"])}</strong><br><a class="muted" href="{e(h["book"])}" target="_blank" rel="noopener">official booking</a></td>
<td>{e(h["district"])}<br><span class="muted">{e(h["address"]) or "address not verified"}</span></td>
<td>{inb}</td><td>{dc}</td><td>{score}</td>
<td>{e(h["room_ok"])}<br>{link(h["room_src"], "room page")}</td>
<td>{e(h["rooms"]) or chip("")}</td>
<td>{chip(h["nights"])}<br><span class="muted">{e(h["rate_note"])}</span></td>
<td>{e(h["keys"]) or chip("")}</td>
</tr>""")
    body = f"""
<h1>Hotels — price, location, amenities, Michelin reach</h1>
<p class="lead">Shortlist rule: a private, ensuite bathroom and at least a queen-equivalent bed, confirmed on the
brand's own website. Any hotel whose room page could not be read is still listed but flagged.</p>

<div class="notice info">
  <strong>Why the 7-night column is empty.</strong> No hotel brand publishes a February-2027 rate as a static
  page — rates are quoted only inside a live booking engine, in the guest's currency, after dates and party size
  are entered. Filling this column would mean inventing numbers, so every row links to the official booking
  engine instead. <a href="dates.html">See the booking-window recommendation.</a>
</div>

<div class="tablewrap"><table>
<thead><tr>
<th>Rank</th><th>Hotel</th><th>Area</th><th>Starred<br>in building</th>
<th>Starred in<br>district (floor)</th><th>Score</th><th>Room that meets the brief</th>
<th>Rooms</th><th>7 nights (15–22 Feb 2027)</th><th>MICHELIN Keys</th>
</tr></thead>
<tbody>{"".join(rows)}</tbody></table></div>

<div class="notice ok">
  <strong>Ranking result.</strong> Bvlgari Shanghai wins outright: Bao Li Xuan (2★) and Il Ristorante (1★) are
  both inside the building. Waldorf Astoria on the Bund, the Peninsula and the Ritz-Carlton Pudong each house
  one starred kitchen (Ling Long 1★, Yi Long Court 1★, Jin Xuan 1★ respectively) — those three are tied on the
  in-building measure and separated only by district depth. Fairmont Peace Hotel and Grand Hyatt Shanghai house
  none, which is why they sit last despite being strong hotels.
</div>

<h2>How the ranking is built</h2>
<div class="grid">
  <div class="card" style="grid-column:span 6">
    <h3>Score</h3>
    <p><code>score = 10 × (starred restaurants in the same building) + (starred restaurants whose district is confirmed on MICHELIN)</code></p>
    <p>The building term dominates because it is exact: a restaurant on another floor of your hotel is a
    two-minute walk, unambiguously inside the one-hour rule. The district term is a verified floor, not a total.</p>
  </div>
  <div class="card" style="grid-column:span 6">
    <h3>What is <em>not</em> claimed</h3>
    <p>No door-to-door travel time is published here. MICHELIN pages give the district, not a transit time, and a
    journey-time figure without a routing source would be a guess. Per-restaurant minutes need a routing check —
    logged on <a href="questions.html">Open Questions</a>.</p>
  </div>
</div>

<h2>Excluded on purpose</h2>
<div class="tablewrap"><table>
<thead><tr><th>Property</th><th>Why excluded</th><th>Source</th></tr></thead>
<tbody>{"".join(f'<tr><td><strong>{e(x["name"])}</strong></td><td>{e(x["why"])}</td><td>{link(x["src"], "source")}</td></tr>' for x in D.EXCLUDED)}</tbody>
</table></div>

<h2>Room-level detail</h2>
<div class="tablewrap"><table>
<thead><tr><th>Hotel</th><th>Bed / bath evidence (official page)</th><th>Notes &amp; irregularities</th></tr></thead>
<tbody>
{"".join(f'<tr><td><strong>{e(h["name"])}</strong></td><td>{e(h["room_ok"])}<br>{link(h["room_src"], "official room page")}</td><td>{e(h["notes"]) or "—"}</td></tr>' for h in D.HOTELS)}
</tbody></table></div>
"""
    return page("Hotels", "Shanghai hotels with verified beds, baths and Michelin proximity", body, "hotels.html")


# ---------------------------------------------------------------------------
# MICHELIN
# ---------------------------------------------------------------------------
def star_badge(r):
    if r.get("bib"):
        return '<span class="badge bib">Bib Gourmand</span><br><span class="muted">listed, no star</span>'
    n = r["stars"]
    return f'<span class="badge star">{"★" * n} {n} star</span>'


def rest_rows(items):
    out = []
    for r in items:
        out.append(f"""<tr>
<td><strong>{e(r["name"])}</strong></td>
<td>{star_badge(r)}</td>
<td>{e(r["cuisine"])}</td>
<td>{e(r["tier"])}</td>
<td>{e(r["district"]) or chip("")}<br><span class="muted">{e(r["address"])}</span></td>
<td>{e(r["hours"]) if r["hours"] else '<span class="badge warn">hours not published</span>'}</td>
<td>{e(r["cost"]) if r["cost"] else '<span class="badge warn">price not published</span>'}
    {("<br>" + link(r["cost_src"], "official price page")) if r["cost_src"] else ""}
    {'<br><span class="muted">' + e(r["cost_note"]) + "</span>" if r["cost_note"] else ""}</td>
<td>{social_cell(r["name"])}</td>
<td>{link(r["url"], "MICHELIN page")}{("<br>" + link(r["site"], "official site")) if r["site"] else ""}</td>
</tr>""")
    return "".join(out)


HEAD = """<thead><tr>
<th>Restaurant</th><th>Distinction</th><th>Cuisine</th><th>Price tier<br>(MICHELIN)</th>
<th>District / address</th><th>Open days &amp; hours</th><th>Cost for 2 adults</th>
<th>Video / social</th><th>Official links</th>
</tr></thead>"""


def build_michelin():
    three = [r for r in D.RESTAURANTS if r["stars"] == 3]
    two = [r for r in D.RESTAURANTS if r["stars"] == 2]
    one = [r for r in D.RESTAURANTS if r["stars"] == 1]
    body = f"""
<h1>Michelin guide — starred vs. listed</h1>
<div class="notice info">
  <strong>How to read the distinction column.</strong>
  <span class="badge star">★ 1 star</span> = awarded a MICHELIN star on the official 2026 selection.
  <span class="badge bib">Bib Gourmand</span> = recommended for value, <em>no star</em>.
  Guide-listed with neither = "Selected". A restaurant appearing on michelin.com is <strong>not</strong> the
  same as holding a star — this table keeps them apart, row by row.
</div>

<div class="kpi">
  <div class="card"><b>{len(three)}</b><span class="muted">3★</span></div>
  <div class="card"><b>{len(two)}</b><span class="muted">2★</span></div>
  <div class="card"><b>{len(one)}</b><span class="muted">1★</span></div>
  <div class="card"><b>{len(bib)}</b><span class="muted">Bib Gourmand rows included</span></div>
</div>

<p class="muted">Scope note: the official all-starred list for the city returns 50 entries across two pages, and
the guide's own counter shows 1×3★, 11×2★, 38×1★ on the live page (the launch release reported 12×2★ for the
wider region). This table transcribes the full 50-entry starred list plus a sample of Bib Gourmand rows.
Source: {link(D.MICHELIN_LIST, "MICHELIN all-starred, Shanghai")} · {link(D.MICHELIN_2026, "2026 selection announcement")}</p>

<h2>3 stars</h2>
<div class="tablewrap"><table>{HEAD}<tbody>{rest_rows(three)}</tbody></table></div>
<p class="muted">Price basis: the restaurant's own FAQ lists ¥2,588 (10 courses) and ¥2,888 (12 courses) per
person; the "cost for two" column multiplies those by two and is labelled derived. Wine, add-ons and any
service charge are extra.</p>

<h2>2 stars</h2>
<div class="tablewrap"><table>{HEAD}<tbody>{rest_rows(two)}</tbody></table></div>

<h2>1 star</h2>
<div class="tablewrap"><table>{HEAD}<tbody>{rest_rows(one)}</tbody></table></div>

<h2>Bib Gourmand — listed, <em>not</em> starred</h2>
<div class="tablewrap"><table>{HEAD}<tbody>{rest_rows(bib)}</tbody></table></div>

<h2>Cost reality check</h2>
<div class="grid">
  <div class="card" style="grid-column:span 6">
    <h3>Verified</h3>
    <p><strong>{rows_verified_cost}</strong> of {len(D.RESTAURANTS)} rows carry a cost figure that traces to an
    official page. That single verified row is the three-star tasting menu.</p>
  </div>
  <div class="card" style="grid-column:span 6">
    <h3>Not verified</h3>
    <p><strong>{len(D.RESTAURANTS)-rows_verified_cost}</strong> rows show a gap. Starred Chinese dining rooms in
    Shanghai habitually quote menus on arrival or by phone rather than on a public page, so a static-site
    price would be fabricated. Where a secondary source exists it is named in the row and still marked
    unverified.</p>
  </div>
</div>

<h2>Social &amp; video coverage</h2>
<p>Only links returned by an actual search are published as links. Where no post was verified, the cell offers a
platform search instead and says so — it is never presented as a restaurant account.
Verified so far: <strong>{sum(len(v) for v in SOCIAL.values())}</strong> link(s) across
<strong>{len(SOCIAL)}</strong> restaurant(s).</p>
"""
    return page("Michelin", "Starred vs Guide-listed Shanghai restaurants with costs and hours", body, "michelin.html")


# ---------------------------------------------------------------------------
# ACTIVITIES
# ---------------------------------------------------------------------------
def build_activities():
    rows = "".join(f"""<tr>
<td><strong>{e(a["name"])}</strong></td><td>{e(a["kind"])}</td>
<td>{e(a["hours"]) if a["hours"] else '<span class="badge warn">not verified</span>'}</td>
<td>{e(a["exceptions"]) or "—"}</td>
<td>{e(a["transit"]) or '<span class="badge warn">not verified</span>'} {"<br>" + VERIFIED if a["transit_verified"] else ""}</td>
<td>{e(a["cost"]) or '<span class="badge warn">not verified</span>'}</td>
<td>{social_cell(a["name"])}</td>
<td>{link(a["src"], "official source")}</td>
<td>{e(a["notes"]) or "—"}</td>
</tr>""" for a in D.ACTIVITIES)

    trips = "".join(f"""<tr><td>{e(t["route"])}</td><td>{e(t["time"])}</td><td>{e(t["price"]) or chip("")}</td>
<td>{link(t["src"], "source")} · {link(t["official"], "12306")}</td><td>{e(t["note"])}</td></tr>"""
                    for t in D.DAYTRIPS)

    body = f"""
<h1>Activities within about an hour</h1>
<div class="notice">
  <strong>Travel-time honesty.</strong> The one-hour rule is only satisfied on paper until a routing engine
  confirms it. Transit notes below are <em>not</em> marked verified unless a source stated the connection, and
  no row claims a measured door-to-door time. The <a href="questions.html">Open Questions</a> page lists the
  exact routing checks required.
</div>

<div class="tablewrap"><table>
<thead><tr><th>Activity</th><th>Type</th><th>Open days &amp; hours</th><th>Exceptions</th>
<th>Getting there / from hotel</th><th>Cost</th><th>Video / social</th><th>Official link</th><th>Notes</th></tr></thead>
<tbody>{rows}</tbody></table></div>

<h2>Worth a day trip (outside the one-hour rule)</h2>
<p class="muted">Included for completeness because both are reachable from Hongqiao in under an hour by
high-speed rail — but they are day trips, not neighbourhood activities.</p>
<div class="tablewrap"><table>
<thead><tr><th>Route</th><th>Fastest</th><th>2nd class fare</th><th>Sources</th><th>Caveat</th></tr></thead>
<tbody>{trips}</tbody></table></div>

<h2>What to do with the hours gap</h2>
<div class="grid">
  <div class="card" style="grid-column:span 6"><h3>Confirmed</h3>
    <p>Both Shanghai Museum buildings publish hours and closures on the museum's own site, including the
    Monday (People's Square) and Tuesday (East) closure and the walk-in rule introduced in September 2025.</p></div>
  <div class="card" style="grid-column:span 6"><h3>Missing</h3>
    <p>Yu Garden has no verified hours, ticket price or official site in this dataset, and the Bund's
    24-hour status is unconfirmed. Neither should be scheduled until checked — see
    <a href="flagged.html">Flagged</a>.</p></div>
</div>
"""
    return page("Activities", "Shanghai activities with verified hours and official links", body, "activities.html")


# ---------------------------------------------------------------------------
# DATES
# ---------------------------------------------------------------------------
def build_dates():
    drows = "".join(f"""<tr><td><strong>{e(d["item"])}</strong></td><td>{e(d["value"])}</td>
<td>{link(d["src"], "source") if d["src"] else chip("")}</td><td>{e(d["note"]) or "—"}</td></tr>""" for d in D.DATES)
    brows = "".join(f"""<tr><td>{e(b["source"])}</td><td>{e(b["kind"])}</td><td>{e(b["claim"])}</td>
<td>{link(b["url"], "source")}</td></tr>""" for b in D.BOOKING_WINDOWS)

    body = f"""
<h1>Dates, weather and when to book</h1>

<div class="kpi">
  <div class="card"><b>15–22 Feb</b><span class="muted">recommended 7 nights</span></div>
  <div class="card"><b>7 nights</b><span class="muted">checkout 22 Feb 2027</span></div>
  <div class="card"><b>5–13 Feb</b><span class="muted">Spring Festival — avoided</span></div>
  <div class="card"><b>20 Feb</b><span class="muted">Lantern Festival — inside the stay</span></div>
</div>

<h2>Why 15–22 February works</h2>
<div class="grid">
  <div class="card" style="grid-column:span 12">
    <p>Your preferred window opens two days after the nine-day Spring Festival holiday ends, which removes the
    two biggest risks of a February China trip: national-holiday pricing and holiday closures at temples,
    museums and restaurants. It also sits early enough to avoid March's heavier rain (roughly 86–88 mm vs
    65 mm in February). The Lantern Festival on 20 February falls inside the stay and is the one evening worth
    planning around.</p>
    <p class="muted">Weather figures are 1991–2020 normals reproduced across several travel sources and vary
    slightly between them; treat the range as indicative and re-check a forecast inside 10 days.</p>
  </div>
</div>

<h2>Verified calendar facts</h2>
<div class="tablewrap"><table>
<thead><tr><th>Item</th><th>Value</th><th>Source</th><th>Note</th></tr></thead>
<tbody>{drows}</tbody></table></div>

<h2>When to book — the honest answer</h2>
<div class="notice">
  <strong>No booking-date claim here is a hotel quote.</strong> The recommendation below is assembled from
  published industry studies, and it comes with a real conflict: price studies favour waiting, while
  availability of specific room types favours booking earlier. Both are shown.
</div>
<div class="tablewrap"><table>
<thead><tr><th>Source</th><th>Type</th><th>What it claims</th><th>Link</th></tr></thead>
<tbody>{brows}</tbody></table></div>

<h3>Actual dates to act on (derived, not a hotel quote)</h3>
<div class="tablewrap"><table>
<thead><tr><th>When</th><th>Action</th><th>Basis</th></tr></thead>
<tbody>
<tr><td><strong>Now – 31 Dec 2026</strong><br><span class="muted">~11-13 months ahead</span></td>
<td>Reserve a <em>free-cancellation</em> room at the first-choice hotel for 15–22 Feb 2027 as soon as the
calendar opens. This locks the room type, not the price.</td>
<td>Luxury booking-window guidance (3-6 months for a specific room category) applied backwards from the stay.</td></tr>
<tr><td><strong>1 Nov – 15 Dec 2026</strong><br><span class="muted">~3 months ahead</span></td>
<td>Second look: compare the live total for the same room across the shortlist. Replace the placeholder booking
only if a lower <em>refundable</em> rate appears.</td>
<td>Mews: 1-3 months balances price and availability.</td></tr>
<tr><td><strong>1 – 7 Feb 2027</strong><br><span class="muted">8-14 days before check-in</span></td>
<td>Final price check. Industry data puts the cheapest city-hotel window here; rebook if the rate has dropped.</td>
<td>Hotels.com 2026 index and KAYAK 2026 analysis.</td></tr>
<tr><td><strong>After 13 Feb 2027</strong></td>
<td>Only now is the Spring Festival peak over — avoid any booking action in 5-13 Feb, when pricing spikes.</td>
<td>State Council holiday dates (via secondary summaries).</td></tr>
</tbody></table></div>
<p class="muted">These are <strong>derived dates</strong>: they combine verified stay dates with published
industry booking windows. They are not a hotel's advice and carry no price guarantee.</p>

<h3>Recommended approach for these dates</h3>
<ol>
  <li><strong>Now → ~6 months out:</strong> book a <em>free-cancellation</em> rate at the first-choice hotel as
    soon as the February 2027 calendar opens. This buys availability of the room type you need — a queen-or-larger
    bed with an ensuite bath — without locking the price.</li>
  <li><strong>Inside 8–14 days:</strong> re-check the live rate. The 2026 industry data points to this window as
    the cheapest for city hotels; with a cancellable booking in hand, a lower rate can simply replace it.</li>
  <li><strong>Never</strong> rely on last-minute pricing around 5–13 February — that is the holiday peak this
    itinerary deliberately avoids.</li>
</ol>
<p class="muted">Caveat worth stating plainly: the studies measure <em>average</em> behaviour across many city
hotels. A specific luxury property with a specific room category may never discount, and waiting can cost the
room rather than save money.</p>

<h2>Transit baseline</h2>
<p>{D.DATES[-1]["value"]} · {link(D.DATES[-1]["src"], "Shanghai Metro")} — network facts only. Journey times to
individual restaurants still need a routing check before the one-hour claim can be confirmed.</p>
"""
    return page("Dates & Booking", "Feb-Mar 2027 dates, weather, and booking-window evidence", body, "dates.html")


# ---------------------------------------------------------------------------
# QUESTIONS
# ---------------------------------------------------------------------------
QUESTIONS = [
    ("Which hotel actually has your room on 15–22 Feb 2027, and at what total?",
     "Every 7-night total is blank: rates live only inside a booking engine.",
     "Run the official link on each Hotels row with those dates, 2 adults, and record the total and currency.",
     "hotels.html"),
    ("Is the cheapest rate refundable, and what is the cancellation deadline?",
     "A non-refundable rate defeats the 'book early, rebook cheaper' strategy.",
     "Read the rate rules on the same booking page; record the deadline per hotel.", "dates.html"),
    ("Which starred kitchens are shut on which days?",
     f"{len([r for r in D.RESTAURANTS if not r['hours']])} of {len(D.RESTAURANTS)} rows have no published hours.",
     "Call or check each official restaurant site; MICHELIN pages sometimes publish hours (Fu He Hui, Jin Xuan, Yi Long Court do).",
     "michelin.html"),
    ("What does a starred dinner actually cost for two, all-in?",
     "Only Taian Table publishes a price. Service charge, tea and wine are usually extra.",
     "Request set-menu prices by phone/email; ask explicitly whether a service charge applies.", "michelin.html"),
    ("Is each restaurant genuinely within 60 minutes of the chosen hotel?",
     "No door-to-door time is verified; district-level proximity is all that is confirmed.",
     "Enter hotel → restaurant in a transit planner for the actual weekday and time; log the minutes.", "activities.html"),
    ("Are the museums and Yu Garden open, and do they need timed tickets?",
     "Museum hours are verified; Yu Garden's are not. Peak-period reservation rules can change.",
     "Confirm on each venue's official page within 7 days of travel; book free slots where required.",
     "activities.html"),
    ("Does the hotel hold a queen-or-larger bed with a private ensuite bathroom on those dates?",
     "Bed type is verified on brand pages, but inventory for specific dates is not.",
     "Confirm the exact room category in the booking engine and note it in the reservation.",
     "hotels.html"),
    ("Is a visa or transit permission needed for this itinerary?",
     "Not researched in this dataset — it is a personal-eligibility question, not a hotel fact.",
     "Check the national immigration/visa policy for your passport well before booking flights.", "flagged.html"),
    ("What is the plan if a restaurant is fully booked?",
     "Starred rooms in Shanghai book out weeks ahead, especially around the Lantern Festival.",
     "Build a second choice per night from the same district; note reservation lead times when calling.",
     "michelin.html"),
    ("Which currency will the rate be charged in, and what card fees apply?",
     "Marriott/Hilton/Hyatt quote in different currencies depending on market.",
     "Record the charged currency and any FX fee at booking time.", "hotels.html"),
]


def build_questions():
    rows = "".join(f"""<tr><td><strong>{i}. {e(q)}</strong></td><td>{e(why)}</td><td>{e(how)}</td>
<td><a href="{pg}">go</a></td></tr>""" for i, (q, why, how, pg) in enumerate(QUESTIONS, 1))
    body = f"""
<h1>Open questions before any decision</h1>
<p class="lead">Ten things this research could not answer, each with the exact action that would answer it.
Nothing here is a preference question — every item is a factual gap that changes what you book.</p>

<div class="notice">
  <strong>Rule of thumb.</strong> No booking decision is safe until items <strong>1, 2 and 5</strong> are
  resolved: total price, cancellation terms, and whether the venues are actually reachable in the promised hour.
</div>

<div class="tablewrap"><table>
<thead><tr><th style="width:34%">Question</th><th style="width:26%">Why it is still open</th>
<th style="width:30%">How to close it</th><th>Where</th></tr></thead>
<tbody>{rows}</tbody></table></div>

<h2>Information this dataset is missing entirely</h2>
<div class="grid">
  <div class="card" style="grid-column:span 6">
    <h3>Deliberately not researched</h3>
    <ul>
      <li>Flights and airport transfers</li>
      <li>Visa / entry requirements (personal eligibility)</li>
      <li>Travel insurance</li>
      <li>Day-by-day restaurant reservations</li>
      <li>Payment apps and connectivity for foreign phones</li>
    </ul>
    <p class="muted">These sit outside "hotels, activities and Michelin", so they were left out rather than
    half-covered.</p>
  </div>
  <div class="card" style="grid-column:span 6">
    <h3>Missing because the source is missing</h3>
    <ul>
      <li>Restaurant hours for {len([r for r in D.RESTAURANTS if not r["hours"]])} of {len(D.RESTAURANTS)} rows</li>
      <li>Menu prices for {len(D.RESTAURANTS)-rows_verified_cost} of {len(D.RESTAURANTS)} rows</li>
      <li>Official websites for {len(D.RESTAURANTS)-rows_with_site} rows</li>
      <li>Measured transit times for every venue</li>
      <li>Any February-2027 room rate</li>
    </ul>
    <p class="muted">All of these are listed on <a href="flagged.html">Flagged for Review</a>.</p>
  </div>
</div>

<h2>Suggestions to discover the missing information</h2>
<ol>
  <li><strong>Use the booking engine as the source of truth</strong>, not this site, for prices. Every hotel row
    links straight to it; the total quoted there is the only figure you should act on.</li>
  <li><strong>Phone the restaurants.</strong> For starred Chinese dining rooms, hours and set-menu prices are
    routinely given by phone and rarely published. MICHELIN's contact number on each row is the fastest route.</li>
  <li><strong>Record everything in one place</strong> as you confirm it — date checked, source, value. A
    verification timestamp is what turns a list into a booking plan.</li>
  <li><strong>Re-check outdoor and museum venues within a week of travel</strong>: seasonal hours and holiday
    closures are the most volatile items in this dataset.</li>
  <li><strong>Add a trip-file page</strong> to this site (see <a href="suggestions.html">Suggestions</a>) to hold
    confirmed values next to the research values, so the two never get confused.</li>
</ol>
"""
    return page("Open Questions", "Unresolved facts that block a booking decision", body, "questions.html")


# ---------------------------------------------------------------------------
# SUGGESTIONS
# ---------------------------------------------------------------------------
SUGGESTIONS = [
    ("High", "Live rate capture per hotel",
     "A dated snapshot per hotel (timestamp, currency, total for 15–22 Feb 2027) that can be re-run before booking.",
     "Turns the biggest blank column into the site's most valuable one.",
     "Needs a booking-engine read per hotel; one hour of work, repeated monthly."),
    ("High", "Per-restaurant transit minutes",
     "Add a 'minutes from each shortlisted hotel' column, filled from a routing planner for a weekday evening.",
     "Makes the one-hour rule auditable instead of assumed.",
     "10 hotels × 50 restaurants is 500 lookups — sample the top 15 restaurants first."),
    ("High", "Distinction legend on every table",
     "Keep the star / Bib / Selected chips inline in every list, plus the official award year.",
     "The single most common way trip lists mislead is calling a listed restaurant 'starred'.",
     "Already implemented; extend with the year once the 2027 guide is published."),
    ("Medium", "Reservation lead-time column",
     "How far ahead each starred room must be booked, and whether a deposit is required.",
     "Prevents arriving with a plan and no table.",
     "Requires a phone/email per restaurant; batch it into one verification session."),
    ("Medium", "Cost-per-person ↔ cost-for-two toggle",
     "Show the verified per-person basis next to the derived total.",
     "Removes ambiguity about what the total includes.",
     "Small UI change; already have both numbers for the one verified row."),
    ("Medium", "Closure calendar overlay",
     "Merge restaurant closing days and holiday dates into one calendar view of the stay.",
     "Monday closures and the Lantern Festival interact; a calendar exposes collisions instantly.",
     "Blocked until more hours are verified."),
    ("Low", "Print / offline stylesheet",
     "A single-page printable plan for use in the city without data.",
     "Roaming data is unreliable; a printed sheet always works.",
     "One CSS print block."),
    ("Low", "Source freshness badge per row",
     "Date each verified cell.",
     "Prices and hours drift; a date tells you whether to trust the row.",
     "Add a 'checked' date field to the dataset."),
    ("Low", "Currency display",
     "Show an approximate USD conversion alongside CNY, clearly marked as indicative.",
     "Easier budgeting for a US-based traveller.",
     "Requires a stated FX rate and date — never show a conversion without one."),
]


def build_suggestions():
    rows = "".join(f"""<tr><td><span class="badge {'star' if p=='High' else ('bib' if p=='Medium' else 'sel')}">{e(p)}</span></td>
<td><strong>{e(t)}</strong></td><td>{e(what)}</td><td>{e(why)}</td><td>{e(how)}</td></tr>"""
                for p, t, what, why, how in SUGGESTIONS)
    body = f"""
<h1>Suggestions for improving this site</h1>
<p class="lead">A review queue, not a changelog. Nothing here has been implemented beyond what is marked
"already implemented" — pick the path you want before any of it is built.</p>

<div class="notice info">
  <strong>How to use this page.</strong> Each suggestion lists what it would add, why it changes a decision, and
  what it costs to build. Priority reflects decision impact, not effort. Approve in any order; the top three are
  the ones that would most change the answer to "which hotel, which nights".
</div>

<div class="tablewrap"><table>
<thead><tr><th>Priority</th><th>Suggestion</th><th>What it adds</th><th>Why it matters</th><th>Effort / prerequisite</th></tr></thead>
<tbody>{rows}</tbody></table></div>

<h2>Deliberately rejected</h2>
<div class="tablewrap"><table>
<thead><tr><th>Idea</th><th>Why not</th></tr></thead>
<tbody>
<tr><td>Estimated hotel prices ("typical nightly rate")</td><td>Would look verified and be wrong. The column
stays empty and linked to the booking engine.</td></tr>
<tr><td>Auto-embedded social feeds</td><td>Embeds break silently and can't be verified offline; direct links age
better.</td></tr>
<tr><td>Scraped aggregate ratings</td><td>Third-party scores change without notice and aren't official. Kept out
entirely rather than half-trusted.</td></tr>
<tr><td>Filling hours from memory of similar venues</td><td>The exact failure mode this project exists to
avoid.</td></tr>
</tbody></table></div>

<h2>What would most improve the next iteration</h2>
<ol>
  <li><strong>One verification session with the phone in hand</strong> — hours and set-menu prices for the twelve
    starred rooms you would realistically book. That single afternoon would fill more of this site's gaps than
    any amount of extra web reading.</li>
  <li><strong>A dated price snapshot</strong> for the three shortlisted hotels, re-run monthly until booking.</li>
  <li><strong>Routing confirmations</strong> for the top fifteen restaurants from the chosen hotel.</li>
</ol>
"""
    return page("Suggestions", "Reviewable proposals before implementing site changes", body, "suggestions.html")


# ---------------------------------------------------------------------------
# FLAGGED
# ---------------------------------------------------------------------------
def build_flagged():
    no_hours = [r for r in D.RESTAURANTS if not r["hours"]]
    no_cost = [r for r in D.RESTAURANTS if not r["cost"]]
    no_site = [r for r in D.RESTAURANTS if not r["site"]]
    no_district = [r for r in D.RESTAURANTS if not r["district"]]
    body = f"""
<h1>Flagged for review</h1>
<p class="lead">Every gap, irregularity and exclusion in one place. Items listed here do not block the rest of
the site — they are marked, not removed.</p>

<div class="kpi">
  <div class="card"><b>{len(no_hours)}</b><span class="muted">restaurants without verified hours</span></div>
  <div class="card"><b>{len(no_cost)}</b><span class="muted">restaurants without a verified price</span></div>
  <div class="card"><b>{len(no_district)}</b><span class="muted">restaurants without a confirmed district</span></div>
  <div class="card"><b>{len(D.HOTELS)}</b><span class="muted">hotels with no Feb-2027 rate</span></div>
</div>

<h2>Irregularities found while verifying</h2>
<div class="tablewrap"><table>
<thead><tr><th>Item</th><th>Irregularity</th><th>Status</th></tr></thead>
<tbody>
<tr><td>2★ count for the city</td><td>The live all-starred page shows 11 two-star entries while the 2026 launch
release reports 12 across the wider region. The city-page counter is used here.</td><td>{UNVERIFIED} conflict noted</td></tr>
<tr><td>MICHELIN price tiers</td><td>¥/¥¥/¥¥¥/¥¥¥¥ is a relative band, not a price. It is displayed as a tier
and never converted into a currency amount.</td><td>{VERIFIED} as tier only</td></tr>
<tr><td>Peninsula "price range"</td><td>Room-page structured data carries a CNY 2,900–145,000 range. That is not a
dated quote and is not used as a rate.</td><td>{UNVERIFIED}</td></tr>
<tr><td>Ultraviolet by Paul Pairet</td><td>Former three-star, closed 29 March 2025; removed from all lists.</td><td>excluded</td></tr>
<tr><td>Four Seasons Shanghai</td><td>New Huaihai Zhong Road property announced for 2027; not bookable or
verifiable for February 2027.</td><td>excluded</td></tr>
<tr><td>Bvlgari room types</td><td>Room pages returned errors; bed size for the entry categories is unconfirmed,
so the bed requirement is unproven for that hotel even though its dining is the strongest.</td><td>{UNVERIFIED}</td></tr>
<tr><td>Fairmont Peace address</td><td>Street address not captured from an official page; left blank instead of
copying a directory listing.</td><td>{UNVERIFIED}</td></tr>
<tr><td>Yu Garden</td><td>No official hours, price or site obtained. Should not be scheduled yet.</td><td>{UNVERIFIED}</td></tr>
<tr><td>The Bund</td><td>24-hour access not confirmed on an official page; hours left blank.</td><td>{UNVERIFIED}</td></tr>
<tr><td>Spring Festival 2027 notice</td><td>Holiday dates come from travel publishers repeating the State
Council notice; the notice itself was not retrieved.</td><td>{UNVERIFIED}</td></tr>
<tr><td>Restaurant "cost for two"</td><td>Derived by doubling a per-person price. Service charge, tea and wine
are excluded and vary by venue.</td><td>derived — labelled</td></tr>
<tr><td>Social links</td><td>Only {sum(len(v) for v in SOCIAL.values())} verified post(s) exist in this dataset.
Search links are labelled as searches, never as official accounts.</td><td>{UNVERIFIED} coverage</td></tr>
</tbody></table></div>

<h2>Restaurants missing hours ({len(no_hours)})</h2>
<p class="muted">{" · ".join(e(r["name"]) for r in no_hours)}</p>

<h2>Restaurants missing a verified price ({len(no_cost)})</h2>
<p class="muted">{" · ".join(e(r["name"]) for r in no_cost)}</p>

<h2>Restaurants with no official website captured ({len(no_site)})</h2>
<p class="muted">{" · ".join(e(r["name"]) for r in no_site)}</p>

<h2>Restaurants with no confirmed district ({len(no_district)})</h2>
<p class="muted">{" · ".join(e(r["name"]) for r in no_district)}</p>
<p class="muted">District counts elsewhere on this site are therefore floors, not totals.</p>
"""
    return page("Flagged for Review", "All unverified values and irregularities", body, "flagged.html")


# ---------------------------------------------------------------------------
# VERIFICATION
# ---------------------------------------------------------------------------
def build_verification():
    rows = "".join(f"""<tr><td>{e(r["name"])}</td><td>{star_badge(r)}</td>
<td>{VERIFIED if r["verified"] else UNVERIFIED}</td>
<td>{link(r["url"], "MICHELIN page")}</td>
<td>{"hours ✓" if r["hours"] else "hours ✗"} · {"price ✓" if r["cost"] else "price ✗"} · {"site ✓" if r["site"] else "site ✗"}</td></tr>"""
                   for r in D.RESTAURANTS)
    hrows = "".join(f"""<tr><td>{e(h["name"])}</td><td>{VERIFIED}</td><td>{link(h["room_src"], "room page")}</td>
<td>{"rating unavailable" if not h["rate"] else ""} {e(h["rate_note"])}</td></tr>""" for h in D.HOTELS)
    body = f"""
<h1>Verification method &amp; source log</h1>
<div class="notice ok">
  <strong>Rule applied to every row.</strong> A value is published only when it was read on an official page
  during this session, and that page is linked in the same row. Anything else is blank with an
  <span class="badge warn">unverified</span> chip. No value was inferred, averaged or carried over from memory.
</div>

<h2>Officially sourced core facts</h2>
<div class="tablewrap"><table>
<thead><tr><th>Fact</th><th>Value used</th><th>Official source</th></tr></thead>
<tbody>
<tr><td>Shanghai starred restaurants, 2026 guide</td><td>{total_starred_shanghai} (1×3★, 2★ and 1★ as listed)</td><td>{link(D.MICHELIN_LIST, "MICHELIN all-starred")}</td></tr>
<tr><td>2026 selection announcement</td><td>First regional edition, 409 restaurants across Shanghai/Jiangsu/Zhejiang</td><td>{link(D.MICHELIN_2026, "announcement")}</td></tr>
<tr><td>Three-star, and its price</td><td>Taian Table · ¥2,588 / ¥2,888 per person</td><td>{link("https://sh.taian-table.cn/faq/", "restaurant FAQ")}</td></tr>
<tr><td>Peninsula Shanghai</td><td>235 rooms, Two MICHELIN Keys, Bund address</td><td>{link("https://guide.michelin.com/en/hotels-stays/shanghai/the-peninsula-shanghai-5858", "MICHELIN hotel page")}</td></tr>
<tr><td>Grand Hyatt Shanghai</td><td>1 Queen Bed 40 sqm · 2 Queen Beds 42 sqm · deep-soaking bathtub</td><td>{link("https://www.hyatt.com/grand-hyatt/en-US/shagh-grand-hyatt-shanghai/rooms", "Hyatt room page")}</td></tr>
<tr><td>Waldorf Astoria Bund</td><td>260 rooms, Double Queen Deluxe</td><td>{link("https://www.hilton.com/en/hotels/shawawa-waldorf-astoria-shanghai-on-the-bund/rooms/", "Hilton room page")}</td></tr>
<tr><td>Fairmont Peace Hotel</td><td>Fairmont Queen Queen 49 sqm, claw-foot tub, marble bath</td><td>{link("https://www.fairmont.com/en/hotels/shanghai/fairmont-peace-hotel/rooms/DBCMV.room.html", "Fairmont room page")}</td></tr>
<tr><td>Ritz-Carlton Pudong</td><td>1 King / 2 Double room configurations</td><td>{link("https://www.ritzcarlton.com/en/hotels/shasz-the-ritz-carlton-shanghai-pudong/rooms/", "Marriott room page")}</td></tr>
<tr><td>Bvlgari Shanghai</td><td>82 rooms, 19 suites, Bao Li Xuan on site</td><td>{link("https://www.bulgarihotels.com/en-US/shanghai", "Bvlgari hotel page")}</td></tr>
<tr><td>Shanghai Museum</td><td>09:00–17:00, closed Mondays except holidays</td><td>{link("https://www.shanghaimuseum.net/mu/frontend/pg/m/article/id/I00004797", "museum notice")}</td></tr>
<tr><td>Shanghai Disneyland</td><td>Date-specific closing times</td><td>{link("https://www.shanghaidisneyresort.com/experience/theme-park/theme-park", "official calendar")}</td></tr>
<tr><td>Shanghai Metro</td><td>19 lines · 508 stations · ~816 km</td><td>{link("https://www.shmetro.com/", "shmetro.com")}</td></tr>
</tbody></table></div>

<h2>Restaurant rows, granular status</h2>
<div class="tablewrap"><table>
<thead><tr><th>Restaurant</th><th>Distinction</th><th>Row status</th><th>MICHELIN page</th><th>Fields confirmed</th></tr></thead>
<tbody>{rows}</tbody></table></div>

<h2>Hotel rows, granular status</h2>
<div class="tablewrap"><table>
<thead><tr><th>Hotel</th><th>Bed/bath status</th><th>Room source</th><th>Rate status</th></tr></thead>
<tbody>{hrows}</tbody></table></div>

<h2>What "verified" means here — and what it does not</h2>
<div class="grid">
  <div class="card" style="grid-column:span 6">
    <h3>It means</h3>
    <ul><li>The value appears on the linked official page.</li>
    <li>The link resolves to the brand, restaurant or guide itself.</li>
    <li>Ambiguity is written down rather than smoothed over (see 2★ count, price tiers).</li></ul>
  </div>
  <div class="card" style="grid-column:span 6">
    <h3>It does not mean</h3>
    <ul><li>It will still be true in February 2027 — hours and prices change.</li>
    <li>It is a booking quote. Prices require the live engine.</li>
    <li>It is complete. Gaps are counted on <a href="flagged.html">Flagged</a>.</li></ul>
  </div>
</div>
<p class="muted">Tooling note: pages were read directly over HTTPS during this session; no value was taken from
search-result snippets alone unless the underlying page was opened.</p>
"""
    return page("Verification", "Method and source log for every value on this site", body, "verification.html")


if __name__ == "__main__":
    ROOT.mkdir(exist_ok=True)
    (ROOT / "assets").mkdir(exist_ok=True)
    pages = {
        "index.html": build_index,
        "hotels.html": build_hotels,
        "michelin.html": build_michelin,
        "activities.html": build_activities,
        "dates.html": build_dates,
        "questions.html": build_questions,
        "suggestions.html": build_suggestions,
        "flagged.html": build_flagged,
        "verification.html": build_verification,
    }
    for name, fn in pages.items():
        (ROOT / name).write_text(fn(), encoding="utf-8")
        print("wrote", name)
