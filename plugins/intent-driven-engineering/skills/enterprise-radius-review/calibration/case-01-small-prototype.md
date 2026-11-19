# Case 01 — Small prototype (local productivity-review CLI)

## Status
Generic expectation registered in SKILL.md v1.1.0 (Calibration Set item 1) before the first run.
Specific expectation below was recorded from the first run on 2026-11-19 (skill v1.1.0) and reviewed against the evidence. Treat it as a **regression baseline**, not an independent test of the skill.

## Subject
- System / repo: `progressive-ai-team-starter` — a deterministic Python CLI that turns notes into priorities, next actions, and approval flags. No LLM calls.
- Unit to rate: the V1 productivity-review job (`run.py` → `app/review.py` → `app/quality_gate.py`, plus `/review`).
- What the reviewer may run: the unit tests, one example run with a fixed date, and the viability scorer — **on a scratch copy**, because runs write to tracked evidence files.

## Expected outcome
- Current credible radius: **1, approaching 2**
- Ceiling set by: **Radius 2** — the owner's KEEP/CHANGE/DROP verdict on their own notes (the intent's success criterion) is **Unknown**; no verdicts are recorded in `evidence/runs.jsonl`.
- Form: **Short**
- Out-of-scope radii (should be N/A): **3, 4, 5** (the intent explicitly excludes integrations, schedules, and infrastructure).
- Must be flagged:
  - the shared keyword list between reviewer and quality gate (a missing word passes both);
  - `hooks/*.md` are written specs, not enforced hooks;
  - viability run 2 reused run 1's cases, so it does not prove viability.
- Must NOT happen:
  - recommending platform infrastructure, agents, or integrations;
  - scoring Radius 2 on test results alone.

## Why this expectation
The build is well tested and was honestly evaluated on held-out cases, but the intent defines success as the owner's own verdict on real notes, and none exists yet.

## Note
This repo's evidence changes as the owner records feedback. Once verdicts exist, this case's expectation no longer holds: pin the review to commit `2d6e3f9` of `progressive-ai-team-starter` or register a new case version.
