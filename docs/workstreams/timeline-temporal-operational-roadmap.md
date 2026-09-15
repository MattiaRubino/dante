# Timeline / Temporal-Operational Vertical — Implementation Roadmap

- **Status:** FROZEN EXECUTION ROADMAP — ORDER AGREED 2026-09-07
- **Branch/workstream:** `feature/timeline-temporal-operational`
- **Protected-main anchor at roadmap freeze:** `981f6cf9ad985d0b811bc4172c12a7529fbc9b15`
- **Current protected-main DB authority at roadmap freeze:** PostgreSQL 18.6 / Alembic `20260906_18` / topology `89|5|18|77|173|91|272|0|0|0`
- **Semantic authority set:**
  - `docs/workstreams/timeline-temporal-operational-map.md`
  - `docs/workstreams/timeline-temporal-operational-second-audit-2026-09-07.md`
  - `docs/workstreams/timeline-temporal-operational-final-pre-roadmap-audit-2026-09-07.md`
- **Purpose:** define the exact implementation order and fixed execution discipline for completing the full Timeline / Temporal-Operational vertical end-to-end, without losing any item from the semantic map.

---

# 0. Fixed branch execution contract

This section is a **blocking rule of the workstream**.

## 0.1 Live progress source of truth

The canonical implementation-progress ledger lives in:

```text
docs/workstreams/timeline-temporal-operational-map.md
→ section "Live implementation progress ledger"
```

Every roadmap capability has a stable checklist ID.

Allowed statuses:

```text
⬜ NOT STARTED
🟨 IN PROGRESS
✅ DONE
⛔ BLOCKED
```

`✅ DONE` is intentionally strict.

A capability may receive a green check only when all applicable Definition-of-Done requirements are satisfied.

## 0.2 No stale checklist rule

For every implementation change:

```text
implementation change
+
required tests
+
manual acceptance evidence where applicable
+
progress-ledger update
+
same-change documentation
=
one reviewed slice
```

It is forbidden to:

- implement a capability and leave its ledger status stale;
- mark a capability `✅` before the real behavior exists;
- mark a capability `✅` merely because an old prototype/mock visually demonstrated it;
- defer known tests/documentation to a future cleanup block merely to call the current block complete;
- skip a map item because the next feature appears more useful.

If implementation discovers a new legitimate requirement:

1. stop the affected slice;
2. classify it against Domain/Logical/Physical authority;
3. add it to the map with a stable checklist ID;
4. place it into the roadmap/dependency graph;
5. only then continue implementation.

No hidden TODO is an acceptable substitute for this process.

## 0.3 Green-check Definition of Done

For a semantic/product capability, `✅` requires every applicable item below.

### Semantic gate

- exact owner/capability identified;
- relevant `!=` boundaries re-read and preserved;
- relation/cardinality/ownership semantics resolved to the degree needed by the slice;
- OPEN-BY-DESIGN questions required by this slice explicitly resolved or intentionally carried forward with a blocking future gate;
- no generic shortcut (`status`, `due_at`, `repeat`, `assigned_to`, generic JSON relation, etc.) introduced.

### Persistence gate

- current protected `main` and Alembic head reverified immediately before implementation;
- existing PostgreSQL/SQLAlchemy/Dictionary representation inspected first;
- new DDL introduced only when a real semantic persistence gap is proven;
- only forward Alembic migration used;
- historical migrations untouched;
- runtime ACL/migrator/owner/observer rules preserved;
- direct PostgreSQL proof added where schema/integrity changes.

### Backend/application gate

- governed application operation/query implemented;
- transaction owner explicit;
- adapters flush but do not hide commits;
- idempotency semantics classified;
- expected-state/concurrency semantics classified;
- retry behavior classified;
- partial/async outcome semantics truthful;
- history/current-state/provenance/reconciliation handled where consequential;
- DanteContext/auth/timezone/visibility requirements respected.

### Frontend gate

- frontend consumes real application/backend result;
- no fake backend success;
- no new runtime mock source;
- no canonical meaning inferred from ViewModel-only fields;
- F0/T1/C1 inherited interaction contracts preserved unless explicitly reopened;
- loading/pending/error/conflict/empty states truthful;
- accessibility and mobile behavior covered where affected.

### Automated-test gate

As applicable:

- domain/unit tests;
- application/service tests;
- PostgreSQL/direct integrity tests;
- API/integration tests;
- frontend unit/component tests;
- interaction regressions;
- E2E using real backend + real test PostgreSQL;
- timezone/DST/concurrency/idempotency tests;
- provider/offline/recovery tests for the relevant slice.

