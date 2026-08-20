# DANTE — B2.5 Frontend Pre-Production Foundation v0

**Status:** FOUNDATION BASELINE / QA PASS / B2 VISUAL WORK STILL OPEN  
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

## Validation

The machine-readable contract test is stdlib-only and covers contract-version coherence, mode/state consistency, 24 required responsive matrix combinations, three-signal maximum, five-continuity target and fixture identity/basic shape.

Local execution of the committed guard logic against the v0 contract shape:

```text
frontend pre-production contracts: PASS
contractVersion=0.1.0
responsiveCases=24
signalsMaxVisible=3
continuityTargetVisible=5
```

Qualification: this is contract-layer evidence, not browser/visual responsive evidence. The actual B2 resize matrix remains to be run against the repaired Home artifact.

## Post-write remote QA

Against PRE-SCOPE `bb2ddc396763b06aa4406035baab837d8e2b704b`:

```text
expected physical paths   17
actual physical paths     17
added                     12
modified                   5
deleted                    0
unexpected                 0
```

The branch remained a linear fast-forward from PRE-SCOPE. Important contract/test/checkpoint payloads were read back from the remote branch. The final branch HEAD is recorded by Git and must be re-read before the next write gate.
