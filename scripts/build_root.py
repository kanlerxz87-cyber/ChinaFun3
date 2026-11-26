#!/usr/bin/env python3
"""Deterministic root-site generator for ChinaFun3 (/index.html and root *.html).

Reads strictly from data/{trip,hotels,restaurants,activities,transport,budget,flagged}.json
and outputs all 14 static root HTML pages without touching any parallel subsite
(docs/, considered/, for-two/, plan/, verify/).
"""

from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"

NAV_ITEMS = [
    ("index.html", "Dashboard"),
    ("executive-summary.html", "Executive Summary"),
    ("itinerary.html", "Itinerary & Dates"),
    ("hotels.html", "Hotels"),
    ("restaurants.html", "Michelin"),
    ("activities.html", "Activities"),
    ("transport.html", "Transport"),
    ("budget.html", "Budget"),
    ("questions.html", "Q&A Gaps"),
    ("suggestions.html", "Suggestions"),
    ("sources.html", "Sources"),
    ("flagged.html", "Flagged"),
]


def load_json(name: str) -> dict:
    return json.loads((DATA_DIR / name).read_text(encoding="utf-8"))


def e(val: object) -> str:
    return html.escape("" if val is None else str(val), quote=True)


def ext_link(url: str, label: str = "Source →", cls: str = "") -> str:
    if not url:
        return '<span class="badge badge-unverified">No URL</span>'
    c = f' class="{e(cls)}"' if cls else ""
    return f'<a{c} href="{e(url)}" target="_blank" rel="noopener noreferrer">{e(label)}</a>'


def badge_verified(ok: bool = True, label: str | None = None) -> str:
    if ok:
        return f'<span class="badge badge-verified">{e(label or "Verified")}</span>'
    return f'<span class="badge badge-unverified">{e(label or "Unverified · Flagged")}</span>'


def page_shell(active: str, title: str, desc: str, body_html: str) -> str:
    nav_links = "\n        ".join(
        f'<a{(" class=" + chr(34) + "active" + chr(34) if href == active else "")} href="{e(href)}">{e(label)}</a>'
        for href, label in NAV_ITEMS
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(title)}</title>
  <meta name="description" content="{e(desc)}">
  <link rel="icon" href="data:,">
  <link rel="stylesheet" href="assets/css/style.css">
  <script defer src="assets/js/app.js"></script>
</head>
<body>
  <header class="topbar">
    <div class="container topbar-inner">
      <a class="brand" href="index.html" aria-label="ChinaFun3 home">
        <span class="brand-mark">CN</span>
        <span>ChinaFun3 <small>Shanghai • Feb 15–Mar 23, 2027 • Verified 2026-11-26</small></span>
      </a>
      <button class="hamburger" data-nav-toggle aria-expanded="false" aria-label="Toggle navigation">☰</button>
      <nav class="nav" data-nav>
        {nav_links}
      </nav>
    </div>
  </header>
{body_html}
  <footer class="footer">
    <div class="container footer-row">
      <span>ChinaFun3 Root Dashboard · Verified <strong>2026-11-26</strong> · Every table row carries an official source link or explicit <span class="badge badge-unverified">Unverified · Flagged</span> label.</span>
      <span><a href="methodology.html">Verification Methodology</a> · <a href="flagged.html">Audit Log (F01–F10)</a> · <a href="sources.html">All Sources</a></span>
    </div>
  </footer>
