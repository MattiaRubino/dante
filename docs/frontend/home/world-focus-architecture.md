# DANTE — World Focus Architecture

**Status:** CURRENT SUPPORTING ARCHITECTURE — PRE-BACKEND  
**Date:** 2026-09-01  
**Branch:** `feature/home-react`

This document describes the current system architecture of World Focus. Product semantics are governed by `world-focus-product-contract.md`; platform ownership is governed by `world-focus-platform-contract.md`; route/workspace/geometry are governed by the structural and geometry contracts.

It no longer carries roadmap/status authority.

## 1. Architecture thesis

World Focus is a reusable application surface for one user-recognizable continuity context.

It is not a dashboard engine, a chatbot page or a new ontology.

Conceptually:

```text
WORLD FOCUS HOST
route / lifecycle / entry / return / failure boundary
        │
        ▼
WORLD ORIENTATION
identity / concise purpose
        │
        ├───────────────────────────────────────┐
        ▼                                       ▼
DYNAMIC WORLD COMPOSITION                CONTEXTUAL DANTE
question-driven projections              interaction / Insight / Proposal
stable + adaptive + ephemeral            governed result presentation
        │                                       │
        └───────────────┬───────────────────────┘
                        ▼
              APPLICATION BOUNDARIES
              typed intents / projections
              validation / freshness / races
                        │
                        ▼
            LOCAL DETERMINISTIC ADAPTER [NOW]
            REAL BACKEND ADAPTER         [LATER]
```

DANTE and content are peers inside the World product experience, but the exact spatial relationship is a current product gate and is not prescribed here.

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
```

The same canonical reality may appear in multiple Worlds without source duplication.

## 3. Route and shell ownership

World Focus is a dedicated route below the shared AppShell/Topbar:

```text
APP SHELL / GLOBAL TOPBAR
└ route outlet
   └ /worlds/:worldId
      └ WORLD FOCUS SHELL
         ├ visual frame
         ├ rectangular workspace
         └ shell controls
```

AppShell is not owned by World Focus. Home is not the visible background. World Focus must remain usable without ornamental VFX.

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

The active World itself is currently route-owned. Do not recreate a Session object merely to mirror route state.

### Authorized DANTE context

Built by the authoritative Context Builder/application layer from World context + actual request + actor/recipient + disclosure/governance + freshness/material basis.

The frontend does not decide authorization by hiding/showing UI.

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
```

These axes remain independent.

Stable user-owned composition must remain predictable. Adaptive content is bounded and cannot silently rewrite/remove stable user content. Ephemeral Insight/query output is temporary unless deliberately promoted under an accepted configuration workflow.

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

Do not invent endpoint, ORM or persistence shapes during the frontend phase.

B2 Continuity is the first real example of this architecture.

## 8. Async / concurrency

B0 provides latest-read coordination and cancellation semantics.

Required invariant:

```text
request A starts
user changes World/context
request B supersedes A
-> A can never commit into the active context
```

Frontend read lifetime is not future durable DANTE runtime/effect lifetime.

A DANTE run remains bound to its initiating World/cursor generation even if the user navigates elsewhere.

## 9. DANTE architecture inside World Focus

DANTE is native to the World experience but is not a second AI runtime.

World Focus supplies bounded contextual coordinates and presentation interaction. The broader DANTE Intelligence Platform owns context reconstruction, routing, governance, durable runtime, tools/effects and audit.

Already accepted presentation semantics:

```text
P0 QUIET
P1 INVOKE
P2 CONTEXTUAL ENTRY
P3 INSIGHT
P4 PROPOSAL
P5 ACTION / RECEIPT
```

Do not collapse fact, answer, Insight, candidate, recommendation, Proposal and effect receipt into one generic `AI response` state.

The exact persistent/transient spatial geometry of DANTE inside the World workspace is intentionally unresolved and is the current next reverse-engineering gate.

Critically:

```text
Home AI surface != World contextual DANTE surface
```

Shared Intelligence capability does not imply shared page geometry/component ownership.

## 10. Insight / Explore

Insight and Explore are controlled presentation depths over validated application results.

They may use inline, sidecar, modal, full-screen or route presentation depending on the real vertical. Presentation surface and semantic depth are separate axes.

No nested modal chain or arbitrary AI-generated UI.

## 11. Personalization

Future stable customization should use a deliberate draft/apply workflow rather than live accidental persistence.

```text
View
-> Customize Draft
-> Apply / Cancel
```

Removing a module changes presentation config, not canonical reality.

Future cross-device persistence must define revision/concurrency/migration semantics; silent last-write-wins is not assumed.

## 12. Failure isolation

Layered failure boundaries:

```text
route/shell failure
-> route-level safe error surface

projection/read failure
-> local truthful state

renderer/Insight failure
-> local render boundary

AI/provider failure
-> DANTE-local degradation
```

One module/provider/AI failure must not collapse the whole World.

`empty`, `partial`, `stale`, `error` and `unavailable` are semantically distinct.

## 13. Responsive architecture

The frozen shell has one macro structure across current web widths. Inner features adapt to allocated container space using CSS Grid/Flex/container queries where appropriate.

Do not duplicate viewport breakpoints in JavaScript when the feature only needs to know its own allocated width.

The immediate DANTE spatial gate must explicitly pressure large desktop, laptop, tablet/narrow and mobile before freezing its footprint.

## 14. Accessibility

Target WCAG 2.2 AA.

Every vertical considers:

- keyboard and focus ownership/restoration;
- screen-reader roles/names/states/read order;
- non-color-only state;
- reduced motion;
- zoom/text pressure;
- pointer/touch targets;
- non-drag alternatives if customization uses drag;
- visual chart/data alternatives where needed.

## 15. Performance

Permanent expectations:

- no all-life-data load to open a World;
- no request-per-widget architecture;
- bounded critical projections;
- heavy specialist code lazy where justified;
- history/series bounded/paginated/downsampled as appropriate;
- module rerenders isolated;
- no uncontrolled layout thrash;
- listeners/RAF/observers cleaned up;
- VFX degrades before it compromises interaction latency;
- DANTE expansion/conversation must be profiled against content reflow once its spatial model exists.

## 16. Security / privacy / disclosure

- untrusted text remains text;
- external URLs fail closed unless allowed by the safe link policy;
- no arbitrary iframe/HTML/JS;
- no secrets/tokens in frontend logs;
- no sensitive uncontrolled localStorage;
- frontend visibility is not authority;
- multi-actor projection must be disclosure-safe before React/DANTE presentation.

## 17. Backend stop line

Pre-backend World Focus may build real frontend behavior, typed intents, deterministic adapters and validation seams.

It may not build/fake:

- World persistence tables/Alembic;
- business endpoints;
- provider state as canonical truth;
- real LLM/provider streaming;
- durable Run/Task backend;
- tool/effect execution.

The final backend vertical should plug into these boundaries rather than rewrite the product surface.

## 18. Current next architectural question

No new content module vertical is selected until the **World contextual DANTE presence / spatial interaction contract** is reverse-engineered and user-approved.

That gate decides spatial behavior only; it consumes rather than redefines the World/DANTE semantic model already closed by WR2.
