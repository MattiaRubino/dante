# DANTE — World Focus WF1 Checkpoint

**Status:** **WF0 STRUCTURE FROZEN / WF-G3 GEOMETRY LOCKED**  
**Date:** 2026-08-31  
**Branch:** `feature/home-react`  
**Scope:** dedicated World Focus route + frozen structural shell/geometry baseline

This checkpoint supersedes the earlier `/home?focus=...` overlay implementation and all earlier transition/portal geometry experiments.

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

The authoritative structural contract is:

`docs/frontend/home/world-focus-structural-contract.md`

Machine authorities:

- `prototypes/frontend/shared/contracts/world-focus-structure.contract.json`
- `prototypes/frontend/shared/contracts/world-focus-shell-responsive.matrix.json`

## 2. Current interaction

Home keeps the select-then-open World carousel behavior:

```text
first activation
-> select / center World

subsequent activation on the centered World
-> navigate to /worlds/:worldId
```

Pointer drag must not open World Focus. Keyboard activation preserves the same semantics.

The route works without an intermediate ornamental transition.

## 3. Frozen ownership tree

```text
AppShell / Global Topbar
└── /worlds/:worldId
    └── worldFocus.shell
        ├── worldFocus.visualFrame
        ├── worldFocus.workspace
        └── worldFocus.shellControls

reserved transient future layer:
worldFocus.overlayLayer
```

The visual frame is decorative/reference geometry only. The rectangular workspace is the persistent application-layout authority.

Future AI, modules, widgets, charts, insights and backend-driven projections must consume that workspace rather than redefine the shell.

## 4. WF-G3 locked geometry

Runtime authority:

`apps/web/src/features/world-focus/model/world-focus-geometry.ts`

Geometry version:

```text
wf-g3
```

Locked ellipse frame:

```text
center  cx 50%, cy 50%
outer   rx 52.25%, ry 90%
origin  rx 50%,    ry 87%
inner   rx 47.75%, ry 84%
```

`origin` is tangent to both lateral route edges at mid-height. `outer` extends beyond it; `inner` remains inside it.

Locked workspace anchors:

```text
standard inline inset: clamp(136px, 14vw, 224px)
compact inline inset:  clamp(76px, 18vw, 112px)
standard block inset:  clamp(32px, 5vh, 64px)
compact block inset:   20px
compact tuning max:    720px
```

The workspace is never clipped to a circle/ellipse. The current blue fill/border is geometry-debug presentation only.

## 5. Responsive freeze

World Focus keeps one macro composition across current web widths:

```text
Visual Frame
+ Rectangular Workspace
+ Shell Controls
```

At `<= 720px`, only workspace inset tuning changes. No region is reparented and no second World Focus product surface is introduced.

Pressure widths:

```text
1856
1600
1366
1200
1024
901
900
760
721
720
719
390
```

No unexpected horizontal overflow is allowed.

## 6. Structural change control

WF0/WF-G3 are frozen.

Any later structural/geometry change requires explicit user approval **before** production writes and must deliberately update:

1. WF0 structural contract;
2. machine-readable contracts;
3. geometry version if geometry changes;
4. unit/E2E guards;
5. documentation;
6. responsive validation.

Regression guards must not be weakened merely to accept accidental drift.

## 7. What remains intentionally open

The freeze does not yet decide:

- workspace inner module composition;
- contextual DANTE AI exact placement;
- widget grid/drag/resize behavior;
- AI insight visual grammar;
- overlays/drill-down presentation;
- final World skin/colors/textures/particles;
- optional entry animation;
- backend/API semantics;
- World profile/config persistence;
- module registry / WorldFocusProjection contracts.

These decisions must be made inside the frozen shell unless WF0 is intentionally reopened.

## 8. Quality guards

WF0 is guarded by:

- `tests/prototypes/world-focus-preprod-contracts.py` — machine contract drift;
- `world-focus-geometry.test.ts` — locked geometry values;
- `world-focus-page.test.tsx` — React ownership/region/state contract;
- `world-focus.spec.ts` — route, Topbar, region, pressure-width and overflow contract;
- Frontend CI runs the World Focus machine drift guard before normal quality gates.

The current branch must still be validated by the real worktree/CI before claiming all gates green.

## 9. Working rule from now on

> **World features consume the World Focus skeleton; they do not renegotiate it.**

This is the structural baseline from which the visual skin and then the actual World content can continue.
