# DANTE — Home Timeline T1 Frozen Behavior Contract

- Status: **FROZEN — USER ACCEPTED BASELINE**
- Workstream: `feature/home-react`
- Behavioral baseline accepted after: `6e7795eab62c828f8dd0b010d893164dfa31b9b9`
- Scope: Home Timeline interaction/geometry behavior already validated during T1 hardening

This document is a change-control boundary. It does not prevent internal refactoring; it prevents accidental observable regressions.

## Approval rule

Any change that intentionally alters one of the frozen behaviors below requires explicit user approval **before the first production write**.

Implementation-only work may proceed without a product-contract change only when it preserves the frozen behavior and is covered by the existing regression gates.

Regression tests protecting this contract must not be weakened or rewritten to make an accidental behavior pass.

## Frozen interaction contract

### Card body / focus / drag

- free card body is the focus/select and drag surface;
- a normal card drag is one gesture: pointer down → hold → move; no preparatory click is required;
- drag must activate on the **first gesture** even when another card currently owns focus;
- a simple click on another card while one card is focused performs **deselect first**: it must not simultaneously focus the target or open a nested action;
- after focus has been dismissed, a subsequent normal card-body click may focus the target card;
- a completed drag must not be followed by an accidental focus/deselect click caused by the synthetic post-drag click;
- drag remains custom Timeline behavior, not browser-native HTML drag.

### Explicit action regions

- title opens the event Detail action and must not be treated as generic card-body drag/focus input;
- time text opens the time editor and must not be treated as generic card-body drag/focus input;
- subitem and expander controls retain their explicit actions;
- while surrounding cards are semantically inactive because another card owns focus, a simple click must respect the deselect-first rule rather than opening their nested action.

### Drag lifecycle

- no native browser drag ghost;
- no text selection during event drag;
- only one custom drag overlay exists for one active event move;
- Escape, pointer cancellation, visibility loss or genuine window deactivation may cancel an active drag without leaving leaked listeners, overlays or `is-drag-source` state;
- ordinary focus transfer between elements inside the same window must not cancel the pending drag gesture.

### Move semantics

- event move follows the accepted prototype grammar: drop commits the move and feedback exposes undo;
- no confirmation-before-drop is introduced for drag without explicit approval;
- the anchored time editor remains a separate confirmable time-edit interaction.

## Frozen geometry contract

### Compact overlap

- overlapping events occupy deterministic bounded lanes;
- a small overlap cluster must not spread events arbitrarily across the full Timeline canvas;
- moving/focusing an event must not cause unrelated lateral jumps;
- intrinsic card width remains bounded by the Timeline layout/runtime policies rather than browser content feedback loops.

### Expanded groups

- expanded group headers and event columns use the same published geometry;
- event group columns align with their corresponding header chips;
- Timeline grid and group-header scroller remain horizontally synchronized;
- no separate near-equivalent geometry calculation may be introduced that causes header/event drift.

## Frozen visual/product boundaries

The following are not side effects that may be introduced during unrelated work:

- no new Peek layer between card and Detail;
- no arbitrary redesign of card density, typography, spacing or lane distribution;
- no new whole-card action that steals title/time/subitem semantics;
- no Timeline visual/layout change justified only as cleanup, modernization or refactor.

Those may be revisited only as explicit, separately approved product scopes.

## Executable regression guards

Primary browser regression file:

`apps/web/e2e/timeline-interactions.spec.ts`

It must permanently protect at least:

1. custom dragging never falls back to native browser drag/selection;
2. focused-card state never consumes the first drag gesture on another card;
3. simple click on another card preserves deselect-first semantics;
4. compact overlap cards stay in a bounded deterministic cluster;
5. expanded header/event geometry and horizontal scrolling stay aligned.

The Timeline interaction contract runs in normal Chromium Web E2E and additionally in Firefox CI because pointer/focus behavior can differ across engines.

Relevant unit/component suites remain complementary and should cover reducer/state/layout semantics independently of browser interaction.

## Required gate before handoff

For any commit touching production Timeline paths, the assistant must complete the relevant automatic checks before asking the user to pull and manually validate. At minimum, depending on scope:

- format/lint for touched files;
- typecheck;
- Timeline unit/component tests;
- production build;
- Timeline Playwright regression suite;
- Firefox Timeline contract when pointer/focus/drag behavior is touched.

The user manual/visual check remains the final acceptance gate. A test pass never authorizes an observable change to this frozen contract.
