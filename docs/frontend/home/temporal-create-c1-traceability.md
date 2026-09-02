# DANTE — Temporal Create C1 Traceability

**Status:** FINAL AUTOMATED TRACEABILITY — MANUAL ACCEPTANCE PENDING  
**Date:** 2026-09-02  
**Branch:** `feature/home-timeline`  
**Implementation candidate:** `7028633921d1b438bd04961a718457afd82ccc13`  
**Frontend CI:** `33635389124` / #632 — FULL PASS  
**Scope:** complete pre-backend **manual** Timeline Temporal Create C1

## 1. Purpose

This file is the closure-grade traceability record for C1. It connects implemented manual Create behavior to product evidence, closed semantic models, CP6 materialized database, Alembic families, frontend application boundaries, UI surfaces and automated proof.

It is deliberately not a claim that browser fields are database rows.

The permanent mapping direction is:

```text
Product requirement / simulation evidence
→ Domain owner + invariant
→ Logical representation
→ Physical / CP6 mechanism
→ frontend application model
→ manual authoring / projection surface
→ future backend/provider adapter
```

Never:

```text
UI field == DB column
```

and never:

```text
schema object exists
== generic semantic CRUD is authorized
```

## 2. Source authority used

Primary authorities consumed for this traceability:

- `docs/product/product-identity-and-north-star.md`;
- `docs/product/v1-scheduling-flexibility.md`;
- `docs/product/v1-execution-status.md`;
- `docs/product/v1-confirmation-and-reminders.md`;
- `docs/product/feature-discovery-simulation-2026-08.md`;
- `docs/product/multi-actor-collaboration-discovery-simulation-2026-08.md`;
- `docs/domain/README.md` and accepted Domain Atlas / Language Map;
- `docs/logical-model/README.md` and Whole Logical closure;
- `docs/physical-model/README.md` and accepted Physical Model;
- `docs/database/README.md` and current Database Dictionary/reference;
- `apps/backend/migrations/versions/20260825_03_cp6_schedule_actual_session.py`;
- `apps/backend/migrations/versions/20260825_04_cp6_recurrence.py`;
- `apps/backend/migrations/versions/20260826_06_cp6_occurrence_generation.py`;
- `apps/backend/migrations/versions/20260826_07_cp6_runtime_acl_activation.py`;
- `apps/backend/migrations/versions/20260826_08_cp6_final_qa_hardening.py`;
- `docs/frontend/home/temporal-f0-contract.md`;
- `docs/frontend/home/timeline-t1-frozen-contract.md`;
- `docs/frontend/home/temporal-create-c1-scope-amendment.md`;
- code under `apps/web/src/features/temporal-create/`;
- `apps/web/src/features/home/ui/timeline/timeline-create-bridge.tsx`;
- `apps/web/e2e/temporal-create.spec.ts`;
- `apps/web/e2e/temporal-create-appearance.spec.ts`.

Current database baseline is the materialized CP6 system of record:

- PostgreSQL 18.6;
- Alembic head `20260826_08`;
- 68 DANTE tables;
- 5 ordinary views;
- 14 routines;
- 75 trigger attachments;
- 95 physical indexes;
- 68 foreign keys;
- 120 CHECK constraints.

## 3. North Star and Create role

DANTE's product direction is not “calendar CRUD”. The Timeline/Create surface contributes to the broader operating loop by letting a person manually express an intention, temporal placement or constraint precisely enough for later planning/execution systems without pretending that planned state is lived reality.

C1 therefore optimizes for:

- manual speed for simple creation;
- progressive depth when needed;
- preservation of semantic distinctions under the UI;
- user authority over the committed effect;
- no fabricated provider/backend/Actual truth;
- recoverable future connection to backend/application owners.

The product principle “simple appointment may remain simple” is implemented through Quick → Expanded → Full rather than by flattening richer semantics out of the model.

## 4. Manual-only input boundary

C1 owns **manual authoring**, not AI interpretation.

Current entry sources:

```text
Timeline +
Timeline double-click
Timeline Shift-drag/range
```

