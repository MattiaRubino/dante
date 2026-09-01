# DANTE — C1 Temporal Create Manual Acceptance

**Status:** PREPARED — PENDING FINAL DOCS SYNC AND USER TEST  
**Date:** 2026-09-01  
**Branch:** `feature/home-timeline`  
**Implementation candidate:** `36aa4652731cd9a09334fd52214e66bd87544e22`  
**Scope:** complete pre-backend Create capability only; this document does not authorize C2

## Purpose

This is the repeatable human acceptance gate for C1. Automated CI is necessary but not sufficient. The capability is frozen only after these checks are performed against the final branch descendant and the user explicitly approves the result.

## Local preparation

Use the real Timeline worktree:

```bash
cd /home/mattia/projects/dante-timeline

git status --short --branch
git fetch origin feature/home-timeline
git merge --ff-only origin/feature/home-timeline
git rev-parse HEAD

corepack pnpm --filter @dante/web dev
```

Before testing, the worktree must be on the documented final descendant of implementation candidate `36aa4652...` and must not contain unrelated local changes.

Test primarily at a normal desktop viewport around 1440×900. Use browser responsive mode for the explicit mobile check.

## Acceptance protocol

### 1. Quick Activity — happy path + reveal + Undo

1. Open Home.
2. Press the Timeline `+`.
3. Confirm title receives focus immediately.
4. Keep type `Attività`.
5. Enter a title such as `Nuova attività`.
6. Set a visible time and duration, for example 13:30 / 60 min.
7. Choose a context.
8. Create.

Expected:

- editor closes without page jump;
- created projection appears at the expected date/time/context;
- created card receives focus;
- feedback says the item was created;
- `Annulla` removes it again;
- no second/ghost card remains.

### 2. Dirty draft protection — keyboard, pointer and focus containment

1. Open Create from `+`.
2. Type a title without saving.
3. Press Escape.

Expected:

- `Scartare questa bozza?` appears as the active confirmation;
- focus is on the first confirmation action;
- Tab cycles only between the two confirmation actions and never reaches fields/buttons behind the confirmation;
- Escape from the confirmation means “continue editing” and returns focus to the control from which close was attempted;
- draft content is unchanged.

Then click outside the composer to request close again and choose `Scarta`.

Expected:

- composer closes;
- focus returns to the Timeline `+` trigger;
- discarded draft does not reappear on the next open.

### 3. Progressive disclosure — Quick → Expanded → Full

1. Open Create and enter an Activity title.
2. Open `Dettagli e pianificazione`.
3. Confirm Expanded keeps the existing draft unchanged.
4. Open `Editor completo →`.
5. Confirm Full keeps the same draft unchanged.
6. Return to Expanded/compact and verify values remain intact.

Expected: one draft, one semantic operation path, no reset or duplicate state between surfaces.

### 4. Flexible/window Activity — intent must not become fake placement

1. Create an Activity such as `Montare il video`.
2. Set expected duration to 180 min.
3. In Expanded choose a bounded temporal window.
4. Choose movement policy inside the window.
5. Optionally add fallback/replanning policy.
6. Create.

Expected:

- result is reported as created/accepted local intent;
- UI identifies it as `Da pianificare` rather than pretending an exact schedule exists;
- no fake fixed Timeline card is rendered at the draft's previous time;
- Undo removes the local rich intent/projection truth cleanly.

Repeat the truth check for open/deadline/preferred-window forms if desired: none may silently become an accepted exact placement.

### 5. Full Activity — execution/session/recurrence/policy depth

Create an Activity and exercise:

- splittable execution;
- minimum session;
- maximum session count;
- preparation/recovery/spacing if exposed;
- weekly recurrence with multiple weekdays;
- recurrence end rule;
- non-confirmed outcome/review policy;
- reminder;
- notes/tags.

Expected:

- fields remain stable while moving Expanded ↔ Full;
- recurrence controls are understandable and keyboard reachable;
- Project/World or other external-owned object creation is not faked locally;
- unavailable ownership is explained truthfully as a handoff/dependency.

