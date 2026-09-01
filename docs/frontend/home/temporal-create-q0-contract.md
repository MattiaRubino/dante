# DANTE — Temporal Create Q0 Product / UX / Architecture Contract

**Status:** FREEZE CANDIDATE — USER REVIEW REQUIRED
**Date:** 2026-09-01
**Owner workstream:** `feature/home-timeline`
**Integration target:** `feature/home-react`
**Prerequisite:** F0 frontend temporal application foundation closed on `7034b9b0d100709785ebe96e3816aab3e7b1d1f8`
**Roadmap capability:** C1 — `+` / Create to production depth
**Scope stop:** complete pre-backend Create capability; no real API, persistence, provider synchronization, solver, AI runtime or voice runtime

---

## 1. Purpose

Q0 freezes the product, interaction and frontend architectural contract for DANTE temporal creation before implementation begins.

The target is not a prettier calendar event form.

The target is a Create capability that is:

- as fast to invoke as the best calendar/task products;
- semantically faithful to DANTE's richer Domain;
- progressive rather than form-heavy;
- keyboard-, pointer-, touch- and accessibility-safe;
- deterministic before a backend exists;
- ready to swap from the F0 local adapter to a future authoritative adapter;
- maintainable without turning Home Timeline into a monolithic feature;
- performant under repeated daily use;
- structurally compatible with H0 and the frozen Timeline interaction grammar.

Q0 is the authority for **how creation works**. Later implementation may tune visual metrics, copy and micro-animation, but it must not silently change the semantic or lifecycle rules established here.

---

## 2. Authority order

For temporal creation, use this authority order:

1. accepted Product / Domain / Logical / Physical temporal semantics;
2. H0 Whole Home Structural Contract;
3. T1 frozen Timeline interaction contract;
4. F0 temporal application foundation contract;
5. this Q0 Create contract;
6. implementation code and tests;
7. historical prototype behavior.

If a visual convenience conflicts with a semantic invariant, the semantic invariant wins.

If a child Create surface would require changing H0 macro geometry, Create must adapt instead of rewriting Home composition.

---

## 3. Product principle

DANTE must make simple creation feel simple while preserving enough structure that complex future behavior does not require a rewrite.

The permanent product rule is:

```text
simple surface
!=
simple data model
```

and:

```text
what the thing is
!=
where it is placed
!=
what occurrence exists
!=
when it is executed
!=
what actually happened
```

The Create composer may hide complexity. It must not erase it.

---

## 4. Non-collapse invariants

Creation must preserve the following distinctions:

```text
Activity != Event
source/intention != placement
all-day/date-span != midnight-to-midnight timed block
floating local != named-zone local != exact absolute instant
unscheduled != invalid/missing time
Schedule/placement != Occurrence
Occurrence != Session
Session != Actual
planned duration != actual duration
proposal/preview != accepted effect
calendar/life-area != sharing/ACL
manual input != AI/voice interpretation
pending != applied
no-op != success-with-mutation
local projection id != backend canonical DB identity
```

C1 does not need to expose every concept in the UI, but it must not encode a shortcut that makes any distinction unrecoverable later.

---

## 5. F0 prerequisite and closure assumption

Q0 consumes F0 rather than bypassing it.

The accepted frontend path is:

```text
Create UI
  ↓
Create draft
  ↓
validation / candidate placement
  ↓
F0 typed command
  ↓
TemporalWorkspacePort
  ↓
deterministic local adapter now
real authoritative adapter later
  ↓
truthful operation result
  ↓
projection / reveal / recovery
```

Create UI must not:

- mutate Timeline fixture/component state directly;
- import the in-memory adapter implementation as its application contract;
- invent REST/GraphQL DTOs;
- mirror PostgreSQL tables;
- fabricate network latency;
- use localStorage as fake backend durability;
- treat successful local projection as proof of future server persistence.

---

# 6. Competitive benchmark — adopted design pressure

