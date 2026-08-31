# DANTE — World Focus WF1 Checkpoint

**Status:** IMPLEMENTATION CANDIDATE / SECOND VISUAL QA PENDING  
**Date:** 2026-08-31  
**Branch:** `feature/home-react`  
**Scope:** WF1 route/shell/entry-transition foundation only

This checkpoint records the current WF1 implementation candidate. It does **not** declare WF1 closed until the second real visual/manual review passes.

## 1. Implemented boundary

WF1 establishes:

```text
Home centered World
-> select once to center
-> activate centered World again
-> route-backed immersive World Focus
-> close / browser back
-> exact still-mounted Home context
```

World Focus is represented as validated search/navigation state on the owning application destination:

```text
/home?focus=<world-id>
/worlds?focus=<world-id>
```

This keeps the source route mounted beneath the immersive application surface, so transient Home state is not reconstructed after exit.

`/worlds` without `focus` remains the existing Mondi Overview placeholder. WF1 does not design the Mondi Overview.

## 2. Global Topbar invariant

The global AppShell Topbar is **not part of World Focus** and must not change when World Focus opens.

Non-negotiable invariant:

```text
Topbar identity
Topbar geometry
Topbar visuals
Topbar interaction
Topbar z-order

remain exactly the normal AppShell behavior.
```

World Focus occupies the application surface **below** the accepted 64px global Topbar and has a lower stacking level than the Topbar.

The earlier WF1 candidate that hid the Topbar was rejected during user visual QA and that special-case CSS/route-shell behavior has been removed.

## 3. State/lifecycle decision

The source screen remains mounted while World Focus is open.

The underlay is:

- `inert`;
- `aria-hidden`;
- visually covered only below the global Topbar.

Browser history owns live-entry back behavior. A direct/deep-link load without a live opener snapshot has a deterministic fallback close that removes only `focus`.

World Focus explicitly represents the WF1 shell lifecycle states:

```text
loading
ready
error
unavailable
```

`loading` is exposed with `aria-busy` plus a status message. `error` and `unavailable` remain distinct alert states and do not masquerade as empty content.

Focus moves into the immersive surface on entry. On exit, restoration is deferred until the still-mounted underlay has left its `inert` state, then returns to the live opener when it still exists.

## 4. Home entry behavior

The accepted Home carousel remains unchanged.

WF1 adds a bounded entry bridge at the Home shell boundary:

```text
inactive World activation
-> existing carousel selection/centering only

already active centered World activation
-> OPEN_WORLD_FOCUS intent at route boundary
```

Pointer travel above the click threshold remains drag/navigation and must not open World Focus.

Keyboard activation follows the same select-first/open-second rule.

The bridge emits only presentation identity + opener geometry. It does not create backend/Domain identity.

## 5. Transition architecture — v2 after visual rejection

The first CSS-only orbit/portal candidate was rejected during user visual QA because it did not reach the required premium/cinematic quality.

The replacement is a bounded GPU-driven entry engine based on established modern WebGL transition techniques:

```text
real clicked World origin
-> radial SDF expansion
-> procedural noise deformation
-> turbulent energy boundary
-> polar tunnel / radial streak field
-> world-color activation flash
-> World Focus atmosphere settles underneath
-> GPU transition layer tears down
```

Implementation rules:

- one shared WebGL2 fragment-shader engine for every World;
- no Three.js scene graph;
- no Rive/WASM runtime;
- no downloaded video/VFX dependency;
- no per-World animation implementation;
- no continuous WebGL rendering after entry;
- WebGL canvas exists only during the approximately one-second live entry;
- renderer resources and WebGL context are explicitly released after teardown;
- `preserveDrawingBuffer` is disabled;
- depth, stencil and antialias buffers are not requested;
- `failIfMajorPerformanceCaveat` forces a lightweight fallback on unsuitable devices;
- device pixel ratio is bounded;
- resize/layout geometry is measured outside the per-frame hot path;
- WebGL-unavailable devices receive a bounded CSS fallback;
- reduced-motion users skip the ornamental live-entry engine entirely.

The visual direction follows researched GPU transition patterns rather than arbitrary DOM decoration: expanding signed-distance masks, noise-deformed boundaries, shader-driven ripple/reveal fields and GPU-controlled progress.

## 6. World variation

World variation remains declarative and bounded:

```text
accent
motion character
texture family
orbital density (legacy profile field; not a DOM orbit count)
particle density
ambient intensity
```

The same engine reads the profile and changes energy, density and motion characteristics without introducing a custom renderer per World.

The current catalog remains explicitly synthetic pre-backend frontend presentation data:

```text
World Focus fixture id
!= Domain identity
!= backend DTO
!= database row
!= persisted World entity
```

WF2 will establish the explicit frontend application/data-source boundary.

## 7. Current surface contents

WF1 intentionally contains only:

- immersive application surface below the unchanged Topbar;
- back control;
- World identity/title/description;
- empty semantic World canvas boundary;
- explicit loading/error/unavailable shell presentation;
- GPU entry engine + fallback;
- final ambient/theme infrastructure.

No production widget composition, AI conversation, Insight, personalization, or backend integration is part of WF1.

## 8. Automated pressure

WF1 specifications cover:

- live opener snapshot vs direct-entry fallback;
- back/Escape close semantics;
- select-first/open-second Home behavior;
- Home state preservation through browser back;
- opener focus restoration;
- pointer drag not opening World Focus;
- keyboard entry;
- direct `/home?focus=...` fallback;
- loading/error/unavailable shell-state semantics;
- reduced-motion usability;
- Topbar remaining visible and geometrically above World Focus;
- live entry moving from `entering` to `settled`.

The previous worktree run before the v2 visual replacement established green lint, typecheck, architecture, generated checks, 90/90 unit tests and build; the single remaining E2E failure at that point belonged to the independent Access workstream. The v2 transition must be rerun through the same gates before WF1 closure.

## 9. Required local gate

Before WF1 can close:

```text
pnpm format:check
pnpm lint
pnpm typecheck
pnpm architecture:check
pnpm generated:check
pnpm test
pnpm build
pnpm test:e2e:web
git diff --check
```

Independent Timeline/Access workstream failures must be attributed accurately rather than silently fixed from WF1.

## 10. Required second user visual/manual gate

At minimum validate:

1. the global Topbar is visually and behaviorally unchanged before/during/after World Focus;
2. center `Musica`, activate it again and judge the new GPU entry;
3. verify the effect clearly originates from the selected sphere rather than the screen center;
4. compare `Musica` and `Viaggi` for one coherent engine with different character;
5. ensure the transition reads as entering a World, not opening a modal/page;
6. verify there is no obvious frame drop or delayed interaction on the target machine;
7. browser/back control returns to the same Home state;
8. AI collapsed/expanded state survives;
9. Timeline state survives;
10. active World remains selected after return;
11. focus returns to the opener after close/back;
12. dragging a World does not open the focus;
13. keyboard activation works select-first/open-second;
14. direct `/home?focus=music` remains usable without needing an opener;
15. reduced-motion remains clear and usable;
16. compact and large desktop do not clip the shell.

## 11. Exclusions retained

WF1 authorizes no:

- backend/API work;
- database/Alembic change;
- provider integration;
- real LLM execution;
- World Domain entity;
- Mondi Overview design;
- widget/module implementation beyond the empty canvas shell;
- Timeline/Orientation/Context Rail redesign;
- Topbar redesign.

Do not advance to WF2/WF3 closure language until WF1 QA is actually earned.
