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
| T02 | Edit Activity salva dopo reload, campi e Sessioni esistenti, mutazione parziale rifiutata, policy Play aggiornata; **Save senza modifiche non scrive**, l'errore 422 non espone testo framework, e la cancellazione di un risultato non perde draft non salvati | PARZIALE: test Edit/card e nuove regressioni jsdom/remote no-op, 422, cancel/retry e draft isolation; nuova esecuzione Vitest e walkthrough reale APERTI. |
| T03 | Hard Delete Activity con cascata confermata: Objective e Reality policy polimorfici inclusi; per istanza ricorrente Solo questa crea skip e cancella solo il suo grafo, Tutta la serie cancella sorgente, istanze e grafi; unschedule/Undo preservano identità, CAS e storico pertinente; tray dopo refetch | CANDIDATO `_150`–`_155` e `_158`, regressioni PostgreSQL e Inspector scope; nuovo browser autenticato per eliminazione one-off, annullamento e rilettura. **Non eseguiti** sul nuovo head; ricorrenza in browser e verifica visiva APERTE. |
| T04 | Create/Edit/Postpone/Delete Event, data nel passato, Agenda, Undo, identità e Scope. Hard delete one-off, Solo questa istanza/Tutta la serie per Event ricorrenti; cancellazione grafo owner-only, isolamento fratelli, antirigenerazione, concorrenza/rollback/CAS; unschedule non distruttivo | CANDIDATO `_152`, `_156`–`_158` con regressioni PostgreSQL, Inspector scope/annullamento e browser autenticato one-off/cancel/reload; **non eseguiti** sul nuovo head. Ricorrenza in browser, passato/correzioni restano APERTI. |
| T05 | Ricorrenza: prima occorrenza, futuro, eccezione singola, intervalli, Sessioni interne senza orario autonomo, timezone/DST; conversione one-off→serie e **prima istanza fisica** senza duplicati, più Schedule distinti per più intervalli di una Activity | PARZIALE: prove pregresse B06/M3 e Session untimed; nuovi P3 E2E e protezioni scope candidate ma non ancora eseguite sul nuovo SHA. |
| T06 | Play/Pausa/Riprendi/Stop sulla card e sul pannello, main e Sessione interna, ripetizione, errori/retry | PARZIALE: test Session e card; percorso reale incrociato APERTO. |
| T07 | Sessione conclusa: Stop non ripresenta Play, non altera Schedule, conserva tempo reale e minimo leggibile | PARZIALE: test realtà e geometria; screenshot e stack reale APERTI. |
| T08 | Edit/Move con tentativi reali richiede Mantieni/Elimina/Annulla; X della Sessione interna rimuove la configurazione e i tentativi al Salva; Hard Delete Activity confermata rimuove il grafo | PARZIALE: decisione attuale in `activity-session-operational-lifecycle-v2.md`; Keep, Delete, X e Hard Delete passano in PostgreSQL mirato su `0e848943`. Guard `_149` passato nel test PostgreSQL mirato su `cd3b589`; visibilità Sessioni mai avviate secondo il piano corrente candidata senza prova PostgreSQL/browser. Drag e ricorrenza APERTI. |
| T09 | Objective quantità (target richiesto), creazione/edizione atomica **solo prima di risultati registrati**, input, conferma, correzione, cancellazione definitiva confermata del solo risultato, scope protetto, policy automatica/esplicita | PARZIALE: 7 test PG mirati PASS sul vecchio checkpoint `035b28bc`; nuove prove dialog, trasporto CAS, mancata scrittura, bozza incompleta preservata ed E2E RT-01 candidate **non ancora eseguite**. |
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

## Audit mirato del 2026-11-09 — Objective registrato e Save senza modifiche

La decisione `confirmed-objective-edit-and-recurring-protection-v1.md` ha **superato** i vecchi mock che autorizzavano una Definition revision dopo la registrazione. Nel test esistente `remote-reality-objective-corrections.test.ts`, la sequenza è stata corretta da *Objective già registrato → cambia definizione → correggi* a **cambia definizione di Objective non registrato → registra risultato → correggi risultato**. Il test non è stato eliminato: conserva verifica di serializzazione, Operation ID, CAS e due operazioni distinte. Il mock di `applyActivityEdits` che fingeva il successo di un batch vuoto è stato sostituito con un'intenzione di retirement reale e tipizzata. I rifiuti autoritativi su risultati registrati restano provati via PostgreSQL nei test Objective.

Nuove regressioni e copertura intenzionale:
- `activity-inspector-actions.test.tsx`: Save invariato senza Objective e con tutte e quattro le tipologie registrate, senza richiesta atomica; cancellazione registrazione con nuova bozza incompleta, conferma annullata, 409 simulato e retry riuscito senza perdita delle altre righe.
- `event-inspector-actions.test.tsx`: parità Event con quattro tipologie registrate, no-op senza mutazione, nuova bozza conservata, fallimento e retry della cancellazione.
- `remote-activity-edit-settings.test.ts`: rifiuto locale del payload atomico vuoto prima di Auth, conservazione di CAS, risposta 422 trasformata in messaggio utente localizzato.
- `remote-reality-objective-corrections.test.ts`: ordine lecito definizione→registrazione→correzione, eliminazione CAS con errore stale, invalidazione Timeline **solo dopo risposta valida**, rifiuto di risposta 200 incoerente.
- `objective-recording-delete-dialog.test.tsx`: test DOM/aria, annullamento, tastiera e focus, conferma esplicita e richiesta in corso.
- `temporal-stateful-runtime.spec.ts`: E2E Event con obiettivo confermato e nuova bozza vuota; cancellazione lascia il draft nello stesso Edit e rimuove solo il risultato da API/PostgreSQL. `temporal-stateful-personas.spec.ts` resta responsabile dei percorsi P1/P2/P3 e dei controlli anti-duplicazione, con Schedule distinti leciti per gli intervalli Activity.

**Decisione di housekeeping:** nessun test legittimo è stato eliminato o disabilitato. Sono stati corretti due **mock obsoleti**, non rimosse le garanzie che coprivano. Il registro `test-case-registry.json` ora comprende i due file stateful E2E e il nuovo file di test del dialog con contratto, scopo e invarianti. Gli altri file esistenti restano `UNREVIEWED` fino alla verifica integrale del file e all'esecuzione; la qualifica di una nuova voce è una verifica dell'intenzione/assertion, **non** un PASS di runtime.

**Evidenza di esecuzione:** i precedenti 36 test unitari e 7 PostgreSQL PASS sono stati eseguiti dall'owner su `035b28bc`, prima delle modifiche UI successive. La nuova revisione richiede ancora format/lint/typecheck/Vitest, test registry integrity, 3-browser E2E e gate completo su singolo SHA.
