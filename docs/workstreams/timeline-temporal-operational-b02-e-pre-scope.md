# Timeline / Temporal-Operational — B02-E Exact PRE-SCOPE

- **Status:** APPROVED / B02-E1 PROVEN / B02-E2 NEXT
- **Date:** 2026-09-15
- **Branch:** `feature/timeline-temporal-operational`
- **Reviewed branch anchor:** `b2daafaec3f56737f0783318d62be96e4b0c74e0`
- **Parent plan:** `docs/workstreams/timeline-temporal-operational-b02-execution-plan.md`
- **Live ledger:** `docs/workstreams/timeline-temporal-operational-map.md`
- **Authorization carried by this document:** bounded B02-E1 → E4 implementation after explicit user approval.
- **Product implementation authorized now:** B02-E approved; execute one slice at a time and stop at its evidence gate.
- **CI authorized now:** none; CI remains deferred by explicit user instruction.

---

## 0. Gate result

B02-A through B02-D are proven for one same-local-day `floating_local interval` Activity path.

B02-E is not one undifferentiated “support every date field” change. It is the bounded closure sequence that must:

1. activate the existing exact CP6 Schedule forms without collapsing their meanings;
2. add one narrow lossless representation for accepted coarse local-period placement;
3. make establish/revise/unschedule/Undo form-generic while preserving history and expected-state concurrency;
4. query and render each activated form truthfully across local-date and DST boundaries;
5. close the remaining B02 ledger obligations only after executed evidence;
6. stop before Event Core, Routine, Occurrence generation, Session, Actual or provider synchronization.

No implementation may start until the user explicitly approves this PRE-SCOPE.

---

## 1. Authority reopened and findings

The following authority was re-read against the current B02 implementation:

- Domain Schedule v0 and continuations;
- Logical Model Slice C — Time / Reality;
- Final pre-roadmap audit, especially FA-03;
- Physical PostgreSQL mapping and CP6 M03/M05/M07;
- current Database Dictionary Schedule objects;
- B02 execution plan, roadmap and live ledger;
- current backend Schedule/API/Timeline implementation;
- current web temporal model, create composer, Timeline and data sources.

Binding semantic boundary:

```text
Activity
!= Schedule
!= Temporal Constraint
!= Session
!= Actual
!= scheduling proposal
```

Binding precision boundary:

```text
Tuesday
!= Tuesday afternoon
!= Tuesday at 18:00
!= Tuesday 18:00-20:00
!= start Tuesday 18:00 / end unresolved
```

A date-based placement is not an exact 24-hour interval. A named-zone placement is not an absolute placement. A coarse accepted placement is not unplaced and must not be encoded as invented timestamps.

---

## 2. Current physical and product truth

| Placement meaning | CP6 physical representation | Current B02 product activation | B02-E decision |
| --- | --- | --- | --- |
| Date span / all-day | `schedule_placement_date_state.date_span`, finite non-empty half-open `daterange` | Not activated | Activate losslessly |
| Floating local | local timestamp payload with `point | start_only | interval` extent | Only same-local-day interval | Keep interval path; remove same-day restriction; preserve physical non-interval extents without pretending they are exposed |
| Named-zone local | local wall-clock payload + IANA `zone_id` + optional resolved instants | Not activated | Activate interval with explicit DST disambiguation and retained resolved instants |
| Absolute | aware instant payload with `point | start_only | interval` extent | Not activated | Activate interval; render in request effective zone without changing canonical form |
| Coarse local period | No dedicated CP6 payload | Not representable losslessly | Add one narrow fifth form; never invent time boundaries |
| No current placement | absence of current binding; Schedule/history may remain | Proven in B02-D | Preserve |
| Multiple Schedule records per subject | schema permits 0..N Schedule owners for one subject; current binding is per Schedule | Product path currently establishes one at a time | Preserve; do not add a universal subject-level uniqueness constraint |

The CP6 named-zone trigger already validates the IANA vocabulary and round-trip consistency of supplied resolved instants. B02-E must calculate and require the accepted resolution at the application boundary for exposed named-zone placements, including ambiguous and nonexistent wall-clock cases.

