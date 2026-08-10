# Workstream — Phase 4 Home / Today

- Status: **IN PROGRESS**
- Branch: `prototype/phase-4-today-home`
- Pull request: #2 (`prototype/phase-4-today-home` → `main`)
- Work type: coded UX prototype / design validation
- Current operational milestone: **Home/Today v21**
- Accepted `main` baseline last synchronized: `73f0d172de239853e568532535a4739ce77a0877`

## Purpose

Validate the Home/Today experience before production implementation, especially spatial hierarchy, timeline density, progressive disclosure, overlap handling, grouped expansion and navigation.

## Required reading before editing Phase 4

1. `README.md`
2. `docs/PROJECT-STATUS.md`
3. `docs/development/operating-rules.md`
4. this workstream handoff
5. `docs/phase-4/frontend-master.md`
6. the exact current version/migration material referenced by the frontend master
7. relevant regression tests under `tests/prototypes/`

The accepted architecture/product baseline comes from current `main`. Phase 4 branch-local files are authoritative only for unmerged Phase 4 UX/prototype work.

## Current source of truth

The exact operational prototype state is:

- `docs/phase-4/frontend-master.md` — **primary Phase 4 save game and current version authority**;
- current milestone recorded there: **Home/Today v21**;
- `docs/phase-4/today-v14.md` through `today-v21.md` — iteration-specific records where present;
- `prototypes/today/archive/` — archived/restorable prototype material;
- `tests/prototypes/` — regression checks for preserved prototype behavior.

`docs/ux/today-home-v7.md` is an important documented milestone/baseline, **not the latest prototype version**. Do not start implementation from v7 merely because that document is broader or older. Always use `frontend-master.md` to resolve the current Phase 4 state first.

The frontend master log must be updated after meaningful Phase 4 changes.

## Known accepted direction

- Home/Today is not a flat dashboard-card collection; the direction is spatial/layered.
- The prototype uses progressive disclosure rather than showing all detail at once.
- Timeline density and overlapping items must remain usable under realistic load.
- Group/context expansion and multi-day navigation are part of the exploration.
- The prototype is exploratory and does not define the final production component architecture by itself.

## Parallel-work boundary

Backend/domain work may proceed without waiting for final Phase 4 styling. The prototype may continue using simulated data until stable backend contracts exist.

Do not force backend schema decisions from temporary visual implementation details. Conversely, do not change accepted product/domain semantics merely to simplify the prototype.

Phase 4 normally owns:

- `docs/phase-4/`;
- relevant Phase 4 files under `docs/ux/`;
- `prototypes/today/`;
- `tests/prototypes/`;
- this handoff.

Avoid editing `PROJECT-STATUS.md`, root README or broad architecture files for ordinary prototype iterations. Update global files only when Phase 4 changes global project truth or reaches an accepted integration milestone.

## Next steps

Continue from the exact latest state recorded in `docs/phase-4/frontend-master.md` on the prototype branch. When a Phase 4 decision becomes durable beyond the prototype, move/update the relevant documentation so it reaches `main` with the eventual PR.

Before eventual merge, compare the branch against current `main` and run the semantic/documentation coherence gate from `docs/development/operating-rules.md`.

## Handoff rule

If another chat/agent takes over Phase 4, it must read the branch-local frontend master before editing. This file points to the active source and clarifies authority; it does not replace the detailed Phase 4 log.
