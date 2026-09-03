# Cairn Engineering Documentation

Version: 1.0
Status: Baseline for implementation planning

## Authority order

1. Explicit product decisions made by the product owner
2. `SRS.md`
3. `HIGH-LEVEL-DESIGN.md` and `LOW-LEVEL-DESIGN.md`
4. ADRs and contracts
5. Sprint plan and development rules
6. Source code and tests

If documents conflict, stop implementation, record the decision, and update the affected documents before coding.

## Reading order

1. `SRS.md` — complete requirements and release scope
2. `HIGH-LEVEL-DESIGN.md` — system boundaries and architecture
3. `LOW-LEVEL-DESIGN.md` — modules, data, APIs, workflows, and states
4. `ARCHITECTURE-DECISION-RECORDS.md` — decisions and rejected alternatives
5. `API-CONTRACT.md` and `DATA-MODEL.md` — implementation contracts
6. `SECURITY-PRIVACY.md` and `OPERATIONS-DEPLOYMENT.md`
7. `DEVELOPMENT-RULES.md` and `TDD-STRATEGY.md`
8. `SPRINT-PLAN.md` and `AGILE-DELIVERY-PLAN.md`
9. `traceability/` — requirement coverage

## Current build gate

Documentation baseline is complete only when SRS requirements have design mappings, test strategy mappings, and a release target. No production implementation begins until the first sprint is explicitly selected and its acceptance criteria are understood.

## Product boundary

Cairn is a responsive web SaaS that discovers technical information from permitted sources, clusters documents into events, computes user relevance, and serves evidence-backed briefs. MVP proves the feed-to-brief loop before adding advanced intelligence, billing, teams, or native apps.
