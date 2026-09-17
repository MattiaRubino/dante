# Timeline / Temporal-Operational Vertical — Implementation Roadmap

- **Status:** CURRENT EXECUTION ROADMAP — reconciled 2026-09-17
- **Branch/workstream:** `feature/timeline-temporal-operational`
- **Current completed frontier:** B03-D Event Agenda/internal parts ✅ CLOSED / PROVEN
- **Current active block:** B03 Event Core
- **Next implementation gate:** `APPROVE B03-E`
- **Current candidate DB authority:** PostgreSQL 18.6 / Alembic `20260917_29`
- **Current candidate topology:** `101|5|31|78|198|119|297|0|0|0`
- **Live progress ledger:** `docs/workstreams/timeline-temporal-operational-map.md`
- **B03 plan:** `docs/workstreams/timeline-temporal-operational-b03-execution-plan.md`
- **B03-A closure:** `docs/workstreams/timeline-temporal-operational-b03-a-closure-2026-09-16.md`
- **B03-B closure:** `docs/workstreams/timeline-temporal-operational-b03-b-closure-2026-09-17.md`
- **B03-C closure:** `docs/workstreams/timeline-temporal-operational-b03-c-closure-2026-09-17.md`
- **B03-D closure:** `docs/workstreams/timeline-temporal-operational-b03-d-closure-2026-09-17.md`
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
```

A block closes only after applicable semantic, persistence, backend, frontend, proof and documentation gates are reconciled.

---

# 1. Current ordered roadmap

```text
B00 Real Data Spine                              ✅ CLOSED / PROVEN
B01 Activity Core                                ✅ CLOSED / PROVEN
B02 Schedule Core                                ✅ CLOSED / PROVEN
B03 Event Core                                   🟨 B03-A/B/C/D CLOSED / B03-E NEXT
B04 Temporal Constraints + Movement Policy       ⬜
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

---

# 3. B03 — Event Core using shared Schedule 🟨

Objective:

```text
Activity ─┐
          ├→ one shared Schedule identity/current/history capability
Event ────┘
```

No `event_schedule` duplicate engine is authorized.

## B03-A — Event canonical core ✅ CLOSED / PROVEN

Established canonical Event identity/expectation/create/read/self-scope at `_27`.

## B03-B — Shared Schedule + Event Timeline ✅ CLOSED / PROVEN

Established `_28` typed Activity-or-Event Schedule authorization, atomic Event + initial Schedule, floating/named-zone/date-span/multi-day Event, Timeline union, strict transport/hydration and minimal truthful Event Create.

## B03-C — Event placement lifecycle ✅ CLOSED / PROVEN

Activated Event reschedule, postponed/TBD with no current placement, read after placement removal, stale-CAS protection and guarded Undo on the shared Schedule machinery. No new migration was needed.

Proof:

```text
PostgreSQL/backend targeted gate       9 PASS / 2 deselected
Event lifecycle web gate               5 files / 16 PASS
@dante/web typecheck                   PASS
```

## B03-D — Agenda/internal parts ✅ CLOSED / PROVEN

B03-D activates bounded ordered Event-internal Agenda values without identity inflation.

Persistence at `_29`:

```text
event_agenda_part
event_agenda_current
event_agenda_mutation_operation
create_self_event_with_agenda(...)
replace_self_event_agenda(...)
```

Accepted behavior:

```text
ordered bounded Agenda values
no NativeRef per Agenda part
aggregate revision/CAS
operation-id idempotent replay
create/add/edit/reorder/remove
reload authoritative backend truth
real Event-detail Agenda editor
stale conflict reloads current server truth
```

Proof summary:

```text
focused PostgreSQL/API Agenda              2 PASS
DB/Alembic/Dictionary gate                12 PASS
B03-D affected web gate                    6 files / 19 PASS
@dante/i18n typecheck                      PASS
@dante/web typecheck                       PASS
final B02+B03 backend regression           13 PASS / 2 deselected
final Activity/Schedule/Event web regression 5 files / 26 PASS
```

Closure authority: `docs/workstreams/timeline-temporal-operational-b03-d-closure-2026-09-17.md`.

## B03-E — Whole-B03 closure ⬜ NEXT

B03-E is a **proof/closure slice**, not an invitation to invent new Event semantics.

Required evidence:

```text
whole-B03 relevant PostgreSQL/API regressions
relevant backend/frontend broad regressions
real-stack Chromium Event create/reschedule/all-day/multi-day/reload
Firefox critical interaction proof where affected
manual Event userTest
Dictionary/SQLAlchemy/Alembic/live-catalog final reconciliation
map/roadmap/handoff/global-doc closure reconciliation
```

If a B03-E proof reveals a concrete defect, fix the defect in its owning B03 capability; otherwise do not reopen B03-A/B/C/D scope.

Deferred beyond B03 remain explicit:

```text
Event recurrence                   → B06
Temporal Constraints               → B04
Life Area / Calendar / Tags        → B05
Session/execution                  → B08
participants / invitations         → B09
Actual / Outcome / Confirmation    → B10
reminders / conditional policy     → B11
provider conferencing / sync       → B13
```

---

# 4. B04 — Temporal Constraints + Movement Policy ⬜

Introduce temporal constraints as truth distinct from Schedule placement and establish movement/replanning policy foundations.

# 5. B05 — Product Organization ⬜

Activate Calendar/Life Area, Tags and accepted grouping/context semantics without turning presentation organization into temporal truth.

# 6. B06 — Routine / Recurrence / Occurrence Baseline ⬜

Activate Routine as owner, Recurrence as policy and Occurrence as generated instance; Event recurrence is activated here, not in B03.

# 7. B07 — UI/UX Consolidation v1 ⬜

Dedicated product-quality planning checkpoint after B06.

# 8. B08 — Session Runtime ⬜

Real execution runtime; Session remains distinct from Schedule and Actual.

# 9. B09 — Responsibility / Participation ⬜

Actor relations, responsibility and participation/invitation boundaries.

# 10. B10 — Actual / Outcome / Confirmation / Resolution ⬜

Record what actually happened and the resulting authoritative resolution flow.

# 11. B11 — Advanced Recurrence / Conditional / Reminder ⬜

Advanced recurrence, bounded conditional effects and reminders.

# 12. B12 — Replanning / Conflict / Solver ⬜

Conflict detection, candidate generation and governed acceptance.

# 13. B13 — Provider / Offline / Multi-device ⬜

Provider mapping/sync/conferencing plus offline and multi-device reconciliation.

# 14. B14 — Analytics / Statistics / Signals ⬜

Derived analytics/signals over accepted canonical truth.

# 15. B15 — Whole Vertical Closure ⬜

Cross-block regression, recovery/anti-resurrection, operational hardening and final acceptance.

---

# 16. Current gate

```text
B03-A  ✅ CLOSED / PROVEN
B03-B  ✅ CLOSED / PROVEN
B03-C  ✅ CLOSED / PROVEN
B03-D  ✅ CLOSED / PROVEN
B03-E  ⬜ NEXT / requires explicit approval
```

CI remains separate and is not implicitly authorized.