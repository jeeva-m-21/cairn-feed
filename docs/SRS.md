# Cairn Software Requirements Specification

Version: 1.0 | Status: Baseline | Date: September 2026

## 1. Purpose and scope

Cairn is a personal intelligence platform for AI and developer technology professionals. It turns permitted source documents into clustered events, ranks events for each user, and serves a concise cited brief from a precomputed canonical Cairn Record.

The SRS records the complete product requirement set from the PRD. Release targets prevent later-phase requirements from entering MVP accidentally.

Release labels: MVP/P0, P1/Phase 2, P2/Phase 3+, Legal/Launch prerequisite, OOS/explicitly out of scope.

## 2. Users and roles

- Reader: authenticated user who configures interests, reads events and briefs, saves content, and submits feedback.
- Anonymous visitor: may view public marketing and explicitly published public event pages only; no private personalization.
- Administrator/curator: manages sources, reviews clusters, reviews quality flags, and audits evidence.
- System worker: executes ingestion, clustering, verification, precompute, ranking, and alert jobs; never acts outside a defined job contract.

## 3. Product principles

REQ-P-001 Events, not articles, are the primary product unit. MVP.
REQ-P-002 Hard work is precomputed once; read-time personalization assembles cached verified variants. MVP.
REQ-P-003 Every non-trivial factual claim must have retrievable evidence. MVP.
REQ-P-004 Global importance and personal relevance are separate values. MVP.
REQ-P-005 Density and useful information per minute outrank engagement time. All releases.
REQ-P-006 Uncertainty and source disagreement are visible. MVP.
REQ-P-007 Functional UI labels remain literal: Feed, Brief, Alert, Search, Saved. MVP.

## 4. Functional requirements

### Onboarding and profile

REQ-ONB-001 The reader shall select topics from a curated topic tree. MVP.
REQ-ONB-002 The reader shall select experience level: Beginner, Intermediate, Advanced, Expert. MVP.
REQ-ONB-003 The reader shall select a default reading style: summary, briefing, or deep dive. MVP.
REQ-ONB-004 The reader shall select interest facets: Research, Coding, Product, Business, Career, Hackathons. MVP; Hackathons affect ranking only until Opportunity Intelligence.
REQ-ONB-005 A reader who skips onboarding shall receive a non-empty AI and Developer Tools default feed. MVP.
REQ-ONB-006 A completed profile shall produce at least eight matching recent events when the precomputed catalogue contains enough data. MVP.

### Feed and discovery

REQ-FED-001 The feed shall display event cards rather than duplicate source articles. MVP.
REQ-FED-002 A card shall show event title, source count, first-seen time, category tags, signal chips, relevance reason, and Read brief CTA. MVP.
REQ-FED-003 The feed shall provide For You, Breaking, Deep Dive, and Research sections. MVP.
REQ-FED-004 The feed shall rank by transparent MVP heuristic combining global importance, personal relevance, novelty, recency, and diversity. MVP.
REQ-FED-005 Explicit interests shall remain distinguishable from inferred interests. MVP.
REQ-FED-006 Reading behavior shall influence ranking within a session when enough signals exist. MVP; sustained relearning P1.
REQ-FED-007 Twenty source documents covering one event shall render as one event card with source count. MVP.
REQ-FED-008 Search shall support event/entity/topic queries and URL-addressable filters. P1.
REQ-FED-009 Readers shall save events. P1.

### Briefs and evidence

REQ-BRF-001 Opening an event shall serve a personalized brief from the same Cairn Record for all readers. MVP.
REQ-BRF-002 Briefs shall progressively render title/relevance reason, TL;DR, primary content, and optional visuals. MVP.
REQ-BRF-003 Depth, terminology, section order, and framing shall adapt to the reader profile without changing verified facts. MVP.
REQ-BRF-004 Standard sections shall include TL;DR, What Happened, Why It Matters, What to Watch, and Sources where applicable. MVP.
REQ-BRF-005 Claims shall expose supporting source documents and evidence passages. MVP.
REQ-BRF-006 Claims shall carry Confirmed, Supported, Developing, Conflicting, or Unverified status. MVP.
REQ-BRF-007 Conflicting sources shall show both positions and must not be silently resolved. MVP.
REQ-BRF-008 Unsupported high-impact facts shall be omitted or explicitly labeled, never presented as verified. MVP.
REQ-BRF-009 A degraded service path shall still show the cached TL;DR and source list. MVP.
REQ-BRF-010 Readers shall be able to view the original source. MVP.
REQ-BRF-011 Explain-term, simplify, go deeper, evidence expansion, and follow-up interactions shall reuse the Cairn Record where possible. P1.
REQ-BRF-012 Benchmark tables shall use structured benchmark records and flag non-comparable evaluation conditions. P1.
REQ-BRF-013 Grounded architecture/process diagrams shall render only when supported by structured verified data. P1.
REQ-BRF-014 Reading mode shall be opt-in. P2.

### Ingestion, clustering, and verification

REQ-ING-001 MVP shall ingest permitted RSS/official blogs, Hacker News, GitHub releases, arXiv, and Hugging Face sources. MVP.
REQ-ING-002 Every source shall have license/terms metadata and an ingestion status. Legal prerequisite.
REQ-ING-003 Ingestion shall be idempotent by canonical URL/source identity. MVP.
REQ-ING-004 Normalization shall retain source identity, timestamps, title, URL, excerpt/reference, entities, and retrieval metadata. MVP.
REQ-ING-005 Clustering shall use semantic similarity, entity overlap, temporal proximity, and source relationships. MVP.
REQ-ING-006 Low-confidence cluster decisions shall enter administrator review rather than auto-publish. MVP.
REQ-ING-007 Administrators shall merge, split, confirm, and reject clusters with audit records. MVP.
REQ-ING-008 Users shall be able to flag that documents are not the same story. P1.
REQ-ING-009 Claims shall be checked against retrieved source passages using entailment/contradiction analysis. MVP.
REQ-ING-010 A source can be disabled without deleting historical evidence. MVP.
REQ-ING-011 X/Twitter, paywalled scraping, disallowed robots/ToS sources, and full-text reproduction are excluded from MVP. OOS.

