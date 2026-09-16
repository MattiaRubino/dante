# DANTE Database System of Record

- **Status:** CURRENT / AUTHORITATIVE DATABASE REFERENCE
- **Last reconciled:** 2026-09-16
- **PostgreSQL:** 18.6
- **Protected-main Alembic head:** `20260906_18`
- **Protected-main topology:** `89|5|18|77|173|91|272|0|0|0`
- **Timeline candidate branch:** `feature/timeline-temporal-operational`
- **Timeline candidate Alembic head:** `20260916_27`
- **Timeline candidate topology:** `98|5|29|78|195|115|288|0|0|0`
- **Pre-vertical integration:** PR #66 / merge `1ecd58145860aebfaaa3dc1bd356b90f7a8eb19b` is historical context only; protected-main identity remains repository authority
- **Authenticated DANTE context authority:** `../architecture/authenticated-dante-context.md`
- **Access/Auth reference:** `access-auth.md`
- **Shared Email Platform authority:** `../architecture/email-platform.md`
- **Recovery operator authority:** `../operations/postgres-recovery-runbook.md`
- **Persistence doctrine:** `../development/backend-cp6-02-postgresql-persistence-constitution.md`
- **Persistence ADR:** `../decisions/ADR-010-postgresql-persistence-constitution.md`
- **Timeline workstream authority:** `../workstreams/timeline-temporal-operational-map.md`
- **B02 closure authority:** `../workstreams/timeline-temporal-operational-b02-closure-2026-09-16.md`
- **B03 authority:** `../workstreams/timeline-temporal-operational-b03-execution-plan.md`

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
20260915_26 b02_named_zone_gap_resolution     [B02 closure]
    ↓
20260916_27 b03_event_core                    [B03-A current candidate head]
```

No accepted historical migration was edited, rebased or flattened.

## 3. Current candidate topology

```text
98 tables
5 views
29 routines
78 triggers
195 physical indexes
115 foreign keys
288 CHECK constraints
0 enums/domains
0 sequences
0 materialized views
0 partitioned tables
0 RLS policies
```

`_27` adds exactly two Event-owned/control tables and one bounded Event create routine over the B02 closure state:

```text
event_expectation
event_create_operation
create_self_event(...)
```

No Event-specific Schedule table or scheduling engine was introduced.

## 4. Timeline persistence classification

### B01 Activity

`dante.activity` remains the CP6 Activity NativeRef owner. B01 adds the narrow dependent/control surface:

```text
activity_intention
activity_create_operation
create_self_activity(...)
```

### B02 Schedule

`dante.schedule` remains the single CP6 Schedule owner. B02 composes the existing Schedule placement MaterialState/current/history machinery and accepted placement union:

```text
date_span
floating_local
named_zone_local
absolute
coarse_local_period
```

The physical Schedule subject family remains `activity | event | occurrence`. B02 product-activated Activity; B03 must reuse the same Schedule owner for Event.

### B03-A Event

`dante.event` remains the CP6 Event NativeRef owner. B03-A adds only the minimum self-scoped expected-occurrence descriptor and technical create receipt:

```text
event_expectation
event_create_operation
create_self_event(...)
```

The Event descriptor contains title/self ownership/creation chronology only. Schedule placement, Recurrence, Participation, Session, Actual, Outcome, provider identity and generic status remain separate owners/capabilities.

Permanent boundaries include:

```text
Activity != Event
Event != Schedule
Event != Recurrence != Occurrence
Event != Session != Actual != Outcome
Event identity != operation identity
Event identity != provider identity
Schedule identity != placement MaterialState
current accepted placement != newest row
```

## 5. Proof state

B02 remains closed/proven at `_26`.

B03-A first real-stack proof executed on 2026-09-16:

```text
apps/backend/tests/integration/temporal/test_b03_event_core.py
2 / 2 PASS
```

The `_27` Dictionary/current-catalog/migration reconciliation is part of the same B03-A slice and must be green before B03-A is labeled CLOSED/PROVEN.

## 6. Runtime role model

Application roles remain:

```text
dante_owner      NOLOGIN ownership identity
dante_migrator   LOGIN migration identity
dante_runtime    LOGIN application runtime identity
dante_observer   LOGIN statistics-only collector identity
```

For B03-A, runtime receives `SELECT` on `event_expectation` and bounded `EXECUTE` on `create_self_event(...)`; it receives no generic Event/receipt DML.

## 7. Recovery boundary

The accepted recovery doctrine remains unchanged. B03-A adds ordinary canonical/control state only. Whole-vertical recovery/anti-resurrection closure remains B15; no production/cloud recovery claim is implied by local candidate proof.

## 8. Same-change rule

No real business object → no ceremonial Dictionary entry. Every real current business object requires matching Dictionary/Alembic/SQLAlchemy/catalog/ACL proof. Candidate branch truth remains explicitly distinct from protected-main truth until integration.