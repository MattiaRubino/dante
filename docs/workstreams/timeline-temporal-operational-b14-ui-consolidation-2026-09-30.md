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

## 2026-10-08 — Activity interval editor focused gate GREEN

The user ran the post-fix local gate after commit `d084e6e9`, reporting:
- `ruff check` **PASS / exit 0** for the changed backend and test files;
- `tests/test_b14_activity_replan.py` **4/4 PASS / exit 0**;
- focused temporal replan, edit snapshot, planned Session link and exact catalog
  PostgreSQL suites **15/15 PASS / exit 0**, 32.62s.

The immediately preceding same-source frontend/generated gate reported:
- canonical `pnpm api:generate` **PASS**;
- deterministic `pnpm generated:check` **PASS** (483 files);
- web and API-client TypeScript **PASS**;
- focused Vitest **15/15 PASS**.

Thus **Activity interval add/remove + coordinated replan automated scope is
PROVEN by focused local tests**, including historical Schedule-role retention.
It still lacks a separate user-reported real-app visual/dogfood acceptance.
The six canonical generated OpenAPI/Orval outputs exist as *uncommitted edits
in the user's local worktree*, NOT yet in this GitHub branch. The user must
publish the exact generator-produced files without rewriting or discarding them.
No CI/GitHub Actions were run.

This does not close all Activity/Event Inspector/Edit/Duplicate: Objective
definition lifecycle, planned Session title revisions, optional Life Area
unassign, recurring edit scope, robust duplication and real-stack acceptance
remain outstanding.

## 2026-10-08 — Generated interval-client publication and Objective post-create addition

The user published and pushed canonical OpenAPI/Orval artifacts in
`c22f04ae`. GitHub branch HEAD confirmed and the generated
`newIntervalRow.zod.ts` path verified without any literal backslash.
This completes the repository-publication step following the already green
interval editor automated gate. Visual/real-stack acceptance is still pending.

The next **bounded candidate** exposes post-create Activity Objective **ADD**
using the existing self-scoped, idempotent Objective create endpoint and current
editor snapshot. The editor now supports boolean, quantitative comparator,
qualitative, and numeric range definitions; a separate write action and
readback; stable operation ID across transport-error retries; no alteration of
prior Objective observations/evaluations. Current objectives stay read-only.
An unsaved Objective draft is included in close/discard guards and blocks
accidental main core form submission. Focused remote-contract and UI tests
were added. **User-run typecheck/Vitest are pending**.

**Not implemented yet**: definition retirement and replacement/versioning with
historical evaluation semantics, accepted reorder and existing Objective edits;
planned Session display-name evolution, Life Area unassign, recurring update
scope, advanced faithful duplication and whole Inspector/Event reconciliation.
Do not describe the new Objective ADD slice as complete Objective lifecycle or
finished Inspector.

## 2026-10-08 — Post-create Activity Objective ADD user local gate GREEN

The user's exact focused local gate after `d5da6d3e` reports:
`pnpm --filter @dante/web typecheck` exit 0;
`pnpm --filter @dante/web exec vitest run` over
`activity-inspector-actions.test.tsx` and
`remote-activity-edit-settings.test.ts`: **17/17 passed** (12+5),
exit 0. No CI/GitHub Actions. This provides focused automated proof
for adding an Objective after creating an Activity, including retry
operation IDs and readback through the canonical authoring endpoint.
It does **not** prove editing/retiring previously accepted Objective
definitions, cross-Occurrence updates, or the full Inspector real-app UX.
Next semantic gate: change Objective definition without retroactively
reinterpreting recorded observations and accepted evaluations.

## 2026-10-08 — Canonical selected-instance edit scope and past-fact corrections (user-corrected product rule)

**AUTHORITY: this section replaces the earlier Objective lifecycle design gate and
any earlier prose proposing an unanchored "future-only" edit from a selected past
instance.** This is the active B14/B07 product decision for **all edits**
(Activity, Event, recurrence-derived instances, Objectives and other editable
capabilities), not an Objectives-only rule. It governs modification targeting;
separate domain safety and write-authority checks still apply.

### Scope in the save UI (recurring instances only)

Only TWO scope labels:

