import subprocess
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path


class FooterSupportLinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_footer_menu = False
        self.found_support_link = False

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "nav" and attributes.get("aria-label") == "Footer menu":
            self.in_footer_menu = True
        if (
            self.in_footer_menu
            and tag == "a"
            and attributes.get("href") == SUPPORT_URL
            and attributes.get("title") == "Support iSoul on Buy Me a Coffee"
        ):
            self.found_support_link = True

    def handle_endtag(self, tag):
        if tag == "nav" and self.in_footer_menu:
            self.in_footer_menu = False


ROOT = Path(__file__).resolve().parents[1]
SUPPORT_URL = "https://buymeacoffee.com/isoul"


class SupportLinkTests(unittest.TestCase):
    def test_support_link_is_visible_in_site_footer(self):
        with tempfile.TemporaryDirectory() as destination:
            subprocess.run(
                ["hugo", "--gc", "--minify", "--destination", destination],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            )

            for relative_page in ("index.html", "discover/index.html"):
                html = (Path(destination) / relative_page).read_text(encoding="utf-8")
                parser = FooterSupportLinkParser()
                parser.feed(html)
                self.assertTrue(
                    parser.found_support_link,
                    f"Support link missing from footer in {relative_page}",
                )
                self.assertIn("Support iSoul", html)


if __name__ == "__main__":
    unittest.main()
