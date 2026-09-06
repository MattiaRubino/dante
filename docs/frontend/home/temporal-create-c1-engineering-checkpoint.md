# DANTE — Temporal Create C1 Engineering Checkpoint

**Status:** CURRENT ENGINEERING CHECKPOINT — AUTOMATED GREEN / MANUAL OPEN  
**Date:** 2026-09-04  
**Repository:** `MattiaRubino/dante`  
**Branch:** `feature/home-timeline`  
**Worktree:** `/home/mattia/projects/dante-timeline`  
**Code checkpoint:** `1e7b7752b69f006a4b632e2e2d3ef1522d30e95e`  
**Frontend CI:** #937 / `33905239085` — Quality PASS, Mobile PASS, Chromium PASS, Firefox frozen PASS, Gate PASS

## Engineering state

The major C1 frontend foundations are implemented and automatically healthy:

- type-driven base Create;
- Activity/Event placement semantics;
- base + Advanced disclosure;
- conditional execution controls;
- Routine-backed Activity repeat / Event-owned recurrence;
- CP6 custom recurrence authoring;
- Planning Tray v2;
- all-day per-day lane v2;
- Event Agenda/internal parts;
- Timeline materialization/Undo integration;
- simple desktop Create floating + draggable;
- Advanced desktop floating + bounded;
- non-modal Create: Home/Timeline remains interactive;
- explicit close/discard contract;
- mobile bounds;
- frozen T1 regression preserved.

## Known intentional integration boundary

C1 does not own canonical recurring-instance generation.

The local Create bridge can materialize the authored master/first placed projection. Future recurring Occurrences must come from the Routine/Event recurrence evaluator/backend and later temporal range-query/read-model bridge.

Do not add a browser recurrence engine to make the demo look complete.

## Manual gate

Engineering green does not mean C1 is closed. The user is intentionally polishing Create one UX foundation at a time.

The current candidate to inspect is the floating/non-modal Create behavior. Any next implementation scope should be exactly one user-selected issue.

A simple-only left pin/dock has been discussed but is not implemented or required yet.

## Frozen dependencies

Do not reopen H0, T1 or F0 without a demonstrated defect. Do not touch PostgreSQL/Alembic/CP6 for current UX polish.

## Closure

```text
ENGINEERING AUTOMATED GREEN
MANUAL PRODUCT ITERATION ACTIVE
C1 NOT CLOSED
C2 BLOCKED
```

Final closure requires explicit `C1 MANUAL PASS — APPROVED`.
