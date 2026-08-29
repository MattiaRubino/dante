# DANTE — Home Production-Depth Handoff

**Status:** ACTIVE / P1 FROZEN / P2 NEXT  
**Date:** 2026-08-29  
**Working branch:** `feature/home-react`  
**Worktree:** `/home/mattia/projects/dante-frontend`  
**P1 frozen implementation checkpoint:** `e11d6c53d2fe1361b37345bbc3f49792541bd45d`  
**Current protected main:** `baa9aba52932a0fa09b957ee7668aeb459fb4a20`

Read `docs/frontend/home/current-checkpoint.md` together with this file. P1 closure details are in `docs/frontend/app-shell/p1-global-app-shell.md`; intentionally deferred decisions are tracked in `docs/frontend/open-decisions.md`.

## What is already accepted

The Home React migration has a stable macro-composition baseline and P1 Global App Shell + Topbar is frozen for implementation scope.

User-reviewed and currently frozen unless a later bounded issue proves otherwise:

- global Home macro geometry / regional placement;
- shell attachment geometry;
- overall Home visual direction;
- current navy/violet panel-material family;
- DANTE orange for generic active/infrastructure chrome;
- semantic colors remain owned by Worlds, timeline groups/events and semantic states;
- visual palette is centrally configurable through design tokens rather than scattered raw component colors;
- shared persistent AppShell/Topbar ownership;
- current inline Topbar Search interaction model;
- DANTE master logo remains unmodified.

The current Home is real React, not an iframe/prototype bridge.

Component-specific parity/production work remains for later passes. Do not reopen accepted macro layout while fixing a component.

## Production-depth strategy

Work **one product surface at a time** and take each touched surface to production-grade depth before moving on.

Each pass must combine:

- accepted prototype visual/behavioral intent;
- correct React/TypeScript ownership and state boundaries;
- reusable infrastructure where justified;
- real frontend-local interaction behavior;
- truthful unavailable/pending/error behavior for backend-dependent capabilities;
- responsive, accessibility, keyboard/focus, reduced-motion and test evidence appropriate to the surface;
- future backend integration through explicit ports/adapters rather than component rewrites.

Quality target is a large, advanced production application, not a demo.

## Pass order

1. **Global App Shell + Topbar — FROZEN / P1**
2. **Day Context Strip / Day Route — NEXT / P2**
3. Orientation
4. AI conversational surface
5. Central Stage / Mondi
6. Segnali
7. Timeline
8. Context Rail — Capture
9. Context Rail — Resolution
10. whole-Home integration/hardening

Adjust this order only for a real dependency.

## P1 closure summary

The Topbar is now shared application infrastructure rather than Home-owned decoration.

Current shell behavior includes:

- persistent AppShell with route outlet;
- `/home`, `/worlds`, `/today`, `/profile`, `/settings` real router destinations;
- Access `/` outside AppShell;
- Search represented by a lens trigger that expands into an inline central search field;
- immediate local destination results below Search;
- keyboard/focus behavior for Search and menus;
- truthful remote-search unavailability;
- Create capability discovery without fake writes;
- launcher and neutral account shell;
- deprecated Review kept bounded rather than expanded;
- shell-owned visual/theme bridge and responsive behavior.

Further Topbar brand-background color tuning is explicitly deferred. Do not recolor the DANTE master logo to solve contrast.

Before the final inline-Search/visual polish, the complete frontend gate was green including 29/29 Playwright E2E. The post-polish regression suite still needs one real rerun; do not claim that rerun as green until executed. P1 product scope nevertheless remains frozen, and any regression fix must be bounded to the defect.

## Immediate next pass — P2 Day Context Strip / Day Route

P2 owns the viewed-day context strip/ribbon and the Home day-route interaction model.

The goal is not merely to make the strip clickable. P2 must establish one coherent frontend source of truth for the day being viewed and define how the relevant Home surfaces consume it without duplicating state.

P2 should determine and productionize, within existing product contracts:

- what constitutes `viewed day` versus real current day/now;
- previous/next-day navigation and return-to-today behavior where supported by the accepted design;
- whether viewed-day state belongs in route/search state or another explicit navigation state boundary;
- synchronization requirements between Day Context, Orientation and Timeline;
- browser history/deep-link expectations for day changes;
- date formatting/i18n and timezone-safe frontend representation;
- keyboard/focus/accessibility and responsive behavior;
- empty/loading/error boundaries only where real data dependencies exist;
- future calendar/backend integration boundary without fake persistence.

Do not create a second global-navigation system beside the Topbar. Do not change the frozen AppShell ownership or accepted Home macro geometry.

Before writing P2, inspect the actual current React day ribbon/orientation/timeline code and machine-readable Home contracts. Do not infer the day model only from screenshots.

## Architecture / engineering rules that must remain true

- UI/view model != backend DTO != Domain != persistence row.
- Backend-dependent features use explicit ports/adapters and boundary validation when integration arrives.
- No ad-hoc direct HTTP contract from components.
- No fake backend success.
- Frontend-local behavior should be real, not a static mock.
- Routing must use the application router, not hard-coded browser navigation hacks.
- Shared shell concerns stay outside Home feature ownership.
- Avoid premature mega-abstractions, but do not duplicate genuinely shared state/behavior.
- Styling/material choices remain centrally configurable through semantic/design/theme tokens.
- Generated token output is generated authority; source token files are editable authority.
- Keep semantic World/event/state colors distinct from generic infrastructure chrome.
- Do not manually edit generated route-tree output.

## Current theme authority

Read and preserve:

- `packages/design-tokens/tokens/home-theme.json`
- `packages/design-tokens/tokens/shell-theme.json`
- `packages/design-tokens/tokens/primitives.json`
- `packages/design-tokens/tokens/semantic.json`
- `packages/design-tokens/terrazzo.config.ts`
- `apps/web/src/features/home/ui/home-skin.css`
- `apps/web/src/app-shell/ui/app-shell-theme.css`

A future broad recolor should be possible primarily from token/theme ownership rather than editing individual components.

## Required read order for a new chat/agent

Before proposing P2 writes, inspect at least:

1. `docs/frontend/home/production-depth-handoff.md`
2. `docs/frontend/home/current-checkpoint.md`
3. `docs/frontend/app-shell/p1-global-app-shell.md`
4. `docs/frontend/open-decisions.md`
5. `docs/frontend/home/contract.md`
6. `docs/frontend/ui-registry.md`
7. `docs/frontend/design-tokens.md`
8. `docs/frontend/production-readiness/component-architecture.md`
9. `docs/frontend/production-readiness/backend-integration-contract.md`
10. `docs/frontend/production-readiness/quality-gates.md`
11. machine-readable Home contracts under `prototypes/frontend/shared/contracts/` relevant to day/responsive behavior;
12. actual current React implementation under `apps/web/src/features/home/`, AppShell and routes.

For visual archaeology, use the complete modular Home prototype preserved on `main` as the oracle. Do not revive arbitrary historical screenshots or prototype branches as competing targets.

## Operational rule

Work remains on `feature/home-react` until explicitly authorized otherwise.

Before every new implementation write scope:

- verify current branch/HEAD and unexpected movement;
- state the bounded write gate and exclusions;
- wait for explicit user authorization unless the user's message itself unmistakably authorizes that exact write;
- no merge/rebase/force/history rewrite/main mutation without an explicit gate;
- do not touch the parallel Access/Auth workstream;
- never manually edit `routeTree.gen.ts`.

When a pass is finished, update current documentation/registry/contracts only where touched behavior or ownership actually changed.
