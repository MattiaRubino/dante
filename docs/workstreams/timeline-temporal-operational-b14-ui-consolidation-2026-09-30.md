# B14 + B07 — consolidamento prodotto e UI guidato dall'uso

- **Stato:** ATTIVO — direzione e priorità fornite dall'utente durante l'uso dell'app
- **Avvio:** 2026-09-30
- **Branch:** `feature/timeline-temporal-operational`
- **Base:** B00–B13 e B12 chiusi; frontiera di persistenza prima di U2 `20260929_93`
- **Fonte della lista viva:** questo documento, Roadmap, Map e Handoff
- **CI:** non usata; i test locali sono eseguiti dall'utente

## Obiettivo

Rendere Home e Timeline utilizzabili come prodotto: creare, trovare, capire e gestire ogni capacità già implementata senza dover conoscere il lessico interno, copiare identificativi o ricostruire passaggi nascosti.

Il lavoro include la completezza del Create di B14 e il consolidamento UI/UX di B07 nello stesso ciclo. B07 resta un identificatore storico: non attende più una seconda fase dopo B14.

## Metodo di lavoro

L'utente fornisce decisioni concrete durante l'uso: cosa mantenere, rimuovere, aggiungere, spostare, raggruppare o far funzionare in modo diverso. Ogni decisione viene trattata come una voce della lista viva, senza creare sottoblocchi artificiali.

Per ogni voce:

1. registrare il comportamento attuale e quello desiderato;
2. controllare il confine Domain, persistence, API e frontend che la voce tocca;
3. modificare UI, comportamento e regole necessarie come un'unica consegna;
4. aggiornare test mirati e documentazione coinvolta;
5. segnare l'esito qui e pubblicare il checkpoint sul branch.

Le voci possono essere lavorate singolarmente oppure in un gruppo quando condividono la stessa schermata, modello o flusso. La scelta avviene in base a ciò che l'utente decide mentre usa il prodotto.

## Regole permanenti

- Nessun controllo editabile resta visibile se il suo valore non è salvato e applicato, è chiaramente di sola lettura, oppure indirizza a un flusso che lo possiede davvero.
- La UI può cambiare completamente; le distinzioni canoniche restano esplicite: Activity, Event, Routine, Recurrence, Occurrence, Schedule, Session, Actual, Outcome, Confirmation, Plan, Step e Dependency non vengono fuse per comodità visiva.
- Uno spostamento di Schedule, una proposta e un fatto avvenuto restano azioni diverse anche quando sono presentate nello stesso spazio dell'interfaccia.
- Quando una scelta richiede una nuova regola o persistenza, la si implementa nel livello proprietario e si aggiorna API, client e test se esposti pubblicamente.
- Le migrazioni pubblicate restano immutabili; una correzione dati è sempre forward-only.
- Il Quick Create non può fingere capacità: ogni dato mostrato come editabile deve arrivare al contratto canonico che lo possiede.
- Le modifiche di B14 vengono pubblicate in checkpoint frequenti e coerenti sul branch; i gate di test restano locali lato utente.

## Lista viva

| Voce | Decisione dell'utente | Stato | Evidenza / note |
|---|---|---|---|
| U0 | Inventario delle capacità create e gestibili preparato; l'utente definisce ora flussi e collocazione della UI. | pronto | inventario discusso il 2026-09-30 |
| U1 | Rivedere l'ingresso `+`: chiusura senza bozza, posizione e forma del pannello di Create, rapporto con il calendario e necessità di un comando Crea separato. | candidato pronto — prova visiva utente | decisione 2026-09-30: resta il solo `+` a sinistra; nessun comando Crea in alto. Il Create base è un pannello fisso non trascinabile che sostituisce visivamente la colonna Cattura/Da risolvere. Geometria desktop corrente: rail destra **475 px**, sottratta alla Timeline come sibling H0 senza introdurre una terza colonna; policy Timeline, fallback Home e test di layout sono allineati. Default Activity oraria. Doppio clic sulla Timeline semina data/ora. Click esterno con bozza pulita chiude; bozza modificata offre Annulla, Scarta o Sposta in Da collocare (solo Activity: crea senza Schedule). Gli Event restano collocati. Base desktop, foglio avanzato e mobile hanno larghezza/altezza/overflow responsivi. Checkpoint geometria: `1002a807`, `f4e27639`, `774d4ee5`, `98126f57`. |
| U2 | Consolidare il Quick Create come superficie canonica di authoring, mantenendo la logica del vertical e correggendo i contratti che oggi impongono vincoli di prodotto non più desiderati. | **IMPLEMENTAZIONE IN CORSO — backend/API salvati, client/UI/docs finali mancanti** | contratto fissato; migrazione `_94`, mapping, application layer, API U2 e test backend/API sono già pubblicati sul branch. |

