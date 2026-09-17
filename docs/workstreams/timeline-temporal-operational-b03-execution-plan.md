# Timeline / Temporal-Operational — B03 Event Core Execution Plan

- **Status:** B03-A ✅ — B03-B ✅ — B03-C ✅ — B03-D ✅ CLOSED / PROVEN — B03-E NEXT
- **Date:** 2026-09-17
- **Branch:** `feature/timeline-temporal-operational`
- **Current DB authority:** PostgreSQL 18.6 / Alembic `20260917_29`
- **Current topology:** `101|5|31|78|198|119|297|0|0|0`
- **Primary semantic authority:** `docs/domain/concepts/event.md`
- **Detailed semantic freeze:** `docs/workstreams/archive/timeline-temporal-operational-map-ledger-snapshot-2026-09-15.md`
- **Live work map:** `docs/workstreams/timeline-temporal-operational-map.md`
- **Roadmap:** `docs/workstreams/timeline-temporal-operational-roadmap.md`
- **B03-A closure:** `docs/workstreams/timeline-temporal-operational-b03-a-closure-2026-09-16.md`
- **B03-B closure:** `docs/workstreams/timeline-temporal-operational-b03-b-closure-2026-09-17.md`
- **B03-C closure:** `docs/workstreams/timeline-temporal-operational-b03-c-closure-2026-09-17.md`
- **B03-D closure:** `docs/workstreams/timeline-temporal-operational-b03-d-closure-2026-09-17.md`
- **Next implementation gate:** `APPROVE B03-E`
- **CI:** separate authorization required

The archived semantic map remains binding for the complete Event functionality inventory and all semantic `!=` boundaries. This file is the current B03 execution authority.

---

# 0. Binding objective

B03 activates **Event as a distinct originating owner** and proves the Schedule engine is shared.

```text
Activity ─┐
          ├── shared Schedule identity/current/history capability
Event ────┘
```

Forbidden:

```text
activity_schedule + event_schedule split
Event-specific Schedule current/history model
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
Agenda part != Activity/Event/Occurrence/Schedule/Session/Actual by default
original expectation != current Schedule != Actual occurrence
```

---

# 1. Authority result

Re-opened Domain/Logical/Physical authority established:

```text
Event                      LR-01 native identity owner
Schedule                   LR-02 dependent scoped record
dante.event                canonical Event NativeRef shell
native_address             owner_family='event'
dante.schedule             shared Schedule owner
Schedule subject family    activity | event | occurrence
Event recurrence shell     exists but remains B06-owned
```

No Event-specific Schedule persistence is justified.

---

# 2. B03-A — Event canonical core ✅ CLOSED / PROVEN

Established at `_27`:

```text
event_expectation
event_create_operation
create_self_event(...)
TemporalEventApplication
POST /api/v1/temporal/events
GET  /api/v1/temporal/events/{event_ref}
```

Proved stable Event identity, explicit self-Person scope, canonical title data, idempotent same-intent replay, changed-intent conflict and guarded downgrade.

Closure: `timeline-temporal-operational-b03-a-closure-2026-09-16.md`.

---

# 3. B03-B — Shared Schedule + Event Timeline ✅ CLOSED / PROVEN

`_28` generalized Schedule self-scope from Activity-only to an explicit Activity/Event typed union while preserving the single Schedule machinery.

Governed Schedule capability remains shared:

```text
establish_self_schedule_placement(...)
revise_self_schedule_placement(...)
unschedule_self_schedule(...)
undo_self_schedule_unschedule_any(...)
```

Activated Event placement/read forms:

```text
floating-local timed Event
named-zone-local timed Event
all-day/date-span Event
multi-day date-span Event
```

Timeline projection is explicitly discriminated:

```text
scheduled_activity | scheduled_event
```

Named-zone source wall-clock intent remains distinct from resolved instants; all-day Event does not fabricate exact clock time.

Closure: `timeline-temporal-operational-b03-b-closure-2026-09-17.md`.

---

# 4. B03-C — Event placement lifecycle ✅ CLOSED / PROVEN

Accepted invariant:

```text
same Event identity
+ same Schedule identity
+ placement may revise or become absent
+ Schedule history remains monotonic
```

B03-C uses the shared Schedule mutation capability; it required no new migration.

Proven behavior:

```text
reschedule with stable EventRef/ScheduleRef
placement MaterialState advances monotonically
postponed/TBD = Event alive + Schedule/history retained + no current placement
no placeholder date/time
Event remains readable after current placement removal
stale expected-state mutations fail closed
guarded Undo writes a new accepted MaterialState
Undo replay is idempotent
Create-runtime Event can revise/postpone/undo without reload
Timeline Event routes mutations through canonical Schedule datasource
Activity lifecycle remains intact
```

Proof:

```text
PostgreSQL/backend targeted gate    9 PASS / 2 deselected
web Event lifecycle gate            5 files / 16 PASS
@dante/web typecheck                PASS
```

Closure: `timeline-temporal-operational-b03-c-closure-2026-09-17.md`.

---

# 5. B03-D — Agenda/internal parts ✅ CLOSED / PROVEN

## 5.1 Accepted semantic model

