# DANTE Database System of Record

- **Status:** CURRENT / AUTHORITATIVE DATABASE REFERENCE
- **Last reconciled:** 2026-09-25
- **PostgreSQL:** 18.6
- **Protected-main Alembic head:** `20260906_18`
- **Protected-main topology:** `89|5|18|77|173|91|272|0|0|0`
- **Timeline candidate branch:** `feature/timeline-temporal-operational`
- **Timeline candidate Alembic head:** `20260925_74`
- **Last proven candidate topology:** B10-A / `20260925_74` / `159|5|115|93|305|258|435`
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
20260924_58 → 20260924_65 B08 Session Runtime
    ↓
20260925_66 → 20260925_69 B09 Responsibility / Participation
    ↓
20260925_70 B10-A guarded Actual realization authoring/read
    ↓
20260925_71 B10-A exact Activity/Event/Occurrence subject-family authority
    ↓
20260925_72 B10-A Actual/scoped-address owner creation-order repair
    ↓
20260925_73 B10-A canonical family-aware Actual function signatures
    ↓
20260925_74 B10-A current-history qualification + canonical receipt FK name
```

No accepted historical migration was edited, rebased, renumbered or flattened. B10-A acceptance repairs `_72`–`_74` are forward-only.

## 3. Current candidate topology

```text
159 tables
5 views
115 routines
93 triggers
305 physical indexes
258 foreign keys
435 CHECK constraints
0 enums/domains
0 sequences
0 materialized views
0 partitioned tables
0 RLS policies
```

User-run PostgreSQL/application/catalog proof on 2026-09-25 established B10-A `_74` at `159|5|115|93|305|258|435`:

```text
14 passed in 25.06s
POSTGRES TEST EXIT: 0
```

The accepted B10-A vertical also passed repository generation/check, API-client typecheck, web typecheck, focused web tests and OpenAPI inventory during the same local acceptance cycle. Generated OpenAPI/Orval artifacts are committed at `780c612d`. No CI/GitHub Actions were used.

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

### B08 Session Runtime

B08 reuses the CP6 Session timing substrate and adds bounded subject/operation persistence and capabilities.

```text
Activity   → Session subject
Occurrence → Session subject
Schedule   ≠ Session subject/owner
```

Session START on an unplaced Activity is valid and does not fabricate Schedule. Session END creates no Activity completion, Occurrence resolution, Actual or Outcome.

### B09 Person referents / Responsibility / Participation

`_66`–`_69` materialize typed responsibility/expected-participation relations and owner-local Person referents without collapsing Person into Account. The local Person label is presentation, not universal identity. B09-D adds no database objects.

### B10-A Actual realization — closed / proven

B10-A activates explicit Actual realization over the existing CP6 Actual substrate for Activity, Event and Occurrence.

Canonical family:

```text
actual
actual_realization_state
actual_realization_timing
actual_realization_session_basis
actual_realization_current_history
actual_current_realization
actual_realization_operation
```

The new `actual_realization_operation` table is an immutable self-scoped idempotency receipt. Runtime does not receive raw mutation authority over the Actual realization family; consequential writes remain behind bounded `SECURITY DEFINER` capabilities.

Canonical semantics:

```text
Actual owner identity is stable for the subject realization context
realization state is append-only MaterialState truth
current accepted realization is explicit current binding/history
no Actual = unknown
realization_occurred=false = known non-realization
optional timing = instant | start_only | interval
optional Session evidence preserves exact Session + exact Session timing MaterialState
```

Permanent boundaries:

```text
Schedule != Session != Actual
Session END != Actual
Session evidence != Actual identity
Actual != Outcome != Confirmation
Expected outcome != Outcome
current accepted state != latest row
idempotency key != Domain identity
```

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
Expected outcome != Outcome
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
B01–B06                               CLOSED / PROVEN
B08                                   CLOSED / USER-REPORTED / PROVEN SUBBLOCKS
B09-A `_66` persistence              ✅ CLOSED / PROVEN 2026-09-25
B09-B `_67`–`_68` authoring         ✅ CLOSED / PROVEN 2026-09-25
B09-C `_69` Person referents         ✅ CLOSED / PROVEN 2026-09-25
B09-D whole-block integration         ✅ CLOSED / USER-REPORTED 2026-09-25
B10-A `_70`–`_74` Actual core        ✅ CLOSED / PROVEN 2026-09-25
```

B10-A closure evidence is recorded in `../workstreams/timeline-temporal-operational-b10-a-closure-2026-09-25.md`. The integrated B10 real-app walkthrough remains deferred until B10-E.

## 7. Current database cursor

B10-B Outcome is next but has not started. Before any schema change, inspect current Product/Domain/Logical/Physical Outcome authority and obtain user approval for the proposed change/file gate.

Do not infer a generic Outcome status enum from UI labels alone.

```text
Actual != Outcome
Expected outcome != Outcome
Outcome != Confirmation
Session END != Outcome
absence of Outcome != implicit success/failure
```
