# Timeline / Temporal-Operational Vertical — Semantic Work Map / Live Ledger

- **Status:** CURRENT SEMANTIC MAP + LIVE IMPLEMENTATION LEDGER — reconciled 2026-09-17
- **Branch:** `feature/timeline-temporal-operational`
- **Roadmap:** `docs/workstreams/timeline-temporal-operational-roadmap.md`
- **B02 closure:** `docs/workstreams/timeline-temporal-operational-b02-closure-2026-09-16.md`
- **B03 plan:** `docs/workstreams/timeline-temporal-operational-b03-execution-plan.md`
- **B03-A closure:** `docs/workstreams/timeline-temporal-operational-b03-a-closure-2026-09-16.md`
- **B03-B closure:** `docs/workstreams/timeline-temporal-operational-b03-b-closure-2026-09-17.md`
- **B03-C closure:** `docs/workstreams/timeline-temporal-operational-b03-c-closure-2026-09-17.md`
- **Detailed semantic freeze:** `docs/workstreams/archive/timeline-temporal-operational-map-ledger-snapshot-2026-09-15.md`
- **Historical roadmap freeze:** `docs/workstreams/archive/timeline-temporal-operational-roadmap-freeze-2026-09-07.md`

The archived semantic freeze remains the binding detailed inventory for the full vertical: functionality, semantic disambiguations, non-collapse rules, ownership, lifecycle, projection, provider/offline, policy, analytics and future-block checklists. This file is the **current live progress authority**. Compacting live status never deletes or weakens the archived semantic contract.

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
Agenda part != Activity/Event/Occurrence/Session/Actual by default
Event != Availability / Capacity Claim
```

These boundaries cannot be weakened by UI convenience, ORM convenience, provider shape or roadmap pressure.

---

# 2. High-level semantic tree

```text
TIMELINE / TEMPORAL-OPERATIONAL
│
├── ORIGINATING
│   ├── Activity
│   ├── Event
│   ├── Routine
│   └── Session recording
│
├── TEMPORAL EXPECTATION
│   ├── Schedule
│   ├── Temporal Constraint
│   ├── Movement / replanning policy
│   ├── Recurrence
│   └── Occurrence
│
├── EXECUTION / REALITY
│   ├── Session
│   ├── Actual
│   └── Outcome
│
├── RESOLUTION / COMMON GROUND
│   ├── Confirmation
│   ├── Acknowledgement
│   └── Resolution Queue / review
│
├── PRODUCT ORGANIZATION
│   ├── Calendar / Life Area
│   ├── Tags
│   ├── Context / grouping
│   └── Appearance
│
├── CONDITIONAL / AUTOMATION
│   ├── Conditional Policy
│   ├── Reminder intent
│   └── bounded automatic effects
│
└── DERIVED SURFACES
    ├── Timeline
    ├── Planning Tray
    ├── Detail / History
    ├── Resolution Queue
    ├── conflict / replanning explanation
    └── Analytics / Signals
```

This is a work map, not an inheritance hierarchy and not authorization for a generic temporal mega-entity.

---

# 3. Status semantics

```text
⬜ NOT STARTED
🟨 IN PROGRESS
✅ DONE / CLOSED for exact scope
⛔ BLOCKED
```

A green item means its applicable semantic, persistence/application and proof obligations for that exact scope are satisfied. Future semantic concepts are never marked green merely because their names exist in Domain/Physical authority.

---

# 4. Current roadmap position

```text
B00 Real Data Spine                              ✅ CLOSED / PROVEN
B01 Activity Core                                ✅ CLOSED / PROVEN
B02 Schedule Core                                ✅ CLOSED / PROVEN
B03 Event Core                                   🟨 B03-A + B03-B + B03-C CLOSED / B03-D NEXT
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

---

# 5. Completed foundation

## B00 — Real Data Spine ✅

```text
SPINE-001 … SPINE-012   ✅
B00-T01 … B00-T05      ✅
```

Real authenticated backend/PostgreSQL path, truthful empty/error states, isolated test fixtures, context/timezone handling and real-stack E2E are established.

## B01 — Activity Core ✅

