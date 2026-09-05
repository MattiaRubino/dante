# DANTE — World Focus D2 Adaptive Conversation Surface Review

**Status:** D2 CLOSED / VALIDATED — D3 NEXT READ-ONLY PREFLIGHT  
**Date:** 2026-09-05  
**Branch:** `feature/home-react`

## 1. Scope and disposition

D2 materializes only the spatial/presentation shell for an ongoing contextual DANTE conversation inside World Focus.

It does **not** materialize conversation messages, model/provider output, a backend adapter, durable Run state, contextual/deictic invocation, Insight semantics, Proposal/Decision/effect semantics, persistence, AuthZ, API, DB or LLM execution.

Accepted D0 behavior is now executable:

```text
wide allocated World workspace with viable split
-> non-modal DANTE conversation sidecar

constrained/mobile World workspace
-> route-owned DANTE focus surface below Global Topbar

wide sidecar + explicit user maximize
-> same conversation surface identity promoted to route focus
-> restore returns the same identity to adaptive presentation
```

## 2. Scope anchor

```text
PRE-SCOPE 0a0a43ac06f93d986674f8521e521dcc05ea2c1e
CODE/TEST  7b787766be83096e82eab1ac116b2704fae5f202
CI         33958677991 / run #969 PASS
```

Final compare from PRE-SCOPE:

```text
status    ahead
ahead_by  24
behind_by 0
merge-base == PRE-SCOPE
```

Net D2 code/test/i18n paths: 15.

No AppShell, Timeline, Access/Auth, generated route tree, backend, API, DB, Alembic, provider, LLM or persistence path changed.

## 3. Materialized ownership

D2 reuses the existing Workspace Platform instead of creating a second conversation/surface engine.

```text
WorldFocusWorkspaceHost
-> remains the single transient surface-stack owner

WorldFocusWorkspaceAllocation
-> remains the single physical split/overlay/external placement policy

WorldFocusDanteConversationPresentationController
-> owns only D2 presentation preference: adaptive | focus
-> asks the existing allocator whether the same conversation can occupy a real sidecar
-> promotes the same surface to `route` when sidecar split is not viable

WorldFocusSurfaceLayer
-> continues rendering workspace-owned placements

WorldFocusRouteSurfaceLayer
-> renders active `external` route-owned placements through the same finite registry/error-boundary path

WorldFocusPage
-> provides the route-owned host below the existing Global Topbar ownership
```

Conversation identity is therefore not presentation geometry.

## 4. Interaction law discovered during falsification

A first production attempt generalized:

```text
presentation = route
=> World main interaction inert
```

Existing Workspace tests correctly rejected that collapse.

The corrected law is orthogonal:

```text
route presentation
!= automatically blocking interaction

generic route surface
-> external + non-blocking by default

DANTE route-focus surface
-> external + explicit blocksWorkspaceInteraction=true
```

The explicit interaction flag also acts as an admission/barrier law so a weaker late surface cannot silently become authoritative above an active route-focus surface.

No kind-specific allocator branch such as `if dante-conversation` was introduced.

## 5. Responsive law

D2 introduces no second viewport breakpoint system.

Adaptive presentation asks the existing allocator against the actual measured World workspace:

```text
sidecar hypothetical placement is viable
-> sidecar

sidecar hypothetical placement is not viable
-> route
```

The hypothetical sidecar check clears route-focus interaction blocking before resolving the trial plan, preventing a route-focus state from falsely proving itself permanently non-splittable.

This preserves the existing Workspace policy, including the established split viability threshold and bounded main/sidecar geometry.

## 6. Focus and accessibility

D2 proves:

- sidecar conversation is non-modal (`aria-modal=false`);
- maximize moves focus to the corresponding Restore control in route focus;
- restore returns focus to the corresponding Maximize control when sidecar becomes viable;
- automatic constrained/mobile transition does not leave focus trapped in the World that becomes inert; focus moves into the active route-focus conversation control;
- route focus blocks the World only when its explicit interaction law requires it;
- generic route presentation remains non-blocking;
- the same registered renderer is used in sidecar and route presentation.

Exact return to the original D1 invoker after a real ongoing-conversation entry transition is not claimed by D2 because D3 has not yet materialized the conversation adapter/entry transition. That remains a later executable obligation rather than a fabricated test harness guarantee.

