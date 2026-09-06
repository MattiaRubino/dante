# DANTE — P1 Global App Shell + Topbar

**Status:** IMPLEMENTATION FROZEN / USER-REVIEWED / LEGACY REVIEW CLEANUP APPLIED / CURRENT BRANCH QA REQUIRED  
**Branch:** `feature/home-react`  
**Frozen implementation checkpoint:** `e11d6c53d2fe1361b37345bbc3f49792541bd45d`  
**Date:** 2026-09-02

## Closure decision

P1 is closed for product/implementation scope. Do not keep polishing the shell while starting the next Home surface unless a bounded regression proves a real defect.

The user accepted the current Topbar direction and explicitly chose to defer any further brand-background color tuning. The approved DANTE master logo must remain unmodified; current Topbar background treatment may be revisited only as later visual polish.

A bounded AppShell/Home hygiene cleanup on 2026-09-02 removed the legacy disabled global `Review` affordance, its hard-coded badge, dedicated icon/CSS and localization. That cleanup closes already-deprecated debt; it does not introduce a replacement global Review workflow and does not move Context Rail Resolution into the Topbar.

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
- Create, launcher and neutral account icon at right.

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
- authenticated Access → Home handoff.

These are tracked in `docs/frontend/open-decisions.md`.

The former disabled Global Topbar Review control is no longer a deferred capability. Its open decision was resolved by removal because it duplicated/blurred the accepted Resolution responsibility and had no truthful global workflow behind it.

## QA evidence and remaining check

Before the later visual/Search polish, the complete frontend gate was green, including lint, typecheck, architecture, generated-source checks, unit tests, formatting, production build and **29/29 Playwright E2E**.

Later branch-wide work has repeatedly exercised the shared AppShell through current frontend CI. The 2026-09-02 Review cleanup adds a direct component regression asserting that no `Review` button is rendered. Do not claim the cleanup's final CI as green until the workflow attached to the cleanup commit actually completes.

Therefore:

- P1 product/implementation scope remains frozen;
- Review legacy debt is closed by bounded removal, not redesign;
- if current branch CI exposes a regression, fix only the bounded AppShell defect and return immediately to the active World Focus sequencing.

## Next pass

The historical P1 next-pass label was **P2 — Day Context Strip / Day Route**. Current branch sequencing is governed by `docs/frontend/home/current-checkpoint.md`; at the 2026-09-02 checkpoint World Focus WS0–WS8 is closed and M0 Materialization Mapping is next.

Any later work must preserve the frozen AppShell/Topbar ownership and the accepted Home macro geometry. It must not reintroduce the removed legacy Review affordance without a new explicit product contract.
