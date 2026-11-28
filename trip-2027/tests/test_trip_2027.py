#!/usr/bin/env python3
"""Strict automated verification suite for /trip-2027/ static couple trip dashboard."""

from __future__ import annotations

import datetime
import json
import re
import subprocess
import sys
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

TRIP_ROOT = Path(__file__).resolve().parent.parent
REPO_ROOT = TRIP_ROOT.parent
DATA_DIR = TRIP_ROOT / "data"

EXPECTED_PAGES = [
    "index.html",
    "executive-summary.html",
    "hotels.html",
    "restaurants.html",
    "activities.html",
    "itinerary.html",
    "transport.html",
    "visa-budget.html",
    "questions.html",
    "suggestions.html",
    "flagged.html",
    "repo-audit.html",
]


class PageAuditParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.has_viewport = False
        self.ids: set[str] = set()
        self.links: list[str] = []
        self.assets: list[str] = []
        self.in_table_scroll = 0
        self.tables_outside_scroll = 0
        self.in_tbody = False
        self.in_tr = False
        self.current_tr_links: list[str] = []
        self.tbody_rows_links: list[list[str]] = []
        self.tag_stack: list[tuple[str, bool]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = dict(attrs)
        if tag == "meta" and attr_map.get("name") == "viewport":
            if "width=device-width" in (attr_map.get("content") or ""):
                self.has_viewport = True

        if attr_map.get("id"):
            self.ids.add(attr_map["id"] or "")

        is_scroll_div = tag == "div" and "table-scroll" in (attr_map.get("class") or "").split()
        if is_scroll_div:
            self.in_table_scroll += 1
        self.tag_stack.append((tag, is_scroll_div))

        if tag == "table" and self.in_table_scroll == 0:
            self.tables_outside_scroll += 1

        if tag == "tbody":
            self.in_tbody = True
        elif tag == "tr" and self.in_tbody:
            self.in_tr = True
            self.current_tr_links = []
        elif tag == "a" and attr_map.get("href"):
            href = attr_map["href"] or ""
            self.links.append(href)
            if self.in_tr:
                self.current_tr_links.append(href)
        elif tag in ("link", "script") and (attr_map.get("href") or attr_map.get("src")):
            ref = attr_map.get("href") or attr_map.get("src") or ""
            self.assets.append(ref)

    def handle_endtag(self, tag: str) -> None:
        if tag == "tr" and self.in_tr:
            self.in_tr = False
            self.tbody_rows_links.append(self.current_tr_links)
        elif tag == "tbody":
            self.in_tbody = False

        while self.tag_stack:
            popped_tag, was_scroll = self.tag_stack.pop()
            if was_scroll:
                self.in_table_scroll -= 1
            if popped_tag == tag:
                break


class Trip2027VerificationTests(unittest.TestCase):
    def test_01_build_is_deterministic_and_complete(self) -> None:
        before = {
            p: (TRIP_ROOT / p).read_text(encoding="utf-8")
            for p in EXPECTED_PAGES
            if (TRIP_ROOT / p).exists()
        }
        res = subprocess.run(
            [sys.executable, str(TRIP_ROOT / "scripts" / "build.py")],
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertIn("Built 12 verified HTML pages", res.stdout)
        for page in EXPECTED_PAGES:
            path = TRIP_ROOT / page
            self.assertTrue(path.is_file(), f"Missing generated page {page}")
            if page in before:
                self.assertEqual(before[page], path.read_text(encoding="utf-8"))

    def test_02_all_tables_mobile_wrapped_and_every_row_has_source_or_flag(self) -> None:
        parsed_pages: dict[str, PageAuditParser] = {}
        for page in EXPECTED_PAGES:
            parser = PageAuditParser()
            parser.feed((TRIP_ROOT / page).read_text(encoding="utf-8"))
            parsed_pages[page] = parser
            self.assertTrue(parser.has_viewport, f"{page} missing responsive viewport meta")
            self.assertEqual(
                parser.tables_outside_scroll,
                0,
                f"{page} has table outside .table-scroll mobile container",
            )
            self.assertGreater(len(parser.tbody_rows_links), 0, f"{page} has zero data rows")
            for idx, row_links in enumerate(parser.tbody_rows_links, start=1):
                has_proof = any(
                    lnk.startswith("https://") or lnk.startswith("flagged.html#F")
                    for lnk in row_links
                )
                self.assertTrue(
                    has_proof,
                    f"{page} tbody row #{idx} lacks https:// source or flagged.html#F anchor: {row_links}",
                )

        # Verify all internal links, assets, and #Fxx anchors resolve
        for page, parser in parsed_pages.items():
            for asset in parser.assets:
                if not asset.startswith(("http://", "https://")):
                    self.assertTrue((TRIP_ROOT / asset).is_file(), f"{page} missing asset {asset}")
            for href in parser.links:
                if href.startswith(("https://", "mailto:", "tel:")):
                    continue
                self.assertFalse(href.startswith("http://"), f"Insecure http:// link in {page}: {href}")
                path_part, _, frag = href.partition("#")
                target_file = (TRIP_ROOT / path_part).resolve() if path_part else (TRIP_ROOT / page).resolve()
                self.assertTrue(target_file.is_file(), f"{page} broken internal link {href} -> {target_file}")
                if frag and target_file.parent == TRIP_ROOT:
                    target_parser = parsed_pages[target_file.name]
                    self.assertIn(
                        frag,
                        target_parser.ids,
                        f"{page} broken fragment #{frag} in {target_file.name}",
                    )

    def test_03_social_links_are_direct_and_never_search_or_bare_homepages(self) -> None:
        restaurants = json.loads((DATA_DIR / "restaurants.json").read_text(encoding="utf-8"))["restaurants"]
        activities = json.loads((DATA_DIR / "activities.json").read_text(encoding="utf-8"))["activities"]
        governance = json.loads((DATA_DIR / "governance.json").read_text(encoding="utf-8"))
        flag_ids = {flag["id"] for flag in governance["flagged_items"]}

        # Verify both starred and non-starred (Bib Gourmand + Selected) restaurants are represented
        starred = [r for r in restaurants if r["starred"]]
        bib = [r for r in restaurants if r["category"] == "bib" and not r["starred"]]
        selected = [r for r in restaurants if r["category"] == "selected" and not r["starred"]]
        self.assertGreaterEqual(len(starred), 10)
        self.assertGreaterEqual(len(bib), 3)
        self.assertGreaterEqual(len(selected), 4)

        forbidden_substrings = ("/results?", "search_query=", "/search?", "google.com/search")
        for record in restaurants + activities:
            missing_any_social = False
            for platform in ("youtube", "tiktok", "instagram"):
                entry = record["social"].get(platform)
                if entry is None:
                    missing_any_social = True
                    continue
                url = entry["url"]
                parsed = urlparse(url)
                self.assertEqual(parsed.scheme, "https")
                for bad in forbidden_substrings:
                    self.assertNotIn(bad, url, f"Search placeholder social URL forbidden: {url}")
                self.assertNotIn(
                    parsed.path,
                    ("", "/"),
                    f"Bare social homepage URL forbidden for {record['name']}: {url}",
                )
            if missing_any_social:
                self.assertTrue(
                    record.get("flag_id"),
                    f"{record['name']} has a missing social platform without a review flag",
                )
                self.assertIn(record["flag_id"], flag_ids, f"{record['name']} references an unknown flag")

    def test_04_couple_menu_and_hotel_arithmetic_integrity(self) -> None:
        # Verify published couple menu calculations match exact 2026 PDF formulas
        self.assertAlmostEqual(298 * 2 * 1.166, 694.936, places=3)
        self.assertAlmostEqual(338 * 2 * 1.166, 788.216, places=3)
        self.assertAlmostEqual(988 * 2 * 1.166, 2304.016, places=3)
        self.assertAlmostEqual(1288 * 2 * 1.166, 3003.616, places=3)
        self.assertAlmostEqual(1788 * 2, 3576, places=2)
        self.assertAlmostEqual(300 * 2 * 1.10, 660.0, places=2)
        self.assertAlmostEqual(450 * 2 * 1.10, 990.0, places=2)
        self.assertAlmostEqual(1288 * 2 * 1.10, 2833.60, places=2)

        # Verify Scenario 1 & Scenario 2 dining bundle sums in governance.json
        scen1_sum = 888 + 788.22 + 660 + 988 + 2284
        self.assertAlmostEqual(scen1_sum, 5608.22, places=2)
        scen2_sum = 2288 + 3576 + 2304.02 + 3003.62 + 990 + 988
        self.assertAlmostEqual(scen2_sum, 13149.64, places=2)

        hotels = json.loads((DATA_DIR / "hotels.json").read_text(encoding="utf-8"))["hotels"]
        self.assertEqual(len(hotels), 9)
        priced = [h for h in hotels if h["seven_night_total_usd"] is not None]
        self.assertEqual(len(priced), 8)
        for h in priced:
            # Tax-inclusive 7-night total must exceed 7 * pre-tax nightly base
            self.assertGreater(h["seven_night_total_usd"], h["nightly_base_usd"] * 7)

    def test_05_itinerary_respects_monday_and_tuesday_closures(self) -> None:
        days = json.loads((DATA_DIR / "itinerary_transport.json").read_text(encoding="utf-8"))["itinerary_days"]
        day1_mon = days[0]
        day2_tue = days[1]
        mon_plan = " ".join([day1_mon["morning"], day1_mon["afternoon"], day1_mon["evening"]])
        tue_plan = " ".join([day2_tue["morning"], day2_tue["afternoon"], day2_tue["evening"]])

        # Monday-closed venues must not appear in Day 1 active blocks
        for closed_mon in ("Da Vittorio", "Taian Table", "Sir Elly", "Power Station of Art", "People's Square"):
            self.assertNotIn(closed_mon, mon_plan)

        # Tuesday-closed venues must not appear in Day 2 active blocks
        for closed_tue in ("Shanghai Museum East", "Sir Elly"):
            self.assertNotIn(closed_tue, tue_plan)

        # Check no retired/hallucinated venues appear as active recommendations
        restaurants_raw = (TRIP_ROOT / "restaurants.html").read_text(encoding="utf-8")
        self.assertIn("Ultraviolet by Paul Pairet (formerly 3★) closed permanently on March 29, 2025", restaurants_raw)
        self.assertIn("102 House (awarded 2★ at the April 2026 ceremony) closed permanently on July 8, 2026", restaurants_raw)

    def test_06_user_constraints_are_explicit_and_no_passport_is_assumed(self) -> None:
        overview = json.loads((DATA_DIR / "overview.json").read_text(encoding="utf-8"))
        governance = json.loads((DATA_DIR / "governance.json").read_text(encoding="utf-8"))
        constraints = overview["intake_constraints"]
        self.assertEqual((constraints["traveler_count"], constraints["trip_min_nights"], constraints["trip_max_nights"]), (2, 7, 14))
        self.assertEqual((constraints["travel_window_start"], constraints["travel_window_end"]), ("2027-02-15", "2027-03-23"))
        self.assertEqual((constraints["preferred_window_start"], constraints["preferred_window_end"]), ("2027-02-15", "2027-02-18"))
        preferred_start = datetime.date.fromisoformat(constraints["preferred_window_start"])
        preferred_end = datetime.date.fromisoformat(constraints["preferred_window_end"])
        self.assertEqual((preferred_end - preferred_start).days, 3)
        self.assertEqual((datetime.date(2027, 2, 19) - preferred_start).days, 4)
        self.assertLess(4, constraints["trip_min_nights"])
        for option in overview["duration_options"]:
            start = datetime.date.fromisoformat(option["check_in"])
            end = datetime.date.fromisoformat(option["check_out"])
            nights = (end - start).days
            self.assertGreaterEqual(nights, 7)
            self.assertLessEqual(nights, 14)
            self.assertGreaterEqual(start.isoformat(), constraints["travel_window_start"])
            self.assertLessEqual(end.isoformat(), constraints["travel_window_end"])
        self.assertEqual(len(overview["duration_options"]), 3)
        self.assertEqual(len(governance["questions"]), 11)
        self.assertTrue(any(q["id"] == "Q11" and "3 hotel nights" in q["question"] and "4 nights" in q["question"] for q in governance["questions"]))

        index = (TRIP_ROOT / "index.html").read_text(encoding="utf-8")
        summary = (TRIP_ROOT / "executive-summary.html").read_text(encoding="utf-8")
        questions = (TRIP_ROOT / "questions.html").read_text(encoding="utf-8")
        visa_page = (TRIP_ROOT / "visa-budget.html").read_text(encoding="utf-8")
        activities_page = (TRIP_ROOT / "activities.html").read_text(encoding="utf-8")
        itinerary_page = (TRIP_ROOT / "itinerary.html").read_text(encoding="utf-8")
        self.assertIn("does not fit inside", index)
        self.assertNotIn("21–28 Nights", summary)
        self.assertIn("Q01–Q11", questions)
        self.assertIn("Passport nationality unknown", index)
        self.assertIn("flagged.html#F17", index)
        self.assertIn('id="calc-visa"', visa_page)
        self.assertIn('<option value="" selected>', visa_page)
        self.assertIn('<option value="1376.21" selected>Andaz Xintiandi', visa_page)
        self.assertIn("confirm one King, F21", visa_page)
        self.assertIn("conditional u.s.-passport entry examples", visa_page.lower())
        self.assertIn("each traveler’s passport", activities_page)
        self.assertIn("each traveler’s passport", itinerary_page)
        self.assertNotIn("US passports", activities_page)
        self.assertNotIn("direct US return", itinerary_page)
        self.assertNotIn("Checked <code>2026-11-26</code> for two US passport holders", index)

    def test_07_hotel_cluster_tie_and_dated_price_limits_are_visible(self) -> None:
        hotels_data = json.loads((DATA_DIR / "hotels.json").read_text(encoding="utf-8"))
        overview = json.loads((DATA_DIR / "overview.json").read_text(encoding="utf-8"))
        restaurants = json.loads((DATA_DIR / "restaurants.json").read_text(encoding="utf-8"))["restaurants"]
        coverage = hotels_data["cluster_coverage"]
        self.assertEqual(coverage["tracked_venue_count"], len(restaurants))
        self.assertEqual(coverage["starred_count"], sum(1 for r in restaurants if r["starred"]))
        self.assertEqual(coverage["bib_gourmand_count"], sum(1 for r in restaurants if r["category"] == "bib"))
        self.assertEqual(coverage["selected_count"], sum(1 for r in restaurants if r["category"] == "selected"))
        self.assertEqual(coverage["tracked_venue_count"], coverage["starred_count"] + coverage["bib_gourmand_count"] + coverage["selected_count"])
        self.assertTrue(all("18/18 deep-verified venues" in h["cluster_summary"] for h in hotels_data["hotels"]))
        self.assertIn("raw count does not distinguish", hotels_data["ranking_methodology"])
        self.assertIn("not a weighted score or price sort", hotels_data["ranking_methodology"])
        self.assertIn("cheapest future booking date", hotels_data["rate_snapshot_note"])
        self.assertTrue(all("comparison_note" in row for row in overview["rate_curve_windows"]))
        self.assertTrue(all("cheapest_window" not in row for row in overview["rate_curve_windows"]))
        self.assertIn("booking-time forecast", overview["duration_options"][0]["pricing_verdict"])

        hotels = hotels_data["hotels"]
        self.assertEqual(sorted(h["rank"] for h in hotels), list(range(1, len(hotels) + 1)))
        self.assertTrue(all(h.get("rank_rationale") for h in hotels), "Every overall-order position needs an explanation")
        priced = sorted(
            (h for h in hotels if h["seven_night_total_usd"] is not None),
            key=lambda h: (h["seven_night_total_usd"], h["name"].casefold()),
        )
        self.assertEqual(len(priced), 8)
        expected_price_ranks = {h["rank"]: str(i) for i, h in enumerate(priced, start=1)}
        for h in hotels:
            if h["seven_night_total_usd"] is None:
                expected_price_ranks[h["rank"]] = "unranked"
        hotels_html = (TRIP_ROOT / "hotels.html").read_text(encoding="utf-8")
        rendered_rank_pairs = re.findall(
            r'data-overall-rank="(\d+)" data-price-rank="(\d+|unranked)"', hotels_html
        )
        self.assertEqual(len(rendered_rank_pairs), len(hotels))
        self.assertEqual(
            {int(overall): price for overall, price in rendered_rank_pairs},
            expected_price_ranks,
        )

        exec_html = (TRIP_ROOT / "executive-summary.html").read_text(encoding="utf-8")
        index_html = (TRIP_ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn("Coverage tie:", hotels_html)
        self.assertIn("Observed price rank:", hotels_html)
        self.assertIn("Official MICHELIN Directory", hotels_html)
        self.assertIn("Official Metro Reference", hotels_html)
        self.assertIn("not a booking forecast", exec_html.lower())
        self.assertNotIn("Lowest Observed Stay Window", exec_html)
        self.assertNotIn("Lowest Observed 7-Night Stay-Date Sample", index_html)
        self.assertNotIn("When to Book for Best Prices", exec_html)

    def test_08_every_primary_record_has_an_https_source_and_new_flags_resolve(self) -> None:
        overview = json.loads((DATA_DIR / "overview.json").read_text(encoding="utf-8"))
        governance = json.loads((DATA_DIR / "governance.json").read_text(encoding="utf-8"))
        itinerary = json.loads((DATA_DIR / "itinerary_transport.json").read_text(encoding="utf-8"))
        hotels = json.loads((DATA_DIR / "hotels.json").read_text(encoding="utf-8"))
        restaurants = json.loads((DATA_DIR / "restaurants.json").read_text(encoding="utf-8"))["restaurants"]
        activities = json.loads((DATA_DIR / "activities.json").read_text(encoding="utf-8"))["activities"]

        rows = []
        for dataset, keys in (
            (overview, ("hero_kpis", "city_comparison", "duration_options", "rate_curve_windows", "action_timeline")),
            (governance, ("visa_options", "budget_scenarios", "questions", "suggestions", "flagged_items", "repo_audit")),
            (itinerary, ("itinerary_days", "airport_transit", "cluster_routes")),
        ):
            for key in keys:
                rows.extend(dataset[key])
        official_source_roots = (
            "brilliantbylangham.com", "bulgarihotels.com", "capellahotels.com", "china-embassy.gov.cn",
            "davittorio.com", "gov.cn", "guide.michelin.com", "jinxuanchineserestaurantshanghai.com",
            "langhamhotels.com", "marriott.com", "michelin.com", "mmbund.com", "nia.gov.cn",
            "peninsula.com", "poluxbypp.com", "powerstationofart.com", "shanghai.gov.cn", "shanghaidisneyresort.com",
            "shanghaimuseum.net", "shmetro.com", "taian-table.cn", "upperhouse.com", "yugarden.com.cn",
        )
        for row in rows:
            self.assertTrue(row.get("source_url"), f"Missing source URL in row: {row}")
            parsed_source = urlparse(row["source_url"])
            self.assertEqual(parsed_source.scheme, "https", row["source_url"])
            self.assertTrue(
                any(parsed_source.hostname == root or parsed_source.hostname.endswith("." + root) for root in official_source_roots),
                f"Primary source row points outside the official-source domain allowlist: {row['source_url']}",
            )

        for record in restaurants:
            for field in ("official_url", "michelin_url"):
                self.assertTrue(record.get(field), f"{record['name']} missing {field}")
                self.assertEqual(urlparse(record[field]).scheme, "https")
        for record in activities:
            self.assertTrue(record.get("official_url"), f"{record['name']} missing official_url")
            self.assertEqual(urlparse(record["official_url"]).scheme, "https")
        for record in restaurants + activities:
            for field in ("open_days", "hours", "exceptions"):
                value = record.get(field)
                self.assertTrue(value and value.strip(), f"{record['name']} missing {field}")
                if value.strip().startswith("—"):
                    self.assertTrue(record.get("flag_id"), f"Unverified {field} in {record['name']} lacks a review flag")
        for hotel in hotels["hotels"]:
            for field in ("quote_url", "room_spec_url"):
                self.assertTrue(hotel.get(field), f"{hotel['name']} missing {field}")
                self.assertEqual(urlparse(hotel[field]).scheme, "https")
            if hotel["room_spec_url"] == hotel["quote_url"]:
                self.assertIn("MICHELIN", hotel.get("room_spec_label", ""), f"{hotel['name']} must not label a MICHELIN listing as an official room spec")
            if hotel["id"] in {"w-shanghai-bund", "bvlgari-shanghai"}:
                self.assertTrue(hotel["bath_verified"].startswith("—"), f"Unconfirmed exact-room bath must remain blank for {hotel['name']}")
                self.assertEqual(hotel.get("flag_id"), "F05")
            if hotel["id"] == "langham-xintiandi":
                self.assertIn("2 single beds", hotel["bed_verified"])
                self.assertEqual(hotel.get("flag_id"), "F04")
            if hotel["seven_night_total_usd"] is None:
                self.assertTrue(hotel.get("flag_id"), f"Unpriced hotel lacks a review flag: {hotel['name']}")
        for restaurant in restaurants:
            if restaurant["couple_price_cny"] is None:
                self.assertTrue(restaurant.get("flag_id"), f"Unpriced restaurant lacks a review flag: {restaurant['name']}")
        for activity in activities:
            if activity["couple_cost_display"].startswith("—"):
                self.assertTrue(activity.get("flag_id"), f"Unpriced activity lacks a review flag: {activity['name']}")

        flags = json.loads((DATA_DIR / "governance.json").read_text(encoding="utf-8"))["flagged_items"]
        flag_ids = {f["id"] for f in flags}
        flags_by_id = {f["id"]: f for f in flags}
        self.assertTrue({"F17", "F18", "F19", "F20", "F21"}.issubset(flag_ids))
        self.assertEqual(flags_by_id["F05"]["severity"], "High")
        self.assertEqual(flags_by_id["F21"]["severity"], "High")
        for record in hotels["hotels"] + restaurants + activities:
            record_flag_ids = set(record.get("flag_ids", []))
            if record.get("flag_id"):
                record_flag_ids.add(record["flag_id"])
            for record_flag_id in record_flag_ids:
                self.assertIn(record_flag_id, flag_ids, f"{record.get('name')} references an unknown flag")
        self.assertEqual(next(h for h in hotels["hotels"] if h["id"] == "peninsula-shanghai")["seven_night_total_usd"], None)
        flagged_html = (TRIP_ROOT / "flagged.html").read_text(encoding="utf-8")
        for flag_id in ("F17", "F18", "F19", "F20", "F21"):
            self.assertIn(f'id="{flag_id}"', flagged_html)


if __name__ == "__main__":
    unittest.main()
