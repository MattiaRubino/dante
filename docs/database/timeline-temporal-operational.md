# Timeline / Temporal-Operational — Candidate Database Overlay

- **Status:** CURRENT CANDIDATE DATABASE AUTHORITY — B09-C `_69` source materialized; PostgreSQL proof pending; real-stack validation deferred to B15
- **Reconciled:** 2026-09-25
- **Branch:** `feature/timeline-temporal-operational`
- **Protected-main baseline:** `20260906_18` / `89|5|18|77|173|91|272|0|0|0`
- **Candidate source head:** `20260925_69`
- **Last proven candidate topology:** B09-B / `20260925_68` / `156|5|106|93|301|251|426`
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
    ↓
20260924_61 B08-A END qualification
    ↓
20260924_62 B08-B pause/resume immutable transitions
    ↓
20260924_63 B08-B transition replay repair
    ↓
20260924_64 B08-B elapsed/paused/active runtime metrics
    ↓
20260924_65 B08-C TC-009 Session active-duration rule
    ↓
20260925_66 B09-A Responsibility / Participation persistence
    ↓
20260925_67 B09-B guarded Responsibility / Participation authoring
    ↓
20260925_68 B09-B qualify Event column references inside authoring functions
    ↓
20260925_69 B09-C owner-local Person referents
```

`_59` and `_60` are forward-only repairs of contracts introduced by `_58`.

## 3. Current candidate topology

```text
Alembic     20260925_69
Tables      158
Views       5
Routines    109
Triggers    93
Indexes     303
FKs         254
CHECKs      433
Enums       0
Domains     0
Sequences   0
Materialized/partitioned 0
RLS         0
```

Last proven candidate remains `_66` / `153|5|99|93|298|242|419`. `_67` is implemented and not yet user-proven.

`_60` adds one FK from the Session END receipt to the exact resulting `MaterialStateRef`; it replaces the END routine signature without adding another routine. `_61`–`_64` extend B08-A/B Session lifecycle and metrics. `_65` changes no object counts: it widens the existing constrained-facet CHECK, replaces deferred totality, and forward-renames/replaces the duration mutation routine; routine counts stay flat.

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
TC-009 Session active-duration minimum → activated and locally proven in B08-C `_65`
TC-010 spacing/recovery             → later anchor-specific reopening
TC-011 relative before/after        → future bounded relation/reference review
```

## 6. Proof state

```text
B01–B06                              ✅ CLOSED / PROVEN
B08-A `_58` base implementation       implemented
B08-A `_59` subject-family repair     implemented
B08-A `_60` immutable-END repair      implemented
B08-A automated + real-stack proof ✅ CLOSED PER USER-REPORTED B08-B DEPENDENCY
B08-B pause/resume + metric proof   ✅ CLOSED PER USER REPORT
B08-C `_65` local automated proof   ✅ CLOSED / PROVEN 2026-09-24
B09-A `_66` persistence             ✅ CLOSED / PROVEN 2026-09-25
B09-B `_67`–`_68` authoring        ✅ CLOSED / PROVEN 2026-09-25
B09-C `_69` Person referents        CANDIDATE / LOCAL PROOF PENDING
```

B08-A and B08-B are treated as closed based on the user’s B08-B closure report; the original local logs are not stored here. B08-C `_65` passed the user-run local generated/client, web, backend unit/API and PostgreSQL catalog/integration gates on 2026-09-24. It remains candidate branch truth until protected-main integration; B08-D owns the one real-stack walkthrough. B09-B `_67`–`_68` is closed on its automated proof; real-stack validation is deferred to B15 whole-vertical closure.


## 7. B08-B / B08-C candidate database semantics

B08-B `_62`–`_64` reuses the CP6 Session timing substrate and returns elapsed, paused and active seconds from canonical timing and pause facts. It adds no parallel Session table. The user reported B08-B closed on 2026-09-24.

B08-C `_65` activates `duration / session.active_duration` only for a soft minimum rule directly owned by an Activity. It reuses `temporal_constraint_state`, `temporal_constraint_duration_state`, the existing current-history envelope and the existing duration mutation capability. DB totality admits Schedule placement minimum/maximum as before, or Session active-duration minimum + soft + Activity only. No new object is added.

Runtime Session reads query only the authenticated Activity’s current duration rule and compare it to that one Session’s `active_seconds`; paused time is excluded. An open under-threshold Session is pending; an ended under-threshold Session is violated. Schedule evaluation excludes this facet. The evaluation is not persisted and never blocks Pause/Resume/End or creates Schedule/completion/Actual/Outcome.

Dictionary, SQLAlchemy mapping and migration `_65` define the same `session.active_duration` facet contract. The B08-C freeze specifies the exact admitted subset and proof obligations.

## 8. B09 candidate database semantics

B09-A `_66` adds current typed relations only:

```text
event_expected_participation
activity_responsibility
event_responsibility
```

B09-B `_67` keeps those tables default-deny and adds insert-only operation receipts plus SECURITY DEFINER capabilities. Current holder/requirement rows may change; accepted commands are append-only receipts. `_self_referenceable_person` is INVOKER, not runtime-executable, and `_69` admits the caller's self Person or an owner-local registered Person. The owner's label is presentation, not Person identity; `person_referent_catalog` and immutable operation receipts stay default-deny.

```text
Responsibility != Participation
expected Participation != Actual / attendance
Person != Account
public holder/participant vocabulary = self only
```


## B09-C candidate persistence

`_69` atomically creates a native UUIDv7 Person and its native address with one owner-local label and receipt. A single catalog entry identifies a Person referentially admitted for B09-B's existing Responsibility and expected Event Participation functions; no Account, invitation or Actual is created. The bounded rename operation changes only the owner-local label under revision CAS. Current-state tables and history receipts remain distinct. Source-derived catalog target is `158|5|109|93|303|254|433`; direct PostgreSQL verification remains pending.
