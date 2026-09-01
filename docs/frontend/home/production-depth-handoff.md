# DANTE — Frontend Production-Depth Handoff

**Status:** CURRENT HANDOFF — MULTI-WORKSTREAM FRONTEND BRANCH / WORLD FOCUS D2 NEXT  
**Date:** 2026-09-01  
**Working branch:** `feature/home-react`  
**Worktree:** `/home/mattia/projects/dante-frontend`

This document is the branch-level durable handoff for a new frontend chat/agent. For exact live state and immediate gate, always read `docs/frontend/home/current-checkpoint.md` first, then the active workstream checkpoint/handoff.

---

## 1. Current branch topology

Three distinct concerns coexist:

```text
APP SHELL / HOME
TEMPORAL / TIMELINE
WORLD FOCUS
```

They share product/domain foundations but do not own one another's layout or interaction semantics.

In particular:

```text
Home AI != World contextual DANTE
Home Timeline != full temporal workspace
World Focus != Home overlay
Mondi Overview != World Focus
```

Do not transfer component geometry/state semantics from one surface to another merely because the underlying DANTE capability is related.

---

## 2. Production-depth standard

Each bounded product capability is taken to full frontend depth before the next observable capability is opened:

- product semantics and scenario pressure;
- React/TypeScript ownership;
- narrow application/state seams;
- async/race behavior;
- truthful loading/empty/partial/stale/error/unavailable behavior where applicable;
- responsive/container behavior;
- keyboard/focus/accessibility/reduced motion;
- security/privacy/disclosure boundaries;
- performance/resource cleanup;
- deterministic pre-backend adapters only where needed;
- unit/component/integration/E2E evidence;
- real-browser automated acceptance;
- human/user functional + visual acceptance where available/required;
- truthful final disposition.

A green automated suite is necessary but does not mean a human visual review happened.

When the user explicitly delegates closure authority, sequencing may proceed on sufficient engineering/browser evidence, but documentation must still state honestly which human/manual review was not performed.

---

## 3. Backend integration stop line

Current frontend work must remain backend-ready without fabricating backend semantics.

Permanent rule:

```text
frontend view model != backend DTO != Domain model != persistence row
```

Frontend may define intent-specific ports/adapters/runtime validation seams justified by a real vertical. It may not invent endpoint shapes, ORM rows, SQL contracts, provider truth, durable Runs or effects merely to make the UI look complete.

Real API/DB/provider/LLM/tool integration occurs only in the separately authorized final backend vertical.

---

## 4. AppShell / Home authority

Durable Home/shared-shell authorities:

```text
docs/frontend/home/contract.md
docs/frontend/home/home-structural-contract.md
docs/frontend/app-shell/p1-global-app-shell.md
docs/frontend/open-decisions.md
docs/frontend/ui-registry.md
docs/frontend/design-tokens.md
```

Shared AppShell/Global Topbar is application infrastructure, not owned by Home, Timeline or World Focus.

The accepted Home macro composition and shell geometry must not be reopened by an unrelated World/Timeline implementation.

---

## 5. Timeline handoff

Timeline T1 observable behavior is frozen and user accepted.

Start a Timeline chat with:

```text
1. docs/frontend/home/timeline-current-checkpoint.md
2. docs/frontend/home/timeline-handoff.md
3. docs/frontend/home/timeline-t1-frozen-contract.md
4. docs/frontend/home/temporal-experience-architecture.md
5. docs/frontend/home/temporal-frontend-roadmap.md
```

T2+ roadmap content is planning authority only when Timeline is explicitly resumed. It does not authorize parallel temporal work while World Focus is active.

World Focus CI continues to preserve the frozen Firefox Timeline interaction contract. Never weaken it as collateral damage.

---

## 6. World Focus handoff — current state

World Focus is the active workstream.

Start with:

