# Timeline / Temporal-Operational Vertical — Semantic Work Map / Live Ledger

- **Status:** CURRENT SEMANTIC MAP + LIVE IMPLEMENTATION LEDGER — reconciled 2026-09-18
- **Branch:** `feature/timeline-temporal-operational`
- **Roadmap:** `docs/workstreams/timeline-temporal-operational-roadmap.md`
- **B03 closed execution authority:** `docs/workstreams/timeline-temporal-operational-b03-execution-plan.md`
- **B03-E / whole-B03 closure:** `docs/workstreams/timeline-temporal-operational-b03-e-closure-2026-09-18.md`
- **B03 manual acceptance:** `docs/workstreams/timeline-temporal-operational-b03-usertest.md` ✅ PASS
- **Pre-B04 governance closure:** `docs/workstreams/timeline-temporal-operational-pre-b04-governance-2026-09-18.md` ✅ CLOSED / FROZEN
- **B04 execution plan:** `docs/workstreams/timeline-temporal-operational-b04-execution-plan.md`
- **B04-A implementation freeze:** `docs/workstreams/timeline-temporal-operational-b04-a-implementation-freeze.md`
- **Timeline candidate DB overlay:** `docs/database/timeline-temporal-operational.md`
- **Detailed semantic freeze:** `docs/workstreams/archive/timeline-temporal-operational-map-ledger-snapshot-2026-09-15.md`

The archived semantic freeze remains the binding detailed inventory for the full vertical. This file is the current implementation/proof ledger; compacting historical evidence here does not weaken that archived semantic contract.

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
Temporal Constraint != Movement Policy
Temporal Constraint != Recurrence
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

Current candidate persistence authority:

```text
Alembic head     20260918_32
Topology         107|5|33|85|212|129|309|0|0|0
```

Governance baseline remains binding:

```text
DB same-change gate          ✅ FROZEN
candidate DB overlay         ✅ ESTABLISHED
Temporal exact API inventory ✅ 13 pre-B04 operations frozen
new API operationId rule     ✅ explicit stable semantic IDs required
OpenAPI → Orval/client gate  ✅ BINDING
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

Items 012–015 remain future-owner semantic obligations, not unfinished B03 implementation. Their unchecked state is deliberate and must not be changed to fabricate completeness.

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

## 4.4 B03 manual-acceptance transfer

Postponed/TBD semantics remain:

```text
Event alive
+ Schedule/history retained
+ no current placement
```

Transferred to B05:

- ⬜ **[ORG-EVT-TBD-001]** Surface postponed/TBD Events for rediscovery and explicit replanning without converting them into Activity Planning Tray items or fabricating date/time truth.

---

# 5. Pre-B04 DB/API governance ✅ CLOSED / FROZEN

- ✅ **[GOV-DB-001]** Whole DB SoR reconciled to protected-main `_18` and entering Timeline candidate `_29` without collapsing the two authorities.
- ✅ **[GOV-DB-002]** Dictionary README reconciled to whole-B03 closure.
- ✅ **[GOV-DB-003]** Timeline candidate-specific DB overlay established.
- ✅ **[GOV-DB-004]** Protected-main architecture banner/topology reconciled to `_18` while historical phase evidence remains historical.
- ✅ **[GOV-DB-005]** DB same-change closure rule frozen for all B04+ persistence slices.
- ✅ **[GOV-API-001]** Exact pre-B04 Temporal public API inventory frozen at 13 operations.
- ✅ **[GOV-API-002]** `(path, method) -> operationId` exact-set and uniqueness test added.
- ✅ **[GOV-API-003]** Existing verbose pre-B04 operationIds retained as compatibility contract.
- ✅ **[GOV-API-004]** Every new B04+ Temporal endpoint must use an explicit stable semantic operationId and reconcile OpenAPI/Orval/client/tests in the same change.

Authority: `timeline-temporal-operational-pre-b04-governance-2026-09-18.md`.

---

# 6. B04 — Temporal Constraints + Movement Policy 🟡 IN PROGRESS

B04 establishes Temporal Constraint truth distinct from Schedule placement and later activates Movement Policy without collapsing policy, proposal, solver result or accepted effect.

## 6.1 B04-A — Temporal Constraint canonical core 🟡 IN PROGRESS

Frozen first complete rule:

```text
subject             self-owned Activity | Event
identity            ScopedRecordRef, not NativeRef
facet               temporal_constraint.rule
family              boundary
boundary kind       earliest_start
constrained facet   schedule.start
strength            hard | soft
temporal form       absolute
boundary             finite timestamptz
```

Permanent B04-A non-collapse:

```text
Temporal Constraint != Schedule
Temporal Constraint != Movement Policy
Temporal Constraint != Recurrence
Temporal Constraint != Session / Actual
Temporal Constraint != Availability / Capacity
constraint revision != Schedule revision
proposal != accepted constraint
current accepted state != newest row
idempotency receipt != constraint identity != MaterialState identity
```

### A1 — DDL / mappings ✅ PROVEN

Candidate migrations:

```text
20260918_30 temporal_constraint_core
20260918_31 temporal_constraint_totality_hardening
20260918_32 current_history_dispatch_hardening
```

Six canonical/control tables and two new routines are materialized; SQLAlchemy registers exactly the six Temporal Constraint mappings. Shared CP6 dispatchers are extended rather than duplicated.

### A2 — direct PostgreSQL structural/integrity proof ✅ PROVEN

Evidence includes:

```text
focused B04-A core                            4 PASS
shared current-history legacy-family proof    4 PASS
Temporal + CP6 final regression              32 PASS / 2 deselected
B04-A catalog / owner / ACL                   3 PASS
```

Direct `_32` topology:

```text
107|5|33|85|212|129|309|0|0|0
```

A2 proves Activity/Event ownership boundaries, runtime no-direct-bypass, typed rule totality, MaterialState exclusivity and correct shared current-history dispatch.

### A3 — create / revise / retire CAS + idempotency ✅ PROVEN

Proven behavior:

```text
create establishes stable constraint + scoped address + immutable complete rule state
same operation id + same material intent replays accepted result
same key + changed intent conflicts
revise requires expected current MaterialStateRef
stale expected state conflicts
revise appends state and closes/opens history
retire requires expected current state
retire removes only current binding and closes history
stable constraint/history survive retirement
```

### A4 — DB / Dictionary / docs 🟡 MATERIALIZED, PROOF PENDING

Current A4 change reconciles:

```text
Dictionary 107 tables / 5 views / 33 routines
scope 145 standalone / 85 triggers / 212 indexes / 129 FK / 309 CHECK
current-catalog expectations → 20260918_32
DB SoR + Timeline DB overlay
live map / roadmap / handoff
```

A4 remains open until the whole-DB Dictionary/current-catalog tests run green against PostgreSQL `_32`.

### A5 — application / API ⬜ NOT STARTED

No public Temporal Constraint endpoint has been activated yet. A5 must obey the frozen API governance chain:

```text
application operation/query
→ explicit stable temporal_* operationId
→ exact Temporal inventory
→ OpenAPI snapshot
→ pnpm api:generate
→ @dante/api-client
→ affected API/frontend tests
→ docs
```

Existing 13 pre-B04 Temporal operationIds remain frozen compatibility baseline.

## 6.2 Remaining B04 slices

```text
B04-B Boundary / Deadline constraints          ⬜
B04-C Windows / Preferences / Evaluation       ⬜
B04-D Movement Policy                          ⬜
B04-E Advanced-family applicability            ⬜
B04-F Whole-B04 closure                        ⬜
```

B04-A completion does not transition directly to B05.

---

# 7. B05–B15 ownership register

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

The detailed functionality lists remain binding in the archived semantic freeze.

---

# 8. Current gate

```text
B03 Event Core             ✅ CLOSED / PROVEN
Pre-B04 governance         ✅ CLOSED / FROZEN
B04                        🟡 IN PROGRESS
└─ B04-A
   ├─ A1                   ✅
   ├─ A2                   ✅
   ├─ A3                   ✅
   ├─ A4                   🟡 reconciliation materialized; proof pending
   └─ A5                   ⬜
```

Immediate gate: run the reconciled A4 Dictionary/current-catalog PostgreSQL proof. Only after A4 is green does the workstream move to the separate B04-A5 application/API scope.

CI remains separately authorized and is not implicitly launched.
