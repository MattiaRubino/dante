# Timeline / Temporal-Operational — B03 Event Core Execution Plan

- **Status:** B03-A ✅ CLOSED / PROVEN — B03-B ✅ CLOSED / PROVEN — B03-C ✅ CLOSED / PROVEN — B03-D NEXT
- **Date:** 2026-09-17
- **Branch:** `feature/timeline-temporal-operational`
- **Current DB authority:** PostgreSQL 18.6 / Alembic `20260917_28`
- **Current topology:** `98|5|29|78|195|115|288|0|0|0`
- **Primary semantic authority:** `docs/domain/concepts/event.md`
- **Detailed semantic freeze:** `docs/workstreams/archive/timeline-temporal-operational-map-ledger-snapshot-2026-09-15.md`
- **Live work map:** `docs/workstreams/timeline-temporal-operational-map.md`
- **Roadmap:** `docs/workstreams/timeline-temporal-operational-roadmap.md`
- **B03-A closure:** `docs/workstreams/timeline-temporal-operational-b03-a-closure-2026-09-16.md`
- **B03-B closure:** `docs/workstreams/timeline-temporal-operational-b03-b-closure-2026-09-17.md`
- **B03-C closure:** `docs/workstreams/timeline-temporal-operational-b03-c-closure-2026-09-17.md`
- **Next implementation gate:** `APPROVE B03-D`
- **CI:** separate authorization required

The detailed archived semantic map remains binding for the complete functionality/logics inventory and all semantic `!=` boundaries. This file is the current B03 execution authority.

---

# 0. Binding objective

B03 activates **Event as a distinct originating owner** and proves that the B02 Schedule engine is genuinely shared.

```text
Activity ─┐
          ├── shared Schedule identity/current/history capability
Event ────┘
```

Forbidden:

```text
activity_schedule + event_schedule split
Event-specific current/history model
Event-as-Activity shortcut
generic temporal mega-entity
```

Permanent boundaries:

```text
Activity != Event
Event != Schedule
Event != Recurrence
Event != Occurrence
Event != Session
Event != Actual
Event != Outcome
Event != Participation
Event != Availability / Capacity Claim
Event identity != provider identity
Agenda part != Activity/Event/Occurrence/Session/Actual by default
original expectation != current Schedule != Actual occurrence
```

---

# 1. Authority result

Domain/Logical/Physical re-open proved:

```text
Event                      LR-01 native identity owner
Schedule                   LR-02 dependent scoped record
dante.event                canonical Event NativeRef shell
native_address             supports owner_family='event'
dante.schedule             shared Schedule owner
Schedule subject family    activity | event | occurrence
Event recurrence shell     exists but remains B06-owned
```

No Event-specific Schedule persistence is justified.

---

# 2. B03-A — Event canonical core ✅ CLOSED / PROVEN

B03-A filled only the Event-owned descriptive/create gap:

```text
event_expectation
event_create_operation
create_self_event(uuid,text,text,uuid,text)
TemporalEventApplication
POST /api/v1/temporal/events
GET  /api/v1/temporal/events/{event_ref}
```

Accepted behavior includes UUIDv7 Event identity, explicit self-Person scope, bounded canonical title data, idempotent same-intent replay, changed-intent conflict and guarded downgrade.

Closure authority: `docs/workstreams/timeline-temporal-operational-b03-a-closure-2026-09-16.md`.

---

# 3. B03-B — Shared Schedule + Event Timeline ✅ CLOSED / PROVEN

## 3.1 Accepted invariant

```text
Activity and Event both use the same ScheduleRef,
placement MaterialState, current binding and history machinery.
```

## 3.2 Implemented persistence/runtime behavior

`_28` generalized Schedule self-scope from Activity-only to an explicit typed union:

```text
Activity → activity_intention.self_person_ref
Event    → event_expectation.self_person_ref
```

No generic EAV owner shortcut and no `event_schedule` structure were introduced.

The governed shared Schedule capability family remains:

```text
establish_self_schedule_placement(...)
revise_self_schedule_placement(...)
unschedule_self_schedule(...)
undo_self_schedule_unschedule_any(...)
```

Scheduled Event creation commits Event identity/expectation and initial Schedule truth atomically.

## 3.3 Event placement forms activated

```text
timed floating-local
timed named-zone-local
all-day single-day via date_span
multi-day all-day/date_span
```

