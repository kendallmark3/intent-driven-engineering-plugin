# Intent-Driven Engineering Plugin

Version 1.0.0

This Claude Code plugin packages three reusable skills:

1. `intent-refiner`
2. `enterprise-radius-review`
3. `proof-case-study-builder`

Together they form a practical chain:

```text
ROUGH IDEA
   ↓
intent-refiner
   ↓
CLEAR INTENT
   ↓
BUILD / PROTOTYPE / IMPLEMENT
   ↓
enterprise-radius-review
   ↓
ENTERPRISE DELIVERY + GOVERNANCE CHECK
   ↓
proof-case-study-builder
   ↓
EVIDENCE + VALUE STORY
```

## Skills

### intent-refiner

Use for:
- "Give me the intent."
- "Turn this into an intent file."
- "Clean up this requirement."
- "Give Claude/Copilot this feature."

Produces:
- Outcome
- Inputs
- Outputs
- Success Criteria
- Constraints and Boundaries
- Evidence

### enterprise-radius-review

Use for:
- "Do a Radius Analysis."
- "Where does this belong?"
- "Who owns this?"
- "Is this ready for production?"
- "What is missing from this architecture?"

Reviews:
1. Intent & Discovery
2. Prototype & Proof
3. Engineering & Integration
4. Delivery & Production
5. Enterprise Operation & Governance

### proof-case-study-builder

Use for:
- "Turn this into a case study."
- "Put this on Repogenic."
- "Document what we built."
- "Give me the proof."

Separates claims into:
- Observed
- Measured
- Proposed

and never invents proof.

## Local Development

From the directory containing this plugin:

```bash
claude --plugin-dir ./intent-driven-engineering
```

If this plugin is inside a marketplace repo at `plugins/intent-driven-engineering`, point `--plugin-dir` to that folder.

## Marketplace Installation

For a repository containing `.claude-plugin/marketplace.json`:

```text
/plugin marketplace add <github-owner>/<repo>
```

Then install:

```text
/plugin install intent-driven-engineering@intent-driven-engineering-marketplace
```

The exact marketplace name comes from the root `.claude-plugin/marketplace.json`.

## Natural Invocation

The skills are model-invoked from their descriptions. You can simply ask:

```text
Use the intent refiner on this feature...
```

```text
Do a Radius Analysis on this architecture...
```

```text
Turn this completed project into an evidence-based case study...
```

## Governance Rule

Corrections do not automatically rewrite these skills.

A correction is evidence. A reusable correction becomes a proposed skill delta, is tested against the failing case and prior successful cases, and is promoted only when it improves the skill without breaking established behavior.

## Repository Structure

```text
plugins/intent-driven-engineering/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   ├── intent-refiner/
│   │   └── SKILL.md
│   ├── enterprise-radius-review/
│   │   └── SKILL.md
│   └── proof-case-study-builder/
│       └── SKILL.md
└── README.md
```