---

## 3. Coarse precision decision proposed for approval

### 3.1 New temporal form

Add one envelope form:

```text
coarse_local_period
```

Add one protected payload table:

```text
dante.schedule_placement_coarse_local_period_state
```

Required columns:

| Column | Contract |
| --- | --- |
| `material_state_ref uuid` | PK/FK to the owning `schedule_placement_state` |
| `local_date date` | finite civil date associated with the accepted period |
| `period_code text` | bounded value: `morning | afternoon | evening` |

No `starts_local_at`, `ends_local_at`, duration, offset or derived clock boundary is stored for this form.

`Tuesday` remains `date_span`.  
`Tuesday afternoon` becomes `coarse_local_period(local_date=Tuesday, period_code=afternoon)`.

“Night” is deliberately not activated in this first bounded vocabulary because ownership across midnight is semantically ambiguous. It requires a later explicit authority decision rather than a hidden convention.

### 3.2 Query and rendering

A coarse local period belongs to its explicit `local_date` for local-date window inclusion.

It renders as a truthful label such as:

```text
Martedì · Pomeriggio
```

It does not render as a time-grid block and does not consume an inferred interval.

### 3.3 Precision-changing operations

- Move coarse placement to another day while retaining its period → new `coarse_local_period` MaterialState.
- Change afternoon to morning/evening → new `coarse_local_period` MaterialState.
- Drop/select an exact time → explicit revision to `floating_local` or `named_zone_local`.
- Change exact time to a coarse period → explicit revision to `coarse_local_period`.
- No drag/drop or default duration may silently refine or broaden precision.

---

## 4. Activated transport contract

B02-E replaces floating-only Schedule payloads with one explicit discriminated placement union. The exact wire names remain snake_case.

### 4.1 Date span

```json
{
  "kind": "date_span",
  "start_date": "2026-09-15",
  "end_date_exclusive": "2026-09-16"
}
```

Rules:

- half-open civil-date range;
- end strictly after start;
- no conversion to midnight instants for canonical storage;
- one-day Activity all-day placement is valid.

### 4.2 Floating-local interval

```json
{
  "kind": "floating_local_interval",
  "starts_local_at": "2026-09-15T15:00:00",
  "ends_local_at": "2026-09-15T16:00:00"
}
```

Rules:

- offset-free wall-clock values;
- end after start;
- may cross a local-date boundary;
- no effective/request timezone is attached to the canonical placement.

### 4.3 Named-zone-local interval

```json
{
  "kind": "named_zone_local_interval",
  "starts_local_at": "2026-10-25T02:30:00",
  "ends_local_at": "2026-10-25T03:30:00",
  "zone_id": "Europe/Rome",
  "disambiguation": "later"
}
```

Rules:

- local values remain canonical alongside `zone_id`;
- accepted requests resolve and retain `resolved_start_at` and `resolved_end_at`;
- `reject`, `earlier` and `later` are explicit accepted policies;
- a gap or overlap is never silently accepted through a library default;
- start and end are resolved independently and the resulting instant interval must remain ordered;
- responses expose retained resolution needed to reconstruct what was accepted.

`compatible` may remain an internal utility for local-day boundary calculation; it is not the default user mutation policy.

### 4.4 Absolute interval

```json
{
  "kind": "absolute_interval",
  "starts_at": "2026-09-15T13:00:00Z",
  "ends_at": "2026-09-15T14:00:00Z"
}
```

Rules:

- aware instants only;
- normalize to UTC without changing the instant;
- end after start;
- display conversion to the effective zone does not change canonical absolute meaning.

### 4.5 Coarse local period

```json
{
  "kind": "coarse_local_period",
  "local_date": "2026-09-15",
  "period": "afternoon"
}
```

Rules:

- no clock time or duration;
- no inferred interval;
- rendered in a date/coarse lane, not as an exact time block.

### 4.6 Extent boundary

CP6 also permits `point` and `start_only` for floating, named-zone and absolute forms. B02-E preserves those physical rows and validates that form-totality remains intact, but does not expose new Activity authoring UI for them in this slice.

