# Architettura di verifica di tutto Dante

> **Norma obbligatoria:** [DANTE — Mandatory Test Engineering Standard](testing-standard.md). Questo documento specifica architettura e copertura; il documento normativo stabilisce procedure, collocazione, nomenclatura, obblighi e prova dell'esecuzione per qualsiasi contributo al monorepo.

- **Stato:** candidato del branch `feature/timeline-temporal-operational`, da qualificare sullo stesso SHA e nella vera app. Non è una dichiarazione che tutti i comportamenti siano già coperti.
- **Ambito:** tutto il repository e tutti i flussi implementati, dal Domain e dal Blueprint PostgreSQL alle migrazioni, al runtime, alle API, ai client, al Web, al mobile e alle dipendenze esterne.
- **Baseline backend:** [testing-and-ci-v0.md](testing-and-ci-v0.md). La matrice Temporal è un dettaglio funzionale in [temporal-regression-testing.md](temporal-regression-testing.md), non il perimetro del programma.

La convenzione dei nomi e la mappa dai vecchi file di fase ai test attuali sono in [test-naming-and-discovery.md](test-naming-and-discovery.md).
La prima esecuzione WSL del gate completo è registrata in [full-gate-baseline-2026-10-12.md](full-gate-baseline-2026-10-12.md): il suo risultato complessivo è rosso.

## Regola per ogni cambiamento

1. Identificare il contratto di prodotto e le autorità coinvolte: Domain/decisioni → Logical → Physical → Blueprint database → Dictionary → Alembic/SQLAlchemy → runtime/HTTP → OpenAPI/client → Web/mobile → effetto osservabile. Una freccia non implica che ogni funzione attraversi tutti gli strati; dichiarare quelli effettivi.
2. Scrivere una prova che fallisce prima della correzione, o una prova del nuovo requisito; includere un caso avverso e l'interazione con almeno un comportamento vicino quando la modifica può interferire. Associare il bug al contratto e al percorso di test. Per i dati: isolamento owner, transazione/rollback, ricarica e concorrenza dove pertinenti.
3. Eseguire i test mirati per iterare, quindi **tutti** i gruppi di `bash tooling/verify-all-current-tests-local.sh` sul medesimo candidato. Un gruppo rosso o bloccato lascia il gate complessivo aperto. Non rimuovere, saltare o indebolire un test per far diventare verde il riepilogo. Un test obsoleto va sostituito con la prova della regola attuale e con la motivazione della sostituzione.
4. Conservare SHA, fingerprint del worktree, versioni e configurazione, log per gruppo, esito funzionale e limiti. Un cambiamento successivo riapre il gate. Gli esiti cumulati di SHA diversi non costituiscono una prova integrale.
5. Se una superficie è visiva o dipende da servizi reali, aggiungere la relativa prova browser/dispositivo/provider e l'accettazione nella vera app. Non chiamare PASS complessivo un insieme di unit test verdi.

Il gate è locale, senza CI, pubblicazione o modifica Git. Il controllo `generated:check` rigenera gli artefatti in modo temporaneo, li confronta e ne ripristina lo snapshot; il fingerprint finale rileva modifiche residue. Lanciare il gate in un worktree dedicato o comunque senza edit concorrenti. I check che scrivono log o build temporanee restano separati dai sorgenti; se un processo lascia modifiche, `SOURCE_STABILITY` fallisce.

## Topologia delle prove

