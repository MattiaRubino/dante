# DANTE — Temporal Workstream Live Status

**Status:** ACTIVE AUTHORITY — C1 MANUAL UX ITERATION / NOT CLOSED  
**Date:** 2026-09-04  
**Repository:** `MattiaRubino/dante`  
**Branch:** `feature/home-timeline`  
**Worktree:** `/home/mattia/projects/dante-timeline`  
**Integration target:** `feature/home-react`  
**Current code checkpoint:** `1e7b7752b69f006a4b632e2e2d3ef1522d30e95e`  
**Checkpoint CI:** Frontend CI #937 / `33905239085` — Quality PASS, Mobile PASS, Chromium PASS, Firefox frozen PASS, Gate PASS  
**C1:** OPEN — manual product iteration in progress  
**C2:** BLOCKED until explicit C1 manual approval

## 1. Live authority

This file is the current operational truth for Timeline / Temporal Create. Older implementation checkpoints remain historical evidence only.

Read in this order:

1. `temporal-live-status.md`;
2. `temporal-create-c1-manual-findings-2026-09-04.md`;
3. `temporal-create-handoff.md`;
4. `temporal-create-c1-scope-amendment.md`;
5. `temporal-create-c1-traceability.md`;
6. `temporal-frontend-roadmap.md`;
7. `temporal-f0-contract.md`;
8. `timeline-t1-frozen-contract.md`.

`temporal-create-c1-rearchitecture-2026-09-03.md`, `temporal-create-c1-engineering-checkpoint.md` and `temporal-create-c1-final-validation.md` are historical/superseded records and must not be used as live status.

## 2. Frozen foundations

Do not casually reopen:

- H0 Whole Home structure and breakpoints;
- T1 Timeline continuous viewport, semantic anchor, Now, custom drag/focus, time edit, move + Undo and Firefox interaction contract;
- F0 temporal application foundation closed at `7034b9b0d100709785ebe96e3816aab3e7b1d1f8`;
- closed Domain/Logical model and accepted Physical/CP6 baseline.

Permanent non-collapse rules:

```text
Activity != Event != Routine
Schedule/placement != Occurrence != Session != Actual
planned/intended != happened
recurrence specification != generated Occurrence
Context/group membership != appearance override
ViewModel != application model != DTO != DB row
provider intent != provider execution
manual Create != AI/NL/voice input
```

## 3. Current Create product state

### Base / simple Create

Desktop `+` opens a compact floating Create surface at a stable initial position.

Current contract:

- title-first;
- actionable type chooser exposes Activity and Event;
- sensible base fields are immediately visible;
- simple Create is draggable on desktop;
- no dimming/frozen Home backdrop;
- Timeline remains scrollable/interactable while Create stays open;
- backdrop no longer closes Create;
- close / Cancel / Escape are explicit close paths;
- dirty draft close opens the discard confirmation and preserves the draft until explicitly discarded.

A possible future **simple-only pin/dock to the left** has been discussed but is NOT implemented and is NOT yet an accepted production contract.

### Advanced

Advanced is the same authoring flow at greater depth, rendered as a larger floating desktop surface rather than the old giant centered modal/workspace.

Current contract:

- bounded to viewport;
- internal vertical scrolling when required;
- visible scrollbar chrome is suppressed;
- close/actions/back-to-quick remain reachable;
- Timeline behind it remains usable;
- mobile remains bounded/full-screen appropriate to viewport;
- Advanced is not coupled to a future pin/dock state.

Do not reintroduce the old user-visible Quick → Expanded → Full mental model.

### Recurrence UX

Common `Ripeti` exists for Event and Activity.

- Event recurrence is Event-owned.
- Activity repeat is explicitly **Routine-backed**; Activity itself never becomes canonical recurrence owner.
- `Personalizzata…` is inside the `Ripeti` selector; there is no separate oversized `Personalizza…` button.
- custom recurrence retains the four CP6 families.

Known integration limit: after local Create, the current frontend materializes the authored master/first placed projection only. It does **not** fabricate canonical future Occurrences. Future recurring instances belong to the Routine/Event recurrence evaluator + backend/read-model vertical.

This is intentional architecture, not permission to fake a recurrence engine in the browser.

### Planning Tray

Current direction/implementation:

- desktop anchored popover;
- mobile bottom sheet;
- direct remove with confirmation;
- one carried card during drag;
- no Timeline dimming scrim;
- no duplicate drop-preview ghost;
- snapped time belongs to the carried interaction;
- drop preserves the same Activity identity;
- Escape is zero mutation;
- Undo returns the same Activity to the tray.

### All-day

Per-day all-day v2 is implemented and regression-covered:

- all-day lane lives inside each day;
- minute zero begins below the lane;
- all-day is not a fake 00:00–24:00 timed event;
- multi-day continuation preserves one identity.

### Event Agenda

Structured Event-internal agenda parts are implemented and mapped to native Timeline subitems without inventing child Event identities.

## 4. Timeline proper vs Create

The Timeline renderer/interaction engine is already a mature frontend subsystem. It owns rendering/geometry/interactions, not source-specific ingestion.

Timeline should consume normalized temporal read-model/projections. It must not know whether data originated from manual Create, Routine, provider sync, AI or another vertical.

The missing end-to-end bridge is future work:

```text
Activity / Event / Routine / providers / other sources
→ backend/application temporal range query
→ normalized Timeline projections
→ existing Timeline engine
```

F0 already provides the typed port/adapter seam. Real range/window query, real API adapter, recurrence materialization, Session/Actual runtime and durable reconciliation remain later vertical/backend work.

## 5. Database / backend stop line

Current DB authority remains:

- PostgreSQL 18.6;
- Alembic head `20260826_08`;
- CP6 CLOSED/materialized;
- 68 tables, 5 views, 14 routines, 75 trigger attachments, 95 indexes, 68 FKs, 120 CHECK constraints.

Recurrence owners remain Routine and Event only. Families remain:

- `calendar_wall_clock`;
- `elapsed_interval`;
- `quota_per_period`;
- `cyclic_positional`.

Outside current C1:

- real API transport;
- PostgreSQL application writes;
- canonical server IDs/durable idempotency;
- runtime Auth/ACL;
- provider writes/sync/invitations/booking/conferencing;
- notification/alarm delivery;
- authoritative solver;
- recurrence evaluator/checkpoints and canonical Occurrence generation;
- Session/Actual runtime;
- multi-device reconciliation;
- AI/NL/voice runtime.

## 6. Current validation truth

Code checkpoint `1e7b7752...` passed Frontend CI #937 / `33905239085`:

- Quality PASS;
- Mobile Bundle PASS;
- Chromium Web E2E PASS;
- Firefox frozen Timeline PASS;
- Frontend CI Gate PASS.

This authorizes the next manual UX check. It does NOT close C1.

## 7. Current working method

The user explicitly wants the remaining Create work handled **one foundation at a time**.

For each iteration:

```text
one product problem
→ agree exact behavior
→ bounded implementation
→ full relevant automated validation
→ user checks it
→ only then choose the next problem
```

Do not bundle unrelated UX improvements or “nice-to-have” features into one pass.

## 8. Immediate next action

The next chat/agent should NOT start C2, backend recurrence, pinning or additional Create features automatically.

First let the user manually inspect the current floating/non-modal Create candidate. Then continue with the next single UX decision the user chooses.

C1 can close only after an explicit final user approval:

`C1 MANUAL PASS — APPROVED`