### Alerts and feedback

REQ-ALT-001 Readers shall configure topic filters, importance threshold, quiet hours, and channels. P1.
REQ-ALT-002 Related updates shall merge into one alert. P1.
REQ-ALT-003 Alert channels shall include in-app and email for the first alert release. P1/Phase 2.
REQ-FBK-001 Readers shall submit useful, not useful, incorrect, too long, or too technical feedback. P1.
REQ-FBK-002 Administrators shall review quality flags with the Cairn Record and evidence chain. P1/Phase 2.
REQ-FBK-003 Behavioral feedback shall update inferred interest weights without overriding explicit selections. P1.

### Admin and operations

REQ-ADM-001 Administrators shall access a cluster review queue. MVP.
REQ-ADM-002 Administrators shall see source health, fetch status, and failure rates. MVP.
REQ-ADM-003 Administrators shall disable unreliable sources. MVP.
REQ-ADM-004 Administrators shall see cost and latency metrics by pipeline stage. MVP.
REQ-ADM-005 Administrative actions shall be authorized and audited. MVP.

### Ask Mode and opportunities

REQ-ASK-001 Ask Mode shall answer free-form questions over the event graph with citations. P1/Phase 2; deliberately deferred until the core loop is proven.
REQ-OPP-001 Opportunity Intelligence shall match hackathons and grants to interests and skills. P2.
REQ-TEAM-001 Shared collections, team curation, exports, and organization intelligence shall be available in later releases. P2.
REQ-MOB-001 Native mobile applications shall not be built before responsive web retention is demonstrated. OOS until gate.

## 5. Non-functional requirements

REQ-NFR-001 Feed first content target: p50 <300 ms, p95 <800 ms.
REQ-NFR-002 Brief shell target: p50 <500 ms, p95 <1.2 s.
REQ-NFR-003 Brief primary content target: p50 <1.5 s, p95 <3 s.
REQ-NFR-004 Background event precompute target: p50 <5 min, p95 <20 min.
REQ-NFR-005 The service shall degrade to cached verified content when personalization or generation providers fail.
REQ-NFR-006 Data shall be encrypted in transit and at rest with least-privilege access.
REQ-NFR-007 Users shall have export and deletion paths aligned with GDPR/CCPA expectations.
REQ-NFR-008 Raw behavior data shall have a defined retention TTL and aggregate use policy.
REQ-NFR-009 The frontend shall be responsive, keyboard accessible, and usable at mobile breakpoints.
REQ-NFR-010 All public source links and citations shall remain traceable to the source identity and retrieval timestamp.
REQ-NFR-011 Jobs shall be retryable and idempotent with dead-letter handling.
REQ-NFR-012 Every production request and job shall emit structured logs, metrics, and correlation identifiers.

## 6. Trust and legal constraints

REQ-TRU-001 No fabricated benchmarks, quotes, statistics, citations, features, dates, or specifications.
REQ-TRU-002 Briefs shall synthesize rather than reproduce publisher paragraphs.
REQ-TRU-003 Source links shall be prominent and referral traffic measurable.
REQ-TRU-004 Outside counsel review is required before adding non-permissive sources or public launch.
REQ-TRU-005 Corrections shall re-run verification and visibly mark affected records as updated.

## 7. Business, brand, and launch requirements

REQ-BRAND-001 The working product name shall be Cairn and the tagline shall be “Know what matters. Skip the noise.” All releases.
REQ-BRAND-002 The interface shall use a field-notebook/analyst-desk direction: restrained palette, humanist or serif reading typography, monospace metadata accents, no gradient-orb or generic AI dashboard styling. MVP.
REQ-BRAND-003 Functional navigation labels shall remain literal and shall not be replaced with trail-metaphor labels. MVP.
REQ-LAUNCH-001 Before public launch, the product shall complete trademark, domain, social-handle, and app-store checks. Legal/Launch prerequisite.
REQ-LAUNCH-002 Outside counsel shall review sources, licensing, privacy, and public launch readiness. Legal/Launch prerequisite.
REQ-BIZ-001 The entitlement model shall support Free, Pro, Team, and Enterprise tiers without weakening verification standards. P1/Phase 2.
REQ-BIZ-002 The product shall not place sponsored items inside the ranked feed. All releases.
REQ-BIZ-003 Billing shall be deferred until the feed-to-brief retention loop is validated, while entitlement boundaries remain designed. P1/Phase 2.

## 8. Metrics and release acceptance

REQ-MET-001 The product shall measure factuality, citation coverage, clustering quality, relevance feedback, brief quality, alert precision, latency, cost, retention, and source diversity. MVP instrumentation; metric refinement ongoing.
REQ-MET-002 Raw session time and scroll depth shall not be primary success metrics. All releases.
REQ-MET-003 The first release shall prove the loop: permitted source document → normalized document → clustered event → relevance-ranked card → cited brief → evidence inspection. MVP.
REQ-MET-004 Launch shall be limited to responsive web/PWA-capable delivery; native mobile requires a later retention decision. MVP.

MVP is accepted only when a seeded or live source document can be normalized, clustered into an event, verified into a Cairn Record, ranked for a configured reader, and rendered as a cited brief with a degraded cached path. The complete traceability matrix maps every MVP requirement to design and tests.
