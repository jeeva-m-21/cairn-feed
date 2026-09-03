# Cairn Operations and Deployment Baseline

## Environments

Local uses Docker Compose and deterministic provider fixtures. Staging mirrors production topology with synthetic or permitted test sources. Production uses managed PostgreSQL/pgvector, Redis, object storage, web/API containers, worker autoscaling, and centralized observability.

## CI gates

Format/lint, type checks, unit/integration/contract tests, migration validation, dependency scan, secret scan, build, and smoke tests. Pull requests must include test evidence and traceability updates.

## Runtime health

Expose liveness and readiness separately. Readiness checks database and queue connectivity. Monitor API latency, error rate, cache hit rate, queue lag, job retries/dead letters, ingestion freshness, cluster review backlog, citation coverage, provider failures, cost, and alert delivery.

## Reliability

Use database backups and restore drills, Redis as disposable cache, object-store versioning, queue retries with dead letters, idempotency keys, circuit breakers for providers, and feature flags for risky connectors. Keep the last publishable Cairn Record available for degraded serving.

## Release and rollback

Deploy migrations backward-compatible first, then application, then cleanup migrations later. Roll back application independently where possible. Disable a connector or precompute feature via configuration without deleting evidence. Every release has a smoke test for onboarding → feed → brief → evidence.

## Legal operations

Maintain source approval records, terms snapshots, takedown/correction process, referral-link checks, and launch counsel sign-off. No source connector is enabled in production without approval metadata.
