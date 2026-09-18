# DANTE Database System of Record

- **Status:** CURRENT / AUTHORITATIVE DATABASE REFERENCE
- **Last reconciled:** 2026-09-18
- **PostgreSQL:** 18.6
- **Protected-main Alembic head:** `20260906_18`
- **Protected-main topology:** `89|5|18|77|173|91|272|0|0|0`
- **Timeline candidate branch:** `feature/timeline-temporal-operational`
- **Timeline candidate Alembic head:** `20260917_29`
- **Timeline candidate topology:** `101|5|31|78|198|119|297|0|0|0`
- **Pre-vertical integration:** PR #66 / merge `1ecd58145860aebfaaa3dc1bd356b90f7a8eb19b` is protected-main historical context
- **Authenticated DANTE context authority:** `../architecture/authenticated-dante-context.md`
- **Access/Auth reference:** `access-auth.md`
- **Timeline candidate DB overlay:** `timeline-temporal-operational.md`
- **Shared Email Platform authority:** `../architecture/email-platform.md`
- **Recovery operator authority:** `../operations/postgres-recovery-runbook.md`
- **Persistence doctrine:** `../development/backend-cp6-02-postgresql-persistence-constitution.md`
- **Persistence ADR:** `../decisions/ADR-010-postgresql-persistence-constitution.md`
- **Timeline workstream authority:** `../workstreams/timeline-temporal-operational-map.md`
- **Pre-B04 governance closure:** `../workstreams/timeline-temporal-operational-pre-b04-governance-2026-09-18.md`

## 1. Authority model

```text
Product / Domain / Logical / Physical
→ PostgreSQL Persistence Constitution / ADR-010
→ current human DB reference + Dictionary semantic contract
→ Alembic forward evolution
→ SQLAlchemy mappings/MetaData
→ real PostgreSQL catalog
→ direct tests / recovery proof
```

Permanent invariant:

```text
CURRENT DB REFERENCE
≈ DATABASE DICTIONARY
≈ SQLALCHEMY
≈ ALEMBIC
≈ REAL POSTGRESQL
≈ DIRECT TESTS
```

Protected `main` remains integration authority. Candidate truth is never relabeled as protected-main truth before its applicable integration gates and merge/readback. On the Timeline branch, this document records both protected-main truth and the checked-out candidate truth; `timeline-temporal-operational.md` is the feature-specific human overlay for candidate-only persistence.

## 2. Current migration graph

The Timeline candidate extends protected-main `20260906_18` only through forward revisions:

```text
20260906_18 account_application_context        [protected-main authority]
    ↓
20260908_19 activity_core                      [B01]
    ↓
20260909_20 b02_schedule_establish             [B02-A]
    ↓
20260909_21 b02_schedule_acl_hardening
    ↓
20260913_22 b02_schedule_revision              [B02-C]
    ↓
20260914_23 b02_schedule_unschedule_undo       [B02-D]
    ↓
20260914_24 b02_schedule_plpgsql_disambiguation
    ↓
20260915_25 b02_schedule_form_completeness     [B02-E]
    ↓
20260915_26 b02_named_zone_gap_resolution      [B02 closure]
    ↓
20260916_27 b03_event_core                     [B03-A]
    ↓
20260917_28 b03 shared Event/Schedule activation [B03-B; B03-C reuses shared lifecycle]
    ↓
20260917_29 b03_event_agenda                   [B03-D / B03 closure candidate head]
```

No accepted historical migration was edited, rebased, renumbered or flattened.

## 3. Current candidate topology

```text
101 tables
5 views
31 routines
78 triggers
198 physical indexes
119 foreign keys
297 CHECK constraints
0 enums/domains
0 sequences
0 materialized views
0 partitioned tables
0 RLS policies
```

The exact machine-readable inventory is `dictionary/scope.json` plus the per-object Dictionary tree. Prose counts are a convenience view and must never override that inventory or the live PostgreSQL catalog.

## 4. Timeline persistence classification

### B01 Activity

