# Changelog

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
