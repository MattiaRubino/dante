# DANTE — Date, orari, intervalli e fusi orari

- **Stato:** CONTRATTO DI PRODOTTO APPROVATO / implementazione del branch Temporal in verifica finale
- **Ambito:** Timeline Temporal, Quick Create, Advanced Create, Activity/Event Edit, istanze e serie.
- **Autorità semantica:** [Schedule Domain](../../domain/concepts/schedule.md), [intervalli e Sessioni](../../domain/decisions/activity-intervals-and-sessions-v2.md), [scopes ricorrenti](../../domain/decisions/recurring-series-edit-exception-policy-v1.md).
- **Regola di verifica:** comportamento approvato ≠ integrazione/prova completa. Le interazioni Create/Edit hanno copertura mirata, ma l'accettazione dell'intero verticale (persistenza, API, rilettura, Timeline e browser/DB E2E sullo stesso SHA) va verificata separatamente. Il selettore manuale del fuso della Timeline non è ancora incluso.

## Intervalli temporali

- **TMP-CLOCK-001:** modificare l'inizio sposta la fine preservando la durata del singolo periodo, anche attraversando mezzanotte o cambiando data.
- **TMP-CLOCK-002:** modificare la fine mantiene l'inizio e cambia la durata; l'utente sceglie esplicitamente la data di fine.
- **TMP-CLOCK-003:** la fine deve essere strettamente successiva all'inizio; nessuna conversione automatica a domani per compensare un orario finale invalido.
- **TMP-CLOCK-004:** i periodi notturni con data finale esplicita successiva sono validi.
- **TMP-CLOCK-005:** spostare l'inizio di una collocazione Tutto il giorno conserva il numero di giorni civili inclusivi. La fine inclusiva non può precedere l'inizio.
- **TMP-CLOCK-006:** stesse regole in Create rapido, Avanzate, Edit normale, singola istanza e scope ricorrenti compatibili; nessuna logica divergente per layout.

## Intervalli Activity

- **TMP-INTERVAL-001:** un'Activity singola non mostra «Intervallo 1» finché non è aggiunto un secondo intervallo.
- **TMP-INTERVAL-002:** durata positiva, massimo 100 intervalli, sovrapposizioni vietate; intervalli adiacenti e pause tra intervalli sono ammessi.
- **TMP-INTERVAL-003:** muovere un intervallo conserva la sua durata e non sposta automaticamente gli altri.
- **TMP-INTERVAL-004:** errore di sovrapposizione: bordo dell'intervallo da correggere e relativa etichetta rossi, senza spiegazioni testuali sotto i campi.
- **TMP-INTERVAL-005:** un Event non espone intervalli multipli; tutti gli intervalli di una Activity restano una sola Activity con Schedule distinti e envelope coerente.

## Errori e salvataggio

- **TMP-VALIDATION-001:** i controlli temporali invalidi ricevono bordo rosso. Nessun testo di errore visibile sotto data/ora; mantenere metadati accessibili per screen reader.
- **TMP-VALIDATION-002:** Salva/Conferma sono disabilitati finché il dato temporale è invalido; correzione dei campi e Annulla restano disponibili.
- **TMP-VALIDATION-003:** la validazione si applica sia alla bozza client sia al comando backend; il backend non deve mai accettare uno Schedule invalido.

## Fusi degli elementi

- **TMP-ZONE-001:** di default si utilizza un unico fuso IANA per inizio e fine. Il pulsante con globo è a destra della riga «Orario / Tutto il giorno», non sotto i campi di data/ora e non come menu dentro l'orologio.
- **TMP-ZONE-002:** Event singoli e Activity non ricorrenti con un solo intervallo possono avere fusi distinti di inizio/fine. Il pulsante generale mostra **«Personalizzato»** quando i due IANA ID differiscono.
- **TMP-ZONE-003:** serie ricorrenti, edit della serie e Activity con più intervalli usano un unico fuso. Le istanze e gli altri editor rispettano i limiti del proprio tipo di Schedule; Tutto il giorno non ammette doppio fuso.
- **TMP-ZONE-004:** in **Create Activity** con due zone diverse, premere **«Aggiungi intervallo»** è una scelta esplicita di passare a una programmazione multi-intervallo: l'aggiunta è consentita, `endTimeZoneId` viene azzerato, resta il fuso iniziale e il selettore non mostra più «Personalizzato». La durata originaria rimane invariata e la fine visualizzata viene ricalcolata nel fuso unico. Non introdurre una conferma supplementare per questa azione, né permettere fusi distinti sui nuovi intervalli. Per gli altri passaggi incompatibili (es. cambio del tipo di ricorrenza) non eliminare implicitamente dati già accettati; applicare le protezioni specifiche dell'editor/comando.
- **TMP-ZONE-005:** nel cambio manuale della zona di un estremo, i campi locali e gli istanti devono seguire le regole di proiezione del relativo editor; spostare la data/ora iniziale preserva la durata effettiva, modificare la fine varia la durata.
- **TMP-ZONE-006:** conservare in persistenza date, orari locali, zone IANA degli estremi, disambiguazione DST e istanti risolti dove previsti dal contratto. Non ridurre il caso a soli timestamp UTC.
- **TMP-ZONE-007:** con fusi diversi la fine deve essere successiva all'inizio confrontando **istanti effettivi**, non le semplici stringhe di data/ora. Ore DST inesistenti rifiutate; ore ambigue trattate secondo la disambiguazione canonica.

