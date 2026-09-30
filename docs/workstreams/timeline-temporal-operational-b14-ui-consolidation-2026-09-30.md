# B14 + B07 — consolidamento prodotto e UI guidato dall'uso

- **Stato:** ATTIVO — U2 source candidate pubblicata; gate locale/generated pendenti
- **Avvio:** 2026-09-30
- **Branch:** `feature/timeline-temporal-operational`
- **Base chiusa:** B00–B13 e B12
- **Frontiera persistence source corrente:** `20260930_94`
- **Ultima frontiera catalogo provata prima di U2:** `_93` / `196|5|155|100|397|344|497|0|0|0`
- **Gate U2:** `docs/workstreams/timeline-temporal-operational-b14-u2-gate-2026-09-30.md`
- **CI:** non usata; i test locali sono eseguiti dall'utente

## Obiettivo

Rendere Home e Timeline utilizzabili come prodotto: creare, trovare, capire e gestire ogni capacità già implementata senza dover conoscere il lessico interno, copiare identificativi o ricostruire passaggi nascosti.

B14 e B07 vengono lavorati nello stesso ciclo: ogni decisione dell'utente viene verificata lungo il vertical proprietario (`persistence → backend → API → client → UI`) quando modifica un contratto, oppure resta puro consolidamento UI quando non modifica la verità canonica.

## Regole permanenti

- PostgreSQL resta unica autorità canonica.
- Nessun controllo editabile resta visibile se il valore non viene realmente salvato/applicato oppure se non è chiaramente read-only/futuro.
- Migrazioni pubblicate immutabili; ogni correzione persistence è forward-only.
- Generated OpenAPI/client mai editati a mano.
- Quick Create non può fingere capability.
- `Activity != Event != Routine`, `Routine != Recurrence != Occurrence`, `Occurrence != Schedule`, `Schedule != Session != Actual`, `Actual != Outcome != Confirmation`.
- `Life Area != Tag != Context`; organizzazione prodotto non diventa ownership Domain o Schedule truth.
- `planned/intended != happened`, `projection != canonical truth`, `proposal != accepted effect`.
- Checkpoint frequenti sul branch; nessuna GitHub Action/CI per i gate di questo workstream.

## Lista viva

| Voce | Decisione | Stato | Nota |
|---|---|---|---|
| U0 | Inventario capacità e superfici | pronto | base per il consolidamento user-guided |
| U1 | `+` nel rail destro, chiusura draft, doppio click Timeline, geometria Home | candidato/provato progressivamente | rail desktop 475 px; Create sostituisce Cattura/Da risolvere; niente terza colonna |
| U2 | Quick Create canonico: date, Life Area opzionale, colore, location, descrizione, authoring Activity/Event | **SOURCE CANDIDATE PUBBLICATA — gate locale richiesto** | `_94` + backend/API + runtime web + UI U2 + test source presenti; generated/client e prova locale ancora da eseguire |
| U3+ | successivo polish e organizzazione UI | da continuare dopo gate U2 | include Advanced centrale e successive decisioni utente |

## U2 — decisioni canoniche

### Oggetto e collocazione

- Quick Create espone **Activity** ed **Event** come capability correnti.
- `Timer` e `Sveglia` restano entry future disabilitate finché non esiste il relativo vertical.
- Collocazione rapida: `Orario`, `Tutto il giorno`, `Da collocare` per Activity; Event resta collocato.
- La vecchia `Fascia` non è una quarta semantica di collocazione Quick: le fasce orarie sono shortcut del controllo inizio/fine.

### Intervallo temporale

- Modalità `Orario`: due date esplicite e sempre visibili attorno ai due orari: `data inizio | ora inizio → ora fine | data fine`.
- Le date usano un picker DANTE controllato, non l'input data nativo del browser; quindi nessun comando browser `Cancella` fa parte del prodotto.
- Ora e minuti restano editabili da tastiera e tramite stepper; l'orologio apre gli orari a passi di 15 minuti.
- Le fasce `Mattina/Pomeriggio/Sera/Notte` appartengono al comando tra inizio e fine e impostano entrambi gli estremi.
- Multi-day esplicito: nessun rollover nascosto della sola ora finale.
- La UI produce una Schedule canonica attraverso il contratto di placement U2; le date UI non diventano una seconda fonte di verità.

### Life Area, colore e Tag

- **Life Area opzionale** per nuova Activity/Event.
- Assenza = vero stato canonico `null/unassigned`; nessuna Life Area fittizia `-`, `Personal` o equivalente.
- Campo Quick `Life Area (opzionale)` scrivibile/selezionabile.
- Un nome nuovo resta solo nel draft e viene creato atomicamente soltanto quando `Aggiungi` viene accettato.
- Se il comando complessivo fallisce, non deve restare una Life Area orfana.
- Selezionare una Life Area esistente usa colore/revisione canonici senza creare una nuova revisione.
- Cambiare esplicitamente il colore di una Life Area selezionata produce un update revision-guarded.
- Senza Life Area, un colore scelto è override dell'item.
- I Tag B05 restano capability canonica secondaria molti-a-molti ma sono fuori dal Quick Create.
- Il pannello storico `Life Area e Tag` non viene rimosso finché le capability di gestione Tag/area ancora necessarie non hanno una destinazione equivalente.

### Location e descrizione

- `location` è opzionale sia per Activity sia per Event.
- `description` è opzionale e persistita canonicamente, non solo nel metadata React/frontend.
- Location/description non sono Schedule, Context, Life Area o Tag.