```text
Event
└── ordered bounded Agenda/internal values
```

Agenda parts remain values internal to Event. They do not receive NativeRef or independent temporal ownership merely to support editing/reordering.

```text
Agenda part != Activity
Agenda part != Event
Agenda part != Occurrence
Agenda part != Schedule
Agenda part != Session
Agenda part != Actual
```

## 5.2 Persistence at `_29`

```text
event_agenda_part
  event_ref + position + content

event_agenda_current
  event_ref + aggregate revision + updated_at

event_agenda_mutation_operation
  self-scoped operation receipt + expected/resulting revision
  + accepted ordered text[] snapshot
```

Capabilities:

```text
create_self_event_with_agenda(...)
replace_self_event_agenda(...)
```

The wrapper reuses the existing Event create capability rather than duplicating Event identity creation. Empty Agenda remains compatible with pre-B03-D Event create.

## 5.3 Mutation contract

Whole-Agenda replacement is the canonical mutation boundary for add/edit/reorder/remove.

```text
EventRef
+ operation_id
+ expected_revision
+ complete ordered normalized Agenda list
```

Proven semantics:

- initial revision `0` is truthful without a fabricated current row;
- accepted mutation advances revision by exactly one;
- stale expected revision conflicts;
- same operation/same intent replays exactly;
- changed intent under reused operation id conflicts;
- rows remain normalized and position-ordered;
- maximum 100 parts; each part bounded canonical text;
- runtime has no generic direct Agenda DML authority.

## 5.4 API/product

Event read returns canonical Agenda revision + ordered values.

Mutation endpoint:

```text
PUT /api/v1/temporal/events/{event_ref}/agenda
```

The Event detail Agenda editor uses real backend read/mutation truth and supports:

```text
add
edit
reorder up/down
remove
reload
stale conflict → authoritative reload
```

Create activates Agenda as the only B03-D rich Event field; unrelated rich prototype Event fields remain deferred/fail-closed.

## 5.5 Executed proof

```text
focused PostgreSQL/API Agenda               2 PASS
DB/Alembic/Dictionary gate                 12 PASS
B03-D affected web gate                     6 files / 19 PASS
@dante/i18n typecheck                       PASS
@dante/web typecheck                        PASS
final B02+B03 backend regression            13 PASS / 2 deselected
final Activity/Schedule/Event web regression 5 files / 26 PASS
```

The DB gate includes `_29` migration proof, current catalog, whole database catalog, fresh single-head proof and head→base→head roundtrip.

Closure: `timeline-temporal-operational-b03-d-closure-2026-09-17.md`.

---

# 6. Current B03 gaps after B03-D

All B03-A/B/C/D implementation gaps are closed.

Remaining closure-only gaps:

```text
GAP-B03-E01  whole-B03 broad regression gate
GAP-B03-E02  real-stack Chromium Event create/reschedule/all-day/multi-day/reload
GAP-B03-E03  Firefox critical interaction proof where affected
GAP-B03-E04  manual Event userTest
GAP-B03-E05  final Dictionary/live-catalog/docs reconciliation after all proof
```

B03-E must not widen Event semantics just because prototype controls exist.

---

# 7. B03-E — Whole-B03 closure ⬜ NEXT

B03-E is a closure/proof slice.

Required evidence:

- B03 create/application proof;
- timed/all-day/multi-day shared Schedule proof;
- postponed/TBD history/query proof;
- Agenda semantic/frontend proof;
- shared Schedule Activity+Event regression;
- relevant backend/frontend broad regressions;
- real-stack Chromium Event acceptance;
- Firefox proof where the affected critical interactions require it;
- manual Event userTest;
- final Dictionary/SQLAlchemy/Alembic/live-catalog reconciliation;
- final map/roadmap/handoff/global status reconciliation.

If a proof exposes a concrete defect, fix that defect in the owning capability. Otherwise B03-E adds no new product semantics.

CI remains separate and requires explicit authorization.

---

# 8. Rich Event prototype stop line

Still deferred/fail-closed:

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

---

# 9. Risk register

```text
R1  silently accepting unsupported Event fields             FORBIDDEN
R2  cloning Activity Schedule logic into Event               FORBIDDEN
R3  generic owner/EAV shortcut erasing owner meaning         FORBIDDEN
R4  treating postponed Event as unplaced Activity            FORBIDDEN
R5  Event implies availability/busy capacity                 FORBIDDEN
R6  activating recurrence before B06                         FORBIDDEN
R7  Agenda identity inflation                                FORBIDDEN
R8  projection union becoming canonical ontology             FORBIDDEN
R9  frontend behavior preceding backend truth                FORBIDDEN
R10 Agenda part acquiring Schedule/Session/Actual by default  FORBIDDEN
```

---

# 10. Current gate

```text
B03-A  ✅ CLOSED / PROVEN
B03-B  ✅ CLOSED / PROVEN
B03-C  ✅ CLOSED / PROVEN
B03-D  ✅ CLOSED / PROVEN
B03-E  ⬜ NEXT / NOT YET AUTHORIZED
```

Next action requires explicit:

```text
APPROVE B03-E
```