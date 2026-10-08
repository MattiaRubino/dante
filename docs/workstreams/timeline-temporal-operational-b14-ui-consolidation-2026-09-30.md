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
- **Ultimo gate web locale completamente verde:** `779fa723` — typecheck PASS + 17/17 focused PASS
- **U3 Create/Advanced provato fino a:** Quick/Advanced timezone split, Reminder unico, Verifica esito separata, all-day esplicito, Aspetto rimosso
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
| U3+ | polish e organizzazione UI | **ATTIVO / CURRENT CREATE SLICE PROVEN** | planning tray unificato, Advanced centrale, Reminder/verification separation, all-day esplicito; prossimo checkpoint = verifica UI reale + IA Advanced |

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

Decisioni già consolidate nel candidate e ora coperte dal gate focused verde a `779fa723`:

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

Il rerun utente sul branch a `779fa723` ha chiuso il precedente mismatch del globo Advanced:

```text
web typecheck                 PASS
composer                      2/2 PASS
entry U2                      9/9 PASS
top/U1                        6/6 PASS
focused total                 17/17 PASS
```

Il current Create slice U3 è quindi provato lato automated focused gate. Il prossimo passo è:

1. fare la verifica UI reale dei punti colore / all-day / Reminder / Advanced;
2. continuare l'information architecture Advanced Activity vs Event sulla base di ciò che emerge visivamente;
3. integrare B04 vincoli temporali + movement policy nella superficie Advanced;
4. progettare e spostare Session / Actual / Outcome / Confirmation / Reconciliation prima di ripulire definitivamente il planning tray;
5. definire il sistema di delivery delle notifiche Reminder solo verso la fine del ciclo.

## 2026-10-06 — compact closure cursor

The remaining Create work is intentionally compressed into three coherent batches documented in `timeline-temporal-operational-create-closure-mini-roadmap-2026-10-06.md`: (A) Event/Scaletta/B09/common parity, (B) shared Reality + Objectives, (C) cleanup + closure gate. Avoid further prototype-only fields or artificial micro-slices.

## 2026-10-06 — Today verification rail candidate

- The Today row extends downward by 48 px; Timeline, Context Rail and Quick Create share the same bottom boundary.
- The derived Resolution Queue at forward revisions `20261006_116`–`20261006_117` reads explicit shared Reality review policy (while respecting legacy Activity policy only when no shared policy exists) and unassessed Objectives. Activity work requires a completed bounded Session; Event/Occurrence work requires an ended current placement resolved in the effective IANA zone. A missing Actual is never inferred as a failure.
- The lower Context Rail lists pending Reality, Objective and B10 Reconciliation cards. Reality actions record the exact Session timing basis when provided; Objective controls use the canonical Observation/Evaluation endpoint and refresh the queue after mutation.
- Date-only Event placements use the exclusive local end date in the effective zone. Historical review and post-creation editing remain separate product work; no completed-state register is presented by this candidate.
- Candidate is unproven until the user-run local migration, focused backend/web and real-app checks pass. No CI or GitHub Actions are requested.

## 2026-10-08 — Activity Inspector / edit checkpoint

Branch candidate `6f6e60eb` adds one self-scoped edit snapshot request backed by a single SQL statement. It includes current Activity placement rows, planned Session Schedule rows, Objective evaluations, life area, capture/reality policies, the primary placement lock and Reminder. The Activity ID and authenticated self identity bound the read; this is a read model, not a second truth store. No latency benchmark or PostgreSQL execution proof is claimed.

The editor's metadata, capture and reality changes now use one guarded HTTP command and one database transaction. Each existing canonical mutation retains its own idempotency/CAS authority, and a failure rolls back the group. The web typecheck, focused 8 tests and affected ESLint checks passed in the coding workspace. The focused PostgreSQL snapshot/rollback tests and Ruff require the user's local Python/PostgreSQL environment; they are unreported.

This is **not** whole Inspector/edit closure. Editing or adding/removing accepted Activity intervals and planned Session Schedules, changing Objective definitions, full Reminder and organization editing, faithful duplication of every form, recurring scope, generated OpenAPI/client, and real-app visual acceptance remain open. Direct interval Schedule mutation remains blocked until a coordinated replan preserves the envelope, placement constraints and history.

### Local gate for the verification rail candidate

