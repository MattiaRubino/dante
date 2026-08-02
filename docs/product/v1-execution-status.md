# LifeOS V1 — Execution Status and Actual Results

## Principle

LifeOS must distinguish what was planned from what actually happened. A binary completed/not-completed checkbox is not sufficient for activities, routines, and programs that may be partial, replaced, postponed, cancelled, or still awaiting confirmation.

## Execution states

A planning item may use these execution states when applicable:

- pending: planned and not yet due;
- in progress: started but not yet closed;
- completed: completed as intended;
- partially completed: some meaningful portion was completed;
- skipped: intentionally not performed;
- missed: not performed before its valid time or deadline;
- postponed: moved to another valid occurrence or time;
- replaced: another item was performed in its place;
- cancelled: no longer expected to occur;
- awaiting confirmation: its scheduled time has passed, but LifeOS cannot reliably infer the outcome;
- not applicable: the item became irrelevant because of a broader change.

Not every item type must expose every state. The valid state transitions depend on the item's type, timing rules, recurrence, and fallback policy.

## Planned versus actual values

An item may record both planned and actual execution data, including:

- planned and actual start time;
- planned and actual end time;
- planned and actual duration;
- planned and actual quantity;
- target and achieved distance, repetitions, pages, lessons, calories, cost, or other module-specific measurements;
- completion percentage;
- perceived difficulty, energy, quality, or satisfaction when useful;
- a short reason or note.

Examples:

- planned run: 5 km; actual run: 3.8 km;
- planned study: 60 minutes; actual study: 40 minutes;
- planned meal: option X; actual meal: replacement Y;
- planned task: complete all sections; actual result: two of three sections.

## Confirmation flow

LifeOS must not silently mark an item as completed merely because its scheduled time passed.

When the outcome is unknown, the item becomes awaiting confirmation. The user can then confirm it with a quick action or provide a more precise result.

Confirmation should remain lightweight:

- common outcomes are available as direct controls;
- additional measurements are requested only when relevant;
- the user may confirm multiple overdue items together;
- LifeOS avoids repeatedly asking about low-value items when the user has configured a default behaviour.

## Consequences

Execution results can affect:

- daily and long-term statistics;
- remaining workload;
- routine adherence;
- goal and program progress;
- future duration estimates;
- replanning proposals;
- risk and feasibility assessments;
- recommendations for replacement, recovery, maintenance, or early program completion.

A partial result is not automatically treated as failure. Its meaning depends on the item's objective, minimum acceptable result, and remaining plan.

## History and audit

LifeOS preserves the relevant history of planned and actual states so the user can understand what changed over time. Postponing or replacing an item must not erase the fact that the original occurrence was changed.

Corrections and undo remain possible. Statistics should use the corrected current result while retaining enough history for troubleshooting and meaningful change tracking.