1. **Solo questa** — the **selected/clicked instance only**, regardless of
   whether it is past, current or future.
2. **Questa e le prossime** — the **selected/clicked instance ALWAYS**, plus
   the future instances of the same recurrence which occur after the selected
   instance. Never silently reprocess any *other* already-past instance.

This is **not** "Le prossime" without the selected one, and not a retroactive
"tutta la serie". The clicked item is always the temporal anchor. For a
non-recurring Activity/Event the only target is that individual item.

For a concrete chronological timeline

```text
past      1   2   3  | NOW |  4   5   6      future
select 1; Solo questa            -> 1
select 1; Questa e le prossime   -> 1 + 4 + 5 + 6  (NEVER 2,3)
select 4; Solo questa            -> 4
select 4; Questa e le prossime   -> 4 + 5 + 6
select 5; Questa e le prossime   -> 5 + 6         (NEVER 4)
```

General predicate for "Questa e le prossime": include the selected instance
as its own branch; for **additional** instances include only those (a) of the
same recurrence, (b) strictly later in recurrence ordering than the selected,
and (c) future at the time the command is accepted. Past instances between a
selected past anchor and the present remain untouched. The meaning of current,
past and future must use canonical temporal/occurrence state and a controlled
time boundary, not an arbitrary browser-local comparison. Scope and the exact
affected instance set must be confirmed by preview/CAS at persistence, with
no silent skipping of separately customized future items.

### Historical records and Objective facts

The user-authored **current accepted value is authoritative**. DANTE must
not infer or ask *why* the user is correcting an earlier value. An earlier
Activity/Event can be **fixed/corrected**, including previously defined
Objectives, recorded observations and assessments. Do not allow **deletion
of already-realized/recorded historical facts** in the past; support correction
to a new authoritative value instead. Historical correction of an Objective
must be in-place from the product user's point of view: **same logical
Objective**, corrected current definition/assessment, *not* a new unrelated
visible Objective. Old persisted versions remain available privately for
audit/undo/history, never more authoritative than the corrected current value.

When an Objective target or a recorded result is corrected, reconcile the
current dependent assessment with the corrected data where computable. Never
fabricate a manual/qualitative assessment; obtain the needed user decision.
Do not silently mutate the older accepted evaluation records. The user's
correction to selected past item does **not** propagate to other past items,
even if the same recurrence generated them.

For **current/future** instances, ordinary modifications, removal of not-yet-
realized Objectives/planned content, and scoped updates are allowed where
the owning domain's rules permit. "Questa e le prossime" always includes the
selected item; historical-fact non-deletion continues to hold even when a
scope command begins on a past item. The UI must disable/deny an action that
would delete the selected past fact, rather than secretly applying that
deletion only to later items.

### Persistence boundaries and still-open work

The existing `temporal_objective` is keyed by `objective_ref`, with
Observation/Evaluation bound to this identity. The API currently supports
create/record/list but **no change of existing definition, correction,
retirement, scoped recurrence edit or reorder**. The 17/17 focused frontend
gate proves **ADD only**.

Next implementation must provide current logical Objective identity and
append-only definition/correction history, explicit current-state readback,
CAS/idempotency and self-owner security; retain historical Observation/
Evaluation identities. Past corrections become canonical without
destructively updating old records. Future Objective retirement/removal
must not appear as an accepted historical-fact delete. For recurring
Activity/Event, distinguish materialized instances from recurrence policy;
never equate Routine, Recurrence, Occurrence and Schedule.

Mandatory proof scenarios include exact target sets 1 versus 1+4+5+6,
4 versus 4+5+6 and 5+6, no touch to 2/3 when editing 1, no future-only
scope from a selected 1 or 4, correction of evaluated past Objectives/
observations preserving old audit versions, no deletion of past recorded
facts, current/future removal, owner isolation, replay/CAS/conflicts,
individual overrides, and Event/Activity parity. Only mark implemented
after forward migration + ORM/Database Dictionary exact catalog +
API/OpenAPI/generated client + web tests + user-run real-app proof.

