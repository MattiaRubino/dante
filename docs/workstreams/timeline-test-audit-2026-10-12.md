# Audit dei test del branch Timeline — 12 ottobre 2026

## Perimetro ed evidenza

Riferimento remoto: `feature/timeline-temporal-operational` a `e78e1fa37017232bb0f36a0280a945fe2cc84694`, discendente di `main` (`981f6cf9ad985d0b811bc4172c12a7529fbc9b15`). Il confronto GitHub indica 2.841 commit sul branch, ma restituisce soltanto i primi 300 file cambiati: **non è una storia completa dei file cancellati**. L'inventario CSV allegato elenca i **491 file di test/contratto presenti ora** nel candidato: 489 file scoperti per nome/configurazione più due script di contratti prototype. Include le due nuove prove backend già pubblicate nel commit remoto. Non afferma che ogni file sia stato riesaminato semanticamente o eseguito.

Il checkout dell'assistente ha cronologia Git troncata; `git fetch` è impedito dal proxy dell'ambiente. Il runtime offre Python 3.12 e `uv 0.12.23`, mentre il backend richiede Python 3.14, `uv ==0.12.5` e PostgreSQL Docker 18.6. I browser Playwright non sono installati. Questi limiti sono **blocchi di esecuzione**, non PASS né motivi per disattivare i test.

## Inventario corrente

| Gruppo | File | Esecuzione in questo ambiente |
| --- | ---: | --- |
| Backend unità/contratti | 93 | Bloccata dal runtime Python/uv |
| Backend PostgreSQL/integration | 135 | Bloccata da Python/uv e Docker PostgreSQL |
| Web Vitest | 225 | 225 file verdi, 1.049 casi verdi dopo bonifica; snapshot iniziale 217/8 |
| Browser Web con fixture | 22 | 127 casi in 21 file più 2 casi Session panel; esecuzione bloccata |
| Browser Web stack reale | 8 | 87 casi scoperti in 8 file/progetti; esecuzione bloccata |
| Pacchetti api-client/i18n/time | 3 | 3 file verdi, 28 casi verdi |
| Tooling AI/observability | 3 | 29 casi verdi con runtime standard; ripetizione pytest WSL aperta |
| Contratti prototype | 2 | Entrambi verdi |

Vitest Web, eseguito **da `apps/web` con il suo `vitest.config.ts`**, ha prodotto `1.035 passed, 14 failed` su 1.049 casi. La prova iniziale dalla radice (`812 passed, 234 failed, 18 skipped`) è metodologicamente invalida per il Web: senza il config `jsdom`, molti test React falliscono con `document is not defined`. Non usare il comando root come gate globale. I browser non hanno eseguito test: il probe Playwright non ha avviato il `webServer` dopo la trasformazione Vite e manca anche Chromium; le liste sono solo discovery. I due contratti prototype sono passati con Python 3.12. Il tooling ha passato 19 casi `unittest` AI, 7 `unittest` observability e 3 funzioni `test_*` AI lanciate direttamente; il loro gruppo pytest resta da ripetere nel gate WSL.

## Quattordici test rossi: classificazione iniziale (ora risolti in Vitest)

| File | Casi | Evidenza e decisione |
| --- | ---: | --- |
| `timeline-create-bridge-b01.test.tsx` | 2 | Usa `loadUnplaced` e «Apri attività da collocare»; il componente attuale usa `TemporalPlanningTrayDataSource.listItems` e «Elementi già creati». **Contratto del test obsoleto**; riscrivere deduplicazione, refetch e errore di lettura sul percorso corrente. |
| `timeline-planning-tray-b02.test.tsx` | 5 | Stesso adapter/ingresso storico; preservare prova di collocazione, CAS, identità, invalidazione e rifiuto senza sostituirla con sole asserzioni di copy. |
| `timeline-schedule-unschedule-undo-b02.test.tsx` | 1 | Cerca il comando «Riporta nel Planning Tray» nella vecchia superficie. Verificare l'attuale destinazione e riprovare assenza autorevole/Undo. |
| `timeline-event-lifecycle-b03.test.tsx` | 1 | Attende uno stato Event che non compare dopo posticipazione. **Possibile regressione vera**; tracciare chiamata, readback e navigazione prima di cambiare l'atteso. |
| `activity-structure-readback.test.tsx` | 1 | Cerca «Finestra Activity». Verificare etichetta attuale, poi mantenere la prova di Schedule/figli letti senza creare Sessioni future. |
| `responsibility-controls.test.tsx` | 1 | Il test usa un `getByRole('alert')` singolo, ma sono presenti più alert. Scoprire se vi è un duplicato UI o un selettore fragile. |
| `temporal-create-enterprise.test.ts` | 1 | Attende che l'agenda Event elimini spazi e voci vuote, ma riceve i valori grezzi. Verificare la regola attuale tra preparazione, persistenza e lettura: possibile regressione di normalizzazione. |
| `temporal-create-activity-fields.test.tsx` | 2 | I controlli Session minimum e «Una sessione» non sono trovati. Verificare se sono stati trasferiti nell'attuale UI; la capacità e la precisione di un minuto non vanno perse. |

I primi otto casi nei tre file B01/B02 sono obsoleti **come harness UI**, non come comportamento richiesto. Gli altri sei rimangono da diagnosticare. Il PASS dei 1.035 casi non prova che le interazioni reali segnalate dall'utente funzionino: i bug su Edit, Play, ricorrenza, obiettivi e scrolling hanno attraversato i gate mirati precedenti.

