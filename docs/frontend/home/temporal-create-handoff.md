# DANTE — Temporal Create C1 Workstream Handoff

**Status:** ACTIVE RESTART AUTHORITY — C1 OPEN / MANUAL UX ITERATION  
**Date:** 2026-09-04  
**Repository:** `MattiaRubino/dante`  
**Branch:** `feature/home-timeline`  
**Local worktree:** `/home/mattia/projects/dante-timeline`  
**Integration target:** `feature/home-react`  
**Current code checkpoint:** `1e7b7752b69f006a4b632e2e2d3ef1522d30e95e`  
**Code checkpoint CI:** Frontend CI #937 / `33905239085` — FULL GREEN  
**C1:** NOT CLOSED  
**C2:** BLOCKED

## 1. Restart procedure

Do not treat a new chat as a new branch or a new product design exercise.

Read in order:

1. `docs/frontend/home/temporal-live-status.md`;
2. `docs/frontend/home/temporal-create-c1-manual-findings-2026-09-04.md`;
3. this handoff;
4. `docs/frontend/home/temporal-create-c1-scope-amendment.md`;
5. `docs/frontend/home/temporal-create-c1-traceability.md`;
6. `docs/frontend/home/temporal-frontend-roadmap.md`;
7. `docs/frontend/home/temporal-f0-contract.md`;
8. `docs/frontend/home/timeline-t1-frozen-contract.md`;
9. current code under `apps/web/src/features/temporal-create/` and `apps/web/src/features/home/ui/timeline/`.

The 2026-09-03 re-architecture/checkpoint documents are historical context only where they conflict with the 2026-09-04 authority.

Fresh-check the branch before any write.

Local sync:

```bash
cd /home/mattia/projects/dante-timeline
git fetch origin feature/home-timeline
git pull --ff-only origin feature/home-timeline
git status --short --branch
git rev-parse HEAD
```

Run web locally with Vite:

```bash
cd /home/mattia/projects/dante-timeline/apps/web
corepack pnpm exec vite
```

## 2. Working method — important user requirement

The user wants the remaining `+` work handled **one thing at a time together**.

Do not respond to one UX finding by implementing a bundle of adjacent ideas.

Required cycle:

```text
user identifies one problem
→ discuss only that problem
→ agree exact behavior
→ bounded write scope
→ automated validation
→ user manually judges it
→ only then move to next problem
```

During implementation do not send progress chatter. Surface only a genuine blocker requiring input, otherwise report when finished/validated.

## 3. Current Create behavior to preserve

### Simple/base Create

Desktop:

- first click on `+` opens floating, not pinned;
- stable initial position near upper-left of the usable Home area;
- compact/simple surface;
- draggable by the heading area;
- Home/Timeline is not dimmed or frozen;
- Timeline can continue to scroll/interact while Create remains open;
- backdrop is structural only and does not own outside-click close;
- explicit close/Cancel/Escape paths remain;
- dirty close opens discard confirmation and preserves draft until explicit discard.

Mobile keeps bounded viewport-appropriate behavior.

### Advanced

- same draft/authoring flow;
- larger floating desktop surface, not the previous giant centered modal/workspace;
- bounded to viewport;
- internal scrolling as needed;
- scrollbar chrome hidden;
- back to simple, close and actions remain reachable;
- Timeline behind remains usable;
- do not couple Advanced to pin/dock behavior.

A future simple-only **pin/dock to the left** was discussed but is NOT implemented. Do not add it without a new explicit user decision.

## 4. Current Create semantics

### Activity

Placement choices:

- Orario;
- Tutto il giorno;
- Da collocare.

Execution/session controls must never silently change placement.

User-facing repeat is allowed, but it is **Routine-backed**. Never create a canonical Activity-owned recurrence.

### Event

Supports timed/all-day, Context, location, common recurrence and Advanced Event depth.

Event recurrence remains Event-owned.

### Recurrence

Quick choices include common calendar frequencies plus `Personalizzata…` inside the `Ripeti` selector.

Custom grammar retains CP6 families:

- `calendar_wall_clock`;
- `elapsed_interval`;
- `quota_per_period`;
- `cyclic_positional`.

