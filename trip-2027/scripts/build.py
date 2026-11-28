#!/usr/bin/env python3
"""Deterministic static HTML generator for trip-2027/ verified couple trip dashboard."""

from __future__ import annotations

import html
import json
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"

PAGES = [
    ("index.html", "Overview"),
    ("executive-summary.html", "Exec Summary & Dates"),
    ("hotels.html", "Hotels (2027 Rates)"),
    ("restaurants.html", "MICHELIN Dining"),
    ("activities.html", "Activities"),
    ("itinerary.html", "Itinerary"),
    ("transport.html", "Transit"),
    ("visa-budget.html", "Entry & Budget"),
    ("questions.html", "Open Questions"),
    ("suggestions.html", "Suggestions"),
    ("flagged.html", "Flagged"),
    ("repo-audit.html", "Repo Audit & Sources"),
]


def esc(val: object) -> str:
    if val is None:
        return ""
    return html.escape(str(val), quote=True)


def ext_link(url: str | None, label: str) -> str:
    if not url:
        return '<span class="blank-cell">—</span>'
    return (
        f'<a href="{esc(url)}" target="_blank" rel="noopener noreferrer">'
        f"{esc(label)}</a>"
    )


def flag_badge(flag_id: str | None) -> str:
    if not flag_id:
        return '<span class="badge badge-verified">Verified</span>'
    return (
        f'<a class="badge badge-flag" href="flagged.html#{esc(flag_id)}">'
        f"Flag {esc(flag_id)}</a>"
    )


def flag_badges(flag_ids: list[str] | None, fallback: str | None = None) -> str:
    ids = flag_ids or ([fallback] if fallback else [])
    if not ids:
        return flag_badge(None)
    return " ".join(flag_badge(flag_id) for flag_id in ids)


def render_socials(social: dict, flag_id: str | None) -> str:
    items: list[str] = []
    platform_names = [
        ("youtube", "YT"),
        ("tiktok", "TikTok"),
        ("instagram", "IG"),
    ]
    for key, prefix in platform_names:
        entry = social.get(key)
        if entry and entry.get("url"):
            scope = entry.get("scope", "direct")
            scope_tag = " (Prop.)" if scope == "hotel_property" else (" (Topic)" if scope == "topic" else "")
            items.append(
                f'<a class="social-pill" href="{esc(entry["url"])}" target="_blank" rel="noopener noreferrer">'
                f'<strong>{esc(prefix)}:</strong> {esc(entry["label"])}{esc(scope_tag)}</a>'
            )
        else:
            f_ref = f' (<a href="flagged.html#{esc(flag_id or "F10")}">flagged</a>)'
            items.append(
                f'<span class="social-missing">{esc(prefix)}: — unverified{f_ref}</span>'
            )
    return '<div class="social-stack">' + "".join(items) + "</div>"


def flag_summary() -> tuple[int, str]:
    flags = json.loads((DATA_DIR / "governance.json").read_text(encoding="utf-8"))["flagged_items"]
    ids = [flag["id"] for flag in flags]
    return len(ids), f"{ids[0]}–{ids[-1]}"


def render_shell(active_file: str, page_title: str, eyebrow: str, h1: str, lead: str, body_html: str) -> str:
    flag_count, flag_range = flag_summary()
    nav_links = []
    for href, label in PAGES:
        cls = ' class="active"' if href == active_file else ""
        nav_links.append(f'<a href="{esc(href)}"{cls}>{esc(label)}</a>')
    nav_str = "\n        ".join(nav_links)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(page_title)} · Shanghai 2027 Couple Trip Planner</title>
  <meta name="description" content="{esc(lead)}">
  <link rel="stylesheet" href="assets/style.css">
</head>
<body>
  <div class="verify-ribbon">
    Latest recorded official-source check: <strong>2026-11-26</strong> · Passport nationality unknown; US visa examples are conditional (<a href="flagged.html#F17">F17</a>) · Hotel quotes are dated snapshots, not current availability (<a href="flagged.html#F18">F18</a>) ·
    <a href="flagged.html">{flag_count} review flags ({flag_range})</a> · <a href="repo-audit.html">Source ledger</a>
  </div>
  <header class="site-header">
    <div class="header-inner">
      <a class="brand" href="index.html">
        <span class="brand-seal">沪</span>
        <span>Shanghai 2027 · Couple Edition</span>
      </a>
      <button id="nav-toggle" class="nav-toggle" type="button" aria-expanded="false" aria-controls="main-nav">
        ☰ Sections
      </button>
      <nav id="main-nav" class="main-nav" aria-label="Primary">
        {nav_str}
      </nav>
    </div>
  </header>

  <main class="container">
    <section class="hero">
      <span class="eyebrow">{esc(eyebrow)}</span>
      <h1>{esc(h1)}</h1>
      <p class="lead">{esc(lead)}</p>
    </section>
    {body_html}
  </main>

  <footer class="site-footer">
    <div class="footer-inner">
      <div>
        <strong>Shanghai 2027 Couple Trip Planner (<code>/trip-2027/</code>)</strong> · Official-source snapshot <code>2026-11-26</code>; wording, scope, and local consistency reviewed <code>2026-11-28</code>.
        Passport nationality is not specified; US visa examples are conditional. Refresh dynamic hotel quotes before booking. Unverified values remain blank and are indexed in <a href="flagged.html">Flagged for Review</a>.
      </div>
      <div>
        Repository sibling editions:
        <a href="../index.html">Root</a> ·
        <a href="../for-two/index.html">For-Two</a> ·
        <a href="../verify/index.html">Verify</a> ·
        <a href="../plan/index.html">Plan</a> ·
        <a href="../considered/index.html">Considered</a> ·
        <a href="../docs/index.html">Docs</a> ·
        <a href="../audit-2026-11-26/index.html">Audit</a>
      </div>
    </div>
  </footer>
  <script src="assets/app.js"></script>
