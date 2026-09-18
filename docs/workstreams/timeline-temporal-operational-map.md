# Timeline / Temporal-Operational Vertical — Semantic Work Map / Live Ledger

- **Status:** CURRENT SEMANTIC MAP + LIVE IMPLEMENTATION LEDGER — reconciled 2026-09-18
- **Branch:** `feature/timeline-temporal-operational`
- **Roadmap:** `docs/workstreams/timeline-temporal-operational-roadmap.md`
- **B03 closed execution authority:** `docs/workstreams/timeline-temporal-operational-b03-execution-plan.md`
- **B03-E / whole-B03 closure:** `docs/workstreams/timeline-temporal-operational-b03-e-closure-2026-09-18.md`
- **B03 manual acceptance:** `docs/workstreams/timeline-temporal-operational-b03-usertest.md` ✅ PASS
- **Detailed semantic freeze:** `docs/workstreams/archive/timeline-temporal-operational-map-ledger-snapshot-2026-09-15.md`

The archived semantic freeze remains the binding detailed inventory for the full vertical. This file is the current implementation/proof ledger; compacting it does not weaken that archived semantic contract.

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
Schedule != Session
Schedule != Actual
Session != Actual
Actual != Outcome
Outcome != Confirmation
planned/intended != happened
current accepted state != latest row
idempotency key != Domain identity
provider identity != DANTE identity
projection != canonical truth
proposal != accepted effect
pending != success
unscheduled != deleted
Undo != DB/history rewind
estimated effort != scheduled duration != Session duration
floating-local != named-zone-local != absolute instant
date span != coarse local period
coarse precision != fabricated exact clock time
source wall-clock intent != resolved instant
Agenda part != Activity/Event/Occurrence/Schedule/Session/Actual by default
Event != Availability / Capacity Claim
postponed/TBD Event != Planning Tray Activity
```

These boundaries cannot be weakened by UI convenience, ORM convenience, provider shape or roadmap pressure.

---

# 2. Current roadmap position

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

Current candidate persistence authority:

```text
Alembic head     20260917_29
Topology         101|5|31|78|198|119|297|0|0|0
```

---

# 3. Completed foundation

## B00 — Real Data Spine ✅

Authenticated frontend → backend/application → DanteContext/self Person → PostgreSQL truth, truthful empty/error behavior and isolated real-stack proof are established.

## B01 — Activity Core ✅

Canonical Activity identity, self-owned actionable-intention descriptor, idempotent create, Planning Tray/read path and reload identity are established.

## B02 — Schedule Core ✅

All accepted Schedule forms and lifecycle behavior are proven at B02 scope: date-span, floating-local, named-zone-local, absolute, coarse-local-period, establish/revision/current/history/CAS/idempotency/unschedule/guarded Undo/DST and product integration.

---

# 4. B03 — Event Core ✅ CLOSED / PROVEN

B03 activates Event as a distinct originating owner while keeping one shared Schedule engine:

```text
Activity ─┐
          ├── one Schedule identity/current/history capability
