# Timeline / Temporal-Operational — B03 Event Core Execution Plan

- **Status:** PRE-SCOPE COMPLETE / IMPLEMENTATION NOT YET AUTHORIZED
- **Date:** 2026-09-16
- **Branch:** `feature/timeline-temporal-operational`
- **Current branch authority:** B00/B01/B02 closed; B03 next
- **Database baseline:** PostgreSQL 18.6 / Alembic `20260915_26`
- **Current topology:** `96|5|28|78|191|111|285|0|0|0`
- **Primary semantic authority:** `docs/domain/concepts/event.md`
- **Live work map:** `docs/workstreams/timeline-temporal-operational-map.md`
- **Roadmap:** `docs/workstreams/timeline-temporal-operational-roadmap.md`
- **Inherited Schedule authority:** B02 closure + CP6 Schedule/current/history machinery
- **Purpose:** freeze the exact B03 Event implementation boundary before product/schema writes.

---

# 0. Binding objective

B03 activates **Event as a distinct originating owner** and uses it to prove that B02 Schedule is genuinely shared.

The target architecture is:

```text
Activity ─┐
          ├── shared Schedule owner/current/history capability
Event ────┘
```

not:

```text
activity_schedule
+
event_schedule
```

B03 is therefore not a second scheduling engine. It adds the minimum durable Event expectation state, a governed Event create path, Event-aware Schedule authorization, Event Timeline projection, Event-specific postponed/TBD behavior and the bounded Event Agenda capability already accepted by the product/domain contracts.

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

No B03 convenience may collapse those distinctions.

---

# 1. Authority re-open result

## 1.1 Domain

`docs/domain/concepts/event.md` fixes Event as a persistent expected occurrence whose temporal placement is intrinsic to the represented thing.

Binding consequences for B03:

- Event identity survives official reschedule;
- timed, all-day and multi-day are temporal forms, not Event subtypes;
- Event may have no current Schedule while postponed/TBD;
- a postponed/TBD Event retains identity and historical/original expectation;
- no placeholder date/time may be fabricated merely to keep Event visible;
- early/late/overrun reality does not rewrite Schedule unless expectation was explicitly revised;
- ordinary Event attendance is not a Session;
- Participation response is not Actual attendance;
- Event is not a capacity/busy claim;
- recurring Event uses Event-owned Recurrence, but canonical recurrence/Occurrence generation remains B06;
- Agenda/internal parts remain Event-internal unless independent lifecycle semantics are genuinely required.

## 1.2 Logical

Whole Logical authority classifies:

```text
Event     = LR-01 native identity owner
Schedule  = LR-02 dependent scoped record
```

No generic `Entity`, generic `Status`, generic `timeline_entry` or generic relationship blob is authorized.

## 1.3 CP6 / Physical

Current physical authority already contains:

- `dante.event(event_ref)` as the canonical Event NativeRef shell;
- `EventRow` SQLAlchemy mapping;
- `native_address.owner_family = 'event'` eligibility;
- shared `dante.schedule(schedule_ref, subject_native_ref)`;
- shared placement MaterialState/current/history structures;
- Event eligibility for Schedule/Actual subject validation;
- `event.recurrence` facet infrastructure reserved for the later recurrence block.

The CP6 Schedule subject validator already accepts:

```text
activity | event | occurrence
```

Therefore **no Event-specific Schedule identity/table is justified**.

---

# 2. Current repository gaps

## GAP-B03-01 — Event has identity shell only

Unlike B01 Activity, current Event has no typed self-owned descriptive product row.

Current Activity pattern:

```text
activity
+
activity_intention
+
activity_create_operation
+
create_self_activity(...)
```

Current Event pattern:

```text
event
```

only.

B03 therefore requires a narrow typed Event descriptor rather than storing Event title/intent in Schedule, frontend metadata or generic JSON.

### PRE-SCOPE physical decision

Candidate forward representation:

```text
event_expectation
  event_ref        PK/FK → event.event_ref
  self_person_ref  FK → person.person_ref
  title            bounded non-empty text
  created_at       timestamptz
```

Name rationale: Event represents an expected occurrence; `event_expectation` avoids falsely treating the row as generic Event metadata or an Activity intention.

Final DDL/signature remains implementation-slice authority after exact-head re-read.

## GAP-B03-02 — no governed idempotent Event create

B03 needs a bounded operation receipt/capability analogous in discipline to Activity, not identical by copy:

```text
event_create_operation
create_self_event(...)
```

Requirements:

- operation identity separate from Event NativeRef;
- same operation + same intent may replay;
- same operation + changed intent rejects;
- authenticated self Person bound explicitly;
- application-issued UUIDv7 EventRef;
- runtime receives bounded EXECUTE, not generic Event DML.

## GAP-B03-03 — shared Schedule DB capabilities are still Activity-scoped

Although the CP6 Schedule model itself accepts Event, current B02 runtime routines still authorize the subject by joining `activity_intention`.

Current affected capability families include:

```text
establish_self_schedule_placement(...)
revise_self_schedule_placement(...)
unschedule_self_schedule(...)
undo_self_schedule_unschedule_any(...)
```

B03 must generalize **self-owned schedulable subject authorization** to the activated owner family:

```text
Activity → activity_intention.self_person_ref
Event    → event_expectation.self_person_ref
```

without creating a generic owner table/EAV shortcut and without activating Occurrence product behavior early.

## GAP-B03-04 — Timeline backend/API is Activity-only

Current range query starts from `activity_intention` and current API items are `scheduled_activity` with `activity_ref`.

B03 needs an owner-typed normalized projection such as:

```text
scheduled_activity
scheduled_event
```

or an equivalent explicit discriminated union.

The read model may share placement decoding; canonical Activity/Event identity must remain distinct.

## GAP-B03-05 — frontend Timeline protocol is Activity-only

Current TypeScript read model/parser strictly accepts:

```text
kind = scheduled_activity
activity_ref
```

B03 must add Event as a typed union member and preserve strict protocol validation.

The generic frontend `TemporalProjectionItem.subject` already supports native `kind + id`, so no generic canonical frontend owner model is needed.

## GAP-B03-06 — Event Create exists as rich prototype but normal runtime is fail-closed

The C1 frontend already contains Event authoring controls and an explicit regression proving Event cannot persist before B03:

```text
temporal.create.capability_not_available
```

B03 must remove that fail-closed barrier only for fields whose canonical owner is actually implemented in B03.

Unsupported rich intent must continue to fail closed instead of being silently discarded.

---

# 3. B03 product activation boundary

## 3.1 Activate in B03

The minimum truthful Event creation surface is:

```text
Event identity
+ title
+ accepted Schedule
+ optional Event-internal Agenda parts
```

User-visible placement forms activated for Event in B03:

- timed floating-local;
- timed named-zone-local;
- all-day single-day via `date_span`;
- multi-day all-day/date-span.

Shared absolute Schedule capability remains valid at API/runtime level but need not be exposed as a primary manual Event Create control.

`coarse_local_period` remains a valid shared Schedule form in B02, but B03 does **not** automatically reinterpret a coarse placement as an Event UX mode. Current Event authority/C1 requires a concrete Event placement; coarse Event authoring stays fail-closed unless separately justified.

## 3.2 Explicitly deferred / fail-closed in B03

Current frontend prototypes expose more than B03 may canonically persist. These fields remain noncanonical/fail-closed unless their owning later block is activated:

| Prototype intent | B03 treatment | Future owner/gate |
| --- | --- | --- |
| Event recurrence | fail closed | B06 |
| temporal constraints / movement policy | fail closed | B04 |
| Calendar/Life Area/context organization beyond temporary UI default | do not canonize | B05 |
| participant/invite fields | fail closed | B09 |
| actual attendance | not activated | B09/B10 |
| availability busy/free | do not make Event truth/capacity | later capacity/provider boundary |
| visibility sharing policy | fail closed | actor/security/visibility authority |
| provider conference creation | fail closed | B13 |
| reminders/confirmation policy | fail closed | B10/B11 |
| Actual/Outcome/completion | not activated | B10 |
| Session/execution | not activated | B08 |
| appearance tone | presentation only; not Event canonical truth | B07/B05 |
| preparation/recovery scheduling rules | do not persist as ad-hoc Event columns | B04 / linked Activity semantics |
| resources/pre-read/provider material | defer until exact relation/artifact ownership is activated | later bounded slice |

This table is a blocking truthfulness rule: **B03 must never accept a rich Event form and silently throw away unsupported fields.**

## 3.3 Purpose / expected outcome / notes

The product requirements recognize purpose, expected outcome and notes as useful Event/meeting context, but current Logical/Physical authority does not yet supply an accepted typed persistence owner for them.

B03 does not need those fields to prove Event + Schedule. They remain fail-closed in the first B03 activation rather than forcing a speculative Event mega-profile.

