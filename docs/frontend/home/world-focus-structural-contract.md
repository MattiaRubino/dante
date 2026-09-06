# DANTE — World Focus Structural Contract WF0

**Status:** **FROZEN — USER-AUTHORIZED STRUCTURAL BASELINE**  
**Date:** 2026-08-31  
**Branch:** `feature/home-react`  
**Pre-scope HEAD:** `98b486a308961022ba0d8f43bb79339518457741`  
**Scope:** World Focus route ownership, macro regions, structural geometry, responsive tuning boundary and change control  
**Out of scope:** inner workspace module design, AI placement inside the workspace, visual skin, particles/galaxy treatment, optional entry animation, backend/API semantics

WF0 applies the same structural-freeze discipline as H0 Whole Home. It exists so future World Focus work consumes a stable application surface instead of renegotiating page geometry while adding AI, widgets, modules, charts, insights or backend data.

It does **not** freeze incidental DOM shape or every future visual detail. Refactors remain allowed when the observable structural contract stays equivalent and all guards remain green.

---

## 1. Change-control rule

The World Focus structural baseline is frozen.

Explicit user approval is required **before the first production write** when a change intentionally alters any of the following:

- World Focus as a dedicated route versus an overlay;
- relationship with the shared AppShell/Topbar;
- required macro-region presence or ownership;
- whether the visual frame participates in application layout;
- rectangular workspace ownership;
- stable ellipse geometry or its reference semantics;
- standard/compact structural-mode ownership;
- whether transient overlays participate in macro geometry;
- whether World-specific skin/content may move the shell or workspace.

Regression guards protecting WF0 must not be weakened, deleted or rewritten merely to accept accidental drift.

---

## 2. Authority hierarchy

When World Focus structure disagrees across sources, use this precedence:

```text
1. this WF0 Structural Contract
2. world-focus-structure.contract.json
3. world-focus-shell-responsive.matrix.json
4. world-focus-geometry.ts / geometry contract
5. current React implementation
6. historical World Focus experiments
```

H0 remains authoritative for Home. AppShell remains authoritative for the Global Topbar. WF0 may not redefine either boundary.

---

## 3. Frozen ownership tree

```text
APP SHELL / GLOBAL TOPBAR                 owner: app-shell
└── ROUTE OUTLET
    └── /worlds/:worldId
        └── WORLD FOCUS SHELL              owner: worldFocus.shell
            ├── VISUAL FRAME               owner: worldFocus.visualFrame
            ├── WORKSPACE                  owner: worldFocus.workspace
            └── SHELL CONTROLS             owner: worldFocus.shellControls

reserved future transient layer:
WORLD FOCUS OVERLAY LAYER                 owner: worldFocus.overlayLayer
```

### Permanent ownership consequences

- The Global Topbar is outside World Focus ownership and must not be copied, hidden, recolored, re-layered or recomposed by World Focus.
- `worldFocus.shell` owns the route-level composition below the Topbar.
- `worldFocus.visualFrame` owns only identity/decorative/reference presentation. It has no application-layout authority and remains non-interactive.
- `worldFocus.workspace` is the one rectangular authority for persistent World content.
- `worldFocus.shellControls` owns route/shell controls such as Back but may not move or resize the workspace.
- Future `worldFocus.overlayLayer` is transient and explicitly excluded from macro geometry.

---

## 4. Dedicated route boundary

World Focus is a real route surface:

```text
/home
/worlds
/worlds/:worldId
```

Opening a World from Home or Mondi Overview navigates to the same `/worlds/:worldId` surface.

Required:

- Home is not the visible World Focus background;
- World Focus is not a Home structural overlay;
- route navigation works with no ornamental transition;
- browser history/deep-link behavior remains deterministic;
- the stable end surface is independent from any optional future animation.

---

## 5. Frozen visual-frame geometry — WF-G3

The accepted World-frame reference is three true concentric SVG ellipses centered on the World Focus route surface.

```text
center: cx 50%, cy 50%

outer:  rx 52.25%, ry 90%
origin: rx 50%,    ry 87%
inner:  rx 47.75%, ry 84%
```

Semantics:

- `outer` = external boundary of the reserved future visual-frame band;
- `origin` = canonical reference line for future animation/asset placement;
- `inner` = internal boundary of the reserved visual-frame band.

The `origin` ellipse uses `rx = 50%`; therefore at route mid-height it is mathematically tangent to the left and right route edges. `outer` extends beyond those edges and `inner` remains inside them.

The taller `ry` values deliberately produce elongated corner arcs instead of a rigid circle.

These ellipses are **reference geometry**, not a content container.

---

## 6. Frozen workspace boundary

The real application workspace is rectangular.

Current structural anchors:

```text
standard inline inset: clamp(136px, 14vw, 224px)
compact inline inset:  clamp(76px, 18vw, 112px)
standard block inset:  clamp(32px, 5vh, 64px)
compact block inset:   20px
compact tuning max:    720px
```

