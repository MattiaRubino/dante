# DANTE — World Focus WF1 Checkpoint

**Status:** IMPLEMENTATION CANDIDATE / AUTOMATED + USER QA PENDING  
**Date:** 2026-08-31  
**Branch:** `feature/home-react`  
**Scope:** WF1 route/shell/entry-transition foundation only

This checkpoint records the WF1 implementation candidate. It does **not** declare WF1 closed until the real frontend gates and user visual/manual review pass.

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

This is deliberate for WF1. It keeps the source route mounted beneath the immersive application surface, so transient Home state is not reconstructed after exit.

`/worlds` without `focus` remains the existing Mondi Overview placeholder. WF1 does not design the Mondi Overview.

## 2. State/lifecycle decision

The source screen remains mounted while World Focus is open.

The underlay is:

- `inert`;
- `aria-hidden`;
- visually covered by the fixed immersive surface.

The persistent AppShell/Topbar also remains mounted so shell geometry does not change, but is hidden from interaction while a validated World Focus state is active.

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

## 3. Home entry behavior

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

## 4. Transition architecture

One shared transition engine is used for every World.

Live entry carries one short-lived in-memory visual snapshot:

```text
world id
entry source
opener client rectangle
```

The snapshot:

- has a five-second TTL;
- is not persisted;
- is not backend state;
- is not part of URL semantics;
- is used only to visually hand the selected Home sphere into the full-screen World Focus.

World variation is declarative and bounded:

```text
accent
motion character
texture family
orbital density
particle density
ambient intensity
```

There is no custom animation component or WebGL scene per World.

The current implementation uses CSS/compositor-friendly transform/opacity and bounded gradient/orbit layers. Richer particle/3D behavior is intentionally deferred until measured value/performance justify it.

`prefers-reduced-motion` removes entry and continuous ornamental animation while preserving the final surface and navigation.

## 5. Current World identity status

The current World Focus catalog is explicitly synthetic pre-backend frontend presentation data.

```text
World Focus fixture id
!= Domain identity
!= backend DTO
!= database row
!= persisted World entity
```

WF2 will establish the explicit frontend application/data-source boundary.

## 6. Current surface contents

WF1 intentionally contains only:

- immersive shell/background;
- back control;
- World identity/title/description;
- empty semantic World canvas boundary;
- explicit loading/error/unavailable shell presentation;
- transition/theme infrastructure.

No production widget composition, AI conversation, Insight, personalization, or backend integration is part of WF1.

## 7. Tests authored

WF1 adds automated specifications for:

- live opener snapshot vs direct-entry fallback;
- back/Escape close semantics;
- select-first/open-second Home behavior;
- Home state preservation through browser back;
- opener focus restoration;
- pointer drag not opening World Focus;
- keyboard entry;
- direct `/home?focus=...` fallback;
- loading/error/unavailable shell-state semantics;
- reduced-motion usability.

These tests are **authored but not claimed green by this checkpoint** until executed in the real worktree.

## 8. Required local gate

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

Use the actual repository script names if the workspace aggregate differs.

## 9. Required user visual/manual gate

At minimum validate:

1. center `Musica`, activate it again, inspect expansion;
2. browser/back control returns to the same Home state;
3. AI collapsed/expanded state survives;
4. active World remains selected after return;
5. focus returns to the opener after close/back;
6. dragging a World does not open the focus;
7. keyboard activation works select-first/open-second;
8. direct `/home?focus=music` is usable;
9. reduced-motion route remains clear and usable;
10. compact and large desktop do not clip the shell;
11. transition quality is high enough without adding heavier rendering technology.

## 10. Exclusions retained

WF1 authorizes no:

- backend/API work;
- database/Alembic change;
- provider integration;
- real LLM execution;
- World Domain entity;
- Mondi Overview design;
- widget/module implementation beyond the empty canvas shell;
- Timeline/Orientation/Context Rail redesign.

Do not advance to WF2/WF3 closure language until WF1 QA is actually earned.
