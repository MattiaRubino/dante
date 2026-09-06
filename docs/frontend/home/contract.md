# DANTE — Home Contract

**Status:** current pre-production behavior contract — legacy Global Topbar Review cleanup aligned 2026-09-02  
**Current working B2 baseline:** B2 Home Shell + Timeline Quick Add v25 over B2 Home Visual Skin v24 over B2 Home Branding v23 over B2 Central Stage v22  
**Last formally closed Home milestone:** B1 Context Rail v1  
**Branch:** `feature/home-react`

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

B2 v25 treats the topbar as a real application bar rather than a floating card.

Current accepted arrangement:

```text
LEFT                         CENTER                    RIGHT
DANTE + Cerca                Home / Mondi / Oggi       Crea / launcher / account
```

Shell rules:

- sticky at the top of the viewport;
- edge-to-edge at shell level with 24 px internal horizontal inset;
- Search lives immediately after DANTE on the left;
- primary Home / Mondi / Oggi navigation remains centered;
- `Crea` is the first control in the right utility group;
- launcher and account follow it;
- existing Search/Create controls are moved/reused rather than duplicated;
- the working reviewed shell suppresses the outer Home-stage vertical side frame that previously strengthened a nested-panel reading.

Current prototype controls remain:

- Crea;
- Home / Mondi / Oggi nav controls;
- Search;
- secondary launcher;
- profile/settings menu.

Important: several topbar controls are mock/prototype interactions. Their presence does not imply production routing, persistence or backend services.

The former legacy topbar Review Queue was already deprecated because B1 establishes Resolution as the preferred unresolved-matter concept. A bounded AppShell/Home cleanup on 2026-09-02 removed the disabled global Review button, hard-coded badge, dedicated icon/CSS and localization. No replacement global Review workflow was invented, and Context Rail Resolution remains separately owned inside Home.

The DANTE identity-anchor treatment is governed by B2 branding v23. Historical `LifeOS` strings may still exist inside untouched prototype-only/deprecated controls; v23-v25 do not authorize a blind global rename.

## 4. Conversational surface

Natural language is a global interaction layer over the same DANTE reality, not a separate semantic product.

Current Home keeps a first-class structured GUI. AI availability must not be required to understand the operational core.

B2 branding v23 uses the approved DANTE symbol-only identity on the AI surface; later v24/v25 work does not reopen that identity decision.

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

## 6. Central stage — retained B2 v22 working contract

The current central-stage behavior oracle remains v22 no persistent add. Later v23 identity, v24 visual skin and v25 shell/timeline work do not reopen the Home-stage add/configuration model.

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

### 6.2 Home-stage responsibility

The Home central stage is a **read / navigate / open** projection.

It is not the place where the user performs persistent configuration CRUD.

Permanent rules:

```text
NO persistent +
NO ghost add slots
NO placeholder World/Signal entities
NO direct creation mutation from Home stage
```

State rules:

```text
PARTIAL
show only real items

FULL / OVERFLOW
normal projection navigation

EMPTY
may show a contextual CTA
CTA opens the dedicated management/creation surface
CTA does not create directly inside Home
```

This is a product and architecture rule, not merely a visual preference.

The B2 v25 timeline `+` does **not** violate this rule: it belongs to the temporal projection, not to Mondi/Segnali capacity or configuration.

### 6.3 Mondi / continuity

Technical ID: `home.stage.continuity`  
Visible name: `Mondi` (`Worlds` in English)

Role:

> Significant realities the user wants readily recoverable, resumable or explorable over time.

Rules:

- not a Domain Model taxonomy;
- not necessarily a persisted `World` entity;
- current visual grammar preserves the established sphere carousel;
- desktop target remains five visible **real** items where enough items exist;
- selection/previous/next/drag continue the existing interaction lineage;
- partial state renders only the Mondi that actually exist;
- empty visual capacity is not represented as fake spheres or `+` items;
- creation/edit/order/archive/removal belongs to the dedicated Mondi management surface;
- Home may expose an empty-state management entry only when no real Mondi are available.

### 6.4 Segnali / signals

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
- no persistent add/configure affordance is part of Home central stage;
- Signal selection/configuration/order/removal belongs to the dedicated Signals management surface;
- Home may expose an empty-state management entry only when no real Signals are available.

### 6.5 Management handoff

The Home stage may emit the semantic intent:

```text
OPEN_MANAGEMENT
```

That intent means “open the management surface for the active projection”. It does **not** mean `CREATE_NOW`.

The old working event `ADD_REQUEST` is superseded by this boundary and is not part of contract v0.2.0.

The exact routes/sheets/pages/backend endpoints for Mondi and Signals management are deliberately not invented here. They belong to the later dedicated surface/API implementation scope.

### 6.6 Current responsive hardening