A later explicit Event-detail expansion may activate them when their exact canonical shape is justified.

---

# 4. Event Agenda boundary

B03 must satisfy the existing Event Agenda requirement without promoting Agenda parts into independent temporal owners.

Accepted semantics:

```text
Event
└── Agenda/internal parts
    ├── ordered internal item
    ├── ordered internal item
    └── ordered internal item
```

and:

```text
Agenda part != Activity
Agenda part != Event
Agenda part != Occurrence
Agenda part != Session
Agenda part != Actual
```

Candidate narrow persistence:

```text
event_agenda_part
  event_ref
  ordinal
  body/title
```

with an Event-scoped composite identity/ordering contract unless implementation proof demonstrates a real need for a separate stable scoped reference.

B03 does not invent a new LR-01 owner merely because the UI can reorder agenda rows.

The first activation may bound Agenda to create/read/reload semantics. Later editable/history-rich Agenda behavior requires its own materiality/reconciliation decision if needed.

---

# 5. Schedule reuse contract for Event

B03 must preserve one Schedule engine.

## 5.1 Establish

Atomic Event Create with initial placement conceptually becomes:

```text
create Event identity/expectation
+
establish shared Schedule placement for EventRef
+
commit once
```

No product-visible success is returned before both canonical effects commit.

## 5.2 Revise

Existing Schedule revision semantics remain:

- same ScheduleRef;
- exact expected current MaterialStateRef;
- immutable new placement MaterialState;
- old current-history episode closes;
- new episode opens;
- stale expected state rejects;
- replay/idempotency remains governed.

Event does not receive a separate revision mechanism.

## 5.3 Postpone / TBD

For Event, removing current placement means:

```text
same Event identity
+
retained Schedule/history/original expectation
+
no current accepted Schedule
```

This is semantically different from an unplaced Activity.

Therefore:

```text
postponed/TBD Event != Planning Tray Activity
```

B03 must not place postponed Events into the Activity Planning Tray merely for UI convenience.

A minimum self-scoped Event detail/read capability must keep the Event reconstructible after current Schedule absence. A future unified no-placement surface may display postponed Events only if reason/type remain explicit.

## 5.4 Undo

Guarded Schedule Undo remains the B02 monotonic operation. Restoring a just-unscheduled Event creates a new accepted placement MaterialState; it does not reopen old history.

---

# 6. Timeline/read-model contract

B03 extends the normalized Timeline projection, not the canonical persistence model.

Conceptual current-window union:

```text
TimelineItem
├── scheduled_activity
└── scheduled_event
```

Both carry:

- stable native owner ref;
- stable ScheduleRef;
- current placement MaterialStateRef;
- title;
- exact placement form/payload.

Event-specific Agenda data is not required on every compact Timeline item unless the frozen frontend subitem contract genuinely consumes it. Detail/create/read surfaces may retrieve Agenda separately.

All-day and multi-day Event rendering reuses the existing real all-day/date-span lane and continuation behavior; no fake 00:00–24:00 timed block.

---

# 7. Planned implementation slices

The slices below are the PRE-SCOPE recommendation. They are not implementation authorization by themselves.

## B03-A — Event canonical core

Goal: establish Event as a real self-owned canonical originating owner without prematurely activating the full rich UI.

Candidate changes:

- forward Alembic `_27` if exact-head re-read confirms no later branch migration;
- `event_expectation` typed descriptor;
- `event_create_operation` immutable receipt;
- optional narrow `event_agenda_part` if Agenda is included in A rather than D;
- SQLAlchemy + Dictionary entries;
- `create_self_event(...)` bounded runtime capability;
- backend Event record/application/API data source;
- Event create validation/idempotency/self-scope tests;
- Event remains normal-runtime UI fail-closed until B03-B proves Schedule integration.

Exit proof:

```text
EventRef exists canonically
+ self ownership is explicit
+ title survives reload
+ replay same intent is safe
+ changed-intent operation reuse rejects
+ no Schedule/Activity identity collapse
```

## B03-B — shared Schedule + Event Timeline

Goal: prove Schedule survives a second owner.

Candidate changes:

- forward routine hardening/generalization if required;
- self-subject authorization for Activity OR Event through typed descriptors;
- no Event-specific Schedule tables/routines unless a real capability difference is proven;
- atomic Event + initial Schedule application operation;
- timed floating/named-zone Event;
- all-day/date-span Event;
- multi-day Event;
- backend Timeline union Activity + Event;
- API response union;
- TypeScript Timeline union/parser/rendering;
- activate minimal Event Create surface;
- rerun Activity Schedule regressions.