This bounded interval activation does not claim that every future partial-extent Schedule UX is complete.

---

## 5. Schedule mutation semantics

The existing operation identities and receipts remain separate from Schedule and MaterialState identity.

### Establish

- one existing/new Activity;
- one stable ScheduleRef;
- one placement MaterialState;
- exactly one matching typed payload;
- explicit current binding;
- open current-history episode;
- replay only for same normalized material intent.

### Revise

- exact ScheduleRef and expected current MaterialStateRef;
- new immutable placement MaterialState;
- form may stay the same or intentionally change;
- prior current-history episode closes;
- new episode opens;
- stale basis rejects;
- semantically equal payload may be a proven no-op, but replay and no-op stay distinguishable.

### Unschedule

Unschedule remains form-independent: close the open current-history episode and remove only the current binding. Keep Activity, Schedule, all placement states/payloads and history.

### Guarded Undo

Undo becomes form-generic:

- target one exact unschedule receipt;
- require continued absence and no newer accepted placement;
- copy the retained prior typed payload into a new MaterialState of the same temporal form;
- open a new current-history episode;
- never rewind chronology;
- conflict if newer truth exists.

The existing floating-only Undo copy is therefore not sufficient for B02-E closure.

### Fingerprints

Intent fingerprints include:

- subject/Schedule identity as applicable;
- expected state where applicable;
- exact temporal form;
- exact extent;
- normalized payload values;
- named-zone id, selected disambiguation and resolved instants where applicable;
- coarse period code without fabricated boundaries.

Same operation id + materially different normalized intent rejects.

---

## 6. Timeline query semantics

The public query remains:

```text
[start_date, end_date_exclusive)
maximum 62 civil dates
authenticated self Person
effective named timezone from DanteContext
```

Inclusion rules:

| Form | Window inclusion |
| --- | --- |
| `date_span` | civil-date range overlap |
| `floating_local` | local wall-clock interval overlap with local midnight boundaries; no instant conversion |
| `named_zone_local` | retained resolved instant overlap with UTC bounds derived from each requested local boundary in the effective zone |
| `absolute` | instant overlap with those same effective-zone UTC bounds |
| `coarse_local_period` | `local_date` inside the half-open civil-date window |

The implementation must use local-day boundary helpers and must not assume a local day lasts 24 elapsed hours. Europe/Rome 2026 spring and autumn transitions are mandatory evidence.

Timeline response items preserve a discriminated placement payload. They do not flatten every form into `starts_local_at/ends_local_at`.

Current Timeline renders only current accepted placement states. History never becomes duplicate current cards.

---

## 7. Product/UI scope

### 7.1 Activity Create and edit

For exact timed Activity placement, the primary controls become:

```text
Data | Da | A
      durata calcolata tra parentesi
```

Examples:

```text
Da 11:30  A 12:30  (1 ora)
Da 11:30  A 12:15  (45 minuti)
```

The user edits start and end. Duration is derived for display and validation. It is Schedule duration and never Activity estimated effort.

The existing “Durata prevista” selector is removed from the primary exact-time row for Activity. If a duration shortcut is retained anywhere, it may only update the explicit end value and must remain secondary to `Da/A`.

### 7.2 Placement choices

- `Da collocare` → no Schedule/current placement and therefore no date/time controls.
- `Tutto il giorno` → date-span semantics.
- `Orario` → floating-local by default or named-zone when the user intentionally selects a zone.
- coarse period → explicit morning/afternoon/evening choice with a date and no exact time.
- absolute placement is supported by the canonical/API/runtime path and rendered correctly; no ordinary end-user “UTC mode” is added to the primary Create surface.

### 7.3 Timeline rendering

- date-span → all-day/date lane;
- coarse period → coarse/date lane with the period label;
- floating interval → time grid using its wall-clock values;
- named-zone interval → time grid converted for the viewing zone while retaining/showing source zone where relevant;
- absolute interval → time grid converted for the effective viewing zone.

### 7.4 Existing unschedule decision retained

