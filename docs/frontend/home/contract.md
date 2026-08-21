# DANTE — Home Contract

**Status:** current pre-production behavior contract  
**Current working B2 baseline:** B2 Central Stage v22 no persistent add  
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

Current prototype contains Create, Home / Mondi / Oggi navigation, Search, legacy Review Queue, secondary launcher and profile/settings menu. Several controls remain mock/prototype interactions; their presence does not imply production routing, persistence or backend services.

The legacy topbar Review Queue is **deprecated** because B1 establishes Resolution as the preferred unresolved-matter concept. Visible LifeOS-era product strings/lockup are transitional historical UI and are scheduled for the dedicated DANTE branding pass.

## 4. Conversational surface

Natural language is a global interaction layer over the same DANTE reality, not a separate semantic product. Current Home keeps a first-class structured GUI. AI availability must not be required to understand the operational core.

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

## 6. Central stage — current B2 v22 working contract

The current user-reviewed B2 working oracle is v22 no persistent add. B2 is still open for product identity/skin and final QA; v22 closes the Home-stage add/configuration model.

### 6.1 Shared workspace

```text
home.stage owns outer geometry
mode selector/navigation anchors belong to home.stage
continuity/signals own only inner layout
mode switch must not alter stage outer bounds
AI expanded/collapsed reflow belongs to Home shell
```

Changing `Mondi ↔ Segnali` changes the projection inside the stage, not the surrounding shell. AI expanded/collapsed may intentionally reflow/resize the stage exactly as the Home shell dictates; projections adapt to the resulting real stage geometry rather than override shell behavior.

### 6.2 Home-stage responsibility

The Home central stage is a **read / navigate / open** projection. It is not the place where the user performs persistent configuration CRUD.

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

### 6.3 Mondi / continuity

Technical ID: `home.stage.continuity`  
Visible name: `Mondi` (`Worlds` in English)

Role: significant realities the user wants readily recoverable, resumable or explorable over time.

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

Role: compact observations worth understanding at a glance: values, deltas, trends, planned-vs-actual, target progress, trajectories and cautious patterns where semantically justified.

Rules:

- no universal Life Score;
- no arbitrary productivity/health/happiness scores;
- no invented percentages without valid semantics/evidence;
- correlation must not be presented as causation;
- different signals may use different micro-visual grammars;
- current desktop composition renders at most three complete visible Signal items;
- Signal navigation/selection/drag uses the same interaction grammar as continuity;
- Signal track remains an inner-stage concern and must not redefine stage outer geometry;
- no persistent add/configure affordance is part of Home;
- Signal selection/configuration/order/removal belongs to the dedicated Signals management surface;
- Home may expose an empty-state management entry only when no real Signals are available.

### 6.5 Management handoff

The Home stage may emit `OPEN_MANAGEMENT`: “open the management surface for the active projection”. It does **not** mean `CREATE_NOW`.

The old working event `ADD_REQUEST` is superseded and is not part of contract v0.2.0. Exact routes/sheets/pages/backend endpoints for Mondi and Signals management are deliberately not invented here.

### 6.6 Current responsive hardening

v22 inherits the responsive geometry hardening established in v21 while removing the ghost/add-slot layer.

- stage rendering follows real physical stage geometry;
- `ResizeObserver` may be used where JS measurement is genuinely required;
- ordinary layout adaptation remains owned by CSS/container/layout contracts where possible;
- Continuity spacing may adapt to actual stage width to preserve the five-item target when enough real items exist;
- partial Continuity does not synthesize items merely to fill visual capacity;
- Signals remains centered inside its own inner track;
- projection-specific outer-geometry patches are forbidden;
- no persistent add control participates in stage geometry.

A fresh automated browser PASS for all 24 matrix combinations is **not** claimed; the machine-readable matrix remains the target for final automated verification.

### 6.7 Machine-readable authority

Contract version: **`0.2.0`**

- `prototypes/frontend/shared/contracts/home-stage.contract.json`;
- `prototypes/frontend/shared/contracts/home-stage.view-model.schema.json`;
- `prototypes/frontend/shared/contracts/home-responsive.matrix.json`;
- `prototypes/frontend/shared/fixtures/home-stage.v0.json`.

These are frontend view contracts, **not** Domain/DTO/database contracts.

## 7. Timeline

The current timeline preserves the mature temporal behavior lineage: continuous 24h day, contextual initial positioning, nonlinear density, overlap lanes, zoom with semantic anchor, visibility filters, grouped expansion with common time, cluster-based margins, event focus/subtasks, anchored precise time editing, drag/move with snap/cross-day/undo, calendar/date navigation, return-to-now and environmental/day route.

B2/B2.5 do not alter these semantics.

## 8. Context Rail — B1 accepted contract

`home.contextRail` is one integrated secondary surface adjacent to the timeline and supports:

```text
USER -> DANTE     Capture
DANTE -> USER     Resolution
```

It is intentionally subordinate to the timeline, stretches with the timeline column, yields/disappears with timeline expansion and does not add an extra floating toolbar.

### Capture

Technical ID: `home.contextRail.capture`. Low-friction unclassified capture: free text, voice/attachment affordances, submit, recent trace and `Registro completo`. It must not become a generic notes app, taxonomic form, second AI transcript or infinite feed.

### Resolution

Technical ID: `home.contextRail.resolution`. Matters whose semantic state materially benefits from user decision, confirmation, correction or deeper inspection. It must not become notifications, generic alerts/reminders, normal upcoming events, `Per te`, `In evidenza`, metrics or every unknown in the model.

Complex resolution escalates to the future controlled overlay/sheet/contextual-surface grammar. The rejected B1 focus/expand chevrons remain rejected; accepted B1 keeps both functions visible.

## 9. Responsive/cross-platform qualification

Current desktop rail is part of the web prototype. Narrower representation may differ, but Capture/Resolution semantics remain cross-platform.

For Home central-stage desktop work, the engineering guard matrix spans widths 1856/1600/1366/1200/1024/901 × AI expanded/collapsed × both stage modes. v22 inherits the v21 user-reviewed responsive baseline and adds no-persistent-add/partial-real-items semantics. Final automated matrix execution remains required before full closure.

## 10. Frontend/backend pre-production boundary

```text
frontend view model != backend DTO != Domain model != persistence row
Home projection query != management mutation
```

Prototype fixtures are synthetic. Components must not invent endpoint paths, consume ORM/database shapes or make ad-hoc direct HTTP calls. Real backend integration uses explicit adapters, runtime validation, stable identities, stale/error/concurrency behavior and backend-authoritative AuthZ.

The empty-state `OPEN_MANAGEMENT` intent transfers the user to the appropriate management feature. Creation/configuration commands belong there; Home stage itself does not issue a direct create mutation.

See `docs/frontend/production-readiness/backend-integration-contract.md`.

## 11. Pre-production quality contract

A visual render at one width is not sufficient evidence. Apply applicable contract/static, component/state, responsive geometry, visual regression, accessibility, backend/client integration, performance and security/supply-chain gates.

`tests/prototypes/frontend-preprod-contracts.py` is the initial framework-neutral contract-drift guard, not a replacement for later production lint/type/component/E2E/visual/accessibility tooling.

## 12. Current B2 open decisions

The add/configuration model is decided by v22.

Before B2 closure:

1. align logo/visible product naming to DANTE;
2. review overall palette/skin;
3. review Home background/atmosphere;
4. rerun applicable final QA after those changes.

## 13. Documentation rule

Every Home change updates applicable UI registry, contract, terminology/localization, tokens, change log, checkpoint/QA and production-readiness contract/fixture/test evidence.
