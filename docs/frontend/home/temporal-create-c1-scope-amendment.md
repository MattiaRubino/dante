# DANTE — Temporal Create C1 Scope Amendment

**Status:** ACTIVE AUTHORITY — IMPLEMENTATION COMPLETE / AUTOMATED PASS / MANUAL ACCEPTANCE PENDING  
**Original amendment date:** 2026-09-01  
**Final implementation reconciliation:** 2026-09-02  
**Owner workstream:** `feature/home-timeline`  
**Integration target:** `feature/home-react`  
**Final implementation candidate:** `81808814abb4e4998c7bde5b0c6cb8f5f903aa62`  
**Frontend CI:** `33613239926` / #536 — FULL PASS  
**Supersedes where conflicting:** `temporal-create-q0-contract.md`, `temporal-create-q0-approval.md`, and the original bounded C1 section of `temporal-frontend-roadmap.md`  
**Scope stop:** maximum useful pre-backend Create system; no real API, PostgreSQL application persistence, provider execution, authoritative solver, recurrence evaluator, AI runtime, voice runtime or server-side product Auth/ACL implementation

## 1. Why this amendment exists

The original Q0/C1 contract intentionally bounded the first Create vertical to a compact Activity/Event grammar.

The user later explicitly required the `+` workstream to reach the **maximum useful frontend/application depth before backend integration**, rather than stop at Quick Add.

This amendment therefore expands C1 while retaining Q0/F0 rules for semantics, architecture, validation, accessibility, performance, operation truth and backend separation.

C1 closes only when its UI/application design can connect to future backend adapters without structural redesign.

## 2. Permanent semantic invariants

```text
Activity != Event
identity != placement
Schedule != Occurrence != Session != Actual
planned != actual
recurrence source != generated Occurrence
all-day != midnight hack
floating local != zoned != absolute
unscheduled != invalid
proposal != accepted effect
calendar/context != sharing/ACL
manual input != AI interpretation
frontend projection id != canonical backend identity
ViewModel != application model != DTO != DB row
```

No richer UI may collapse these distinctions for convenience.

## 3. Product topology — one capability, progressive surfaces

```text
ENTRY
  ├── Timeline/header +
  ├── contextual Timeline double-click
  ├── contextual Timeline range
  ├── future global Create
  ├── future keyboard command
  ├── future import
  ├── future deterministic/NL interpretation
  ├── future voice
  └── future governed DANTE intelligence
          │
          ▼
      SHARED CREATE DRAFT
          │
          ├── QUICK CREATE
          ├── EXPANDED CREATE
          └── FULL CREATE EDITOR
          │
          ▼
      normalize / validate
          │
          ▼
      candidate preview
          │
          ▼
       user commit
          │
          ▼
      F0 command boundary
          │
          ▼
 local deterministic adapter now
 authoritative backend adapter later
```

Quick, Expanded and Full are views of one application capability, never three independent Create engines.

## 4. Quick Create role

Quick must remain intentionally fast and calm.

Its common path is limited to high-frequency creation data such as:

- title;
- Activity/Event;
- primary temporal placement;
- context/calendar/life area;
- clear expansion path;
- truthful commit/cancel behavior.

Deep recurrence, planning and integration details belong to progressive disclosure, not the resting Quick surface.

## 5. Activity creation scope

Activity may progressively author:

### Identity / organization

- title;
- context/life area;
- notes;
- owning-vertical handoffs where real owners exist.

Generic tags/labels are **not** part of the current C1 contract because there is no approved generic owner model that justifies inventing one in Create.

### Scheduling intent

- fixed placement;
- all-day/date form where meaningful;
- unscheduled/open Activity;
- bounded scheduling window;
- deadline-constrained Activity;
- preferred window;
- earliest start and due/deadline boundary where applicable;
- floating/named-zone semantics where applicable.

Flexible scheduling intent may exist before a solver. In that case C1 retains structured intent and **does not fake a concrete accepted Schedule**.

### Duration / execution intent

- expected duration, including exact non-preset values in deeper surfaces;
- indivisible/splittable structure;
- minimum session duration;
- maximum sessions where meaningful;
- preparation/recovery/spacing;
- partial completion allowed;
- early finish when result reached;
- compatible merge intent.

These fields are planning intent. They do not fabricate Session or Actual records.

### Replanning / fallback

- locked;
- movable inside window;
- confirmation-required;
- freely replannable;
- fallback such as skip, same window, next valid date, shorten/split or dependency replan.

C7 still owns broader candidate-plan/conflict/replanning experience.

### Recurrence ownership — final clarification

Activity does **not** own recurrence.

Current CP6/Alembic M4 materializes recurrence families only for Routine and Event. Therefore C1 must preserve:

```text
persistent repeated Activity intent
→ Routine owning vertical
→ Routine Recurrence
→ backend Occurrence generation later
```

No `Activity.repeat`, no Activity recurrence editor and no Activity recurrence capability may be introduced.

### Confirmation / reminder intent

C1 may author confirmation/outcome/review/reminder policy where product-defined, but must not fabricate notification delivery or Actual outcome.

## 6. Event creation scope

Event has a distinct time-centred grammar and may author:

- title;
- start/end/duration;
- all-day multi-day date span;
- floating-local / named-zone semantics;
- IANA timezone;
- context;
- location;
- notes;
- availability/busy intent;
- visibility distinct from ACL;
- purpose;
- expected outcome;
- agenda;
- decision-required intent;
- preparation/recovery buffers;
- recurrence;
- confirmation/reminder policy;
- participant/resource/pre-read/conference integration intent.

