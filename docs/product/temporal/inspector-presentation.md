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
- **Bordo del colore effettivo mostrato sulla card**: colore della Life Area assegnata oppure, per Activity/Event senza Area, colore personale dell'elemento. Se non esiste alcun colore, fallback **ARANCIONE DANTE `#EA5C12`**. Cambiando Area, colore dell'Area o colore personale, l'Inspector già aperto aggiorna bordo e indicazione Area senza richiedere chiusura e riapertura.
- Il colore dell'Area non segnala Play/Pausa/Stop, esito o validazione. I loro stati mantengono informazioni testuali e accessibili.
- **Unica palette di controlli**: select/option, input, textarea e pulsanti secondari dell'Inspector riusano i token già definiti per Quick/Advanced Create/Edit in `temporal-panel-controls.css`: pannello blu notte `#0D1524`, sezioni `#111C2D`, campi blu attenuato `#172438`, menu `#111B2D`, selezione `#2C3B53`, testo principale caldo `#F3F0EA`. Il bordo dei controlli è `#4A5E76`; le cornici decorative sono più discrete (`#34445C`). I menu nativi adottano `color-scheme: dark` e gli stessi colori delle `option` in Create/Edit. **Nessuna tinta viola/Area nei campi e nei menu.** Il rosso di validazione e i colori di stato runtime restano semanticamente distinti. I popup nativi sono soggetti anche al rendering del sistema operativo: verificarli nel browser reale, non dichiarare conformità dai soli CSS.
- **Header Activity, ordine obbligatorio**: (1) toolbar esistente; (2) **titolo a sinistra + controlli Play/Pausa/Stop della Sessione principale a destra sulla stessa riga**; (3) immediatamente sotto, *se presente*, stato/timer/registrazione principale, con orario di avvio e durata effettiva; (4) **orario singolo o tutti gli intervalli**; (5) Life Area; (6) Sessioni secondarie; (7) altri blocchi condizionali. Quando manca una Sessione principale visualizzabile, non inventare pulsanti o righe di stato. **Mai posizionare i controlli runtime dentro la riga temporale**, perché con più intervalli possono finire a lato dei periodi o sovrapporsi.
- **Header Event**: stessa toolbar e gerarchia di titolo → orario → Scaletta (se presente) → Area (se assegnata), **senza controlli runtime della Sessione Activity**. La scaletta vuota non occupa spazio. La Descrizione, se presente, è l'ultima sezione, dopo Obiettivi e gli altri blocchi condizionali. Il titolo rimane troncabile senza comprimere Play/Stop, e la riga di stato effettivo non deve troncare il timer.

## 3. Collocazione: uno o molti intervalli

- **Un solo intervallo:** la riga data/orario resta sostanzialmente come prima; non mostrare una sezione «Intervallo 1» artificiale.
- **Molti intervalli:** sostituire la sola riga temporale con **tutti** gli intervalli canonici `role_code=interval`, ordinati per `presentation_order`; data e orari leggibili, anche se attraversano più giorni. Il riferimento alla card aperta non limita la lista a un solo intervallo.
- **Envelope tecnico** e Schedule `planned` delle Sessioni **non sono** ulteriori intervalli della Activity; non visualizzarli come tali. Il totale degli intervalli non deve riempire i vuoti tra i periodi.
- Le collocazioni in fuso devono essere formattate usando i *resolved instants* della sorgente e il fuso di visualizzazione; le collocazioni floating mantengono l'ora locale senza inventare una timezone. Un readback incompleto/illeggibile non deve presentare un elenco parziale come se fosse completo.
- L'Inspector non introduce un secondo clock/Play per ciascun intervallo. Le Occurrence mantengono le proprie identità e protezioni e non devono essere confuse con l'intera serie.

## 4. Gerarchia dei blocchi, separatori e scroll

- **Separatori di sezione:** spazio verticale e linea principale sopra Area, Sessioni, Obiettivi, Descrizione e blocchi Event (Partecipazione, Agenda, Verifica, ecc.), solo quando i blocchi sono effettivamente presenti. I titoli delle sezioni visibili in Activity e Event usano la stessa tipografia discreta in maiuscolo, senza cambiare le etichette accessibili.
- **Descrizione:** quando presente è sempre l'ultima sezione dell'Inspector, identica per Activity ed Event e distinta dalla scaletta e dagli Obiettivi. Il titolo «Descrizione» resta fuori dalla cornice; solo il testo è nel riquadro bordato, come nelle altre sezioni. `ActivityInspectorActions` non ripete più descrizione o località sotto il titolo: la Località compare nella propria sezione finale prima della Descrizione. Un eventuale riferimento di contesto per un elemento secondario rimane distinto e compare come sezione «Contesto» verso il fondo. L'Event continua a leggere il profilo una sola volta per scaletta e descrizione.
- **Separatori interni:** righe sottili *dentro un unico contenitore arrotondato* per più Obiettivi o più punti della scaletta. Le Sessioni interne restano compatte, senza un enorme box per Sessione. Nessun doppio bordo sovrapposto o riuso dei selettori CSS degli Editor.
- **Scroll generale Inspector:** rimane esattamente disponibile come oggi.
- **Scroll interno solo al bisogno:** `overflow-y: auto` e `max-height` indicativi per Sessioni secondarie **320px**, Obiettivi **390px**, agenda Event **310px**, intervalli multipli **240px**. Nelle Sessioni scorre solo l'elenco dentro la cornice, con il titolo di sezione fuori e spazio riservato tra barra e Play/Stop. Se il contenuto è più corto, nessuno scrollbar interno. Su viewport piccoli limitare in rapporto a `dvh`, mantenendo tastiera/focus e scorrimento accessibili; non lasciare che i controlli sovrappongano o escano dal pannello.
- **Nomi troppo lunghi** (Activity, Sessione, Obiettivo, punto Agenda) visualmente tronchi con `…`; testo completo conservato nel DOM e disponibile con attributo `title` ove applicabile. **Non troncare** timer, errori, target, orari o stato necessario a decidere.

