# DANTE — Frontend Production-Depth Handoff

**Status:** CURRENT HANDOFF — MULTI-WORKSTREAM FRONTEND BRANCH  
**Date:** 2026-09-01  
**Working branch:** `feature/home-react`  
**Worktree:** `/home/mattia/projects/dante-frontend`

This document is the durable handoff for a new chat/agent working on the frontend branch. For the exact live state and immediate gate, always read `docs/frontend/home/current-checkpoint.md` first.

## 1. Current branch topology

Three distinct concerns coexist on this branch:

```text
APP SHELL / HOME
TEMPORAL / TIMELINE
WORLD FOCUS
```

They share the same product/domain foundation, but they do not own each other's layout or interaction semantics.

In particular:

```text
Home AI != World contextual DANTE
Home Timeline != full temporal workspace
World Focus != Home overlay
Mondi Overview != World Focus
```

Do not transfer a component or geometry from one surface to another merely because the underlying DANTE capability is related.

## 2. Production-depth standard

Each bounded product capability is taken to full frontend depth before the next observable capability is opened:

- product semantics and scenario pressure;
- React/TypeScript ownership;
- state and async/race handling;
- truthful loading/empty/partial/stale/error/unavailable behavior where applicable;
- responsive/container behavior;
- keyboard/focus/accessibility;
- security/privacy/disclosure boundaries;
- performance/resource cleanup;
- deterministic pre-backend adapters where needed;
- unit/component/integration/E2E evidence;
- real-browser review;
- explicit user functional + visual acceptance.

A green automated suite is necessary but not sufficient for product freeze.

## 3. Backend integration stop line

Current frontend work must remain backend-ready without fabricating backend semantics.

Permanent rule:

```text
frontend view model != backend DTO != Domain model != persistence row
```

Frontend code may define intent-specific ports/adapters and runtime validation seams justified by a real vertical. It may not invent endpoint shapes, ORM rows, SQL contracts, provider truth or durable effects.

Real API/DB/provider/LLM integration occurs in the separately authorized final vertical.

## 4. AppShell / Home authority

Durable Home and shared-shell authorities:

- `docs/frontend/home/contract.md`
- `docs/frontend/home/home-structural-contract.md`
- `docs/frontend/app-shell/p1-global-app-shell.md`
- `docs/frontend/open-decisions.md`
- `docs/frontend/ui-registry.md`
- `docs/frontend/design-tokens.md`

Shared AppShell/Topbar is application infrastructure, not owned by Home, Timeline or World Focus.

The accepted Home macro composition and shell geometry must not be reopened by an unrelated World/Timeline implementation.

## 5. Timeline handoff

Timeline T1 observable behavior is frozen and user accepted.

Start a Timeline chat with:

1. `docs/frontend/home/timeline-current-checkpoint.md`
2. `docs/frontend/home/timeline-handoff.md`
3. `docs/frontend/home/timeline-t1-frozen-contract.md`
4. `docs/frontend/home/temporal-experience-architecture.md`
5. `docs/frontend/home/temporal-frontend-roadmap.md`

The roadmap after T1 is planning authority only when the Timeline workstream is explicitly resumed. It does not authorize parallel temporal work while World Focus is active.

## 6. World Focus handoff

World Focus is the active workstream.

Start a World Focus chat with:

1. `docs/frontend/home/world-focus-current-checkpoint.md`
2. `docs/frontend/home/world-focus-handoff.md`
3. `docs/frontend/home/world-focus-product-contract.md`
4. `docs/frontend/home/world-focus-platform-contract.md`
5. `docs/frontend/home/world-focus-structural-contract.md`
6. `docs/frontend/home/world-focus-geometry-contract.md`
7. `docs/frontend/home/world-focus-delivery-methodology.md`
8. evidence documents named by the handoff only when deeper archaeology is required.

Current World Focus state:

```text
structure/route                frozen
WF-G3 geometry                 frozen
B0 foundation                  closed
WR0-WR2 product/context model  closed
B1 Orientation                 closed for sequencing
B2 Continuity                  automated pass; integrated user acceptance deferred
next gate                      World contextual DANTE spatial/presence reverse engineering
```

Do not start another World content vertical before that DANTE gate is resolved.

## 7. Shared engineering rules

- use existing React/TanStack/Vite/TypeScript/tooling rather than creating a duplicate stack;
- strict TypeScript remains enabled; do not weaken it to make a change pass;
- prefer explicit narrow ownership over global managers/event buses;
- no generic repository or universal entity just for frontend convenience;
- no arbitrary generated HTML/JSX/UI from AI;
- routing uses the application router;
- generated route tree is never manually edited;
- design/theme values remain centrally owned;
- semantic state is not communicated by color alone;
- decorative VFX must degrade before it harms responsiveness;
- frontend hiding is never authorization;
- provider unavailable/unknown is never coerced to semantic false;
- cancellation of a React read is not cancellation of a future durable DANTE run/effect.

## 8. Required project authorities when semantics are touched

Re-read the exact current sources relevant to the change, including as applicable:

- Product Identity / North Star;
- feature-discovery simulations;
- multi-actor/collaboration simulations;
- Domain Atlas / Language Map;
- Logical Model;
- Physical Model;
- Database source of record / Alembic history;
- Intelligence Context/Runtime boundaries;
- Governed Operation/Effect contracts;
- frontend production-readiness contracts.

A frontend label or layout convenience never creates a new Domain concept.

## 9. Operational safety

- fresh HEAD check before a new write scope;
- stay on `feature/home-react` unless explicitly authorized otherwise;
- no merge/rebase/force/history rewrite/main mutation without explicit authorization;
- do not casually modify Access/Auth;
- do not weaken frozen Timeline/World geometry regression guards;
- after a material workstream change, update the live checkpoint and the relevant workstream handoff in the same documentation pass.
