# Test di regressione Timeline e Temporal

Questa è la matrice funzionale Temporal della [verifica di tutto Dante](dante-verification-architecture.md); il gate e l'obbligo per ogni modifica valgono per l'intero repository.

- **Stato:** strategia corrente del candidato `feature/timeline-temporal-operational`; qualificazione integrale ancora aperta.
- **Perimetro:** Activity, Event, Routine/Recurrence/Occurrence, Schedule, Session, Actual, Objective, creazione, modifica, cancellazione, revisione e Timeline.
- **Evidenza iniziale:** `../workstreams/timeline-test-audit-2026-10-12.md` e relativo inventario CSV. La presenza di un file non equivale a copertura o PASS.

## Regola di accettazione

Ogni modifica a questo verticale richiede un test che fallisce sul difetto (o prova un comportamento nuovo), poi un giro completo di `bash tooling/verify-all-current-tests-local.sh` sul **medesimo candidato**, seguito dall'accettazione nella vera app per le interazioni visive. Il comando esegue anche test non Temporal: l'unificazione è nel gate, non in un file monolitico. Un gruppo rosso, non eseguito o bloccato lascia il gate aperto. Nessun PASS cumulato da commit diversi vale come PASS integrale. Non eliminare test rossi per rendere verde il comando: classificare obsolescenza dell'harness, contratto ancora valido, o difetto reale, e mantenere l'invariante nel test sostitutivo.

Il gate locale non avvia GitHub Actions. I test mirati possono abbreviare il ciclo di sviluppo, ma non sostituiscono il giro finale. Registrare SHA, stato del worktree, gruppo, conteggi, log, configurazione PostgreSQL/browser e risultato del walkthrough; un cambio di codice o di test successivo riapre il gate.

## Architettura

| Strato | Confine effettivamente verificato | Responsabilità e limiti |
| --- | --- | --- |
| Regole pure (pytest/Vitest) | Tempo, transizioni, identità, proiezione, geometria | Edge cases e invarianti con orologio/fuso deterministici; non prova persistenza. |
| Applicazione e contratti HTTP | Comando → autorizzazione → validazione → risposta; serializzazione API | Doppio invio, errore, replay, identità; fake solo ai confini esterni. |
| PostgreSQL 18.6 reale | Migrazione, vincoli, owner, revisione/CAS, transazione, storico | Rilettura da una nuova richiesta/connessione; concorrenti e rollback; non sostituibile con SQLite. |
| UI con fixture (Vitest + Playwright) | Componente, accessibilità, geometria, scroll, input, errori | Testare il DOM e il browser reale; le fixture non provano backend e DB. |
| Browser a stack reale | Utente → Web → API → PostgreSQL → reload | Pochi percorsi critici lunghi, isolamento per utente/dato, screenshot/trace in caso di errore; non rimpiazza le varianti ai livelli inferiori. |

