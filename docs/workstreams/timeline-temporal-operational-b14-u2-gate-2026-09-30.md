# B14/U2 — Canonical Quick Create local gate

- **Status:** CANDIDATE GATE — source implementation published; local generation/tests still required
- **Date:** 2026-09-30
- **Branch:** `feature/timeline-temporal-operational`
- **Persistence source head:** Alembic `20260930_94`
- **Pre-U2 proven catalog:** `_93` / `196|5|155|100|397|344|497|0|0|0`
- **CI:** forbidden for this gate; the user runs all commands locally

## Purpose

U2 turns the Home `+` Quick Create into a real canonical authoring path instead of a UI-only redesign. The gate proves one vertical chain:

```text
Quick Create draft
→ U2 authoring request
→ authenticated application layer
→ bounded PostgreSQL authoring functions
→ Activity/Event canonical descriptor
→ optional Life Area organization
→ accepted Schedule when placement is supplied
→ Timeline invalidation/read refresh
```

The following distinctions remain mandatory:

```text
Activity != Event
Life Area != Tag != Context
Occurrence != Schedule
Schedule != Session != Actual
planned/intended != happened
projection != canonical truth
```

## U2 contract under proof

- Life Area is optional for new Activity/Event; no assignment row is valid `unassigned` state.
- No synthetic `-`, `Personal` or fallback Life Area is created.
- New Life Areas staged in Quick Create are created atomically only when `Aggiungi` succeeds.
- Existing Life Area colour edits are revision-guarded; merely selecting an area does not create a colour revision.
- Without a Life Area, colour is a per-item override.
- `description` and `location` are canonical Activity/Event authoring metadata.
- Location is supported for both Activity and Event.
- Timed multi-day placement carries explicit start/end dates and times; no hidden end-time rollover.
- Quick Create uses the U2 authoring API only when the current intent is losslessly representable. Rich historical advanced intent remains on the established runtime until migrated; it is never silently discarded.
- Tag capability remains canonical B05 functionality but is intentionally outside Quick Create.

## Published implementation checkpoints

Backend / persistence:

- `865f458e` — U2 contract recorded.
- `48bb8d1e` — forward-only `_94` migration: optional organization and canonical authoring metadata.
- `73861f19` — Activity mapping.
- `4dee862b` — Event mapping.
- `61c4d5c5` — transactional `TemporalAuthoringApplication`.
- `32f01251` — PostgreSQL U2 proof.
- `bf80ea30` — public U2 authoring API.
- `680b267b` — FastAPI router registration.
- `a20731a9` — U2 API contract tests.

Web authoring / UI:

- `42ff23b4` — authoring data-source contract.
- `cabcc9a3` — strict remote U2 adapter.
- `db4716f6` — remote adapter wire tests.
- `0793aed9` — U2 authoring draft.
- `e15d94cf` / `649c355d` — controlled DANTE date picker.
- `289f5c7d` / `5eb741dc` — optional Life Area field.
- `b1b73f4b` — shared U2 draft.
- `a6b325e0` / `066c48f8` — U2 Quick Create core.
- `c508a3db` — shared draft across Create surfaces.
- `703eec28` / `d41afaa9` — explicit selected-vs-edited Life Area colour intent.
- `8043ce05` / `f4f69c81` — lossless U2 request mapper and tests.
- `93924cdd` — accepted Life Area appearance carried by Timeline group ViewModel.
- `1d3cabfe` — compatible Quick Create submit routed to canonical U2 authoring.
- `8a2c7393` — canonical Life Area colour/revision refreshed before authoring.
- `d059bc9f` — `Senza Life Area` treated as valid U2 organization state.
- `cc0204e6` — UI entry tests prove U2 Activity/Event authoring path.
- `792a82a2` — recurrence fallback test typing tightened.

## Generated contract rule

`packages/api-client/openapi/dante-v1.openapi.json` and `packages/api-client/src/generated/` are generated artifacts. They must **not** be edited manually.

Before U2 can be marked proven, regenerate them from the current backend:

```bash
pnpm api:generate
pnpm generated:check
```

Any resulting generated diff belongs in the U2 checkpoint and must be reviewed/committed after the local gate.

## Local gate

Run from the user worktree only.

```bash
cd ~/projects/dante
git pull --ff-only origin feature/timeline-temporal-operational

docker compose -f infra/compose/local.yaml up -d --wait postgres

cd apps/backend
uv run --locked alembic upgrade head
uv run --locked pytest -q --no-cov -x --tb=short -m postgres \
  tests/integration/temporal/test_b14_u2_authoring.py \
  tests/integration/temporal/test_b05_life_area_catalog.py \
  tests/integration/temporal/test_b05_primary_life_area_assignment.py \
  tests/integration/temporal/test_b05_secondary_tags.py \
  tests/integration/temporal/test_b03_event_lifecycle.py \
  tests/integration/database/test_current_catalog.py \
  tests/integration/database/test_database_current_catalog.py

uv run --locked pytest -q --no-cov -x --tb=short \
  tests/unit/temporal/test_b14_u2_authoring_api.py

cd ../..

pnpm api:generate
pnpm generated:check

pnpm --filter @dante/web typecheck
pnpm --filter @dante/web exec vitest run \
  src/features/temporal/remote-authoring-data-source.test.ts \
  src/features/temporal-create/application/temporal-create-u2-submit.test.ts \
  src/features/temporal-create/ui/temporal-create-entry-u2.test.tsx \
  src/features/temporal-create/ui/temporal-create-top-u1.test.tsx \
  src/features/temporal-create/ui/temporal-create-entry-u1.test.tsx \
  src/features/temporal-create/ui/temporal-create-composer.test.tsx \
  src/features/home/ui/home-create-interaction-bridge.test.tsx \
  src/features/home/ui/home-u1-create-layout.test.tsx

pnpm --filter @dante/api-client typecheck
```

If `pnpm api:generate` changes tracked generated files, inspect and commit those changes before declaring the public API/client chain closed.

## Manual product proof after automated gate

Use the real app and verify at least:

1. Activity with title only and no Life Area can be added.
2. Event with title only and no Life Area can be added.
3. Activity accepts location and description and they survive a reload/read path.
4. A new Life Area typed in Create does not exist before `Aggiungi`; after successful Add it exists and is assigned.
5. Selecting an existing Life Area inherits its accepted colour without revising it.
6. Changing the selected Life Area colour and adding performs the guarded revision.
7. No Life Area + chosen colour produces item-level appearance, not a fake Life Area.
8. Timed item can span different explicit start/end dates.
9. Date popover is DANTE-controlled and exposes no browser `Cancella` action.
10. Tags remain available in organization management but are absent from Quick Create.

## Closure rule

U2 is not marked `CLOSED / PROVEN` merely because source code exists. Closure requires:

```text
Alembic _94 applied
+ PostgreSQL/backend tests pass
+ OpenAPI/generated regenerated and clean
+ web typecheck/tests pass
+ real-app authoring proof passes
+ B14 ledger / Roadmap / Map / Handoff / DB Dictionary reconciled to the proven frontier
```

The next visual/UI iteration may proceed only after failures from this gate are either fixed or explicitly shown to be unrelated test-environment noise.
