# B14 live Session execution — bounded implementation scope and acceptance

**Branch:** `feature/timeline-temporal-operational`  
**Approved product authority:** `docs/domain/decisions/activity-session-live-timeline-v1.md` (user-approved 2026-10-10).  
**PRE-SCOPE HEAD:** `0138a8844be7661a3e075ac2c2d671bcb4a5fcb2` (the last baseline before these candidate writes).  
**Last observed candidate HEAD:** `ae617045431130b41dbd4c0f13cd539df6429071`.  

## Purpose

One complete candidate implementing and testing the right-hand Session desk with five-minute preview, main/internal hierarchy, atomic main Pause/Stop and noncascade Resume, actual-aware single Timeline card with planned-vs-real history preserved, batched authenticated real timing feed, immutable Schedule and no fake execution. The old _135 publication scope remains historic evidence.

## Exact implementation diff through observed candidate HEAD

### CREATE

- `apps/backend/migrations/versions/20261010_136_b14_session_hierarchy.py`
- `apps/backend/migrations/versions/20261010_137_b14_session_visuals.py`
- `apps/backend/tests/integration/temporal/test_b14_session_hierarchy.py`
- `apps/web/src/features/home/ui/timeline/timeline-session-reality.test.ts`
- `apps/web/src/features/home/ui/timeline/timeline-session-reality.ts`
- `docs/database/dictionary/routines/list_self_activity_session_visuals.json`
- `docs/database/dictionary/routines/transition_self_activity_session_group.json`
- `docs/domain/decisions/activity-session-live-timeline-v1.md`
- `tooling/verify-b14-session-live-local.sh`

### UPDATE

- `apps/backend/src/dante/modules/temporal/session_panel_api.py`
- `apps/backend/src/dante/modules/temporal/session_runtime.py`
- `apps/backend/tests/integration/database/test_current_catalog.py`
- `apps/backend/tests/integration/database/test_database_current_catalog.py`
- `apps/backend/tests/integration/temporal/test_b14_session_panel.py`
- `apps/backend/tests/test_session_panel.py`
- `apps/web/src/features/home/ui/timeline/model/timeline-types.ts`
- `apps/web/src/features/home/ui/timeline/timeline-day-stream.tsx`
- `apps/web/src/features/home/ui/timeline/timeline-session-panel.test.tsx`
- `apps/web/src/features/home/ui/timeline/timeline-session-panel.tsx`
- `apps/web/src/features/home/ui/timeline/timeline-surface.tsx`
- `apps/web/src/features/home/ui/timeline/timeline.css`
- `apps/web/src/features/temporal/use-session-panel.ts`
- `apps/web/tests-browser/session-panel/session-panel.spec.ts`
- `docs/database/README.md`
- `docs/database/dictionary/routines/start_self_planned_activity_session.json`
- `docs/database/dictionary/scope.json`
- `docs/database/timeline-temporal-operational.md`
- `docs/domain/decisions/activity-intervals-and-sessions-v2.md`
- `docs/domain/decisions/activity-planned-session-reschedule-product-v1.md`
- `docs/frontend/home/timeline-session-panel.md`
- `docs/workstreams/timeline-session-panel-scope.md`
- `docs/workstreams/timeline-temporal-operational-handoff.md`
- `docs/workstreams/timeline-temporal-operational-map.md`
- `docs/workstreams/timeline-temporal-operational-roadmap.md`

### DELETE

- None. Old current-product wording is superseded in place, without deleting historical evidence.

## Explicitly out of scope

No CI/GitHub Actions, no protected-main merge, no Event-to-Bozze Move, no generic Home redesign, no automatic Actual/Outcome/Confirmation, no new nested Session table, no user configuration of five-minute offset, no overwriting accepted Schedule, no rewriting applied Alembic revisions, no editing generated OpenAPI/Orval manually.

## Verification and known outstanding points

Candidate source and docs are **published**; new user-local gate **NOT RUN**, and real-app visual acceptance **NOT RUN**. User runs a single `bash tooling/verify-b14-session-live-local.sh` on the WSL worktree after a standalone explicit `git pull --ff-only origin feature/timeline-temporal-operational`. Do not infer success from remote commits. Generated OpenAPI/Orval artifacts must be preserved after local generation, then published exactly once when green. 

Specifically inspect the named/floating-zone early internal Session admission, near-midnight starts, multiple main attempts, multi-interval card clipping, and actual group Pause/Stop transaction races in the user-local gate and manual acceptance. If any is incomplete, keep candidate OPEN and repair it before marking this block accepted. The existing Draft Vault and M5 technical gates predate this change and cannot substitute for current regressions.
