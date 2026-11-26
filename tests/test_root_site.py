#!/usr/bin/env python3
"""Validation suite for the re-verified ChinaFun3 root dashboard."""

from __future__ import annotations

import json
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ROOT_PAGES = [
    "index.html",
    "executive-summary.html",
    "itinerary.html",
    "hotels.html",
    "restaurants.html",
    "activities.html",
    "transport.html",
    "budget.html",
    "questions.html",
    "suggestions.html",
    "sources.html",
    "flagged.html",
    "methodology.html",
    "404.html",
]


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.refs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for k, v in attrs:
            if k in ("href", "src") and v:
                self.refs.append(v)


class RootSiteTests(unittest.TestCase):
    def test_json_datasets_valid_and_consistent(self) -> None:
        hotels = json.loads((ROOT / "data/hotels.json").read_text(encoding="utf-8"))
        rest = json.loads((ROOT / "data/restaurants.json").read_text(encoding="utf-8"))
        act = json.loads((ROOT / "data/activities.json").read_text(encoding="utf-8"))
        trip = json.loads((ROOT / "data/trip.json").read_text(encoding="utf-8"))
        bud = json.loads((ROOT / "data/budget.json").read_text(encoding="utf-8"))
        flg = json.loads((ROOT / "data/flagged.json").read_text(encoding="utf-8"))

        self.assertEqual(len(hotels["hotels"]), 12)
        self.assertEqual(sum(1 for h in hotels["hotels"] if h["bookable_feb15"]), 11)
        active_hotel_names = " ".join(h["name"] for h in hotels["hotels"])
        self.assertNotIn("Four Seasons", active_hotel_names)

        self.assertEqual(rest["summary"]["starred_total"], 50)
        self.assertEqual(rest["summary"]["total_live_entries"], 153)
        self.assertEqual(len(rest["all_starred_50"]), 50)
        self.assertEqual(sum(1 for r in rest["all_starred_50"] if r["stars"] == 3), 1)
        self.assertEqual(sum(1 for r in rest["all_starred_50"] if r["stars"] == 2), 11)
        self.assertEqual(sum(1 for r in rest["all_starred_50"] if r["stars"] == 1), 38)
        all_names = " ".join(r["name"] for r in rest["all_starred_50"] + rest["featured"])
        self.assertNotIn("Ultraviolet", all_names)
        self.assertNotIn("102 House", all_names)

        self.assertEqual(len(act["activities"]), 12)
        self.assertEqual(len(trip["peninsula_windows"]), 6)
        self.assertEqual(len(bud["exact_verified_menu_totals_for_two"]), 8)
        self.assertEqual(len(flg["flagged_irregularities"]), 10)

    def test_root_html_pages_exist_and_relative_links_resolve(self) -> None:
        for page in ROOT_PAGES:
            p = ROOT / page
            self.assertTrue(p.exists(), f"Missing root page: {page}")
            content = p.read_text(encoding="utf-8")
            parser = LinkParser()
            parser.feed(content)
            for ref in parser.refs:
                if ref.startswith(("http://", "https://", "data:", "mailto:", "tel:", "#")):
                    continue
                rel = ref.split("#", 1)[0].split("?", 1)[0]
                if not rel:
                    continue
                target = (ROOT / rel).resolve()
                self.assertTrue(target.exists(), f"Broken relative link '{ref}' in {page}")

    def test_no_unverified_minutes_or_surrogate_claims_in_root_html(self) -> None:
        idx = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertNotIn("24-month search limit", idx)
        self.assertIn("50", idx)
        tr_json = json.loads((ROOT / "data/transport.json").read_text(encoding="utf-8"))
        for row in tr_json["district_corridors"]:
            self.assertEqual(row["minutes"], "")
        tr_html = (ROOT / "transport.html").read_text(encoding="utf-8")
        self.assertIn("Minutes Unverified (F07)", tr_html)


if __name__ == "__main__":
    unittest.main()