## U2 — checkpoint implementazione salvati

Questa sezione è il punto di ripartenza operativo e viene aggiornata durante il lavoro.

### Fatto e pubblicato

- `865f458e` — contratto B14/U2 documentato: Life Area opzionale, due date esplicite, location Activity/Event, descrizione canonica, colore e Advanced condiviso.
- `48bb8d1e` — migrazione forward-only `20260930_94_b14_u2_optional_authoring_metadata.py`: metadata canonici e wrapper authoring bounded.
- `73861f19` — mapping SQLAlchemy Activity aggiornato.
- `4dee862b` — mapping SQLAlchemy Event aggiornato.
- `61c4d5c5` — `TemporalAuthoringApplication`: authoring transazionale, Life Area opzionale/creabile, colore e Schedule nello stesso confine transazionale.
- `32f01251` — test PostgreSQL U2 per unassigned, metadata, multi-day, Life Area creata/aggiornata e ACL bounded.
- `bf80ea30` — API pubblica U2 `/api/v1/temporal/authoring/activities|events` con contratto unico Quick Create.
- `680b267b` — router U2 registrato nell'app FastAPI.
- `a20731a9` — test unit/contract dell'API U2: operation id stabili, unassigned reale, location/description condivise e confini multi-day espliciti.

### Da fare prima di dichiarare U2 chiuso

1. **OpenAPI + generated client**: rigenerare dal backend U2, senza edit manuale del generated; aggiungere/aggiornare test contract client.
2. **Runtime Create web**: spostare Activity/Event Quick Create sul nuovo endpoint U2, preservando i flussi storici compatibili finché la migrazione UI non è completa.
3. **UI Quick Create**:
   - due date sempre visibili ai lati degli orari;
   - date come display cliccabili con calendario controllato DANTE, niente picker nativo/Cancella;
   - Life Area opzionale, selezione o nuova area creata solo al submit;
   - colore associato alla Life Area oppure override item se unassigned;
   - location anche Activity;
   - descrizione;
   - Tag fuori dal Quick Create;
   - rimozione del vecchio controllo esterno Life Area/Tag solo dopo equivalenza funzionale.
4. **Advanced**: superficie centrale ampia, stesso draft del rail, senza duplicare stato o persistenza.
5. **Proiezioni/Timeline**: mostrare correttamente unassigned, colore accettato e metadata utili senza creare fonti locali parallele.
6. **Catalog/Dictionary/scope/DB docs**: riconciliare `_94`, nuove colonne/funzioni e la supersessione deliberata dell'obbligo B05.
7. **Roadmap / Map / Handoff**: aggiornare al checkpoint U2 reale dopo i gate.
8. **Gate locale utente**: Alembic/PostgreSQL + test backend U2/regressioni B05/B03/B02 + API/OpenAPI/client + web typecheck/vitest + prova visiva/E2E. Nessuna CI.

## U2 — contratto Quick Create e authoring canonico

### Oggetto e collocazione

- Il Quick Create espone **Activity** ed **Event** come capacità operative attuali. `Timer` e `Sveglia` possono restare visibili come future entry disabilitate finché non esiste il relativo vertical.
- Collocazione rapida: `Orario`, `Tutto il giorno`, `Da collocare`; la vecchia `Fascia` non resta nel Quick Create.
- La UI non altera le distinzioni `Activity != Event`, `Schedule != Session != Actual` e `planned/intended != happened`.

### Intervallo temporale

- Per la modalità `Orario` sono visibili **sempre due date**, una di inizio e una di fine, con i due orari al centro: `data inizio | ora inizio → ora fine | data fine`.
- Le date sono display cliccabili leggibili (es. `mar 30 set`), non campi numerici `gg/mm/aaaa`; il calendario è un popover controllato da DANTE, non il picker nativo del browser.
- Il popover calendario si chiude dopo la selezione o al click esterno; nessuna azione browser `Cancella` deve essere esposta.
- Gli orari restano editabili da tastiera e con controllo ore/minuti; l'orologio apre la lista a passi di 15 minuti. Le fasce (`Mattina`, `Pomeriggio`, `Sera`, `Notte`) appartengono al comando tra inizio e fine e impostano entrambi gli estremi.
- Un intervallo che attraversa mezzanotte o più giorni deve essere **esplicito nelle due date**; non sono ammessi rollover nascosti della sola ora finale.
- La rappresentazione UI deve continuare a produrre una Schedule canonica; se il contratto pubblico oggi esprime `date + start + duration`, la seconda data viene trasformata in un intervallo/durata senza creare una seconda fonte di verità.

