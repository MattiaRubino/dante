# Timeline / Temporal-Operational — B03 Event Core manual userTest

- **Status:** READY / NOT EXECUTED
- **Prepared:** 2026-09-17
- **Branch:** `feature/timeline-temporal-operational`
- **Scope:** B03-A through B03-D product acceptance before B03-E closure
- **CI:** not required by this protocol

This is a manual product acceptance protocol. It is **not evidence of PASS until the user executes it and explicitly accepts the result**.

## Preconditions

1. Pull the current `feature/timeline-temporal-operational` branch.
2. Run DANTE through the normal local authenticated stack used for manual testing.
3. Use the Italian UI.
4. Start from a disposable/test account or otherwise use uniquely identifiable Event titles.

The protocol checks product semantics, not implementation details. Do not inspect or edit PostgreSQL manually during the flow.

---

## A — Timed Event create + reload

1. Open Home / Timeline.
2. Click **Aggiungi alla timeline**.
3. Select **Evento**.
4. Create a timed Event for today with a clear title, for example `B03 manual timed`.
5. Confirm it appears in the Timeline as an Event at the chosen time.
6. Reload the page.

**PASS if:**

- the Event is still present after reload;
- title and placement remain correct;
- it is not shown in the Planning Tray;
- the UI does not present it as an Activity.

---

## B — Event reschedule + reload

Using the Event from A:

1. Move/reschedule it with the Timeline interaction already exposed by the product (drag, keyboard move, or time edit).
2. Confirm the visible placement changes.
3. Reload the page.

**PASS if:**

- the Event remains the same logical item;
- the new placement survives reload;
- there is no duplicate old Event left behind;
- no Activity is created as a side effect.

---

## C — Postpone/TBD + guarded Undo

Using the same timed Event:

1. Open its Event detail.
2. Use **Posticipa / data da definire**.
3. Confirm the Event disappears from the placed Timeline.
4. Reload the page if useful to confirm no fake date/time appears.
5. Use the offered **Annulla** guarded Undo.
6. Reload again.

**PASS if:**

- postponing does not delete or convert the Event;
- no placeholder date/time is fabricated;
- Undo restores a real placement;
- the restored Event survives reload;
- the wording never says the Event was returned to the Planning Tray.

---

## D — All-day and multi-day Event

1. Create a second Event with **Tutto il giorno** for one day.
2. Create a third Event with **Tutto il giorno** spanning at least three calendar days.
3. Confirm the single-day Event appears only on its intended day.
4. Confirm the multi-day Event spans each intended date without becoming a timed midnight block.
5. Reload the page.

**PASS if:**

- single-day and multi-day placement survive reload;
- multi-day ordering/span is unchanged;
- the UI preserves all-day semantics rather than inventing exact clock times.

---

## E — Agenda/internal parts

Open the detail of one Event and exercise the real Agenda editor:

1. Add three Agenda parts, for example `Rischi`, `Decisioni`, `Prossimi passi`.
2. Edit one part.
3. Move one part up/down so the order changes.
4. Remove one part.
5. Close and reopen the Event detail.
6. Reload the whole page and reopen the Event detail again.

**PASS if:**

- the accepted ordered Agenda survives close/reopen and full reload;
- edit/reorder/remove results are exact;
- stale/local UI state does not overwrite backend truth;
- Agenda parts are presented as internal ordered parts, not independent Activities/Events or schedulable items.

---

## F — Boundary sanity

During A–E verify there is no accidental exposure of deferred B03 concepts:

```text
Event recurrence execution/provider sync
participants/invitations
Session/execution truth
Actual/Outcome/Confirmation
availability/busy capacity claims
Agenda-part independent scheduling
```

Those concepts belong to later blocks and must not be claimed as completed behavior by B03.

**PASS if:** the B03 product surface remains bounded to Event expectation + shared Schedule lifecycle + Agenda/internal parts.

---

# Acceptance record

Fill only after execution:

```text
A Timed Event create + reload        NOT RUN
B Reschedule + reload                NOT RUN
C Postpone/TBD + Undo                NOT RUN
D All-day + multi-day                NOT RUN
E Agenda/internal parts              NOT RUN
F Boundary sanity                    NOT RUN

Overall B03 manual userTest          NOT RUN
Executed by                          —
Executed at                          —
Notes                                —
```

B03-E must not cite this file as manual PASS until the user explicitly reports successful execution/acceptance.