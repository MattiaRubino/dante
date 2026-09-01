# DANTE — Temporal Frontend Roadmap

**Status:** CURRENT WORKING ROADMAP — T1 FROZEN / T2 NEXT WHEN TEMPORAL WORKSTREAM RESUMES  
**Date:** 2026-09-01  
**Branch:** `feature/home-react`  
**Consumes:** `temporal-experience-architecture.md`, `timeline-t1-frozen-contract.md`, current Home/product contracts, closed Domain/Logical/Physical/Database semantics and frontend production standards.  
**Scope stop:** production-grade frontend temporal capability before real backend/API/provider/solver integration.

This roadmap is planning authority for the temporal workstream. It does **not** authorize temporal implementation while another workstream is active. Current active frontend product work is World Focus.

## 1. Delivery model

Temporal work follows production-depth mini-verticals:

```text
one bounded capability
-> semantics/scenario pressure
-> implementation to production depth
-> automated gates
-> real-browser/manual review
-> user visual/functional validation
-> fixes
-> explicit acceptance
-> freeze
-> next capability
```

A slice is not complete because it renders or because CI is green.

## 2. Permanent boundaries

### Product surfaces

One temporal capability serves multiple purpose-built projections:

```text
Home Timeline
Home expanded Timeline
Dedicated full-page temporal workspace
Shared contextual item Detail
Resolution handoff
Global/contextual DANTE and future voice entry
```

They may use different renderers/layouts but must not create independent temporal semantics/stores.

### Semantic non-collapse

```text
Goal != Activity/Event/Session
Schedule != Session != Actual
Occurrence != recurrence source
planned/intended != actual
Proposal != Decision != accepted effect
provider acknowledgement != canonical completion
```

### Backend stop line

No component direct HTTP, invented endpoint contract, ORM/DB row leakage or fake durable/provider success during the frontend phase.

## 3. T0 — temporal contract / scenario oracle — ESTABLISHED

The temporal architecture and canonical scenarios established the interaction/product grammar used to harden T1.

Representative pressure includes:

- simple appointment;
- structured learning session;
- diet/workout/session realities;
- early/overrunning call;
- flexible/movable activity;
- recurrence occurrence scope;
- unresolved confirmation;
- conflict/replan;
- equivalent manual/contextual-DANTE requests.

Generic `Peek` between card and Detail was rejected as a mandatory layer.

## 4. T1 — Timeline parity / interaction hardening — USER ACCEPTED / FROZEN

T1 is closed for observable behavior.

The authoritative change-control contract is:

`docs/frontend/home/timeline-t1-frozen-contract.md`

Frozen areas include:

- viewed-date/now behavior already accepted;
- focus/deselect-first grammar;
- title/time/subitem explicit action regions;
- first-gesture custom drag;
- no native drag ghost/text selection;
- same-day/cross-day movement behavior covered by accepted tests;
- anchored time edit separate from drag;
- undo/recovery on supported operations;
- deterministic compact overlap lanes;
- expanded group/header/event alignment and horizontal sync;
- Chromium + Firefox critical pointer/focus/drag coverage.

Do not reopen T1 for cleanup/modernization. Any deliberate observable change requires explicit user approval before production writes.

## 5. T2 — Temporal application core / truthful local adapter — NEXT ONLY WHEN RESUMED

Goal:

Establish shared application boundaries for new Phase-2 interactions without rewriting frozen T1 behavior.

Likely scope, only when explicitly resumed:

- temporal projection identity;
- query/read ports;
- typed semantic intents;
- operation request/result model;
- deterministic local adapter;
- draft vs accepted state;
- expected-state/conflict representation;
- undo/recovery contract;
- clock abstraction where justified;
- projection model separate from Domain/backend DTO/persistence.

The adapter should be able to simulate truthful outcomes such as applied, validation rejection, confirmation required, expected-state conflict, pending, known failure and reconciliation-required/unknown where future external effects warrant it.

Do not add generic repository/UoW/state-machine libraries merely for architectural appearance.

## 6. T3 — Create / edit / move vertical

Goal:

Move new creation/edit/move workflows onto the shared application intent boundary while preserving simple interaction.

