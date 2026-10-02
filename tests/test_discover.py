import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class DiscoverCatalogTests(unittest.TestCase):
    def test_catalog_has_every_v1_medium_and_required_editorial_fields(self):
        catalog_path = ROOT / "data" / "discover" / "catalog.json"
        self.assertTrue(catalog_path.exists(), "catalog.json should exist")

        items = json.loads(catalog_path.read_text(encoding="utf-8"))["items"]
        self.assertEqual({"film", "tv", "anime", "music"}, {item["type"] for item in items})

        required = {"id", "title", "type", "year", "country", "genres", "blurb", "palette", "source_url"}
        for item in items:
            self.assertTrue(required.issubset(item), item)
            self.assertTrue(item["blurb"].strip())
            self.assertIn(item["palette"], {"teal", "coral", "moss", "blue", "violet", "gold", "rose", "ink"})
            self.assertTrue(item["source_url"].startswith("https://"))


class DiscoverVoiceTests(unittest.TestCase):
    def test_five_default_voices_are_bounded_and_attributed(self):
        voices_path = ROOT / "data" / "discover" / "voices.json"
        self.assertTrue(voices_path.exists(), "voices.json should exist")

        voices = json.loads(voices_path.read_text(encoding="utf-8"))["voices"]
        self.assertEqual(5, len(voices))
        self.assertEqual(
            {"stuart-heritage", "peter-bradshaw", "lucy-mangan", "wrong-every-time", "alexis-petridis"},
            {voice["id"] for voice in voices},
        )
        self.assertEqual({"film", "tv", "anime", "music"}, {voice["category"] for voice in voices})

        for voice in voices:
            self.assertLessEqual(len(voice["items"]), 3)
            self.assertTrue(voice["home_url"].startswith("https://"))
            self.assertTrue(voice["feed_url"].startswith("https://"))
            self.assertIn(voice["automation"], {"feed", "rss-article"})
            for item in voice["items"]:
                self.assertTrue(item["source_url"].startswith("https://"))
                self.assertIn(item["status"], {"editorial-example", "needs-editorial-summary"})


class DiscoverTonightTests(unittest.TestCase):
    def test_tonight_data_is_bounded_to_supported_regions(self):
        tonight_path = ROOT / "data" / "discover" / "tonight.json"
        self.assertTrue(tonight_path.exists(), "tonight.json should exist")

        tonight = json.loads(tonight_path.read_text(encoding="utf-8"))
        regions = tonight["regions"]
        self.assertEqual(["GB", "US"], [region["code"] for region in regions])
        self.assertTrue(tonight["source_url"].startswith("https://"))
        self.assertEqual("https://creativecommons.org/licenses/by-sa/4.0/", tonight["licence_url"])
        for region in regions:
            self.assertIn(region["status"], {"unavailable", "limited", "ready", "stale"})
            self.assertLessEqual(len(region["channels"]), 5)
            self.assertTrue(region["note"].strip())
            for channel in region["channels"]:
                self.assertLessEqual(len(channel["programmes"]), 4)


class DiscoverRenderedPageTests(unittest.TestCase):
    def test_hugo_build_renders_accessible_discovery_experience(self):
        with tempfile.TemporaryDirectory() as destination:
            result = subprocess.run(
                ["hugo", "--minify", "--destination", destination],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )
            self.assertEqual(0, result.returncode, result.stderr)
            page_path = Path(destination) / "discover" / "index.html"
            self.assertTrue(page_path.exists(), "Hugo should render /discover/")
            page = page_path.read_text(encoding="utf-8")
            for marker in (
                "data-discover-app",
                "data-filter-type=film",
                "data-random",
                "data-region",
                "data-region-code=GB",
                "data-region-code=US",
                "New episodes tonight",
                "New-episode data from",
                "not a complete national EPG",
                "United Kingdom",
                "United States",
                "https://creativecommons.org/licenses/by-sa/4.0/",
            ):
                self.assertIn(marker, page)
            for removed_marker in (
                "data-voice-form",
                "data-seerr-form",
                "data-seerr-link",
                "My voices",
                "Optional Seerr handoff",
            ):
                self.assertNotIn(removed_marker, page)
            self.assertIn("<noscript>", page)
            self.assertNotIn("&amp;#34;", page)
            self.assertIn("data-media-type=film", page)
            self.assertIn("/discover/discover.js", page)
            self.assertIn("/discover/discover.css", page)


class DiscoverNavigationTests(unittest.TestCase):
    def test_discover_is_linked_from_the_main_menu(self):
        config = (ROOT / "hugo.toml").read_text(encoding="utf-8")
        self.assertIn('identifier = "discover"', config)
        self.assertIn('url = "/discover/"', config)


if __name__ == "__main__":
    unittest.main()
