import re
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CSS = ROOT / "assets" / "css" / "custom.css"


class AppShelfLayoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.build_dir = tempfile.TemporaryDirectory(prefix="isoul-app-shelf-")
        subprocess.run(
            ["hugo", "--gc", "--minify", "--destination", cls.build_dir.name],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        cls.html = (Path(cls.build_dir.name) / "app-shelf" / "index.html").read_text()
        cls.css = CSS.read_text()

    @classmethod
    def tearDownClass(cls):
        cls.build_dir.cleanup()

    def test_each_app_shelf_table_has_a_responsive_wrapper(self):
        wrappers = r"<div class=app-shelf-table>\s*<table>"
        self.assertEqual(3, len(re.findall(wrappers, self.html)))

    def test_tables_align_with_surrounding_article_text(self):
        self.assertRegex(self.css, r"\.app-shelf-table\s*\{[^}]*width:\s*100%")
        self.assertNotRegex(self.css, r"\.app-shelf-table\s*\{[^}]*translateX")
        self.assertRegex(self.css, r"\.app-shelf-table table\s*\{[^}]*table-layout:\s*fixed")
        self.assertRegex(self.css, r"\.app-shelf-table th:nth-child\(2\)[^}]*width:\s*30%")
        self.assertRegex(self.css, r"\.app-shelf-table td:nth-child\(2\) a\s*\{[^}]*white-space:\s*nowrap")

    def test_mobile_preserves_headers_and_scrolls_the_table(self):
        mobile = re.search(r"@media\s*\(max-width:\s*640px\)\s*\{(?P<body>.*)\}\s*$", self.css, re.S)
        self.assertIsNotNone(mobile)
        if mobile is None:
            self.fail("Missing App Shelf mobile breakpoint")
        rules = mobile.group("body")
        self.assertRegex(rules, r"\.app-shelf-table\s*\{[^}]*overflow-x:\s*auto")
        self.assertRegex(rules, r"\.app-shelf-table table\s*\{[^}]*min-width:\s*44rem")
        self.assertNotRegex(rules, r"\.app-shelf-table thead\s*\{[^}]*position:\s*absolute")
        self.assertNotRegex(rules, r"\.app-shelf-table tr\s*\{[^}]*display:\s*block")


if __name__ == "__main__":
    unittest.main()
