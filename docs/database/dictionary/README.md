# DANTE Database Dictionary

- **Status:** CURRENT / MATERIALIZED FOR CHECKED-OUT REPOSITORY STATE
- **Schema version:** 1
- **Serialization:** JSON
- **PostgreSQL:** 18.6
- **Protected-main Alembic head:** `20260906_18`
- **Protected-main topology:** `89|5|18|77|173|91|272|0|0|0`
- **Current candidate Alembic source head on `feature/timeline-temporal-operational`:** `20260921_48`
- **Current candidate expected topology:** `129|5|62|90|254|185|366|0|0|0` (B05-D proven)
- **Frozen CP6 head:** `20260826_08`
- **Last reconciled:** 2026-09-21

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

A mismatch is a defect. Protected `main` remains integration authority. B05-A `_45`, B05-B `_46` and B05-C `_47` passed direct PostgreSQL proof (the latter: 26 selected tests).

## 2. Current checked-out business-schema inventory

Authoritative counts are in `scope.json`:

```text
tables      129
views         5
routines     62
standalone  196
triggers     90
indexes      254
FKs          185
CHECKs       366
```

No enum/domain, sequence, materialized view, partitioned table or RLS policy exists in the DANTE business-schema inventory.

## 3. Post-CP6 Timeline evolution

```text
B01 / 20260908_19
  Activity intention/create capability

B02 / 20260909_20 → 20260915_26
  shared Schedule establishment/revision/unschedule/Undo
  complete accepted placement union
  DST/source-intent hardening

B03 / 20260916_27 → 20260917_29
  Event expectation/shared Schedule authorization/Agenda

B04-A / 20260918_30 → 20260918_33
  Temporal Constraint identity, rule MaterialState/current/history,
  expected-state CAS, idempotency and API activation

B04-B / 20260919_34
  absolute earliest/latest-start/latest-completion boundaries

B04-C / 20260919_35 → 20260919_36
  absolute windows + deterministic evaluation + runtime read ACL

B04-D / 20260919_37 → 20260919_39
  Schedule Movement Policy + governed automatic move + proposal/acceptance

B04-E / 20260919_40 → 20260919_41
  planned Schedule duration constraints + runtime read ACL
  boundary/window/duration evaluation composition
  hard-duration integration into governed automatic movement

B04-F / 20260920_42
  Schedule establish/revise hard-constraint guard

B05-A / 20260920_43 → 20260920_45
  self-scoped LR-12 Life Area identity, creation and mutation receipts
  bounded create/list/mutate/reorder, revision, archive, visibility and appearance
  no NativeRef, item assignment or Tags

B05-B / 20260920_46
  typed Activity/Event actor-local current primary assignment and immutable receipts
  bounded create/reassign/list/legacy inventory; direct old create privilege retired
  no invented legacy default, provider calendar, Domain owner, Tag or sharing grant

B05-C / 20260920_47
  actor-local secondary Tag catalog, archive and immutable operation receipt
  typed independent Activity/Event many-valued edges and attach/detach receipts
  no primary-area replacement, hierarchy, Goal/Plan or sharing grant

B05-D / 20260921_48
  actor-scoped postponed Event discovery with no fabricated placement
  Event/Schedule pair assertion and governed Undo + normal replan composition
  no Activity Planning Tray conversion, new Domain owner or Schedule-truth bypass
```

The object tree and `scope.json`, not this prose summary, are structural source of truth.

## 4. Timeline persistence classification

### 4.1 Activity / Schedule / Event

Existing B01–B03 ownership remains unchanged. `dante.schedule` remains the single shared accepted-placement owner.

### 4.2 Temporal Constraint — B04-A/B/C/E ✅ CLOSED / PROVEN

Temporal Constraint is a stable `ScopedRecordRef` LR-05 dependent. Boundary, window and duration rule MaterialStates remain independently revisable from Schedule.

Accepted boundary variants:

```text
earliest_start     + schedule.start
latest_start       + schedule.start
latest_completion  + schedule.completion
```

Accepted window variants:

```text
start_within              + schedule.start
completion_within         + schedule.completion
full_placement_contained  + schedule.placement
placement_overlaps        + schedule.placement
```

Accepted duration variants:

```text
minimum + schedule.placement
maximum + schedule.placement
```

`temporal_constraint_duration_state` is the typed MaterialState payload for TC-008. It stores only exact positive planned placement duration; no generic JSON rule payload exists.

`mutate_self_schedule_duration_constraint(...)` reuses the common Temporal Constraint identity/current/history/idempotency engine. `enforce_temporal_constraint_rule_totality()` now enforces exact family exclusivity across boundary/window/duration payloads.

Runtime SELECT on the duration payload is least privilege and exists only to support the canonical application read/evaluation surface.

### 4.3 Movement Policy — B04-D ✅ CLOSED / PROVEN

Movement Policy remains a typed Schedule-owned material facet:

```text
schedule.movement_policy
```

`assert_absolute_schedule_move_hard_admissible(...)` now evaluates current hard boundary, window **and duration** rules. Thus B04-D automation cannot bypass B04-E hard duration constraints.

### 4.4 Advanced-family applicability — B04-E ✅ CLOSED / PROVEN

```text
TC-008 implemented
TC-009 runtime deferred B08
TC-010 runtime deferred B06/B08/B10 by anchor
TC-011 runtime persistence deferred until reviewed bounded relation/reference support exists
```

No fake prior-time field, generic relation root, `related_id + type`, or opaque JSON relation payload was introduced.

## 5. Permanent non-collapse

```text
Schedule != Temporal Constraint
Schedule != Movement Policy
Temporal Constraint != Movement Policy
planned Schedule duration != Activity estimated effort
planned Schedule duration != Session duration
planned Schedule duration != Actual duration
Movement Policy != Authority itself
Movement Policy != solver result
proposal != accepted effect
policy revision != Schedule revision
constraint revision != Schedule revision
hard planning violation != impossible reality
soft preference violation != automatic rejection
evaluation != solver decision
violation != automatic mutation
current accepted state != newest row
idempotency key != Domain identity
```

## 6. Proof state

```text
B01 Activity Core                    CLOSED / PROVEN
B02 Schedule Core                    CLOSED / PROVEN
B03 Event Core                       CLOSED / PROVEN
B04-A                                CLOSED / PROVEN at 20260918_33
B04-B                                CLOSED / PROVEN at 20260919_34
B04-C                                CLOSED / PROVEN at 20260919_36
B04-D Movement Policy                CLOSED / PROVEN at 20260919_39
B04-E Advanced-family applicability  CLOSED / PROVEN at 20260919_41
B04-F Whole-B04 closure              CLOSED / PROVEN at 20260920_42
B04 overall                          CLOSED / PROVEN
B05-A Life Area full lifecycle        CLOSED / PROVEN at `_45`
B05-B primary assignment             CLOSED / PROVEN at `_46` (16 selected tests)
B05-C secondary Tags                 CLOSED / PROVEN at `_47` (26 selected tests)
```

Observed B04-E evidence:

```text
core duration + movement integration             4 PASS
application/evaluator/regression                13 PASS / 3 deselected
whole catalog + B04-E catalog reconciliation     3 PASS
DATABASE_CURRENT_TOPOLOGY                         116|5|44|90|233|153|331|0|0|0
```

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

B04-F and B05 are closed. User-run `_46` selected catalog/ACL/application proof passed (16 tests); legacy items remain unassigned until explicitly reconciled. `_47` adds six Tag catalog/typed-edge/receipt tables and six bounded functions, with matching mappings and Dictionary objects. Its direct PostgreSQL proof passed (26 selected tests). `_48` adds the postponed Event discovery/replan routines with matching mapping and Dictionary entries; the B05-D gate passed. The B05-E real-stack walkthrough is complete.
