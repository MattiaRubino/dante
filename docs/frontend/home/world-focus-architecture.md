# DANTE — World Focus Architecture

**Status:** CURRENT SUPPORTING ARCHITECTURE — PRE-BACKEND — WORKSPACE PLATFORM CLOSED / D2 NEXT  
**Date:** 2026-09-01  
**Branch:** `feature/home-react`

This document describes the current supporting system architecture of World Focus. Product semantics are governed by `world-focus-product-contract.md`; platform ownership by `world-focus-platform-contract.md`; route/workspace/geometry by the structural and geometry contracts; live sequencing by `world-focus-current-checkpoint.md` and the roadmap.

It does not carry independent roadmap authority.

## 1. Architecture thesis

World Focus is a reusable application surface for one user-recognizable continuity context.

It is not a dashboard engine, chatbot page or new ontology.

Conceptually:

```text
WORLD FOCUS ROUTE / SHELL
route / lifecycle / entry / return / route failure boundary
        │
        ├──────────────────────────────────────────────┐
        ▼                                              ▼
RECTANGULAR WORLD WORKSPACE                    ROUTE-OWNED DEEP LAYER
orientation + composition                      constrained/mobile/deep focus
        │                                              │
        ├──────────────────────┐                       │
        ▼                      ▼                       │
DYNAMIC WORLD COMPOSITION   CONTEXTUAL DANTE           │
question-driven projections quiet invoke / composer    │
stable+adaptive+ephemeral   sidecar where viable       │
        │                      │                       │
        └──────────┬───────────┴───────────────────────┘
                   ▼
          APPLICATION BOUNDARIES
          typed intents / projections
          validation / freshness / races
                   │
                   ▼
       LOCAL DETERMINISTIC ADAPTER [NOW]
       REAL BACKEND ADAPTER         [LATER]
```

The Workspace Platform controls ordinary composition and workspace-local transient surfaces. D2 is responsible for the narrow route-owned focus-overlay seam required when ongoing DANTE conversation needs more space than the frozen World workspace can provide.

## 2. Permanent semantic boundaries

```text
World != canonical Domain owner
World relevance != canonical membership
World relevance != authorization
World projection != canonical truth
World composition != DANTE context universe
UI model != backend DTO != Domain != persistence row
AI output != fact
AI proposal != Decision
Decision != effect
provider state != canonical state
planned != actual
absence != false
UI hiding != authorization
presentation geometry != conversation identity
selected reference != authorization
DOM != DANTE context payload
```

The same canonical reality may appear in multiple Worlds without source duplication.

## 3. Route and shell ownership

World Focus is a dedicated route below shared AppShell/Global Topbar:

```text
APP SHELL / GLOBAL TOPBAR
└ route outlet
   └ /worlds/:worldId
      └ WORLD FOCUS SHELL
         ├ visual frame
         ├ rectangular workspace
         ├ shell controls
         └ route-owned deep/focus layer [D2+ when active]
```

AppShell/Topbar are not owned by World Focus. Home is not the visible background. World Focus must remain usable without ornamental VFX.

The route-owned deep layer may cover the World experience when a real vertical requires focus/depth, but it must not resize or re-own the Global Topbar and must not silently rewrite frozen WF-G3 workspace geometry.

Exact frozen geometry lives in `world-focus-structural-contract.md` and `world-focus-geometry-contract.md`.

## 4. World context model

WR2 established four distinct layers:

```text
1. WORLD IDENTITY / PURPOSE
2. STABLE WORLD RELEVANCE DEFINITION
3. CURRENT INTERACTION CURSOR / SESSION WHEN NEEDED
4. AUTHORIZED PURPOSE-SCOPED DANTE CONTEXT
```

### World identity

Presentation identity only: reference, user-recognizable name, concise purpose, theme/presentation profile where applicable.

### Stable relevance

Typed application/presentation configuration describing what kinds of authoritative DANTE reality are intentionally relevant to this context.