“Riporta nel Planning Tray” remains an immediate non-destructive Schedule operation with visible guarded Undo. No confirmation dialog is added.

Delete, archive, completion/confirmation actions, icon menus and the broader advanced card command design are not part of B02-E.

### 7.5 Drag boundary

- exact interval drag may revise exact start/end while preserving form;
- date-span drag changes civil dates without manufacturing instants;
- coarse date-to-date movement preserves period;
- a coarse/date placement dropped onto an exact time requires an explicit precision-changing interaction;
- drag never records Session or Actual.

---

## 8. B02-E execution slices after approval

### B02-E1 — canonical placement union and forward DDL

- introduce backend placement value types and validation;
- add the coarse local-period physical payload;
- extend placement-totality enforcement and ACL safely;
- make establish/revise/Undo support the activated union;
- preserve existing floating operation replay and history;
- targeted unit and PostgreSQL tests only.

### B02-E2 — Timeline read projection and DST

- emit discriminated current placement payloads;
- implement form-specific window inclusion;
- prove half-open windows, cross-midnight floating intervals, date spans, 23-hour and 25-hour local days;
- prove named-zone gap/overlap behavior and absolute display-zone conversion.

### B02-E3 — web authoring, rendering and interaction

- connect all-day/date-span, named-zone and coarse Activity placement to canonical mutations;
- implement `Da/A (durata)` exact-time UX;
- render form-specific Timeline lanes/cards;
- preserve direct unschedule/Undo and stale-conflict truthfulness;
- implement/prove direct exact-interval drag without Actual semantics.

### B02-E4 — closure evidence

- targeted backend/frontend regression;
- real local E2E and Firefox proof when the user authorizes that test phase;
- manual B02-E userTest;
- Database Dictionary/topology reconciliation if DDL changed;
- map/roadmap/handoff reconciliation;
- no CI run until separately authorized by the user.

A slice stops when its own evidence is complete. It does not mark later slices green.

---

## 9. Exact write manifest after approval

No paths in this section are authorized until explicit approval.

### CREATE

```text
apps/backend/migrations/versions/20260915_25_b02_schedule_form_completeness.py
apps/backend/tests/integration/temporal/test_b02_schedule_forms_precision_dst.py
apps/web/src/features/home/ui/timeline/timeline-schedule-forms-b02.test.tsx
apps/web/e2e/temporal-schedule-forms-b02.spec.ts
docs/database/dictionary/tables/schedule_placement_coarse_local_period_state.json
docs/workstreams/timeline-temporal-operational-b02-e-usertest.md
```

### UPDATE — backend/runtime

```text
apps/backend/src/dante/modules/temporal/schedule.py
apps/backend/src/dante/modules/temporal/activity.py
apps/backend/src/dante/modules/temporal/application.py
apps/backend/src/dante/modules/temporal/api.py
apps/backend/src/dante/platform/database/mappings/schedule.py
apps/backend/src/dante/platform/database/mappings/__init__.py
apps/backend/tests/test_temporal_schedule.py
apps/backend/tests/test_temporal_timeline.py
apps/backend/tests/unit/platform/test_time.py
apps/backend/tests/integration/temporal/test_b02_schedule_create.py
apps/backend/tests/integration/temporal/test_b02_schedule_place.py
apps/backend/tests/integration/temporal/test_b02_schedule_revision.py
apps/backend/tests/integration/temporal/test_b02_schedule_unschedule_undo.py
```

`apps/backend/src/dante/platform/time.py` may be updated only if an executed DST test proves a missing primitive; existing classification, explicit disambiguation and local-day-bound helpers must be reused first.

### UPDATE — web/product

