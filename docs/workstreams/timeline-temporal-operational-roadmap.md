# Timeline / Temporal-Operational Vertical — Implementation Roadmap

- **Status:** CURRENT EXECUTION ROADMAP — reconciled 2026-09-18
- **Branch/workstream:** `feature/timeline-temporal-operational`
- **Current completed frontier:** B03 Event Core ✅ CLOSED / PROVEN
- **Pre-B04 governance gate:** ✅ CLOSED / BASELINE FROZEN
- **Current active/next block:** B04 Temporal Constraints + Movement Policy
- **Next implementation gate:** `APPROVE B04`
- **Current candidate DB authority:** PostgreSQL 18.6 / Alembic `20260917_29`
- **Current candidate topology:** `101|5|31|78|198|119|297|0|0|0`
- **Live progress ledger:** `docs/workstreams/timeline-temporal-operational-map.md`
- **B03 plan/closed execution authority:** `docs/workstreams/timeline-temporal-operational-b03-execution-plan.md`
- **B03-E / whole-B03 closure:** `docs/workstreams/timeline-temporal-operational-b03-e-closure-2026-09-18.md`
- **Pre-B04 governance closure:** `docs/workstreams/timeline-temporal-operational-pre-b04-governance-2026-09-18.md`
- **Timeline candidate DB overlay:** `docs/database/timeline-temporal-operational.md`
- **Detailed semantic freeze:** `docs/workstreams/archive/timeline-temporal-operational-map-ledger-snapshot-2026-09-15.md`

The archived semantic freeze preserves the complete functionality/non-collapse inventory. This document is the current sequencing authority.

---

# 0. Fixed execution contract

```text
semantic capability
→ current persistence inspection
→ DDL only if a real gap exists
→ backend/application operation/query
→ API/transport
→ frontend integration
→ read model/projection
→ automated tests
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
Schedule != Session != Actual
Session != Actual != Outcome
Routine != Recurrence != Occurrence
provider identity != DANTE identity
proposal != accepted effect
pending != success
idempotency key != Domain identity
current accepted state != latest row
Undo != history rewind
Agenda part != Activity/Event/Occurrence/Schedule/Session/Actual by default
postponed/TBD Event != Planning Tray Activity
```

A block closes only after applicable semantic, persistence, backend, frontend, proof and documentation gates are reconciled.

For every DB-affecting B04+ slice the same reviewed change must reconcile Alembic, SQLAlchemy, Dictionary/scope, real catalog, ACL, current DB references, the Timeline DB overlay, direct PostgreSQL proof and affected workstream docs.

For every public Temporal API change the same reviewed change must reconcile the exact Temporal `(path, method) -> operationId` inventory, OpenAPI snapshot, generated `@dante/api-client`, affected tests and workstream docs. Existing pre-B04 operationIds are frozen compatibility baseline; new Temporal operations require explicit stable semantic operationIds rather than implicit FastAPI naming.

---

# 1. Current ordered roadmap