**Status: USER-APPROVED DESIGN DECISION / IMPLEMENTATION OPEN.** The prior
design requiring a newly visible successor Objective for every edit, and
past-anchor "Le prossime" excluding the clicked instance, are explicitly
**superseded**.

## 2026-10-08 — Consolidated Inspector / Edit / Duplicate delivery cursor

This checkpoint was reconciled against the **live GitHub branch at
`39e8ab961e98efe8c5fa5b329c5a91f125007714`**, including roadmap,
map, handoff, DB overlay/Dictionary, _121 migration, backend API, web
Inspector/Edit/Duplicate, recurrence authoring and user-run local gates.
It does not claim a fresh local test run after this documentation checkpoint.

### Closed with explicitly reported focused proof

- B01–B13 remain closed at their **qualified evidence levels** recorded
  in their own closure files. B14+B07 and final B15 are active/open.
- Create Activity/Event consolidation (Reality + Objectives, Activity planned
  Sessions, Event Scaletta/participants and common recurrence/Reminder)
  has its **reported automatic gate**, not a universal post-create dogfood
  pass. Life Area in one-off/recurring Create is **frozen** on 13/13
  focused web and 4 real-stack Chromium/Firefox cases (WebKit intentionally
  skipped). The Create UI does not expose Sub-Activities.
- Activity post-create **Inspector profile, combined core editor, Life Area
  reassignment, envelope placement protection, placement planning, new/
  removed planned Session Schedule rows** have implemented frontend/API
  paths with focused snapshot/replan tests. Do not confuse partial
  coverage with a final combined Inspector real-app acceptance.
- Activity interval **reposition / add / remove**, coordinated with envelope
  and planned Session Schedule rows: canonical preview + CAS/atomic apply,
  history-preserving unschedule. User-run gate after `d084e6e9`: Ruff
  exit 0; 4/4 backend unit; 15/15 focused PostgreSQL/catalog; earlier
  frontend gate 15/15, web/API typechecks and deterministic generated check
  483. Canonically generated six OpenAPI/Orval files were pushed to the
  branch in `c22f04ae`. **Focused automation PROVEN; real-app UX pending.**
- Add **new** Objective post-Create in Activity editor: user-run
  `pnpm --filter @dante/web typecheck` exit 0 and focused Vitest
  17/17 exit 0 (12 UI + 5 remote). Existing Objective definitions remain
  read-only in this editor. This proves the focused web authoring slice,
  **not edit/correct/remove or cross-recurrence behavior**.

### Accepted policy, NOT implemented

The user-approved **global modification scope** in the preceding section
supersedes all old "future-only" options: **Solo questa** vs
**Questa e le prossime**; both always include the selected/clicked instance.
Selecting past #1 among past #1/#2/#3 and future #4/#5/#6 yields
`{1}` or `{1,4,5,6}`, **never #2/#3**. Selecting future #4
yields `{4}` or `{4,5,6}`. Other past records stay untouched.
Past factual/Objective records may be corrected and the user's corrected
value becomes current canonical truth; they cannot be deleted.
Future/unrealized content may be edited/removed in its owner-approved scope.
Keep append-only internal history and reconcile dependent evaluation without
inventing qualitative/manual judgments. The policy applies to **all**
relevant Activity/Event fields and modifications, not just Objectives.

### Open implementation gaps, ordered by dependency

1. **M1 — Cross-cutting recurrence edit scope and authoritative targeting.**
   One selected-instance anchor, canonical past/current/future classification,
   current accepted Recurrence/Occurrence association, future-instance
   propagation with explicit exception/override handling, bounded preview,
   idempotent self-scoped CAS/rollback. No mutation to other already-past
   instances. Do not silently update generated Occurrence vs Activity identities.
2. **M2 — Editable Objective lifecycle and correction of recorded facts.**
   Maintain one logical product Objective identity with immutable definition
   versions/current binding, allow corrections to old target and old observed
   result, update current dependent deterministic Evaluation while preserving
   previous assessments, ask for manual reassessment when necessary.
   Current/future removals and accepted reorder; retirement not destruction
   of historical facts. Scope consistently in Activity **and Event**.
   Present backend currently only creates/lists/records Objectives.
