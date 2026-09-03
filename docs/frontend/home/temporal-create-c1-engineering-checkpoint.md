# DANTE — Temporal Create C1 Engineering Checkpoint

**Status:** ACTIVE RE-ARCHITECTURE CHECKPOINT — AUTOMATED PARTIAL PASS  
**Date:** 2026-09-03  
**Repository:** `MattiaRubino/dante`  
**Branch:** `feature/home-timeline`  
**Worktree:** `/home/mattia/projects/dante-timeline`  
**Current code checkpoint:** `bd9bc6db13301763393c5345685dd38a1837aaaa`  
**Frontend CI:** #759 / `33744558905` — Quality PASS, Mobile PASS, Chromium 83/96 with 13 stale-contract failures, Firefox skipped, Gate FAIL

## 1. Purpose

This checkpoint replaces the stale claim that C1 is in final engineering pass.

The 2026-09-02 implementation did reach full automated green, but the user manual product review on 2026-09-03 produced a legitimate `C1 MANUAL FAIL` and triggered an information-architecture re-architecture.

Current product authority is `temporal-create-c1-rearchitecture-2026-09-03.md`.

## 2. Historical engineering baseline

Preserve as regression evidence:

- old implementation/harness `2b910092ecd70de74338427924666a965938ba9f`;
- CI #676 FULL GREEN;
- old docs descendant `27dd5093d21b0a49c8413068aacca139fb2366a4`;
- CI #680 FULL GREEN.

The old baseline proved F0/recurrence/Context/Timeline regression behavior under the old UX. It is not the current closure candidate.

## 3. Current re-architecture engineering goals

### Create IA

- title first;
- extensible type registry/grid;
- actionable types only;
- sensible default fields immediately visible;
- base + Advanced user-facing disclosure;
- conditional nested fields;
- no dead/deferred owner UI.

### Activity

- Orario/Tutto il giorno/Da collocare;
- placement chosen by user remains authoritative;
- execution/session settings conditional;
- no Activity recurrence.

### Event

- timed/all-day;
- sensible start/end defaults;
- location/Context in base path;
- quick recurrence;
- CP6 custom recurrence behind custom/Advanced;
- Agenda/internal parts still to finish.

### Planning Tray

- anchored desktop popover;
- mobile bottom sheet;
- direct remove;
- carried-card drag;
- same identity placement;
- Escape and Undo correctness.

### All-day

- per-day lane;
- lane consumes geometry;
- minute zero below lane;
- no global header strip;
- no fake 24-hour timed card.

## 4. Current implementation chain

- `0e21164355b39d76d27b2192cb5d510e77e765f8` — type-driven base flow;
- `0d863a3765c88ded440bae45ab6a1d1e6d1257c2` — exact advanced duration;
- `586105ca46cd8f3b5f7fbeb663892032c9eb37f0` — conditional execution options;
- `757a5d198353544cac4568f7804e2c39e1d86ea5` — quick Event recurrence;
- `788deee039324631575e52f871ad476a0e9165a9` — anchored Planning Tray;
- `a0cf00ef5507ff6eab4b00d5b97749e7d8d19aa2` — carried-card drag;
- `8413f2f0a2c7c6a2b82b6c06216039977cef437b` — direct remove;
- `2ec74d25f57e8b749273e0baf10e3f3d2eaa57f7` — explicit placement/split execution test groundwork;
- `833e59a8df8063bdcfb359c8b70250619cc74e7a` — all-day lane geometry;
- `87aa3925fe6e275d230781e8f32a95953149a4bb` — per-day lane preparation;
- `bd9bc6db13301763393c5345685dd38a1837aaaa` — geometry integrated into viewport runtime.

## 5. Current code facts

### Temporal Create

- product composer reports `base` or `advanced` presentation;
- old internal `TemporalCreateSurface` naming may remain below UI and can be refactored later if doing so materially reduces complexity; do not change solely for cosmetic naming;
- type selection is no longer the old `<select>` contract;
- Activity/Event base fields are type-driven;
- quick Event recurrence has landed;
- conditional execution fields have landed;
- deferred owner UI has been removed from the normal Advanced path.

### Planning Tray

The product implementation has landed anchored popover and carried-card interaction checkpoints. The Playwright suite has not yet been migrated to those new accessible controls/geometry.

### All-day runtime

`applyTimelineAllDayGeometry` now transforms the base rendered-day list using `state.allDayItems` and active filters.

The offset time mapper means:

```text
map(minute) = allDayLaneHeight + baseMapper.map(minute)
```

and inverse mapping subtracts the all-day offset.

This is the correct foundation for Now/zoom/scroll/drag correctness.

The visual lane remains unfinished: geometry without visual lane is not a product-complete feature.

## 6. CI #759 analysis

Quality PASS proves:

- format/active Home checks;
- lint;
- typecheck;
- architecture;
- generated-source drift;
- unit suite;
- production build;
- diff check;
- repository mutation check.

Mobile Bundle PASS also remains green.

Chromium ran 96 tests:

- 83 passed;
- 13 failed.

The failing tests are concentrated in Temporal Create and assert obsolete pre-refactor controls such as:

- `Dettagli e pianificazione`;
- header `+/-` disclosure;
- `Aperta, senza collocazione` old radio;
- `surface=quick`;
- old Type `<select>`;
- old Full progression;
- old all-day strip contract.

The correct fix is to migrate those tests to the new contract, not to restore the old product.

Firefox frozen Timeline was skipped because the Chromium job failed; therefore the current checkpoint is not full green.

## 7. Current engineering backlog

1. mount new per-day all-day lane visually;
2. final all-day CSS;
3. remove transitional global header-layer implementation;
4. migrate E2E to base + Advanced/type grid;
5. Planning Tray v2 E2E;
6. Orario + Divisibile regression;
7. quick recurrence/custom CP6 E2E;
8. Event Agenda/internal parts;
9. Reminder/Alarm semantic decision;
10. full CI including Firefox frozen;
11. candidate documentation reconciliation;
12. new manual acceptance.

## 8. Engineering quality bar

Do not:

- add sleeps to hide synchronization defects;
- weaken tests without replacing the protected contract;
- introduce fake backend/provider success;
- let UI convenience collapse Activity/Event/Routine semantics;
- make all-day a 24-hour timed Schedule;
- let session structure silently unschedule placed Activity;
- generate recurrence Occurrences in browser;
- optimize bundle size by adding asynchronous draft/focus complexity without measured need.

## 9. Gate

```text
ENGINEERING CHECKPOINT = PARTIAL PASS
C1 RE-ARCHITECTURE ACTIVE
NOT MANUAL-TEST READY
NOT FROZEN / CLOSED
C2 BLOCKED
```