Le classi di prova restano quelle di `testing-and-ci-v0.md`. Questa distribuzione segue i test *small/medium/large* descritti dal [Google Testing Blog](https://testing.googleblog.com/2010/12/test-sizes.html) e la preferenza per dipendenze vere dove servono [fedeltà](https://testing.googleblog.com/2024/02/increase-test-fidelity-by-avoiding-mocks.html). Per le sequenze di stati [Hypothesis stateful](https://hypothesis.readthedocs.io/en/latest/stateful.html) è una tecnica candidata: la dipendenza non è oggi nel `pyproject.toml` backend e va aggiunta esplicitamente prima di prometterne esecuzione. Per i browser valgono [isolamento e trace di Playwright](https://playwright.dev/docs/best-practices). Sono tecniche pubbliche adottabili, non un'affermazione di conoscere le suite interne di Apple, Meta, Amazon o OpenAI.

## Matrice funzionale obbligatoria

Per ogni riga servono almeno successo, input/ordine avverso, rifiuto senza scritture parziali e readback dopo reload, ai confini pertinenti. `PARZIALE` indica test esistenti, non copertura completa. `APERTO` è lavoro ancora da implementare o provare; non costruire un test che congeli un comportamento non deciso.

| ID | Scenario minimo e incroci che devono restare veri | Evidenza oggi / lacuna |
| --- | --- | --- |
| T01 | Create Activity semplice, Sessione principale on/off, intervalli multipli, Sessioni interne nominate senza orario autonomo, Schedule unplaced → colloca | PARZIALE: B01/B02, `temporal-create-u2-submit`, Planning Tray e UI attuale verdi in Vitest; combinazione ricorrente da provare nello stack. |
| T02 | Edit Activity salva dopo reload, campi e Sessioni esistenti, mutazione parziale rifiutata, policy Play aggiornata | PARZIALE: test Edit e card mirati; intero percorso Play dopo Edit APERTO. |
| T03 | Hard Delete Activity con cascata confermata: Objective e Reality policy polimorfici inclusi; per istanza ricorrente Solo questa crea skip e cancella solo il suo grafo, Tutta la serie cancella sorgente, istanze e grafi; unschedule/Undo preservano identità, CAS e storico pertinente; tray dopo refetch | CANDIDATO `_150`–`_155` e `_158`, regressioni PostgreSQL e Inspector scope; nuovo browser autenticato per eliminazione one-off, annullamento e rilettura. **Non eseguiti** sul nuovo head; ricorrenza in browser e verifica visiva APERTE. |
| T04 | Create/Edit/Postpone/Delete Event, data nel passato, Agenda, Undo, identità e Scope. Hard delete one-off, Solo questa istanza/Tutta la serie per Event ricorrenti; cancellazione grafo owner-only, isolamento fratelli, antirigenerazione, concorrenza/rollback/CAS; unschedule non distruttivo | CANDIDATO `_152`, `_156`–`_158` con regressioni PostgreSQL, Inspector scope/annullamento e browser autenticato one-off/cancel/reload; **non eseguiti** sul nuovo head. Ricorrenza in browser, passato/correzioni restano APERTI. |
| T05 | Ricorrenza: prima occorrenza, futuro, eccezione singola, intervalli, Sessioni interne senza orario autonomo, timezone/DST | PARZIALE: `_150` ammissione bloccata dopo skip e test PostgreSQL **non eseguito**; B06/M3 e prova PostgreSQL mirata Sessione untimed su `0e848943`; conversione in ricorrenza nell'Edit APERTA. |
| T06 | Play/Pausa/Riprendi/Stop sulla card e sul pannello, main e Sessione interna, ripetizione, errori/retry | PARZIALE: test Session e card; percorso reale incrociato APERTO. |
| T07 | Sessione conclusa: Stop non ripresenta Play, non altera Schedule, conserva tempo reale e minimo leggibile | PARZIALE: test realtà e geometria; screenshot e stack reale APERTI. |
| T08 | Edit/Move con tentativi reali richiede Mantieni/Elimina/Annulla; X della Sessione interna rimuove la configurazione e i tentativi al Salva; Hard Delete Activity confermata rimuove il grafo | PARZIALE: decisione attuale in `activity-session-operational-lifecycle-v2.md`; Keep, Delete, X e Hard Delete passano in PostgreSQL mirato su `0e848943`. Guard `_149` passato nel test PostgreSQL mirato su `cd3b589`; visibilità Sessioni mai avviate secondo il piano corrente candidata senza prova PostgreSQL/browser. Drag e ricorrenza APERTI. |
| T09 | Objective quantità (target richiesto), creazione/edizione atomica, input, conferma, correzione, policy automatica/esplicita | PARZIALE: M5/Objective; integrazione Create/Edit → review → reload APERTA. |
| T10 | Attività scaduta non avviata e Objective non confermato appaiono in `Da verificare`; negazione esplicita senza inventare Actual | PARZIALE: funzione PG/review; browser reale APERTO. |
| T11 | Timeline: eventi simultanei, Sessione anticipata, durata 1 minuto, colonne senza collisione, etichette, scroll su/giù, mobile/DST | PARZIALE: test di geometria e scroll mirati; browser visivo reale APERTO. |
| T12 | Concorrenza, owner diverso, replay identico/divergente, fallimento a metà, vecchia revisione e rollback | PARZIALE: suite PostgreSQL/contratti distribuita; mappatura per T01–T10 APERTA. |

I casi T01–T12 sono **traccianti**, non sinonimi di un numero di test o di una copertura già ottenuta. Ogni bug nuovo aggiorna la riga e aggiunge un caso preciso nel file funzionale più vicino, con almeno un'interazione pertinente (es. Edit → Play o Stop → reload → Play impedito). Una fixture che simula la risposta del server non può essere l'unica prova di un vincolo autoritativo. Per combinazioni troppo numerose, scegliere coppie e confini mirati; per ordini non banali, generare sequenze contro un modello indipendente, registrando seed ed esempio ridotto.

## Procedura di bonifica iniziale

1. Il CSV fotografa i file presenti; verificare raccolta e semantica di ciascun gruppo, compresi test B00 e test non Temporal che il branch porterebbe in `main`.
2. I 14 casi rossi Web iniziali sono stati migrati al datasource e all'interfaccia attuali: Vitest completo è verde (1.049/1.049). Restano aperti backend, browser e debito lint; un successivo FAIL funzionale resta FAIL finché il codice non viene riparato.
3. Eseguire il gate WSL completo con Python 3.14, uv bloccato, PostgreSQL 18.6 e browser installati. Conservare il riepilogo e i log, classificare ogni rosso. In questo ambiente i gruppi backend e browser restano `BLOCKED_ENV`.
4. Colmare T01–T12 con test di stato/invarianti e percorsi reali; includere una prova delle interazioni fra funzionalità, non soltanto schermate isolate. Ripetere il gate dopo ogni modifica fino a un risultato integralmente verde e fare walkthrough delle geometrie effettive.
5. Bonificare gli errori lint preesistenti emersi dal nuovo gate, senza eccezioni globali o disattivare le regole per ottenere un verde artificiale. `eslint .` diretto sul candidato rileva 340 errori e 3 warning, inclusa la configurazione project service del test browser Session panel; ripetere `pnpm lint` con pnpm 11.22.0 nel runtime canonico.

Non usare percentuali di coverage o quantità di test come surrogato della matrice: la prova deve fallire quando si reintroduce il bug e spiegare quale requisito protegge.