Named-zone source wall-clock fields remain distinct from resolved instants. All-day Event does not fabricate a `00:00 → 24:00` timed block. Coarse Event authoring remains outside the minimal B03-B create contract.

## 3.4 Timeline/read-model union

```text
TimelineItem
├── scheduled_activity
└── scheduled_event
```

Activity/Event identity remains explicit in backend DTOs and TypeScript discriminated unions. Timeline is a projection, never canonical owner truth.

## 3.5 Executed proof

```text
PostgreSQL/API targeted selection      18 PASS / 4 FAIL first run
single _28 PL/pgSQL regression         fixed by af16b700
exact failed selection rerun           4 PASS
Event transport/Timeline web           10 PASS
B03 Create-runtime web                  2 PASS
@dante/web typecheck                    PASS
```

Closure authority: `docs/workstreams/timeline-temporal-operational-b03-b-closure-2026-09-17.md`.

---

# 4. B03-C — Event placement lifecycle ✅ CLOSED / PROVEN

## 4.1 Accepted invariant

```text
same Event identity
+ same Schedule identity
+ current placement may revise or become absent
+ Schedule history remains monotonic
```

B03-C uses the same canonical Schedule mutation family already established by B02/B03-B. No `_29` was required because there was no persistence gap.

## 4.2 Reschedule

Event reschedule uses `revise_self_schedule_placement(...)` through the existing backend/API Schedule boundary. `EventRef` and `ScheduleRef` remain stable while placement MaterialState advances.

Timeline rereads authoritative current truth after mutation; no local optimistic Event-specific state becomes canonical.

## 4.3 Postponed / TBD

Accepted semantics:

```text
Event identity retained
Schedule identity/history retained
no current accepted placement
no fabricated placeholder date/time
postponed/TBD Event != Planning Tray Activity
```

The Event remains readable through its Event owner read path while the Timeline correctly omits it because there is no current placement.

## 4.4 Guarded Undo

Undo of postponement uses the canonical Schedule unschedule token/operation boundary and writes a **new** accepted placement MaterialState.

```text
old historical MaterialState remains historical
restored placement gets a fresh MaterialState
current/history chronology remains monotonic
```

Undo replay is idempotent. Stale revision/unschedule attempts fail closed with conflict.

## 4.5 Create runtime + Timeline

An Event immediately after Create can revise, postpone and guarded-undo through `TemporalScheduleDataSource` without requiring a reload and without a local fake Event lifecycle.

Timeline controls retain `scheduled-event` identity while routing Schedule mutations through the same canonical boundary used by Activity.

Owner-aware copy remains distinct: postponed Event is not described as returning to Planning Tray.

## 4.6 Executed proof

```text
PostgreSQL/backend targeted gate       9 PASS / 2 deselected
Event lifecycle web gate               5 files / 16 PASS
@dante/web typecheck                   PASS
```

The backend proof covers stable identity, MaterialState advance, Timeline relocation, Event read after postponement, no current placement, preserved history, stale CAS conflicts, guarded Undo, monotonic restored history and idempotent Undo replay.

The web proof covers Event Timeline reschedule, Event postpone/Undo, authoritative reload behavior, Create-runtime lifecycle, canonical revision behavior, Event hydration and remote Timeline parsing.

Closure authority: `docs/workstreams/timeline-temporal-operational-b03-c-closure-2026-09-17.md`.

---

# 5. Current B03 gaps after B03-C

```text
GAP-B03-D01  Agenda/internal-part canonical persistence absent
GAP-B03-D02  durable Agenda ordering/edit/reload semantics not activated
GAP-B03-D03  real Event Agenda frontend integration not activated
GAP-B03-E01  whole-B03 real-stack/manual/final reconciliation remains
```

B03-A/B/C gaps are closed. These remaining gaps belong to B03-D/E and must not be solved by widening already-closed slices retroactively.

---

# 6. B03-D — Agenda/internal parts ⬜ NEXT

## 6.1 Goal

Activate a bounded ordered Event Agenda model while preserving Agenda parts as Event-internal structure by default.

Accepted hierarchy:

```text
Event
└── ordered Agenda/internal parts
```

Default non-collapse:

```text
Agenda part != Activity
Agenda part != Event
Agenda part != Occurrence
Agenda part != Session
Agenda part != Actual
```

