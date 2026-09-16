# Timeline / Temporal-Operational Vertical — Semantic Work Map / Live Ledger

- **Status:** CURRENT SEMANTIC MAP + LIVE IMPLEMENTATION LEDGER — reconciled 2026-09-16
- **Branch:** `feature/timeline-temporal-operational`
- **Roadmap:** `docs/workstreams/timeline-temporal-operational-roadmap.md`
- **B02 closure:** `docs/workstreams/timeline-temporal-operational-b02-closure-2026-09-16.md`
- **B03 plan:** `docs/workstreams/timeline-temporal-operational-b03-execution-plan.md`
- **B03-A closure:** `docs/workstreams/timeline-temporal-operational-b03-a-closure-2026-09-16.md`
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
B03 Event Core                                   🟨 B03-A CLOSED / B03-B NEXT
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

The exact item-level evidence remains in `timeline-temporal-operational-b02-closure-2026-09-16.md` and the archived detailed ledger.

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
- ✅ **[EVT-002]** Resolve minimum meaningful Event descriptive persistence. — `event_expectation` is now canonical and self-Person scoped.
- ✅ **[EVT-003]** Implement idempotent `CreateEvent`. — `event_create_operation` + `create_self_event(...)` + backend/API are proven.
- ⬜ **[EVT-004]** Activate Event macro-class in `+` Create only when initial Schedule commit is truthful.
- ⬜ **[EVT-005]** Implement timed Event using shared B02 Schedule.
- ⬜ **[EVT-006]** Implement all-day/date-span Event in real all-day lane.
- ⬜ **[EVT-007]** Implement multi-day Event semantics/query/rendering.
- ⬜ **[EVT-008]** Implement postponed/TBD Event with identity/history and no fake placeholder Schedule.
- ⬜ **[EVT-009]** Preserve original expectation/current Schedule/Actual separation through Event lifecycle.
- ⬜ **[EVT-010]** Implement Event Agenda/internal parts at accepted product level.
- ⬜ **[EVT-011]** Preserve Agenda part `!= Activity/Event/Occurrence/Session/Actual` by default.
- ⬜ **[EVT-012]** Implement preparation/follow-up Activity relation only when exact relation semantics are activated.
- ⬜ **[EVT-013]** Implement Place/conference intent only through justified relation/profile semantics.
- ⬜ **[EVT-014]** Preserve ordinary Event attendance `!= Session`.
- ⬜ **[EVT-015]** Preserve Event `!= Availability/Capacity Claim`.

## 6.3 B03 proof ledger

- ✅ **[B03-T01]** Event create/application tests. — real PostgreSQL/API `2 passed`; self-scope, CSRF, replay and changed-intent conflict proven.
- ⬜ **[B03-T02]** Timed/all-day/multi-day PostgreSQL/API tests.
- ⬜ **[B03-T03]** Postponed/TBD history/query tests.
- ⬜ **[B03-T04]** Event Agenda semantic/frontend tests.
- ⬜ **[B03-T05]** Shared Schedule regression suite rerun for Activity + Event.
- ⬜ **[B03-T06]** E2E Event create/reschedule/all-day/reload test.
- ⬜ **[B03-T07]** Manual `userTest` Event acceptance.

## 6.4 B03-A — Event canonical core ✅ CLOSED / PROVEN

Closure authority:

```text
docs/workstreams/timeline-temporal-operational-b03-a-closure-2026-09-16.md
```

Current B03-A persistence:

```text
Alembic head     20260916_27
Topology         98|5|29|78|195|115|288|0|0|0

new tables       event_expectation
                 event_create_operation
new routine      create_self_event(uuid,text,text,uuid,text)
```

Executed proof:

```text
Event core/API PostgreSQL                         2 PASS
catalog/Dictionary/migration targeted gate       10 PASS
initial harness-only privilege defect             1 FAIL
corrected harness rerun                           1 PASS
```

The initial failure was not a product/migration defect; it was the new migration test reading `dante.alembic_version` without the accepted migrator/owner role discipline. Commit `8dc423adc8f2cf5cf115061192c603d806e923b3` fixed the harness and the exact failed proof passed.

B03-A does not claim Event Schedule/Timeline/UI/Agenda behavior.

## 6.5 B03-B — Shared Schedule + Event Timeline ⬜ NEXT

Exact scope:

```text
1. generalize B02 self-subject authorization from Activity-only to typed Activity OR Event
2. preserve one shared Schedule owner/current/history model
3. atomic Event + initial Schedule application operation
4. timed floating-local Event
5. timed named-zone Event
6. all-day/date-span Event
7. multi-day Event
8. backend Timeline Activity/Event discriminated union
9. API + TypeScript strict union
10. activate only the minimal truthful Event Create surface
11. rerun Activity Schedule regressions to prove no B02 regression
```

No recurrence, constraints, participants, Session, Actual, Outcome, reminder, provider sync or Agenda persistence is smuggled into B03-B.

## 6.6 Remaining B03 slices

```text
B03-C  Event placement lifecycle
       reschedule + postponed/TBD + detail/read + guarded Undo

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
B03-B  ⬜ NOT AUTHORIZED YET
```

The next implementation action is explicit approval of B03-B. CI remains a separate authorization.