The user runs these checks in `~/projects/dante` after pulling the branch; no CI is run. The API response adds `objective_review`, so regenerate the checked-in client before checking its determinism. Review and publish generated file changes as generated output only.

```bash
pnpm api:generate
pnpm generated:check
pnpm --filter @dante/api-client typecheck
pnpm --filter @dante/web typecheck
pnpm --filter @dante/web exec vitest run \
  src/features/home/ui/context-rail/context-rail.test.tsx \
  src/features/temporal/actual-realization-controls.test.tsx \
  src/features/home/ui/home-page.test.tsx
cd apps/backend
uv run --locked pytest -q --no-cov --tb=short -m postgres \
  tests/integration/temporal/test_b14_resolution_reality_objectives.py \
  tests/integration/temporal/test_b14_u6_reality_policy.py \
  tests/integration/temporal/test_b14_u6_resolution_queue.py \
  tests/integration/database/test_current_catalog.py \
  tests/integration/database/test_database_current_catalog.py
uv run --locked ruff check \
  migrations/versions/20261006_116_b14_resolution_reality_objectives.py \
  migrations/versions/20261006_117_b14_resolution_effective_zone.py \
  src/dante/modules/temporal/resolution_queue_api.py \
  tests/integration/temporal/test_b14_resolution_reality_objectives.py
```

Visual acceptance: a completed real Session with `Chiedi al termine` yields one Reality card; an unassessed Objective yields its own card independently. A past timed or all-day Event with the same explicit policy yields a Reality card. Registering an Actual with the exact Session basis or an Objective result removes only its corresponding pending card. Quick Create and the rail share the new lower edge.

## 2026-10-08 — Activity Inspector post-create continuation (candidate)

The user requested completing the Inspector's real post-create edit/duplicate vertical
before visual polish. Branch baseline was `24b3b934`, which already includes Activity
profile/policy/reminder editing, coordinated time replan, and adding/removing planned
Session Schedule rows. The accepted semantic boundary remains
`Activity != Schedule != Session != Actual`.

This continuation wires two additional **existing canonical capabilities**:
- change an Activity's primary Life Area through the self-scoped
  `life-area-assignments/activities/{ref}` endpoint using the accepted
  assignment revision and a retry-stable operation ID;
- protect/unprotect its accepted envelope Schedule through the existing
  `placement-lock` endpoint using expected-revision CAS.

Both operations invalidate authoritative Timeline/planning reads and do not invent
a parallel frontend truth. The post-create editor shows explicit individual
apply controls for these separate persistence transactions. Unsaved independent
edits prevent the general core Save and coordinated replan from closing the
editor and silently dropping intent. Focused web coverage was added for the
requests and the user interaction. **No local web, PostgreSQL, generated,
or real-app proof is claimed for this continuation yet.**

This is **not full Inspector/Edit/Duplicate closure**. Still open: revisioned
Objective definition edit/retire, null/unassign Life Area semantics, existing
Activity interval add/remove, existing planned Session title edits, recurring
edit scope, robust duplication of unsupported temporal/recurring forms,
and integrated real-stack acceptance. Do not represent these as implemented.
No CI/GitHub Actions were run.

## 2026-10-08 — Local gate blocker: B14 role capacity migration `_121`

User-run gate on the Inspector continuation: web typecheck succeeded, focused
Vitest 14/14 succeeded. All seven focused PostgreSQL tests stopped during
Alembic fixture setup, before functional assertions: `_121` attempted to
drop a non-existent, doubly convention-expanded CHECK identifier
(`ck_activity_schedule_role_ck_activity_schedule_role_ck__b98d`).

The physical CHECK installed by `_106` and listed in the Dictionary is
`ck_activity_schedule_role_ck_activity_schedule_role_order`. Because the
canonical naming convention itself prefixes `ck_<table>_`, the already
expanded name must be wrapped in Alembic `op.f(...)` on both drop/create.
This is an exceptional in-place correction to a candidate migration that
failed before application; a later migration could not repair an earlier
migration that never completes. It does **not** change the accepted rule,
drop user data or rewrite any applied placement history.

Post-fix PostgreSQL test results remain pending. Do not claim functional
backend proof from the seven setup errors; rerun the focused gate first.

## 2026-10-08 — Inspector PostgreSQL gate, second iteration