### Manual acceptance gate

- tested through the real product surface using isolated test data / `userTest` workflow;
- browser reload proves persistence where applicable;
- no mock-only success path;
- negative/error/conflict path tested where user-visible;
- manual findings recorded if behavior is not obvious from automated proof.

### Same-change documentation gate

If the slice changes persistence/contracts/behavior, applicable documentation must be updated in the same reviewed slice:

- semantic/workstream docs;
- Alembic/SQLAlchemy/Dictionary/database docs;
- frontend contract/registry;
- API/application contract;
- recovery/observability/security docs where affected;
- live progress ledger status/evidence.

Only after all applicable gates pass may the item turn `✅`.

## 0.4 No runtime mock rule

From the first real-data slice onward:

```text
normal DANTE runtime
→ no fake Timeline cards
→ no mock repository pretending persistence
→ no fake provider success
→ no fake notification success
→ no frontend-generated canonical recurrence
```

Mocks/fixtures remain valid only in explicitly bounded test contexts.

Recommended separation:

```text
unit/component tests
→ mocks/fixtures allowed

E2E/manual acceptance
→ real backend + isolated real PostgreSQL test data

normal app runtime
→ real application/backend data only
```

Historical prototype fixtures may be retained only if they are moved behind explicit test/dev-test boundaries and cannot contaminate normal runtime behavior.

## 0.5 Slice-over-layer rule

Implementation proceeds by **end-to-end capability slices**, not by finishing the whole frontend and later the whole backend.

Canonical development flow:

```text
semantic capability
→ current persistence inspection
→ DDL only if required
→ backend/application operation/query
→ API/transport
→ frontend integration
→ read model/projection
→ automated tests
→ manual userTest
→ ledger green check
```

A slice should leave DANTE capable of performing a real user-visible operation, not leave two disconnected half-implementations.

## 0.6 Shared capability rule

Shared semantic capabilities are implemented once and reused.

Examples:

```text
Activity ─┐
Event ────┼→ Schedule capability
Occurrence┘

Routine ──┐
Event ────┼→ Recurrence capability
          └→ Occurrence generation

Activity ─┐
Event ────┼→ Actual capability
Occurrence┘
```

The Event block must exercise/extend the Schedule capability created earlier; it must not clone `event_schedule` behavior independently.

## 0.7 Branch/merge discipline

The workstream documentation branch may hold the frozen map/roadmap, but implementation should remain reviewable in bounded slices.

Before creating each implementation branch:

1. re-read branch closure rules;
2. verify current protected `main` SHA and Alembic head;
3. confirm the previous required slice is actually integrated;
4. create the new bounded branch from that current protected `main`.

Suggested branch naming:

```text
feature/temporal-b00-real-data-spine
feature/temporal-b01-activity-core
feature/temporal-b02-schedule-core
...
```

Do not accumulate the entire vertical into one unreviewable implementation branch.

---

# 1. Roadmap dependency thesis

The order is dependency-driven, not noun-order-driven.

```text
REAL DATA SPINE
      ↓
ACTIVITY CORE
      ↓
SCHEDULE CORE
      ↓
EVENT CORE
      ↓
TEMPORAL CONSTRAINTS + PRODUCT ORGANIZATION
      ↓
ROUTINE / RECURRENCE / OCCURRENCE BASELINE
      ↓
SESSION RUNTIME
      ↓
ACTOR RELATIONS / PARTICIPATION BOUNDARY
      ↓
ACTUAL / OUTCOME / CONFIRMATION / RESOLUTION
      ↓
ADVANCED RECURRENCE / CONDITIONAL POLICY / REMINDERS
      ↓
REPLANNING / CONFLICT / SOLVER
      ↓
PROVIDER / OFFLINE / MULTI-DEVICE
      ↓
ANALYTICS / SIGNALS
      ↓
WHOLE-VERTICAL CLOSURE
```

Why this order:

- real data must exist before product behavior can be trusted;
- Activity is the simplest high-frequency originating owner and gives the first useful real product slice;
- Schedule is shared and must be established before Event/Routine can stress it;
- Event is the second owner used to prove Schedule was not designed Activity-specifically;
- Temporal Constraints and Life Area organization are required before serious recurring/replanning behavior;
- Routine/Recurrence/Occurrence baseline must exist before execution/resolution can be tested across repeated expectations;
- Session creates actual execution facts;
- Actual/Outcome/Confirmation become meaningful after execution and expectations exist;
- completion-relative and anchor-stream recurrence require Actual/Session anchors, so they intentionally come later;
- replanning needs real constraints/history rather than an invented planner state;
- providers/offline should synchronize DANTE semantics, not define them;
- analytics should consume mature canonical history, not prototype status fields;
- closure happens only after the entire vertical survives recovery/privacy/performance/QA.

