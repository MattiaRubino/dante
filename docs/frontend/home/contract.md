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

Current composition:

```text
GLOBAL TOPBAR
ORIENTATION / CURRENT SITUATION
AI / CONVERSATIONAL SURFACE
CENTRAL STAGE (Worlds / Stats working prototype)
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

## 6. Central stage — currently unresolved B2 scope

`Worlds` / `Stats` are working prototype modes only.

Current interaction may remain functional while B2 answers the actual user jobs. Do not canonize current mixed `Worlds` categories or generic Stats merely because they exist.

No B1 change is authorized in this region.

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

B1 does not alter these semantics.

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

## 10. Documentation rule

Every Home change must update:

- UI registry;
- this contract when behavior/role/state changes;
- terminology/localization when copy/names change;
- tokens when visual semantic values change;
- change log;
- current checkpoint / QA when accepted artifact changes.