3. **M3 — Remaining post-create Activity editor breadth.**
   Rename existing planned Session display names without replacing a
   Schedule/execution history; primary Life Area **unassign/null** (current
   API only assigns another valid area); other unhandled Create settings/
   temporal forms; confirm Reminder/policy paths and guarded operation
   boundaries. Audit `ActivityInspectorActions` current `Elimina` action
   (Activity retirement) against the approved no-deletion-of-past-recorded-
   facts policy: do not assume existing retirement is safe in every case.
4. **M4 — Duplication and Event Inspector parity.** Activity Duplica
   seeds metadata, intervals, planned Sessions, Objectives and some policy,
   but rejects unsupported stored temporal forms, and recurring-template
   duplication is not faithfully implemented. Must not copy past Actual,
   Observation, Evaluation, execution sessions, historical operation IDs or
   authority as if new facts. Event has working B03 lifecycle/Scaletta
   editing but **not** the equivalent complete Inspector/Edit/Duplicate
   product flow. Include Event-specific attendees/Scaletta semantics,
   common fields and Event Occurrence vs source identity; do not transfer
   Activity-only intervals/Session semantics to Event.
5. **M5 — Whole product acceptance and B15.** Desktop/mobile layout,
   focus/keyboard/panel lifecycle and unsaved-change guard; real-stack
   one-off/recurring Activity/Event tests, present/past/future edits, scopes
   `1` vs `1+4+5+6`, revisions and replay, failed operations,
   duplicates, null Life Area, Objective correction/deletion limits;
   exact migration + SQLAlchemy/Dictionary/ACL/catalog reconciliation;
   canonical OpenAPI/client generation, focused backend/web tests and
   user-run visual acceptance. No GitHub Actions or CI.

### Exact next execution

Start with **M1 bounded scope foundation and tests**, then make M2 Objective
edit/correction consume that shared selection contract; avoid implementing
incompatible one-off Objective edit and later duplicating scope semantics.
Before changing the database, inspect the current B06/B11 recurrence/
checkpoint and _113 Objective definition ownership/Observation/Evaluation
invariants. Continue to use live GitHub as source of truth; user executes
tests only in local WSL `~/projects/dante`. No remote CI.

**Status: CHECKPOINT DOCUMENTED / M1–M5 OPEN.** No code, migrations,
client artifacts or frontend were changed by this checkpoint.

## 2026-10-08 — M1-A canonical recurrence edit target selector (candidate)

After verifying existing B06/B11 authority, **reuse** the already deployed
Routine/Event Recurrence GET/replace endpoints, historical Recurrence state
and idempotent CAS, B06 Occurrence identity/checkpoint, typed coordinate,
skip/exclusion, and B14 materialization to Activity/Occurrence. Do not
reimplement these capabilities. Existing APIs allow editing a recurrence
rule or one Occurrence, but **do not yet expose a shared command that
applies arbitrary Activity/Event edits to the selected instance and all
eligible next future instances atomically**.

M1-A implementation adds the **pure, fail-closed target selection**
`occurrence_edit_scope.py` with focused unit tests. It encodes exactly
two scopes: `only_this` and `this_and_following`, both including the
clicked Occurrence. The latter additionally picks only later future
recurrence-generated Occurrences under an acceptance-time, aware instant;
already-past neighbors remain untouched. Upcoming explicit extras are not
mistaken for generated following Occurrences; overridden, skipped or
already-realized *other future* candidates are surfaced as blocking
conflicts instead of silently overwritten. The plan distinguishes
accepted per-instance target refs from a required future source-template
revision, so not-yet-materialized future instances must inherit the new
accepted policy. Equal-time anchor ties, naive clocks, duplicate refs,
mixed owner sources, absent clicked target, incomplete inventory and
unbounded candidate sets fail closed.

This is **pure selection only**. No API route, DB read or mutation has
been added. It does NOT claim owner verification on its own, because
that must be supplied by self-scoped guarded database capabilities; nor
does it claim transactional CAS, exhaustive future enumeration or
Event/Activity apply wiring. These are next, and require an authoritative
bounded current inventory plus recurrence source revision with a
save-time re-read/compare-and-swap transaction. The callback must never
accept a client-submitted list as proof of self scope/completeness.

