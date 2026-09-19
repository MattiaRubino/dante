# Timeline / Temporal-Operational Vertical — Implementation Roadmap

- **Status:** CURRENT EXECUTION ROADMAP — reconciled 2026-09-19
- **Branch/workstream:** `feature/timeline-temporal-operational`
- **Current completed frontier:** B04-D Movement Policy ✅ CLOSED / PROVEN
- **Current active block:** B04 Temporal Constraints + Movement Policy
- **Current next slice:** B04-E Advanced-family applicability
- **Current candidate DB authority:** PostgreSQL 18.6 / Alembic `20260919_39`
- **Current candidate topology:** `115|5|42|89|232|152|329|0|0|0`
- **Live progress ledger:** `docs/workstreams/timeline-temporal-operational-map.md`
- **B04 execution authority:** `docs/workstreams/timeline-temporal-operational-b04-execution-plan.md`
- **B04-D closure:** `docs/workstreams/timeline-temporal-operational-b04-d-closure-2026-09-19.md`

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

Dependency chain remains unchanged through B15; B05 starts only after B04-F.

---

# 2. B04 completed slices

## B04-A ✅ CLOSED / PROVEN

Stable self-owned Activity/Event Temporal Constraint identity, immutable `temporal_constraint.rule` MaterialState/current/history, expected-state CAS, idempotent mutation and public CRUD/read capability.

## B04-B ✅ CLOSED / PROVEN

Absolute boundary matrix:

```text
earliest_start     + schedule.start
latest_start       + schedule.start
latest_completion  + schedule.completion
```

## B04-C ✅ CLOSED / PROVEN

Absolute window matrix:

```text
start_within              + schedule.start
completion_within         + schedule.completion
full_placement_contained  + schedule.placement
placement_overlaps        + schedule.placement
```

Derived evaluation distinguishes hard validity, soft preference and not-evaluable states without solver search or automatic mutation.

## B04-D ✅ CLOSED / PROVEN

Movement Policy is separately materialized as `schedule.movement_policy` and decomposes policy into:

```text
automatic_movement_code  blocked | automatic
acceptance_path_code     direct | confirmation_required
```

Governed automatic movement:

```text
blocked                      → reject automation
automatic + direct           → commit only if hard-admissible and placement CAS still matches
automatic + confirmation     → proposal first; accepted Schedule changes only after explicit acceptance
```

Persistence authority:

```text
20260919_37 Movement Policy core
20260919_38 governed absolute Schedule move
20260919_39 proposal-accept replay fix
115|5|42|89|232|152|329|0|0|0
```

B04-D does not search for a candidate placement and does not implement B12 solver/replanning semantics. It does not implement the full future multi-actor Authority model.

No public Temporal HTTP endpoint was added, so no OpenAPI/client regeneration was required.

Observed proof:

```text
Movement Policy / governed move / ACL            7 PASS
whole catalog / Dictionary / SQLAlchemy / DB     3 PASS
```

Closure authority: `timeline-temporal-operational-b04-d-closure-2026-09-19.md`.

---

# 3. B04-E — Advanced-family applicability ⬜ NEXT

B04-E owns explicit applicability and bounded activation for the remaining frozen families:

```text
TC-008 minimum / maximum planned Schedule duration
TC-009 minimum contiguous Session duration
TC-010 spacing / recovery
TC-011 relative-before / relative-after
```

Rules for B04-E:

- activate only semantics whose constrained facts and reference anchors already exist canonically;
- do not fabricate Session/Actual/Occurrence history on Activity/Event;
- do not use generic `related_id + type` or JSON relation payloads;
- preserve extension seams where runtime ownership belongs to B06/B08/B10/B12;
- close each frozen-map item either as implemented or as an explicit applicability deferral with owner/reopening trigger.

Likely truthful subset to assess first: planned Schedule placement duration. Session-contiguous, prior-realization spacing and heterogeneous relative anchors require stricter owner/reference review.

---

# 4. B04-F — Whole-B04 closure ⬜

Whole-B04 regression, DB/docs/API consistency, applicable product/manual acceptance and final closure evidence. B05 starts only after B04-F.

---

# 5. B05–B15

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

# 6. Current gate

```text
B04-D ✅ CLOSED / PROVEN
B04-E ⬜ NEXT
```

Immediate action: freeze the B04-E applicability matrix against current Domain / Logical / Physical authority, then implement only the truthful subset. CI remains separate and is not implicitly authorized.
