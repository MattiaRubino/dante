# LifeOS V1 — Scheduling State, Execution Outcome, and Actual Results

## Principle

LifeOS must distinguish what was planned, what happened to the schedule, and what the user actually achieved.

A single status field or binary completed/not-completed checkbox is not sufficient. Rescheduling, cancellation, execution outcome, confirmation, and actual measurements describe different dimensions and must not be collapsed into one ambiguous value.

Not every item type exposes every dimension.

## 1. Planning and scheduling state

Planning state describes the current operational position of an item or occurrence.

Possible values include:

- planned: accepted and expected in the future;
- available: eligible for execution inside its valid window but not assigned to one exact time;
- in progress: currently being performed when the type supports it;
- rescheduled: its accepted date or time was changed before or during execution handling;
- postponed: it was not performed at the expected time and was deliberately moved later;
- suspended: temporarily inactive because its routine, program, project, or temporary mode paused it;
- cancelled: it is no longer expected to occur;
- expired: its valid window ended and it cannot occur without a new decision;
- closed: no further scheduling action is expected because an outcome was recorded or the item became irrelevant.

Rescheduled and postponed are preserved as change history even after the item's current planning state moves forward.

## 2. Execution outcome

Execution outcome describes what happened in relation to the intended action.

Possible outcomes include:

- completed: completed as intended;
- partially completed: a meaningful portion was completed;
- skipped: intentionally not performed without carrying the same occurrence forward;
- missed: not performed before its valid time or deadline;
- replaced: another activity or solution was used instead;
- not completed: explicitly confirmed as not done when `missed` would not accurately describe the situation;
- not applicable: the item became irrelevant because of a broader change;
- unconfirmed: its expected time passed but LifeOS does not know the result.

An ordinary appointment or informational event may not require an execution outcome at all. It can end normally unless an outcome, attendance state, decision, or follow-up is relevant.

## 3. Attendance and participation

Events involving other people may separately record attendance or invitation state, for example:

- invited;
- accepted;
- tentative;
- declined;
- attended;
- partially attended;
- did not attend;
- attendance unknown.

Attendance is not the same as task completion. A user may attend a meeting while its intended decision remains unresolved.

## 4. Confirmation state and provenance

Outcome knowledge is recorded separately from the outcome itself.

Relevant confirmation states include:

- user-confirmed;
- automatically applied by a user-approved rule;
- imported from an integration;
- inferred provisionally;
- awaiting confirmation;
- corrected after the original entry.

LifeOS must not present an inferred or automatic value as though the user explicitly confirmed it.

## Planned versus actual values

An item may record planned and actual execution data, including:

- planned and actual start time;
- planned and actual end time;
- planned and actual duration;
- planned and actual quantity;
- target and achieved distance, repetitions, pages, lessons, cost, or another module-specific measurement;
- completion percentage;
- perceived difficulty, energy, quality, or satisfaction when useful;
- a short reason or note.

Examples:

- planned run: 5 km; actual run: 3.8 km;
- planned study: 60 minutes; actual study: 40 minutes;
- planned meal: option X; actual meal: replacement Y;
- planned task: complete all sections; actual result: two of three sections.

## Postponement and replacement links

Postponement must not erase the original expectation.

LifeOS preserves:

- the original occurrence or planned time;
- the new occurrence or accepted time;
- when the change was made;
- reason and source when available;
- whether the change was proactive rescheduling or a post-deadline postponement.

Replacement similarly links the original item to the replacement and records whether the replacement fully or partially satisfied the original intent.

## Confirmation flow

LifeOS must not silently mark an item as completed merely because its scheduled time passed.

When the outcome is unknown, it remains unconfirmed. The user can confirm it through a quick action or provide a more precise result.

Confirmation should remain lightweight:

- common outcomes use direct controls;
- measurements are requested only when relevant;
- multiple overdue items can be confirmed together;
- low-value items can remain unconfirmed silently according to user policy;
- automatic outcomes require an explicit reusable rule.

## Consequences

Execution results can affect:

- daily and long-term statistics;
- remaining workload;
- routine adherence;
- goal, project, and program progress;
- future duration estimates;
- replanning proposals;
- risk and feasibility assessments;
- recommendations for replacement, recovery, maintenance, or early completion.

A partial result is not automatically treated as failure. Its meaning depends on the item's objective, minimum acceptable result, and remaining plan.

## Corrections, reopening, and audit

The user can correct an outcome, reopen an item where appropriate, or undo a recent mistaken change.

LifeOS preserves enough history to understand:

- what was originally planned;
- how the schedule changed;
- what outcome was recorded;
- how the outcome was known;
- which corrections were later made.

Statistics use the corrected current result while audit and decision history retain relevant previous values.

## Canonical rule

- scheduling state explains **where the item is operationally**;
- execution outcome explains **what happened**;
- attendance explains **whether a participant took part**;
- confirmation and provenance explain **how LifeOS knows**;
- actual measurements explain **how much or how well was done**.
