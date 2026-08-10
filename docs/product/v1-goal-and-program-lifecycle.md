# LifeOS V1 — Goal and Program Lifecycle

## Principle

Goals and programs must remain simple to understand for the user while preserving enough history to support reliable scheduling, analytics, adaptation, and recovery from mistakes.

A goal describes the result the user wants. A program describes an organised path of activities, routines, milestones, and rules intended to support one or more goals. A goal may exist without a program, and a program may continue, finish, or be replaced without automatically deciding the state of the goal.

## Visible lifecycle

The user-facing lifecycle uses a small set of clear states:

- Draft;
- Scheduled;
- Active;
- Paused;
- Finished.

Archiving is a separate visibility action rather than a lifecycle state.

Internally, a finished program also records how it ended, for example:

- completed;
- ended early;
- cancelled before starting;
- replaced by another program;
- merged into another program.

This avoids exposing an unnecessarily technical list of states while preserving accurate history.

## Draft

A draft may be incomplete, imported but not yet reviewed, or still under discussion with the assistant.

A draft:

- does not generate active commitments or notifications;
- may contain tentative dates and calendar previews;
- may be edited freely;
- may be duplicated, deleted, or approved;
- may show missing information or unresolved conflicts.

## Scheduled

A program becomes scheduled after the user approves it and it has a future start date.

Scheduled items may appear in future calendar views, but the program has not yet begun. Before activation, the user can still change the plan without treating those changes as execution-time adaptations.

If the user cancels it before the start, it is closed with the outcome `cancelled before starting` rather than recorded as a failed or abandoned active program.

## Active

A program becomes active when its start condition is reached or when the user starts it manually.

While active, LifeOS:

- generates or manages its relevant planning items;
- tracks user-reported execution and outcomes;
- applies approved confirmation and replanning rules;
- compares actual progress with the current program structure;
- preserves the historical version that governed each completed period.

## Pause

Pausing means temporarily stopping the program without losing its history or treating it as finished.

A pause records:

- when the pause begins;
- an optional expected resume date;
- an optional reason;
- what should happen to future program-generated items.

The recommended default is:

- completed and past items remain unchanged;
- future program-generated items become suspended rather than deleted;
- fixed external commitments are not moved silently;
- notifications and automatic generation for the paused program stop;
- unrelated calendar items remain untouched.

When pausing, the user can choose or approve a policy such as:

- freeze the program and decide later;
- shift the remaining plan by the pause duration;
- replan from a new resume date;
- preserve the original deadline and propose reductions or compression;
- keep selected fixed items active while suspending the rest.

LifeOS must show the impact before applying a structural change.

## Resume

Resuming a paused program does not blindly restore old dates. LifeOS checks the current calendar, active constraints, elapsed time, missed dependencies, recovery requirements, and any changed user context.

It then proposes the smallest valid adjustment, such as:

- continue from the next unfinished step;
- shift remaining items;
- rebuild only the current week;
- repeat a previous phase;
- reduce or extend the program;
- preserve the deadline with an explicit trade-off;
- create a revised continuation when the old structure is no longer suitable.

The user approves material changes before they are committed.

## Editing an active program

An active program is never rewritten as though the new structure had always existed.

Changes use effective-dated versions:

- past execution remains attached to the version that was active at the time;
- the new version applies from an explicit date or program step;
- the reason and origin of the change are recorded;
- the user can compare major versions and undo a recent mistake.

Minor operational changes, such as moving one occurrence, remain occurrence-level exceptions. Structural changes, such as changing weekly volume, phases, milestones, or completion rules, create a new program version.

Before applying a structural revision, LifeOS shows:

- what changes;
- which future items are affected;
- whether the deadline, workload, milestones, or linked goals change;
- which assumptions or constraints caused the revision.

## Completion and user authority

A program may be completed because:

- its defined activities or duration have been completed;
- its final milestone has been reached;
- the user explicitly declares it complete;
- an approved completion rule marks it complete.

The user's explicit declaration is authoritative. LifeOS does not require external proof.

Completing a program does not automatically complete every linked goal. At closure, LifeOS may ask whether linked goals should also be marked achieved, remain active, or receive a follow-up program.

## Ending early

The user can stop a program at any time without deleting it.

Ending early:

- preserves all completed history and actual results;
- stops or suspends future generated items according to the chosen closure action;
- records an optional reason without forcing one;
- allows unresolved items to be cancelled, left independent, moved elsewhere, or included in a replacement program;
- does not label the user as having failed.

Useful optional reasons may include changed priorities, unsuitable plan, health or availability change, goal no longer relevant, external interruption, or replacement by a better plan.

## Replacement and continuation

When a program is replaced, LifeOS links the old and new programs rather than erasing the old one.

The replacement may inherit selected goals, constraints, unfinished milestones, source documents, and relevant history, but it receives its own lifecycle and versions.

A closed program should normally remain closed. If closure was accidental, the user can undo it. Otherwise, continuing later creates a linked continuation or new cycle so historical reporting remains accurate.

## Archiving

Archiving hides a program from normal active views without deleting it or changing how it ended.

Archived programs remain available for:

- history and statistics;
- comparison;
- duplication;
- continuation;
- source and decision traceability.

Deleting is reserved for erroneous or unwanted data and follows the product's deletion and recovery rules.

## Relationship with calendar items

Closing, pausing, or revising a program must handle its future items explicitly.

LifeOS distinguishes:

- program-generated items that can be suspended or regenerated;
- items already completed or historically modified;
- independent items merely linked to the program;
- fixed external commitments that must not be moved silently;
- shared items whose other participants may be affected.

No broad program action silently rewrites completed history or unrelated commitments.

## Recommended default behaviour

The default product behaviour is:

1. keep the visible state model small;
2. preserve detailed closure outcomes internally;
3. pause by suspending future generated work, not deleting it;
4. resume through a previewed replan rather than a blind date shift;
5. version structural changes from an effective date;
6. preserve past execution exactly as it occurred;
7. treat user-declared completion as authoritative;
8. keep goals and programs related but independently controllable;
9. use replacement and continuation links instead of rewriting history;
10. archive for cleanliness and delete only for actual removal.