### Colore

- `activity_intention.color_code` / `event_expectation.color_code` possiedono l'override item.
- Il colore della Life Area resta actor-local organization state.
- La Timeline può proiettare l'apparenza accettata ma non diventa proprietaria di quella verità.

## U2 — implementazione pubblicata

### Persistence / backend / API

- `865f458e` — contratto U2 iniziale.
- `48bb8d1e` — migration forward-only `20260930_94_b14_u2_optional_authoring_metadata.py`.
- `_94` aggiunge `description`, `location`, `color_code` a `dante.activity_intention` e `dante.event_expectation` con vincoli DB.
- `_94` aggiunge wrapper bounded `create_self_activity_authoring(...)` e `create_self_event_authoring(...)`; runtime non riceve direct-write sui descriptor.
- `73861f19` — mapping Activity.
- `4dee862b` — mapping Event.
- `61c4d5c5` — `TemporalAuthoringApplication`: Activity/Event + Life Area opzionale/nuova/revisionata + eventuale Schedule nello stesso boundary applicativo.
- `32f01251` — PostgreSQL proof U2: unassigned, metadata, multi-day, replay/idempotenza, Life Area atomica/colore revision-guarded, ACL bounded.
- `bf80ea30` — `/api/v1/temporal/authoring/activities` e `/events`.
- `680b267b` — router FastAPI registrato.
- `a20731a9` — contract tests API U2.

### Web / UI authoring

- `42ff23b4` — authoring data-source frontend.
- `cabcc9a3` — adapter remoto U2.
- `db4716f6` — wire tests adapter.
- `0793aed9` — U2 authoring draft.
- `e15d94cf` + `649c355d` — calendario DANTE custom.
- `289f5c7d` + `5eb741dc` — campo Life Area opzionale.
- `b1b73f4b` — draft U2 condiviso.
- `a6b325e0` + `066c48f8` — core UI U2.
- `9dbbefa0` — field surface spostata sul core U2.
- `c508a3db` — Quick/Advanced condividono lo stesso draft.
- `703eec28` + `d41afaa9` — distinzione colore accettato vs colore modificato dall'utente.
- `8043ce05` + `f4f69c81` — mapping Quick draft → request U2 e test.
- `93924cdd` — Timeline group ViewModel conserva revision/colore actor-local accettati senza possederli.
- `1d3cabfe` — Quick Create compatibile usa il nuovo authoring U2; intenti avanzati non ancora rappresentabili restano sul runtime storico e non vengono silently dropped.
- `8a2c7393` — campo Life Area rilegge il catalogo canonico in produzione prima della selezione/colour edit.
- `d059bc9f` — `Senza Life Area` trattato come stato organizzativo legittimo, non legacy.
- `cc0204e6` — entry tests Activity/Event U2.
- `792a82a2` — typing test fallback recurrence consolidato.

## Confine temporaneo con Advanced

U2 chiude il **Quick authoring compatibile**. Le capability avanzate storiche che non sono ancora rappresentate dal nuovo DTO U2 non vengono semplificate o perse: il runtime rileva l'intento e resta sul percorso storico.

Questo è deliberato e temporaneo. La prossima fase UI deve migrare/organizzare le capability Advanced nella superficie centrale mantenendo lo stesso draft e poi potrà ridurre il fallback storico. Finché quel passaggio non è completo non è corretto affermare che ogni possibile configurazione Advanced utilizzi già il DTO U2.

## Generated API client

Il public contract backend è cambiato, quindi prima del gate devono essere rigenerati:

```text
packages/api-client/openapi/dante-v1.openapi.json
packages/api-client/src/generated/
```

Solo tramite:

```bash
pnpm api:generate
pnpm generated:check
```

Nessun edit manuale è ammesso.

## Gate U2

Il comando autorevole è registrato in:

`docs/workstreams/timeline-temporal-operational-b14-u2-gate-2026-09-30.md`

Il gate comprende:

```text
Alembic upgrade _94
PostgreSQL U2 + regressioni B05/B03/database catalog
API U2 unit contract
OpenAPI export + generated client
web typecheck
U2 adapter/mapper/entry + U1 regressions
api-client typecheck
manual real-app proof
```

## Cosa NON è ancora chiuso

- Il source tree U2 è candidate, non `PROVEN`, finché l'utente non esegue il gate locale.
- OpenAPI/generated devono essere rigenerati localmente dal backend corrente e l'eventuale diff deve essere committato.
- Dictionary/catalog e Roadmap/Map/Handoff devono essere promossi alla frontiera `_94` **dopo** il gate, usando la topologia realmente osservata e non inventata.
- La superficie Advanced centrale grande è la prossima decisione/UI work: il draft condiviso è già predisposto, la forma visuale finale non è ancora congelata.
- Ulteriore polish Home/Timeline continua dopo il gate U2.

## Supersessione B05 deliberata

B05 resta valido per catalogo Life Area, assignment actor-local, colori e Tag, ma la precedente regola di prodotto “ogni nuovo planning item deve avere una Life Area primaria” è superseded da U2.

```text
Activity/Event may exist without Life Area assignment
absence of assignment != synthetic category
Life Area remains organization, not Domain ownership
Tag remains secondary many-to-many organization
```

## Chiusura

U2 sarà marcato `CLOSED / PROVEN` solo dopo esito positivo del gate locale e riconciliazione generated/catalog/docs. B14+B07 resta attivo anche dopo U2 per continuare il consolidamento visuale e delle superfici secondo l'uso reale dell'app.
