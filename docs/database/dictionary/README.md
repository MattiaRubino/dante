# DANTE Database Dictionary

- **Status:** CURRENT / MATERIALIZED FOR CHECKED-OUT REPOSITORY STATE
- **Schema version:** 1
- **Serialization:** JSON
- **PostgreSQL:** 18.6
- **Protected-main Alembic head:** `20260906_18`
- **Protected-main topology:** `89|5|18|77|173|91|272|0|0|0`
- **Current candidate Alembic head on `feature/timeline-temporal-operational`:** `20260914_23`
- **Current candidate topology:** `95|5|23|77|190|110|284|0|0|0`
- **Frozen CP6 head:** `20260826_08`
- **Last reconciled:** 2026-09-14

## 1. Purpose

Machine-readable companion to the current DANTE Database System of Record.

```text
Current checked-out DB Reference
≈ Database Dictionary
≈ SQLAlchemy MetaData / mappings
≈ Alembic
≈ real PostgreSQL
≈ direct tests
```

A mismatch is a defect.

Protected `main` remains integration authority. The `_23` materialization documented here is candidate truth only on `feature/timeline-temporal-operational` until the applicable workstream gates complete and protected-main merge/readback occurs.

## 2. Current checked-out business-schema inventory

Candidate workstream materialization:

```text
tables       95
views         5
routines     23
standalone  123
triggers     77
indexes      190
FKs          110
CHECKs       284
```

The cumulative delta over protected-main `_18 / 89|5|18|77|173|91|272` is exactly:

```text
B01 / 20260908_19
+ dante.activity_intention                         table
+ dante.activity_create_operation                  table
+ dante.create_self_activity(...)                  routine
+ 4 physical indexes
+ 4 foreign keys
+ 3 CHECK constraints

B02-A / 20260909_20
+ dante.schedule_establish_operation               table
+ dante.establish_self_floating_schedule(...)      routine
+ 4 physical indexes
+ 4 foreign keys
+ 2 CHECK constraints

B02-A ACL hardening / 20260909_21
+ no structural object
- direct dante_runtime SELECT on schedule_establish_operation

B02-C / 20260913_22
+ dante.schedule_revision_operation                table
+ dante.revise_self_floating_schedule(...)         routine
+ 3 physical indexes
+ 4 foreign keys
+ 2 CHECK constraints

B02-D / 20260914_23
+ dante.schedule_unschedule_operation              table
+ dante.schedule_unschedule_undo_operation         table
+ dante.unschedule_self_schedule(...)              routine
+ dante.undo_self_schedule_unschedule(...)         routine
+ 6 physical indexes
+ 7 foreign keys
+ 5 CHECK constraints
```

No enum/domain, sequence, materialized view, partitioned table or RLS policy is introduced by B01, B02-A, B02-C or B02-D. Platform Observability adds no Dictionary business object, Alembic revision or SQLAlchemy business mapping.

## 3. Frozen CP6 baseline vs current materialization

`expected_baseline` remains exactly:

```text
68 tables / 5 views / 14 routines / 87 standalone
75 triggers / 95 indexes / 68 FKs / 120 CHECKs
```

Current candidate `current_materialization` is:

```text
95 tables / 5 views / 23 routines / 123 standalone
77 triggers / 190 indexes / 110 FKs / 284 CHECKs
```

`completed_stages` remains CP6 provenance only. Recovery, Access/Auth, Email, pre-vertical context and Timeline vertical provenance are represented per object through `implementation.introducing_stage`, `alembic_revision` and `runtime_acl_stage`; no fictitious CP6 stage is invented.

## 4. Post-CP6 evolution

```text
RECOVERY
20260830_09

ACCESS/AUTH
20260827_09
20260827_10
20260829_11
20260830_12
20260831_13

SHARED EMAIL PLATFORM
20260903_14
20260903_15
20260904_16

CONVERGENCE
20260904_17
  no-DDL Alembic merge revision

PRE-VERTICAL AUTHENTICATED DANTE CONTEXT
20260906_18
  protected-main head

TIMELINE / TEMPORAL-OPERATIONAL B01 CANDIDATE
20260908_19
  activity_intention
  activity_create_operation
  create_self_activity(...)

TIMELINE / TEMPORAL-OPERATIONAL B02-A CANDIDATE
20260909_20
  schedule_establish_operation
  establish_self_floating_schedule(...)

20260909_21
  forward-only ACL hardening; no structural topology delta

TIMELINE / TEMPORAL-OPERATIONAL B02-C CANDIDATE
20260913_22
  schedule_revision_operation
  revise_self_floating_schedule(...)

TIMELINE / TEMPORAL-OPERATIONAL B02-D CANDIDATE
20260914_23
  schedule_unschedule_operation
  schedule_unschedule_undo_operation
  unschedule_self_schedule(...)
  undo_self_schedule_unschedule(...)
```

Candidate workstream evolution does not become protected-main truth merely because it exists in this Dictionary branch.

## 5. Timeline vertical persistence classification

### 5.1 B01 Activity

`dante.activity` remains the single LR-01 Activity NativeRef owner materialized by CP6.

B01 adds only:

```text
activity_intention
= typed canonical dependent descriptor for the existing Activity

activity_create_operation
= immutable technical idempotency/control receipt

create_self_activity(...)
= bounded runtime capability surface
```

Permanent boundaries preserved:

```text
Activity identity != activity_intention row
Activity != operation receipt
operation id != NativeRef
create capability != generic runtime DML authority
Activity != Schedule != Session != Actual != Outcome
```

### 5.2 B02-A Schedule establishment