Tests to run **locally by the user**: backend Ruff for the new core and
test file, plus focused unit `tests/test_b14_occurrence_edit_scope.py`.
Status **IMPLEMENTED CANDIDATE / USER UNIT GATE PENDING**. M1 overall
remains OPEN; B14/B07 remains ACTIVE.

## 2026-10-08 — M1-A first user local gate: 18 unit pass; Ruff repair

User-run focused local gate after `4f50c0d3`:
`pytest -q --no-cov --tb=short tests/test_b14_occurrence_edit_scope.py`
**18 passed / UNIT=0**; Ruff reported exactly one non-semantic
`RUF005` in `test_b14_occurrence_edit_scope.py:231` (tuple
concatenation; `RUFF=1`). Follow-up commit `7ef6a32f` replaces
tuple concatenation with iterable unpacking while keeping exactly the
same test data and target-selection semantics.

**Status**: 18 unit tests user-green on prior commit;
Ruff fix pushed but rerun **pending**, no PostgreSQL/API/web/apply gate.
Do not reopen the successful unit coverage solely to check formatting.
M1 remains OPEN. Next is the authoritative self-scoped Recurrence/
Occurrence inventory and transactional CAS preview/apply boundary;
B06/B11 existing functions must be reused.

## 2026-10-08 — M1-A proven; M1-B guarded materialized inventory candidate

User local rerun after `a62ab230`: **Ruff PASS / RUFF=0** and
`tests/test_b14_occurrence_edit_scope.py` **18 passed / UNIT=0**.
Close **M1-A pure selector** on focused unit proof; do not mark M1
complete or imply any accepted recurring edits.

**M1-B implementation candidate**, forward-only Alembic
`20261008_122_b14_recurrence_edit_inventory.py`:
- `dante.list_self_recurrence_edit_occurrences(uuid,uuid)` is a
  SECURITY DEFINER, self-owned read, authorized by existing B06
  `get_self_occurrence` for the selected Occurrence. It enumerates
  **all accepted materialized Occurrences** from the selected source,
  including skipped, current-Scheduled and explicit extra instances,
  without a browser Timeline window filter. It aborts above **10,000**
  accepted rows rather than returning a truncated inventory; grants
  EXECUTE only to runtime, not table SELECT/DML.
- `OccurrenceEditInventoryApplication.read` uses a database transaction
  timestamp and the canonical typed B06 row parser, verifies source
  consistency and selected identity. The GET endpoint
  `/api/v1/temporal/occurrences/{occurrence_ref}/edit-inventory`
  returns a read-only snapshot with explicit
  `materialized_only=true` and `apply_authorized=false`;
  unseen/unmaterialized future occurrences are **not** implied to be
  in the list.
- M1-B integration test checks Routine/Event parity, self isolation,
  skip, explicit extra, already-Scheduled selected row, endpoint
  response and role-grant boundary. Dictionary now registers 197
  routines, 231 tables, 5 views, 103 triggers, 471 indexes,
  405 foreign keys, 572 CHECK; current Alembic is `_122`.
  Both exact DB/catalog probes updated. No new physical tables/mappings.

**Proof pending**: user-run migration, focused PostgreSQL and exact
catalog checks, Ruff, OpenAPI schema/generation + API-client/web
typechecks. These have not been run by the assistant and are NOT
claimed green. The branch currently has no web save UI or actual
recurrence batch mutation. **M1-C still open**: prove full apply-time
inventory under concurrency, owner/Source CAS and replay, detect
overridden and already-realized future instances, resolve selected
Activity→Occurrence and Event source/Occurrence identity, and commit
the chosen change plus future source-template policy **atomically**.
Do not ever feed `materialized_only` snapshot into the pure
M1-A selector as if it proved future source-policy propagation.

No CI/GitHub Actions. User runs all gates in local
`~/projects/dante`.

## 2026-10-08 — M1 consolidated owner-scoped save candidate and whole-gate request

