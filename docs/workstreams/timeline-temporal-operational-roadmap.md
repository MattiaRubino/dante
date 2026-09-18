# Timeline / Temporal-Operational Vertical — Implementation Roadmap

- **Status:** CURRENT EXECUTION ROADMAP — reconciled 2026-09-18
- **Branch/workstream:** `feature/timeline-temporal-operational`
- **Current completed frontier:** B03 Event Core ✅ CLOSED / PROVEN
- **Current active/next block:** B04 Temporal Constraints + Movement Policy
- **Next implementation gate:** `APPROVE B04`
- **Current candidate DB authority:** PostgreSQL 18.6 / Alembic `20260917_29`
- **Current candidate topology:** `101|5|31|78|198|119|297|0|0|0`
- **Live progress ledger:** `docs/workstreams/timeline-temporal-operational-map.md`
- **B03 plan/closed execution authority:** `docs/workstreams/timeline-temporal-operational-b03-execution-plan.md`
- **B03-E / whole-B03 closure:** `docs/workstreams/timeline-temporal-operational-b03-e-closure-2026-09-18.md`
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

---

# 1. Current ordered roadmap

```text
B00 Real Data Spine                              ✅ CLOSED / PROVEN
B01 Activity Core                                ✅ CLOSED / PROVEN
B02 Schedule Core                                ✅ CLOSED / PROVEN
B03 Event Core                                   ✅ CLOSED / PROVEN
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

B03 proved Event as a distinct canonical owner using the same Schedule capability as Activity. It includes:

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

---

# 3. B04 — Temporal Constraints + Movement Policy ⬜ NEXT

B04 introduces **Temporal Constraint truth distinct from Schedule placement** and establishes movement/replanning policy foundations without turning constraints into placements or solver decisions.

Before implementation B04 must reopen the relevant Domain / Logical / Physical authority and map every constraint/movement capability against the archived semantic freeze.

Expected non-collapse boundaries include:

```text
Schedule != Temporal Constraint
constraint != accepted placement
movement policy != solver result
proposal != accepted mutation
planned/intended != happened
```

No B04 implementation is considered approved until the explicit `APPROVE B04` gate.

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
B03 Event Core  ✅ CLOSED / PROVEN
B04             ⬜ NEXT

Next explicit gate: APPROVE B04
```

CI remains separate and is not implicitly authorized.