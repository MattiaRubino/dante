# Nomi e raccolta dei test Dante

> **Norma obbligatoria valida per tutto il repository:** [DANTE Test Engineering Standard](testing-standard.md). Il presente documento dettaglia denominazione e discovery: non è una policy isolata per la Timeline.

Il nome di un file di test indica **capacità e comportamento**. Il percorso indica il confine della prova (unit, database, integrazione, browser, contratto). Un codice di fase (`B05`, `B14-M2`, `CP6-M3`, `U2`, `M5`) rimane nei documenti storici e nelle revisioni Alembic, non nel nome di un test eseguibile.

Esempi:

| Confine | Prima | Dopo |
| --- | --- | --- |
| PostgreSQL | `test_cp6_m7.py` | `test_runtime_database_acl.py` |
| Temporal | `test_b14_u6_manual_session.py` | `test_retrospective_session_entry.py` |
| API | `test_b12_c_openapi_contract.py` | `test_plan_admission_openapi_contract.py` |
| Browser | `temporal-b03-event-core.spec.ts` | `event-create-read.spec.ts` |
| UI | `timeline-planning-tray-b02.test.tsx` | `timeline-planning-tray-placement.test.tsx` |

Regole per i prossimi file:

- usare il lessico del Domain e un comportamento riconoscibile, ad esempio `test_objective_definition_result_correction.py`; specificare `api`, `catalog`, `acl`, `integration` o `journey` quando separa prove della stessa capacità;
- non usare `whole_block`, `final`, `hostile` o il nome di una milestone **come unica informazione**: dire quale invariante è sottoposto a pressione;
- collocare i casi che condividono fixture e confine accanto alla capacità proprietaria. Non creare un unico file gigante per una verticale;
- il test `test_...` e la descrizione del caso devono spiegare input, azione, risultato e, per le regressioni, quale errore viene intercettato; un nome chiaro non dimostra automaticamente che l'assert sia valido;
- aggiornare i riferimenti eseguibili quando un file cambia nome. `tooling/check-test-file-names.py` blocca i nuovi identificativi di fase nel gate generale.

Il [registro delle rinomine](test-file-rename-map-2026-10-12.csv) mappa tutti i 180 file spostati senza cambiare i loro assert. I documenti di evidenza storica possono citare i percorsi di allora; il registro consente di trovare quello attuale. Gli script locali che invocano nomi espliciti sono stati aggiornati. Una rinomina non chiude alcun test rosso né certifica copertura semantica: la qualificazione dell'inventario e la correzione dei fallimenti rimangono attività distinte.

## Test-case registry and future edits

docs/development/test-case-registry.json is the repository-wide inventory
of executable test files. Each record has a suite boundary, provisional
contract family, candidate behavior inferred from its name, review status,
purpose and invariant. Every pre-existing test starts UNREVIEWED and must
not be presented as semantically qualified or passing. Review the accepted
Domain/Logical/Physical contract, test assertions, negative cases and
cross-feature interactions before setting QUALIFIED, with explicit
purpose and invariant. New tests must be registered and QUALIFIED in the
same change. All assertions and cases remain owned by their test files;
the registry is a durable index, not duplicated executable truth.

The TEST_INTEGRITY gate calls
python3 tooling/testing/verify_test_integrity.py and blocks unregistered
test files, stale cross-test imports, pytest_plugins references and old
script paths after renames. Cross-test fixtures should ultimately live
under support/ or conftest.py instead of depending on arbitrary test_*
modules. Test inventory PASS is structural only, never proof of behavior.
