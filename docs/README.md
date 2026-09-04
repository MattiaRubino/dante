# DANTE Documentation Index

- **Status:** CURRENT NAVIGATION / AUTHORITY INDEX
- **Last reconciled:** 2026-09-04
- **Current candidate:** `integration/access-auth-main-20260904`
- **Accepted candidate proof HEAD:** `81639c61478b476c995652d0060dde8f53aef089`
- **Current work:** PROTECTED-MAIN INTEGRATION READY

## Authority order

```text
1. executable/materialized repository truth
2. accepted Product / Domain / Logical / Physical / constitutions / ADRs
3. current subsystem references
4. PROJECT-STATUS / ROADMAP / current workstream
5. durable evidence / Git chronology
6. conversation memory
```

Protected `main` still owns integrated Recovery-only truth at Alembic `20260830_09`. The accepted integration candidate contains Recovery + Access/Auth + shared Email Platform at the no-DDL merge head `20260904_17` and has passed combined CI plus the enriched-baseline CP07 whole LOCAL recovery rehearsal.

## Current lifecycle

```text
Product / Domain / Logical / Physical          CLOSED / CURRENT
Engineering / Frontend / Backend CP1–CP6      CLOSED / ACCEPTED
PostgreSQL                                     18.6
Protected-main Recovery                        CLOSED / INTEGRATED
Access/Auth M1–M5                              CLOSED / ACCEPTED
Shared Email Platform                          CLOSED / ACCEPTED / OWNERSHIP VERIFIED
Apple real external UAT                        BOUNDED DEFERRED
Candidate Alembic                              20260904_17
Candidate DB                                   88/5/16/76/172/89/270
Combined candidate CI                          PASS
CP07 whole LOCAL recovery                      PASS
Integration candidate                          READY FOR PROTECTED-MAIN MERGE
feature/platform-observability                 CLOSED / OPERATIONAL PASS / NOT INTEGRATED
M6 Native Mobile                               FUTURE / OPTIONAL
later M7 Access/security maturity              FUTURE
```

CP07 `LOCAL PASS` does not claim a remote backup provider or production/cloud recovery. Those remain separate future deployment gates.

## Mandatory continuation entry points

1. `../README.md`
2. `PROJECT-STATUS.md`
3. `ROADMAP.md`
4. `development/agent-operating-manual.md`
5. `development/documentation-lifecycle-policy.md`
6. active workstream record
7. subsystem authority relevant to the task
8. exact current Git refs

## Access/Auth

- `workstreams/access-auth.md`
- `workstreams/access-auth-integration-acceptance-2026-09-04.md`
- `architecture/access-auth-architecture.md`
- `architecture/access-auth-security-contract.md`
- `architecture/access-auth-api-contract.md`
- `architecture/access-auth-testing-contract.md`
- `architecture/access-auth-m5-contract.md`
- `architecture/access-auth-m5-persistence-api-contract.md`
- `database/access-auth.md`
- `frontend/access.md`

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

## Integration sequence

```text
accepted combined candidate
→ PR #52 to protected main
→ post-merge main verification + current-document reconciliation
→ enriched main into feature/platform-observability
→ observability release rechecks
→ protected-main PR
→ future bounded workstreams
```

Temporary handoffs do not belong on protected main; current specs must not become append-only diaries.