Q0 uses competitors as design pressure, not as product authority.

## 6.1 Google Calendar

Useful patterns:

- direct temporal-context creation;
- predictable manual date/time editing;
- strong keyboard expectations;
- stable event/recurrence identity;
- explicit timezone semantics;
- incremental synchronization and conditional updates at integration level.

DANTE adopts:

- temporal context should prefill creation when the invocation comes from the Timeline;
- future provider adapters must preserve stable external identity and reconciliation semantics;
- date/time correctness must be stronger than cosmetic calendar behavior.

DANTE rejects:

- treating every temporal concept as one generic Event row.

Official references:

- <https://developers.google.com/workspace/calendar/api/v3/reference/events>
- <https://developers.google.com/workspace/calendar/api/guides/sync>

## 6.2 Notion Calendar

Useful patterns:

- contextual event creation;
- calm progressive event surface;
- timezone treated as a first-class user concern without dominating every interaction;
- external provider identity remains explicit.

DANTE adopts:

- timezone is normally quiet but immediately available when meaningful;
- the creation surface should stay visually calm;
- external calendar/provider identity must not be confused with DANTE context or sharing.

Official reference:

- <https://www.notion.com/help/time-zones>

## 6.3 Linear

Useful patterns from a large non-calendar application:

- extremely low-friction composer invocation;
- progressive properties;
- strong keyboard-first operation;
- draft preservation instead of accidental loss;
- immediate local product feeling;
- client-side projection and later synchronization rather than blocking every interaction on network round-trips.

DANTE adopts:

- Create must feel immediate;
- title-first interaction;
- secondary structure appears progressively;
- drafts are explicit application state, not uncontrolled component leftovers;
- future backend synchronization should preserve the current immediate frontend experience.

DANTE does not copy Linear's issue model into temporal semantics.

Official references:

- <https://linear.app/docs/creating-issues>
- <https://linear.app/developers/graphql>

## 6.4 Todoist

Useful patterns:

- one fast Quick Add entry;
- structured values become lightweight chips/actions;
- contextual calendar creation can prefill time/duration;
- floating and fixed temporal meaning are distinguishable.

DANTE adopts:

- a compact first surface;
- temporal/context values represented as editable chips or equally lightweight controls;
- future deterministic/NL parsing must fill a structured draft, never mutate accepted state directly.

Official references:

- <https://www.todoist.com/help/articles/use-task-quick-add-in-todoist-va4Lhpzz>
- <https://www.todoist.com/help/articles/set-a-fixed-time-or-floating-time-for-a-task-YUYVp27q>

## 6.5 Fantastical

Useful patterns:

- natural-language interpretation;
- visible structured preview before commit;
- template concept separate from recurrence;
- mature timezone behavior.

DANTE adopts for architecture:

```text
raw input
→ interpretation
→ structured draft
→ visible preview
→ user commit
```

Natural-language/AI parsing is **not** implemented in C1 unless a real owning capability exists.

Official reference:

- <https://flexibits.com/fantastical/help/adding-events-and-tasks>

## 6.6 Akiflow

Useful pattern:

- Task, Event and planned time are not treated as one indistinguishable thing.

DANTE adopts the principle and keeps an even stricter semantic model:

```text
Activity
→ accepted placement
→ future Occurrence
→ future Session
→ future Actual
```

Official reference:

- <https://product.akiflow.com/help/articles/7262522-keyboard-shortcuts>

## 6.7 Sunsama

Useful pattern:

- planned time and actual execution time are distinct;
- one task may lead to multiple working sessions.

DANTE adopts the distinction but does not auto-equate planned time with completion or Actual.

Official reference:

- <https://help.sunsama.com/docs/usage-guides/tasks/planned-and-actual-times/>

## 6.8 Motion

Useful pattern for later scheduling depth:

- duration, earliest start, deadline, priority and working constraints can be inputs while placement is an output.

