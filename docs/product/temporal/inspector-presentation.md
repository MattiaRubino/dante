# DANTE — Inspector Activity/Event: presentazione, runtime e leggibilità

- **Stato:** decisione di prodotto approvata il 20 novembre 2026; implementazione candidata su `feature/timeline-temporal-operational`; prove locali e browser da acquisire sul commit finale.
- **Autorità:** questa pagina descrive esclusivamente l'**Inspector di sola consultazione/operatività** aperto dalla Timeline, non gli editor `Create`, `Modifica`, `Solo questa`, `Questa e le successive` o `Dalla prossima`. Il registro cronologico e la prova di esecuzione sono in [Timeline — Live Execution Ledger](../../workstreams/timeline-temporal-operational-map.md).
- **Invarianti superiori:** [Activity/Session lifecycle](../../domain/decisions/activity-session-operational-lifecycle-v2.md), [Activity intervals and Sessions](../../domain/decisions/activity-intervals-and-sessions-v2.md), [Session desk and reality](../../domain/decisions/activity-session-live-timeline-v1.md), [date, intervalli, time-zone](timezone-and-time-editing.md), [confirmed Objective and recurrence protection](../../domain/decisions/confirmed-objective-edit-and-recurring-protection-v1.md), [test standard](../../development/testing-standard.md).

## 1. Perimetro: cambiare la presentazione, non i comportamenti

L'Inspector è la modalità `timeline-event-modal--inspector` del `EventDetailDialog`, distinta da `timeline-event-modal--edit`. Condivide la shell fra Activity ed Event, **non** forza lo stesso contenuto: l'Activity mantiene Sessione principale, Sessioni pianificate e relative registrazioni; l'Event mantiene partecipazione, scaletta/agenda in sola lettura, ricorrenza e dati specifici. Le sezioni condizionali già implementate restano condizionali; niente nuove autorizzazioni o controlli inventati.

**Non cambiare:** gli handler Play/Pausa/Riprendi/Stop, il timer e i dati effettivi, i CAS/idempotency lock, le registrazioni Session/Actual/Outcome/Objective, reminder, guard di ricorrenza, cancellazioni, gli indicatori di disponibilità e gli stati disabilitati. Non trasformare un'Activity conclusa o un Event trascorso in un Result confermato. Non manipolare gli Schedule solo per cambiare la visualizzazione. Create/Edit, tutti gli scope e il Context Rail Home conservano le proprie funzionalità e semantiche.

**Cambiare solo quanto necessario:** disposizione dei blocchi già esistenti, tipografia, spazi, bordi, tronca-testo, scroll; lettura di *tutti* gli Schedule di ruolo `interval` per la visualizzazione degli intervalli multipli (read-only). Riutilizzare l'endpoint `GET /api/v1/temporal/activities/{ref}/children`, già utilizzato dalle Sessioni pianificate, senza una seconda richiesta identica nell'Inspector.

## 2. Shell e colori

- Larghezza massima desktop indicativa: **600px** (da 540px); su display piccoli restare entro il viewport. Non creare una colonna permanente né alterare la geometria della Timeline. L'Inspector conserva posizione vicino alla card e **scroll verticale esterno**, altezza massima corrente e header toolbar sticky.
- **Bordo del colore esatto della Life Area effettiva**, stesso valore dell'indicatore Area. La cornice non usa il colore decorativo della card come sostituto della Life Area. Se la Life Area è assente / `null` / senza colore, fallback **ARANCIONE DANTE `#EA5C12`**: non grigio. Cambiando soggetto, nessun vecchio colore deve sopravvivere al cambio.
- Il colore dell'Area non segnala Play/Pausa/Stop, esito o validazione. I loro stati mantengono informazioni testuali e accessibili.
- Header: azioni esistenti a sinistra, close a destra; titolo più leggibile (circa 21px). Data/orari 14px; Area **subito dopo gli orari**, **prima delle Sessioni secondarie**. Controlli runtime della **Sessione principale** restano a destra dell'orario, nella stessa posizione operativa. In esecuzione/pausa/conclusa mantenere esattamente le relative righe con avvio, timer e tempi reali, senza spostare i comandi.

