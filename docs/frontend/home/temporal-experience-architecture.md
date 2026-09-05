# DANTE — Temporal Experience Architecture

**Status:** ACTIVE WORKING DESIGN RECORD — pre-roadmap, pre-implementation  
**Date:** 2026-08-30  
**Branch:** `feature/home-react`  
**Scope:** frontend product/interaction architecture for Home temporal experience, full-page temporal workspace, contextual detail and shared temporal operation boundaries  
**Not authorized by this document:** backend/API implementation, persistence changes, Domain/Logical/Physical reopenings, final route naming, final visual design, AI provider selection

---

## 1. Purpose

This document records the current accepted working direction for the DANTE temporal experience so that later roadmap and implementation work do not lose the reasoning already established across product simulations, Domain/Logical/Physical design, database materialization, AI/runtime/effect contracts, Home frontend work and external product benchmarking.

The objective is not to design a generic calendar.

DANTE must support time as a foundational dimension of the user's life without reducing the whole product to calendar items. A simple appointment must remain simple, while richer realities such as a learning session, diet step, workout, meeting, routine occurrence, flexible activity, shared commitment or replanning proposal must be able to expose the depth that is actually relevant.

The frontend must therefore hide semantic and operational complexity rather than destroy it.

```text
rich semantics underneath
        ↓
progressive disclosure
        ↓
simple, legible user interaction
```

This document fixes the current architectural direction before the next mini-roadmap. It does not yet fix exact component names, final labels, pixels or routes.

---

## 2. Source-of-truth alignment

This design consumes rather than redefines the existing DANTE stack.

Relevant authority includes:

- Product Identity / North Star;
- Today Experience;
- Scheduling Flexibility;
- Execution Status;
- Confirmation / Reminders / Automatic Outcomes;
- Calendar Contexts and Grouped Views;
- Work Context and Meeting Lifecycle;
- Adaptive Intelligence;
- Global Search and Command;
- multi-actor and feature-discovery simulations;
- closed Domain Atlas and Logical Model;
- selected Physical Model and CP6 PostgreSQL materialization;
- AI / Context / Runtime Boundaries;
- Governed Operation / Effect Contract;
- Search / Calendar / Solver boundaries;
- current Home frontend contract and production-depth guidance;
- current Phase-1 React Timeline implementation.

Permanent non-collapse pressure relevant to the frontend includes, among other things:

```text
Goal != Activity/Event/Session
Schedule != Session != Actual
Occurrence != current start/end
Recurrence != recurring item
planned/intended != actual reality
Proposal != Decision != accepted effect
Confirmation != Authority
provider acknowledgement != canonical completion
AI output != canonical truth
```

The frontend may use simpler product vocabulary, but its application contracts must not make these distinctions impossible to recover later.

---

## 3. Macro Home structure — retained

The current Home macro-composition is considered sound and should not be redesigned merely because the temporal layer is becoming deeper.

Conceptually:

```text
GLOBAL TOPBAR

ORIENTATION / CURRENT SITUATION
- Ora / Prossimo
- In evidenza
- Per te

GLOBAL AI / CONVERSATIONAL SURFACE

HOME TIMELINE                                CONTEXT RAIL
- operational temporal reality              - Capture
- expandable                                - Resolution
- direct interaction
```

A dedicated top-level navigation destination already exists in the shell and is intended to open a **full-page temporal workspace**. Its current visible name is not treated as final design authority by this document.

### 3.1 Ora / Prossimo

Role:

> Immediate temporal orientation: what is happening now and what follows next.

It must not become a duplicate mini-calendar.

Examples:

- current call in progress;
- next meaningful commitment;
- immediate continuation of the day.

### 3.2 In evidenza

Role:

> Material attention item that deserves prominence now.

It must not be a generic upcoming feed.

Examples:

- current overrun puts a later fixed commitment at risk;
- important preparation is missing;
- a material change requires attention.

### 3.3 Per te

Role:

> Contextual suggestion, discovery or opportunity relevant to the user.

It must remain distinct from warnings, confirmations, normal upcoming items and Resolution.

### 3.4 Capture

Direction:

```text
USER -> DANTE
```

