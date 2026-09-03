# Requirements to Test Traceability Baseline

| SRS IDs | Required test evidence |
|---|---|
| REQ-ONB-* | API/application tests for profile persistence and default-feed behavior; browser flow tests |
| REQ-FED-* | Ranking unit tests, feed contract tests, browser accessibility and responsive tests |
| REQ-BRF-001..010 | Record selection tests, citation integrity integration tests, SSE/E2E tests, degraded-path test |
| REQ-ING-* | Connector contract fixtures, idempotency tests, source-policy tests, retry/dead-letter tests |
| REQ-ALT-* / REQ-FBK-* | Alert rule unit tests, delivery integration tests, authorization and feedback persistence tests |
| REQ-ADM-* | Role/permission tests, state transition tests, audit-log integration tests |
| REQ-NFR-* | Performance/load tests, security tests, accessibility tests, observability assertions, restore drills |
| REQ-TRU-* | Evidence policy tests, prompt-injection fixtures, source reproduction checks, correction workflow tests |

No requirement is considered implemented solely because a UI exists. Each behavior requires a test at the lowest useful boundary plus an end-to-end test for critical user journeys.
