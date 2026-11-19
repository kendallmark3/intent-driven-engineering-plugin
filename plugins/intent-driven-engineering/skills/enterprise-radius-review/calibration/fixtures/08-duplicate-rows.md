# Radius Review: duplicate Radius Summary rows

> Advisory review — not a security review, architecture approval, or production readiness sign-off.

## Scope & Method
- Unit rated: search agent
- Ran: unit tests
- Read: README.md, intent file, CI config

## Executive Finding
Synthetic validator fixture. Two rows for Radius 2 disagree.

## Current Credible Radius
Radius: 2
Ceiling: scope
Two rows for Radius 2 disagree.

## Radius Summary
| Radius | Status | Core evidence | Unknown material gap |
|---|---|---|---|
| 1 | Reached | Documented | No |
| 2 | Reached | Verified | No |
| 2 | Not reached | Unknown | Yes |
| 3 | N/A — no integrations intended | — | — |
| 4 | N/A — no integrations intended | — | — |
| 5 | N/A — no integrations intended | — | — |

## Authority & Autonomy
- Human: approves releases
- Agent: none
- System: CI tests

## Proof Required Before Expansion
- See ceiling explanation above.
