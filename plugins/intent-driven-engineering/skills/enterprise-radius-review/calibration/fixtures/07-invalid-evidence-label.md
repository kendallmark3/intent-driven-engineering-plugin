# Radius Review: invalid evidence classification

> Advisory review — not a security review, architecture approval, or production readiness sign-off.

## Scope & Method
- Unit rated: report generator
- Ran: unit tests
- Read: README.md, intent file, CI config

## Executive Finding
Synthetic validator fixture. Labels outside the four evidence levels.

## Current Credible Radius
Radius: 2
Ceiling: Radius 3
Labels outside the four evidence levels.

## Radius Summary
| Radius | Status | Core evidence | Unknown material gap |
|---|---|---|---|
| 1 | Reached | Documented | No |
| 2 | Reached | Tested | No |
| 3 | Not reached | Verifiedish | Yes |
| 4 | N/A — no deployment intended | — | — |
| 5 | N/A — no deployment intended | — | — |

## Authority & Autonomy
- Human: approves releases
- Agent: none
- System: CI tests

## Proof Required Before Expansion
- See ceiling explanation above.