DANTE reserves this for future scheduling-constraint/replanning phases. It does not overload the initial Create surface with solver semantics.

Official reference:

- <https://www.usemotion.com/help/time-management/auto-scheduling/reference-auto-scheduling>

## 6.9 Reclaim

Useful patterns for later planning depth:

- different temporal object classes have different scheduling behavior;
- flexibility can decrease over time;
- lock/replanning semantics are explicit.

DANTE reserves those concepts for C5/C7 rather than encoding them as one premature `fixed/flexible` boolean.

Official reference:

- <https://help.reclaim.ai/en/articles/11325700-habits-vs-tasks-vs-focus-time-when-to-use-each-in-reclaim>

---

# 7. Product target derived from the benchmark

DANTE Create should combine:

```text
Google Calendar      → predictability and calendaring correctness
Notion Calendar      → contextual/timezone calmness
Linear               → speed, drafts, progressive interaction
Todoist              → compact structured Quick Add
Fantastical           → structured preview architecture
Akiflow               → object != time-slot discipline
Sunsama               → planned != executed truth
Motion / Reclaim      → future constraints/replanning extensibility
DANTE Domain / F0     → identity, authority, reversibility, truthful state
```

No competitor is copied end-to-end.

---

# 8. Create capability topology

The canonical topology is:

```text
ENTRY CONTEXTS
│
├── Timeline/header +
├── contextual Timeline position     [supported when C1 slice enables it]
├── contextual empty-range selection [architecture-ready; implementation gated]
├── future global create
├── future keyboard command
├── future deterministic parser
├── future voice
└── future governed AI
        │
        ▼
CREATE CONTEXT
        │
        ▼
CREATE DRAFT
        │
        ├── identity/type
        ├── temporal candidate
        ├── context/calendar
        ├── notes when supported
        └── validation state
        │
        ▼
CANDIDATE PREVIEW
        │
        ▼
USER COMMIT
        │
        ▼
F0 COMMAND
        │
        ▼
TemporalWorkspacePort
        │
        ▼
operation result
        │
        ├── applied
        ├── no-op
        ├── rejected
        └── failed
        │
        ▼
projection / reveal / recovery / Undo
```

All future input channels converge on the same application contract.

AI and voice never receive a privileged path to canonical state.

---

# 9. Supported C1 semantic creation grammar

The first production Create vertical supports only object kinds that belong naturally in the Timeline creation flow.

## 9.1 Activity

User meaning:

> something I intend/want to do

Examples:

- workout;
- study English;
- edit a video;
- write a song;
- photograph a location.

An Activity may have a temporal placement, but its identity is not the placement.

Future Session/Actual semantics must remain possible without reinterpreting the Activity as a calendar event.

## 9.2 Event

User meaning:

> something that happens at a determined temporal point/block

Examples:

- appointment;
- meeting/call;
- dinner;
- concert;
- flight.

An Event normally has stronger temporal placement semantics than an Activity, but C1 must not infer future attendance, completion or Actual from the passage of time.

## 9.3 Explicitly excluded object creation

C1 `+` is not the universal DANTE object factory.

Do not put these directly into the first Create composer:

- Goal creation;
- Program creation;
- Project creation;
- World creation;
- Asset creation;
- full Routine editor;
- Session creation as a substitute for Activity;
- Actual/measurement entry;
- collaboration/share administration.

Future `Altro tipo…` or global Create may hand off to their owning verticals.

---

# 10. Temporal forms supported by the Create UX

C1 must use F0 temporal semantics instead of inventing a second date model.

## 10.1 Timed fixed placement

Typical UI:

```text
Oggi · 14:00 · 45 min
```

Application meaning:

- explicit accepted start;
- explicit duration/end;
- local/named-zone semantics preserved as required.

## 10.2 All-day / date span

Typical UI:

```text
4 settembre · Tutto il giorno
```

Application meaning:

- true date span;
- exclusive end semantics;
- no fake `00:00 → 24:00` timed event.

