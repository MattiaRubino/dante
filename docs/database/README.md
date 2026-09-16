# DANTE Database System of Record

- **Status:** CURRENT / AUTHORITATIVE DATABASE REFERENCE
- **Last reconciled:** 2026-09-16
- **PostgreSQL:** 18.6
- **Protected-main Alembic head:** `20260906_18`
- **Protected-main topology:** `89|5|18|77|173|91|272|0|0|0`
- **Timeline candidate branch:** `feature/timeline-temporal-operational`
- **Timeline candidate Alembic head:** `20260915_26`
- **Timeline candidate topology:** `96|5|28|78|191|111|285|0|0|0`
- **Pre-vertical integration:** PR #66 / merge `1ecd58145860aebfaaa3dc78933f4ee42698f33b` is historical context only; protected-main identity remains repository authority
- **Authenticated DANTE context authority:** `../architecture/authenticated-dante-context.md`
- **Access/Auth reference:** `access-auth.md`
- **Shared Email Platform authority:** `../architecture/email-platform.md`
- **Recovery operator authority:** `../operations/postgres-recovery-runbook.md`
- **Persistence doctrine:** `../development/backend-cp6-02-postgresql-persistence-constitution.md`
- **Persistence ADR:** `../decisions/ADR-010-postgresql-persistence-constitution.md`
- **Timeline workstream authority:** `../workstreams/timeline-temporal-operational-map.md`
- **B02 closure authority:** `../workstreams/timeline-temporal-operational-b02-closure-2026-09-16.md`
- **B03 pre-scope authority:** `../workstreams/timeline-temporal-operational-b03-execution-plan.md`

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

Protected `main` is the integration authority. Candidate truth becomes protected-main truth only after the applicable workstream/integration gates. This document therefore records protected-main truth and the current checked-out Timeline candidate separately.

## 2. Current migration graph

The Timeline candidate extends the protected-main `20260906_18` only through forward revisions:

```text
20260906_18 account_application_context       [protected-main authority]
    ↓
20260908_19 activity_core                     [B01]
    ↓
20260909_20 b02_schedule_establish            [B02-A]
    ↓
20260909_21 b02_schedule_acl_hardening
    ↓
20260913_22 b02_schedule_revision             [B02-C]
    ↓
20260914_23 b02_schedule_unschedule_undo      [B02-D]
    ↓
20260914_24 b02_schedule_plpgsql_disambiguation
    ↓
20260915_25 b02_schedule_form_completeness    [B02-E]
    ↓
20260915_26 b02_named_zone_gap_resolution     [current Timeline candidate head]
```

No accepted historical migration was edited, rebased or flattened.

## 3. Current candidate topology

```text
96 tables
5 views
28 routines
78 triggers
191 physical indexes
111 foreign keys
285 CHECK constraints
0 enums/domains
0 sequences
0 materialized views
0 partitioned tables
0 RLS policies
```

This topology is the reconciled B02 closure state and matches the current Dictionary `scope.json`, SQLAlchemy metadata, Alembic and the executed PostgreSQL current-catalog proof.

## 4. Timeline persistence classification through B02

### B01 Activity

`dante.activity` remains the CP6 Activity NativeRef owner. B01 adds the narrow dependent/control surface:

```text
activity_intention
activity_create_operation
create_self_activity(...)
```

No generic Task/status identity was introduced.

### B02 Schedule

`dante.schedule` remains the single CP6 Schedule owner. B02 composes the existing Schedule placement MaterialState/current/history machinery and adds bounded operation-control/capability surfaces for establishment, revision, unschedule and guarded Undo.

Accepted placement union at B02 closure:

```text
date_span
floating_local
named_zone_local
absolute
coarse_local_period
```

Permanent boundaries:

```text
Activity != Schedule
Event != Schedule
Schedule != Session != Actual
Schedule identity != placement MaterialState
current accepted placement != newest row
operation receipt != Schedule identity != MaterialState identity
unscheduled != deleted
Undo != history rewind
```

The Schedule physical subject family remains:

```text
activity | event | occurrence
```

B02 product-activated Activity only. B03 Event must reuse this Schedule owner rather than introduce Event-specific Schedule persistence.

## 5. B02 closure evidence

Executed candidate evidence at `_26`:

```text
Dictionary / SQLAlchemy / Alembic parity        PASS
current-catalog + migration PostgreSQL gate     20 / 20 PASS
repository HEAD → base → HEAD round-trip         1 / 1 PASS
B02 PostgreSQL proof group                      11 PASS / 2 deselected
```

The final B02 closure record carries the backend/web/full-stack evidence. This document does not relabel candidate truth as protected-main truth.

## 6. Runtime role model

Application roles remain:

```text
dante_owner      NOLOGIN ownership identity
dante_migrator   LOGIN migration identity
dante_runtime    LOGIN application runtime identity
dante_observer   LOGIN statistics-only collector identity
```

Runtime receives narrow SELECT/EXECUTE capability only. Operation receipt/current/history tables are not opened to generic runtime DML merely for application convenience. Security-definer routines must keep trusted search paths and exact ACL proof.

## 7. B03 database starting point

B03 pre-scope begins from `_26 / 96|5|28|78|191|111|285|0|0|0`.

Verified current Event/Schedule physical facts:

```text
dante.event                         exists as CP6 LR-01 NativeRef shell
SQLAlchemy EventRow                 exists
Schedule subject eligibility        activity | event | occurrence
Event product descriptor            MISSING
governed Event create receipt       MISSING
B02 Schedule self-scope routines    currently Activity-descriptor bound
```

Therefore B03 has a real narrow persistence gap for Event descriptive/create state, while **no Event-specific Schedule table is justified**.

Any B03 forward DDL must satisfy the same-change rule:

```text
semantic authority
+ forward Alembic
+ SQLAlchemy
+ Dictionary
+ this human DB reference
+ runtime ACL
+ direct PostgreSQL proof
```

Historical CP6/B01/B02 migrations remain immutable.

## 8. Recovery boundary

The accepted recovery doctrine remains unchanged. B02 introduces ordinary canonical/control state but no new provider/outbox family. Whole-vertical recovery/anti-resurrection closure remains B15; no production/cloud recovery claim is implied by local candidate proof.

## 9. Same-change rule

No real business object → no ceremonial Dictionary entry. Every real current business object requires matching Dictionary/Alembic/SQLAlchemy/catalog/ACL proof. A candidate branch may carry reconciled candidate documentation before protected-main integration, but the distinction must remain explicit.