`dante.schedule` remains the CP6 scoped Schedule owner. B02-A does not create a second Schedule identity or generic calendar object.

B02-A adds only:

```text
schedule_establish_operation
= immutable operation/idempotency control receipt

establish_self_floating_schedule(...)
= bounded capability establishing one accepted floating-local interval placement
```

The capability composes existing CP6 objects:

```text
Activity NativeRef
→ Schedule ScopedRecordRef
→ schedule.placement MaterialStateRef
→ typed floating-local interval payload
→ explicit scoped current binding
→ Schedule current-history episode
```

Permanent boundaries preserved:

```text
Activity != Schedule
Schedule != Temporal Constraint != Session != Actual
Schedule identity != placement MaterialState
current accepted placement != newest row
operation id != Schedule identity != MaterialState identity
receipt != canonical Schedule truth
runtime capability != generic Schedule DML
```

`20260909_21` removes direct runtime `SELECT` from the receipt table. Runtime receives only the capability and the pre-existing/read-model SELECT surfaces required for the product read path.

### 5.3 B02-C Schedule placement revision

`dante.schedule` remains the stable owner. B02-C adds one immutable revision receipt and one bounded capability. A successful revision creates a new `schedule.placement` MaterialStateRef, closes the prior open current-history episode, moves the explicit current binding and opens one new episode. It never overwrites the prior payload, clones the Activity/Schedule, or creates Actual/Session truth.

The exact expected-state basis is the currently accepted placement MaterialStateRef. Same operation plus same intent replays the recorded effect; different reuse conflicts; a stale expected state is rejected before any replacement state is committed. Runtime receives EXECUTE on the capability and no direct receipt/current/history DML.

### 5.4 B02-D Schedule unschedule and guarded Undo

Unschedule records true absence: it closes the exact current placement-history episode and removes only the explicit current binding. Activity, Schedule, placement MaterialState and history remain retained; no placeholder or fake MaterialState represents absence.

Undo is authorized by the exact self-scoped unschedule receipt and only while the Schedule remains absent with no later placement-history episode. Acceptance copies the prior floating-local interval into a new immutable MaterialStateRef and opens a new current-history episode. It never reopens the old row. Both capabilities are idempotent by operation plus intent, and runtime has EXECUTE only.

## 6. Object contract

Every standalone business-schema object records object identity, purpose, classification, semantic traceability, implementation provenance, exact structure, lifecycle/state-history semantics, security/ACL and proof obligations.

Embedded table objects remain PK/FK/UQ/CHECK/index/trigger attachments. Routines remain standalone because signature/security/search-path/ACL are independently governed.

## 7. Shared Email classification

Email delivery objects are `family=email_platform` shared technical infrastructure. Access/Auth is a consumer, not platform owner. They are not MaterialState and are not a generic event-bus/outbox root.

## 8. Operational observer scope

`dante_observer` is deliberately **outside the business-object inventory above**. It is a provisioning-owned PostgreSQL operational role, not a table/view/routine/model and therefore must not be represented as fake Dictionary business materialization.

Its exact security contract is current authority in:

- `../dante-postgresql-database-part-12.md` — Section 46 / `DANTE-OBSERVABILITY-OBSERVER-CONTRACT v1`
- `../README.md` — observer-role routing
- `../../../infra/observability/README.md` — collector usage
- provisioning and live PostgreSQL ACL tests

Required posture remains `LOGIN NOINHERIT`, `pg_read_all_stats` membership with `INHERIT TRUE / SET FALSE / ADMIN FALSE`, `search_path=pg_catalog`, no database `CREATE`/`TEMP`, no DANTE/public business-object access and no DANTE application-role membership.

## 9. Validation

Required:

```text
JSON Schema consistency
filename/object-key agreement
FK/trigger target resolution
scope counts ↔ object tree
Dictionary ↔ SQLAlchemy ↔ Alembic ↔ PostgreSQL
owner/ACL parity
routine search_path/security parity
extension-owned objects excluded correctly
observer technical-role/provisioning/live-ACL parity
```

`test_current_catalog.py` and `test_database_current_catalog.py` are current live cross-representation gates. `test_migrations.py` proves current Alembic authority plus independent B01, B02-A, B02-C and B02-D fail-closed downgrade protection. Historical CP6 tests independently prove the frozen CP6 baseline. Platform Observability PostgreSQL acceptance additionally proves the exact observer-role boundary.

For B01, `create_self_activity` receives dedicated exact runtime proof of owner, SECURITY DEFINER posture, volatility/parallel safety, trusted search path and EXECUTE boundary; generic table ACL reconciliation proves runtime can read `activity_intention` but cannot directly mutate B01 persistence or inspect `activity_create_operation`.

For B02-A, `establish_self_floating_schedule` receives the same exact capability proof. Generic table ACL reconciliation proves `schedule_establish_operation` has no runtime table privilege after `_21`, while the application exercises the capability and Timeline read path through real PostgreSQL. B02-C adds equivalent obligations for governed revision. B02-D adds candidate obligations for exact-current withdrawal, retained absence, exact-receipt guarded Undo, monotonic new-state restoration and immutable replay; B02-D evidence remains pending until the deliberately deferred test gate runs.

## 10. Same-change rule

No real business object → no ceremonial Dictionary entry. Every real current DANTE business object requires a matching Dictionary entry and same-change reconciliation.

Operational-role contracts remain same-change governed through their dedicated technical-role reference, provisioning and live privilege tests rather than by inventing business Dictionary objects.

A candidate schema may update the checked-out Dictionary before merge, but must remain explicitly labeled candidate until protected-main integration. Green automated evidence and manual workstream acceptance remain separate gates.
