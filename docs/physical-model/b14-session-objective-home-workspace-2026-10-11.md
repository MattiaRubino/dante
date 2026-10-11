# B14 Physical Overlay — Session Execution, Objective Draft and Home Views

- **Status:** CURRENT BRANCH IMPLEMENTATION OVERLAY / USER-LOCAL TECHNICAL GATE GREEN / LIVE-APP ACCEPTANCE OPEN
- **Date:** 2026-10-11
- **Accepted selection:** `pm-12-accepted-physical-model-v1.md` (PostgreSQL 18 family; runtime 18.6)
- **Domain:** `../domain/decisions/activity-session-live-timeline-v1.md` §8
- **Logical:** `../logical-model/slices/b14-session-objective-home-workspace-2026-10-11.md`
- **Database authority:** `../database/timeline-temporal-operational.md`, `../database/dictionary/scope.json`, exact object entries
- **Source:** `../../apps/backend/migrations/versions/20261010_135_b14_session_panel_untimed_start.py` through `20261010_141_b14_independent_planned_sessions.py`

## 1. Forward-only migration chain

Candidate branch migrations form an accepted forward path:
`20261009_134 -> 20261009_135 -> 20261010_136 -> _137 -> _138 -> _139 -> _140 -> _141`.

- **135:** bounded Session panel read and untimed planned-Session admission.
- **136:** owner-guarded atomic directional main Pause/Stop cascade plus planned Start checks.
- **137:** bounded owner-only Session timing/paused history for single-card view.
- **138:** legal Stop from paused Session, closed pause history, UUIDv7 for current MaterialState.
- **139:** `temporal_objective_input_draft`, one record per canonical Objective, owner, JSONB staged payload, revision/CAS and confirmation receipt. Two physical indexes (PK + owner read), one Objective FK and three CHECK constraints. Routines `save_self_objective_input_draft`, `list_self_objective_input_drafts`, `confirm_self_objective_input_draft`. The latter atomically executes the pre-existing canonical ObjectiveResult function and stores the replay receipt.
- **140:** bounded owner-only routines `list_self_home_finished_work`, `list_self_home_objective_work`. Read operations; no new user truth or inferred completion.
- **141:** owner-controlled `start_self_session_for_planned` (not directly granted to runtime/PUBLIC) invoked only inside planned Schedule/actor admission. Original generic `start_self_session` preserves main live-capture guard. No Session nesting table or extra Schedule engine.

**Current exact candidate schema:** **238 tables, 5 views, 228 routines, 103 triggers, 486 indexes, 421 foreign keys, 596 CHECK**. Cumulative WSL user tests and exact cross-representation catalog verification were reported green. These results are candidate-branch evidence, not protected-main merge evidence.

## 2. Owner-only security / bounded reads

The runtime does not receive direct DML grants on the provisional Objective table. Its API calls approved SECURITY DEFINER routines via the existing DatabaseRuntime transaction boundary. CAS and idempotent replay are required for input save and confirmation; no published migration should be rewritten after application (fixes require new forward migration). Historical Session and Objective results are never overwritten by a visual projection.

The History/Objective workspace read is self-scoped and bounded (1–100 max request, Home default 40). This is not an unlimited historical browser. Timezone-aware projected Session geometry is frontend-only and cannot become Schedule truth.

## 3. Existing Physical baseline remains in force

The accepted PM-12/PM-14 architecture was a selection and constraint baseline, **not a complete inventory of every later vertical migration**. This additive overlay tracks current branch implementation without rewriting its protected-main or phase-time evidence. The earlier `activity-subactivity-session-overlay-v1.md` continues to govern Activity decomposition; its capture policy now means optional **main** clock, not the prohibition of all separately planned internal Session runs.

## 4. Acceptance and source discipline

Current status: migrations/Dictionary/SQLAlchemy/current PG catalog and targeted tests are green according to the user-local gate across prior turns; generated API files were pushed in `a9a8353a`. Still open: real app verification of independent child Start, parent cascade, Stop, right-edge Session desk, three Home pages, and persistent draft/explicit confirmation. No CI was used.
