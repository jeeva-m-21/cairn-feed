# Cairn Agile Delivery Plan

## Method

Use Scrum-inspired Agile with one-week or two-week sprints, a prioritized product backlog, explicit sprint goal, daily engineering coordination, review/demo, and retrospective. TDD is mandatory inside every story.

## Backlog hierarchy

Product goal → release goal → epic → user story → acceptance criteria → tests → implementation tasks.

Stories must name actor, behavior, and value. Acceptance criteria use Given/When/Then and include failure/degraded behavior where relevant.

## Ceremonies

- Backlog refinement: clarify scope, dependencies, risk, and testability.
- Sprint planning: select one coherent vertical goal and reserve capacity for defects.
- Daily sync: progress, blockers, and integrity risks.
- Sprint review: demonstrate a real user flow using deterministic seeded/live-safe data.
- Retrospective: improve delivery, test quality, and product trust.

## WIP and change control

Limit active work. New scope enters the backlog unless it resolves a release-blocking defect or legal/security issue. Architecture changes require an ADR and impact review. Any requirement change updates SRS, traceability, tests, and sprint scope.

## Release gates

Gate A: documentation and contracts approved.
Gate B: core feed-to-brief vertical slice passes.
Gate C: evidence/legal/admin safeguards pass.
Gate D: production readiness, observability, rollback, and smoke tests pass.

## Agile metrics

Track cycle time, escaped defects, test coverage by behavior, failed deployment recovery time, story acceptance rate, cluster precision, citation coverage, brief latency, and cost per event. Do not optimize raw time-on-app.
