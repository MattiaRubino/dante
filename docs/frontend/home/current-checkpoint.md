# DANTE — Home Current Checkpoint

**Status:** **USER-REVIEWED / APPROVED REACT MIGRATION BASELINE**  
**Date:** 2026-08-24  
**Mainline purpose:** product/UX oracle for implementation in the React/TypeScript frontend already materialized on `main`.

This file supersedes the historical baseline metadata at the top of `docs/frontend/home/contract.md`. The behavior sections in that contract remain authoritative unless explicitly overridden here.

## Current accepted Home baseline

```text
B2 Home Infrastructure Color v27
  over B2 Home Edge Attachment v26
  over B2 Home Shell + Timeline Quick Add v25
  over B2 Home Visual Skin v24
  over B2 Home Branding v23
  over B2 Central Stage v22
```

The exploratory prototype branch is frozen as historical evidence; React implementation now proceeds from `main`.

## Accepted shell and topbar

```text
LEFT                         CENTER                    RIGHT
DANTE + Cerca                Home / Mondi / Oggi       Crea / Review / launcher / account
```

- application bar is sticky and shell-level edge-to-edge;
- DANTE official symbol/wordmark treatment is retained;
- Search follows DANTE;
- primary navigation remains centered;
- `Crea` is the first right-side utility action;
- Review/launcher remain legacy/prototype controls until a bounded cleanup decides their production fate.

## Accepted Home surface geometry

- application shell is fluid rather than capped to the old prototype width;
- expanded AI surface is attached to the left application edge with square attached-side corners and preserved right-side geometry;
- collapsed AI rail is also attached to the left edge with square-left / rounded-right treatment;
- timeline attaches to the left edge while preserving its right-side relationship with the Context Rail;
- timeline attached-side corners are square; free-side rounding remains;
- Context Rail remains subordinate to and paired with the timeline.

These are visual/layout requirements, not permission for projection-specific geometry hacks.

## Accepted visual language

Generic interface chrome uses:

```text
primary / active / selected interaction = DANTE orange
inactive generic controls               = neutral blue-grey / charcoal
```

Semantic color is preserved where it identifies content or state:

- Mondi/world identities;
- timeline group identities such as Focus, Riunioni, Salute and Creatività;
- event/category borders;
- semantic success/warning/error states.

Legacy generic purple chrome is not part of the accepted DANTE direction. The reviewed v27 pass covers temporal controls and Context Rail infrastructure such as `Ora`, selected day, Capture controls/status markers and Resolution confirmation chrome.

## Central stage boundary

The retained v22 rule is unchanged:

```text
Home stage = READ / NAVIGATE / OPEN
NO persistent +
NO ghost add slots
NO placeholder World/Signal entities
NO direct configuration CRUD in Home stage
```

Mondi and Segnali are projections inside one stable Home stage. Configuration/creation belongs to their dedicated management surfaces.

## Timeline

Accepted temporal header:

```text
add / month / now / week / actions
```

`home.timeline.quickAdd` is a real contextual Home control, but its current bridge to global `Crea` is still **prototype-only**. React migration must preserve the affordance without inventing backend write semantics. Final create type, date/time prefill, destination and persistence contract remain separate decisions.

The mature timeline behavior contract remains intact: calendar/date navigation, return-to-now, continuous day, overlap lanes, zoom, grouping, event focus/time editing and drag/move semantics are not reopened by the migration.

## Context Rail

`home.contextRail` keeps two simultaneously visible responsibilities:

```text
USER -> DANTE     Capture
DANTE -> USER     Resolution
```

- Capture is low-friction input without forced classification first;
- Resolution surfaces matters that genuinely require a user decision/confirmation/correction;
- Resolution is not a notifications center;
- complex resolution escalates to a deeper controlled surface rather than being crammed into the rail.

## React migration contract

Do **not** port the prototype monolith line-by-line.

Use the existing React/TypeScript materialization on `main` and reconstruct the accepted Home by ownership boundary. Expected component ownership includes, at minimum, application shell/topbar, Home orientation, AI surface, central stage/Mondi/Segnali projection, Today timeline and Context Rail.

Migration sequence:

1. preserve visual/behavioral parity;
2. consume semantic tokens/localization/contracts rather than historical raw prototype values;
3. use explicit frontend view models/adapters;
4. keep backend DTO/domain/persistence shapes out of components;
5. add responsive/accessibility/visual/component evidence in the real React stack;
6. only then address remaining small visual refinements or new product behavior.

## Machine-readable Home authorities

- `prototypes/frontend/shared/contracts/home-stage.contract.json`
- `prototypes/frontend/shared/contracts/home-stage.view-model.schema.json`
- `prototypes/frontend/shared/contracts/home-responsive.matrix.json`
- `prototypes/frontend/shared/fixtures/home-stage.v0.json`
- `tests/prototypes/frontend-preprod-contracts.py`

These are frontend view contracts, not backend/domain/database contracts.

## Frozen historical evidence

Historical prototype branch commit:

`2203c96c4aa1dc10258a84bcf461aa0b923e8951`

Final user-reviewed local wrapper:

```text
DANTE_Home_v43_VERIFIED_INJECTION_COLOR_FIX.html
size       87386 bytes
SHA-256    e82058e4e980208feb3f0c055dab3eec81812be1fa47e5f036e8d5d0e1fe859d
```

Exploratory archives/work files remain on `prototype/frontend` and are intentionally excluded from `main`.