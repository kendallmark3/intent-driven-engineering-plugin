---
name: enterprise-radius-review
description: Advisory, evidence-labelled review of an AI system, architecture, repository, gateway, agentic workflow, platform capability, shared service, or production proposal using a five-radius enterprise model. Use when the user requests a Radius Review/Analysis, asks whether a system is production-ready, where a capability or platform belongs, how far a team's responsibility extends, or what enterprise controls are missing. For a narrow ownership or placement question, answer briefly and offer the full review.
version: 1.4.0
---

# Enterprise Radius Review

## Purpose

Determine how far a proposed or existing AI capability extends from business intent into enterprise operation, and expose what is present, missing, overbuilt, misplaced, or insufficiently evidenced.

Do not reward complexity. The preferred design is the **minimum sufficient architecture that safely achieves the intent**.

**Advisory only.** A Radius Review is an architecture judgment, not a certification. It does not replace a security review, architecture approval, validation/quality sign-off, or operational readiness approval. State this in every review.

## The Five Radii

### Radius 1 — Intent & Discovery

Ask:
- What problem is being solved?
- Who receives value?
- What outcome matters?
- What are the success criteria?
- What authority and constraints apply?
- Why is AI or agentic behavior needed at all?

Evidence examples:
- problem statement;
- intent;
- baseline;
- measurable success criteria;
- identified owners.

### Radius 2 — Prototype & Proof

Ask:
- Can the concept work?
- What must be demonstrated before investment expands?
- Which model, agent, MCP server, workflow, API, or prototype capability is actually necessary?
- What evidence distinguishes a demo from a credible proof?

Evidence examples:
- working prototype;
- evaluation results;
- example traces;
- acceptance results;
- failure cases;
- human review results.

### Radius 3 — Engineering & Integration

Ask:
- How does the capability integrate with enterprise systems?
- What APIs, services, repositories, data contracts, identities, and dependencies are involved?
- Where does reusable capability belong?
- Which parts are application-specific versus shared?

Typical concerns:
- service boundaries;
- APIs and events;
- repositories;
- data contracts;
- MCP/tool adapters;
- reusable skills;
- dependency ownership;
- testability.

### Radius 4 — Delivery & Production

Ask:
- Can the capability be deployed, operated, observed, secured, rolled back, and supported?
- What happens when dependencies fail?
- How are secrets, identity, networking, environments, release controls, and observability handled?

Typical concerns:
- CI/CD;
- environments;
- cloud runtime;
- IAM;
- secrets;
- networking;
- logging;
- metrics;
- traces;
- reliability;
- rollback;
- incident handling;
- support ownership.

### Radius 5 — Enterprise Operation & Governance

Ask:
- Can the enterprise safely reuse, govern, audit, fund, measure, and evolve the capability?
- Which controls are centralized?
- Which decisions remain with teams?
- How is value proven over time?

Typical concerns:
- model catalog;
- AI gateway;
- capability/tool registry;
- MCP governance;
- policy enforcement;
- audit evidence;
- DLP;
- cost governance;
- change control;
- kill switch;
- reusable shared services;
- enterprise evaluation standards;
- ownership and support;
- measurable business value.

## Additional Lenses

Apply these across all five radii.

### Intent → Authority → Capability → Execution → Evidence → Value

For each stage ask:
- Is the intent clear?
- Who or what has authority?
- What capability is needed?
- Where is execution performed?
- What evidence is produced?
- What business or operational value is demonstrated?

### Human / Agent / System

Separate responsibilities:

**Humans**
- declare outcomes;
- establish boundaries;
- approve consequential actions;
- own business judgment.

**Agents**
- reason;
- explore;
- plan;
- synthesize;
- choose among permitted capabilities.

**Systems**
- enforce deterministic controls;
- validate schemas and policies;
- run tests;
- record evidence;
- block disallowed actions.

Do not make the agent responsible for deterministic enforcement when a system control can do it reliably.

## Trigger

Run the full review only when the user explicitly asks for a Radius Review/Analysis or asks an architecture-readiness question about a system as a whole. For a narrow ownership or placement question, answer it directly using the radius vocabulary and offer the full review instead of running it.

Full-review triggers:
- "Do a Radius Analysis."
- "Where does this belong?"
- "Who owns this capability/platform?"
- "Is this platform or application?"
- "Is this ready for production?"
- "Where should the MCP servers live?"
- "What is missing from this architecture?"
- "How far should this team own?"
- "Review this repo/gateway/agent/platform architecture."