```text
B00 Real Data Spine                              ✅ CLOSED / PROVEN
B01 Activity Core                                ✅ CLOSED / PROVEN
B02 Schedule Core                                ✅ CLOSED / PROVEN
B03 Event Core                                   ✅ CLOSED / PROVEN
PRE-B04 DB/API GOVERNANCE                        ✅ CLOSED / FROZEN
B04 Temporal Constraints + Movement Policy       ⬜ NEXT
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

Dependency chain remains:

```text
REAL DATA SPINE
→ ACTIVITY CORE
→ SCHEDULE CORE
→ EVENT CORE
→ PRE-B04 DB/API GOVERNANCE
→ TEMPORAL CONSTRAINTS + PRODUCT ORGANIZATION
→ ROUTINE / RECURRENCE / OCCURRENCE BASELINE
→ UI/UX CONSOLIDATION v1
→ SESSION RUNTIME
→ ACTOR RELATIONS / PARTICIPATION
→ ACTUAL / OUTCOME / CONFIRMATION / RESOLUTION
→ ADVANCED RECURRENCE / CONDITIONAL POLICY / REMINDERS
→ REPLANNING / CONFLICT / SOLVER
→ PROVIDER / OFFLINE / MULTI-DEVICE
→ ANALYTICS / SIGNALS
→ WHOLE-VERTICAL CLOSURE
```

---

# 2. Completed foundation

## B00 — Real Data Spine ✅

Authenticated frontend → backend → DanteContext/self Person → PostgreSQL truth and real empty/error behavior are established.

## B01 — Activity Core ✅

Canonical Activity identity, actionable-intention descriptor, idempotent create, Planning Tray/read projection and reload identity are established.

## B02 — Schedule Core ✅

One shared Schedule identity/current/history machinery is proven for Activity across accepted temporal forms and lifecycle semantics including CAS, idempotency, unschedule, guarded Undo and DST/source-intent handling.

## B03 — Event Core ✅ CLOSED / PROVEN

B03 proved Event as a distinct canonical owner using the same Schedule capability as Activity:

```text
B03-A Event canonical core                    ✅
B03-B shared Schedule + Event Timeline        ✅
B03-C Event placement lifecycle               ✅
B03-D Agenda/internal parts                   ✅
B03-E whole-B03 proof + manual acceptance     ✅
```

Final whole-B03 evidence includes:

```text
real-stack Chromium + Firefox                 2 PASS
web broad regression                          158 files / 741 PASS
Temporal PostgreSQL broad regression          24 PASS / 2 deselected
backend broad                                 494 PASS + one generated snapshot mismatch
OpenAPI governance after canonical generation 8 PASS
manual Event userTest A–F                     PASS
```

Closure authority: `docs/workstreams/timeline-temporal-operational-b03-e-closure-2026-09-18.md`.

No recurrence, participants, Session, Actual/Outcome, reminders or provider sync were pulled into B03.

## Pre-B04 DB/API governance ✅ CLOSED / FROZEN

Before B04, current DB documentation was reconciled to `_29`, a candidate-specific DB overlay was established, stale B03-D pre-closure prose was removed, and the complete 13-operation Temporal API surface was placed under exact OpenAPI inventory/operationId governance.

Authority: `docs/workstreams/timeline-temporal-operational-pre-b04-governance-2026-09-18.md`.

This gate changes governance, not product semantics; B04 remains unstarted.

---

# 3. B04 — Temporal Constraints + Movement Policy ⬜ NEXT

B04 introduces **Temporal Constraint truth distinct from Schedule placement** and establishes movement/replanning policy foundations without turning constraints into placements or solver decisions.

The B04 pre-scope/execution plan is frozen. Implementation starts only after the explicit `APPROVE B04` gate and must obey the DB/API same-change gates frozen by the pre-B04 governance closure.

Expected non-collapse boundaries include:

```text
Schedule != Temporal Constraint
constraint != accepted placement
movement policy != solver result
proposal != accepted mutation
planned/intended != happened
```

---

# 4. B05 — Product Organization ⬜

Activate Calendar/Life Area, Tags and accepted grouping/context semantics without turning presentation organization into temporal truth.

Transferred from B03 manual acceptance:

```text
provide a discoverable surface for postponed/TBD Events
so they can later be explicitly rescheduled
without converting them into Activity Planning Tray items
and without fabricating date/time truth
```

---

# 5. B06 — Routine / Recurrence / Occurrence Baseline ⬜

Activate Routine as owner, Recurrence as policy and Occurrence as generated instance; Event recurrence is activated here, not in B03.

# 6. B07 — UI/UX Consolidation v1 ⬜

Dedicated product-quality planning checkpoint after B06, when Activity/Event/Constraint/Organization/Routine vocabulary is stable enough for serious consolidation without repeated rebuilds.

# 7. B08 — Session Runtime ⬜

Real execution runtime; Session remains distinct from Schedule and Actual.

# 8. B09 — Responsibility / Participation ⬜

Actor relations, responsibility and participation/invitation boundaries.

# 9. B10 — Actual / Outcome / Confirmation / Resolution ⬜

Record what actually happened and the resulting authoritative resolution flow.

# 10. B11 — Advanced Recurrence / Conditional / Reminder ⬜

Advanced recurrence, bounded conditional effects and reminders.

# 11. B12 — Replanning / Conflict / Solver ⬜

Conflict detection, candidate generation and governed acceptance.

# 12. B13 — Provider / Offline / Multi-device ⬜

Provider mapping/sync/conferencing plus offline and multi-device reconciliation.

# 13. B14 — Analytics / Statistics / Signals ⬜

Derived analytics/signals over accepted canonical truth.

# 14. B15 — Whole Vertical Closure ⬜

Cross-block regression, recovery/anti-resurrection, operational hardening and final acceptance.

---

# 15. Current gate

```text
B03 Event Core             ✅ CLOSED / PROVEN
Pre-B04 DB/API governance  ✅ CLOSED / FROZEN
B04                        ⬜ NEXT

Next explicit gate: APPROVE B04
```

CI remains separate and is not implicitly authorized.