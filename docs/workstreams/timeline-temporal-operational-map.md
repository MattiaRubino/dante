# Timeline / Temporal-Operational Vertical — Semantic Work Map / Live Ledger

- **Status:** CURRENT SEMANTIC MAP + LIVE IMPLEMENTATION LEDGER — reconciled 2026-09-17
- **Branch:** `feature/timeline-temporal-operational`
- **Roadmap:** `docs/workstreams/timeline-temporal-operational-roadmap.md`
- **B03 plan:** `docs/workstreams/timeline-temporal-operational-b03-execution-plan.md`
- **B03-A closure:** `docs/workstreams/timeline-temporal-operational-b03-a-closure-2026-09-16.md`
- **B03-B closure:** `docs/workstreams/timeline-temporal-operational-b03-b-closure-2026-09-17.md`
- **B03-C closure:** `docs/workstreams/timeline-temporal-operational-b03-c-closure-2026-09-17.md`
- **B03-D closure:** `docs/workstreams/timeline-temporal-operational-b03-d-closure-2026-09-17.md`
- **Detailed semantic freeze:** `docs/workstreams/archive/timeline-temporal-operational-map-ledger-snapshot-2026-09-15.md`

The archived semantic freeze remains the binding detailed inventory for the full vertical. This file is the current implementation/proof ledger; compacting it does not weaken the archived semantic contract.

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
```

These boundaries cannot be weakened by UI convenience, ORM convenience, provider shape or roadmap pressure.

---

# 2. Current roadmap position

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

# 4. B03 — Event Core 🟨

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
- ⬜ **[EVT-014]** Ordinary Event attendance `!= Session`.
- ⬜ **[EVT-015]** Event `!= Availability/Capacity Claim`.

Items 012–015 remain future-owner semantic obligations; they are not missing B03-D implementation.

## 4.2 Proof ledger

- ✅ **[B03-T01]** Event create/application PostgreSQL/API proof.
- ✅ **[B03-T02]** Timed/all-day/multi-day shared-Schedule proof.
- ✅ **[B03-T03]** Postponed/TBD history/query/CAS/guarded-Undo proof.
- ✅ **[B03-T04]** Event Agenda persistence/API/frontend/add-edit-reorder-remove/reload/CAS proof.
- ✅ **[B03-T05]** Shared Schedule Activity + Event regression remains green through `_29`.
- ⬜ **[B03-T06]** Real-stack Event create/reschedule/all-day/multi-day/reload acceptance. → B03-E
- ⬜ **[B03-T07]** Manual `userTest` Event acceptance. → B03-E

---

# 5. B03 slice closures

## B03-A — Event canonical core ✅ CLOSED / PROVEN

Closure: `timeline-temporal-operational-b03-a-closure-2026-09-16.md`.

Established Event identity/expectation/self-scope/create/read at `_27` without claiming Schedule or Agenda behavior.

## B03-B — Shared Schedule + Event Timeline ✅ CLOSED / PROVEN

Closure: `timeline-temporal-operational-b03-b-closure-2026-09-17.md`.

Established `_28` shared Activity/Event Schedule authorization, atomic Event + initial Schedule, floating/named-zone/date-span/multi-day Event, Timeline union and minimal truthful Event Create. No `event_schedule` was introduced.

## B03-C — Event placement lifecycle ✅ CLOSED / PROVEN

Closure: `timeline-temporal-operational-b03-c-closure-2026-09-17.md`.

Established reschedule, truthful postponed/TBD, read with no current placement, stale-CAS rejection and guarded Undo through new Schedule MaterialState, including immediate lifecycle after Event create.

Proof:

```text
PostgreSQL/backend targeted    9 PASS / 2 deselected
web lifecycle                  5 files / 16 PASS
@dante/web typecheck           PASS
```

## B03-D — Agenda/internal parts ✅ CLOSED / PROVEN

Closure: `timeline-temporal-operational-b03-d-closure-2026-09-17.md`.

`_29` adds narrow Event-owned Agenda persistence:

```text
event_agenda_part
event_agenda_current
event_agenda_mutation_operation
create_self_event_with_agenda(...)
replace_self_event_agenda(...)
```

Accepted semantics:

```text
ordered bounded Agenda values
no NativeRef per Agenda part
aggregate revision/CAS
operation-id idempotent replay
atomic whole-list add/edit/reorder/remove
real backend read/reload
real Event-detail Agenda editor
stale CAS → reload authoritative truth
```

Executed closure evidence:

```text
focused PostgreSQL/API Agenda              2 PASS
DB/Alembic/Dictionary gate                12 PASS
B03-D affected web gate                    6 files / 19 PASS
@dante/i18n typecheck                      PASS
@dante/web typecheck                       PASS
final B02+B03 backend regression           13 PASS / 2 deselected
final Activity/Schedule/Event web regression 5 files / 26 PASS
```

No recurrence, constraints, participants, Session, Actual, Outcome, reminders or provider sync were activated.

---

# 6. Remaining B03 slice

```text
B03-E  whole-B03 closure
       relevant full regressions
       real-stack Chromium Event acceptance
       Firefox critical interaction proof where affected
       manual Event userTest
       final Dictionary/live-catalog/docs reconciliation
```

B03-E is a closure/proof slice. It must not invent new Event semantics merely to enlarge scope.

---

# 7. B04–B15 ownership register

The detailed functionality lists remain binding in the archived semantic freeze.

```text
B04  Temporal Constraints + movement policy
B05  Calendar / Life Area / Tags / product organization
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

Transfers remain explicit:

```text
Event recurrence                → B06
Temporal Constraints            → B04
Life Area / Calendar / Tags     → B05
Session/execution               → B08
participants/invites            → B09
Actual/Outcome/Confirmation     → B10
reminders/conditional policy    → B11
provider/conference/sync        → B13
```

---

# 8. Current gate

```text
B03-A  ✅ CLOSED / PROVEN
B03-B  ✅ CLOSED / PROVEN
B03-C  ✅ CLOSED / PROVEN
B03-D  ✅ CLOSED / PROVEN
B03-E  ⬜ NEXT / NOT YET AUTHORIZED
```

The next implementation action is B03-E closure proof. CI remains separately authorized.