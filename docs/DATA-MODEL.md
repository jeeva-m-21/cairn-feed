# Cairn Data Model Baseline

## Relational entities

User, Session, UserInterest, UserBehavior, Source, SourceDocument, Entity, DocumentEntity, Event, EventSource, EventRelationship, Claim, Evidence, Benchmark, CairnRecord, CairnRecordVersion, Visualization, GeneratedBrief, Alert, SavedItem, Feedback, ReviewAction, AuditLog, JobRun.

## Required invariants

- Source license metadata is mandatory before enablement.
- Canonical source URL is unique per source.
- An event cannot publish without a confirmed or reviewed cluster state.
- A published claim has an evidence policy result.
- A Cairn Record version references the event version and evidence snapshot used to build it.
- Generated briefs reference a Cairn Record version; they do not own independent facts.
- Admin mutations create immutable audit records.
- User behavior and alerts are accessible only to their owner or authorized admin.

## Indexes

UserInterest by user/topic; SourceDocument by source/canonical URL/fetched time; Event by cluster state/importance/created time; Entity aliases using trigram/fuzzy index; Claim/Evidence by event and confidence; vector indexes for document/event embeddings; behavior by user/time with retention jobs.

## Retention

Raw source references and excerpts follow source policy and legal review. Behavior logs are bounded by a documented TTL. Audit logs are retained longer than behavior logs and are append-only. Deleted user data is removed or anonymized according to the deletion policy.
