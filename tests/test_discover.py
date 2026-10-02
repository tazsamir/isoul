import json
import re
import shutil
import subprocess
import tempfile
import unittest
from datetime import date
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
        self.assertEqual({"film", "tv", "screen", "music"}, {voice["category"] for voice in voices})
        nick_creamer = next(voice for voice in voices if voice["id"] == "wrong-every-time")
        self.assertEqual("screen", nick_creamer["category"])

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


class DiscoverSeasonalCalendarTests(unittest.TestCase):
    def test_calendar_has_sourced_tv_and_movie_releases_for_each_region(self):
        calendar_path = ROOT / "data" / "discover" / "calendar.json"
        self.assertTrue(calendar_path.exists(), "calendar.json should exist")

        calendar = json.loads(calendar_path.read_text(encoding="utf-8"))
        self.assertEqual(["GB", "US"], [region["code"] for region in calendar["regions"]])
        for region in calendar["regions"]:
            self.assertTrue(region["seasons"], region["code"])
            for season in region["seasons"]:
                self.assertRegex(season["id"], r"^\d{4}-(winter|spring|summer|autumn)$")
                self.assertLessEqual(season["starts_on"], season["ends_on"])
                self.assertEqual({"tv", "movie"}, set(season["releases"]))
                for medium in ("tv", "movie"):
                    self.assertTrue(season["releases"][medium], (region["code"], medium))
                    for release in season["releases"][medium]:
                        self.assertTrue({"title", "release_date", "blurb", "source_url"}.issubset(release))
                        self.assertTrue(release["source_url"].startswith("https://"))
                        self.assertLessEqual(season["starts_on"], release["release_date"])
                        self.assertLessEqual(release["release_date"], season["ends_on"])
                        self.assertEqual(
                            date.fromisoformat(release["release_date"]).strftime("%A"),
                            release["weekday"],
                        )

    def test_calendar_has_responsive_component_styles(self):
        stylesheet = (ROOT / "static" / "discover" / "discover.css").read_text(encoding="utf-8")
        for selector in (
            ".discover-calendar-controls",
            ".discover-calendar-tabs",
            ".discover-release-grid",
            ".discover-release-card",
            ".discover-calendar-panel-heading",
        ):
            self.assertIn(selector, stylesheet)


class DiscoverRenderedPageTests(unittest.TestCase):
    def test_discover_uses_compact_dark_media_dashboard_contract(self):
        stylesheet = (ROOT / "static" / "discover" / "discover.css").read_text(encoding="utf-8")
        for marker in (
            "--discover-bg: #0b0b0f",
            "--discover-surface: #16161a",
            "--discover-surface-2: #1f1f26",
            "--discover-accent: #00a4dc",
            "font-family: ui-sans-serif",
            "grid-template-columns: repeat(auto-fill, minmax(190px, 1fr))",
            "aspect-ratio: 2 / 3",
            "@media (max-width: 640px)",
        ):
            self.assertIn(marker, stylesheet)

        self.assertNotIn("font-family: ui-serif", stylesheet)
        for visual_order_override in ("#wander { order:", "#calendar { order:", "#tonight { order:", "#voices { order:"):
            self.assertNotIn(visual_order_override, stylesheet)
        declarations = re.findall(r"font-size:\s*([^;]+)", stylesheet)
        self.assertTrue(declarations)
        for declaration in declarations:
            self.assertNotIn("var(", declaration)
            rem_sizes = [float(size) for size in re.findall(r"(\d*\.?\d+)rem", declaration)]
            px_sizes = [float(size) for size in re.findall(r"(\d*\.?\d+)px", declaration)]
            self.assertTrue(rem_sizes or px_sizes, declaration)
            self.assertTrue(all(size >= 0.75 for size in rem_sizes), declaration)
            self.assertTrue(all(size >= 12 for size in px_sizes), declaration)

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
            jump_positions = [
                page.find('href=#wander'),
                page.find('href=#calendar'),
                page.find('href=#tonight'),
                page.find('href=#voices'),
            ]
            self.assertTrue(all(position >= 0 for position in jump_positions))
            self.assertEqual(sorted(jump_positions), jump_positions)
            section_positions = [
                page.find('id=wander'),
                page.find('id=calendar'),
                page.find('id=tonight'),
                page.find('id=voices'),
            ]
            self.assertTrue(all(position >= 0 for position in section_positions))
            self.assertEqual(sorted(section_positions), section_positions)
            for marker in (
                "data-discover-app",
                'data-visual-style=dark-media-dashboard',
                "data-filter-type=film",
                "data-random",
                "data-global-region",
                "Country for Calendar and Tonight",
                "data-region-code=GB",
                "data-region-code=US",
                "data-calendar-app",
                "data-calendar-medium=tv",
                "data-calendar-medium=movie",
                "data-calendar-season",
                "data-calendar-season-region=US",
                "Seasonal TV & film calendar",
                "TV premieres",
                "Cinema releases",
                "Browse AniChart",
                "Browse Letterboxd",
                "https://anichart.net/",
                "https://letterboxd.com/films/",
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
            self.assertEqual(1, page.count("data-global-region"))
            self.assertNotIn("<select data-calendar-region", page)
            self.assertNotIn("<select data-region", page)
            self.assertNotIn("&amp;#34;", page)
            self.assertIn("data-media-type=film", page)
            self.assertRegex(page, r'/discover/discover\.js\?v=[0-9a-f]{64}')
            self.assertRegex(page, r'/discover/discover\.css\?v=[0-9a-f]{64}')


class DiscoverNavigationTests(unittest.TestCase):
    def test_discover_is_linked_from_the_main_menu(self):
        config = (ROOT / "hugo.toml").read_text(encoding="utf-8")
        self.assertIn('identifier = "discover"', config)
        self.assertIn('url = "/discover/"', config)


if __name__ == "__main__":
    unittest.main()