Invitations, resource booking, conferencing and provider writes remain truthful unavailable integration seams.

## 7. Event recurrence scope

C1 Event recurrence must preserve all four CP6 M4 families:

```text
calendar_wall_clock
elapsed_interval
quota_per_period
cyclic_positional
```

Current accepted creation depth:

### Calendar / wall-clock

- daily;
- weekly + weekdays;
- monthly civil-date anchor;
- monthly ordinal weekday;
- yearly civil-date anchor;
- positive interval;
- open/until/count termination.

### Elapsed interval

- positive elapsed interval authoring;
- no browser-side evaluator execution.

### Quota per period

- quota count;
- day/week/month/year;
- every N periods;
- frame `floating-local | named-zone | absolute-UTC`;
- week start when weekly;
- IANA period zone when named-zone.

### Cyclic positional

- cycle length;
- day/week position unit;
- multiple active positions;
- human-friendly 1-based UI representation.

C1 stores specification only. M6/backend owns recurrence-generated Occurrence creation and exact governing recurrence-state binding.

## 8. Other DANTE object types / handoff

Timeline `+` is not a universal CRUD factory.

C1 has a typed owner handoff registry for:

- Project;
- Goal;
- Routine;
- Program;
- World;
- Template;
- Reminder;
- Block;
- Asset.

Current availability is explicitly `deferred` for all targets.

The application handoff contract preserves a normalized immutable Create draft snapshot and contains no route, href, fake CRUD or fake success.

An owning vertical may later activate the seam without moving its model into Timeline Create.

## 9. Structured future-input seam

C1 owns a source-neutral `TemporalCreateFieldSeed` and invocation path.

Future inputs may include:

- global Create;
- keyboard command;
- import;
- governed DANTE interpretation;
- voice adapter after that vertical exists.

They must all converge on the same normalization, validation, preview and commit path.

DANTE must not automate Create by clicking UI controls.

C1 does not implement AI/voice interpretation/runtime itself.

## 10. UI / interaction quality target

The complete C1 system must remain a mature application surface rather than an administrative form.

Required:

- title dominance and fast common path;
- semantic grouping;
- Activity/Event-specific sections;
- progressive disclosure;
- contextual Timeline prefill;
- distinct candidate preview;
- responsive popover/full-screen strategy;
- keyboard/focus ownership;
- dirty-discard protection;
- touch/pointer safety where applicable;
- reduced-motion compatibility with frozen Timeline;
- IT/EN i18n;
- unambiguous accessible names;
- no raw debug/i18n keys;
- no misleading unavailable affordance;
- mobile containment/no horizontal overflow.

## 11. Application architecture requirements

C1's accepted application layer includes only abstractions demonstrated by real needs:

- structured Create draft/session;
- Activity scheduling/execution intent;
- Event recurrence/event intent;
- confirmation/reminder intent;
- candidate Timeline projection;
- deterministic validation;
- F0 prepared command/result path;
- rich-intent metadata/idempotency;
- structured field seed;
- typed external-owner handoff;
- immutable application-boundary prepared snapshot;
- local deterministic runtime;
- Undo/reveal integration.

Do not mirror PostgreSQL rows or invent REST DTOs.

## 12. Relationship with later temporal phases

C1 owns **initial creation-time authoring**.

C5 still owns deeper editing of existing recurrence/flexibility/source scope, including this occurrence vs future/source behavior.

C6 owns runtime Session/Actual/execution/correction surfaces.

C7 owns conflict/proposal/affected-item/replanning experience and future solver integration.

C2 remains the immediate next capability after C1 freeze: Card → structured Detail.

## 13. Backend stop line

The later backend/external vertical owns:

- API transport;
- canonical identities;
- PostgreSQL transactions/application persistence;
- durable server idempotency;
- product Auth/ACL enforcement;
- provider/calendar sync and writes;
- invitations/room/resource/conference execution;
- notification delivery;
- authoritative solver;
- recurrence evaluator/checkpoints;
- Occurrence generation;
- Session runtime;
- Actual/outcome runtime;
- multi-device reconciliation;
- AI runtime;
- voice runtime.

Connecting these should extend/replace adapters and external seams rather than force a Create UI/application rewrite.

## 14. Final implementation reconciliation

Implementation candidate:

`81808814abb4e4998c7bde5b0c6cb8f5f903aa62`

CI #536 / run `33613239926` proves:

- Quality PASS;
- Mobile PASS;
- full Chromium Web E2E PASS;
- frozen Firefox Timeline interaction PASS;
- final gate PASS.

Current measurable evidence:

- architecture 199 modules / 477 dependencies / zero violations;
- web unit 28 files / 168 tests;
- Home route `252.22 kB raw / 86.38 kB gzip`.

Detailed semantic/technical mapping is frozen in `temporal-create-c1-traceability.md`.

## 15. Closure rule

C1 has satisfied the **automated implementation** side of this amendment.

It is not closed until the user manually reviews the complete capability using `temporal-create-c1-manual-acceptance.md` and explicitly approves it.

Current state:

```text
IMPLEMENTATION COMPLETE
AUTOMATED PASS
MANUAL ACCEPTANCE PENDING
NOT YET FROZEN / CLOSED
```

Explicit user PASS is the only remaining closure gate.