These may supply deterministic facts already known by the interaction:

- date;
- start time;
- duration/range;
- existing manual Context/defaults where appropriate.

Application file:

`application/temporal-create-seed.ts`

`TemporalCreateFieldSeed` is therefore a structured **manual-prefill** value. It is applied before the manual draft opens, then enters ordinary normalization and validation.

It is explicitly **not** the C1 contract for:

- natural-language input;
- DANTE/AI interpretation;
- voice;
- confidence/alternatives;
- model provenance;
- AI proposal governance.

Future DANTE/AI work remains a separate vertical. It may later call compatible shared downstream application/domain/backend operations if that vertical's own contract justifies it. It does not need to reuse the C1 form/session/seed.

Automated proof:

- `application/temporal-create-seed.test.ts`;
- `ui/temporal-create-entry.tsx` invocation wiring.

The tests prove that manual prefill cannot bypass normal validation or invent Activity recurrence.

## 5. Ownership and non-collapse matrix

| C1 capability | Product / simulation requirement | Domain / Logical invariant | Physical / CP6 evidence | Frontend representation | Manual UI / seam | Automated evidence | Disposition |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Activity vs Event | Simple appointments may remain simple; action/planning and event semantics must not collapse | `Activity` and `Event` are separate LR-01 native owners | Separate owner tables/families; M4 recurrence has Event owner family but no Activity family | `TemporalCreateKind = activity | event`; kind-aware normalization | Distinct Activity/Event grammar | session, enterprise, E2E | **Implemented** |
| Activity repetition | Repeated work needs durable Routine semantics, not a convenience boolean | Routine is native owner; Activity is not recurrence owner | M4 calls recurrence family creation for `routine` and `event` only | Activity normalization forces Event recurrence intent to `none` | Routine handoff; no Activity recurrence editor | seed, handoff, boundary, session, E2E | **Implemented / owner-correct** |
| Event recurrence | Repeated time-centred events require source recurrence semantics | recurrence source != generated Occurrence | `event_recurrence_*` M4 family | `TemporalCreateEventRecurrenceIntent` | Event recurrence editor | model/runtime/enterprise/E2E | **Implemented** |
| Generated Occurrence | Recurrence specification must not fabricate future occurrence truth in browser | Occurrence is distinct LR-01 owner | M6 owns generation + governing recurrence-state binding | Create stores recurrence specification only | Copy says evaluator/generation is backend-owned | enterprise/runtime/E2E | **Deferred by design** |
| Schedule vs Session vs Actual | Planned time does not prove execution or outcome | `Schedule != Session != Actual`; missing Actual != false | M3 materializes separate families | placement, execution intent, confirmation intent are separate | Create authors plan/policy without Session/Actual | F0 + Create tests | **Implemented distinction** |
| Planned vs happened | DANTE must represent reality, not force it to match plan | planned != Actual; Observation != Actual | separate state/history structures downstream | no Create success fabricates Actual | outcome policy only | runtime/confirmation tests | **Implemented distinction** |
| Provisional inference | Product may infer provisionally but cannot assert false certainty | provenance/confirmation != outcome | authoritative Actual/provenance remains downstream | `infer-provisional` policy value, not Actual | copy marks result provisional/non-authoritative | E2E + i18n | **Implemented seam** |
| Context vs appearance | User may want visual distinction without changing organization | UI terminology/presentation != ontology; Context membership != color override | no CP6 owner promotion is implied by a CSS tone | `contextId` remains membership; `appearanceTone` is optional presentation | inherit Context tone or choose color override | model/runtime/appearance E2E | **Implemented non-collapse** |
| External-owned objects | `+` must not become universal CRUD | Project/Goal/Routine/etc retain their own owners | schema existence does not authorize generic frontend CRUD | typed handoff target + immutable draft snapshot | explicit deferred owner dependencies | handoff tests | **Implemented seam / deferred owner** |
| Manual vs AI | Manual precision and DANTE intelligence are different interaction surfaces | AI output != canonical truth; user authority preserved | no DB fact requires AI to pass through Create form | manual Create session only | no NLP/chat/voice affordance | code boundary + manual acceptance | **Explicitly separated** |

