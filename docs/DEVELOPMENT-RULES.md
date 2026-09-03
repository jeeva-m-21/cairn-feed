# Cairn Development Rules

## Source of truth

Product owner decisions override all documents. SRS defines behavior. Architecture documents define boundaries. API/data contracts define interfaces. Tests are executable behavior contracts.

## TDD gate

No production code without a failing test first. For every behavior: RED (write one focused test and run it to confirm expected failure), GREEN (minimal implementation), REFACTOR (clean design with tests green), then full relevant suite. Test behavior, not private implementation. Mocks are permitted only at external boundaries.

## Agile rules

Work in short sprints. Each sprint must end with a user-providable feature, demo path, acceptance criteria, telemetry, and deferred scope. Do not create horizontal “backend first/frontend later” sprints for user-facing work.

## Quality gates

Before merge: focused tests, full suite, type/lint checks, migration checks, security checks, accessibility checks for UI, API contract compatibility, and review of requirement traceability. Before release: production-like smoke test, degraded-path test, observability check, rollback plan, and legal source check.

## Product integrity

Never bypass evidence gates, source licensing metadata, authorization, or audit records for speed. Never silently change published factual content. Never expose provider secrets or private behavior data. Do not add billing, teams, native mobile, broad crawling, or unrelated chat until explicitly approved.

## Engineering conventions

Use UTC timestamps, typed boundaries, stable error codes, idempotent jobs, opaque cursors, correlation IDs, and explicit state transitions. Prefer small modules with one responsibility. Keep provider-specific code behind adapters. Schema changes require reversible migrations.

## Definition of done

A story is done only when acceptance tests pass, error/loading/degraded/permission states exist, telemetry is emitted, docs/contracts are updated, security and accessibility are checked, and the feature is demonstrated through its intended user flow.
