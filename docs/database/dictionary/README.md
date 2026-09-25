# DANTE Database Dictionary

- **Status:** CURRENT / MATERIALIZED FOR CHECKED-OUT REPOSITORY STATE
- **Schema version:** 1
- **Serialization:** JSON
- **PostgreSQL:** 18.6
- **Protected-main Alembic head:** `20260906_18`
- **Protected-main topology:** `89|5|18|77|173|91|272|0|0|0`
- **Current candidate branch:** `feature/timeline-temporal-operational`
- **Current candidate Alembic source head:** `20260925_69`
- **Last proven candidate topology:** B09-C / `20260925_69` / `158|5|109|93|303|254|433`
- **Frozen CP6 head:** `20260826_08`
- **Last reconciled:** 2026-09-25

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

A mismatch is a defect. Protected `main` remains integration authority; candidate branch truth remains explicitly separate until integration.

## 2. Current checked-out business-schema inventory

Authoritative counts are in `scope.json`:

```text
tables      158
views         5
routines    109
standalone  272
triggers     93
indexes     303
FKs         254
CHECKs      433
```

No enum/domain, sequence, materialized view, partitioned table or RLS policy exists in the DANTE business-schema inventory.

## 3. Post-CP6 Timeline evolution

```text
B01 / 20260908_19
  Activity intention/create capability

B02 / 20260909_20 → 20260915_26
  shared Schedule establishment/revision/unschedule/Undo
  accepted placement forms + DST/source-intent hardening

B03 / 20260916_27 → 20260917_29
  Event expectation/shared Schedule authorization/Agenda

B04 / 20260918_30 → 20260920_42
  Temporal Constraint core, boundary/window/planned-duration semantics,
  deterministic evaluation, Movement Policy and Schedule hard-constraint guards

B05 / 20260920_43 → 20260921_48
  Life Area lifecycle, typed primary assignment, secondary Tags,
  postponed Event discovery/replan composition

B06-A / 20260921_49 → 20260921_51
  Routine source core, lifecycle and initial Recurrence companion corrections

B06-B / 20260922_52 → 20260922_54
  immutable Routine/Event Recurrence authoring, current/history/CAS,
  explicit DST policy and current-state reader validation

B06-C / 20260922_55
  bounded Occurrence checkpoint, explicit extra, skip, structural exclusion,
  62-day horizon and 10,000-Occurrence checkpoint cap

B06-D / 20260922_56 → 20260923_57
  self-owned Occurrence authorization in shared Schedule capabilities
  bounded execute-only expected-Occurrence Timeline read
  scheduled Occurrence composition through existing get_self_occurrence + Schedule
  Routine presentation through existing list_self_routines

B08-A / 20260924_58 → 20260924_61
  Session execution subject, immutable START/END transitions, exact Activity/Occurrence subject family

B08-B / 20260924_62 → 20260924_64
  Pause/Resume replay-safe transitions and elapsed/paused/active runtime metrics

B08-C / 20260924_65
  TC-009 direct Activity Session active-duration soft minimum; existing duration mutation routine forward-renamed, no object-count delta

B09-A / 20260925_66
  typed current Responsibility and expected Event Participation relations

B09-B / 20260925_67 → 20260925_68
  guarded authoring receipts and SECURITY DEFINER capabilities over the B09-A relations; `_68` forward-repairs qualified Event Participation function bodies without an object-count delta

B09-C / 20260925_69
  owner-local Person referent catalog and create/rename receipts, three bounded capabilities and widened guarded Person admissibility; user-run PostgreSQL/catalog proof passed 2026-09-25
```

B06-E whole-block closure required no new migration. `_57` remains the last proven B06 checkpoint; later B08 candidate migrations continue through `_65`.

The object tree and `scope.json`, not prose summaries, are structural source of truth.

## 4. Persistence classification

### Activity / Event / Routine

Distinct canonical owners. No repeated-Activity shortcut replaces Routine; no Event-specific or Occurrence-specific Schedule engine exists.

### Schedule

