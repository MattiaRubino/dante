# DANTE — Home Current Pre-Frontend Checkpoint

**Source lineage:** LifeOS Phase 4 — Home vNext Orientation + Day Ribbon v1  
**Current workstream:** `prototype/frontend`  
**Status:** **APPROVED WORKING VISUAL/BEHAVIOR ORACLE**  
**Nature:** standalone HTML/CSS/JavaScript UX prototype; not production application code and not final Information Architecture/product vocabulary

## Exact artifact

```text
path
prototypes/frontend/home/current/home.html

size
748625 bytes

SHA-256
986e7d22b4cb536c8a89eacf116bee3350dd0b8aafeb497df2f837fc9c1bf5df

Git blob SHA
fd9788212fbbd1ee40e53271cc39cedd9275b341
```

The artifact is migrated into `prototype/frontend` by reusing the exact corrected Git blob from the historical Phase 4 branch. No byte transformation, visual reconstruction or semantic reimplementation is part of A1.

The historical source was corrected by the user on commit `cb58b1528292398ccedeaedb60b44a4ff6e6235f`; the corrected delta changed exactly one source line so `drRoadGrad` uses `gradientUnits:'userSpaceOnUse'` with percentage x coordinates.

## What the current artifact carries

At a high level the exact artifact contains:

- global Home shell and conversational AI surface;
- current-situation composition around `Ora` / immediate continuation, attention and contextual/dynamic information;
- central prototype stage with current `Worlds` / `Stats` modes and navigation behavior;
- Home orientation strip and synchronized day context;
- day ribbon / week navigation;
- contextual `Ora` return-to-current-time action;
- calendar navigation;
- 24-hour timeline;
- nonlinear temporal density and overlap handling;
- group chips, filters/reordering and grouped timeline expansion;
- timeline panel expansion;
- event focus/subtasks;
- drag/move and Undo lineage;
- zoom and manual time editing with anchored picker;
- environmental/path context;
- current side/secondary surfaces.

This list is an index only. The exact HTML remains the visual/behavior oracle.

## Architecture/research constraints

Continue to preserve:

- one reality, multiple projections;
- time primary, not sovereign;
- current situation broader than the timeline;
- stable semantics with adaptive/contextual presentation;
- GUI as a first-class interaction language;
- visible user authority and inspectable durable state;
- progressive disclosure rather than an infinite dashboard;
- no permanent UI merely because an internal ontology concept exists;
- Mobile/Web semantic continuity with surface-specific representation.

See `docs/frontend/research-index.md` and the linked current/main and preserved Phase 4 evidence.

## Prototype vocabulary qualification

Visible labels are not canonized by this checkpoint.

In particular:

- `Worlds` is historical/working prototype vocabulary, not an accepted Domain primitive or final product noun;
- `Stats` is a working prototype mode, not a finalized IA destination;
- `Per te`, `Appunti`, `Review` and similar copy remain subject to deliberate product/naming review;
- `Today v21` remains a historical temporal behavior milestone, not a second current name for Home.

## Visual/product guardrails

- professional rather than toy-like;
- warm/personal without infantilization;
- capable without enterprise/cockpit heaviness;
- no decorative-control accumulation;
- no equal-weight dashboard grid for every available concept;
- no AI supremacy over user control;
- hierarchy should come from relevance, scale, spacing, typography and restrained accents before extra containers;
- solving a local problem must not silently alter accepted out-of-scope regions.

## Current QA evidence

For the corrected artifact:

```text
size                         748625 bytes
SHA-256                      986e7d22b4cb536c8a89eacf116bee3350dd0b8aafeb497df2f837fc9c1bf5df
Git blob SHA                 fd9788212fbbd1ee40e53271cc39cedd9275b341
DOM IDs                      67
duplicate DOM IDs            0
style blocks                 37
CSS parse errors             0
inline scripts               20
inline JS syntax failures    0
exact remote blob identity   PASS
```

The previously recorded Chromium smoke belonged to the immediately preceding blob and was **not rerun after the one-line corrective replacement**. Do not report that smoke as a PASS for the corrected blob.

The complete historical `today-v21-regression.py` suite was also **NOT RUN** against this corrected integrated Home artifact.

Detailed migrated QA record: `prototypes/frontend/home/current/qa-static.json`.

## Continuation rule

A2 derives a maintainable modular `work/` source from this exact oracle without changing visual output or behavior. The oracle under `current/` is not edited during A2.

After A2, user-approved Home work proceeds through the two side surfaces, central stage purpose/content, naming, overlay grammar, full functional review, final brand/skin and final Home QA/checkpoint.