`dante.activity` remains the CP6 Activity NativeRef owner. B01 added the narrow descriptor/control surface:

```text
activity_intention
activity_create_operation
create_self_activity(...)
```

### B02 Schedule

`dante.schedule` remains the single shared CP6 Schedule owner. B02 composes the accepted placement MaterialState/current/history machinery and the complete currently accepted placement union:

```text
date_span
floating_local
named_zone_local
absolute
coarse_local_period
```

The physical Schedule subject family remains bounded to accepted owners; B03 activates Event against the same Schedule owner rather than creating `event_schedule`.

### B03 Event

`dante.event` remains the CP6 Event NativeRef owner. B03 adds only the Event-specific canonical/control truth that is actually required:

```text
event_expectation
event_create_operation
event_agenda_part
event_agenda_current
event_agenda_mutation_operation
create_self_event(...)
create_self_event_with_agenda(...)
replace_self_event_agenda(...)
```

B03-B generalizes the shared Schedule authorization/capability to Event. B03-C introduces no separate Event scheduling engine or DDL; it reuses shared Schedule revision/unschedule/Undo. B03-D adds ordered Event-internal Agenda truth with aggregate CAS/idempotency control.

Permanent boundaries include:

```text
Activity != Event
Event != Schedule
Event != Recurrence != Occurrence
Event != Session != Actual != Outcome
Agenda part != Activity/Event/Occurrence/Schedule/Session/Actual
Event identity != operation/idempotency identity
provider identity != DANTE Event identity
Schedule identity != placement MaterialState
current accepted placement != newest row
```

## 5. Proof state

```text
B01 Activity Core     CLOSED / PROVEN
B02 Schedule Core     CLOSED / PROVEN at 20260915_26
B03 Event Core        CLOSED / PROVEN at candidate 20260917_29
B04                   NOT STARTED; explicit gate remains APPROVE B04
```

B03 closure includes real PostgreSQL/API proof, Dictionary/Alembic/current-catalog reconciliation, shared Activity/Event Schedule regression, frontend/browser proof, manual acceptance and governed OpenAPI/client regeneration. Detailed proof authority remains in the B03 closure documents under `docs/workstreams/`.

## 6. Runtime role model

Current protected-main and candidate role vocabulary is:

```text
dante_owner      NOLOGIN ownership identity
dante_migrator   LOGIN migration identity
dante_runtime    LOGIN application runtime identity
dante_observer   LOGIN statistics-only collector identity
```

Business migrations own the exact ACL delta for the objects/capabilities they create or alter. Runtime does not receive blanket business-object DML merely because a table exists.

## 7. Recovery boundary

The accepted recovery doctrine is unchanged by B01-B03. Timeline candidate state is ordinary canonical/control state and must participate in the same recovery/anti-resurrection discipline when the whole vertical reaches its recovery closure. No local candidate proof is represented as production/cloud recovery proof.

## 8. Same-change rule — binding

A database-affecting slice is incomplete until every affected current representation is reconciled in the same reviewed change:

```text
Alembic
≈ SQLAlchemy mappings / MetaData
≈ Database Dictionary entries + scope counts
≈ real PostgreSQL catalog / current-catalog tests
≈ object owners / ACL
≈ docs/database/README.md
≈ active feature DB overlay (when candidate-only truth exists)
≈ protected-main architecture reference when protected-main truth changes
≈ direct PostgreSQL proof
≈ affected workstream map / roadmap / closure evidence
```

Rules:

- no real business object → no ceremonial Dictionary entry;
- no new column/table/routine/trigger/index/constraint without the corresponding structural and semantic representation;
- no candidate-only object may be described as protected-main materialization;
- no accepted historical migration is rewritten to make documentation easier;
- a mismatch between Dictionary, SQLAlchemy, Alembic, catalog, ACL or current human references is a defect, not acceptable lag;
- a slice cannot be marked CLOSED/PROVEN while a known affected current representation is stale.

The pre-B04 governance closure makes this gate explicit for all B04+ Timeline work.