# DANTE Workstream Records

- **Status:** CURRENT INDEX
- **Last reconciled:** 2026-09-22
- **Rule:** current subsystem/workstream files describe present truth; Git/PR/archive preserve chronology

## 1. Current project state

```text
Product / Domain / Logical / Physical            CLOSED / CURRENT
Engineering / Frontend / Backend CP1–CP6        CLOSED / ACCEPTED
PostgreSQL                                       18.6

Access/Auth + Shared Email                       CLOSED / INTEGRATED
PostgreSQL Recovery                              CLOSED / INTEGRATED
Platform Observability                           CLOSED / INTEGRATED VIA PR #58
AI deterministic low-level foundation            CLOSED / INTEGRATED VIA PR #63
Home / World Focus reconciliation                CLOSED / INTEGRATED VIA PR #65
Pre-vertical foundation                          CLOSED / INTEGRATED VIA PR #66

Protected-main baseline at temporal selection    Alembic 20260906_18
Active candidate workstream                      feature/timeline-temporal-operational
Candidate temporal DB authority                  Alembic 20260922_55
Candidate temporal topology                      145|5|87|92|285|223|408|0|0|0

Timeline / Temporal-Operational:
B00 Real Data Spine                              ✅ CLOSED / PROVEN
B01 Activity Core                                ✅ CLOSED / PROVEN
B02 Schedule Core                                ✅ CLOSED / PROVEN
B03 Event Core                                   ✅ CLOSED / PROVEN
B04 Temporal Constraints + Movement Policy       ✅ CLOSED / PROVEN
B05 Product Organization                         ✅ CLOSED / PROVEN
B06 Routine / Recurrence / Occurrence Baseline   🟨 B06-D IMPLEMENTATION IN PROGRESS
B07 UI/UX Consolidation v1                       ⬜ planned after B06
B15 Whole Vertical Closure                       ⬜ future
```

Candidate branch truth is not protected-main truth until integration. Branch-local roadmap/map/handoff remain the authority for temporal sequencing and progress.

## 2. Current Timeline / Temporal-Operational authority

Use these files for the active vertical:

- `timeline-temporal-operational-roadmap.md` — current ordered roadmap B00–B15;
- `timeline-temporal-operational-map.md` — current semantic map + live proof ledger;
- `timeline-temporal-operational-handoff.md` — current B06-D handoff;
- `timeline-temporal-operational-b06-execution-plan.md` — current B06 execution authority;
- `timeline-temporal-operational-b06-c-implementation-freeze.md` — proven B06-C surface;
- `timeline-temporal-operational-b06-c-closure-2026-09-22.md` — B06-C direct closure evidence;
- `timeline-temporal-operational-b06-d-implementation-freeze.md` — approved B06-D Schedule/Timeline/UI boundary;
- `timeline-temporal-operational-b03-a-closure-2026-09-16.md` — B03-A closure;
- `timeline-temporal-operational-b03-b-closure-2026-09-17.md` — B03-B closure;
- `timeline-temporal-operational-b03-c-closure-2026-09-17.md` — B03-C closure;
- `timeline-temporal-operational-b03-d-closure-2026-09-17.md` — B03-D Event Agenda closure;
- `timeline-temporal-operational-b03-e-closure-2026-09-18.md` — B03-E / whole-B03 closure;
- `timeline-temporal-operational-b03-usertest.md` — executed manual B03 acceptance, PASS.

Historical snapshots under `archive/` preserve old wording/numbering without competing with current authority, including the complete initial temporal semantic/functionality map:

- `archive/timeline-temporal-operational-roadmap-freeze-2026-09-07.md`;
- `archive/timeline-temporal-operational-map-ledger-snapshot-2026-09-15.md`;
- `archive/timeline-temporal-operational-live-ledger-snapshot-2026-09-16-pre-b03.md`.

The archived full map remains binding semantic evidence for capability inventory, `!=` disambiguations, ownership/lifecycle/projection rules and later-block obligations. The live map tracks what is implemented/proven.

### Current temporal numbering