Exit proof:

```text
Activity and Event both use the same Schedule owner/current/history machinery
```

## B03-C — reschedule + postponed/TBD

Goal: complete Event placement lifecycle.

Candidate changes:

- Event Schedule revision through existing shared revision capability;
- Event unschedule/postpone/TBD through shared currentness removal;
- Event detail/read after absence;
- no Planning Tray collapse;
- guarded Undo;
- reload/history/current-state proof.

Exit proof:

```text
original expectation/history remains reconstructible
current Schedule may be absent
Event identity remains stable
```

## B03-D — Agenda/internal parts

Goal: activate the accepted Event-internal Agenda boundary.

Candidate changes:

- typed Event Agenda persistence if not included in B03-A;
- ordered create/read/reload;
- frontend Agenda authoring wired to real canonical result;
- no automatic Activity/Event/Occurrence/Session/Actual creation;
- future rich editing/history deferred unless separately required.

## B03-E — closure

Required closure evidence:

- Event create/application tests;
- timed/all-day/multi-day PostgreSQL/API tests;
- postponed/TBD history/query tests;
- Agenda semantic/frontend tests;
- shared Schedule Activity + Event regression suite;
- full relevant backend/frontend regression;
- real-stack Chromium Event create/reschedule/all-day/multi-day/reload;
- Firefox critical interaction regression where affected;
- manual Event userTest;
- Dictionary/SQLAlchemy/Alembic/live catalog reconciliation;
- same-change map/roadmap/handoff reconciliation.

CI remains separate and requires explicit user authorization.

---

# 8. Expected persistence evolution

B03 has a **real persistence gap**, so a forward migration is likely justified.

Expected new canonical/control objects are narrowly bounded to Event itself, not Schedule duplication:

```text
possible _27
  event_expectation
  event_create_operation
  create_self_event(...)
  [event_agenda_part if activated in same slice]
```

A following forward revision may be justified to generalize B02 Schedule capability functions from Activity-only self-scope to Activity/Event self-scope while preserving the same Schedule operation receipts/current/history tables.

Historical CP6/B01/B02 migrations must not be edited.

Every real new object requires same-change:

```text
Alembic
+ SQLAlchemy
+ Dictionary
+ human DB reference
+ runtime ACL
+ direct PostgreSQL proof
```

---

# 9. B03 risk register

## R1 — silently persisting prototype-only fields

Highest immediate product risk. The Event form already exposes future concepts. B03 must activate only supported canonical fields and reject the rest.

## R2 — cloning Activity-specific Schedule logic into Event

Forbidden. The correct repair is bounded shared subject authorization over the one CP6 Schedule capability.

## R3 — treating postponed Event as unplaced Activity

Forbidden. Same visual absence does not imply same semantic reason.

## R4 — making Event imply busy/capacity

Forbidden. `Event != Availability / Capacity Claim`.

## R5 — activating recurrence early

Forbidden. Event recurrence authoring exists in the prototype, but canonical evaluator/Occurrence lifecycle remains B06.

## R6 — Agenda identity inflation

Do not create a new native owner merely to support list-item editing.

## R7 — accidental API/read-model genericization into canonical ontology

A typed projection union is allowed. A generic `temporal_item` canonical table/owner is not.

---

# 10. PRE-SCOPE result

```text
Event Domain authority reopened                         PASS
Whole Logical Event/Schedule ownership reopened        PASS
CP6 Event NativeRef shell verified                     PASS
CP6 Schedule Event eligibility verified                PASS
current Alembic head `_26` verified                    PASS
Event SQLAlchemy identity shell verified               PASS
B01/B02 application seams inspected                    PASS
B02 Schedule runtime Activity-hardcoding identified    GAP
Timeline backend/API Activity-only shape identified    GAP
frontend Event prototype + fail-closed boundary read   PASS
frontend Timeline Activity-only protocol identified    GAP
Event minimum descriptor persistence                   GAP
Event create idempotency capability                    GAP
Agenda bounded persistence                             GAP / B03 obligation
provider/recurrence/participation/future fields        EXPLICITLY DEFERRED
B03 implementation                                     NOT YET AUTHORIZED
```

Recommended next gate:

```text
APPROVE B03-A
```

Only after that approval should implementation begin.