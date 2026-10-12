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
