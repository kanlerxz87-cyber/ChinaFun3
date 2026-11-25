"""Offline verification tests for the verify/ dashboard.

Run: python3 -m unittest discover -s verify/tests -v
"""
import glob
import json
import os
import re
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
VERIFY = os.path.join(ROOT, "verify")


def load(name):
    with open(os.path.join(VERIFY, "data", name), encoding="utf-8") as fh:
        return json.load(fh)


class TestData(unittest.TestCase):
    def test_all_json_parse(self):
        files = glob.glob(os.path.join(VERIFY, "data", "*.json"))
        self.assertGreaterEqual(len(files), 6)
        for f in files:
            json.load(open(f, encoding="utf-8"))

    def test_hotel_arithmetic(self):
        hotels = load("hotels.json")["hotels"]
        self.assertEqual(len(hotels), 8)
        for h in hotels:
            if h["nightly_usd"] is None:
                self.assertIsNone(h["seven_night_total_usd"])
                continue
            self.assertEqual(h["seven_night_total_usd"], h["nightly_usd"] * 7)
            self.assertEqual(h["seven_night_total_usd_taxes"], h["nightly_usd_taxes"] * 7)

    def test_restaurant_directory_counts(self):
        restaurants = load("restaurants.json")["restaurants"]
        self.assertEqual(len(restaurants), 50)
        three = [r for r in restaurants if r["stars"] == 3]
        two = [r for r in restaurants if r["stars"] == 2]
        one = [r for r in restaurants if r["stars"] == 1]
        self.assertEqual(len(three), 1)
        self.assertEqual(len(two), 11)
        self.assertEqual(len(one), 38)
        for r in restaurants:
            self.assertTrue(r["url"].startswith("https://guide.michelin.com/"), r["name"])
            self.assertIn(r["band"], ["¥", "¥¥", "¥¥¥", "¥¥¥¥"], r["name"])

    def test_deep_verified_restaurants_have_required_fields(self):
        restaurants = load("restaurants.json")["restaurants"]
        deep = [r for r in restaurants if r.get("deep")]
        self.assertEqual(len(deep), 12)
        for r in deep:
            self.assertTrue(r.get("addr"), r["name"])
            self.assertTrue(r.get("district"), r["name"])

    def test_activities_verified_have_hours(self):
        activities = load("activities.json")["activities"]
        for a in activities:
            if a["verified"]:
                self.assertTrue(a["hours"], a["name"])
                self.assertTrue(a["days"], a["name"])
                self.assertTrue(a["hours_source"], a["name"])
            else:
                self.assertEqual(a["hours"], "", a["name"])

    def test_flagged_ids_unique(self):
        items = load("flagged.json")["items"]
        ids = [i["id"] for i in items]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertGreaterEqual(len(ids), 8)


class TestHtml(unittest.TestCase):
    def setUp(self):
        self.pages = sorted(glob.glob(os.path.join(VERIFY, "*.html")))

    def test_expected_pages_exist(self):
        expected = {
            "index.html", "hotels.html", "restaurants.html", "activities.html",
            "transport.html", "budget.html", "questions.html", "suggestions.html",
            "sources.html", "flagged.html", "verification.html",
        }
        names = {os.path.basename(p) for p in self.pages}
        self.assertTrue(expected.issubset(names), expected - names)

    def test_every_table_row_has_source_or_unverified_flag(self):
        # Every <tr> that is a data row must contain either an external href
        # (source link) or the Unverified badge in its cells.
        for path in self.pages:
            html = open(path, encoding="utf-8").read()
            for tr in re.findall(r"<tr>(.*?)</tr>", html, flags=re.S):
                if "<th" in tr:
                    continue  # header row
                if "href=" in tr:
                    continue
                self.assertIn("Unverified", tr, "row without source or flag in %s: %s" % (path, tr[:120]))

    def test_internal_links_resolve(self):
        for path in self.pages:
            html = open(path, encoding="utf-8").read()
            for href in re.findall(r'href="([^"#]+?)"', html):
                if href.startswith(("http", "mailto:", "tel:")):
                    continue
                target = os.path.join(VERIFY, href)
                self.assertTrue(os.path.exists(target), "broken internal link %s -> %s" % (path, href))

    def test_restaurants_page_row_count(self):
        html = open(os.path.join(VERIFY, "restaurants.html"), encoding="utf-8").read()
        data_rows = [tr for tr in re.findall(r"<tr>(.*?)</tr>", html, flags=re.S) if "<th" not in tr]
        self.assertEqual(len(data_rows), 50)


if __name__ == "__main__":
    unittest.main()