**User-run local proof of _122/M1-B (reported Oct 8):**
Ruff 0; focused PostgreSQL + exact current catalog **10 passed /
POSTGRES=0**; `pnpm api:generate` 0; deterministic
`pnpm generated:check` **484 current files / 0**; API and
web typechecks both 0. Generated client was left deliberately modified
locally: OpenAPI JSON, `generated/dante.ts`, model index,
`occurrenceEditInventoryResponse.zod.ts`. This is expected source
generation, not a failure. Do not claim these files already pushed.

**The following is a new, wider implementation candidate atop _122.**
Forward-only `20261008_123` adds the single append-only table
`occurrence_profile_edit` and five SECURITY DEFINER functions:
typed zone-aware occurrence ordering, current merged profile patch,
owned Activity→Occurrence lookup, current source edit CAS state,
and atomic accepted profile edit with immutable affected-ref receipt.
It reuses B06 immutable Occurrence ownership and _122 full inventory,
locks owner Recurrence source + current Recurrence state, CAS-checks
source profile edit revision and governing state, idempotently replays
the *same* operation, and rejects conflicting future local profile
overrides or recorded Actual/Objective Observations. A failed write
leaves no partial application or new accepted operation.

`Solo questa` addresses **the selected Occurrence always**.
`Questa e le prossime` addresses **the selected plus later future
same-source generated Occurrences**, excluding every other already-past
Occurrence. The immutable revision is the future inheritance policy:
current effective patch is determined for materialized past and future
and for later as-yet-unmaterialized future Occurrences. The receipt
contains the exact *currently materialized* affected refs; the
policy additionally affects unmaterialized future instances.

One-off Activity continues using existing core-edit. A
Routine-materialized Activity is mapped to its governing Occurrence
through a self-owned read; Activity Inspector projects the effective
accepted profile, Activity/Event Timeline projects the accepted title,
and newly created Routine-derived Activities inherit their accepted
title/description/location/color corrections at materialization.
The Activity editor now offers exactly `Solo questa` and
`Questa e le prossime` when editing the recurring Activity's
**general metadata**, using a stable retry operation ID and rejecting
mixed general-profile and non-profile saves rather than splitting a
single perceived action into multiple non-atomic writes. It sends
**only changed fields**, to avoid reverting unrelated future values.
The backend mutation endpoint also works for Event Occurrence metadata
without copying Activity Session semantics into Event.

Focused PostgreSQL integration tests cover: 1 vs 1+future targeting,
isolation of other past instances, unmaterialized future inheritance,
replay/fingerprint conflict, stale state, cross-owner refusal, Event
single-target and protected-future rejection, capability-only grants,
direct API read/save, and scheduled Event Timeline title readback. Focused web tests cover scope choice, accepted
remote operation payload and conflict handling. These are
**implemented but NOT YET USER-RUN**.

**Exact current Dictionary candidate:** _123, tables=232, views=5,
routines=202, triggers=103, indexes=473, FK=408, CHECK=576.
SQLAlchemy row and Dictionary parity updated. The `get_self_activity_profile`
function now uses PARALLEL RESTRICTED rather than SAFE due to its
effective scoped patch dependency. New API/schema requires a fresh
canonical OpenAPI/Orval generation, client typecheck, web and
PostgreSQL gates. No CI or GitHub Actions.

**Honest scope boundary:** M1 now has an implemented end-to-end
**metadata** recurrence edit candidate, including backend support
for recurring Event metadata, but it is not legitimate to label
ALL modifications closed. Existing Objectves, Reality,
Session/Scaletta, Reminder, Life Area, Schedule and other domain-specific
writes must consume the same selected-anchor contract with their own
audit/safety semantics (M2/M3/M4); the entire B14/B07 Inspector/Modifica/
Duplica journey and B15 visual acceptance remain OPEN. Recurring Event
Inspector UI parity is still M4. Do not silently broaden the metadata
route to accept unimplemented domain commands.

**Whole user gate once** (rather than piecemeal micro-gates):
Ruff _123 + all touched APIs/mappings/tests; PostgreSQL
`test_b14_m1_scoped_profile_edit.py`, `test_b14_m1_edit_inventory.py`,
both exact catalog probes, previous focused selector unit, touched
Activity/Event snapshot/integration tests; `pnpm api:generate`,
`pnpm generated:check`, TypeScript client/web typechecks and focused
Vitest Activity Inspector/remote recurring profile editor. Inspect
local generated diff, then commit canonical generated files once
after the entire gate is green.

