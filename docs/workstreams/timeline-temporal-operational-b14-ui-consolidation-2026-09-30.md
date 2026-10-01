# B14 + B07 — consolidamento prodotto e UI guidato dall'uso

- **Stato:** ATTIVO — U2 CLOSED / PROVEN; U3+ UI consolidation corrente
- **Avvio:** 2026-09-30
- **Riconciliato:** 2026-10-01
- **Branch:** `feature/timeline-temporal-operational`
- **Base chiusa:** B00–B13 e B12
- **Frontiera persistence corrente:** `20261001_95`
- **Frontiera catalogo provata:** `_95` / `196|5|157|100|397|344|503|0|0|0`
- **Gate U2:** `docs/workstreams/timeline-temporal-operational-b14-u2-gate-2026-09-30.md`
- **Chiusura U2:** `docs/workstreams/timeline-temporal-operational-b14-u2-closure-2026-10-01.md`
- **Generated U2:** `dd94c6ee876bf5e671a516898b064c37e2d90741`
- **U3 handoff corrente:** `docs/workstreams/timeline-temporal-operational-b14-u3-handoff-2026-10-01.md`
- **Ultimo gate web locale completamente verde:** `899f9260` — typecheck + 16/16 focused PASS
- **Ultimo rerun U3:** `5c3634d4` — typecheck PASS, 16 focused PASS / 1 FAIL; failure circoscritto al globo Quick ancora montato in Advanced
- **Fix candidate successivo:** `1e0ef2f9` + `08478d93`; richiede nuovo gate locale
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
| U2 | Quick Create canonico: date, Life Area opzionale, colore, location, descrizione, authoring Activity/Event | **CLOSED / PROVEN 2026-10-01** | `_95`; catalogo e generated riconciliati; gate locale verde |
| U3+ | polish e organizzazione UI | **ATTIVO** | planning tray unificato, Advanced centrale, Reminder/verification separation, all-day esplicito; candidate corrente da provare |

## U2 — decisioni canoniche chiuse

### Oggetto e collocazione

- Quick Create espone **Activity** ed **Event** come capability correnti.
- `Timer` e `Sveglia` restano entry future disabilitate finché non esiste il relativo vertical.
- Collocazione rapida: `Orario`, `Tutto il giorno`, `Da collocare` per Activity ed Event nel ciclo U3; l'assenza di placement resta distinta dalla semantica di Event posticipato.
- La vecchia `Fascia` non è una quarta semantica di collocazione Quick: le fasce orarie sono shortcut del controllo inizio/fine.

### Intervallo temporale

- Modalità `Orario`: due date esplicite e sempre visibili attorno ai due orari: `data inizio | ora inizio → ora fine | data fine`.
- Le date usano un picker DANTE controllato, non l'input data nativo del browser; nessun comando browser `Cancella` fa parte del prodotto.
- Ora e minuti restano editabili da tastiera e tramite stepper; l'orologio apre gli orari a passi di 15 minuti.
- Le fasce `Mattina/Pomeriggio/Sera/Notte` appartengono al comando tra inizio e fine e impostano entrambi gli estremi.
- Multi-day esplicito: nessun rollover nascosto della sola ora finale.
- La UI produce una Schedule canonica attraverso il contratto di placement U2; le date UI non diventano una seconda fonte di verità.

### Life Area, colore e Tag

- **Life Area opzionale** per nuova Activity/Event.
- Assenza = vero stato canonico `null/unassigned`; nessuna Life Area fittizia `-`, `Personal` o equivalente.
- Campo Quick `Life Area (opzionale)` scrivibile/selezionabile.
- Un nome nuovo resta solo nel draft e viene creato atomicamente soltanto quando `Aggiungi` viene accettato.
- Se il comando complessivo fallisce, non resta una Life Area orfana.
- Selezionare una Life Area esistente usa colore/revisione canonici senza creare una nuova revisione.
- Cambiare esplicitamente il colore di una Life Area selezionata produce un update revision-guarded.
- Senza Life Area, un colore scelto è override dell'item.
- I Tag B05 restano capability canonica secondaria molti-a-molti ma sono fuori dal Quick Create.
- Il pannello storico `Life Area e Tag` non viene rimosso finché le capability di gestione ancora necessarie non hanno una destinazione equivalente.

### Location e descrizione

- `location` è opzionale sia per Activity sia per Event.
- `description` è opzionale e persistita canonicamente.
- Location/description non sono Schedule, Context, Life Area o Tag.

### Colore

- `activity_intention.color_code` / `event_expectation.color_code` possiedono l'override item.
- Il colore della Life Area resta actor-local organization state.
- La Timeline può proiettare l'apparenza accettata ma non diventa proprietaria di quella verità.

## U2 — implementazione chiusa

### Persistence / backend / API

