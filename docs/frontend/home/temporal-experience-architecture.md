# DANTE — Temporal Experience Architecture

**Status:** CURRENT TEMPORAL PRODUCT / APPLICATION ARCHITECTURE — T1 IMPLEMENTED AND FROZEN  
**Date:** 2026-09-01  
**Branch:** `feature/home-react`  
**Scope:** frontend product/interaction architecture for Home Timeline, future full-page temporal workspace, contextual Detail/Resolution and shared temporal operation boundaries.  
**Not authorized by this document:** backend/API/persistence changes, new Domain semantics, provider/solver integration, final route naming or production AI provider selection.

## 1. Purpose

DANTE must support time as a foundational dimension of life without reducing life to calendar events.

A simple appointment stays simple. Rich realities such as learning sessions, workouts, meetings, recurring program steps, flexible activities, shared commitments and replanning proposals may expose deeper semantics only when relevant.

```text
rich semantics underneath
-> progressive disclosure
-> simple, legible user interaction
```

## 2. Source-of-truth alignment

Temporal frontend work consumes rather than redefines:

- Product Identity / North Star;
- Today/temporal product simulations;
- scheduling flexibility;
- execution status / Actual;
- confirmation/reminder/automatic-outcome semantics;
- calendar contexts/grouped views;
- work/meeting lifecycle;
- adaptive intelligence;
- global search/command;
- multi-actor simulations;
- Domain Atlas / Logical / Physical / Database authorities;
- Intelligence Context/Runtime boundaries;
- Governed Operation/Effect contract;
- current Home/AppShell contracts.

Permanent non-collapse:

```text
Goal != Activity/Event/Session
Schedule != Session != Actual
Occurrence != recurrence source
planned/intended != actual
Proposal != Decision != accepted effect
Confirmation != Authority
provider acknowledgement != canonical completion
AI output != canonical truth
```

Frontend vocabulary may be simpler, but application contracts must preserve recoverable semantics.

## 3. Home temporal responsibilities

The accepted Home macro-composition remains stable. Temporal work must not duplicate the same responsibility across regions.

### Ora / Prossimo

Immediate temporal orientation: what is happening now and what follows next.

Not a mini-calendar.

### In evidenza

Material consequence/attention that deserves prominence now.

Not a generic upcoming feed.

### Per te

Contextual suggestion/opportunity/discovery.

Not the same thing as a warning, confirmation or Resolution item.

### Capture

```text
USER -> DANTE
```

Low-friction input without forcing classification first.

### Resolution

```text
DANTE -> USER
```

Matters whose state materially benefits from confirmation, correction, decision or deeper inspection.

Resolution is not a notification center or generic upcoming feed.

### Timeline

Operational temporal reality: what is around the user in time and what direct temporal interactions are available now.

## 4. Avoid duplicate responsibility

The same underlying reality may appear in several surfaces only at different information altitude/responsibility.

Example: call overruns.

```text
Timeline
shows temporal fact / current execution

Ora / Prossimo
shows current orientation

In evidenza
shows material downstream consequence if any

Resolution
appears only when a decision/correction is needed

DANTE
may explain or propose within governed semantics
```

Do not duplicate the same warning card across every Home region.

## 5. Two temporal projections, one capability

DANTE should support both:

```text
HOME TIMELINE
operational lens

FULL-PAGE TEMPORAL WORKSPACE
planning/management lens
```

They are projections over one temporal application capability, not independent products.

### Home Timeline primary question

> What is happening around me, what comes next, and what can I do about it now?

Expected capability can progressively include continuous navigation, now/current context, day navigation, zoom/density, grouping/filtering, focus, quick create/inspect, direct time edit, move, bounded completion/confirmation, conflict/status indication, contextual DANTE, undo/recovery and handoff to deeper Detail/Resolution/planning.

### Full-page temporal workspace primary question

> How is my time organized, what is flexible/unresolved, what conflicts, and what should change?

