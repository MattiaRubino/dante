# DANTE — Temporal Workstream Live Status

**Status:** C1 AUTOMATED FULL PASS — FINAL DOCUMENTATION VALIDATION / USER MANUAL ACCEPTANCE PENDING  
**Date:** 2026-09-02  
**Repository:** `MattiaRubino/dante`  
**Branch:** `feature/home-timeline`  
**Worktree:** `/home/mattia/projects/dante-timeline`  
**Integration target:** `feature/home-react`  
**Validated implementation / harness candidate:** `2b910092ecd70de74338427924666a965938ba9f`  
**Frontend CI:** run `33660540265` / #676 — **FULL PASS**

## Live authority

This file is the operational status for the isolated Timeline / Temporal Create workstream.

Read in this order:

1. `temporal-create-c1-final-validation.md` — latest candidate/evidence/status authority;
2. `temporal-create-c1-manual-acceptance.md` — single final human gate;
3. `temporal-create-c1-traceability.md` — semantic/product/physical mapping;
4. `temporal-create-c1-engineering-checkpoint.md` — detailed engineering history;
5. `temporal-create-handoff.md`;
6. `temporal-create-c1-scope-amendment.md`;
7. `temporal-frontend-roadmap.md`;
8. `temporal-f0-contract.md`;
9. `timeline-t1-frozen-contract.md`;
10. `temporal-experience-architecture.md`.

Where older C1 documents contain a stale candidate SHA, CI run, architecture/test count, bundle measurement or gate status, `temporal-create-c1-final-validation.md` wins **only for that current evidence metadata**. Their detailed semantic/history content remains authoritative and must not be deleted merely to align numbers.

## Stable closed foundations

Do not casually reopen:

- H0 Whole Home structural baseline;
- T1/T1-A/T1-B Timeline interaction/navigation baseline;
- F0 at `7034b9b0d100709785ebe96e3816aab3e7b1d1f8`;
- closed Domain and Logical model;
- accepted Physical Model;
- CP6 PostgreSQL materialization / Alembic head `20260826_08`;
- `Schedule != Occurrence != Session != Actual`;
- `planned != actual`;
- `recurrence source != generated Occurrence`;
- `Context/group membership != appearance override`;
- `ViewModel != frontend application model != DTO != DB row`;
- no fake backend/provider/AI/voice success.

## C1 product boundary — manual only

Timeline Create remains a manual authoring capability:

```text
Timeline +
Timeline double-click
Timeline Shift-drag/range
        ↓
deterministic structured manual prefill
        ↓
one shared Create draft/session
        ↓
Quick ↔ Expanded ↔ Full
        ↓
normalize → validate → preview
        ↓
explicit user commit
        ↓
F0 application command
        ↓
deterministic local runtime
```

Permanent:

- no chat inside `+`;
- no natural-language parser;
- no AI command bar;
- no voice input;
- `TemporalCreateFieldSeed` is deterministic prefill, not an AI/NL abstraction;
- future DANTE/AI stays a separate product vertical.

## Current C1 capability

### Activity

Activity supports structured scheduling/execution intent without fabricating lived reality:

- timed, all-day and unplaced forms where semantically valid;
- exact expected duration;
- open/window/deadline/preferred constraints;
- movement/replanning policy;
- indivisible/splittable execution intent;
- minimum/max sessions;
- preparation/recovery/spacing;
- partial/finish-early/merge intent;
- fallback policy;
- confirmation/review/reminder policy;
- Context, notes and appearance override;
- external-owner handoff.

**Activity does not own recurrence.** Persistent repetition belongs to Routine.

### `Da collocare` / Planning Tray

An Activity without an accepted exact slot is now represented explicitly in the Planning Tray.

Keep these meanings separate:

```text
Da collocare = current unplaced Activity state
Collocazione = placement area/process
Vincolo temporale = scheduling constraint
Durata prevista = expected work duration
```

Planning Tray provides:

