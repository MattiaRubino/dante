# DANTE — World Focus Platform Contract

**Status:** CURRENT PRE-BACKEND PLATFORM AUTHORITY  
**Date:** 2026-09-01  
**Branch:** `feature/home-react`

This document defines implementation ownership and platform invariants for World Focus inside the frozen route/shell/workspace. Product semantics are governed by `world-focus-product-contract.md`; exact structural geometry is governed by the structural/geometry contracts.

## 1. Platform thesis

World Focus is a small application platform for one continuity context, not a dashboard framework and not a second DANTE runtime.

Target conceptual ownership:

```text
WORLD FOCUS HOST
route / lifecycle / entry / return / top-level failure
        │
        ▼
WORLD ORIENTATION
identity / concise purpose
        │
        ├───────────────────────────────────────┐
        ▼                                       ▼
DYNAMIC COMPOSITION                       CONTEXTUAL DANTE
question-driven projections               interaction / Insight / Proposal
stable + adaptive + ephemeral             presentation over shared Intelligence
        │                                       │
        └────────────────┬──────────────────────┘
                         ▼
               APPLICATION BOUNDARIES
               typed reads / intents
               validation / freshness / races
                         │
                         ▼
             deterministic local adapter [NOW]
             real backend adapter         [LATER]
```

The exact spatial relation between contextual DANTE and dynamic composition is intentionally unresolved and is the current product gate.

## 2. Permanent invariants

```text
World != canonical Domain owner
World relevance != ownership
World relevance != authorization
WorldProjection != canonical truth
ModuleConfig != canonical source data
ModuleProjection != canonical source data
LayoutConfig != Domain semantics
AI output != accepted fact
AI proposal != Decision
Tool call != authorization
Provider state != DANTE canonical state
Planned != actual
Observation != causation
Absence != false
UI hiding != authorization
```

One canonical reality may be projected into several Worlds without duplication.

## 3. Layering / package ownership

Current feature shape:

```text
apps/web/src/features/world-focus/
├── model/
├── application/
├── ui/
└── index.ts
```

Dependency direction:

```text
model
  -> pure feature semantics/primitives

application
  -> model
  -> orchestration / typed boundaries

ui
  -> model/application

route
  -> public feature API
```

World Focus must not import Home internals. Home, Timeline and World Focus are sibling product surfaces.

Do not create speculative `manager/service/core/plugin-system` forests without a concrete owner/problem.

## 4. Host / route ownership

The host owns:

- `/worlds/:worldId` lifecycle;
- entry/return source;
- browser back/deep-link behavior;
- active World identity at route/navigation level;
- top-level usable/loading/error/unavailable boundary;
- focus entry/return where applicable;
- mounting the frozen World Focus workspace.

The host does not own:

- per-module semantics;
- backend authorization;
- DANTE provider/model routing;
- persistence schema;
- per-World page branching.

## 5. Session / cursor rule

Do **not** maintain a feature Session object merely because the route has an active World.

A session/cursor is introduced only when a real interaction needs transient ownership beyond route state, e.g.:

```text
selected projection/source
current Explore/Insight
contextual conversation reference
deictic follow-up target
request interaction generation
query/Lens scope when actually justified
```

The old Lens-only Session was removed with B1.

A cursor stores bounded references/hints, not copied canonical truth, secrets or serialized React state.

## 6. Application / projection boundaries

Frontend components consume intent-specific application boundaries.

Preferred pattern:

```text
UI
-> typed intent-specific reader/command seam
-> runtime validation
-> deterministic local adapter [NOW]
-> real backend adapter [LATER]
```

Do not introduce a generic repository because several modules need data.

The application boundary owns:

- request identity/generation;
- validation of unknown adapter payloads;
- conversion into frontend projection semantics;
- truthful resource state;
- provenance/freshness fields where meaningful;
- intent invocation seams;
- cancellation/race ownership.

It does not invent backend DTOs/ORM rows.

B2 Continuity is the first concrete production example.

## 7. Runtime validation

Static TypeScript is not a trust boundary.

B0 provides a validator-neutral boundary pattern:

