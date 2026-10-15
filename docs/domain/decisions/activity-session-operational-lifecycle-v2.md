# Activity and Session operational lifecycle v2

**Status:** CURRENT / NORMATIVE
**Accepted:** 2026-10-14
**Supersedes:** the timed-internal-Session availability and edit/delete rules in `activity-session-live-timeline-v1.md` and `activity-intervals-and-sessions-v2.md`.

These are accepted product rules. They are not evidence that every rule is
implemented or accepted in PostgreSQL and the browser. Track that separately
in `../../workstreams/timeline-temporal-operational-lifecycle-matrix.md`.

## Model

An **Activity** is the intended work. Its **Activity intervals** are the accepted plan. A **Session** is one real execution attempt. Starting, pausing, resuming or stopping a Session never moves an Activity interval and never completes the Activity by itself.

An Activity may expose one optional generic **Activity Session** and zero or more named **internal Sessions**. Named Sessions are Activity-owned execution parts. They are not calendar placements and therefore have no configured start/end, no own reminder, and no Timeline card.

A real Session can start before an Activity interval or end after it. Its timestamps are factual execution history and remain independent of later planning changes.

## Availability and timer rules

The Session panel uses the Activity interval, not an internal Session time:

- named rows become available `PREVIEW_LEAD` before a precise Activity interval and remain available until its end;
- an Activity without an exact interval does not receive an invented minute-level availability;
- starting from the Inspector makes the started row actionable immediately, even outside the current Activity interval;
- Stop removes that completed attempt from the panel; it never offers Play for that same attempt;
- an unstarted row disappears at the end of the Activity interval and enters **Da verificare** only while the Activity's accepted plan is wholly in the past;
- an open or paused row remains actionable after the Activity interval ends until explicitly stopped or deleted.

If generic Activity capture is enabled, a named Session requires the generic Session to be running. Pausing or stopping generic capture pauses or stops open named Sessions. Resuming the generic Session does not resume a named Session. With generic capture disabled, named Sessions run independently.

Multiple Activity intervals remain planning only. There is no Session per interval. Pausing during one interval then resuming during another resumes the same real Session; Stop then Play creates a new attempt.

## Reminder

Reminder belongs to the Activity interval/Schedule only. Internal Sessions have no `Ricorda` control. The panel preview is the current five-minute availability rule; making that lead configurable is a future policy change, not a per-Session reminder.

## Editing, moving and deleting

Before an edit, move or card drag of an Activity that has real Session attempts, the UI asks for one explicit disposition:

| Choice | Effect |
| --- | --- |
| **Mantieni Sessioni** | Change the Activity plan only. Open/paused Sessions keep their runtime state; completed Sessions retain their timestamps. |
| **Elimina Sessioni** | Remove every real Session of the Activity, including active/paused/completed attempts and their linked pause/runtime data, then apply the requested Activity change. |
| **Annulla** | Apply nothing. |

The editor clearly labels retained Session attempts as `in corso`, `in pausa`, or `conclusa`.

Removing a named internal Session from the editor is a draft operation. On **Salva**, it removes the internal Session configuration and all real attempts linked to it. Closing/cancelling the editor does not remove anything.

Deleting a non-recurring Activity is a hard cascade after one confirmation:
Activity, Objectives, Schedule and intervals, reminders, named Session
configuration and every real Session are deleted. Dante does not retain an
archive/tombstone for this product action.

Deleting an Activity that belongs to a recurring Routine first asks for a
scope:

| Choice | Effect |
| --- | --- |
| **Solo questa istanza** | Delete that materialized Activity and all of its Objectives, Schedule/intervalli, reminders, Session configuration and real Sessions. Persist the occurrence as skipped so the Routine cannot recreate the deleted Activity. Other instances and the Routine remain intact. |
| **Tutta la serie** | Delete the Routine/recurrence source, every materialized and future instance, and for every materialized Activity all Objectives, Schedule/intervalli, reminders, Session configuration and real Sessions. Nothing of the series remains. |
| **Annulla** | Delete nothing. |

Both deletion paths are one atomic operation. A partial series deletion or a
deleted occurrence that later rematerializes is invalid.

Moving an Activity removes its unstarted rows from the panel when the current interval no longer makes them available. They appear in **Da verificare** only if the Activity's current accepted plan has ended. Moving the Activity into the future removes those rows from **Da verificare** and makes them available again at the new preview time. Retained open/paused rows remain in the panel and completed rows remain historical.

## Review queue

Once every current Activity interval has ended, each live-capable generic or named Session with no real attempt enters **Da verificare**. A record-only Activity has no generic Play row and follows its separate Reality review policy. Visibility is derived from the **current** plan: moving the Activity into the future clears these pending entries, and reaching its new end can show them again. This is not a completion, failure, Actual, Outcome or Confirmation. Recording, replanning or deleting the pending item is a separate follow-up workflow.