---

# 2. B00 — Real Data Spine and runtime mock retirement

## Objective

Create the minimum real end-to-end application path that all later temporal capabilities will use, and remove normal-runtime dependency on fake Timeline/product data.

## Scope

Backend/application foundation:

- authenticated `DanteContext` path verified;
- Account → self Person application context available;
- effective request timezone available;
- application operation/query pattern for temporal vertical established;
- transport boundary established;
- runtime result/error mapping established;
- real PostgreSQL-backed query path established.

Frontend foundation:

- temporal feature data source goes through feature/application adapter;
- normal Timeline runtime no longer depends on hard-coded cards/mock repository;
- empty state is truthful when DB contains no temporal product data;
- test fixture/demo data isolated from normal runtime.

Testing foundation:

- isolated test account/data workflow (`userTest` or equivalent accepted test fixture identity) defined;
- E2E can run against real backend + test PostgreSQL;
- seed/setup/cleanup is deterministic;
- reload/session boundary can verify persistence in later blocks.

## Explicit non-goals

B00 does not invent Activity/Event schema merely to make a demo card appear.

It does not authorize generic `temporal_item` or `timeline_entry` persistence.

## Required proof

- normal runtime with empty DB renders no fake temporal cards;
- test fixture path can intentionally create bounded test data without leaking into normal runtime;
- backend/frontend failures remain visible and are not replaced by mock success;
- F0/T1 behavior unaffected.

## Exit condition

B01 can implement `CreateActivity` without inventing a second data-source architecture.

---

# 3. B01 — Activity Core: first real originating owner

## Objective

Make the most common `+` path create a real persistent Activity and render that same Activity through the real product read path.

## UX shape

Opening `+` goes directly to structured Create with:

```text
CREA
[ Activity ] [ Event ] [ Routine ]

REGISTRA
Session
```

At B01 only Activity becomes a real enabled creation operation. Other macro choices may remain visibly staged/disabled until their block, but must not fake success.

Activity is the default selected class to minimize the common-path click count.

## Semantic scope

Resolve only the Activity product state necessary for a real first lifecycle while preserving future compatibility:

- stable Activity identity;
- minimum meaningful actionable-intention/descriptive state;
- optional unplaced state;
- no generic status/done/repeat/due_at field;
- Activity remains separate from Schedule/Session/Actual/Outcome.

If a durable Activity descriptive/profile representation is missing from current Physical baseline, prove and implement the smallest typed forward extension required.

## Backend/application

Required operation/query concepts:

- `CreateActivity`;
- fetch/list/query unplaced Activities for Planning Tray;
- fetch Activity detail sufficient for current projection;
- idempotent create operation;
- authenticated ownership/context handling;
- no hidden commit inside adapter.

## Frontend

- Activity default selected in Create;
- create draft is not canonical Activity;
- submit calls real operation;
- pending/error/applied state truthful;
- successful create appears through refreshed real query;
- unplaced Activity appears in Planning Tray;
- browser reload preserves it;
- no duplicate Activity when projection refreshes.

## Tests

Minimum:

- creation validation;
- idempotent retry same payload;
- same idempotency key + different payload conflict;
- unauthorized context rejection;
- real PostgreSQL persistence;
- frontend submit/pending/error/success;
- E2E create → Planning Tray → reload;
- dirty draft discard != Activity delete/cancel.

## Exit condition

DANTE can create one real unplaced Activity from `+` with zero runtime mock dependence.

---

# 4. B02 — Schedule Core and first real Timeline mutation

## Objective

Implement Schedule once as a shared capability and make Activity placement/movement real, history-preserving and concurrency-safe.

## Semantic scope

- Schedule subject eligibility beginning with Activity;
- exact placement forms supported by current CP6/F0;
- coarse accepted placement semantics where required by final audit;
- Schedule current accepted MaterialState/history;
- accepted Schedule != proposal;
- Schedule absent remains valid;
- 0..N placement semantics not prematurely collapsed to one universal Schedule;
- actual execution remains out of scope.

## User operations

- create Activity already placed from Create;
- Planning Tray → Timeline placement;
- Timeline move earlier/later;
- resize/adjust end where current UI contract supports it;
- anchored time editor;
- unschedule back to Planning Tray where Activity semantics permit;
- guarded Undo;
- exact time correction versus new accepted replan semantics classified.

## Backend/application