It is not generic ownership, SQL, ACL or a universal relation table.

### Interaction cursor/session

Introduced only when a real interaction requires transient cross-step ownership, such as selection, Explore, Insight or contextual conversation.

The active World itself is route-owned. Do not recreate a Session object merely to mirror route state.

The mounted Workspace Platform cursor carries bounded refs/generation only. DOM focus references are kept separately by concrete UI owners such as D1's DANTE entry provider.

### Authorized DANTE context

Built by authoritative Context Builder/application logic from World context + actual request + actor/recipient + disclosure/governance + freshness/material basis.

Frontend does not decide authorization by showing/hiding UI.

D1's global quiet invoke intentionally passes `contextReference:null`; explicit deictic reference binding is D4 scope.

## 5. Dynamic composition architecture

World Focus is question-driven.

```text
bounded authorized projections
-> classify which World questions have useful answers
-> rank current value
-> compose restrained surface
```

Output families include Orientation, Situation, Continuity, Attention, Next, Change, optional Trajectory, Evidence, Explore, Act/Decide and Intelligence.

They are not mandatory page regions.

### Composition axes

Current shared primitives distinguish:

```text
stability: stable / adaptive / ephemeral
origin: system-default / user / dante-proposed / application-derived
prominence: lead / primary / supporting
footprint: wide / standard / compact
```

Stable user-owned composition remains predictable. Adaptive content is bounded and cannot silently rewrite/remove stable user content. Ephemeral Insight/query output is temporary unless deliberately promoted under an accepted configuration workflow.

The logical composition planner uses a bounded 12-unit contract, but physical rendering may collapse/adapt at narrow main-container widths. Logical grid meaning does not require pathological 12 physical tracks everywhere.

## 6. Renderer/module architecture

A renderer/module is a controlled presentation implementation for one validated projection shape.

Permanent rules:

```text
module kind != Domain owner
module kind != World question
module config != source data
module projection != source data
```

Use a finite registry of approved renderers. Unknown kinds fail locally/safely. No remote executable plugin, arbitrary JSX/HTML or LLM-generated component code.

Specialist renderers are allowed when generic rendering would materially damage semantics or UX; do not create a universal mega-widget with dozens of optional fields.

The same rule applies to transient/deeper surface renderers through the finite surface registry.

## 7. Application/projection boundary

World UI talks to intent-specific application boundaries, not generic repositories.

Current pattern:

```text
UI
-> typed application reader/intent
-> runtime boundary validation
-> deterministic local adapter [pre-backend]
```

Future:

```text
same UI/application contract
-> generated/real backend adapter
```

Do not invent endpoint, ORM or persistence shapes during frontend phase.

B2 Continuity is the first real projection example. D3 will later add a deterministic presentation-independent conversation adapter without pretending to be the real Intelligence backend.

## 8. Async / concurrency

B0 provides latest-read coordination and cancellation semantics.

Required invariant:

```text
request A starts
user changes World/context
request B supersedes A
-> A can never commit into active context
```

Workspace Platform additionally supports `expectedGeneration` for stale transient presentation intents.

Frontend read/presentation lifetime is not future durable DANTE runtime/effect lifetime.

A future DANTE Run remains bound to its initiating World/cursor generation even if the user navigates elsewhere; mounted React state alone must not become durable Run authority.

## 9. Workspace Platform architecture

The engineering-closed Workspace Platform now materializes the shared orchestration layer previously described abstractly.

Final platform evidence:

```text
HEAD 6c441335a75bb913af8da1eda569d8094d38a539
CI   33549465793 — PASS
```

Core model:

```text
COMPOSITION
stable / adaptive / ephemeral
lead / primary / supporting
finite approved renderers

WORKSPACE STATE
world id
generation
selected bounded reference
finite surface descriptors

PHYSICAL ALLOCATION
mainAllocation: full | split
topLayer: none | overlay | focus
interaction: interactive | inert
```

