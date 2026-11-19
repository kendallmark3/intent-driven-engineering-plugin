# Engineering Readiness Report — enterprise-radius-review 1.4.0

Scope: INTENT-001 (deterministic hardening and enterprise readiness). Baseline: v1.3.1, commit `9e73060`. Local development and testing only; not pushed or merged.

## Baseline

- 13/13 existing checker tests passed.
- Adversarial probes against the v1.3.1 checker: **7 invalid inputs passed silently** (labels like `Reachedish`/`Verifiedish`, a duplicate row that contradicted the first, Unknown core evidence with "no gap", Radius 1 marked N/A, an N/A row hiding an Unknown gap, an in-scope radius above an N/A one). 3 inputs gave misleading messages (short row reported as "missing"; `Radius: 7` and an unparsable ceiling reported as "no line"). A non-UTF-8 file crashed with a traceback.
- Already correct in v1.3.1: missing rows, ceiling mismatch, stated-vs-computed radius mismatch, nonzero exit on failure.

## Changes and reasons

| Change | Reason (failure case) |
|---|---|
| Labels must match as whole words; a trailing source (`Documented — README.md`) is still accepted | `Reachedish` was read as Reached |
| Duplicate rows and rows with < 4 cells are FAILs | a second, contradicting row was silently ignored; short rows were misreported as missing |
| Unknown core evidence with gap = No is a FAIL | contradicts the evidence definitions; let a row look gap-free |
| Radius 1 cannot be N/A; N/A rows cannot carry evidence or a gap; nothing in scope above an N/A radius | N/A could hide an Unknown gap or skip a radius |
| Computed radius applies the ceiling rule to every row, not the status cell | fixture 06: Radius 5 marked Reached on Reported evidence computed as 5 (found by the pre-registered fixture, not the probes) |
| No radius computed when the table is unreadable | a radius from a malformed table is misleading |
| WARN (exit unchanged): N/A without reason; Verified while "Ran: nothing executed" | judgment calls a human should see; warn rather than fail to keep existing reviews valid |
| Specific messages for bad `Radius:`/`Ceiling:` values; non-UTF-8 → exit 2 | understandable errors |
| SKILL.md: evidence-reference guidance, ceiling-gap explanation (step 3a), N/A rules, Execution Safety | Improvements B, C, D, H |
| Versions to 1.4.0; README trigger list, install command, local-dev path, structure | stale `1.0.0` references, `<github-owner>/<repo>` placeholder, README still listed the narrowed "Who owns this?" trigger |

No new dependencies, frameworks, agents, services, or distribution mechanism.

## Test results

- Expectations for 16 synthetic fixtures committed first (`42def26`), before the checker changes. `expected.json` is unchanged since.
- 28/28 tests pass (13 original, 13 regression, 2 fixture suites).
- All 16 fixtures match their pre-registered exit code, radius, ceiling, and required FAIL/WARN text.
- Repeatability (checker): each fixture run 50 times via the CLI → 1 distinct output per fixture (800 runs). The unit suite repeats each fixture 20 times.
- `claude plugin validate` passes for the marketplace and the plugin.

One test assertion was narrowed during the run: "no warnings" is now required only for passing fixtures. It was not part of the pre-registration; fixture 11 correctly warns about unjustified N/A rows alongside its FAIL.

## Compatibility

- Reviews valid under 1.3.1 stay valid, except where they relied on the defects above. A plain `N/A` (no reason) now produces a WARN but still passes.
- `check()` keeps its 3-tuple return; `check_all()` adds warnings. CLI arguments, exit codes 0/1, and the run-log row format are unchanged; exit 2 now also covers encoding errors.

## Known limitations

- The checker cannot tell whether an evidence label is true, whether a gap is material, or whether an N/A reason is valid on the merits. A source reference is not proof.
- The "nothing executed" warning depends on wording (`nothing`, `none`, `not run`, `read-only`).
- Gap explanations (step 3a) are not machine-checked.
- **Review (model-output) repeatability is not demonstrated.** Fixtures test the checker only. Calibration cases 02 and 03 still need real systems and pre-registered expectations; case 01 remains a regression baseline, not an independent test.

## Remaining risks

- Reviewers can satisfy the checker with plausible but wrong labels; human review of evidence remains necessary.
- Stricter N/A rules may surface FAILs in older saved reviews that excluded inner radii.

## Recommendation

Suitable for **enterprise evaluation as an advisory tool**, with the checker as a structural gate. Before relying on scores across teams, register cases 02 and 03 on real systems and record at least three fresh-session runs each in `run-log.md`.