### Life Area, colore e Tag

- La **Life Area non è obbligatoria** per creare una nuova Activity o Event. L'assenza è stato canonico `null/unassigned`, non una Life Area sintetica chiamata `-`, `Personal` o equivalente.
- Il Quick Create contiene un campo `Life Area (opzionale)` scrivibile/selezionabile. Focus/click mostra le Life Area esistenti; testo nuovo prepara una nuova Life Area nel draft.
- Una Life Area digitata durante il draft viene creata **solo quando `Aggiungi` viene accettato**. La creazione dell'item non deve lasciare Life Area orfane se il comando complessivo fallisce.
- Se viene selezionata una Life Area esistente, il suo colore è il colore predefinito dell'elemento.
- Se si modifica il colore con una Life Area selezionata e si conferma, viene aggiornata l'apparenza della Life Area attraverso il suo contratto canonico/revisionato; le successive selezioni ereditano il nuovo colore.
- Se non è selezionata alcuna Life Area, un colore scelto è un override dell'elemento, non la creazione di una Life Area fittizia.
- I **Tag** B05 restano una capacità canonica secondaria molti-a-molti ma non fanno parte del Quick Create in questa fase; non vengono eliminati dalla piattaforma.
- Il vecchio controllo esterno `Life Area e Tag` viene rimosso/spostato solo quando le capacità ancora necessarie sono raggiungibili dalla nuova superficie.

### Location e descrizione

- **Location è opzionale sia per Activity sia per Event.** Non è più una capability solo Event.
- `Descrizione` è un campo opzionale del Quick Create. Deve essere persistita tramite un contratto canonico esplicito; un valore solo nel metadata frontend non è sufficiente.
- Location e descrizione non cambiano la semantica di Schedule e non vengono usate come scorciatoie per Context, Life Area o Tag.

### Colore dell'elemento

- Il colore visuale può derivare dalla Life Area oppure essere sovrascritto a livello dell'elemento.
- L'override dell'elemento deve essere persistito nel proprietario corretto e non nel solo stato React.
- La Timeline usa lo stesso stato accettato per renderizzare la card; nessun secondo catalogo colori locale.

### Opzioni avanzate

- Il footer del rail mantiene `Opzioni avanzate`, `Annulla`, `Aggiungi` fissi.
- `Opzioni avanzate` non espande indefinitamente i 475 px del rail: apre una **superficie centrale ampia** sopra la Home.
- Quick Create e Advanced condividono **lo stesso draft**, non due form o due fonti di verità; chiudendo Advanced si torna al rail conservando le modifiche.
- La superficie avanzata organizza le capacità già implementate (timezone/temporal policy, recurrence, constraints, execution structure, reminder/confirmation/outcome, partecipanti e proprietà Event, ecc.) senza esporre controlli che non persistono realmente.

### Confini di implementazione U2

La consegna U2 è considerata completa solo quando sono coerenti:

1. persistenza PostgreSQL e migrazioni forward-only;
2. mapping SQLAlchemy e application layer;
3. API/OpenAPI;
4. generated client rigenerato, mai editato a mano;
5. runtime Create e UI;
6. test PostgreSQL/backend, contract/client e web mirati;
7. Dictionary/scope e documenti Database/Workstream coinvolti;
8. Roadmap, Map e Handoff.

La precedente regola B05 secondo cui ogni nuovo planning item deve ricevere una Life Area primaria viene quindi **deliberatamente superseded da U2**: una Life Area resta una classificazione actor-local utile, ma non è prerequisito ontologico per l'esistenza di Activity/Event.

## Chiusura

B14/B07 chiude quando l'utente considera coerenti i flussi principali e l'inventario non contiene più comandi inutili, nascosti dietro passaggi tecnici o privi di comportamento reale. B15 conserva il controllo verticale finale su persistenza, catalogo, API, client, frontend e regressioni.
