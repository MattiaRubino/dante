# DANTE Architecture Index

- **Status:** CURRENT / AUTHORITATIVE NAVIGATION
- **Last reconciled:** 2026-09-05
- **Scope:** current repository architecture and long-lived subsystem contracts

This index describes the current repository tree directly. Protected-main integration status is determined by Git reachability and `../PROJECT-STATUS.md`; a branch-local candidate is never promoted to protected-main truth by documentation wording alone.

## 1. Current architecture state

```text
Product / Domain / Logical / Physical       CLOSED / CURRENT
Engineering Foundation                      CLOSED / ACCEPTED
Frontend Foundation                         CLOSED / ACCEPTED
Backend CP1–CP6                              CLOSED / ACCEPTED
PostgreSQL                                   18.6 / sole canonical persistence
Access/Auth M1–M5                            CLOSED / INTEGRATED
Shared Email Platform                        CLOSED / INTEGRATED
PostgreSQL Recovery                          CLOSED / INTEGRATED
Platform Observability                       MATERIALIZED / ACCEPTED IN CURRENT TREE
```

Current application database contract remains `20260904_17` with topology `88/5/16/76/172/89/270`. Platform Observability adds no DANTE business DDL or application persistence model.

## 2. System entry points

- `system-overview.md`
- `technical-decisions.md`
- `../PROJECT-STATUS.md`
- `../ROADMAP.md`

## 3. Access/Auth

- `access-auth-architecture.md`
- `access-auth-security-contract.md`
- `access-auth-api-contract.md`
- `access-auth-testing-contract.md`
- `access-auth-m4-contract.md`
- `access-auth-m5-contract.md`
- `access-auth-m5-persistence-api-contract.md`
- `../frontend/access.md`
- `../database/access-auth.md`

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

## 4. Shared Email Platform

- `email-platform.md`
- `access-auth-email-delivery.md` — Access/Auth consumer integration
- `../decisions/ADR-012-email-delivery-platform.md`
- `../development/email-platform-local-uat.md`
- `../development/email-platform-acceptance-2026-09-03.md`

The Email Platform is shared infrastructure. DANTE owns durable delivery lifecycle and ambiguity policy; provider transport is an external effect and is never executed inside the authoritative caller transaction.

## 5. Platform Observability

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

## 6. Database / persistence

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

## 7. Important ADRs

- `../decisions/ADR-007-domain-model-informed-persistence-boundaries.md`
- `../decisions/ADR-008-frontend-engineering-stack.md`
- `../decisions/ADR-009-frontend-architecture-boundaries.md`
- `../decisions/ADR-010-postgresql-persistence-constitution.md`
- `../decisions/ADR-011-access-auth-architecture.md`
- `../decisions/ADR-012-email-delivery-platform.md`

## 8. Historical evidence

Branch histories, dated acceptance records and old milestone banners are evidence only. They never override the current executable repository or current/evolving references.

- `../archive/branches/2026-09-feature-access-auth.md`
- `../archive/branches/2026-09-feature-platform-observability.md`
- `../workstreams/access-auth-integration-acceptance-2026-09-04.md`

Temporary branch handoffs must be removed before protected-main integration under `../development/documentation-lifecycle-policy.md`.
