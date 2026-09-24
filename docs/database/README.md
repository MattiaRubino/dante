# DANTE Database System of Record

- **Status:** CURRENT / AUTHORITATIVE DATABASE REFERENCE
- **Last reconciled:** 2026-09-24
- **PostgreSQL:** 18.6
- **Protected-main Alembic head:** `20260906_18`
- **Protected-main topology:** `89|5|18|77|173|91|272|0|0|0`
- **Timeline candidate branch:** `feature/timeline-temporal-operational`
- **Timeline candidate Alembic head:** `20260924_65`
- **Timeline candidate topology awaiting local proof:** `150|5|99|93|292|236|418|0|0|0`
- **Timeline candidate DB overlay:** `timeline-temporal-operational.md`
- **Persistence doctrine:** `../development/backend-cp6-02-postgresql-persistence-constitution.md`
- **Persistence ADR:** `../decisions/ADR-010-postgresql-persistence-constitution.md`
- **Timeline workstream authority:** `../workstreams/timeline-temporal-operational-map.md`

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
20260908_19 B01 Activity
    ↓
20260909_20 → 20260915_26 B02 Schedule
    ↓
20260916_27 → 20260917_29 B03 Event
    ↓
20260918_30 → 20260920_42 B04 Temporal Constraint + Movement Policy
    ↓
20260920_43 → 20260921_48 B05 Product Organization
    ↓
20260921_49 → 20260923_57 B06 Routine / Recurrence / Occurrence
    ↓
20260924_58 B08-A Session subject + START/READ/END
    ↓
20260924_59 B08-A exact Activity/Occurrence subject-family repair
    ↓
20260924_60 B08-A immutable Session END MaterialState repair
    ↓
20260924_61 B08-A END qualification
    ↓
20260924_62 → 20260924_63 B08-B pause/resume + replay repair
    ↓
20260924_64 B08-B runtime metrics
    ↓
20260924_65 B08-C Session active-duration TC-009
```

No accepted historical migration was edited, rebased, renumbered or flattened. `_59` and `_60` are forward-only repairs.

## 3. Current candidate topology

```text
150 tables
5 views
99 routines
93 triggers
292 physical indexes
236 foreign keys
418 CHECK constraints
0 enums/domains
0 sequences
0 materialized views
0 partitioned tables
0 RLS policies
```

The `_60` delta is one FK on `session_end_operation.resulting_material_state_ref`; the END routine signature is replaced rather than duplicated. `_61`–`_64` add B08-A/B Session lifecycle and metrics. `_65` changes no object counts and activates B08-C using the existing duration tables and governed mutation routine.

## 4. Timeline persistence classification

### B01 Activity

Activity is a NativeRef owner and may exist without Schedule. Activity identity is not Schedule identity.

### B02 Schedule

`dante.schedule` is the shared accepted-placement authority. Current/history/CAS/idempotency/Undo remain independent from the subject identity.

### B03 Event

Event remains a distinct NativeRef owner while reusing shared Schedule authority.

### B04 Temporal Constraint / Movement Policy

Constraint, policy, solver proposal and accepted placement remain separate concepts.

```text
Schedule != Temporal Constraint
Schedule != Movement Policy
Movement Policy != solver result
proposal != accepted effect
```

### B05 Product Organization

Life Area and Tags are actor-local product organization, not Domain identity owners.

### B06 Routine / Recurrence / Occurrence

```text
Routine != Recurrence != Occurrence
Occurrence != Schedule
```

Canonical Occurrences reuse the existing shared Schedule engine. No `occurrence_schedule` authority exists.

### B08-A Session Runtime candidate

B08-A reuses the CP6 Session timing substrate and adds only bounded subject/operation persistence and capabilities.

```text
Activity   → Session subject
Occurrence → Session subject
Schedule   ≠ Session subject/owner
```

`_59` enforces the exact Activity/Occurrence family at the database boundary. `_60` restores the global MaterialState rule for END:

```text
S1 = open session.timing MaterialState
END(expected=S1)
→ create immutable S2 with ended_at
→ close S1 current-history interval
→ bind S2 current
→ receipt(expected=S1, resulting=S2)
```

Runtime never updates protected `session_timing_absolute` payload in place after `_60`. An END replay returns the exact produced `MaterialStateRef` from the immutable receipt.

Session START on an unplaced Activity is valid and does not fabricate Schedule. Session END creates no Activity completion, Occurrence resolution, Actual or Outcome.

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
planned Schedule duration != Session duration
window != placement
preference != accepted Schedule
evaluation != solver decision
solver proposal != accepted Schedule
current accepted state != newest row
idempotency key != Domain identity
projection != canonical truth
```

## 6. Proof state

```text
B01–B06                              CLOSED / PROVEN
B08-A `_58` base implementation       implemented
B08-A `_59` family repair             implemented
B08-A `_60` immutable-END repair      implemented
B08-A/B automated + real-stack proof ✅ CLOSED PER USER-REPORTED B08-B DEPENDENCY
B08-C `_65` local automated proof     ✅ CLOSED / PROVEN 2026-09-24
```

B08-A/B are treated as closed based on the user’s B08-B closure report; their exact test logs are not committed. B08-C `_65` passed the user-run generated/client, web, backend unit/API and PostgreSQL catalog/integration gates on 2026-09-24. The single real-stack walkthrough remains B08-D scope.
