# DANTE — Home / Frontend Current Checkpoint

**Status:** CURRENT LIVE ENTRY POINT  
**Date:** 2026-09-01  
**Working branch:** `feature/home-react`  
**Worktree:** `/home/mattia/projects/dante-frontend`  
**Current branch baseline before this documentation cleanup:** `aa495e38304ae26a4635e9c843cabbe1cb954f6e`

This file is the **live branch checkpoint** for a new chat/agent. Do not reconstruct current state from older phase labels or historical roadmap documents.

## 1. Workstreams currently present on this branch

The branch contains three distinct frontend concerns that must not be collapsed:

```text
HOME / APP SHELL
shared application shell and Home composition

TEMPORAL / TIMELINE
Home Timeline + shared temporal capability

WORLD FOCUS
one focused World as its own route/application surface
```

Home, Timeline and World Focus share product/domain authorities but are not the same UI surface and must not borrow component semantics from one another merely because they all involve DANTE.

## 2. Global AppShell / Home baseline

The shared AppShell/Topbar is already productionized and remains outside World Focus ownership.

Accepted durable rules include:

- persistent shared AppShell and Global Topbar;
- real application routing;
- Home / Mondi / Oggi navigation;
- inline Topbar Search rather than a Home-owned modal;
- centralized design-token/theme ownership;
- no fake backend writes;
- Access/Auth remains a separate workstream and must not be casually modified here.

For durable Home product semantics read:

- `docs/frontend/home/contract.md`
- `docs/frontend/home/home-structural-contract.md`
- `docs/frontend/app-shell/p1-global-app-shell.md`

## 3. Timeline current state

Timeline Phase T1 is **user-accepted and frozen** for observable interaction/geometry behavior.

The current temporal architecture and future pre-backend roadmap remain active, but no Timeline work is currently authorized merely because the roadmap contains T2+.

Read in this order when resuming Timeline:

1. `docs/frontend/home/timeline-current-checkpoint.md`
2. `docs/frontend/home/timeline-handoff.md`
3. `docs/frontend/home/timeline-t1-frozen-contract.md`
4. `docs/frontend/home/temporal-experience-architecture.md`
5. `docs/frontend/home/temporal-frontend-roadmap.md`

Never weaken Timeline regression tests to accommodate unrelated World Focus work.

## 4. World Focus current state

World Focus is the **active product workstream**.

Durable current state:

```text
WF0 structural shell / route          FROZEN
WF-G3 geometry                        FROZEN
B0 production foundation              CLOSED
WR0 product reverse engineering       CLOSED
WR1 DANTE <-> user stress             COMPLETE / gaps found
WR2 gap closure                       CLOSED / no structural gaps
B1 Orientation                        CLOSED for sequencing
B2 Continuity / Resume                IMPLEMENTED / AUTOMATED PASS
B2 integrated user acceptance         DEFERRED
```

Why B2 acceptance is deferred:

The latest user review exposed that the next architectural/product gate must establish **DANTE's real spatial/presentation presence inside World Focus before more World content verticals are composed**. Backend/API/provider/real-LLM work remains deferred, but the frontend must know DANTE's actual footprint and interaction states so later dynamic composition is designed against the real available workspace.

Important correction:

```text
Home AI surface != World contextual DANTE surface
```

Do not copy Home AI geometry/components into World Focus by analogy. The World surface requires its own bounded reverse engineering and user-approved interaction architecture.

Read in this order when resuming World Focus:

1. `docs/frontend/home/world-focus-current-checkpoint.md`
2. `docs/frontend/home/world-focus-handoff.md`
3. `docs/frontend/home/world-focus-product-contract.md`
4. `docs/frontend/home/world-focus-platform-contract.md`
5. `docs/frontend/home/world-focus-structural-contract.md`
6. `docs/frontend/home/world-focus-geometry-contract.md`
7. `docs/frontend/home/world-focus-delivery-methodology.md`
8. supporting reverse-engineering/review evidence referenced by the handoff.

## 5. World Focus immediate next gate

Do **not** start another content mini-vertical yet.

Next bounded work is:

> **World contextual DANTE presence / spatial interaction reverse engineering.**

It must determine, before implementation:

- DANTE's role inside a focused World versus Home/global AI;
- quiet/invoke/contextual/insight/proposal/action presentation states;
- persistent vs transient presence;
- composer/conversation placement and expansion behavior;
- whether/when DANTE consumes layout space versus overlays it;
- interaction with selected World content, Insight and Explore;
- desktop/laptop/tablet/mobile pressure;
- minimum viable remaining content area;
- focus/keyboard/a11y/responsive behavior;
- AI-unavailable behavior;
- pre-backend frontend shell required now versus real runtime deferred to the final backend vertical.

Only after this gate is researched, stress-tested, user-reviewed and frozen may integrated B2 visual acceptance and later World content verticals continue.

## 6. Permanent World Focus delivery method

Every mini-vertical follows:

```text
authority re-read
-> requirements
-> simulations / adversarial pressure
-> product comparison
-> current technology research where relevant
-> architecture alternatives
-> explicit decision / rejected alternatives
-> complete frontend implementation
-> responsive / a11y / security / performance / async / errors
-> automated gates
-> real browser review
-> user functional + visual review
-> fixes
-> explicit user OK
-> freeze
-> next vertical
```

A green CI run never closes a mini-vertical by itself.

## 7. Backend stop line

For World Focus and the temporal frontend phase, do not invent:

- real business APIs;
- DB/Alembic changes;
- persistence rows as frontend contracts;
- provider integrations;
- real LLM/tool execution;
- fake durable success.

Use typed frontend/application ports and deterministic local adapters only where a real product vertical needs them. Real backend/API/DB/provider/LLM integration comes at the agreed final vertical.

## 8. Global authority / semantic alignment

Frontend work consumes rather than redefines:

- Product Identity / North Star;
- product simulations;
- Domain Atlas / Language Map;
- Logical Model;
- Physical Model;
- current Database/Alembic source of record;
- Intelligence / Context / Governed Effect contracts;
- frontend production-readiness contracts.

Permanent examples:

```text
UI model != backend DTO != Domain != persistence row
AI output != canonical fact
AI proposal != Decision
World != canonical Domain owner
World relevance != authorization
planned != actual
absence != false
UI hiding != authorization
```

## 9. Operational rules

- continue on `feature/home-react` until explicitly authorized otherwise;
- inspect fresh branch HEAD before writes;
- do not touch the parallel Access/Auth workstream without a bounded reason;
- no merge/rebase/force/history rewrite/main mutation without explicit authorization;
- never manually edit generated route-tree output;
- preserve frozen Timeline and World geometry contracts unless explicitly reopened by the user;
- update this live checkpoint whenever the active workstream or next gate materially changes.
