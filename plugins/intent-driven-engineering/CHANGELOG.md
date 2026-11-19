# Changelog

## 1.3.1

- Wording cleanup in the changelog and test comments; no behaviour change.

## 1.3.0

- `enterprise-radius-review`: added `scripts/check_review.py` (standard library only) — checks the advisory line, Scope & Method (unit / ran / read) and Radius Summary, recomputes the radius and ceiling with the ceiling rule, and flags any mismatch with the stated score. With `--expected` and `--log` it scores a calibration run against the pre-registered case and appends to `calibration/run-log.md`. It does not judge evidence labels.
- Output format: `Current Credible Radius` now has parsable `Radius:` / `Ceiling:` lines, and a required `Radius Summary` table (both forms).
- Validation step: run the checker when Python is available; check by hand otherwise.
- 13 unit tests, including the inflated-score pattern (outer radius claimed while inner radii have Unknown gaps).

## 1.2.0

- `enterprise-radius-review`: rewrote the ceiling rule so it has one reading (highest radius N with radii 1..N all reached; report "N, approaching N+1"; never round up).
- Narrowed the skill description so narrow ownership questions get a brief answer plus an offer, not a full review.
- Added a consistency check to Validation and synced the skill's `version` field.
- Added `calibration/`: procedure, pre-registration template, case 01 (small prototype, regression baseline), placeholders for cases 02 and 03, and a run log.

## 1.1.0

- Hardened `enterprise-radius-review` (incubating, advisory-only): advisory statement, evidence labels (Verified/Documented/Reported/Unknown), ceiling rule, scope rule, ran-vs-read Scope & Method section, Short Form, narrowed full-review triggers, and a Calibration Set.

## 1.0.0

Initial release.

- Added `intent-refiner`.
- Added `enterprise-radius-review`.
- Added `proof-case-study-builder`.
- Added governed learning rule: corrections become proposed deltas and are regression-tested before promotion.