- searchable unplaced-Activity list;
- quick date/time placement;
- drag into Timeline with snapped live preview;
- planning foreground mode while dragging;
- Escape cancellation with no mutation;
- explicit remove/delete;
- Undo restoring the exact prior state;
- same Activity identity across unplaced ↔ placed transitions;
- mobile bounded bottom sheet.

### Event

Event supports:

- timed and all-day multi-day placement;
- floating-local / named-zone semantics and IANA timezone;
- location, availability and visibility;
- purpose, expected outcome, agenda and decision intent;
- participants/resources/pre-read/conference intent;
- buffers, reminders and confirmation;
- all four CP6 recurrence families.

The all-day Event strip now mounts on the real `.dante-timeline-header` and remains outside the timed grid.

### Recurrence

Event recurrence remains:

- calendar wall-clock;
- elapsed interval;
- quota per period;
- cyclic positional.

Browser Create stores specification only. Backend M6 remains the owner of recurrence-generated Occurrences and governing recurrence-state binding.

### Context / appearance

Context/group membership remains organizational/filtering truth. Appearance override is presentation-only and never changes membership.

### External owners

Typed handoff targets remain:

`Project`, `Goal`, `Routine`, `Program`, `World`, `Template`, `Reminder`, `Block`, `Asset`.

All remain explicitly deferred; no fake route/CRUD/success.

## Final automated evidence

Validated SHA:

`2b910092ecd70de74338427924666a965938ba9f`

Frontend CI `33660540265` / #676:

- Quality: **PASS**;
- Mobile Bundle: **PASS**;
- Chromium full Web E2E: **96 / 96 PASS**;
- Firefox frozen Timeline interactions: **10 / 10 PASS**;
- Frontend CI Gate: **PASS**.

Quality evidence:

- frontend contract drift PASS;
- format PASS;
- lint PASS;
- typecheck **5/5** PASS;
- architecture **218 modules / 537 dependencies / 0 violations**;
- generated-source drift PASS;
- web unit **35 files / 185 tests PASS**;
- package suites PASS;
- production build PASS;
- diff PASS;
- repository mutation PASS.

Production Home route:

```text
287.61 kB raw
94.69 kB gzip
```

## Late hardening record

The final validation also preserves three demonstrated fixes:

1. all-day Event no longer targets obsolete Timeline header markup;
2. Planning Tray state/cleanup satisfies current React, lint and `exactOptionalPropertyTypes` contracts;
3. global Access keyboard E2E now starts from an explicit neutral document focus origin instead of relying on runner/browser startup focus.

The Access harness change adds no product autofocus, no sleeps and removes no assertion. Final compare against the pre-harness candidate was `10 additions / 0 deletions` in the Access E2E file.

## Backend / external stop line

Still outside C1:

- API/PostgreSQL writes;
- canonical server identity and durable server idempotency;
- product Auth/ACL enforcement;
- provider execution/sync;
- notifications;
- authoritative solver;
- recurrence evaluator/checkpoints;
- Occurrence generation;
- Session/Actual runtime;
- multi-device reconciliation;
- AI/NL runtime/input;
- voice runtime/input.

## Current gate

Current state:

```text
IMPLEMENTATION COMPLETE
AUTOMATED FULL PASS
FINAL AUTOMATED VALIDATION RECORDED
FINAL DOCUMENTATION DESCENDANT MUST BE CI-GREEN
USER MANUAL ACCEPTANCE PENDING
NOT FROZEN / CLOSED
```

No C2 work starts before explicit user approval.

## Next action

After the documentation descendant itself is fully CI-green:

1. sync `/home/mattia/projects/dante-timeline` with `git pull --ff-only`;
2. execute the **single** protocol in `temporal-create-c1-manual-acceptance.md`;
3. report any real defect precisely, or approve with `C1 MANUAL PASS — APPROVED`;
4. only then record `C1 TEMPORAL CREATE → FROZEN / CLOSED`;
5. only then begin C2 Card → structured Detail.