Candidate behavior:

- Timeline quick create;
- coordinate/viewed-date create where approved;
- quick vs expanded create;
- edit time;
- drag/move/cross-day move;
- cancel/validation/undo;
- recurrence scope only when recurrence is actually involved.

Manual UI and future AI/voice should converge on the same semantic application intents.

## 7. T4 — Structured Detail profiles + contextual DANTE

Goal:

Represent richer DANTE temporal realities without overloading Timeline cards.

Potential profiles:

- simple appointment;
- activity/task-like item;
- structured learning session;
- meal/diet step;
- workout/session;
- meeting/work item where current semantics support it.

Use a shared Detail shell plus capability-specific modules, not a universal optional-field monster.

Pre-backend contextual DANTE must produce the same typed candidate/operation contracts expected later; model-like output is never canonical truth.

## 8. T5 — Execution truth / Actual / Resolution

Goal:

Represent what actually happened separately from what was planned.

Candidate states/workflows include in-progress, ended-unconfirmed, completed, partial, skipped, postponed/replaced/cancelled where semantically valid, and planned-vs-actual timing/value.

Resolution should handle bounded confirmation/correction and escalate complex cases rather than becoming a generic notification center.

## 9. T6 — Flexible scheduling / recurrence / conflict / replan

Goal:

Represent fixed, movable, window-constrained, unscheduled, recurring and conflicting temporal realities without flattening them into ordinary events.

Candidate replan remains visually/semantically distinct from accepted plan until applied.

Prefer the smallest valid affected scope; hard constraints must never be silently violated just to make a clean calendar.

## 10. T7 — Full-page temporal workspace architecture proof

Goal:

Validate that shared temporal application semantics are not accidentally Home-specific.

First proof may include:

- full day;
- useful week/planning projection;
- shared selection/Detail;
- shared create/edit/move operations;
- unscheduled/flexible planning area if ready.

Do not stretch the Home Timeline to 100vw and call it a new workspace.

## 11. T8 — Full temporal workspace depth

Only after T7 succeeds, expand with justified views/capabilities such as richer Day, Week, Month, Agenda, grouped/focus views, multi-select, timezone controls, flexible tray, broader planning horizon, conflict/load inspection and candidate-plan mode.

Long horizons must change abstraction level; a year is not 365 miniature rich day timelines.

## 12. T9 — Global DANTE / future voice convergence

Demonstrate that natural-language and future voice are alternative entry paths to the same temporal application operations.

Representative requests may include create/move/replace-occurrence/replan/confirmation queries.

Broad/material changes require preview/confirmation according to product/governance policy; no production AI provider is required to close the frontend phase.

## 13. T10 — Production hardening / pre-backend freeze

Required before backend integration:

### Architecture

- no direct component HTTP;
- no backend DTO/DB leakage;
- no universal Thing/Event collapse;
- no duplicate Home/full-page store;
- architecture/generated checks green.

### Behavior

- scenario oracle coverage;
- create/edit/move/undo;
- Detail profiles;
- Actual/confirmation;
- recurrence scope;
- flexible/unscheduled;
- conflict/proposal/replan;
- manual/DANTE command equivalence for covered flows.

### Accessibility

WCAG 2.2 AA target, keyboard/focus, screen-reader semantics, reduced motion, non-color-only state, touch/mobile alternatives.

### Performance

Dense-day/multi-day/week pressure, fluid scroll/zoom/drag, bounded rendering/windowing when needed, no layout thrash, cleanup/memory checks, bundle review.

### Tests

Unit/model/component/integration/E2E/a11y/responsive/visual/performance as applicable.

## 14. Final backend vertical

After frontend freeze, real application/API/provider/solver integration should replace local adapters without changing the accepted temporal product semantics or forcing a renderer rewrite.

## 15. Resume rule

When temporal work is explicitly resumed:

1. read `timeline-current-checkpoint.md`;
2. read `timeline-handoff.md`;
3. re-read the frozen T1 contract;
4. re-read the exact Domain/Logical/Physical/DB/Intelligence authorities touched by T2;
5. define one bounded T2 slice;
6. get the normal implementation gate before production writes.