## Do Not Trigger

Do not perform the full review for:
- a tiny code fix;
- a narrow syntax question;
- a trivial local script with no enterprise implications;
- an architecture discussion where the user explicitly wants only one isolated component answered.

## Execution Safety

By default a Radius Review reads; it does not execute. It must not require unrestricted code execution, automatic dependency installation, sending proprietary repository content to an external service, modifying the reviewed repository, elevated permissions, or cloud infrastructure.

- Running a reviewed repository's tests, builds, scripts, or evals executes code that repository controls. On an unfamiliar or untrusted repository, ask before running anything, and prefer a scratch copy so tracked files are not changed.
- If nothing was run, say so in Scope & Method (`Ran: nothing executed`) and do not label anything **Verified** that you only read.
- `scripts/check_review.py` uses only the Python standard library, reads the review file it is given, runs nothing from the reviewed repository, and makes no network calls. It writes only when `--log` is passed.

## Review Process

0. **Set scope.** Name the unit being rated (one capability, agent, or service). If the subject is a platform containing parts at different maturity, rate each part separately or pick one and say which; never give one radius to a mixed portfolio.
0a. **Set depth.** Small or single-component subject → use the Short Form. Otherwise use the Full Form.
1. Restate the intended outcome in one or two sentences.
2. Evaluate each radius and label every material claim with an evidence level:
   - **Verified** — the reviewer ran or observed it (tests, evals, live telemetry, deployed config).
   - **Documented** — stated in repo docs, configs, or diagrams, not independently checked.
   - **Reported** — asserted by a person or ticket, no artifact.
   - **Unknown** — no evidence found.
   Cite the source for each when one exists: a file path, commit, config file, test or eval run, deployment artifact, telemetry query, architecture decision, or the person who provided it. A reference shows where a claim comes from; it does not prove the claim. Never promote **Documented** to **Verified** without having run or directly observed it.
3. Determine the current credible radius using the **ceiling rule**:
   - A radius is **reached** only if its core claims are at least **Documented** and it has no material gap at **Unknown**.
   - The current credible radius is the highest radius N such that radii 1 through N are all reached. The first radius that is not reached sets the ceiling; name it.
   - A radius with partial evidence but an Unknown material gap is not reached. Report this as "Radius N, approaching N+1" — never round up.
   - If no radius is reached, the current credible radius is 0 (intent not yet established).
   - If the score rests mainly on Documented evidence, say so in the Executive Finding.
3a. **Explain the gap that sets the ceiling** (and any other material gap): what capability or evidence is missing, why it matters to the intended outcome, which radius it affects, what evidence would resolve it, and whether it is genuinely needed for the intended scope. A concern the intent does not need is out of scope, not a gap.
4. Identify claimed radii that lack evidence.
5. Separate application responsibilities from shared platform responsibilities.
6. Identify authority and autonomy boundaries.
7. Identify missing deterministic controls.
8. Identify reusable capabilities that belong in shared services or a registry.
9. Identify the smallest next step needed to move outward one radius.
10. State what proof is required before expanding further.

## Output Format

```markdown
# Radius Review: <subject>

> Advisory review — not a security review, architecture approval, or production readiness sign-off.

## Scope & Method
- Unit rated: <capability/agent/service>
- Ran: <tests, evals, commands actually executed — or "nothing executed">
- Read: <docs, configs, code inspected>

## Executive Finding
<Current radius, biggest strength, biggest gap, and recommended next move. Label the overall radius as a judgment.>

## Current Credible Radius
Radius: <0-5> (approaching <N+1>, if applicable)
Ceiling: <Radius M | scope | none>
<Why that radius set the ceiling, and the dominant evidence level behind the score.>

## Radius Summary
| Radius | Status | Core evidence | Unknown material gap |
|---|---|---|---|
| 1 | <Reached / Not reached / N/A — reason> | <Verified / Documented / Reported / Unknown> | <Yes / No> |
| 2 | ... | ... | ... |
| 3 | ... | ... | ... |
| 4 | ... | ... | ... |
| 5 | ... | ... | ... |

## Radius 1 — Intent & Discovery
### Present
- ...
### Missing
- ...
### Evidence
- ...

## Radius 2 — Prototype & Proof
...

## Radius 3 — Engineering & Integration
...

## Radius 4 — Delivery & Production
...

## Radius 5 — Enterprise Operation & Governance
...

## Authority & Autonomy
- Human:
- Agent:
- System:

## Shared vs Team-Owned Capabilities
### Shared / Platform
- ...
### Team / Application
- ...

## Missing Evidence
- ...

## Major Risks
- ...

## Recommended Next Radius
- ...

## Proof Required Before Expansion
- ...
```

