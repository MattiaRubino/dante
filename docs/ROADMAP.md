# DANTE Roadmap

- **Status:** CURRENT REPOSITORY ROADMAP — branch candidate reconciled 2026-09-18
- **Pre-vertical integration merge:** `1ecd58145860aebfaaa3dc78933f4ee42698f33` via PR #66
- **Protected-main baseline at vertical selection:** PostgreSQL 18.6 / Alembic `20260906_18` / topology `89|5|18|77|173|91|272|0|0|0`
- **Active candidate workstream:** `feature/timeline-temporal-operational`
- **Candidate temporal DB authority:** PostgreSQL 18.6 / Alembic `20260917_29`
- **Candidate temporal topology:** `101|5|31|78|198|119|297|0|0|0`
- **Temporal roadmap:** `workstreams/timeline-temporal-operational-roadmap.md`
- **Temporal live map/ledger:** `workstreams/timeline-temporal-operational-map.md`
- **B03-E / whole-B03 closure:** `workstreams/timeline-temporal-operational-b03-e-closure-2026-09-18.md`

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
        B03 Event Core                              ✅ CLOSED / PROVEN
        B04 Temporal Constraints + Movement Policy  ⬜ NEXT
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

Current candidate truth after B03 closure:

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

B03-E introduced no database migration, so `_29` remains the candidate authority.

This remains candidate-branch truth, not protected-main truth.

## 4. Temporal vertical completed foundation

### B00 — Real Data Spine ✅

Normal runtime uses authenticated Web → FastAPI/application → PostgreSQL truth with real empty/error behavior and disposable full-stack proof.

### B01 — Activity Core ✅

Canonical Activity identity, actionable-intention descriptor, idempotent create, unplaced state, Planning Tray projection and reload identity are real.

### B02 — Schedule Core ✅

Schedule is a shared canonical capability activated for Activity across accepted temporal forms, with governed establish/revision/current-history/unschedule/Undo/CAS/idempotency/DST semantics.

### B03 — Event Core ✅ CLOSED / PROVEN

B03 established Event as a distinct canonical originating owner using the shared Schedule capability rather than an Event-specific temporal engine.

```text
B03-A canonical Event identity/expectation/create/read       ✅
B03-B shared Schedule + timed/all-day/multi-day Timeline     ✅
B03-C reschedule + postponed/TBD + guarded Undo              ✅
B03-D ordered Event Agenda/internal parts                    ✅
B03-E whole-B03 regression/real-stack/manual closure         ✅
```

Final B03 proof includes:

```text
real-stack Chromium + Firefox                 2 PASS
web broad regression                          158 files / 741 PASS
Temporal PostgreSQL broad regression          24 PASS / 2 deselected
backend broad                                 494 PASS + sole generated OpenAPI mismatch
OpenAPI governance after canonical generation 8 PASS
manual Event userTest A–F                     PASS
```

The manual Agenda rename defect was closed before acceptance with explicit Save/Cancel plus Enter/Escape behavior. Postponed/TBD Event rediscovery is transferred to B05 Product Organization without changing B03's canonical no-current-Schedule semantics.

## 5. Next bounded work — B04

B04 is **Temporal Constraints + Movement Policy**.

Before implementation it must reopen and reconcile the relevant Domain / Logical / Physical authority and the archived temporal functionality map.

Required semantic separation starts with:

```text
Schedule != Temporal Constraint
constraint != placement
movement policy != solver result
proposal != accepted effect
planned/intended != happened
```

B04 must not activate later-owned semantics early.

The next explicit gate is:

```text
APPROVE B04
```

## 6. B05 transfer from B03 manual acceptance

B05 Product Organization now explicitly owns this discovered need:

```text
provide a discoverable surface for postponed/TBD Events
so they can later be explicitly rescheduled
without converting them into Activity Planning Tray items
and without fabricating date/time truth
```

This is a product-organization concern, not a reason to weaken Event/Schedule semantics.

## 7. UI/UX checkpoint

A dedicated **B07 UI/UX Consolidation v1** remains after B06, when the core planning vocabulary is stable enough for serious consolidation without repeated rebuilds.

Later execution/resolution UI is consolidated after B10; final polish remains B15.

## 8. Stable semantic boundaries

```text
Person != Account != Principal != Actor
AuthSession != DANTE Session
Activity != Event != Routine
Routine != Recurrence != Occurrence
Occurrence != Schedule
Schedule != Temporal Constraint
Schedule != Session != Actual
Actual != Outcome
Event != Availability / Capacity Claim
Agenda part != Activity/Event/Occurrence/Schedule/Session/Actual by default
postponed/TBD Event != Planning Tray Activity
identity != MaterialState != chronology
planned != happened
provider identity != DANTE identity
projection != canonical truth
```

UUID ordering is never chronology/currentness authority.

PostgreSQL remains canonical persistence authority. Provider/network I/O remains outside authoritative PostgreSQL transactions. No generic repository/UoW/EAV/Fact/Version/relationship framework is pre-authorized.