- create/attach accepted Schedule;
- revise Schedule MaterialState;
- explicit current binding;
- historical state preservation;
- expected-state check;
- idempotency;
- no stale last-write-wins;
- local-day/range query enough to project scheduled Activity.

## Frontend

Existing T1 gestures become real backend operations without changing frozen interaction grammar.

```text
drag
→ mutation
→ authoritative result
→ projection refresh
```

not local coordinate mutation masquerading as truth.

## Tests

- all supported Schedule forms;
- reschedule earlier/later;
- duration expansion/reduction;
- unschedule;
- identity stable through movement;
- history/current binding;
- stale expected revision conflict;
- guarded Undo;
- DST/local-day query cases where this slice exposes them;
- Planning Tray placement identity preservation;
- Firefox T1 regression suite remains green;
- E2E create → place → move → reload → history/read current.

## Exit condition

Activity + Schedule is a real complete product loop and Schedule is reusable by Event/Occurrence.

---

# 5. B03 — Event Core using the shared Schedule capability

## Objective

Implement Event as a distinct originating owner and use it to prove that Schedule/read-model/UI abstractions are not Activity-specific.

## Semantic scope

- Event identity/expectation;
- timed Event;
- all-day/date-span Event;
- multi-day Event;
- current Schedule plus historical expectation;
- postponed/TBD with no current Schedule;
- Agenda/internal Event parts at their accepted product level;
- Place/conference field only through justified existing relation/profile semantics;
- Participation/provider execution not yet fully implemented unless required for minimum Event create.

## Frontend

`Event` macro choice becomes active.

The Create tree shows Event-specific fields only:

- time/date semantics;
- all-day/multi-day;
- Agenda/internal structure;
- applicable context.

Do not implement one universal form object with hidden irrelevant fields.

## Shared capability proof

Event placement must reuse B02 Schedule operations/read model.

No separate Activity/Event time engine.

## Tests

- timed Event create;
- all-day lane rendering;
- multi-day rendering/query;
- reschedule preserving identity/history;
- postponed/TBD without fake placeholder time;
- Event Agenda part != Activity owner by default;
- Event plus scheduled Activity overlap UI behavior remains deterministic;
- reload persistence;
- Activity Schedule regressions rerun against shared capability.

## Exit condition

Activity and Event are both real, and Schedule has survived two semantic owners.

---

# 6. B04 — Temporal Constraints and movement-policy foundation

## Objective

Represent the difference between accepted placement, temporal admissibility/preference and governance of movement.

## Semantic scope

Implement only typed forms justified for first vertical use, but architecture must preserve the larger accepted family:

- earliest start;
- latest start;
- latest completion/delivery / Deadline semantics;
- hard validity window;
- preferred/soft window;
- minimum/maximum duration;
- minimum contiguous execution duration;
- spacing/recovery;
- relative before/after where required;
- movement policy separate from constraints.

## Important boundaries

```text
Temporal Constraint != Schedule
Deadline != universal due_at
movement policy != Temporal Constraint
constraint violation in Actual != invalid history
```

## Product behavior

- advanced Create/detail can express only supported typed constraints;
- user sees when a proposed manual placement violates a hard/soft constraint;
- soft warning does not become hard rejection;
- hidden constraints are not silently ignored.

## Tests

- hard vs soft;
- exact constrained facet;
- Deadline passage does not create Outcome;
- Schedule revision against constraint;
- range/DST edge where applicable;
- constraint display/explanation;
- no generic `due_at` fallback.

## Exit condition

Planning semantics have real constraints and movement governance suitable for recurrence/replanning later.

---

# 7. B05 — Product organization: Calendar / Life Area + Tags

## Objective

Replace prototype grouping assumptions with real user-controlled product organization while preserving Domain separation.

## Semantic/product scope

- primary Calendar/Life Area organization;
- user-defined labels such as `Palestra`, `Inglese`, `Lavoro`;
- create/rename/reorder/archive/hide/show;
- icon/color/appearance as presentation metadata, not semantic owner;
- tags as secondary many-valued organization;
- item relation to one primary Life Area where product contract requires it;
- Goal/Plan links remain distinct future relations;
- shared-item actor-local organization requirement preserved even if collaboration is not activated yet.

## Frontend

- Timeline groups/filtering consume real organization;
- no hard-coded prototype group strings as canonical taxonomy;
- hidden group does not erase scheduling/conflict truth;
- color is not sole information carrier.

## Backend/persistence gate

Life Area is an LR-12/product-organization question, not permission to create a new LR-01 owner.

Exact durable representation must be proven against current Logical/Physical model before DDL.

