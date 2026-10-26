# Intent-Driven Engineering — Claude Code Plugin Marketplace

Claude Code plugin marketplace for **Intent-Driven Engineering (IDE)**.

## Install

```text
/plugin marketplace add kendallmark3/intent-driven-engineering-plugin
/plugin install intent-driven-engineering@intent-driven-engineering-marketplace
```

## Plugins

| Plugin | Version | Skills |
|---|---|---|
| [`intent-driven-engineering`](plugins/intent-driven-engineering) | 1.0.0 | `intent-refiner`, `enterprise-radius-review`, `proof-case-study-builder` |

```text
ROUGH IDEA → intent-refiner → CLEAR INTENT → BUILD
  → enterprise-radius-review → GOVERNANCE CHECK
  → proof-case-study-builder → EVIDENCE + VALUE STORY
```

## Architecture

```mermaid
flowchart TB
    subgraph REPO["GitHub · kendallmark3/intent-driven-engineering-plugin"]
        direction TB
        MKT[".claude-plugin/marketplace.json<br/><i>intent-driven-engineering-marketplace</i>"]
        subgraph PLUGIN["plugins/intent-driven-engineering · v1.0.0"]
            direction TB
            PJ[".claude-plugin/plugin.json"]
            S1["skills/intent-refiner"]
            S2["skills/enterprise-radius-review"]
            S3["skills/proof-case-study-builder"]
        end
        MKT -->|source| PLUGIN
    end

    subgraph CC["Claude Code"]
        direction LR
        ADD["/plugin marketplace add"]
        INST["/plugin install"]
        LOAD["Skills loaded<br/>model-invoked by description"]
        ADD --> INST --> LOAD
    end

    REPO -.->|clone| ADD
    LOAD --> FLOW

    subgraph FLOW["Intent-Driven Engineering workflow"]
        direction TB
        IDEA(["Rough idea"]) --> R1["intent-refiner"]
        R1 --> INTENT(["Clear intent<br/>outcome · inputs · outputs<br/>success criteria · constraints · evidence"])
        INTENT --> BUILD(["Build / prototype"])
        BUILD --> R2["enterprise-radius-review"]
        R2 --> GOV(["Five-radius governance check"])
        GOV --> R3["proof-case-study-builder"]
        R3 --> PROOF(["Evidence + value story<br/>observed · measured · proposed"])
    end

    GATE{{"Governed learning<br/>correction → proposed delta → regression test → promote"}}
    R1 -.-> GATE
    R2 -.-> GATE
    R3 -.-> GATE

    classDef skill fill:#ffffff,stroke:#1d1d1f,stroke-width:1.5px,color:#1d1d1f
    classDef artifact fill:#f5f5f7,stroke:#d2d2d7,color:#1d1d1f
    classDef file fill:#ffffff,stroke:#86868b,color:#424245
    class R1,R2,R3 skill
    class IDEA,INTENT,BUILD,GOV,PROOF artifact
    class MKT,PJ,S1,S2,S3,ADD,INST,LOAD file
    classDef gate fill:#ffffff,stroke:#86868b,stroke-dasharray:4 3,color:#424245
    class GATE gate
    style REPO fill:#fbfbfd,stroke:#d2d2d7,color:#1d1d1f
    style PLUGIN fill:#ffffff,stroke:#d2d2d7,color:#1d1d1f
    style CC fill:#fbfbfd,stroke:#d2d2d7,color:#1d1d1f
    style FLOW fill:#fbfbfd,stroke:#d2d2d7,color:#1d1d1f
```

### Five-radius model (`enterprise-radius-review`)

```mermaid
flowchart LR
    R1["1 · Intent & Discovery"] --> R2["2 · Prototype & Proof"] --> R3["3 · Engineering & Integration"] --> R4["4 · Delivery & Production"] --> R5["5 · Enterprise Operation & Governance"]
    classDef r fill:#ffffff,stroke:#86868b,color:#1d1d1f
    class R1,R2,R3,R4,R5 r
```

## Local development

```bash
claude --plugin-dir ./plugins/intent-driven-engineering
```

See [plugins/intent-driven-engineering/README.md](plugins/intent-driven-engineering/README.md) for details.

---
Part of [LearnTeachMaster.org](https://learnteachmaster.org) · [intent-driven-engineering.com](https://intent-driven-engineering.com)
