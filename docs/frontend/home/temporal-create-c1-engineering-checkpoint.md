# DANTE — Temporal Create C1 Engineering Checkpoint

**Status:** FINAL AUTOMATED ENGINEERING PASS — USER MANUAL ACCEPTANCE PENDING  
**Date:** 2026-09-02  
**Repository:** `MattiaRubino/dante`  
**Branch:** `feature/home-timeline`  
**Worktree:** `/home/mattia/projects/dante-timeline`  
**Final implementation candidate:** `81808814abb4e4998c7bde5b0c6cb8f5f903aa62`  
**Frontend CI:** `33613239926` / #536 — FULL PASS

## 1. Purpose

This checkpoint preserves the exact engineering state of C1 after the final semantic, accessibility, recurrence, input-boundary and integration-seam hardening.

It is not the user acceptance record. C1 remains open until the complete manual protocol is explicitly approved.

## 2. Final C1 architecture

```text
manual + / Timeline context / future typed input
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
manual/DANTE input != canonical truth
frontend projection id != server canonical id
ViewModel != app model != DTO != DB row
```

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

### Shared lifecycle

Implemented:

- one structured draft across all surfaces;
- normalization at draft and application boundaries;
- Quick/Expanded/Full round-trip without duplicated state;
- contextual Timeline defaults;
- structured seed path for future semantic inputs;
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
- context and notes;
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

## 7. Hardening history that must be preserved

### Architecture cycles

Earlier component/type cycles were removed. Current final architecture check:

```text
199 modules
477 dependencies
0 violations
```

Do not reintroduce cycles through convenience barrels or UI-to-UI type ownership.

### i18n typing and accessible names

The resource shape is typed across IT/EN. Accessible labels were made semantically unambiguous rather than making Playwright locators weaker.

Notable resolved collisions:

- reminder vs confirmation section;
- recurrence quota period;
- monthly ordinal weekday vs frequency option wording.

### Zoned/DST arithmetic

Zoned Event arithmetic uses `ZonedDateTime`/Instant elapsed truth rather than raw wall-clock subtraction.

Dedicated tests preserve Europe/Rome DST forward/backward behavior.

### Rich-intent idempotency

F0 fingerprints minimal projection command. C1 separately fingerprints rich metadata. Exact replay is idempotent; changed rich intent under the same operation ID rejects without side effects.

### Prepared-operation snapshot ownership

Final hardening at `81808814...` makes `runtime.prepare()` own a normalized deep-frozen copy before validation/placement/command creation.

This prevents a mutable caller from changing title, Event intent, recurrence arrays or other rich fields between prepare and execute.

Test: `application/temporal-create-boundary.test.ts`.

### Typed semantic seed

`TemporalCreateFieldSeed` deep-merges into normal Create defaults and then re-enters normal normalization/validation.

It cannot use structured prefill to create an Activity recurrence or skip validation.

`TemporalCreateInvocation` already transports the seed into the same UI session.

### Typed owner handoff

The handoff registry is application-owned, not UI-owned.

All current targets are explicit `deferred` dependencies. `prepareTemporalCreateHandoff()` preserves an immutable normalized snapshot and has no route/href/fake operation.

Test: `application/temporal-create-handoff.test.ts`.

### Timeline virtualization E2E

A prior Shift-drag failure was traced to retaining `.first()` across virtualized day recycling. The resulting raw pointer coordinate was outside the viewport.

Final test selects a currently visible date, reanchors by stable `data-timeline-date`, verifies visible geometry and reacquires after the first composer close.

This preserves the real gesture contract without adding sleeps/timeouts or weakening assertions.

### Dirty discard modal

The discard flow remains a named `alertdialog`, traps Tab within its actions, restores the real prior control on continue and makes underlying form/header `inert` while active.

### Projection performance

Create projection layout remains O(n) over current Create projections through cached group/day maps and slot counters.

### Runtime allocation

Local runtime remains lazily initialized once per mounted Create entry.

## 8. UI/CSS audit

The previously identified Full Event one-off CSS debt is no longer present in the active component structure.

Full Event uses shared:

- `temporal-create-section__heading`;
- `temporal-create-check-grid`.

Do not reintroduce `.is-subsection` / `.temporal-create-checkline` merely to create a cosmetic diff.

The UI target remains high-density but calm progressive disclosure, not an administrative DB editor.

## 9. Physical/CP6 alignment

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

## 10. Final automated evidence

Implementation candidate:

`81808814abb4e4998c7bde5b0c6cb8f5f903aa62`

CI:

- run ID `33613239926`;
- run number `536`.

### Quality — PASS

- frontend pre-production contract drift PASS;
- active Home format PASS;
- lint PASS;
- typecheck: 5/5;
- architecture: 199 modules / 477 dependencies / zero violations;
- generated-source drift PASS;
- web unit: 28 files / 168 tests PASS;
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

## 11. Bundle decision

Final Home route:

```text
252.22 kB raw
86.38 kB gzip
```

Earlier full C1 candidate #416 was 83.74 kB gzip. The additional recurrence/seed/handoff/boundary depth adds a small measured increment while materially strengthening the contract.

Decision remains: no dynamic import/Suspense split for C1 solely for gzip recovery. Draft continuity, deterministic validation/focus and error handling remain synchronous. Revisit only on a future measured route-growth case.

## 12. No demonstrated C1 engineering defect remains

Final audit accepted for the automated candidate:

- owner-correct Activity/Event/Routine semantics;
- recurrence four-family depth;
- no local Occurrence generation;
- flexible Activity without fake Schedule;
- no fake Session/Actual;
- provisional inference truth;
- provider seams only;
- typed external-owner handoff;
- source-neutral structured seed;
- application-boundary immutable snapshot;
- minimal + rich idempotency;
- preview/accepted separation;
- Undo cleanup;
- Timeline contextual entries;
- virtualized day handling;
- accessibility/focus/inert modal behavior;
- responsive/mobile containment;
- i18n;
- architecture/performance gates.

## 13. Human acceptance gate

Use only:

`docs/frontend/home/temporal-create-c1-manual-acceptance.md`

If manual acceptance finds a defect:

```text
C1 MANUAL FAIL
→ reopen demonstrated defect + necessary adjacent contract
→ repair
→ full automated CI again
→ repeat only the required final manual protocol
```

If the user explicitly approves:

```text
C1 MANUAL PASS — APPROVED
→ record acceptance
→ C1 TEMPORAL CREATE = FROZEN / CLOSED
→ next C2 Card → structured Detail
```

Until explicit approval, do not start C2.