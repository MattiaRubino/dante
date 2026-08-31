# DANTE — World Focus WF1 Checkpoint

**Status:** IMPLEMENTATION CANDIDATE / USER VISUAL QA PENDING  
**Date:** 2026-08-31  
**Branch:** `feature/home-react`  
**Scope:** WF1 route/shell/entry-transition foundation only

This checkpoint records the current WF1 implementation candidate. It does **not** declare WF1 closed until the real frontend gates and user visual/manual review pass.

## 1. Non-negotiable product boundary

World Focus is an immersive depth surface for one selected World.

It is not the Mondi Overview and it is not a new Domain entity.

The persistent application topbar is outside World Focus ownership and is **untouchable** by the World Focus feature:

```text
World Focus MUST NOT
- hide the topbar
- recolor the topbar
- restyle the topbar
- change its blur/material
- change its z-index/layer ownership
- replace or recompose it
```

World Focus always occupies the application area **below** the existing topbar.

## 2. Start / optional transition / end contract

Navigation and presentation are deliberately separate:

```text
START
source screen + selected World

    ↓ route/navigation always works

OPTIONAL TRANSITION
camera-like focus + portal presentation

    ↓

END
stable World Focus surface
```

The middle transition is ornamental presentation only.

The start and end states MUST remain correct when the transition is skipped entirely.

No backend, Domain, authorization, routing, persistence, or application behavior may depend on the animation completing.

## 3. Entry gesture contract

Desktop mouse:

```text
single click
-> normal carousel selection/navigation

double click on a World
-> open World Focus
```

Keyboard remains independently accessible:

```text
Enter on an inactive World
-> select/center

Enter on the active World
-> open World Focus
```

Touch/pen must not rely on browser double-tap semantics:

```text
first tap
-> select/center

subsequent tap on the active World
-> open World Focus
```

Pointer travel above the bounded click threshold remains drag/navigation and must not open World Focus.

## 4. Route/lifecycle contract

World Focus remains route-backed through validated application search state:

```text
/home?focus=<world-id>
/worlds?focus=<world-id>
```

The source route remains mounted beneath the immersive surface so transient Home state is preserved rather than reconstructed.

While World Focus is active the Home underlay is:

- still mounted;
- `inert`;
- `aria-hidden`;
- never treated as canonical World Focus content.

Browser history owns live-entry back behavior. Direct/deep-link loads without a live opener snapshot have a deterministic close path that removes only `focus`.

## 5. Motion preference contract

WF1 establishes the frontend preference contract:

```text
WorldFocusMotionPreference
= immersive | instant
```

Default:

```text
immersive
```

`instant` means:

```text
START
-> END
```

with no portal/camera transition in the middle.

The current pre-backend preference is persisted as presentation configuration under:

```text
dante.preferences.world-focus-motion.v1
```

This is UI/product preference state only. It is not Domain truth and it does not justify a database change in the current phase.

The future Settings surface must use this same typed contract instead of inventing a second switch.

`prefers-reduced-motion: reduce` always suppresses the ornamental transition regardless of the stored preference.

Navigation remains available in every mode.

## 6. Transition v3 visual grammar

The transition target is no longer a generic overlay expansion.

The intended choreography is:

```text
selected World
-> source camera visually locks toward it
-> World grows toward the focus center
-> energetic/cosmic aperture ignites from that World
-> portal/tunnel expands through the application area
-> source Home recedes
-> stable World Focus atmosphere resolves
```

The topbar is never part of this choreography.

The source camera effect is implemented only on the Home underlay beneath the topbar.

## 7. Rendering architecture

The transition uses one bounded procedural WebGL2 effect shared by every World.

No Three.js scene, Rive runtime, permanent particle engine, video overlay, or per-World animation implementation is introduced for WF1.

The WebGL renderer:

- mounts only for the immersive entry;
- targets roughly 1.24 seconds;
- caps device pixel ratio;
- disables depth/stencil/antialias buffers not needed by the effect;
- does not preserve the drawing buffer;
- avoids GPU readback;
- cleans up shaders/program/VAO;
- requests context loss after teardown;
- falls back to bounded CSS presentation when WebGL2 is unavailable or rejected.

The expensive transition renderer does not remain mounted in the settled World Focus.

## 8. Stable end state

The end state is independent from WebGL.

WF1 currently leaves a static, declarative World anchor beneath the topbar to visually retain the selected World after the transition ends.

The end anchor:

- is ordinary DOM/CSS presentation;
- uses the World accent/theme parameters;
- does not require a running render loop;
- is also present when entry mode is `instant`;
- is placeholder visual structure for WF1, not a final content/module design decision.

The production World canvas remains intentionally empty in WF1.

## 9. World variation boundary

One shared transition grammar is used for every World.

Allowed declarative variation remains bounded to presentation parameters such as:

```text
accent
motion character
texture family
particle density
ambient intensity
```

There is no custom animation code path per World.

## 10. Current World identity status

The current World Focus catalog remains synthetic pre-backend frontend presentation data.

```text
World Focus fixture id
!= Domain identity
!= backend DTO
!= database row
!= persisted World entity
```

WF2 establishes the explicit frontend application/data-source boundary.

## 11. Shell states

World Focus explicitly represents:

```text
loading
ready
error
unavailable
```

`loading` exposes `aria-busy` plus a status message. `error` and `unavailable` remain distinct states and do not masquerade as empty content.

Focus moves into the immersive surface on entry. On exit, focus returns to the live opener when it still exists.

## 12. Automated pressure authored

WF1 coverage includes or is expected to include:

- double-click desktop entry;
- single click remains selection only;
- keyboard select/open behavior;
- touch/pen select/open boundary;
- live opener vs direct-entry fallback;
- persisted `instant` preference;
- reduced-motion suppression;
- topbar remains visible;
- Home state preservation through browser back;
- opener focus restoration;
- pointer drag not opening World Focus;
- shell loading/error/unavailable semantics.

These tests are not claimed green for the v3 candidate until executed in the real worktree.

## 13. Required visual gate

Before WF1 can close, validate at minimum:

1. the topbar is pixel-for-pixel unaffected during the entire sequence;
2. single mouse click does not open World Focus;
3. double click does open it;
4. the visual motion appears to originate from the actual selected World;
5. the source scene appears to focus toward the World rather than merely fade;
6. the portal reads as one coherent aperture/tunnel, not layered random effects;
7. the transition resolves cleanly into the stable end state;
8. the static end anchor remains convincing when the animation is disabled;
9. `instant` feels immediate rather than broken;
10. reduced motion remains fully usable;
11. browser back restores the previous Home state.

## 14. Exclusions retained

WF1 authorizes no:

- backend/API work;
- database/Alembic change;
- provider integration;
- real LLM execution;
- World Domain entity;
- Mondi Overview design;
- production widget/module composition;
- Timeline/Orientation/Context Rail redesign;
- topbar redesign of any kind.

Do not advance to WF2/WF3 closure language until WF1 user visual QA is actually earned.