For radii beyond the intended scope, state **Not required for current intent** rather than treating absence as a defect.

### Short Form

For small systems or single components, use only: Advisory line, Scope & Method, Executive Finding, a five-row table (Radius | Present | Evidence level + source | Gap), Authority & Autonomy, Proof Required Before Expansion. Mark out-of-scope radii **N/A**. Always include Current Credible Radius and Radius Summary, in both forms.

In the Radius Summary: **Reached** needs core evidence Verified or Documented and no Unknown material gap; otherwise **Not reached**. Unknown core evidence is itself an Unknown material gap. Keep exactly one row per radius. `Ceiling` is the first radius that is not Reached, `scope` if that radius is N/A, or `none` if all five are Reached.

Scope exclusions (**N/A**):
- Use N/A only for radii genuinely outside the intended scope, written `N/A — <reason>` with "—" in the other cells.
- An applicable capability that is absent or unproven is **Not reached**, never N/A. N/A cannot carry evidence or an Unknown gap.
- Radius 1 is never N/A. Exclusions are the outermost radii only: once a radius is N/A, every radius above it is N/A.

## Quality Rules

- Never equate more infrastructure with better architecture.
- Do not move a concern into a central platform merely because it could be centralized.
- Centralize capabilities that provide repeatable governance, interoperability, safety, or economic benefit.
- Keep domain decisions close to domain teams.
- Distinguish design claims from demonstrated evidence; every material claim carries an evidence label and source.
- Apply the ceiling rule: never score an outer radius while an inner radius has an Unknown material gap.
- Never give a single radius to a portfolio of capabilities at different maturity.
- Separate prototype success from production readiness.
- Make ownership explicit.
- Identify the exact control or evidence required before recommending broader autonomy.
- Do not invent enterprise policies that were not provided.

## Validation

Before finalizing, ask:
- Did the review state its scope and what it actually ran versus only read?
- Did the review identify the current credible radius, and does it respect the ceiling rule?
- If you can run Python 3, save the review to a file and run `python3 scripts/check_review.py <review-file>` from this skill's directory. Fix every FAIL before finalizing and resolve or explain every WARN. The script checks the structure, the labels, the scope rules, and recomputes the radius and ceiling from the Radius Summary. It does not judge whether an evidence label is right, whether a gap is material, or whether an exclusion is justified on the merits — that stays with you and the human reviewer. If Python is unavailable, apply the same checks by hand.
- Would a second run on the same evidence give the same radius and the same ceiling? If the score depends on a judgment call (for example, whether a gap is material), name that call explicitly.
- Does it include the advisory statement?
- Did it distinguish missing capability from intentionally out-of-scope capability?
- Did it separate application, platform, and enterprise control responsibilities?
- Are human, agent, and system responsibilities clear?
- Are claims tied to evidence?
- Is the recommended next step smaller than "build the whole platform"?
- Would the proposed architecture still make sense if the AI buzzwords were removed?

## Learning Rule

Treat corrections as proposed deltas, not automatic changes.

A new Radius rule should be promoted only when it improves the failing case without degrading prior successful reviews or causing systematic over-centralization, over-governance, or architectural inflation.

### Calibration Set

Keep at least three reference cases with expected outcomes, and re-run them before promoting any rule change:
1. **Small prototype** — expected: Radius 1–2, Short Form, outer radii N/A, no recommendation to build platform infrastructure.
2. **Production service with real telemetry and evals** — expected: Radius 4, mostly Verified evidence, specific Radius 5 gaps.
3. **Well-documented system with thin evidence** — expected: score capped by the ceiling rule, finding states the score rests on Documented evidence.

Add each real correction as a new case.

Case files, the pre-registration template, and the run log live in `calibration/` next to this file. Write a case's expected outcome **before** running the review on it, and do not edit it afterward to fit the result.