## 10.3 Unscheduled

A supported Activity may intentionally exist without an accepted time placement when the product flow allows it.

```text
placement = null
```

This is not a validation failure.

## 10.4 Floating local vs zoned/absolute

The UI normally hides timezone complexity when it is irrelevant.

When timezone becomes meaningful, the composer must preserve the chosen form rather than silently normalizing everything to a browser-local instant.

## 10.5 Flexible scheduling

Bounded windows, deadline-driven placement, preferred windows, chunking and solver-managed flexibility are **architecture-reserved but not part of the initial C1 grammar**.

They belong to C5/C7.

Create must not block their future addition.

---

# 11. Primary UX surface

The first surface is intentionally compact.

Conceptual structure:

```text
┌────────────────────────────────────────────┐
│ Aggiungi                                   │
│                                            │
│ [ Cosa vuoi aggiungere?                  ] │
│                                            │
│ [Attività] [Evento]                        │
│                                            │
│ [Oggi] [14:00] [30 min] [Personale]        │
│                                            │
│ + Dettagli                                 │
│                              [Aggiungi] ↵   │
└────────────────────────────────────────────┘
```

This diagram is structural, not a pixel-locked visual design.

## 11.1 Primary information order

1. title / intent;
2. Activity vs Event;
3. temporal placement controls;
4. context/calendar;
5. progressive details;
6. primary commit action.

Title receives initial focus.

## 11.2 Progressive disclosure

The primary surface must not show every future temporal capability.

Expanded details may include only fields owned by C1, such as:

- explicit end instead of duration;
- all-day;
- timezone when relevant;
- context/calendar;
- notes if product-approved for creation.

Recurrence, solver constraints, Session, Actual, complex reminders, guests, attachments, conference provider setup and collaboration do not enter merely because space exists.

---

# 12. Activity/Event interaction rule

The type selector is a user-facing semantic decision, not a cosmetic label.

Changing type may change:

- defaults;
- temporal language;
- whether duration or end-time is emphasized;
- which secondary fields are available;
- which future capabilities become applicable.

Changing type must not silently destroy already entered compatible data.

If a field becomes semantically invalid after type change, the draft must either:

- preserve it in a recoverable way while hidden; or
- explicitly explain the destructive transformation before applying it.

No silent data loss.

---

# 13. Defaulting policy

Defaults reduce friction but must never pretend user intent that cannot be justified.

## 13.1 Header `+`

Opening from the Timeline header should derive a safe default from:

- viewed/current temporal context;
- F0 Clock;
- currently selected context/calendar when unambiguous;
- product-approved default duration.

Header `+` must not use a stale prototype date once the real Clock-backed Create flow is active.

## 13.2 Contextual Timeline invocation

When C1 enables invocation from an empty temporal position:

```text
clicked day/time
→ draft date/start default
```

A selected range may additionally prefill duration.

The context is a default, not accepted truth until the user commits.

## 13.3 Default duration

A short useful default may be provided, but it must be clearly editable and must not become hidden domain truth.

Different Activity/Event defaults are allowed only if product-tested and deterministic.

---

# 14. Draft lifecycle

Draft state is an application concern, not incidental uncontrolled form state.

Canonical lifecycle:

```text
closed
  ↓ open
clean draft
  ↓ edit
dirty draft
  ├── validate
  ├── preview
  ├── reset field(s)
  ├── request close
  └── commit
        ↓
pending/settled operation
```

## 14.1 Clean close

If nothing meaningful changed:

- Escape closes immediately;
- outside-close behavior may close immediately if the chosen presentation allows it;
- focus returns to the exact opener.

## 14.2 Dirty close

A meaningful dirty draft must not disappear silently.

The UI may use a lightweight discard decision rather than a heavy nested modal.

Required choices:

- continue editing;
- discard.

Persistent cross-session Drafts are **not required in C1**. The architecture must allow them later without changing field ownership.

