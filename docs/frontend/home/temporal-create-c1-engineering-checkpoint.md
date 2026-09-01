# DANTE — Temporal Create C1 Engineering Checkpoint

**Status:** FINAL AUTOMATED ENGINEERING PASS — PENDING USER MANUAL ACCEPTANCE  
**Date:** 2026-09-01  
**Repository:** `MattiaRubino/dante`  
**Branch:** `feature/home-timeline`  
**Worktree:** `/home/mattia/projects/dante-timeline`  
**Final implementation candidate:** `36aa4652731cd9a09334fd52214e66bd87544e22`  
**Frontend CI:** run `33542270688` / #416 — FULL PASS

## Purpose

This file preserves the exact engineering state reached for C1 so a future chat/agent can continue without reconstructing decisions from conversation history.

This is **not** user acceptance. Automated engineering closure is complete; C1 remains open until the manual protocol is executed and the user explicitly approves.

## 1. Product/architecture state

The amended C1 mandate is:

```text
Quick Create
+
Expanded Create
+
Full Create / deep authoring
+
truthful external-vertical seams
```

Permanent boundaries:

```text
ViewModel != frontend application model != DTO != Domain != persistence
intention != placement != occurrence != execution
Schedule != Occurrence != Session != Actual
Proposal != accepted state
planned != actual
manual / keyboard / future AI / future voice -> same semantic application boundary
```

No backend, provider, solver, AI or voice success is faked.

## 2. Major implemented areas

Primary code:

- `apps/web/src/features/temporal-create/`
- `apps/web/src/features/home/ui/timeline/timeline-create-bridge.tsx`
- `apps/web/e2e/temporal-create.spec.ts`

The capability includes:

- model/session/draft semantics;
- local application runtime over F0;
- rich Create intent separate from Timeline projection;
- Quick, Expanded and Full UI levels;
- Activity-specific authoring;
- Event-specific authoring;
- recurrence;
- context/organization fields;
- truthful handoff fields;
- responsive/mobile styling;
- Timeline projection bridge;
- validation/focus lifecycle;
- unit and browser regression coverage.

### Activity semantics

Supported pre-backend authoring includes:

- context/life-area;
- expected duration;
- fixed/open/bounded-window/deadline/preferred-window intent;
- movement/replanning policy;
- execution/session structure;
- minimum/max sessions and buffers where applicable;
- recurrence source specification;
- outcome/confirmation/review policy seams;
- notes/tags;
- external owning-vertical handoffs.

Flexible/open/deadline/window/preferred intent produces **no fake accepted placement**.

### Event semantics

Supported authoring includes:

- start/end/duration;
- all-day/date-span;
- floating vs zoned time mode;
- timezone ID;
- location;
- recurrence;
- availability;
- visibility;
- participant/resource/conference intent as provider handoff only.

Event is not silently converted to unscheduled.

## 3. Failure/fix history — preserve this knowledge

### A. Architecture cycles

CI exposed two real Create UI import cycles.

Resolution:

- shared UI types extracted outside component-to-component imports;
- final dependency-cruiser: 194 modules / 459 dependencies / zero violations.

Do not hide/reintroduce cycles through barrels.

### B. i18n contract drift

Older tests expected generic `Durata`; product uses the more precise `Durata prevista / Expected duration`.

Resolution:

- preserve improved product wording;
- align tests in both languages;
- recurrence accessible names made unambiguous.

### C. Contextual Shift-drag E2E

Initial failure looked like a gesture bug. Trace showed raw pointer Y around `-1680px`: a recycled Timeline day was off-screen after the preceding dialog flow. Locator actions can auto-scroll; raw `page.mouse` does not.

Resolution:

- explicitly scroll target day into viewport;
- remeasure current geometry;
- then perform raw Shift-drag.

Do not revert to stale/off-screen bounding boxes.

### D. Mobile sub-pixel geometry

Browser returned about `390.0000028px` on a 390px viewport.

Resolution:

- tiny tolerance only for numeric bounding-box noise;
- strict `scrollWidth <= clientWidth` remains the real horizontal-overflow invariant.

### E. Real DST defect

