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

### M2 — Context selector is fixture-derived and cannot author a new context

The current Create context options are derived directly from Timeline prototype groups. The UI does not explain this ownership and does not allow the user to create a new context from the authoring flow.

**Required correction:** separate presentation classification/context authoring from hard-coded fixture groups. The Create picker should be searchable and support a truthful new-context flow with explicit color/tone and a local pre-backend contract. Do not promote a UI context label into a canonical Domain owner or fake backend persistence.

### M3 — Full editor jumps to a right-hand drawer

Opening Full Create changes the spatial model abruptly by pinning the editor to the right edge. This feels disconnected from Quick/Expanded authoring and was rejected in manual review.

**Required correction:** Full should be a deliberate larger Create workspace, not an arbitrary right drawer. Preserve authoring continuity and use a centered/maximized responsive workspace on desktop, full-screen on compact/mobile.

### M4 — Expanded/Full navigation back to a smaller surface is not discoverable

Although code contains surface-change actions, the manual experience does not provide a clear, persistent way to move backward. A bottom `compact` action is insufficient when the form is long.

**Required correction:** persistent surface navigation in the header: Quick ↔ Expanded ↔ Full with clear back affordance and no draft loss.

### M5 — Personalization/appearance depth is insufficient

Manual review identified missing personalization, especially color and related visual differentiation.

**Required correction:** add UI-owned appearance metadata without polluting Domain semantics. At minimum support a controlled color/tone choice, make context tone visible in the picker, and allow an item-level visual override where useful. Keep design-token-safe values rather than arbitrary CSS strings.

### M6 — Competitive UX audit required before final freeze

A targeted benchmark must be used to decide what DANTE should adopt rather than extending the form blindly.

Initial benchmark set:

- Google Calendar — fast event create, calendar selection, event color, guests/location/availability/visibility/reminders;
- Notion Calendar — calendar/color ownership, right-side detail editing, moving between calendars, event types;
- Linear — modal vs full-screen creation, keyboard-first transitions, templates/default properties, inline taxonomy creation;
- Sunsama — task planned time/timeboxing, context/channel routing to calendars, multiple working sessions;
- Fantastical — slot/double-click/drag manual authoring, templates, availability, calendar sets.

DANTE must borrow interaction strengths only where they fit its own semantics. Natural-language parsing/AI authoring is not part of the Timeline `+` manual Create surface.

### M7 — Quick/Expanded panel feels spatially fixed

Before Full Create, the floating composer cannot be repositioned even when it covers relevant Timeline content.

**Required correction:** Quick and Expanded should be pointer-draggable through an explicit header/drag affordance, clamped to the viewport, with the position preserved when moving between those two surfaces. Full remains a deliberate larger workspace rather than a draggable floating panel. Keyboard/focus interaction must remain intact.

## 2. Re-opened C1 correction plan

```text
M1 native Timeline interaction for accepted timed Create items
→ M2 context/taxonomy picker + truthful local new-context contract
→ M3/M4/M7 spatial model + persistent surface navigation + drag
→ M5 appearance/personalization
→ benchmark-informed UX polish
→ blocking unit/E2E/a11y/responsive regression coverage
→ FULL CI green
→ regenerate manual acceptance around the corrected experience
→ single user manual re-acceptance
```

## 3. Permanent constraints retained

- `+` is manual Create only; no DANTE/AI/NLP authoring UI.
- Activity does not own recurrence; repeated Activity intent hands off to Routine.
- Event recurrence remains aligned to CP6 families.
- Preview is not accepted state.
- No fake backend persistence/provider success/Occurrence generation.
- T1 frozen interaction grammar must not be duplicated or weakened.
- UI appearance/context metadata must not be promoted into canonical ontology without authority.
- C1 remains OPEN until explicit user PASS after the corrected candidate is automated-green.