## 14.3 Draft preservation during internal expansion

Opening/closing `Dettagli`, changing temporal control mode or navigating between fields must never reset the draft.

---

# 15. Validation contract

Validation is deterministic and machine-readable under the UI.

UI copy is localized presentation, not the application error identity.

Example:

```text
temporal.projection.title.required
→ "Inserisci un titolo"
```

Rules:

- validate fields as early as useful without blocking typing;
- commit performs authoritative frontend validation before command execution;
- validation does not mutate accepted projection state;
- the first actionable invalid field receives focus after failed commit;
- field errors are associated through accessible description;
- an error summary appears only when it improves recovery, not by default for one obvious field;
- invalid start/end is never silently corrected unless the interaction explicitly communicates that transformation.

---

# 16. Candidate preview

Preview is part of the target architecture because it makes temporal creation inspectable before commit.

```text
draft temporal fields
→ candidate placement
→ optional Timeline preview/ghost
```

The preview is:

- visually distinguishable from accepted items;
- non-canonical;
- removable with draft close;
- not included in normal accepted-item queries as though persisted;
- never announced as success.

C1 may stage preview delivery:

- first implementation: compact textual/field preview;
- production-depth completion: Timeline spatial preview where invocation/context makes it useful.

An interactive drag of the preview is not required until its interaction grammar can be proven not to conflict with T1 card dragging and accessibility.

---

# 17. Commit and operation lifecycle

Commit path:

```text
valid draft
→ create command
→ TemporalWorkspacePort.execute()
→ truthful result
```

UI states must distinguish:

```text
idle
pending
applied
no-op
rejected
failed
```

The deterministic local adapter may settle immediately.

Do not add a fake spinner or artificial timeout merely to simulate production networking.

The component must still be architected so a future real adapter can surface pending/retry/failure without changing the form contract.

---

# 18. Idempotency and duplicate-submit protection

A Create commit owns one F0 `operationId`.

Repeated delivery of the exact same operation must not duplicate the item.

The UI must additionally guard normal human double-submit/repeated Enter without relying solely on button disable timing.

If the operation intent changes, it receives a new operation id.

Reusing the same idempotency key for a different payload is invalid and must remain rejected by F0/application semantics.

---

# 19. Result handling

## 19.1 Applied

On a successful local application:

- close or settle the composer according to accepted UX;
- reveal the new projection in Timeline when representable there;
- preserve semantic focus;
- expose Undo when the operation is reversible.

## 19.2 No-op

Create normally should not generate meaningful no-op, but the general result contract remains truthful.

No fake success feedback is emitted for a non-effect.

## 19.3 Rejected

Keep recoverable draft state when possible.

Examples:

- validation rejection;
- identity conflict;
- future expected-state conflict.

## 19.4 Failed

Future infrastructure/network failure must not erase the user's draft.

Retry must use correct idempotency semantics.

## 19.5 Adjusted/conflict reconciliation

Future authoritative adapters may return adjusted/conflicting state.

The Create UI must not assume that the initially submitted local draft is always the final server-authoritative projection.

---

# 20. Created-item reveal and Undo

A successful Create should not end with only a toast.

When the created item has a visible Timeline placement:

```text
applied
→ reveal destination day/time
→ reveal created card
→ preserve/establish meaningful focus
```

The exact scroll/reveal mechanism must reuse the accepted Timeline viewport semantics rather than invent a competing absolute scrollbar behavior.

Undo should remove/reverse the just-created local projection through F0 operation semantics, not direct component deletion.

---

# 21. Keyboard contract

Required minimum:

- activating the existing `+` opens Create;
- title receives focus;
- Tab / Shift+Tab follow logical visual order;
- Enter submits only where it does not conflict with text-field semantics;
- Escape requests close;
- dirty Escape enters discard flow rather than losing data;
- date/time controls expose predictable arrow-key behavior;
- selection controls expose native/ARIA-correct keyboard behavior;
- after close/cancel, focus returns to the exact opener;
- after applied creation/reveal, focus behavior is deterministic and tested.

