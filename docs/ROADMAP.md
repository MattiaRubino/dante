# DANTE Roadmap

- **Status:** CURRENT REPOSITORY ROADMAP — branch candidate reconciled 2026-09-17
- **Pre-vertical integration merge:** `1ecd58145860aebfaaa3dc78933f4ee42698f33` via PR #66
- **Protected-main baseline at vertical selection:** PostgreSQL 18.6 / Alembic `20260906_18` / topology `89|5|18|77|173|91|272|0|0|0`
- **Active candidate workstream:** `feature/timeline-temporal-operational`
- **Candidate temporal DB authority:** PostgreSQL 18.6 / Alembic `20260917_29`
- **Candidate temporal topology:** `101|5|31|78|198|119|297|0|0|0`
- **Temporal roadmap:** `workstreams/timeline-temporal-operational-roadmap.md`
- **Temporal live map/ledger:** `workstreams/timeline-temporal-operational-map.md`
- **B03-A closure:** `workstreams/timeline-temporal-operational-b03-a-closure-2026-09-16.md`
- **B03-B closure:** `workstreams/timeline-temporal-operational-b03-b-closure-2026-09-17.md`
- **B03-C closure:** `workstreams/timeline-temporal-operational-b03-c-closure-2026-09-17.md`
- **B03-D closure:** `workstreams/timeline-temporal-operational-b03-d-closure-2026-09-17.md`

`protected-main baseline` and `candidate branch truth` remain deliberately separate. The candidate branch is not protected-main integration until the repository integration gate actually completes.

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
        B03 Event Core                              🟨 B03-A/B/C/D CLOSED / B03-E NEXT
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

Protected-main currently includes:

```text
Access/Auth + Shared Email
PostgreSQL Recovery
Platform Observability
AI deterministic low-level foundation
Home / World Focus reconciliation
Pre-vertical identity/context/time/scale foundation
```

The pre-vertical foundation supplied UUIDv7 reuse, backend Clock abstraction, named IANA timezone/DST policy, authenticated Account → DanteContext → self Person mapping, governed device-timezone transport, persistent LOCAL/DEV dogfood and deterministic real-PostgreSQL convergence proof.

## 3. Candidate database boundary

Protected-main baseline at temporal selection:

```text
Alembic             20260906_18
Topology            89|5|18|77|173|91|272|0|0|0
```

Current candidate truth after B03-D:

```text
Alembic             20260917_29
Tables              101
Views                 5
Routines              31
Triggers              78
Indexes               198
Foreign keys          119
Checks                297
```

`_28` established shared Activity/Event Schedule authorization. `_29` adds only the narrow Event Agenda aggregate/value/idempotency capability; it does not add a second temporal engine or identity for Agenda parts.

This remains candidate-branch truth, not protected-main truth.

## 4. Temporal vertical completed foundation

### B00 — Real Data Spine ✅

Normal runtime uses authenticated Web → FastAPI/application → PostgreSQL truth with real empty/error behavior and disposable full-stack proof.

### B01 — Activity Core ✅

Canonical Activity identity, actionable-intention descriptor, idempotent create, unplaced state, Planning Tray projection and reload identity are real.

### B02 — Schedule Core ✅

Schedule is a shared canonical capability activated for Activity across accepted temporal forms, with governed establish/revision/current-history/unschedule/Undo/CAS/idempotency/DST semantics.

### B03-A — Event canonical core ✅

Established Event as a distinct canonical originating owner with self-scoped create/read.

### B03-B — Shared Schedule + Event Timeline ✅

Proved Event uses the same Schedule identity/current/history machinery as Activity, including atomic Event + initial Schedule and timed/all-day/multi-day Timeline projection.

### B03-C — Event placement lifecycle ✅

Activated reschedule, truthful postponed/TBD, read with no current placement and guarded Undo through shared Schedule state evolution.

### B03-D — Event Agenda/internal parts ✅

Activated bounded ordered Event Agenda values without identity inflation.

Canonical `_29` shape:

```text
event_agenda_part
event_agenda_current
event_agenda_mutation_operation
create_self_event_with_agenda(...)
replace_self_event_agenda(...)
```

Semantics:

```text
Agenda part != Activity/Event/Occurrence/Schedule/Session/Actual
no NativeRef per Agenda part
aggregate revision/CAS
operation-id idempotent replay
atomic add/edit/reorder/remove as whole-list replacement
real Event read/reload and Event-detail Agenda editor
```

Executed B03-D proof:

```text
focused PostgreSQL/API Agenda               2 PASS
DB/Alembic/Dictionary gate                 12 PASS
B03-D affected web gate                     6 files / 19 PASS
@dante/i18n typecheck                       PASS
@dante/web typecheck                        PASS
final B02+B03 backend regression            13 PASS / 2 deselected
final Activity/Schedule/Event web regression 5 files / 26 PASS
```

## 5. Next bounded work — B03-E

B03-E is **whole-B03 closure/proof**, not a new feature expansion.

Required next evidence:

```text
relevant broad backend/PostgreSQL regressions
relevant broad frontend regressions
real-stack Chromium Event create/reschedule/all-day/multi-day/reload
Firefox critical interaction proof where affected
manual Event userTest
final Dictionary / SQLAlchemy / Alembic / live-catalog reconciliation
final temporal/global documentation closure
```

B03-E must not activate deferred semantics early:

```text
Event recurrence                   → B06
Temporal Constraints               → B04
Life Area / Calendar / Tags        → B05
Session/execution                  → B08
participants / invitations         → B09
Actual / Outcome / Confirmation    → B10
reminders / conditional policy     → B11
provider conferencing / sync       → B13
```

The next explicit gate is:

```text
APPROVE B03-E
```

## 6. UI/UX checkpoint

A dedicated **B07 UI/UX Consolidation v1** remains after B06, when the core planning vocabulary is stable enough for serious consolidation without repeated rebuilds.

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
Agenda part != Activity/Event/Occurrence/Schedule/Session/Actual by default
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
Temporal candidate frontier               B03-D ✅ / Alembic 20260917_29
Next temporal implementation              B03-E ⬜ requires approval
CI                                        not implicitly authorized
```