# DANTE — Temporal Workstream Live Status

**Status:** C1 AUTOMATED PASS — PENDING USER MANUAL ACCEPTANCE  
**Date:** 2026-09-02  
**Repository:** `MattiaRubino/dante`  
**Branch:** `feature/home-timeline`  
**Worktree:** `/home/mattia/projects/dante-timeline`  
**Integration target:** `feature/home-react`  
**Final C1 implementation candidate:** `81808814abb4e4998c7bde5b0c6cb8f5f903aa62`  
**Frontend CI:** run `33613239926` / #536 — FULL PASS

## Live authority

This file is the live operational status for the isolated Timeline / Temporal Create workstream.

Read next:

1. `temporal-create-c1-traceability.md`;
2. `temporal-create-c1-engineering-checkpoint.md`;
3. `temporal-create-c1-manual-acceptance.md`;
4. `temporal-create-handoff.md`;
5. `temporal-create-c1-scope-amendment.md`;
6. `temporal-frontend-roadmap.md`;
7. `temporal-f0-contract.md`;
8. `timeline-t1-frozen-contract.md`;
9. `temporal-experience-architecture.md`.

The C1 scope amendment wins over older Q0/C1 scope where they conflict. This live status and the handoff win for the current checkpoint/gate state.

## Stable closed foundations

Do not casually reopen:

- H0 Whole Home structural baseline;
- T1/T1-A/T1-B Timeline interaction/navigation baseline;
- F0 temporal application foundation at `7034b9b0d100709785ebe96e3816aab3e7b1d1f8`;
- closed Domain and Logical model;
- accepted Physical Model;
- materialized CP6 PostgreSQL baseline / Alembic head `20260826_08`;
- `Schedule != Occurrence != Session != Actual`;
- `planned != actual`;
- `ViewModel != frontend application model != DTO != DB row`;
- no fake backend/provider/AI/voice success.

## C1 product shape

C1 is one Create capability with progressive surfaces:

```text
Timeline + / contextual gestures / future semantic inputs
                         ↓
                 SHARED CREATE DRAFT
                         ↓
      Quick Create ↔ Expanded Create ↔ Full Create
                         ↓
             validation + candidate preview
                         ↓
                    user commit
                         ↓
                  F0 command port
                         ↓
          deterministic local adapter now
          authoritative backend adapter later
```

## Current implemented semantics

### Shared capability

- one immutable/normalized draft model across Quick/Expanded/Full;
- title-first Quick Create;
- contextual Timeline defaults from `+`, double-click and Shift-drag range;
- structured source-neutral seed for future global Create / keyboard / import / governed DANTE interpretation;
- candidate preview separate from accepted projection;
- deterministic validation and invalid-control focus;
- operation lifecycle, rich metadata, reveal/focus and Undo;
- application-boundary snapshot ownership preventing mutable prepare/execute drift;
- rich-intent idempotency in addition to F0 projection idempotency;
- IT/EN i18n, modal focus protections, Axe checks and mobile Full editor.

### Activity

Supported creation-time authoring:

- timed, all-day and unscheduled forms where semantically applicable;
- exact expected duration including non-preset values in Expanded/Full;
- open, bounded-window, deadline and preferred-window scheduling intent;
- earliest/deadline boundaries where applicable;
- movement/replanning policy;
- indivisible/splittable execution intent;
- minimum/max sessions;
- preparation/recovery/spacing;
- partial/finish-early/compatible-merge intent;
- fallback policy;
- confirmation/outcome/review policy;
- reminder policy;
- context and notes.

**Activity has no recurrence editor.** Persistent repetition belongs to Routine. C1 presents an explicit Routine handoff instead of reintroducing `Activity.repeat`.

Flexible/open/deadline/window/preferred intent never fabricates a fixed Schedule.

### Event

Supported creation-time authoring:

- start/end/duration;
- all-day multi-day span;
- floating-local vs named-zone time semantics;
- IANA timezone;
- location;
- availability;
- visibility distinct from ACL;
- purpose, expected outcome, agenda and decision-required intent;
- participant/resource/pre-read/conference integration intent;
- preparation/recovery buffers;
- confirmation/reminder policy;
- all four CP6 recurrence families.

