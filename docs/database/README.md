# DANTE Database System of Record

- **Status:** CURRENT / AUTHORITATIVE DATABASE REFERENCE
- **Last reconciled:** 2026-09-19
- **PostgreSQL:** 18.6
- **Protected-main Alembic head:** `20260906_18`
- **Protected-main topology:** `89|5|18|77|173|91|272|0|0|0`
- **Timeline candidate branch:** `feature/timeline-temporal-operational`
- **Timeline candidate Alembic head:** `20260919_34`
- **Timeline candidate topology:** `107|5|34|85|212|129|309|0|0|0`
- **Pre-vertical integration:** PR #66 / merge `1ecd58145860aebfaaa3dc1bd356b90f7a8eb19b` is protected-main historical context
- **Authenticated DANTE context authority:** `../architecture/authenticated-dante-context.md`
- **Timeline candidate DB overlay:** `timeline-temporal-operational.md`
- **Persistence doctrine:** `../development/backend-cp6-02-postgresql-persistence-constitution.md`
- **Persistence ADR:** `../decisions/ADR-010-postgresql-persistence-constitution.md`
- **Timeline workstream authority:** `../workstreams/timeline-temporal-operational-map.md`
- **Pre-B04 governance closure:** `../workstreams/timeline-temporal-operational-pre-b04-governance-2026-09-18.md`
- **B04-A closure:** `../workstreams/timeline-temporal-operational-b04-a-closure-2026-09-18.md`
- **B04-B closure:** `../workstreams/timeline-temporal-operational-b04-b-closure-2026-09-19.md`

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

Protected `main` remains integration authority. Candidate truth is never relabeled as protected-main truth before its applicable integration gates and merge/readback.

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
20260918_30 b04_temporal_constraint_core         [B04-A]
    ↓
20260918_31 b04_temporal_constraint_totality_hardening
    ↓
20260918_32 b04_current_history_dispatch_hardening
    ↓
20260918_33 b04_temporal_constraint_api_activation [B04-A closure]
    ↓
20260919_34 b04_absolute_boundary_deadline       [B04-B closure / current candidate head]
```

No accepted historical migration was edited, rebased, renumbered or flattened.

`_34` is a forward semantic expansion of the existing Temporal Constraint boundary payload. It adds one governed mutation routine but no table/view/trigger/index/FK/CHECK object count.

## 3. Current candidate topology

```text
107 tables
5 views
34 routines
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

This topology was read directly from PostgreSQL 18.6 and is the accepted Timeline candidate topology through `_34`. The exact machine-readable inventory is `dictionary/scope.json` plus the per-object Dictionary tree.

## 4. Timeline persistence classification

### B01 Activity

`dante.activity` remains the CP6 Activity NativeRef owner. B01 added the narrow descriptor/control surface:

```text
activity_intention
activity_create_operation
create_self_activity(...)
```

### B02 Schedule

`dante.schedule` remains the single shared CP6 Schedule owner. B02 composes the accepted placement MaterialState/current/history machinery and the accepted placement union:

```text
date_span
floating_local
named_zone_local
absolute
coarse_local_period
```

### B03 Event

`dante.event` remains the CP6 Event NativeRef owner. B03 adds Event expectation/create truth and ordered Agenda/internal values while reusing the shared Schedule engine.

### B04 Temporal Constraint

Temporal Constraint is a stable `ScopedRecordRef` LR-05 dependent. It is not a NativeRef root, Schedule placement, Movement Policy, Recurrence or evidence of Actual realization.

Canonical/control surface:

```text
temporal_constraint
temporal_constraint_state
temporal_constraint_boundary_state
temporal_constraint_boundary_absolute_state
temporal_constraint_current_history
temporal_constraint_mutation_operation

enforce_temporal_constraint_rule_totality()
mutate_self_absolute_earliest_start_constraint(...)
mutate_self_absolute_boundary_constraint(...)
```

The bounded control engine remains shared:

