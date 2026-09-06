# DANTE Architecture Index

- **Status:** CURRENT / AUTHORITATIVE NAVIGATION
- **Last reconciled:** 2026-09-06
- **Scope:** current repository architecture and long-lived subsystem contracts

This index describes the current repository tree directly. Protected-main integration status is determined by Git reachability and `../PROJECT-STATUS.md`; historical branch wording never overrides protected-main truth.

## 1. Current architecture state

```text
Product / Domain / Logical / Physical       CLOSED / CURRENT
Engineering Foundation                      CLOSED / ACCEPTED
Frontend Foundation                         CLOSED / ACCEPTED
Backend CP1–CP6                              CLOSED / ACCEPTED
PostgreSQL                                   18.6 / sole canonical persistence
Access/Auth M1–M5                            CLOSED / INTEGRATED
Authenticated DANTE Context                  CLOSED / INTEGRATED VIA PR #66
Shared Email Platform                        CLOSED / INTEGRATED
PostgreSQL Recovery                          CLOSED / INTEGRATED
Platform Observability                       CLOSED / INTEGRATED VIA PR #58
AI deterministic low-level foundation        CLOSED / INTEGRATED VIA PR #63
Home / World Focus reconciliation            CLOSED / INTEGRATED VIA PR #65
Pre-vertical foundation                      CLOSED / INTEGRATED VIA PR #66
AI production/private-data qualification     NOT CLAIMED
```

Current protected-main application database truth is `20260906_18` with topology `89/5/18/77/173/91/272`. The pre-vertical integration merge is `1ecd58145860aebfaaa3dc1bd356b90f7a8eb19b`.

## 2. System entry points

- `system-overview.md`
- `technical-decisions.md`
- `../PROJECT-STATUS.md`
- `../ROADMAP.md`

## 3. AI / Intelligence

Current AI architecture authority and durable evidence:

- `dante-ai-implementation-baseline-final.md` — final implementation architecture baseline
- `dante-ai-search-intelligence-boundary-amendment-2026-09.md` — independent Search / Intelligence boundary
- `../workstreams/ai-foundation-closure-2026-09-05.md` — deterministic foundation closure evidence
- `../workstreams/ai-runtime-model-target-closure-acceptance-2026-09-05.md` — accepted development model-target/binding decision

Permanent boundaries include:

```text
DANTE domain/application authority > model/provider authority
Search != Intelligence
Search remains deterministic and independently usable without AI runtime
Intelligence consumes Search only through public Search surfaces
provider/model output != canonical DANTE truth
ModelTarget != ProviderBinding != model/deployment
DEEP_REASONING may remain dormant without a physical binding
production/private-data activation requires separate qualification
```

The current development binding uses Gemini 3.8 Flash through DANTE's application-owned `ModelAccess` boundary and native Gemini Interactions protocol. This is a development-foundation decision, not production/private-data qualification or permanent provider preference.

The deterministic AI foundation is protected-main truth through PR #63 / merge `431fb34029baeacc9ef9f721e9626b39ca10dd39`.

## 4. Access/Auth and authenticated DANTE context

Access/Auth authority:

- `access-auth-architecture.md`
- `access-auth-security-contract.md`
- `access-auth-api-contract.md`
- `access-auth-testing-contract.md`
- `access-auth-m4-contract.md`
- `access-auth-m5-contract.md`
- `access-auth-m5-persistence-api-contract.md`
- `../frontend/access.md`
- `../database/access-auth.md`

Authenticated DANTE context authority:

- `authenticated-dante-context.md` — explicit Account → self Person application-context bridge, timezone policy and request-level resolution contract
- `../workstreams/pre-vertical-foundation-closure-2026-09-06.md` — durable closure evidence

Permanent identity/auth boundary:

```text
Person != Account != Principal != Actor
AuthSession != DANTE Session
EmailIdentity != Account
PasswordCredential optional
Principal request-runtime only
provider identity = issuer + subject
provider email != identity/link authority
provider assertion != DANTE AuthSession
passwordless Account valid
method != factor != assurance
```

