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

    def test_desktop_tables_reserve_useful_space_for_each_column(self):
        self.assertRegex(self.css, r"\.app-shelf-table\s*\{[^}]*width:\s*min\(")
        self.assertRegex(self.css, r"\.app-shelf-table\s*\{[^}]*left:\s*50%")
        self.assertRegex(self.css, r"\.app-shelf-table\s*\{[^}]*transform:\s*translateX\(-50%\)")
        self.assertRegex(self.css, r"\.app-shelf-table table\s*\{[^}]*table-layout:\s*fixed")
        self.assertRegex(self.css, r"\.app-shelf-table th:nth-child\(2\)[^}]*width:\s*24%")

    def test_mobile_rows_become_labelled_cards(self):
        mobile = re.search(r"@media\s*\(max-width:\s*640px\)\s*\{(?P<body>.*)\}\s*$", self.css, re.S)
        self.assertIsNotNone(mobile)
        if mobile is None:
            self.fail("Missing App Shelf mobile breakpoint")
        rules = mobile.group("body")
        self.assertRegex(rules, r"\.app-shelf-table thead\s*\{[^}]*position:\s*absolute")
        self.assertRegex(rules, r"\.app-shelf-table tr\s*\{[^}]*display:\s*block")
        self.assertRegex(rules, r"\.app-shelf-table td,[^{]*\{[^}]*display:\s*grid")
        self.assertIn('content: "App"', rules)
        self.assertIn('content: "Notes"', rules)


if __name__ == "__main__":
    unittest.main()
