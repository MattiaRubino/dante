# LifeOS V1 — Goal and Program Creation

## Principle

LifeOS supports three creation modes for goals and programs:

1. quick creation;
2. assisted creation;
3. import from an existing file or external plan.

All three modes produce the same structured LifeOS model. The difference is how much information the user provides and how much assistance is used to organise it.

## Quick creation

Quick creation accepts a minimal description such as:

- goal: reach spoken English B2;
- target period: six months;
- available time: two hours per day;
- priority: high.

LifeOS can create a simple plan immediately, for example by reserving a two-hour daily block for the requested period.

Before final confirmation, LifeOS offers an optional operational-refinement step. It may ask whether the user wants to specify details such as preferred days, preferred time windows, rest days, blocked dates, activity types, or review frequency.

The user may decline refinement. In that case LifeOS keeps the plan intentionally simple rather than forcing a questionnaire.

## Completion and user declaration

LifeOS treats the user's explicit declaration as authoritative for their own progress and results.

If the user confirms that an activity was completed, that a program was followed, or that a goal was reached, LifeOS records it accordingly. The product does not require documentary proof, a certificate, sensor evidence, or an external verification unless the user explicitly wants to track one.

LifeOS may distinguish between:

- activity completion: the planned session or commitment was reported as completed;
- program completion: the planned sequence or duration was reported as completed;
- goal achievement: the user reported that the desired result was achieved.

These distinctions are useful for organisation and statistics, but they are not an investigation into whether the user is telling the truth.

The source of a result should still be transparent, for example:

- user-confirmed;
- automatically marked according to a user-defined rule;
- imported from an integration;
- inferred provisionally and awaiting confirmation.

LifeOS should not challenge a confirmed result without a concrete reason. If the user later says that real progress is missing, the system can reassess the plan, identify likely problems, and propose a more realistic structure.

## Assisted creation

In assisted creation, the user describes the desired result naturally. LifeOS asks only for information that materially affects the plan.

The assistant may first propose a draft structure, then ask operational scheduling questions such as:

- which days are available;
- whether the activity should happen every day or only on selected days;
- whether a specific day or evening is required;
- which time windows are preferred or forbidden;
- which sessions are fixed, flexible, divisible, or optional;
- whether the user wants a lighter, balanced, or intensive version.

The interaction should remain adaptive. It must not ask for details that are unnecessary for the requested level of planning.

Before calendar insertion, LifeOS shows:

- the proposed goal and completion handling;
- milestones, activities, routines, and program steps;
- total and weekly time requirements;
- proposed days and time windows;
- conflicts and assumptions;
- flexibility and replanning rules;
- review and measurement points.

The user can approve, edit, simplify, intensify, save as a draft, or import only selected parts.

## Import from file or external plan

The user can import a plan that already exists instead of recreating it manually.

Possible sources include:

- a plan created with ChatGPT, Claude, or another assistant;
- a diet plan from a dietitian;
- a training program from a personal trainer;
- a study schedule or course syllabus;
- a medical, rehabilitation, travel, work, or project plan;
- a spreadsheet, document, PDF, structured text, image, or supported data export.

LifeOS extracts the useful structure, including dates, durations, recurrence, activities, quantities, dependencies, milestones, constraints, notes, and completion criteria.

The imported source remains attached or referenced so the user can trace where the structured plan came from.

After extraction, LifeOS asks only the missing operational questions needed to schedule the plan, for example:

- when the plan should start;
- which days and hours are available;
- whether dates in the source are mandatory or adaptable;
- how to handle missing sessions;
- which measurements or confirmations should be tracked.

LifeOS then presents a structured preview before adding anything to the calendar. The user can correct extraction errors, exclude sections, change timing, and approve the complete plan or only selected parts.

## Common output

Regardless of creation mode, the resulting structure may contain:

- goal definition;
- target period or deadline;
- milestones;
- activities and routines;
- calendar blocks and valid scheduling windows;
- measurable targets and actual results;
- dependencies and constraints;
- fallback and replanning rules;
- review cadence;
- source and provenance information;
- assumptions requiring later confirmation.

## User control

LifeOS may create a simple schedule from minimal information when the user requests simplicity. It must not force detailed optimisation.

It also must not silently invent critical restrictions, medical instructions, dietary quantities, professional recommendations, or success criteria that were not provided or approved.

No complex plan is inserted across the calendar without a visible preview and user approval.