## Tests

- create/rename/reorder/archive/hide;
- Activity/Event assignment;
- tags independent of Life Area;
- same visible label as Goal would not imply same identity;
- filter/group changes do not duplicate item;
- hidden items remain queryable to authorized conflict logic;
- accessibility presentation checks.

## Exit condition

Real Timeline data can be organized into user-defined life areas without ontology shortcuts.

---

# 8. B06 — Routine + Recurrence + Occurrence baseline

## Objective

Activate the third macro creation class and implement the four CP6-materialized recurrence families end-to-end, including backend-generated Occurrences and series editing boundaries.

## Routine scope

- Routine identity/product state;
- recurrence material state;
- pause/resume/end lifecycle if required by first usable Routine;
- composite/internal structure only to the extent needed by accepted product behavior;
- Life Area/context links;
- no `Activity.repeat` persistence.

## Recurrence baseline scope

Implement/runtime-author the four existing CP6 families:

- calendar wall-clock;
- elapsed interval;
- quota per period;
- cyclic positional.

Also preserve:

- pattern anchor/phase;
- effective range;
- open/until/count semantics;
- timezone mode;
- quota period frame;
- DST behavior;
- not-generated-by-rule != generated-and-skipped;
- virtual future vs materialized instance threshold.

Completion-relative and anchor-stream-relative remain deferred to B10 because they require Actual/Session anchors.

## Occurrence generation scope

- backend generation/evaluator/checkpoint;
- no browser canonical expansion;
- stable Occurrence identity when materialized;
- `recurrence_generated` exact governing Recurrence MaterialState + compatible coordinate;
- `explicit_extra` source relation but **no governing recurrence state**;
- Schedule optional;
- this occurrence vs this-and-future editing boundary;
- historical Occurrences retain generating state.

## Event recurrence

The same recurrence capability must also support recurring Event semantics, proving reuse.

## Tests

- each of four CP6 families;
- recurrence anchor/effective range;
- DST wall-clock behavior;
- quota instances without exact times;
- explicit extra;
- structural exclusion vs skip;
- this occurrence only;
- this and future;
- source recurrence revision with old Occurrence provenance retained;
- virtual future invalidation vs materialized history preservation;
- Event and Routine reuse;
- browser never fabricates canonical future Occurrences.

## Exit condition

Routine and recurring Event generate real backend-governed Occurrences that Timeline can query/render correctly.

---

# 9. B07 — Session Runtime: actual execution episodes

## Objective

Make `REGISTRA Session` real and allow Activity/Occurrence execution to create real Session history without conflating execution with completion.

## Capture paths

- spontaneous manual retrospective Session;
- timer/stopwatch start;
- pause;
- resume;
- end;
- contextual start from Activity;
- contextual start from Occurrence;
- imported/automatic capture architecture boundary retained for B12.

## Semantic/runtime scope

- Session identity;
- absolute/elapsed-only timing;
- timing precision;
- pauses;
- elapsed/active/paused derived durations;
- execution-context relation shape explicitly designed before persistence;
- Session may exist with no Activity/Schedule;
- Session end != Activity/Occurrence completion;
- correction preserves identity;
- split/merge lineage;
- false record deletion/invalidation boundary;
- overlapping Sessions allowed where semantically compatible;
- stale-running detection/review;
- device/source provenance baseline.

## Multi-surface foundation

Even before full offline sync, Session commands must support:

- idempotent control operations;
- expected current state/revision;
- conflict rather than silent last-write-wins;
- web/mobile-compatible command semantics.

## Tests

- manual Session;
- spontaneous Session;
- start/pause/resume/end;
- pause does not split identity;
- explicit end then later new Session;
- correction;
- split/merge;
- overlapping Sessions;
- stale-running warning/proposal;
- concurrent operations;
- timing precision;
- no fake Activity creation;
- end Session leaves Activity completion unresolved;
- E2E timer persistence through reload/reconnect behavior supported by current runtime.

## Exit condition

DANTE has a trustworthy actual-execution record independent from planned Schedule and completion status.

---

# 10. B08 — Actor relations: Responsibility / Participation integration

## Objective

Introduce the actor/context relations needed by Activity/Event lifecycle without using ambiguous `assigned_to` or generic participant blobs.

## Responsibility scope

Preserve separately:

- requester;
- responsible/accountable Actor;
- expected performer;
- actual performer;
- Authority where later applicable.

A first personal/self-only slice may be intentionally narrow, but the persistence/API shape must not make later distinction impossible.

## Participation scope

For Event:

- invited/intended participation;
- response: accepted/tentative/declined/unknown;
- Actual participation/attendance separate;
- response history where material;
- no-response != declined;
- accepted != attended.

## Acknowledgement boundary

Where shared material Schedule changes eventually require common ground, preserve Acknowledgement semantics without forcing it on ordinary personal scheduling.

## Tests

- self responsibility path;
- participant response state/history;
- actual attendance independent from response;
- unexpected attendance without prior invitation;
- no ambiguous assigned_to/participants JSON;
- Event occurrence remains shared while actor-specific participation differs.

## Exit condition

Temporal owners can express actor-specific responsibility/participation without collapsing roles.

---

# 11. B09 — Actual + Outcome + Confirmation + Resolution Queue

## Objective

Close the expectation→reality→result→attestation loop and make `Da risolvere` a real derived workflow.

## Actual scope

- Activity/Event/Occurrence subject eligibility;
- realization occurred / known non-realization / partial/different semantics as justified;
- timing where applicable;
- 0..N Session basis where applicable;
- no Actual remains unknown rather than negative;
- competing assertion/reconciliation boundary;
- current accepted realization MaterialState/history.

## Outcome scope

Implement only typed/context-specific result vocabulary needed by actual product scenarios.

No universal success/failure enum.

## Confirmation scope

- confirmer Actor;
- exact target/material state;
- purpose/context;
- historical binding;
- correction to target invalidates automatic carry-forward;
- no Confirmation != false.

## Resolution Queue

Derived query reasons:

- Actual unknown after expectation window;
- Outcome required but absent;
- Confirmation required;
- Session anomaly;
- provider/reconciliation conflict when later enabled.

Quick actions such as:

```text
Fatto
Parziale
Saltato
Posticipato
Sostituito
Conferma
Correggi
```

must map to exact operations/effects rather than generic status.

## Atomic operation requirement

One-tap `Fatto` may need:

```text
Actual
+
Outcome
+
Confirmation
```

If product semantics require all of them, the local PostgreSQL operation must be atomic.

## Tests

- unknown vs known non-realization;
- multiple Sessions supporting one Actual;
- Event Actual without Session;
- partial/different realization;
- context-specific Outcome;
- no Outcome != negative;
- Confirmation binds S1 and not corrected S2;
- no-answer remains unresolved;
- Resolution Queue appears/disappears based on real facts;
- multi-effect atomicity;
- history/reconciliation.

## Exit condition

DANTE can truthfully answer what was expected, what happened, what resulted and what the user actually confirmed.

---

# 12. B10 — Advanced Recurrence + Conditional Policy + reminders/review automation

## Objective

Add recurrence families and conditional behavior that depend on real Session/Actual/Outcome facts, then connect reminder intent to existing shared delivery infrastructure.

## Advanced recurrence

- completion-relative recurrence;
- anchor-stream-relative recurrence;
- qualifying Actual/Session anchor definition;
- sequential-chain behavior;
- no premature future generation when qualifying anchor absent;
- history under source revisions.

A dedicated forward persistence/runtime change is allowed only after proving the CP6 four-family baseline cannot represent these semantics honestly.

## Conditional Policy

- transition activation vs persistent-state activation vs repeated observation;
- bounded response semantics;
- dedup/idempotency;
- competing policy detection;
- loop/cycle runtime safeguards;
- policy activation != response success.

## Review/confirmation policy

- immediate request;
- later/day-end;
- weekly review;
- silent unresolved;
- explicitly authorized automatic bounded outcome.

## Reminder intent

- reminder intent owned by applicable policy/workflow;
- delivery channel external;
- existing Shared Email Platform reused for email;
- durable intent in canonical transaction when required;
- provider I/O after commit;
- ambiguous provider result not blindly retried;
- no fake human Confirmation.

## Tests

- completion-relative waits for qualifying Actual;
- anchor-stream generates one expected instance per qualifying anchor as defined;
- duplicate source fact does not duplicate effect;
- transition vs persistent activation;
- policy loop safeguards;
- automatic outcome preserves policy provenance;
- reminder intent/delivery separation;
- email ambiguity/retry semantics;
- daily/weekly review grouping.

## Exit condition

Advanced recurrence and review/reminder automation operate from real canonical facts without becoming a generic workflow engine.

---

# 13. B11 — Replanning / conflict / solver candidate flow

## Objective

Implement explainable constraint-aware replanning only after real temporal truth, constraints and movement policies exist.

## Inputs

