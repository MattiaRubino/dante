# DANTE — World Focus Geometry Contract WF-G3 Candidate

**Status:** CANDIDATE / visual approval pending  
**Geometry version:** `wf-g3-candidate`  
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

The visual frame is defined by exactly three **true concentric SVG ellipses** centered on the World Focus surface:

- `outer` — outer boundary of the future World visual-frame band;
- `origin` — canonical reference/origin for future transition, drawing or asset placement;
- `inner` — inner boundary of the future World visual-frame band.

These are SVG `<ellipse>` primitives, not manually drawn Bézier/path approximations.

The origin ellipse is the geometric authority:

```text
cx = 50%
cy = 50%
rx = 50%
ry = 87%
```

Therefore its left and right extrema are mathematically tangent to the lateral route edges at mid-height. It must not disappear outside the viewport at the side midpoint.

The frame band is formed by:

```text
outer  rx 52.25% / ry 90%  -> extends outside the route laterally
origin rx 50%    / ry 87%  -> touches both route sides at mid-height
inner  rx 47.75% / ry 84%  -> remains slightly inside
```

The taller vertical radii intentionally produce long, elegant corner arcs rather than a rigid circular silhouette.

Future galaxy, particle, magic-circle, shader, SVG or image assets must fit this visual-frame band; they must not redefine the page geometry.

## 3. Workspace rule

The real application workspace remains rectangular and independent from the visual-frame ellipses.

It:

- is never clipped to a circle or ellipse;
- remains the layout authority for future AI, modules, widgets, insights, charts, timelines and drill-down surfaces;
- may visually overlap future decorative layers only when explicitly approved, without changing its geometry authority.

During geometry QA the workspace is intentionally rendered with a blue debug fill/border. That color is not product skin.

## 4. Responsive authority

All structural values come from:

`apps/web/src/features/world-focus/model/world-focus-geometry.ts`

The candidate contract owns:

- the exact three ellipse `rx` / `ry` pairs;
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

`wf-g3-candidate` is not locked until user visual approval.

Once approved it must be promoted to a locked version and any later geometry change requires all of:

1. explicit product approval;
2. intentional edit of `world-focus-geometry.ts`;
3. geometry version bump;
4. contract-test update;
5. responsive/E2E geometry revalidation;
6. this document updated in the same change.

Color, particles, galaxy texture, magic-circle styling, asset choice and optional entry animation are skin/presentation work and must not silently move the approved ellipses or workspace.

## 6. Current visual gate

Before any cosmic/Dr-Strange-style styling is reintroduced, verify in the real browser that:

- the page below the Topbar is white;
- exactly three true concentric ellipse guides exist;
- the origin ellipse touches the left/right route edge at side mid-height;
- the outer ellipse extends outside that edge;
- the inner ellipse remains slightly inside;
- the corner arcs read as smooth elongated geometry rather than a rigid circle;
- the center/origin guide is visually stronger than outer/inner guides;
- the blue workspace remains a separate rectangular debug region;
- nothing overflows or moves arbitrarily.

No visual skin work is authorized until this geometry gate is approved.
