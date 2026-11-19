"""Tests for check_review.py. Run: python3 -m unittest discover -s scripts"""
import contextlib
import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_review as cr  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
CASE01 = os.path.join(HERE, os.pardir, "calibration", "case-01-small-prototype.md")
FIXTURES = os.path.join(HERE, os.pardir, "calibration", "fixtures")


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

    # Regression tests for the v1.4.0 hardening. Each input passed silently before.
    def test_label_must_be_whole_word(self):
        rows = [("Reachedish", "Verifiedish", "No")] + SMALL[1:]
        problems, r, _ = cr.check(review(rows, 1, "Radius 2"))
        self.assertTrue(any("Status must be" in p for p in problems))
        self.assertIsNone(r)

    def test_label_with_source_still_accepted(self):
        rows = [("Reached", "Documented — README.md#intent", "No — none open")] + SMALL[1:]
        self.assertEqual(cr.check(review(rows, 1, "Radius 2"))[0], [])

    def test_duplicate_row_fails(self):
        text = review(SMALL, 1, "Radius 2").replace("| 2 | Not reached", "| 1 | Not reached | Unknown | Yes |\n| 2 | Not reached")
        problems, r, _ = cr.check(text)
        self.assertTrue(any("more than one row for Radius 1" in p for p in problems))
        self.assertIsNone(r)

    def test_short_row_named(self):
        text = review(SMALL, 1, "Radius 2").replace("| 2 | Not reached | Verified | Yes |", "| 2 | Not reached | Verified |")
        problems = cr.check(text)[0]
        self.assertTrue(any("Radius 2 has 3 cells" in p for p in problems))
        self.assertFalse(any("missing the row" in p for p in problems[:1]))

    def test_unknown_core_with_no_gap_fails(self):
        rows = [SMALL[0], ("Not reached", "Unknown", "No")] + SMALL[2:]
        self.assertTrue(any("core evidence is Unknown" in p for p in cr.check(review(rows, 1, "Radius 2"))[0]))

    def test_radius1_na_fails(self):
        rows = [("N/A", "—", "—")] + SMALL[1:]
        self.assertTrue(any("Radius 1 cannot be N/A" in p for p in cr.check(review(rows, 0, "scope"))[0]))

    def test_na_cannot_carry_gap(self):
        rows = [SMALL[0], ("N/A", "Unknown", "Yes")] + SMALL[2:]
        self.assertTrue(any("Radius 2 is N/A but" in p for p in cr.check(review(rows, 1, "scope"))[0]))

    def test_rated_radius_above_na_fails(self):
        rows = [SMALL[0], ("N/A", "—", "—"), ("Not reached", "Documented", "Yes")] + SMALL[3:]
        self.assertTrue(any("Radius 3 is rated but Radius 2 is N/A" in p for p in cr.check(review(rows, 1, "scope"))[0]))

    def test_na_without_reason_warns_only(self):
        problems, warnings, _, _ = cr.check_all(review(SMALL, 1, "Radius 2"))
        self.assertEqual(problems, [])
        self.assertEqual(len(warnings), 3)
        rows = SMALL[:2] + [("N/A — outside intent", "—", "—")] * 3
        self.assertEqual(cr.check_all(review(rows, 1, "Radius 2"))[1], [])

    def test_verified_with_nothing_ran_warns(self):
        text = review([("Reached", "Verified", "No")] + SMALL[1:], 1, "Radius 2").replace("- Ran: unit tests", "- Ran: nothing executed")
        problems, warnings, _, _ = cr.check_all(text)
        self.assertEqual(problems, [])
        self.assertTrue(any("nothing was executed" in w for w in warnings))

    def test_bad_radius_and_ceiling_values_named(self):
        problems = cr.check(review(SMALL, 7, "the second one"))[0]
        self.assertTrue(any("no number 0-5" in p for p in problems))
        self.assertTrue(any("is not 'Radius M', 'scope' or 'none'" in p for p in problems))

    def test_non_utf8_file_exits_2(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "bad.md")
            with open(path, "wb") as f:
                f.write(b"\xff\xfe\x00bad")
            with redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()) as err:
                self.assertEqual(cr.main([path]), 2)
            self.assertIn("not UTF-8", err.getvalue())

    def test_missing_file_exits_2(self):
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(cr.main([os.path.join(HERE, "no-such-review.md")]), 2)


class FixtureTests(unittest.TestCase):
    """Every file in calibration/fixtures/ against its pre-registered expectation."""
    RUNS = 20

    def run_fixture(self, name):
        out = io.StringIO()
        with redirect_stdout(out):
            code = cr.main([os.path.join(FIXTURES, name)])
        return code, out.getvalue()

    def test_fixtures_match_expected(self):
        with open(os.path.join(FIXTURES, "expected.json"), encoding="utf-8") as f:
            cases = json.load(f)
        self.assertGreaterEqual(len(cases), 10)
        for name, exp in sorted(cases.items()):
            with self.subTest(fixture=name):
                with open(os.path.join(FIXTURES, name), encoding="utf-8") as f:
                    problems, warnings, r, c = cr.check_all(f.read())
                code, _ = self.run_fixture(name)
                self.assertEqual(code, exp["exit"], problems)
                self.assertEqual((r, c), (exp["radius"], exp["ceiling"]))
                for s in exp["must_report"]:
                    self.assertTrue(any(s in p for p in problems), "%r not in %r" % (s, problems))
                for s in exp["must_warn"]:
                    self.assertTrue(any(s in w for w in warnings), "%r not in %r" % (s, warnings))
                if exp["exit"] == 0 and not exp["must_warn"]:
                    self.assertEqual(warnings, [])  # a clean review raises no warnings

    def test_fixtures_repeatable(self):
        for name in sorted(os.listdir(FIXTURES)):
            if name.endswith(".md") and name[:2].isdigit():
                with self.subTest(fixture=name):
                    first = self.run_fixture(name)
                    for _ in range(self.RUNS - 1):
                        self.assertEqual(self.run_fixture(name), first)


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
