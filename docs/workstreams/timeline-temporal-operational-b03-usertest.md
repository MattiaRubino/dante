# Timeline / Temporal-Operational — B03 Event Core manual userTest

- **Status:** ✅ EXECUTED / PASS
- **Prepared:** 2026-09-17
- **Executed/accepted:** 2026-09-18
- **Branch:** `feature/timeline-temporal-operational`
- **Scope:** B03-A through B03-D product acceptance for B03-E closure
- **CI:** not required by this protocol
- **Closure:** `timeline-temporal-operational-b03-e-closure-2026-09-18.md`

This is the executed manual product acceptance record for B03 Event Core.

## Preconditions used

The test was executed through the authenticated local real stack with PostgreSQL/backend/frontend truth. The product semantics were tested through the UI; PostgreSQL was not manually edited during the flow.

---

## A — Timed Event create + reload ✅ PASS

Acceptance criteria:

- Event remains present after reload;
- title and placement remain correct;
- it is not shown in the Activity Planning Tray;
- the UI does not present it as an Activity.

Result: **PASS**.

---

## B — Event reschedule + reload ✅ PASS

Acceptance criteria:

- same logical Event survives reschedule;
- new placement survives reload;
- no duplicate old Event remains;
- no Activity is created as a side effect.

Result: **PASS**.

---

## C — Postpone/TBD + guarded Undo ✅ PASS

Acceptance criteria:

- postponing does not delete or convert the Event;
- no placeholder date/time is fabricated;
- Undo restores a real placement;
- restored placement survives reload;
- wording does not claim a Planning Tray transition.

Result: **PASS**.

Manual acceptance also identified a future product-organization need: a postponed/TBD Event with no current Schedule is canonically alive but, after the immediate Undo affordance is gone, needs a discoverable product surface for later rescheduling. It must **not** be converted into a Planning Tray Activity. This is transferred to **B05 Product Organization** and is non-blocking for B03 closure.

---

## D — All-day and multi-day Event ✅ PASS

Acceptance criteria:

- single-day and multi-day placement survive reload;
- multi-day ordering/span remains correct;
- all-day semantics remain date-span truth rather than fabricated midnight clock time.

Result: **PASS**.

---

## E — Agenda/internal parts ✅ PASS after defect correction

The manual flow exercised real Agenda add/edit/reorder/remove/reload behavior.

An initial manual run exposed a real UX defect: rename persistence depended on pressing Enter and did not provide an explicit product commit/cancel affordance. Before closure this was corrected with:

```text
Salva     explicit accepted rename
Annulla   discard draft without backend mutation
Enter     save
Escape    cancel
```

The correction was covered by the Agenda editor test and manually retested successfully.

Acceptance criteria after correction:

- accepted ordered Agenda survives close/reopen and full reload;
- edit/reorder/remove results are exact;
- local draft/cancel does not overwrite backend truth;
- Agenda parts remain internal ordered values, not independent Activities/Events or schedulable items.

Result: **PASS**.

Agenda remains explicitly distinct from independently scheduled sub-events. A future need for timed internal segments requires its own semantic design and is not implemented by giving Agenda parts Schedule identity.

---

## F — Boundary sanity ✅ PASS

B03 does not claim the deferred concepts below as implemented behavior:

```text
Event recurrence execution/provider sync
participants/invitations
Session/execution truth
Actual/Outcome/Confirmation
availability/busy capacity claims
Agenda-part independent scheduling
```

Result: **PASS**.

---

# Acceptance record

```text
A Timed Event create + reload        PASS
B Reschedule + reload                PASS
C Postpone/TBD + Undo                PASS
D All-day + multi-day                PASS
E Agenda/internal parts              PASS
F Boundary sanity                    PASS

Overall B03 manual userTest          PASS
Executed/accepted at                 2026-09-18
Notes                                Agenda explicit rename UX defect fixed and retested;
                                     postponed/TBD rediscovery transferred to B05.
```

This record is valid evidence for B03-E / whole-B03 closure.