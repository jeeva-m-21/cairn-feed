# Cairn Security and Privacy Baseline

## Controls

Use secure, httpOnly, same-site sessions or an equivalent vetted identity provider. Hash passwords with a current password hashing scheme if self-managed. Enforce authorization at the API/service layer, not only in the UI. Use least-privilege database roles and separate admin credentials.

Encrypt transport and managed storage. Keep provider secrets in deployment secret managers. Redact tokens, source payloads, and personal behavior from logs. Validate all provider outputs before persistence or rendering.

## Privacy

Collect only profile, saved content, behavior, and delivery data needed for personalization and operations. Explain inferred interest use. Provide export, deletion, and account disable flows. Apply bounded retention to raw behavior. Do not use private user content for model training without an explicit policy and consent decision.

## Threat priorities

Account takeover, cross-user data access, admin abuse, prompt/provider injection from source text, malicious source URLs, SSRF through connectors, unsafe HTML, citation manipulation, queue replay, and secret leakage.

## Required tests

Authorization matrix tests, SSRF/URL allowlist tests, malicious source-content fixture tests, XSS output tests, rate-limit tests, audit-log tests, deletion/export tests, and dependency vulnerability scanning.
