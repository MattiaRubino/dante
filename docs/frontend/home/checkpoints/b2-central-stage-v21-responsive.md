# DANTE — Home B2 Central Stage v21 Responsive Working Baseline

**Status:** USER-REVIEWED / APPROVED WORKING BASELINE / B2 OPEN  
**Date:** 2026-08-20  
**Branch:** `prototype/frontend`  
**PRE-SCOPE:** `fb6df17d8c3b36a1542e3ee346aee92c0ca0f88c`

## Purpose

Preserve the B2 central-stage state after responsive hardening and user review, without falsely declaring the whole B2 scope closed.

This checkpoint supersedes v16 as the current **working visual/behavior baseline** for B2. B1 Context Rail v1 remains the last formally closed Home milestone; v21 is the current B2 oracle for continuation.

## Current B2 direction

- central-stage projections are `Mondi` and `Segnali`;
- technical projection IDs are `home.stage.continuity` and `home.stage.signals`;
- `Mondi` preserves the sphere-carousel lineage;
- desktop continuity target remains five visible sphere positions;
- partial continuity uses the existing sphere positions as ghost `+` slots rather than creating extra geometry;
- `Segnali` uses the same previous/next, selection and drag/swipe interaction grammar;
- `Segnali` renders at most three complete visible items in the current desktop working composition;
- the compact Signal track remains centered within the stage;
- mode switching must not redefine the outer stage geometry, selector anchor or lateral-navigation anchors;
- AI expanded/collapsed reflow remains owned by the Home shell.

## Responsive hardening represented by v21

The v21 lineage repairs the previously open global-window-resize failure by making stage rendering follow the real physical stage geometry rather than relying only on early `window.resize` timing.

The working implementation includes:

- stage-geometry resynchronization after real layout changes;
- `ResizeObserver`-based stage observation where available;
- centered Signal track constrained to the intended inner stage footprint;
- adaptive Continuity spacing so five sphere positions fit the narrow critical desktop state rather than overflowing;
- preservation of the existing B1 AI expanded/collapsed shell reflow.

Critical narrow state previously isolated and checked during iteration:

```text
viewport        901 × 768
AI              collapsed
scene width     ~439 px
continuity      5 visible sphere positions fit inside stage
```

## Exact saved preview identities

### Full state

```text
source preview
DANTE_Home_B2_full_responsive_guarded_preview_v21.html

size
762160 bytes

SHA-256
b653b5455903d0978cae88ff76fb74c285d0104334871cdb9f406f6d945c4cde
```

### Partial state

```text
source preview
DANTE_Home_B2_partial_responsive_guarded_preview_v21.html

size
762090 bytes

SHA-256
390f12cf6c327be27342dcc038d398fd2751c3e2a9cbab3fbf2d981092405763
```

The archive under `prototypes/frontend/home/archive/b2-central-stage-v21/` stores deterministic gzip+Base64 unified diffs from the previously saved v16 artifacts to these v21 outputs.

## QA qualification

Established for this working checkpoint:

- user reviewed the responsive v21 previews and accepted them as the current working baseline;
- v21 static checks reported zero duplicate DOM IDs and zero inline-JavaScript syntax failures;
- the previously isolated narrow Continuity overflow was corrected;
- the B2.5 machine-readable contract keeps the 24-case target matrix explicit.

Not claimed:

- a fresh automated browser PASS for every one of the 24 matrix combinations in this repository-write scope;
- production React/Next implementation;
- backend integration/API PASS;
- complete B2 closure.

The browser automation environment used during iteration blocked the attempted complete rerun in some runs, so this checkpoint records user-reviewed working acceptance rather than inventing an automated-matrix PASS.

## Still open before B2 closure

1. decide whether/how a persistent add affordance should appear for Mondi, Segnali and future stage projections;
2. align the visible product lockup/logo to DANTE;
3. review the overall Home palette/skin;
4. review the Home background/atmosphere;
5. run the applicable final B2/Home QA after those decisions land.

No backend endpoint, persistence entity, Domain change or production-framework selection is created by this checkpoint.
