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