```text
apps/web/src/features/temporal/model.ts
apps/web/src/features/temporal/activity-data-source.ts
apps/web/src/features/temporal/schedule-data-source.ts
apps/web/src/features/temporal/timeline-read.ts
apps/web/src/features/temporal/remote-activity-data-source.ts
apps/web/src/features/temporal/remote-schedule-data-source.ts
apps/web/src/features/temporal/remote-timeline-read.ts
apps/web/src/features/temporal/in-memory-temporal-workspace.ts
apps/web/src/features/temporal/timeline-runtime-boundary.tsx
apps/web/src/features/temporal-create/model/temporal-create-session.ts
apps/web/src/features/temporal-create/application/temporal-create-runtime.ts
apps/web/src/features/temporal-create/application/temporal-create-projection.ts
apps/web/src/features/temporal-create/ui/temporal-create-core-fields.tsx
apps/web/src/features/home/ui/timeline/timeline-all-day-runtime.ts
apps/web/src/features/home/ui/timeline/timeline-all-day-layer.tsx
apps/web/src/features/home/ui/timeline/timeline-day-stream.tsx
apps/web/src/features/home/ui/timeline/timeline-overlays.tsx
apps/web/src/features/home/ui/timeline/timeline-surface.tsx
apps/web/src/features/home/ui/timeline/timeline.css
packages/i18n/src/resources/it/temporal-runtime.ts
packages/i18n/src/resources/en/temporal-runtime.ts
packages/i18n/src/resources/it/home.ts
packages/i18n/src/resources/en/home.ts
```

Adjacent existing `*.test.ts[x]` files for these modules may be updated only when their covered contract changes.

### UPDATE — generated API surface

The repository’s existing OpenAPI/API-client generation command may update only the generated specification and generated temporal models/operations deriving from `apps/backend/src/dante/modules/temporal/api.py`. The exact generated diff must be reviewed before commit; unrelated generated churn is rejected.

Expected generated families include:

```text
packages/api-client/src/generated/model/*Schedule*.ts
packages/api-client/src/generated/model/*Schedule*.zod.ts
packages/api-client/src/generated/model/timeline*.ts
packages/api-client/src/generated/model/timeline*.zod.ts
packages/api-client/src/generated/endpoints/temporal/*
```

If the actual generator uses different exact paths, stop, record the generated manifest, and revalidate before committing; do not hand-edit generated files.

### UPDATE — Dictionary and workstream evidence

```text
docs/database/dictionary/tables/schedule_placement_state.json
docs/database/dictionary/tables/schedule_placement_date_state.json
docs/database/dictionary/tables/schedule_placement_floating_local_state.json
docs/database/dictionary/tables/schedule_placement_named_zone_state.json
docs/database/dictionary/tables/schedule_placement_absolute_state.json
docs/database/dictionary/tables/schedule_establish_operation.json
docs/database/dictionary/tables/schedule_revision_operation.json
docs/database/dictionary/tables/schedule_unschedule_undo_operation.json
docs/database/dictionary/scope.json
docs/database/dictionary/README.md
docs/physical-model/mappings/postgresql-18.4-v1.md
docs/workstreams/timeline-temporal-operational-b02-execution-plan.md
docs/workstreams/timeline-temporal-operational-map.md
docs/workstreams/timeline-temporal-operational-roadmap.md
docs/workstreams/timeline-temporal-operational-handoff.md
```

Only dictionary/topology entries actually changed by migration `20260915_25` are rewritten. Existing generated dictionary workflow is preferred over manual drift.

### DELETE

```text
none
```

No historical migration, Schedule state, payload, operation receipt or test evidence may be deleted.

---

## 10. Required targeted evidence

### Backend/value tests

- discriminated placement validation for every activated form;
- offset-free floating values;
- aware normalized absolute values;
- date-span half-open validation;
- coarse period contains no exact boundary;
- named-zone unique/gap/overlap resolution with explicit policy;
- cross-form material equality and fingerprint stability.

### PostgreSQL integration

- establish/revise/unschedule/Undo for date-span, floating, named-zone, absolute and coarse;
- one exact matching payload per live placement state;
- current/history chronology across cross-form revisions;
- same operation/same intent replay;
- same operation/different intent rejection;
- stale expected-state rejection;
- cross-self rejection;
- generic Undo copies the exact prior form into a new MaterialState;
- 0..N Schedule owners per subject remain possible;
- no subject-level universal 1:1 uniqueness introduced.

### Timeline/DST

