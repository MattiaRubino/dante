# DANTE — Home Contract

**Status:** current pre-production behavior contract  
**Current working B2 baseline:** B2 Central Stage v21 responsive  
**Last formally closed Home milestone:** B1 Context Rail v1  
**Branch:** `prototype/frontend`

This file tells a new chat/agent what the current Home is expected to contain and do. It is authoritative for Home behavior/intent at the prototype level; it does not create backend semantics.

## 1. Home job

Home is the recurring orientation/operation surface. It combines:

- current situation;
- conversational access;
- temporal reality;
- carried/contextual information;
- direct action;
- secondary contextual support.

It must not become a universal dashboard, ontology browser or AI-only cockpit.

## 2. Structural regions

Current composition:

```text
GLOBAL TOPBAR
ORIENTATION / CURRENT SITUATION
AI / CONVERSATIONAL SURFACE
CENTRAL STAGE
DAY / TIMELINE
RIGHT CONTEXT RAIL
```

The registry at `docs/frontend/ui-registry.md` enumerates controls and statuses.

## 3. Topbar

Current prototype contains:

- Create;
- Home / Mondi / Oggi nav controls;
- Search;
- legacy Review Queue;
- secondary launcher;
- profile/settings menu.

Important: several topbar controls are mock/prototype interactions. Their presence does not imply production routing, persistence or backend services.

The legacy topbar Review Queue is currently **deprecated** because B1 establishes Resolution as the preferred unresolved-matter concept. It remains visible only until a separate cleanup scope decides the final global access pattern.

Visible LifeOS-era product strings/lockup are transitional historical UI and are scheduled for the dedicated DANTE branding pass; their presence does not change current product identity.

## 4. Conversational surface

Natural language is a global interaction layer over the same DANTE reality, not a separate semantic product.

Current Home keeps a first-class structured GUI. AI availability must not be required to understand the operational core.

## 5. Orientation

Keep distinct:

```text
Ora / Prossimo
In evidenza
Per te
```

- `Ora / Prossimo`: current moment + immediate continuation.
- `In evidenza`: materially relevant attention item.
- `Per te`: contextual suggestion/opportunity/discovery.

Do not collapse all three into generic recommendations.

## 6. Central stage — current B2 v21 working contract

The current user-reviewed B2 working oracle is v21 responsive. B2 is still open; v21 is not a claim that all stage/product-identity decisions are closed.

### 6.1 Shared workspace

The central stage is one shared workspace with stable outer ownership:

```text
home.stage owns outer geometry
mode selector/navigation anchors belong to home.stage
continuity/signals own only inner layout
mode switch must not alter stage outer bounds
AI expanded/collapsed reflow belongs to Home shell
```

Changing `Mondi ↔ Segnali` changes the projection inside the stage, not the surrounding shell.

Changing AI expanded/collapsed may intentionally reflow/resize the stage exactly as the Home shell dictates; projections must adapt to the resulting real stage geometry rather than override that shell behavior.

### 6.2 Mondi / continuity

Technical ID: `home.stage.continuity`  
Visible name: `Mondi` (`Worlds` in English)

Role:

> Significant realities the user wants readily recoverable, resumable or explorable over time.

Rules:

- not a Domain Model taxonomy;
- not necessarily a persisted `World` entity;
- current visual grammar preserves the established sphere carousel;
- desktop target remains five visible sphere positions in the current guard matrix;
- selection/previous/next/drag continue the existing interaction lineage;
- in partial state, unused existing sphere positions may be rendered as ghost `+` slots;
- those empty slots are UI composition only and must not become placeholder backend entities;
- persistent/full-state add placement remains unresolved and must be decided separately.

### 6.3 Segnali / signals

Technical ID: `home.stage.signals`  
Visible name: `Segnali` (`Signals` in English)

Role:

> Compact observations worth understanding at a glance: values, deltas, trends, planned-vs-actual, target progress, trajectories and cautious patterns where semantically justified.

Rules:

- no universal Life Score;
- no arbitrary productivity/health/happiness scores;
- no invented percentages without valid semantics/evidence;
- correlation must not be presented as causation;
- different signals may use different micro-visual grammars;
- current desktop composition renders at most three complete visible Signal items;
- Signal navigation/selection/drag uses the same interaction grammar as continuity;
- Signal track remains an inner-stage concern and must not redefine stage outer geometry;
- persistent add/configure affordance remains unresolved.

### 6.4 Current responsive hardening

v21 repairs the previously open working defect where window/parent reflow could leave stage content using stale geometry.

Current direction:

- stage rendering follows real physical stage geometry;
- `ResizeObserver` may be used where a JS measurement is genuinely required;
- ordinary layout adaptation should remain owned by CSS/container/layout contracts where possible;
- Continuity spacing may adapt to the actual stage width to preserve the five-position target in the current desktop guard matrix;
- Signals remains centered inside its own inner track;
- projection-specific outer-geometry patches are forbidden.

The current user-reviewed v21 previews are the working visual/behavior oracle. A fresh automated browser PASS for all 24 B2.5 matrix combinations is **not** claimed by this documentation scope; the machine-readable matrix remains the target for final automated verification.

### 6.5 Machine-readable authority

- `prototypes/frontend/shared/contracts/home-stage.contract.json`;
- `prototypes/frontend/shared/contracts/home-stage.view-model.schema.json`;
- `prototypes/frontend/shared/contracts/home-responsive.matrix.json`;
- `prototypes/frontend/shared/fixtures/home-stage.v0.json`.

These are frontend view contracts, **not** Domain/DTO/database contracts. They do not create backend endpoints, persistence entities or authorization semantics.

## 7. Timeline

The current timeline preserves the mature temporal behavior lineage:

