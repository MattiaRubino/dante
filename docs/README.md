# DANTE Documentation Index

- **Status:** CURRENT NAVIGATION / AUTHORITY INDEX
- **Last reconciled:** 2026-09-04
- **Protected main:** Access/Auth + shared Email Platform + Recovery integrated
- **Current Alembic:** `20260904_17`
- **Current work:** `feature/platform-observability` integration

## Authority order

```text
1. executable/materialized repository truth
2. accepted Product / Domain / Logical / Physical / constitutions / ADRs
3. current subsystem references
4. PROJECT-STATUS / ROADMAP / legitimate active workstream
5. durable evidence / Git chronology
6. conversation memory
```

Protected `main` owns the combined Access/Auth + shared Email Platform + Recovery truth at Alembic `20260904_17`. PR #52 integrated the accepted candidate at merge commit `5f76ec54ad78542f137e8730e904f805d9e59e56`; post-merge Backend and Frontend CI passed on that exact commit.

## Current lifecycle

```text
Product / Domain / Logical / Physical          CLOSED / CURRENT
Engineering / Frontend / Backend CP1–CP6      CLOSED / ACCEPTED
PostgreSQL                                     18.6
Recovery                                       CLOSED / INTEGRATED
Access/Auth M1–M5                              CLOSED / INTEGRATED
Shared Email Platform                          CLOSED / INTEGRATED / OWNERSHIP VERIFIED
Apple real external UAT                        BOUNDED DEFERRED
Protected-main Alembic                         20260904_17
Protected-main DB                              88/5/16/76/172/89/270
database-local CP07                            PASS
Email post-restore whole-flow gate             REMEDIATION REQUIRED
post-merge Backend CI                          PASS
post-merge Frontend CI                         PASS
feature/platform-observability                 CLOSED / OPERATIONAL PASS / NEXT INTEGRATION
M6 Native Mobile                               FUTURE / OPTIONAL
later M7 Access/security maturity              FUTURE
```

The historical CP07 run directly proves its executed LOCAL PostgreSQL/database-local and MaterialState recovery scope. It did not directly prove Email `quarantine_after_restore()` ordering before Email workers resume, so application Email traffic reopen after PITR is not inferred from that run. Remote-provider and production/cloud recovery remain separate future gates.

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

## Database / Recovery

- `database/README.md` — current Database System of Record
- `database/dictionary/README.md` — machine-readable current contract
- `database/dante-postgresql-database.md` — current human-readable architecture/reference
- `database/dante-postgresql-database-part-*.md` — detailed design/reference evidence; historical phase banners do not override current authority
- `operations/postgres-recovery-runbook.md` — current LOCAL recovery operator contract
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
enriched protected main
→ feature/platform-observability
→ observability release/integration rechecks
→ protected-main Observability PR
→ future bounded workstreams
```

Temporary handoffs do not belong on protected main; current specs must not become append-only diaries.
