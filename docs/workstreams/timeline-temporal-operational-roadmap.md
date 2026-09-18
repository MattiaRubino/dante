# Timeline / Temporal-Operational Vertical — Implementation Roadmap

- **Status:** CURRENT EXECUTION ROADMAP — reconciled 2026-09-18
- **Branch/workstream:** `feature/timeline-temporal-operational`
- **Current completed frontier:** B03 Event Core ✅ CLOSED / PROVEN
- **Pre-B04 governance gate:** ✅ CLOSED / BASELINE FROZEN
- **Current active block:** B04 Temporal Constraints + Movement Policy
- **Current active slice:** B04-A Temporal Constraint canonical core — A4 reconciliation proof pending
- **Current candidate DB authority:** PostgreSQL 18.6 / Alembic `20260918_32`
- **Current candidate topology:** `107|5|33|85|212|129|309|0|0|0`
- **Live progress ledger:** `docs/workstreams/timeline-temporal-operational-map.md`
- **B04 execution authority:** `docs/workstreams/timeline-temporal-operational-b04-execution-plan.md`
- **B04-A implementation freeze:** `docs/workstreams/timeline-temporal-operational-b04-a-implementation-freeze.md`
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
Temporal Constraint != Movement Policy
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

For every public Temporal API change the same reviewed change must reconcile the exact Temporal `(path, method) -> operationId` inventory, OpenAPI snapshot, generated `@dante/api-client`, affected tests and workstream docs. Existing pre-B04 operationIds are frozen compatibility baseline; new Temporal operations require explicit stable semantic operationIds.

---

# 1. Current ordered roadmap