Zoned Event end/duration editing initially used wall-clock `PlainDateTime` arithmetic.

Example:

```text
Europe/Rome spring forward
2026-03-29 01:30 -> 03:30
wall-clock difference = 120 min
real elapsed difference = 60 min
```

Using 120 minutes as elapsed duration would move a zoned end to 04:30 and be wrong.

Resolution:

- shared Event end/duration helpers accept `timeMode` + `timeZoneId`;
- floating uses wall-clock arithmetic;
- zoned constructs `ZonedDateTime` and measures real Instants;
- invalid zoned input is rejected/falls back rather than fabricated;
- dedicated tests cover normal multi-day, Europe/Rome spring-forward and fall-back.

Files:

- `temporal-create-field-shared.ts`;
- `temporal-create-event-fields.tsx`;
- `temporal-create-field-shared.test.ts`.

### F. Rich-intent idempotency

F0 fingerprints the minimal projection command, while C1 owns richer recurrence/session/provider metadata.

Resolution:

- C1 adds canonical rich-intent fingerprinting by `operationId`;
- exact prepared replay is accepted;
- same operation ID with different rich intent rejects `operation-id-reused` side-effect-free;
- Undo removes both projection and matching local rich record.

Files:

- `temporal-create-runtime.ts`;
- `temporal-create-runtime.test.ts`.

### G. Projection bridge O(n²)

Audit found per-projection `slice().filter()` plus repeated group lookups.

Resolution:

- precompute context tone/index maps;
- cache mounted sections by date;
- slot counters keyed by date/all-day/start minute;
- single projection pass;
- preserve collision offsets and expanded-group interpolation.

Current preparation complexity is O(n) in Create projections, aside from bounded mounted-day DOM queries.

### H. Unnecessary runtime allocations

`useRef(createLocalTemporalCreateRuntime())` preserved the first value but evaluated the constructor on every render, building discarded workspaces.

Resolution at `891eab584f017f655eb5876169e848fc67a69f79`:

- runtime now uses lazy state initialization and is created once per mounted entry.

### I. Contextual focus return

Contextual double-click/Shift-drag Create previously restored focus to the global `+` on cancel.

Resolution at `891eab584f017f655eb5876169e848fc67a69f79`:

- Create records the actual return target;
- global `+` returns to `+`;
- contextual Timeline Create returns to `.timeline-grid`;
- successful reveal can transfer focus to the created projection.

### J. Dirty-discard focus trap

The discard confirmation focused its first action but the Tab trap still considered the full composer, allowing keyboard traversal back into fields behind the confirmation. Continue-editing also always returned to title rather than the real prior control.

Resolution at `6a0c46982238645db3caf7128017f28debd0d965`:

- discard confirmation is a named `alertdialog`;
- Tab root switches to the confirmation while active;
- Escape continues editing;
- the close-attempt active control is remembered and restored when connected;
- E2E asserts focus cycles only between the two confirmation actions.

### K. Modal truth beyond keyboard

The confirmation was still semantically modal while underlying form/header remained pointer-operable.

Resolution at final candidate `36aa4652731cd9a09334fd52214e66bd87544e22`:

- underlying composer header and form become natively `inert` while discard confirmation is active;
- keyboard, pointer and accessibility semantics now agree with `alertdialog aria-modal`.

## 4. Final hardening commit trail

Important checkpoints:

- `4e19a06a7b1e313a929a86d2b1013c0d58437824` — contextual gesture visibility + mobile sub-pixel E2E;
- `14eccbf18d42c421d4609a8a4be1514f8f7c0afd` — DST-aware shared time helpers;
- `3a5da6ca4aa25f006c805fa54dd377fced5e0f43` — Event fields integrate mode/timezone;
- `8896dbb8e336328db23cc5d8526bc8f93cbe5fbf` — dedicated temporal arithmetic tests;
- `3d08302272926e298857b7ba6235d82b35150c41` — rich Create idempotency;
- `3bb1f888498ed36199c026216cef22cedf3ddfb2` — rich collision regression;
- `4ca8de311e10fb03a4d5fd47903ebe4396271d95` — linear projection layout;
- `4bbbe89508504876edb36a5103388a098bf9b2c9` — saved C1 docs checkpoint;
- `891eab584f017f655eb5876169e848fc67a69f79` — lazy runtime + contextual focus return;
- `6a0c46982238645db3caf7128017f28debd0d965` — discard alertdialog/focus containment;
- `36aa4652731cd9a09334fd52214e66bd87544e22` — underlying draft inert while discard modal is active; **final implementation candidate**.