`dante.schedule` remains the single accepted temporal-placement authority reused by Activity/Event/Occurrence where authorized.

### Temporal Constraint / Movement Policy

Constraint and Movement Policy remain independent from accepted Schedule state and from solver output.

```text
Schedule != Temporal Constraint
Schedule != Movement Policy
Temporal Constraint != Movement Policy
Movement Policy != solver result
proposal != accepted effect
```

### Life Area / Tag

Actor-local product organization structures; not new Domain roots and not generic relationship/EAV mechanisms.

### Recurrence / Occurrence

```text
Routine != Recurrence != Occurrence
Occurrence != Schedule
```

Occurrence provenance remains private. Runtime exposure is through bounded self-scoped capabilities rather than direct table SELECT grants.

## 5. Permanent non-collapse

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
Movement Policy != solver result
proposal != accepted effect
evaluation != solver decision
solver proposal != accepted Schedule
current accepted state != newest row
idempotency key != Domain identity
projection != canonical truth
```

## 6. Proof state

```text
B01 Activity Core                     CLOSED / PROVEN
B02 Schedule Core                     CLOSED / PROVEN
B03 Event Core                        CLOSED / PROVEN
B04 overall                           CLOSED / PROVEN through `_42`
B05 overall                           CLOSED / PROVEN through `_48`
B06-A Routine core                    CLOSED / PROVEN at `_51`
B06-B Recurrence authoring            CLOSED / PROVEN at `_54`
B06-C Occurrence checkpoint           CLOSED / PROVEN at `_55`
B06-D Schedule + Timeline             CLOSED / PROVEN at `_57`
B06-E whole-block closure             CLOSED / PROVEN at `_57`
B06 overall                           CLOSED / PROVEN
B08-A/B                              CLOSED / USER-REPORTED
B08-C                                CLOSED / PROVEN `_65` — user-run local automated gate
B08-D                                CLOSED / USER-REPORTED
B09-A                                CLOSED / PROVEN `_66`
B09-B                                CLOSED / PROVEN `_68`
B09-C                                CLOSED / PROVEN `_69` — user-run local gate 2026-09-25
```

Final B06 closure evidence is owned by `../../workstreams/timeline-temporal-operational-b06-e-closure-2026-09-23.md`. Whole-B06 closure did not change the catalog after `_57`.

## 7. Object contract

Every standalone business-schema object records semantic traceability, implementation provenance, exact structure, lifecycle/currentness semantics, ACL and proof obligations. Embedded indexes/FKs/CHECKs/triggers remain attached to their owning tables; routines remain standalone because signature/security/search-path/ACL are independently governed.

Shared entries retain original introducing provenance even when later slices extend bounded dispatchers. Later semantics/proof are updated without falsifying historical provenance.

## 8. Validation

Required validation remains:

```text
JSON Schema consistency
filename/object-key agreement
FK/trigger target resolution
scope counts ↔ object tree
Dictionary ↔ SQLAlchemy ↔ Alembic ↔ PostgreSQL
owner/ACL parity
routine search_path/security parity
extension-owned objects excluded correctly
```

## 9. Same-change rule

No real object → no ceremonial Dictionary entry. Every real current DANTE business object requires matching Dictionary/Alembic/SQLAlchemy/current-human-reference/direct-PostgreSQL proof in the same reviewed slice.

## 10. Next boundary

B09-C Person-referent implementation is closed on the user-run 2026-09-25 PostgreSQL catalog proof: `_69` topology `158|5|109|93|303|254|433`, reconciled with Dictionary and SQLAlchemy. B09-D has no schema/Dictionary delta; integrated tests and the user's B09 real-app walkthrough are pending. B10 follows closed B09.

Provider integration, native/offline, broad analytics and account collaboration are outside this vertical and must not create speculative Dictionary entries.

B08-C / 20260924_65 reuses existing Temporal Constraint duration tables and mutation capability. It adds no physical object count; the current facet CHECK and deferred totality/mutation functions admit only the Activity-owned soft-minimum Session active-duration subset.
