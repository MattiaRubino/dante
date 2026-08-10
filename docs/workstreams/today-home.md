# Workstream — Phase 4 Home / Today

- Status: **IN PROGRESS**
- Branch: `prototype/phase-4-today-home`
- Pull request: #2 (`prototype/phase-4-today-home` → `main`)
- Work type: coded UX prototype / design validation
- Current integration checkpoint: **Home Shell v11 + Today timeline v21**
- Accepted `main` baseline last synchronized: `73f0d172de239853e568532535a4739ce77a0877`

## Purpose

Validate the Home/Today experience before production implementation, especially spatial hierarchy, timeline density, progressive disclosure, overlap handling, grouped expansion and navigation.

## Required reading before editing Phase 4

1. `README.md`
2. `docs/PROJECT-STATUS.md`
3. `docs/development/operating-rules.md`
4. this workstream handoff
5. `docs/phase-4/home-shell-v11.md` — accepted outer Home shell checkpoint
6. `docs/phase-4/frontend-master.md` — Today v21 behavior/save game
7. `docs/phase-4/today-v21.md`
8. relevant regression tests under `tests/prototypes/`

The accepted architecture/product baseline comes from current `main`. Phase 4 branch-local files are authoritative only for unmerged Phase 4 UX/prototype work.

## Current source of truth

Phase 4 is now intentionally composed from two accepted prototype baselines that have **not yet been integrated**:

- `docs/phase-4/home-shell-v11.md` + `prototypes/home/archive/v11/` — authoritative Home shell/design checkpoint;
- `docs/phase-4/frontend-master.md` + `docs/phase-4/today-v21.md` + v21 tests/archive — authoritative Today/timeline behavior baseline.

The simplified Today block visible inside Home Shell v11 is **not** the functional timeline authority. It is a placeholder and must be replaced/integrated with the full v21 timeline engine in the next iteration.

`docs/ux/today-home-v7.md` remains an important historical milestone/baseline, not the latest source.

## Known accepted direction

- Home/Today is not a flat dashboard-card collection; the direction is spatial/layered.
- The accepted Home shell is Synaptic Nebula with left conversational AI, central Worlds/Stats stage and right contextual rail.
- `Home / Mondi / Oggi` are global destinations; Worlds/Stats switching is a separate Home-local surface control.
- Worlds and Stats share the same carousel interaction contract: arrows, drag, loop and click-to-center.
- Stats shows exactly three visible cards with no ghost cards at the edges.
- the primary global create action is `+ Crea` in the topbar after the LifeOS brand;
- search belongs to the right utility cluster;
- the assistant is a compact conversation surface, not a dashboard status card;
- timeline density and overlapping items must remain usable under realistic load;
- group/context expansion and multi-day navigation remain part of the timeline behavior contract;
- the prototype is exploratory and does not define the final production component architecture by itself.

## Parallel-work boundary

Backend/domain work may proceed without waiting for final Phase 4 styling. The prototype may continue using simulated data until stable backend contracts exist.

Do not force backend schema decisions from temporary visual implementation details. Conversely, do not change accepted product/domain semantics merely to simplify the prototype.

Phase 4 normally owns:

- `docs/phase-4/`;
- relevant Phase 4 files under `docs/ux/`;
- `prototypes/home/` and `prototypes/today/`;
- `tests/prototypes/`;
- this handoff.

Avoid editing `PROJECT-STATUS.md`, root README or broad architecture files for ordinary prototype iterations. Update global files only when Phase 4 changes global project truth or reaches an accepted integration milestone.

## Next exact task

Integrate the full Today v21 timeline engine into Home Shell v11.

Rules for that integration:

1. Home Shell v11 owns the outer topbar/hero/AI/Worlds/Stats/right-rail visual composition.
2. Today v21 owns timeline behavior and must not be silently simplified.
3. Start by restoring both exact artifacts and running their regression/validation checks.
4. Integrate incrementally; after each slice verify v21 timeline capabilities and v11 shell behavior.
5. Any unavoidable behavioral/design conflict must be documented explicitly before dropping or changing functionality.
6. Create the next checkpoint without overwriting either accepted baseline.

Before eventual merge, compare the branch against current `main` and run the semantic/documentation coherence gate from `docs/development/operating-rules.md`.

## Handoff rule

A new chat/AI must be able to resume without conversation history by reading this file, `home-shell-v11.md`, `frontend-master.md`, and the referenced restorable artifacts/tests.