User-reported local result after the _121 naming repair: Ruff PASS;
15 focused PostgreSQL/catalog tests executed, **12 passed / 3 failed**.
The earlier 7 fixture setup errors disappeared. Remaining failures:
(1) Activity replan replacement attempted a direct runtime SELECT from
`session_planned_schedule_link`, which is deliberately owner-only;
(2–3) current catalog test constants still identified `_120`.

Follow-up implementation switches execution-provenance lookup to the already
granted, self-scoped `list_self_subject_sessions` and
`get_self_session_planned_schedule` functions; historical role-slot allocation
also switches to `get_self_activity_schedule_roles` to prevent the next
owner-only SELECT failure. Runtime table privileges are **not broadened**.
Both catalog test constants now specify `20261008_121`. A positive
PostgreSQL regression assertion exercises linked Session readback via the
canonical owned functions.

These edits are published but **not yet verified by a fresh user-run local
PostgreSQL gate**. Until that gate reports success, the complete Inspector
post-create vertical remains open.

## 2026-10-08 — Activity Inspector interval editor vertical (candidate)

The user-run Inspector DB gate at commit `aa781443` is **GREEN**:
Ruff PASS and **16/16** focused PostgreSQL/catalog tests passed in 46.46s.
This supersedes the earlier 12/15 result for the owned-function fixes.

The new candidate extends the coordinated `ActivityReplanCommand` and editor to
**add/remove existing Activity-owned interval Schedule rows**, alongside moving
existing intervals and adding/removing planned Session Schedule rows. The same
single transaction and mandatory preview preserve these invariants:
- every current interval and planned Session row must be explicitly retained or
  removed by matching its accepted placement state (CAS);
- one to 100 current Activity intervals, max 100 current planned Session rows,
  ordered non-overlapping intervals, bounded planned Session envelope;
- the envelope derives from the current intervals; all rows share temporal form
  and zone, no inferred timezone changes;
- removed intervals are **unscheduled, not deleted**. Historical Schedule role
  identity and past role slots are retained; new rows receive new Schedule UUIDs
  and monotone role order. No Session/Actual execution history is copied;
- placement locks, open execution and accepted Actual block affected editing;
  no direct runtime access to private PostgreSQL tables.

The backend request adds `new_intervals` and `remove_intervals`, both
explicitly bounded; frontend preview now renders `interval_added` and
`interval_removed`. Unit, PostgreSQL and web interaction/contract tests were
added to prove replacement, preserved historical identity and no silent
mutation. This is **IMPLEMENTED / NOT YET PROVEN** until the user's local
Ruff, unit, PostgreSQL, web, generated OpenAPI/Orval/client and visual gates
pass. The generated OpenAPI/client must be regenerated by the canonical
`pnpm api:generate` tool; never hand-edit generated sources.

This only closes the interval add/remove implementation candidate. Overall
Inspector/Modifica/Duplica closure still requires post-create Objective
definition lifecycle, optional Life Area unassignment, faithful advanced
duplication, existing planned Session display-name evolution, recurring scope,
and real-stack product acceptance.

## 2026-10-08 — User local interval-editor gate and fix

The first user-run interval-editor gate at `7a2a3a1a` reported:
`pnpm api:generate` PASS; `generated:check` PASS, **483 sources
deterministic**; web/api-client TypeScript PASS; focused Vitest **15/15 PASS**.
Backend Ruff had 2 style findings (RUF021 operator precedence and RUF001
ambiguous EN DASH), focused unit **3/4 PASS** and PostgreSQL **14/15 PASS**.
Both functional failures share a concrete bug: the pure preflight loop
dereferenced `by_ref[row.schedule_ref]` for an Activity interval explicitly
listed under `remove_intervals`, causing `KeyError` *before* preview/apply.

The follow-up source fix `1156186d` filters both prior Activity intervals
and planned Session rows to retained IDs before the placement revision loop.
The separate, explicit removal-preview and unschedule phases remain intact.
The two Ruff findings are also corrected. **Post-fix unit/Ruff/PostgreSQL
gate remains pending; do not assert closure**.

User-local API generation created six legitimate uncommitted generated
artifacts (OpenAPI JSON, model index, ActivityReplanCommand model, apply/preview
models and NewIntervalRow model). They passed deterministic verification but
still must enter the Git branch via generated-source tooling output; they must
not be discarded or hand-edited. No CI or GitHub Actions were used.
