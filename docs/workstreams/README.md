# DANTE Workstream Records

- **Status:** CURRENT INDEX
- **Last reconciled:** 2026-09-23
- **Rule:** current subsystem/workstream files describe present truth; Git/PR/archive preserve chronology

## 1. Current project state

```text
Product / Domain / Logical / Physical            CLOSED / CURRENT
Engineering / Frontend / Backend CP1–CP6        CLOSED / ACCEPTED
PostgreSQL                                       18.6

Access/Auth + Shared Email                       CLOSED / INTEGRATED
PostgreSQL Recovery                              CLOSED / INTEGRATED
Platform Observability                           CLOSED / INTEGRATED
AI deterministic low-level foundation            CLOSED / INTEGRATED
Home / World Focus reconciliation                CLOSED / INTEGRATED
Pre-vertical foundation                          CLOSED / INTEGRATED

Protected-main baseline at temporal selection    Alembic 20260906_18
Active candidate workstream                      feature/timeline-temporal-operational
Candidate temporal DB authority                  Alembic 20260923_57
Candidate temporal topology                      145|5|88|92|285|223|408|0|0|0

Timeline / Temporal-Operational:
B00–B06                                           ✅ CLOSED / PROVEN
B07 UI/UX Consolidation v1                       ⏸ DEFERRED until after B12
B08 Session Runtime                              ← NEXT
B09 Responsibility / Participation               ⬜
B10 Actual / Outcome / Confirmation / Resolution ⬜
B11 Advanced Recurrence / Conditional / Reminder ⬜
B12 Replanning / Conflict / Solver               ⬜
B15 Whole Vertical Closure                       ⬜
```

Former B13 Provider/Offline/Multi-device and B14 Analytics/Statistics/Signals are outside the active `+`/Timeline vertical and remain future backlog concepts. Their historical identifiers are not reassigned.

Candidate branch truth is not protected-main truth until integration.

## 2. Current Timeline / Temporal-Operational authority

Read these files for the active vertical:

1. `timeline-temporal-operational-post-b06-scope-decision-2026-09-23.md` — accepted vertical boundary and post-B06 sequencing;
2. `timeline-temporal-operational-roadmap.md` — current execution order;
3. `timeline-temporal-operational-map.md` — current semantic map + live proof ledger;
4. `timeline-temporal-operational-handoff.md` — current B08 handoff;
5. `timeline-temporal-operational-b06-execution-plan.md` — closed B06 execution authority/evidence route;
6. `timeline-temporal-operational-b06-e-closure-2026-09-23.md` — whole-B06 closure.

Detailed B04/B05/B06 closure records remain durable evidence and are linked by the roadmap/map. Historical snapshots under `archive/` preserve old wording/numbering without competing with current authority.

The archived full semantic map remains binding evidence for capability inventory and non-collapse obligations; the live map owns current progress/sequencing.

## 3. Active temporal sequence

```text
B00 Real Data Spine                              ✅
B01 Activity Core                                ✅
B02 Schedule Core                                ✅
B03 Event Core                                   ✅
B04 Temporal Constraints + Movement Policy       ✅
B05 Product Organization                         ✅
B06 Routine / Recurrence / Occurrence Baseline   ✅

B08 Session Runtime                              ← NEXT
B09 Responsibility / Participation
B10 Actual / Outcome / Confirmation / Resolution
B11 Advanced Recurrence / Conditional / Reminder
B12 Replanning / Conflict / Solver
B07 UI/UX Consolidation v1                       ← DEFERRED
B15 Whole Vertical Closure
```

Vertical scope is bounded to:

```text
Home `+`
→ canonical create/configuration
→ Timeline representation/actions
→ required Session/Actual lifecycle
→ advanced recurrence/reminders
→ replanning/conflict/solver proposals
→ final UI/UX consolidation
```

Explicitly outside this vertical:

```text
external provider integration
native/mobile/offline/multi-device
account-to-account collaboration/chat/shared editing
broad analytics/statistics/signals
```

## 4. Current temporal gate

```text
B06 ✅ CLOSED / PROVEN at `_57`
B07 ⏸ DEFERRED
B08 ← NEXT / NOT STARTED
```

Current candidate persistence authority:

```text
Alembic  20260923_57
Topology 145|5|88|92|285|223|408|0|0|0
```

No new migration is pre-authorized for B08. Current persistence is inspected first; forward-only DDL is added only for a demonstrated semantic gap.

## 5. Global authority

Global current truth is owned by:

- `../PROJECT-STATUS.md` for protected-main truth plus active-candidate pointer;
- `../ROADMAP.md` for repository-level sequencing;
- executable repository truth;
- current subsystem references;
- the active bounded workstream authority while the branch remains unmerged.

Protected-main integration records remain distinct from branch candidate truth.

## 6. Documentation lifecycle rule

Before continuing any active workstream:

1. verify exact branch/worktree/remote relation;
2. read current global/subsystem authority;
3. read active roadmap/map/handoff;
4. use archived semantic freezes as evidence, not competing live status;
5. prefer repository/code/tests over conversation memory;
6. keep protected-main and unmerged candidate truth distinct;
7. do not mark selected/unimplemented capability as PASS;
8. update the live ledger in the same closure/reconciliation slice;
9. archive/supersede stale planning rather than leave competing live authorities;
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
Occurrence != Schedule
Responsibility != Participation
Activity != Event != Routine
projection != canonical truth
current accepted state != latest row
Undo != history rewind
```