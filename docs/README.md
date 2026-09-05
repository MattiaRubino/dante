# DANTE Documentation Index

- **Status:** CURRENT NAVIGATION / AUTHORITY INDEX
- **Last reconciled:** 2026-09-05
- **Current protected-main tree:** Access/Auth + shared Email Platform + Recovery + Platform Observability
- **Protected-main Observability merge:** `b74a806deed68b2729dd04678c0a5674cd572e8a` via PR `#58`
- **Current Alembic:** `20260904_17`

## Authority order

```text
1. executable/materialized repository truth
2. accepted Product / Domain / Logical / Physical / constitutions / ADRs
3. current subsystem references
4. PROJECT-STATUS / ROADMAP / legitimate active workstream
5. durable evidence / Git chronology
6. conversation memory
```

## Current lifecycle

```text
Product / Domain / Logical / Physical          CLOSED / CURRENT
Engineering / Frontend / Backend CP1–CP6      CLOSED / ACCEPTED
PostgreSQL                                     18.6
Recovery                                       CLOSED / INTEGRATED
Access/Auth M1–M5                              CLOSED / INTEGRATED
Shared Email Platform                          CLOSED / INTEGRATED / OWNERSHIP VERIFIED
Apple real external UAT                        BOUNDED DEFERRED
Alembic                                        20260904_17
Database                                       88/5/16/76/172/89/270
Database-local CP07                            PASS
Application / Email reopen CP08                PASS
Platform Observability source                  CLOSED / OPERATIONAL PASS
Platform Observability protected main          CLOSED / INTEGRATED VIA PR #58
M6 Native Mobile                               FUTURE / OPTIONAL
later M7 Access/security maturity              FUTURE
```

Remote-provider and production/cloud recovery remain separate future gates.

## Mandatory continuation entry points

1. `../README.md`
2. `PROJECT-STATUS.md`
3. `ROADMAP.md`
4. `development/agent-operating-manual.md`
5. `development/documentation-lifecycle-policy.md`
6. legitimate active workstream record, when one exists
7. subsystem authority relevant to the task
8. exact current Git refs

## Access/Auth

Access/Auth M1–M5 is integrated and has no active workstream authority file.

Current subsystem authority:

- `architecture/access-auth-architecture.md`
- `architecture/access-auth-security-contract.md`
- `architecture/access-auth-api-contract.md`
- `architecture/access-auth-testing-contract.md`
- `architecture/access-auth-m5-contract.md`
- `architecture/access-auth-m5-persistence-api-contract.md`
- `database/access-auth.md`
- `frontend/access.md`

Historical/evidence routing:

- `archive/branches/2026-09-feature-access-auth.md` — consolidated branch history, **NON-AUTHORITATIVE**
- `workstreams/access-auth-m5-review-2026-09-02.md` — historical validation/UAT evidence
- `workstreams/access-auth-integration-acceptance-2026-09-04.md` — historical integration/CI/CP07 evidence

## Shared Email Platform

- `architecture/email-platform.md`
- `architecture/access-auth-email-delivery.md`
- `decisions/ADR-012-email-delivery-platform.md`
- `development/email-platform-local-uat.md`
- `development/email-platform-acceptance-2026-09-03.md`

## Platform Observability

Current/evolving authority:

- `architecture/observability-runtime-contract.md` — signal, privacy, cardinality, failure and ownership contract
- `development/observability-runbook.md` — setup, validation, incident, rotation and rollback procedures
- `../infra/observability/README.md` — Alloy/Grafana/LOCAL runtime and source-controlled operational assets
- `database/dante-postgresql-database-part-12.md` — Section 46 exact `dante_observer` database security contract

Historical/evidence routing:

- `archive/branches/2026-09-feature-platform-observability.md` — single consolidated Platform Observability branch/integration history, **NON-AUTHORITATIVE**

There is no active `workstreams/platform-observability.md` authority. The source workstream and integration branch are closed; Git, PR `#58` and the consolidated branch record retain chronology.

## Database / Recovery

- `database/README.md` — current Database System of Record
- `database/dictionary/README.md` — machine-readable current contract
- `database/dante-postgresql-database.md` — current human-readable architecture/reference
- `database/dante-postgresql-database-part-*.md` — detailed design/reference evidence; historical phase banners do not override current authority
- `operations/postgres-recovery-runbook.md` — current LOCAL recovery + application/Email reopen operator contract
- `development/backend-cp6-02-postgresql-persistence-constitution.md`
- `decisions/ADR-010-postgresql-persistence-constitution.md`

Permanent invariant:

```text
current human DB reference
≈ Database Dictionary
≈ SQLAlchemy mappings
≈ Alembic
≈ real PostgreSQL
≈ direct tests
```

## Current integration sequence

```text
Platform Observability protected-main integration via PR #58    CLOSED
→ future bounded workstreams start from current protected main
```

Temporary handoffs do not belong on protected main; current specifications must not become append-only diaries.
