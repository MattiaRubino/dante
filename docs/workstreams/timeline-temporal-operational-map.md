# Timeline / Temporal-Operational Vertical — Semantic Work Map / Live Ledger

- **Status:** CURRENT SEMANTIC MAP + LIVE IMPLEMENTATION LEDGER — reconciled 2026-09-19
- **Branch:** `feature/timeline-temporal-operational`
- **Roadmap:** `docs/workstreams/timeline-temporal-operational-roadmap.md`
- **B04 execution plan:** `docs/workstreams/timeline-temporal-operational-b04-execution-plan.md`
- **B04-A closure:** `docs/workstreams/timeline-temporal-operational-b04-a-closure-2026-09-18.md` ✅
- **B04-B closure:** `docs/workstreams/timeline-temporal-operational-b04-b-closure-2026-09-19.md` ✅
- **B04-C closure:** `docs/workstreams/timeline-temporal-operational-b04-c-closure-2026-09-19.md` ✅
- **B04-D closure:** `docs/workstreams/timeline-temporal-operational-b04-d-closure-2026-09-19.md` ✅
- **Timeline candidate DB overlay:** `docs/database/timeline-temporal-operational.md`

The archived semantic freeze remains the binding detailed inventory for the full vertical. This file is the live implementation/proof ledger.

---

# 1. Permanent semantic boundaries

```text
Person != Account != Principal != Actor
Goal != Plan != Activity
Activity != Event != Routine
Activity != Schedule
Event != Schedule
Routine != Recurrence
Recurrence != Occurrence
Occurrence != Schedule
Schedule != Temporal Constraint
Schedule != Movement Policy
Temporal Constraint != Movement Policy
Movement Policy != Authority itself
Movement Policy != solver result
Schedule != Session
Schedule != Actual
Session != Actual
Actual != Outcome
Outcome != Confirmation
planned/intended != happened
proposal != accepted effect
pending != success
current accepted state != latest row
idempotency key != Domain identity
provider identity != DANTE identity
projection != canonical truth
unscheduled != deleted
Undo != DB/history rewind
estimated effort != scheduled duration != Session duration
floating-local != named-zone-local != absolute instant
date span != coarse local period
coarse precision != fabricated exact clock time
Agenda part != Activity/Event/Occurrence/Schedule/Session/Actual by default
Event != Availability / Capacity Claim
postponed/TBD Event != Planning Tray Activity
window != placement
preference != accepted Schedule
evaluation != solver decision
violation != automatic mutation
policy revision != Schedule revision
constraint revision != Schedule revision
```

---

# 2. Current roadmap position

```text
B00 Real Data Spine                              ✅ CLOSED / PROVEN
B01 Activity Core                                ✅ CLOSED / PROVEN
B02 Schedule Core                                ✅ CLOSED / PROVEN
B03 Event Core                                   ✅ CLOSED / PROVEN
PRE-B04 DB/API GOVERNANCE                        ✅ CLOSED / FROZEN
B04 Temporal Constraints + Movement Policy       🟡 IN PROGRESS
├─ B04-A Temporal Constraint canonical core      ✅ CLOSED / PROVEN
├─ B04-B Boundary / Deadline constraints         ✅ CLOSED / PROVEN
├─ B04-C Windows / Preferences / Evaluation      ✅ CLOSED / PROVEN
├─ B04-D Movement Policy                         ✅ CLOSED / PROVEN
├─ B04-E Advanced-family applicability           ⬜ NEXT
└─ B04-F Whole-B04 closure                       ⬜
B05 Product Organization                         ⬜
B06 Routine / Recurrence / Occurrence Baseline   ⬜
B07 UI/UX Consolidation v1                       ⬜
B08 Session Runtime                              ⬜
B09 Responsibility / Participation               ⬜
B10 Actual / Outcome / Confirmation / Resolution ⬜
B11 Advanced Recurrence / Conditional / Reminder ⬜
B12 Replanning / Conflict / Solver               ⬜
B13 Provider / Offline / Multi-device             ⬜
B14 Analytics / Statistics / Signals             ⬜
B15 Whole Vertical Closure                       ⬜
```

Current candidate persistence authority:

```text
PostgreSQL       18.6
Alembic head     20260919_39
Topology         115|5|42|89|232|152|329|0|0|0
```

---

# 3. Completed foundation

## B00–B03 ✅ CLOSED / PROVEN

