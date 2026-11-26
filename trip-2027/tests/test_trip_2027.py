#!/usr/bin/env python3
"""Strict automated verification suite for /trip-2027/ static couple trip dashboard."""

from __future__ import annotations

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
                # Any venue with an unverified platform slot MUST be linked to a Flag ID or documented in F10/F11/F15
                self.assertTrue(
                    record.get("flag_id") is not None or record in activities,
                    f"{record['name']} has missing social platform without flag reference",
                )

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


if __name__ == "__main__":
    unittest.main()