Role:

> Low-friction input without forcing classification first.

Examples:

- free text;
- observation;
- fact;
- expense;
- intention;
- quick reminder-like input;
- actual/report;
- future voice/attachment input.

Capture must not become a second AI transcript or a taxonomic form.

### 3.5 Resolution

Direction:

```text
DANTE -> USER
```

Role:

> Surface matters whose state materially benefits from user confirmation, correction, decision or deeper inspection.

Examples:

- completed / partial / skipped;
- uncertain categorization;
- conflict requiring a choice;
- requested confirmation;
- actual value to capture.

Resolution must not become a notification center, upcoming feed, `Per te`, metrics panel or generic unknown-state inbox.

Complex resolution must escalate to a deeper controlled surface rather than being compressed into the narrow rail.

---

## 4. Avoid duplicate responsibility across Home surfaces

The same underlying reality may legitimately appear in more than one Home region, but each region must expose a different product responsibility.

Example: a call is overrunning.

```text
Timeline
→ shows the temporal fact: "in progress · +17 min"

Ora / Prossimo
→ shows current orientation: "Client call · in progress"

In evidenza
→ may show the material consequence: "English is now at risk"

Resolution
→ appears only if a decision/correction is actually required

AI
→ may offer interpretation or a governed proposal
```

Rejected pattern:

```text
same warning/card duplicated in
Ora/Prossimo + In evidenza + Timeline + Resolution + AI
```

The later roadmap must explicitly preserve ownership boundaries so Home remains calm and understandable.

---

## 5. Two temporal projections, one temporal capability

DANTE should have both:

1. an embedded **Home Timeline**;
2. a dedicated **full-page Temporal Workspace**.

They are not two separate temporal products and must not develop independent semantics.

```text
                 SHARED TEMPORAL CAPABILITY
                         │
              ┌──────────┴──────────┐
              ↓                     ↓
        HOME TIMELINE        FULL-PAGE WORKSPACE
        operational lens     planning/management lens
```

### 5.1 Home Timeline

Primary question:

> What is happening around me, what comes next, and what can I do about it now?

The Home Timeline remains powerful. It is not intended to become a crippled agenda preview.

Expected Home-level capabilities include, progressively:

- continuous temporal navigation;
- now/current context;
- day navigation;
- zoom/density;
- grouping/filtering;
- event/activity focus;
- quick inspect;
- quick create;
- direct time edit;
- drag/move where semantically allowed;
- subtasks/internal session structure where useful;
- simple completion/confirmation actions where appropriate;
- conflict/status indication;
- contextual AI entry;
- undo/recovery for supported low-risk local actions;
- handoff to deeper detail, resolution or full-page planning.

Home should be optimized for **operation in time**, not broad-range planning.

### 5.2 Full-page Temporal Workspace

Primary question:

> How is my time organized, what is flexible or unresolved, what conflicts, and what should change?

The full-page workspace gets room for deeper planning and management, for example:

- day;
- week;
- month;
- agenda;
- continuous timeline;
- broader-range planning;
- load and conflict inspection;
- flexible / unscheduled work;
- selection and multi-selection;
- bulk movement where semantically valid;
- richer grouping/filtering/lenses;
- timezone presentation;
- recurrence/occurrence scope editing;
- candidate replanning preview;
- larger comparison/what-moves surfaces;
- history/reconciliation entry points;
- richer planning-oriented inspector.

Exact view set, names, default mode and navigation are still open design decisions.

The longer the horizon, the more the projection should move away from execution detail toward load, patterns, milestones, deadlines and planning consequences. A yearly view must not simply render 365 miniature day timelines.

---

## 6. Development strategy — not two full implementations in parallel

The two temporal surfaces should be **designed together**, but not independently implemented to completion at the same time.

Accepted working strategy:

```text
1. design shared temporal experience
2. define shared application/interaction architecture
3. implement first vertical in Home
4. mount an early real full-page slice
5. use it to pressure-test the shared architecture
6. continue iteratively across both surfaces
```

Reasoning:

- Home already has a mature Phase-1 temporal renderer and interaction lineage;
- it is the cheapest and safest place to prove the first production-depth vertical;
- waiting until Home is 100% complete before testing the full-page surface risks making the shared architecture accidentally Home-specific;
- building both complete in parallel risks duplicate state, divergent semantics, premature abstractions and repeated refactors.

Therefore:

> **Design together. Architecture together. Home first for implementation. Full-page early for validation.**

---

## 7. Shared capability does not mean one mega-component

The desired reuse boundary is semantic/application-level first, not DOM-level first.

### 7.1 Strong candidates for shared ownership

```text
temporal identities/references
projection contracts
selection primitives
semantic user intents
create/edit/move operation contracts
draft and proposal state
confirmation semantics
recurrence/occurrence scope semantics
planned-vs-actual presentation inputs
conflict representation
replanning proposal model
date/time primitives
frontend data-source ports
operation lifecycle/error/conflict state
shared contextual detail contracts where justified
```

### 7.2 Things that do not need to share one renderer

```text
Home day-stream DOM
full-page day renderer
week renderer
month renderer
agenda renderer
planning layout
Home shell geometry
full-page shell geometry
responsive composition
CSS/layout internals
```

Rejected direction:

```text
<MegaTimeline
  variant="home|full"
  mode="day|week|month|agenda|planning"
  compact
  expanded
  ...dozens of behavioral flags
/>
```

Preferred direction:

```text
shared temporal capability
        ↓
multiple purpose-built projections/renderers
```

Reuse must follow coherent responsibility, not line-count reduction.

---

## 8. Progressive disclosure — central UX rule

DANTE's semantic depth must not become visual overload.

Temporal interaction should use progressive disclosure:

```text
LEVEL 0 — TIMELINE CARD
what / when / state / one material signal

LEVEL 1 — QUICK INSPECT / PEEK
frequent actions and concise context without losing temporal position

LEVEL 2 — CONTEXTUAL DETAIL WORKSPACE
full item/session-specific detail and contextual AI

LEVEL 3 — DEEP EDIT / RESOLUTION / REPLAN
structural, broad, risky, recurring, conflicting or multi-object changes
```

A simple appointment may never need to go beyond Level 1.

A diet step, meeting, learning session or workout may use Level 2.

A recurring-program change, broad replan or shared consequential operation may require Level 3.

Timeline cards must remain glanceable and must not expose every linked Goal, World, Program, task, note, provenance field, recurrence rule, participant, status axis and AI control simultaneously.

---

## 9. Contextual Detail Workspace — shared entry surface

A temporal item opened from Home, full-page temporal workspace, search or another valid projection should resolve to the same underlying detail capability when it represents the same canonical/product reality.

Conceptually:

```text
HOME TIMELINE ───────┐
                     │
FULL TEMPORAL PAGE ──┼──→ CONTEXTUAL DETAIL
                     │
SEARCH / OTHER ──────┘
```

The Detail surface is not owned only by the Home Timeline.

### 9.1 Do not build a universal optional-field monster

The Domain rejects a universal semantic `Thing`; the frontend should not recreate one accidentally as a universal detail form containing dozens of optional fields.

Preferred architecture:

```text
CONTEXTUAL DETAIL SHELL
│
├── shared chrome / common interaction grammar
│
└── feature-specific or capability-specific detail modules
```

Possible examples:

- simple appointment detail;
- meeting detail;
- learning/session detail;
- workout detail;
- meal/diet-program detail;
- ordinary activity detail;
- program-generated step detail.

Common shell does not imply identical internal semantics.

### 9.2 Contextual AI

Rich detail may host a contextual DANTE conversation/command surface.

Example:

```text
English Lesson
> today I only want to do speaking
```

The context may include the selected occurrence/session, relevant originating program/routine, constraints, materials, previous decisions and other authorized information appropriate to the requested action.

The user should not need to restate the entire object identity in natural language.

---

## 10. Manual, AI, command and future voice interaction must converge

DANTE will support at least two visible interaction modes:

- structured/manual UI;
- natural-language AI interaction.

Future mobile voice is expected to become another input mode.

These must not become separate business-logic paths.

Conceptual direction:

```text
MANUAL
+ / click / drag / edit / keyboard
             │
             │
             ▼
     SHARED APPLICATION INTENT
             ▲
             │
AI GLOBAL / AI CONTEXTUAL / FUTURE VOICE
```

Then, as materially applicable:

```text
target resolution
↓
current/expected-state validation
↓
constraints / authority / governance / autonomy policy
↓
direct low-risk operation
OR
candidate / proposal / preview
↓
confirmation when required
↓
governed effect
↓
truthful result / pending / conflict / unknown / reconciliation
```

Natural language is not allowed to bypass deterministic validation, permissions or state consistency.

An AI interpretation is not automatically an accepted canonical effect.

---

## 11. Temporal realities the UI must eventually distinguish

The temporal experience must be able to project materially different realities without flattening all of them into ordinary fixed calendar events.

Important categories include:

### Accepted scheduled placement

A normal accepted temporal placement.

### All-day/date semantics

Date-based meaning must not be fabricated as an arbitrary timezone-shifted instant.

### Flexible or window-constrained activity

Examples:

- must happen inside a bounded window;
- preferred window;
- deadline-constrained;
- open scheduling.

A flexible item should not be visually represented as though a precise time had already been accepted when it has not.

### Unscheduled but actionable work

The full-page workspace is expected to need a planning tray or equivalent surface for items that require placement but do not yet have one.

### Candidate / proposal

A DANTE or user-generated replan candidate must remain visually and semantically distinct from the accepted plan until applied.

### In-progress / Session reality

Execution may start before or after Schedule and may exceed expected duration.

### Planned vs Actual

If an item was scheduled for 14:00–15:00 but actually happened 13:52–15:17, DANTE should preserve both realities rather than rewriting the original plan to match execution.

### Unconfirmed outcome

Passage of time must not silently establish completion.

### Conflict / pressure

A conflict or overrun may be surfaced without silently moving everything that follows.

### Pending / unknown external result

Provider/runtime ambiguity must not be rendered as false success or false failure.

The default Timeline must still remain calm. These distinctions are projected only where relevant rather than displayed simultaneously on every card.

---

## 12. Adaptive replanning behavior

DANTE's temporal value is not simply automatic rescheduling.

When reality changes, DANTE should seek the smallest valid replanning scope that respects actual constraints and user authority.

Example:

```text
14:00–15:00  Client call
15:00–16:00  English
16:30        fixed appointment
```

The call runs until 15:17.

Rejected universal behavior:

```text
move every later item by +17 minutes
```

Possible DANTE behavior:

- preserve the fixed commitment;
- identify which later item is movable;
- shorten only if its semantics allow shortening;
- move inside an accepted window;
- propose a later valid placement;
- report that not everything fits when no valid solution exists;
- ask for a decision when a material trade-off is required.

Hard constraints must not be silently violated to produce a visually clean calendar.

Candidate replans must remain candidates until accepted or authorized by the applicable autonomy policy.

---

## 13. Recurrence and occurrence behavior

Editing a recurring item must eventually distinguish scope explicitly where material.

Possible product scopes include, depending on the actual semantic family:

```text
this occurrence only
selected linked occurrences
future occurrences
whole routine/program/source
```

Occurrence identity must not be defined by current start/end time. Moving one expected occurrence must not silently destroy its identity and create an unrelated replacement merely for UI convenience.

The exact UI wording and supported scope combinations remain later design work.

---

## 14. Confirmation and Resolution relationship

Confirmation is not a universal `completed` boolean.

The temporal experience must support configurable confirmation behavior such as:

- immediate;
- later in the day;
- daily review;
- weekly review;
- remain silently unconfirmed;
- explicit automatic outcome only under accepted policy;
- provisional inference from trusted integration where applicable.

The Timeline may show a lightweight state marker, but should not be crowded with every possible outcome action.

Resolution remains the Home location for concise user decisions when appropriate, with escalation to Detail/Deep Resolution for richer cases.

---

## 15. Rich internal session structure

Some temporal items contain meaningful internal execution structure.

Example learning session:

```text
English Lesson
3 / 5 activities

Vocabulary       complete
Grammar          complete
Listening        complete
Speaking         pending
Review           pending
```

The card may show a compact progress cue.

