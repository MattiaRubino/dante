# DANTE — Temporal Create C1 Engineering Checkpoint

**Status:** FINAL AUTOMATED ENGINEERING PASS — USER MANUAL ACCEPTANCE PENDING  
**Date:** 2026-09-02  
**Repository:** `MattiaRubino/dante`  
**Branch:** `feature/home-timeline`  
**Worktree:** `/home/mattia/projects/dante-timeline`  
**Final implementation candidate:** `7028633921d1b438bd04961a718457afd82ccc13`  
**Frontend CI:** `33635389124` / #632 — FULL PASS

## 1. Purpose

This checkpoint preserves the exact engineering state of C1 after the final semantic, accessibility, recurrence, appearance, input-boundary, contextual-gesture and integration hardening.

It is not the user acceptance record. C1 remains open until the complete manual protocol is explicitly approved.

## 2. Final C1 architecture

```text
manual Timeline + / double-click / range gesture
                    ↓
          deterministic manual prefill
                    ↓
           shared Create session
                    ↓
       Quick ↔ Expanded ↔ Full
                    ↓
       normalize / validate / preview
                    ↓
             explicit commit
                    ↓
               F0 command
                    ↓
       deterministic local runtime
                    ║
                    ║ STOP
                    ║
         future backend adapter
```

Permanent boundaries:

```text
Activity != Event
Activity repetition -> Routine ownership
recurrence source != generated Occurrence
Schedule != Session != Actual
planned != actual
floating != zoned != absolute
preview != accepted projection
manual Create != DANTE/AI/voice input
frontend projection id != server canonical id
ViewModel != app model != DTO != DB row
```

C1 does not expose natural-language, AI or voice authoring. `TemporalCreateFieldSeed` is a deterministic prefill helper for the manual Create flow, not a generic semantic interpreter contract.

## 3. Final implementation surface

Primary files:

- `apps/web/src/features/temporal-create/model/temporal-create-session.ts`
- `apps/web/src/features/temporal-create/application/temporal-create-runtime.ts`
- `apps/web/src/features/temporal-create/application/temporal-create-projection.ts`
- `apps/web/src/features/temporal-create/application/temporal-create-seed.ts`
- `apps/web/src/features/temporal-create/application/temporal-create-handoff.ts`
- `apps/web/src/features/temporal-create/ui/`
- `apps/web/src/features/home/ui/timeline/timeline-create-bridge.tsx`
- `apps/web/e2e/temporal-create.spec.ts`
- `apps/web/e2e/temporal-create-appearance.spec.ts`

### Shared lifecycle

Implemented:

- one structured draft across all surfaces;
- normalization at draft and application boundaries;
- Quick/Expanded/Full round-trip without duplicated state;
- contextual manual Timeline defaults;
- deterministic structured manual prefill;
- validation + invalid-control focus;
- candidate preview;
- prepared operation + deterministic execution;
- applied projection + rich metadata record;
- reveal/focus + Undo;
- dirty draft confirmation and focus restoration;
- responsive/mobile behavior.

## 4. Activity final semantics

Supported:

- timed/all-day/unscheduled where applicable;
- Context and notes;
- exact expected duration in deeper surfaces;
- open/window/deadline/preferred scheduling intent;
- earliest/deadline boundaries;
- movement/replanning policy;
- indivisible/splittable session intent;
- minimum/max sessions;
- preparation/recovery/spacing;
- partial/early-finish/merge intent;
- fallback policy;
- confirmation/review/inference policy;
- reminder configuration;
- owning-vertical handoff.

Not supported by design:

- Activity recurrence.

Persistent repetition is represented as a required Routine owning-vertical handoff. `createTemporalCreateFields()` normalizes Event recurrence state to `none` whenever kind is Activity.

Flexible Activity intent produces no fake exact placement.

## 5. Event final semantics

Supported:

- timed and all-day/multi-day placement;
- explicit start/end/duration;
- floating-local and named-zone semantics;
- IANA timezone validation;
- DST-correct duration/end arithmetic;
- location;
- availability;
- visibility;
- purpose;
- expected outcome;
- agenda;
- decision-required intent;
- required/optional participants;
- rooms/resources;
- pre-read;
- preparation/recovery buffers;
- conferencing intent;
- reminder/confirmation policy;
- all four CP6 recurrence families.

No external invitation, booking, conference creation or provider sync is claimed.

## 6. Event recurrence final depth

M4/Alembic owner truth:

```text
Routine recurrence family
Event recurrence family
NO Activity recurrence family
```

C1 Event recurrence:

### calendar-wall-clock

- daily;
- weekly + weekday set;
- monthly anchored to civil date;
- monthly ordinal weekday;
- yearly anchored to civil date;
- interval;
- open/until/count termination.

### elapsed-interval

- positive elapsed interval authoring.

### quota-per-period

- quota count;
- period: day/week/month/year;
- period span;
- frame: floating-local/named-zone/absolute-UTC;
- week start for weekly period;
- named-zone IANA period zone.

### cyclic-positional

- cycle length;
- day/week unit;
- multiple active positions;
- human 1-based UI positions.

Occurrence generation remains exclusively downstream M6/backend work.

## 7. Context / appearance hardening

C1 models the visual override explicitly without collapsing it into Context membership.

```text
Context/groupId
→ grouping + filtering + inherited tone

appearanceTone
→ optional presentation override only
```

Guarantees:

- default appearance inherits Context tone;
- override persists Quick/Expanded/Full session state;
- preview and accepted Timeline projection use the override visually;
- override does not mutate `groupId`;
- filters continue to use Context/group membership;
- appearance color names are independent from Context names;
- E2E verifies a Focus item with the red visual tone is hidden by Urgenze filtering and remains visible under Focus filtering after reset.

The final vocabulary is stable presentation language rather than category language: Purple/Cyan/Green/Amber/Pink/Red and IT equivalents.

## 8. Hardening history that must be preserved

### Architecture cycles

Earlier component/type cycles were removed. Current final architecture check:

```text
214 modules
522 dependencies
0 violations
```

Do not reintroduce cycles through convenience barrels or UI-to-UI type ownership.

### i18n typing and accessible names

The resource shape is typed across IT/EN. Accessible labels were made semantically unambiguous rather than making Playwright locators weaker.

Notable resolved collisions:

- reminder vs confirmation section;
- recurrence quota period;
- monthly ordinal weekday vs frequency option wording.

Appearance controls also use independent localized color names instead of Context labels.

### Zoned/DST arithmetic

Zoned Event arithmetic uses `ZonedDateTime`/Instant elapsed truth rather than raw wall-clock subtraction.

Dedicated tests preserve Europe/Rome DST forward/backward behavior.

### Rich-intent idempotency

F0 fingerprints minimal projection command. C1 separately fingerprints rich metadata. Exact replay is idempotent; changed rich intent under the same operation ID rejects without side effects.

### Prepared-operation snapshot ownership

At final candidate `7028633921d1b438bd04961a718457afd82ccc13`, `runtime.prepare()` owns a normalized deep-frozen copy before validation/placement/command creation.

This prevents mutable callers from changing title, Event intent, recurrence arrays or other rich fields between prepare and execute.

Test: `application/temporal-create-boundary.test.ts`.

### Manual prefill seed

`TemporalCreateFieldSeed` deep-merges deterministic structured prefill into normal Create defaults and then re-enters normal normalization/validation.

It cannot create Activity recurrence or bypass validation.

Its C1 role is deliberately bounded to manual Create/context prefill. It is **not** the contract for future DANTE/NL/voice input.

Test: `application/temporal-create-seed.test.ts`.

### Typed owner handoff

The handoff registry is application-owned, not UI-owned.

All current targets are explicit `deferred` dependencies. `prepareTemporalCreateHandoff()` preserves an immutable normalized snapshot and has no route/href/fake operation.

Test: `application/temporal-create-handoff.test.ts`.

### Timeline virtualization / browser viewport E2E

The final contextual-create hardening covers a real mismatch between mounted Timeline sections, the scrollable Timeline grid and the browser viewport.

The accepted E2E contract now:

- scrolls `.timeline-grid` into the browser viewport;
- finds a day section with a useful visible intersection inside both the Timeline grid and browser viewport;
- anchors it by stable `data-timeline-date`;
- derives double-click coordinates from the visible section-local band;
- reacquires geometry after Create closes;
- derives Shift-drag coordinates from the current browser-space intersection;
- uses no arbitrary sleeps/timeouts and weakens no gesture assertion.

This replaces the stale assumption that any mounted Timeline day is automatically browser-visible. The hardened contextual gesture test passed in Chromium at CI #632 and the frozen Timeline Firefox contract also passed.

### Appearance E2E / card remount

The appearance contract originally used a temporary imperative DOM marker as card identity. Filtering can unmount/remount the card, so that marker is not a persistent identity contract.

