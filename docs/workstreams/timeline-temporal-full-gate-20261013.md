# DANTE Timeline — full gate, 13 October 2026

## Verified checkpoint

- Branch: `feature/timeline-temporal-operational`
- Source-stable SHA: `23754d0d8b8267be799b0b6dd4d663f4f3542a1f`
- Complete gate: 27/27 groups, 20 green, 7 red, 721.6 seconds.
- PostgreSQL: **374 cases pass**. Shards 08 and 16 passed after isolated Docker infrastructure retries, with no skipped cases.
- Browser fixture and nonauthenticated browser: green.
- Manual Create/Advanced B14 browser hardening: green.
- Backend non-PostgreSQL, repository typecheck, build, generated drift, mobile bundle, API client tests, architecture, observability and i18n/time: green.

## The seven red groups

| Group | Grounded diagnostic |
| --- | --- |
| BACKEND_FORMAT | 245 Python files require Ruff formatting |
| BACKEND_RUFF | 120 errors; 63 default safe auto-fixes available |
| BACKEND_MYPY | 420 type errors in 67 files |
| REPO_FORMAT | 224 files require Prettier |
| REPO_ESLINT | 334 errors, 3 warnings; 37 auto-fixable |
| WEB_VITEST | 3 failing overnight/end-clock cases, 1051 passing tests |
| WEB_BROWSER_REAL_STACK | 6 failures of 87; database restart timeout creates 503 cascade, plus one fixture identity collision |

## Source repairs published after that gate

- `temporal-create-core-u2.tsx`: retain the explicitly authored End clock and advance its date by one day when Start crosses it, instead of altering End time. Requires focused Vitest confirmation.
- `access-auth.spec.ts`: the database stop/start helper uses the existing pinned backend venv interpreter when available and permits longer bounded Docker recovery. Still asserts real HTTP 503 and unauthenticated state.
- `temporal-runtime-foundation.spec.ts`: WebKit B00 uses exclusive synthetic identities 49–51, instead of colliding with Firefox Life Area (56) and Schedule forms (58).
- `tooling/testing/repair_full_gate_style.sh`: safe one-shot Ruff/ESLint edits and Ruff/Prettier formatting; verify both format gates, generated drift and repository typecheck before atomic commit/push; record remaining mypy/lint and focused Vitest results.

## Next step

On a clean local WSL checkout of the branch, pull the latest GitHub commits and execute:

```bash
bash tooling/testing/repair_full_gate_style.sh
```

The script writes `temp/FULL_GATE_REPAIR_LOGS.tar.gz`. Use its residual diagnostic logs to fix real typing and lint errors; **do not disable checks or declare the full gate green**. Run the unchanged complete parallel gate again only when the static backlog and functional failures are addressed.