## 3. Collocazione: uno o molti intervalli

- **Un solo intervallo:** la riga data/orario resta sostanzialmente come prima; non mostrare una sezione «Intervallo 1» artificiale.
- **Molti intervalli:** sostituire la sola riga temporale con **tutti** gli intervalli canonici `role_code=interval`, ordinati per `presentation_order`; data e orari leggibili, anche se attraversano più giorni. Il riferimento alla card aperta non limita la lista a un solo intervallo.
- **Envelope tecnico** e Schedule `planned` delle Sessioni **non sono** ulteriori intervalli della Activity; non visualizzarli come tali. Il totale degli intervalli non deve riempire i vuoti tra i periodi.
- Le collocazioni in fuso devono essere formattate usando i *resolved instants* della sorgente e il fuso di visualizzazione; le collocazioni floating mantengono l'ora locale senza inventare una timezone. Un readback incompleto/illeggibile non deve presentare un elenco parziale come se fosse completo.
- L'Inspector non introduce un secondo clock/Play per ciascun intervallo. Le Occurrence mantengono le proprie identità e protezioni e non devono essere confuse con l'intera serie.

## 4. Gerarchia dei blocchi, separatori e scroll

- **Separatori di sezione:** spazio verticale e linea principale fra Sessioni, Obiettivi, Descrizione e blocchi Event (Partecipazione, Agenda, Verifica, ecc.), solo quando i blocchi sono effettivamente presenti.
- **Separatori interni:** righe sottili *dentro un unico contenitore arrotondato* per più Obiettivi o più punti della scaletta. Le Sessioni interne restano compatte, senza un enorme box per Sessione. Nessun doppio bordo sovrapposto o riuso dei selettori CSS degli Editor.
- **Scroll generale Inspector:** rimane esattamente disponibile come oggi.
- **Scroll interno solo al bisogno:** `overflow-y: auto` e `max-height` indicativi per Sessioni secondarie **320px**, Obiettivi **390px**, agenda Event **310px**, intervalli multipli **240px**. Se il contenuto è più corto, nessuno scrollbar interno. Su viewport piccoli limitare in rapporto a `dvh`, mantenendo tastiera/focus e scorrimento accessibili; non lasciare che i controlli sovrappongano o escano dal pannello.
- **Nomi troppo lunghi** (Activity, Sessione, Obiettivo, punto Agenda) visualmente tronchi con `…`; testo completo conservato nel DOM e disponibile con attributo `title` ove applicabile. **Non troncare** timer, errori, target, orari o stato necessario a decidere.

## 5. Sessioni e realtà: invarianti di ogni stato

Proteggere combinazioni Activity con/ senza Sessione principale; mai avviata, live, paused, stopped/recorded; 0–N Sessioni `planned` con stati disponibili, bloccati, attivi, paused, stopped; presenza di Sessioni storiche e Obiettivi confermati. La principale opzionale e le Sessioni interne senza principale mantengono le policy accettate.

- Main Play avvia solo la principale, senza auto-start delle interne.
- Main Pause sospende ogni interna attiva; Main Resume **non** riattiva automaticamente le interne.
- Main Stop termina atomicamente tutte le interne ancora aperte, non quelle mai avviate; non conferma l'Activity.
- La disponibilità delle interne cambia quando la principale inizia/pausa/riprende/si chiude, secondo policy esistente. Il timer principale continua ad aggiornarsi; nessuno stile può interrompere il suo React mounting/ciclo di vita.
- Il runtime con / senza Sessioni registrate non modifica il piano. Non duplicare la riga della Sessione principale né creare nuovi tentativi.

## 6. Obiettivi Inspector: visualizzazione e validazione