- continuous 24h day;
- contextual initial positioning;
- nonlinear density;
- overlap lanes;
- zoom with semantic anchor;
- filters that do not redefine underlying geometry semantics;
- grouped expansion while keeping time common;
- cluster-based margins;
- event focus/subtasks;
- precise anchored time picker;
- drag/move with existing snap/cross-day/undo behavior;
- calendar/date navigation;
- return-to-now;
- environmental/day route.

B2/B2.5 do not alter or authorize changes to these semantics.

## 8. Context Rail — B1 accepted contract

### 8.1 Purpose

`home.contextRail` is one integrated secondary surface adjacent to the timeline.

It supports two complementary directions:

```text
USER -> DANTE     Capture
DANTE -> USER     Resolution
```

It is intentionally subordinate to the timeline.

### 8.2 Geometry

- one outer surface, not two visually unrelated floating cards;
- stretches with the timeline column;
- does not intentionally leave a large arbitrary empty block under its content;
- yields/disappears with the existing timeline expansion behavior;
- no extra floating toolbar/control is added around it.

### 8.3 Capture

Technical ID: `home.contextRail.capture`

Job:

> Let the user tell DANTE something with minimal friction without classifying it first.

Allowed examples:

- observation;
- expense statement;
- fact;
- idea;
- intention;
- quick reminder-like input;
- Actual/report;
- attachment/voice entry when those capabilities are eventually implemented.

Current prototype content:

- free text composer;
- voice icon button;
- attachment icon button;
- submit icon button;
- small trace of recent captured entries;
- explicit `Registro completo` deeper-history affordance.

Must **not** become:

- a generic notes app;
- a taxonomic form requiring Goal/Task/Observation/etc. before capture;
- a second AI transcript;
- an infinite history feed.

### 8.4 Resolution

Technical ID: `home.contextRail.resolution`

Job:

> Surface matters whose semantic state materially benefits from a user decision, confirmation, correction or deeper inspection.

Current prototype examples:

- outcome of today's workout: `Fatto / Parziale / Saltato`;
- uncertain expense category: `Conferma / Correggi`;
- moved meeting conflict: deeper details.

Allowed:

- explicit confirmation;
- simple 2–3 option choice;
- simple correction;
- open a deeper surface;
- later/snooze only where semantics explicitly permit it.

Must **not** become:

- notifications center;
- generic alert feed;
- generic reminders;
- normal upcoming events;
- `Per te`;
- `In evidenza`;
- metrics/stats;
- every unknown in the model.

Resolution state and attention delivery remain separate.

### 8.5 Deep escalation

If resolution needs history, provenance, many fields, complex scope, comparison or significant consequences, the rail must not cram the workflow into ~306px. It escalates to the future controlled overlay/sheet/contextual-surface grammar.

### 8.6 Rejected behavior

The B1 preview briefly tested chevrons that changed the rail into hidden `balanced/capture-focus/resolution-focus` states.

**REJECTED.**

Reason:

- unclear mental model;
- expansion often added blank space rather than information;
- unnecessary hidden state;
- reduced predictability.

Accepted B1 keeps both functions simultaneously visible.

## 9. Responsive/cross-platform qualification

Current desktop rail is part of the web prototype. Existing narrower breakpoint behavior may hide the side rail. This does **not** mean Capture/Resolution are desktop-only capabilities. Mobile representation must be designed later under the cross-platform rule with the same semantics.

For Home central-stage desktop work, the engineering guard matrix is defined in `prototypes/frontend/shared/contracts/home-responsive.matrix.json` across widths 1856/1600/1366/1200/1024/901, AI expanded/collapsed and both stage modes.

The previous v16 global-resize defect is no longer the current working state: v21 is the user-reviewed responsive baseline. Final automated matrix execution remains a separate evidence requirement before full closure.

Responsive rules must be owned by the correct layout/container boundary. Projection-specific patches must not silently redefine Home-shell or stage outer geometry.

## 10. Frontend/backend pre-production boundary

For touched durable Home features:

```text
frontend view model != backend DTO != Domain model != persistence row
```

Prototype fixtures are synthetic. Components must not invent endpoint paths, consume ORM/database shapes or make ad-hoc direct HTTP calls as their architectural contract.

Real backend integration will use explicit feature/data-source adapters, runtime validation at untrusted boundaries, stable identities, explicit stale/error/concurrency behavior and backend-authoritative AuthZ.

See `docs/frontend/production-readiness/backend-integration-contract.md`.

## 11. Pre-production quality contract

A visual render at one width is not sufficient evidence.

For touched durable Home behavior, apply the applicable quality layers from `docs/frontend/production-readiness/quality-gates.md`, including:

- contract/static coherence;
- component/state behavior;
- responsive geometry matrix;
- visual regression;
- accessibility;
- backend/client integration when real APIs exist;
- performance and security/supply-chain gates at the production boundary.

`tests/prototypes/frontend-preprod-contracts.py` is the initial framework-neutral contract-drift guard. It does not replace later production lint/type/component/E2E/visual/accessibility tooling.

## 12. Current B2 open decisions

Before B2 closure:

1. decide whether/how persistent add affordances should exist for Mondi, Segnali and future stage projections;
2. align logo/visible product naming to DANTE;
3. review overall palette/skin;
4. review Home background/atmosphere;
5. rerun applicable final QA after those changes.

## 13. Documentation rule

Every Home change must update:

- UI registry;
- this contract when behavior/role/state changes;
- terminology/localization when copy/names change;
- tokens when visual semantic values change;
- change log;
- current checkpoint / QA when accepted artifact changes;
- applicable production-readiness contract/fixture/test evidence from B2.5 onward.