A global single-key shortcut such as `C` or `N` is **not frozen in Q0** until DANTE owns a global keyboard map and collision policy.

---

# 22. Pointer and touch contract

Pointer interaction must not weaken T1 Timeline dragging.

Rules:

- Create controls never start a Timeline event drag accidentally;
- empty-slot contextual creation is isolated from scroll/drag gestures;
- outside click behavior cannot silently discard a dirty draft;
- pointer capture is cleaned up;
- touch does not depend on hover;
- mobile controls meet practical touch target requirements;
- no native HTML drag ghost is introduced by Create preview behavior.

---

# 23. Focus and accessibility contract

Create must be usable without a pointer.

Required:

- semantic dialog/sheet labeling appropriate to presentation mode;
- initial focus on title/input;
- deterministic close focus restoration;
- accessible Activity/Event selection semantics;
- labels for every temporal control;
- `aria-describedby` or equivalent association for field errors;
- non-color-only indication of type, validation and preview status;
- status messaging for operation outcome when necessary;
- no focus disappearance behind the Timeline viewport;
- reduced-motion preference respected for open/close/reveal motion;
- automated WCAG A/AA checks where tooling can detect issues;
- manual keyboard/focus verification before freeze.

Desktop and mobile may use different presentation mechanics while preserving the same semantic operation model.

---

# 24. Responsive presentation

## 24.1 Wide / desktop

Preferred pattern:

- anchored compact composer/dialog;
- does not resize H0 macro regions;
- does not push Timeline or Context Rail geometry;
- collision-aware against viewport edges;
- expanded details remain bounded and scrollable when necessary.

## 24.2 Compressed desktop/tablet

The composer may reposition or become more sheet-like rather than shrinking controls below usable density.

## 24.3 Compact/mobile

Preferred pattern:

- bottom sheet or full-height adaptive sheet;
- keyboard-safe viewport;
- safe-area aware;
- no desktop popover squeezed to 390px;
- primary action reachable without forcing hidden content behind the software keyboard.

Presentation changes; application semantics do not.

---

# 25. H0 structural invariant

Create is an overlay/capability consumer.

It must not:

- change AppShell ownership;
- alter Hero macro composition;
- renegotiate Timeline/Context Rail sibling ownership;
- resize Central Stage to make room;
- turn Context Rail into a Create container;
- introduce a fourth H0 macro responsive mode.

Any genuinely shared shell change requires separate change control.

---

# 26. Maintainability architecture

C1 must not become one giant `quick-add.tsx` that owns application semantics, parsing, layout and persistence.

Expected responsibility boundaries are conceptually:

```text
Create presentation shell
Create field components / temporal controls
Create draft model / validation
Create context/default resolver
Create candidate/preview presenter
Create operation controller
F0 public temporal application boundary
Timeline reveal integration
```

Exact filenames may differ, but responsibilities must remain separable and testable.

Rules:

- UI imports the public temporal capability boundary, not infrastructure internals;
- application/model code remains React-free where practical;
- adapter implementation is injected/composed outside leaf field components;
- no backend DTO leaks into UI form types;
- no raw DB vocabulary becomes UI state merely because it exists physically;
- design tokens and existing semantic tokens are reused;
- no unnecessary third-party state/form/date library is introduced;
- i18n remains through the shared localization architecture;
- feature-specific code stays under temporal/Create ownership instead of spreading through HomeShell.

---

# 27. Performance contract

Create is a high-frequency interaction and must feel immediate.

## 27.1 Invocation

Opening the core composer must not require:

- a network request;
- full Timeline data reload;
- provider synchronization;
- expensive recurrence expansion;
- large dynamic dependency initialization.

On a normal modern desktop, opening should remain perceptually immediate and avoid long tasks.

