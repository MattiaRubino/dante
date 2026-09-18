# Timeline / Temporal-Operational — B03-E Whole-B03 Closure

- **Status:** ✅ CLOSED / PROVEN
- **Date:** 2026-09-18
- **Branch:** `feature/timeline-temporal-operational`
- **Accepted product/code anchor before final documentation reconciliation:** `90fb3f1f4debd81b48abba765d3b012a96360fdf`
- **Alembic head:** `20260917_29`
- **Candidate topology:** `101|5|31|78|198|119|297|0|0|0`
- **Parent slices:** B03-A/B/C/D ✅ CLOSED / PROVEN
- **Next block:** B04 Temporal Constraints + Movement Policy
- **CI:** not used; closure evidence was executed locally

## 1. Closure scope

B03-E is a proof/reconciliation slice. It adds no new Event semantics. Its purpose is to prove the complete B03 Event Core across persistence, backend/API, frontend, real browser stack, manual product acceptance and documentation authority.

B03 closes with these permanent boundaries intact:

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
Agenda part != Activity/Event/Occurrence/Schedule/Session/Actual by default
postponed/TBD Event != Planning Tray Activity
projection != canonical truth
Undo != history rewind
```

## 2. Whole-B03 accepted capability

B03 now proves one canonical Event owner using the same Schedule capability already used by Activity:

```text
Activity ─┐
          ├── shared ScheduleRef / current / history / CAS / idempotency
Event ────┘
```

Accepted Event behavior includes:

```text
canonical Event identity + expectation
self-scoped idempotent create/read
atomic Event + initial shared Schedule
floating-local timed Event
named-zone-local timed Event with source/DST intent
all-day/date-span Event
multi-day Event
Timeline scheduled_activity | scheduled_event projection
reschedule with stable EventRef/ScheduleRef
postponed/TBD = Event alive + history retained + no current placement
guarded Undo through a new accepted MaterialState
ordered bounded Event Agenda/internal values
Agenda add/edit/reorder/remove/reload with aggregate CAS/idempotency
strict API/frontend parsing and authoritative reload behavior
```

No `event_schedule` duplicate temporal engine and no NativeRef per Agenda part were introduced.

## 3. B03-E executed evidence

### 3.1 Real-stack browser proof

The authenticated disposable real stack exercised frontend + backend + PostgreSQL through the product UI.

```text
Chromium   PASS
Firefox    PASS
Result     2 PASS
```

The scenario covered Event create, Timeline reschedule, all-day/date-span, multi-day and canonical reload preservation.

During this proof B03-E exposed and fixed real integration defects rather than hiding them:

- latent inactive Create fields were incorrectly treated as active unsupported Event intent;
- the Home Timeline bridge was injecting the Activity-only create runtime instead of the B03 runtime;
- strict Event response parsing had not yet admitted canonical `agenda_revision` returned after B03-D;
- the Playwright harness had a Chromium response-body/navigation race.

The browser proof passed after those owning defects were corrected.

### 3.2 Broad frontend regression

```text
@dante/web broad Vitest
158 test files / 741 tests PASS
```

### 3.3 Broad Temporal PostgreSQL regression

```text
Temporal PostgreSQL broad gate
24 PASS / 2 deselected
```

### 3.4 Broad backend / OpenAPI governance

The broad non-PostgreSQL backend run reached:

```text
494 PASS
1 generated OpenAPI snapshot mismatch
```

The sole failure was the governed OpenAPI/client snapshot after the intentional B03 public contract changes. The generated artifacts were then regenerated through the canonical repository generator and committed. The focused OpenAPI governance gate was rerun:

```text
tests/test_openapi_export.py
8 PASS in 4.26s
```

The full 494-test selection was not redundantly rerun after this generated-artifact-only reconciliation; the previously observed functional tests were already green and the sole failed guard was rerun directly.

## 4. Manual product acceptance

The B03 manual userTest was executed against the authenticated local real stack and explicitly accepted after the Agenda rename correction.

```text
A Timed Event create + reload        PASS
B Reschedule + reload                PASS
C Postpone/TBD + Undo                PASS
D All-day + multi-day                PASS
E Agenda/internal parts              PASS
F Boundary sanity                    PASS

Overall B03 manual userTest          PASS
```

Manual acceptance exposed one real Agenda UX defect: rename previously depended on Enter and was not explicit enough. The accepted fix added explicit **Salva** / **Annulla**, retained Enter/Escape keyboard behavior, and proved that cancel does not issue a backend mutation.

Accepted fix anchors before final documentation reconciliation:

```text
c3550209  fix(web): make Agenda rename explicit
90fb3f1f  test(web): cover explicit Agenda rename actions
```

## 5. Product transfer discovered by manual acceptance

Postponing an Event correctly removes its current placement without deleting or converting the Event. It must not enter the Activity Planning Tray.

The manual flow also exposed a legitimate future product-organization need: after the immediate guarded Undo affordance is gone, a postponed/TBD Event needs a discoverable surface from which it can be found and deliberately rescheduled.

This is transferred to **B05 Product Organization** as a bounded requirement:

```text
surface postponed/TBD Events for rediscovery and explicit replanning
without converting them into Activity Planning Tray items
without fabricating a date/time
```

This transfer is non-blocking for B03 because B03-C's canonical no-current-Schedule semantics are correct and proven.

## 6. Agenda boundary clarified

B03-D Agenda is not a hidden sub-event model.

```text
Event: Convegno
Agenda:
- Apertura
- Discussione
- Chiusura
```

Those values are ordered internal content. They do not independently own time, ScheduleRef, EventRef or Timeline presence.

If a future vertical requirement needs internal timed segments such as `09:00–10:00 Apertura` and `10:15–11:00 Talk A`, that requires an explicit future semantic model. B03 must not falsify Agenda by silently granting it independent scheduling.

## 7. Persistence authority at closure

No database change was introduced by B03-E. The accepted candidate authority remains:

```text
PostgreSQL 18.6
Alembic     20260917_29
Topology    101|5|31|78|198|119|297|0|0|0
```

The `_29` Dictionary/SQLAlchemy/Alembic/current-catalog authority had already passed the B03-D closure gates and remained untouched during B03-E.

## 8. Deferred semantics remain deferred

B03 does not activate:

```text
Temporal Constraints / movement policy     → B04
Calendar / Life Area / Tags                 → B05
Event recurrence / Routine / Occurrence     → B06
Session/execution                           → B08
participants / invitations                  → B09
Actual / Outcome / Confirmation             → B10
advanced recurrence / reminders             → B11
provider conferencing / sync                → B13
Agenda-part independent Schedule            → not authorized by B03
```

## 9. Closure decision

B03-E is **CLOSED / PROVEN** and therefore **B03 Event Core is CLOSED / PROVEN**.

All B03 implementation/proof slices are complete:

```text
B03-A  ✅ CLOSED / PROVEN
B03-B  ✅ CLOSED / PROVEN
B03-C  ✅ CLOSED / PROVEN
B03-D  ✅ CLOSED / PROVEN
B03-E  ✅ CLOSED / PROVEN

B03 Event Core  ✅ CLOSED / PROVEN
```

The next implementation block is:

```text
B04 Temporal Constraints + Movement Policy
```

No CI run is implied by this closure.