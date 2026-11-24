# Home Timeline — controlli e pannello «Attività e risultati»

**Stato:** riferimento corrente del candidato `feature/timeline-temporal-operational` (24 novembre 2026). L'accettazione visiva nell'app reale e il gate completo restano separati dalle verifiche mirate.

Questo documento descrive le superfici attualmente implementate. Le regole di Schedule, Session, Actual, Outcome e Objective restano nei rispettivi documenti di dominio; un pannello Home non crea una nuova verità su ciò che è accaduto.

## Testata della Timeline

| Controllo | Superficie attuale | Funzione |
| --- | --- | --- |
| Sessioni | Pannello interno alla Timeline, sotto la testata | Raggruppa per Activity le Sessioni disponibili con i comandi ammessi. Il comportamento operativo è descritto in [Timeline Session desk](timeline-session-panel.md). |
| Cattura rapida | Pannello temporaneo sotto l'icona | Mostra l'anteprima già esistente. Campo in sola lettura, invio, allegato, voce e registro disabilitati: non salva alcuna cattura. |
| Bozze | Pannello interno alla Timeline | Cerca le bozze esistenti, le riprende, duplica o elimina tramite conferma. Le bozze non sono Schedule né Sessioni. |

L'icona di Cattura rapida apre e richiude il pannello; `Escape`, la X o un click esterno lo chiudono. X ed `Escape` riportano il focus al controllo. Lo spostamento della Cattura non attiva un nuovo servizio di registrazione e lascia libera l'altezza del pannello a destra.

## Pannello destro

«Attività e risultati» occupa la colonna destra disponibile e contiene tre viste selezionabili, anche con frecce sinistra/destra da tastiera. La vista iniziale è **Da verificare**. Ogni vista legge dati dell'utente autenticato; le tre liste hanno significati distinti.

| Vista | Cosa presenta oggi | Fonte e azione |
| --- | --- | --- |
| **Cronologia** | Card di Activity, Event e Occurrence materializzate con una collocazione accettata il cui termine è passato. È una vista del piano corrente nel passato, non un attestato di esecuzione o completamento. | Candidati da `GET /api/v1/temporal/home/chronology-candidates`; card dalla lettura canonica `GET /api/v1/temporal/timeline/window`. Click sulla card apre lo stesso Inspector della Timeline. |
| **Da verificare** | Decisioni di riconciliazione, revisioni di Reality, revisioni di Objective e Sessioni mai avviate secondo le regole del relativo owner. | `GET /api/v1/temporal/resolution-queue`; usa i controlli dei rispettivi owner. La voce «mai avviata» è una domanda derivata dal piano, non una dichiarazione di mancata esecuzione. |
| **Obiettivi** | Obiettivi privi di risultato confermato, raggruppati per Activity/Event/Occurrence; segnala anche un input provvisorio salvato. | `GET /api/v1/temporal/home/objective-work?limit=40`; espande gli stessi `ObjectiveControls` usati nell'Inspector. La bozza di input non equivale al risultato confermato. |

Il vecchio endpoint `home/finished-work` descrive fatti di Session/Reality; non è la fonte della nuova Cronologia. Le viste **Da verificare** e **Obiettivi** conservano per ora i controlli già presenti: il futuro editor raggruppato delle registrazioni di Sessione è ancora una scelta di prodotto da implementare, non una funzione attuale.

### Cronologia: inclusione, ordine e ricerca

Il backend legge solo Schedule con collocazione **corrente accettata** dell'utente. Esclude Activity ritirate o istanze superate, Occurrence saltate/superate e righe Activity pianificate che la Timeline non espone come card autonome. Per una Occurrence con più Schedule seleziona la prima collocazione corrente, coerente con la lettura Timeline. Una Occurrence solo attesa, senza Schedule materializzato, non viene creata da questa lettura e non produce una card apribile.

