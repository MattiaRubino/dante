# LifeOS V1 Scope

## Product model

LifeOS V1 is designed primarily for individual use. Each registered user manages their own calendar, goals, activities, programs, preferences, and personal data.

The architecture must not assume that all calendar items are permanently private or owned by exactly one user.

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

## V1 boundary

V1 does not require full collaboration features such as team workspaces, shared project management, role hierarchies, task assignment, group chat, or granular collaborative permissions.

The domain model must nevertheless preserve a future path to shared items and broader collaboration without requiring the personal calendar model to be rebuilt.