## 6. Temporal placement traceability

| C1 form | Semantic meaning | F0/application representation | Backend/physical relation | C1 behavior |
| --- | --- | --- | --- | --- |
| Timed floating | local wall-clock intent without named-zone binding | floating-local placement | compatible with local/date temporal payload semantics | deterministic local projection |
| Timed zoned | local civil time bound to IANA zone | zoned placement | named-zone semantics remain distinct from instant/provider revision | DST-aware duration/end arithmetic uses real Instants |
| Absolute | exact Instant representation | F0 supports absolute | CP6 supports absolute temporal framing where applicable | **not exposed as normal manual C1 control** |
| All-day | date span, not midnight timed hack | date-span, exclusive end | date semantics remain first-class | multi-day Event supported/validated |
| Unscheduled Activity | valid planning intent with no accepted exact placement | placement `null` + structured scheduling intent | future Schedule/solver boundary | no arbitrary Timeline slot fabricated |
| Event unscheduled | invalid for current Event Create grammar | normalized/rejected away | Event remains time-centred | cannot silently create unscheduled Event |

C1 intentionally does not expose every substrate representation merely because F0 or PostgreSQL can encode it. Manual UI exposes only representations justified by the current authoring contract.

## 7. Activity scheduling and execution traceability

Product scheduling rules reject a single fixed/flexible flag. C1 therefore supports structured Activity intent for:

- fixed placement;
- open/unscheduled;
- bounded window;
- deadline constrained;
- preferred window;
- earliest start / deadline boundaries where applicable;
- locked, window-bound, confirmation-required or freely replannable movement;
- indivisible vs splittable execution;
- minimum session duration;
- maximum session count where meaningful;
- preparation/recovery/spacing;
- partial completion, early finish and compatible merge intent;
- fallback such as skip, same-window, next valid date, shorten/split and dependency replan.

These are **planning/application specifications**. They do not construct Session rows, Actual rows or solver output.

Frontend owners:

- `model/temporal-create-session.ts`;
- `ui/temporal-create-activity-fields.tsx`;
- `application/temporal-create-runtime.ts`.

Primary automated evidence:

- `model/temporal-create-session.test.ts`;
- `application/temporal-create-enterprise.test.ts`;
- `application/temporal-create-runtime.test.ts`;
- `e2e/temporal-create.spec.ts`.

## 8. Event recurrence family traceability

Alembic M4 defines exactly four recurrence `family_code` values:

```text
calendar_wall_clock
elapsed_interval
quota_per_period
cyclic_positional
```

C1 exposes the same four semantic families for Event without mirroring database tables directly.

### Calendar / wall-clock

C1 manual authoring exposes:

- daily;
- weekly + selected weekdays;
- monthly anchored to authored civil date;
- monthly ordinal weekday with supported ordinal positions;
- yearly anchored to authored civil date;
- recurrence interval;
- open / until-date / occurrence-count termination.

This preserves civil-calendar semantics without presenting database vocabulary as UI.

### Elapsed interval

C1 captures a positive elapsed interval in minutes as authoring intent. Authoritative evaluator anchoring/execution remains backend work.

### Quota per period

C1 exposes:

- quota count;
- day/week/month/year;
- every N periods;
- floating-local / named-zone / absolute-UTC frame;
- week start when period is weekly;
- IANA period timezone when frame is named-zone.

The UI copy explicitly prevents silent dependence on device timezone/library defaults.

### Cyclic positional

C1 exposes a human-friendly **1-based active-position list**. Multiple active positions are normalized, unique, ordered and bounded by cycle length.

The technical physical representation remains a persistence concern rather than UI vocabulary.

## 9. Recurrence state/history and M6 boundary

C1 does not flatten recurrence into a repeat flag. CP6 recurrence participates in material-state/history structures. M6 then allows recurrence-generated Occurrences to bind to the exact governing recurrence state that produced them.

