# Timeline / Temporal-Operational — B03 Event Core Execution Plan

- **Status:** B03-A ✅ CLOSED / PROVEN — B03-B NEXT
- **Date:** 2026-09-16
- **Branch:** `feature/timeline-temporal-operational`
- **Current DB authority:** PostgreSQL 18.6 / Alembic `20260916_27`
- **Current topology:** `98|5|29|78|195|115|288|0|0|0`
- **Primary semantic authority:** `docs/domain/concepts/event.md`
- **Detailed semantic freeze:** `docs/workstreams/archive/timeline-temporal-operational-map-ledger-snapshot-2026-09-15.md`
- **Live work map:** `docs/workstreams/timeline-temporal-operational-map.md`
- **Roadmap:** `docs/workstreams/timeline-temporal-operational-roadmap.md`
- **B03-A closure:** `docs/workstreams/timeline-temporal-operational-b03-a-closure-2026-09-16.md`
- **Next implementation gate:** `APPROVE B03-B`
- **CI:** separate authorization required

The detailed archived semantic map remains binding for the complete functionality/logics inventory and all semantic `!=` boundaries. This file is the current B03 execution authority.

---

# 0. Binding objective

B03 activates **Event as a distinct originating owner** and proves that the B02 Schedule engine is genuinely shared.

Target:

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
dante.event                existing canonical Event NativeRef shell
native_address             already supports owner_family='event'
dante.schedule             shared Schedule owner
Schedule subject family    activity | event | occurrence
Event recurrence shell     exists but remains B06-owned
```

Therefore no Event-specific Schedule persistence is justified.

---

# 2. B03-A — Event canonical core ✅ CLOSED / PROVEN

B03-A filled only the Event-owned descriptive/create gap.

Implemented:

```text
event_expectation
  event_ref        PK/FK → event.event_ref
  self_person_ref  FK → person.person_ref
  title            bounded text
  created_at       timestamptz