## Gate integrale locale

`bash tooling/verify-all-current-tests-local.sh` esegue, con log indipendenti e senza fermarsi al primo errore, tutti i test backend non-PostgreSQL e PostgreSQL, tooling, due contratti prototype, tre pacchetti, Web Vitest, browser Session panel, browser con fixture e browser a stack reale. Comprende anche diff check, Ruff, mypy, lint, typecheck e verifica dei confini architetturali; registra SHA e impronta dell'intero candidato, e fallisce se il worktree cambia durante il giro. Il riepilogo contiene i codici di uscita e `LOG_DIR`. Usa il branch e lo stack locali preparati dall'utente; non genera API, non pulisce il worktree, non esegue CI e non pubblica. **Il gate non è ancora passato nel suo insieme**: si attendono l'esecuzione WSL e la correzione dei rossi già misurati. Per la futura regola “ogni modifica passa tutto”, il gate deve arrivare verde sullo stesso candidato; la documentazione precedente di PASS cumulativi su commit diversi non soddisfa questa regola nuova.

La prima ripetizione locale del Web aveva confermato `1.035 passed, 14 failed`. Dopo la migrazione dei test alla superficie attuale, il giro completo **sul worktree risultante** ha dato **225 file e 1.049 test verdi**. B01/B02 usano `TemporalPlanningTrayDataSource` e verificano identità, refetch, fallimento di scrittura e invalidazione; la UI deduplica una lettura che ripete la stessa identità. Undo Activity/Event usa il comando «Sposta in Da collocare» con conferma e controllo di lock. I due test dell'antico campo `minSessionMinutes` sono stati sostituiti con prove dei controlli attuali per intervalli e Sessioni pianificate, compresa precisione di un minuto; il test del modello di `minSessionMinutes` rimane separato. Agenda bozza e normalizzazione della richiesta canonica sono distinte e testate su entrambi i confini. Il PASS Vitest **non** prova PostgreSQL o browser reale.

`tsc --noEmit` per Web e api-client è verde; `dependency-cruise` ha trovato zero violazioni su 1.223 moduli e 3.483 dipendenze. Il lint diretto sull'intero repository (`eslint .`) ha rilevato **340 errori e 3 warning**, fra cui un errore di configurazione del project service su `apps/web/tests-browser/session-panel/session-panel.spec.ts`. Il lint diretto sugli otto test toccati mostra 27 errori preesistenti nei due file `activity-structure-readback.test.tsx` e `responsibility-controls.test.tsx`; non risultano nuovi errori negli altri test migrati. `pnpm typecheck` non è partito: questo ambiente ha pnpm 11.25.0 e il repository esige 11.22.0. I tre pacchetti hanno passato 28 test, i contratti prototype due script, AI/observability 26 casi `unittest`; i tre test Python scoperti solo come funzioni e il gruppo pytest tooling restano da ripetere in WSL. Non trasformare questo probe in un PASS o promettere che il comando integrale sia verde. La strategia/matrice corrente è `../development/temporal-regression-testing.md`.

Il debito lint è distribuito in 88 file. Le categorie principali del probe sono `no-base-to-string` (121), `require-await` (81), `no-unnecessary-type-assertion` (33), `no-unsafe-assignment` (22), `no-unsafe-member-access` (17) e `no-unused-vars` (13). Occorre distinguere correzioni meccaniche sicure, conversioni dei test fake e il problema di configurazione del test browser, poi ripetere il comando integrale: non sono 340 regressioni causate da questa bonifica.

## Architettura delle suite da stabilire dopo la bonifica

Organizzare per funzionalità e confine verificato, mantenendo un unico comando integrale: Create/Edit/Delete di Activity ed Event; collocazione, intervalli e ricorrenza; policy e ciclo Play/Pause/Stop delle Sessioni; Objective definizione/input/conferma/correzione; review storica e identità; Timeline geometria/scroll/mobile. Ogni scenario critico deve attraversare il dato salvato e letto di nuovo. Prove pure controllano invarianti e casi limite; PostgreSQL verifica owner/CAS, rollback, idempotenza, concorrenza e storia; browser a fixture verifica geometria e accessibilità; browser a stack reale verifica la sequenza Create → Edit → Start → Stop → Review dopo reload. Varie combinazioni (Sessione interna senza main, ricorrenza con Sessione senza orario, obiettivo quantità, passato, più intervalli, errori/retry) devono essere coperte tramite scenari nominati e dati condivisi, senza duplicare la logica applicativa nei test.

Prima di chiamare la suite “gate di regressione”, occorre: risolvere i 14 rossi senza indebolire invarianti; completare la raccolta backend e browser; mappare ogni comportamento attuale a prove di successo, rifiuto, persistenza e interazione; aggiungere i casi oggi mancanti; fare un giro completo verde **sullo stesso HEAD** e un walkthrough visivo reale. Un test che passa con sole mock non certifica il database o il browser.

Inventario dettagliato: `timeline-test-inventory-2026-10-12.csv`. `PASS/FAIL` nel CSV indica soltanto il gruppo eseguito qui e il runner indicato sopra; `BLOCKED_ENV` e `LISTED_NOT_RUN` restano non verificati.
