# DANTE — Home Production-Depth Handoff

**Status:** ACTIVE / NEXT IMPLEMENTATION PHASE  
**Date:** 2026-08-28  
**Working branch:** `feature/home-react`  
**Worktree:** `/home/mattia/projects/dante-frontend`  
**Implementation checkpoint before this handoff:** `927200ba64140bc9f7382bf1e9a24b4e832ba926`  
**Current protected main:** `baa9aba52932a0fa09b957ee7668aeb459fb4a20`

## What is already accepted

The Home React migration has reached a stable macro-composition baseline.

User-reviewed and currently frozen unless a later bounded issue proves otherwise:

- global Home macro geometry / regional placement;
- shell attachment geometry;
- overall Home visual direction;
- current navy/violet panel-material family;
- DANTE orange for generic active/infrastructure chrome;
- semantic colors remain owned by Worlds, timeline groups/events and semantic states;
- visual palette is centrally configurable through design tokens rather than scattered raw component colors.

The current Home is real React, not an iframe/prototype bridge.

Important: visual parity is not considered globally complete in every detail. In particular, some component-specific visuals/behavior (for example Central Stage sphere rendering and interaction fidelity) still need to be closed when that component receives its production-depth pass. Do not reopen the accepted macro layout while doing so.

## New implementation strategy

From this checkpoint forward, work **one product surface at a time** and take each touched surface to a production-grade depth before moving to the next.

This is no longer a broad visual mock pass. Each pass must combine:

- accepted prototype visual/behavioral intent;
- correct React/TypeScript ownership and state boundaries;
- reusable infrastructure where justified;
- real frontend-local interaction behavior;
- truthful unavailable/pending/error behavior for backend-dependent capabilities;
- responsive, accessibility, keyboard/focus, reduced-motion and test evidence appropriate to the surface;
- future backend integration through explicit ports/adapters rather than component rewrites.

Quality target is a large, advanced production application. Do not optimize for the quickest demo implementation.

## High-level pass order

Current intended order:

1. **Global App Shell + Topbar**
2. Day Context Strip / Day Route
3. Orientation
4. AI conversational surface
5. Central Stage / Mondi
6. Segnali
7. Timeline
8. Context Rail — Capture
9. Context Rail — Resolution
10. whole-Home integration/hardening

This order may be adjusted only for a real dependency, not convenience.

## Immediate next pass — Global App Shell + Topbar

Treat the Topbar as shared application infrastructure, not as a Home-owned decorative component.

Target architecture is a persistent application shell containing the global Topbar and a route outlet. Home, Mondi, Oggi and future pages should render below the same shell rather than each owning a duplicate bar.

For destinations whose real vertical is not implemented yet, use clean routable placeholder/default pages where useful. They must preserve normal browser back/forward/deep-link behavior and the persistent Topbar; do not invent the future Mondi/Oggi product implementation during this pass.

Standard shell interactions that are generic and can be implemented correctly now should be productionized now (for example navigation and the generic UI shell for Search/Create/launcher/account overlays). Backend-dependent search, creation, account/session or other writes must not fake success.

Reusable overlay primitives are allowed when they genuinely serve several global shell controls. They should centralize focus management, keyboard/Escape, outside interaction, ARIA, portal/layering, responsive positioning, reduced motion and related concerns instead of duplicating ad-hoc implementations.

Legacy `Review` remains bounded/deprecated product debt; do not build a large new workflow around it unless a separate product decision explicitly reopens it.

## Architecture / engineering rules that must remain true

- UI/view model != backend DTO != Domain != persistence row.
- Backend-dependent features use explicit ports/adapters and boundary validation when integration arrives.
- No ad-hoc direct HTTP contract from components.
- No fake backend success.
- Frontend-local behavior should be real, not a static mock.
- Routing must use the application router, not hard-coded browser navigation hacks.
- Shared shell concerns belong outside Home feature ownership where appropriate.
- Avoid premature mega-abstractions, but do not duplicate cross-cutting primitives already clearly needed by several surfaces.
- Styling/material choices must remain centrally configurable. Prefer design/semantic/theme tokens; do not scatter raw palette values through components.
- Generated token output is generated authority; source token files are the editable authority.
- Keep semantic World/event/state colors distinct from generic infrastructure chrome.
- Do not manually edit generated route-tree output.

## Current theme authority

Home palette/material configuration is intentionally centralized.

Read and preserve:

- `packages/design-tokens/tokens/home-theme.json`
- `packages/design-tokens/tokens/primitives.json`
- `packages/design-tokens/tokens/semantic.json`
- `packages/design-tokens/terrazzo.config.ts`
- `apps/web/src/features/home/ui/home-skin.css`

A future broad recolor should be possible primarily from the token/theme layer rather than by editing every component.

## Required read order for a new chat/agent

Before proposing writes, inspect at least:

1. `docs/frontend/home/production-depth-handoff.md` — this file; current phase/strategy.
2. `docs/frontend/home/current-checkpoint.md` — accepted Home visual/product checkpoint.
3. `docs/frontend/home/contract.md` — durable Home behavior/product boundaries.
4. `docs/frontend/ui-registry.md` — control IDs/statuses and what is ACTIVE/WORKING/PROTOTYPE_ONLY/DEPRECATED.
5. `docs/frontend/design-tokens.md` plus the Home theme/token files above.
6. `docs/frontend/production-readiness/component-architecture.md`.
7. `docs/frontend/production-readiness/backend-integration-contract.md`.
8. `docs/frontend/production-readiness/quality-gates.md`.
9. Machine-readable Home contracts under `prototypes/frontend/shared/contracts/` when the touched surface depends on them.
10. The actual current React implementation under `apps/web/src/features/home/` and current routes before making assumptions from documentation.

For visual archaeology, the complete modular Home prototype is now preserved on `main`; use it as the visual/behavior oracle where needed. Do not revive arbitrary older screenshots or historical prototype branches as a competing target.

## Operational rule

Work remains on `feature/home-react` until explicitly authorized otherwise.

Before every write scope:

- verify current branch/HEAD and unexpected movement;
- state the bounded write gate and exclusions;
- wait for explicit user authorization unless the user's message itself unmistakably authorizes that exact write;
- no merge/rebase/force/history rewrite/main mutation without an explicit gate;
- do not touch the parallel Access/Auth workstream.

When a pass is finished, update current documentation/registry/contracts only where the touched behavior or ownership actually changed, and record enough state that another chat can continue without rediscovering the project.
