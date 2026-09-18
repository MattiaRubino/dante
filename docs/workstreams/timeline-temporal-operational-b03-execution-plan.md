# Timeline / Temporal-Operational — B03 Event Core Execution Plan

- **Status:** ✅ B03-A/B/C/D/E CLOSED / PROVEN — B03 EVENT CORE CLOSED
- **Reconciled:** 2026-09-18
- **Branch:** `feature/timeline-temporal-operational`
- **DB authority:** PostgreSQL 18.6 / Alembic `20260917_29`
- **Topology:** `101|5|31|78|198|119|297|0|0|0`
- **Primary semantic authority:** `docs/domain/concepts/event.md`
- **Detailed semantic freeze:** `docs/workstreams/archive/timeline-temporal-operational-map-ledger-snapshot-2026-09-15.md`
- **Live work map:** `docs/workstreams/timeline-temporal-operational-map.md`
- **Roadmap:** `docs/workstreams/timeline-temporal-operational-roadmap.md`
- **B03-A closure:** `timeline-temporal-operational-b03-a-closure-2026-09-16.md`
- **B03-B closure:** `timeline-temporal-operational-b03-b-closure-2026-09-17.md`
- **B03-C closure:** `timeline-temporal-operational-b03-c-closure-2026-09-17.md`
- **B03-D closure:** `timeline-temporal-operational-b03-d-closure-2026-09-17.md`
- **B03-E / whole-B03 closure:** `timeline-temporal-operational-b03-e-closure-2026-09-18.md`
- **Manual acceptance:** `timeline-temporal-operational-b03-usertest.md` ✅ PASS
- **Next implementation gate:** `APPROVE B04`
- **CI:** no CI launch was required for B03 closure

The archived semantic map remains binding for the complete Event functionality inventory and all semantic `!=` boundaries. This file records the closed B03 execution result; current sequencing continues in the temporal roadmap.

---

# 0. Binding objective — achieved

B03 activated **Event as a distinct originating owner** while proving that Activity and Event share one Schedule capability:

```text
Activity ─┐
          ├── shared Schedule identity/current/history capability
Event ────┘
```

Forbidden collapses remain forbidden:

```text
activity_schedule + event_schedule split
Event-specific Schedule current/history model
Event-as-Activity shortcut
generic temporal mega-entity
```

Permanent boundaries retained:

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
postponed/TBD Event != Planning Tray Activity
```

---

# 1. B03-A — Event canonical core ✅ CLOSED / PROVEN

Established at `_27`:

```text
event_expectation
event_create_operation
create_self_event(...)
TemporalEventApplication
POST /api/v1/temporal/events
GET  /api/v1/temporal/events/{event_ref}
```

Proved stable Event identity, explicit self-Person scope, canonical title data, idempotent replay, changed-intent conflict and guarded migration behavior.

Closure: `timeline-temporal-operational-b03-a-closure-2026-09-16.md`.

---

# 2. B03-B — Shared Schedule + Event Timeline ✅ CLOSED / PROVEN

`_28` generalized the existing Schedule self-scope into an explicit Activity/Event typed union while preserving one Schedule machinery.

Activated Event forms:

```text
floating-local timed Event
named-zone-local timed Event
all-day/date-span Event
multi-day date-span Event
```

Timeline projection remains explicitly discriminated:

```text
scheduled_activity | scheduled_event
```

Named-zone source wall-clock intent remains distinct from resolved instants; all-day Event does not fabricate clock time.

Closure: `timeline-temporal-operational-b03-b-closure-2026-09-17.md`.

---

# 3. B03-C — Event placement lifecycle ✅ CLOSED / PROVEN

Accepted invariant:

```text
same Event identity
+ same Schedule identity
+ placement may revise or become absent
+ Schedule history remains monotonic
```

Proven behavior includes reschedule, postponed/TBD with no current placement, stale-CAS fail-closed, read while unplaced, guarded Undo through a new MaterialState and immediate lifecycle after create.

Postponed/TBD remains distinct from an Activity Planning Tray item.

Closure: `timeline-temporal-operational-b03-c-closure-2026-09-17.md`.

---

# 4. B03-D — Agenda/internal parts ✅ CLOSED / PROVEN

`_29` activated ordered bounded Event-owned Agenda values without identity inflation:

```text
event_agenda_part
event_agenda_current
event_agenda_mutation_operation
create_self_event_with_agenda(...)
replace_self_event_agenda(...)
```

The canonical mutation boundary is aggregate whole-list replacement with EventRef + operation id + expected revision. Add/edit/reorder/remove, CAS, replay and authoritative reload are proven.

Agenda parts do not receive NativeRef, ScheduleRef, Session identity or Actual identity merely because they are editable or ordered.

Closure: `timeline-temporal-operational-b03-d-closure-2026-09-17.md`.

---

# 5. B03-E — Whole-B03 closure ✅ CLOSED / PROVEN

B03-E added no new semantics; it executed the closure proof.

Accepted evidence:

```text
real-stack Chromium + Firefox Event E2E      2 PASS
web broad regression                         158 files / 741 PASS
Temporal PostgreSQL broad regression         24 PASS / 2 deselected
backend broad run                            494 PASS + sole generated OpenAPI mismatch
focused OpenAPI governance after generation  8 PASS
manual Event userTest A–F                    PASS
```

The generated OpenAPI/client mismatch was reconciled through the canonical generator; it was the only failure in the broad non-PostgreSQL backend run.

The manual test exposed and closed the Agenda rename UX defect with explicit **Salva / Annulla**, retaining Enter/Escape behavior and proving cancel causes no backend mutation.

Closure: `timeline-temporal-operational-b03-e-closure-2026-09-18.md`.
Manual acceptance: `timeline-temporal-operational-b03-usertest.md`.

---

# 6. B03 final persistence authority

No database change was required by B03-E. Final candidate authority remains:

```text
PostgreSQL 18.6
Alembic     20260917_29
Topology    101|5|31|78|198|119|297|0|0|0
```

B03-D had already reconciled Dictionary, SQLAlchemy mappings, current-catalog expectations and Alembic head to `_29`; B03-E did not alter that materialization.

---

# 7. Transfers and stop lines

Manual acceptance identified one product-organization transfer:

```text
B05: provide a discoverable surface for postponed/TBD Events
     so they can later be explicitly rescheduled
     without converting them into Planning Tray Activities
     and without fabricating date/time truth.
```

Agenda remains ordered Event-internal content. Independently timed internal segments/sub-events are not Agenda and require a future explicit semantic model if product requirements justify them.

Deferred ownership remains:

```text
Temporal Constraints / movement policy     → B04
Calendar / Life Area / Tags                 → B05
Event recurrence / Routine / Occurrence     → B06
Session/execution                           → B08
participants / invitation responses        → B09
Actual / Outcome / Confirmation            → B10
advanced recurrence / reminders             → B11
provider conferencing / sync               → B13
Agenda-part independent Schedule            → not authorized by B03
```

---

# 8. Closure decision

```text
B03-A  ✅ CLOSED / PROVEN
B03-B  ✅ CLOSED / PROVEN
B03-C  ✅ CLOSED / PROVEN
B03-D  ✅ CLOSED / PROVEN
B03-E  ✅ CLOSED / PROVEN

B03 Event Core  ✅ CLOSED / PROVEN
```

There are no remaining B03 implementation or proof gates.

The next explicit implementation gate is:

```text
APPROVE B04
```

B04 owns Temporal Constraints + Movement Policy and must begin by reopening the relevant Domain/Logical/Physical authority before implementation.