event_create_operation
create_self_event(uuid,text,text,uuid,text)
TemporalEventApplication
POST /api/v1/temporal/events
GET  /api/v1/temporal/events/{event_ref}
```

Accepted behavior:

- Event identity is application-issued UUIDv7;
- Person self-scope is explicit;
- title is canonical typed Event expectation data;
- operation identity is separate from Event identity;
- same operation + same normalized intent replays;
- same operation + changed intent rejects;
- runtime receives narrow `SELECT`/`EXECUTE`, not generic Event DML;
- canonical Event expectation blocks destructive `_27` downgrade;
- Event Create does not imply Schedule creation in B03-A.

Executed proof:

```text
Event core/API PostgreSQL                         2 PASS
catalog/Dictionary/migration targeted gate       10 PASS
initial harness-only privilege defect             1 FAIL
corrected exact harness rerun                     1 PASS
```

The harness defect was fixed in `8dc423adc8f2cf5cf115061192c603d806e923b3`; it was not a product or migration failure.

B03-A closure authority is the dedicated closure document linked above.

---

# 3. Current B03 gaps after A

```text
GAP-B03-B01  B02 Schedule self-subject authorization is still Activity-descriptor bound
GAP-B03-B02  no atomic Event + initial Schedule application operation yet
GAP-B03-B03  Timeline backend/API remains Activity-only
GAP-B03-B04  frontend Timeline protocol remains Activity-only
GAP-B03-B05  normal-runtime Event Create remains deliberately fail-closed
GAP-B03-C01  postponed/TBD Event lifecycle not active
GAP-B03-D01  Agenda/internal-part canonical persistence absent
```

These are separate gaps and must stay in their owning slices.

---

# 4. B03-B — Shared Schedule + Event Timeline ⬜ NEXT

## 4.1 Goal

Prove the already-established B02 Schedule engine survives a second semantic owner.

Exit invariant:

```text
Activity and Event both use the same ScheduleRef,
placement MaterialState, current binding and history machinery.
```

## 4.2 Persistence/runtime work

Generalize self-subject authorization from:

```text
Activity → activity_intention.self_person_ref
```

to the explicit typed union:

```text
Activity → activity_intention.self_person_ref
Event    → event_expectation.self_person_ref
```

Do **not** create a generic EAV owner table merely to avoid a typed branch.

Affected capability families must be exact-head inspected before edits, including the shared establish/revise/unschedule/Undo routines introduced by B02.

If forward SQL changes are needed, use a new migration after `_27`; historical CP6/B01/B02/B03-A migrations remain immutable.

## 4.3 Atomic Event + Schedule create

Product-visible scheduled Event creation must commit Event truth and initial Schedule truth together.

Required semantic transaction:

```text
create Event identity/expectation
+ establish shared Schedule for EventRef
+ commit once
```

No success response before both effects are accepted.

Idempotency must not collapse Event-create operation identity with Schedule-establish operation identity or Domain identities.

## 4.4 Event placement forms activated in B03-B

User-visible Event placement surface:

```text
timed floating-local
timed named-zone-local
all-day single-day via date_span
multi-day all-day/date_span
```

Shared absolute Schedule remains valid at API/runtime level but need not become a primary manual Event control.

`coarse_local_period` remains a valid shared B02 Schedule form but is not automatically promoted to Event authoring mode without separate semantic justification.

No fake `00:00 → 24:00` timed blocks for all-day Event.

## 4.5 Timeline/read-model union

B03-B extends the **projection**, not canonical persistence:

```text
TimelineItem
├── scheduled_activity
└── scheduled_event
```

Both may carry:

```text
native owner ref
ScheduleRef
current placement MaterialStateRef
title
exact placement form/payload
```

Activity/Event identity remains explicit in backend DTOs and TypeScript discriminated unions.

No generic canonical `temporal_item` table/owner is authorized.

## 4.6 Frontend activation

The existing Event authoring prototype may be activated only for fields canonically supported by B03-B.

Minimum truthful Create path:

```text
Event
title
placement form supported by B03-B
```

Unsupported rich prototype intent remains fail-closed; nothing is silently discarded.

## 4.7 B03-B proof obligations

Required targeted evidence before B03-B closure:

- Event + floating-local Schedule create/reload;
- Event + named-zone Schedule create/reload, including inherited DST semantics;
- all-day Event real date-span lane;
- multi-day Event range/query/render;
- ScheduleRef/current/history identity behaves exactly as shared B02 machinery;
- stale expected-state/idempotency rules remain intact where shared mutations are touched;
- Timeline returns Activity and Event deterministically;
- strict frontend parser accepts the new Event union and rejects malformed payloads;
- Activity create/Schedule/Timeline regressions remain green;
- no Event-specific Schedule table/current/history structure appears.

B03-T02 and the B03-T05 shared Schedule regression gate are expected to become green here. B03-T06 may remain for later lifecycle/full-stack closure if the B03-B E2E does not yet include reschedule/postpone.

---

# 5. B03-C — Event placement lifecycle ⬜

Goal: complete Event placement lifecycle without collapsing it into Activity semantics.

Required behavior:

```text
same Event identity
+ historical/original expectation retained
+ current Schedule may change or be absent
```

Postponed/TBD Event:

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

Reschedule uses existing shared Schedule revision semantics; guarded Undo creates a new accepted placement MaterialState rather than reopening old history.

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

Candidate persistence remains narrow, e.g. Event-scoped ordered parts, unless implementation re-read proves a need for a stronger scoped identity. Do not mint LR-01 owners just to support list editing.

---

# 7. B03-E — closure ⬜

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
```

---

# 10. Current gate

```text
B03-A  ✅ CLOSED / PROVEN
B03-B  ⬜ NOT AUTHORIZED YET
B03-C  ⬜
B03-D  ⬜
B03-E  ⬜
```

Next action requires explicit:

```text
APPROVE B03-B
```