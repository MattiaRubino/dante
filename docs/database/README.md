# DANTE Database System of Record

- **Status:** CURRENT / AUTHORITATIVE DATABASE REFERENCE
- **Last reconciled:** 2026-09-23
- **PostgreSQL:** 18.6
- **Protected-main Alembic head:** `20260906_18`
- **Protected-main topology:** `89|5|18|77|173|91|272|0|0|0`
- **Timeline candidate branch:** `feature/timeline-temporal-operational`
- **Timeline candidate Alembic head:** `20260924_58`
- **Timeline candidate topology awaiting local proof:** `148|5|94|93|290|229|414|0|0|0`
- **Timeline candidate DB overlay:** `timeline-temporal-operational.md`
- **Persistence doctrine:** `../development/backend-cp6-02-postgresql-persistence-constitution.md`
- **Persistence ADR:** `../decisions/ADR-010-postgresql-persistence-constitution.md`
- **Timeline workstream authority:** `../workstreams/timeline-temporal-operational-map.md`
- **Post-B06 scope decision:** `../workstreams/timeline-temporal-operational-post-b06-scope-decision-2026-09-23.md`
- **Whole-B06 closure:** `../workstreams/timeline-temporal-operational-b06-e-closure-2026-09-23.md`

## 1. Authority model

```text
Product / Domain / Logical / Physical
→ PostgreSQL Persistence Constitution / ADR-010
→ current human DB reference + Dictionary semantic contract
→ Alembic forward evolution
→ SQLAlchemy mappings / MetaData
→ real PostgreSQL catalog
→ direct tests
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

Protected `main` remains integration authority. Candidate truth is never relabeled as protected-main truth before merge/readback.

## 2. Current Timeline migration graph

```text
20260906_18 protected-main baseline
    ↓
20260908_19 B01 Activity core
    ↓
20260909_20 → 20260915_26 B02 Schedule core / closure
    ↓
20260916_27 → 20260917_29 B03 Event core / closure
    ↓
20260918_30 → 20260918_33 B04-A Temporal Constraint core / API activation
    ↓
20260919_34 B04-B absolute boundary / deadline
    ↓
20260919_35 → 20260919_36 B04-C absolute windows / runtime-read ACL
    ↓
20260919_37 → 20260919_39 B04-D Movement Policy / governed move / replay fix
    ↓
20260919_40 → 20260919_41 B04-E planned Schedule duration + runtime-read ACL
    ↓
20260920_42 B04-F Schedule hard-constraint guard
    ↓
20260920_43 → 20260920_45 B05-A Life Area lifecycle
    ↓
20260920_46 B05-B typed primary Life Area assignment
    ↓
20260920_47 B05-C secondary Tags
    ↓
20260921_48 B05-D postponed Event discovery/replan composition
    ↓
20260921_49 → 20260921_51 B06-A Routine source/core corrections
    ↓
20260922_52 → 20260922_54 B06-B Recurrence authoring/read validation
    ↓
20260922_55 B06-C bounded Occurrence checkpoint/control
    ↓
20260922_56 B06-D Occurrence authorization in shared Schedule capabilities
    ↓