## 27.2 Typing

Title typing must not re-render the whole Timeline surface.

Per-keystroke work is limited to bounded draft state and lightweight validation/interpretation.

No scan over the full temporal workspace is allowed merely because a character changed.

## 27.3 Preview updates

Spatial preview work must be isolated and coalesced where geometry changes rapidly.

Do not trigger full-day layout recomputation when only preview metadata changed unless the renderer proves it necessary.

## 27.4 Memory/lifecycle

Closing Create releases:

- listeners;
- observers;
- temporary preview state;
- RAF work;
- timers;
- pointer capture;
- transient subscriptions.

No unbounded draft history or operation cache is introduced at the component layer.

## 27.5 Bundle discipline

C1 should reuse:

- `@dante/time`;
- F0 primitives;
- existing design/i18n infrastructure.

Do not add a heavy date library, form framework or state manager solely for Quick Add without demonstrated need.

Production build/bundle delta must be inspected before C1 freeze.

## 27.6 Performance verification

Before C1 closure, inspect at least:

- repeated open/close cycles;
- rapid typing;
- repeated create/Undo;
- long-scroll creation context;
- dense-day destination reveal;
- compact viewport with software-keyboard pressure where feasible;
- cleanup after cancelled/failed drafts.

---

# 28. Reliability and failure safety

Create must remain safe under:

- repeated submit;
- Escape during dirty state;
- adapter rejection;
- future transport failure;
- stale UI state;
- unmount/navigation during operation;
- viewport recycling while a candidate destination is outside current mounted days;
- reduced motion;
- rapid Activity/Event switching;
- timezone/DST boundaries;
- invalid start/end;
- all-day/timed transitions when supported.

No path may leave a ghost preview, orphan listener or misleading success state.

---

# 29. Security/privacy baseline

Even before backend integration:

- user-entered title/notes are rendered as text, never trusted HTML;
- no sensitive draft content is written to console logs;
- operation errors use machine-readable codes rather than leaking provider/backend internals;
- future analytics/telemetry must prefer event metadata over raw user content;
- external provider identifiers remain explicit data, not executable URLs or HTML.

Backend authorization/ACL enforcement remains server-owned and is not simulated in C1.

---

# 30. Future backend swap contract

The backend phase should replace the adapter, not the Create UX architecture.

Target evolution:

```text
TODAY
Create draft
→ F0 command
→ deterministic in-memory adapter
→ confirmed projection

FUTURE
Create draft
→ same application command family
→ real adapter / outbox if adopted
→ authenticated API
→ authoritative domain service
→ PostgreSQL/provider effects
→ confirmed / adjusted / conflict / failed
→ same UI recovery contract
```

Future backend work owns:

- canonical persisted identity;
- authorization/ACL;
- durable idempotency;
- server-side validation/policy;
- transaction boundaries;
- provider synchronization;
- durable audit/provenance;
- authoritative conflict detection;
- multi-device synchronization;
- retry/reconciliation persistence;
- observability and operational SLOs.

C1 must not pretend these exist locally.

---

# 31. Future AI / voice / natural-language contract

Future alternative input is allowed only through the same draft/command boundary.

```text
voice / AI / parser
→ candidate interpretation
→ structured Create draft
→ visible user-verifiable fields/preview
→ user or policy-authorized commit
→ F0/application command
```

Forbidden:

```text
AI
→ direct DB mutation
```

The user remains final authority for material Create effects unless a separately accepted automation policy explicitly grants bounded authority.

---

# 32. Future recurrence / flexibility compatibility

C1 must not paint itself into a fixed-block-only architecture.

Later phases must be able to add:

- recurrence source vs occurrence scope;
- bounded window;
- deadline;
- preferred window;
- replannable placement;
- lock semantics;
- chunking/session constraints;
- proposals;
- solver candidates.

These should extend capability-specific draft sections rather than turn the original compact composer into a permanent mega-form.

---