The authenticated context does not modify those Access/Auth semantics. It consumes an admitted `Principal`, resolves the associated `Account`, and exposes a separate typed `DanteContext` containing the explicit self `Person` NativeRef plus user/default timezone policy. It does not add a universal `user_id`, workspace/world/tenant identity or generic profile/preferences model.

## 5. Shared Email Platform

- `email-platform.md`
- `access-auth-email-delivery.md` — Access/Auth consumer integration
- `../decisions/ADR-012-email-delivery-platform.md`
- `../development/email-platform-local-uat.md`
- `../development/email-platform-acceptance-2026-09-03.md`

The Email Platform is shared infrastructure. DANTE owns durable delivery lifecycle and ambiguity policy; provider transport is an external effect and is never executed inside the authoritative caller transaction.

## 6. Platform Observability

- `observability-runtime-contract.md` — current/evolving signal, privacy, ownership, cardinality and failure contract
- `../development/observability-runbook.md` — operator setup, validation, incident, rotation and rollback procedure
- `../../infra/observability/README.md` — Alloy/Grafana runtime and source-controlled operational assets
- `../database/dante-postgresql-database-part-12.md` — exact PostgreSQL observer-role contract

Architectural boundary:

```text
backend metrics/traces ──OTLP──────┐
backend JSON logs ───────file──────┤
Web errors/vitals/traces ─Faro─────┼─> Grafana Alloy ─> Grafana Cloud
PostgreSQL stats ───────observer───┤
readiness ───────────────blackbox───┘
```

Permanent rules:

```text
telemetry != canonical DANTE state
telemetry != Domain history / Evidence / Provenance
telemetry failure != permission to alter product truth
no product/Auth/API data dependency from Web observability
no raw URL/query/SQL/identity/session/secret telemetry dimensions
bounded cardinality and bounded retry/buffering
```

`dante_observer` is provisioning-owned technical infrastructure, not an Account, Principal, Actor or application model. It has `LOGIN NOINHERIT`, with `pg_read_all_stats` membership using `INHERIT TRUE / SET FALSE / ADMIN FALSE`, `search_path=pg_catalog`, no database `CREATE`/`TEMP` and no DANTE/public business-object access.

## 7. Database / persistence

- `../database/README.md`
- `../database/dictionary/README.md`
- `../database/dante-postgresql-database.md`
- `../development/backend-cp6-02-postgresql-persistence-constitution.md`
- `../decisions/ADR-010-postgresql-persistence-constitution.md`

Permanent invariant:

```text
current DB reference
≈ Database Dictionary
≈ SQLAlchemy mappings
≈ Alembic
≈ real PostgreSQL
≈ direct tests
```

Current protected-main database truth is `20260906_18 / 89|5|18|77|173|91|272|0|0|0`. The former `20260904_17` topology is historical integration context only.

## 8. Important ADRs

- `../decisions/ADR-007-domain-model-informed-persistence-boundaries.md`
- `../decisions/ADR-008-frontend-engineering-stack.md`
- `../decisions/ADR-009-frontend-architecture-boundaries.md`
- `../decisions/ADR-010-postgresql-persistence-constitution.md`
- `../decisions/ADR-011-access-auth-architecture.md`
- `../decisions/ADR-012-email-delivery-platform.md`

## 9. Historical evidence

Branch histories, dated acceptance records and old milestone banners are evidence only. They never override the current executable repository or current/evolving references.

- `../archive/branches/2026-09-feature-access-auth.md`
- `../archive/branches/2026-09-feature-platform-observability.md`
- `../workstreams/access-auth-integration-acceptance-2026-09-04.md`
- `../workstreams/pre-vertical-foundation-closure-2026-09-06.md`
- dated AI architecture hardening/evaluation records retained by the AI workstream

Temporary branch handoffs must be removed before protected-main integration under `../development/documentation-lifecycle-policy.md`.