```text
unknown adapter/external payload
-> adapter-owned validation
-> validated frontend application value
-> UI
```

Validation errors must not echo rejected sensitive payload contents into user-facing UI/logging.

Choose a schema library only when the first real transport/shared-schema problem proves the need.

## 8. Async / race / cancellation

B0 provides latest-read ownership semantics.

Required behavior:

```text
A starts
B supersedes A
-> A aborted/invalidated
-> A can never commit into B/current World
```

Upstream AbortSignal may cancel obsolete reads.

Important distinction:

```text
frontend read lifetime != future durable DANTE Run/effect lifetime
```

Unmount/navigation must not semantically cancel durable backend work unless an explicit cancellation operation exists.

A contextual DANTE run remains bound to the initiating World/cursor generation.

## 9. Shared status vocabulary

Use finite truthful states where applicable:

```text
loading
ready
empty
partial
stale
error
unavailable
```

Do not collapse:

```text
empty == unavailable
stale == current
provider timeout == no result
```

Not every component must expose every state; the owning projection defines applicable lifecycle.

## 10. Composition model

World composition consumes Product Contract output questions.

```text
available authorized projections
-> useful current questions
-> ranking
-> stable/adaptive/ephemeral composition
```

Shared axes:

```text
stability: stable / adaptive / ephemeral
origin: system-default / user / dante-proposed / application-derived
```

They are independent.

Stable user-owned composition cannot be silently rearranged/removed by adaptive logic.

No free-coordinate dashboard system is selected by default. Prefer CSS Grid/Flex/container queries and discrete presentation profiles until real customization proves otherwise.

## 11. Module / renderer registry

A finite registry maps validated projection kind to approved renderer.

Required behavior:

- deterministic registration/order where needed;
- duplicate kind fails fast;
- unknown kind fails locally/safely;
- renderer owns inner presentation, parent owns outer placement;
- local error boundary around independently failing renderer/surface;
- no remote executable plugin loading;
- no LLM-generated JSX/HTML/JS.

`ModuleKind` does not encode Domain or World semantics.

## 12. DANTE integration boundary

World Focus does not build a parallel AI architecture.

Conceptual path:

```text
World identity/relevance
+ interaction cursor
+ actual user purpose
        ↓
authoritative Context Builder
recipient / sensitivity / disclosure / freshness
        ↓
authorized minimized context
        ↓
DANTE Intelligence runtime
        ↓
typed answer / Insight / Proposal / governed operation result
        ↓
registered World presentation
```

World Focus may provide contextual coordinates and render results. Intelligence owns provider routing, durable runtime, tools/effects, governance and audit.

DANTE may broaden beyond the current World only when the user's actual purpose requires authorized broader context.

## 13. DANTE presentation semantics

Already accepted:

```text
P0 QUIET
P1 INVOKE
P2 CONTEXTUAL ENTRY
P3 INSIGHT
P4 PROPOSAL
P5 ACTION / RECEIPT
```

Keep source-backed facts distinct from DANTE explanation/Insight/candidate/recommendation/Proposal/effect receipt.

The platform does not yet freeze whether these appear inline, sidecar, dock, overlay, full-surface or another combination. That geometry is the current next gate.

Critical non-collapse:

```text
Home AI surface != World contextual DANTE surface
```

## 14. Coherent basis / freshness

Important visible projections and contextual results must carry enough identity/freshness semantics to avoid answering against an unrelated basis.

As applicable:

```text
request/projection generation
basis/material-state reference
as-of/freshness
source/provider freshness
```

DANTE may reuse a compatible basis or re-read/revalidate.

If refreshed reality materially differs, the result must make the changed basis truthful.

## 15. Interaction depth / presentation surface

Semantic depth and concrete surface are separate.

Current finite depth vocabulary may include:

```text
peek
insight
explore
```

Presentation may include as justified:

```text
inline
popover
sidecar
modal
full-screen
route
```

Do not hard-wire “Insight = modal” or “Explore = route” as universal rules.

Avoid nested modal chains.

## 16. Personalization boundary

Future customization is explicit:

```text
View
-> Customize Draft
-> Apply / Cancel
```