v22 inherits the responsive geometry hardening established in v21 while removing the ghost/add-slot layer.

Current direction:

- stage rendering follows real physical stage geometry;
- `ResizeObserver` may be used where a JS measurement is genuinely required;
- ordinary layout adaptation should remain owned by CSS/container/layout contracts where possible;
- Continuity spacing may adapt to the actual stage width to preserve the five-item target when enough real items exist;
- partial Continuity does not synthesize items merely to fill the five-position capacity;
- Signals remains centered inside its own inner track;
- projection-specific outer-geometry patches are forbidden;
- no persistent add control participates in stage geometry.

The v25 shell changes must still pass the same final responsive matrix before B2 closure. A fresh automated browser PASS for all 24 B2.5 matrix combinations is **not** claimed by this checkpoint.

### 6.7 Machine-readable authority

Contract version: **`0.2.0`**

- `prototypes/frontend/shared/contracts/home-stage.contract.json`;
- `prototypes/frontend/shared/contracts/home-stage.view-model.schema.json`;
- `prototypes/frontend/shared/contracts/home-responsive.matrix.json`;
- `prototypes/frontend/shared/fixtures/home-stage.v0.json`.

These are frontend view contracts, **not** Domain/DTO/database contracts. They do not create backend endpoints, persistence entities or authorization semantics.

## 7. Timeline

The timeline preserves the mature temporal behavior lineage:

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

### 7.1 B2 v25 temporal-header quick add

B2 v25 extends the temporal-header grid from:

```text
month / now / week / actions
```

to:

```text
add / month / now / week / actions
```

Technical ID: `home.timeline.quickAdd`  
Visible label: `+`

Current prototype contract:

- the control is a real button in the timeline component markup;
- it owns a dedicated first grid column;
- month/year and `Ora` move right as part of the same grid rather than via independent floating offsets;
- it visually uses the accepted v24 charcoal/orange language;
- its current prototype click bridges to the existing global `Crea` popover.

The click bridge is **not** a final product/backend contract. Still open:

- whether the final quick-add flow creates an event, task/commitment or another temporal object;
- how viewed day/current time are prefilled;
- whether a specific timeline coordinate preselects an exact time;
- final route/sheet/popover ownership;
- command, validation, persistence, authorization and backend endpoint semantics.

Until that later contract exists, `home.timeline.quickAdd` is `PROTOTYPE_ONLY` and must not invent writes.

The v25 quick-add does not change event drag, time edit, calendar navigation, zoom, grouping or other mature timeline semantics.

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

The removal of the deprecated Global Topbar Review placeholder does not change this ownership. Resolution is not implicitly globalized by that cleanup.

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

v22 inherits the v21 user-reviewed responsive baseline; v23-v25 add identity, visual-skin and shell/header deltas over it. Final automated matrix execution remains a separate evidence requirement before full closure.

Responsive rules must be owned by the correct layout/container boundary. Projection-specific patches must not silently redefine Home-shell or stage outer geometry.

## 10. Frontend/backend pre-production boundary

For touched durable Home features:

```text
frontend view model != backend DTO != Domain model != persistence row
Home projection query != management mutation
```

Prototype fixtures are synthetic. Components must not invent endpoint paths, consume ORM/database shapes or make ad-hoc direct HTTP calls as their architectural contract.

Real backend integration will use explicit feature/data-source adapters, runtime validation at untrusted boundaries, stable identities, explicit stale/error/concurrency behavior and backend-authoritative AuthZ.

For central-stage management specifically, the empty-state `OPEN_MANAGEMENT` intent transfers the user to the appropriate management feature. Creation/configuration commands belong there; Home stage itself does not issue a direct create mutation.

For timeline quick-add specifically, v25 defines only the accepted contextual UI affordance. It does not define a production command or backend write.

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

The central-stage add/configuration model is decided by v22. DANTE identity is aligned by v23. Working palette/background are accepted by v24. The global shell placement and contextual timeline `+` placement are accepted by v25. The deprecated global Review placeholder is removed and is no longer an open decision.

Before B2 closure:

1. define the final production semantics/destination/context prefill for timeline quick-add;
2. productionize the accepted visual token layer when implementation reaches shared theme code;
3. finish remaining small shell/detail refinements;
4. rerun applicable responsive / visual / accessibility QA.

Any future global unresolved-matter entry must earn a new explicit contract; do not resurrect `Review` as a disabled placeholder or fake count.

## 13. Documentation rule

Every Home change must update:

- UI registry;
- this contract when behavior/role/state changes;
- terminology/localization when copy/names change;
- tokens when visual semantic values change;
- change log;
- current checkpoint / QA when accepted artifact changes;
- applicable production-readiness contract/fixture/test evidence from B2.5 onward.
