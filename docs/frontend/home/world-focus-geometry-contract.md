# DANTE — World Focus Geometry Contract WF-G3

**Status:** **LOCKED — USER-AUTHORIZED GEOMETRY BASELINE**  
**Geometry version:** `wf-g3`  
**Date:** 2026-08-31  
**Scope:** World Focus visual-frame + workspace structural geometry only

WF-G3 is subordinate to `world-focus-structural-contract.md` (WF0) and freezes the exact geometry that future visual skin, modules, AI, insights and backend work must consume.

It is not permission to treat the ellipses as a content container.

## 1. Route/surface ownership

World Focus is a real application route/surface:

```text
/home
/worlds
/worlds/:worldId
```

Opening a World from Home navigates to `/worlds/:worldId`.

World Focus is not rendered on top of Home and does not use Home as its visible background. The global AppShell Topbar remains outside World Focus ownership and is not modified by this contract.

## 2. Locked visual-frame geometry

The World Focus route owns a route surface below the global Topbar.

The visual frame is defined by exactly three **true concentric SVG ellipses** centered on the World Focus surface:

- `outer` — external boundary of the future World visual-frame band;
- `origin` — canonical reference/origin for future transition, drawing or asset placement;
- `inner` — internal boundary of the future World visual-frame band.

These are SVG `<ellipse>` primitives, not manually drawn Bézier/path approximations.

The origin ellipse is the geometric authority:

```text
cx = 50%
cy = 50%
rx = 50%
ry = 87%
```

Therefore its left and right extrema are mathematically tangent to the lateral route edges at mid-height.

The frame band is:

```text
outer  rx 52.25% / ry 90%  -> extends outside the route laterally
origin rx 50%    / ry 87%  -> touches both route sides at mid-height
inner  rx 47.75% / ry 84%  -> remains slightly inside
```

The taller vertical radii deliberately produce elongated corner arcs instead of a rigid circular silhouette.

Future galaxy, particle, magic-circle, shader, SVG or image assets must use this band as their geometry reference. They may not silently move it.

## 3. Locked workspace geometry

The real application workspace is rectangular and independent from the visual-frame ellipses.

Structural anchors:

```text
standard inline inset: clamp(136px, 14vw, 224px)
compact inline inset:  clamp(76px, 18vw, 112px)
standard block inset:  clamp(32px, 5vh, 64px)
compact block inset:   20px
compact tuning max:    720px
```

Permanent rules:

- workspace is never clipped to a circle or ellipse;
- visual frame never becomes widget/module layout authority;
- future World skin may visually overlap where explicitly designed but cannot redefine workspace geometry;
- future World content cannot redefine shell or visual-frame geometry;
- transient overlays cannot become persistent layout owners.

The current blue workspace fill/border is debug geometry only and is not product skin.

## 4. Responsive authority

The runtime geometry authority is:

`apps/web/src/features/world-focus/model/world-focus-geometry.ts`

The machine structural authority is:

`prototypes/frontend/shared/contracts/world-focus-structure.contract.json`

The pressure matrix is:

`prototypes/frontend/shared/contracts/world-focus-shell-responsive.matrix.json`

The 720 px boundary changes workspace inset tuning only. It does not authorize a second macro World Focus composition.

## 5. Change control

`wf-g3` is frozen.

Any later geometry change requires all of:

1. explicit user/product approval before production writes;
2. intentional edit of `world-focus-geometry.ts`;
3. geometry version bump (`wf-g4`, ...);
4. machine-contract update;
5. unit/E2E contract update;
6. responsive geometry revalidation;
7. this document and WF0 updated in the same approved change.

Regression guards must not be weakened merely to accept accidental geometry drift.

Color, particles, galaxy texture, magic-circle styling, asset choice and optional entry animation are presentation work and may not silently move WF-G3.

## 6. Frozen meaning

From this point:

> **the visual skin must fit the geometry; the geometry does not chase the visual skin.**

Likewise:

> **workspace features consume the rectangular workspace; they do not turn the World frame into their layout container.**
