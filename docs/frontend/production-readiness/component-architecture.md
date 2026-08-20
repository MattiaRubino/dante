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
- duplicated expanded/collapsed geometry rules per mode.

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

## 6. Event/intention model

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
ADD_REQUEST
```

Production implementation may map these to reducers/state machines/hooks, but must retain equivalent observable behavior and test coverage.

## 7. Responsive architecture

Use parent/container geometry for component decisions. Global viewport width governs Home composition; central-stage available container width governs projection layout.

JavaScript measurement is allowed only where real geometry/math requires it (for example carousel transforms) and must observe the actual owner container, not duplicate CSS breakpoints in unrelated scripts.

Resize must be reversible and deterministic:

```text
state A → resize/reflow → state B → reverse resize/reflow → equivalent state A
```

## 8. Production migration rule

The prototype DOM structure is not a public API. Production migration preserves:

- component responsibilities;
- state ownership;
- intents;
- view-model contracts;
- responsive invariants;
- accessibility outcomes;
- visual oracle where accepted.

It does not preserve incidental selectors, historical CSS cascade or monolithic script layout.