It gets room for broader planning: day/week/month/agenda/continuous views, load/conflict inspection, flexible/unscheduled work, selection/multi-selection, grouping/filtering, recurrence scope, candidate replanning, timezone controls, history/reconciliation and richer planning inspectors.

Long horizons must change abstraction level. A year is not 365 miniature rich day timelines.

## 6. Development strategy

Accepted strategy:

```text
design shared temporal experience
-> define shared application semantics/operations
-> prove new verticals in Home
-> mount full-page temporal proof early enough to catch Home-specific abstractions
-> expand iteratively
```

Do not build two complete temporal systems in parallel and do not wait until every Home temporal feature exists before validating the shared capability elsewhere.

## 7. Shared capability != mega-renderer

Strong candidates for shared semantic/application ownership:

```text
temporal identities/references
projection contracts
selection primitives
semantic intents
create/edit/move operations
draft/proposal state
confirmation semantics
recurrence/occurrence scope
planned-vs-actual inputs
conflict representation
replanning proposal model
time primitives
data-source ports
operation lifecycle/error/conflict state
contextual detail contracts where justified
```

Purpose-built renderers may differ:

```text
Home day stream
full-page day
week
month
agenda
planning layout
responsive composition
```

Rejected:

```text
one MegaTimeline with dozens of variant flags
```

## 8. Progressive disclosure

Temporal UX uses depth only when needed.

```text
LEVEL 0 — TIMELINE CARD
what / when / state / one material signal

LEVEL 1 — BOUNDED INLINE/ANCHORED ACTIONS
frequent direct interaction without losing temporal position

LEVEL 2 — CONTEXTUAL DETAIL WORKSPACE
full item/session-specific context and contextual DANTE where justified

LEVEL 3 — DEEP EDIT / RESOLUTION / REPLAN
structural, broad, risky, recurring, conflicting or multi-object changes
```

A mandatory generic Peek layer between card and Detail is rejected.

## 9. Contextual Detail

The same underlying temporal reality opened from Home, full-page workspace, Search or another valid projection should resolve to the same underlying Detail capability when semantically equivalent.

Architecture:

```text
CONTEXTUAL DETAIL SHELL
├ shared chrome / interaction grammar
└ capability-specific detail modules
```

Do not create one universal optional-field object containing every possible appointment/meeting/workout/lesson/meal/program property.

## 10. Manual / DANTE / future voice convergence

Structured UI, DANTE natural language and future voice are alternative input paths into the same semantic application operations.

```text
MANUAL UI ------------------┐
                            ▼
                     SHARED APPLICATION INTENT
                            ▲
DANTE / FUTURE VOICE -------┘
```

Then as applicable:

```text
target resolution
-> expected/current-state validation
-> constraints / authority / governance
-> direct low-risk operation OR candidate/proposal
-> confirmation when required
-> governed effect
-> truthful result / pending / conflict / unknown / reconciliation
```

Natural language never bypasses permissions, constraints or consistency checks.

## 11. Temporal reality classes the UI must preserve

The product must eventually distinguish, when relevant:

### Accepted scheduled placement

Normal accepted plan.

### Date/all-day semantics

Do not fabricate arbitrary timezone-shifted instants for date-based meaning.

### Flexible/window-constrained activity

Preferred/bounded/open scheduling is not displayed as a precise accepted time until one exists.

### Unscheduled actionable work

Full planning workspace may need a tray/equivalent for work needing placement.

### Candidate / Proposal

Must remain visually/semantically distinct from accepted plan until applied.

### In-progress / Session reality

Execution may start early/late and exceed planned duration.

### Planned vs Actual

Preserve both realities rather than rewriting plan to match execution.

### Unconfirmed outcome

Time passing does not silently prove completion.

### Conflict / pressure

May be surfaced without silently moving every later item.

### Pending / unknown external result

Provider/runtime ambiguity is not false success/failure.

The default Timeline remains calm; distinctions are projected only when relevant.

