# DANTE Documentation Index

- **Status:** CURRENT NAVIGATION / AUTHORITY INDEX
- **Last reconciled:** 2026-09-05
- **Current protected-main tree:** Access/Auth + shared Email Platform + Recovery + Platform Observability + Home/Timeline/Temporal foundation
- **Protected-main Observability merge:** `b74a806deed68b2729dd04678c0a5674cd572e8a` via PR `#58`
- **Protected-main Home/Timeline merge:** `9dae13163549ca6d342978876be9582d7ec08610` via PR `#61`
- **Current AI integration candidate:** PR `#63` from `feature/ai-implementation` / merge pending
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
Home / Timeline / Temporal foundation          CLOSED / INTEGRATED VIA PR #61
Temporal C1 manual acceptance                  OPEN / exact user token still required
AI low-level deterministic foundation          CLOSED / PASS ON FEATURE / PR #63 MERGE PENDING
AI production/private-data activation          OFF / NOT CLAIMED
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

## Home / Timeline / Temporal

Protected `main` includes the Home/Timeline/Temporal integration from PR `#61`.

Current subsystem references include:

- `frontend/home/current-checkpoint.md`
- `frontend/home/home-structural-contract.md`
- `frontend/temporal-frontend-roadmap.md`
- `frontend/temporal-f0-contract.md`
- `frontend/timeline-t1-frozen-contract.md`
- `frontend/temporal-create-c1-manual-acceptance.md`

Git integration state and semantic acceptance state are distinct. The PR `#61` merge establishes repository integration; it does **not** manufacture the exact C1 manual approval token. C1 therefore remains open until the required user acceptance is recorded.

## AI / Intelligence / Search

Current branch-local integration truth while PR `#63` remains unmerged:

- `workstreams/ai-implementation.md` — active implementation/integration workstream; authoritative for current branch stage and merge-pending disposition
- `architecture/dante-ai-implementation-baseline-final.md` — **FROZEN IMPLEMENTATION-ENTRY ARCHITECTURE REFERENCE** accepted before implementation began; its architecture invariants remain applicable, but its acceptance-time status lines such as `Implementation: NONE YET`, provider/model `OPEN`, and `Current next action: I0` are historical entry-state metadata and are **not current implementation-status claims**
- `architecture/dante-ai-post05-final-mega-acceptance.md` — durable pre-implementation architecture acceptance evidence
- `architecture/dante-ai-foundation.md` — current semantic/architectural baseline within its bounded AI-00 scope

Historical/superseded implementation-candidate evidence:

- `architecture/dante-ai-implementation-baseline.md` — superseded pre-implementation candidate evidence
- `architecture/dante-ai-implementation-baseline-v2.md` — superseded pre-implementation candidate evidence
- `architecture/dante-ai-implementation-baseline-v3.md` — superseded pre-implementation candidate evidence; accepted into the later final baseline/mega-acceptance chain

The historical files above retain the status language that was true at their own checkpoints. They must not be read as present-tense repository implementation status and must not override executable truth, this navigation index, or the active workstream.

Current bounded AI implementation posture on PR `#63`:

```text
Search deterministic foundation                IMPLEMENTED / NO REAL PRODUCT DATA ADAPTER YET
Intelligence request-local foundation           IMPLEMENTED
ModelAccess                                     IMPLEMENTED
Gemini native Interactions development binding  IMPLEMENTED / DEVELOPMENT ONLY
Deep reasoning physical binding                 DORMANT
real Ask DANTE product integration              DEFERRED
private-data eligibility                        NO
production activation                           OFF
AI persistence / DB / Alembic change            NONE
```

`Search` here means DANTE's deterministic internal discovery/query foundation over authorized DANTE data. It is not web search, not a frontend search bar, and not an AI/model dependency. Real product/data Search families remain deferred until an owning capability/data seam exists.

After PR `#63` is merged and post-merge acceptance succeeds, branch-local `MERGE PENDING` wording must be retired/reconciled on protected `main` according to the documentation lifecycle policy.

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
→ Home / Timeline / Temporal integration via PR #61             CLOSED
→ AI low-level foundation integration via PR #63                MERGE PENDING / REQUIRED CHECKS MUST PASS ON FINAL HEAD
→ post-merge acceptance + workstream retirement                 REQUIRED AFTER MERGE
→ future bounded workstreams start from then-current protected main
```

Temporary handoffs do not belong on protected main; current specifications must not become append-only diaries.