- current accepted Schedule;
- Activity/Event/Occurrence identities;
- hard/soft Temporal Constraints;
- movement policy;
- Routine source/Occurrence exception boundaries;
- fixed commitments;
- relevant Life Areas including hidden ones;
- actor relations where relevant;
- history/Actual information where allowed/useful;
- Availability/Capacity only through its separate accepted boundary if/when available.

## Candidate semantics

OR-Tools/other planner output is candidate state only.

```text
solver candidate != accepted Schedule
```

## Product behavior

Show:

- proposed moves;
- affected items;
- hard violations prevented;
- soft trade-offs;
- hidden conflicting commitments safely disclosed;
- smallest useful replan scope;
- this occurrence vs future source impact.

User/application Authority applies accepted effects unless explicit bounded automation is configured.

## Fallback semantics

Support only justified operations from map:

- move;
- postpone;
- skip;
- shorten;
- split;
- replace;
- preserve priority portion;
- expand scope to dependencies/day/week only when required.

## Tests

- proposal != applied effect;
- stale candidate rejected/recomputed;
- hard/soft constraint behavior;
- hidden Life Area conflict awareness;
- occurrence-vs-series scope;
- minimal replan scope;
- explanation does not leak unauthorized details;
- solver absence/failure leaves canonical state unchanged.

## Exit condition

DANTE can propose and apply governed replans without collapsing planner state into truth.

---

# 14. B12 — Provider integration + offline / multi-device reconciliation

## Objective

Synchronize external calendars/capture surfaces with already-established DANTE semantics rather than designing DANTE around provider schemas.

## Provider Event/Occurrence/Schedule

- ExternalRef mapping;
- provider series/instance identity separate from DANTE Event/Occurrence;
- import/update/deletion/tombstone;
- provider Schedule assertion separate from accepted DANTE Schedule;
- detached recurring instances;
- unsupported/lossy recurrence mapping explicit;
- user correction protected from blind provider overwrite;
- external apply state truthful.

## Session imports

- provider/source app/device identity;
- imported timing/provenance;
- duplicate detection;
- later provider update versus user correction reconciliation.

## Offline/multi-device

When the selected Physical target is activated:

- local state explicitly noncanonical;
- pending/offline operation state visible;
- reconnect/replay idempotent;
- expected-state conflict resolution;
- device clock drift handling;
- concurrent Web/Mobile Session control;
- no silent last-write-wins.

## Tests

- provider identity separation;
- recurrence mapping failure path;
- provider tombstone;
- user-corrected imported record then provider update;
- offline create/move/session control as supported;
- replay duplicate;
- concurrent mutation conflict;
- clock drift;
- provider ambiguous result;
- no local copy presented as canonical before acceptance.

## Exit condition

External systems and offline clients integrate without becoming the source of ontology or silently overwriting canonical DANTE truth.

---

# 15. B13 — Analytics / statistics / Signals

## Objective

Expose trustworthy user-facing statistics derived from mature canonical temporal history.

## Base analytics

- scheduled duration;
- Session elapsed duration;
- active duration;
- paused duration;
- start/end deviation;
- early/late start/finish;
- overrun/underrun;
- Schedule revision count;
- postpone/cancel/skip patterns;
- expected Occurrence counts;
- Actual coverage;
- context-specific Outcome distributions;
- Confirmation coverage;
- time allocation by Life Area/tag;
- week/month/year range trends.

## Routine analytics

Adherence/streak require the exact evaluation basis:

- expected Occurrences;
- Actuals;
- Outcomes;
- Confirmation policy/current truth;
- period boundaries;
- any specialist criterion needed.

## Overlap handling

Distinguish:

- raw Session duration;
- unique wall-clock coverage;
- active effort;
- category/domain contribution;
- intentional multi-domain overlap.

No universal `SUM(duration) = time spent` rule.

## Privacy/current-truth behavior

- corrected accepted facts drive ordinary analytics;
- audit history remains separate;
- deletion/redaction propagates appropriately to derived user-linked analytics;
- hidden/private details do not leak through aggregates/explanations;
- product analytics != OTel/Grafana operational telemetry.

## Tests

- planned vs actual calculations;
- overlap cases;
- recurrence adherence;
- corrected timing changes analytics;
- deleted/redacted source behavior;
- timezone period boundaries;
- DST week/day ranges;
- Life Area aggregation;
- authorization/disclosure.

## Exit condition

User statistics are reproducible from canonical semantics and do not invent a universal productivity ontology.

---

# 16. B14 — Whole Vertical Closure

## Objective

Prove the temporal-operational vertical as one coherent production-quality capability before branch/workstream closure.

## Functional closure sweep

Every live ledger item in the map must be either:

```text
✅ DONE
```

