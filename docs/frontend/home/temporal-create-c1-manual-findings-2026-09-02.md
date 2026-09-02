# DANTE — Temporal Create C1 Manual Findings — 2026-09-02

**Status:** MANUAL ACCEPTANCE FAILED / C1 REOPENED  
**Branch:** `feature/home-timeline`  
**Last automated-green descendant before manual review:** `9abc891f21a4166859617bb6211e0a23ca6dd36e` / Frontend CI #539 FULL PASS  
**Authority:** user manual acceptance feedback; C1 must not be frozen until every material finding is resolved and re-accepted.

## 1. Findings

### M1 — Newly created timed items are visually present but interaction-inert

A newly created Activity appears in the Timeline but does not behave like an accepted Timeline card. It cannot be treated as a production-grade created item while it bypasses the frozen T1 interaction grammar.

**Root cause identified during follow-up audit:** Create currently renders accepted projections through `TimelineCreateBridge` portal cards (`temporal-create-projection-card`) rather than feeding a normal Timeline ViewModel/card path. The result visually resembles a Timeline item while not participating in the existing focus/detail/time-edit/drag/keyboard lifecycle.

**Required correction:** accepted timed Create projections must enter the normal Timeline interaction path or another single shared interaction path. Do not duplicate T1 drag/edit behavior inside the Create portal just to make it look interactive. Preview may remain a separate ephemeral projection.

**Implementation checkpoint:** `d5daaa95a7ad9b3e65f38f83a28c3b02bc2562f9` materializes accepted timed Create projections into the normal Timeline reducer/ViewModel path and removes them by identity on Create Undo. Validation still required before disposition can move to resolved.

### M2 — Context selector is fixture-derived and cannot author a new context

The current Create context options are derived directly from Timeline prototype groups. The UI does not explain this ownership and does not allow the user to create a new context from the authoring flow.

**Required correction:** separate presentation classification/context authoring from hard-coded fixture groups. The Create picker should be searchable and support a truthful new-context flow with explicit color/tone and a local pre-backend contract. Do not promote a UI context label into a canonical Domain owner or fake backend persistence.

### M3 — Full editor jumps to a right-hand drawer

Opening Full Create changes the spatial model abruptly by pinning the editor to the right edge. This feels disconnected from Quick/Expanded authoring and was rejected in manual review.

**Required correction:** Full should be a deliberate larger Create workspace, not an arbitrary right drawer. Preserve authoring continuity and use a centered/maximized responsive workspace on desktop, full-screen on compact/mobile.

**Checkpoint:** resolved in `ef07f121efa26909fd5bbb0bfe9fd056294125af`; Frontend CI #543 FULL PASS.

### M4 — Expanded/Full navigation back to a smaller surface is not discoverable

Although code contains surface-change actions, the manual experience does not provide a clear, persistent way to move backward. A bottom `compact` action is insufficient when the form is long.

**Required correction:** persistent surface navigation in the header/footer reachability path: Quick ↔ Expanded ↔ Full with clear back affordance and no draft loss.

**Checkpoint:** hardened in `ef07f121efa26909fd5bbb0bfe9fd056294125af`; Frontend CI #543 FULL PASS. Final user acceptance remains required.

### M5 — Personalization/appearance depth is insufficient

Manual review identified missing personalization, especially color and related visual differentiation.

**Required correction:** add UI-owned appearance metadata without polluting Domain semantics. At minimum support a controlled color/tone choice, make context tone visible in the picker, and allow an item-level visual override where useful. Keep design-token-safe values rather than arbitrary CSS strings.

### M6 — Benchmark against neighboring products is required

C1 should be re-audited against high-quality create/authoring patterns from Google Calendar, Notion Calendar, Linear, Sunsama/Fantastical and other relevant products. The goal is not visual copying for its own sake: adopt mature patterns where they improve DANTE's manual workflow, then preserve DANTE-specific semantics where neighboring tools collapse distinctions that DANTE intentionally keeps separate.

### M7 — Quick/Expanded feels spatially fixed

Before Full Create, the authoring panel should be movable on desktop when the user needs to inspect the Timeline underneath. It must remain viewport-clamped, keyboard/a11y-safe and deterministic; Full can remain a deliberate workspace rather than a draggable window.

**Checkpoint:** implemented in `ef07f121efa26909fd5bbb0bfe9fd056294125af`; Frontend CI #543 FULL PASS.

## 2. Guardrails retained during the reopen

- `+` remains manual; no AI/NLP/voice input is introduced.
- Activity recurrence is not reintroduced. Repeating Activity intent remains a Routine handoff.
- Event recurrence retains the four CP6 baseline families.
- No API/DB/provider success is faked.
- Preview remains ephemeral; accepted items must use the normal interactive presentation path.
- Domain/Logical closure is not reopened just to satisfy a visual Create feature.
- New context/color capabilities must be presentation/application contracts until an owning backend/domain capability is explicitly designed.

## 3. Closure rule

C1 remains `OPEN / MANUAL FAIL` until all material findings above are implemented, automated validation is green, documentation is reconciled, and the user explicitly passes one final coherent manual acceptance run.
