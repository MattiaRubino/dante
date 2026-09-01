# DANTE — Temporal Create C1 Engineering Checkpoint

**Status:** SAVED ENGINEERING CHECKPOINT / C1 HARDENING ACTIVE  
**Date:** 2026-09-01  
**Repository:** `MattiaRubino/dante`  
**Branch:** `feature/home-timeline`  
**Worktree:** `/home/mattia/projects/dante-timeline`  
**Implementation checkpoint:** `4ca8de311e10fb03a4d5fd47903ebe4396271d95`  
**Frontend CI:** run `33539539640` / #410

## Purpose

This file preserves the exact engineering state reached during C1 so a future chat/agent can continue without reconstructing the work from conversation history.

It is deliberately more detailed than `temporal-live-status.md` and `temporal-create-handoff.md`.

Do not treat this as user acceptance. C1 remains open until final automated gates are green and the user manually tests and explicitly approves the complete Create capability.

## 1. Product/architecture state at this checkpoint

The current Create implementation follows the amended C1 mandate:

```text
Quick Create
+
Expanded Create
+
Full Create / deep authoring
+
truthful external-vertical seams
```

The implementation must preserve these permanent boundaries:

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

### Create feature

Primary code lives under:

- `apps/web/src/features/temporal-create/`
- `apps/web/src/features/home/ui/timeline/timeline-create-bridge.tsx`

The feature currently includes:

- model/session/draft semantics;
- local application runtime over F0;
- projection adapter for Home Timeline;
- Quick, Expanded and Full UI levels;
- Activity-specific fields;
- Event-specific fields;
- recurrence fields;
- organization/context fields;
- handoff fields;
- responsive Create styling;
- Timeline bridge styling;
- unit and Playwright coverage.

### Activity semantics

Current authoring includes the justified pre-backend subset of:

- context/life-area;
- expected duration;
- scheduling constraint intent;
- movement/replanning policy;
- session structure and minimum-session intent;
- recurrence source specification;
- outcome/confirmation policy seams;
- notes and tags;
- links/handoffs to external owning verticals.

Flexible/open/deadline/window/preferred intent must not be rendered as a fake concrete accepted placement.

### Event semantics

Current authoring includes:

- start/end/duration;
- all-day/date-span;
- floating vs zoned time mode;
- timezone ID;
- location;
- recurrence;
- availability;
- visibility;
- participant/resource/conference intent as provider handoff only.

## 3. Recent failure/fix history — preserve this knowledge

### A. Architecture boundary failure

CI found two real import cycles inside Create UI.

Resolution:

- shared UI types were extracted so field/components do not import types through each other;
- dependency-cruiser subsequently reported a clean graph.

Rule: do not reintroduce component-to-component type cycles or hide them behind a barrel.

### B. i18n test drift

The product had moved to the more precise label `Durata prevista / Expected duration`, while an older test still expected `Durata`.

Resolution:

- keep the improved UX wording;
- update the contract test to the actual current label in both languages;
- recurrence accessible naming was also made unambiguous.

Rule: do not regress product language solely to satisfy stale tests.

### C. Shift-drag contextual Create E2E

A Playwright failure initially looked like a gesture bug.

Trace showed raw mouse Y around `-1680px`: the test was measuring a recycled/off-screen day section after the preceding double-click flow. Playwright locator actions can auto-scroll; raw `page.mouse` does not.

Resolution:

- explicitly scroll the intended day section into view;
- capture fresh geometry after the previous dialog closes;
- then issue Shift + raw pointer drag.

This tests the real gesture instead of synthetic coordinates.

### D. Mobile width failure

Browser geometry returned roughly `390.0000028px` on a 390px viewport.

Resolution:

- allow tiny sub-pixel tolerance in the numeric bounding-box assertion;
- retain the strict independent no-horizontal-overflow check based on `documentElement.scrollWidth <= clientWidth`.

This is not a license for a wider tolerance or actual overflow.

### E. Real DST bug

Audit found that Event end/duration editing used `PlainDateTime` arithmetic even when the Event was zoned.

Example problem:

```text
Europe/Rome spring forward
2026-03-29 01:30 -> 03:30
wall-clock delta = 120m
real elapsed delta = 60m
```

If 120m were then added to the zoned start, the resulting end would become 04:30, which is wrong.

Resolution:

- shared Event end/duration helpers now accept `timeMode` and `timeZoneId`;
- floating mode uses wall-clock `PlainDateTime` arithmetic;
- zoned mode constructs `ZonedDateTime` values and derives elapsed minutes from real Instants;
- invalid zoned date/time returns null/fallback rather than fabricating an answer;
- dedicated tests cover normal multi-day arithmetic plus Europe/Rome spring-forward and fall-back.

Files involved:

- `apps/web/src/features/temporal-create/ui/temporal-create-field-shared.ts`
- `apps/web/src/features/temporal-create/ui/temporal-create-event-fields.tsx`
- `apps/web/src/features/temporal-create/ui/temporal-create-field-shared.test.ts`

### F. Rich-intent idempotency gap

F0 fingerprints the minimal projection command. C1 also stores richer metadata such as recurrence/session/provider intent above F0.

Before hardening, a caller could theoretically reuse the same `operationId` with an unchanged minimal projection command but changed rich metadata, causing the local C1 record to drift even though F0 considered it the same operation.

Resolution:

- `LocalTemporalCreateRuntime` now stores an operation-level rich fingerprint;
- fingerprint includes the projection command envelope/payload plus complete `prepared.metadata`;
- exact replay returns the same execution object;
- same operation ID with different rich intent returns an `operation-id-reused` rejection and does not mutate records;
- undo remains responsible for removing both F0 projection and the matching rich local record.

Files involved:

- `apps/web/src/features/temporal-create/application/temporal-create-runtime.ts`
- `apps/web/src/features/temporal-create/application/temporal-create-runtime.test.ts`

### G. Create projection layout complexity

Audit found per-projection `slice(0, index).filter(...)` plus repeated group searches, creating O(n²) work as user-created projections accumulate.

Resolution in `timeline-create-bridge.tsx`:

- precompute context tone/index maps;
- cache mounted day sections by date;
- maintain slot counters keyed by date/all-day/start minute;
- perform one projection scan;
- preserve existing collision offsets and expanded-group interpolation.

Current intended complexity for this preparation pass is O(n) in the number of Create projections, aside from bounded DOM queries per mounted date.

## 4. Commit trail for the final hardening sequence

Useful checkpoints in the latest sequence include:

- `4e19a06a7b1e313a929a86d2b1013c0d58437824` — gesture visibility/sub-pixel E2E correction;
- `14eccbf18d42c421d4609a8a4be1514f8f7c0afd` — DST-aware shared time helpers;
- `3a5da6ca4aa25f006c805fa54dd377fced5e0f43` — Event field integration with time mode/timezone;
- `8896dbb8e336328db23cc5d8526bc8f93cbe5fbf` — dedicated temporal field arithmetic tests;
- `3d08302272926e298857b7ba6235d82b35150c41` — rich Create idempotency guard;
- `3bb1f888498ed36199c026216cef22cedf3ddfb2` — rich idempotency collision regression test;
- `4ca8de311e10fb03a4d5fd47903ebe4396271d95` — linear Create projection layout.

Earlier intermediate commits are not closure checkpoints merely because an individual CI slice passed.

## 5. CI evidence at save time

Implementation checkpoint:

`4ca8de311e10fb03a4d5fd47903ebe4396271d95`

Frontend CI:

- run ID `33539539640`;
- run number `410`.

Verified status at save time:

### Quality — PASS

The run has completed successfully through:

- frontend contract drift;
- active Home workstream formatting;
- lint;
- typecheck;
- architecture;
- generated-source drift;
- unit tests;
- production build;
- diff check;
- repository mutation check.

### Mobile Bundle — PASS

- Expo dependency compatibility;
- Android Hermes bundle smoke.

### Web E2E — IN PROGRESS AT SAVE TIME

Do not convert this line to PASS from memory. Re-fetch the workflow.

A previous superseded workflow had successful Chromium and successful frozen Firefox Timeline steps after the contextual gesture/mobile fixes, but later hardening commits mean those results are supporting evidence only.

### Final gate

Not yet claimable at this save point because Web E2E had not completed on `4ca8de31...`.

## 6. Bundle/performance audit still open

The expanded C1 feature increased the Home route chunk by a modest amount relative to the earlier compact Create baseline. The Full editor is not needed for first paint, so lazy-loading is worth evaluating.

Do **not** introduce dynamic import/Suspense complexity automatically.

Only split Expanded/Full if all of these are true:

- critical Home/Quick Create path becomes measurably smaller;
- no visible loading flash or layout jump is introduced;
- keyboard/focus continuity remains correct;
- tests remain deterministic;
- architecture does not become more coupled;
- error/loading fallback is truthful;
- benefit is material enough to justify another boundary.

If those conditions are not met, keep the current synchronous implementation and document the measured tradeoff.

## 7. Final audit still required before manual test

Re-check:

- timer/RAF cleanup;
- MutationObserver/listener cleanup;
- modal/backdrop focus restoration;
- repeated create/undo/reopen behavior;
- filtered group rendering;
- expanded Timeline group rendering;
- mobile and compact Home pressure widths;
- no raw i18n keys;
- no fake provider side effects;
- no unintended mutation on invalid create;
- no rich-record drift on retry/undo;
- no regression of frozen Timeline gestures/card drag/time edit/Undo;
- no unnecessary rerender/layout work under many local created projections.

## 8. Manual acceptance gate to prepare later

The final user verification should exercise at least:

1. Quick Activity create and Undo;
2. Quick Event create;
3. dirty Escape/backdrop discard protection and opener focus restoration;
4. Expanded Activity with flexible/window scheduling intent and no fake placement;
5. Full Activity with session/recurrence/policy fields;
6. Event Full Create with end date/time, timezone, location, visibility/availability and provider handoff note;
7. all-day multi-day Event;
8. unscheduled Activity;
9. invalid advanced Activity and automatic focus on the actual invalid field;
10. Timeline double-click contextual defaults;
11. Timeline Shift-drag range defaults;
12. mobile Full Create with no horizontal overflow;
13. existing Timeline scroll/scrubber/Ora/card interactions regression smoke.

The user must explicitly approve after this manual pass. Do not auto-close C1.

## 9. Next step after this saved checkpoint

Resume from current branch HEAD, re-fetch CI, complete the bundle/critical-path decision and final static audit. Only after the actual final descendant is fully green should the manual C1 test be requested.

After explicit user PASS:

```text
C1 -> FROZEN / CLOSED
next -> C2 Card -> structured Detail
```

Until then, remain in C1.
