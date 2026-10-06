# Timeline / Temporal-Operational — Create closure mini-roadmap

- **Date:** 2026-10-06
- **Status:** ACTIVE / decision freeze
- **Scope:** finish the Activity/Event Create product surface without reopening already-proven kernel blocks.

This is deliberately small. Work should be delivered in the largest coherent batches that stay truthful and testable; do not split it into artificial day-long micro-slices.

## Frozen product decisions

- Activity and Event share the common Create grammar for title, placement, all-day, timezone, Life Area/color, location, description, recurrence and Reminder.
- Event **Agenda** remains the canonical B03-D capability. Product copy becomes **Scaletta**. A Scaletta item owns only ordered text/edit/reorder/remove. It has no independent Schedule, duration, Session, Actual, Outcome or play/pause/stop.
- Activity planned Sessions remain Activity-only.
- **Sub-Activities are not a current Create product capability.** Any retained internal/kernel implementation is non-product and must not leak back into Create copy or controls.
- Event participants use the existing B09 Person / Expected Participation model (`required | optional`). Participant expectation is not invitation delivery, acceptance, attendance or shared-calendar access.
- DANTE remains personal-first. Sharing one Activity/Event must not expose another person's Timeline, free/busy reason, Life Areas or unrelated planning. Broader collaboration/calendar sharing is future scope.
- Global realization and target evaluation are separate:
  - **Reality / Actual:** whether the Activity/Event was realized in reality.
  - **Objectives:** zero or more expected targets evaluated independently.
- Objectives must reuse accepted Criterion / Evaluation / Observation semantics rather than turning measurements into Outcome:
  - boolean/manual assessment;
  - numeric/quantity target with comparator/unit;
  - qualitative assessment;
  - acceptable range as the first product forms.
- Example: `Run 10 km` may have `Actual = activity realized`, `Observation = 8 km`, and objective Evaluation = target not fully reached. These facts are not contradictory.
- B10 Outcome remains a contextual result/disposition of an Actual when useful. It is not the numeric measurement store and is not mandatory configuration in Create.
- Confirmation remains epistemically separate from Actual, Outcome and objective Evaluation.

## Batch A — existing capability consolidation

Complete together where practical:

1. Event Create cleanup:
   - compact **Scaletta** UI aligned visually with Activity planned Session rows;
   - remove prototype-only Event fields that have no accepted persistence/runtime effect;
   - keep canonical description/location and common Create fields.
2. B09 participants:
   - replace free-text required/optional participant textareas with Person-backed expected participation;
   - preserve `required | optional`;
   - no fake email invitation/provider behavior.
3. Common Activity/Event parity:
   - one recurrence product UI/subset;
   - one Reminder grammar;
   - verify recurring Event/Routine paths really materialize the accepted Schedule/Reminder truth.

## Batch B — Reality + Objectives

Implement one shared product model for Activity and Event:

1. Optional global Reality policy:
   - manual/no automatic prompt;
   - ask at end;
   - automatic confirmation only where the accepted policy permits it.
2. Objectives `0..N`:
   - add/edit/remove/reorder;
   - initial product forms: boolean, quantity/number target, qualitative, range;
   - observed values remain Observation-compatible facts;
   - assessment remains Criterion/Evaluation-compatible.
3. Reality and Objectives are independently optional. Users may track only Reality, only Objectives, both, or neither.
4. Do not create a second fake Outcome system. Integrate with B10 only where an actual contextual Outcome is semantically useful.

## Batch C — cleanup and closure gate

- remove superseded Create components, fields, validation and copy;
- keep B13 Plan/Step/Dependency infrastructure separate from Create Activity/Event;
- reconcile OpenAPI/generated client only when public contracts change;
- focused backend/web tests + typecheck/generated checks;
- user-run synthetic real-stack acceptance over Activity/Event, one-off/recurring, Life Area/no Life Area, Reminder, Sessions/Scaletta, participants, Reality and Objectives;
- only after that move to broad bugfix/polish without changing the underlying Create model again.

## Stop line

Do not add provider conferencing, shared calendar/free-busy exposure, invitation acceptance, resource booking, timed Agenda parts or new collaboration semantics merely to mimic external calendar products.


## 2026-10-06 — Batch A implementation candidate

The branch now contains the first consolidated Event Create candidate:

- B03-D Agenda is presented as **Scaletta** in Create and Timeline copy while retaining the canonical Agenda persistence/API contract.
- Scaletta uses the same compact structural grammar as Activity planned Sessions but remains ordered text only; no time, Schedule, Session or Reality identity is introduced.
- The prototype-only Event advanced panel has been removed from the active Create surface.
- Expected participants are staged through B09 Person referents and persisted as canonical Event Expected Participation (`required | optional`); no invitation/shared-calendar semantics are fabricated.
- Post-create retry is generic so Reminder/Reality/Participation follow-up can be retried without authoring a duplicate source.
- Stale Create tests that still exposed Sub-Activities were rewritten to the accepted Session-only product boundary.
- A focused PostgreSQL test candidate now covers recurring Event policy → Occurrence Schedule → Reminder → replay.

This is an **implementation candidate**, not a PASS claim. The user-run local web/backend/generated gates remain required before Batch A is marked proven.
