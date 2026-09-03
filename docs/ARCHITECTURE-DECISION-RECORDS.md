# Architecture Decision Records

## ADR-001: Modular monolith before service extraction
Status: Accepted.

Decision: Begin with a modular monolith and workers, with domain interfaces and queues.

Why: The product has many domains but one early team. Distributed services would add deployment, consistency, and debugging cost before scale proves the need. Boundaries still prevent a later extraction from becoming a rewrite.

Rejected: Full microservices now — too much operational surface; single unstructured application — poor ownership and testability.

## ADR-002: PostgreSQL plus pgvector
Status: Accepted.

Decision: PostgreSQL is the source of truth and pgvector is the initial similarity layer.

Why: Events, evidence, claims, users, and audit data need relational integrity. pgvector avoids a second operational database at MVP scale.

Rejected: Dedicated vector database immediately — defer until measured scale or query requirements justify it.

## ADR-003: Precompute canonical records
Status: Accepted.

Decision: Generate and verify event content in background; personalize by selecting cached variants at read time.

Why: Meets latency, cost, consistency, and citation requirements. Prevents per-read factual drift.

Rejected: Fresh article generation on every open — slow, expensive, and inconsistent.

## ADR-004: Evidence-first publication gate
Status: Accepted.

Decision: A claim without retrievable evidence cannot be shown as an unqualified fact.

Why: Trust is the product's differentiator. LLM self-review is not sufficient.

Rejected: Citation-only prompting without post-generation checks — inadequate control.

## ADR-005: SSE for progressive briefs
Status: Accepted.

Decision: Use Server-Sent Events for one-way incremental brief delivery.

Why: Simpler than WebSockets and sufficient for server-to-browser streaming.

Rejected: WebSockets — unnecessary bidirectional complexity for MVP.

## ADR-006: Deterministic MVP ranking
Status: Accepted.

Decision: Use a versioned weighted heuristic with stored score components.

Why: Explainable, testable, and useful before sufficient behavior data exists.

Rejected: Learned ranker at launch — cold-start, explainability, and data-quality risks.

## ADR-007: Permitted sources only
Status: Accepted.

Decision: MVP supports official/permissive and API-governed sources only; no paywalled scraping or full-text reproduction.

Why: Legal and trust constraints are launch blockers, not backlog polish.

Rejected: Broad web scraping — unacceptable legal and source-quality risk.

## ADR-008: TDD with vertical slices
Status: Accepted.

Decision: Every production behavior starts with a failing test and is delivered in a demonstrable vertical slice.

Why: The system has high integrity requirements and many interfaces; test-first contracts reduce integration drift.

Rejected: Test-after development — insufficient evidence of behavioral intent.
