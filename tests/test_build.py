import importlib.util
import unittest
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

spec = importlib.util.spec_from_file_location("build", Path(__file__).parents[1] / "scripts/build.py")
build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)


class BadgeTests(unittest.TestCase):
    def test_reserved_characters_are_encoded(self):
        url = build.badge_url({"label": "C++ / C# & A-B_C", "color": "123ABC", "logo": "cplusplus"})
        self.assertIn("C%2B%2B%20%2F%20C%23%20%26%20A--B__C", url)
        self.assertNotIn("#", url)
        self.assertEqual(parse_qs(urlsplit(url).query)["logo"], ["cplusplus"])

    def test_invalid_color_is_rejected(self):
        with self.assertRaises(ValueError):
            build.catalog([{"category": "Test", "badges": [{"label": "Test", "color": "red"}]}])

    def test_duplicate_labels_are_rejected(self):
        badge = {"label": "Python", "color": "3776AB"}
        with self.assertRaises(ValueError):
            build.catalog([{"category": "Test", "badges": [badge, badge]}])

    def test_text_only_badge(self):
        self.assertNotIn("logo=", build.badge_url({"label": "PLC", "color": "B3001B"}))


if __name__ == "__main__":
    unittest.main()
