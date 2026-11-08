"""Tests for scripts/markdown/apply_fixes.py. Run from this folder: python3 -m unittest test_apply_fixes"""
import contextlib
import io
import json
import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts", "markdown"))
import apply_fixes  # noqa: E402

CHAPTER_NAME = "Chapter 3 Pricing That Pays the Rent.md"


class ApplyFixesTest(unittest.TestCase):
    def setUp(self):
        self.working_folder = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.working_folder, "manuscript"))
        shutil.copy(os.path.join(os.path.dirname(__file__), "sample-chapter.md"),
                    os.path.join(self.working_folder, "manuscript", CHAPTER_NAME))
        self.chapter_path = os.path.join(self.working_folder, "manuscript", CHAPTER_NAME)
        self.original_text = open(self.chapter_path, encoding="utf-8").read()

    def tearDown(self):
        shutil.rmtree(self.working_folder)

    def run_batch(self, mode, fixes):
        batch_path = os.path.join(self.working_folder, "fixes.json")
        json.dump({"name": "test", "folder": "manuscript", "backups": "backups",
                   "startMarker": "[START CHAPTER]", "endMarker": "[END CHAPTER]",
                   "fixes": [dict(fix, doc=CHAPTER_NAME) for fix in fixes]},
                  open(batch_path, "w", encoding="utf-8"))
        captured = io.StringIO()
        with contextlib.redirect_stdout(captured):
            apply_fixes.run(mode, batch_path)
        return captured.getvalue()

    def test_check_changes_nothing(self):
        output = self.run_batch("check", [{"id": "A", "find": "In order to price", "replace": "To price"}])
        self.assertIn("READY: A", output)
        self.assertEqual(open(self.chapter_path, encoding="utf-8").read(), self.original_text)
        self.assertFalse(os.path.exists(os.path.join(self.working_folder, "backups")))

    def test_apply_backs_up_and_is_repeatable(self):
        fixes = [{"id": "A", "find": "In order to price", "replace": "To price"},
                 {"id": "B", "kind": "replaceAll", "find": "store front", "replace": "storefront"}]
        self.run_batch("apply", fixes)
        backups = os.listdir(os.path.join(self.working_folder, "backups"))
        self.assertEqual(len(backups), 1)
        self.assertEqual(open(os.path.join(self.working_folder, "backups", backups[0]), encoding="utf-8").read(),
                         self.original_text)
        second_run = self.run_batch("apply", fixes)
        self.assertIn("ALREADY APPLIED: A", second_run)
        self.assertEqual(len(os.listdir(os.path.join(self.working_folder, "backups"))), 1)

    def test_ambiguous_and_outside_markers_are_skipped(self):
        output = self.run_batch("apply", [{"id": "rent", "find": "rent", "replace": "lease"},
                                          {"id": "notes", "find": "delve into", "replace": "explore"}])
        self.assertIn("FOUND 4 TIMES", output)
        self.assertIn("NOT FOUND", output)
        self.assertEqual(open(self.chapter_path, encoding="utf-8").read(), self.original_text)

    def test_deletion_that_never_matched_is_not_reported_done(self):
        output = self.run_batch("check", [{"id": "C", "find": "text that is not there", "replace": ""}])
        self.assertIn("GONE", output)
        self.assertNotIn("ALREADY APPLIED", output)


if __name__ == "__main__":
    unittest.main()
