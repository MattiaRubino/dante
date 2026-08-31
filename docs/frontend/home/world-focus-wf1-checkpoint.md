# DANTE — World Focus WF1 Checkpoint

**Status:** WF-G3 GEOMETRY CANDIDATE / USER VISUAL QA PENDING  
**Date:** 2026-08-31  
**Branch:** `feature/home-react`  
**Scope:** dedicated World Focus route + structural geometry candidate

This checkpoint supersedes the earlier `/home?focus=...` overlay implementation and the earlier transition experiments.

## 1. Current architectural decision

World Focus is a real application route/surface:

```text
/home
/worlds
/worlds/:worldId
```

Opening a World from Home navigates to `/worlds/:worldId`.

World Focus is **not** rendered over Home and Home is **not** its visible background.

The persistent AppShell Topbar is outside World Focus ownership and remains unchanged.

## 2. Current interaction

Home keeps its existing World carousel behavior:

```text
first activation
-> select / center World

subsequent activation on the centered World
-> navigate to /worlds/:worldId
```

Pointer drag must not open World Focus. Keyboard activation preserves the same select-then-open semantics.

## 3. WF-G3 candidate geometry

The geometry authority is:

```text
apps/web/src/features/world-focus/model/world-focus-geometry.ts
```

Geometry version:

```text
wf-g3-candidate
```

The World Focus route is intentionally plain during this gate:

- white route surface below the Topbar;
- three concentric SVG ellipse guides centered on the route;
- `outer` extends slightly outside the lateral route edge;
- `origin` is tangent to the left/right route edge at mid-height and is the canonical future animation/asset reference line;
- `inner` remains slightly inside;
- the vertical radii are taller than the route half-height so the visible corner arcs are elongated rather than circular;
- one real rectangular workspace remains independent from those visual guides;
- the workspace is blue only as temporary geometry/debug visualization.

The workspace is never clipped to a circle or ellipse.

## 4. Geometry change control

WF-G3 remains a candidate until the user visually approves it.

Once approved it is promoted to a locked geometry version. Any later geometry change requires:

1. explicit user/product approval;
2. intentional edit to the geometry authority;
3. geometry version bump;
4. contract test update;
5. responsive/E2E revalidation;
6. documentation update in the same change.

Cosmic styling, particles, magic-circle treatment, image/shader assets and optional entry animation are presentation layers. They may use the approved ellipse band but may not silently move it or redefine the workspace.

## 5. Responsive pressure

The desktop pressure widths are:

```text
1600
1366
1024
901
```

Compact behavior is separately bounded below `720px`.

At every pressure width:

- the origin ellipse remains centered and tangent to the lateral route edges at mid-height;
- outer remains outside the origin line and inner remains inside it;
- the rectangular workspace stays independently bounded;
- no horizontal overflow is allowed.

## 6. Current content boundary

The workspace is intentionally empty except for truthful shell states:

```text
loading
ready
error
unavailable
```

No production AI surface, widgets, modules, charts, insight surfaces or backend data are authorized in this geometry gate.

## 7. Deferred presentation

All previous camera/WebGL/portal transition experiments are outside the current runtime target.

The required navigation is currently:

```text
Home
-> World Focus route
```

without an intermediate ornamental transition.

An optional transition may be designed later, but only after the structural geometry is approved and without making navigation depend on it.

## 8. Current World identity status

The current World catalog remains synthetic pre-backend frontend presentation data.

```text
World Focus fixture id
!= Domain identity
!= backend DTO
!= database row
!= persisted World entity
```

No World Domain primitive or database change is introduced by WF1.

## 9. Visual gate now required

Before adding any cosmic/Dr-Strange-style skin, verify in the real browser:

1. Home opens a dedicated `/worlds/:worldId` page;
2. the Topbar remains exactly the global Topbar;
3. the area below it is white;
4. exactly three concentric ellipse guides are visible;
5. the central/origin guide reaches the left/right route edge at side mid-height;
6. the outer guide is farther outside and the inner guide farther inside;
7. the corner arcs look smooth and intentionally oval;
8. the blue rectangular workspace remains independent from the visual frame;
9. resizing across the pressure widths behaves predictably;
10. nothing overflows or changes geometry ownership.

Only after this visual gate is approved can the geometry be marked LOCKED and presentation work resume.
