"""Tests for check_review.py. Run: python3 -m unittest discover -s scripts"""
import io
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_review as cr  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
CASE01 = os.path.join(HERE, os.pardir, "calibration", "case-01-small-prototype.md")


def review(rows, radius, ceiling, advisory=True, scope=True):
    parts = ["# Radius Review: test", ""]
    if advisory:
        parts += ["> Advisory review — not a security review, architecture approval, or production readiness sign-off.", ""]
    if scope:
        parts += ["## Scope & Method", "- Unit rated: one CLI", "- Ran: unit tests", "- Read: README", ""]
    parts += ["## Executive Finding", "Judgment.", "",
              "## Current Credible Radius", "Radius: %s" % radius, "Ceiling: %s" % ceiling, "",
              "## Radius Summary",
              "| Radius | Status | Core evidence | Unknown material gap |", "|---|---|---|---|"]
    parts += ["| %d | %s | %s | %s |" % ((i + 1,) + r) for i, r in enumerate(rows)]
    return "\n".join(parts) + "\n"


# Case 01 shape: R1 reached, R2 has an Unknown gap, R3-5 out of scope.
SMALL = [("Reached", "Documented", "No"), ("Not reached", "Verified", "Yes"),
         ("N/A", "—", "—"), ("N/A", "—", "—"), ("N/A", "—", "—")]


class CheckTests(unittest.TestCase):
    def test_consistent_review_passes(self):
        problems, r, c = cr.check(review(SMALL, 1, "Radius 2"))
        self.assertEqual(problems, [])
        self.assertEqual((r, c), (1, "Radius 2"))

    def test_inflated_score_fails(self):
        # Inflated-score pattern: Radius 4 claimed while inner radii have Unknown gaps.
        rows = [("Not reached", "Documented", "Yes"), ("Not reached", "Unknown", "Yes"),
                ("Reached", "Documented", "No"), ("Reached", "Documented", "No"), ("Not reached", "Unknown", "Yes")]
        problems, r, c = cr.check(review(rows, 4, "Radius 5"))
        self.assertEqual((r, c), (0, "Radius 1"))
        self.assertTrue(any("Stated radius 4" in p for p in problems))

    def test_reached_with_unknown_gap_fails(self):
        rows = [("Reached", "Documented", "Yes")] + SMALL[1:]
        problems, _, _ = cr.check(review(rows, 1, "Radius 2"))
        self.assertTrue(any("marked Reached" in p for p in problems))

    def test_reached_on_reported_evidence_fails(self):
        rows = [("Reached", "Reported", "No")] + SMALL[1:]
        problems, _, _ = cr.check(review(rows, 1, "Radius 2"))
        self.assertTrue(any("marked Reached" in p for p in problems))

    def test_scope_ceiling(self):
        rows = [("Reached", "Verified", "No"), ("Reached", "Verified", "No")] + SMALL[2:]
        problems, r, c = cr.check(review(rows, 2, "scope"))
        self.assertEqual(problems, [])
        self.assertEqual((r, c), (2, "scope"))

    def test_missing_advisory_and_scope_fail(self):
        problems, _, _ = cr.check(review(SMALL, 1, "Radius 2", advisory=False, scope=False))
        self.assertTrue(any("advisory" in p for p in problems))
        self.assertTrue(any("Scope & Method" in p for p in problems))

    def test_scope_labels_with_bold_and_notes(self):
        text = review(SMALL, 1, "Radius 2").replace("- Ran: unit tests", "- **Ran (on a scratch copy):**\n  - unit tests")
        text = text.replace("- Unit rated:", "- **Unit rated:**")
        self.assertEqual(cr.check(text)[0], [])

    def test_ready_is_not_read(self):
        text = review(SMALL, 1, "Radius 2").replace("- Read: README", "- Ready: soon")
        self.assertTrue(any("Read:" in p for p in cr.check(text)[0]))

    def test_missing_row_fails(self):
        problems, _, _ = cr.check(review(SMALL[:4], 1, "Radius 2"))
        self.assertTrue(any("Radius 5" in p for p in problems))

    def test_bold_and_r_prefix_tolerated(self):
        text = review(SMALL, 1, "Radius 2").replace("| 1 | Reached", "| **R1** | **Reached**")
        text = text.replace("Radius: 1", "**Radius: 1** (approaching 2)")
        self.assertEqual(cr.check(text)[0], [])


class CalibrationTests(unittest.TestCase):
    def run_main(self, text, *args):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "review.md")
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
            log = os.path.join(d, "run-log.md")
            out = io.StringIO()
            with redirect_stdout(out):
                code = cr.main([path, "--expected", CASE01, "--log", log] + list(args))
            with open(log, encoding="utf-8") as f:
                return code, out.getvalue(), f.read()

    def test_case01_expectation_parses(self):
        with open(CASE01, encoding="utf-8") as f:
            self.assertEqual(cr.expected(f.read()), (1, "Radius 2"))

    def test_match_logs_pass(self):
        code, out, log = self.run_main(review(SMALL, 1, "Radius 2"), "--note", "t")
        self.assertEqual(code, 0)
        self.assertIn("MATCH", out)
        self.assertIn("| yes | yes | t (check_review.py) |", log)

    def test_mismatch_logs_fail(self):
        rows = [("Reached", "Documented", "No"), ("Reached", "Verified", "No")] + SMALL[2:]
        code, out, log = self.run_main(review(rows, 2, "scope"))
        self.assertEqual(code, 1)
        self.assertIn("MISMATCH", out)
        self.assertIn("| no |", log)


if __name__ == "__main__":
    unittest.main()
