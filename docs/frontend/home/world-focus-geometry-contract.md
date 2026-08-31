# DANTE — World Focus Geometry Contract WF-G2 Candidate

**Status:** CANDIDATE / visual approval pending  
**Geometry version:** `wf-g2-candidate`  
**Scope:** World Focus structural geometry only

This contract exists to stop World Focus geometry from drifting during later visual, module, AI, insight, responsive and backend work.

## 1. Route/surface ownership

World Focus is a real application route/surface:

```text
/home
/worlds
/worlds/:worldId
```

Opening a World from Home navigates to `/worlds/:worldId`.

World Focus is not rendered on top of Home and does not use Home as its visible background. The global AppShell Topbar remains outside World Focus ownership and is not modified by this contract.

## 2. Candidate geometry

The World Focus route owns a full white route surface below the global Topbar.

The visual frame is defined by exactly three **true concentric circles** centered on the World Focus surface:

- `outer` — outer boundary of the future World visual-frame band;
- `origin` — canonical reference/origin for future transition, drawing or asset placement;
- `inner` — inner boundary of the future World visual-frame band.

These are SVG `<circle>` primitives, not manually drawn Bézier/path approximations.

Their radii are intentionally large enough that the rectangular viewport clips away the side-middle portions. The intended visible result is therefore only four corner arc groups:

```text
upper-left                         upper-right
     )))                         (((



     )))                         (((
lower-left                         lower-right
```

There must be no persistent vertical side bulge and no inverted hand-authored curve.

Future galaxy, particle, magic-circle, shader, SVG or image assets must fit this visual-frame band; they must not redefine the page geometry.

## 3. Workspace rule

The real application workspace remains rectangular and independent from the visual-circle frame.

It:

- is never clipped to a circle or ellipse;
- remains the layout authority for future AI, modules, widgets, insights, charts, timelines and drill-down surfaces;
- may visually overlap future decorative layers only when explicitly approved, without changing its geometry authority.

During geometry QA the workspace is intentionally rendered with a blue debug fill/border. That color is not product skin.

## 4. Responsive authority

All structural values come from:

`apps/web/src/features/world-focus/model/world-focus-geometry.ts`

The candidate contract owns:

- the exact three guide radii;
- workspace inline inset;
- compact workspace inline inset;
- workspace vertical inset;
- compact vertical inset.

Do not duplicate these values in module/projection CSS.

The workspace must remain bounded at the desktop pressure widths:

```text
1600
1366
1024
901
```

Compact behavior is separately bounded below `720px`.

## 5. Change control

`wf-g2-candidate` is not locked until user visual approval.

Once approved it must be promoted to a locked version and any later geometry change requires all of:

1. explicit product approval;
2. intentional edit of `world-focus-geometry.ts`;
3. geometry version bump;
4. contract-test update;
5. responsive/E2E geometry revalidation;
6. this document updated in the same change.

Color, particles, galaxy texture, magic-circle styling, asset choice and optional entry animation are skin/presentation work and must not silently move the approved circles or workspace.

## 6. Current visual gate

Before any cosmic/Dr-Strange-style styling is reintroduced, verify in the real browser that:

- the page below the Topbar is white;
- exactly three true concentric circle guides exist;
- only their four corner arc portions are materially visible;
- the center/origin guide is visually stronger than outer/inner guides;
- there is no side-middle bulge or inverse-looking curve;
- the blue workspace remains a separate rectangular debug region;
- resizing across the pressure widths does not distort circles into ellipses;
- nothing overflows or moves arbitrarily.

No visual skin work is authorized until this geometry gate is approved.
