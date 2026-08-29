# DANTE — P1 Global App Shell + Topbar

**Status:** IMPLEMENTATION FROZEN / USER-REVIEWED / POST-POLISH REGRESSION QA PENDING  
**Branch:** `feature/home-react`  
**Frozen implementation checkpoint:** `e11d6c53d2fe1361b37345bbc3f49792541bd45d`  
**Date:** 2026-08-29

## Closure decision

P1 is closed for product/implementation scope. Do not keep polishing the shell while starting the next Home surface unless a bounded regression proves a real defect.

The user accepted the current Topbar direction and explicitly chose to defer any further brand-background color tuning. The approved DANTE master logo must remain unmodified; current Topbar background treatment may be revisited only as later visual polish.

## What P1 now owns

The shared application shell owns:

- persistent Global Topbar outside Home feature ownership;
- pathless application layout and route outlet;
- real router destinations for `/home`, `/worlds`, `/today`, `/profile`, `/settings`;
- local/global-navigation Search shell;
- global Create capability discovery without fake writes;
- application launcher;
- account/menu shell without fake identity/session behavior;
- responsive shell layout, keyboard/focus behavior and shared menu primitives;
- shell-owned visual/theme bridge.

Access `/` remains outside AppShell and is not modified by this pass.

## Final Topbar/Search UX

Normal state:

- DANTE master brand at left;
- Home / Mondi / Oggi primary navigation centered;
- Search represented by a lens icon in utilities;
- Create, deprecated Review, launcher and neutral account icon at right.

Search state:

- click, `/`, or Ctrl/Cmd+K enters search mode;
- primary navigation is temporarily replaced by a wide inline search field;
- no modal and no backdrop;
- input receives focus;
- local application destinations appear immediately below the field;
- Arrow Up/Down, Enter, Escape and click are supported;
- closing restores the normal Topbar and trigger focus where appropriate;
- personal-data/backend search remains explicitly unavailable rather than simulated.

## Brand/account decision

The DANTE symbol and wordmark use the approved master assets. Do not recolor or reinterpret the logo to solve contrast problems.

The account trigger uses a neutral user icon rather than fake initials. Real identity, avatar, session and logout behavior belong to Access/Auth integration.

## Truthful deferred behavior

P1 deliberately does not invent:

- remote/personal-data Search backend semantics;
- Create persistence or domain entities;
- real account/session/logout state;
- a new Review workflow;
- authenticated Access → Home handoff.

These are tracked in `docs/frontend/open-decisions.md`.

## QA evidence and remaining check

Before the later visual/Search polish, the complete frontend gate was green, including lint, typecheck, architecture, generated-source checks, unit tests, formatting, production build and **29/29 Playwright E2E**.

The final P1 polish subsequently changed Search from dialog-based to inline Topbar Search, replaced fake account initials, and adjusted shell/brand presentation. Unit and E2E specifications were updated with that implementation, but the post-polish suite has not yet been rerun in the local WSL worktree at the time of this checkpoint.

Therefore:

- P1 product/implementation scope is frozen;
- do not claim the final post-polish regression run as green until it is actually executed;
- if that run exposes a regression, fix only the bounded P1 defect and return immediately to P2.

## Next pass

**P2 — Day Context Strip / Day Route.**

P2 must preserve the frozen AppShell/Topbar ownership and the accepted Home macro geometry. It should productionize viewed-day context and temporal navigation without duplicating Topbar navigation or inventing backend persistence.