- date-span overlap at both half-open boundaries;
- floating cross-midnight overlap;
- Europe/Rome spring 2026 local-day UTC bounds = 23 elapsed hours;
- Europe/Rome autumn 2026 local-day UTC bounds = 25 elapsed hours;
- nonexistent `2026-03-29 02:30 Europe/Rome` rejected unless an explicit supported policy is selected;
- ambiguous `2026-10-25 02:30 Europe/Rome` earlier/later produce distinct retained instants;
- absolute instant appears on the correct effective local date;
- historical placements do not duplicate current cards;
- coarse placement never receives fabricated time text or grid geometry.

### Web

- Activity “Da collocare” has no date/time placement controls;
- exact Activity uses `Da` and `A` and shows computed duration;
- changing end changes Schedule duration only;
- all-day Activity produces date-span;
- named-zone Activity preserves chosen zone and DST decision;
- coarse Activity renders its period label;
- reload/refetch preserves each form once;
- exact drag revises Schedule, not Activity identity/Actual;
- stale conflict and persistence outage never show fake success;
- direct unschedule + visible guarded Undo remains unchanged.

### Final B02 evidence

- local E2E create → place → move → cross-form revise → unschedule → Undo → reload/history;
- Firefox critical interaction pass;
- manual B02-E protocol approved by user;
- CI remains a separate later authorization gate.

---

## 11. Explicitly out of scope

- Event Core and Event authoring persistence;
- Routine/Recurrence/Occurrence generation or exception materialization;
- Session, Actual, Outcome, completion or attendance;
- confirmation/acknowledgement workflows;
- Temporal Constraint solver or replanning engine;
- provider import/export/write reconciliation;
- offline sync;
- archive/delete semantics and their icon/menu design;
- general card action redesign;
- customizable definitions of morning/afternoon/evening;
- “night” coarse period;
- automatic precision inference from natural language;
- capacity/busy semantics;
- Activity estimated effort;
- CI execution before separate user authorization.

---

## 12. Stop conditions

Stop and re-gate if:

1. the branch head changed from the reviewed anchor before implementation begins;
2. the new coarse form requires broader precision ontology than the bounded local period approved here;
3. generic mutation would require broad runtime table UPDATE/DELETE privileges;
4. named-zone acceptance cannot retain both local intention and exact resolved instant;
5. a query implementation assumes 24-hour local days;
6. form-general Undo cannot remain monotonic and expected-state guarded;
7. a proposed UI converts coarse/date-only input into exact timestamps;
8. a new uniqueness rule would collapse the accepted 0..N Schedule cardinality;
9. implementation would require Event/Routine/Occurrence/Session/Actual product owners;
10. generated API or Dictionary output contains unrelated churn;
11. any test needs CI or external-provider execution before the user authorizes it.

---

## 13. Approval gate

Explicit approval of this document authorizes the bounded B02-E1 → E4 implementation on the named branch and paths, subject to every stop condition above.

It does not authorize CI.

Required user decision:

```text
APPROVE B02-E PRE-SCOPE
or
REQUEST CHANGES
```


---

## 14. B02-E1 executed evidence — 2026-09-15

The user explicitly approved this PRE-SCOPE with `APPROVE B02-E PRE-SCOPE`.

B02-E1 is **PROVEN** on branch `feature/timeline-temporal-operational`:

- implementation commit: `db057a422361122f7eed506239b6489c35d7d520`;
- semantic/ACL correction: `dca566180ac96f4072820de60946a72d9ab99ba3`;
- local unit/value evidence: `29 passed, 2 deselected`;
- real PostgreSQL evidence supplied by the user: `4 passed, 2 deselected in 9.66s`;
- covered: five activated placement forms, exact typed-payload totality, cross-form revision, replay/reuse rejection, stale-state and cross-self rejection, generic monotonic Undo, history chronology, and 0..N Schedule records for one Activity;
- CI was not run, per explicit instruction.

B02-E2 is the next bounded slice. E1 evidence does not promote Timeline read/DST, web authoring/rendering, drag, Firefox, E2E, Dictionary closure, or final B02 acceptance.
