# Lifecycle candidate Git write gate

BRANCH
`feature/timeline-temporal-operational`

PRE-SCOPE
`6ca79a6e978d90c82961f6b7282b33332f86c34b`

CREATE
- `apps/backend/migrations/versions/20261014_146_b14_internal_session_execution_lifecycle.py`
- `docs/domain/decisions/activity-session-operational-lifecycle-v2.md`
- `docs/workstreams/timeline-temporal-operational-lifecycle-matrix.md`
- `packages/api-client/src/generated/model/retainedPlannedRow.zod.ts`
- `docs/workstreams/timeline-temporal-operational-lifecycle-write-gate.md`

UPDATE
- `apps/backend/src/dante/modules/temporal/activity_replan_api.py`
- `apps/backend/src/dante/modules/temporal/session_panel_api.py`
- `apps/backend/tests/integration/database/test_absolute_window_catalog.py`
- `apps/backend/tests/integration/database/test_current_catalog.py`
- `apps/backend/tests/integration/database/test_database_current_catalog.py`
- `apps/backend/tests/integration/database/test_migrations.py`
- `apps/backend/tests/integration/database/test_recurrence_reminder_catalog.py`
- `apps/backend/tests/integration/database/test_session_catalog.py`
- `apps/backend/tests/integration/database/test_temporal_constraint_catalog.py`
- `apps/backend/tests/integration/temporal/test_activity_replan.py`
- `apps/backend/tests/integration/temporal/test_planned_session_execution_link.py`
- `apps/backend/tests/test_activity_replan.py`
- `apps/backend/tests/test_session_panel.py`
- `apps/web/src/features/home/ui/timeline/activity-edit-panel.tsx`
- `apps/web/src/features/home/ui/timeline/activity-inspector-actions.test.tsx`
- `apps/web/src/features/temporal-create/application/activity-duplicate-seed.ts`
- `apps/web/src/features/temporal-create/application/temporal-create-quick-submit.test.ts`
- `apps/web/src/features/temporal-create/application/temporal-create-u2-submit.ts`
- `apps/web/src/features/temporal-create/ui/temporal-create-activity-fields.test.tsx`
- `apps/web/src/features/temporal-create/ui/temporal-create-advanced-activity-structure.tsx`
- `apps/web/src/features/temporal-create/ui/temporal-create-entry-authoring.test.tsx`
- `apps/web/src/features/temporal/activity-planned-sessions-card-detail.test.tsx`
- `apps/web/src/features/temporal/activity-planned-sessions-card-detail.tsx`
- `apps/web/src/features/temporal/activity-structure-readback.test.tsx`
- `apps/web/src/features/temporal/activity-structure-readback.tsx`
- `apps/web/src/features/temporal/remote-activity-edit-settings.ts`
- `docs/database/README.md`
- `docs/frontend/home/timeline-session-panel.md`
- `packages/api-client/openapi/dante-v1.openapi.json`
- `packages/api-client/src/generated/model/activityReplanCommand.zod.ts`
- `packages/api-client/src/generated/model/index.ts`
- `packages/api-client/src/generated/model/newPlannedRow.zod.ts`
- `packages/api-client/src/generated/model/temporalApplyActivityReplanBody.zod.ts`
- `packages/api-client/src/generated/model/temporalPreviewActivityReplanBody.zod.ts`

DELETE
None.

PURPOSE
Publish an explicitly incomplete lifecycle candidate: accepted product rules,
untimed named Session UI/API projection, early-start migration, panel timing,
updated contract and test coverage. PostgreSQL acceptance and the remaining
hard-deletion/review/edit-disposition capabilities are pending. This write does
not authorize UI acceptance or branch closure.

EXPLICITLY OUT OF SCOPE
Protected `main`, release/deployment, real user data, and any code path outside
the paths listed above.

## Local evidence before push

- `pytest -m 'not postgres'`: 628 passed, 372 deselected (proxy variables
  unset for the local transport).
- Web Vitest: 1055 passed / 225 files.
- Typecheck, targeted Ruff/Mypy/ESLint, filename and test integrity: passed.
- PostgreSQL 18/PostGIS and real browser: unavailable in this workspace.
