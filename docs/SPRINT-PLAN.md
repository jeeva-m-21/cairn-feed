# Cairn Sprint Plan

Assumption: two-week sprints. Each sprint has a user-visible outcome.

## Sprint 0 — Contracts and deployable shell

Feature: a visitor can open the Cairn shell and see the product direction; engineering can run the full stack locally.

Scope: repository setup, documentation contracts, Next.js/FastAPI/DB/Redis Compose baseline, design tokens, health endpoints, CI test gates.

Demo: run one command, open web shell, verify API health and database migration.

Acceptance: responsive shell renders; health checks pass; CI runs tests; no secrets committed.

Deferred: product flows.

## Sprint 1 — Seeded event feed

Feature: a reader can browse a useful event feed from deterministic seeded events.

Scope: event/read models, feed sections, cards, pagination, loading/empty/error states, seeded fixtures.

Demo: open Home, browse For You/Breaking/Research, inspect source count and relevance reason.

Acceptance: duplicate documents are represented by one event; skipped onboarding gets default feed; mobile and keyboard flows work.

Deferred: live ingestion and personalization learning.

## Sprint 2 — Onboarding and relevance

Feature: a reader can configure topics and experience level and receive a relevant feed.

Scope: auth/session baseline, onboarding flow, profile persistence, deterministic relevance scoring, score explanation.

Demo: create two profiles, configure different topics/levels, show different feed order and reasons.

Acceptance: explicit interests affect ranking; no profile leaks; profile failure has recoverable state.

Deferred: behavioral relearning.

## Sprint 3 — Live source ingestion

Feature: permitted sources can produce normalized documents through a repeatable pipeline.

Scope: source registry, RSS/official blog adapter, GitHub/arXiv/HN/HF adapters as individually testable connectors, idempotency, health.

Demo: fetch fixture/live-safe sources, show normalized documents and source health.

Acceptance: duplicate fetch is no-op; disabled source does not enqueue; failed source retries and reports degraded.

Deferred: broad web crawling and X.

## Sprint 4 — Clustering and review

Feature: related documents become one event; ambiguous clusters are reviewable.

Scope: embeddings interface, deterministic clustering signals, confidence thresholds, admin queue, merge/split/confirm, audit log.

Demo: ingest multiple launch reports, show one event; submit ambiguous set, merge/split in admin.

Acceptance: cluster decisions are explainable and idempotent; low confidence never auto-publishes.

Deferred: learned clustering.

## Sprint 5 — Evidence-backed brief

Feature: a reader opens an event and receives a cited brief with verified claims.

Scope: claim/evidence model, provider adapter fixtures, verification states, Cairn Record generation, citation UI, degraded cached path.

Demo: open event as Beginner and Expert; inspect different presentation with same evidence; force provider failure and show cached fallback.

Acceptance: unsupported claims are omitted/labeled; conflicts visible; evidence links resolve to source references.

Deferred: diagrams, benchmarks, Ask Mode.

## Sprint 6 — Progressive serving and quality operations

Feature: briefs render progressively and administrators can monitor quality.

Scope: SSE protocol, cache strategy, record versioning, source health, quality flags, latency/cost dashboards.

Demo: stream a brief, inspect request/job correlation, review flagged content.

Acceptance: latency budgets are measured; reconnect/stale version handling works; admin actions audited.

Deferred: billing and alerts.

## Sprint 7 — Saves, search, feedback, alerts

Feature: a reader can retain, find, evaluate, and receive important events.

Scope: saves, event search, feedback, alert configuration/merging, in-app/email delivery.

Demo: save event, search it, submit “too technical,” configure threshold, receive merged alert.

Acceptance: alert quiet hours work; related updates merge; user data isolated.

Deferred: advanced behavioral model.

## Sprint 8 — Production launch hardening

Feature: invited beta users can use Cairn reliably in production.

Scope: security review, privacy/export/delete, rate limits, backups, monitoring, runbooks, deployment, smoke tests, legal source review, support workflow.

Demo: deploy, onboard test account, use feed-to-brief flow, exercise degraded path and rollback procedure.

Acceptance: release gates A-D pass; no launch-blocking legal/security gaps; rollback is tested.

Deferred: P1/P2 expansion.

## Post-MVP

Benchmark intelligence, grounded diagrams, behavioral relearning, Ask Mode, Opportunity Intelligence, teams, billing, additional licensed sources, and native apps require separate approved release plans.
