# B14 live Session execution — user-local gate evidence (2026-10-10)

**Branch and verified source head:** `feature/timeline-temporal-operational` at `8097918df51fd6b890d86d0cd2eeaf3d6870c43d`, including Alembic `20261010_138`.  
**Method:** User pulled with `git pull --ff-only origin feature/timeline-temporal-operational`, then executed `bash tooling/verify-b14-session-live-repair-local.sh` in their WSL worktree. This is **user-reported local execution**, not GitHub CI or an assistant-executed test.  
**Local log directory:** `/tmp/dante-session-live-repair.aEjb42`.

## Results (exact user output)

| Gate | Exit code |
| --- | ---: |
| PY_SYNTAX | 0 |
| RUFF | 0 |
| POSTGRES | 0 |
| WEB_TYPECHECK | 0 |
| WEB_LINT | 0 |
| VITEST | 0 |
| BROWSER | 0 |

The prior full gate had also passed PY_UNIT, GENERATE, GENERATED_CHECK and API_TYPECHECK. Its failures (3 PostgreSQL cases, Web optional `visuals` type, one Vitest mock and browser 390px overflow) were addressed by `_138` and source/test/CSS fixes, and their **affected gates** were rerun above. The local verification is therefore **green for this candidate's technical acceptance**. This is **not yet real-app visual/user acceptance**. Preserve the distinction: no assertion of user-tested live Session workflows on their application data.

## Exact generated artifacts still local, intentionally not published

Generated OpenAPI/Orval output currently on user's WSL, as shown by `git status --short` after green gate:

- `packages/api-client/openapi/dante-v1.openapi.json`
- `packages/api-client/src/generated/dante.ts`
- `packages/api-client/src/generated/model/index.ts`
- `packages/api-client/src/generated/model/sessionPanelResponse.zod.ts`
- `packages/api-client/src/generated/model/sessionPanelPauseRange.zod.ts`
- `packages/api-client/src/generated/model/sessionPanelVisual.zod.ts`
- `packages/api-client/src/generated/model/temporalGetSessionPanelParams.zod.ts`

Exactly these **seven** local generated artifacts need publishing after the user pulls documentation-only updates. **No reset, clean, re-generation, CI or additional test rerun required** to publish them. Do not confuse these with the seven previously published **Draft Vault** generated artifacts, which are already on GitHub.

## Next: user-visible acceptance, not yet a closed workstream

Start the normal local authorized app stack with `export DANTE_E2E_CONTROL_ID=temporal-b08-d-usertest` and `uv run --project apps/backend python tooling/run-access-auth-stack.py`. Check real near-start preview (-5 minutes), arrival at start, overlapping Activities grouped, timing moved into/out of window, main-only Play, atomic main Pause/Stop across children, no automatic child Resume, independent child actions, ended/paused timing conservation, single Activity card adapting to reality while preserving planned coordinates, multi-day/multi-interval clipping, refresh and narrow-width behavior. Investigate any difference as a targeted follow-up, retaining historical data.

**Still open:** end-user visual acceptance, Event canonical Move-to-Bozze parity, any prior unaccepted M5/Bozze UI experience. Do not claim global B14/B15 closure from this technical proof.
