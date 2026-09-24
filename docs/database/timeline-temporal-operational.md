# Timeline / Temporal-Operational — Candidate Database Overlay

- **Status:** CURRENT CANDIDATE DATABASE AUTHORITY — B08-A repaired, awaiting user proof
- **Reconciled:** 2026-09-24
- **Branch:** `feature/timeline-temporal-operational`
- **Protected-main baseline:** `20260906_18` / `89|5|18|77|173|91|272|0|0|0`
- **Candidate source head:** `20260924_60`
- **Candidate topology awaiting B08-A proof:** `148|5|94|93|290|230|414|0|0|0`
- **Whole-DB SoR:** `README.md`
- **Machine-readable authority:** `dictionary/`
- **Persistence doctrine:** `../development/backend-cp6-02-postgresql-persistence-constitution.md`
- **Current workstream map:** `../workstreams/timeline-temporal-operational-map.md`

## 1. Authority boundary

This is candidate-branch database truth, not protected-main truth. The authority chain remains:

```text
Product / Domain / Logical / Physical
→ PostgreSQL Persistence Constitution
→ candidate overlay + Dictionary
→ Alembic
→ SQLAlchemy
→ live PostgreSQL
→ direct proof
```

## 2. Candidate evolution

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
20260924_60 B08-A immutable END MaterialState repair
```

`_59` and `_60` are forward-only repairs of contracts introduced by `_58`.

## 3. Current candidate topology

```text
Alembic     20260924_60
Tables      148
Views       5
Routines    94
Triggers    93
Indexes     290
FKs         230
CHECKs      414
Enums       0
Domains     0
Sequences   0
Materialized/partitioned 0
RLS         0
```

`_60` adds one FK from the Session END receipt to the exact resulting `MaterialStateRef`; it replaces the END routine signature without adding another routine.

## 4. B08-A Session persistence

B08-A reuses the existing CP6 Session identity/timing substrate:

```text
session
session_timing_state
session_timing_absolute
session_timing_elapsed
session_timing_pause
session_timing_current_history
```

B08-A adds only:

```text
session_execution_subject
session_start_operation
session_end_operation

start_self_session
end_self_session
list_self_subject_sessions
get_self_session
```

Runtime has no direct DML on those private command/subject tables. Mutation remains behind bounded self-scoped `SECURITY DEFINER` capabilities.

### Exact subject contract

```text
Activity   → Session subject ✅
Occurrence → Session subject ✅
Routine    → direct Session subject ❌
Event      → ordinary baseline Session subject ❌
Schedule   → Session subject/owner ❌
```

`_59` requires the requested family to be `activity` or `occurrence` and to match `native_address.owner_family` exactly before any Session write.

### Immutable Session timing contract

A `session.timing` MaterialState payload is immutable. Capturing END is therefore a state transition, not an UPDATE of the old payload:

```text
START
→ MaterialState S1 { started_at, ended_at = NULL }
→ S1 current

END(expected=S1)
→ MaterialState S2 { same started_at, ended_at = accepted END instant }
→ close S1 current-history interval
→ S2 current
→ END receipt binds expected=S1 and resulting=S2
```

The replay of an accepted END returns the exact `resulting_material_state_ref` recorded in its receipt even if later lifecycle work changes the Session's current state. `_60` also repairs any candidate `_58` END receipts by splitting the previously mutated payload into truthful historical and current MaterialStates.

Permanent boundaries remain:

```text
Schedule != Session
Session != Actual
Session != Outcome
Session END != Activity completion
Session END != Occurrence completion
planned Schedule duration != Session elapsed/active duration
```

Session START on an unplaced Activity is valid and must not fabricate Schedule.

## 5. Existing temporal authority remains unchanged

`dante.schedule` remains the sole accepted-placement authority. B08-A neither requires nor manufactures Schedule. It also creates no Actual or Outcome.

Deferred constraint families remain:

```text
TC-009 contiguous Session duration  → B08-C
TC-010 spacing/recovery             → later anchor-specific reopening
TC-011 relative before/after        → future bounded relation/reference review
```

## 6. Proof state

```text
B01–B06                              ✅ CLOSED / PROVEN
B08-A `_58` base implementation       implemented
B08-A `_59` subject-family repair     implemented
B08-A `_60` immutable-END repair      implemented
B08-A automated proof                ⬜ user rerun required
B08-A real-stack Activity proof      ⬜ required
B08-A real-stack Occurrence proof    ⬜ required
```

Until those B08-A gates pass, `_60` is **candidate source truth, not proven closure**. B08-B remains blocked.