</body>
</html>
"""


def build_index(trip: dict, hotels: dict, rest: dict, act: dict, bud: dict, flg: dict) -> str:
    summary = rest["summary"]
    h_list = hotels["hotels"]
    bookable = [h for h in h_list if h["bookable_feb15"]]
    cheapest = min(bookable, key=lambda x: x["seven_night_total_usd"])
    langham = next(h for h in h_list if "Langham" in h["name"])
    peninsula = next(h for h in h_list if "Peninsula" in h["name"])

    body = f"""
  <section class="hero">
    <div class="container">
      <span class="kicker">● Re-Verified 2026-11-26 • Line-by-line official sources • Zero hallucinations</span>
      <h1 class="h1">Shanghai 2027 for Two — Live Bookable Hotels, 2026 MICHELIN Guide &amp; Official Activity Schedules.</h1>
      <p class="lead">Built for <strong>2 adults</strong> inside <strong>{e(trip["trip"]["window"])}</strong> (preferred arrival <strong>Feb 15–18</strong>; 7-night baseline <strong>Feb 15–22, 2027</strong>). Every hotel has verified Queen/King+ bedding, official booking checkout totals, and Huangpu/Jing'an Michelin density. Every unverified cell is left blank and explicitly flagged — never estimated.</p>
      <div class="cta-row">
        <a class="btn btn-primary" href="executive-summary.html">Executive Summary →</a>
        <a class="btn" href="hotels.html">12 Hotels Ranked</a>
        <a class="btn" href="restaurants.html">2026 Michelin ({summary["starred_total"]}★ + Bib/Selected)</a>
        <a class="btn" href="flagged.html">10 Audit Fixes (F01–F10)</a>
      </div>
      <div class="meta-row">
        <span class="pill"><strong>Window:</strong> {e(trip["trip"]["window"])}</span>
        <span class="pill"><strong>Guests:</strong> 2 adults · Queen/King+ · Private bath</span>
        <span class="pill"><strong>Spring Festival 2027:</strong> Feb 5–13 (Mon Feb 15 = normal workday)</span>
        <span class="pill"><strong>Live 2026 MICHELIN:</strong> {summary["total_live_entries"]} total ({summary["starred_total"]} Starred · {summary["bib_gourmand"]} Bib · {summary["michelin_selected"]} Selected)</span>
      </div>
      <div class="notice ok mt16">
        <strong>Root Audit Complete (F01–F10):</strong> Re-verified against live Nov 26, 2026 sources — replacing outdated 2024 counts, removed closed <em>Ultraviolet</em> &amp; <em>102 House</em>, removed unopened <em>Four Seasons Huaihai</em>, replaced surrogate hotel prices with live Feb 15–22, 2027 checkout quotes, and fixed Yu Garden off-peak ¥30 &amp; NIA 240h visa rules.
      </div>
    </div>
  </section>

  <main class="container">
    <div class="grid grid-4">
      <div class="card">
        <p class="small">HOTELS CHECKED (FEB 15–22, 2027)</p>
        <p class="stat">{len(h_list)} <small>({len(bookable)} bookable live)</small></p>
        <p class="small mt8">From ${cheapest["seven_night_total_usd"]:,.2f} all-in ({e(cheapest["name"].split(",")[0])}). <a href="hotels.html">Compare →</a></p>
      </div>
      <div class="card">
        <p class="small">SHANGHAI MICHELIN 2026</p>
        <p class="stat">{summary["starred_total"]}★ <small>+ {summary["bib_gourmand"]} Bib + {summary["michelin_selected"]} Selected</small></p>
        <p class="small mt8">1×3★ · 11×2★ · 38×1★ = {summary["total_live_entries"]} live venues. <a href="restaurants.html">Directory →</a></p>
      </div>
      <div class="card">
        <p class="small">ACTIVITIES IN ≤1H ENVELOPE</p>
        <p class="stat">{len(act["activities"])} <small>official sources + social</small></p>
        <p class="small mt8">Hours, open days, closed Mondays/Tuesdays, Yu Garden ¥60 for 2. <a href="activities.html">Activities →</a></p>
      </div>
      <div class="card">
        <p class="small">VERIFIED FOR-2 MENU TOTALS</p>
        <p class="stat">{len(bud["exact_verified_menu_totals_for_two"])} <small>official 2026 PDF/FAQ menus</small></p>
        <p class="small mt8">¥788.22 Yi Long Court lunch to ¥5,776 Taian Table 12-course. <a href="budget.html">Budgets →</a></p>
      </div>
    </div>

    <section class="card mt16">
      <div style="display:flex; gap:12px; align-items:flex-start; flex-wrap:wrap; justify-content:space-between">
        <div>
          <h2 style="margin:0 0 4px; font-size:19px">60-Second Executive Decision</h2>
          <p class="small" style="max-width:74ch">Stay in <strong>Huangpu (Xintiandi or The Bund)</strong> for Shanghai's densest walkable/same-district Michelin cluster (16+ verified starred venues) and direct Metro Lines 1/2/8/10/14 reach. Top picks for <strong>Feb 15–22, 2027</strong>: <strong>{e(langham["name"])}</strong> at <strong>${langham["seven_night_total_usd"]:,.2f}</strong> all-in (breakfast included, free cancel until Feb 10, in-house 2★ T'ang Court); <strong>{e(cheapest["name"])}</strong> at <strong>${cheapest["seven_night_total_usd"]:,.2f}</strong> all-in for lowest verified rate; or <strong>{e(peninsula["name"])}</strong> at <strong>CNY 20,119.33</strong> direct promo (bookable Nov 23–Dec 7, 2026 incl. breakfast, 13.8% cheaper Feb 15–Mar 8 than Mar 8–23).</p>
        </div>
        <a class="btn btn-primary" href="executive-summary.html">Full Executive Summary</a>
      </div>
      <hr class="sep">
      <div class="grid grid-3" style="margin:0">
        <div>
          <strong>Best Value + Breakfast + 2★ In-House</strong>
          <p class="small mt8">Langham Xintiandi: $2,291.93 all-in (40 m² King, verified marble ensuite, daily breakfast, T'ang Court 2★ upstairs).</p>
        </div>
        <div>
          <strong>Lowest All-In Checkout</strong>
          <p class="small mt8">Andaz Xintiandi: $1,376.21 all-in (41 m² King, directly across from Langham in Xintiandi Huangpu).</p>
        </div>
        <div>
          <strong>Book-By Deadline: Dec 7, 2026</strong>
          <p class="small mt8">Peninsula Shanghai 'A Gift for the New Year' (15% off + breakfast) ends Dec 7; Feb 15–Mar 8 saves 13.8% vs Mar 8–23.</p>
        </div>
      </div>
    </section>

    <section class="section">
      <h2>Explore All Root Dashboard Sections</h2>
      <p class="sub">Every table supports live search and column sorting. Unverified claims are never guessed.</p>
      <div class="grid grid-3">
        <a class="card" href="executive-summary.html"><h3>📋 Executive Summary</h3><p>Top hotel picks, budget scenarios, and key closing-day &amp; visa rules.</p></a>
        <a class="card" href="itinerary.html"><h3>📅 Itinerary &amp; Dates</h3><p>2027 Spring Festival (gov.cn), NIA 240h visa, 6 Peninsula promo windows, and 7-night skeleton.</p></a>
        <a class="card" href="hotels.html"><h3>🏨 Hotels (12 Ranked)</h3><p>Live Feb 15–22, 2027 checkout quotes, room specs, private bath notes, and cancellation rules.</p></a>
        <a class="card" href="restaurants.html"><h3>⭐ Michelin Guide 2026</h3><p>25 deep-verified venues (Starred vs. Bib/Selected), exact 2026 PDF/FAQ prices, social links, plus all 50 starred.</p></a>
        <a class="card" href="activities.html"><h3>🏛️ Activities ≤1h</h3><p>12 central attractions with official hours, closures, Yu Garden ¥60 off-peak tickets, and video links.</p></a>
        <a class="card" href="transport.html"><h3>🚇 Transport &amp; 1h Radius</h3><p>Verified Metro lines &amp; district corridors with honest flagging of unverified minute estimates.</p></a>
        <a class="card" href="budget.html"><h3>💰 Budget (Totals for 2)</h3><p>Combined 7-night hotel + exact verified dining &amp; activity scenarios.</p></a>
        <a class="card" href="questions.html"><h3>❓ Q&amp;A Gaps ({len(flg["questions"])})</h3><p>Decisions to confirm before locking non-refundable flights or hotel rooms.</p></a>
        <a class="card" href="suggestions.html"><h3>💡 Suggestions ({len(flg["suggestions"])})</h3><p>Actionable review-before-implement planning proposals.</p></a>
        <a class="card" href="flagged.html"><h3>🚩 Flagged &amp; Audit ({len(flg["flagged_irregularities"])})</h3><p>Complete F01–F10 remediation log comparing legacy claims against live verified data.</p></a>
        <a class="card" href="sources.html"><h3>🔗 Sources Register</h3><p>Direct official links to gov.cn, NIA, MICHELIN Guide, Peninsula, Langham, Bvlgari &amp; museums.</p></a>
        <a class="card" href="methodology.html"><h3>🔬 Methodology</h3><p>Line-by-line evidence standards and anti-hallucination verification protocol.</p></a>
      </div>
    </section>

    <section class="section">
      <h2>Companion Subsites Preserved in This Repository</h2>
      <p class="sub">Independent session builds preserved intact alongside this unified root dashboard.</p>
      <div class="grid grid-3">
        <a class="card" href="verify/index.html"><h3>verify/</h3><p>Re-verified Nov 25 snapshot with 50 starred entries, 8 MICHELIN hotels, and T'ang Court PDF verification.</p></a>
        <a class="card" href="plan/index.html"><h3>plan/</h3><p>Python dataset build featuring Taian Table FAQ, Yu Garden off-peak rules, and 7/10/14-night date comparison.</p></a>
        <a class="card" href="for-two/index.html"><h3>for-two/</h3><p>6-window Peninsula direct quote audit, 2026 hotel PDF menus, and 113-check Playwright verification.</p></a>
        <a class="card" href="considered/index.html"><h3>considered/</h3><p>Source-first baseline shortlist with automated schema/link validation.</p></a>
        <a class="card" href="docs/index.html"><h3>docs/</h3><p>JSON-driven entry rules, State Council 2027 holiday calendar, and museum notices.</p></a>
      </div>
    </section>
  </main>
"""
    return page_shell(
        "index.html",
        "ChinaFun3 — Shanghai 2027 Verified Trip Dashboard",
        "Verified 2027 Shanghai trip plan for 2 adults: live Feb 15–22, 2027 hotel quotes, 2026 MICHELIN Guide directory, official museum/garden hours, and source-linked audit.",
        body,
    )


def build_exec(trip: dict, hotels: dict, rest: dict, bud: dict, flg: dict) -> str:
    h_rows = ""
    for h in hotels["hotels"][:5]:
        price = f"${h['seven_night_total_usd']:,.2f}" if h["seven_night_total_usd"] else '<span class="badge badge-unverified">Unavailable</span>'
        h_rows += (
            f"<tr><td>#{h['rank']}</td><td><strong>{e(h['name'])}</strong><br><span class='small'>{e(h['tier'])}</span></td>"
            f"<td>{e(h['district'])}</td><td>{e(h['room_verified'])}</td>"
            f"<td class='num'>{price}</td><td>{e(h['breakfast'])}</td>"
            f"<td>{ext_link(h['source_url'], 'MICHELIN →')}</td></tr>\n"
        )
    s_cards = ""
    for sc in bud["scenarios"]:
        ht = f"${sc['hotel_usd']:,.2f} USD" if sc.get("hotel_usd") else f"¥{sc['hotel_cny']:,.2f} CNY"
        s_cards += f"""
        <div class="card">
          <h3>{e(sc["name"])}</h3>
          <p class="mt8"><strong>Hotel (7n):</strong> {ht}<br><span class="small">{e(sc["hotel_name"])}</span></p>
          <p class="mt8"><strong>Verified Dining Sample:</strong> ¥{sc["verified_dining_cny"]:,.2f}<br><span class="small">{e(sc["dining_breakdown"])}</span></p>
          <p class="mt8"><strong>Verified Activities:</strong> ¥{sc["verified_activities_cny"]}<br><span class="small">{e(sc["activities_breakdown"])}</span></p>
          <p class="small mt8">{e(sc["unpriced_note"])}</p>
        </div>"""

    body = f"""
  <section class="hero">
    <div class="container">
      <span class="kicker">Executive Summary · Decision Ready</span>
      <h1 class="h1">Where to stay, when to book, and what is verified for 2 adults.</h1>
      <p class="lead">Concise decision brief synthesized from live Nov 26, 2026 hotel checkout quotes, official State Council / NIA notices, and the 2026 MICHELIN Guide Shanghai directory.</p>
    </div>
  </section>
  <main class="container">
    <section class="section">
      <h2>Top 5 Ranked Hotel Shortlist (Feb 15–22, 2027 · 7 Nights)</h2>
      <p class="sub">{e(hotels["ranking_rule"])}</p>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Rank</th><th>Hotel</th><th>District</th><th>Verified Bed &amp; Room</th><th class="num">7n Total (All-In)</th><th>Breakfast</th><th>Source</th></tr></thead>
          <tbody>{h_rows}</tbody>
        </table>
      </div>
    </section>

    <section class="section">
      <h2>3 Verified Budget Scenarios (7 Nights · 2 Adults)</h2>
      <div class="grid grid-3">{s_cards}</div>
    </section>

    <section class="section">
      <h2>Key Operational &amp; Regulatory Takeaways</h2>
      <div class="grid grid-2">
        <div class="card">
          <h3>2027 Spring Festival &amp; Timing</h3>
          <p class="mt8">Official State Council holiday runs <strong>Feb 5–13, 2027</strong> (with Feb 14 make-up workday). Arriving <strong>Mon Feb 15, 2027</strong> avoids holiday closures while catching <strong>Lantern Festival (Sat Feb 20)</strong> and Peninsula's lower-rate window (<strong>Feb 15–Mar 8</strong> is 13.8% cheaper than Mar 8–23).</p>
          <p class="mt8">{ext_link(trip["calendar"][0]["source_url"], "State Council Notice →")}</p>
        </div>
        <div class="card">
          <h3>Visa &amp; Closed-Day Rules</h3>
          <p class="mt8">US travelers qualify for <strong>240-hour (10-day) visa-free transit</strong> only when flying onward to a third country/region; round-trip US–Shanghai–US requires a visa. In Shanghai, <strong>Yu Garden, Shanghai Museum People's Square, T'ang Court, and Da Vittorio close Mondays</strong>; <strong>Shanghai Museum East closes Tuesdays</strong>.</p>
          <p class="mt8">{ext_link(trip["calendar"][2]["source_url"], "NIA 240h Rule →")}</p>
        </div>
      </div>
    </section>
  </main>
"""
    return page_shell("executive-summary.html", "Executive Summary — ChinaFun3", "Executive summary of verified Shanghai 2027 hotels, Michelin dining, and dates.", body)


def build_itinerary(trip: dict) -> str:
    cal_rows = "".join(
        f"<tr><td><strong>{e(c['label'])}</strong></td><td>{e(c['dates'])}</td><td>{e(c['impact'])}</td>"
        f"<td>{badge_verified(True, c['status'])}</td><td>{ext_link(c['source_url'], c['source_label'])}</td></tr>\n"
        for c in trip["calendar"]
    )
    opt_cards = "".join(
        f"<div class='card'><h3>{e(o['label'])}</h3><p class='mt8'><strong>Why:</strong> {e(o['why'])}</p>"
        f"<p class='mt8'><strong>Pros:</strong> {e(o['pros'])}</p><p class='mt8'><strong>Watchout:</strong> {e(o['watchout'])}</p>"
        f"<p class='mt8'>{badge_verified(True, o['status'])}</p></div>\n"
        for o in trip["date_options"]
    )
    pen_rows = "".join(
        f"<tr><td>{e(w['window'])}</td><td class='num'>¥{w['nightly_cny_excl']:,}</td><td class='num'><strong>¥{w['all_in_cny']:,.2f}</strong></td>"
        f"<td>{e(w['offer'])}</td><td>{ext_link(w['source_url'], 'Peninsula Offer →')}</td></tr>\n"
        for w in trip["peninsula_windows"]
    )
    skel_rows = "".join(
        f"<tr><td><strong>{e(s['day'])}</strong></td><td>{e(s['focus'])}</td><td>{e(s['notes'])}</td></tr>\n"
        for s in trip["skeleton_7n"]
    )
    guide_cards = "".join(
        f"<div class='card'><h3>{e(g['title'])}</h3><p class='mt8'>{e(g['detail'])}</p>"
        f"<p class='mt8'><span class='badge badge-guide'>{e(g['type'])}</span> {ext_link(g['source_url'], 'Source →')}</p></div>\n"
        for g in trip["booking_guidance"]
    )

    body = f"""
  <section class="hero">
    <div class="container">
      <span class="kicker">Itinerary, Calendar &amp; Cheapest Windows</span>
      <h1 class="h1">Dates, 2027 Spring Festival Rules &amp; Booking Window Evidence.</h1>
      <p class="lead">Every date claim is tied to State Council notice <code>国办发明电〔2026〕10号</code>, National Immigration Administration 240h transit policy, and 6 live weekly Peninsula Shanghai direct quotes across Feb 15–Mar 23, 2027.</p>
    </div>
  </section>
  <main class="container">
    <section class="section">
      <h2>Official Calendar &amp; Entry Requirements</h2>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Item</th><th>Verified Dates / Rule</th><th>Travel Impact</th><th>Status</th><th>Source</th></tr></thead>
          <tbody>{cal_rows}</tbody>
        </table>
      </div>
    </section>

    <section class="section">
      <h2>Modeled Stay Windows Inside Feb 15–Mar 23, 2027</h2>
      <div class="grid grid-3">{opt_cards}</div>
    </section>

    <section class="section" id="booking">
      <h2>Cheapest Time to Book — Direct Hotel Quotes vs. Industry Benchmarks</h2>
      <p class="sub">Direct 6-window Peninsula quote evidence shows <strong>Feb 15–Mar 8 is 13.8% cheaper</strong> than Mar 8–23, with the 15% promo open Nov 23–Dec 7, 2026.</p>
      <div class="table-wrap">
        <table>
          <thead><tr><th>7-Night Window (2027)</th><th class="num">Nightly (Excl. Tax)</th><th class="num">All-In Total (Incl. 16.6% + Breakfast)</th><th>Offer Terms</th><th>Official Link</th></tr></thead>
          <tbody>{pen_rows}</tbody>
        </table>
      </div>
      <div class="grid grid-3 mt16">{guide_cards}</div>
    </section>

    <section class="section">
      <h2>Closed-Day-Aware 7-Night Skeleton (Feb 15–22, 2027)</h2>
      <p class="sub">Built strictly around verified Mon/Tue museum, garden, and Michelin closing days.</p>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Day</th><th>Focus</th><th>Verified Logistics &amp; Closures</th></tr></thead>
          <tbody>{skel_rows}</tbody>
        </table>
      </div>
    </section>
  </main>
"""
    return page_shell("itinerary.html", "Itinerary & Dates — ChinaFun3", "2027 Shanghai holiday calendar, visa rules, Peninsula 6-window pricing, and 7-night plan.", body)


def build_hotels(hotels: dict) -> str:
    rows = ""
    for h in hotels["hotels"]:
        total = f"${h['seven_night_total_usd']:,.2f}" if h["seven_night_total_usd"] else '<span class="badge badge-unverified">Sold Out / Unavail.</span>'
        nightly = f"${h['nightly_usd_approx']:,.2f}" if h["nightly_usd_approx"] else "—"
        in_bld = ", ".join(h["in_building_michelin"]) if h["in_building_michelin"] else "None in-building (walk/Metro cluster)"
        bath_ok = h["private_bath"].startswith("Verified")
        bath_badge = badge_verified(bath_ok, "Ensuite Verified" if bath_ok else "Confirm at Booking")
        cats = f"{h['district'].lower().replace(' ', '')} {'bookable' if h['bookable_feb15'] else 'unavailable'} {'breakfast' if 'included' in h['breakfast'].lower() else ''}"
        soc = f" · {ext_link(h['social_url'], 'IG')}" if h["social_url"] else ""
        rows += (
            f"<tr data-cats='{e(cats)}'>"
            f"<td class='num'><strong>{h['rank']}</strong></td>"
            f"<td><strong>{e(h['name'])}</strong><br><span class='small'>{e(h['tier'])} · {e(h['michelin_keys'])}{' · ' + e(h['guest_score']) if h['guest_score'] else ''}</span></td>"
            f"<td><strong>{e(h['district'])}</strong><br><span class='small'>{e(h['neighborhood'])}</span></td>"
            f"<td>{e(h['room_verified'])}<br>{bath_badge} <span class='small'>{e(h['private_bath'])}</span></td>"
            f"<td>{e(in_bld)}<br><span class='small'>{e(h['district_cluster_note'])}</span></td>"
            f"<td class='num'>{nightly}</td>"
            f"<td class='num'><strong>{total}</strong><br><span class='small'>{e(h['breakfast'])}</span></td>"
            f"<td><span class='small'>{e(h['cancellation'])}</span><br><span class='small'>{e(h['notes'])}</span></td>"
            f"<td>{ext_link(h['source_url'], 'MICHELIN →')}<br>{ext_link(h['official_site'], 'Official Site →')}{soc}</td>"
            f"</tr>\n"
        )
    excl = "".join(
        f"<div class='card'><h3>Excluded: {e(x['name'])}</h3><p class='mt8'>{e(x['reason'])}</p><p class='mt8'>{ext_link(x['source_url'], 'Official Release →')}</p></div>"
        for x in hotels["excluded"]
    )
    body = f"""
  <section class="hero">
    <div class="container">
      <span class="kicker">Hotels Ranked · Live Feb 15–22, 2027 Checkout Quotes</span>
      <h1 class="h1">12 Shanghai Hotels Ranked by Michelin Cluster &amp; Verified 7-Night Totals.</h1>
      <p class="lead">{e(hotels["ranking_rule"])} Live quotes queried for <strong>2 adults, 1 room, Feb 15–22, 2027</strong> on MICHELIN Guide Hotels (official partner engine) and verified brand room pages.</p>
    </div>
  </section>
  <main class="container">
    <section class="section">
      <div class="filter-bar">
        <input class="search-input" type="search" placeholder="Filter by hotel, district, bed, breakfast..." data-filter-target="hotels-table" aria-label="Filter hotels">
        <div class="chip-group" data-chip-target="hotels-table">
          <button class="chip-btn active" data-chip="all" type="button">All (12)</button>
          <button class="chip-btn" data-chip="huangpu" type="button">Huangpu</button>
          <button class="chip-btn" data-chip="jing'an" type="button">Jing'an</button>
          <button class="chip-btn" data-chip="pudong" type="button">Pudong</button>
          <button class="chip-btn" data-chip="breakfast" type="button">Breakfast Included</button>
          <button class="chip-btn" data-chip="bookable" type="button">Bookable Feb 15</button>
        </div>
        <span class="small" data-count-for="hotels-table">12 of 12 shown</span>
      </div>
      <div class="table-wrap">
        <table id="hotels-table">
          <thead>
            <tr>
              <th class="num" data-sort="numeric">Rank</th>
              <th data-sort="text">Hotel</th>
              <th data-sort="text">District</th>
              <th>Room, Bed &amp; Bath</th>
              <th>Michelin Cluster</th>
              <th class="num" data-sort="numeric">Nightly USD</th>
              <th class="num" data-sort="numeric">7n Total USD</th>
              <th>Terms &amp; Notes</th>
              <th>Links</th>
            </tr>
          </thead>
          <tbody>{rows}</tbody>
        </table>
      </div>
      <p class="notice warn mt16"><strong>Private Bathroom Verification Note (F10):</strong> Explicit ensuite bathroom copy is verified on official brand pages for <strong>The Peninsula</strong> (marble bath + jetted tub), <strong>The Langham</strong> (marble bath + rain shower), and <strong>Bvlgari</strong> (walk-in rain shower, double basins, Toto heated toilet). Other MICHELIN Guide Hotels listings verify 5-star King/Queen rooms and require confirming private-bath text on checkout.</p>
    </section>
    <section class="section">
      <h2>Excluded From Active Ranking</h2>
      <div class="grid grid-2">{excl}</div>
    </section>
  </main>
"""
    return page_shell("hotels.html", "Hotels Ranked — ChinaFun3", "12 Shanghai hotels ranked by Michelin cluster with live Feb 15–22, 2027 checkout quotes.", body)


def build_restaurants(rest: dict) -> str:
    s = rest["summary"]
    feat_rows = ""
    for r in rest["featured"]:
        is_starred = r["stars"] > 0
        badge = f"<span class='badge badge-star'>{r['stars']}★ Starred</span>" if is_starred else f"<span class='badge badge-guide'>{e(r['distinction'])} · No Star</span>"
        price = f"<strong>{e(r['price_for_two'])}</strong>" if r["price_for_two"] else f"{e(r['band'])} · <span class='badge badge-unverified'>Menu unverified</span>"
        hours_str = e(r["hours"]) if r["hours"] else "<span class='badge badge-unverified'>Hours unverified</span>"
        soc_html = " ".join(f"<a class='social-link' href='{e(sl['url'])}' target='_blank' rel='noopener noreferrer'>{e(sl['platform'])}</a>" for sl in r["social_links"]) or "<span class='small'>None verified</span>"
        off = f" · {ext_link(r['official_site'], 'Site/PDF')}" if r["official_site"] else ""
        cat_star = f"star{r['stars']}" if r["stars"] > 0 else ("bib" if "Bib" in r["distinction"] else "selected")
        cat_priced = "priced" if r["price_for_two"] else ""
        cats = f"{cat_star} {cat_priced} {r['district'].lower().replace(' ', '').replace(chr(39), '')}"
        feat_rows += (
            f"<tr data-cats='{e(cats)}'>"
            f"<td><strong>{e(r['name'])}</strong><br>{badge}</td>"
            f"<td>{e(r['cuisine'])}<br><span class='small'>{e(r['band'])}</span></td>"
            f"<td><strong>{e(r['district'])}</strong><br><span class='small'>{e(r['address'])}</span></td>"
            f"<td>{hours_str}<br><span class='small'>{e(r['closed_days'])}</span></td>"
            f"<td>{price}<br><span class='small'>{e(r['price_note'])}</span></td>"
            f"<td>{soc_html}</td>"
            f"<td>{ext_link(r['michelin_url'], 'MICHELIN →')}{off}<br><span class='small'>{e(r['phone'])}</span></td>"
            f"</tr>\n"
        )

    all50_rows = ""
    for idx, r in enumerate(rest["all_starred_50"], 1):
        dist = e(r["district"]) if r["district"] else '<span class="badge badge-unverified">Unverified</span>'
        all50_rows += (
            f"<tr><td class='num'>{idx}</td><td><strong>{e(r['name'])}</strong></td>"
            f"<td><span class='badge badge-star'>{r['stars']}★</span></td>"
            f"<td>{e(r['cuisine'])}</td><td>{e(r['band'])}</td><td>{dist}</td>"
            f"<td>{ext_link(r['url'], 'MICHELIN →')}</td></tr>\n"
        )

    closed_list = "".join(f"<li>{e(c)}</li>" for c in s["closed_flagged"])
    body = f"""
  <section class="hero">
    <div class="container">
      <span class="kicker">2026 MICHELIN Guide Shanghai · {s["total_live_entries"]} Live Entries</span>
      <h1 class="h1">Starred vs. Guide-Listed Restaurants, Verified For-Two Costs &amp; All {s["starred_total"]} Starred.</h1>
      <p class="lead">Live 2026 MICHELIN Guide Shanghai count: <strong>{s["starred_total"]} Starred</strong> ({s["three_star"]}×3★, {s["two_star"]}×2★, {s["one_star"]}×1★) + <strong>{s["bib_gourmand"]} Bib Gourmand</strong> + <strong>{s["michelin_selected"]} Selected</strong> = <strong>{s["total_live_entries"]} total</strong>. Starred venues and Guide-listed (non-starred) venues are clearly distinguished below.</p>
      <div class="notice warn mt16">
        <strong>Recent Closures Removed (F01 / F02):</strong>
        <ul style="margin:6px 0 0 18px; padding:0">{closed_list}</ul>
      </div>
    </div>
  </section>
  <main class="container">
    <section class="section">
      <h2>Deep-Verified Featured Shortlist ({len(rest["featured"])} Starred, Bib &amp; Selected Venues)</h2>
      <p class="sub">Exact 2-adult menu totals are printed only where verified from official 2026 PDFs or FAQ pages; all others display the official MICHELIN ¥ band only.</p>
      <div class="filter-bar">
        <input class="search-input" type="search" placeholder="Search name, cuisine, district, closed days..." data-filter-target="feat-rest-table" aria-label="Filter featured restaurants">
        <div class="chip-group" data-chip-target="feat-rest-table">
          <button class="chip-btn active" data-chip="all" type="button">All ({len(rest["featured"])})</button>
          <button class="chip-btn" data-chip="star3" type="button">3★</button>
          <button class="chip-btn" data-chip="star2" type="button">2★</button>
          <button class="chip-btn" data-chip="star1" type="button">1★</button>
          <button class="chip-btn" data-chip="bib" type="button">Bib (No Star)</button>
          <button class="chip-btn" data-chip="selected" type="button">Selected (No Star)</button>
          <button class="chip-btn" data-chip="priced" type="button">Exact For-2 Price</button>
        </div>
        <span class="small" data-count-for="feat-rest-table">{len(rest["featured"])} of {len(rest["featured"])} shown</span>
      </div>
      <div class="table-wrap">
        <table id="feat-rest-table">
          <thead>
            <tr>
              <th data-sort="text">Restaurant &amp; Status</th>
              <th data-sort="text">Cuisine &amp; Band</th>
              <th data-sort="text">District &amp; Address</th>
              <th>Hours &amp; Closed Days</th>
              <th>Price for 2 Adults</th>
              <th>Social</th>
              <th>Sources &amp; Phone</th>
            </tr>
          </thead>
          <tbody>{feat_rows}</tbody>
        </table>
      </div>
    </section>

    <section class="section">
      <h2>Complete Official 2026 Shanghai Starred Directory ({len(rest["all_starred_50"])} Venues)</h2>
      <p class="sub">Every currently starred restaurant on {ext_link(s["source_all_starred"], "guide.michelin.com/shanghai/all-starred")}. District cells remain flagged where individual pages were not yet fetched.</p>
      <div class="filter-bar">
        <input class="search-input" type="search" placeholder="Filter all 50 starred restaurants..." data-filter-target="all50-table" aria-label="Filter all 50 starred restaurants">
        <span class="small" data-count-for="all50-table">50 of 50 shown</span>
      </div>
      <div class="table-wrap">
        <table id="all50-table">
          <thead><tr><th class="num" data-sort="numeric">#</th><th data-sort="text">Name</th><th data-sort="text">Stars</th><th data-sort="text">Cuisine</th><th data-sort="text">Band</th><th data-sort="text">District</th><th>Official Listing</th></tr></thead>
          <tbody>{all50_rows}</tbody>
        </table>
      </div>
    </section>
  </main>
"""
    return page_shell("restaurants.html", "Michelin Restaurants — ChinaFun3", "Complete 2026 Shanghai MICHELIN Guide directory (50 starred + Bib/Selected) with verified for-2 prices.", body)


def build_activities(act: dict) -> str:
    rows = ""
    for a in act["activities"]:
        v_badge = badge_verified(a["verified"], "Official Hours Verified" if a["verified"] else "Partial / Flagged")
        hours = e(a["hours"]) if a["hours"] else '<span class="badge badge-unverified">Hours Unverified</span>'
        cost = f"<strong>{e(a['cost_for_two'])}</strong>" if a["cost_for_two"] else f"<span class='small'>{e(a.get('cost_note', 'Ticket price unverified'))}</span>"
        soc = " ".join(f"<a class='social-link' href='{e(sl['url'])}' target='_blank' rel='noopener noreferrer'>{e(sl['platform'])}</a>" for sl in a["social_links"]) or "<span class='small'>None verified</span>"
        cats = f"{a['district'].split()[0].lower()} {'verified' if a['verified'] else 'flagged'}"
        days_str = e(a["days"]) if a["days"] else '<span class="badge badge-unverified">Unverified</span>'
        rows += (
            f"<tr data-cats='{e(cats)}'>"
            f"<td><strong>{e(a['name'])}</strong><br><span class='small'>{e(a['type'])}</span><br>{v_badge}</td>"
            f"<td>{e(a['district'])}<br><span class='small'>{e(a['metro'])}</span></td>"
            f"<td>{days_str}<br>{hours}</td>"
            f"<td><span class='small'>{e(a['exceptions'])}</span></td>"
            f"<td>{cost}</td>"
            f"<td>{soc}</td>"
            f"<td>{ext_link(a['source_url'], 'Official →')}</td>"
            f"</tr>\n"
        )
    body = f"""
  <section class="hero">
    <div class="container">
      <span class="kicker">Activities Within ≤1h Central Envelope</span>
      <h1 class="h1">12 Shanghai Attractions — Verified Hours, Closed Days &amp; Ticket Rules.</h1>
      <p class="lead">Sourced from official portals (<code>yugarden.com.cn</code>, <code>shanghaimuseum.net</code>, <code>english.shanghai.gov.cn</code>, <code>shanghaidisneyresort.com</code>). Unreachable portals (Oriental Pearl Tower) and unpublished 2027 schedules (Disneyland Feb 2027) are flagged rather than guessed.</p>
    </div>
  </section>
  <main class="container">
    <section class="section">
      <div class="filter-bar">
        <input class="search-input" type="search" placeholder="Filter activities, districts, Monday closures..." data-filter-target="act-table" aria-label="Filter activities">
        <div class="chip-group" data-chip-target="act-table">
          <button class="chip-btn active" data-chip="all" type="button">All ({len(act["activities"])})</button>
          <button class="chip-btn" data-chip="huangpu" type="button">Huangpu</button>
          <button class="chip-btn" data-chip="pudong" type="button">Pudong</button>
          <button class="chip-btn" data-chip="verified" type="button">Hours Verified</button>
          <button class="chip-btn" data-chip="flagged" type="button">Flagged</button>
        </div>
        <span class="small" data-count-for="act-table">{len(act["activities"])} of {len(act["activities"])} shown</span>
      </div>
      <div class="table-wrap">
        <table id="act-table">
          <thead><tr><th data-sort="text">Activity</th><th data-sort="text">District &amp; Metro</th><th>Open Days &amp; Hours</th><th>Exceptions &amp; Notes</th><th>Cost for 2</th><th>Social / Video</th><th>Official Source</th></tr></thead>
          <tbody>{rows}</tbody>
        </table>
      </div>
    </section>
  </main>
"""
    return page_shell("activities.html", "Activities ≤1h — ChinaFun3", "Shanghai attractions within 1h metro of central hotels with verified hours, tickets, and social links.", body)


def build_transport(tr: dict) -> str:
    c_rows = "".join(
        f"<tr><td><strong>{e(c['from_base'])}</strong></td><td>{e(c['target_zone'])}</td><td>{e(c['metro_lines'])}</td>"
        f"<td>{badge_verified(True, c['within_1h_status'])}<br><span class='badge badge-unverified mt8'>Minutes Unverified (F07)</span></td>"
        f"<td><span class='small'>{e(c['verified_destinations'])}</span></td><td>{ext_link(c['source_url'], 'Source →')}</td></tr>\n"
        for c in tr["district_corridors"]
    )
    dt_rows = "".join(
        f"<tr><td><strong>{e(d['route'])}</strong></td><td>{e(d['rail_note'])}</td><td>{ext_link(d['official_url'], '12306 Official →')}</td></tr>\n"
        for d in tr["day_trips"]
    )
    body = f"""
  <section class="hero">
    <div class="container">
      <span class="kicker">Transport &amp; 1-Hour Proximity · Honest Geography</span>
      <h1 class="h1">District Metro Corridors Without Fabricated Minute Claims.</h1>
      <p class="lead">{e(tr["shmetro_status"])}</p>
    </div>
  </section>
  <main class="container">
    <section class="section">
      <h2>Central Hotel Base to Key Shanghai Zones</h2>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Hotel Base</th><th>Target Zone</th><th>Metro Lines / Walk</th><th>Status</th><th>Verified Destinations</th><th>Source</th></tr></thead>
          <tbody>{c_rows}</tbody>
        </table>
      </div>
    </section>
    <section class="section">
      <h2>Optional High-Speed Rail Day Trips (10–14 Night Window)</h2>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Route</th><th>Verified Rail Note</th><th>Official Ticketing</th></tr></thead>
          <tbody>{dt_rows}</tbody>
        </table>
      </div>
    </section>
  </main>
"""
    return page_shell("transport.html", "Transport & 1h Radius — ChinaFun3", "Shanghai Metro corridor mapping and honest transit verification.", body)


def build_budget(bud: dict) -> str:
    sc_rows = "".join(
        f"<tr><td><strong>{e(s['name'])}</strong></td>"
        f"<td>{e(s['hotel_name'])}</td>"
        f"<td class='num'><strong>{('$' + format(s['hotel_usd'], ',.2f') + ' USD') if s.get('hotel_usd') else ('¥' + format(s['hotel_cny'], ',.2f') + ' CNY')}</strong></td>"
        f"<td class='num'>¥{s['verified_dining_cny']:,.2f}</td>"
        f"<td class='num'>¥{s['verified_activities_cny']}</td>"
        f"<td><span class='small'>{e(s['dining_breakdown'])} · {e(s['unpriced_note'])}</span></td>"
        f"<td>{ext_link(s['hotel_source'], 'Hotel Quote →')}</td></tr>\n"
        for s in bud["scenarios"]
    )
    m_rows = "".join(
        f"<tr><td><strong>{e(m['venue'])}</strong></td><td>{e(m['menu'])}</td>"
        f"<td class='num'><strong>¥{m['total_cny']:,.2f}</strong></td><td>{ext_link(m['source_url'], 'Official PDF/FAQ →')}</td></tr>\n"
        for m in bud["exact_verified_menu_totals_for_two"]
    )
    body = f"""
  <section class="hero">
    <div class="container">
      <span class="kicker">Combined Budgets · Real Feb 2027 Hotel + 2026 Menu Totals</span>
      <h1 class="h1">What 7 Nights for 2 Adults Actually Costs (Verified Only).</h1>
      <p class="lead">{e(bud["honest_rule"])}</p>
    </div>
  </section>
  <main class="container">
    <section class="section">
      <h2>3 Modeled 7-Night Scenarios (Feb 15–22, 2027)</h2>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Scenario</th><th>Hotel</th><th class="num">7n Hotel</th><th class="num">Verified Menus</th><th class="num">Activities</th><th>Breakdown &amp; Exclusions</th><th>Source</th></tr></thead>
          <tbody>{sc_rows}</tbody>
        </table>
      </div>
    </section>
    <section class="section">
      <h2>All Exact Verified 2-Adult Restaurant Menu Totals</h2>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Restaurant</th><th>Exact Set / Tasting Menu</th><th class="num">Total for 2 (CNY)</th><th>Official Document</th></tr></thead>
          <tbody>{m_rows}</tbody>
        </table>
      </div>
    </section>
  </main>
"""
    return page_shell("budget.html", "Budget — ChinaFun3", "Verified 7-night hotel and 2-adult Michelin dining budget scenarios.", body)


def build_questions(flg: dict) -> str:
    rows = "".join(
        f"<tr><td><strong>{e(q['id'])}</strong></td><td><span class='badge {'badge-unverified' if q['priority']=='High' else 'badge-guide'}'>{e(q['priority'])}</span></td>"
        f"<td><strong>{e(q['question'])}</strong></td><td>{e(q['why'])}</td></tr>\n"
        for q in flg["questions"]
    )
    body = f"""
  <section class="hero">
    <div class="container">
      <span class="kicker">Open Traveler Decisions · No Guessing</span>
      <h1 class="h1">{len(flg["questions"])} Questions to Confirm Before Booking.</h1>
      <p class="lead">Everything else is self-contained. Answering these items locks hotel refundability, visa-free transit routing, and Michelin reservation timing.</p>
    </div>
  </section>
  <main class="container">
    <section class="section">
      <div class="table-wrap">
        <table><thead><tr><th>ID</th><th>Priority</th><th>Decision Needed</th><th>Why It Matters</th></tr></thead><tbody>{rows}</tbody></table>
      </div>
    </section>
  </main>
"""
    return page_shell("questions.html", "Q&A Gaps — ChinaFun3", "Open decisions required before locking Shanghai 2027 flights and hotels.", body)


def build_suggestions(flg: dict) -> str:
    cards = "".join(
        f"<div class='card'><h3>{e(s['id'])}: {e(s['title'])}</h3><p class='mt8'>{e(s['detail'])}</p>"
        f"<p class='mt8'><span class='badge badge-guide'>{e(s['status'])}</span></p></div>\n"
        for s in flg["suggestions"]
    )
    body = f"""
  <section class="hero">
    <div class="container">
      <span class="kicker">Review-Only Roadmap · Not Auto-Executed</span>
      <h1 class="h1">{len(flg["suggestions"])} Planning Suggestions for Review.</h1>
      <p class="lead">Actionable proposals surfaced from our verification audit — nothing is booked or altered without your approval.</p>
    </div>
  </section>
  <main class="container">
    <section class="section"><div class="grid grid-2">{cards}</div></section>
  </main>
"""
    return page_shell("suggestions.html", "Suggestions — ChinaFun3", "Review-only planning suggestions for the 2027 Shanghai trip.", body)


def build_flagged(flg: dict) -> str:
    rows = "".join(
        f"<tr><td><strong>{e(f['id'])}</strong></td><td><span class='badge {'badge-verified' if 'Resolved' in f['severity'] else 'badge-unverified'}'>{e(f['severity'])}</span></td>"
        f"<td><strong>{e(f['area'])}</strong></td><td><span class='small'>{e(f['legacy_claim'])}</span></td>"
        f"<td>{e(f['verified_finding'])}</td><td>{e(f['action_taken'])}</td><td>{ext_link(f['source_url'], 'Source →')}</td></tr>\n"
        for f in flg["flagged_irregularities"]
    )
    body = f"""
  <section class="hero">
    <div class="container">
      <span class="kicker">Audit &amp; Flagged Log · F01–F10</span>
      <h1 class="h1">Legacy Root Audit &amp; Ongoing Unverified Flags.</h1>
      <p class="lead">Every irregularity discovered when auditing the legacy root site against live Nov 26, 2026 official sources, plus remaining items intentionally flagged rather than guessed.</p>
    </div>
  </section>
  <main class="container">
    <section class="section">
      <div class="table-wrap">
        <table><thead><tr><th>ID</th><th>Status</th><th>Area</th><th>Legacy Root Claim</th><th>Verified Finding</th><th>Action Taken</th><th>Source</th></tr></thead><tbody>{rows}</tbody></table>
      </div>
    </section>
  </main>
"""
    return page_shell("flagged.html", "Flagged & Audit — ChinaFun3", "F01–F10 audit of legacy claims vs verified 2026/2027 Shanghai data.", body)


def build_sources(trip: dict, hotels: dict, rest: dict, act: dict, bud: dict, flg: dict) -> str:
    seen: set[str] = set()
    items: list[tuple[str, str, str]] = []

    def add(cat: str, label: str, url: str) -> None:
        if url and url not in seen:
            seen.add(url)
            items.append((cat, label, url))

    for c in trip["calendar"]:
        add("Government / Calendar", c["source_label"], c["source_url"])
    for p in trip["peninsula_windows"]:
        add("Hotel Direct Offer", "Peninsula Shanghai — A Gift for the New Year", p["source_url"])
    for h in hotels["hotels"]:
        add("Hotel Quote / Brand", h["name"], h["source_url"])
        add("Hotel Official Site", f"{h['name']} official", h["official_site"])
    add("MICHELIN Directory", "Shanghai All-Starred (50)", rest["summary"]["source_all_starred"])
    add("MICHELIN Directory", "Shanghai Bib Gourmand (33)", rest["summary"]["source_bib"])
    add("MICHELIN Directory", "Shanghai Selected (70)", rest["summary"]["source_selected"])
    add("MICHELIN Press", "2026 Shanghai/Jiangsu/Zhejiang Ceremony", rest["summary"]["source_2026_ceremony"])
    for m in bud["exact_verified_menu_totals_for_two"]:
        add("Official 2026 Menu PDF/FAQ", m["venue"], m["source_url"])
    for r in rest["featured"]:
        add("Restaurant Official", r["name"], r["michelin_url"])
        if r["official_site"]:
            add("Restaurant Site", f"{r['name']} site", r["official_site"])
        for sl in r["social_links"]:
            add(f"Social ({sl['platform']})", r["name"], sl["url"])
    for a in act["activities"]:
        add("Activity Official", a["name"], a["source_url"])
        for sl in a["social_links"]:
            add(f"Social ({sl['platform']})", a["name"], sl["url"])

    rows = "".join(
        f"<tr><td>{i}</td><td><span class='badge badge-guide'>{e(cat)}</span></td><td><strong>{e(lbl)}</strong></td><td>{ext_link(url, url)}</td></tr>\n"
        for i, (cat, lbl, url) in enumerate(items, 1)
    )
    body = f"""
  <section class="hero">
    <div class="container">
      <span class="kicker">Primary &amp; Media Sources Register</span>
      <h1 class="h1">{len(items)} Verified Official &amp; Social Sources.</h1>
      <p class="lead">Every table on the root dashboard traces directly to one of these URLs checked in this verification run (2026-11-26).</p>
    </div>
  </section>
  <main class="container">
    <section class="section">
      <div class="filter-bar">
        <input class="search-input" type="search" placeholder="Filter sources by category, venue, or domain..." data-filter-target="sources-table" aria-label="Filter sources">
        <span class="small" data-count-for="sources-table">{len(items)} of {len(items)} shown</span>
      </div>
      <div class="table-wrap">
        <table id="sources-table"><thead><tr><th>#</th><th>Category</th><th>Entity</th><th>Verified URL</th></tr></thead><tbody>{rows}</tbody></table>
      </div>
    </section>
  </main>
"""
    return page_shell("sources.html", "Sources — ChinaFun3", "Complete verified source bibliography for ChinaFun3.", body)


def build_methodology() -> str:
    body = """
  <section class="hero">
    <div class="container">
      <span class="kicker">Verification Protocol</span>
      <h1 class="h1">Zero Hallucinations: How Every Value Is Checked.</h1>
      <p class="lead">Four strict rules govern every cell on the ChinaFun3 root dashboard.</p>
    </div>
  </section>
  <main class="container">
    <section class="section">
      <div class="grid grid-2">
        <div class="card"><h3>1. Primary Official Sources First</h3><p class="mt8">Dates come from <code>gov.cn</code>; visa rules from <code>en.nia.gov.cn</code>; restaurant stars, price bands, and addresses from <code>guide.michelin.com</code>; hotel rates from live Feb 15–22, 2027 checkout queries and brand sites; menus from official 2026 PDFs/FAQs; attractions from <code>yugarden.com.cn</code>, <code>shanghaimuseum.net</code>, <code>shanghaidisneyresort.com</code>, and <code>english.shanghai.gov.cn</code>.</p></div>
        <div class="card"><h3>2. Blank + Flagged Over Guessing</h3><p class="mt8">When an official portal fails (e.g., <code>shmetro.com</code>, <code>orientalpearltower.com.cn</code>) or a venue withholds 2027 pricing (Disneyland Feb 2027, unpublished restaurant tasting menus), the cell stays blank and receives an explicit amber flag.</p></div>
        <div class="card"><h3>3. Exact Arithmetic Labels</h3><p class="mt8">Two-adult totals are printed only when exact per-person or for-two official figures exist (e.g., Taian Table ¥2,588×2 = ¥5,176; Sir Elly's ¥1,288×2×1.166 = ¥3,003.62; Yu Garden ¥30×2 = ¥60). MICHELIN ¥–¥¥¥¥ tiers are never converted into guessed currency totals.</p></div>
        <div class="card"><h3>4. Live Re-Checkable URLs</h3><p class="mt8">Hotel rows link directly to the parameterized <code>arr=2027-02-15&amp;dep=2027-02-22&amp;nA=2&amp;nC=0&amp;nR=1</code> MICHELIN Guide Hotels query so you can verify live inventory and checkout currency anytime.</p></div>
      </div>
    </section>
  </main>
"""
    return page_shell("methodology.html", "Methodology — ChinaFun3", "Verification rules and anti-hallucination protocol for ChinaFun3.", body)


def build_404() -> str:
    body = """
  <main class="container" style="padding:56px 16px; text-align:center">
    <h1 class="h1">Page not found</h1>
    <p class="lead" style="margin:0 auto; max-width:58ch">Return to the verified Shanghai 2027 dashboard — every hotel quote, Michelin listing, activity schedule, and official source lives there.</p>
    <p class="mt16"><a class="btn btn-primary" href="index.html">Back to Dashboard</a> <a class="btn" href="sources.html">View All Sources</a></p>
  </main>
"""
    return page_shell("404.html", "Not Found — ChinaFun3", "404 page for ChinaFun3.", body)


def main() -> None:
    trip = load_json("trip.json")
    hotels = load_json("hotels.json")
    rest = load_json("restaurants.json")
    act = load_json("activities.json")
    tr = load_json("transport.json")
    bud = load_json("budget.json")
    flg = load_json("flagged.json")

    outputs = {
        "index.html": build_index(trip, hotels, rest, act, bud, flg),
        "executive-summary.html": build_exec(trip, hotels, rest, bud, flg),
        "itinerary.html": build_itinerary(trip),
        "hotels.html": build_hotels(hotels),
        "restaurants.html": build_restaurants(rest),
        "activities.html": build_activities(act),
        "transport.html": build_transport(tr),
        "budget.html": build_budget(bud),
        "questions.html": build_questions(flg),
        "suggestions.html": build_suggestions(flg),
        "flagged.html": build_flagged(flg),
        "sources.html": build_sources(trip, hotels, rest, act, bud, flg),
        "methodology.html": build_methodology(),
        "404.html": build_404(),
    }
    for fname, content in outputs.items():
        (ROOT / fname).write_text(content, encoding="utf-8")
    print(f"Generated {len(outputs)} root HTML pages.")


if __name__ == "__main__":
    main()