The axes are deliberately separate so states such as a split sidecar under a confirmation modal do not require a combinatorial synthetic mode.

Allocation uses actual measured workspace width via `ResizeObserver`. Reusable modules query the actual allocated `world-focus-main` container rather than global viewport/full workspace width.

Wide sidecars consume real main width. Sidecars fall back to non-modal overlay when split minima cannot be preserved. Blocking modal/full-focus states make main and visible underlying sidecar inert. Older competing surfaces become dormant.

A blocking-tail barrier prevents newer non-blocking surfaces from jumping above an authoritative blocking surface.

Automated stress includes 500 deterministic composition scenarios and 500 deterministic workspace-width/surface-stack scenarios.

## 10. DANTE architecture inside World Focus

DANTE is native to the World experience but is not a second AI runtime and is not the Home AI surface copied into another route.

World Focus supplies bounded contextual coordinates and presentation interaction. The broader DANTE Intelligence Platform later owns context reconstruction, routing, governance, durable runtime, tools/effects and audit.

Accepted semantic depths:

```text
P0 QUIET
P1 INVOKE
P2 CONTEXTUAL ENTRY
P3 INSIGHT
P4 PROPOSAL
P5 ACTION / RECEIPT
```

Do not collapse fact, answer, Insight, candidate, recommendation, Proposal and effect receipt into one generic `AI response` state.

### Accepted D0 spatial direction

D0 reverse engineering compared current Google Workspace/Gemini, Microsoft 365/Copilot, VS Code/Copilot Chat, Notion Agent and Linear Agent patterns.

Accepted synthesis:

> **AI availability is persistent; AI footprint is not.**

Spatial ladder:

```text
quiet invoke
-> compact non-modal composer
-> wide ongoing conversation sidecar
-> constrained/mobile route-owned focus overlay
-> explicit maximize/restore
-> explicit bounded contextual/deictic invocation
```

### D1 implemented state

D1 has implemented the quiet invoke + compact composer:

```text
no auto-open
popover / non-modal
World remains interactive
textarea autofocus
close/Escape focus restoration
truthful unavailable behavior
draft preservation
no fake answer/Run/tool/effect
global contextReference=null
```

D1 also corrected non-modal popover wrappers so they are pointer-transparent outside the actual panel.

D1 code evidence:

```text
HEAD f17291de32e6bdced20536807b32928ec1be6aea
CI   33552437179 — PASS
```

## 11. D2 active architectural problem — sidecar vs route-owned focus

D2 is the active next slice.

The same logical ongoing conversation must remain presentation-independent while geometry changes:

```text
wide workspace
-> internal split sidecar

constrained/mobile
-> route-owned focus overlay below Global Topbar

explicit deep work
-> maximize sidecar -> focus overlay

restore
-> same logical conversation
```

Critical distinction:

The Workspace Platform's `full-screen` slot is workspace-local. At 390px viewport the frozen World workspace may be only ~238px wide, so this cannot be the final mobile conversation container.

D2 must establish a narrow route-owned overlay seam that covers World content while using route width below Global Topbar, without modifying AppShell ownership or WF-G3 macro geometry.

Presentation geometry must not become conversation identity or backend schema.

D2 must not pull D3 forward: no fake transcript, model calls, provider runtime, streaming or durable conversation backend.

## 12. Insight / Explore

Insight and Explore are controlled presentation depths over validated application results.

They may use inline, sidecar, modal, focus or route presentation depending on the real vertical. Presentation surface and semantic depth remain separate axes.

No nested arbitrary modal chain and no AI-generated executable UI.

Conversation is not automatically Insight. D5 will prove the concrete separation.

## 13. Proposal / governed operation presentation

P4/P5 must remain distinct from generic assistant text.

Permanent grammar:

```text
assistant suggestion != Proposal automatically
Proposal != Decision
Decision != effect
tool call != authorization
provider success != canonical completion
runtime completion != Actual automatically
```

D6 will integrate controlled confirmation/receipt presentation with existing blocking/Escape infrastructure, still without real backend effect execution.

## 14. Personalization

Future stable customization should use deliberate draft/apply rather than accidental live persistence:

```text
View
-> Customize Draft
-> Apply / Cancel
```

Removing a module changes presentation config, not canonical reality.

Future cross-device persistence must define revision/concurrency/migration semantics; silent last-write-wins is not assumed.

## 15. Failure isolation

Layered boundaries:

```text
route/shell failure
-> route-level safe error

projection/read failure
-> local truthful state

renderer/surface failure
-> local render boundary

AI/provider failure
-> DANTE-local degradation
```

One module/provider/AI failure must not collapse the whole World.

`empty`, `partial`, `stale`, `error` and `unavailable` remain semantically distinct.

D1 proves that unavailable AI entry/submit does not erase the draft or make the World unusable.

## 16. Responsive architecture

The frozen shell has one macro structure across current web widths. Inner features adapt to **allocated container space** using CSS Grid/Flex/container queries.

Do not duplicate viewport breakpoints in JavaScript when a feature only needs its own allocation.

D2 is the explicit exception where route-level available space matters for the route-owned focus surface; even there, geometry policy must remain separate from conversation semantics and should avoid duplicated breakpoint truth.

Pressure widths include desktop, laptop, threshold boundaries, ~720 constrained layouts and 390 mobile.

## 17. Accessibility

Target WCAG 2.2 AA.

Every vertical considers:

- keyboard/focus ownership/restoration;
- screen-reader roles/names/states/read order;
- non-color-only state;
- reduced motion;
- zoom/text pressure;
- >=44px primary touch targets where applicable;
- non-drag alternatives if customization later uses drag;
- chart/data alternatives where needed.

Ordinary sidecar conversation must not be called modal or focus-trapped. A future route-owned blocking/focus surface may use modal/focus-owned semantics only if outside interaction is actually inert and focus behavior matches.

## 18. Performance

Permanent expectations:

- no all-life-data load to open a World;
- no request-per-widget architecture;
- bounded critical projections;
- heavy specialist code lazy where justified;
- history/series bounded/paginated/downsampled;
- module rerenders isolated;
- no uncontrolled layout thrash;
- listeners/RAF/observers cleaned up;
- VFX degrades before compromising interaction latency;
- DANTE sidecar/focus presentation changes must avoid pathological remount/reflow and be profiled as D2-D3 mature.

## 19. Security / privacy / disclosure

- untrusted text remains text;
- external URLs fail closed unless allowed by safe link policy;
- no arbitrary iframe/HTML/JS;
- no secrets/tokens in frontend logs;
- no sensitive uncontrolled localStorage;
- frontend visibility is not authority;
- multi-actor projection must be disclosure-safe before React/DANTE presentation;
- selected references are pointers/context coordinates, not retrieval permission.

## 20. Backend stop line

Pre-backend World Focus may build real frontend behavior, typed intents, deterministic adapters and validation seams.

It may not build/fake:

- World persistence tables/Alembic;
- business endpoints;
- provider state as canonical truth;
- real LLM/provider streaming;
- durable Run/Task backend;
- tool/effect execution;
- fake successful assistant/provider effects.

The final backend vertical should plug into these boundaries rather than rewrite the product surface.

## 21. Current next architectural question

The old question `How should DANTE occupy the World?` is closed by D0/D1.

The current active architectural question is narrower:

> **How should D2 preserve one logical ongoing conversation across wide workspace sidecar and constrained/mobile route-owned focus presentation, with explicit maximize/restore, correct focus/Escape ownership and no backend/message semantics pulled forward?**

That is the next slice. Do not reopen the entire World/DANTE architecture unless new implementation evidence materially falsifies an accepted contract.
