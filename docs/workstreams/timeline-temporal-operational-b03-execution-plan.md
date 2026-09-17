# Timeline / Temporal-Operational — B03 Event Core Execution Plan

- **Status:** B03-A ✅ CLOSED / PROVEN — B03-B ✅ CLOSED / PROVEN — B03-C NEXT
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
- **Next implementation gate:** `APPROVE B03-C`
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

## 3.5 Frontend activation

The minimal truthful Event Create path is active for canonically supported B03-B placement intent. Unsupported rich Event prototype intent remains fail-closed.

Event Timeline projections are visible but **read-only for lifecycle mutation** in B03-B. Event reschedule/unschedule/Undo belongs to B03-C.

## 3.6 Executed proof

```text
PostgreSQL/API targeted selection      18 PASS / 4 FAIL first run
single _28 PL/pgSQL regression         fixed by af16b700
exact failed selection rerun           4 PASS
Event transport/Timeline web           10 PASS
B03 Create-runtime web                  2 PASS
@dante/web typecheck                    PASS
```

The initial four failures exposed one real migration regression: `_28` had redefined `unschedule_self_schedule(...)` without preserving B02 strict PL/pgSQL disambiguation. `af16b700` restored `#variable_conflict error` and qualified the history update, after which the exact four failed proofs passed.

The final frontend gate also verified that the Activity|Event projection union does not accidentally grant Activity-only lifecycle actions to Event before B03-C.

Closure authority: `docs/workstreams/timeline-temporal-operational-b03-b-closure-2026-09-17.md`.

---

# 4. Current B03 gaps after B03-B

```text
GAP-B03-C01  Event reschedule product lifecycle not active
GAP-B03-C02  postponed/TBD Event lifecycle not active
GAP-B03-C03  Event read/detail after current Schedule absence not active
GAP-B03-C04  Event guarded Undo product path not active
GAP-B03-D01  Agenda/internal-part canonical persistence absent
```

B03-B gaps are closed. These remaining gaps belong to later slices and must not be solved by widening B03-B semantics retroactively.

---

# 5. B03-C — Event placement lifecycle ⬜ NEXT

## 5.1 Goal

Complete Event placement lifecycle without collapsing Event into Activity semantics.

Required invariant:

```text
same Event identity
+ historical/original expectation retained
+ current Schedule may change or be absent
+ Schedule history remains monotonic
```

## 5.2 Reschedule

Event reschedule must use the existing shared Schedule revision capability. No Event-specific revision engine is allowed.

Expected-current-state/CAS, idempotency and current/history rules remain identical to the shared Schedule semantics already proven for Activity.

## 5.3 Postponed / TBD

```text
Event identity retained
Schedule/history retained
no current accepted Schedule
no fabricated placeholder date/time
```

And:

```text
postponed/TBD Event != Planning Tray Activity
```

A postponed/TBD Event remains an Event whose current accepted Schedule is absent; it is not converted to an Activity and is not deleted.

## 5.4 Detail/read

Event detail/read must remain truthful when:

- a current Schedule exists;
- Schedule placement has been revised;
- no current Schedule exists after postponement/TBD;
- historical Schedule episodes exist.

Original Event expectation, current Schedule and future Actual truth must remain distinguishable.

## 5.5 Guarded Undo

Undo must create a new accepted Schedule placement MaterialState when the accepted basis is still valid. It must never reopen or rewrite old current-history episodes.

## 5.6 Frontend activation

Only after backend/API lifecycle capabilities are proven may Event Timeline/detail surfaces expose:

```text
reschedule
unschedule/postpone/TBD
Undo where the exact accepted basis allows it
```

Activity lifecycle behavior must remain unchanged.

## 5.7 B03-C proof obligations

Required targeted evidence before B03-C closure:

- Event reschedule with stable EventRef and ScheduleRef;
- current placement MaterialState advances monotonically;
- stale expected-state conflict;
- idempotent replay / changed-intent conflict;
- postpone/TBD removes current accepted placement without deleting Event/history;
- Event remains readable/detail-visible while current Schedule is absent;
- guarded Undo restores by a new MaterialState, never history rewind;
- Activity Schedule lifecycle regressions remain green;
- frontend Event lifecycle controls remain typed and truthful.

---

# 6. B03-D — Agenda/internal parts ⬜

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

Candidate persistence remains narrow unless implementation re-read proves a need for a stronger scoped identity.

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
R9  Event lifecycle UI preceding backend truth              FORBIDDEN
```

---

# 10. Current gate

```text
B03-A  ✅ CLOSED / PROVEN
B03-B  ✅ CLOSED / PROVEN
B03-C  ⬜ NEXT / NOT YET AUTHORIZED
B03-D  ⬜
B03-E  ⬜
```

Next action requires explicit:

```text
APPROVE B03-C
```