- `865f458e` — contratto U2 iniziale.
- `48bb8d1e` — migration forward-only `20260930_94_b14_u2_optional_authoring_metadata.py`.
- `_94` aggiunge `description`, `location`, `color_code` a `dante.activity_intention` e `dante.event_expectation` con vincoli DB.
- `_94` aggiunge wrapper bounded `create_self_activity_authoring(...)` e `create_self_event_authoring(...)`; runtime non riceve direct-write sui descriptor.
- `20261001_95` ripristina forward-only il read ACL storico sui descriptor dopo il revoke troppo ampio di `_94`; direct write resta negato.
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
- `dd94c6ee` — OpenAPI + generated TypeScript/Zod client U2 rigenerati e pubblicati.

## Frontiera DB / Dictionary provata

```text
Alembic head         20261001_95
tables               196
views                   5
routines               157
triggers               100
physical indexes       397
foreign keys           344
check constraints      503
domain/enum              0
sequence/matview         0
policies                 0
```

Dictionary e test di catalogo descrivono la stessa topologia. Le due nuove routine U2 e i sei CHECK metadata sono registrati; le vecchie descrizioni B05 che implicavano Life Area obbligatoria sono state superseded.

## Gate U2 — PROVEN

Chiusura dettagliata:

`docs/workstreams/timeline-temporal-operational-b14-u2-closure-2026-10-01.md`

Evidenza locale riportata:

```text
Alembic current                         20261001_95 (head)
focused U2/B05/B03/backend regressions  PASS
U2 API unit contract                    PASS
web typecheck                           PASS
web focused suite                       8 files / 26 tests PASS
api-client typecheck                    PASS
generated:check                         PASS / deterministic
final current catalog pair              8 passed in 30.04s
```

Nessuna CI/GitHub Action è stata usata.

## Confine temporaneo con Advanced

U2 chiude il **Quick authoring compatibile**. Le capability avanzate storiche che non sono ancora rappresentate dal DTO U2 non vengono semplificate o perse: il runtime rileva l'intento e resta sul percorso storico.

Questo è deliberato e temporaneo. U3+ deve migrare/organizzare le capability Advanced nella superficie centrale mantenendo lo stesso draft e poi ridurre progressivamente il fallback storico. Finché quel passaggio non è completo non è corretto affermare che ogni configurazione Advanced utilizzi già il DTO U2.

## Supersessione B05 deliberata

B05 resta valido per catalogo Life Area, assignment actor-local, colori e Tag, ma la precedente regola di prodotto “ogni nuovo planning item deve avere una Life Area primaria” è superseded da U2.

```text
Activity/Event may exist without Life Area assignment
absence of assignment != synthetic category
Life Area remains organization, not Domain ownership
Tag remains secondary many-to-many organization
```

## U3+ — decisioni correnti

Handoff dettagliato e gate corrente:

`docs/workstreams/timeline-temporal-operational-b14-u3-handoff-2026-10-01.md`

Decisioni già consolidate nel candidate:

1. planning tray `Da collocare` unico per Activity non collocata, Event mai collocato ed Event posticipato, senza collassarne identità/storia;
2. Event può essere creato direttamente `Da collocare`;
3. Advanced è una superficie centrale viewport e conserva lo stesso draft del Quick;
4. `Ricorda` è un solo controllo principale: si configura prima del submit; la scrittura B11-C avviene dopo l'authoring solo perché necessita del `schedule_ref` accettato;
5. `Reminder configuration != notification delivery`: il delivery viene affrontato alla fine del consolidamento;
6. Quick `Orario` mantiene il globo compatto; Advanced espone esplicitamente `timeMode` + `timeZoneId` e non monta il globo Quick;
7. `Verifica esito` è distinta dal Reminder e dalla B10 `Confirmation`; per ora espone solo la policy realmente supportata;
8. `Tutto il giorno` usa due date esplicite sia per Activity sia per Event e non inventa fuso/orario su un date-span;
9. `Da collocare` non mostra `Ripeti` né `Ricorda`;
10. `Aspetto` Advanced è superseded dal controllo canonico Life Area + colore del Create ed è stato rimosso insieme a componente/stili non più referenziati;
11. Session / Actual / Outcome / Confirmation / Reconciliation restano temporaneamente visibili nel planning tray finché non viene costruita la destinazione sostitutiva; solo allora verranno rimossi da `Da collocare`.

## Cursor U3+

L'ultimo rerun utente sul candidate `5c3634d4` ha dato `web typecheck PASS`, `composer 2/2 PASS`, `entry U2 9/9 PASS`, `top/U1 5/6 PASS`. L'unico failure era coerente con una vera incoerenza UI: il Core montava ancora il globo Quick mentre Advanced mostrava già i controlli espliciti del fuso.

Il candidate corrente aggiunge:

```text
1e0ef2f9  Core timezone affordance renderizzata solo quando richiesta
08478d93  Composer passa showCompactTimezone=false in Advanced
```

Il prossimo passo è:

1. rieseguire il gate web indicato nell'U3 handoff;
2. se verde, fare la verifica reale dei punti colore / all-day / Reminder / Advanced;
3. continuare l'information architecture Advanced Activity vs Event;
4. integrare B04 vincoli temporali + movement policy nella superficie Advanced;
5. progettare e spostare Session / Actual / Outcome / Confirmation / Reconciliation prima di ripulire definitivamente il planning tray;
6. definire il sistema di delivery delle notifiche Reminder solo verso la fine del ciclo.
