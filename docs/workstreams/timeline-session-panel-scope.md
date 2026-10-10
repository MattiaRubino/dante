# Session panel — historical _135 publication gate

> **HISTORICAL / _135 EVIDENCE ONLY (superseded 2026-10-10).** This remains exact publication evidence for the original panel. Current accepted product rules and new implementation are in `docs/domain/decisions/activity-session-live-timeline-v1.md` and `docs/frontend/home/timeline-session-panel.md`. Do not use this past path list as the scope for the _136/_137 extension.

BRANCH: `feature/timeline-temporal-operational`

PRE-SCOPE: `da9ca36046110474e6902fb676862e27cbb8cff6`

PURPOSE: right-side Timeline Session panel with clock-aware availability, Activity grouping, existing runtime controls, safe untimed planned execution, isolated batched read, tests and generated contract.

EXPLICITLY OUT OF SCOPE: Bozze/legacy-item redesign, Objective edits, Event semantics, existing history, CI/Actions, protected main, deployment and persistent user database migration.

CREATE:

- `apps/backend/migrations/versions/20261009_135_b14_session_panel_untimed_start.py`
- `apps/backend/src/dante/modules/temporal/session_panel_api.py`
- `apps/backend/tests/test_session_panel.py`
- `apps/backend/tests/integration/temporal/test_b14_session_panel.py`
- `apps/web/src/features/temporal/use-session-panel.ts`
- `apps/web/src/features/home/ui/timeline/timeline-session-panel.tsx`
- `apps/web/src/features/home/ui/timeline/timeline-session-panel.css`
- `apps/web/src/features/home/ui/timeline/timeline-session-panel.test.tsx`
- `apps/web/playwright.session-panel.config.ts`
- `apps/web/tests-browser/session-panel/index.html`
- `apps/web/tests-browser/session-panel/fixture.tsx`
- `apps/web/tests-browser/session-panel/session-panel.spec.ts`
- `docs/database/dictionary/routines/list_self_open_activity_sessions.json`
- `docs/database/dictionary/routines/list_self_session_panel_inputs.json`
- `docs/frontend/home/timeline-session-panel.md`
- `docs/workstreams/timeline-session-panel-scope.md`
- `tooling/verify-b14-session-panel-local.sh`
- `packages/api-client/src/generated/model/sessionPanelExecution.zod.ts`
- `packages/api-client/src/generated/model/sessionPanelGroup.zod.ts`
- `packages/api-client/src/generated/model/sessionPanelResponse.zod.ts`
- `packages/api-client/src/generated/model/sessionPanelRow.zod.ts`

UPDATE:

- `apps/backend/src/dante/bootstrap/app.py`
- `apps/backend/tests/integration/database/test_current_catalog.py`
- `apps/backend/tests/integration/database/test_database_current_catalog.py`
- `apps/web/src/features/home/ui/timeline/timeline-header.tsx`
- `apps/web/src/features/home/ui/timeline/timeline-surface.tsx`
- `docs/database/dictionary/routines/start_self_planned_activity_session.json`
- `docs/database/dictionary/scope.json`
- `docs/database/timeline-temporal-operational.md`
- `docs/workstreams/timeline-temporal-operational-handoff.md`
- `docs/workstreams/timeline-temporal-operational-map.md`
- `docs/workstreams/timeline-temporal-operational-roadmap.md`
- `packages/api-client/openapi/dante-v1.openapi.json`
- `packages/api-client/src/generated/dante.ts`
- `packages/api-client/src/generated/model/index.ts`

DELETE: none.

The approved candidate is published on the branch. Remote tree and payload readback confirmed the exact 21 CREATE and 14 UPDATE paths above with no additional changes from PRE-SCOPE. No CI or persistent application database migration was run. PostgreSQL, browser and real-app acceptance remain for the user-local gate in `docs/frontend/home/timeline-session-panel.md`.
