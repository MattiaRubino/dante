# LifeOS V1 Scope

## Product model

LifeOS V1 is designed primarily for individual use. Each registered user manages their own calendar, goals, activities, programs, preferences, and personal data.

The architecture must not assume that all calendar items are permanently private or owned by exactly one user.

## Planning item model

LifeOS uses a common planning-item foundation with explicit types and type-specific behaviour. The purpose is not to force every item into the same workflow, but to avoid building unrelated systems for concepts that share scheduling, reminders, recurrence, visibility, notes, links, and status.

Initial item families include:

- events;
- activities and tasks;
- routines and recurring templates;
- programs and structured plans;
- reminders and calendar blocks where useful.

Each family may contain subtypes. Examples include one-off events, all-day events, appointments, flexible activities, deadline-only tasks, measurable activities, recurring routines, and multi-step programs.

Type-specific data and behaviour should remain separate from the common item fields so that the model does not become one oversized generic record.

## Standard calendar and planning capabilities

LifeOS must support the normal baseline expected from modern calendar and planning applications, including where relevant:

- one-off and recurring items;
- fixed dates and times;
- all-day items;
- flexible scheduling windows;
- deadlines;
- reminders and notifications;
- locations and travel-related context;
- notes, links, attachments, colours, and visibility;
- completion, cancellation, postponement, and confirmation states;
- recurrence exceptions and editing one occurrence or the whole series;
- links to goals, projects, programs, routines, and optional modules.

The exact capabilities available depend on the selected item type.

## Shared events and activities

A calendar item may be personal or shared with multiple users.

Shared items have:

- one common event or activity record for shared facts such as title, schedule, location, and shared description;
- one participant record per user for personal state and preferences.

Participant-specific data may include:

- invitation or attendance status;
- personal reminders;
- private notes;
- local colour or visibility preferences;
- personal completion or confirmation state;
- links to the participant's own goals, plans, travel time, and surrounding activities.

A change to shared facts can be propagated to all participants, while each participant continues managing their own LifeOS independently.

## Independent calendar items

Activities and events may exist independently. They do not require a parent goal, program, project, routine, or optional module.

Connections to higher-level structures remain optional and can be added only when they provide real value. This keeps simple actions such as an appointment, dinner, errand, or one-off workout quick to create and manage.

An item may later be linked to one or more relevant structures without being recreated.

## V1 boundary

V1 focuses on personal planning and management.

The domain model supports participants and shared-item ownership from the beginning, but V1 does not require the complete account-to-account collaboration flow. Invitations, participant account linking, shared editing rules, attendance coordination, and broader collaboration may be activated in a later version without redesigning personal items.

V1 also does not require team workspaces, shared project management, role hierarchies, task assignment, group chat, or granular collaborative permissions.
