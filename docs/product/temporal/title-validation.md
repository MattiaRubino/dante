# DANTE — Validazione titolo in Create e Edit

- **Stato:** contratto di prodotto approvato il 19 novembre 2026; implementazione candidata nel branch Temporal. La prova UI/real-stack deve essere eseguita sul commit finale.
- **Ambito:** Activity ed Event, Create rapido/avanzato, Edit normale, Edit «Solo questa», «Questa e le successive» e «Dalla prossima istanza». Lo stesso campo titolo condiviso governa tutte le superfici.

## Regola funzionale

- **TITLE-001 (riposo):** all'apertura il titolo può essere vuoto in Create senza bordo rosso, messaggio o animazione. Negli Edit il titolo esistente è inizialmente valido. Il campo non segnala un errore prima di un tentativo.
- **TITLE-002 (azione disponibile):** `Aggiungi` e `Salva modifiche` restano cliccabili **quando l'unico problema è il titolo vuoto o composto soltanto da spazi**. Il titolo vuoto non è un motivo di `disabled`. Si conservano invece i blocchi autonomi già previsti: operazione in corso, caricamento dati essenziali, vincoli temporali, errori bloccanti e protezioni delle registrazioni.
- **TITLE-003 (tentativo non valido):** cliccando la CTA primaria o inviando un form che supporta Enter con titolo vuoto, **non parte alcuna mutazione** (né UI application command, né HTTP API, né SQL). Il titolo riceve il focus, l'intera cornice condivisa assume un bordo rosso visibile anche con focus, sotto il campo compare il messaggio `Inserisci un titolo.` con `role="alert"` e `aria-invalid`.
- **TITLE-004 (micro-feedback):** al tentativo non valido la cornice esegue una **breve vibrazione una volta**; un secondo tentativo la può ripetere. Non vibra al mount, a ogni re-render o continuativamente. Rispettare `prefers-reduced-motion: reduce`: in quel caso nessuna animazione, ma colore e messaggio rimangono.
- **TITLE-005 (correzione):** non appena il titolo diventa non vuoto dopo trim, il bordo e il messaggio scompaiono. Se l'utente cancella nuovamente un titolo valido, l'errore ricompare **solo al prossimo tentativo di salvataggio**.
- **TITLE-006 (saving autentico):** spinner, stato `pending` e `disabled` della CTA sono ammessi soltanto per una reale operazione autorizzata, non per un titolo mancante. Un pulsante disabled per motivi indipendenti non deve visualizzare un falso cursore di caricamento.
- **TITLE-007 (scope):** nelle modifiche di istanza e di serie il tentativo con titolo vuoto precede la preview, l'accettazione e il salvataggio per lo scope selezionato; non modifica la Recurrence, le Occurrence o gli Schedule.
- **TITLE-008 (non-regressione):** l'errore del titolo non cancella modifiche locali a intervalli, timezone, Sessioni, Obiettivi, Area, Scaletta, Reminder o altri attributi; il campo non usa il `required` nativo che impedirebbe la validazione visuale controllata. Nessuna modifica alle altre regole di ammissione e ai blocchi esistenti.

## Evidenza e test

Copertura mirata da eseguire sullo stesso commit: Create Advanced Activity/Event, Create Quick, Activity Edit, Event Edit, Event series editor, hook condiviso. Controllare CTA cliccabile, assenza di errore iniziale, nessuna chiamata di mutazione, focus, bordo, messaggio, animazione ripetibile e scomparsa dopo correzione. In E2E real-stack confermare anche l'assenza di nuovi record per il titolo vuoto.

Questo documento integra [date, orari, intervalli e timezone](timezone-and-time-editing.md) e non modifica le protezioni delle Sessioni e delle serie.
