# Timeline / Temporal-Operational Vertical — Implementation Roadmap

- **Status:** CURRENT EXECUTION ROADMAP — reconciled 2026-09-22
- **Branch/workstream:** `feature/timeline-temporal-operational`
- **Current completed frontier:** B06-C ✅ CLOSED / PROVEN
- **Current block:** B06 Routine / Recurrence / Occurrence Baseline 🟨 IN PROGRESS — B06-D next
- **Current candidate DB source:** PostgreSQL 18.6 / Alembic `20260922_55`
- **Candidate proven topology:** `145|5|87|92|285|223|408|0|0|0` (B06-C proven)
- **Live progress ledger:** `docs/workstreams/timeline-temporal-operational-map.md`
- **B04 execution authority:** `docs/workstreams/timeline-temporal-operational-b04-execution-plan.md`
- **B04-E closure:** `docs/workstreams/timeline-temporal-operational-b04-e-closure-2026-09-19.md`
- **B04 whole-block closure:** `docs/workstreams/timeline-temporal-operational-b04-f-closure-2026-09-20.md`
- **B05 execution authority:** `docs/workstreams/timeline-temporal-operational-b05-execution-plan.md`
- **B06 execution authority:** `docs/workstreams/timeline-temporal-operational-b06-execution-plan.md`
- **B06-B closure:** `docs/workstreams/timeline-temporal-operational-b06-b-closure-2026-09-22.md`
- **B06-C implementation freeze:** `docs/workstreams/timeline-temporal-operational-b06-c-implementation-freeze.md`
- **B06-C closure:** `docs/workstreams/timeline-temporal-operational-b06-c-closure-2026-09-22.md`

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
B04 Temporal Constraints + Movement Policy       ✅ CLOSED / PROVEN
├─ B04-A Temporal Constraint canonical core      ✅ CLOSED / PROVEN
├─ B04-B Boundary / Deadline constraints         ✅ CLOSED / PROVEN
├─ B04-C Windows / Preferences / Evaluation      ✅ CLOSED / PROVEN
├─ B04-D Movement Policy                         ✅ CLOSED / PROVEN
├─ B04-E Advanced-family applicability           ✅ CLOSED / PROVEN
└─ B04-F Whole-B04 closure                       ✅ CLOSED / PROVEN
B05 Product Organization                         ✅ CLOSED / PROVEN
B06 Routine / Recurrence / Occurrence Baseline   🟨 IN PROGRESS — B06-D next
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

B05-A is closed with direct `_45` proof. B05-B passed 16 selected PostgreSQL tests at `_46` and is closed; its closure record fixes the retained legacy-unassigned boundary. B05-C passed 26 selected direct PostgreSQL tests at `_47` and is closed. B05-D passed deterministic generated/client/typecheck gates, 41 selected web tests and 24 selected PostgreSQL/API/catalog tests at `_48`. B05-E completed the real-stack manual walkthrough; B05 is closed.

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

# 3. B04-F — Whole-B04 closure ✅ CLOSED / PROVEN

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

Closure authority: `timeline-temporal-operational-b04-f-closure-2026-09-20.md`.

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
B04 ✅ CLOSED / PROVEN
B05-A ✅ CLOSED / PROVEN at `_45`
B05-B ✅ CLOSED / PROVEN at `_46`
B05-C ✅ CLOSED / PROVEN at `_47` (26 selected PostgreSQL tests)
B05-D ✅ CLOSED / PROVEN at `_48` (41 selected web + 24 PostgreSQL/API/catalog tests)
B05-E ✅ WHOLE-BLOCK CLOSURE / MANUAL WALKTHROUGH COMPLETE
B05   ✅ CLOSED / PROVEN
B06-A ✅ CLOSED / PROVEN at `_51` (26 selected PostgreSQL/catalog regressions; OpenAPI/client generation + API-client typecheck)
B06-B ✅ CLOSED / PROVEN at `_54` (1 fingerprint + 28 PostgreSQL/catalog regressions; API contract/client typecheck)
B06-C ✅ CLOSED / PROVEN at `_55` (22 selected backend + 41 PostgreSQL tests)
```

Closure authorities:

- `timeline-temporal-operational-b06-a-closure-2026-09-21.md`
- `timeline-temporal-operational-b06-b-closure-2026-09-22.md`
- `timeline-temporal-operational-b06-c-closure-2026-09-22.md`

Current action: begin B06-D shared Schedule, bounded Timeline projection and functional recurring UI from the proven `_55` frontier. No CI or Actions were launched for B06-C.