Browser C1 authors recurrence specifications only.

Known current behavior: local Create materializes the first/master placed projection. It does not render a full future recurring series because canonical Occurrence generation belongs to the future Routine/Event recurrence backend vertical. Do not fake that series in frontend state.

### Event Agenda

Ordered Event-internal agenda parts are implemented and presented using native Timeline subitems. They are not independent child Events.

### Planning Tray

Unplaced Activity:

- anchored desktop tray / mobile bottom sheet;
- direct remove + confirmation;
- one carried card on drag;
- no dim scrim / duplicate ghost;
- same identity on placement;
- Escape no mutation;
- Undo restores unplaced Activity.

### All-day

Per-day lane is implemented. Minute zero begins below it; multi-day continuation keeps one identity; never model all-day as fake 24-hour timed occupation.

## 5. Timeline proper

T1 is mature/frozen frontend behavior, not a throwaway mock.

It already owns:

- rolling temporal window/recycling;
- semantic viewport anchoring;
- Now;
- zoom;
- density/overlap layout;
- compact/expanded Context geometry;
- custom card focus/drag;
- first-drag correctness;
- time edit;
- move + Undo;
- all-day geometry;
- Firefox critical regression.

Timeline is a consumer of normalized projections. It must not directly understand raw DB rows, provider SDK objects or which input source created an item.

Future missing bridge:

```text
canonical temporal sources
→ real backend/application range query
→ normalized Timeline read-model
→ existing Timeline engine
```

## 6. F0 frozen application foundation

Closed at `7034b9b0d100709785ebe96e3816aab3e7b1d1f8`.

Preserve:

- typed identities;
- operation IDs/idempotency;
- Clock;
- date-span/floating/zoned/absolute placement forms;
- immutable drafts;
- commands/results/queries;
- deterministic local adapter;
- optimistic revisions/stale-write rejection;
- guarded Undo;
- subscriptions/subscriber isolation;
- no fake network/storage/DB adapter.

Range/window queries remain future real-consumer work rather than a reason to corrupt Timeline rendering.

## 7. Domain / DB authority

Permanent distinctions:

```text
Activity != Event != Routine
Schedule != Occurrence != Session != Actual
planned/intended != happened
recurrence specification != generated Occurrence
Context != appearance
provider identity != canonical DANTE identity
UI terminology != ontology
ViewModel != application model != DTO != DB row
```

DB baseline:

- PostgreSQL 18.6;
- Alembic head `20260826_08`;
- CP6 CLOSED/materialized;
- 68 tables;
- 5 views;
- 14 routines;
- 75 trigger attachments;
- 95 indexes;
- 68 FKs;
- 120 CHECK constraints.

Recurrence owners: Routine and Event only. Repeated Activity intent is mediated by Routine.

Do not touch DB/Alembic/CP6 for current Create polish.

## 8. Current automated evidence

Code checkpoint `1e7b7752...`:

Frontend CI #937 / `33905239085`:

- Quality PASS;
- Mobile Bundle PASS;
- Chromium Web E2E PASS;
- Firefox frozen Timeline PASS;
- Frontend CI Gate PASS.

Previous #935 exposed one over-specific test assertion after the product contract changed; production behavior was not widened. The test was narrowed to the actual accepted contract: Quick is draggable; Advanced is floating/bounded; Timeline remains interactive.

## 9. Current manual status

C1 has NOT received final manual approval.

The next action is to let the user inspect the latest floating/non-modal Create foundation and choose the next **single** UX problem.

Do not start C2 or a backend recurrence implementation.

C1 closes only on explicit:

`C1 MANUAL PASS — APPROVED`

## 10. Git governance

Before every write:

1. fresh exact branch HEAD check;
2. explicit bounded file/scope gate;
3. create candidate from exact parent where possible;
4. compare candidate against parent;
5. fresh race-check immediately before ref update;
6. non-force fast-forward only;
7. branch readback;
8. complete automated validation before asking for manual test.

Never force/rebase/squash or mutate `main`. Do not create/switch branches unless explicitly requested.
