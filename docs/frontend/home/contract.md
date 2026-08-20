# DANTE — Home Contract

**Status:** current pre-production behavior contract  
**Accepted build:** B1 Context Rail v1  
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

Current prototype contains Create, Home/Mondi/Oggi nav controls, Search, legacy Review Queue, secondary launcher and profile/settings menu. Several controls remain mock/prototype interactions; presence does not imply production routing, persistence or backend services.

The legacy topbar Review Queue is deprecated because B1 establishes Resolution as the preferred unresolved-matter concept. It remains visible until a separate cleanup scope decides the final global access pattern.

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

## 6. Central stage — B2 WIP + B2.5 engineering contract

The last accepted Home remains B1; B2 is not visually closed.

Current saved B2 working direction:

- two projections: continuity (`Mondi`) and signals (`Segnali`);
- continuity keeps the sphere-carousel lineage and desktop target of five visible positions;
- a partial continuity state derives empty add slots in the UI rather than persisting placeholder backend entities;
- signals uses the same navigation grammar and shows at most three complete visible items in the desktop guard matrix;
- external add placement remains unresolved.

B2.5 fixes the engineering ownership independent of final visual polish:

```text
home.stage owns outer geometry
mode selector/navigation anchors belong to home.stage
continuity/signals own only inner layout
mode switch must not alter stage outer bounds
AI expanded/collapsed reflow belongs to Home shell
```

Machine-readable authority:

- `prototypes/frontend/shared/contracts/home-stage.contract.json`
- `prototypes/frontend/shared/contracts/home-stage.view-model.schema.json`
- `prototypes/frontend/shared/contracts/home-responsive.matrix.json`
- `prototypes/frontend/shared/fixtures/home-stage.v0.json`

These are frontend view contracts, **not** Domain/DTO/database contracts.

## 7. Timeline

The current timeline preserves the mature temporal behavior lineage:

- continuous 24h day;
- contextual initial positioning;
- nonlinear density;
- overlap lanes;
- zoom with semantic anchor;
- visibility filters;
- grouped expansion with common time;
- cluster-based margins;
- event focus/subtasks;
- precise anchored time picker;
- drag/move with snap/cross-day/undo behavior;
- calendar/date navigation;
- return-to-now;
- environmental/day route.

B2/B2.5 do not authorize timeline semantic changes.

## 8. Context Rail — B1 accepted contract

### 8.1 Purpose

`home.contextRail` is one integrated secondary surface adjacent to the timeline supporting:

```text
USER -> DANTE     Capture
DANTE -> USER     Resolution
```

It is intentionally subordinate to the timeline.

### 8.2 Geometry

- one outer surface, not two unrelated cards;
- stretches with the timeline column;
- no arbitrary large lower void by design;
- yields/disappears with existing timeline expansion;
- no extra floating toolbar around it.

### 8.3 Capture

Technical ID: `home.contextRail.capture`

Job: let the user tell DANTE something with minimal friction without classifying first.

Current prototype: free-text composer, voice/attachment affordances, submit, small recent trace and `Registro completo`.

Must not become a generic notes app, taxonomic form, second AI transcript or infinite history feed.

### 8.4 Resolution

Technical ID: `home.contextRail.resolution`

Job: surface matters whose semantic state materially benefits from user decision, confirmation, correction or deeper inspection.

Current prototype examples include workout outcome, uncertain expense category and moved-meeting conflict.

Must not become notifications, generic alerts/reminders, normal upcoming events, `Per te`, `In evidenza`, metrics or every unknown in the model.

Resolution state and attention delivery remain separate.

### 8.5 Deep escalation

Complex resolution requiring history/provenance/many fields/comparison/significant consequences escalates to the future controlled overlay/sheet/contextual-surface grammar.

### 8.6 Rejected behavior

B1 focus/expand chevrons and hidden balanced/focus states are **REJECTED**: unclear mental model, unnecessary hidden state and often blank expansion. Accepted B1 keeps both functions visible.

## 9. Responsive/cross-platform qualification

Current desktop rail is part of the web prototype. Existing narrower breakpoint behavior may hide it; Capture/Resolution are not therefore desktop-only capabilities. Mobile representation must later preserve semantic outcomes.

For Home central-stage desktop work, the current engineering guard matrix is defined in `home-responsive.matrix.json` across widths 1856/1600/1366/1200/1024/901, AI expanded/collapsed and both stage modes. The known B2 global-resize defect remains open until this matrix passes on the actual artifact.

## 10. Frontend/backend pre-production boundary

For touched durable Home features:

```text
frontend view model != backend DTO != Domain model != persistence row
```

Prototype fixtures are synthetic. Components must not invent endpoint paths, consume ORM/database shapes or make ad-hoc direct HTTP calls as their architectural contract. Real backend integration will use explicit adapters/runtime validation and backend-authoritative AuthZ.

See `docs/frontend/production-readiness/backend-integration-contract.md`.

## 11. Documentation / quality rule

Every Home change updates applicable registry, contract, terminology/localization, tokens, change log and checkpoint/QA. From B2.5, touched durable behavior also updates applicable production-readiness contract/fixture/test evidence.
