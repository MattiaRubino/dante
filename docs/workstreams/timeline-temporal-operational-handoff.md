# Timeline / Temporal-Operational — Workstream Handoff

- **Status:** B02 ✅ CLOSED / PROVEN → B03 PRE-SCOPE ✅ COMPLETE
- **Reconciled:** 2026-09-16
- **Branch:** `feature/timeline-temporal-operational`
- **Current roadmap:** `docs/workstreams/timeline-temporal-operational-roadmap.md`
- **Current live map/ledger:** `docs/workstreams/timeline-temporal-operational-map.md`
- **B02 closure:** `docs/workstreams/timeline-temporal-operational-b02-closure-2026-09-16.md`
- **B03 execution plan:** `docs/workstreams/timeline-temporal-operational-b03-execution-plan.md`
- **Next implementation gate:** `APPROVE B03-A`
- **Authorization boundary:** B03 deep-read/PRE-SCOPE is complete; no B03 product code or DDL is authorized until the user approves B03-A
- **CI:** no CI launch is implied or authorized by this handoff

## 1. Current workstream position

```text
B00 Real Data Spine                              ✅ CLOSED / PROVEN
B01 Activity Core                                ✅ CLOSED / PROVEN
B02 Schedule Core                                ✅ CLOSED / PROVEN
B03 Event Core                                   🟨 PRE-SCOPE COMPLETE / IMPLEMENTATION PENDING
B04 Temporal Constraints + Movement Policy       ⬜
B05 Product Organization                         ⬜
B06 Routine / Recurrence / Occurrence Baseline   ⬜
B07 UI/UX Consolidation v1                       ⬜ planned after B06
B08 Session Runtime                              ⬜
B09 Responsibility / Participation               ⬜
B10 Actual / Outcome / Confirmation / Resolution ⬜
B11 Advanced Recurrence / Conditional / Reminder ⬜
B12 Replanning / Conflict / Solver               ⬜
B13 Provider / Offline / Multi-device             ⬜
B14 Analytics / Statistics / Signals             ⬜
B15 Whole Vertical Closure                       ⬜
```

## 2. B03 deep-read result

B03 is **not** a second temporal engine.

Current authority already provides:

```text
Event NativeRef shell                           EXISTS
SQLAlchemy EventRow                             EXISTS
Schedule subject eligibility                    activity | event | occurrence
shared Schedule MaterialState/current/history   EXISTS / B02 PROVEN
Event recurrence facet shell                    EXISTS but B06-owned
```

Real B03 gaps are:

```text
Event typed expectation/descriptor persistence  MISSING
Event idempotent create capability              MISSING
B02 Schedule runtime self-scope                  ACTIVITY-DESCRIPTOR BOUND
Timeline backend/API Event projection            MISSING
frontend Timeline Event protocol                 MISSING
normal-runtime Event Create                      deliberately FAIL-CLOSED
Event Agenda durable bounded persistence         MISSING
```

The exact analysis and stop lines are frozen in `timeline-temporal-operational-b03-execution-plan.md`.

## 3. Shared Schedule contract

B03 must reuse B02:

```text
Activity ─┐
          ├→ one Schedule owner/current/history capability
Event ────┘
```

Forbidden unless current authority is explicitly reopened and disproves the present model:

```text
event_schedule table
Event-specific scheduling engine
Event-specific current/history model
```

Existing Schedule runtime routines must instead be boundedly generalized from Activity-only self-scope to typed Activity/Event self-scope.

## 4. Event semantics frozen for B03

B03 must preserve:

```text
Event != Activity
Event != Schedule
Event != Recurrence
Event != Occurrence
Event != Session
Event != Actual
Event != Outcome
Event != Participation
Event != Availability / Capacity Claim
Event identity != provider identity
Agenda part != independent Activity/Event/Occurrence/Session/Actual by default
original expectation != current accepted Schedule != Actual occurrence
```

Activated B03 product placement surface is expected to cover:

- timed floating-local Event;
- timed named-zone Event;
- all-day single-day Event through `date_span`;
- multi-day all-day/date-span Event;
- Schedule revision/reschedule;
- postponed/TBD Event with no current Schedule and no fake placeholder time;
- guarded Undo;
- bounded Event Agenda/internal parts.

## 5. Rich Event prototype stop line

The existing frontend Event form contains future-domain concepts. B03 must not silently persist or discard them.

Remain fail-closed/deferred:

```text
Event recurrence                           → B06
Temporal Constraints / movement policy     → B04
Life Area / product organization           → B05
participants / invitation responses        → B09
Session/execution                          → B08
Actual / Outcome / Confirmation            → B10
reminders / conditional policy             → B11
provider conferencing / sync               → B13
availability/capacity meaning               → separate accepted capacity/provider boundary
visibility/sharing policy                  → actor/security/visibility authority
```

Purpose, expected outcome, free-form resources/pre-read and similar rich meeting metadata are not forced into a speculative Event mega-profile in B03-A; they remain unavailable until an exact canonical owner/shape is justified.

## 6. Planned B03 slices

```text
B03-A  Event canonical core
       Event descriptor + create receipt/capability + self ownership

B03-B  Shared Schedule + Timeline
       genericize typed self-scope, atomic scheduled Event, timed/all-day/multi-day,
       Activity/Event Timeline union

B03-C  Event placement lifecycle
       reschedule + postponed/TBD + Event detail/read + guarded Undo

B03-D  Agenda/internal parts
       bounded ordered Event-internal persistence and real Create/read integration

B03-E  closure
       PG/API/frontend/full-stack/manual + Dictionary/SQLAlchemy/Alembic/docs reconciliation
```

No CI is launched automatically.

## 7. Database starting point

B03 starts from the reconciled B02 candidate:

```text
PostgreSQL 18.6
Alembic     20260915_26
Topology    96|5|28|78|191|111|285|0|0|0
```

`docs/database/README.md` and `docs/database/dictionary/README.md` were reconciled from stale `_23` prose to `_26`. The machine-readable Dictionary `scope.json` was already structurally correct at the `_26` counts.

A forward `_27` is likely justified for the Event descriptor/create boundary, subject to the mandatory exact-head re-read immediately before implementation. Historical CP6/B01/B02 migrations remain immutable.

## 8. Next gate

PRE-SCOPE is complete.

The next authorized action requires explicit approval:

```text
APPROVE B03-A
```

After that approval, implementation begins with the smallest Event canonical core slice. No B03-B/C/D code is smuggled into B03-A unless a transactional/integrity dependency proves it cannot be separated cleanly.