# 33. Testing strategy for C1

## 33.1 Unit/model

Cover at minimum:

- creation defaults;
- Activity/Event semantics;
- temporal form conversion without semantic collapse;
- dirty/clean lifecycle;
- validation;
- operation-id reuse rules;
- candidate placement;
- all-day/date-span semantics;
- DST/timezone edge cases;
- no direct accepted-state mutation.

## 33.2 Component

Cover:

- open/close;
- progressive details;
- type switching;
- field errors;
- focus restoration;
- discard flow;
- pending/rejected/failed rendering with deterministic adapter doubles where needed;
- preview cleanup.

## 33.3 E2E Chromium

Cover real user paths:

- header `+` happy path;
- keyboard-only creation;
- invalid temporal range;
- cancel/discard;
- Activity/Event distinction;
- created-card reveal;
- Undo;
- responsive desktop/compact behavior;
- repeated create cycles;
- no regression of T1 card interactions.

## 33.4 Firefox

At minimum protect the critical Create contract plus the already frozen Timeline contract.

## 33.5 Accessibility

Automated axe/WCAG checks supplement but do not replace manual keyboard/focus testing.

---

# 34. Delivery slices inside C1

C1 remains one capability but should be implemented in bounded slices, each respecting the user approval gate.

Recommended sequence:

```text
C1-A  composer shell + title + clean draft lifecycle
C1-B  Activity/Event + temporal controls
C1-C  context/calendar + all-day/timezone details
C1-D  F0 create command + truthful result states
C1-E  created-card reveal + Undo
C1-F  responsive/mobile + keyboard/a11y hardening
C1-G  contextual Timeline invocation + candidate preview
C1-H  performance/destructive regression hardening + freeze
```

The exact split may be adjusted if implementation evidence shows a smaller safer boundary.

Do not batch all slices behind one final manual review.

---

# 35. Explicit non-goals for initial C1

C1 does not implement:

- real backend/API persistence;
- external provider mutation;
- collaboration/sharing permissions;
- full recurrence editor;
- auto-scheduling solver;
- advanced reminders/notifications;
- guest management;
- attachments;
- conferencing provider integration;
- AI runtime;
- voice runtime;
- goal/program/project/world CRUD;
- Session/Actual/completion tracking;
- global Drafts workspace;
- offline sync engine;
- multi-device delta sync.

Each may consume the C1/F0 seams later.

---

# 36. Quality verdict before implementation

From a product/UX/architecture perspective, this Q0 target is considered **sufficiently mature for production-oriented implementation** if accepted by the user.

Reasons:

1. it combines mature competitor patterns without importing a competitor's weaker domain assumptions;
2. it preserves DANTE's core temporal distinctions;
3. it sits on the already-tested F0 command/query/revision/idempotency/Undo boundary;
4. it avoids backend-shaped frontend code;
5. it has an explicit future adapter swap path;
6. it treats accessibility, responsive behavior and keyboard operation as contract requirements rather than polish;
7. it protects H0 and T1 ownership;
8. it defines performance and cleanup expectations before implementation;
9. it avoids a universal mega-form;
10. it keeps AI, voice, recurrence, solver and Actual semantics in their correct future verticals.

This does **not** mean the future UI implementation is already proven excellent. That can only be established after the real composer is built, profiled, tested and manually accepted.

The conclusion is narrower and stronger:

> No additional speculative frontend foundation or benchmark round is required before beginning C1 implementation. Remaining unknowns should now be resolved by building the bounded Create slices and testing real interaction behavior.

---

# 37. Q0 exit / freeze gate

Q0 may be marked:

```text
Q0 = FROZEN / APPROVED
```

only after the user accepts this documented contract.

After Q0 freeze:

- implementation may refine presentation details;
- semantic/lifecycle/ownership changes require explicit reopening;
- C1-A begins as the next bounded capability slice;
- each C1 slice still requires automated validation and user approval before progression.