Therefore:

```text
Create recurrence draft
!= recurrence MaterialState persisted by backend
!= evaluator checkpoint
!= generated Occurrence
```

A later backend adapter must preserve this separation. A later C5/Detail flow owns source revision/scope editing; C1 only authors the initial manual specification.

## 10. Confirmation, reminders and provider seams

Product confirmation/reminder rules allow ask-now/later, daily/weekly review, silent-unconfirmed, explicit automatic policies and provisional inference. C1 captures these as structured policy intent.

Real notification delivery is absent by design.

For Event collaboration/integration C1 captures:

- required participants;
- optional participants;
- rooms/resources;
- pre-read/material;
- conference intent;
- location;
- availability;
- visibility.

It does **not** claim:

- invitation delivery;
- room booking;
- conferencing link creation;
- external calendar synchronization;
- sharing/ACL changes.

These remain future backend/provider seams.

## 11. Context / appearance traceability

The appearance capability was added without promoting visual tone into a new domain owner or generic tag/category system.

Application/UI relation:

```text
fields.contextId
→ Timeline groupId
→ grouping + filtering
→ inherited default tone

fields.appearanceTone = null
→ inherit current Context tone

fields.appearanceTone = tone
→ visual tone override only
→ contextId/groupId unchanged
```

Manual color vocabulary is independent from Context labels:

```text
purple / viola
cyan / ciano
green / verde
amber / ambra
pink / rosa
red / rosso
```

This prevents the UI from implying, for example, that red means membership in the Urgenze Context.

Automated proof:

- `model/temporal-create-appearance.test.ts`;
- `application/temporal-create-appearance-runtime.test.ts`;
- `e2e/temporal-create-appearance.spec.ts`.

The E2E verifies:

1. Focus Context inherits Focus tone by default;
2. manual custom red tone changes preview/card presentation;
3. Full ↔ Expanded preserves the override;
4. accepted card still displays Focus Context;
5. Urgenze filter hides it;
6. reset + Focus filter shows it;
7. override remains visual;
8. Undo removes the real created projection.

## 12. External owning-vertical handoff

Create is not a universal CRUD factory.

Application file:

`application/temporal-create-handoff.ts`

Typed targets:

```text
project
goal
routine
program
world
template
reminder
block
asset
```

Current registry state for all targets is `deferred`.

`prepareTemporalCreateHandoff()` produces an immutable normalized draft snapshot and deliberately contains no route, href, CRUD callback or success effect.

The Routine target is also the owner-correct escape hatch for persistent Activity repetition.

Automated proof: `application/temporal-create-handoff.test.ts`.

## 13. Draft, progressive disclosure and preview

Quick, Expanded and Full are one session/draft, not separate form engines.

Required preserved behavior:

- Quick is title-first and low-friction;
- Expanded reveals common structured planning;
- Full reveals deep owner-specific authoring;
- round-trips preserve values;
- candidate preview stays visually/state-wise separate from accepted projection;
- validation never requires partially committing a real item.

The Timeline bridge accepts preview separately from applied effects.

Automated proof: session tests and C1 E2E suites.

## 14. Command boundary, idempotency and snapshot integrity

F0 owns the minimal temporal command/result boundary and exact operation idempotency.

C1 adds rich specification metadata that must not be lost merely because visible Timeline projection is minimal.

### Rich idempotency

C1 fingerprints canonical rich metadata by operation ID:

- exact prepared replay is idempotent;
- same operation ID with changed rich intent rejects as `operation-id-reused`;
- rejected collision is side-effect free.

### Prepared-snapshot ownership

At implementation candidate `7028633921d1b438bd04961a718457afd82ccc13`, `runtime.prepare()` re-normalizes and deeply freezes its own specification before validation, placement/capability projection and execution.

This closes a prepare/execute TOCTOU class of bug: mutable caller data cannot change the prepared command/specification after preparation.

Automated proof:

- `application/temporal-create-runtime.test.ts`;
- `application/temporal-create-boundary.test.ts`.

## 15. Undo and local runtime truth