Removing a module changes presentation configuration only.

Future persistence must define version/revision/migration/concurrency semantics; do not assume silent last-write-wins.

AI-suggested stable configuration remains a proposal until accepted under product policy.

## 17. Error isolation

Layered ownership:

```text
route/page failure
-> safe route error

read/projection failure
-> local resource state

renderer / Insight failure
-> local render boundary

AI/provider failure
-> local DANTE degradation
```

A single failure must not crash the whole World.

Raw internal errors are not dumped into user-visible fallback copy.

## 18. Safe content / external links

Default policy:

```text
text is text
internal navigation uses router
external URLs are untrusted
no arbitrary HTML/JSX/JavaScript
no arbitrary iframe/embed
no credential-bearing clickable URLs
```

B0 safe-link policy allows only supported absolute credential-free HTTPS external URLs.

Rich HTML is not admitted without an explicitly defined grammar + sanitizer/rendering policy.

## 19. Responsive architecture

World Focus consumes the frozen single macro shell/rectangular workspace.

Features should adapt to allocated space using CSS layout/container queries where appropriate.

The 720px structural tuning boundary does not authorize a different undocumented product surface.

The current DANTE spatial gate must explicitly define how contextual DANTE and dynamic content coexist across large desktop, laptop, narrow/tablet and mobile.

## 20. Accessibility

Target WCAG 2.2 AA.

Per vertical review:

- keyboard/focus ownership/restoration;
- semantic roles/names/states;
- screen-reader reading order;
- reduced motion;
- zoom/text expansion;
- pointer/touch target quality;
- non-color-only communication;
- non-drag alternatives where applicable;
- chart/data alternatives where visual-only output is insufficient.

Automated axe complements rather than replaces manual critical-path review.

## 21. Performance / observability

Permanent expectations:

- route/shell small;
- critical projections first;
- no all-life-data load;
- no request-per-widget pattern;
- heavy specialist code lazy where justified;
- bounded/paginated/downsampled large data;
- isolate rerenders;
- clean listeners/observers/RAF;
- no uncontrolled layout thrash;
- ornamental VFX degrades before interaction quality.

B0 currently exposes vendor-neutral timing for:

```text
dante.world-focus.open-to-usable
```

Instrumentation failure is non-authoritative/non-blocking and remains separate from audit.

The DANTE spatial gate must later profile conversation expansion/reflow against real content density before performance budgets are frozen.

## 22. Security / privacy / disclosure

Each vertical asks:

```text
what crosses browser boundary?
what is untrusted/sensitive?
what is hidden vs authorized?
can aggregate/explanation leak concealed facts?
what is logged?
what persists locally?
what needs authoritative revalidation?
```

World relevance does not expand permissions.

Multi-actor projection/context must be disclosure-safe before presentation.

No sensitive uncontrolled localStorage.

## 23. Time / locale / units

Use existing packages:

```text
@dante/i18n
@dante/time
@dante/design-tokens
```

Do not use translated labels as stable IDs.

Preserve semantic time/number/unit/currency meaning until presentation formatting.

## 24. Dependencies / architecture restraint

B0 deliberately did not add, absent proven need:

```text
XState
Redux/Zustand/Jotai
TanStack Query
react-grid-layout
schema library lock-in
react-error-boundary
React Compiler transform
feature-flag vendor
observability vendor
sanitizer
runtime plugin loader
generic event bus
generic DI/service locator
```

Re-evaluate only against a concrete proven problem.

## 25. Backend stop line

Before the final backend vertical, World Focus may not introduce/fake:

- real business API;
- DB/Alembic World persistence;
- provider SDK/state as canonical truth;
- real LLM routing/streaming;
- durable Run/Task backend;
- tool/effect execution;
- cross-device config sync claims.

The final backend integration should replace local adapters, not force a product/platform rewrite.

## 26. Current next platform gate

No new content vertical starts now.

Immediate gate:

> **World contextual DANTE presence / spatial interaction contract**

It consumes all semantic/context rules above and decides only the still-open presentation/layout behavior required before more dynamic content is composed.