```text
ACT-001 … ACT-017      ✅
B01-T01 … B01-T08      ✅
```

Canonical Activity identity, self-owned actionable-intention descriptor, idempotent create, Planning Tray/read path and reload identity are established. No fake completion/Session/Actual semantics were introduced.

## B02 — Schedule Core ✅

```text
SCH-001 … SCH-024      ✅
B02-T01 … B02-T09      ✅
```

All accepted Schedule forms and lifecycle behavior are proven at B02 scope: date-span, floating-local, named-zone-local, absolute, coarse-local-period, establish, revision, current/history, CAS, idempotency, Planning Tray placement, drag/time editor, unschedule, guarded Undo, range/local-day query, DST behavior and Chromium/Firefox real-stack proof.

---

# 6. B03 — Event Core 🟨

## 6.1 Semantic target

B03 activates Event as a distinct originating owner while proving that Schedule remains shared:

```text
Activity ─┐
          ├── one Schedule owner/current/history capability
Event ────┘
```

Forbidden:

```text
event_schedule
Event-specific temporal engine
Event-specific current/history model
Event-as-Activity shortcut
Event-as-busy/capacity shortcut
```

## 6.2 Capability ledger

- ✅ **[EVT-001]** Re-open Event Domain/Logical/Physical authority before implementation.
- ✅ **[EVT-002]** Minimum meaningful Event descriptive persistence: `event_expectation` self-Person scoped.
- ✅ **[EVT-003]** Idempotent `CreateEvent`: `event_create_operation` + `create_self_event(...)` + backend/API.
- ✅ **[EVT-004]** Event macro-class activated in `+` Create only for the minimal truthful scheduled-Event contract.
- ✅ **[EVT-005]** Timed Event uses the shared B02 Schedule capability.
- ✅ **[EVT-006]** All-day/date-span Event projects into the real all-day lane without fabricated clock time.
- ✅ **[EVT-007]** Multi-day Event semantics/query/rendering preserve date-span truth.
- ✅ **[EVT-008]** Postponed/TBD Event retains Event identity and Schedule history with no current placement and no fabricated placeholder date/time.
- 🟨 **[EVT-009]** Event expectation/current Schedule separation is proven through B03-C; future Actual truth remains B10-owned.
- ⬜ **[EVT-010]** Event Agenda/internal parts at accepted product level. → B03-D
- ⬜ **[EVT-011]** Agenda part `!= Activity/Event/Occurrence/Session/Actual` by default. → B03-D proof
- ⬜ **[EVT-012]** Preparation/follow-up Activity relation only when exact relation semantics are activated.
- ⬜ **[EVT-013]** Place/conference intent only through justified relation/profile semantics.
- ⬜ **[EVT-014]** Ordinary Event attendance `!= Session`.
- ⬜ **[EVT-015]** Event `!= Availability/Capacity Claim`.

## 6.3 B03 proof ledger

- ✅ **[B03-T01]** Event create/application tests — real PostgreSQL/API self-scope, CSRF, replay and changed-intent conflict.
- ✅ **[B03-T02]** Timed/all-day/multi-day PostgreSQL/API tests — floating, named-zone/DST, date-span, multi-day, mixed Timeline and idempotency proven.
- ✅ **[B03-T03]** Postponed/TBD history/query tests — stable Event/Schedule identity, no current placement, preserved monotonic history, stale CAS rejection and guarded Undo proven.
- ⬜ **[B03-T04]** Event Agenda semantic/frontend tests. → B03-D
- ✅ **[B03-T05]** Shared Schedule regression suite for Activity + Event — B02 PL/pgSQL hardening preserved through `_28`; B03-C regression selection remains green.
- ⬜ **[B03-T06]** E2E Event create/reschedule/all-day/reload test. → B03-E after lifecycle and Agenda are complete
- ⬜ **[B03-T07]** Manual `userTest` Event acceptance. → B03-E

## 6.4 B03-A — Event canonical core ✅ CLOSED / PROVEN

Closure authority:

`docs/workstreams/timeline-temporal-operational-b03-a-closure-2026-09-16.md`