20260923_57 B06-D bounded execute-only expected-Occurrence Timeline read
```

`_57` is the current proven candidate database frontier after **whole-B06 closure**. B06-E introduced no further migration.

No accepted historical migration was edited, rebased, renumbered or flattened.

## 3. Current candidate topology

```text
145 tables
5 views
88 routines
92 triggers
285 physical indexes
223 foreign keys
408 CHECK constraints
0 enums/domains
0 sequences
0 materialized views
0 partitioned tables
0 RLS policies
```

`_56` changed existing shared Schedule capability ownership predicates. `_57` added exactly one bounded SECURITY DEFINER expected-Occurrence read routine; it did not widen direct runtime table privileges on private Occurrence/Routine provenance tables.

## 4. Timeline persistence classification

### B01 Activity

`dante.activity` remains the Activity NativeRef owner. Activity can exist unplaced; Activity identity is not Schedule identity.

### B02 Schedule

`dante.schedule` remains the single shared accepted-placement authority. Current/history/CAS/idempotency/Undo semantics remain independent from Activity/Event/Routine/Occurrence identity.

### B03 Event

`dante.event` remains a distinct NativeRef owner while reusing shared Schedule authority. Agenda remains Event-internal ordered value truth.

### B04 Temporal Constraint / Movement Policy

Temporal Constraint is a stable dependent with typed boundary/window/planned-duration MaterialState semantics. Movement Policy is a separate Schedule-owned governance facet.

```text
Schedule != Temporal Constraint
Schedule != Movement Policy
Temporal Constraint != Movement Policy
Movement Policy != solver result
proposal != accepted effect
```

Deterministic application evaluation remains derived/non-persistent and does not search for candidate schedules.

### B05 Product Organization

Life Area and secondary Tags are actor-local product organization structures, not new Domain identity owners. Activity/Event typed relations remain explicit; no generic relationship/EAV shortcut is introduced.

### B06 Routine / Recurrence / Occurrence

```text
Routine != Recurrence != Occurrence
Occurrence != Schedule
```

B06 uses owner-specific Routine/Event recurrence truth and canonical Occurrence identity/provenance. Materialized Occurrences reuse the **existing shared Schedule engine** rather than creating an `occurrence_schedule` authority.

Runtime read remains least privilege:

```text
scheduled Occurrence
→ shared Schedule read + get_self_occurrence

unscheduled expected Occurrence
→ list_self_expected_occurrences_in_window(...)

Routine presentation
→ list_self_routines
```

No direct runtime SELECT grant on private Occurrence provenance tables is required.

## 5. Permanent non-collapse invariants

```text
Activity != Event != Routine
Routine != Recurrence != Occurrence
Occurrence != Schedule
Schedule != Temporal Constraint
Schedule != Movement Policy
Schedule != Session != Actual
Session != Actual != Outcome
Actual != Outcome != Confirmation
Responsibility != Participation
planned Schedule duration != Activity estimated effort
planned Schedule duration != Session duration
planned Schedule duration != Actual duration
window != placement
preference != accepted Schedule
evaluation != solver decision
solver proposal != accepted Schedule
current accepted state != newest row
idempotency key != Domain identity
projection != canonical truth
```

B12 owns deterministic candidate generation/optimization and governed solver proposals. AI does not become canonical scheduling authority.

## 6. Proof state

```text
B01 Activity Core                     CLOSED / PROVEN
B02 Schedule Core                     CLOSED / PROVEN
B03 Event Core                        CLOSED / PROVEN
B04 overall                           CLOSED / PROVEN at `_42`
B05 overall                           CLOSED / PROVEN through `_48`
B06-A Routine core                    CLOSED / PROVEN at `_51`
B06-B Recurrence authoring            CLOSED / PROVEN at `_54`
B06-C Occurrence checkpoint           CLOSED / PROVEN at `_55`
B06-D Schedule + Timeline             CLOSED / PROVEN at `_57`
B06-E whole-block closure             CLOSED / PROVEN at `_57`
B06 overall                           CLOSED / PROVEN
```

Final B06 closure evidence includes generated/client/web sanity plus persistent local dogfood state surviving browser reload as recorded by the B06-E closure document. No additional DDL was needed after `_57`.

## 7. Next persistence boundary — B08

B08 Session Runtime is next, but **no migration is pre-authorized**.

Before any DDL:

```text
Product / Domain / Logical Session authority
→ accepted Physical mapping
→ existing CP6 Session structures/capabilities
→ current Alembic/Dictionary/SQLAlchemy/PostgreSQL catalog
→ identify a concrete semantic gap
```

Only then may a new forward-only migration be introduced.

B08 must preserve:

```text
Schedule != Session
Session != Actual
planned duration != Session elapsed/active duration
```

Provider integration, native/offline, broad analytics and account collaboration are outside the current `+`/Timeline vertical and must not drive schema expansion here.