# DANTE — B2.5 Frontend Pre-Production Foundation v0

**Status:** FOUNDATION BASELINE / B2 VISUAL WORK STILL OPEN  
**Date:** 2026-08-20  
**Branch:** `prototype/frontend`  
**PRE-SCOPE:** `bb2ddc396763b06aa4406035baab837d8e2b704b`

## Purpose

Raise the frontend workstream from coded UX + documentation to a production-shaped pre-production contract before continuing fragile responsive iteration and before the later `apps/web` migration.

## Added baseline

- explicit component/geometry ownership;
- server/UI/transient state separation;
- framework-neutral states/events;
- frontend/backend integration boundary;
- view-model != DTO != Domain != persistence rule;
- runtime-boundary validation requirement;
- synthetic fixtures;
- desktop resize/reflow matrix;
- visual/behavior/accessibility/integration/performance/security quality-gate model;
- production-web handoff criteria;
- executable stdlib contract-drift test.

## Home central-stage machine-readable baseline

```text
contract     prototypes/frontend/shared/contracts/home-stage.contract.json
view schema  prototypes/frontend/shared/contracts/home-stage.view-model.schema.json
resize QA    prototypes/frontend/shared/contracts/home-responsive.matrix.json
fixture      prototypes/frontend/shared/fixtures/home-stage.v0.json
```

Key B2 working constraints preserved:

- one `home.stage` geometry owner;
- working projections are continuity (`Mondi`) and signals (`Segnali`);
- Continuity desktop target = 5 visible sphere positions;
- Signals desktop maximum = 3 complete visible items;
- mode switch must not change outer stage geometry or selector/navigation anchors;
- AI expanded/collapsed reflow remains Home-shell behavior, not projection-specific behavior.

## What this does not claim

- B2 visual/responsive closure: **NO**;
- global resize defect fixed: **NO**;
- production `apps/web` scaffold started: **NO**;
- backend API/endpoints defined: **NO**;
- production framework/package versions frozen: **NO**;
- logo/branding alignment completed: **NO**.

The last formally accepted Home build remains B1 Context Rail v1. B2 v16 remains a saved WIP oracle while responsive hardening continues against this new engineering baseline.

## Validation qualification

The machine-readable contract test is designed to run without third-party Python packages and validates contract-version coherence, mode/state consistency, 24 required responsive matrix combinations, three-signal maximum, five-continuity target and fixture identity/basic shape.

Repository post-write path/HEAD verification remains required after this checkpoint is written.