Permanent rules:

- workspace is never clipped to a circle or ellipse;
- visual-frame geometry never becomes widget/module layout authority;
- World-specific skin cannot resize the workspace;
- World-specific content cannot resize the shell or visual frame;
- shell controls cannot reauthor workspace geometry;
- transient overlays cannot participate in macro layout.

The current blue workspace fill/border is debug geometry only and is not product skin.

---

## 7. What the workspace will own later

WF0 freezes **where persistent World application work belongs**, not its internal product layout.

Future persistent content such as:

- contextual DANTE AI;
- module composition;
- pinned/adaptive widgets;
- charts and statistics;
- timelines;
- people/places/artifacts/assets projections;
- AI-generated insight surfaces promoted into the World;

must consume `worldFocus.workspace` rather than renegotiate the shell.

Exact inner placement, columns, module sizing, AI placement and personalization behavior remain intentionally open until their own bounded contract is designed.

Working rule:

> **World features consume the World Focus skeleton; they do not renegotiate it.**

---

## 8. Overlay boundary

Future dialogs, drill-downs, temporary AI insights and personalization chrome may use a route-owned overlay layer.

That layer:

- is transient;
- may visually cover workspace content;
- does not own persistent content placement;
- does not change shell dimensions;
- does not change workspace dimensions;
- does not change visual-frame reference geometry.

Do not turn an overlay into a second competing World layout system.

---

## 9. Responsive structural modes

World Focus deliberately has **one macro composition** across current web widths.

### WF0-STANDARD — width >= 721 px

```text
Visual Frame
+ Rectangular Workspace
+ Shell Controls
```

Uses standard workspace inset tuning.

### WF0-COMPACT — width <= 720 px

```text
Visual Frame
+ Rectangular Workspace
+ Shell Controls
```

Uses compact workspace inset tuning only.

The composition does not stack/reparent/swap regions merely because the viewport crosses 720 px.

The 720 px boundary is a tuning boundary, not permission for an undocumented second product surface.

---

## 10. Pressure widths and runtime invariants

The machine-readable pressure matrix covers:

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

At those widths the structural guards must protect at least:

- Global Topbar visible and outside World Focus ownership;
- dedicated `/worlds/:worldId` route;
- no unexpected horizontal page overflow;
- visual-frame bounds equal to the World Focus shell bounds;
- exactly one rectangular workspace;
- workspace contained by the route surface;
- visual frame not clipping workspace;
- stable macro composition on both sides of the 720 px tuning boundary.

---

## 11. Forbidden structural drift

The following must fail review/tests rather than silently ship:

- mounting World Focus as a Home structural overlay;
- rendering a World Focus-owned Global Topbar;
- modifying the Global Topbar from World Focus;
- turning the visual frame into a layout container;
- clipping the workspace to an ellipse;
- replacing the rectangular workspace with a circular layout;
- allowing Back/shell controls to change workspace geometry;
- allowing World-specific skin to change macro geometry;
- allowing World-specific content to change macro geometry;
- allowing transient overlays to participate in persistent layout;
- introducing an undocumented responsive macro mode;
- accidental horizontal page overflow.

---

## 12. Intentionally open

WF0 intentionally does **not** decide:

- workspace inner module composition;
- contextual AI exact placement inside the workspace;
- widget grid/drag/resize behavior;
- AI insight visual grammar;
- drill-down/dialog design;
- final World skin, colors, textures or particles;
- optional entry animation;
- backend/API semantics;
- World profile/config persistence;
- module registry and projection contracts;
- future mobile-native product composition.

These open decisions are not permission to alter WF0 macro ownership.

---

## 13. Executable guards

WF0 uses the same layered approach as H0:

### Q0 — machine-readable drift guard

- `world-focus-structure.contract.json`
- `world-focus-shell-responsive.matrix.json`
- `tests/prototypes/world-focus-preprod-contracts.py`

### Q1 — React ownership/state guard

`world-focus-page.test.tsx` protects required macro regions, structural/geometry version markers, state semantics and absence of obsolete overlay/portal runtime.

### Q2 — browser geometry/route guard

`world-focus.spec.ts` protects route entry, Topbar boundary, no Home overlay, required regions, pressure widths and horizontal-overflow/containment invariants.

Regression guards assert structural relationships, not incidental future visual polish.

---

## 14. Required gate for future structural change

Any intentional WF0 structural change follows:

```text
explicit user approval
→ deliberately update WF0 + machine contracts
→ implementation
→ Q0/Q1/Q2 + relevant feature tests
→ build / CI
→ user visual/manual validation
→ new accepted baseline
```

A green test suite by itself does not authorize structural redesign.

---

## 15. WF0 closure meaning

WF0 is the frozen World Focus skeleton.

From this point, skin, AI, widget/module composition and later backend vertical work must be built **inside** the owned boundaries rather than changing the shell whenever a new feature appears.