Real Data Spine, Activity Core, shared Schedule Core and Event Core are established. Event remains distinct from Activity while reusing shared Schedule authority; Agenda remains Event-internal value truth.

## Pre-B04 governance ✅ CLOSED / FROZEN

DB same-change reconciliation and Temporal API inventory/operationId/OpenAPI generation rules remain binding for all later slices.

---

# 4. B04 — Temporal Constraints + Movement Policy 🟡 IN PROGRESS

## B04-A ✅ CLOSED / PROVEN

Established stable self-owned Activity/Event Temporal Constraint identity, `temporal_constraint.rule` MaterialState/current/history, expected-state CAS, idempotent create/revise/retire and public CRUD/read capability.

## B04-B ✅ CLOSED / PROVEN

Closed absolute boundary matrix:

```text
earliest_start     + schedule.start
latest_start       + schedule.start
latest_completion  + schedule.completion
```

## B04-C ✅ CLOSED / PROVEN

Closed absolute window matrix:

```text
start_within              + schedule.start
completion_within         + schedule.completion
full_placement_contained  + schedule.placement
placement_overlaps        + schedule.placement
```

Deterministic evaluation remains derived/non-persistent and distinguishes hard validity from soft preference.

## B04-D — Movement Policy ✅ CLOSED / PROVEN

Movement Policy is a typed Schedule-owned governance facet, not a generic Movement entity and not a Temporal Constraint.

Canonical state:

```text
schedule.movement_policy

automatic_movement_code  blocked | automatic
acceptance_path_code     direct | confirmation_required
```

Canonical persistence:

```text
schedule_movement_policy_state
schedule_movement_policy_current_history
schedule_movement_policy_mutation_operation
schedule_move_proposal
schedule_move_request_operation
schedule_move_accept_operation
```

Governed behavior:

```text
blocked
  → automatic movement rejected

automatic + direct
  → supplied absolute candidate commits only when hard-admissible and expected placement still current

automatic + confirmation_required
  → request persists proposal only
  → explicit acceptance rechecks proposal basis, current policy, placement CAS and hard constraints
```

The policy engine does not search for a placement. Broad replanning/candidate generation/optimization remain B12.

Hard constraint violation or unsupported hard semantics fail closed. Soft violations do not block an otherwise authorized automatic move.

`proposal != accepted effect` is persisted explicitly. Movement Policy revision appends independent policy MaterialState/history and does not revise Schedule placement.

B04-D public HTTP/API surface:

```text
no new public Temporal endpoint
```

Therefore OpenAPI/generated-client artifacts intentionally remain unchanged in D.

Persistence authority:

```text
20260919_37 b04_schedule_movement_policy_core
20260919_38 b04_governed_schedule_move
20260919_39 b04_schedule_move_accept_replay_fix
Topology      115|5|42|89|232|152|329|0|0|0
```

Observed proof:

```text
Movement Policy / governed move / ACL            7 PASS
whole catalog / Dictionary / SQLAlchemy / DB     3 PASS
```

Closure authority: `timeline-temporal-operational-b04-d-closure-2026-09-19.md`.

## B04-E — Advanced-family applicability ⬜ NEXT

Min/max duration, contiguous-session, spacing/recovery and relative-before/after must be activated only where existing canonical anchors make them truthful. Session/Actual/Occurrence/Solver-dependent semantics stay deferred to their owning blocks.

## B04-F — Whole-B04 closure ⬜

Whole-B04 regression, product/API/DB consistency and final closure evidence. B05 begins only after B04-F.

---

# 5. Later ownership register

```text
B05  Calendar / Life Area / Tags / product organization
B06  Routine + Recurrence + Occurrence baseline
B07  UI/UX Consolidation v1
B08  Session Runtime
B09  Responsibility / Participation / actor relations
B10  Actual + Outcome + Confirmation + Resolution
B11  advanced recurrence + conditional policy + reminders
B12  replanning / conflict / solver
B13  provider + offline / multi-device
B14  analytics / statistics / signals
B15  whole-vertical closure
```

# 6. Current gate

```text
B04-D ✅ CLOSED / PROVEN
B04-E ⬜ NEXT
```

Immediate next gate: B04-E applicability freeze and implementation only for advanced Temporal Constraint families that can be represented/evaluated truthfully against currently canonical anchors.

CI remains separate and is not implicitly authorized.
