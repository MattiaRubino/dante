# C1 Manual Findings — 2026-09-04

**Status:** ACTIVE BINDING MANUAL FINDINGS  
**Branch:** `feature/home-timeline`  
**Current code checkpoint after recovery:** `1e7b7752b69f006a4b632e2e2d3ef1522d30e95e`  
**Checkpoint CI:** Frontend CI #937 / `33905239085` — FULL GREEN  
**C1 manual closure:** NOT YET APPROVED

This document records the 2026-09-04 user findings and the decisions that supersede conflicting 2026-09-03 Create UX assumptions.

## 1. Advanced / recurrence recovery findings

The first 2026-09-04 manual pass found:

1. Advanced expanded into an oversized/tall surface that trapped the workflow and could make navigation/closing difficult.
2. `Opzioni avanzate` was visually over-weighted.
3. Event temporal information was duplicated between base and Advanced.
4. Activity could not express repetition even though repeated Activity intent must be authorable without making Activity the recurrence owner.
5. quota patterns such as N times/week needed a truthful Activity authoring path;
6. Planning Tray drag dimmed Timeline and showed both a carried card and a second ghost/preview.

Recovery decisions implemented:

- base Create remains compact;
- Event time/location appears once;
- common Repeat is available to Event and Activity;
- Event recurrence is Event-owned;
- Activity Repeat is Routine-backed;
- quota uses CP6 `quota_per_period`;
- `Personalizzata…` lives inside `Ripeti` and opens Advanced recurrence depth;
- Planning drag uses one carried card, no scrim and no duplicate ghost;
- Agenda/internal Event parts are structured and mapped to native Timeline subitems;
- per-day all-day lane is used instead of a global strip/fake 24-hour timed block.

## 2. Recurrence materialization finding

The user tested `Ripeti → Ogni giorno` and observed that local Create adds only the first/master card to Timeline.

Diagnosis:

- C1 stores/authors the recurrence specification;
- the local bridge currently materializes the authored master/first placed projection;
- canonical future Occurrences are not generated in the browser;
- CP6/backend recurrence evaluator is the correct future owner of canonical recurring instances.

Decision:

**Do not build a fake browser recurrence engine just to duplicate cards.**

Repeated Activity remains:

```text
Activity intent
→ Routine-backed recurrence
→ future backend evaluator
→ canonical Occurrences
→ future temporal range query
→ Timeline
```

Repeated Event remains Event-owned through the same future evaluator/read-model path.

This limitation must remain visible in engineering/handoff truth, but it does not authorize semantic collapse.

## 3. Create blocking/placement finding

The user then identified a more basic usability problem: while Create was open, the surrounding Home/Timeline effectively became frozen, making it impossible to inspect free time or continue navigating the Timeline during authoring.

Binding decision for the current foundation:

### Simple/base desktop

```text
click +
→ floating simple Create
→ stable initial position
→ Timeline remains interactive/scrollable
```

- simple panel is draggable;
- no modal dimming/freeze;
- backdrop no longer owns outside-click close;
- explicit close/Cancel/Escape paths remain;
- dirty draft still requires explicit discard.

### Advanced desktop

Advanced is a larger floating surface, not a giant modal workspace. It remains bounded and does not freeze Timeline.

The user explicitly rejected building a complex matrix of pinned/floating × simple/advanced states.

A possible **simple-only left pin/dock** has been discussed for later, but it is NOT implemented and is not yet final product authority. Advanced should not be coupled to pinning.

## 4. Interaction-design working rule

The user wants to finish remaining Create polish **one issue at a time**.

Do not turn a single observation into a large feature bundle. Foundation before “cool” capabilities.

Correct iteration:

```text
one user finding
→ agree one behavior
→ implement only that
→ automated green
→ manual check
→ next finding
```

## 5. Current validation

`1e7b7752...` completed Frontend CI #937 / `33905239085` with:

- Quality PASS;
- Mobile PASS;
- Chromium PASS;
- Firefox frozen Timeline PASS;
- Gate PASS.

The current candidate is therefore ready for the next manual UX inspection, but C1 is still OPEN.

## 6. Frozen stop lines

These findings do not authorize changes to:

- PostgreSQL/Alembic/CP6 schema;
- F0 frozen application architecture;
- T1 frozen Timeline behavior;
- canonical backend Occurrence generation;
- Session/Actual runtime;
- provider/notification execution;
- C2 structured detail;
- World Focus or Home macro geometry.
