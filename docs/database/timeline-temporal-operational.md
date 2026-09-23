# Timeline / Temporal-Operational — Candidate Database Overlay

- **Status:** CURRENT CANDIDATE DATABASE AUTHORITY
- **Reconciled:** 2026-09-23
- **Branch:** `feature/timeline-temporal-operational`
- **Protected-main baseline:** `20260906_18` / `89|5|18|77|173|91|272|0|0|0`
- **Candidate source head:** `20260923_57`
- **Candidate proven topology:** `145|5|88|92|285|223|408|0|0|0`
- **Whole-DB SoR:** `README.md`
- **Machine-readable authority:** `dictionary/`
- **Persistence doctrine:** `../development/backend-cp6-02-postgresql-persistence-constitution.md`
- **Current workstream map:** `../workstreams/timeline-temporal-operational-map.md`
- **Post-B06 scope decision:** `../workstreams/timeline-temporal-operational-post-b06-scope-decision-2026-09-23.md`
- **Whole-B06 closure:** `../workstreams/timeline-temporal-operational-b06-e-closure-2026-09-23.md`

## 1. Purpose and authority boundary

This file is the human-readable database overlay for Timeline candidate-only persistence. Candidate truth becomes protected-main truth only after integration gates and protected-main merge/readback.

## 2. Candidate evolution

```text
20260906_18 protected-main baseline
    ↓
20260908_19 B01 Activity core
    ↓
20260909_20 → 20260915_26 B02 Schedule core / closure
    ↓
20260916_27 → 20260917_29 B03 Event core / closure
    ↓
20260918_30 → 20260920_42 B04 Temporal Constraint + Movement Policy
    ↓
20260920_43 → 20260921_48 B05 Product Organization
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

B06-E whole-block closure introduced no database migration. `_57` remains the proven candidate frontier.

## 3. Current candidate topology

```text
Alembic     20260923_57
Tables      145
Views       5
Routines    88
Triggers    92
Indexes     285
FKs         223
CHECKs      408
Enums       0
Domains     0
Sequences   0
Materialized/partitioned 0
RLS         0
```

`_57` adds exactly one SECURITY DEFINER read routine and does not widen direct runtime table privileges on private B06 provenance tables.

## 4. Current semantic DB boundary

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
```

`dante.schedule` remains the single shared accepted-placement authority. B06 authorizes self-owned Occurrences into that existing engine; it does not create an Occurrence-specific Schedule authority.

Expected/scheduled Occurrence runtime read remains least privilege:

```text
scheduled Occurrence
→ shared Schedule + get_self_occurrence

unscheduled expected Occurrence
→ list_self_expected_occurrences_in_window(uuid,date,date,text)

Routine display metadata
→ list_self_routines
```

## 5. Temporal Constraint / Movement Policy authority

B04 remains closed/proven.

```text
boundary/window/planned-duration constraints
+ deterministic hard/soft evaluation
+ separate Schedule Movement Policy
+ governed proposal/acceptance paths
```

Permanent distinctions:

```text
constraint != placement
Movement Policy != Temporal Constraint
Movement Policy != solver result
proposal != accepted effect
evaluation != solver decision
```

Deferred B04 families remain owned by later anchors:

```text
TC-009 contiguous Session duration  → B08
TC-010 spacing/recovery             → later anchor-specific reopening
TC-011 relative before/after        → reviewed bounded relation/reference persistence required
```

## 6. Proof state

```text
B01 ✅ CLOSED / PROVEN
B02 ✅ CLOSED / PROVEN
B03 ✅ CLOSED / PROVEN
B04 ✅ CLOSED / PROVEN through `_42`
B05 ✅ CLOSED / PROVEN through `_48`
B06-A ✅ CLOSED / PROVEN at `_51`
B06-B ✅ CLOSED / PROVEN at `_54`
B06-C ✅ CLOSED / PROVEN at `_55`
B06-D ✅ CLOSED / PROVEN at `_57`
B06-E ✅ WHOLE-BLOCK CLOSURE at `_57`
B06 ✅ CLOSED / PROVEN
```

Final B06 closure evidence includes generated/client/web sanity and persistent local dogfood state surviving browser reload. No further DDL was required.

## 7. Next persistence boundary — B08

B08 Session Runtime is the next active block, but no schema change is implied by that sequencing decision.

Required order:

```text
Product / Domain / Logical Session semantics
→ accepted Physical mapping
→ inspect existing CP6 Session tables/routines/mappings
→ identify concrete gap
→ forward-only DDL only if required
→ Dictionary/SQLAlchemy/Alembic/PostgreSQL/direct-test parity
```

B08 must preserve:

```text
Schedule != Session
Session != Actual
planned Schedule duration != Session elapsed/active duration
```

External provider integration, native/offline, broad analytics and account collaboration are outside the active `+`/Timeline vertical and are not persistence drivers for B08–B12.