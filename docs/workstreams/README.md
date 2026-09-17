# DANTE Workstream Records

- **Status:** CURRENT INDEX
- **Last reconciled:** 2026-09-17
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
Candidate temporal DB authority                  Alembic 20260917_29
Candidate temporal topology                      101|5|31|78|198|119|297|0|0|0

Timeline / Temporal-Operational:
B00 Real Data Spine                              ✅ CLOSED / PROVEN
B01 Activity Core                                ✅ CLOSED / PROVEN
B02 Schedule Core                                ✅ CLOSED / PROVEN
B03 Event Core                                   🟨 B03-A/B/C/D CLOSED / B03-E NEXT
B07 UI/UX Consolidation v1                       ⬜ planned after B06
B15 Whole Vertical Closure                       ⬜ future
```

Candidate branch truth is not protected-main truth until integration. Branch-local roadmap/map/handoff remain the authority for temporal sequencing and progress.

## 2. Current Timeline / Temporal-Operational authority

Use these files for the active vertical:

- `timeline-temporal-operational-roadmap.md` — current ordered roadmap B00–B15;
- `timeline-temporal-operational-map.md` — current semantic map + live proof ledger;
- `timeline-temporal-operational-handoff.md` — current handoff/boundary;
- `timeline-temporal-operational-b03-execution-plan.md` — current B03 slice plan;
- `timeline-temporal-operational-b03-a-closure-2026-09-16.md` — B03-A closure;
- `timeline-temporal-operational-b03-b-closure-2026-09-17.md` — B03-B closure;
- `timeline-temporal-operational-b03-c-closure-2026-09-17.md` — B03-C closure;
- `timeline-temporal-operational-b03-d-closure-2026-09-17.md` — B03-D Event Agenda closure.

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
B03-A Event canonical core                  ✅ CLOSED / PROVEN
B03-B Shared Schedule + Event Timeline      ✅ CLOSED / PROVEN
B03-C Event placement lifecycle             ✅ CLOSED / PROVEN
B03-D Agenda/internal parts                 ✅ CLOSED / PROVEN
B03-E Whole-B03 closure                     ⬜ NEXT / requires explicit approval
```

Current candidate persistence authority:

```text
Alembic  20260917_29
Topology 101|5|31|78|198|119|297|0|0|0
```

B03-D adds normalized Event Agenda values plus aggregate revision/CAS and idempotent operation receipts without NativeRef identity for individual parts. The accepted proof is:

```text
focused PostgreSQL/API Agenda               2 PASS
DB/Alembic/Dictionary gate                 12 PASS
B03-D affected web gate                     6 files / 19 PASS
@dante/i18n typecheck                       PASS
@dante/web typecheck                        PASS
final B02+B03 backend regression            13 PASS / 2 deselected
final Activity/Schedule/Event web regression 5 files / 26 PASS
```

B03-E is closure/proof only: broad regressions, real-stack browser acceptance, manual Event userTest and final reconciliation. It must not widen Event semantics without a concrete defect or later owning block.

CI remains separately authorized.

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
projection != canonical truth
current accepted state != latest row
Undo != history rewind
```