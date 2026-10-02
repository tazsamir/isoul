import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("discover_tv", ROOT / "scripts" / "discover_tv.py")
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("Unable to load discover_tv.py")
discover_tv = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(discover_tv)


class DiscoverTVTests(unittest.TestCase):
    def test_v1_only_enables_regions_with_usable_coverage(self):
        self.assertEqual(["GB", "US"], list(discover_tv.REGIONS))

    def test_groups_evening_programmes_into_at_most_five_channels(self):
        records = [
            self.record("BBC One", "17:30", "Too early", "Reality", 2),
            self.record("BBC One", "20:00", "Drama opening", "Scripted", 1),
            self.record("BBC One", "21:00", "Later drama", "Scripted", 2),
            self.record("BBC Two", "21:00", "Documentary", "Documentary", 3),
            self.record("ITV1", "19:30", "Soap", "Scripted", 8),
            self.record("Channel 4", "22:00", "Comedy", "Scripted", 1),
            self.record("5", "20:00", "History", "Documentary", 4),
            self.record("Sky Atlantic", "21:00", "Sixth channel", "Scripted", 1),
        ]

        channels = discover_tv.select_channels(records, discover_tv.REGIONS["GB"])

        self.assertEqual(["BBC One", "BBC Two", "ITV1", "Channel 4", "Channel 5"], [row["name"] for row in channels])
        self.assertEqual(["20:00", "21:00"], [p["time"] for p in channels[0]["programmes"]])
        titles = {p["title"] for row in channels for p in row["programmes"]}
        self.assertNotIn("Too early", titles)
        self.assertNotIn("Sixth channel", titles)
        self.assertTrue(all(p["source_url"].startswith("https://www.tvmaze.com/") for row in channels for p in row["programmes"]))

    def test_country_payload_is_honest_about_sparse_coverage(self):
        records = [self.record("CBS", "20:00", "One show", "Scripted", 1)]

        region = discover_tv.build_region("US", "2026-10-02", records)

        self.assertEqual("limited", region["status"])
        self.assertEqual(1, len(region["channels"]))
        self.assertIn("incomplete", region["note"].lower())

    def test_country_payload_keeps_last_good_data_when_fetch_fails(self):
        previous = {
            "code": "US",
            "label": "United States",
            "status": "ready",
            "date": "2026-10-01",
            "channels": [{"name": "CBS", "programmes": []}],
        }

        region = discover_tv.failed_region("US", "2026-10-02", previous, "network error")

        self.assertEqual("stale", region["status"])
        self.assertEqual("2026-10-01", region["date"])
        self.assertEqual("CBS", region["channels"][0]["name"])
        self.assertNotIn("network error", region["note"])

    def test_daily_workflow_publishes_listings_without_manual_review(self):
        workflow = (ROOT / ".github" / "workflows" / "discover-tv.yml").read_text(encoding="utf-8")

        self.assertIn("cron: '12 16 * * *'", workflow)
        self.assertIn("contents: write", workflow)
        self.assertIn("python scripts/discover_tv.py", workflow)
        self.assertIn("git commit", workflow)
        self.assertIn("git push origin HEAD:main", workflow)
        self.assertNotIn("create-pull-request", workflow)
        self.assertNotIn("draft: true", workflow)

    @staticmethod
    def record(channel, airtime, title, show_type, episode_number):
        return {
            "airdate": "2026-10-02",
            "airtime": airtime,
            "name": "Episode title",
            "number": episode_number,
            "season": 1,
            "url": f"https://www.tvmaze.com/episodes/{episode_number}",
            "show": {
                "name": title,
                "type": show_type,
                "network": {"name": channel},
                "genres": ["Drama"],
            },
        }


if __name__ == "__main__":
    unittest.main()