### 6. Advanced validation — focus the actual invalid control

1. Create an Activity with duration 60 min.
2. Set execution structure to splittable.
3. Enter a minimum session larger than the total duration, e.g. 120 min.
4. Submit.

Expected:

- Create is rejected locally;
- draft remains intact;
- meaningful validation is shown;
- focus moves to the real invalid minimum-session control;
- no Timeline item is created;
- no fake Undo appears.

### 7. Event — distinct Event grammar

1. Open Create.
2. Switch type to `Evento`.
3. Set start and end/date as needed.
4. Open Expanded/Full.
5. Set location, availability and visibility.
6. Configure recurrence.
7. In Full, enter participants/resources and choose provider-default video conference if available.

Expected:

- Activity-only flexible scheduling controls are absent from Event;
- Event remains placed, never silently converted to unscheduled;
- provider note explicitly says invitations/bookings/conference links require the real provider/backend;
- locally creating the Event does not claim invitations, room booking or conference creation occurred;
- recurring Event projection is visibly identified as recurring.

### 8. Zoned Event / timezone truth

1. Create a timed Event.
2. Select zoned/named-zone semantics.
3. Use a valid IANA zone such as `Europe/Rome`.
4. Edit the Event end time/date and verify duration readout remains coherent.

Expected:

- the zone is preserved as semantic input;
- no timezone validation error for a valid IANA zone;
- invalid zone input is rejected rather than silently coerced.

DST spring-forward/fall-back arithmetic is protected automatically by dedicated tests; manual acceptance only needs to confirm the zoned UI is coherent and does not collapse back to floating mode.

### 9. All-day / multi-day Event

1. Create an Event.
2. Choose `Tutto il giorno`.
3. Set an end date equal to or after the start date; test more than one day as well.
4. Create.

Expected:

- all-day representation appears in the all-day area, not as an arbitrary timed card;
- multi-day range is preserved;
- an end date before the start is rejected.

### 10. Unscheduled Activity

1. Create an Activity.
2. Choose `Da pianificare` / unscheduled.
3. Create.

Expected:

- creation succeeds as intent;
- feedback reports `Da pianificare`;
- no fake exact Timeline placement appears.

### 11. Timeline contextual Create — double-click and Shift-drag

On empty Timeline space:

1. Double-click a time position.
2. Confirm Create opens with contextual date/time defaults.
3. Cancel with Escape while the draft is clean.

Expected:

- composer closes;
- keyboard focus returns to the Timeline grid, not the distant `+` button.

Then:

1. Hold Shift.
2. Drag vertically across an empty range.

Expected:

- Create opens with the contextual date/start and a duration derived from the range;
- existing cards do not accidentally become range-create targets;
- normal card drag semantics remain unchanged.

### 12. Mobile Full Create

Use responsive mode at **390×844**.

1. Open Create.
2. Go to Expanded and then Full.
3. Scroll through all fields.
4. Exercise a select, text field, recurrence control and close/discard flow.

Expected:

- Full editor uses the mobile/full-screen treatment;
- no horizontal page overflow;
- no control is clipped outside the viewport;
- touch-sized actions remain usable;
- discard confirmation remains contained and usable.

### 13. Frozen Timeline regression smoke

Without changing Create, verify the accepted Timeline still behaves as before:

- normal wheel/trackpad scroll;
- gray relative temporal scrubber moves both directions and returns to neutral on release;
- orange expansion/split handle remains visually distinct;
- `Ora` works;
- existing card pointer drag still works;
- keyboard Alt nudge + Undo still works;
- direct time editor still works;
- continuous day recycling does not visibly jump;
- no regression at Home pressure boundaries around 900/901 and 1120/1121.

## Acceptance rule

Record one of these outcomes only after the protocol:

```text
C1 MANUAL PASS — APPROVED
```

or

```text
C1 MANUAL FAIL — <precise defect>
```

A failure reopens only the demonstrated defect and its necessary adjacent contract. A pass freezes C1 and authorizes the roadmap to move to C2 Card → structured Detail.