```text
1. docs/frontend/home/world-focus-current-checkpoint.md
2. docs/frontend/home/world-focus-handoff.md
3. docs/frontend/home/world-focus-frontend-roadmap.md
4. docs/frontend/home/world-focus-product-contract.md
5. docs/frontend/home/world-focus-platform-contract.md
6. docs/frontend/home/world-focus-structural-contract.md
7. docs/frontend/home/world-focus-geometry-contract.md
8. docs/frontend/home/world-focus-workspace-platform-checkpoint.md
9. docs/frontend/home/world-focus-dynamic-composition-allocation-review.md
10. docs/frontend/home/world-focus-dante-spatial-presence-review.md
11. docs/frontend/home/world-focus-d1-dante-entry-review.md
12. docs/frontend/home/world-focus-workspace-scenario-oracle-evidence.md
13. docs/frontend/home/world-focus-delivery-methodology.md
14. docs/frontend/home/world-focus-evidence-index.md
```

Current World Focus state:

```text
WF0 structure/route                   FROZEN / USER AUTHORIZED
WF-G3 geometry                        LOCKED / USER AUTHORIZED
WF-V4 VFX                             candidate
B0 foundation                         engineering closed
WR0-WR2 product/context model         closed
B1 Orientation                        closed for sequencing
B2 Continuity                         implemented / automated pass
Workspace Platform                    engineering closed
D0 contextual DANTE spatial contract accepted
D1 quiet invoke + composer             closed for sequencing
NEXT                                  D2 adaptive conversation surface
```

Workspace Platform final evidence:

```text
HEAD 6c441335a75bb913af8da1eda569d8094d38a539
CI   33549465793 — PASS
```

D1 final code evidence:

```text
HEAD f17291de32e6bdced20536807b32928ec1be6aea
CI   33552437179 — PASS
```

D1 was closed for sequencing under explicit user delegated authority after strict real-browser/a11y evidence. Manual assistant visual review is not claimed; integrated visual polish remains D7 work.

---

## 7. World Workspace Platform now available

The old handoff state that said `World Workspace Platform materialization NEXT` is obsolete.

The platform is already implemented and stress-tested.

It provides:

```text
dynamic composition planner
finite approved module registry
finite approved surface registry
local transient workspace reducer
bounded interaction cursor
generation tracking / stale intent guard
surface open / replace / promote / close
Escape ownership
blocking-tail barrier
main allocation full | split
top layer none | overlay | focus
interaction interactive | inert
actual ResizeObserver workspace measurement
nested world-focus-main container queries
wide sidecar real-width allocation
narrow sidecar non-modal overlay fallback
modal/full-focus main inert
visible underlying sidecar inert under blocking layer
dormant surface filtering
local render/surface degradation
```

Stress evidence:

```text
500 deterministic composition scenarios
500 deterministic allocation/surface-stack scenarios
```

It is controlled extensibility, not an AI-generated plugin framework and not a generic dashboard ontology.

---

## 8. D0 contextual DANTE spatial direction now accepted

The old handoff state that said `next gate = World contextual DANTE spatial/presence reverse engineering` is obsolete.

That research was completed and accepted.

External official patterns reviewed included:

```text
Google Workspace / Gemini
Microsoft 365 / Copilot
VS Code / Copilot Chat
Notion Agent
Linear Agent
```

Durable synthesis:

> **AI availability is persistent; AI footprint is not.**

Accepted adaptive hybrid:

```text
quiet DANTE invoke
-> compact non-modal composer
-> wide ongoing conversation sidecar
-> constrained/mobile route-owned focus overlay below Global Topbar
-> explicit maximize/restore
-> explicit bounded contextual/deictic invocation
```

Home AI remains distinct from World DANTE.

---

## 9. D1 contextual DANTE entry now implemented

D1 proves the quiet/invoke part of D0 without faking later conversation/backend behavior.

Implemented:

```text
quiet lower-trailing invoke
>=44px target
localized accessible World-specific label
no auto-open
registered dante-composer popover
aria-modal=false
World remains interactive
textarea autofocus
close/Escape focus restoration
truthful unavailable state
draft-preserving pre-backend submit failure
no fake answer
no fake Run/model/tool/effect
390px containment
axe wide + compact
```

Critical global context decision:

```text
contextReference: null
```

A currently selected projection is not silently inherited. Explicit deictic context belongs to D4.

