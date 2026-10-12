# Gate integrale: prima esecuzione WSL del 12 ottobre 2026

**Candidato:** `438a3d9f5bffda0ec9bd2da4ec12c574e6a7801b`, worktree pulito nel resoconto dell'utente. Log locali: `/tmp/dante-all-tests.XCEzq8` sul sistema WSL dell'utente. Questo è un riepilogo del terminale allegato, non una nuova esecuzione e non l'analisi completa dei file di log. La rinomina successiva dei test non trasforma questi fallimenti in PASS.

| Gruppo | Risultato riportato | Prima classificazione |
| --- | --- | --- |
| DIFF_CHECK, REPO_TYPECHECK, ARCHITECTURE, GENERATED_DRIFT, REPO_BUILD, MOBILE_BUNDLE, OBSERVABILITY_STATIC | 0 | PASS su quel candidato. |
| EVAL_TOOLING, FRONTEND_PROTOTYPE_CONTRACT, WORLD_PROTOTYPE_CONTRACT, API_CLIENT_TESTS, I18N_TESTS, TIME_TESTS, WEB_VITEST, WEB_BROWSER_FIXTURE | 0 | PASS su quel candidato; Vitest include tutti i test correnti. |
| BACKEND_FORMAT | 1 | 237 file da formattare; debito di baseline da qualificare, senza riformattare migrazioni storiche byte-stable. |
| BACKEND_RUFF | 1 | 122 errori; diagnosticare per file/regola e distinguere problemi reali da fixture. |
| BACKEND_MYPY | 1 | 196 errori in 24 file; il frammento mostra errori nel replan Activity. |
| REPO_FORMAT | 1 | 214 file segnalati da Prettier. |
| REPO_ESLINT | 1 | 340 errori e 3 warning, inclusi i due file del browser Session panel fuori dal project service. |
| BACKEND_NON_POSTGRES | 1 | 613 passed, 8 failed; i fallimenti includono Dictionary scope, contratti API e allowlist della dipendenza `ortools`. Non classificarli tutti come vecchi test senza prova. |
| BACKEND_POSTGRES | 1 | 155 passed, 23 failed, 192 errors; i test migration/catalog e runtime sono coinvolti. Il riepilogo non dimostra che siano 215 difetti indipendenti: serve il primo traceback causale nei log WSL. |
| OBSERVABILITY_TOOLING | 2 | Collection error `ModuleNotFoundError: tooling` dal comando in root. Il gate successivo imposta `PYTHONPATH=.` per rendere importabile il package; verifica WSL ancora necessaria. |
| WEB_BROWSER_NONAUTH | 1 | 111 passed, 16 failed; i singoli trace e il primo errore server/browser nei log vanno esaminati. |
| WEB_BROWSER_REAL_STACK | 1 | Porta HTTPS `127.0.0.1:4173` già occupata; il percorso reale non è stato eseguito. Liberare/identificare il processo prima del rerun, senza attribuire il FAIL alle feature. |
| SOURCE_STABILITY | 0 | Nessuna modifica residua al worktree per quel giro. |

Il gate resta **ROSSO**. La priorità di diagnosi è il primo errore causale PostgreSQL, poi i singoli otto test non PostgreSQL, i trace browser e il port conflict; formattazione/lint/typecheck vanno bonificati senza silenziare i controlli. Ogni modifica deve attraversare il gate integrale sullo stesso nuovo candidato. Gli esiti PASS precedenti restano evidenza storica sul proprio SHA.

## Gate 181c5804 — user WSL evidence (12 October 2026)

