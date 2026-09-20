# Timeline / Temporal-Operational Vertical — Implementation Roadmap

- **Status:** CURRENT EXECUTION ROADMAP — reconciled 2026-09-19
- **Branch/workstream:** `feature/timeline-temporal-operational`
- **Current completed frontier:** B04-E Advanced-family applicability ✅ CLOSED / PROVEN
- **Current active block:** B04 Temporal Constraints + Movement Policy
- **Current active slice:** B04-F Whole-B04 closure
- **Current candidate DB authority:** PostgreSQL 18.6 / Alembic `20260920_42`
- **Current candidate topology:** `116|5|44|90|233|153|331|0|0|0`
- **Live progress ledger:** `docs/workstreams/timeline-temporal-operational-map.md`
- **B04 execution authority:** `docs/workstreams/timeline-temporal-operational-b04-execution-plan.md`
- **B04-E closure:** `docs/workstreams/timeline-temporal-operational-b04-e-closure-2026-09-19.md`

The archived semantic freeze preserves the complete functionality/non-collapse inventory. This document is the current sequencing authority.

---

# 0. Fixed execution contract

```text
semantic capability
→ current persistence inspection
→ DDL only if a real gap exists
→ backend/application operation/query
→ API/transport when applicable
→ frontend integration when applicable
→ automated proof
→ manual userTest where applicable
→ live ledger update
→ documentation reconciliation
```

Permanent rules include:

```text
Domain != Logical != Physical != API DTO != frontend ViewModel
projection != canonical truth
planned/intended != happened
Activity != Event != Routine
Schedule != Temporal Constraint != Recurrence
Schedule != Movement Policy
Temporal Constraint != Movement Policy
Movement Policy != Authority itself
Movement Policy != solver result
Schedule != Session != Actual
Session != Actual != Outcome
Routine != Recurrence != Occurrence
planned Schedule duration != Activity estimated effort
planned Schedule duration != Session / Actual duration
proposal != accepted effect
pending != success
idempotency key != Domain identity
current accepted state != latest row
Undo != history rewind
```

A block closes only after applicable semantic, persistence, backend, frontend, proof and documentation gates are reconciled.

---

# 1. Current ordered roadmap

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
├─ B04-E Advanced-family applicability           ✅ CLOSED / PROVEN
└─ B04-F Whole-B04 closure                       🟡 ACTIVE
B05 Product Organization                         ⬜
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

B05 starts only after B04-F closes the whole B04 block.

---

# 2. B04 completed slices

## B04-A ✅ CLOSED / PROVEN

Stable self-owned Activity/Event Temporal Constraint identity, immutable `temporal_constraint.rule` MaterialState/current/history, expected-state CAS, idempotent mutation and public CRUD/read capability.

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

Derived evaluation distinguishes hard validity, soft preference and not-evaluable states without solver search or automatic mutation.

## B04-D ✅ CLOSED / PROVEN

Movement Policy is separately materialized as `schedule.movement_policy`. Governed automatic movement supports `blocked | automatic` and `direct | confirmation_required`, with proposal distinct from accepted effect. Current hard Temporal Constraints are re-evaluated before automatic commit/accept.

Persistence authority:

```text
20260919_37 Movement Policy core
20260919_38 governed absolute Schedule move
20260919_39 proposal-accept replay fix
```

## B04-E ✅ CLOSED / PROVEN

TC-008 is activated as exact planned Schedule placement duration:

```text
minimum | maximum
schedule.placement
hard | soft
positive exact duration
```

The canonical application evaluator composes boundary/window/duration. The governed automatic-move guard also enforces hard duration rules.

Explicit dispositions:

```text
TC-009 contiguous Session duration  → B08 runtime
TC-010 spacing/recovery             → B06/B08/B10 by anchor
TC-011 relative before/after        → deferred until reviewed bounded relation/reference persistence exists
```

Persistence authority:

```text
20260919_40 planned Schedule duration constraints
20260919_41 duration runtime read ACL
20260920_42 Schedule hard-constraint guard
116|5|44|90|233|153|331|0|0|0
```

Observed proof:

```text
4 PASS core/movement
13 PASS / 3 deselected application/regression
3 PASS whole catalog/Dictionary/ACL
```

Closure authority: `timeline-temporal-operational-b04-e-closure-2026-09-19.md`.

---

# 3. B04-F — Whole-B04 closure 🟡 ACTIVE

B04-F is a closure/proof slice, not a new semantic-family implementation slice.

Required evidence from the frozen B04 execution plan:

```text
B04 typed/domain validation
real PostgreSQL migration/current/history/CAS/idempotency
Schedule integration and Activity/Event regression
hard vs soft evaluation
Deadline passage != Outcome
Movement Policy enforcement
frontend Create/edit/read explanation paths actually backed by backend truth
real-stack browser proof for accepted product slice
manual userTest constraint/explanation/movement acceptance
broad affected backend/frontend regressions
Dictionary / SQLAlchemy / Alembic / OpenAPI/client reconciliation
Temporal exact API inventory + post-B03 semantic operationId gate
DB README + Timeline candidate overlay reconciliation
map / roadmap / handoff / final B04 closure record
```

Execution discipline for B04-F:

- first inventory what is already proven by B04-A..E and do not rerun redundant micro-tests;
- run compact whole-B04 backend/PostgreSQL regressions locally;
- run exact Temporal OpenAPI/inventory and generated-client parity only where required by the already-public B04-A/B/C contract;
- inspect current frontend Create/edit/read/explanation behavior and distinguish prototype-only fields from backend-backed truth;
- request manual userTest only for product behavior that cannot be proven in the connector/runtime environment;
- close B04 only after every frozen ledger item is implemented, explicitly deferred, or proven out-of-scope with an owner/reopening trigger.

---

# 4. B05–B15

```text
B05 Product Organization
B06 Routine / Recurrence / Occurrence Baseline
B07 UI/UX Consolidation v1
B08 Session Runtime
B09 Responsibility / Participation
B10 Actual / Outcome / Confirmation / Resolution
B11 Advanced Recurrence / Conditional / Reminder
B12 Replanning / Conflict / Solver
B13 Provider / Offline / Multi-device
B14 Analytics / Statistics / Signals
B15 Whole Vertical Closure
```

# 5. Current gate

```text
B04-E ✅ CLOSED / PROVEN
B04-F 🟡 ACTIVE
```

Immediate action: perform the compact whole-B04 proof/reconciliation matrix. CI remains separate and is not implicitly authorized.