D1 also exposed/fixed a generic surface bug: non-modal popover overlay wrappers are pointer-transparent outside the actual panel so main World interaction remains physically possible.

---

## 10. Immediate active gate — D2 adaptive conversation surface

D2 must prove spatial/presentation continuity for one ongoing DANTE conversation.

Accepted target:

```text
wide allocated workspace
-> internal split sidecar

constrained/mobile
-> route-owned focus overlay below Global Topbar

wide/deep explicit action
-> maximize sidecar to focus overlay

restore
-> same logical conversation / appropriate presentation
```

Critical warning:

The Workspace Platform's current workspace-local `full-screen` slot alone is insufficient for mobile. WF0 can leave only ~238px World workspace width at 390px viewport.

D2 must establish a route-owned overlay seam that may cover the World while using route width below Global Topbar, without resizing/re-owning the Topbar or changing frozen WF-G3 workspace geometry.

Presentation geometry must not become conversation identity.

D2 must **not** pull D3 forward: no assistant transcript, fake reply, streaming, model call, provider/runtime, API or durable conversation persistence.

---

## 11. D3-D7 forward sequence

```text
D3 deterministic pre-backend conversation adapter
   typed user/message/result distinctions
   conversation identity
   loading/error/unavailable/cancellation/generation
   no real LLM/provider/backend

D4 explicit contextual/deictic invocation
   bounded reference only
   reference != source truth/auth/DOM
   global invoke remains context-null

D5 Insight presentation integration
   conversation != Insight
   Insight may own standalone registered surface

D6 Proposal / confirmation / receipt
   Proposal != Decision != effect
   tool call != authorization
   controlled blocking confirmation
   still no real effect backend

D7 integrated World + DANTE visual/product/a11y review
   desktop/laptop/tablet/mobile
   revisit deferred B1/B2 micro-polish
   VFX/content hierarchy
   sparse/dense/unknown World pressure
   explicit frontend freeze before backend
```

---

## 12. Shared engineering rules

- use current React/TanStack/Vite/TypeScript/tooling; do not create a duplicate stack;
- strict TypeScript remains enabled;
- do not weaken ESLint/typecheck/architecture/a11y/E2E to make code pass;
- prefer narrow explicit ownership over global managers/event buses;
- no universal repository/entity abstraction for frontend convenience;
- no arbitrary generated HTML/JSX/UI from AI;
- routing uses the application router;
- generated route tree is never manually edited;
- design/theme values remain centrally owned;
- semantic state is not color-only;
- decorative VFX degrades before interaction quality;
- frontend hiding is never authorization;
- unavailable/unknown provider state is never coerced to semantic false;
- cancellation of a React read is not cancellation of a future durable DANTE Run/effect;
- presentation geometry is not semantic conversation identity;
- World/context labels are not authorization.

---

## 13. Project authorities when semantics are touched

Re-read current sources relevant to the change, including as applicable:

- Product Identity / North Star;
- feature-discovery/product simulations;
- multi-actor/collaboration simulations;
- Domain Atlas / Language Map;
- Logical Model;
- Physical Model;
- current Database/Alembic source of record;
- Intelligence Context/Runtime boundaries;
- Governed Operation/Effect contracts;
- frontend production-readiness contracts.

A frontend label/layout convenience never creates a new Domain concept.

Permanent barriers include:

```text
AI output != canonical fact
AI proposal != Decision
Decision != effect
World != canonical Domain owner
World relevance != authorization
selected context != authorization
provider state != canonical DANTE truth
planned != Actual
absence != false
UI hiding != authorization
```

---

## 14. Operational safety

- fresh HEAD check before every new write scope;
- stay on `feature/home-react` unless explicitly authorized otherwise;
- no merge/rebase/force/history rewrite/main mutation without explicit authorization;
- do not casually modify Access/Auth;
- do not weaken frozen Timeline/World geometry regression guards;
- no failure ZIP/artifact should become a handoff dependency;
- after material workstream change, update the branch live checkpoint + relevant workstream live checkpoint/handoff/roadmap in the same documentation pass.
