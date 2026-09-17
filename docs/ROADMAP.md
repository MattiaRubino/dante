# DANTE Roadmap

- **Status:** CURRENT REPOSITORY ROADMAP — branch candidate reconciled 2026-09-17
- **Pre-vertical integration merge:** `1ecd58145860aebfaaa3dc78933f4ee42698f33` via PR #66
- **Protected-main baseline at vertical selection:** PostgreSQL 18.6 / Alembic `20260906_18` / topology `89|5|18|77|173|91|272|0|0|0`
- **Active candidate workstream:** `feature/timeline-temporal-operational`
- **Candidate temporal DB authority:** PostgreSQL 18.6 / Alembic `20260917_28`
- **Candidate temporal topology:** `98|5|29|78|195|115|288|0|0|0`
- **Temporal roadmap:** `workstreams/timeline-temporal-operational-roadmap.md`
- **Temporal live map/ledger:** `workstreams/timeline-temporal-operational-map.md`
- **B03-A closure:** `workstreams/timeline-temporal-operational-b03-a-closure-2026-09-16.md`
- **B03-B closure:** `workstreams/timeline-temporal-operational-b03-b-closure-2026-09-17.md`
- **B03-C closure:** `workstreams/timeline-temporal-operational-b03-c-closure-2026-09-17.md`

`protected-main baseline` and `candidate branch truth` are deliberately separate. The candidate branch must not be described as protected-main integration until the repository integration gate is actually completed.

## 1. Current sequence

```text
Product / Domain / Logical / Physical
        CLOSED / CURRENT
              ↓
Engineering + Frontend + Backend CP1–CP6
        CLOSED / ACCEPTED
              ↓
Access/Auth + Shared Email + Recovery + Observability + AI foundation
        CLOSED / PROTECTED-MAIN INTEGRATED
              ↓
Home / World Focus + Pre-vertical Foundation
        CLOSED / PROTECTED-MAIN INTEGRATED
              ↓
TIMELINE / TEMPORAL-OPERATIONAL VERTICAL
        B00 Real Data Spine                         ✅ CLOSED / PROVEN
        B01 Activity Core                           ✅ CLOSED / PROVEN
        B02 Schedule Core                           ✅ CLOSED / PROVEN
        B03 Event Core                              🟨 B03-A + B03-B + B03-C CLOSED / B03-D NEXT
        B04 Temporal Constraints                    ⬜
        B05 Product Organization                    ⬜
        B06 Routine / Recurrence / Occurrence       ⬜
        B07 UI/UX Consolidation v1                  ⬜
        B08 Session Runtime                         ⬜
        B09 Responsibility / Participation          ⬜
        B10 Actual / Outcome / Confirmation         ⬜
        B11 Advanced Recurrence / Conditional       ⬜
        B12 Replanning / Solver                     ⬜
        B13 Provider / Offline / Multi-device       ⬜
        B14 Analytics / Signals                     ⬜
        B15 Whole Vertical Closure                  ⬜
```

The exact temporal capability ledger lives in the temporal roadmap/map. The initial full functionality/logic inventory remains preserved and binding in `workstreams/archive/timeline-temporal-operational-map-ledger-snapshot-2026-09-15.md`.

## 2. Protected-main foundation

Protected-main currently includes the accepted pre-vertical foundation:

```text
Access/Auth + Shared Email
PostgreSQL Recovery
Platform Observability
AI deterministic low-level foundation
Home / World Focus reconciliation
Pre-vertical identity/context/time/scale foundation
```

The pre-vertical foundation supplied application-issued UUIDv7 reuse, backend Clock abstraction, named IANA timezone/DST policy, authenticated Account → DanteContext → self Person mapping, governed device-timezone transport, persistent LOCAL/DEV dogfood, deterministic personas/scale profiles and bounded real-PostgreSQL convergence proof.

There is no PV-04.

## 3. Candidate database boundary

Protected-main baseline at temporal selection:

```text
Alembic             20260906_18
Topology            89|5|18|77|173|91|272|0|0|0
```

Current candidate truth after B03-C:

```text
Alembic             20260917_28
Tables              98
Views                5
Routines             29
Triggers             78
Indexes              195
Foreign keys         115
Checks               288
```

`_28` generalizes governed Schedule routine authorization to explicit Activity OR Event ownership. B03-C required no additional migration because Event lifecycle is expressed by the already-canonical shared Schedule revision/unschedule/Undo machinery.

