# Workstream — Phase 4 Home / Today

- Status: **IN PROGRESS**
- Branch: `prototype/phase-4-today-home`
- Pull request: #2 (`prototype/phase-4-today-home` → `main`)
- Work type: coded UX prototype / design validation

## Purpose

Validate the Home/Today experience before production implementation, especially spatial hierarchy, timeline density, progressive disclosure, overlap handling, grouped expansion and navigation.

## Current source of truth

The detailed prototype documentation remains on the active branch until the Phase 4 work is accepted. Before continuing this workstream, read on that branch:

1. `docs/phase-4/frontend-master.md`
2. `docs/ux/today-home-v7.md`
3. `prototypes/today/archive/README.md`
4. `prototypes/README.md`

The frontend master log is the operational handoff for the exact prototype state and must be updated after meaningful Phase 4 changes.

## Known accepted direction

- Home/Today is not a flat dashboard-card collection; the direction is spatial/layered.
- The prototype uses progressive disclosure rather than showing all detail at once.
- Timeline density and overlapping items must remain usable under realistic load.
- Group/context expansion and multi-day navigation are part of the exploration.
- The prototype is exploratory and does not define the final production component architecture by itself.

## Parallel-work boundary

Backend/domain work may proceed without waiting for final Phase 4 styling. The prototype may continue using simulated data until stable backend contracts exist.

Do not force backend schema decisions from temporary visual implementation details. Conversely, do not change accepted product/domain semantics merely to simplify the prototype.

## Next steps

Continue from the exact latest state recorded in `docs/phase-4/frontend-master.md` on the prototype branch. When a Phase 4 decision becomes durable beyond the prototype, move/update the relevant documentation so it reaches `main` with the eventual PR.

## Handoff rule

If another chat/agent takes over Phase 4, it must read the branch-local frontend master before editing. This file only points to the active source; it does not replace the detailed Phase 4 log.