An inline expansion may show a bounded subset when useful.

The contextual Detail can expose full structure, materials, linked program/goal context, actual results and contextual AI.

The Timeline must not duplicate the entire Program/Goal/World hierarchy. It projects how that wider reality manifests in time.

---

## 16. Relationship with Worlds, Goals, Programs and other DANTE surfaces

Time is a foundational dimension, not the owner of every persistent reality.

Conceptually:

```text
World / area / persistent context
        ↓
Goal / desired outcome
        ↓
Plan / Program / Routine
        ↓
Activity / Event / expected step
        ↓
Occurrence / Schedule
        ↓
Session / Actual / Outcome
```

The Timeline typically projects the temporally relevant layer.

The Detail may expose links upward.

Worlds/Goals/Programs remain the better surfaces for longitudinal structure and management.

No temporal view should attempt to become an ontology browser.

---

## 17. Full-page planning pressure

The future full-page workspace should be designed to handle use cases that are inappropriate for the embedded Home Timeline.

Examples:

- repair an overloaded week;
- compare several days;
- place unscheduled work;
- inspect fixed vs flexible commitments;
- perform bounded multi-selection/bulk move;
- manage recurrence scope;
- review broad conflict consequences;
- compare a candidate replan against accepted plan;
- inspect timezone-heavy travel periods;
- understand load and patterns over longer horizons.

The Home Timeline should hand off gracefully to this surface rather than trying to absorb every planning workflow.

---

## 18. Product scenario oracle

Existing simulations should become executable product acceptance pressure rather than remain passive documentation.

Initial archetypes for temporal design and later testing should include at least:

1. simple fixed appointment;
2. meal/diet step with structured detail and substitution request;
3. English lesson with internal activities/materials;
4. workout with planned vs actual execution;
5. meeting/call that starts early or overruns;
6. flexible activity that needs placement;
7. recurring occurrence changed only once;
8. day/week that becomes infeasible and requires replanning;
9. unconfirmed outcome routed to Resolution;
10. global AI command affecting one or more temporal objects;
11. contextual AI command inside an opened item;
12. future voice command equivalent to a supported manual/AI operation;
13. stale/concurrent edit conflict;
14. provider/runtime result that remains pending or unknown;
15. multi-actor change that requires proposal/acceptance rather than silent overwrite.

For each scenario, future work should derive:

```text
product expectation
↓
interaction expectation
↓
application contract
↓
component test
↓
E2E
↓
future backend acceptance pressure
```

---

## 19. Current Phase-1 Timeline — preserve what is already strong

The current React Timeline is not disposable prototype code to replace wholesale.

Existing strengths include:

- continuous multi-day stream;
- contextual initial positioning;
- nonlinear temporal density;
- overlap lanes;
- semantic-anchor zoom;
- group filtering and expanded grouped view;
- calendar/date navigation;
- return to now;
- focus and subtasks;
- anchored time edit;
- drag/move including cross-day behavior;
- undo;
- responsive expansion behavior;
- `PlainDate` / `@dante/time` usage;
- bounded viewport/window extension;
- requestAnimationFrame-based geometry/scroll work;
- cleanup of timers/listeners/frames;
- explicit prototype clock rather than pretending the fixture is production real time.

Phase 2 should build production semantic/application behavior above this foundation rather than casually reopening frozen visual work or replacing Temporal semantics with ordinary `Date` shortcuts.

The current `TimelineEvent` remains a frontend projection model, not the canonical DANTE temporal/domain model.

---

## 20. Quality and commercial bar

The temporal experience must be evaluated as a core product capability of a large modern application.

Required design qualities include:

- low-friction simple cases;
- progressive disclosure for complex cases;
- strong keyboard navigation on desktop;
- equivalent accessible non-drag actions;
- touch/mobile-specific interaction rather than desktop shrinkage;
- focus restoration and modal/panel correctness;
- WCAG 2.2 AA pressure;
- reduced-motion support;
- truthful pending/conflict/error/unknown states;
- deterministic behavior under dense timelines;
- strong performance under long lists and broad ranges;
- virtualization/windowing where justified by measured pressure;
- stable identity and no index/time-position identity shortcuts;
- no direct HTTP from components;
- explicit future frontend data-source ports;
- runtime validation at future untrusted network boundaries;
- backend-authoritative authorization later;
- no fake durable persistence or fake AI success in frontend-only phases.