```text
B00 Real Data Spine
B01 Activity Core
B02 Schedule Core
B03 Event Core
B04 Temporal Constraints + Movement Policy
B05 Product Organization
B06 Routine / Recurrence / Occurrence Baseline
B07 UI/UX Consolidation v1
B08 Session Runtime
B09 Responsibility / Participation
B10 Actual / Outcome / Confirmation / Resolution
B11 Advanced Recurrence / Conditional / Reminder
B12 Replanning / Conflict / Solver
B13 Provider / Offline / Multi-device
B14 Analytics / Statistics / Signals
B15 Whole Vertical Closure
```

## 3. Current temporal gate

```text
B03 Event Core                                   ✅ CLOSED / PROVEN
B04 Temporal Constraints + Movement Policy       ✅ CLOSED / PROVEN
B05 Product Organization                         ✅ CLOSED / PROVEN
B06-A Routine canonical core                     ✅ CLOSED / PROVEN
B06-B Recurrence authoring                       ✅ CLOSED / PROVEN
B06-C Occurrence checkpoint and scope            ✅ CLOSED / PROVEN
```

Current candidate persistence authority:

```text
Alembic  20260922_55
Topology 145|5|87|92|285|223|408|0|0|0
```

Whole-B03 closure evidence includes:

```text
real-stack Chromium + Firefox                 2 PASS
web broad regression                          158 files / 741 PASS
Temporal PostgreSQL broad regression          24 PASS / 2 deselected
backend broad                                 494 PASS + sole generated OpenAPI mismatch
OpenAPI governance after canonical generation 8 PASS
manual Event userTest A–F                     PASS
```

The manual acceptance Agenda rename defect was closed before B03 closure with explicit Save/Cancel behavior and regression coverage. The postponed/TBD rediscovery need is transferred to B05 Product Organization; it does not change B03's correct no-current-Schedule semantics.

The current gate is B06-D shared Schedule, Timeline and functional UI integration. CI remains separately authorized and was not launched for B06-C closure.

## 4. Global authority

Global current truth is owned by:

- `../PROJECT-STATUS.md` for protected-main truth;
- `../ROADMAP.md` for global sequencing plus branch-candidate frontier;
- executable repository truth;
- current subsystem references;
- active bounded workstream authority while the branch remains unmerged.

Protected-main integration records remain distinct from branch candidate truth.

## 5. Pre-vertical foundation disposition

The pre-vertical foundation is closed and integrated. Its retained closure/evidence record is `pre-vertical-foundation-closure-2026-09-06.md`.

Durable references include authenticated DanteContext, Database README, dogfood personas/scale harness and PostgreSQL recovery runbook. There is no PV-04.

## 6. Documentation lifecycle rule

Before continuing any active workstream:

1. verify exact branch/worktree/remote relation;
2. read current global/subsystem authority;
3. read active roadmap/map/handoff;
4. use the archived full semantic map as binding functionality/non-collapse authority;
5. prefer repository/code/tests over conversation memory;
6. keep protected-main and unmerged candidate truth distinct;
7. do not mark selected/unimplemented capability as PASS;
8. update the live ledger in the same closure/reconciliation slice;
9. archive superseded planning snapshots rather than leave competing live authorities;
10. do not falsify unexecuted manual/CI evidence.

## 7. Permanent rules

```text
SELECTED != IMPLEMENTED != PASS != REAL UAT != PRODUCTION DEPLOYED
UNMERGED CANDIDATE TRUTH != PROTECTED-MAIN TRUTH
CURRENT SPECIFICATION != APPEND-ONLY DIARY
APPLIED MIGRATION HISTORY IS IMMUTABLE
NO PASS WITHOUT EXECUTED EVIDENCE
planned != happened
Schedule != Session != Actual
Routine != Recurrence != Occurrence
Activity != Event != Routine
Agenda part != Activity/Event/Occurrence/Schedule/Session/Actual by default
postponed/TBD Event != Planning Tray Activity
projection != canonical truth
current accepted state != latest row
Undo != history rewind
```
