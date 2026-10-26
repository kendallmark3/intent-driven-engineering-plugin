---
name: proof-case-study-builder
description: Turns completed technical work, prototypes, apps, workflows, repositories, or AI systems into evidence-based case studies. Use when the user says "turn this into a case study", "put this on Repogenic", "document what we built", "give me the proof", or wants architecture, technologies, screenshots, validation, lessons, and business value presented without inventing results.
version: 1.0.0
---

# Proof Case Study Builder

## Purpose

Convert real completed work into a credible case study that shows:

- the problem;
- the intent;
- what was built;
- why major choices were made;
- how the result was validated;
- what evidence exists;
- what business or operational value was demonstrated;
- what remains unproven.

This skill is evidence-first.

Do not write marketing claims that the available evidence cannot support.

## Evidence Classification

Classify material claims as:

### Observed
Directly seen in the implementation, repository, screenshots, logs, output, or working behavior.

### Measured
Supported by a count, metric, timing, evaluation, test result, comparison, or other quantified result.

### Proposed
A recommendation, expected benefit, next step, or hypothesis not yet proven.

Never convert **Proposed** into **Observed** or **Measured**.

If the user does not have evidence for a strong claim, weaken the claim or label it explicitly as proposed.

## Trigger

Use when the user asks:
- "Turn this into a case study."
- "Put this on Repogenic."
- "Document what we built."
- "Give me the proof."
- "Show the architecture and screenshots."
- "Write up this prototype."
- "Turn this project into a customer/client story."

## Do Not Trigger

Do not use for:
- an idea that has not been built unless the user explicitly wants a proposed case-study format;
- fictional performance claims;
- invented customer outcomes;
- generic product marketing with no implementation evidence.

## Process

### 1. Establish the problem

State:
- who had the problem;
- what was difficult, slow, risky, expensive, or unclear;
- what constraint made the problem worth solving.

Avoid inflated language.

### 2. State the intent

Summarize the intended outcome and key boundaries.

Keep the intent distinct from the architecture.

### 3. Inventory the evidence

Use only available artifacts such as:
- screenshots;
- repository files;
- running application behavior;
- tests;
- logs;
- evaluation output;
- architecture diagrams;
- API responses;
- deployment records;
- issue history;
- before/after comparisons;
- human review.

If evidence is missing, say so.

### 4. Describe what was built

Explain the actual system at the level necessary for the audience.

Distinguish:
- user experience;
- application components;
- AI/agent components;
- integrations;
- shared services;
- runtime/deployment;
- validation.

Do not add components simply to make the architecture look sophisticated.

### 5. Explain important technology choices

For every major technology named, answer:
- Why was it used?
- What requirement did it satisfy?
- What alternative complexity did it avoid?
- Was it required, selected for convenience, or inherited from the environment?

Do not create a technology laundry list.

### 6. Tie screenshots to claims

Every screenshot or diagram should prove or clarify something.

Suggested caption pattern:

**What this shows:** <observable behavior or architecture fact>  
**Why it matters:** <connection to the intent or evidence>

### 7. Explain validation

State:
- what was tested;
- how it was tested;
- what passed;
- what failed or changed;
- what remains untested.

A prototype can be successful without pretending it is production-ready.

### 8. State business value carefully

Use measured value when available.

When value is inferred rather than measured, label it accordingly.

Good:
- "The prototype reduced a five-step manual workflow to one guided review in the tested scenario."

Also acceptable:
- "If the same behavior holds in production, the approach could reduce manual review effort. Production measurement is still required."

Bad:
- "The solution will save millions" without evidence.

## Default Output Format

```markdown
# <Case Study Title>

## Executive Summary

## The Problem

## Intent

## Constraints

## What We Built

## Architecture

## Technologies Used

## Why These Technologies

## Evidence
### Screenshots
### Tests
### Metrics
### Other Proof

## Validation

## What Worked

## What Changed During Development

## Business / Operational Value

## Limitations and What Is Not Yet Proven

## Lessons Learned

## What We Would Do Next
```

## Optional Evidence Table

When useful:

| Claim | Type | Evidence | Confidence |
|---|---|---|---|
| ... | Observed / Measured / Proposed | ... | High / Medium / Low |

## Writing Style

- credible;
- specific;
- compact;
- technically literate;
- understandable to an executive;
- no hype;
- no invented metrics;
- no "AI-powered" filler unless AI is materially relevant;
- prefer proof over adjectives.

## Quality Rules

- Never invent a screenshot, test, customer result, metric, or deployment.
- Clearly label simulated or synthetic data.
- Explain why architectural choices mattered.
- Include limitations.
- Preserve failed experiments when they provide a useful engineering lesson.
- Distinguish prototype evidence from production evidence.
- Avoid implying enterprise readiness when only a POC was tested.
- Prefer "demonstrated" only when the evidence actually demonstrates the claim.

## Validation

Before finalizing, ask:
- Can every strong claim be traced to evidence?
- Are measured claims actually measured?
- Are proposed benefits labeled as proposed?
- Is the architecture the one that was built, not the one we wish had been built?
- Does each technology have a reason for being mentioned?
- Do screenshots have a purpose?
- Are limitations explicit?
- Is the business value understandable without exaggeration?

## Learning Rule

When the user corrects a case study, classify the correction before changing the skill itself.

Do not permanently encode:
- a one-off tone preference;
- a project-specific technology choice;
- a single customer's reporting format;
- a claim that was true only for one implementation.

Promote a correction into the skill only when it is reusable and survives regression testing against prior successful case studies.
