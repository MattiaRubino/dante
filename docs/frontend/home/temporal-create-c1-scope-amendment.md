# DANTE — Temporal Create C1 Scope Amendment

**Status:** ACTIVE AUTHORITY — IMPLEMENTATION FULL GREEN / MANUAL ACCEPTANCE PENDING  
**Original amendment date:** 2026-09-01  
**Final implementation reconciliation:** 2026-09-02  
**Owner workstream:** `feature/home-timeline`  
**Integration target:** `feature/home-react`  
**Final implementation candidate:** `f092a3db2fbac28421b73e0629f7b4b83a1b0aec`  
**Frontend CI:** `33631013598` / #621 — FULL PASS  
**Supersedes where conflicting:** `temporal-create-q0-contract.md`, `temporal-create-q0-approval.md`, and the original bounded C1 section of `temporal-frontend-roadmap.md`  
**Scope stop:** maximum useful pre-backend **manual** Create system; no real API, PostgreSQL application persistence, provider execution, authoritative solver, recurrence evaluator, AI/NL runtime or input, voice runtime or input, or server-side product Auth/ACL implementation

## 1. Why this amendment exists

The original Q0/C1 contract intentionally bounded the first Create vertical to a compact Activity/Event grammar.

The user later explicitly required the Timeline `+` to reach the **maximum useful frontend/application depth before backend integration**, rather than stop at Quick Add.

A later clarification further froze the input model: this `+` is **manual authoring only**. DANTE/AI, natural-language interpretation and voice belong to separate future product surfaces and must not be mixed into this capability merely because they may eventually create or modify temporal objects.

This amendment therefore expands C1 vertically while retaining Q0/F0 rules for semantics, architecture, validation, accessibility, performance, operation truth and backend separation.

C1 closes only when its manual UI/application design can connect to future backend adapters without structural redesign.

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
Context/group membership != presentation override
visibility != ACL authority
manual Create != DANTE/AI/NL/voice input
frontend projection id != canonical backend identity
ViewModel != application model != DTO != DB row
```

No richer UI may collapse these distinctions for convenience.

## 3. Product topology — one manual capability, progressive surfaces

```text
ENTRY
  ├── Timeline/header +
  ├── contextual Timeline double-click
  └── contextual Timeline Shift-drag/range
          │
          ▼
 deterministic manual prefill
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

Quick, Expanded and Full are views of one manual application capability, never three independent Create engines.

## 4. Manual-only input boundary / relationship with DANTE

C1 is intentionally **not** a generic input framework.

The Timeline `+` does not provide:

- chat;
- natural-language parsing;
- AI command interpretation;
- voice capture/interpretation;
- prompt provenance;
- model confidence/alternatives;
- AI proposal/approval orchestration.

`TemporalCreateFieldSeed` is a structured prefill helper for the manual flow. It lets deterministic Timeline interactions pass facts they already know — such as date, time, duration/range or Context — without scripting UI controls.

It does not establish this architecture:

```text
DANTE/NL/voice → C1 seed → manual Create form
```

A future DANTE/AI vertical remains a separate surface with its own interpretation, proposal, confidence, governance and confirmation contracts. Where semantically appropriate it may later reuse shared downstream application/domain/backend commands. That future reuse does not make the C1 UI/session/seed an AI abstraction today.

## 5. Quick Create role

Quick must remain intentionally fast and calm.

Its common path is limited to high-frequency manual creation data such as:

- title;
- Activity/Event;
- primary temporal placement;
- Context;
- clear expansion path;
- truthful commit/cancel behavior.

Deep recurrence, planning, execution and integration details belong to progressive disclosure, not the resting Quick surface.

## 6. Activity creation scope

Activity may progressively author:

### Identity / organization

- title;
- Context/life area;
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
- earliest start and deadline boundary where applicable;
- floating/named-zone semantics where applicable.

Flexible scheduling intent may exist before a solver. C1 retains structured intent and **does not fake a concrete accepted Schedule**.

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

Current CP6/Alembic M4 materializes recurrence families only for Routine and Event. Therefore C1 preserves:

```text
persistent repeated Activity intent
→ Routine owning vertical
→ Routine Recurrence
→ backend Occurrence generation later
```

