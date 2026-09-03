# Cairn High-Level Design

## 1. Architecture style

Cairn uses a modular monolith with asynchronous workers. This keeps deployment and transactions simple for an early SaaS while enforcing boundaries that permit later extraction. Frontend and backend are separate deployable applications; the pipeline runs through durable jobs rather than request-bound orchestration.

## 2. Context

External systems: permitted source providers, LLM/embedding providers, email provider, object storage, payment provider later, observability platform.

Cairn systems: web client, public API, authenticated API, admin API, ingestion workers, intelligence workers, notification workers, PostgreSQL/pgvector, Redis, object storage.

## 3. Logical modules

1. Identity and access — sessions, roles, account lifecycle.
2. Profile and interest graph — explicit interests, inferred weights, experience/read style.
3. Source registry — license metadata, connector configuration, health.
4. Ingestion — polling, normalization, deduplication, retrieval references.
5. Event intelligence — entities, embeddings, clustering, event lifecycle.
6. Evidence — claims, evidence passages, entailment, confidence labels.
7. Cairn Records — canonical outline, variants, visual/benchmark specs, versioning.
8. Ranking — global importance, personal relevance, diversity, feed sections.
9. Serving — feed, brief assembly, SSE stream, degraded responses.
10. Admin operations — review queues, source health, quality flags, audit log.
11. Notifications — alerts, merge windows, delivery.
12. Analytics — product, quality, cost, latency events.

Each module owns its write models and exposes application services. Cross-module access uses typed interfaces or read projections, never direct arbitrary table mutation.

## 4. Primary data flow

Source adapter → raw document identity → normalized document → entity/embedding jobs → cluster candidate → confirmed event → claim extraction/evidence verification → Cairn Record version → feed projection → personalized brief assembly.

Read flow: authenticated request → authorization → cache/projection lookup → profile selection → record assembly → citations/evidence links → response or SSE events.

## 5. Deployment topology

Local: Docker Compose with web, API, worker, PostgreSQL, Redis, and object-storage emulator.

Production baseline: managed PostgreSQL with pgvector, managed Redis, object storage, containerized FastAPI/worker, Next.js deployment, managed email, and centralized logs/metrics.

## 6. Consistency and transactions

PostgreSQL is authoritative for user, event, evidence, entitlement, and audit state. Redis is disposable acceleration only. Job state is persisted and idempotency keys prevent duplicate effects. A record becomes publishable only after verification gates pass.

## 7. Failure strategy

- Provider timeout: retry with exponential backoff; use cached or prior version.
- Duplicate source document: idempotent no-op.
- Ambiguous cluster: hold for review.
- Verification failure: omit claim or mark developing/unverified.
- Record precompute failure: retain event card and source list; do not publish unverified prose.
- Database unavailable: fail closed for writes; return cached public/read content where safe.
- Notification failure: retry and expose delivery status to operations.

## 8. Security boundary

Public content is explicitly published only. Private profile, behavior, saves, alerts, and admin data require authorization. Admin endpoints require role checks plus audit logging. Provider secrets never reach the browser.

## 9. Scalability path

First scale workers horizontally. Add read replicas and partition behavior/analytics tables only when metrics justify them. Extract ingestion and intelligence services only when deployment cadence, queue volume, or team ownership requires it; preserve domain contracts.

## 10. Architecture quality attributes

Trust and provenance are prioritized over maximum coverage. Latency is achieved through precompute and projections. Operational simplicity is prioritized over premature distributed services. Every generated artifact is versioned against evidence and source snapshots.
