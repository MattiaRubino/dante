# DANTE — Home Current Checkpoint

**Status:** **P1 APP SHELL FROZEN / P2 DAY CONTEXT NEXT**  
**Date:** 2026-08-29  
**Working branch:** `feature/home-react`  
**Worktree:** `/home/mattia/projects/dante-frontend`  
**Protected main:** `baa9aba52932a0fa09b957ee7668aeb459fb4a20`

For the current strategy read `docs/frontend/home/production-depth-handoff.md` first. The durable behavior/product rules in `docs/frontend/home/contract.md` remain authoritative unless explicitly superseded. P1 closure details live in `docs/frontend/app-shell/p1-global-app-shell.md`; intentionally deferred product/backend decisions live in `docs/frontend/open-decisions.md`.

## Current implementation state

The Home prototype/reference package remains preserved on `main`. The active React implementation remains isolated on `feature/home-react`.

The current branch contains:

- real React Home, no iframe/prototype bridge;
- accepted macro Home geometry/material baseline;
- shared persistent AppShell outside Home ownership;
- real router destinations under the shell;
- production-depth Global Topbar behavior;
- inline Topbar Search with real local navigation and truthful unavailable remote search;
- global Create/launcher/account shells without fake backend success;
- neutral account icon instead of fake identity initials;
- shell-owned theme bridge and centralized visual configuration;
- responsive/keyboard/focus/accessibility test coverage for the shell.

P1 implementation/visual checkpoint accepted and frozen on 2026-08-29:

`e11d6c53d2fe1361b37345bbc3f49792541bd45d`

Documentation commits follow that code checkpoint.

## P1 — Global App Shell + Topbar

P1 is **closed for implementation scope**. Do not reopen it while entering P2 unless a bounded regression demonstrates a real defect.

Final accepted direction:

- Topbar is shared application infrastructure, not Home-owned decoration;
- DANTE master logo remains unmodified;
- current brand/background contrast treatment is accepted for now; further color polish is explicitly deferred;
- Home / Mondi / Oggi use real router navigation;
- Search is a lens icon that expands into an inline central search surface; it is not a modal/backdrop;
- local application destinations are searchable immediately below the field;
- Create remains truthful/deferred where real vertical writes do not exist;
- Review remains deprecated bounded debt;
- account/session identity remains owned by Access/Auth.

See `docs/frontend/app-shell/p1-global-app-shell.md` for the exact contract.

### P1 QA status

Before the final Search/visual polish, the complete frontend gate was green, including **29/29 Playwright E2E**.

The final polish changed Search from a dialog to the inline Topbar surface and updated unit/E2E specifications accordingly. The post-polish regression suite has **not yet been rerun** in the local WSL worktree at this documentation checkpoint. Do not claim that final regression run as green until it is actually executed.

This does not reopen P1 product design: implementation is frozen, and any regression fix must be bounded to the defect found.

## User-reviewed Home visual state

The following remain frozen baseline and must not be casually redesigned:

- macro placement and proportions of Home regions;
- fluid shell/edge attachment geometry;
- AI / upper workspace / Timeline / Context Rail macro composition;
- current overall skin/material direction;
- navy/violet family for panel/material depth;
- DANTE orange for generic active/infrastructure chrome;
- semantic colors for Worlds, timeline groups/events and genuine semantic states.

Visual configuration must remain centralized through tokens/theme ownership rather than scattered component values.

## Phase order

Production-depth work continues one surface at a time:

1. Global App Shell + Topbar — **FROZEN / P1**
2. Day Context Strip / Day Route — **NEXT / P2**
3. Orientation
4. AI conversational surface
5. Central Stage / Mondi
6. Segnali
7. Timeline
8. Context Rail — Capture
9. Context Rail — Resolution
10. whole-Home integration/hardening

## Immediate next pass — P2 Day Context Strip / Day Route

P2 must productionize viewed-day context and day navigation while preserving the frozen AppShell and accepted Home macro geometry.

The pass must establish a single coherent viewed-day source of truth for the Home surface, define local day navigation behavior and its relation to the current real day, and avoid creating a second competing navigation system beside the Global Topbar.

Do not invent persistence/backend semantics. Any deeper date/calendar integration should be represented through explicit frontend state/contracts and future integration boundaries.

Before writes, inspect the current Day Ribbon/orientation/timeline interactions and the machine-readable Home stage/responsive contracts so day context is not implemented independently in several components.

## Product boundaries retained

Central Stage remains:

```text
READ / NAVIGATE / OPEN
NO persistent +
NO ghost add slots
NO fake World/Signal entities
NO direct configuration CRUD inside Home stage
```

Timeline quick-add remains a contextual affordance whose production date/time/persistence contract is still open.

Context Rail still means:

```text
USER -> DANTE     Capture
DANTE -> USER     Resolution
```

Resolution is not a notifications center.

## Required references

A new chat/agent should start with:

- `docs/frontend/home/production-depth-handoff.md`
- `docs/frontend/home/current-checkpoint.md`
- `docs/frontend/app-shell/p1-global-app-shell.md`
- `docs/frontend/open-decisions.md`
- `docs/frontend/home/contract.md`
- `docs/frontend/ui-registry.md`
- `docs/frontend/design-tokens.md`
- `docs/frontend/production-readiness/component-architecture.md`
- `docs/frontend/production-readiness/backend-integration-contract.md`
- `docs/frontend/production-readiness/quality-gates.md`
- current code under `apps/web/src/features/home/`, `apps/web/src/app-shell/` and `apps/web/src/routes/`.

For Home-stage/day/responsive work also inspect:

- `prototypes/frontend/shared/contracts/home-stage.contract.json`
- `prototypes/frontend/shared/contracts/home-stage.view-model.schema.json`
- `prototypes/frontend/shared/contracts/home-responsive.matrix.json`
- `prototypes/frontend/shared/fixtures/home-stage.v0.json`

For visual/behavior archaeology use the complete modular Home prototype preserved on `main` as the oracle.

## Operational rule

Continue on `feature/home-react` until explicitly authorized otherwise. Fresh HEAD check before writes. Bounded write gate before each new implementation scope. No merge/rebase/force/history rewrite/main mutation without explicit authorization. Do not touch the parallel Access/Auth workstream. `routeTree.gen.ts` is generated and must never be edited manually.