| Confine | Dove vivono le prove | Che cosa dimostrano e cosa resta separato |
| --- | --- | --- |
| Regole, modelli, applicazione | `apps/backend/tests/unit/`, `apps/backend/tests/test_*.py`, `apps/web/src/**/*.test.*`, `packages/*` | Stati, policy, validazione, errori e combinazioni locali; non simulare PostgreSQL per provare i suoi vincoli. |
| Persistenza e governance | `apps/backend/tests/integration/database/`, `apps/backend/tests/integration/`, `docs/database/dictionary/` | PostgreSQL 18.6 reale nel fixture isolato, provisioning, ruoli/ACL, migrazione fresh → head, oggetti e nomi esatti contro Dictionary, mapping SQLAlchemy e funzioni; i test storici di downgrade non provano da soli un upgrade da release precedente con dati. |
| API e contratti generati | test backend HTTP/OpenAPI, `tooling/check-generated.mjs`, `packages/api-client/` | Trasporto/permessi/errori, schema FastAPI → OpenAPI → client, determinismo e drift; typecheck e test client non provano la risposta di un backend reale. |
| Web e mobile | `apps/web/src/**/*.test.*`, `apps/web/e2e/`, `apps/web/tests-browser/`, `apps/mobile/` | Componenti e browser con fixture/stack reale, accessibilità, layout e scroll; per mobile oggi typecheck e export Android, non ancora una suite funzionale nativa equivalente. |
| Piattaforma e componenti trasversali | `tests/prototypes/`, `tooling/ai-evals/tests/`, `tooling/observability/tests/`, `tooling/observability/validate.py`, `infra/` | Architettura, osservabilità e contratti statici; provider, outage, restore e sicurezza richiedono prove specifiche quando applicabili. |

L'organizzazione è per confine e comportamento: test piccoli per varianti e invarianti; PostgreSQL reale per autorità dei dati; pochi percorsi lunghi Web → API → DB per le integrazioni; test di ambiente/provider e prove di rilascio per quanto non è fedele in locale. Gli stessi invarianti critici sono verificati attraverso più confini, senza duplicare ogni combinazione in ogni E2E. Fixture deterministiche, clock/fusi controllati, isolamento dei dati e tracce di errore riproducibili sono requisiti delle prove nuove.

## Registro di copertura per tutto il prodotto

Queste righe sono **famiglie da censire**, non una certificazione di copertura. Per ciascuna funzione implementata, collegare requisito, modelli, codice, migrazione/Dictionary se presente, prove positive/negative/incrociate ed evidenza di esecuzione. Un file presente indica soltanto che esiste una prova da valutare semanticamente.

| Famiglia | Contratti/incroci da censire | Stato iniziale |
| --- | --- | --- |
| Fondazione dati | Blueprint Parts 1–18, Domain/Logical/Physical, Dictionary scope e oggetti, SQLAlchemy, DAG Alembic, fresh → head, upgrade da schema con dati, rollback/backfill, ruoli e ACL, compatibilità | PARZIALE: test di catalogo/fixture migrata esistono; prova sistematica di upgrade da precedente release e riconciliazione semantica di tutti i contratti aperta. |
| Accesso e identità | Account/principal, auth email/provider/passkey, sessione autenticata, autorizzazione, isolamento, privacy, rate/errori | PARZIALE: test backend e Playwright `auth/`; inventario semantico dei casi e prova finale aperti. |
| Temporal e Home | Activity, Event, Routine/Recurrence/Occurrence, Schedule, Session, Actual, Outcome/Confirmation, Objective, Life Area/Tag, pianificazione, Timeline, review e tutte le interazioni Create/Edit/Delete | PARZIALE: matrice T01–T12 nel documento Temporal; bug reali e policy storiche ancora aperti. |
| World/Focus e navigazione | Workspace, contesto, continuità, app shell, accessibilità, composizione con Temporal e autenticazione | PARZIALE: test browser e unit già presenti; flussi integrati da censire. |
| Intelligenza, ricerca e provider | Model access, policy/egress, retrieval, pubblicazione/evidenza, eval, errori, timeout, costi/limiti, isolamento | PARZIALE: test unit/tooling esistono; prove reali di provider richiedono ambiente non produttivo e inventario dedicato. |
| Servizi trasversali | Email, osservabilità/telemetria, recovery, configurazione, tempo e i18n, infrastruttura, build, compatibilità delle dipendenze | PARZIALE: test e verificatori statici esistono; outage/restore e contratti esterni vanno evidenziati separatamente. |
| Client/dispositivi | Web, pacchetti condivisi, API client generato e mobile; responsive, tastiera, screen reader, Android/iOS e stabilità delle build | PARZIALE: Web, package test, browser e bundle Android; test mobile nativi, dispositivo e iOS non ancora dimostrati dal gate. |

