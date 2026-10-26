---
name: intent-refiner
description: Refines rough requests, ideas, feature requests, problem statements, or implementation-heavy specifications into concise Intent-Driven Engineering intent. Use when the user asks for an intent file, says "give me the intent", "turn this into an intent", "clean up this requirement", "give Claude/Copilot this feature", or wants the outcome, inputs, outputs, success criteria, constraints, and evidence clarified without unnecessary implementation prescription.
version: 1.0.0
---

# Intent Refiner

## Purpose

Turn an informal request into a concise, testable intent that tells an AI engineer or software team **what must become true** without unnecessarily prescribing **how to make it true**.

The goal is minimum sufficient constraint.

Preserve real business, security, regulatory, integration, platform, and technology constraints. Remove implementation choices that are merely assumptions.

## Core Model

Every intent must make these elements clear:

1. **Outcome** — the result that matters.
2. **Inputs** — authoritative information, files, events, interfaces, or user actions available to the work.
3. **Outputs** — observable artifacts, behaviors, decisions, records, or responses that must be produced.
4. **Success Criteria** — how a human or deterministic system can determine whether the outcome was achieved.
5. **Constraints and Boundaries** — what must or must not happen.
6. **Evidence** — what proves the result is real.

## Trigger

Use this skill when the user:
- asks for an intent, intent file, feature intent, or IDE version of a requirement;
- describes something they want to build and wants it handed to Claude Code, Copilot, Cursor, another coding agent, or a team;
- provides a verbose or prescriptive requirement that should be simplified;
- asks to separate the outcome from implementation details;
- wants a durable requirement rather than a one-off prompt.

## Do Not Trigger

Do not use this skill merely because the conversation is technical.

Do not use it when:
- the user explicitly asks for code and the requirement is already sufficiently defined;
- the user asks for a narrow factual explanation;
- the user is brainstorming and does not yet want a committed intent;
- a prescribed technology is a genuine non-negotiable requirement and the task is only to configure or use it.

## Process

### 1. Extract the real outcome

Find the business or user result behind the request.

Prefer:
- "A reviewer can determine whether the evidence package is ready for human review."

Over:
- "Build a FastAPI endpoint using Bedrock and DynamoDB."

The second statement may describe an implementation. It is not the outcome unless those technologies are mandatory constraints.

### 2. Identify authoritative inputs

State what the implementation is allowed to rely on.

Examples:
- uploaded documents;
- repository contents;
- an existing API contract;
- user-selected records;
- a database schema;
- an enterprise policy;
- a ticket or design artifact.

Do not invent sources.

### 3. Define observable outputs

Outputs must be inspectable.

Examples:
- a generated report;
- a status decision;
- a changed file;
- an API response;
- an evidence record;
- a UI state;
- a pull request.

Avoid vague outputs such as "improved experience" without observable behavior.

### 4. Write success criteria

Success criteria must be testable or observable.

Good:
- "All required source documents appear in the evidence summary."
- "A missing required document produces an explicit incomplete status."
- "No external action occurs without human approval."

Weak:
- "The experience feels intelligent."
- "The system works well."

### 5. Separate constraints from preferences

Keep a technical choice only when it is truly required.

Possible legitimate constraints:
- must run in the existing AWS account;
- must integrate with a named enterprise API;
- must use an approved model gateway;
- must not persist PHI;
- must remain phone-only for V1;
- must satisfy a specific latency or regulatory requirement.

Remove speculative prescription such as:
- language choice;
- framework;
- database;
- orchestration library;
- cloud service;
- testing framework;
- hosting design.

unless the user made it a genuine requirement.

### 6. Define evidence

Ask what will prove success.

Evidence can include:
- deterministic tests;
- screenshots;
- logs;
- metrics;
- generated artifacts;
- status codes;
- before/after comparison;
- human review;
- trace records;
- acceptance checks.

Evidence should correspond directly to success criteria.

## Output Format

Use this exact default structure:

```markdown
# Intent: <concise name>

## Outcome
<What must become true and why it matters.>

## Inputs
- ...

## Outputs
- ...

## Success Criteria
- ...

## Constraints and Boundaries
- ...

## Evidence
- ...
```

Add an **Open Questions** section only when a missing answer materially blocks implementation or verification. Do not add questions merely to make the document look complete.

## Quality Rules

- Prefer one clear outcome over a collection of implementation tasks.
- Do not invent user rules.
- Do not invent architecture.
- Do not prescribe agent reasoning steps unless the sequence itself is a requirement.
- Preserve human authority boundaries.
- Prefer deterministic verification where the result can be deterministically checked.
- Keep V1 smaller than the user's eventual vision when the request is explicitly for an MVP.
- Never turn optional future ideas into current requirements.
- Do not use fashionable terminology unless it improves precision.

## Validation

Before finalizing, verify:

- Is the outcome obvious?
- Are inputs authoritative and available?
- Are outputs observable?
- Can each success criterion be checked?
- Are constraints genuine?
- Did unnecessary implementation prescription slip in?
- Is the human/agent boundary clear where relevant?
- Does the evidence prove the success criteria?

If any answer is no, refine before returning the intent.

## Learning Rule

When the user corrects the intent, treat the correction as evidence.

Classify the correction:
- **Reusable** — potentially valid for future intents.
- **Context-specific** — relevant only to this class of work.
- **One-off** — do not generalize.
- **Unclear** — needs more evidence.

Do not silently convert a single correction into a permanent skill rule.

A reusable change should become a proposed skill delta and should be tested against both the failing case and prior successful cases before promotion.
