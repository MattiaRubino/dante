# LifeOS V1 — Today Experience

## Role of the Today view

The Today view is the main operational surface of LifeOS. It helps the user understand the current day, act on planned items, react to changes, and move between immediate execution and broader planning.

This document defines capabilities, not final layout or visual design.

## Core daily actions

From the Today view, the user can:

- see all events, activities, routines, and program steps relevant to the current day;
- expand an item to view its full details;
- edit, move, postpone, cancel, complete, skip, or reopen an item when allowed;
- add a quick event or activity;
- create or import a more structured routine, program, or plan;
- see completed, pending, skipped, missed, and unconfirmed items;
- open linked goals, programs, projects, modules, attachments, locations, and notes;
- see conflicts, schedule pressure, and meaningful changes requiring attention.

## Contextual interaction and replanning

An expanded item can expose a contextual conversation or command surface tied to that specific item and its surrounding plan.

The user can express intentions naturally, for example:

- “Today I do not want this lunch; use option Y instead.”
- “Move this to next week and suggest an equivalent replacement for today.”
- “Swap these two activities.”
- “I only have thirty minutes; shorten or split this activity.”
- “I cannot do this outdoors because of the weather.”
- “Keep today's change, but do not alter the rest of the routine.”
- “Apply this change to the future program as well.”

The system interprets the request in the context of the selected item, checks related constraints, and produces a concrete proposal. A proposal may:

- replace an item with an equivalent alternative;
- move an item to another valid time;
- exchange the positions of two compatible items;
- shorten, split, merge, postpone, skip, or cancel an item;
- adjust connected preparation, travel, recovery, meal, or dependency blocks;
- apply a change only once or update the originating routine or program;
- explain which deadlines, goals, priorities, or future activities would be affected.

Material changes are shown before application. The user remains authoritative and can confirm, modify, or reject the proposal. Simple low-risk edits may be applied directly when the user's instruction is unambiguous and the user has enabled that behaviour.

The interaction surface must not require a long conversation for simple actions. Direct controls remain available for common edits, while natural-language interaction is an additional faster path for contextual or multi-step changes.

The product experience can be implemented before a production AI provider is enabled by using structured commands, deterministic rules, mock responses, and manual ChatGPT-assisted import/export. The domain action and proposal formats remain the same when a future API provider is connected.

## Contextual intelligence

The Today view may surface information that affects execution, including:

- hourly weather when relevant to outdoor activities, travel, or events;
- events or activities at risk because of weather, timing, travel, conflicts, missing preparation, or low remaining capacity;
- high-priority or urgent items;
- items whose timing should be reconsidered;
- concise suggestions or warnings without forcing automatic changes.

Contextual information should be useful and selective. The interface must not become a permanent wall of warnings.

## Expandable planning horizon

The user can move from the current day to broader horizons:

- day;
- week;
- month;
- year.

These are different views over the same planning system, not separate products. The longer the horizon, the more the interface shifts from execution details toward patterns, load, milestones, deadlines, and progress.

## Statistics and progress

The user can access relevant statistics and summaries, including:

- completion and confirmation trends;
- planned versus completed workload;
- consistency and routine adherence;
- goal and program progress;
- time allocation by category or module;
- recurring conflicts, overload, postponements, and missed items;
- longer-term patterns across weeks, months, and years.

Detailed analytics layout and exact metrics remain a later UX and product-design decision.

## Design boundary

The current phase decides what the Today experience must support. It does not yet decide:

- exact screen composition;
- navigation placement;
- card, timeline, agenda, or calendar layout;
- visual hierarchy, colours, spacing, or animations;
- which statistics appear directly on Today versus a dedicated analytics view.

Those decisions will be made during the coded UX prototype.