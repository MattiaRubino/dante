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

## Timeline presentation

The Activity card keeps its planned interval as the editable Schedule, with
planned and real times labelled separately. Starting its generic Activity
Session immediately places the *visible* card at the real start, including
when that falls on another day; Play/Pause preserve its planned visual height.
Stop immediately places and sizes it by the real start/end. This projection
never writes the Schedule or replaces the factual Session timestamps. A very
short completed interval makes the elastic ruler reserve the card's minimum
readable height, so its visible end still corresponds to the ruler end.

Starting/stopping an internal Session alone neither relocates nor resizes the
Activity card. The card only shows the count of configured internal Sessions;
their names, controls and history belong in the Session panel/Inspector.

The Home Timeline provides a rolling **Timeline**, a single **Giorno**, and a
seven-column **Settimana** view. The first two retain the elastic density and
right-hand expansion; the week uses a shared minute scale across columns.
Quarter-hour ruler labels are shown only where their actual mapped positions
have sufficient room; they do not imply a fixed linear 15-minute grid.

## Availability and timer rules

The Session panel uses the Activity interval, not an internal Session time:

- named rows become available `PREVIEW_LEAD` before a precise Activity interval and remain available until its end;
- an Activity without an exact interval does not receive an invented minute-level availability;
- starting from the Inspector makes the started row actionable immediately, even outside the current Activity interval;
- Stop removes that completed attempt from the panel; it never offers Play for that same attempt;
- an unstarted row disappears at the end of the Activity interval **unless the main Activity Session is still open**; it enters **Da verificare** only while the Activity's accepted plan is wholly in the past and no running main attempt is offering that row;
- explicitly starting the main Activity Session makes all its configured internal Session rows visible immediately, even hours before the five-minute preview or beyond the planned end. This never starts any internal Session automatically or changes the accepted Activity interval;
- pausing the main keeps its unstarted internal rows visible but not startable; resuming the main makes them startable again without auto-resuming any child;
- stopping an internal Session removes its completed attempt from the panel for the current main attempt, including outside the normal preview; starting a genuinely new main attempt makes configured internal rows eligible again;
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


## Event parity — deletion, recurrence scope and scheduling

**Accepted product extension (2026-10-15):** The same intent, scope, atomicity,
history-versus-plan, ownership, and no-silent-regeneration rules apply to
**Events**, with Event-owned data instead of Activity-only Session configuration.
An Event remains occurrence-centred: an individual recurring Event instance is
an Occurrence, not a new unrelated Event source.

- **One-off Event / non-recurring Activity:** one explicit hard-delete confirmation
  removes the owned object and its complete owned graph. Event graph includes
  agenda/profile, Schedule and Reminder, Objectives, participation and attendance
  records, Actual/Outcome/Confirmation/reconciliation and any other records
  canonically owned by that Event; Activity graph includes its corresponding
  Activity-specific members and real Session attempts. Never traverse into
  independently owned people, Life Areas, or other subjects.
- **Solo questa istanza:** delete only the selected recurring Event Occurrence's
  owned instance graph, including its Schedule, reminders, participation/attendance
  and factual records specifically owned by that instance; retain the shared
  source Event and all sibling Occurrences. Record a durable technical exclusion
  (e.g. an Occurrence skip) so future materialization cannot recreate the
  deleted instance. For recurring Activity the equivalent action deletes the
  selected Activity's full owned graph, keeping only the technical exclusion.
- **Tutta la serie:** atomically delete the recurring Event source, recurrence,
  every existing/materialized Occurrence and its owned graph, and eliminate all
  future generation. The Activity equivalent deletes its Routine/recurrence
  source, every materialized Activity instance and each owned graph.
  A partial deletion, surviving generated future instance or orphan is invalid.
- **Annulla:** no changes. Every hard-delete action is irreversible in product
  terms: there is no historical archive or Undo for deleted truth.
- **Rimuovi dalla Timeline / sposta:** change only the accepted temporal
  placement, with coordinated preview/confirmation and guarded plan Undo.
  Do **not** hard-delete the Event/Activity or erase actual attendance/results.
  An Event whose placement is withdrawn remains the same expected Event,
  possibly postponed/unplaced, with its original expectation reconstructible.
- **Ricorrenze, modifiche:** preserve stable instance identity, distinguish
  `Solo questa` from `Questa e le prossime` for edits when those are supported,
  and never silently apply a single-instance change to a series.
  For **hard deletion** the choices remain exactly `Solo questa istanza`,
  `Tutta la serie` and `Annulla`.

Deletion must be a **single owner-scoped serializable transaction** with a
current source/instance revision and impacted-history fingerprint, locks
against concurrent checkpoint/materialization, and all-or-nothing graph
removal. Externally owned/shared references must fail closed instead of
causing cross-owner data deletion. The API and UI may offer the action only
after the database provides this guarantee. Passage of time and scheduling
changes do not manufacture Actual, Outcome, attendance or Confirmation.

**Implementation/evidence status:** the scoped deletion and Timeline operations
are present as an integration candidate through `_158`; this does not prove
their PostgreSQL/API/Web/browser acceptance or a same-SHA full gate. Do not
apply the destructive operations to real data until those checks pass.

## Review queue

Once every current Activity interval has ended, each live-capable generic or named Session with no real attempt enters **Da verificare**. A record-only Activity has no generic Play row and follows its separate Reality review policy. Visibility is derived from the **current** plan: moving the Activity into the future clears these pending entries, and reaching its new end can show them again. This is not a completion, failure, Actual, Outcome or Confirmation. Recording, replanning or deleting the pending item is a separate follow-up workflow.
