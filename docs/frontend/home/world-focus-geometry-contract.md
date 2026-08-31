# DANTE — World Focus Geometry Contract WF-G1

**Status:** LOCKED / visual approval pending  
**Geometry version:** `wf-g1`  
**Scope:** World Focus structural geometry only

WF-G1 exists to stop World Focus geometry from drifting during later visual, module, AI, insight, responsive and backend work.

## 1. Route/surface ownership

World Focus is a real application route/surface:

```text
/home
/worlds
/worlds/:worldId
```

Opening a World from Home navigates to `/worlds/:worldId`.

World Focus is not rendered on top of Home and does not use Home as its visible background. The global AppShell Topbar remains outside World Focus ownership and is not modified by this contract.

## 2. Locked geometry

The World Focus route owns a full white route surface below the global Topbar.

Its structural geometry is exactly:

```text
LEFT VISUAL FRAME BAND     RECTANGULAR WORKSPACE     RIGHT VISUAL FRAME BAND

outer guide                                     mirrored outer guide
origin guide                                   mirrored origin guide
inner guide                                     mirrored inner guide
```

Each side contains exactly three curved guides:

- `outer` — outer boundary of the future World visual-frame band;
- `origin` — canonical reference/origin for future transition, drawing or asset placement;
- `inner` — inner boundary of the future World visual-frame band.

The guides are geometry references. Future galaxy, particle, magic-circle, shader, SVG or image assets must fit the band; they must not redefine the page geometry.

## 3. Workspace rule

The real application workspace is rectangular.

It:

- sits between the two side visual-frame bands;
- is never clipped to a circle or ellipse;
- remains the layout authority for future AI, modules, widgets, insights, charts, timelines and drill-down surfaces;
- may visually overlap future decorative layers only when explicitly approved, without changing its geometry authority.

During WF-G1 visual QA the workspace is intentionally rendered with a blue debug fill/border. That color is not product skin.

## 4. Responsive authority

All structural values come from:

`apps/web/src/features/world-focus/model/world-focus-geometry.ts`

The contract owns:

- side rail width;
- compact side rail width;
- workspace-to-frame gap;
- compact workspace gap;
- workspace vertical inset;
- compact vertical inset;
- the exact three guide paths.

Do not duplicate these values in module/projection CSS.

The geometry must remain non-overlapping at the locked desktop pressure widths:

```text
1600
1366
1024
901
```

Compact behavior is separately bounded below `720px`.

## 5. Change control

`wf-g1` is immutable after visual approval.

A geometry change requires all of:

1. explicit product approval;
2. intentional edit of `world-focus-geometry.ts`;
3. geometry version bump (`wf-g2`, ...);
4. contract-test update;
5. responsive/E2E geometry revalidation;
6. this document updated in the same change.

Color, particles, galaxy texture, magic-circle styling, asset choice and optional entry animation are **skin/presentation work** and must not silently move the WF-G1 guides or workspace.

## 6. Current visual gate

Before any cosmic/Dr-Strange-style styling is reintroduced, verify in the real browser that:

- the page below the Topbar is white;
- exactly three black guide curves are visible on the left;
- exactly three mirrored guide curves are visible on the right;
- the center/origin guide is visually stronger than outer/inner guides;
- the blue rectangular workspace stays wholly between the two guide rails;
- resizing across the pressure widths changes proportions only according to the locked responsive contract;
- nothing overflows or moves arbitrarily.

No visual skin work is authorized until this geometry gate is approved.
