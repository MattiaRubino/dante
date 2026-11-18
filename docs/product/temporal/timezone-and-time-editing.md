# DANTE — Date, orari, intervalli e fusi orari

- **Stato:** CONTRATTO DI PRODOTTO APPROVATO, IMPLEMENTAZIONE IN CORSO
- **Ambito:** Timeline Temporal, Quick Create, Advanced Create, Activity/Event Edit, istanze e serie.
- **Autorità semantica:** [Schedule Domain](../../domain/concepts/schedule.md), [intervalli e Sessioni](../../domain/decisions/activity-intervals-and-sessions-v2.md), [scopes ricorrenti](../../domain/decisions/recurring-series-edit-exception-policy-v1.md).
- **Regola di verifica:** una decisione approvata non equivale a implementazione testata. Non dichiarare il doppio fuso operativo finché persistenza, API, rilettura, Timeline ed E2E non sono completi.

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

- **TMP-ZONE-001:** di default esiste un unico fuso IANA per inizio e fine, nella barra superiore a destra di Orario/Tutto il giorno.
- **TMP-ZONE-002:** Event singoli e Activity non ricorrenti con un solo intervallo possono avere opzionalmente fusi distinti di inizio/fine, scelti nel menu dell'orologio. Il selettore generale mostra «Personalizzato» quando differiscono.
- **TMP-ZONE-003:** serie ricorrenti e Activity con più intervalli usano un unico fuso, anche negli editor delle occorrenze ricorrenti. Tutto il giorno non usa doppio fuso.
- **TMP-ZONE-004:** se il passaggio a serie o a più intervalli rende incompatibile il doppio fuso, chiedere una conversione esplicita; vietate conversioni silenziose.
- **TMP-ZONE-005:** cambiando manualmente il fuso di un estremo nell'editor si conserva il suo orario locale e si ricalcola il suo istante; un cambio dell'inizio continua a conservare la durata effettiva.
- **TMP-ZONE-006:** conservare in persistenza date, orari locali, due zone IANA, disambiguazione DST e istanti risolti. Non ridurre il caso a soli timestamp UTC.
- **TMP-ZONE-007:** fine successiva all'inizio confrontando istanti effettivi nel caso di fusi diversi; ore DST inesistenti rifiutate e ore ambigue disambiguate esplicitamente.

## Timeline

- **TMP-VIEW-001:** la collocazione visiva usa l'effectiveZoneId della Timeline, senza cambiare lo Schedule sorgente.
- **TMP-VIEW-002:** l'Inspector può mostrare i fusi e le ore originali dell'elemento; ricaricamento e modifiche devono conservarli.
- **TMP-VIEW-003:** il futuro selettore manuale della timezone della Timeline è un intervento separato e NON rientra nell'implementazione corrente.

## Invarianti di integrazione

Le regole citate non autorizzano a modificare retroattivamente Sessioni/Actual, protezioni, record storici, lock o eccezioni ricorrenti. Migrazioni solo forward, API compatibili, idempotenza/CAS e verifica PostgreSQL. Test funzionali e strutturali obbligatori sullo stesso SHA; nessun PASS senza esecuzione.