## Selettore timezone — comportamento UI condiviso

Le regole di questa sezione valgono per il **medesimo componente** di Quick Create, Advanced Create, Activity Edit, Event Edit, edit della singola occorrenza, edit «Questa e le successive» e altri editor temporali che offrono la selezione del fuso. Le differenze ammesse dipendono solo dal tipo/contratto della programmazione, non da un secondo layout o da una seconda logica del dialogo.

- **TMP-ZONE-UI-001 (posizione):** un pulsante compatto col globo colorato sulla **destra** della barra del tempo apre il pannello ancorato. Il dialogo offre ricerca dei fusi e, quando pertinente, «Ora locale» come modalità *floating*; nessun selettore timezone nei due controlli dell'orologio.
- **TMP-ZONE-UI-002 (ricerca):** selezione per identificativo **IANA**, con ricerca testuale e corrispondenza dei prefissi **GMT±HH:MM**. Il GMT mostrato dipende dalla data della programmazione (ora legale inclusa); i fusi con offset frazionari mantengono i minuti.
- **TMP-ZONE-UI-003 (unico/doppio):** dove ammesso, la voce **«Utilizza fusi orari diversi per inizio e fine»** è *deselezionata di default*, e quando attivata mostra i campi separati «Fuso orario di inizio» e «Fuso orario di fine». Dove **non** è ammesso il doppio fuso, **l'intera voce/checkbox non compare**: non mostrarla disabilitata. Si vede un solo selettore.
- **TMP-ZONE-UI-004 (bozza e conferma):** cambiare checkbox, ricerca o fuso modifica **solo la bozza del pannello**. **OK** applica l'intera scelta e chiude; **Annulla** chiude scartando; **Escape** scarta e chiude; un **clic esterno** chiude **senza applicare**. Riaprendo si rivede l'ultima configurazione confermata. Non applicare modifiche mentre si cerca o si naviga tra le opzioni.
- **TMP-ZONE-UI-005 (non modale):** il pannello resta un **popover leggero** ancorato al globo: **nessun overlay/attenuazione aggiuntiva**, nessun blocco dell'intera finestra Create/Edit, nessun focus trap modale e nessun obbligo di usare OK/Annulla per tornare agli altri controlli. Non reintrodurre il precedente esperimento modale.
- **TMP-ZONE-UI-006 (coerenza):** stesso pulsante, stesso dialogo, stessa ricerca, stessi pulsanti e stesse regole di chiusura nei Create ed Edit di Activity/Event e negli scope ricorrenti applicabili. Non introdurre divergenze visive o funzionali in un solo editor.

## Timeline

- **TMP-VIEW-001:** la collocazione visiva usa l'effectiveZoneId della Timeline, senza cambiare lo Schedule sorgente.
- **TMP-VIEW-002:** l'Inspector può mostrare i fusi e le ore originali dell'elemento; ricaricamento e modifiche devono conservarli.
- **TMP-VIEW-003:** il **selettore manuale della timezone della Timeline** è un intervento separato, **ancora da definire/materializzare**. Non confonderlo con il selettore del fuso degli elementi: cambiare il fuso di visualizzazione non modifica le zone IANA salvate nello Schedule.
- **TMP-VIEW-004:** fino all'approvazione della futura UI Timeline, questa specifica non definisce posizione, scelta predefinita, persistenza della preferenza o conversione delle viste; tali punti vanno fissati prima della relativa implementazione.

## Stato dell'evidenza e criteri di accettazione

- Il ritorno al **popover non modale** è stato applicato preservando lo stato del codice precedente all'esperimento con attenuazione e focus trap. Questa sezione registra il contratto approvato, non un nuovo PASS automatico.
- Le prove focalizzate di Create/Edit e del fuso distinto erano verdi su candidate precedenti; i test devono essere eseguiti nuovamente sullo SHA corrente prima di attribuirgli un esito. Nessun test Web unitario sostituisce un controllo visivo manuale o un E2E browser/API/PostgreSQL.
- Casi da preservare: Event/Activity semplice, Quick/Advanced, Edit locale, Edit di istanza, Edit di serie, fusi uguali/distinti, chiusura OK/Annulla/Escape/clic esterno, ricerca IANA/GMT, GMT stagionale/DST, più intervalli e conversione da «Personalizzato», validazione e rilettura.

## Invarianti di integrazione

Le regole citate non autorizzano a modificare retroattivamente Sessioni/Actual, protezioni, record storici, lock o eccezioni ricorrenti. Migrazioni solo forward, API compatibili, idempotenza/CAS e verifica PostgreSQL. Test funzionali e strutturali obbligatori sullo stesso SHA; nessun PASS senza esecuzione.