## 12. Adaptive replanning

DANTE should seek the smallest valid replanning scope respecting hard constraints and user authority.

Rejected universal behavior:

```text
one item overruns by 17 minutes
-> move every later item +17 minutes
```

Possible correct behavior:

- preserve fixed commitments;
- move only semantically movable items;
- shorten only where allowed;
- fit inside accepted windows;
- propose a valid alternative;
- report infeasibility when nothing fits;
- ask for a decision when trade-offs are material.

Candidate replans remain candidates until accepted/authorized.

## 13. Recurrence / occurrence

A recurring source and an occurrence are distinct.

Editing one occurrence must not silently rewrite the recurrence source/future occurrences.

Future UI must explicitly represent scope when the action could mean:

```text
this occurrence
selected linked occurrences
future/source-level rule
```

The simplest scope compatible with the user's clear intent should remain easiest.

## 14. Actual / execution / confirmation

Planned schedule and actual execution are separate.

Example:

```text
planned  14:00–15:00
actual   13:52–15:17
```

The UI may show both when useful.

Completion/partial/skipped/etc. require truthful semantics; passage of time is not completion proof.

Resolution may collect bounded confirmation/correction, while complex cases escalate to Detail.

## 15. Contextual DANTE

Contextual DANTE may inherit the selected temporal item/session/occurrence and relevant originating context without forcing the user to restate identity.

The Context Builder/application remains authoritative for usable context, disclosure and freshness.

DANTE output is not accepted fact. Broad/material changes remain proposals/controlled operations according to governance.

## 16. Multi-actor / privacy

Shared temporal reality does not expose private actor context automatically.

```text
Visibility != Authority
shared event != all participant private overlays
UI hiding != authorization
```

Projection/context must be disclosure-safe before presentation.

## 17. Frontend application boundary

Current/future frontend structure:

```text
TEMPORAL UI
-> typed temporal application intents/read ports
-> deterministic local adapter [pre-backend]
-> real backend/generated client [later]
```

Permanent rule:

```text
frontend projection != backend DTO != Domain != persistence row
```

No direct component HTTP/SQL/provider integration.

## 18. Error / concurrency semantics

Future operation/read contracts must be able to represent truthful states such as:

```text
validation rejected
confirmation required
expected-state conflict
pending
known failure
unknown / reconciliation required
```

Late or stale client state must not silently overwrite newer accepted state.

Durable future effects are not cancelled merely because a React surface unmounts.

## 19. Accessibility

Target WCAG 2.2 AA.

Temporal interactions must preserve:

- full keyboard access;
- focus ownership/restoration;
- screen-reader semantics;
- non-color-only states;
- reduced motion;
- touch/mobile alternatives;
- non-drag alternatives for drag operations;
- appropriate target sizes.

The frozen T1 interaction contract already protects key pointer/focus/drag behavior.

## 20. Performance

Temporal UI must remain fluid under dense days, multi-day streams and broader planning horizons.

Required principles:

- deterministic/bounded layout;
- no measurement feedback loops/layout thrash;
- cleanup listeners/observers/RAF/timers;
- windowing/virtualization only when real data pressure justifies it;
- longer-range views reduce detail rather than rendering every rich day;
- route/code split heavy views where worthwhile;
- repeated open/close/drag/zoom should not leak memory/resources.

## 21. Current implementation status

```text
T0 architecture/scenario grammar  established
T1 Home Timeline hardening         USER ACCEPTED / FROZEN
T2+                                not started unless temporal workstream resumes
```

T1 observable authority:

`timeline-t1-frozen-contract.md`

Current sequencing/live authority:

- `timeline-current-checkpoint.md`
- `timeline-handoff.md`
- `temporal-frontend-roadmap.md`

## 22. Backend stop line

This architecture does not authorize real backend/API/database/provider/solver/LLM integration. Those arrive through a separately authorized backend vertical after frontend semantics and interaction contracts are proven.