Per ogni famiglia la matrice crescerà in scenari versionati, con stato `PASS sullo SHA`, `FAIL`, `BLOCKED_ENV`, `NOT_RUN` o `NON_APPLICABILE` motivato. La classificazione va fatta per requisito, non per cartella o conteggio. I cambi trasversali (identità, tempo, API, schema, componenti condivisi) richiedono anche percorsi incrociati fra famiglie.

## Gate locale e prove specialistiche

Il comando unico esegue qualità Python/TS, formattazione, lint, architettura, generazione/drift, build Web/pacchetti, bundle Android, contratti statici osservabilità, backend unit e integrazione PostgreSQL, eval/tooling, contratti prototipo, package test, Web Vitest e tre configurazioni Playwright. Il gruppo `BACKEND_POSTGRES` comprende i test esistenti di catalogo e migrazioni attraverso database isolato; il suo PASS non autorizza ad affermare che tutti gli scenari di upgrade storici siano coperti. Consultare i log nominati nel riepilogo per il numero dei casi eseguiti e gli skip.

Restano prove **esplicitamente fuori dal gate automatico corrente** finché non esistono harness ripetibili e ambienti sicuri: upgrade da precedente release popolata, recovery/restore, outage collector end to end, provider esterni reali, sicurezza offensiva, performance/scale, accessibilità manuale, iOS e veri device Android, oltre al registro Physical post-selection validation. Per ciascuna, aggiungere scenario, dati sintetici, esecutore, ambiente, comando, evidenza e criterio di uscita; se è obbligatoria per il cambiamento/rilascio, l'esito `NOT_RUN` blocca l'accettazione di quel cambiamento/rilascio. Non invocare script che scrivono su provider o ambienti condivisi nel gate locale senza isolamento e mandato esplicito.

## Avanzamento controllabile

1. Qualificare ogni test esistente: raccolta, regola ancora valida, dipendenza ambientale, ridondanza, flakiness e difetto reale; conservare un registro dei casi mancanti per tutte le famiglie. L'inventario Temporal del 2026-10-12 è solo il primo campione, non un audit completo di Dante.
2. Bonificare i rossi esistenti del gate, inclusi gli errori ESLint già osservati; eseguire in WSL il gate esteso e registrare anche gruppi bloccati. Le nuove righe introdotte qui non sono ancora state eseguite sul sistema dell'utente.
3. Per ogni fix/funzionalità, ampliare la matrice della famiglia proprietaria e un caso di integrazione adiacente, poi fare il giro completo sul medesimo candidato.
4. Aggiungere harness specialistici solo quando il relativo contratto/ambiente è definito, mantenendo separati prova tecnica, accettazione visiva e integrazione su `main`.

## Structural integrity and browser isolation

The repository-wide registry (docs/development/test-case-registry.json)
tracks test location, owning suite, provisional contract and review
status. Existing files have UNREVIEWED status and no inferred qualified
semantics. TEST_INTEGRITY checks discovery, obsolete imports/plugins,
mypy override names and executable shell script references. A rename
updates all consumers, the registry and current documentation together.

Real-stack Playwright now starts through
tooling/testing/run_real_stack_playwright.py, selecting a free loopback
HTTPS port and propagating DANTE_E2E_WEB_PORT into the browser and the
Auth/Vite stack, without terminating or adopting the developer's 4173
service. Port binding still has a possible race; such a failure remains
environmental until separately diagnosed. The full gate and any user
real-app acceptance must be rerun on the new commit; existing REDs are
not certified by this structural refactor.
