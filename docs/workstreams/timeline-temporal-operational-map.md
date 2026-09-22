# Timeline / Temporal-Operational Vertical — Semantic Work Map / Live Ledger

- **Status:** CURRENT SEMANTIC MAP + LIVE IMPLEMENTATION LEDGER — reconciled 2026-09-22
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
- **B05-B closure:** `docs/workstreams/timeline-temporal-operational-b05-b-closure-2026-09-20.md` ✅
- **B05-C closure:** `docs/workstreams/timeline-temporal-operational-b05-c-closure-2026-09-20.md` ✅
- **B05-D closure:** `docs/workstreams/timeline-temporal-operational-b05-d-closure-2026-09-21.md` ✅
- **B05-E / whole-B05 closure:** `docs/workstreams/timeline-temporal-operational-b05-e-closure-2026-09-21.md` ✅
- **B06 execution plan:** `docs/workstreams/timeline-temporal-operational-b06-execution-plan.md` 🟨
- **B06-A closure:** `docs/workstreams/timeline-temporal-operational-b06-a-closure-2026-09-21.md` ✅
- **B06-B closure:** `docs/workstreams/timeline-temporal-operational-b06-b-closure-2026-09-22.md` ✅
- **B06-C implementation freeze:** `docs/workstreams/timeline-temporal-operational-b06-c-implementation-freeze.md` 🟨
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
B05 Product Organization                         ✅ CLOSED / PROVEN
B06 Routine / Recurrence / Occurrence Baseline   🟨 IN PROGRESS — B06-C proof pending
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
Alembic source   20260922_55
Expected topology 145|5|87|92|285|223|408|0|0|0 (B06-C candidate; proof pending)
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

# 5. B05 — Product Organization ✅ CLOSED / PROVEN

Execution authority: `timeline-temporal-operational-b05-execution-plan.md`. B05-A LR-12 catalog, B05-B actor-local typed Activity/Event assignments, B05-C Tag catalog/typed secondary edges and B05-D production integration are proven. None is a new Domain owner or an implicit assignment of old rows.

```text
ORG-001  authority/pre-scope             ✅ pre-scope recorded
ORG-002  exact durable representation   ✅ B05-A proven
ORG-003  Life Area create               ✅ B05-A proven
ORG-004..008  rename/reorder/archive/hide/appearance                 ✅ B05-A proven
ORG-009  primary per-actor item assignment                         ✅ B05-B proven
ORG-010  separate secondary Tags                                ✅ B05-C proven
ORG-011  non-collapse with Goal/Plan/Tag/Place/provider calendar  ✅ B05-A..D proven
ORG-012  real Timeline organization and filtering                ✅ B05-D
ORG-013  hidden-item scheduling/conflict relevance               ✅ B05-D
ORG-014  actor-local self-only boundary without invented grants    ✅ B05-B proven / B09 sharing deferred
ORG-015  accessible non-color-only presentation                  ✅ B05-D
B05-T01..05  automated lifecycle, relation, view, conflict, accessibility proofs  ✅ B05-A..D proven
B05-T06  manual Life Area organization userTest                    ✅ B05-E proven
```

The B03-E transferred postponed/TBD Event rediscovery belongs to B05-D: no Activity Planning Tray conversion and no invented placement. B05-A `_43`–`_45` and B05-B `_46` are proven. `_46` binds newly created Activity/Event to an actor-local area atomically and inventories unassigned legacy rows. B05-C `_47` adds distinct secondary many-valued Tag profiles and typed edges, proved by 26 direct PostgreSQL tests. B05-D `_48` is proven by generated/client/typecheck gates, 41 selected web tests and 24 selected PostgreSQL/API/catalog tests. B05-E recorded the completed real-stack manual walkthrough, including immediate Event rediscovery, Activity Planning Tray refresh and restored `+` creation with an active Life Area; B05 is closed.

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
B05-B ✅ CLOSED / PROVEN at `_46`
B05-C ✅ CLOSED / PROVEN at `_47` (26 selected PostgreSQL tests)
B05-D ✅ CLOSED / PROVEN at `_48` (41 selected web + 24 PostgreSQL/API/catalog tests)
B05-E ✅ WHOLE-BLOCK CLOSURE / MANUAL WALKTHROUGH COMPLETE
B05   ✅ CLOSED / PROVEN
B06-A ✅ CLOSED / PROVEN
B06-B ✅ CLOSED / PROVEN at `_54` (1 fingerprint + 28 PostgreSQL/catalog regressions)
B06-C 🟨 IMPLEMENTED CANDIDATE at `_55` / DIRECT PROOF PENDING
```

Current gate: B05 ✅ CLOSED / PROVEN → B06-A/B ✅ CLOSED / PROVEN → B06-C candidate `_55` / proof pending. The candidate adds the bounded backend checkpoint, effective-history evaluation, canonical Routine/Event Occurrences, explicit extra, immutable skip, structural exclusion, lifecycle stop and execute-only generation surface. The 62-day half-open range is preserved and a 10,000-Occurrence safety cap rejects dense checkpoints atomically. No Schedule, Timeline, fake Activity or CI/Actions is introduced.