```text
B00 Real Data Spine                              ✅ CLOSED / PROVEN
B01 Activity Core                                ✅ CLOSED / PROVEN
B02 Schedule Core                                ✅ CLOSED / PROVEN
B03 Event Core                                   ✅ CLOSED / PROVEN
PRE-B04 DB/API GOVERNANCE                        ✅ CLOSED / FROZEN
B04 Temporal Constraints + Movement Policy       🟡 IN PROGRESS
├─ B04-A Temporal Constraint canonical core      🟡 IN PROGRESS
├─ B04-B Boundary / Deadline constraints         ⬜
├─ B04-C Windows / Preferences / Evaluation      ⬜
├─ B04-D Movement Policy                         ⬜
├─ B04-E Advanced-family applicability           ⬜
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

Dependency chain remains:

```text
REAL DATA SPINE
→ ACTIVITY CORE
→ SCHEDULE CORE
→ EVENT CORE
→ PRE-B04 DB/API GOVERNANCE
→ B04 TEMPORAL CONSTRAINTS + MOVEMENT POLICY
→ B05 PRODUCT ORGANIZATION
→ B06 ROUTINE / RECURRENCE / OCCURRENCE BASELINE
→ B07 UI/UX CONSOLIDATION v1
→ B08 SESSION RUNTIME
→ B09 ACTOR RELATIONS / PARTICIPATION
→ B10 ACTUAL / OUTCOME / CONFIRMATION / RESOLUTION
→ B11 ADVANCED RECURRENCE / CONDITIONAL POLICY / REMINDERS
→ B12 REPLANNING / CONFLICT / SOLVER
→ B13 PROVIDER / OFFLINE / MULTI-DEVICE
→ B14 ANALYTICS / SIGNALS
→ B15 WHOLE-VERTICAL CLOSURE
```

---

# 2. Completed foundation

## B00 — Real Data Spine ✅

Authenticated frontend → backend → DanteContext/self Person → PostgreSQL truth and real empty/error behavior are established.

## B01 — Activity Core ✅

Canonical Activity identity, actionable-intention descriptor, idempotent create, Planning Tray/read projection and reload identity are established.

## B02 — Schedule Core ✅

One shared Schedule identity/current/history machinery is proven across accepted temporal forms and lifecycle semantics including CAS, idempotency, unschedule, guarded Undo and DST/source-intent handling.

## B03 — Event Core ✅ CLOSED / PROVEN

```text
B03-A Event canonical core                    ✅
B03-B shared Schedule + Event Timeline        ✅
B03-C Event placement lifecycle               ✅
B03-D Agenda/internal parts                   ✅
B03-E whole-B03 proof + manual acceptance     ✅
```

Whole-B03 evidence remains historical closure authority. No recurrence, participants, Session, Actual/Outcome, reminders or provider sync were pulled into B03.

## Pre-B04 DB/API governance ✅ CLOSED / FROZEN

The governance closure fixed DB-reference drift, established the candidate DB overlay, froze the complete 13-operation pre-B04 Temporal API surface and made exact DB/API same-change reconciliation binding for B04+.

---

# 3. B04 — Temporal Constraints + Movement Policy 🟡 IN PROGRESS

B04 introduces **Temporal Constraint truth distinct from Schedule placement** and establishes movement/replanning policy foundations without turning constraints into placements or solver decisions.

Permanent B04 boundaries:

```text
Schedule != Temporal Constraint
Temporal Constraint != Movement Policy
constraint != accepted placement
movement policy != solver result
proposal != accepted mutation
hard planning violation != impossible reality
planned/intended != happened
```

## B04-A — Temporal Constraint canonical core 🟡

Frozen scope activates a stable self-owned Activity/Event constraint identity and the first complete typed `absolute earliest-start` rule.

Execution order and current state:

```text
A1 exact DDL + SQLAlchemy                         ✅ PROVEN
A2 direct PostgreSQL structural/integrity proof   ✅ PROVEN
A3 create/revise/retire CAS + idempotency         ✅ PROVEN
A4 Dictionary/current-catalog/DB docs             🟡 MATERIALIZED; proof pending
A5 application/API                                ⬜ NOT STARTED
B04-A closure proof                               ⬜
```

Candidate persistence authority after A1-A3:

```text
Alembic   20260918_32
Topology  107|5|33|85|212|129|309|0|0|0
```

The A2/A3 evidence includes focused B04-A behavior `4 PASS`, shared current-history dispatch `4 PASS`, wider Temporal+CP6 final regression `32 PASS / 2 deselected`, and catalog/owner/ACL proof `3 PASS`.

A4 is now represented in Dictionary/current DB references, but it does not become ✅ until the reconciled whole-DB current-catalog gates pass against `_32`.

A5 must begin only after A4 is green. Every new public Temporal endpoint in A5 requires an explicit stable `temporal_*` operationId; the existing 13 pre-B04 operationIds are frozen compatibility baseline.

## B04-B — Boundary / Deadline constraints ⬜

Expand truthful boundary semantics beyond the B04-A earliest-start absolute prototype, including earliest-start, latest-start and latest-completion/deadline while preserving date/floating/named-zone/absolute precision. Passing a deadline does not create Outcome truth.

## B04-C — Windows / Preferences / Evaluation ⬜

Hard windows, soft preferred windows and explicit relation semantics such as start-within, completion-within, full-contained and overlaps. Evaluation/explanation is allowed; solver ownership remains B12.

## B04-D — Movement Policy ⬜

Activate movement policy separately from constraint truth and solver output. Candidate policy vocabulary remains subject to exact implementation freeze; accepted movement/override must remain explicit and governed.

## B04-E — Advanced-family applicability ⬜

Min/max duration, spacing and relative constraints only where truthful anchors already exist. Ambiguous dependencies on Routine/Session/Actual/Solver remain deferred to their owning blocks.

## B04-F — Whole-B04 closure ⬜

Whole-B04 regression, DB/docs/API contract consistency, applicable product/manual acceptance and final closure evidence.

**B05 begins only after B04-F, not after B04-A.**

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

Activate Routine as owner, Recurrence as policy and Occurrence as generated instance; Event recurrence product behavior is activated here rather than collapsed into Event core.

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
Pre-B04 governance         ✅ CLOSED / FROZEN
B04                        🟡 IN PROGRESS
└─ B04-A
   ├─ A1                   ✅
   ├─ A2                   ✅
   ├─ A3                   ✅
   ├─ A4                   🟡 reconciliation proof pending
   └─ A5                   ⬜
```

Immediate next gate: prove A4 Dictionary/current-catalog reconciliation locally. After A4 turns green, open a separate B04-A5 application/API scope.

CI remains separate and is not implicitly authorized.