No `Activity.repeat`, no Activity recurrence editor and no Activity recurrence capability may be introduced.

### Confirmation / reminder intent

C1 may author confirmation/outcome/review/reminder policy where product-defined, but must not fabricate notification delivery or Actual outcome.

## 7. Event creation scope

Event has a distinct time-centred grammar and may author:

- title;
- start/end/duration;
- all-day multi-day date span;
- floating-local / named-zone semantics;
- IANA timezone;
- Context;
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

## 8. Event recurrence scope

C1 Event recurrence preserves all four CP6 M4 families:

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

## 9. Context and per-item appearance

C1 may offer a presentation override without redefining Context/group semantics.

Authoritative distinction:

```text
Context/groupId
→ organization, grouping, filtering
→ source of inherited default visual tone

appearanceTone override
→ presentation only
→ no Context/groupId mutation
→ no filter-membership mutation
```

The manual appearance picker uses stable color vocabulary independent from Context names:

- purple / viola;
- cyan / ciano;
- green / verde;
- amber / ambra;
- pink / rosa;
- red / rosso.

This prevents a false mapping such as `Rosso == Urgenze` or `Viola == Focus`.

## 10. Other DANTE object types / handoff

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

## 11. UI / interaction quality target

The complete C1 system must remain a mature application surface rather than an administrative form.

Required:

- title dominance and fast common path;
- semantic grouping;
- Activity/Event-specific sections;
- progressive disclosure;
- contextual manual Timeline prefill;
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
- mobile containment/no horizontal overflow;
- no AI/NL/voice affordance in Create;
- Context/appearance distinction understandable without exposing DB complexity.

## 12. Application architecture requirements

C1's accepted application layer includes only abstractions demonstrated by real needs:

- structured manual Create draft/session;
- deterministic manual prefill;
- Activity scheduling/execution intent;
- Event recurrence/event intent;
- confirmation/reminder intent;
- per-item appearance intent distinct from Context;
- candidate Timeline projection;
- deterministic validation;
- F0 prepared command/result path;
- rich-intent metadata/idempotency;
- typed external-owner handoff;
- immutable application-boundary prepared snapshot;
- local deterministic runtime;
- Undo/reveal integration.

Do not mirror PostgreSQL rows or invent REST DTOs.

Do not generalize the manual Create session into a speculative AI/agent framework.

## 13. Relationship with later temporal phases

C1 owns **initial manual creation-time authoring**.

C5 still owns deeper editing of existing recurrence/flexibility/source scope, including this occurrence vs future/source behavior.

C6 owns runtime Session/Actual/execution/correction surfaces.

C7 owns conflict/proposal/affected-item/replanning experience and future solver integration.

A future AI/DANTE workstream may integrate with these downstream semantic operations through its own surface/contracts; it is outside C1.

C2 remains the immediate next capability after C1 freeze: Card → structured Detail.

## 14. Backend stop line

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
- AI/NL runtime and input;
- voice runtime and input.

Connecting these should extend/replace adapters and external seams rather than force a manual Create UI/application rewrite.

## 15. Final implementation reconciliation

Implementation candidate:

`f092a3db2fbac28421b73e0629f7b4b83a1b0aec`

CI #621 / run `33631013598` proves:

- Quality PASS;
- Mobile PASS;
- full Chromium Web E2E PASS;
- frozen Firefox Timeline interaction PASS;
- final gate PASS.

Current measurable evidence:

- architecture **214 modules / 522 dependencies / zero violations**;
- web unit **34 files / 183 tests**;
- Home route **268.40 kB raw / 90.13 kB gzip**.

Detailed semantic/technical mapping is maintained in `temporal-create-c1-traceability.md`.

## 16. Closure rule

C1 has satisfied the **automated implementation** side of this amendment.

It is not closed until:

1. the final documentation descendant is itself CI-green;
2. the user manually reviews the complete capability using `temporal-create-c1-manual-acceptance.md`;
3. the user explicitly approves it.

Current state:

```text
IMPLEMENTATION COMPLETE
AUTOMATED PASS
DOCUMENTATION RECONCILIATION IN PROGRESS
MANUAL ACCEPTANCE PENDING
NOT YET FROZEN / CLOSED
```

Explicit user PASS is the final closure gate.