## 6.2 Required authority re-open

Before implementation:

1. re-read Event Domain authority and the archived semantic freeze;
2. inspect Logical/Physical definitions touching Event internal parts;
3. inspect existing Event prototype fields and frontend interaction semantics;
4. inspect current persistence to avoid duplicate owner/version/order machinery;
5. introduce DDL only if a real canonical gap exists.

## 6.3 Persistence/application constraints

The Agenda model must be narrow and explicit:

```text
Event-owned
ordered
durable
bounded content
stable identity only if edit/reorder semantics require it
explicit mutation/idempotency/concurrency semantics where applicable
no generic JSON blob as canonical substitute
no generic temporal child mega-entity
```

Agenda items do not receive Schedule, Recurrence, Session or Actual identity merely because they appear inside a temporal owner.

## 6.4 Product behavior target

B03-D should support the accepted Agenda behavior already represented in the product prototype:

```text
read ordered Agenda
add item
edit item
move up/down / reorder
remove item
reload without order or identity drift
```

The real frontend must use backend truth; unsupported rich Event metadata remains fail-closed/deferred.

## 6.5 Proof obligations

Before B03-D closure prove at minimum:

- Event self-scope/authorization for Agenda mutation/read;
- deterministic durable ordering;
- create/add/edit/reorder/remove behavior;
- idempotency/concurrency safety appropriate to the chosen mutation contract;
- Event reload preserves Agenda truth;
- no Agenda item becomes Activity/Event/Occurrence/Session/Actual;
- frontend uses real backend data rather than prototype-only local state;
- Event Schedule lifecycle from B03-C remains green;
- Activity/Schedule regressions remain green.

---

# 7. B03-E — Closure ⬜

Required whole-block closure evidence:

- Event create/application proof;
- timed/all-day/multi-day PostgreSQL/API proof;
- postponed/TBD history/query proof;
- Agenda semantic/frontend proof;
- shared Schedule Activity+Event regression;
- relevant backend/frontend full regressions;
- real-stack Chromium Event create/reschedule/all-day/multi-day/reload;
- Firefox critical interaction proof where affected;
- manual Event userTest;
- Dictionary/SQLAlchemy/Alembic/live-catalog reconciliation;
- map/roadmap/handoff reconciliation.

CI remains separate and requires explicit authorization.

---

# 8. Rich Event prototype stop line

Remain deferred/fail-closed:

| Intent | Owner/gate |
| --- | --- |
| Event recurrence | B06 |
| Temporal Constraints / movement policy | B04 |
| Life Area / Calendar / Tags | B05 |
| participant/invite semantics | B09 |
| Session/execution | B08 |
| Actual / Outcome / Confirmation | B10 |
| reminder / conditional policy | B11 |
| provider conference / sync | B13 |
| availability/busy capacity semantics | separate accepted capacity/provider authority |
| visibility/sharing policy | actor/security/visibility authority |
| preparation/recovery scheduling rules | B04 / linked Activity relation semantics |
| rich resources/pre-read metadata | later explicit canonical owner decision |

Purpose, expected outcome, notes and similar rich meeting metadata are not forced into speculative generic Event JSON merely because the prototype has controls for them.

---

# 9. Risk register

```text
R1  silently accepting unsupported Event form fields        FORBIDDEN
R2  cloning Activity Schedule logic into Event              FORBIDDEN
R3  generic owner/EAV shortcut erasing owner meaning        FORBIDDEN
R4  treating postponed Event as unplaced Activity           FORBIDDEN
R5  Event implies availability/busy capacity                FORBIDDEN
R6  activating recurrence before B06                        FORBIDDEN
R7  Agenda identity inflation                               FORBIDDEN
R8  projection union becoming canonical ontology            FORBIDDEN
R9  frontend behavior preceding backend truth               FORBIDDEN
R10 Agenda part acquiring Schedule/Session/Actual by default FORBIDDEN
```

---

# 10. Current gate

```text
B03-A  ✅ CLOSED / PROVEN
B03-B  ✅ CLOSED / PROVEN
B03-C  ✅ CLOSED / PROVEN
B03-D  ⬜ NEXT / NOT YET AUTHORIZED
B03-E  ⬜
```

Next action requires explicit:

```text
APPROVE B03-D
```