Earlier intermediates are evidence, not closure checkpoints.

## 5. Final CI evidence

Implementation candidate:

`36aa4652731cd9a09334fd52214e66bd87544e22`

Frontend CI:

- run ID `33542270688`;
- run number `416`.

### Quality — PASS

- frontend contract drift PASS;
- active Home format PASS;
- lint PASS;
- typecheck: 5 successful / 5 total;
- architecture: 194 modules / 459 dependencies / zero violations;
- generated-source drift PASS;
- unit tests PASS;
- web suite: 25 files / 151 tests PASS;
- production build PASS;
- diff check PASS;
- repository mutation check PASS.

### Mobile Bundle — PASS

- Expo dependency compatibility PASS;
- Android Hermes bundle smoke PASS.

### Web E2E — PASS

- Chromium full Web E2E PASS;
- frozen Timeline interaction contract in Firefox PASS;
- no failure artifact uploaded.

### Final gate — PASS

`Frontend CI Gate` completed successfully.

## 6. Bundle/performance decision

Final production build on #416:

```text
Home route: 233.28 kB raw / 83.74 kB gzip
```

Earlier pre-expanded C1 evidence:

```text
Home route: ~76.98 kB gzip
```

The full deeper C1 surface therefore costs about **+6.8 kB gzip** on Home.

Decision: **no dynamic import/Suspense split for Expanded/Full in C1**.

Reasoning:

- saving is modest;
- advanced validation participates in deterministic focus behavior;
- draft continuity must remain synchronous/predictable;
- a lazy boundary would require loading/error/focus recovery states;
- added complexity is not justified by measured route cost.

This is a deliberate performance tradeoff. Revisit only if future route growth produces a material performance case.

## 7. Final static audit result

Checked and accepted for automated candidate:

- semantic truth of flexible Activity vs exact placement;
- Event placement distinction;
- floating vs zoned time semantics;
- invalid-range rejection;
- rich idempotency;
- Undo rich-record cleanup;
- Timeline projection layout complexity;
- requestAnimationFrame/timer/listener/MutationObserver cleanup paths;
- local runtime allocation;
- direct/contextual focus restoration;
- dirty-modal Tab containment and inert background;
- mobile full-screen overflow protection;
- no fake provider effects;
- no raw Create i18n key exposure;
- frozen Timeline interaction regression gates.

No demonstrated C1 defect remains from this audit.

### Note on exact replay after later Undo

F0 intentionally keeps an operation ID's original idempotent result even if a later independent Undo changes current truth. C1's current UI has no path that replays the same prepared Create after that Undo. Do not mutate F0's historical idempotency semantics to solve a hypothetical future transport case. A future remote adapter/reconciliation layer owns that scenario.

## 8. Human acceptance gate

The versioned manual protocol is:

`docs/frontend/home/temporal-create-c1-manual-acceptance.md`

It covers:

- Quick Activity + Undo;
- dirty discard keyboard/pointer/focus;
- progressive disclosure;
- flexible Activity without fake placement;
- Full Activity depth;
- invalid advanced focus;
- Event grammar/provider truth;
- zoned UI;
- all-day multi-day Event;
- unscheduled Activity;
- Timeline double-click/Shift-drag;
- mobile Full editor;
- frozen Timeline regression smoke.

Only the user can close this gate.

## 9. Next state transition

If manual test finds a defect:

```text
C1 MANUAL FAIL
-> reopen demonstrated defect + required adjacent contract
-> repair
-> full automated gate again
-> manual retest
```

If user explicitly approves:

```text
C1 MANUAL PASS — APPROVED
-> document acceptance
-> C1 FROZEN / CLOSED
-> next: C2 Card -> structured Detail
```

Until explicit approval, remain in C1.
