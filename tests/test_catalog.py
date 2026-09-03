import unittest

from ccstatusline_editor.app import COMMON_WIDGET_FIELDS, WIDGET_OPTIONS, WIDGET_TYPES


class CatalogTests(unittest.TestCase):
    def test_new_widget_types_present(self):
        types = {w["type"] for w in WIDGET_TYPES}
        for t in ("sandbox-status", "git-ci-status", "cache-timer", "fable-weekly-usage"):
            self.assertIn(t, types)

    def test_new_widget_options(self):
        sandbox_keys = {f["key"] for f in WIDGET_OPTIONS["sandbox-status"]}
        self.assertEqual(sandbox_keys, {"format", "nerdFont"})
        self.assertEqual({f["key"] for f in WIDGET_OPTIONS["git-ci-status"]}, {"hideNoGit"})
        cache_keys = {f["key"] for f in WIDGET_OPTIONS["cache-timer"]}
        self.assertIn("ttlSeconds", cache_keys)
        self.assertIn("hideWhenEmpty", cache_keys)
        self.assertIn("symbolHot", cache_keys)
        display_keys = {f["key"] for f in WIDGET_OPTIONS["fable-weekly-usage"]}
        self.assertEqual(display_keys, {"display", "invert", "cursor"})

    def test_common_item_fields(self):
        keys = [f["key"] for f in COMMON_WIDGET_FIELDS]
        self.assertEqual(keys, ["rawValue", "merge", "hide"])
        kinds = {f["key"]: f["kind"] for f in COMMON_WIDGET_FIELDS}
        self.assertEqual(kinds["rawValue"], "json-bool")
        self.assertEqual(kinds["merge"], "item-select")
        self.assertEqual(kinds["hide"], "json-bool")


if __name__ == "__main__":
    unittest.main()
