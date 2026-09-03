# DANTE — Temporal Create C1 Traceability

**Status:** ACTIVE RE-ARCHITECTURE TRACEABILITY — NOT CLOSURE GRADE YET  
**Date:** 2026-09-03  
**Branch:** `feature/home-timeline`  
**Current code checkpoint:** `bd9bc6db13301763393c5345685dd38a1837aaaa`  
**Checkpoint CI:** #759 / `33744558905` — Quality PASS, Mobile PASS, Chromium 83/96 with 13 stale-contract failures, Firefox skipped, Gate FAIL  
**Scope:** pre-backend manual Timeline Create C1 re-architecture

## 1. Purpose

This file maps current C1 product requirements to semantic authority, implementation checkpoints and required automated proof.

It is no longer a closure record. The old closure-grade traceability was superseded by the 2026-09-03 manual fail.

Primary authority:

- `temporal-create-c1-rearchitecture-2026-09-03.md`;
- `temporal-create-c1-manual-findings-2026-09-03.md`;
- `temporal-live-status.md`;
- `temporal-create-handoff.md`.

## 2. Stable semantic mapping

| Product concept | DANTE authority | Non-collapse rule |
| --- | --- | --- |
| Activity | native LR owner | not Event, not Routine, not Schedule |
| Event | native LR owner | not Activity, recurrence may be Event-owned |
| Routine | native LR owner | owns persistent repeated Activity intent |
| Schedule/placement | MaterialState facet | planned placement != Actual |
| Session | native owner/runtime concept | execution != Schedule |
| Actual | realization record | planned != happened |
| Event recurrence | CP6/M4 | specification != generated Occurrence |
| Routine recurrence | CP6/M4 | repeated Activity != `Activity.repeat` |
| Occurrence | backend-generated/explicit event in recurrence flow | browser C1 does not canonically generate |
| Context | grouping/filter membership | Context != appearance color |
| Appearance | presentation override | appearance != category/Context |
| Provider intent | frontend authored intent | intent != provider execution |

## 3. Manual-fail requirement mapping

### R1 — Remove misleading header `+`

User finding: `+` beside close looked like another add action.

Target:

- simple header with close only;
- Advanced is a content-level disclosure action.

Implementation family:

- type-driven base flow from `0e211643...` and subsequent Create refactor.

Required proof:

- E2E asserts no header expansion `+` beside close;
- Advanced toggle remains keyboard accessible.

### R2 — Title first + extensible type chooser

Target:

```text
Title
→ Type registry/grid
→ selected-type fields
```

Implementation:

- `0e21164355b39d76d27b2192cb5d510e77e765f8`.

Required proof:

- title receives initial focus;
- Activity/Event are selectable through type tiles/grid rather than old select;
- layout can accommodate future actionable types;
- unavailable owner types are absent, not disabled.

### R3 — No wizard tax / sensible defaults

Activity default:

- Orario selected;
- date/time/duration visible;
- Context visible.

Event default:

- timed selected;
- date/start/end visible;
- Context/location/repeat available.

Required proof:

- base path can create normal Activity/Event without entering Advanced;
- changing all-day/unplaced removes irrelevant controls rather than disabling them.

### R4 — One coherent base + Advanced model

Target:

- no user-visible Quick/Expanded/Full mental model;
- one Create editor;
- `Opzioni avanzate` expands relevant depth.

Implementation:

- Create composer currently reports product surfaces as `base` / `advanced` even if lower model types still preserve old internal presentation names.

Required proof:

- E2E protects `base` → Advanced → base round-trip without draft loss;
- no old `Dettagli e pianificazione`/`Editor completo` dependency.

### R5 — Activity placement/execution non-collapse

Target:

```text
Orario + Divisibile → remains placed
```

Implementation/checkpoint:

- `2ec74d25f57e8b749273e0baf10e3f3d2eaa57f7` regression groundwork.

Required proof:

- create exact-time Activity;
- enter Advanced;
- choose splittable;
- author min/max session values;
- submit;
- native Timeline card remains at authored placement;
- does not enter Planning Tray.

### R6 — Conditional Activity execution controls

Implementation:

- `586105ca46cd8f3b5f7fbeb663892032c9eb37f0`.

Required proof:

- indivisible hides multi-session-only controls;
- splittable reveals them;
- hiding does not destroy valid authored values unexpectedly unless normalization explicitly requires it.

### R7 — Quick Event recurrence

Implementation:

- `757a5d198353544cac4568f7804e2c39e1d86ea5`.

Target quick choices:

- never;
- daily;
- weekly;
- monthly;
- yearly;
- custom.

Required proof:

- daily/weekly/monthly/yearly map to Event calendar recurrence without deep form navigation;
- `Personalizza…` exposes custom CP6 depth;
- custom values round-trip through Advanced;
- no browser Occurrence generation.

### R8 — Planning Tray anchored to trigger

Implementation:

- `788deee039324631575e52f871ad476a0e9165a9`.

Required proof:

- desktop panel geometry is anchored to trigger;
- it does not become detached far-right drawer;
- mobile remains bounded bottom sheet;
- focus/open/close behavior is accessible.

### R9 — Carried-card planning drag

Implementation:

- `a0cf00ef5507ff6eab4b00d5b97749e7d8d19aa2`.

Required proof:

- tray recedes during active drag;
- carried card follows pointer;
- Timeline planning mode foregrounds target;
- snapped target preview exists;
- Escape cancels with no mutation;
- drop mutates placement of same identity exactly once;
- Undo returns same Activity to unplaced state.

### R10 — Direct remove action

Implementation:

- `8413f2f0a2c7c6a2b82b6c06216039977cef437b`.

Required proof:

- direct remove `×`/trash available;
- explicit confirmation;
- cancel is non-mutating;
- confirm removes local projection;
- Undo restores same projection.

### R11 — Per-day all-day lane

Implementation chain:

- `833e59a8df8063bdcfb359c8b70250619cc74e7a` — geometry model;
- `87aa3925fe6e275d230781e8f32a95953149a4bb` — lane preparation;
- `bd9bc6db13301763393c5345685dd38a1837aaaa` — geometry integrated into rendered Timeline days.

Current state:

- mapper/height/offset support exists;
- visual `TimelineAllDayLane` exists;
- visual lane still needs per-day mounting;
- old transitional global header-layer code/CSS must be removed.

Required proof:

- lane is inside each relevant Timeline day, not global header;
- minute zero begins below lane;
- all-day card does not enter timed events layer;
- multi-day continuation semantics;
- Now/scroll/zoom anchors remain stable;
- Activity unplaced remains semantically distinct from Event all-day.

### R12 — No dead deferred-owner UI

Target:

- no normal Create section saying owner vertical is unavailable;
- no disabled Routine/Project/etc primary tiles unless product has a real action.

Architecture may retain typed handoff registry.

Required proof:

- base/Advanced UI contains no `Richiede il verticale proprietario` dead block;
- deferred handoff contracts remain code-level/documented seams.

### R13 — Event Agenda/internal parts

Status: NOT YET COMPLETE.

Target:

- author ordered Event-internal parts such as Listening/Orale/Scritto;
- no universal generic sub-entity;
- native Timeline may present Event `subitems` when mapped explicitly.

Required proof to add with implementation:

- add/edit/remove/reorder or minimum coherent ordered authoring;
- draft round-trip;
- native Event shows parts appropriately;
- no independent Schedule/Actual identity fabricated for agenda parts.

### R14 — Reminder/Alarm

Status: SEMANTIC REVIEW REQUIRED BEFORE UI.

Target decision:

- either define a truthful reminder-intent owner/application boundary and expose it with explicit no-delivery semantics;
- or keep it hidden/deferred.

Forbidden:

- claiming alarm is active;
- claiming notification delivery;
- fake provider/device integration.

## 4. CP6 recurrence traceability

C1 Event custom recurrence must continue to cover all four families:

| UI family | CP6 family |
| --- | --- |
| Calendar / civil time | `calendar_wall_clock` |
| Elapsed interval | `elapsed_interval` |
| Quota per period | `quota_per_period` |
| Cyclic positions | `cyclic_positional` |

Event recurrence details already modeled include:

- daily/weekly/monthly/monthly ordinal/yearly;
- weekday sets;
- positive interval;
- open/until/count termination;
- elapsed minutes;
- quota count/period/period interval;
- floating/named-zone/absolute-UTC quota frame;
- week start;
- named-zone period timezone;
- cyclic day/week unit;
- cycle length and multiple positions.

Activity must never expose this editor.

## 5. F0 mutation traceability

Planning Tray placement must reuse F0 placement mutation, not local visual duplication.

Expected lifecycle:

```text
same Activity projection
placement = null
→ replacePlacement(...)
→ same projection identity/revision advances
→ native Timeline card
→ mutation Undo
→ same Activity returns to placement = null
```

Delete similarly uses real projection removal/Undo.

## 6. Current automated evidence

Historical pre-refactor:

- #676 FULL GREEN on `2b910092...`;
- #680 FULL GREEN on `27dd5093...`.

Current re-architecture checkpoint:

- `bd9bc6db13301763393c5345685dd38a1837aaaa`;
- CI #759 / `33744558905`;
- Quality PASS;
- Mobile PASS;
- Chromium 83/96 PASS;
- 13 C1 failures caused primarily by old product locators/vocabulary;
- Firefox frozen skipped;
- Gate FAIL.

The current red is real and must stay red until replacement coverage for the new contract exists.

## 7. Test migration matrix

Rewrite, do not delete:

| Old test assumption | New assertion |
| --- | --- |
| `surface=quick` | `surface=base` |
| `Dettagli e pianificazione` | `Opzioni avanzate` |
| header `+/-` depth | no header depth action; content Advanced toggle |
| Type `<select>` | type registry/grid tile/button |
| `Aperta, senza collocazione` old control | current `Da collocare` placement choice |
| global all-day strip | per-day all-day lane |
| old Full mobile editor | base + Advanced mobile editor |
| tray far-side panel | anchored desktop popover / mobile bottom sheet |
| planning ghost target only | carried card + target slot |
| `...` delete menu | direct remove action + confirmation |

## 8. Closure traceability

C1 cannot move to closure grade until every ACTIVE requirement has:

- implementation;
- automated proof;
- full CI green;
- current docs;
- one coherent user manual acceptance.

Current status:

```text
TRACEABILITY ACTIVE
NOT CLOSURE GRADE
C1 RE-ARCHITECTURE ACTIVE
C2 BLOCKED
```
