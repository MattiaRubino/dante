# DANTE — Temporal Workstream Live Status

**Status:** C1 IMPLEMENTATION FULL GREEN — USER MANUAL ACCEPTANCE PENDING  
**Date:** 2026-09-02  
**Repository:** `MattiaRubino/dante`  
**Branch:** `feature/home-timeline`  
**Worktree:** `/home/mattia/projects/dante-timeline`  
**Integration target:** `feature/home-react`  
**Final C1 implementation candidate:** `f092a3db2fbac28421b73e0629f7b4b83a1b0aec`  
**Frontend CI:** run `33631013598` / #621 — FULL PASS

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

The C1 scope amendment wins over older Q0/C1 scope where they conflict. This live status and the handoff win for current checkpoint/gate state.

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

## C1 product contract — manual only

C1 is the highest-depth useful **manual authoring** system for Timeline Create before backend integration.

```text
Timeline +
Timeline double-click
Timeline Shift-drag/range
        ↓
manual structured prefill
        ↓
SHARED CREATE DRAFT
        ↓
Quick ↔ Expanded ↔ Full
        ↓
normalize → validate → candidate preview
        ↓
explicit user commit
        ↓
F0 command/application boundary
        ↓
deterministic local adapter now
        ↓
real backend adapter later
```

Permanent clarification:

- `+` is not a chat;
- `+` is not an AI command bar;
- `+` does not parse natural language;
- `+` does not own voice input;
- `TemporalCreateFieldSeed` is a deterministic manual-prefill mechanism, not an AI/NL/voice contract;
- DANTE/AI remains a separate future vertical/surface;
- a future DANTE vertical may reuse compatible downstream application/domain/backend commands only if its own contract justifies that reuse.

## Current implemented semantics

### Shared capability

- one normalized draft model across Quick/Expanded/Full;
- title-first Quick Create;
- contextual manual defaults from Timeline `+`, double-click and Shift-drag range;
- deterministic manual prefill without UI scripting;
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
- Context and notes.

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

Event recurrence depth includes:

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

### Context and appearance

Context and appearance are intentionally distinct:

```text
Context/group membership
→ organization + grouping + filters + inherited default tone

optional appearance override
→ presentation only
→ never changes Context/group membership or filtering
```

Manual Create defaults to inherited Context color. The user may choose a stable presentation color override (`Viola`, `Ciano`, `Verde`, `Ambra`, `Rosa`, `Rosso`). Color labels are no longer borrowed from Context names, preventing a false `color == category` equivalence.

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
- M7 `20260826_07`: runtime ACL activation;
- `20260826_08`: final forward-only CP6 QA hardening, not a semantic M8 stage.

## Final implementation evidence

Implementation candidate:

`f092a3db2fbac28421b73e0629f7b4b83a1b0aec`

Frontend CI `33631013598` / #621:

- Quality: **PASS**;
- Mobile Bundle: **PASS**;
- Chromium full Web E2E: **PASS**;
- Firefox frozen Timeline interaction contract: **PASS**;
- Frontend CI Gate: **PASS**.

Quality details:

- frontend contract drift PASS;
- format PASS;
- lint PASS;
- typecheck **5/5** PASS;
- architecture: **214 modules / 522 dependencies / 0 violations**;
- generated-source drift PASS;
- web unit suite: **34 files / 183 tests PASS**, plus package suites;
- production build PASS;
- diff check PASS;
- repository mutation check PASS.

Production Home route:

```text
268.40 kB raw
90.13 kB gzip
```

No lazy split is introduced merely to recover gzip at the cost of asynchronous draft/focus/error complexity. Revisit only from measured route-growth evidence.

## Current gate

C1 is still:

```text
IMPLEMENTATION FULL GREEN
DOCUMENTATION RECONCILIATION REQUIRED TO REMAIN CI-GREEN
USER MANUAL ACCEPTANCE PENDING
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
- AI runtime/input;
- voice runtime/input.

## Next action

Only after the final documentation descendant is itself CI-green:

1. sync `/home/mattia/projects/dante-timeline` with `git pull --ff-only`;
2. execute the single final protocol in `temporal-create-c1-manual-acceptance.md`;
3. report a precise defect or explicitly state `C1 MANUAL PASS — APPROVED`;
4. only then mark `C1 TEMPORAL CREATE → FROZEN / CLOSED` and move to C2.