This is candidate-branch truth, not protected-main truth.

## 4. Temporal vertical completed foundation

### B00 — Real Data Spine ✅

Normal runtime uses authenticated Web → FastAPI/application → PostgreSQL truth with real empty/error behavior and disposable full-stack proof.

### B01 — Activity Core ✅

Canonical Activity identity, actionable-intention descriptor, idempotent create, unplaced state, Planning Tray projection and reload/refetch identity are real.

### B02 — Schedule Core ✅

Schedule is a shared canonical capability activated for Activity across date-span, floating-local, named-zone-local, absolute and coarse-local-period, with governed establish/revision/current-history/unschedule/Undo/CAS/idempotency/DST semantics.

### B03-A — Event canonical core ✅

B03-A established Event as a real distinct originating owner:

```text
event_expectation
event_create_operation
create_self_event(...)
TemporalEventApplication
POST /api/v1/temporal/events
GET  /api/v1/temporal/events/{event_ref}
```

### B03-B — Shared Schedule + Event Timeline ✅

B03-B proves Schedule is genuinely shared rather than Activity-specific:

```text
Activity ─┐
          ├→ one Schedule identity/current/history capability
Event ────┘
```

Accepted scope includes:

```text
typed Activity-or-Event self-subject authorization
atomic Event + initial Schedule commit
floating-local Event
named-zone Event
all-day/date-span Event
multi-day Event
Timeline backend/API Activity+Event union
strict TypeScript union/parser/hydration
minimal truthful Event Create activation
Activity Schedule regression proof
```

No `event_schedule` was introduced.

### B03-C — Event placement lifecycle ✅

B03-C activates Event lifecycle on the same shared Schedule authority:

```text
reschedule through shared Schedule revision
stable EventRef + ScheduleRef
monotonic placement MaterialState evolution
postponed/TBD without placeholder date/time
Event remains readable with no current placement
stale expected-state conflicts fail closed
guarded Undo writes a new accepted MaterialState
Undo replay remains idempotent
newly-created Event can revise/postpone/undo without reload
Activity lifecycle remains unchanged
```

Proof summary:

```text
PostgreSQL/backend targeted gate       9 PASS / 2 deselected
Event lifecycle web gate               5 files / 16 PASS
@dante/web typecheck                   PASS
```

The boundary remains explicit: `Event expectation != current Schedule != future Actual`. B03-C proves the first distinction; Actual/Outcome/Confirmation remains B10-owned.

## 5. Next bounded work — B03-D

B03-D owns bounded ordered Event Agenda/internal parts:

```text
Event
└── ordered Agenda/internal parts

Agenda part != Activity
Agenda part != Event
Agenda part != Occurrence
Agenda part != Session
Agenda part != Actual
```

The next slice must inspect Domain/Logical/Physical authority and existing persistence before adding schema, then activate only the minimum durable identity/order/content and frontend behavior required for Event Agenda create/read/edit/reorder/remove/reload.

B03-D must not activate recurrence, constraints, participants, Session, Actual/Outcome/Confirmation, reminders or provider sync early.

The next explicit gate is:

```text
APPROVE B03-D
```

## 6. UI/UX checkpoint

A dedicated **B07 UI/UX Consolidation v1** remains after B06.

Reason: after Activity + Event + Routine + Schedule + Constraints + Life Areas/Tags + Recurrence/Occurrence are real, the product vocabulary is stable enough for a serious redesign without repeatedly rebuilding the same forms.

Later execution/resolution UI is consolidated after B10; final polish remains B15.

## 7. Stable semantic boundaries

```text
Person != Account != Principal != Actor
AuthSession != DANTE Session
Activity != Event != Routine
Routine != Recurrence != Occurrence
Occurrence != Schedule
Schedule != Session != Actual
Actual != Outcome
Event != Availability / Capacity Claim
identity != MaterialState != chronology
planned != happened
provider identity != DANTE identity
projection != canonical truth
```

UUID ordering is never chronology/currentness authority.

PostgreSQL remains canonical persistence authority. Provider/network I/O remains outside authoritative PostgreSQL transactions. No generic repository/UoW/EAV/Fact/Version/relationship framework is pre-authorized.

## 8. Current gate summary

```text
Protected-main integration frontier       PR #66 / Alembic 20260906_18
Temporal candidate frontier               B03-C ✅ / Alembic 20260917_28
Next temporal implementation              B03-D ⬜ requires approval
CI                                        not implicitly authorized
```