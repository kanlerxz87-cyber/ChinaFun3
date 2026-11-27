"""Verification rules for the audit-ddc78a00 page (run from repo root)."""
import json
import re
import sys
import unittest
from pathlib import Path
from urllib.parse import urlparse

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import build  # noqa: E402

DATA = json.loads((HERE / "data" / "checks.json").read_text(encoding="utf-8"))
OFFICIAL_HOSTS = {
    "guide.michelin.com", "www.yugarden.com.cn", "www.news.cn", "en.nia.gov.cn",
    "www.shanghaimuseum.cn", "german.shanghai.gov.cn", "english.shanghai.gov.cn",
    "www.langhamhotels.com", "us.china-embassy.gov.cn", "sanfrancisco.china-consulate.gov.cn",
    "www.museumofartpd.org.cn",
}


class AuditTests(unittest.TestCase):
    def test_every_check_has_official_https_source(self):
        for c in DATA["checks"]:
            with self.subTest(id=c["id"]):
                u = urlparse(c["official_source"])
                self.assertEqual(u.scheme, "https")
                self.assertIn(u.hostname, OFFICIAL_HOSTS)

    def test_ids_unique_and_fields_present(self):
        ids = [c["id"] for c in DATA["checks"]]
        self.assertEqual(len(ids), len(set(ids)))
        for c in DATA["checks"]:
            for k in ("topic", "trip_claim", "evidence", "action", "source_label", "result"):
                self.assertTrue(str(c.get(k, "")).strip(), f"{c['id']} missing {k}")

    def test_results_use_defined_status_key(self):
        for c in DATA["checks"]:
            self.assertIn(c["result"], DATA["status_key"])

    def test_non_confirmed_rows_are_flagged_in_page(self):
        html_text = build.page()
        for c in DATA["checks"]:
            if c["result"] != "Confirmed":
                self.assertIn(c["id"], html_text)

    def test_built_index_matches_data(self):
        built = (HERE / "index.html").read_text(encoding="utf-8")
        self.assertEqual(built, build.page(), "run python3 audit-ddc78a00/build.py")

    def test_page_links_only_https(self):
        built = (HERE / "index.html").read_text(encoding="utf-8")
        for href in re.findall(r"href='([^']+)'", built):
            if href.startswith(("http", "//")):
                self.assertTrue(href.startswith("https://"), href)


if __name__ == "__main__":
    unittest.main()