Visual benchmarking can borrow proven interaction ideas from Google Calendar, Notion Calendar, Linear, Todoist, Sunsama, Motion, Reclaim, Akiflow, Fantastical and similar products, but provider schemas and interaction conventions are evidence, not DANTE semantic authority.

---

## 21. Explicit non-decisions

This document deliberately does **not** decide:

- final name of the full-page temporal destination;
- final route/path;
- exact full-page navigation hierarchy;
- exact day/week/month/agenda visual composition;
- exact iconography/colors/micro-animation;
- exact responsive breakpoints;
- whether Peek is right-side, anchored, overlay or another grammar at each breakpoint;
- exact Detail panel width/layout;
- exact AI chat layout;
- exact mobile voice affordance;
- final create object taxonomy;
- backend routes/DTOs;
- persistence/API command shapes;
- AI provider/model;
- solver invocation mechanics;
- server-state library;
- generic state-machine library;
- overlay framework;
- a universal temporal repository abstraction.

These remain later decisions and must not be silently invented during implementation.

---

## 22. Rejected shortcuts

Do not proceed with any of the following as default architecture:

```text
Home Timeline and full-page calendar with separate business logic

one universal Event CRUD model for all DANTE temporal reality

one giant Timeline component with dozens of mode flags

one giant ItemDetail object/form with every field optional

AI directly mutating frontend/canonical state

drag implementation bypassing the same validation used by edit/AI

passage of scheduled end time => completed

provider timeout => failed

last-write-wins for material stale edits

recurring occurrence identity = current start timestamp

candidate replan rendered as already accepted schedule

all conflicts automatically solved by shifting later items

Home card overloaded with every linked semantic dimension

Resolution used as notification center

full-page workspace implemented only after Home is fully complete

full Home and full-page workspace independently implemented in parallel
```

---

## 23. Working decision summary

The current agreed direction is:

1. **Retain the Home macro-structure.**
2. **Retain Ora/Prossimo, In evidenza and Per te as distinct responsibilities.**
3. **Retain Capture and Resolution as the two directions USER→DANTE and DANTE→USER.**
4. **Keep the embedded Home Timeline as a powerful operational temporal surface.**
5. **Use the existing top-level temporal destination as a real full-page planning/management workspace; ignore the current label until naming is deliberately decided.**
6. **Treat Home Timeline and full-page workspace as two projections of one shared temporal capability, not separate products.**
7. **Design both surfaces together, but do not implement both completely in parallel.**
8. **Implement the first production-depth vertical in Home, then introduce a real full-page slice early to pressure-test shared architecture.**
9. **Share semantic/application contracts more strongly than DOM/layout.**
10. **Build contextual Detail as a shared cross-entry capability with a common shell and specific content, not a universal optional-field monster.**
11. **Use progressive disclosure: Card → Quick Inspect → Detail → Deep Edit/Resolution/Replan.**
12. **Manual UI, AI global, AI contextual and future voice must converge on the same validated operation semantics.**
13. **Preserve Schedule, Session, Actual, Occurrence, Recurrence, Proposal, Confirmation and conflict distinctions underneath simple UX.**
14. **Do not let Timeline duplicate Worlds/Goals/Programs; show their temporal manifestation and link upward when useful.**
15. **Use real DANTE simulations as design and test oracles.**
16. **Preserve the strong Phase-1 Timeline engine and reopen visuals only for concrete semantic, accessibility, performance or product needs.**

---

## 24. Next session

The next step is intentionally **not code yet**.

Create a compact implementation roadmap that turns this architecture into an ordered sequence of frontend design and engineering slices, including:

- what must be specified before touching code;
- which shared contracts come first;
- which Home slice should be the first production-depth implementation;
- how early the full-page slice should be introduced;
- which scenario oracles gate each step;
- where to stop before backend implementation.

That roadmap should remain small enough to execute, while preserving the architecture fixed in this record.