- Ogni riga presenta **nome ben leggibile**, un sottotesto **solo** se esiste un target quantitativo o intervallo (`≥ X`, `≤ X`, `= X`, `min–max`, eventuale unità) e i controlli esistenti di risultato + **Conferma**. Nessuna nota «Risultato Sì/No» o «Valuta» sotto al titolo: le selezioni sono già autoesplicative.
- Font e target realmente leggibili; campi e pulsante della stessa altezza, affiancati quando possibile e a capo se lo spazio lo richiede. I risultati già confermati restano una vista read-only fedele, senza nuovo tipo di correzione/cancellazione.
- **Errore rosso solo dopo clic su Conferma** con valore mancante o malformato nell'Inspector: bordo rosso localizzato sul campo, messaggio breve, una micro-vibrazione ripetibile ad ogni tentativo, rispettando `prefers-reduced-motion`. Nessun errore al mount, digitazione o semplice blur. Correggendo l'input, l'errore scompare. Zero è un valore numerico valido quando consentito; una misura validamente inferiore al target **non** è un errore di input.
- Consentire il *tentativo* tramite Conferma quando il campo è vuoto **solo nell'Inspector**; senza payload valido **nessuna** bozza, Observation, Result o HTTP di mutazione. Quando busy, mantenere il blocco attuale. Il Context Rail Home mantiene il comportamento precedente di Conferma disabilitata per valore invalido.
- La bozza rimane persistente, versionata e **non confermata**; la conferma esplicita effettua l'operazione canonica e la rilettura. Non inventare valori, successo, Actual, Outcome o completamento dal trascorrere del tempo.

## 7. Event: stessa presentazione, contenuti propri

- L'Event utilizza **lo stesso stile dell'Inspector**, ma non riceve controlli Activity main/secondary Session.
- La **Scaletta** già supportata resta un elenco ordinato e read-only nell'Inspector; numerazione e separatori coerenti, altezza limitata e scroll interno condizionale. Nessuna nuova checkbox, esecuzione, riordinamento, o nuova azione di salvataggio.
- Partecipazione, Descrizione, reminder, verifica realtà, dati dell'Occurrence e le altre sezioni Event rimangono secondo i contratti attuali.
- Non alterare nessuno dei layout Create/Edit della scaletta (componente condiviso, CSS solo con selettore Inspector).

## 8. Implementation & acceptance

**Owner tecnici:** `apps/web/src/features/home/ui/timeline/timeline-overlays.tsx`, `timeline.css`, `timeline-inspector-reality.tsx`, `timeline-event-agenda-editor.tsx`, `apps/web/src/features/temporal/activity-planned-sessions-card-detail.tsx` e `objective-controls.tsx`.

**Regressioni mirate da mantenere:** editor non toccati; colore Life Area valido/null/assente; un intervallo vs due o più e envelope non mostrato; lettura `/children` una sola volta; ordine titolo→orari→Area→Sessioni; main timer live e Pause/Resume/Stop; parent/child session gating e historical stop; Objective boolean/quantity/range/qualitative, invalid solo dopo Conferma senza write, correzione reset, validi `0` e sotto target; Context Rail unaffected; Event senza Sessione Activity, scaletta lunga e read-only; viewport stretti e overflow/scroll senza sovrapposizione.

**Prove obbligatorie:** Web TypeScript typecheck, ESLint/Prettier sui file coinvolti, Vitest esistenti `objective-controls.test.tsx`, `timeline-runtime-detail-controls.test.tsx`, `activity-planned-sessions-card-detail.test.tsx` ed Event agenda; Playwright con real browser, desktop e mobile width, focus e interazioni; gate 27 gruppi sullo stesso commit in WSL. **Non dichiarare PASS finché i risultati non sono eseguiti.** Nessuna migrazione DB o nuova API prevista: solo lettura esistente.

## 9. Estensioni esplicitamente escluse

Il ridisegno del Context Rail Home, l'eventuale spostamento del pannello Note/Cattura e la discussione sulla politica di risoluzione/valutazione automatica degli Obiettivi **non sono parte di questo intervento**; si discuteranno separatamente dopo l'accettazione visiva dell'Inspector. Le impostazioni Objective in Create/Edit sono già definite e non si modificano.
