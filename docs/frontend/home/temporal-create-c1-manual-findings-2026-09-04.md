# C1 Manual Findings — 2026-09-04

## Checkpoint

- Branch: `feature/home-timeline`
- Pre-scope checkpoint: `bbff55b58720d9f8e1cb83565510bfbe924275f7`
- Manual result: **FAIL**

This manual pass supersedes the previous automated-green candidate as a product acceptance signal. The automated gates were healthy, but the Create experience still exposed material UX failures that must be corrected before a new manual acceptance.

## Findings

1. **Advanced was effectively an inline expansion of Quick Create.** The small floating composer grew into a very tall surface, made navigation difficult and could leave closing controls unreachable while the page itself was locked.
2. **The Advanced entry control was visually over-weighted.** `Opzioni avanzate` presented as a large full-width bar rather than a secondary action.
3. **Event temporal authoring was duplicated.** Date/start/end/location existed in the fast path and portions of the same temporal intent were rendered again inside Advanced.
4. **Activity repetition was not authorable from Create.** The UI exposed recurrence only for Event even though a user must be able to express repeated Activities without making Activity the canonical recurrence owner.
5. **Quota repetition such as “3 times per week” was not reachable as an Activity authoring flow.** This must be represented as Routine-backed recurrence intent, preserving the Activity/ Routine ownership distinction.
6. **Planning Tray drag used excessive visual indirection.** The Timeline was dimmed while a carried card and a second drop-preview ghost were shown simultaneously. The intended interaction is direct manipulation: one lifted card follows the pointer and carries its snapped target time.

## Recovery decisions

- Quick Create remains compact, fast and draggable on desktop.
- Advanced activates a large centered workspace, bounded to the viewport, with a permanently reachable header/close affordance, internal scrolling and reachable actions.
- Event date/start/end/location are authored in one place only; Advanced contains only genuine depth.
- `Ripeti` is available for both Event and Activity in the fast path.
- Event recurrence remains Event-owned.
- Activity repetition is preserved as **Routine-backed recurrence intent**. Activity never becomes the canonical recurrence owner, and the browser does not fabricate canonical Occurrences.
- Quota patterns such as N times per week use the existing recurrence grammar rather than an ad-hoc Activity repeat flag.
- Planning Tray drag presents one carried card, no dimming scrim and no second ghost card. The snapped time is shown on the carried card itself; drop preserves the same Activity identity, Escape is zero mutation, and Undo returns the Activity to the tray.

## Frozen boundaries

This recovery does not change PostgreSQL, Alembic, CP6 schema/migrations, F0 architecture, T1 native Timeline drag grammar, All-Day architecture, Reminder/Alarm delivery, provider/backend execution, backend Occurrence generation, C2, World Focus or Home macro geometry.

## Validation gate

A new manual pass is allowed only after the recovery candidate has completed the full automated sequence:

- Quality PASS
- Mobile Bundle PASS
- Chromium Web E2E PASS
- Firefox frozen T1 PASS
- Frontend CI Gate PASS

Only then can C1 manual acceptance be attempted again.
