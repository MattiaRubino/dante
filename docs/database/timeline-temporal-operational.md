# Timeline / Temporal-Operational — Candidate Database Overlay

- **Status:** CURRENT CANDIDATE DATABASE AUTHORITY — B08-A repair awaiting user proof
- **Reconciled:** 2026-09-24
- **Branch:** `feature/timeline-temporal-operational`
- **Protected-main baseline:** `20260906_18` / `89|5|18|77|173|91|272|0|0|0`
- **Candidate source head:** `20260924_59`
- **Candidate topology awaiting B08-A proof:** `148|5|94|93|290|229|414|0|0|0`
- **Whole-DB SoR:** `README.md`
- **Machine-readable authority:** `dictionary/`
- **Persistence doctrine:** `../development/backend-cp6-02-postgresql-persistence-constitution.md`
- **Current workstream map:** `../workstreams/timeline-temporal-operational-map.md`

## 1. Authority boundary

This file is the human-readable persistence overlay for the Timeline candidate branch. Candidate truth becomes protected-main truth only after the required local proof and protected-main integration/readback.

Permanent chain:

```text
Product / Domain / Logical / Physical
→ PostgreSQL Persistence Constitution
→ this candidate overlay + Dictionary
→ Alembic
→ SQLAlchemy mappings
→ live PostgreSQL
→ direct proof
```

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
20260921_49 → 20260921_51 B06-A Routine source/core
    ↓
20260922_52 → 20260922_54 B06-B Recurrence authoring/read
    ↓
20260922_55 B06-C bounded Occurrence checkpoint/control
    ↓
20260922_56 → 20260923_57 B06-D shared Schedule + expected-Occurrence Timeline read
    ↓
20260924_58 B08-A Session subject + START/READ/END capability
    ↓
20260924_59 B08-A exact Activity/Occurrence subject-family repair
```

`_59` is forward-only and replaces the permissive six-argument Session-start capability introduced by `_58`; it does not add another semantic owner or another timing system.

## 3. Current candidate topology

```text
Alembic     20260924_59
Tables      148
Views       5
Routines    94
Triggers    93
Indexes     290
FKs         229
CHECKs      414
Enums       0
Domains     0
Sequences   0
Materialized/partitioned 0
RLS         0
```

The counts are unchanged by `_59`: one start routine signature is replaced by another.

## 4. B08-A Session persistence

B08-A reuses the CP6 Session identity/timing family:

```text
session
session_timing_state
session_timing_absolute
session_timing_elapsed
session_timing_pause
session_timing_current_history
```

`_58` adds only the bounded execution-context/command persistence required by the product path:

```text
session_execution_subject
session_start_operation
session_end_operation
```

and bounded runtime capabilities:

```text
start_self_session
end_self_session
list_self_subject_sessions
get_self_session
```

Runtime receives no direct DML on the private Session tables. Writes stay behind `SECURITY DEFINER` self-scoped capabilities.

### Exact execution-subject contract

```text
Activity   → Session subject ✅
Occurrence → Session subject ✅
Routine    → direct Session subject ❌
Event      → ordinary baseline Session subject ❌
Schedule   → Session subject/owner ❌
```

`_59` requires `requested_subject_family IN ('activity','occurrence')` and verifies that it exactly matches `native_address.owner_family` before Session creation. Therefore an Activity endpoint cannot create a Session over an Occurrence ref and vice versa.

### Session timing lifecycle policy

The accepted CP6 Session timing aggregate is a live execution tracker. During one timer episode, the current absolute timing MaterialState may evolve through captured lifecycle facts:

```text
START → started_at known, ended_at NULL
PAUSE / RESUME → pause rows on the same absolute timing state
END → ended_at established on that live timing state
```

This is a narrow Session-timing lifecycle rule, not permission to mutate arbitrary MaterialStates in place. A later semantic correction/replacement of an already recorded Session timing belongs to a new MaterialState/current-history binding.

Permanent boundaries remain:

```text
Schedule != Session
Session != Actual
Session != Outcome
Session end != Activity completion
Session end != Occurrence completion
planned Schedule duration != Session elapsed/active duration
```

## 5. Existing temporal authority remains unchanged

`dante.schedule` remains the single accepted-placement authority. Session START never fabricates Schedule and Session END never rewrites Schedule.

B04 Temporal Constraint / Movement Policy remains closed/proven. Deferred families:

```text
TC-009 contiguous Session duration  → B08-C
TC-010 spacing/recovery             → later anchor-specific reopening
TC-011 relative before/after        → future bounded relation/reference review
```

## 6. Proof state

```text
B01 ✅ CLOSED / PROVEN
B02 ✅ CLOSED / PROVEN
B03 ✅ CLOSED / PROVEN
B04 ✅ CLOSED / PROVEN through `_42`
B05 ✅ CLOSED / PROVEN through `_48`
B06 ✅ CLOSED / PROVEN through `_57`

B08-A `_58` implementation            implemented
B08-A `_59` family-contract repair     implemented
B08-A automated proof                  ⬜ user rerun required
B08-A real-stack Activity proof        ⬜ required
B08-A real-stack Occurrence proof      ⬜ required
```

Until those B08-A gates pass, `_59` is **candidate source truth, not proven candidate closure** and B08-B stays blocked.