## 7. No fake conversation semantics

The D2 conversation shell deliberately renders no:

```text
assistant message
user transcript
model answer
provider result
conversation history
canonical fact
Proposal / Decision / receipt
backend Run state
```

The empty structural body is intentional. D3 is the next owner for typed deterministic pre-backend conversation state.

## 8. Falsification evidence

Useful failures were kept as engineering evidence instead of being hidden by weakened tests.

### Historical Workspace regression caught

The existing allocator suite rejected the incorrect universal `route => inert` rule. The repair separated presentation geometry from interaction blocking and preserved historical generic-route semantics.

### Lifecycle lint failure

An effect-driven preference reset was rejected. The production repair uses a keyed idle/active presentation session so each newly opened conversation starts `adaptive` naturally while maximize/restore preference remains stable during the same open surface lifetime.

### CI #968 typecheck failure

```text
CI 33954166534 / run #968
Mobile Bundle PASS
Web E2E PASS
Quality FAIL at Typecheck only
```

Root cause:

```text
exactOptionalPropertyTypes=true
blocksWorkspaceInteraction: undefined
```

The repair omits the optional property when absent rather than widening the type or disabling compiler safety.

No behavioral test or contract was weakened.

## 9. Final green

Final CI `33958677991` / run `#969` on `7b787766be83096e82eab1ac116b2704fae5f202`:

```text
Frontend pre-production contracts PASS
World Focus pre-production contracts PASS
Format active Home workstreams PASS
Lint PASS
Typecheck PASS
Architecture PASS
Generated-source drift PASS
Unit tests PASS
Production build PASS
Diff check PASS
Repository mutation check PASS
Mobile Bundle PASS
Chromium Web E2E PASS
frozen Timeline Firefox PASS
Frontend CI Gate PASS
```

Measured final suite:

```text
82 / 82 web test files
399 / 399 web unit tests
305 modules / 929 dependencies / 0 architecture violations
```

Retained hostile pressure includes the existing 500 synthetic workspace allocation scenarios and 500 deterministic composition scenarios.

## 10. Net changed code/test/i18n paths

```text
apps/web/src/features/world-focus/model/world-focus-d2-route-allocation.test.ts
apps/web/src/features/world-focus/model/world-focus-workspace-allocation.ts
apps/web/src/features/world-focus/model/world-focus-workspace.ts
apps/web/src/features/world-focus/ui/world-focus-core-surfaces.tsx
apps/web/src/features/world-focus/ui/world-focus-dante-conversation.css
apps/web/src/features/world-focus/ui/world-focus-dante-conversation.test.tsx
apps/web/src/features/world-focus/ui/world-focus-dante-conversation.tsx
apps/web/src/features/world-focus/ui/world-focus-page.tsx
apps/web/src/features/world-focus/ui/world-focus-route-surface-layer.tsx
apps/web/src/features/world-focus/ui/world-focus-surface-layer.tsx
apps/web/src/features/world-focus/ui/world-focus-workspace-allocation.test.tsx
apps/web/src/features/world-focus/ui/world-focus-workspace-host.tsx
apps/web/src/features/world-focus/ui/world-focus-workspace.tsx
packages/i18n/src/resources/en/world-focus.ts
packages/i18n/src/resources/it/world-focus.ts
```

## 11. Explicit non-effects

D2 does not change:

```text
WF0 route/shell ownership
WF-G3 macro geometry
Global Topbar ownership
World semantic/domain authority
M1/M2/M3 composition semantics
Timeline
Access/Auth/AuthZ
backend/API/DB/Alembic
provider/LLM execution
persistence
DANTE message/result truth semantics
```

## 12. Closure disposition

> **D2 ADAPTIVE CONVERSATION SURFACE — CLOSED / VALIDATED.**

The next sequential owner is:

> **D3 DETERMINISTIC PRE-BACKEND CONVERSATION ADAPTER — READ-ONLY PREFLIGHT NEXT.**

D3 must preserve:

```text
assistant output != canonical fact
presentation geometry != conversation identity
World/context generation guards remain authoritative for mounted frontend state
no backend/provider/LLM yet
no D4 contextual-reference widening
no D5 Insight collapse
no D6 Proposal/Decision/effect collapse
```

Human/manual visual acceptance remains **NOT PERFORMED**. Automated browser green is not a substitute for that review.
