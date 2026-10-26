---
name: enterprise-radius-review
description: Reviews an AI system, architecture, repository, gateway, agentic workflow, platform capability, shared service, team boundary, or production proposal using a five-radius enterprise model. Use when the user asks where something belongs, who should own it, whether it is production-ready, how far a team's responsibility extends, what enterprise controls are missing, or requests a Radius Analysis.
version: 1.0.0
---

# Enterprise Radius Review

## Purpose

Determine how far a proposed or existing AI capability extends from business intent into enterprise operation, and expose what is present, missing, overbuilt, misplaced, or insufficiently evidenced.

Do not reward complexity. The preferred design is the **minimum sufficient architecture that safely achieves the intent**.

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

Use when the user asks:
- "Do a Radius Analysis."
- "Where does this belong?"
- "Who owns this?"
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

## Review Process

1. Restate the intended outcome in one or two sentences.
2. Determine the highest radius the current solution credibly reaches.
3. Evaluate every radius up to that point.
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

## Executive Finding
<Current radius, biggest strength, biggest gap, and recommended next move.>

## Current Credible Radius
<1-5 with explanation>

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

## Quality Rules

- Never equate more infrastructure with better architecture.
- Do not move a concern into a central platform merely because it could be centralized.
- Centralize capabilities that provide repeatable governance, interoperability, safety, or economic benefit.
- Keep domain decisions close to domain teams.
- Distinguish design claims from demonstrated evidence.
- Separate prototype success from production readiness.
- Make ownership explicit.
- Identify the exact control or evidence required before recommending broader autonomy.
- Do not invent enterprise policies that were not provided.

## Validation

Before finalizing, ask:
- Did the review identify the current credible radius?
- Did it distinguish missing capability from intentionally out-of-scope capability?
- Did it separate application, platform, and enterprise control responsibilities?
- Are human, agent, and system responsibilities clear?
- Are claims tied to evidence?
- Is the recommended next step smaller than "build the whole platform"?
- Would the proposed architecture still make sense if the AI buzzwords were removed?

## Learning Rule

Treat corrections as proposed deltas, not automatic changes.

A new Radius rule should be promoted only when it improves the failing case without degrading prior successful reviews or causing systematic over-centralization, over-governance, or architectural inflation.