Candidate: 181c58049c95d4914987a9c22f1d2cd6bc3c2f17. The attached
user terminal output reports a clean worktree and logs at
/tmp/dante-all-tests.xrLSaV (on the user's WSL machine). This is reported
evidence, not a new execution or an examination of individual trace files.

The naming checker reports 489 passing test filenames. Both
BACKEND_NON_POSTGRES and BACKEND_POSTGRES stop at collection with 63 errors.
Current sources include imports and pytest_plugins still referencing test
modules renamed in the earlier 180-file migration. The structural repair
requires new local collection and full gate proof, not automatic PASS.

Quality gates: BACKEND_FORMAT 237 files; BACKEND_RUFF 122 errors;
BACKEND_MYPY 196 errors in 24 files; REPO_FORMAT 214 files;
REPO_ESLINT 340 errors and 3 warnings. Web non-auth Playwright:
111 passed, 16 failed. Web real-stack: blocked by occupied HTTPS port 4173.
Pass on this candidate: diff/stability, repository typecheck, architecture,
generated drift, build, Android bundle, observability static and tooling,
AI eval tooling, prototype contracts, package tests, Web Vitest and browser
Session Panel. Full outcome: RED. Keep all functional failures open.

## Gate abfaa5b2 — second WSL run, 12 October 2026 (reported evidence)

The user executed the full gate after pulling `abfaa5b2`, before the
mandatory standard commit `18d44ea8`. Evidence is the user-provided shell
output and `/tmp/dante-all-tests.lJYgFd` on their WSL computer; full
individual logs are not accessible through this report.

- `TEST_FILE_NAMES`: PASS; `TEST_INTEGRITY`: FAIL with remaining old
  Python module references in **20** Temporal test files. Both PostgreSQL
  and non-PostgreSQL pytest groups fail collection on those same 20 files;
  the earlier import repair was incomplete.
- `BACKEND_FORMAT`: 237 files; `BACKEND_RUFF`: 125 errors.
  `BACKEND_MYPY`: 702 errors in 84 files after expansion of the scan to
  `src tests tooling` (not evidence of 702 newly introduced application bugs).
- `REPO_FORMAT`: 214 files; `REPO_ESLINT`: 338 errors and 3 warnings.
  `REPO_TYPECHECK`, architecture, generated drift, build and Android
  bundle: PASS.
- Static observability, eval and observability tooling, prototypes, package
  tests, Web Vitest and browser Session Panel: PASS.
- Non-auth browser: 111 PASS, 16 FAIL (4.3 minutes), including Temporal
  Create, planning-tray and timeline interaction scenarios.
- The pasted output ends at `RUN WEB_BROWSER_REAL_STACK`; **no result for
  that group or final SOURCE_STABILITY may be inferred** from it.

**Full outcome RED.** A later commit correcting 20 old-module imports
does not itself prove collection or the other quality/browser groups PASS.
Require a fresh local `pytest --collect-only` preflight and the full gate on
the new SHA. Do not disable mypy/ESLint/formatting failures to achieve green.

## Gate 697bcd2f — PostgreSQL cascade diagnosed (user WSL, 12 October 2026)

The WSL `pytest --collect-only` preflight succeeded (**990 tests in
3.55 seconds**); structural integrity and test naming passed. The full
candidate remained **RED**. Non-PostgreSQL backend: **613 passed, 8 failed,
369 deselected**. The real PostgreSQL group finished after **360.99 seconds**
with **138 passed, 21 failed, 211 errors, 621 deselected**.

The user supplied the initial error stack and frequency count from
`/tmp/dante-all-tests.Athu1R/BACKEND_POSTGRES.log` (WSL-local):
**211 errors share one** `psycopg.OperationalError` for the previous
disposable cluster endpoint `127.0.0.1:55332` (`Connection refused`).
The first traceback is teardown of
`test_liveness_survives_database_outage_and_readiness_recovers_without_app_restart`.
The session-scoped PostgreSQL fixture shares a Docker container between
tests; the outage test calls `stop()`/`start()` and the fixture previously
published port `127.0.0.1::5432`, which may not survive restart with
the same host mapping. Treat this as a **single infrastructure failure with
cascading errors**, not 211 independent product defects. Root cause
(port remapping versus another restart failure) requires the next focused
local test to confirm; the harness now explicitly pins and checks the
host port and fails early on an unrecoverable outage.

Separate deterministic drift: historical
`test_migrations.py` still expected Alembic `20260917_29` whereas
the candidate's verified head is `20261011_142`. The latest migration
deliberately refuses downgrade (`Owner-only derived review queue is
forward-only`). The corrective tests retain legacy rollback-guard
probes at the **historical reversible head** and independently verify the
**current forward-only** contract and current head. Do not remove
historical downgrade guards, nor weaken canonical forward-only migrations.

This evidence **does not** close the remaining 21 PostgreSQL assertions,
8 non-PostgreSQL failures, Ruff/mypy/format/ESLint debt, browser
failures or unobserved real-stack result. Next first run the focused
`test_runtime.py` outage/recovery tests and the Alembic head/current
forward-only tests, then all PostgreSQL cases and ultimately the complete
same-SHA gate; preserve distinct failures.

## Focused outage/Alembic repair validation on 88ecdac7 — user WSL (12 October 2026)

User-provided terminal output on active branch at
`88ecdac73bd0e3f212ea3dc13d99678229f36272`, Python 3.14.7 /
pytest 9.1.1 / WSL, with `uv run --locked pytest -vv -x --no-cov --tb=short`:

- PostgreSQL outage/readiness recovery and current catalog:
  `test_liveness_survives_database_outage_and_readiness_recovers_without_app_restart`,
  `test_readiness_response_never_exposes_database_details`,
  `test_current_catalog_matches_dictionary_sqlalchemy_and_alembic`.
  **3 passed in 21.55 s**.
- Alembic fresh-to-head, current forward-only guard and historical
  reversible-head round trip:
  `test_fresh_database_reaches_the_single_repository_head`,
  `test_current_repository_head_refuses_downgrade_by_design`,
  `test_historical_reversible_head_round_trips_to_base_and_back`.
  **3 passed in 9.80 s**.

These **six scoped checks PASS**, supporting the outage recovery fix and
the current-versus-historical migration test split. They do **not** prove
that all PostgreSQL tests pass in sequence or that the remaining
non-PostgreSQL, static quality and browser gates are resolved.
Next: run the entire PostgreSQL-marked suite on an identical candidate,
record first-cause failures and then re-run the full monorepo gate.

## Full PostgreSQL suite on c512854a — user WSL (12 October 2026)

The user ran `uv run --locked pytest -v --no-cov --tb=short
--durations=20 -m postgres` on
`c512854a071321ded3f2ecbe28141cc87565644c`, Python 3.14.7,
pytest 9.1.1, real PostgreSQL 18.6 via disposable Docker fixture.
Exact WSL log: `/tmp/dante-postgres-full.6Ciak9.log`.

**Collected 991; 370 PostgreSQL selected, 621 deselected; 350 passed,
20 failed, zero fixture errors, 777.54 seconds (12:57).**
Both database-outage tests passed **in sequence**, proving the previously
observed 211-error infrastructure cascade no longer occurs.

Twenty independent *test cases*, but fewer shared causes:
- Six B04/B08/B11 catalog probes expected obsolete September Alembic
  HEADs although they use the fresh **current** `migrated_database`;
  the candidate update targets its new head and preserves stage-specific
  tests separately.
- Four B12 Plan cases failed together with `NoSuchColumnError: starts_at`;
  the SELECT lacked the two named `COALESCE` projection aliases.
- Three B06/B14 Routine authoring/replay cases failed from the same
  ambiguous PL/pgSQL `routine_ref` output-vs-column reference, requiring
  a **forward-only Alembic function correction**, not just a Python change.
- Two CP6 Dictionary probes compare evolving cumulative Dictionary
  trigger lists against immutable M5/M6 stage counts; stage-catalog
  snapshots must be explicitly scoped.
- One B04 mapping probe excludes the later duration subtype; one
  historical CP6 concurrency probe hits current narrowed runtime ACL
  (`42501`) rather than validating the original stage ACL.
- One B08 workflow test still assumes Stop while paused is forbidden;
  one B03 Event test rejects a supported coarse-local-period Schedule.
- **Unresolved schema/metadata drift**: the Alembic `command.check`
  test reported extensive differences (CHECK names, defaults,
  foreign keys, indexes, nullable fields, uniqueness). This is **real
  failing evidence**, not an acceptable harmless baseline or permission
  to disable the check. Independently reconcile against the physical
  Dictionary and migration contract.

Corrections after this SHA are **UNVERIFIED** until the corresponding
scoped user-local PostgreSQL runs complete. The global gate also retains
prior failures in non-PostgreSQL pytest, Ruff, mypy, formatting, ESLint,
Web Playwright and real-stack acceptance. No all-green certification.

## Scoped PostgreSQL regression verification — 0ddb2583, user WSL (12 October 2026)

The user pulled `0ddb2583fa0af303f0cd9c2a8bb37f0cbed164b3`.
`python3 tooling/testing/verify_test_integrity.py` reported
`REGISTERED=491 DISCOVERED=491 UNREVIEWED=491` and **PASS**
(structural inventory and executable-reference integrity; *not* test
semantic qualification).

The real WSL command `uv run --locked pytest -v -x --no-cov --tb=short`
ran seven selected PostgreSQL tests. **7 passed in 20.79s**:

- `test_migrations.py`: fresh database reaches current head; current
  `20261012_143` is forward-only; prior `20261011_142` review-queue
  forward-only guard independently remains enforced (3 cases).
- `test_routine_core.py`: Routine lifecycle / primary Life Area / replay.
- `test_plan_conflict.py`: B12-A current conflict read / prerequisite.
- `test_session_workflow.py`: unplaced Activity Session pause/resume,
  TC009 independence.
- `test_shared_schedule_event.py`: invalid schedule atomicity and valid
  coarse-local-period Event acceptance.

**Interpretation:** the new Routine migration, Plan projection, historical
migration guard separation and changed Session/Event behaviors are validated
for these *scoped* cases. Prior baseline remains **20 failed / 350 passed**
until *all 20* are rerun, particularly catalog stage tests, 3 remaining Plan
cases, 2 remaining Routine cases, CP6 concurrency, and Alembic autogenerate
metadata drift. The complete monorepo gate is still **RED**. All 491
existing registry files remain **UNREVIEWED**; a green structural check
does not certify semantic coverage.

## Re-run of prior PostgreSQL failures on 7af29c89 — user WSL (12 October 2026)

The user pulled `7af29c8923d631fa0571209259c1451f15035661`
(documentation-only update from `0ddb2583`) and selected **19** of the
previous **20** failing PostgreSQL tests from
`/tmp/dante-postgres-full.6Ciak9.log`, excluding only the known Alembic
`command.check` metadata drift. Re-run evidence:
`/tmp/dante-regressions.A475mj.log`, Python 3.14.7,
`pytest -vv --no-cov --tb=short --durations=10`.
**14 passed, 5 failed in 39.88 seconds**.

The remaining five defects were classified from exact exceptions:
- `test_b04_e_duration_catalog_and_acl`: *current* schema
  `238|5|228|103|486|421|596|0|0|0` compared against *historical*
  B04-E topology `158|5|109|93|303|254|433|0|0|0`.
- `test_b04_d_revision_and_topology`: current schema compared against
  historical B04-D topology `145|5|87|92|285|223|408|0|0|0`.
- `test_m6_dictionary_reconciles_final_structural_surface`:
  `psycopg.errors.SyntaxError` because SQL used reserved word
  `constraint` as a table alias in the new historical-catalog query.
- `test_b08_session_catalog_reuses_cp6_and_adds_bounded_subject_capabilities`:
  exact Session source-edge set omitted the legitimate later B14
  `session_manual_record_operation` retrospective record.
- `test_b04_catalog_surface_and_live_topology`: historic B04-A/C table
  set omitted the subsequently accepted B04-E
  `temporal_constraint_duration_state`, while the probe used a
  *current* `migrated_database`.

Correction strategy **retains historical contracts**: migration-stage
snapshot tests run against `provisioned_database` upgraded to their
accepted exact historical revisions, instead of weakening baseline
numbers or blindly using the current counts. Current catalog and
current least-privilege ACL tests continue to exercise the current
head separately. SQL alias and Session exact-edge corrections retain
their other assertions. These changes are not user-locally verified
until a new targeted test run.

**Global and PostgreSQL gates are still RED**; the earlier excluded
Alembic/SQLAlchemy schema metadata drift remains unaddressed.

## Five remaining catalog regressions — 5018c36d, user WSL (12 October 2026)

The user pulled `5018c36d61dfcc3b0c8b47b6ba617baa53270b5c`
and reran the exact five previously failing PostgreSQL catalog cases
with `uv run --locked pytest -vv --no-cov --tb=short --durations=10`.
**5 passed in 10.93 seconds**:

- B04-E duration catalog/ACL at accepted historical revision.
- B04-D movement-policy historical topology.
- CP6-M06 structural Dictionary/catalog snapshot.
- B08 current Session catalog, including the manual-record receipt.
- B04 historical temporal-constraint catalog snapshot.

The previous **14** of **19** targeted regressions passed on `7af29c89`,
and the final five passed after corrective commit `5018c36d`.
**This is staggered, scoped regression evidence, not an entire 19-case
single-revision run nor an entire PostgreSQL suite PASS.**

Outstanding known PostgreSQL blocker:
`test_alembic_check_reports_no_dante_schema_drift_with_extensions_present`,
which compares fresh migrated physical DANTE schema against registered
SQLAlchemy metadata using Alembic autogenerate with
`compare_type=True` and `compare_server_default=True`. This check
remains enabled and **RED** pending exact-diff diagnosis and
Dictionary-grounded correction. Other monorepo test/quality gates
remain open as documented above.

## Complete one-SHA gate — ee2ed0fa, user WSL (12 October 2026)

Full original evidence supplied by the user: `FULL_GATE_LOGS.tar.gz`
(27 group logs and CONSOLE.log), `FULL_GATE_SUMMARY.md`, and terminal
output. Authoritative candidate
`ee2ed0fabd32f5a6b8ce1fc2b89d63b41a6cda93`; tree fingerprint
`e3b0c442...` before and after; worktree remained clean.
**27/27 groups executed, 18 PASS, 9 FAIL; global gate RED.**

- PostgreSQL **369 passed / 2 failed / 621 deselected**, 774.40 seconds:
  the historical-head test
  `test_database_current_catalog.py` still asserts
  `20261011_142` instead of head `20261012_143`; independent
  `test_migrations.py::test_alembic_check_reports_no_dante_schema_drift_with_extensions_present`
  reports autogenerate schema/ORM differences (CHECK constraint
  expressions/naming, 26 foreign keys, index/unique constraints,
  seven defaults and two nullabilities). **Do not suppress autogenerate.**
- Backend non-PostgreSQL **613 passed / 8 failed**: Dictionary
  `completed_stages` schema frozen at 40 while scope has 61;
  Occurrence-window API test injects stale `application` instead
  of `materialization`; Session HTTP inventory omits planned name
  and Session Panel; Tag mapping inventory still hard-codes 135 instead
  of comparing against all 238 current Dictionary tables; Temporal
  OpenAPI manual exact inventory lacks 44 post-baseline routes;
  two existing-Schedule response tests omit intentionally nullable
  Life Area fields; runtime dependency allowlist omits `ortools`.
- Backend formatting: **242** files; Ruff: **132** errors;
  mypy: **678** errors across 77 files. Repository Prettier:
  **214** files; ESLint: **338 errors / 3 warnings**, including
  a missing Playwright session-panel config from the TS project service.
  These are real failed quality gates, not PASS or authorization to
  disable the tools.
- Non-auth browser: **111 passed / 16 failed**. The log shows
  multiple legacy `getByLabel('Ora').fill(...)` selectors now
  resolving to several buttons instead of a text input, mismatched
  Advanced Create/Planning Tray semantics and a Timeline focus
  interaction failure. Proxy attempts to `127.0.0.1:8000` were
  refused during non-auth fixture runs. Diagnose per intended test
  boundary; do not simply remove failing cases.
- Real-stack browser: **74 failed / 10 passed / 3 skipped**
  in approximately **59.3 minutes**. Repeated initial login helper
  waits for a no-longer-detected `Continua` control and eventually
  times out before an auth request. Browser video/screenshot/trace
  artifacts were not included in this log archive, so the exact
  rendered page and root condition **cannot yet be established**.
  Must validate real HTTPS/FastAPI/PostgreSQL spine, not replace with
  fixture UI.
- All other checks, including source stability, test discovery,
  generated client drift, package unit suites, architecture/typecheck,
  build, mobile bundle, eval/observability/prototype contracts and
  fixture browser, passed for **ee2ed0fa only**.

After this report the scoped corrective batch aligns Dictionary stage
schema, current database head, several transport/inventory response
contracts, admitted runtime dependencies, and TS config. Those edits
remain **UNVERIFIED** until the whole same-SHA gate completes; the
entire metadata drift, the 44-API inventory, browser failures and
large quality backlog remain OPEN.