Event ────┘
```

Forbidden:

```text
event_schedule
Event-specific temporal engine
Event-specific Schedule current/history model
Event-as-Activity shortcut
Event-as-busy/capacity shortcut
```

## 4.1 Capability ledger

- ✅ **[EVT-001]** Event Domain/Logical/Physical authority re-opened before implementation.
- ✅ **[EVT-002]** Canonical Event expectation persistence activated.
- ✅ **[EVT-003]** Idempotent governed Event create activated.
- ✅ **[EVT-004]** Event macro-class activated in Create for truthful supported scope.
- ✅ **[EVT-005]** Timed Event uses shared Schedule capability.
- ✅ **[EVT-006]** All-day/date-span Event preserves non-timed truth.
- ✅ **[EVT-007]** Multi-day Event semantics/query/rendering preserve date-span truth.
- ✅ **[EVT-008]** Postponed/TBD retains Event and Schedule history with no current placement.
- ✅ **[EVT-009]** Event expectation/current Schedule separation proven; Actual remains B10-owned.
- ✅ **[EVT-010]** Event Agenda/internal parts activated at accepted product level.
- ✅ **[EVT-011]** Agenda part remains Event-internal value: `!= Activity/Event/Occurrence/Schedule/Session/Actual` by default.
- ⬜ **[EVT-012]** Preparation/follow-up Activity relation only when exact relation semantics are activated.
- ⬜ **[EVT-013]** Place/conference intent only through justified relation/profile semantics.
- ⬜ **[EVT-014]** Ordinary Event attendance `!= Session`; later actor/execution blocks own the relevant behavior.
- ⬜ **[EVT-015]** Event `!= Availability/Capacity Claim`; future availability semantics must remain distinct.

Items 012–015 remain future-owner semantic obligations, not unfinished B03 implementation.

## 4.2 Proof ledger

- ✅ **[B03-T01]** Event create/application PostgreSQL/API proof.
- ✅ **[B03-T02]** Timed/all-day/multi-day shared-Schedule proof.
- ✅ **[B03-T03]** Postponed/TBD history/query/CAS/guarded-Undo proof.
- ✅ **[B03-T04]** Event Agenda persistence/API/frontend/add-edit-reorder-remove/reload/CAS proof.
- ✅ **[B03-T05]** Shared Schedule Activity + Event regression remains green through `_29`.
- ✅ **[B03-T06]** Real-stack Event create/reschedule/all-day/multi-day/reload acceptance in Chromium + Firefox.
- ✅ **[B03-T07]** Manual Event userTest A–F accepted after closing the Agenda rename UX defect.
- ✅ **[B03-T08]** Broad web regression: 158 files / 741 tests PASS.
- ✅ **[B03-T09]** Broad Temporal PostgreSQL regression: 24 PASS / 2 deselected.
- ✅ **[B03-T10]** Broad backend reached 494 PASS with sole generated OpenAPI mismatch; canonical regeneration followed by focused OpenAPI gate 8 PASS.

## 4.3 Slice closures

```text
B03-A Event canonical core                  ✅ CLOSED / PROVEN
B03-B Shared Schedule + Event Timeline      ✅ CLOSED / PROVEN
B03-C Event placement lifecycle             ✅ CLOSED / PROVEN
B03-D Agenda/internal parts                 ✅ CLOSED / PROVEN
B03-E Whole-B03 closure                     ✅ CLOSED / PROVEN
```

Closure authorities:

```text
timeline-temporal-operational-b03-a-closure-2026-09-16.md
timeline-temporal-operational-b03-b-closure-2026-09-17.md
timeline-temporal-operational-b03-c-closure-2026-09-17.md
timeline-temporal-operational-b03-d-closure-2026-09-17.md
timeline-temporal-operational-b03-e-closure-2026-09-18.md
```

## 4.4 B03 manual-acceptance transfer

B03-C correctly models postponed/TBD as:

```text
Event alive
+ Schedule/history retained
+ no current placement
```

The manual test exposed a product-organization gap after the immediate Undo affordance expires: the user needs a discoverable surface for postponed/TBD Events and an explicit way to reschedule them later.

Transferred to B05:

- ⬜ **[ORG-EVT-TBD-001]** Surface postponed/TBD Events for rediscovery and explicit replanning without converting them into Activity Planning Tray items or fabricating date/time truth.

Agenda remains internal Event content. If independently timed sub-events/segments are ever required, they need a distinct future semantic model rather than an Agenda shortcut.

---

# 5. B04 — Temporal Constraints + Movement Policy ⬜ NEXT

B04 must begin from the archived functionality map and current Domain/Logical/Physical authority, then establish Temporal Constraint truth as distinct from Schedule placement.

Initial non-collapse obligations:

```text
Schedule != Temporal Constraint
constraint != placement
movement policy != accepted movement
proposal != accepted effect
solver candidate != canonical truth
```

No B04 code is authorized merely by this ledger; the explicit next gate is `APPROVE B04`.

---

# 6. B05–B15 ownership register

The detailed functionality lists remain binding in the archived semantic freeze.

```text
B05  Calendar / Life Area / Tags / product organization
     + postponed/TBD Event rediscovery/replanning surface transferred from B03
B06  Routine + Recurrence + Occurrence baseline
B07  UI/UX Consolidation v1
B08  Session Runtime
B09  Responsibility / Participation / actor relations
B10  Actual + Outcome + Confirmation + Resolution Queue
B11  advanced recurrence + conditional policy + reminders
B12  replanning/conflict/solver
B13  provider integration + offline/multi-device reconciliation
B14  analytics/statistics/Signals
B15  whole-vertical closure/recovery/cross-cutting proof
```

---

# 7. Current gate

```text
B03 Event Core  ✅ CLOSED / PROVEN
B04             ⬜ NEXT

Next explicit gate: APPROVE B04
```

CI remains separately authorized.