## 5. Sessioni e realtà: invarianti di ogni stato

Proteggere combinazioni Activity con/ senza Sessione principale; mai avviata, live, paused, stopped/recorded; 0–N Sessioni `planned` con stati disponibili, bloccati, attivi, paused, stopped; presenza di Sessioni storiche e Obiettivi confermati. La principale opzionale e le Sessioni interne senza principale mantengono le policy accettate.

- Main Play avvia solo la principale, senza auto-start delle interne.
- Main Pause sospende ogni interna attiva; Main Resume **non** riattiva automaticamente le interne.
- Main Stop termina atomicamente tutte le interne ancora aperte, non quelle mai avviate; chiude **l'esecuzione effettiva dell'Activity**, ma non conferma automaticamente esito/Obiettivi. La Schedule originale resta registrata separatamente dalla realtà.
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

**Regressioni mirate da mantenere:** editor non toccati; colore Life Area, colore personale senza Area, fallback arancione e aggiornamento mentre l'Inspector resta aperto; un intervallo vs due o più e envelope non mostrato; lettura `/children` una sola volta; **main Session presente una sola volta nella riga del titolo, stato/registrazione subito sotto e orari dopo**, sia con uno sia con molti intervalli; main timer live e Pause/Resume/Stop senza nuovi mount durante refresh della pianificazione; parent/child session gating e historical stop; Objective boolean/quantity/range/qualitative, invalid solo dopo Conferma senza write, correzione reset, validi `0` e sotto target; **menu nativi, sfondi e input identici ai token Create/Edit**; Context Rail unaffected; Event senza Sessione Activity, scaletta lunga e read-only; viewport stretti e overflow/scroll senza sovrapposizione.

**Prove obbligatorie:** Web TypeScript typecheck, ESLint/Prettier sui file coinvolti, Vitest esistenti `objective-controls.test.tsx`, `timeline-runtime-detail-controls.test.tsx`, `activity-planned-sessions-card-detail.test.tsx`, `timeline-inspector-header-layout.test.tsx` ed Event agenda; Playwright con real browser, desktop e mobile width, focus e interazioni; gate 27 gruppi sullo stesso commit in WSL. **Non dichiarare PASS finché i risultati non sono eseguiti.** Nessuna migrazione DB o nuova API prevista: solo lettura esistente.

## 9. Estensioni esplicitamente escluse

Il ridisegno del Context Rail Home, l'eventuale spostamento del pannello Note/Cattura e la discussione sulla politica di risoluzione/valutazione automatica degli Obiettivi **non sono parte di questo intervento**; si discuteranno separatamente dopo l'accettazione visiva dell'Inspector. Le impostazioni Objective in Create/Edit sono già definite e non si modificano.

## 10. Fascia «Tutto il giorno»: contenitore e controllo delle Sessioni (22 novembre)

La sezione `TimelineAllDayLane` è un **pannello sticky indipendente** dalle
ore sottostanti, non una seconda linea oraria. La griglia del giorno ha
già escluso il righello: la fascia **non aggiunge** i precedenti 44 px di
colonna vuota. Usa una superficie **blu notte opaca**, leggermente rientrata
(8 px laterali), **cornice completa blu-grigia da 1 px** (resa tramite
`inset box-shadow` per non alterare le altezze del time mapper),
angoli 11 px, piccola ombra e **solo un puntino arancione da 5 px**
vicino all'intestazione. È esplicitamente vietata la vecchia linea
arancione continua superiore: si confonde con la now-line e con i
separatori fra i giorni.

- **Collassato:** header 34 px, al massimo **due righe da 42 px** con
  card da 38 px. Titolo 13,5 px, periodo 11,5 px, header 11 px. Per
  0/1/2 elementi la geometria è rispettivamente `0/76/118 px`.
  I singoli elementi conservano il colore della loro Life Area e la
  linea colorata *interna* alla card, non sulla cornice comune.