The final E2E follows the native Timeline card by stable content identity across the remount while retaining strong assertions for tone, Context, filtering and Undo. T1 rendering was not modified merely to satisfy a test hook.

### Dirty discard modal

The discard flow remains a named `alertdialog`, traps Tab within its actions, restores the real prior control on continue and makes underlying form/header `inert` while active.

### Projection performance

Create projection layout remains O(n) over current Create projections through cached group/day maps and slot counters.

### Runtime allocation

Local runtime remains lazily initialized once per mounted Create entry.

## 9. UI/CSS audit

Full Event reuses the existing Create section grammar.

Shared heading style targets:

```css
.temporal-create-section__heading :is(h3, h4)
```

This lets semantic heading depth remain correct without adding a one-off visual subsection class.

Preserve shared:

- `temporal-create-section__heading`;
- `temporal-create-check-grid`.

Do not reintroduce `.is-subsection` / `.temporal-create-checkline` merely to create a cosmetic diff.

The UI target remains high-density but calm progressive disclosure, not an administrative DB editor.

## 10. Physical/CP6 alignment

Current database system of record:

- PostgreSQL 18.6;
- Alembic head `20260826_08`;
- 68 tables;
- 5 views;
- 14 routines;
- 75 triggers;
- 95 indexes;
- 68 FKs;
- 120 CHECKs.

Relevant migration chain:

```text
20260825_03  Schedule / Actual / Session
20260825_04  Routine + Event Recurrence
20260826_06  Occurrence generation
20260826_07  runtime ACL activation
20260826_08  final CP6 QA hardening
```

M4 recurrence families:

`calendar_wall_clock`, `elapsed_interval`, `quota_per_period`, `cyclic_positional`.

M6 preserves `recurrence_generated` vs `explicit_extra` and exact governing recurrence state.

C1 does not attempt to execute any of that backend runtime.

## 11. Final automated evidence

Implementation candidate:

`7028633921d1b438bd04961a718457afd82ccc13`

CI:

- run ID `33635389124`;
- run number `632`.

### Quality — PASS

- frontend pre-production contract drift PASS;
- active Home format PASS;
- lint PASS;
- typecheck: 5/5;
- architecture: **214 modules / 522 dependencies / zero violations**;
- generated-source drift PASS;
- web unit: **34 files / 183 tests PASS**;
- package suites PASS;
- production build PASS;
- diff check PASS;
- repository mutation check PASS.

### Mobile — PASS

- Expo dependency compatibility PASS;
- Android Hermes bundle smoke PASS.

### Web E2E — PASS

- full Chromium suite PASS;
- frozen Timeline Firefox contract PASS;
- failure artifact step skipped because no failure evidence existed.

### Final gate — PASS

`Frontend CI Gate` PASS.

## 12. Bundle decision

Final Home route:

```text
268.40 kB raw
90.13 kB gzip
```

Decision remains: no dynamic import/Suspense split for C1 solely for gzip recovery. Draft continuity, deterministic validation/focus and error handling remain synchronous. Revisit only on a future measured route-growth case.

## 13. No demonstrated C1 engineering defect remains

Final implementation audit accepted for the automated candidate:

- manual-only authoring boundary;
- owner-correct Activity/Event/Routine semantics;
- recurrence four-family depth;
- no local Occurrence generation;
- flexible Activity without fake Schedule;
- no fake Session/Actual;
- provisional inference truth;
- provider seams only;
- typed external-owner handoff;
- deterministic manual prefill;
- application-boundary immutable snapshot;
- minimal + rich idempotency;
- Context/appearance non-collapse;
- preview/accepted separation;
- Undo cleanup;
- Timeline contextual entries;
- browser/Timeline viewport-safe contextual gesture E2E;
- accessibility/focus/inert modal behavior;
- responsive/mobile containment;
- i18n;
- architecture/performance gates.

## 14. Human acceptance gate

Use only:

`docs/frontend/home/temporal-create-c1-manual-acceptance.md`

If manual acceptance finds a defect:

```text
C1 MANUAL FAIL
→ reopen demonstrated defect + necessary adjacent contract
→ repair
→ full automated CI again
→ repeat the required final manual protocol
```

If the user explicitly approves:

```text
C1 MANUAL PASS — APPROVED
→ record acceptance
→ C1 TEMPORAL CREATE = FROZEN / CLOSED
→ next C2 Card → structured Detail
```

Until explicit approval, do not start C2.