Current C1 executes against the deterministic in-memory F0 adapter only.

On applied Create:

- projection is added;
- rich local record is retained separately;
- reveal/focus can target placed projection;
- Undo uses the F0 undo token;
- successful Undo removes both projection and matching C1 rich local record.

This is truthful local application behavior, not a persistence claim.

## 16. Interaction, accessibility and responsive proof

C1 protects:

- opener focus;
- contextual focus return to Timeline grid;
- dirty draft discard confirmation as named modal `alertdialog`;
- contained Tab order;
- exact previous-control focus restoration when continuing editing;
- native `inert` background while discard confirmation is active;
- unambiguous accessible names;
- automated Axe WCAG A/AA checks on advanced surfaces;
- mobile Full Create at 390×844 with strict no-horizontal-overflow invariant;
- Timeline double-click and Shift-drag contextual manual entry;
- contextual gesture E2E anchored to a useful intersection of day-section, Timeline grid viewport and browser viewport, then reacquired after Create close;
- no arbitrary sleep/retry masking of contextual gesture failures;
- appearance-card filter/remount coverage without relying on an ephemeral imperative marker;
- frozen Timeline pointer/focus/drag behavior in Firefox;
- no AI/NL/voice affordance inside the Create product surface.

## 17. Performance / architecture proof

Current accepted design deliberately avoids speculative framework work.

Relevant guarantees:

- Create projections prepare layout in O(n) with cached group/day lookup and slot counters;
- local runtime is lazily initialized once per mounted entry;
- no component direct HTTP;
- no localStorage fake persistence;
- no ORM/DB-row-shaped frontend model;
- no duplicate Create engine per surface;
- no UI component dependency cycles;
- listener/RAF/observer cleanup remains covered by existing Timeline architecture/tests.

CI #632 architecture result:

```text
214 modules
522 dependencies cruised
0 dependency violations
```

## 18. Final automated evidence

Implementation candidate:

`7028633921d1b438bd04961a718457afd82ccc13`

Frontend CI:

`33635389124` / #632

Result:

- Quality — PASS;
- Mobile Bundle — PASS;
- Chromium full Web E2E — PASS;
- Firefox frozen Timeline interaction contract — PASS;
- Frontend CI Gate — PASS.

Quality evidence:

- frontend contract drift PASS;
- active Home format PASS;
- lint PASS;
- typecheck **5/5** PASS;
- architecture **214 modules / 522 dependencies / zero violations**;
- generated-source drift PASS;
- web unit suite **34 files / 183 tests PASS** plus package suites;
- production build PASS;
- diff check PASS;
- repository mutation check PASS.

Production Home route:

```text
268.40 kB raw
90.13 kB gzip
```

No dynamic split is added solely to recover gzip at the cost of asynchronous draft/focus/error complexity. Route splitting remains a measured future performance decision.

## 19. Backend stop line / disposition

The following remain intentionally outside C1:

- API transport;
- PostgreSQL writes/transactions;
- canonical server IDs;
- durable server idempotency;
- product Auth/ACL enforcement;
- provider/calendar synchronization;
- invitations and room/resource booking;
- conferencing creation;
- notification delivery;
- authoritative solver;
- recurrence evaluator/checkpoints;
- Occurrence generation;
- Session runtime;
- Actual/outcome execution runtime;
- multi-device reconciliation;
- AI/NL interpretation/runtime/input;
- voice runtime/input.

These are **deferred integration/runtime responsibilities**, not missing C1 fields.

## 20. Closure state

Automated engineering and traceability gates are satisfied on the implementation candidate.

C1 remains:

```text
IMPLEMENTATION FULL GREEN
DOCUMENTATION RECONCILIATION COMPLETE
FINAL DOCUMENTATION DESCENDANT MUST BE CI-GREEN
MANUAL ACCEPTANCE PENDING
NOT YET FROZEN / CLOSED
```

Only explicit user acceptance after the final documentation descendant is green and the single manual protocol is executed may transition C1 to `FROZEN / CLOSED` and authorize C2.
