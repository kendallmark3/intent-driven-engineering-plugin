# Calibration Set — enterprise-radius-review

These cases check that the skill scores systems consistently and does not inflate radius. Re-run them before promoting any rule change (see the Learning Rule in `SKILL.md`).

## Files
- `case-template.md` — copy this for each new case. Fill in **Expected outcome** before running the review.
- `case-01-small-prototype.md` — reference case: small local prototype.
- `case-02-production-service.md` — placeholder: needs a real production service.
- `case-03-documented-thin-evidence.md` — placeholder: needs a well-documented system with thin evidence.
- `run-log.md` — one row per review run. This is the evidence record.
- `../scripts/check_review.py` — deterministic checker and scorer (standard library only). Tests: `python3 -m unittest discover -s scripts`.

## Procedure
1. **Pre-register.** Fill in the case's Expected outcome, then commit it (or otherwise date-stamp it) before running anything. Someone who knows the system should set it.
2. **Get permission.** Only run against systems and data you are authorised to review with an AI assistant.
3. **Run in fresh sessions.** Run the review on the same case at least 3 times, each in a new session, so earlier runs do not influence later ones.
4. **Score and record every run**, including runs that miss. Save the review to a file, then from the skill directory:
   ```bash
   python3 scripts/check_review.py review.md --expected calibration/case-NN-name.md --log calibration/run-log.md --note "fresh session, run 1"
   ```
   It checks the structure, recomputes the radius and ceiling with the ceiling rule, compares them with the pre-registered expectation, and appends a row to `run-log.md`. Fill in the Form column by hand (the script does not judge Short vs. Full).
5. **Review the result** against the pass criteria below. Without Python, score by hand and add the row yourself.
6. **Do not edit expected outcomes after running.** If an expectation was wrong, record why and add a new case version instead.

## Pass criteria for a run
- Current credible radius matches the expected radius.
- The radius named as the ceiling matches.
- Form (Short or Full) matches.
- Advisory statement and Scope & Method (ran vs. read) are present.
- No radius above the ceiling is scored as reached.
- No out-of-scope radius is treated as a defect.

## Consistency criterion for a case
All runs of the same case, on the same evidence, give the same radius and the same ceiling. If they differ, record the judgment call that caused the difference — it is a candidate for a rule clarification.
