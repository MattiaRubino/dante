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
        B03 Event Core                              🟨 B03-A + B03-B CLOSED / B03-C NEXT
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

Current candidate truth after B03-B:

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

`_28` generalizes governed Schedule routine authorization to explicit Activity OR Event ownership without introducing new tables or a second Event scheduling engine.

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

No `event_schedule` was introduced. Event lifecycle mutation remains deferred to B03-C.

Proof summary:

```text
PostgreSQL/API targeted selection      18 PASS / 4 FAIL first run
single _28 PL/pgSQL regression         fixed; exact failed set 4 PASS
Event transport/Timeline web           10 PASS
B03 Create-runtime web                  2 PASS
@dante/web typecheck                    PASS
```

## 5. Next bounded work — B03-C

B03-C owns Event placement lifecycle:

```text
Event reschedule through shared Schedule revision
postponed/TBD without placeholder date/time
stable Event identity while current Schedule may be absent
truthful detail/read after Schedule absence
guarded Undo by new accepted MaterialState, never history rewind
Activity lifecycle path unchanged
```

B03-C must not activate Agenda persistence, recurrence, constraints, participants, Session, Actual/Outcome/Confirmation, reminders or provider sync early.

The next explicit gate is:

```text
APPROVE B03-C
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
Temporal candidate frontier               B03-B ✅ / Alembic 20260917_28
Next temporal implementation              B03-C ⬜ requires approval
CI                                        not implicitly authorized
```