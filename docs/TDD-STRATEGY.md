# Cairn TDD Strategy

## Test pyramid

- Domain unit tests: ranking, confidence labels, state transitions, clustering signals, policy gates.
- Application integration tests: use cases with real database containers or test database, queue adapters, and transaction boundaries.
- Contract tests: API schemas, SSE event shapes, provider adapters, source normalization.
- End-to-end tests: onboarding → feed → event → brief → evidence; admin review; degraded brief.
- Non-functional tests: latency budgets, idempotency, authorization, accessibility, source policy.

## Vertical TDD cycle

1. Select one acceptance criterion from the sprint.
2. Write the smallest failing test at the correct boundary.
3. Run it and verify it fails for the missing behavior.
4. Implement the smallest production change.
5. Run the focused test, then the relevant suite.
6. Refactor only while green.
7. Add the next behavior.

## Required first tests for MVP

- Skipped onboarding returns default feed.
- Twenty documents for one launch create one confirmed event.
- Low-confidence cluster enters review queue.
- Unsupported claim is omitted or labeled.
- Same Cairn Record version serves Beginner and Expert variants.
- Evidence panel returns the exact source reference for a claim.
- Personalization/provider failure returns cached TL;DR and sources.
- Reader cannot access another reader's behavior or alerts.
- Admin merge/split actions create audit records.
- Duplicate ingestion is idempotent.

## Test data

Use deterministic fixtures for sources, documents, entities, events, claims, evidence, profiles, and provider responses. Include conflicting sources, missing evidence, duplicate URLs, stale documents, disabled sources, malformed provider output, and timeout/retry cases.

## Test naming and review

Names state behavior and outcome. Tests must not depend on wall-clock timing, network availability, or provider nondeterminism. External providers use recorded contract fixtures and a small live smoke suite only where credentials and cost are controlled.

## Evidence required in pull requests

Focused RED output, focused GREEN output, full suite output, migration/schema result, and any browser or API smoke result. A passing test written after implementation is not evidence of TDD compliance.