```text
scoped_address                     + temporal_constraint
material_state_address             + temporal_constraint.rule
scoped_current_material_state      + temporal_constraint.rule
shared owner/ref/totality/history dispatchers extended
```

#### B04-A ✅ CLOSED / PROVEN

B04-A established the first complete rule:

```text
subject             self-owned Activity | Event
family              boundary
boundary kind       earliest_start
constrained facet   schedule.start
strength            hard | soft
temporal form       absolute
boundary value      finite timestamptz
```

`_33` closed the application/API activation gap: replay accepts replacement server-generated UUIDs while returning the originally accepted refs, and runtime receives only the narrow current-rule SELECT surface needed by Get/List.

#### B04-B ✅ CLOSED / PROVEN

`_34` expands the exact absolute boundary matrix to:

```text
earliest_start     + schedule.start
latest_start       + schedule.start
latest_completion  + schedule.completion
```

Database invariants require those exact pairings. Unsupported pairings fail at deferred totality. `temporal_form_code` remains exactly `absolute` for B04-B.

The generic B04-B capability is `mutate_self_absolute_boundary_constraint(...)`. The B04-A `mutate_self_absolute_earliest_start_constraint(...)` routine remains present for compatibility.

Permanent boundaries include:

```text
Activity != Event
Event != Schedule
Schedule != Temporal Constraint
Temporal Constraint != Movement Policy
Temporal Constraint != Recurrence
Temporal Constraint != Session / Actual
constraint revision != Schedule revision
deadline != Schedule end
passed deadline != Actual
passed deadline != Outcome / failure
current accepted state != newest row
idempotency key != Domain identity
```

B04-C+ windows/preferences/evaluation, Movement Policy, advanced duration/spacing/relative families and solver semantics remain outside current persistence authority.

## 5. Proof state

```text
B01 Activity Core                    CLOSED / PROVEN
B02 Schedule Core                    CLOSED / PROVEN at 20260915_26
B03 Event Core                       CLOSED / PROVEN at 20260917_29
B04-A overall                        CLOSED / PROVEN at 20260918_33
B04-B overall                        CLOSED / PROVEN at 20260919_34
B04 overall                          IN PROGRESS
```

B04-B local evidence:

```text
API / typed union / inventory                 13 PASS
PostgreSQL/application/catalog                22 PASS / 1 deselected
OpenAPI export/inventory/API                  21 PASS
@dante/api-client typecheck                   PASS
@dante/api-client Vitest                      11 PASS
pnpm generated:check                          PASS / 163 files deterministic
```

The next persistence slice is B04-C Windows / Preferences / Evaluation. No B04-C object or schema change is pre-authorized by B04-B closure.

## 6. Runtime role model

```text
dante_owner      NOLOGIN ownership identity
dante_migrator   LOGIN migration identity
dante_runtime    LOGIN application runtime identity
dante_observer   LOGIN statistics-only collector identity
```

Business migrations own the exact ACL delta for the objects/capabilities they create or alter. Runtime receives only the narrow capability required by the accepted application contract. Temporal Constraint direct business-object writes remain governed through mutation routines.

## 7. Recovery boundary

The accepted recovery doctrine is unchanged. Timeline candidate state is ordinary canonical/control state and must participate in the same recovery/anti-resurrection discipline when the whole vertical reaches its applicable recovery closure. Local B04 candidate proof is not represented as production/cloud recovery proof.

## 8. Same-change rule — binding

A database-affecting slice is incomplete until every affected current representation is reconciled in the same reviewed change:

```text
Alembic
≈ SQLAlchemy mappings / MetaData
≈ Database Dictionary entries + scope counts
≈ real PostgreSQL catalog / current-catalog tests
≈ object owners / ACL
≈ docs/database/README.md
≈ active feature DB overlay
≈ direct PostgreSQL proof
≈ affected workstream map / roadmap / closure evidence
```

No slice can be marked CLOSED / PROVEN while a known affected current representation is stale.
