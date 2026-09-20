# Timeline / Temporal-Operational Vertical — Semantic Work Map / Live Ledger

- **Status:** CURRENT SEMANTIC MAP + LIVE IMPLEMENTATION LEDGER — reconciled 2026-09-20
- **Branch:** `feature/timeline-temporal-operational`
- **Roadmap:** `docs/workstreams/timeline-temporal-operational-roadmap.md`
- **B04 execution plan:** `docs/workstreams/timeline-temporal-operational-b04-execution-plan.md`
- **B04-A closure:** `docs/workstreams/timeline-temporal-operational-b04-a-closure-2026-09-18.md` ✅
- **B04-B closure:** `docs/workstreams/timeline-temporal-operational-b04-b-closure-2026-09-19.md` ✅
- **B04-C closure:** `docs/workstreams/timeline-temporal-operational-b04-c-closure-2026-09-19.md` ✅
- **B04-D closure:** `docs/workstreams/timeline-temporal-operational-b04-d-closure-2026-09-19.md` ✅
- **B04-E closure:** `docs/workstreams/timeline-temporal-operational-b04-e-closure-2026-09-19.md` ✅
- **B04-F / whole-B04 closure:** `docs/workstreams/timeline-temporal-operational-b04-f-closure-2026-09-20.md` ✅
- **B05 execution plan:** `docs/workstreams/timeline-temporal-operational-b05-execution-plan.md` ✅
- **B05-A closure:** `docs/workstreams/timeline-temporal-operational-b05-a-closure-2026-09-20.md` ✅
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
planned Schedule duration != Actual duration
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
B04 Temporal Constraints + Movement Policy       ✅ CLOSED / PROVEN
├─ B04-A Temporal Constraint canonical core      ✅ CLOSED / PROVEN
├─ B04-B Boundary / Deadline constraints         ✅ CLOSED / PROVEN
├─ B04-C Windows / Preferences / Evaluation      ✅ CLOSED / PROVEN
├─ B04-D Movement Policy                         ✅ CLOSED / PROVEN
├─ B04-E Advanced-family applicability           ✅ CLOSED / PROVEN
└─ B04-F Whole-B04 closure                       ✅ CLOSED / PROVEN
B05 Product Organization                         🟡 A1 CREATE/LIST / PROOF PENDING
B06 Routine / Recurrence / Occurrence Baseline   ⬜
B07 UI/UX Consolidation v1                       ⬜
B08 Session Runtime                              ⬜
B09 Responsibility / Participation               ⬜
B10 Actual / Outcome / Confirmation / Resolution ⬜
B11 Advanced Recurrence / Conditional / Reminder ⬜
B12 Replanning / Conflict / Solver               ⬜
B13 Provider / Offline / Multi-device            ⬜
B14 Analytics / Statistics / Signals             ⬜
B15 Whole Vertical Closure                       ⬜
```

Current candidate persistence authority:

```text
PostgreSQL       18.6
Alembic source   20260920_46
Expected topology 123|5|54|90|245|170|354|0|0|0 (B05-B direct PG proof pending)
```

---

# 3. Completed foundation

## B00–B03 ✅ CLOSED / PROVEN

Real Data Spine, Activity Core, shared Schedule Core and Event Core are established. Event remains distinct from Activity while reusing shared Schedule authority; Agenda remains Event-internal value truth.

## Pre-B04 governance ✅ CLOSED / FROZEN

DB same-change reconciliation and Temporal API inventory/operationId/OpenAPI generation rules remain binding for all later slices.

---

# 4. B04 — Temporal Constraints + Movement Policy ✅ CLOSED / PROVEN

## B04-A ✅ CLOSED / PROVEN

Stable self-owned Activity/Event Temporal Constraint identity, `temporal_constraint.rule` MaterialState/current/history, expected-state CAS, idempotent create/revise/retire and public CRUD/read capability.

## B04-B ✅ CLOSED / PROVEN

```text
earliest_start     + schedule.start
latest_start       + schedule.start
latest_completion  + schedule.completion
```

## B04-C ✅ CLOSED / PROVEN

```text
start_within              + schedule.start
completion_within         + schedule.completion
full_placement_contained  + schedule.placement
placement_overlaps        + schedule.placement
```

Deterministic evaluation remains derived/non-persistent and distinguishes hard validity from soft preference.

## B04-D Movement Policy ✅ CLOSED / PROVEN

Movement Policy is a typed Schedule-owned governance facet, not a generic Movement entity and not a Temporal Constraint.

```text
schedule.movement_policy
automatic_movement_code  blocked | automatic
acceptance_path_code     direct | confirmation_required
```

Governed automatic movement never searches for candidates. It checks current policy/current placement basis and hard Temporal Constraint admissibility before a supplied candidate may become accepted Schedule truth. Proposal creation remains distinct from accepted effect.

Persistence authority:

```text
20260919_37 Movement Policy core
20260919_38 governed absolute Schedule move
20260919_39 proposal-accept replay fix
```

## B04-E Advanced-family applicability ✅ CLOSED / PROVEN

Implemented TC-008 as exact planned Schedule placement duration:

```text
minimum | maximum
schedule.placement
hard | soft
positive exact duration
```

The canonical evaluator now composes boundary + window + duration. Hard duration rules are also enforced in B04-D automatic movement.

Explicit applicability dispositions:

```text
TC-009 contiguous Session duration  → B08 runtime
TC-010 spacing/recovery             → B06/B08/B10 according to anchor
TC-011 relative before/after        → later reviewed bounded relation/reference persistence
```

No fake later-owned anchor or generic relation/JSON escape was introduced.

Persistence authority:

```text
20260919_40 planned Schedule duration constraints
20260919_41 duration runtime-read ACL
20260920_42 Schedule hard-constraint guard
Topology      116|5|44|90|233|153|331|0|0|0
```

Observed proof:

```text
core duration + movement integration             4 PASS
application/evaluator/regression                13 PASS / 3 deselected
whole catalog / Dictionary / SQLAlchemy / DB     3 PASS
```

Closure authority: `timeline-temporal-operational-b04-e-closure-2026-09-19.md`.

## B04-F Whole-B04 closure ✅ CLOSED / PROVEN

B04-F does not invent a new Temporal Constraint family. It closes the whole B04 block through:

```text
broad B04 backend/PostgreSQL regression
Activity/Event/Schedule regression
hard/soft/deadline/movement/duration cross-slice proof
exact public Temporal API inventory + OpenAPI snapshot parity
frontend/product path review against backend truth
applicable manual userTest
Dictionary / SQLAlchemy / Alembic reconciliation
final DB docs + map/roadmap/handoff + B04 closure record
```

The whole-B04 closure record is `timeline-temporal-operational-b04-f-closure-2026-09-20.md`.

No PASS came from prototype-only fields.

---

# 5. B05 — Product Organization ⬜ PRE-SCOPE FROZEN / IMPLEMENTATION OPEN

Execution authority: `timeline-temporal-operational-b05-execution-plan.md`. B05-A LR-12 catalog is proven; B05-B source implements actor-local typed Activity/Event assignments, and awaits direct PostgreSQL proof. Neither is a new Domain owner nor an implicit assignment of old rows.

```text
ORG-001  authority/pre-scope             ✅ pre-scope recorded
ORG-002  exact durable representation   ✅ B05-A proven
ORG-003  Life Area create               ✅ B05-A proven
ORG-004..008  rename/reorder/archive/hide/appearance                 ✅ B05-A proven
ORG-009  primary per-actor item assignment                         🟡 B05-B source / direct proof pending
ORG-010  separate secondary Tags                                ⬜ B05-C
ORG-011  non-collapse with Goal/Plan/Tag/Place/provider calendar  ⬜ verify throughout
ORG-012  real Timeline organization and filtering                ⬜ B05-D
ORG-013  hidden-item scheduling/conflict relevance               ⬜ B05-D
ORG-014  actor-local self-only boundary without invented grants    🟡 B05-B source / B09 sharing pending
ORG-015  accessible non-color-only presentation                  ⬜ B05-D
B05-T01..05  automated lifecycle, relation, view, conflict, accessibility proofs  ⬜
B05-T06  manual Life Area organization userTest                    ⬜ B05-E
```

The B03-E transferred postponed/TBD Event rediscovery belongs to B05-D: no Activity Planning Tray conversion and no invented placement. B05-A `_43`–`_45` is proven by the user's catalog test. B05-B `_46` binds newly created Activity/Event to one actor-local area atomically and inventories unassigned legacy rows. Its direct PostgreSQL proof is pending; B05 as a whole remains open.

---

# 6. Later ownership register

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

# 7. Current gate

```text
B04 ✅ CLOSED / PROVEN
B05-A ✅ CLOSED / PROVEN
B05-B 🟡 `_46` SOURCE IMPLEMENTED / DIRECT PROOF PENDING
```

Current gate: B05-A ✅ CLOSED / PROVEN at `_45`; B05-B primary assignment is active. ORG-001..008 are discharged; later obligations stay open. No CI/Actions dispatched.