or explicitly excluded by a newly approved scope change recorded in authority docs.

No silent leftover `⬜`/`🟨` may be ignored during closure.

## Cross-cutting closure

- Auth/DanteContext;
- timezone/Clock/DST;
- idempotency/concurrency;
- history/current-state/provenance;
- privacy/retention/deletion;
- visibility/non-interference;
- provider/offline consistency;
- observability;
- recovery/PITR anti-resurrection implications;
- async outbox/delivery recovery;
- performance/index/query review;
- Dictionary/SQLAlchemy/Alembic/live DB alignment;
- no runtime mocks;
- frontend T1/F0/C1 regressions;
- mobile/accessibility;
- documentation drift check.

## Adversarial scenario rerun

Re-run the final pre-roadmap adversarial suite, including:

- unplaced Activity;
- multiple Schedule placements;
- early/late/extended execution;
- recurrence exception vs future change;
- explicit-extra Occurrence;
- structural exclusion vs skip;
- Session concurrency/offline/drift;
- Confirmation then correction;
- unresolved/no-response;
- automatic outcomes;
- provider ambiguity;
- DST gap/repeat;
- hidden Life Area conflict;
- stale drag;
- idempotency collision;
- PITR anti-resurrection;
- privacy-safe busy projection.

## Recovery closure

Where the vertical introduces new canonical/history/outbox state, prove backup/restore/reconciliation implications and prevent recovery from silently resurrecting retired current state.

## Performance closure

Use realistic range windows/dataset cardinalities to verify:

- Timeline range query;
- recurrence horizon/materialization;
- Planning Tray;
- Resolution Queue;
- history/detail;
- analytics;
- indexes/query plans where needed.

## Final acceptance

- automated CI green;
- direct PostgreSQL acceptance green;
- E2E green;
- manual `userTest` end-to-end walkthrough green;
- progress ledger 100% reconciled;
- no undocumented schema drift;
- no protected-main direct writes;
- branch closure rules followed.

## Exit condition

The vertical is ready for formal branch/workstream closure and protected-main integration under repository governance.

---

# 17. Roadmap-to-map traceability

| Roadmap block | Primary map capability sections |
| --- | --- |
| B00 | §21, §22, §24, §25, §28, runtime/mock/test ledger |
| B01 | §4, §5, §20, §24, §25.3 |
| B02 | §10, §21, §22, §24, §25 |
| B03 | §6, shared §10, §25 |
| B04 | §11, §19, §21 |
| B05 | §20, §25, §26 |
| B06 | §7, §8, §9, shared §10, §21, §22, §25 |
| B07 | §12, §21, §22, §24, §25 |
| B08 | Responsibility/Participation boundaries in §5/§6/§16/§29 plus companion audits |
| B09 | §13, §14, §15, §16, §17, §22, §25.4 |
| B10 | §8 advanced families, §17, §18, §23 |
| B11 | §11, §19, §25.6, §26 |
| B12 | §12.19, §22, §23, §24, §28 |
| B13 | §26 plus privacy/history boundaries |
| B14 | entire map + both completeness audits + final audit adversarial suite |

The live checklist IDs in the primary map are the blocking execution ledger for this traceability.

---

# 18. Roadmap freeze result

```text
ROADMAP STRUCTURE                       FROZEN
END-TO-END SLICE RULE                  FROZEN
LIVE GREEN-CHECK RULE                  FROZEN
NO-RUNTIME-MOCK RULE                   FROZEN
SHARED-CAPABILITY-ONCE RULE            FROZEN
PER-SLICE TEST + USERTEST RULE         FROZEN
SAME-CHANGE DOCUMENTATION RULE         FROZEN

IMPLEMENTATION                         NOT STARTED BY THIS DOCUMENT
NEXT IMPLEMENTATION BLOCK              B00 — REAL DATA SPINE
```

Changing the block order or skipping a ledger item requires an explicit roadmap amendment with reason and dependency analysis; it must not happen implicitly during coding.

---

## 19. Live progress addendum — 2026-09-15

The frozen block order is unchanged. Current execution has reached B02 Schedule Core:

```text
B00                         ✅ CLOSED
B01                         ✅ CLOSED
B02-A/B/C/D                 ✅ PROVEN
B02-E PRE-SCOPE             ✅ APPROVED
B02-E1                      ✅ PROVEN — 29 local tests; 4 PostgreSQL tests
NEXT                        B02-E2 — Timeline read projection and DST
CI                          DEFERRED BY USER INSTRUCTION
```

This addendum reports execution progress only; it does not amend the frozen roadmap structure or promote B02-E2/E3/E4.
