# DANTE Roadmap

- **Status:** CURRENT REPOSITORY ROADMAP — branch candidate reconciled 2026-09-16
- **Pre-vertical integration merge:** `1ecd58145860aebfaaa3dc78933f4ee42698f33` via PR #66
- **Protected-main baseline at vertical selection:** PostgreSQL 18.6 / Alembic `20260906_18` / topology `89|5|18|77|173|91|272|0|0|0`
- **Active candidate workstream:** `feature/timeline-temporal-operational`
- **Candidate temporal DB authority:** PostgreSQL 18.6 / Alembic `20260915_26`
- **Temporal roadmap:** `workstreams/timeline-temporal-operational-roadmap.md`
- **Temporal live map/ledger:** `workstreams/timeline-temporal-operational-map.md`

`protected-main baseline` and `candidate branch truth` are deliberately shown separately. The candidate branch must not be described as protected-main integration until the repository integration gate is actually completed.

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
        B03 Event Core                              ⬜ NEXT
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

The detailed execution order and exact checklists live only in the temporal roadmap/map; this global roadmap does not duplicate their full ledger.

## 2. Pre-vertical foundation — closed

The integrated foundation supplied the small cross-cutting seams required before a real vertical could own operations:

- canonical application-issued UUIDv7 reuse;
- backend Clock abstraction and deterministic time testing;
- named IANA timezone policy and DST edge handling;
- authenticated Account → DanteContext → self Person mapping;
- user/default timezone policy distinct from object-owned temporal semantics;
- governed Web device-timezone transport;
- persistent LOCAL/DEV dogfood;
- deterministic product-independent personas;
- deterministic scale/readiness profiles;
- bounded real-PostgreSQL first-use convergence proof;
- normal LOCAL Vite `/api/v1` proxy topology.

There are exactly three pre-vertical milestones:

```text
PV-01 — Identity / Clock / Time
PV-02 — User Context / Dogfood / Personas
PV-03 — Scale Harness / QA / Closure
```

There is no PV-04.

## 3. Protected-main versus current candidate database boundary

Protected-main baseline at the point the temporal vertical was selected:

```text
PostgreSQL          18.6
Alembic             20260906_18
Topology            89|5|18|77|173|91|272|0|0|0
```

Current candidate truth on `feature/timeline-temporal-operational` after B02 closure:

```text
PostgreSQL          18.6
Alembic             20260915_26
Tables              96
Views                5
Routines             28
Triggers             78
Indexes              191
Foreign keys         111
Checks               285
```

Candidate Dictionary / SQLAlchemy / Alembic parity and HEAD→base→HEAD migration round-trip are proven for B02. This remains candidate-branch truth until integration.

## 4. Temporal vertical completed foundation

### B00 — Real Data Spine ✅

Normal runtime no longer substitutes fake temporal cards/persistence for backend truth. The real product path is authenticated Web → FastAPI/application → PostgreSQL with truthful empty/error behavior and disposable full-stack E2E.

### B01 — Activity Core ✅

Canonical Activity creation, identity, unplaced state, Planning Tray projection, idempotency, reload/refetch and failure truthfulness are real.

### B02 — Schedule Core ✅

Schedule is now a shared canonical capability activated for Activity with:

```text
date_span
floating_local
named_zone_local
absolute
coarse_local_period
```

B02 proves governed placement/revision, explicit current binding/history, Planning Tray placement, drag/editor mutation, unschedule, guarded Undo, CAS/idempotency, DST/source-intent handling and Chromium/Firefox full-stack behavior. Closure authority:

```text
workstreams/timeline-temporal-operational-b02-closure-2026-09-16.md
```

## 5. Next bounded work

The next candidate block is **B03 Event Core**.

B03 exists to prove that Schedule is shared rather than Activity-specific:

```text
Activity ─┐
          ├→ Schedule
Event ────┘
```

It must add real Event identity/expectation, timed/all-day/multi-day/TBD behavior and Event Agenda boundaries without inventing a separate Event scheduling engine.

B03 implementation still requires its own explicit pre-scope/authorization.

## 6. UI/UX checkpoint

A dedicated **B07 UI/UX Consolidation v1** now exists after B06.

Reason: after Activity + Event + Routine + Schedule + Constraints + Life Areas/Tags + Recurrence/Occurrence are real, the temporal product vocabulary is stable enough for a serious redesign without rebuilding the same forms repeatedly.

B07 target is approximately 60–70% mature product quality across Create, Timeline, Planning Tray, temporal editors, responsive/mobile, design-system consistency and accessibility while preserving all governed backend semantics.

Later execution/resolution UI is consolidated again after B10; final visual polish remains part of B15.

## 7. Stable semantic boundaries

Future blocks must preserve:

```text
Person != Account != Principal != Actor
AuthSession != DANTE Session
Activity != Event != Routine
Routine != Recurrence != Occurrence
Occurrence != Schedule
Schedule != Session != Actual
Actual != Outcome
identity != MaterialState != chronology
planned != happened
provider identity != DANTE identity
projection != canonical truth
```

UUID ordering is never chronology/currentness authority.

PostgreSQL remains canonical persistence authority. Provider/network I/O remains outside authoritative PostgreSQL transactions. No generic repository/UoW/EAV/Fact/Version/relationship framework is pre-authorized.

## 8. Existing integrated foundations

```text
Access/Auth + Shared Email                 INTEGRATED
PostgreSQL Recovery                        INTEGRATED
Platform Observability                     INTEGRATED VIA PR #58
AI deterministic low-level foundation      INTEGRATED VIA PR #63
Home / World Focus reconciliation          INTEGRATED VIA PR #65
Pre-vertical foundation                    INTEGRATED VIA PR #66
```

AI production/private-data activation remains a separate qualification. Remote backup-provider and production/cloud recovery remain separately gated.

## 9. Later bounded work outside / after the current temporal sequence

Only when their real trigger exists:

```text
AI real Search owner/data adapter          REAL OWNER/DATA TRIGGER
AI real Ask DANTE integration              PRODUCT-READINESS TRIGGER
AI memory / solver integration             OWNER-DRIVEN / B12-compatible
FTS / pg_trgm / embeddings / pgvector      NEED-DRIVEN
voice / realtime                           FUTURE
browser / computer / code execution        SEPARATE SECURITY GATE
second provider / failover / local model   EVIDENCE-TRIGGERED
deep-reasoning physical binding            EVIDENCE-TRIGGERED
AI production/private-data qualification   SEPARATE ACCEPTANCE
Native Mobile                              OPTIONAL / RE-GATE
later Access/security maturity             FUTURE
production observability tuning            MEASURED-EVIDENCE ONLY
production/cloud recovery                  SEPARATE ACCEPTANCE
```

## 10. Integration rule

The temporal branch is a candidate workstream until its integration process is explicitly completed.

```text
SELECTED != IMPLEMENTED != PASS != REAL UAT != PRODUCTION DEPLOYED
UNMERGED CANDIDATE TRUTH != PROTECTED-MAIN TRUTH
CURRENT SPECIFICATION != APPEND-ONLY DIARY
NO PASS WITHOUT EXECUTED EVIDENCE
```

Closed historical snapshots belong under archive paths or Git history; current canonical documents must describe current truth.