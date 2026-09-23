# DANTE Documentation Index

- **Status:** CURRENT NAVIGATION / AUTHORITY INDEX
- **Last reconciled:** 2026-09-23
- **Protected-main baseline at temporal selection:** PostgreSQL 18.6 / Alembic `20260906_18` / topology `89|5|18|77|173|91|272|0|0|0`
- **Active candidate workstream:** `feature/timeline-temporal-operational`
- **Candidate temporal DB authority:** PostgreSQL 18.6 / Alembic `20260923_57`
- **Candidate temporal topology:** `145|5|88|92|285|223|408|0|0|0`
- **Current temporal frontier:** B06 ✅ CLOSED / PROVEN → B08 Session Runtime NEXT; B07 deliberately deferred until after B12

## Authority order

```text
1. executable/materialized repository truth
2. accepted Product / Domain / Logical / Physical / constitutions / ADRs
3. current subsystem references
4. PROJECT-STATUS / ROADMAP / legitimate active workstream
5. durable evidence / Git chronology
6. conversation memory
```

Candidate branch truth and protected-main truth must remain explicitly distinct until integration.

## Current lifecycle

```text
Product / Domain / Logical / Physical          CLOSED / CURRENT
Engineering / Frontend / Backend CP1–CP6      CLOSED / ACCEPTED
PostgreSQL                                     18.6
Access/Auth + Shared Email                     CLOSED / INTEGRATED
Recovery                                       CLOSED / INTEGRATED
Platform Observability                         CLOSED / INTEGRATED
AI deterministic low-level foundation          CLOSED / INTEGRATED
Home / World Focus                             CLOSED / INTEGRATED
Pre-vertical foundation                        CLOSED / INTEGRATED

Protected-main Alembic baseline                20260906_18
Active Timeline candidate                      feature/timeline-temporal-operational
Candidate Alembic                              20260923_57
Candidate B00–B06                              CLOSED / PROVEN
Candidate B08                                  NEXT / NOT STARTED
Candidate B07                                  DEFERRED until after B12
```

Remote-provider integration, native/offline, account collaboration and broad analytics remain future work outside the current Timeline vertical.

## Mandatory continuation entry points

1. `../README.md`
2. `PROJECT-STATUS.md`
3. `ROADMAP.md`
4. `development/agent-operating-manual.md`
5. `development/documentation-lifecycle-policy.md`
6. active workstream authority, when one exists
7. subsystem authority relevant to the task
8. exact current Git refs

## Active Timeline / Temporal-Operational vertical

Current authority:

1. `workstreams/timeline-temporal-operational-post-b06-scope-decision-2026-09-23.md` — accepted vertical boundary and sequencing;
2. `workstreams/timeline-temporal-operational-roadmap.md` — current execution roadmap;
3. `workstreams/timeline-temporal-operational-map.md` — live semantic/proof ledger;
4. `workstreams/timeline-temporal-operational-handoff.md` — current B08 handoff;
5. `database/timeline-temporal-operational.md` — candidate DB overlay;
6. `database/README.md` + `database/dictionary/` — current persistence authority;
7. B04/B05/B06 execution/closure records — durable evidence.

Active vertical boundary:

```text
Home `+`
→ canonical create/configuration
→ Timeline representation/actions
→ required Session/Actual lifecycle
→ advanced recurrence/reminders
→ replanning/conflict/solver proposals
→ final deferred UI/UX consolidation
```

Explicitly outside this vertical:

```text
external provider integration
native/mobile/offline/multi-device
account-to-account collaboration/chat/shared editing
broad analytics/statistics/signals
```

## Database / Recovery

- `database/README.md` — current Database System of Record
- `database/dictionary/README.md` — current machine-readable contract index
- `database/timeline-temporal-operational.md` — active candidate overlay
- `database/dante-postgresql-database.md` + continuation parts — detailed human reference
- `development/backend-cp6-02-postgresql-persistence-constitution.md`
- `decisions/ADR-010-postgresql-persistence-constitution.md`
- `operations/postgres-recovery-runbook.md`

Permanent invariant:

```text
current human DB reference
≈ Database Dictionary
≈ SQLAlchemy mappings
≈ Alembic
≈ real PostgreSQL
≈ direct tests
```

## Frontend / Home

For current Timeline/Temporal implementation status, the active workstream roadmap/map/handoff outrank the old pre-vertical frontend phase documents.

Current frontend navigation:

- `frontend/README.md`
- `frontend/home/current-checkpoint.md`
- `frontend/home/home-structural-contract.md`
- active Timeline/Temporal workstream authority listed above

Dated C1/Home frontend records preserve historical phase evidence and must not be interpreted as current Timeline sequencing when they conflict with the active workstream.

## Access/Auth and shared Email

Current subsystem authority remains under:

- `architecture/access-auth-architecture.md`
- `architecture/access-auth-security-contract.md`
- `architecture/access-auth-api-contract.md`
- `database/access-auth.md`
- `frontend/access.md`
- `architecture/email-platform.md`
- `development/email-platform-local-uat.md`

Historical Access/Auth integration/branch files remain evidence only.

## Platform Observability

Current authority:

- `architecture/observability-runtime-contract.md`
- `development/observability-runbook.md`
- `../infra/observability/README.md`
- PostgreSQL observer contract in the database reference

## AI / Intelligence / Search

The deterministic low-level AI/Search foundation is integrated platform capability. It is not automatically active scheduling authority for the Timeline vertical.

For B12 specifically:

```text
deterministic solver/candidate generation first
AI interpretation/explanation/ranking optional
AI output != accepted Schedule/effect
```

## Documentation lifecycle

```text
CURRENT/AUTHORITATIVE file
→ must describe present truth

HISTORICAL / ARCHIVE / dated evidence
→ preserves phase-time truth and is not rewritten to pretend it was current later
```

Temporary handoffs must not become competing authorities. Applied migration history is immutable. No PASS is claimed without executed evidence.