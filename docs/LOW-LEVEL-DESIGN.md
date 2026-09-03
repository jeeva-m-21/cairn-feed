# Cairn Low-Level Design

## 1. Module contracts

### Identity
Inputs: login/signup/session commands. Outputs: authenticated principal and role claims. Invariants: password/session secrets are never logged; disabled users cannot create sessions.

### Source registry
`Source {id, name, kind, license_terms, credibility_tier, enabled, connector_config_ref}`. Only enabled and legally approved sources may enqueue ingestion.

### Ingestion
`fetch(source, cursor) -> RawDocument[]`; `normalize(raw) -> SourceDocument`; `dedupe(document) -> existing|new`. Idempotency key is `(source_id, canonical_url, content_hash)`.

### Clustering
`propose_cluster(document_id) -> ClusterDecision`; decision includes candidate event IDs, confidence, signals, and reason. Auto-confirm requires configured threshold; otherwise `needs_review`.

### Verification
`extract_claims(event_id) -> Claim[]`; `retrieve_evidence(claim_id) -> Evidence[]`; `verify(claim, evidence) -> ConfidenceLabel`. A claim cannot enter a publishable record without evidence policy evaluation.

### Cairn Record
`build_record(event_version) -> CairnRecordDraft`; `validate_record(draft) -> Publishable|Rejected`; `publish(record)`. Record is immutable by version; corrections create a new version.

### Personalization
`select_variant(record, profile) -> VariantSelection`; `assemble(selection, relevance_reason) -> Brief`. This service cannot invent factual claims or alter citation bindings.

## 2. Core state machines

Source: `pending -> enabled -> degraded -> disabled`.
Document: `discovered -> fetched -> normalized -> embedded -> clustered|rejected`.
Event: `candidate -> confirmed|needs_review -> published -> updated|superseded|archived`.
Claim: `extracted -> evidence_pending -> supported|confirmed|developing|conflicting|unverified|rejected`.
Record: `draft -> verifying -> publishable|blocked -> published -> superseded`.
Alert: `draft -> eligible -> queued -> sent|failed|suppressed`.

All transitions require an actor/job ID, timestamp, and structured reason.

## 3. Feed ranking

MVP score is deterministic and versioned:
`score = 0.30*personal_relevance + 0.25*global_importance + 0.20*novelty + 0.15*recency + 0.10*source_confidence`.

Apply topic eligibility, explicit-interest boost, diversity constraints, and section-specific weighting after the base score. Store score components for explainability and debugging. No learned ranker ships until behavioral data quality is validated.

## 4. API shape

Authentication: `POST /v1/auth/signup`, `POST /v1/auth/login`, `POST /v1/auth/logout`, `GET /v1/me`.
Profile: `GET/PATCH /v1/profile`, `PUT /v1/profile/interests`.
Feed: `GET /v1/feed?section=for_you&cursor=...`.
Events: `GET /v1/events/{event_id}`, `GET /v1/events/{event_id}/brief`, `GET /v1/events/{event_id}/brief/stream`.
Evidence: `GET /v1/claims/{claim_id}/evidence`.
Saved: `GET/PUT/DELETE /v1/saved/{event_id}`.
Feedback: `POST /v1/events/{event_id}/feedback`.
Admin: `GET /v1/admin/review-queue`, `POST /v1/admin/events/{id}/merge`, `/split`, `/confirm`, `GET /v1/admin/sources/health`, `POST /v1/admin/sources/{id}/disable`.

Every response includes request ID. Cursor pagination is opaque. API errors use `{code, message, request_id, details?}`.

## 5. Brief SSE protocol

Server sends ordered events: `brief.started`, `brief.header`, `brief.section`, `brief.citation_index`, `brief.completed`, or `brief.degraded`. Each event includes record version and request ID. Clients discard stale versions and reconnect with `Last-Event-ID` where supported.

## 6. Persistence rules

Use UUID primary keys, UTC timestamps, soft deletion for user-owned records, unique canonical URL constraints, JSONB only for provider-shaped specs, and relational columns for queryable facts. Store source text by reference with retention policy; do not reproduce disallowed content.

## 7. Jobs

`source.fetch`, `document.normalize`, `document.embed`, `event.cluster`, `event.review_notify`, `event.extract_claims`, `claim.verify`, `record.precompute`, `feed.project`, `alert.evaluate`, `alert.deliver`, `analytics.aggregate`.

Each job has job ID, idempotency key, attempt count, timeout, retry policy, dead-letter destination, and metrics.

## 8. Authorization

Reader may access own profile, behavior-derived feed, saves, alerts, feedback, and published events. Admin may access operational data and perform audited mutations. Source evidence is exposed only through citations attached to published records. Object-storage references use short-lived signed URLs where needed.

## 9. Frontend state requirements

Every feed and brief route implements loading, empty, error, degraded, success, disabled, and permission-denied states. Brief rendering treats SSE as incremental state, never as untrusted HTML. Keyboard focus moves to the brief heading after navigation; citation panels are keyboard reachable and closable.

## 10. Observability

Measure request latency, cache hit rate, queue lag, job retries, cluster confidence, duplicate/miscluster rate, citation coverage, verification labels, record publish blocks, provider cost, and brief completion. Correlate browser request → API request → job/record version.
