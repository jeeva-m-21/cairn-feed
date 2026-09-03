# Cairn API Contract Baseline

## Rules

Base path `/v1`. JSON uses camelCase at the boundary and UTC ISO-8601 timestamps. All mutating endpoints require authentication except signup/login. Every response carries `requestId`; errors are stable and machine-readable.

## Resource contracts

`EventCard`: id, title, category, sourceCount, firstSeenAt, tags, relevanceReason, importanceScore, confidenceLabel, saved.

`Brief`: eventId, recordVersion, title, tldr, sections, claims, sourceCount, generatedAt, degraded.

`Claim`: id, text, confidenceLabel, evidenceCount, sourceIds.

`Profile`: experienceLevel, readingStyle, interests, facets.

## Pagination

Feed and search use opaque cursor pagination: `{items, nextCursor, hasMore}`. Clients must not infer cursor structure.

## Errors

`AUTH_REQUIRED`, `FORBIDDEN`, `NOT_FOUND`, `VALIDATION_ERROR`, `RATE_LIMITED`, `CONFLICT`, `DEPENDENCY_UNAVAILABLE`, `DEGRADED_CONTENT`, `INTERNAL_ERROR`.

## Compatibility

Additive fields are backward compatible. Breaking changes require a new version or migration period. API schema tests run in CI. SSE event names and payloads are versioned with the API.
