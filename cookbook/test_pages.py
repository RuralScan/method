from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from build import check_pages
from pages import pages


class CookbookPagesTest(unittest.TestCase):
    def test_family_and_unassigned_rows_use_different_scopes(self):
        blank = dict.fromkeys(("T3", "T4", "T6", "T6E"), 0)
        profiles = {
            "riparian_buffer": {
                "name": "Riparian Buffers",
                "families": {
                    "riparian_buffer__planted": {
                        "product_type": "zonal_linear",
                        "variants": [{"name": "Filter strip"}],
                        "counts": {**blank, "T3": 1},
                        "mapping_variables": [],
                        "selected": 0,
                        "with_options": 0,
                        "spatially_validated": 0,
                    }
                },
                "practice_counts": {**blank, "T6": 2},
                "totals": {**blank, "T3": 1, "T6": 2},
            }
        }
        pin = {
            "release_id": "release",
            "method": {"revision": "manifest", "manifest": "model.json"},
        }
        rendered = pages(profiles, pin, "evidence-tree", "definition-tree")
        self.assertIn(
            "| Assigned to a family | 1 | 0 | 0 | 0 | 1 |", rendered["README.md"]
        )
        self.assertIn("| Practice-wide | 0 | 0 | 2 | 0 | 2 |", rendered["README.md"])
        guide = rendered["riparian_buffer.md"]
        self.assertIn("Linear corridor", guide)
        self.assertIn("zero compiled T4", guide)
        self.assertIn("/definition-tree/data-model/configuration/", guide)
        self.assertIn("/manifest/model.json", rendered["README.md"])

    def test_comparison_detects_stale_and_retired_pages(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            expected = {"README.md": "Published\n"}
            page = root / "README.md"
            page.write_text(expected["README.md"])
            check_pages(root, expected)
            page.write_text("Out of date\n")
            with self.assertRaisesRegex(ValueError, "page differs"):
                check_pages(root, expected)
            (root / "retired.md").touch()
            with self.assertRaisesRegex(ValueError, "inventory differs"):
                check_pages(root, expected)
