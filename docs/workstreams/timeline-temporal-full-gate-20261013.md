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

## 13 October, static recovery after d8914007 (pending verified rerun)

Local recovery `FULL_GATE_RECOVERY_LOGS.tar.gz` at exactly `d8914007db72334af0e86fdab821b2de0ad50dfb` confirmed Python formatting, Prettier, all-repo TypeScript, and focused midnight-clock Vitest GREEN; Ruff had 57 findings, mypy 421 across 67 files, ESLint 334 errors + 3 warnings. The formatter-only change committed 477 files on the feature branch. No 27-group full gate was rerun after that recovery.

Direct source repairs have now been published on this branch but **not yet validated**:

- mypy type inference: distinct typed variables for core-edit capture/reality/profile/reminder payloads and Objective create/revise/retire branches; covariant fingerprint Mapping; split heterogeneous Pydantic comprehensions and normalize replan date ranges to typed datetime spans.
- Ruff PT018: 16 logically equivalent independent assertions; PT011: four targeted validation-error message assertions; SIM117: two genuinely nested context managers combined; T201: 5 catalog prints replaced with identical stdout output.
- Ruff S608: five ACL/Responsibility test SQL strings now compose identifiers with `psycopg.sql.Identifier`; 11 source dynamic recurrence/responsibility SQL function names now select **explicit static SQL alternatives** for `routine/event` or `activity/event` rather than interpolating identifiers. Applied historical migration f-strings are not bulk-suppressed or rewritten; review remaining S608 individually and preserve DDL behavior.
- The single local follow-up is `bash tooling/testing/verify_static_repair_20261013.sh`: requires clean checkout, pulls, formats new Python/JS source fixes, gates generated drift and full TS, pushes only if those checks pass, then concurrently runs Ruff/mypy/ESLint and produces `temp/STATIC_REPAIR_LOGS.tar.gz` without rerunning PostgreSQL/browser E2E. Source changes may need refinements from this log; **do not claim a green full gate**.
