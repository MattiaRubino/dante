# DANTE — Home B2 Central Stage v16 WIP

**Status:** SAVED WIP / NOT ACCEPTED / B2 OPEN  
**Date:** 2026-08-20  
**Branch:** `prototype/frontend`  
**Base accepted build:** B1 Context Rail v1 (`a781fca7a1ca0f967f41a1b9cad8165c636da900f4bc497974b9d1a849d7a4b0`)

## Why this checkpoint exists

The user explicitly requested that the current B2 visual/interaction progress be preserved before fixing the remaining global window-resize defect and before aligning the visible product logo/name.

This checkpoint is intentionally **not** promoted to the current accepted Home build. B1 remains the accepted oracle until the known B2 geometry defect is repaired and the resulting state is reviewed.

## Current B2 direction preserved here

- central-stage visible modes: `Mondi` and `Segnali`;
- `Mondi` keeps the existing sphere-carousel visual/interaction lineage;
- partial Mondi state is represented by existing sphere positions whose name/icon are replaced by `+` and whose appearance becomes ghosted; carousel geometry itself is not conceptually redefined;
- the external add control tested earlier is not part of this checkpoint;
- `Segnali` uses the same carousel/navigation grammar as Mondi: selection, previous/next and drag/swipe;
- desktop Signal viewport is deliberately capped at **3 visible signals**;
- the compact Signal track is centered rather than spreading three signals across the full stage width;
- current demonstrated signals remain prototype examples, not domain taxonomy or persisted backend contracts.

## Known defect intentionally carried forward

**GLOBAL WINDOW RESIZE / RESPONSIVE GEOMETRY: NOT PASS.**

When the global browser/window width is reduced, parts of the current monolithic Home composition can break or misalign. This checkpoint is saved despite that defect so the approved design progress is not lost. The next B2 task is to fix this without regressing the accepted B1 expanded/collapsed AI behavior, stage geometry, arrows, timeline or contextual rail.

Do not describe this checkpoint as responsive-complete, B2-closed, or production-ready.

## Exact saved preview identities

### Full Mondi state

```text
source preview
DANTE_Home_B2_full_signals3_compact_preview_v16.html

size
759622 bytes

SHA-256
b9fa6ce5644d3b87ace5c9cd0388f9eb311a8f1800dc7ac363c14aee8ecd6efd
```

### Partial Mondi state

```text
source preview
DANTE_Home_B2_partial_signals3_compact_preview_v16.html

size
759552 bytes

SHA-256
0f9f632783e93f0cefe33591cf0ebadf2167f8806381ad03cf68aa3ae1c821e6
```

The archive under `prototypes/frontend/home/archive/b2-central-stage-v16/` stores deterministic gzip+base64 unified diffs against the accepted B1 output.

## QA qualification

Previously established static checks for the preview lineage include zero duplicate IDs and zero inline-JS syntax failures. Geometry checks during B2 iteration were useful for specific fixed-width states but **do not override the known global resize failure**.

Therefore this checkpoint records:

- visual direction: SAVED;
- desktop 3-signal composition: SAVED;
- partial ghost-sphere direction: SAVED;
- global responsive/window-resize QA: **FAIL / OPEN**;
- B2 closure: **NOT DONE**;
- branding/logo alignment: **NOT DONE**.