Per l'inclusione, il termine viene proiettato nel fuso di visualizzazione usato anche dalla Timeline: fine esclusiva per «tutto il giorno», fine dell'intervallo per le forme orarie, fine del giorno per un periodo indicativo. La selezione è in ordine di termine decrescente, con `schedule_ref` come discriminante stabile. Il cursore contiene entrambi; una pagina chiede 40 candidati e il backend legge al massimo una riga ulteriore per stabilire se esiste una pagina successiva. Il numero nell'intestazione conta le card **caricate**, non il totale storico.

Il client risolve ciascun candidato nelle finestre canoniche della Timeline, ciascuna di massimo 62 giorni, e ne riusa titolo, tipo, orario e colore di Area/elemento. Una card senza colore assegnato usa il neutro. Ricerca per titolo, senza distinzione tra maiuscole e minuscole: dopo una breve attesa dalla digitazione il client continua attraverso le pagine storiche fino ai risultati richiesti o alla fine. La barra di ricerca e l'icona di aggiornamento restano sopra la lista; scorrono solo le card. Lo scorrimento vicino al fondo carica automaticamente le pagine successive. Non c'è un pulsante «Mostra precedenti».

L'icona aggiorna i dati senza cancellare il testo cercato; una richiesta precedente viene annullata quando cambia ricerca/vista/aggiornamento. Le invalidazioni della Timeline (per esempio dopo spostamento o eliminazione), il ritorno della finestra in primo piano e il controllo periodico ricostruiscono l'elenco. Se una collocazione passa nel futuro o non è più corrente, scompare alla nuova lettura; un errore mostra `Riprova`. Il refresh non materializza Occurrence e non modifica Schedule. Non è ancora disponibile una misura di latenza su uno storico molto esteso: i test di componente non sono un benchmark.

### Apertura dell'Inspector

Il click sulla card Cronologia invia l'item canonico e il pulsante di origine alla Timeline. La Timeline costruisce la stessa rappresentazione e usa il medesimo `EventDetailDialog` delle proprie card; le future modifiche di quell'Inspector valgono quindi per entrambe le aperture. La card nel pannello è un collegamento di sola lettura, senza Play o Stop propri; eventuali azioni consentite restano governate dall'Inspector e dai loro owner.

## Confini e verifiche

- Nessuna migrazione o nuova tabella per Cronologia: la query è una proiezione autenticata di Schedule/placement esistenti.
- Schedule passato ≠ Session svolta ≠ Activity completata. Stop di una Sessione non conferma automaticamente Activity o Obiettivi.
- Il test PostgreSQL `test_chronology_cursor_reads_only_past_accepted_self_placements` è passato nel WSL dell'owner su `0466c02` (**1 passed, 3 deselected**, 24 novembre 2026). Copre ordine, cursore, isolamento, esclusione del futuro e rifiuto di cursore/fuso errati. Il precedente `MIN(uuid)` era fallito su `93f8a99` ed è stato corretto con `ORDER BY schedule_ref LIMIT 1`.
- I test Web mirati di `context-rail.test.tsx` verificano ricerca oltre la prima pagina, refresh, spostamento nel futuro e apertura dell'Inspector; il typecheck Web/API e i test OpenAPI sono passati nel workspace sul candidato precedente. Browser reale, prestazioni con molto storico e gate completo non sono ancora dichiarati PASS su `0466c02`.

**Implementazione:** `apps/web/src/features/home/ui/timeline/timeline-quick-capture.tsx`, `timeline-draft-vault.tsx`, `timeline-session-panel.tsx`; `apps/web/src/features/home/ui/context-rail/context-rail.tsx`, `past-work.ts`; `apps/backend/src/dante/modules/temporal/resolution_queue_api.py`. I contratti di dominio pertinenti sono [Schedule](../../domain/concepts/schedule.md), [Sessioni operative](../../domain/decisions/activity-session-operational-lifecycle-v2.md) e [Draft Vault](../../domain/concepts/draft-vault.md).
