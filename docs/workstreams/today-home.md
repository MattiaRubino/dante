# Workstream — Phase 4 Home / Today

- Status: **IN PROGRESS**
- Branch: `prototype/phase-4-today-home`
- Pull request: #2 (`prototype/phase-4-today-home` → `main`)
- Work type: coded UX prototype / design validation
- Current approved working checkpoint: **Home + Today Integrated v1**
- Current approved artifact documentation: `docs/phase-4/home-today-integrated-v1.md`
- Exact restorable artifact: `prototypes/home/archive/integrated-v1/`
- Historical accepted component checkpoints: **Home Shell v11** and **Today timeline v21**

## Purpose

Validate the Home/Today experience before production implementation, especially spatial hierarchy, timeline density, progressive disclosure, overlap handling, grouped expansion, temporal navigation and the integration between the Home shell and the Today timeline.

## Required reading before editing Phase 4

1. `README.md`
2. `docs/PROJECT-STATUS.md`
3. `docs/development/operating-rules.md`
4. this workstream handoff
5. `docs/phase-4/home-today-integrated-v1.md` — **current approved integrated working baseline**
6. `prototypes/home/archive/integrated-v1/README.md` — exact restore instructions
7. `docs/phase-4/home-shell-v11.md` — historical accepted Home shell checkpoint
8. `docs/phase-4/frontend-master.md` — Today v21 behavior/save game
9. `docs/phase-4/today-v21.md`
10. relevant regression tests under `tests/prototypes/`

The accepted architecture/product baseline comes from current `main`. Phase 4 branch-local files are authoritative only for unmerged Phase 4 UX/prototype work.

## Current source of truth

For the next Home/Today prototype iteration, the authoritative **integrated working artifact** is:

- `docs/phase-4/home-today-integrated-v1.md`;
- `prototypes/home/archive/integrated-v1/`.

Restore the exact artifact before making changes. Do not reconstruct it approximately from screenshots or conversation history.

The integrated v1 artifact was selected from the user-provided prototype and approved after moving timeline gap/margin labels from the right to the **left**, next to the time-axis side. Its restored HTML SHA-256 is:

`66f1f8af4795aa579394ec07bc872798141907c6c216f5af0daed4f96e5c32b4`

Home Shell v11 and Today v21 remain preserved as historical/component checkpoints and regression references. They must not be deleted or overwritten merely because an integrated working baseline now exists.

`docs/ux/today-home-v7.md` also remains a historical milestone, not the latest source.

## Explicit current constraints

### No Home wing expansion

**Do not add or restore Home wing expansion unless the user explicitly requests it in a later iteration.**

This means:

- no left AI wing expansion behavior;
- no right contextual-detail wing expansion behavior;
- earlier experimental implementations of those behaviors are rejected and are not part of the approved baseline.

This prohibition concerns the Home hero wings only. It does **not** remove the existing Today/timeline panel expansion controlled by the timeline drag handle.

### Timeline margin placement

Timeline gap/margin indicators belong on the **left** side, close to the time axis. Their timing calculation and semantics are unchanged.

### Scope discipline

- Preserve approved areas unless the user explicitly puts them in scope.
- Do not silently transplant UI from discarded conversation previews.
- Do not add controls merely because functionality exists; visual hierarchy and commercial/product cleanliness are explicit design constraints.
- Functional changes require real browser regression checks; visual changes require visual browser verification before delivery.

## Current integrated behavior to preserve

The exact restorable artifact is authoritative. At a high level, the current integrated baseline includes:

- Home topbar and Synaptic Nebula Home composition;
- conversational AI surface on the left;
- central Worlds/Stats surfaces and their accepted carousel behavior;
- contextual detail surface on the right;
- Today environmental header/path;
- week strip synchronized with the day actually being viewed;
- distinct `today` and `viewing` states;
- expandable calendar navigation through day/month/year levels;
- contextual `Ora` return-to-current-time action;
- navigation into both past and future days;
- 24-hour timeline and nonlinear density mapping;
- overlap lanes;
- group filters, group reorder and grouped timeline expansion;
- Appunti/Review side rail;
- timeline drag-handle expansion;
- card focus, with click on empty timeline space clearing focus;
- subtask expansion and mapper reflow;
- event drag/move, cross-day movement, Esc cancel and Undo;
- zoom and time editing;
- timeline gap/margin labels on the left.

This summary is a handoff index, not permission to reimplement the features approximately. Restore the artifact for exact behavior and visual reference.

## Historical component checkpoints

### Home Shell v11

- `docs/phase-4/home-shell-v11.md`
- `prototypes/home/archive/v11/`

Use when a regression needs comparison with the previously accepted Home shell in isolation.

### Today v21

- `docs/phase-4/frontend-master.md`
- `docs/phase-4/today-v21.md`
- `prototypes/today/archive/v21/`

Use when a timeline regression needs comparison with the previously accepted Today behavior in isolation.

These are regression/history anchors. **Integrated v1 is the current working starting point.**

## Parallel-work boundary

Backend/domain work may proceed without waiting for final Phase 4 styling. The prototype may continue using simulated data until stable backend contracts exist.

Do not force backend schema decisions from temporary visual implementation details. Conversely, do not change accepted product/domain semantics merely to simplify the prototype.

Phase 4 normally owns:

- `docs/phase-4/`;
- relevant Phase 4 files under `docs/ux/`;
- `prototypes/home/` and `prototypes/today/`;
- `tests/prototypes/`;
- this handoff.

Avoid editing `PROJECT-STATUS.md`, root README or broad architecture files for ordinary prototype iterations. Update global files only when Phase 4 changes global project truth or reaches an accepted integration milestone that needs promotion.

## Next exact task

**Await the user's next direction.**

Do not make another design or implementation change until the user defines the next scope. Start the next iteration by restoring **Home + Today Integrated v1**, not by continuing from an unapproved local preview.

Before eventual merge, compare the branch against current `main` and run the semantic/documentation coherence gate from `docs/development/operating-rules.md`.

## Handoff rule

A new chat/AI must be able to resume without conversation history by reading this file plus `docs/phase-4/home-today-integrated-v1.md`, and by restoring `prototypes/home/archive/integrated-v1/`.
