# DANTE Documentation Index

- **Status:** CURRENT NAVIGATION / AUTHORITY INDEX
- **Last reconciled:** 2026-09-04
- **Current candidate:** `integration/access-auth-main-20260904`
- **Current work:** COMBINED INTEGRATION QA

## Authority order

```text
1. executable/materialized repository truth
2. accepted Product / Domain / Logical / Physical / constitutions / ADRs
3. current subsystem references
4. PROJECT-STATUS / ROADMAP / current workstream
5. durable evidence / Git chronology
6. conversation memory
```

Protected `main` still owns integrated Recovery-only truth. The integration candidate contains Recovery + Access/Auth + shared Email Platform and must pass full combined QA before the protected-main PR is accepted.

## Current lifecycle

```text
Product / Domain / Logical / Physical          CLOSED / CURRENT
Engineering / Frontend / Backend CP1–CP6      CLOSED / ACCEPTED
PostgreSQL                                     18.6
Protected-main Recovery                        CLOSED / INTEGRATED
Access/Auth M1–M5                              CLOSED / ACCEPTED
Shared Email Platform                          CLOSED / ACCEPTED
Apple real external UAT                        BOUNDED DEFERRED
Candidate Alembic                              20260904_17
Candidate DB                                   88/5/16/76/172/89/270
Combined integration QA                        ACTIVE
feature/platform-observability                 CLOSED / OPERATIONAL PASS / NOT INTEGRATED
M6 Native Mobile                               FUTURE / OPTIONAL
later M7 Access/security maturity              FUTURE
```

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

## Database

- `database/README.md` — current System of Record
- `database/dictionary/README.md` — machine-readable contract
- `database/dante-postgresql-database*.md` — deep CP6 design/reference history; stale phase banners are historical, not current status
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
combined candidate QA
→ protected-main PR for Recovery-compatible Access/Auth + Email foundation
→ enriched main into feature/platform-observability
→ observability release rechecks
→ protected-main PR
→ future bounded workstreams
```

Temporary handoffs do not belong on protected main; current specs must not become append-only diaries.
