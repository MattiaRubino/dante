# DANTE — Home Current Checkpoint

**Status:** **USER-REVIEWED REACT BASELINE / PRODUCTION-DEPTH PHASE STARTING**  
**Date:** 2026-08-28  
**Working branch:** `feature/home-react`  
**Worktree:** `/home/mattia/projects/dante-frontend`  
**Protected main:** `baa9aba52932a0fa09b957ee7668aeb459fb4a20`

For the current implementation strategy and new-chat handoff, read `docs/frontend/home/production-depth-handoff.md` first. The durable behavior/product rules in `docs/frontend/home/contract.md` remain authoritative unless explicitly superseded.

## Current implementation state

The Home prototype/reference package is preserved on `main`. The active React implementation remains isolated on `feature/home-react`.

The branch was reset cleanly onto current `main` plus the approved H1B React skeleton, then rematerialized as a real React Home. The temporary iframe/prototype bridge and earlier failed visual-parity sediment are not the current architecture.

Current implementation lineage includes:

- clean H1B shell/region foundation;
- M1 React materialization of the complete Home regions;
- `/home` route;
- DANTE branding and approved cosmos/background asset;
- centralized Home visual theme/material layer;
- current theme/token rebinding so broad palette changes are controlled from the design-token/theme layer rather than scattered component values.

Implementation checkpoint immediately before the production-depth documentation handoff:

`927200ba64140bc9f7382bf1e9a24b4e832ba926`

The documentation handoff itself is committed after that checkpoint.

## User-reviewed visual state

The following are currently accepted and should be treated as **frozen baseline**, not casually redesigned:

- macro placement and proportions of the Home regions;
- fluid shell/edge attachment geometry;
- Topbar placement;
- AI / upper workspace / Timeline / Context Rail macro composition;
- current overall skin/material direction;
- navy/violet family for panel/material depth;
- DANTE orange for generic active/infrastructure chrome;
- semantic colors for Worlds, timeline groups/events and genuine semantic states.

The visual theme must remain centrally configurable. Current editable authority includes `packages/design-tokens/tokens/home-theme.json`; generated token output is not the source to hand-edit.

## What is not yet closed

M1 is not claimed as pixel/behavior perfect in every component.

Some component-specific details still differ from the final prototype and must be corrected inside the corresponding production-depth pass. The clearest known example is Central Stage / Mondi: sphere rendering and interaction fidelity are not yet equivalent to the prototype.

Do **not** respond to those remaining differences by reopening the accepted macro geometry or broad skin. Fix each component inside its own ownership boundary when its pass arrives.

No claim is made yet that the full current branch has passed the final whole-Home responsive/browser/accessibility/performance matrix after the latest materialization/theme work.

## Phase decision — production depth one surface at a time

From this checkpoint onward, implementation proceeds one surface at a time at production-app depth rather than by another broad mock/parity sweep.

High-level intended order:

1. Global App Shell + Topbar
2. Day Context Strip / Day Route
3. Orientation
4. AI conversational surface
5. Central Stage / Mondi
6. Segnali
7. Timeline
8. Capture
9. Resolution
10. whole-Home integration/hardening

Each pass should close the touched surface as deeply as practical: architecture, real local interactions, routing/overlay behavior where applicable, responsive behavior, accessibility/keyboard/focus, testing and future backend integration boundaries — while preserving the accepted visual/product contract.

## Immediate next pass

**Global App Shell + Topbar.**

Topbar is to become shared persistent application infrastructure rather than a Home-owned decorative element. Home, Mondi, Oggi and future pages should live under a common shell/route outlet.

Generic shell behavior that can be implemented correctly now should work for real. Where deeper verticals do not yet exist, clean routable placeholder/default pages are acceptable so navigation/back/deep-link behavior can be established without inventing the future product.

Search/Create/launcher/account may receive production-grade generic overlay/menu shells where those are shared application primitives. Backend-dependent search/create/session semantics must remain truthful and must not fake successful writes. Legacy Review remains deprecated/bounded debt rather than a new workflow investment.

## Architecture/quality bar

Target quality is a large, advanced professional application, not a demo.

Key rules:

- frontend view model != backend DTO != Domain != persistence row;
- backend integration through explicit ports/adapters and boundary validation;
- no ad-hoc direct HTTP contract from components;
- frontend-local actions should be real;
- backend-dependent actions must not fake success;
- router-based navigation and real browser history/deep links;
- cross-cutting overlay/focus/keyboard concerns should be centralized where genuinely shared;
- semantic/design/theme tokens own configurable visual values;
- no manual edits to generated route-tree output;
- applicable tests, accessibility, responsive and reduced-motion evidence are required before closing a durable pass.

## Product boundaries still retained

Central Stage remains:

```text
READ / NAVIGATE / OPEN
NO persistent +
NO ghost add slots
NO fake World/Signal entities
NO direct configuration CRUD inside Home stage
```

Mondi and Segnali remain projections inside one stable stage. Management belongs to dedicated surfaces.

Timeline quick-add remains a real contextual affordance whose final production mutation/persistence contract is still open; do not invent backend semantics.

Context Rail still means:

```text
USER -> DANTE     Capture
DANTE -> USER     Resolution
```

Resolution is not a notifications center; complex cases escalate to a deeper controlled surface.

## Required references

A new chat/agent should not work from memory alone. Start with:

- `docs/frontend/home/production-depth-handoff.md`
- `docs/frontend/home/contract.md`
- `docs/frontend/ui-registry.md`
- `docs/frontend/design-tokens.md`
- `docs/frontend/production-readiness/component-architecture.md`
- `docs/frontend/production-readiness/backend-integration-contract.md`
- `docs/frontend/production-readiness/quality-gates.md`
- current code under `apps/web/src/features/home/`
- current routes under `apps/web/src/routes/`
- current Home theme/token sources under `packages/design-tokens/`

For Home-stage/responsive work also inspect:

- `prototypes/frontend/shared/contracts/home-stage.contract.json`
- `prototypes/frontend/shared/contracts/home-stage.view-model.schema.json`
- `prototypes/frontend/shared/contracts/home-responsive.matrix.json`
- `prototypes/frontend/shared/fixtures/home-stage.v0.json`

For visual/behavior archaeology use the complete modular Home prototype preserved on `main` as the oracle. Do not choose an old screenshot or arbitrary historical prototype branch as a competing target.

## Operational rule

Continue on `feature/home-react` until explicitly authorized otherwise. Fresh HEAD check before writes. Bounded write gate before each new implementation scope. No merge/rebase/force/history rewrite/main mutation without explicit authorization. Do not touch the parallel Access/Auth workstream.
