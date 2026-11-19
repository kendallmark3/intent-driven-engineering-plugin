# Validator Fixtures — check_review.py

Synthetic review files that test the **deterministic checker** (`../../scripts/check_review.py`), not the reviewer's judgment. They contain no real system data.

- `NN-name.md` — one review per case. Cases 01–03 are well-formed shapes of the three Calibration Set cases; 04–16 are invalid or adversarial inputs designed to expose false advancement or hidden gaps.
- `expected.json` — the pre-registered result per file: exit code, computed radius and ceiling (`null` = the table is invalid, so no radius is computed), substrings that must appear in a FAIL line (`must_report`) or WARN line (`must_warn`). Committed before the checker changes that these cases test. Do not edit an expectation to make a run pass; add a new case instead.

Run all fixtures (from the skill directory):

```bash
python3 -m unittest discover -s scripts
```

`test_check_review.FixtureTests` checks every fixture against `expected.json` and runs each one repeatedly to confirm the output is identical.

These fixtures do **not** calibrate the AI review itself. That needs real systems, pre-registered by someone who knows them, and fresh-session runs — see `../README.md`.