Event recurrence depth now includes:

- calendar daily/weekly/monthly/monthly-ordinal/yearly;
- weekly weekday sets;
- ordinal weekday rules;
- elapsed interval;
- quota per day/week/month/year;
- quota period interval;
- quota frame: floating-local / named-zone / absolute-UTC;
- configurable week start;
- named-zone period timezone;
- cyclic day/week patterns with multiple active positions;
- open/until/count termination.

Create stores recurrence **specification only**. It does not fabricate recurrence MaterialState, evaluator checkpoints or Occurrence generation.

### External owning verticals

Typed handoff registry exists for:

`Project`, `Goal`, `Routine`, `Program`, `World`, `Template`, `Reminder`, `Block`, `Asset`.

All are currently `deferred`. Handoff preparation preserves a normalized immutable draft snapshot and contains no fake route, href, CRUD action or success state.

## CP6 alignment

Current database authority:

- PostgreSQL 18.6;
- Alembic head `20260826_08`;
- CP6 CLOSED / materialized;
- 68 DANTE tables;
- 5 views;
- 14 routines;
- 75 triggers;
- 95 indexes;
- 68 foreign keys;
- 120 CHECK constraints.

Critical Create mapping:

- M3 `20260825_03`: Schedule / Actual / Session remain separate;
- M4 `20260825_04`: recurrence family exists for **Routine and Event only**;
- M4 family codes: `calendar_wall_clock`, `elapsed_interval`, `quota_per_period`, `cyclic_positional`;
- M6 `20260826_06`: backend owns recurrence-generated vs explicit-extra Occurrence generation and exact governing recurrence-state binding;
- M7/M8 retain runtime ACL/final hardening boundaries.

## Final automated evidence

Implementation candidate:

`81808814abb4e4998c7bde5b0c6cb8f5f903aa62`

Frontend CI `33613239926` / #536:

- Quality: **PASS**;
- Mobile Bundle: **PASS**;
- Chromium full Web E2E: **PASS**;
- Firefox frozen Timeline interaction contract: **PASS**;
- Frontend CI Gate: **PASS**.

Quality details:

- frontend contract drift PASS;
- format PASS;
- lint PASS;
- typecheck 5/5 PASS;
- architecture: **199 modules / 477 dependencies / 0 violations**;
- generated-source drift PASS;
- web unit suite: **28 files / 168 tests PASS**, plus package suites;
- production build PASS;
- diff check PASS;
- repository mutation check PASS.

Production Home route at this implementation candidate:

```text
252.22 kB raw
86.38 kB gzip
```

The advanced editor remains synchronous. There is no evidence that a lazy boundary is worth the extra loading/error/focus/draft complexity at the measured size.

## Current gate

Engineering, semantic alignment, traceability and automated validation are complete for the implementation candidate.

C1 is still:

```text
AUTOMATED PASS
MANUAL ACCEPTANCE PENDING
NOT FROZEN / CLOSED
```

No C2 work starts before explicit user acceptance.

## Permanent backend/external stop line

Still outside C1:

- real API transport;
- PostgreSQL application writes;
- canonical server IDs;
- server durable idempotency;
- product Auth/ACL enforcement;
- provider writes/sync/invitations/room booking/conferencing;
- notification delivery;
- authoritative solver;
- recurrence evaluator/checkpoints;
- Occurrence generation;
- Session runtime;
- Actual/outcome runtime;
- multi-device reconciliation;
- AI runtime;
- voice runtime.

## Next action

After the documentation descendant is itself CI-green:

1. sync `/home/mattia/projects/dante-timeline` with `git pull --ff-only`;
2. execute the single final protocol in `temporal-create-c1-manual-acceptance.md`;
3. report a precise defect or explicitly state `C1 MANUAL PASS — APPROVED`;
4. only then mark `C1 TEMPORAL CREATE → FROZEN / CLOSED` and move to C2.