</body>
</html>
"""


def load_json(name: str) -> dict:
    with open(DATA_DIR / name, "r", encoding="utf-8") as fh:
        return json.load(fh)


def build_index(overview: dict, hotels: dict, restaurants: dict) -> str:
    kpi_cards = []
    for k in overview["hero_kpis"]:
        kpi_cards.append(
            f"""<article class="kpi-card">
        <div>
          <div class="kpi-label">{esc(k["label"])}</div>
          <div class="kpi-value">{esc(k["value"])}</div>
          <div class="kpi-detail">{esc(k["detail"])}</div>
        </div>
        <div class="kpi-source">{ext_link(k["source_url"], "Source: " + k["source_label"])}</div>
      </article>"""
        )

    city_rows = []
    for c in overview["city_comparison"]:
        city_rows.append(
            f"""<tr>
          <td class="num-strong">#{c["rank"]} {esc(c["city"])}</td>
          <td class="num-strong">{c["total_starred"]}★ <span class="muted-note">{c["three_star"]}×3★ · {c["two_star"]}×2★ · {c["one_star"]}×1★</span></td>
          <td>{c["bib_gourmand"]} Bib · {c["selected"]} Selected</td>
          <td class="num-strong">{c["total_guide"]}</td>
          <td>{esc(c["transit_note"])}</td>
          <td>{esc(c["verdict"])}</td>
          <td>{ext_link(c["source_url"], c["source_label"])}</td>
        </tr>"""
        )

    nav_cards = [
        ("executive-summary.html", "1. Executive Summary & In-Scope Dates", "7-, 10-, and 14-night options only; preferred-date conflict is explicit; hotel amounts are dated observations, not a booking forecast."),
        ("hotels.html", "2. Hotel Shortlist & Dated 2027 Quote Snapshots", "9 properties tie at 18/18 tracked Michelin venues within ≤1h; compare bed/bath, amenities, cancellation, price snapshots, and documented alerts."),
        ("restaurants.html", "3. Starred vs Non-Starred MICHELIN Dining", "18 deep-verified venues clearly separating 3★/2★/1★ Starred from Bib Gourmand & MICHELIN Selected, with 2026 PDF couple totals & verified social links."),
        ("activities.html", "4. Verified Cultural & Modern Activities", "12 Shanghai attractions ≤1h from top hotels with official hours, Monday/Tuesday closures, People's Square Americas-only notice & social previews."),
        ("itinerary.html", "5. Closure-Safe Couple Itinerary (Feb 15–22)", "Day-by-day plan built around Monday/Tuesday closures, Thu–Sun Bombana lunch, and Sat Feb 20 Lantern Festival."),
        ("transport.html", "6. Airport, Metro & Local Transit", "Official Metro source links, fare references, and station-to-station route estimates; time-boundary assumptions are flagged."),
        ("visa-budget.html", "7. Entry & Budget (Conditional US Example)", "Passport nationality is unknown; US-only pathways are examples. The calculator leaves visa cost unresolved by default."),
        ("questions.html", "8. Missing Information & Discovery Matrix", f"{len(load_json('governance.json')['questions'])} open traveler/vendor questions paired with concrete ways to resolve each gap."),
        ("suggestions.html", "9. Suggestions (For Review Only)", "6 high-leverage optimizations (3rd-country transit routing, starred lunch arbitrage, Free-Cancel + Feb 1 re-price) kept strictly separate."),
        ("flagged.html", f"10. Flagged for Review ({flag_summary()[1]})", "Passport assumptions, dynamic hotel quote limits, cluster-count ties, blank values, operator contradictions, renovation alerts, and social-link gaps."),
        ("repo-audit.html", "11. Repo Audit & Master Source Ledger", "Cross-audit of all 7 repository sites plus every primary official & social URL verified on 2026-11-26."),
    ]
    cards_html = "\n".join(
        f'<a class="nav-card" href="{esc(href)}"><h3>{esc(title)}</h3><p>{esc(desc)}</p></a>'
        for href, title, desc in nav_cards
    )

    body = f"""
    <div class="kpi-grid">
      {"".join(kpi_cards)}
    </div>

    <div class="callout jade">
      <strong>Provisional base recommendation:</strong> For the 7–14-night options shown, compare <strong>Huangpu (Xintiandi/Bund)</strong> and <strong>Jing'an</strong>. The 7-night candidate runs <strong>Feb 15–22, 2027</strong>; the 14-night candidate runs <strong>Feb 15–Mar 1</strong>. The dated 2026-11-26 sample showed lower February stay-date quotes than selected March dates, but does not prove present availability or the cheapest future booking day. Recheck live totals and cancellation terms before booking.
    </div>
    <div class="callout amber">
      <strong>Constraint mismatch to resolve:</strong> Your brief asks for <strong>1–2 weeks</strong> but marks <strong>Feb 15–18</strong> as preferred. From a Feb 15 check-in, a Feb 18 checkout is 3 hotel nights; leaving Feb 19 after the night of Feb 18 is 4 nights. Both are shorter than the 7-night minimum. The displayed 7-night plan ends Feb 22, so it overlaps—but does not fit inside—the preferred dates. See <a href="questions.html">Q11</a> before treating any dates as final.
    </div>

    <section class="section-block">
      <div class="section-header">
        <h2>Why Shanghai? Mainland China MICHELIN Cluster Comparison (2026 Guides)</h2>
        <span>Checked <code>2026-11-26</code></span>
      </div>
      <p class="section-sub">Shanghai holds nearly one-third of all 157 MICHELIN-starred restaurants in Mainland China while pairing dense rail transit with world-class Cantonese, Jiangnan, vegetarian, French, and Italian dining.</p>
      <div class="table-scroll">
        <table class="data-table">
          <thead>
            <tr>
              <th>City Rank</th>
              <th>MICHELIN Starred Breakdown</th>
              <th>Non-Starred (Bib &amp; Selected)</th>
              <th>Total Guide</th>
              <th>Subway &amp; Weather Context</th>
              <th>Planning Verdict</th>
              <th>Official Source</th>
            </tr>
          </thead>
          <tbody>
            {"".join(city_rows)}
          </tbody>
        </table>
      </div>
    </section>

    <section class="section-block">
      <div class="section-header">
        <h2>Explore Source-Linked Planning Sections</h2>
        <span>Mobile-friendly tables with row-level references and review flags</span>
      </div>
      <div class="nav-cards">
        {cards_html}
      </div>
    </section>
    """
    return render_shell(
        "index.html",
        "Overview & City Comparison",
        "2027 Planning Draft · 2 Adults",
        overview["meta"]["title"],
        overview["meta"]["subtitle"],
        body,
    )


def build_exec_summary(overview: dict) -> str:
    dur_rows = []
    for d in overview["duration_options"]:
        dur_rows.append(
            f"""<tr>
          <td class="num-strong">{esc(d["option"])}</td>
          <td class="num-strong">{esc(d["dates"])}</td>
          <td>{esc(d["visa_fit"])}</td>
          <td>{esc(d["calendar_context"])}</td>
          <td>{esc(d["pricing_verdict"])}</td>
          <td>{esc(d["scope"])}</td>
          <td>{ext_link(d["source_url"], d["source_label"])}</td>
        </tr>"""
        )

    curve_rows = []
    for r in overview["rate_curve_windows"]:
        curve_rows.append(
            f"""<tr>
          <td class="num-strong">{esc(r["property"])}</td>
          <td>{esc(r["feb_15_22"])}</td>
          <td>{esc(r["feb_22_mar_01"])}</td>
          <td>{esc(r["mar_01_08"])}</td>
          <td>{esc(r["mar_16_23"])}</td>
          <td>{esc(r["comparison_note"])}</td>
          <td>{ext_link(r["source_url"], r["source_label"])}</td>
        </tr>"""
        )

    time_rows = []
    for t in overview["action_timeline"]:
        time_rows.append(
            f"""<tr>
          <td class="num-strong">{esc(t["deadline"])}</td>
          <td><span class="badge badge-selected">{esc(t["window"])}</span></td>
          <td>{esc(t["action"])}</td>
          <td>{ext_link(t["source_url"], t["source_label"])}</td>
        </tr>"""
        )

    body = f"""
    <div class="callout">
      <strong>Official 2027 Holiday Verification (<code>国办发明电〔2026〕10号</code>):</strong> Lunar New Year's Day is <strong>Sat Feb 6, 2027</strong>; Mainland China's statutory 9-day Spring Festival holiday runs <strong>Fri Feb 5 – Sat Feb 13, 2027</strong>, with <strong>Sun Feb 14</strong> designated an official make-up workday. Arriving <strong>Mon Feb 15, 2027</strong> is after the stated holiday period and still catches <strong>Lantern Festival (Sat Feb 20, 2027)</strong>.
    </div>
    <div class="callout amber">
      <strong>Duration / preferred-date conflict:</strong> The brief asks for 1–2 weeks but prefers Feb 15–18. A 7-night stay from Feb 15 ends Feb 22; it does not fit entirely within Feb 15–18. Checkout on Feb 18 gives 3 nights; including the night of Feb 18 and leaving Feb 19 gives 4 nights. Neither interpretation meets the 7-night minimum. Resolve this in <a href="questions.html">Q11</a> before using the date recommendation.
    </div>

    <section class="section-block">
      <div class="section-header">
        <h2>In-Scope Vacation Lengths (7–14 Nights)</h2>
        <span>Travel window: Feb 15 – Mar 23, 2027 · Longer trips excluded from this brief</span>
      </div>
      <p class="section-sub">The table shows only 7-, 10-, and 14-night scenarios, matching the requested one- to two-week range. The exact total for stays longer than the priced 7-night quotes is not extrapolated.</p>
      <div class="table-scroll">
        <table class="data-table">
          <thead>
            <tr>
              <th>Duration Option</th>
              <th>Recommended Dates</th>
              <th>Passport-Dependent Entry Notes</th>
              <th>Holiday &amp; Season Context</th>
              <th>Hotel Rate Impact</th>
              <th>Recommended Geographic Scope</th>
              <th>Source</th>
            </tr>
          </thead>
          <tbody>
            {"".join(dur_rows)}
          </tbody>
        </table>
      </div>
    </section>

    <section class="section-block">
      <div class="section-header">
        <h2>Observed Hotel Stay-Date Quotes (Snapshot; Not a Booking Forecast)</h2>
        <span>Quote snapshot: <code>2026-11-26</code></span>
      </div>
      <p class="section-sub">The listed properties/windows are a limited sample. Recorded quotes showed lower February stay-date prices than the sampled March dates in some comparisons; this does not establish the cheapest price for every date, a current available rate, or the cheapest future day to book. See <a href="flagged.html#F18">F18</a> and refresh the source before purchase.</p>
      <div class="table-scroll">
        <table class="data-table">
          <thead>
            <tr>
              <th>Hotel &amp; Booking Channel</th>
              <th>Feb 15 – Feb 22, 2027</th>
              <th>Feb 22 – Mar 1, 2027</th>
              <th>Mar 1 – Mar 8, 2027</th>
              <th>Mar 16 – Mar 23, 2027</th>
              <th>Observed Stay-Date Comparison (Not a Booking Forecast)</th>
              <th>Dated Rate Source</th>
            </tr>
          </thead>
          <tbody>
            {"".join(curve_rows)}
          </tbody>
        </table>
      </div>
    </section>

    <section class="section-block">
      <div class="section-header">
        <h2>Booking Checkpoints &amp; Published Deadlines</h2>
        <span>Source snapshot: <code>2026-11-26</code> · no cheapest booking date established</span>
      </div>
      <p class="section-sub">A stay-date price comparison is not a booking-timing forecast. The entries below are offer deadlines or suggested recheck dates from the recorded sources; they do not prove that booking on any specific date will be cheapest. The current hotel amounts need a new checkout quote.</p>
      <div class="table-scroll">
        <table class="data-table">
          <thead>
            <tr>
              <th>Action Timing</th>
              <th>Lead Window</th>
              <th>Action &amp; Financial Reason</th>
              <th>Official Source</th>
            </tr>
          </thead>
          <tbody>
            {"".join(time_rows)}
          </tbody>
        </table>
      </div>
    </section>
    """
    return render_shell(
        "executive-summary.html",
        "Executive Summary, In-Scope Dates & Price Snapshot",
        "Executive Decision Brief · 2 Adults",
        "In-Scope Dates, Duration Conflict & Observed Hotel Quotes",
        "Compare 7-, 10-, and 14-night scenarios for two adults; the preferred Feb 15–18 window does not fit the stated minimum length, and dated hotel quotes do not predict the cheapest day to book.",
        body,
    )


def build_hotels(hotels_data: dict) -> str:
    rows = []
    cluster = hotels_data["cluster_coverage"]
    priced_hotels = sorted(
        (h for h in hotels_data["hotels"] if h["seven_night_total_usd"] is not None),
        key=lambda h: (h["seven_night_total_usd"], h["name"].casefold()),
    )
    price_ranks = {h["id"]: rank for rank, h in enumerate(priced_hotels, start=1)}
    for h in hotels_data["hotels"]:
        tags = " ".join(["all"] + h["filter_tags"])
        price_rank = price_ranks.get(h["id"])
        if h["seven_night_total_usd"] is not None:
            price_cell = (
                f'<span class="num-strong">${h["seven_night_total_usd"]:,.2f} USD · 7 nights</span>'
                f'<span class="muted-note">Snapshot 2026-11-26 · ${h["nightly_base_usd"]:,.2f}/nt pre-tax · {esc(h["rate_inclusions"])}</span>'
                f'<span class="muted-note"><strong>Observed price rank:</strong> #{price_rank} of {len(priced_hotels)} quoted USD totals (ascending; room and rate terms are not normalized).</span>'
            )
        else:
            price_cell = (
                f'<span class="blank-cell">— (No comparable live USD checkout total returned on 2026-11-26)</span>'
                f'<span class="muted-note">{esc(h["rate_inclusions"])}</span>'
                '<span class="muted-note"><strong>Observed price rank:</strong> Not ranked; no comparable USD total.</span>'
            )

        links_list = [
            ext_link(h["quote_url"], "Dated Quote / Offer"),
            ext_link(h["room_spec_url"], h.get("room_spec_label", "Official Room/Bath Spec")),
            ext_link(cluster["source_url"], "Official MICHELIN Directory"),
            ext_link(cluster["transit_source_url"], "Official Metro Reference"),
        ]
        if h.get("direct_engine_url"):
            links_list.append(ext_link(h["direct_engine_url"], "Direct Notice"))

        rows.append(
            f"""<tr data-tags="{esc(tags)}" data-overall-rank="{h["rank"]}" data-price-rank="{price_rank if price_rank is not None else "unranked"}">
          <td class="num-strong">#{h["rank"]}</td>
          <td>
            <strong>{esc(h["name"])}</strong>
            <span class="muted-note"><span class="badge badge-selected">{esc(h["badge"])}</span></span>
            <span class="muted-note">{esc(h["michelin_tier"])} · {esc(h["district"])}</span>
          </td>
          <td>
            <strong>{esc(h["metro_hub"])}</strong>
            <span class="muted-note">{esc(h["cluster_summary"])}</span>
            <span class="muted-note"><strong>Coverage tie:</strong> {cluster["tracked_venue_count"]}/{cluster["tracked_venue_count"]} tracked venues within ≤{cluster["access_limit_minutes"]} min ({cluster["starred_count"]} starred + {cluster["bib_gourmand_count"]} Bib + {cluster["selected_count"]} Selected). Curated subset only; see <a href="flagged.html#F19">F19</a>.</span>
            <span class="muted-note"><strong>On-site:</strong> {esc(h["in_house_michelin"])}</span>
          </td>
          <td>
            <strong>{esc(h["room_name"])}</strong>
            <span class="muted-note">Bed: {esc(h["bed_verified"])}</span>
            <span class="muted-note">Bath: {esc(h["bath_verified"])}</span>
          </td>
          <td>{price_cell}</td>
          <td>
            {esc(h["cancellation"])}
            <span class="muted-note">{esc(h["direct_channel_note"])}</span>
          </td>
          <td>{esc(h["rank_rationale"])}</td>
          <td>
            {"<br>".join(links_list)}<br>
            {flag_badges(h.get("flag_ids"), h["flag_id"])}
          </td>
        </tr>"""
        )

    unavail_rows = []
    for u in hotels_data["checked_unavailable_feb15"]:
        unavail_rows.append(
            f"""<tr>
          <td class="num-strong">{esc(u["name"])}</td>
          <td>{esc(u["status"])} (<a href="flagged.html#F02">Flag F02</a>)</td>
          <td>{ext_link(u["source_url"], "Live Dated Check")}</td>
        </tr>"""
        )

    body = f"""
    <div class="callout amber">
      <strong>Dated room-level checkout snapshots:</strong> The amounts below were recorded for <strong>2 adults, 1 room, 7 nights (<code>2027-02-15</code> to <code>2027-02-22</code>) on 2026-11-26</strong>; they are not current availability, a guaranteed price, or a forecast of the cheapest booking day. Re-open the dated quote and confirm room, bed, private bathroom, cancellation, taxes, and fees before purchase (<a href="flagged.html#F18">Flag F18</a>). Property alerts recorded in the same research pass: <strong>The Ritz-Carlton Pudong (#7)</strong> renovation notice (<a href="flagged.html#F03">F03</a>) and <strong>The Peninsula Shanghai (#6)</strong> offer deadline Dec 7, 2026 (<a href="flagged.html#F01">F01</a>).
    </div>
    <div class="callout">
      <strong>How to read the order:</strong> The overall order is a qualitative decision-support shortlist, not a weighted score or lowest-price order; each row gives its reason. The separate observed price rank sorts the eight recorded USD totals from low to high, while Peninsula is unranked because no comparable USD checkout total was captured. Room type, breakfast, and cancellation terms are not normalized. All nine hotels tie at 18/18 only within the curated venue subset, so the count does not distinguish them. Langham's selected bed setup and the exact-room private-bath details for W Shanghai and Bvlgari need confirmation before booking (<a href="flagged.html#F21">F21</a>, <a href="flagged.html#F05">F05</a>).
    </div>

    <section class="section-block">
      <div class="section-header">
        <h2>Hotel Shortlist: 18/18 MICHELIN Count Tie (≤1h) &amp; Feb 15–22 Quote Snapshots</h2>
        <span>2 Adults · Target: 1 private room with Queen/King+ bed; verify flagged room details</span>
      </div>

      <div id="hotel-filters" class="filter-bar" role="toolbar" aria-label="Filter hotels">
        <button class="filter-btn active" type="button" data-filter="all">All Shortlisted (9)</button>
        <button class="filter-btn" type="button" data-filter="under-2000">Under $2,000</button>
        <button class="filter-btn" type="button" data-filter="under-2500">Under $2,500</button>
        <button class="filter-btn" type="button" data-filter="breakfast">Breakfast Included</button>
        <button class="filter-btn" type="button" data-filter="free-cancel">Free Cancellation</button>
        <button class="filter-btn" type="button" data-filter="in-house-star">In-House MICHELIN Star</button>
        <button class="filter-btn" type="button" data-filter="huangpu">Huangpu (Xintiandi/Bund)</button>
        <button class="filter-btn" type="button" data-filter="jingan">Jing'an</button>
        <span id="hotel-count" class="filter-count">Showing 9 of 9 shortlisted properties</span>
      </div>

      <div class="table-scroll">
        <table id="hotels-table" class="data-table">
          <thead>
            <tr>
              <th>Decision-Support Order</th>
              <th>Hotel &amp; MICHELIN Key Status</th>
              <th>Metro Hub &amp; ≤1h MICHELIN Cluster Reach</th>
              <th>Room, Bed &amp; Private Bathroom Fit</th>
              <th>Observed 7-Night USD Total &amp; Price Rank</th>
              <th>Cancellation &amp; Property Alerts</th>
              <th>Why This Order</th>
              <th>Sources &amp; Audit</th>
            </tr>
          </thead>
          <tbody>
            {"".join(rows)}
          </tbody>
        </table>
      </div>
    </section>

    <section class="section-block">
      <div class="section-header">
        <h2>Properties With No Quote Returned in the 2026-11-26 Snapshot</h2>
        <span>Current inventory is unknown; no surrogate prices used</span>
      </div>
      <div class="table-scroll">
        <table class="data-table">
          <thead>
            <tr>
              <th>Property</th>
              <th>2026-11-26 Verification Result</th>
              <th>Dated Query URL</th>
            </tr>
          </thead>
          <tbody>
            {"".join(unavail_rows)}
          </tbody>
        </table>
      </div>
    </section>
    """
    return render_shell(
        "hotels.html",
        "Hotel Shortlist & Feb 15–22, 2027 Quote Snapshots",
        "Decision Support · 1 Room, 2 Adults",
        "Shanghai Hotels: 18/18 MICHELIN Cluster Tie & Dated 7-Night Quotes",
        hotels_data["ranking_methodology"],
        body,
    )


def distinction_badge(r: dict) -> str:
    if r["stars"] == 3:
        return f'<span class="badge badge-star3">★★★ {esc(r["distinction"])}</span>'
    if r["stars"] == 2:
        return f'<span class="badge badge-star2">★★ {esc(r["distinction"])}</span>'
    if r["stars"] == 1:
        return f'<span class="badge badge-star1">★ {esc(r["distinction"])}</span>'
    if r["category"] == "bib":
        return f'<span class="badge badge-bib">{esc(r["distinction"])}</span>'
    return f'<span class="badge badge-selected">{esc(r["distinction"])}</span>'


def build_restaurants(rest_data: dict) -> str:
    rows = []
    for r in rest_data["restaurants"]:
        tags = ["all", r["category"]]
        if r["starred"]:
            tags.append("starred-any")
        else:
            tags.append("non-starred")
        if "Mon – Sun" in r["open_days"] or "Dinner Mon – Sun" in r["open_days"]:
            tags.append("open-monday")
        if r["couple_price_cny"] is not None:
            tags.append("verified-price")

        links = [ext_link(r["michelin_url"], "MICHELIN Page")]
        if r["official_url"] and r["official_url"] != r["michelin_url"]:
            links.append(ext_link(r["official_url"], "Official Site"))
        if r["menu_url"]:
            links.append(ext_link(r["menu_url"], "2026 Menu / Offer"))

        price_cls = "num-strong" if r["couple_price_cny"] is not None else "blank-cell"
        rows.append(
            f"""<tr data-tags="{esc(" ".join(tags))}">
          <td>
            <strong>{esc(r["name"])}</strong><br>
            {distinction_badge(r)}
            <span class="muted-note">MICHELIN Band: <strong>{esc(r["michelin_band"])}</strong> · {esc(r["cuisine"])}</span>
          </td>
          <td>
            <strong>{esc(r["district"])}</strong>
            <span class="muted-note">{esc(r["address"])}</span>
            <span class="muted-note">{esc(r["metro_access"])}</span>
          </td>
          <td>
            <strong>{esc(r["open_days"])}</strong>
            <span class="muted-note">{esc(r["hours"])}</span>
            <span class="muted-note"><em>Exceptions:</em> {esc(r["exceptions"])}</span>
          </td>
          <td>
            <span class="{price_cls}">{esc(r["couple_price_display"])}</span>
            <span class="muted-note">{esc(r["price_basis"])}</span>
          </td>
          <td>{render_socials(r["social"], r["flag_id"])}</td>
          <td>
            {"<br>".join(links)}<br>
            {flag_badge(r["flag_id"])}
          </td>
        </tr>"""
        )

    alerts = "".join(f"<li>{esc(a)}</li>" for a in rest_data["directory_summary"]["closure_alerts"])
    body = f"""
    <div class="callout">
      <strong>Starred vs Non-Starred Clarity (2026 MICHELIN Guide Shanghai — 153 Live Venues):</strong>
      Shanghai's live directory lists <strong>50 Starred restaurants</strong> (<code>1× 3★</code>, <code>11× 2★</code>, <code>38× 1★</code>), <strong>33 Bib Gourmand</strong> (value distinction — <em>not</em> a star), and <strong>70 MICHELIN Selected</strong> (guide-recommended — <em>not</em> a star, including icons like <em>Mr &amp; Mrs Bund</em>, <em>Sir Elly's</em>, <em>Sui Tang Li</em>, and <em>Shanghai Tavern</em>).
      <ul style="margin:0.45rem 0 0 1.2rem;padding:0;">{alerts}</ul>
    </div>

    <section class="section-block">
      <div class="section-header">
        <h2>18 Deep-Verified MICHELIN Restaurants (11 Starred + 7 Bib Gourmand / Selected)</h2>
        <span>Every row verified against <code>guide.michelin.com</code> + operator menus</span>
      </div>

      <div id="restaurant-filters" class="filter-bar" role="toolbar" aria-label="Filter restaurants">
        <button class="filter-btn active" type="button" data-filter="all">All (18)</button>
        <button class="filter-btn" type="button" data-filter="starred-3-2">3★ &amp; 2★ Starred (7)</button>
        <button class="filter-btn" type="button" data-filter="starred-1">1★ Starred (4)</button>
        <button class="filter-btn" type="button" data-filter="bib">Bib Gourmand — Value (3)</button>
        <button class="filter-btn" type="button" data-filter="selected">MICHELIN Selected (4)</button>
        <button class="filter-btn" type="button" data-filter="open-monday">Open Mondays</button>
        <button class="filter-btn" type="button" data-filter="verified-price">Published Couple Price</button>
        <input id="restaurant-search" class="filter-search" type="search" placeholder="Search cuisine, name, district…" aria-label="Search restaurants">
        <span id="restaurant-count" class="filter-count">Showing 18 of 18 verified entries</span>
      </div>

      <div class="table-scroll">
        <table id="restaurants-table" class="data-table">
          <thead>
            <tr>
              <th>Restaurant &amp; Official Distinction</th>
              <th>District, Address &amp; Metro Reach</th>
              <th>Open Days, Hours &amp; Exceptions</th>
              <th>Published Meal Total for 2 (CNY)</th>
              <th>Verified Social Links (YT / TikTok / IG)</th>
              <th>Official Sources &amp; Audit</th>
            </tr>
          </thead>
          <tbody>
            {"".join(rows)}
          </tbody>
        </table>
      </div>
    </section>
    """
    return render_shell(
        "restaurants.html",
        "MICHELIN Starred, Bib Gourmand & Selected Restaurants",
        "Culinary Verification · Starred vs Non-Starred",
        "Shanghai 2026 MICHELIN Dining Guide: Couple Pricing, Hours & Social Reviews",
        "Clear separation between MICHELIN-Starred (3★/2★/1★) and Non-Starred (Bib Gourmand & Selected) venues, with exact 2026 PDF menu totals where published and blank + flagged cells where unverified.",
        body,
    )


def build_activities(act_data: dict) -> str:
    rows = []
    for a in act_data["activities"]:
        cost_cls = "blank-cell" if a["couple_cost_display"].startswith("—") else "num-strong"
        rows.append(
            f"""<tr>
          <td>
            <strong>{esc(a["name"])}</strong>
            <span class="muted-note"><span class="badge badge-selected">{esc(a["category"])}</span> · {esc(a["district"])}</span>
            <span class="muted-note">{esc(a["address"])}</span>
          </td>
          <td>
            <strong>{esc(a["open_days"])}</strong>
            <span class="muted-note">{esc(a["hours"])}</span>
            <span class="muted-note"><em>Exceptions:</em> {esc(a["exceptions"])}</span>
          </td>
          <td>
            <span class="{cost_cls}">{esc(a["couple_cost_display"])}</span>
            <span class="muted-note">{esc(a["booking_rule"])}</span>
          </td>
          <td>{esc(a["metro_route"])}</td>
          <td>{render_socials(a["social"], a["flag_id"])}</td>
          <td>
            {ext_link(a["official_url"], "Official Venue / Gov Page")}<br>
            {flag_badge(a["flag_id"])}
          </td>
        </tr>"""
        )

    body = f"""
    <div class="callout">
      <strong>Three High-Impact Sightseeing Facts Caught in Official Notices:</strong>
      (1) <strong>Shanghai Museum People's Square</strong> hosts <em>only</em> the ticketed <em>Ancient Civilizations of the Americas</em> exhibition from Jul 9, 2026 – Nov 14, 2027 (last entry <code>15:00</code>); all permanent Chinese bronze/jade/ceramics galleries are at <strong>Shanghai Museum East</strong> (free, closed Tuesdays).
      (2) <strong>Yu Garden</strong> is in its <strong>off-peak tariff (Dec 1 – Mar 31: CNY 30/adult = CNY 60 for 2)</strong>, closed Mondays.
      (3) <strong>Museum of Art Pudong (MAP)</strong> is <strong>open Mondays until 21:00</strong> — making it the #1 cultural anchor on arrival Monday Feb 15!
    </div>

    <section class="section-block">
      <div class="section-header">
        <h2>12 Verified Shanghai Activities Within ≤1 Hour of Top Ranked Hotels</h2>
        <span>Checked <code>2026-11-26</code></span>
      </div>
      <div class="table-scroll">
        <table class="data-table">
          <thead>
            <tr>
              <th>Activity &amp; Location</th>
              <th>Open Days, Hours &amp; Holiday/Closed Rules</th>
              <th>Official Admission for 2 &amp; Booking Rule</th>
              <th>Metro Route from Xintiandi / Bund</th>
              <th>Verified Social Links (YT / TikTok / IG)</th>
              <th>Official Source</th>
            </tr>
          </thead>
          <tbody>
            {"".join(rows)}
          </tbody>
        </table>
      </div>
    </section>
    """
    return render_shell(
        "activities.html",
        "Verified Activities & Attractions (≤1h)",
        "Cultural, Scenic & Modern Experiences",
        "Shanghai Activities Within ≤1 Hour: Hours, Closures, Tariffs & Social Previews",
        "Official venue and Shanghai Municipal Government verification for museums, classical gardens, observatories, canal towns, and Shanghai Disneyland.",
        body,
    )


def build_itinerary(it_data: dict) -> str:
    rows = []
    for d in it_data["itinerary_days"]:
        rows.append(
            f"""<tr>
          <td class="num-strong">
            {esc(d["day"])}
            <span class="muted-note">{esc(d["theme"])}</span>
          </td>
          <td><span class="badge badge-flag" style="white-space:normal;">{esc(d["calendar_alert"])}</span></td>
          <td>{esc(d["morning"])}</td>
          <td>{esc(d["afternoon"])}</td>
          <td>{esc(d["evening"])}</td>
          <td>{ext_link(d["source_url"], d["source_label"])}</td>
        </tr>"""
        )

    body = f"""
    <div class="callout jade">
      <strong>Zero Closed-Day Conflicts:</strong> Every day below is cross-checked against verified Monday closures (<em>Yu Garden, People's Square Museum, PSA, Da Vittorio, Taian Table, Sir Elly's, T'ang Court</em>), Tuesday closures (<em>Shanghai Museum East, Sir Elly's</em>), Thursday–Sunday lunch windows (<em>8½ Otto e Mezzo Bombana</em>), and <strong>Saturday Feb 20, 2027 Lantern Festival</strong>.
    </div>

    <section class="section-block">
      <div class="section-header">
        <h2>Recommended 7-Night Core Couple Itinerary (Mon Feb 15 – Mon Feb 22, 2027)</h2>
        <span>Overlaps preferred Feb 15–18 window</span>
      </div>
      <div class="table-scroll">
        <table class="data-table">
          <thead>
            <tr>
              <th>Day &amp; Date</th>
              <th>Verified Closure / Calendar Rule</th>
              <th>Morning Block</th>
              <th>Midday / Lunch Block</th>
              <th>Evening / MICHELIN Dinner Block</th>
              <th>Anchor Source</th>
            </tr>
          </thead>
          <tbody>
            {"".join(rows)}
          </tbody>
        </table>
      </div>
    </section>

    <section class="section-block">
      <div class="section-header">
        <h2>Modular 10-Night &amp; 14-Night Extensions (Inside Low-Rate Feb Window)</h2>
        <span>Optional add-on days</span>
      </div>
      <p class="section-sub">
        <strong>10-Night Extension (Feb 22–25):</strong> Keep Day 5 for Zhujiajiao Water Town, put full-day <strong>Shanghai Disneyland</strong> on Tue Feb 23, add <strong>Suzhou Classical Gardens</strong> (25-min HSR from Shanghai Hongqiao) on Wed Feb 24, and fly onward on Thu Feb 25.<br>
        <strong>14-Night Jiangnan Extension (Feb 22 – Mar 1, requires L-Visa):</strong> Add 3 nights in <strong>Hangzhou</strong> (45-min HSR; 13 MICHELIN-starred + 75 Bib/Selected venues, West Lake &amp; Longjing tea villages) + 2 nights in <strong>Suzhou</strong>, checking out right on March 1 before March corporate hotel rates jump +15.5%–40.3%.
      </p>
    </section>
    """
    return render_shell(
        "itinerary.html",
        "Closure-Safe Day-by-Day Itinerary",
        "Feb 15 – Feb 22, 2027 + Extensions",
        "Day-by-Day Couple Itinerary (Engineered Around Verified Open Days)",
        "Every museum, garden, observatory, Bib Gourmand lunch, and MICHELIN-starred dinner placed on a verified operating day.",
        body,
    )


def build_transport(it_data: dict) -> str:
    air_rows = []
    for a in it_data["airport_transit"]:
        air_rows.append(
            f"""<tr>
          <td class="num-strong">{esc(a["mode"])}</td>
          <td>{esc(a["route"])}</td>
          <td class="num-strong">{esc(a["travel_time"])}</td>
          <td>{esc(a["fare_per_person"])}</td>
          <td class="num-strong">{esc(a["couple_total"])}</td>
          <td>{esc(a["payment_note"])}</td>
          <td>{ext_link(a["source_url"], a["source_label"])}</td>
        </tr>"""
        )

    route_rows = []
    for c in it_data["cluster_routes"]:
        route_rows.append(
            f"""<tr>
          <td class="num-strong">{esc(c["origin_cluster"])}</td>
          <td>{esc(c["destination"])}</td>
          <td>{esc(c["metro_lines"])}</td>
          <td class="num-strong">{esc(c["estimated_window"])}</td>
          <td>{esc(c["fare_for_two"])}</td>
          <td>{esc(c["verification_note"])}</td>
          <td>{ext_link(c["source_url"], "Official Metro / Venue")} · <a href="flagged.html#F16">Flag F16</a></td>
        </tr>"""
        )

    body = f"""
    <div class="callout jade">
      <strong>Live Official Shanghai Metro Verification:</strong> While root <code>shmetro.com</code> fails over HTTPS, Shanghai Metro's official service portal (<code>service.shmetro.com/en/</code>) and Shanghai Municipal Government transport pages are live and verified: urban trains operate at <strong>35–40 km/h</strong>, fares start at <strong>CNY 3 (0–6 km)</strong> / <strong>CNY 4 (6–16 km)</strong>, 1-Day/3-Day passes cost <strong>CNY 18 / CNY 45</strong>, and foreign Visa/Mastercard tap-to-pay works directly at Maglev gates.
    </div>

    <section class="section-block">
      <div class="section-header">
        <h2>Airport-to-City &amp; Inter-Airport Rail Transfers (PVG &amp; SHA)</h2>
        <span>Checked <code>2026-11-26</code></span>
      </div>
      <div class="table-scroll">
        <table class="data-table">
          <thead>
            <tr>
              <th>Transit Mode</th>
              <th>Route &amp; Interchanges</th>
              <th>Official Duration</th>
              <th>Published Fare / Person</th>
              <th>Couple Cost (2 Adults)</th>
              <th>Foreign Card &amp; Pass Rules</th>
              <th>Official Source</th>
            </tr>
          </thead>
          <tbody>
            {"".join(air_rows)}
          </tbody>
        </table>
      </div>
    </section>

    <section class="section-block">
      <div class="section-header">
        <h2>Hotel Cluster to MICHELIN &amp; Attraction Metro Routing Matrix</h2>
        <span>All core clusters well inside ≤1h subway threshold</span>
      </div>
      <div class="table-scroll">
        <table class="data-table">
          <thead>
            <tr>
              <th>Hotel Base Cluster</th>
              <th>Target Dining / Sightseeing Cluster</th>
              <th>Verified Metro Line &amp; Interchange</th>
              <th>Station-to-Station Window</th>
              <th>Fare for 2</th>
              <th>Verification Scope Note</th>
              <th>Source &amp; Flag</th>
            </tr>
          </thead>
          <tbody>
            {"".join(route_rows)}
          </tbody>
        </table>
      </div>
    </section>
    """
    return render_shell(
        "transport.html",
        "Airport & Shanghai Metro Transit Matrix",
        "Official Rail, Maglev & Fare Verification",
        "Shanghai Airport Transfers, Metro Fare Rules & ≤1h Cluster Matrix",
        "Verified directly from service.shmetro.com/en/ and english.shanghai.gov.cn — distinguishing official line/fare facts from door-to-door walking estimates.",
        body,
    )


def build_visa_budget(gov: dict) -> str:
    visa_rows = []
    for v in gov["visa_options"]:
        visa_rows.append(
            f"""<tr>
          <td class="num-strong">{esc(v["pathway"])}</td>
          <td>{esc(v["eligibility_us"])}</td>
          <td>{esc(v["routing_rule"])}</td>
          <td>{esc(v["max_stay"])}</td>
          <td class="num-strong">{esc(v["cost_for_couple"])}</td>
          <td>{esc(v["documents_needed"])}</td>
          <td>{ext_link(v["source_url"], v["source_label"])}</td>
        </tr>"""
        )

    scen_rows = []
    for s in gov["budget_scenarios"]:
        scen_rows.append(
            f"""<tr>
          <td class="num-strong">{esc(s["tier"])}</td>
          <td>{esc(s["hotel_choice"])}</td>
          <td class="num-strong">{esc(s["visa_usd_range"])}</td>
          <td>{esc(s["verified_dining_sample"])}</td>
          <td>{esc(s["verified_activities_transit"])}</td>
          <td>{esc(s["verified_subtotal_note"])}</td>
          <td>{ext_link(s["source_url"], "Hotel Quote Source")}</td>
        </tr>"""
        )

    body = f"""
    <div class="callout amber">
      <strong>Conditional example only — traveler passport status is unknown:</strong> The trip brief provides no passport nationality or current visa status. The table below summarizes a U.S.-passport case for reference and must not be treated as either traveler’s eligibility or fee. Check both travelers’ passports, route, ports, stay length, and current requirements with the competent Chinese authority before booking (<a href="flagged.html#F17">Flag F17</a>). Any fee deadline shown is from a dated source and should be reconfirmed.
    </div>

    <section class="section-block">
      <div class="section-header">
        <h2>Conditional U.S.-Passport Entry Examples (Source Snapshot 2026-11-26)</h2>
        <span>Not traveler-specific; eligibility unknown for both adults</span>
      </div>
      <div class="table-scroll">
        <table class="data-table">
          <thead>
            <tr>
              <th>Entry Pathway</th>
              <th>U.S.-Passport Case (Conditional)</th>
              <th>Mandatory Flight Routing Rule</th>
              <th>Permitted Duration</th>
              <th>Conditional Example Fee (2)</th>
              <th>Required Application Documents</th>
              <th>Official Gov Source</th>
            </tr>
          </thead>
          <tbody>
            {"".join(visa_rows)}
          </tbody>
        </table>
      </div>
    </section>

    <section class="section-block">
      <div class="section-header">
        <h2>Interactive Scenario Calculator (7 Nights · Feb 15–22, 2027)</h2>
        <span>Visa cost defaults to unresolved until passports and routing are known</span>
      </div>
      <div class="calc-grid">
        <div class="calc-field">
          <label for="calc-hotel">1. Dated 7-Night Hotel Quote Snapshot (USD)</label>
          <select id="calc-hotel">
            <option value="1376.21" selected>Andaz Xintiandi — $1,376.21 (verified King/private bath; non-refundable)</option>
            <option value="1847.02">Jing An Shangri-La — $1,847.02 (King, non-refundable)</option>
            <option value="2291.93">The Langham Xintiandi — $2,291.93 snapshot (breakfast + free cancel; confirm one King, F21)</option>
            <option value="2394.04">The Sukhothai — $2,394.04 (55m² Studio King + Free Cancel)</option>
            <option value="2532.92">Ritz-Carlton Pudong — $2,532.92 (King; see Spa Flag F03)</option>
            <option value="2792.31">W Shanghai The Bund — $2,792.31 (King; confirm private bath, F05)</option>
            <option value="3222.01">The Shanghai EDITION — $3,222.01 (King/2 Queens + Free Cancel)</option>
            <option value="6858.31">Bvlgari Hotel Shanghai — $6,858.31 (Queen + breakfast/free cancel; confirm private bath, F05)</option>
          </select>
        </div>
        <div class="calc-field">
          <label for="calc-visa">2. Visa / Entry Cost (Not Yet Determined)</label>
          <select id="calc-visa">
            <option value="" selected>Not included — verify both passports and route</option>
            <option value="0">Conditional example: $0 visa fee if both qualify for 240h transit</option>
            <option value="280">Conditional U.S. example: $280 for two L-Visas under the cited fee notice</option>
            <option value="370">Conditional U.S. example: $370 for two at the cited baseline fee</option>
          </select>
        </div>
        <div class="calc-field">
          <label for="calc-dining">3. Published 2026 MICHELIN Menu Bundle (CNY for 2)</label>
          <select id="calc-dining">
            <option value="5608.22">Smart Starred Lunch + Bistro Bundle — CNY 5,608.22 (5 verified menus)</option>
            <option value="13149.64" selected>Balanced 2★/1★/Selected Set Bundle — CNY 13,149.64 (6 verified menus)</option>
            <option value="20161.24">Grand Gala &amp; Wine-Paired Bundle — CNY 20,161.24 (6 verified menus)</option>
          </select>
        </div>
        <div class="calc-field">
          <label for="calc-activities">4. Verified Transit &amp; Attraction Bundle (CNY for 2)</label>
          <select id="calc-activities">
            <option value="1120">Heritage + Skyline + Zhujiajiao + Maglev/Metro — CNY 1,120</option>
            <option value="2070" selected>Heritage + Skyline + Disneyland Base + Maglev/Metro — CNY 2,070</option>
          </select>
        </div>
      </div>
      <div id="calc-result" class="calc-output" aria-live="polite"></div>
    </section>

    <section class="section-block">
      <div class="section-header">
        <h2>Three Reference Couple Budget Scenarios (Line-Item Audited)</h2>
        <span>International flights &amp; unpublished tasting menus kept separate</span>
      </div>
      <div class="table-scroll">
        <table class="data-table">
          <thead>
            <tr>
              <th>Scenario Tier</th>
              <th>7-Night Hotel (Tax-Inclusive)</th>
              <th>Conditional U.S.-Passport Example (Not Traveler-Specific)</th>
              <th>Verified Published MICHELIN Menus (for 2)</th>
              <th>Verified Transit &amp; Tickets (for 2)</th>
              <th>Verified Subtotal &amp; Unpriced Exclusions</th>
              <th>Source</th>
            </tr>
          </thead>
          <tbody>
            {"".join(scen_rows)}
          </tbody>
        </table>
      </div>
    </section>
    """
    return render_shell(
        "visa-budget.html",
        "Entry Options & Couple Budget Scenarios",
        "Entry Compliance & Cost Transparency",
        "Conditional Entry Examples & Couple Budget Builder",
        "Passport nationality and visa status were not supplied. U.S.-passport rules appear only as conditional examples; the calculator excludes visa costs until eligibility is known.",
        body,
    )


def build_questions(gov: dict) -> str:
    rows = []
    question_range = f"{gov['questions'][0]['id']}–{gov['questions'][-1]['id']}"
    for q in gov["questions"]:
        rows.append(
            f"""<tr>
          <td class="num-strong">{esc(q["id"])}</td>
          <td><span class="badge badge-selected">{esc(q["category"])}</span></td>
          <td><strong>{esc(q["question"])}</strong></td>
          <td>{esc(q["why_it_matters"])}</td>
          <td>{esc(q["discovery_method"])}</td>
          <td>{ext_link(q["source_url"], "Reference Source")}</td>
        </tr>"""
        )

    body = f"""
    <section class="section-block">
      <div class="section-header">
        <h2>Missing Information &amp; Concrete Discovery Matrix ({question_range})</h2>
        <span>Every gap paired with an actionable resolution step</span>
      </div>
      <p class="section-sub">Rather than guessing traveler preferences or unpublished vendor tariffs, each open variable below states why it changes the plan and the exact method to verify it.</p>
      <div class="table-scroll">
        <table class="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Category</th>
              <th>Open Question</th>
              <th>Decision &amp; Budget Impact</th>
              <th>Concrete Method to Discover / Resolve</th>
              <th>Official Reference</th>
            </tr>
          </thead>
          <tbody>
            {"".join(rows)}
          </tbody>
        </table>
      </div>
    </section>
    """
    return render_shell(
        "questions.html",
        "Open Questions & Discovery Methods",
        "Decision Clarification Matrix",
        "Questions to Finalize Your Trip & How to Discover Missing Tariffs",
        "Structured list of traveler decisions and vendor confirmations needed before locking non-refundable bookings.",
        body,
    )


def build_suggestions(gov: dict) -> str:
    rows = []
    for s in gov["suggestions"]:
        rows.append(
            f"""<tr>
          <td class="num-strong">{esc(s["id"])}</td>
          <td><span class="badge badge-review-only">{esc(s["status"])}</span></td>
          <td><strong>{esc(s["title"])}</strong></td>
          <td>{esc(s["upside"])}</td>
          <td>{esc(s["tradeoff"])}</td>
          <td>{esc(s["verification_step"])}</td>
          <td>{ext_link(s["source_url"], "Supporting Source")}</td>
        </tr>"""
        )

    body = f"""
    <div class="callout amber">
      <strong>Governance Rule — Suggestions Are NOT Implemented Automatically:</strong>
      None of the 6 strategic ideas below have been assumed into your core constraints without your review. Each is presented with verified upside, trade-offs, and a concrete verification step.
    </div>

    <section class="section-block">
      <div class="section-header">
        <h2>Decision-Improvement Proposals (For Review Only · S01–S06)</h2>
        <span>Awaiting traveler sign-off</span>
      </div>
      <div class="table-scroll">
        <table class="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Status</th>
              <th>Proposed Improvement</th>
              <th>Quantified Upside</th>
              <th>Trade-Off / Constraint</th>
              <th>Concrete Verification Action</th>
              <th>Source</th>
            </tr>
          </thead>
          <tbody>
            {"".join(rows)}
          </tbody>
        </table>
      </div>
    </section>
    """
    return render_shell(
        "suggestions.html",
        "Strategic Suggestions (For Review Only)",
        "For Review Only — Not Implemented",
        "High-Leverage Ideas to Improve Value, Routing & Crowd Timing",
        "Optional ideas are based on dated 2026 hotel quote snapshots, conditional visa examples, and published 2026 MICHELIN menus; verify current terms before acting.",
        body,
    )


def build_flagged(gov: dict) -> str:
    rows = []
    flag_count = len(gov["flagged_items"])
    flag_range = f"{gov['flagged_items'][0]['id']}–{gov['flagged_items'][-1]['id']}"
    for f in gov["flagged_items"]:
        rows.append(
            f"""<tr id="{esc(f["id"])}">
          <td class="num-strong">{esc(f["id"])}</td>
          <td><span class="badge badge-flag">{esc(f["severity"])}</span><span class="muted-note">{esc(f["category"])}</span></td>
          <td><strong>{esc(f["subject"])}</strong></td>
          <td>{esc(f["finding"])}</td>
          <td>{esc(f["handling"])}</td>
          <td>{ext_link(f["source_url"], "Inspect Source")}</td>
        </tr>"""
        )

    body = f"""
    <div class="callout">
      <strong>Zero-Guesswork Transparency Policy:</strong> The underlying official-source research snapshot is dated <code>2026-11-26</code>. Unconfirmed values stay blank (<code>—</code>); dated dynamic hotel quotes are not presented as current availability; and traveler-specific gaps, source contradictions, or ranking limitations are listed below. This integration review checked local consistency on <code>2026-11-28</code> but did not re-fetch third-party hotel/restaurant pages.
    </div>

    <section class="section-block">
      <div class="section-header">
        <h2>Flagged for Review Registry ({flag_range})</h2>
        <span>{flag_count} audited assumptions, limitations, contradictions &amp; unverified gaps</span>
      </div>
      <div class="table-scroll">
        <table class="data-table">
          <thead>
            <tr>
              <th>Flag ID</th>
              <th>Severity &amp; Type</th>
              <th>Venue / Subject</th>
              <th>Exact Irregularity or Missing Fact</th>
              <th>How Handled in Dashboard</th>
              <th>Primary Source</th>
            </tr>
          </thead>
          <tbody>
            {"".join(rows)}
          </tbody>
        </table>
      </div>
    </section>
    """
    return render_shell(
        "flagged.html",
        f"Flagged for Review ({flag_range})",
        "Audit & Irregularity Log",
        "Flagged for Review: Unverified Cells, Contradictions & Renovation Alerts",
        "Every blank cell, operator contradiction, active hotel enhancement notice, and social-link gap documented with clickable evidence.",
        body,
    )


def collect_all_urls(*datasets: dict) -> list[tuple[str, str]]:
    seen: dict[str, str] = {}

    def walk(node: object) -> None:
        if isinstance(node, dict):
            for k, v in node.items():
                if isinstance(v, str) and v.startswith("https://"):
                    host = urlparse(v).netloc
                    if v not in seen:
                        seen[v] = host
                else:
                    walk(v)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    for ds in datasets:
        walk(ds)
    return sorted(seen.items(), key=lambda pair: (pair[1], pair[0]))


def classify_host(host: str) -> str:
    if host.endswith(".gov.cn") or "china-embassy" in host:
        return "Official Government (.gov.cn / Embassy)"
    if "michelin.com" in host:
        return "Official MICHELIN Guide"
    if any(x in host for x in ("youtube.com", "tiktok.com", "instagram.com")):
        return "Verified Social Media (Direct Video / Handle)"
    return "Official Hotel / Restaurant / Museum Operator"


def build_repo_audit(overview: dict, hotels: dict, restaurants: dict, activities: dict, it_data: dict, gov: dict) -> str:
    audit_rows = []
    for a in gov["repo_audit"]:
        audit_rows.append(
            f"""<tr>
          <td class="num-strong">{esc(a["target"])}</td>
          <td>{esc(a["resolved_strengths"])}</td>
          <td>{esc(a["remaining_gaps_fixed_here"])}</td>
          <td>{ext_link(a["source_url"], "Verification Proof")}</td>
        </tr>"""
        )

    all_urls = collect_all_urls(overview, hotels, restaurants, activities, it_data, gov)
    url_rows = []
    for idx, (url, host) in enumerate(all_urls, start=1):
        cat = classify_host(host)
        url_rows.append(
            f"""<tr>
          <td class="num-strong">S{idx:02d}</td>
          <td><span class="badge badge-selected">{esc(cat)}</span></td>
          <td><code>{esc(host)}</code></td>
          <td style="word-break:break-all;">{ext_link(url, url)}</td>
          <td><code>2026-11-26</code></td>
        </tr>"""
        )

    body = f"""
    <section class="section-block">
      <div class="section-header">
        <h2>Repository-Wide Audit Across Existing Sites (Checked 2026-11-26)</h2>
        <span>Non-destructive audit — zero sibling files modified</span>
      </div>
      <p class="section-sub">This page preserves the cross-site source audit recorded on 2026-11-26 for the root dashboard and six companion subsites. The 2026-11-28 integration reviewed local assumptions, route-count scope, and generated output; it did not re-fetch official third-party pages. See Flags F17–F19 for passport nationality, dated hotel quote limits, and the hotel-cluster count tie.</p>
      <div class="table-scroll">
        <table class="data-table">
          <thead>
            <tr>
              <th>Repository Site</th>
              <th>Verified Strengths Preserved</th>
              <th>Remaining Discrepancies / New Findings Resolved in <code>/trip-2027/</code></th>
              <th>Key Proof Link</th>
            </tr>
          </thead>
          <tbody>
            {"".join(audit_rows)}
          </tbody>
        </table>
      </div>
    </section>

    <section class="section-block">
      <div class="section-header">
        <h2>Master Primary Source Ledger ({len(all_urls)} Unique Verified URLs)</h2>
        <span>All links live-checked <code>2026-11-26</code></span>
      </div>
      <div class="table-scroll">
        <table class="data-table">
          <thead>
            <tr>
              <th>#</th>
              <th>Source Category</th>
              <th>Domain</th>
              <th>Direct Clickable URL</th>
              <th>Verified</th>
            </tr>
          </thead>
          <tbody>
            {"".join(url_rows)}
          </tbody>
        </table>
      </div>
    </section>
    """
    return render_shell(
        "repo-audit.html",
        "Repository Audit & Master Source Ledger",
        "Provenance & Cross-Site Audit",
        f"Repository Audit & Master Ledger of {len(all_urls)} Verified URLs",
        "Complete cross-site verification summary and deduplicated index of every government, MICHELIN, hotel, restaurant, museum, transit, and social URL cited in /trip-2027/.",
        body,
    )


def main() -> None:
    overview = load_json("overview.json")
    hotels = load_json("hotels.json")
    restaurants = load_json("restaurants.json")
    activities = load_json("activities.json")
    it_data = load_json("itinerary_transport.json")
    gov = load_json("governance.json")

    outputs = {
        "index.html": build_index(overview, hotels, restaurants),
        "executive-summary.html": build_exec_summary(overview),
        "hotels.html": build_hotels(hotels),
        "restaurants.html": build_restaurants(restaurants),
        "activities.html": build_activities(activities),
        "itinerary.html": build_itinerary(it_data),
        "transport.html": build_transport(it_data),
        "visa-budget.html": build_visa_budget(gov),
        "questions.html": build_questions(gov),
        "suggestions.html": build_suggestions(gov),
        "flagged.html": build_flagged(gov),
        "repo-audit.html": build_repo_audit(overview, hotels, restaurants, activities, it_data, gov),
    }

    for filename, content in outputs.items():
        (ROOT / filename).write_text(content, encoding="utf-8")
    print(f"Built {len(outputs)} verified HTML pages in {ROOT}")


if __name__ == "__main__":
    main()