## 2026-10-08 — M1 _123 local gate failures, _124 forward repair candidate

User actually ran the whole _123 local gate after `65519f96`.
**Result:** Ruff **1** (two I001 import order violations in
`occurrence_api.py` and `mappings/__init__.py`); 18 unit **PASS**;
PostgreSQL **16 PASS / 4 FAIL** (all existing B14 Activity
Inspector/edit-snapshot tests); OpenAPI generation **0**;
deterministic generation **489 files / 0**; API/Web typechecks **0**;
Vitest **21/21 PASS / 0**. New M1 scoped PostgreSQL tests and database
catalog tests were among the passing tests. Client source was
generated locally and remains uncommitted; **do not reset it**.

**Confirmed shared root cause:** `20261008_123` replaced
`dante.get_self_activity_profile` using a LATERAL subquery guarded
by a `WHERE origin.occurrence_ref IS NOT NULL`. PostgreSQL
inlining/optimization still evaluates the strict self-Occurrence
patch accessor with NULL for non-recurring Activity.
The accessor correctly raises `occurrence_edit_unavailable`; the
**caller is wrong**, not the access policy. All four existing
Activity read/edit tests fail with this same exception.

**Repair:** do not rewrite an already-executed _123 migration.
The appended forward-only `20261008_124` replaces only the existing
Activity profile read using explicit PL/pgSQL owner fetch and
`IF bound_occurrence IS NOT NULL` before invoking the strict
self-Occurrence patch function. Nonexistent/retired/cross-owner
Activity still returns no row. The equivalent one-off Activity
path in the Timeline SQL now uses a `CASE` guard rather than a
planner-flattenable `WHERE` in a LATERAL query. Both I001 imports
were reordered. The Dictionary updates the one existing routine's
language to PL/pgSQL and revision to _124, and catalog tests now
expect _124 with the exact **unchanged** topology
232/5/202/103/473/408/576. A targeted PostgreSQL regression test
verifies one-off Activity profile, cross-owner isolation and
scheduled Timeline projection.

**Status: _124 published as candidate, user-run gate PENDING.
Do not mark M1 or B14 accepted until the repaired whole gate runs.**
The _123-based 489-file generated client should be reproducible
under _124 because there are no API/schema type changes, but local
deterministic generation must confirm. No CI/GitHub Actions.

## 2026-10-08 — M1 recurring general-metadata automated technical closure (user confirmed)

**Local proof recorded:** After the _123 gate revealed a normal-Activity NULL-Occurrence regression, forward-only _124 guarded the one-off Activity read. User ran the unified _124 local gate: PostgreSQL PASS, deterministic `generated:check` PASS (489 files), API Typecheck PASS, Web Typecheck PASS, Vitest PASS. A single test-only Ruff DTZ011 was repaired in `62c18771`; the final user rerun then printed **All checks passed!** for Ruff. Git diff staged check passed and user committed/pushed nine generated OpenAPI/Orval files, `55a017b9`, 1,013 added lines, with clean `git status --short`. The earlier pure selector (18 unit PASS) and M1-B inventory (10 PostgreSQL PASS) are also user-proven.

**CLOSE M1 only for the recurring general-metadata vertical** (Activity UI, Event backend/Timeline, title/description/location/color metadata, owner/CAS/replay, accepted immutable audit, selected-anchor scope and future inheritance). Do not reopen B06/B11. This is focused *automated* closure, not visual dogfood. **M2** logical Objective definition correction and result/Observation correction remains OPEN; corrections to a selected historical Objective must become the current value of the SAME logical Objective, with internal version/audit preservation and no deletion of accepted past facts. Subsequent dependent evaluation must be deterministically refreshed or explicitly non-reinterpreted; never fabricate a user's manual qualitative judgment. **M3** other Activity fields/Session/Life Area/Schedule retirement, **M4** Event Inspector/edit/duplicate, **M5/B15** real UI whole vertical remain open. The user specifically disallowed piecemeal testing or repeated micro-blocks; finish each owner/domain vertical in one complete implementation and ask for one consolidated local gate.