- **Card indivisibile visivamente:** titolo, data/durata e gli eventuali
  due pulsanti della **Sessione principale** (Play/Pausa e Stop)
  condividono **uno stesso wrapper con sfondo, bordo e angoli**.
  La superficie cliccabile del titolo e i due pulsanti rimangono
  elementi fratelli, mai pulsanti annidati: aprire l'Inspector non
  avvia né ferma la Sessione. Mantengono gli handler e le protezioni
  già accettate, e il testo lungo lascia visibili i controlli.
  Non mostrare timer, indicatori Obiettivi, Sessioni secondarie o
  metadata del profilo. L'azione `Pianifica` per una Occurrence
  attesa continua ad essere accessibile nello stesso wrapper.
- **Tre o più elementi:** dopo le prime due card compare **una riga
  da 32 px** con freccia e testo `Mostra altri N`. Da chiuso il pannello
  misura `34 + 2×42 + 32 = 150 px`. Da aperto **si espande davvero verso
  il basso all'interno della stessa cornice**, mostrando le altre card
  nella stessa struttura, **non in un popup, un secondo pannello o un layer
  assoluto sovrapposto alle ore**. Le card orarie, il righello e la
  linea dell'ora attuale devono scendere dello stesso numero di pixel.
  La geometria aperta è `150 + min(N, 6)×42 px`: ad esempio, 3 elementi
  totali = 192 px, 8 o più = 402 px. Da 7 elementi aggiuntivi in poi
  compare lo **scroll interno** nelle sole righe aggiuntive (massimo
  6 visibili), con `scrollbar-gutter: stable` per non coprire Play/Stop e
  `overscroll-behavior: contain`. Il comando resta in fondo al pannello
  e diventa `Nascondi altri elementi`; anche Escape richiude e
  restituisce il focus. Il clic fuori non richiude automaticamente,
  evitando salti di layout durante le interazioni con la Timeline.
  Nessuna card o pulsante deve finire sotto un pannello flottante.
- **Niente frecce decorative `‹`/`›`** a fianco del titolo o vicino
  ai controlli: il periodo testuale e il colore bastano. I dati
  `data-range-*` e l'informazione di continuità restano nel modello.
- **Stop della Sessione principale su Activity all-day/multi-day**:
  conserva la barra nel **giorno locale dello Stop** e rimuove dalle
  proiezioni della Timeline le barre dei **giorni successivi**;
  se la Sessione dura un minuto, quel minuto è la durata effettiva, ma
  non converte il piano all-day in una card a orario. Il periodo
  programmato rimane distinto dal periodo effettivo. Una Sessione
  interna che finisce **non** tronca la Activity. Gli Obiettivi non
  vengono confermati automaticamente.
- Le prime due card danno precedenza alle Sessioni principali running
  poi paused, altrimenti rispettano l'ordine di proiezione
  con sort stabile. Solo presentazione, non Schedule/Session write.
  All-day, multi-day, aspettative, Week e mobile mantengono
  controllo e identità senza comprimere i pulsanti.
- L'Inspector degli elementi Tutto il giorno resta ancorato al **punto
  reale del clic**, con flip/clamp viewport e fallback da tastiera;
  lo stesso vale per le voci espanse. Il posizionamento degli
  Inspector delle card **orarie** è invariato.
- Fonte unica di verità geometrica:
  `model/timeline-all-day-layout.ts`, in cui header=34,
  row=42, footer condizionale=32, ed espansione limitata a 6 righe
  aggiuntive. Lo stato di apertura per giorno è condiviso fra il pannello
  e `applyTimelineAllDayGeometry`: il mapper/inverso, gli offset dei giorni,
  la now-line, le card orarie e la Week devono ricevere lo **stesso delta**
  della fascia espansa. I test coprono 0/1/2/3/25, apertura e chiusura,
  mapper/inverso, offset giorni, righello Week e scrollbar interna.

**Comportamento Editor → Timeline:** dopo un **Save riuscito**
di Activity o Event (normale, istanza o serie), l'Editor e il relativo
Inspector si chiudono insieme. Questo vale anche convertendo all-day ↔
intervallo a orario: la nuova card nasce nella propria collocazione
senza lasciare Inspector ancorati alla vecchia. **Annulla** torna
all'Inspector senza salvare; errori di Save restano visibili in Editor.
Nessuna chiusura prematura prima della conferma backend.

Il passaggio sticky fra giorni rimane quello già in uso: ogni
contenitore è limitato al proprio giorno, senza una nuova animazione
di transizione o cambiamento del time mapper. Va verificato visivamente
con almeno due giorni consecutivi e una Activity multi-day.

**Accettazione:** typecheck, Prettier/ESLint, Vitest del layout
ed espansione in linea, verifica interattiva browser reale per schermi
larghi/stretti, almeno 20 elementi, scroll interno, clic su Play/Stop vs
Inspector, Escape e richiudi con la freccia. Il gate completo
si esegue **solo dopo** la validazione visiva, sullo stesso SHA.