B03-A established canonical Event expectation/create identity and self-scope at Alembic `_27`. It did not claim Event Schedule/Timeline/UI/Agenda behavior.

## 6.5 B03-B — Shared Schedule + Event Timeline ✅ CLOSED / PROVEN

Closure authority:

`docs/workstreams/timeline-temporal-operational-b03-b-closure-2026-09-17.md`

Current candidate persistence authority:

```text
Alembic head     20260917_28
Topology         98|5|29|78|195|115|288|0|0|0
```

Accepted result:

```text
1. B02 self-subject authorization generalized to typed Activity OR Event
2. one shared Schedule identity/current/history model retained
3. Event + initial Schedule commit atomically
4. floating-local Event
5. named-zone Event with source wall-clock + resolved-instant semantics
6. all-day/date-span Event
7. multi-day Event
8. backend Timeline Activity/Event discriminated union
9. strict API + TypeScript union/parser/hydration
10. minimal truthful Event Create runtime
11. Activity Schedule regressions preserved
12. Event lifecycle mutations remain read-only until B03-C
```

Executed closure evidence:

```text
PostgreSQL/API targeted gate        18 PASS / 4 FAIL on first run
single _28 PL/pgSQL regression      fixed by af16b700
exact failed set rerun              4 PASS
Event transport/Timeline web        10 PASS
B03 Create-runtime web               2 PASS
@dante/web typecheck                 PASS
```

The first-run failures were not accepted as closure evidence; B03-B closed only after the exact failures were fixed and rerun green.

No recurrence, constraints, participants, Session, Actual, Outcome, reminder, provider sync or Agenda persistence was smuggled into B03-B.

## 6.6 B03-C — Event placement lifecycle ✅ CLOSED / PROVEN

Closure authority:

`docs/workstreams/timeline-temporal-operational-b03-c-closure-2026-09-17.md`

Accepted result:

```text
1. Event reschedule uses the shared Schedule revision capability
2. stable EventRef and ScheduleRef across placement revisions
3. placement MaterialState advances monotonically
4. postponed/TBD retains Event + Schedule/history but has no current placement
5. no placeholder date/time and no Event→Activity conversion
6. Event remains readable while current placement is absent
7. stale expected-state mutations fail closed
8. guarded Undo restores through a new MaterialState, never history rewind
9. Undo replay remains idempotent
10. Timeline Event lifecycle uses the same canonical Schedule mutation boundary
11. newly-created Event can revise/postpone/undo without reload
12. Activity lifecycle regression path remains preserved
```

Executed closure evidence:

```text
PostgreSQL/backend targeted gate    9 PASS / 2 deselected
Event lifecycle web gate            5 files / 16 PASS
@dante/web typecheck                PASS
```

B03-C required no new Alembic revision because `_28` already contained the correct shared Schedule lifecycle capability for Event. No duplicate persistence was introduced.

## 6.7 Remaining B03 slices

```text
B03-D  Agenda/internal parts
       bounded ordered Event-internal persistence + real frontend integration

B03-E  closure
       PG/API/frontend/full-stack/manual + DB/Dictionary/docs reconciliation
```

---

# 7. B04–B15 ownership register

The **full detailed functionality lists remain binding in the archived semantic freeze**. Current block ownership is:

```text
B04  Temporal Constraints + movement policy
B05  Calendar / Life Area / Tags / product organization
B06  Routine + Recurrence + Occurrence baseline
B07  UI/UX Consolidation v1 — target ~60–70% product-quality planning UI
B08  Session Runtime
B09  Responsibility / Participation / actor relations
B10  Actual + Outcome + Confirmation + Resolution Queue
B11  advanced recurrence + conditional policy + reminders
B12  replanning/conflict/solver
B13  provider integration + offline/multi-device reconciliation
B14  analytics/statistics/Signals
B15  whole-vertical closure/recovery/cross-cutting proof
```

Important transfers remain explicit:

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
B03-D  ⬜ NEXT / NOT YET AUTHORIZED
B03-E  ⬜
```

The next implementation action requires explicit approval of B03-D. CI remains a separate authorization.