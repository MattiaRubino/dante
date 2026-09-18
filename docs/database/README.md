# DANTE Database System of Record

- **Status:** CURRENT / AUTHORITATIVE DATABASE REFERENCE
- **Last reconciled:** 2026-09-18
- **PostgreSQL:** 18.6
- **Protected-main Alembic head:** `20260906_18`
- **Protected-main topology:** `89|5|18|77|173|91|272|0|0|0`
- **Timeline candidate branch:** `feature/timeline-temporal-operational`
- **Timeline candidate Alembic head:** `20260918_32`
- **Timeline candidate topology:** `107|5|33|85|212|129|309|0|0|0`
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
- **B04-A implementation freeze:** `../workstreams/timeline-temporal-operational-b04-a-implementation-freeze.md`

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
20260906_18 account_application_context          [protected-main authority]
    ↓
20260908_19 activity_core                        [B01]
    ↓
20260909_20 b02_schedule_establish               [B02-A]
    ↓
20260909_21 b02_schedule_acl_hardening
    ↓
20260913_22 b02_schedule_revision                [B02-C]
    ↓
20260914_23 b02_schedule_unschedule_undo         [B02-D]
    ↓
20260914_24 b02_schedule_plpgsql_disambiguation
    ↓
20260915_25 b02_schedule_form_completeness       [B02-E]
    ↓
20260915_26 b02_named_zone_gap_resolution        [B02 closure]
    ↓
20260916_27 b03_event_core                       [B03-A]
    ↓
20260917_28 b03 shared Event/Schedule activation [B03-B]
    ↓
20260917_29 b03_event_agenda                     [B03-D / B03 closure]
    ↓
20260918_30 b04_temporal_constraint_core         [B04-A canonical core]
    ↓
20260918_31 b04_temporal_constraint_totality_hardening
    ↓
20260918_32 b04_current_history_dispatch_hardening [current candidate head]
```

No accepted historical migration was edited, rebased, renumbered or flattened. `_31` and `_32` are forward hardening revisions because already-materialized candidate databases must converge to the same accepted B04-A behavior as a fresh migration.

## 3. Current candidate topology

```text
107 tables
5 views
33 routines
85 triggers
212 physical indexes
129 foreign keys
309 CHECK constraints
0 enums/domains
0 sequences
0 materialized views
0 partitioned tables
0 RLS policies
```

This topology was read directly from PostgreSQL 18.6 migrated through `_32` by the B04-A catalog/ACL proof. The exact machine-readable inventory is `dictionary/scope.json` plus the per-object Dictionary tree. Prose counts are a convenience view and must never override that inventory or the live PostgreSQL catalog.

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

### B04-A Temporal Constraint canonical core

Temporal Constraint is a stable `ScopedRecordRef` LR-05 dependent. It is not a NativeRef root, Schedule placement, Movement Policy, Recurrence or evidence of Actual realization.

B04-A materializes:

```text
temporal_constraint
temporal_constraint_state
temporal_constraint_boundary_state
temporal_constraint_boundary_absolute_state
temporal_constraint_current_history
temporal_constraint_mutation_operation

enforce_temporal_constraint_rule_totality()
mutate_self_absolute_earliest_start_constraint(...)
```

The first complete typed rule path is deliberately narrow and real rather than placeholder-shaped:

```text
subject             self-owned Activity | Event
family              boundary
boundary kind       earliest_start
constrained facet   schedule.start
strength            hard | soft
temporal form       absolute
boundary value      finite timestamptz
```

The existing bounded control engine is extended rather than duplicated:

```text
scoped_address                     + temporal_constraint
material_state_address             + temporal_constraint.rule
scoped_current_material_state      + temporal_constraint.rule
shared owner/ref/totality/history dispatchers extended
```

`_31` closes cross-family MaterialState totality in both directions. `_32` hardens the shared current-history dispatcher so each owner-specific history table dereferences only its own identity column.

Create/revise/retire use expected-state CAS and immutable idempotency receipts. Revision appends a new rule MaterialState and moves currentness; retire closes the open current-history episode and removes only the current binding. Stable constraint identity and history remain.

Permanent boundaries include:

```text
Activity != Event
Event != Schedule
Schedule != Temporal Constraint
Temporal Constraint != Movement Policy
Temporal Constraint != Recurrence
Temporal Constraint != Session / Actual
constraint revision != Schedule revision
current accepted state != newest row
idempotency key != Domain identity
provider identity != DANTE identity
```

B04-B+ deadline/boundary expansion, windows/preferences, Movement Policy, advanced duration/spacing/relative families and solver semantics remain outside B04-A.

## 5. Proof state

```text
B01 Activity Core                    CLOSED / PROVEN
B02 Schedule Core                    CLOSED / PROVEN at 20260915_26
B03 Event Core                       CLOSED / PROVEN at 20260917_29
B04-A A1 DDL / SQLAlchemy            PROVEN
B04-A A2 PostgreSQL / catalog / ACL  PROVEN at 20260918_32
B04-A A3 CAS / idempotency           PROVEN
B04-A A4 DB / Dictionary / docs      MATERIALIZED; reconciliation tests pending
B04-A A5 application / API           NOT STARTED
B04-A overall                        IN PROGRESS
B04 overall                          IN PROGRESS
```

Current B04-A proof already includes focused create/revise/retire/CAS/idempotency tests, Activity/Event subject integrity, runtime direct-bypass rejection, MaterialState exclusivity, shared current-history dispatch regression, broad Temporal/CP6 regression, and direct `_32` topology/owner/ACL proof. A4 is not closed merely because these references were edited; current-catalog/Dictionary parity must run green on the reconciled tree.

## 6. Runtime role model

Current protected-main and candidate role vocabulary is:

```text
dante_owner      NOLOGIN ownership identity
dante_migrator   LOGIN migration identity
dante_runtime    LOGIN application runtime identity
dante_observer   LOGIN statistics-only collector identity
```

Business migrations own the exact ACL delta for the objects/capabilities they create or alter. B04-A tables expose no generic runtime DML; runtime receives EXECUTE only on the governed mutation function. Runtime does not receive blanket business-object DML merely because a table exists.

## 7. Recovery boundary

The accepted recovery doctrine is unchanged. Timeline candidate state is ordinary canonical/control state and must participate in the same recovery/anti-resurrection discipline when the whole vertical reaches its applicable recovery closure. No local B04-A candidate proof is represented as production/cloud recovery proof.

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

The pre-B04 governance closure remains binding for all B04+ Timeline work.
