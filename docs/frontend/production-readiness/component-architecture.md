# DANTE — Frontend Component Architecture v0

- Status: **CURRENT PRE-PRODUCTION CONTRACT**
- Production framework: not selected/frozen by this document

## 1. Architecture objective

Components own one coherent responsibility and expose explicit inputs/events. Layout ownership is singular: a child projection may arrange its internal content but may not redefine the outer geometry owned by its parent.

## 2. Home target decomposition

```text
HomeShell
├── GlobalTopbar
├── Orientation
├── AISurface
├── CentralStage
│   ├── StageModeSelector
│   ├── StageViewport
│   │   ├── ContinuityProjection   (working visible label: Mondi)
│   │   └── SignalsProjection      (working visible label: Segnali)
│   └── StageNavigation
├── TimelineSurface
└── ContextRail
```

This is a responsibility map, not authorization to create React components yet.

Dedicated management surfaces for Mondi and Segnali are **not** children of the Home stage by default. They are separate feature surfaces opened through an explicit management intent.

## 3. Geometry ownership

`HomeShell` owns composition between AI, central stage, timeline and rail.

`CentralStage` owns:

- its outer rectangle;
- mode-selector anchor;
- lateral-navigation anchors;
- viewport/clipping boundary;
- resize/container measurement contract.

`ContinuityProjection` and `SignalsProjection` own only their **inner layout**.

Forbidden:

- mode-specific edits to the stage outer bounds;
- a child positioning stage navigation relative to unrelated panels;
- global viewport patches inside a projection;
- duplicated expanded/collapsed geometry rules per mode;
- persistent add controls that participate in or redefine stage geometry.

## 4. State ownership

### Server/source-backed state

Examples: stage items, signal values, provenance, freshness, capabilities derived from authorization.

This is fetched/synchronized through a data-source adapter and cached by the production client data layer. It is not stored as arbitrary component booleans.

### Durable UI state

Examples: active stage mode, active item index per projection, user-selected view preferences when a product decision makes them persistent.

The production client must define the persistence scope explicitly: local component, URL, client preference or backend preference.

### Transient interaction state

Examples: drag delta, active pointer, settling animation, focus-visible state, open hover affordance.

Transient state is not persisted or sent to the backend.

## 5. Stage state model

Surface availability states:

```text
loading
ready
empty
partial
full
overflow
error
unavailable
```

Interaction states:

```text
idle
dragging
settling
```

These dimensions are separate. An `overflow` data state can still be `dragging`; an `error` state must not masquerade as `empty`.

For an empty projection, `activeIndex` is `null`. The client must not manufacture index `0` when there is no real item.

## 6. Home-stage responsibility and management boundary

The Home central stage is:

```text
READ
NAVIGATE
OPEN
```

It is not a configuration CRUD surface.

Permanent rules:

- no persistent `+` or add button in the normal Home-stage composition;
- partial state renders only real items;
- no ghost/capacity slots are represented as view-model items;
- no placeholder entities are created to fill visual positions;
- full/overflow remains ordinary projection navigation;
- an empty state may show a contextual CTA so the stage is not a dead end;
- that CTA opens the dedicated management/creation surface;
- creation/configuration/removal/order commands are owned by the dedicated Mondi/Signals feature surface, not `CentralStage`.

This boundary keeps `CentralStage` stable as more projections are added and prevents content rendering, management workflow and persistence concerns from collapsing into one component.

## 7. Event/intention model

The stage exposes semantic intents rather than DOM-specific callbacks:

```text
MODE_PREVIOUS
MODE_NEXT
ITEM_PREVIOUS
ITEM_NEXT
ITEM_SELECT
DRAG_START
DRAG_MOVE
DRAG_END
OPEN_MANAGEMENT
```

`OPEN_MANAGEMENT` is a navigation/feature-entry intent. It does not mean “perform create now”.

The previous working `ADD_REQUEST` event is not part of contract v0.2.0.

Production implementation may map these intents to reducers/state machines/hooks, but must retain equivalent observable behavior and test coverage.

## 8. Responsive architecture

Use parent/container geometry for component decisions. Global viewport width governs Home composition; central-stage available container width governs projection layout.

JavaScript measurement is allowed only where real geometry/math requires it and must observe the actual owner container, not duplicate CSS breakpoints in unrelated scripts.

Resize must be reversible and deterministic:

```text
state A → resize/reflow → state B → reverse resize/reflow → equivalent state A
```

The current desktop guard matrix remains six widths × AI expanded/collapsed × continuity/signals. The absence of a persistent add control is itself an invariant: management affordances must not become a new source of geometry drift.

## 9. Production migration rule

The prototype DOM structure is not a public API. Production migration preserves component responsibilities, state ownership, intents, view-model contracts, management boundaries, responsive invariants, accessibility outcomes and the accepted visual oracle. It does not preserve incidental selectors, historical CSS cascade or monolithic script layout.
