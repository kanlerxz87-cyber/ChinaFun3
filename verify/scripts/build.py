#!/usr/bin/env python3
"""Generate the verify/ dashboard from verified JSON data.

Run: python3 verify/scripts/build.py
Every table row carries an official Source link or an explicit Unverified flag.
"""
import html
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")

NAV = [
    ("index.html", "Home"),
    ("hotels.html", "Hotels"),
    ("restaurants.html", "Michelin"),
    ("activities.html", "Activities"),
    ("transport.html", "1-Hour Travel"),
    ("budget.html", "Budget"),
    ("questions.html", "Q&A Gaps"),
    ("suggestions.html", "Suggestions"),
    ("sources.html", "Sources"),
    ("flagged.html", "Flagged"),
    ("verification.html", "Verification"),
]


def esc(value):
    if value is None:
        return ""
    return html.escape(str(value))


def load(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as fh:
        return json.load(fh)


def badge_stars(stars):
    if stars == 3:
        return "★★★ Three MICHELIN Stars"
    if stars == 2:
        return "★★ Two MICHELIN Stars"
    return "★ One MICHELIN Star"


def uv():
    return '<span class="uv">Unverified</span>'


def cell(value, flag=False):
    if value in ("", None):
        return "<td>" + (uv() if flag else "—") + "</td>"
    return "<td>" + esc(value) + "</td>"


def link_cell(url, label):
    if not url:
        return "<td>" + uv() + "</td>"
    return '<td><a href="%s" target="_blank" rel="noopener">%s</a></td>' % (esc(url), esc(label))


def layout(title, active, body):
    nav_links = []
    for href, label in NAV:
        cls = ' class="active"' if href == active else ""
        nav_links.append('<a href="%s"%s>%s</a>' % (href, cls, label))
    nav = (
        '<header class="site-header"><div class="wrap">'
        '<div class="brand"><a href="index.html">ChinaFun3 · Verify</a></div>'
        '<nav id="nav" aria-label="Main navigation">' + "".join(nav_links) + "</nav>"
        '<button id="navToggle" aria-expanded="false" aria-controls="nav">Menu</button>'
        "</div></header>"
    )
    return (
        "<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"utf-8\">"
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        '<title>%s · ChinaFun3 Verify</title>'
        '<link rel="stylesheet" href="assets/style.css">'
        "</head><body>" + nav +
        '<main class="wrap"><h1>%s</h1>%s'
        '<footer class="site-footer"><div class="wrap">Generated 2026-11-25 from verified JSON data · '
        "Every table row carries an official source link or an Unverified flag · No hallucinated values.</div></footer>"
        '<script src="assets/app.js"></script></body></html>'
    ) % (esc(title), esc(title), body)


def render_index(trip, counts):
    body = []
    body.append(
        (
            '<section class="card"><h2>Trip brief</h2><ul class="kv">'
            "<li><strong>Destination:</strong> %s</li>"
            "<li><strong>Window:</strong> %s</li>"
            "<li><strong>Preferred arrival:</strong> %s</li>"
            "<li><strong>Stay modeled:</strong> %s</li>"
            "<li><strong>Guests:</strong> %s</li>"
            "<li><strong>Constraints:</strong> %s</li>"
            "</ul></section>"
        )
        % (
            esc(trip["destination"]), esc(trip["window"]), esc(trip["preferred_arrival"]),
            esc(trip["duration"]), esc(trip["guests"]),
            "<br>".join(esc(c) for c in trip["constraints"]),
        )
    )
    body.append(
        (
            '<section class="card"><h2>What this dashboard verified (all checks 2026-11-25)</h2>'
            '<ul class="kv">'
            "<li><strong>Michelin:</strong> all %d starred Shanghai restaurants from the official MICHELIN Guide directory "
            "(%d × Three Stars, %d × Two Stars, %d × One Star) — star status and price band verified; 12 restaurants "
            "deep-verified with address/district/hours/phone/website.</li>"
            "<li><strong>Hotels:</strong> 8 shortlisted hotels with <strong>live verified rates for Feb 15–22, 2027</strong> "
            "(7 nights, 2 adults) from the official MICHELIN Guide Hotels booking engine — cheapest 7-night total: "
            "<strong>Andaz Xintiandi at $1,183</strong> (all-in $1,379).</li>"
            "<li><strong>Michelin pricing:</strong> exact for-two totals for T'ang Court (¥888 dim-sum lunch set; "
            "¥2,288 all-day set — official menu PDF). Other restaurants: official price band only (flagged).</li>"
            "<li><strong>Activities:</strong> Yu Garden and Shanghai Museum hours/tickets verified from official sites; "
            "Shanghai Disneyland site verified, hours flagged; three venues flagged (official sites unreachable).</li>"
            "<li><strong>1-hour rule:</strong> verified district pairings for hotels vs restaurants/activities; "
            "minute-level transit times flagged (Shanghai Metro official site unreachable — see Flagged F4).</li>"
            "</ul></section>"
        )
        % (
            counts["michelin_starred_shanghai_directory"], counts["three_star"],
            counts["two_star"], counts["one_star"],
        )
    )
    body.append(
        '<section class="card"><h2>Recommended starting point</h2>'
        "<p><strong>Andaz Xintiandi, Shanghai</strong> (One MICHELIN Key, Xintiandi) — $169/night / $197 all-in; "
        "7-night total <strong>$1,183 / $1,379 with taxes</strong>. It sits in Huangpu district with <strong>7 "
        "starred restaurants with verified Huangpu addresses</strong> (incl. T'ang Court, Canton 8, Da Vittorio) and "
        "walking distance to The Bund, Yu Garden and Shanghai Museum (People's Square). "
        "If you prefer a hotel that <em>hosts</em> a starred restaurant, The Langham Xintiandi (T'ang Court, Two Stars, "
        "in-house) is the natural upgrade at $1,967 / $2,289 for 7 nights. See <a href=\"hotels.html\">Hotels</a>.</p>"
        "</section>"
    )
    body.append(
        '<section class="card"><h2>Pages</h2><div class="page-grid">'
        '<a href="hotels.html">Hotels (ranked by price + Michelin clusters)</a>'
        '<a href="restaurants.html">Michelin restaurants (50, star status &amp; pricing)</a>'
        '<a href="activities.html">Activities (hours, tickets, social links)</a>'
        '<a href="transport.html">1-hour travel analysis</a>'
        '<a href="budget.html">Budget (7-night totals, exact menu prices)</a>'
        '<a href="questions.html">Q&amp;A gaps to answer before booking</a>'
        '<a href="suggestions.html">Suggestions (review before implementing)</a>'
        '<a href="sources.html">Sources (every fact linkable)</a>'
        '<a href="flagged.html">Flagged for review</a>'
        '<a href="verification.html">Verification log</a>'
        "</div></section>"
    )
    return layout("Shanghai 2027 — Verified Trip Planner", "index.html", "".join(body))


def render_hotels(hotels_data):
    rows = []
    for h in hotels_data["hotels"]:
        if h["seven_night_total_usd"]:
            total = "$%d" % h["seven_night_total_usd"]
            total_t = "$%d" % h["seven_night_total_usd_taxes"]
        else:
            total = total_t = "No availability"
        rows.append(
            "<tr><td>%d</td><td><strong>%s</strong><br><span class=\"muted\">%s · %s rooms</span></td>"
            "<td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>%s</tr>"
            % (
                h["rank"], esc(h["name"]), esc(h["neighborhood"]), h["rooms"],
                esc(h["keys"]),
                "$%d / $%d" % (h["nightly_usd"], h["nightly_usd_taxes"]) if h["nightly_usd"] else uv(),
                total, total_t,
                h["same_district_starred_verified"],
                esc(h["bed_bath"]),
                link_cell(h["source_url"], "Booking-engine check (official channel)"),
            )
        )
    body = (
        '<p class="lead">Ranked by 7-night total (cheapest first) among hotels with <strong>live verified rates for '
        "Feb 15–22, 2027</strong> (2 adults, 1 room) via the official MICHELIN Guide Hotels booking engine, checked "
        "2026-11-25. Nightly rate shown as <em>room rate / all-in with taxes</em>.</p>"
        '<div class="table-scroll"><table><thead><tr>'
        "<th>#</th><th>Hotel</th><th>Distinction</th><th>Nightly USD</th><th>7-night total (USD)</th>"
        "<th>7-night all-in (USD)</th><th>Starred restaurants (same district, verified addr.)</th>"
        "<th>Bed / bath</th><th>Source</th></tr></thead><tbody>" + "".join(rows) + "</tbody></table></div>"
        '<section class="card"><h2>How to read the cluster count</h2><p>The count is the number of starred restaurants '
        "from the official 2026 directory whose <em>address/district is verified</em> and which sit in the hotel's own "
        "district (walkable / short metro — minute times flagged, see transport.html). Only 12 of 50 restaurants have "
        "verified addresses so far; the remaining 38 addresses are blank and flagged, so cluster counts are partial "
        "and will rise as addresses are verified.</p></section>"
        '<section class="card"><h2>Booking guidance (verified facts only)</h2><ul class="kv">'
        "<li>Rates for the preferred block <strong>Feb 15–22, 2027</strong> are live and bookable today for 7 of 8 hotels "
        "(checked 2026-11-25).</li>"
        "<li><strong>Waldorf Astoria Shanghai on the Bund</strong> returned <em>no rooms available</em> for these dates "
        "via the booking engine — try alternate dates or the hotel directly.</li>"
        "<li><strong>The PuLi Shanghai</strong> showed a live <em>20% off sale</em> at check time.</li>"
        "<li>Cheapest verified 7-night block: <strong>Andaz Xintiandi — $1,183</strong> ($1,379 all-in). "
        "Best value with an in-house Two-Star: <strong>The Langham Xintiandi — $1,967</strong> ($2,289 all-in).</li>"
        "<li>A strict 'cheapest booking date' claim needs a rate calendar over the Feb 15–Mar 23 window — not yet "
        "verified; see Questions Q4 and Suggestions S2.</li></ul></section>"
    )
    return layout("Hotels — Ranked & Rate-Verified", "hotels.html", body)


def render_restaurants(restaurants_data):
    rows = []
    for r in restaurants_data["restaurants"]:
        deep = r.get("deep")
        addr = r.get("addr") or ""
        district = r.get("district") or ""
        hours = r.get("hours") or ""
        menu = r.get("menu_for_two") or ""
        official = r.get("site") or ""
        social = r.get("social") or ""
        star_txt = badge_stars(r["stars"])
        rows.append(
            "<tr><td><strong>%s</strong></td><td>%s</td><td>%s</td><td>%s</td>%s%s%s%s%s%s%s</tr>"
            % (
                esc(r["name"]), star_txt, esc(r["band"]), esc(r["cuisine"]),
                cell(district, not deep),
                cell(addr, not deep),
                cell(hours, not deep),
                ("<td>" + esc(menu) + "</td>") if menu else cell("", True),
                link_cell(official if official else r["url"], official or "MICHELIN Guide page"),
                link_cell(social, "Social (official)") if social else cell("", True),
                link_cell(r["url"], "Source: guide.michelin.com"),
            )
        )
    body = (
        '<p class="lead">All <strong>50 starred Shanghai restaurants</strong> from the official MICHELIN Guide directory '
        "(checked 2026-11-25): 1 Three-Star, 11 Two-Star, 38 One-Star. Star status and price band are verified from the "
        "directory. <span class=\"uv\">Unverified</span> cells were not confirmed from an official source and are left "
        "blank by protocol — never guessed.</p>"
        '<div class="table-scroll"><table><thead><tr>'
        "<th>Restaurant</th><th>Michelin status (2026)</th><th>Price band</th><th>Cuisine</th>"
        "<th>District</th><th>Address</th><th>Hours / days</th><th>Cost for 2 (total)</th>"
        "<th>Official link</th><th>Social</th><th>Source</th></tr></thead><tbody>" + "".join(rows) + "</tbody></table></div>"
        '<section class="card"><h2>Listed in the guide vs currently starred</h2><p>Every row above <strong>currently '
        "holds a MICHELIN Star</strong> in the live 2026 directory. Bib Gourmand (33 in the Shanghai directory) and "
        "MICHELIN Selected (70) are separate, non-star distinctions and are intentionally excluded here.</p></section>"
        '<section class="card"><h2>Cost for two</h2><ul class="kv">'
        "<li><strong>Exact (official menu, incl. service &amp; taxes):</strong> T'ang Court — ¥888 Classic Dim Sum Lunch "
        "Set for Two; ¥2,288 All-Day Set Menu for Two (official 2026 menu PDF).</li>"
        "<li><strong>Not quoted:</strong> no official menu prices are published on the reachable pages for the other 49 "
        "restaurants. Their price band (¥ – ¥¥¥¥) is the only verified pricing anchor; per protocol, no estimated "
        "dollar figures are shown. See Suggestions S4 for how to fill these.</li></ul></section>"
    )
    return layout("Michelin Restaurants — 2026 Directory", "restaurants.html", body)


def render_activities(activities_data):
    rows = []
    for a in activities_data["activities"]:
        verified_badge = (
            '<span class="ok">Verified</span>' if a["verified"] else '<span class="uv">Unverified</span>'
        )
        rows.append(
            "<tr><td><strong>%s</strong><br><span class=\"muted\">%s · %s</span></td>%s%s%s%s%s%s%s%s</tr>"
            % (
                esc(a["name"]), esc(a["type"]), esc(a["district"]),
                "<td>" + verified_badge + "</td>",
                cell(a["days"], not a["verified"]),
                cell(a["hours"], not a["verified"]),
                cell(a["exceptions"], not a["verified"]),
                cell(a["cost_for_two"], not a["verified"]),
                cell(a["social"], not a["verified"]),
                link_cell(a["official_site"], "Official site") if a["official_site"] else cell("", True),
                link_cell(a["hours_source"], "Hours source") if a["hours_source"] else cell("", True),
            )
        )
    body = (
        '<p class="lead">Activities are listed with days open, hours, exceptions, cost for two, and official/social '
        "links. Only values confirmed from an official site are shown; everything else is blank and flagged.</p>"
        '<div class="table-scroll"><table><thead><tr>'
        "<th>Activity</th><th>Status</th><th>Days open</th><th>Hours</th><th>Exceptions</th>"
        "<th>Cost for 2</th><th>Social / media</th><th>Official site</th><th>Hours source</th>"
        "</tr></thead><tbody>" + "".join(rows) + "</tbody></table></div>"
        '<section class="card"><h2>1-hour rule for activities</h2><p>Same-district pairings with the recommended '
        "hotels are noted per row. Minute-level door-to-door transit times could not be verified (Shanghai Metro "
        "official site unreachable — Flagged F4); see <a href=\"transport.html\">1-Hour Travel</a>.</p></section>"
    )
    return layout("Activities — Hours, Tickets, Social Links", "activities.html", body)


def render_transport(hotels_data, activities_data):
    rows = []
    pairings = [
        ("Andaz Xintiandi / The Langham Xintiandi (Xintiandi, Huangpu)",
         "T'ang Court, Canton 8, Lu Style, Oriental Sense & Palate, Imperial Treasure, Da Vittorio, Ling Long — 7 starred (verified Huangpu addresses)",
         "Same district — walk / short metro",
         "Time unverified"),
        ("The Peninsula Shanghai / Waldorf Astoria on the Bund (The Bund, Huangpu)",
         "Same 7 starred Huangpu restaurants",
         "Same district — walk / short metro",
         "Time unverified"),
        ("The PuLi / Upper House / Jing An Shangri-La (Jing'an)",
         "Bao Li Xuan, Tou Zao — 2 starred (verified Jing'an addresses)",
         "Same district",
         "Time unverified"),
        ("Capella Shanghai, Jian Ye Li (Xuhui)",
         "Ji Pin Court — 1 starred (verified Xuhui address)",
         "Same district",
         "Time unverified"),
        ("Any Huangpu/Jing'an hotel → Shanghai Museum East Hall (Pudong)",
         "—", "Cross-district (metro)", "Time unverified"),
        ("Any hotel → Shanghai Disneyland (Pudong Chuansha)",
         "—", "Cross-district (metro; official site advises metro/taxi)", "Time unverified"),
    ]
    for hotel, rest, mode, status in pairings:
        rows.append(
            "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>"
            % (esc(hotel), esc(rest), esc(mode), uv() if status.startswith("Time") else esc(status))
        )
    body = (
        '<section class="card"><h2>Methodology &amp; honesty note</h2><ul class="kv">'
        "<li>The requirement is <em>≤1 hour by subway or bus</em> from the hotel for every activity/restaurant.</li>"
        "<li>What is verified here: each hotel's neighborhood/district and each restaurant's district/address from "
        "official pages (see Michelin / Hotels pages). Same-district = walkable or a short metro ride.</li>"
        "<li>What is <strong>not verified</strong>: minute-level door-to-door travel times. The official Shanghai Metro "
        "site (shmetro.com) returned HTTP 500 from the build sandbox on 2026-11-25, and no map/routing API is in the "
        "allowed host list. Time cells are therefore left blank and flagged — never invented.</li>"
        "</ul></section>"
        '<div class="table-scroll"><table><thead><tr><th>Hotel base</th><th>Starred restaurants / activity in range (verified geography)</th>'
        "<th>Mode</th><th>Door-to-door time</th></tr></thead><tbody>" + "".join(rows) + "</tbody></table></div>"
        '<section class="card"><h2>What to check to close this gap</h2><ul class="kv">'
        "<li>Open shmetro.com (or the official Shanghai Metro app) and check station-to-station times for each "
        "hotel→restaurant pair, then add a <em>verified minutes</em> column.</li>"
        "<li>Verify the remaining 38 restaurant addresses (Michelin pages) so cluster counts become complete.</li>"
        "<li>Confirm bus/taxi ETAs for cross-district trips (Disneyland, Oriental Pearl) from an official source.</li>"
        "</ul></section>"
    )
    return layout("1-Hour Travel — Verified Geography", "transport.html", body)


def render_budget(hotels_data, restaurants_data):
    hrows = []
    for h in hotels_data["hotels"]:
        if h["seven_night_total_usd"]:
            hrows.append(
                "<tr><td>%d</td><td>%s</td><td>$%d</td><td>$%d</td>%s</tr>"
                % (h["rank"], esc(h["name"]), h["seven_night_total_usd"], h["seven_night_total_usd_taxes"],
                   link_cell(h["source_url"], "Booking-engine check (official channel)"))
            )
        else:
            hrows.append(
                "<tr><td>%d</td><td>%s</td><td colspan=\"2\">No rooms available Feb 15–22, 2027 (booking engine)</td>%s</tr>"
                % (h["rank"], esc(h["name"]), link_cell(h["source_url"], "Booking-engine check (official channel)"))
            )
    tang = [r for r in restaurants_data["restaurants"] if r["name"] == "T'ang Court"][0]
    body = (
        '<section class="card"><h2>Hotel — 7-night totals (Feb 15–22, 2027, 2 adults)</h2>'
        '<div class="table-scroll"><table><thead><tr><th>#</th><th>Hotel</th><th>7-night total (USD, room rate)</th>'
        "<th>7-night all-in with taxes (USD)</th><th>Source</th></tr></thead><tbody>" + "".join(hrows) + "</tbody></table></div>"
        '<p class="muted">Rates are live &ldquo;Starting at&rdquo; prices from the official MICHELIN Guide Hotels '
        "booking engine, checked 2026-11-25. Cheapest verified stay: <strong>Andaz Xintiandi — $1,183</strong> "
        "($1,379 all-in).</p></section>"
        '<section class="card"><h2>Michelin dining — total price for a couple of 2 adults</h2>'
        '<div class="table-scroll"><table><thead><tr><th>Restaurant</th><th>Status</th><th>Menu (official source)</th>'
        "<th>Total for 2</th><th>Source</th></tr></thead><tbody>"
        "<tr><td><strong>%s</strong></td><td>%s</td><td>2026 seasonal set-menu PDF (official, langhamhotels.com) — incl. service &amp; taxes</td>"
        "<td><strong>¥888</strong> Classic Dim Sum Lunch Set for Two<br><strong>¥2,288</strong> All-Day Set Menu for Two</td>"
        '<td><a href="https://www.langhamhotels.com/content/dam/langhamhotels/tlshx-pdfs/tang-court/2026/seasonal-set-menu-selection-2026.pdf" target="_blank" rel="noopener">Official menu PDF</a></td></tr>'
        "<tr><td colspan=\"5\" class=\"muted\">All other 49 restaurants: no official menu price published on reachable "
        "pages — band-only anchor (¥–¥¥¥¥), no estimated totals shown (protocol). See Suggestions S4 and "
        '<a href="restaurants.html">Michelin</a> for per-restaurant official links.</td></tr>'
        "</tbody></table></div></section>"
        '<section class="card"><h2>Best time to book (what is verified)</h2><ul class="kv">'
        "<li>For the preferred block <strong>Feb 15–22, 2027</strong>, rates are already live and bookable for 7 of 8 "
        "shortlisted hotels as of <strong>2026-11-25</strong> — booking now locks today's prices.</li>"
        "<li><strong>Waldorf Astoria on the Bund</strong> shows no availability for these dates via the engine; "
        "re-check alternate dates directly.</li>"
        "<li>A data-driven 'cheapest date to book' across the whole Feb 15–Mar 23 window requires a rate calendar "
        "(see Suggestions S2). Nothing here claims a cheapest period that was not measured.</li>"
        "</ul></section>"
    ) % (esc(tang["name"]), badge_stars(tang["stars"]))
    return layout("Budget — Verified Totals", "budget.html", body)


def render_questions():
    qa = [
        ("Q1", "What is the total budget ceiling for the trip (hotel + dining + activities + transport)?",
         "We have verified hotel totals ($1,183–$6,085 for 7 nights) and one exact Michelin total (¥888–¥2,288 for two at T'ang Court). A budget ceiling determines which hotel tier and how many starred dinners fit.",
         "Answer needed before: choosing hotel rank; ranking dining plans.", "budget.html"),
        ("Q2", "Is the stay 7 nights (modeled) or up to 2 weeks (14 nights)?",
         "The brief allows 1–2 weeks; all verified rates here are for the 7-night block Feb 15–22, 2027. Longer stays change totals and availability.",
         "Answer needed before: any booking.", "index.html"),
        ("Q3", "Do you require a Disney day, or are culture/garden/museum activities sufficient?",
         "Disneyland is in Pudong (cross-district, ~1h+ by metro — unverified time); it changes the hotel location logic (Pudong/Lujiazui base) versus a Huangpu/Jing'an base.",
         "Answer needed before: hotel district choice.", "activities.html"),
        ("Q4", "Do you want the cheapest booking date measured across the whole Feb 15–Mar 23 window?",
         "We verified today's live rates for Feb 15–22 only. A cheapest-date claim needs a rate calendar across the window (Suggestion S2).",
         "Answer needed before: final booking date decision.", "budget.html"),
        ("Q5", "What are the passport/visa/entry requirements for your nationality, and are they settled?",
         "Entry rules depend on nationality (visa-free transit rules differ). This dashboard did not verify your specific nationality requirements.",
         "Answer needed before: booking flights.", "flagged.html"),
        ("Q6", "Bed preference: king, queen, or either? Any accessibility needs?",
         "Room-level bed type is not published on reachable official pages (only Peninsula King/Twin verified). Confirm with the hotel.",
         "Answer needed before: hotel booking.", "hotels.html"),
        ("Q7", "How many Michelin-starred dinners do you want to book, and at what star level?",
         "12 of 50 restaurants have verified addresses/hours/websites; the rest are listed with band-only data. Reservations are required at most starred restaurants.",
         "Answer needed before: restaurant reservations.", "restaurants.html"),
        ("Q8", "Do you need a car/driver, or is metro+walking acceptable?",
         "The ≤1-hour rule is defined on subway/bus; transit times are still unverified (F4).",
         "Answer needed before: finalizing the 1-hour analysis.", "transport.html"),
        ("Q9", "Any dietary restrictions or allergies?",
         "Relevant to starred-restaurant set menus (e.g., Fu He Hui is vegetarian-only set menus).",
         "Answer needed before: restaurant reservations.", "restaurants.html"),
        ("Q10", "Travel insurance, cancellation, and payment preferences?",
         "Waldorf's unavailability and rate sales (PuLi 20% off) show inventory moves; flexibility matters.",
         "Answer needed before: booking.", "flagged.html"),
    ]
    rows = "".join(
        "<tr><td>%s</td><td><strong>%s</strong></td><td>%s</td><td>%s</td>"
        '<td><a href="%s">See %s</a></td></tr>'
        % (q[0], esc(q[1]), esc(q[2]), esc(q[3]), q[4], q[4].replace(".html", "").upper())
        for q in qa
    )
    body = (
        '<p class="lead">A clear list of the questions, information and answers needed before any decision can be '
        "reasonably made. Column 3 states what we already have (and its limits); column 4 states what the answer "
        "unlocks.</p>"
        '<div class="table-scroll"><table><thead><tr><th>ID</th><th>Question</th><th>What we know / don&rsquo;t know</th>'
        "<th>Needed before</th><th>Related</th></tr></thead><tbody>" + rows + "</tbody></table></div>"
    )
    return layout("Q&A Gaps — Answer Before Decisions", "questions.html", body)


def render_suggestions():
    sugg = [
        ("S1", "Add a decision-focused 'Recommended Plan' page",
         "Combine verified hotel + dining + activity data into one recommended itinerary with a single total, so decisions are made in one place instead of across tables.",
         "Low effort — data already verified.", "index.html"),
        ("S2", "Build a rate-calendar monitor for the Feb 15–Mar 23 window",
         "To make a real 'cheapest time to book' claim, re-check the booking engine across candidate date blocks and record min/max rates per hotel. Publish the measured cheapest window with dates.",
         "Requires repeated official-channel checks; automate with a scheduled job.", "budget.html"),
        ("S3", "Verify all 50 restaurant addresses & hours from Michelin pages",
         "Only 12 of 50 restaurants are deep-verified. Completing addresses/districts/hours makes the ≤1-hour cluster ranking complete and lets hotel ranking use full cluster counts.",
         "~38 more official page fetches.", "restaurants.html"),
        ("S4", "Fetch official menus to publish exact for-two totals",
         "T'ang Court shows exact totals work (¥888/¥2,288). Repeat for the top cluster restaurants (Da Vittorio, Canton 8, Imperial Treasure, Ling Long, Bao Li Xuan, Tou Zao, Fu He Hui, Taian Table) and replace band-only cells.",
         "Menus may be PDFs; parse with care and re-verify dates.", "budget.html"),
        ("S5", "Integrate verified transit times (Shanghai Metro official)",
         "Once shmetro.com is reachable, compute door-to-door times for every hotel→restaurant/activity pair and add a verified minutes column plus a real isochrone map.",
         "Depends on shmetro.com reachability (currently HTTP 500 from sandbox).", "transport.html"),
        ("S6", "Add booking price-alert / availability tracking",
         "Waldorf sold out for the preferred window; rates change. A weekly re-check (or price-alert) protects the decision and documents the cheapest observed date.",
         "Needs an alerting channel; manual re-check works too.", "flagged.html"),
        ("S7", "Add a map view of hotel × restaurant clusters",
         "A simple static map (hotel pins + starred-restaurant pins with verified addresses) improves the ≤1-hour decision at a glance.",
         "Uses verified coordinates from official pages; no routing needed initially.", "transport.html"),
        ("S8", "Consolidate social/media links for all venues",
         "Only Shanghai Museum's 8 official socials and Da Vittorio's Instagram are verified. Expand via official sites/apps (WeChat, Weibo, Bilibili, Douyin, IG, YouTube, TikTok) — each link must be from the venue's own official account.",
         "Many venues have no IG/TikTok; leave blank+flag where none exists officially.", "activities.html"),
        ("S9", "Add a review-and-approve workflow for flagged items",
         "F1–F10 (incl. the 102 House discrepancy) should be reviewed and resolved before the data is treated as final; a decision log records who approved what.",
         "Process, not code.", "flagged.html"),
        ("S10", "Mobile-first polish + accessibility pass",
         "Tables already scroll on mobile; add print-friendly budget sheet and skip-to-content links for printing/booking on the phone.",
         "Low effort.", "index.html"),
    ]
    rows = "".join(
        "<tr><td>%s</td><td><strong>%s</strong></td><td>%s</td><td>%s</td>"
        '<td><a href="%s">See %s</a></td></tr>'
        % (s[0], esc(s[1]), esc(s[2]), esc(s[3]), s[4], s[4].replace(".html", "").upper())
        for s in sugg
    )
    body = (
        '<p class="lead">Suggestions to improve decision-making on this site. <strong>Review and choose the best path '
        "before implementing any change</strong> — none of these have been built yet.</p>"
        '<div class="table-scroll"><table><thead><tr><th>ID</th><th>Suggestion</th><th>Why / what it improves</th>'
        "<th>Effort / dependency</th><th>Related</th></tr></thead><tbody>" + rows + "</tbody></table></div>"
    )
    return layout("Suggestions — Review Before Implementing", "suggestions.html", body)


def render_sources(sources_data):
    rows = "".join(
        "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>"
        % (esc(s["id"]), esc(s["name"]), link_cell(s["url"], "Open source"), esc(s["verifies"]))
        for s in sources_data["sources"]
    )
    body = (
        '<p class="lead">Every fact on this site traces to one of these official sources. All checks performed '
        "2026-11-25.</p>"
        '<div class="table-scroll"><table><thead><tr><th>ID</th><th>Source</th><th>Link</th><th>What it verifies</th></tr></thead>'
        "<tbody>" + rows + "</tbody></table></div>"
    )
    return layout("Sources — Official Links", "sources.html", body)


def render_flagged(flagged_data):
    rows = "".join(
        "<tr><td>%s</td><td><span class=\"%s\">%s</span></td><td><strong>%s</strong><br><span class=\"muted\">%s</span></td>"
        "<td>%s</td>%s</tr>"
        % (
            esc(f["id"]),
            "uv" if f["severity"] in ("high", "medium") else "warn",
            esc(f["severity"]),
            esc(f["title"]),
            esc(f["detail"]),
            esc(f["action"]),
            link_cell(f.get("source", ""), "Source"),
        )
        for f in flagged_data["items"]
    )
    body = (
        '<p class="lead">Irregularities found while verifying line by line. These are published for review and do not '
        "block the dashboard. No value was guessed to resolve any of them.</p>"
        '<div class="table-scroll"><table><thead><tr><th>ID</th><th>Severity</th><th>Irregularity</th>'
        "<th>Recommended action</th><th>Source</th></tr></thead><tbody>" + rows + "</tbody></table></div>"
    )
    return layout("Flagged for Review", "flagged.html", body)


def render_verification(trip):
    body = (
        '<section class="card"><h2>Protocol</h2><ol class="kv">'
        "<li>Collect candidate facts only from official sources reachable in this environment.</li>"
        "<li>Verify each fact on the official page (or official booking channel) and record the URL and check date.</li>"
        "<li>If a value cannot be confirmed, leave the cell blank and flag it Unverified — never infer or fill in.</li>"
        "<li>Cross-check counts against a second official artifact (press release vs live directory).</li>"
        "<li>Publish every row with its source link; log all irregularities.</li></ol></section>"
        '<section class="card"><h2>Line-by-line verification log (2026-11-25)</h2><ul class="kv">'
        "<li><strong>Michelin directory:</strong> all 50 starred names, star levels, bands, cuisines read from "
        "guide.michelin.com Shanghai all-starred pages 1–2 (2 fetch passes). Cross-checked against the official "
        "2026-04 press release (guide.michelin.com article).</li>"
        "<li><strong>12 restaurant pages:</strong> star icons, addresses, districts, price bands, phones, websites "
        "verified individually on guide.michelin.com (T'ang Court, Ji Pin Court, Canton 8, Lu Style, Oriental Sense &amp; "
        "Palate, Imperial Treasure, Da Vittorio, Bao Li Xuan, Tou Zao, Fu He Hui, Taian Table, Ling Long).</li>"
        "<li><strong>Hours:</strong> T'ang Court — langhamhotels.com (lunch 11:30–14:00, dinner 17:30–21:00, closed Mon); "
        "Da Vittorio, Fu He Hui, Ling Long — official Michelin pages. All other hours left blank+flagged.</li>"
        "<li><strong>Menu price:</strong> T'ang Court official 2026 menu PDF — ¥888 dim-sum lunch set for two; ¥2,288 "
        "all-day set for two (incl. service &amp; taxes).</li>"
        "<li><strong>Hotels:</strong> 8 hotels shortlisted from the official MICHELIN Guide Hotels Shanghai directory; "
        "live 'Starting at' USD rates for Feb 15–22, 2027 (2 adults) pulled from the same official booking engine; "
        "Peninsula Deluxe Room King/Twin verified on peninsula.com.</li>"
        "<li><strong>Activities:</strong> Yu Garden (yugarden.com.cn 参观信息) and Shanghai Museum (shanghaimuseum.net) "
        "hours/tickets/socials verified; Shanghai Disney Resort site verified (hours flagged); Bund / Oriental Pearl / "
        "Jing'an Temple flagged (no reachable official site).</li>"
        "<li><strong>Unreachable official sites:</strong> shmetro.com (HTTP 500), hilton.com, hyatt.com, "
        "middlehousehotels.com, orientalpearltower.com.cn, shanghai.gov.cn — affected cells left blank+flagged.</li>"
        "<li><strong>Counts reconciled:</strong> 3★=1, 2★=11, 1★=38 (directory, 2026-11-25) vs press release "
        "(2★=12 incl. 102 House) — discrepancy logged as F1/F2.</li>"
        "</ul></section>"
    )
    return layout("Verification Log", "verification.html", body)


def main():
    trip = load("trip.json")
    hotels = load("hotels.json")
    restaurants = load("restaurants.json")
    activities = load("activities.json")
    sources = load("sources.json")
    flagged = load("flagged.json")

    pages = {
        "index.html": render_index(trip["trip"], trip["counts"]),
        "hotels.html": render_hotels(hotels),
        "restaurants.html": render_restaurants(restaurants),
        "activities.html": render_activities(activities),
        "transport.html": render_transport(hotels, activities),
        "budget.html": render_budget(hotels, restaurants),
        "questions.html": render_questions(),
        "suggestions.html": render_suggestions(),
        "sources.html": render_sources(sources),
        "flagged.html": render_flagged(flagged),
        "verification.html": render_verification(trip),
    }
    for name, content in pages.items():
        path = os.path.join(ROOT, name)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)
        print("wrote", path)


if __name__ == "__main__":
    main()
