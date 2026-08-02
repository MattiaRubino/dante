# LifeOS V1 — Work Context and Meeting Lifecycle

## Principle

LifeOS should support professional life without becoming a full enterprise project-management suite.

The useful boundary is personal work coordination: protecting focus, organising meetings, preparing decisions, capturing commitments, connecting follow-up work to the user's calendar and programs, and preserving continuity across recurring professional interactions.

A meeting is not only a timed calendar event. It may have preparation before it, a purpose and agenda during it, decisions and commitments produced by it, and follow-up work after it.

## Work context

A planning item may optionally be connected to work context such as:

- organisation or client;
- team;
- project or workstream;
- role or responsibility;
- meeting series;
- person or group involved;
- source system such as an external work calendar, email, Teams, Slack, Meet, Zoom, or another integration.

These relationships are optional. A simple work event must remain quick to create.

LifeOS should allow different working patterns without hard-coding one universal office model. Relevant context may include:

- normal working hours;
- protected focus windows;
- office, remote, hybrid, travel, or client-site location;
- time zones;
- expected response windows;
- meeting-free periods;
- maximum acceptable meeting load;
- preparation and recovery buffers;
- role-specific work patterns configured by the user rather than inferred as absolute truth.

## Meeting types

Meetings may be classified when useful, for example:

- decision meeting;
- working session;
- status update;
- one-to-one;
- client or external call;
- interview;
- planning or review;
- presentation;
- informal coordination;
- social or team interaction.

The type can influence default duration, preparation, follow-up, required participants, and whether an asynchronous alternative should be considered.

The system must not force classification when a normal calendar event is sufficient.

## Before the meeting

A meeting may contain or generate:

- explicit purpose;
- expected outcome;
- agenda;
- decision or approval required;
- required and optional attendees;
- pre-read documents or links;
- questions to prepare;
- preparation activity and protected preparation time;
- location, meeting link, room, or resource;
- minimum notice;
- buffer before and after;
- cancellation and rescheduling rules;
- local time presentation for every relevant participant.

LifeOS can warn when a meaningful meeting has no clear purpose, required preparation cannot fit, or the proposed time violates protected focus, recovery, travel, or personal constraints.

The warning should remain advisory unless an explicit hard rule applies.

## Scheduling and availability

LifeOS should eventually support professional scheduling patterns such as:

- offering selected availability instead of exposing a complete calendar;
- personal booking links with scoped rules;
- choosing among proposed times;
- collecting participant votes;
- considering multiple calendars;
- limiting meeting duration and daily booking count;
- minimum and maximum scheduling notice;
- buffers and travel time;
- time-zone fairness;
- co-host or required-participant availability;
- room or resource requirements;
- round-robin or routing to the appropriate person in later collaborative or business versions.

For V1, the core requirement is a safe availability model and structured meeting proposals. Full organisational routing is not required.

## During the meeting

LifeOS may attach or import:

- manual notes;
- agenda progress;
- transcript or recording reference;
- decisions;
- unresolved questions;
- commitments;
- action items;
- owners;
- due dates;
- related documents;
- attendance information when available and authorised.

AI-generated notes, summaries, decisions, or tasks are always treated as proposals or imported outputs with provenance. They must remain editable and must not be presented as guaranteed truth.

Recording or transcription requires appropriate consent, provider rules, and privacy controls. LifeOS does not silently record meetings.

## After the meeting

The meeting remains a useful object after its end.

LifeOS can support:

- concise recap;
- confirmed decisions;
- assigned follow-up activities;
- unresolved items;
- deadlines and owners;
- documents and source links;
- next meeting or review date;
- reminders for commitments;
- connection to goals, programs, projects, clients, or people;
- a check that action items received realistic calendar capacity.

A follow-up task should be a normal LifeOS planning item linked to the meeting, not text trapped inside meeting notes.

When an action is assigned to another person, LifeOS records the user's relevant commitment or expected follow-up without pretending to control the other person's task system.

## Recurring meeting memory

Recurring meetings should share a persistent series context while preserving each occurrence separately.

A meeting series may retain:

- continuing purpose;
- participants;
- recurring agenda template;
- previous decisions;
- unresolved items carried forward;
- commitments due before the next occurrence;
- relevant documents;
- changes in cadence or ownership;
- occurrence-specific notes and outcomes.

Before the next occurrence, LifeOS can prepare a continuity brief showing what changed since the previous meeting and which commitments remain open.

This is especially useful for one-to-ones, project reviews, client calls, coaching sessions, and recurring planning meetings.

## Meeting load and focus protection

LifeOS should evaluate more than total meeting hours.

Relevant patterns include:

- fragmented workdays;
- insufficient uninterrupted focus time;
- repeated back-to-back meetings;
- meetings outside declared working hours;
- cross-time-zone burden;
- excessive context switching;
- lack of preparation or recovery time;
- concentration of meetings on already low-capacity periods;
- important personal commitments repeatedly displaced by work calls.

Possible proposals include:

- group compatible calls;
- preserve or restore focus blocks;
- shorten a meeting;
- move a flexible meeting;
- add preparation or recovery time;
- convert a status update into an asynchronous update;
- change the cadence of a recurring meeting;
- decline or mark attendance as optional where appropriate;
- expose the trade-off before applying any change.

LifeOS must not automatically decline, cancel, or move meetings involving other people unless the user has explicitly authorised that scope and the external provider supports it safely.

## Meeting usefulness and recurring review

LifeOS may help the user review recurring meetings based on observable history, not subjective surveillance.

Signals may include:

- repeated cancellation or postponement;
- no agenda or preparation;
- no decisions or follow-up over many occurrences;
- frequent overruns;
- consistently optional attendance;
- low personal relevance declared by the user;
- duplicated purpose with another meeting;
- cadence that no longer matches actual work.

The system can propose keeping, shortening, combining, changing cadence, converting to asynchronous coordination, or ending the series.

It should not make hidden productivity judgments about other people.

## Asynchronous work and coordination tax

Not every coordination need deserves a call.

LifeOS can distinguish between work requiring live interaction and work that may be handled through:

- a written update;
- shared notes;
- a decision request;
- a document review;
- a recorded explanation;
- a task assignment;
- a question with an expected response date.

The goal is not to eliminate meetings, but to protect the user's time and ensure that the chosen communication form matches the required outcome.

## Workday startup and shutdown

A lightweight professional daily flow may help the user:

### Start of day

- review today's work commitments;
- identify preparation required for calls;
- surface overdue follow-ups;
- protect the most important focus period;
- resolve conflicts between work and personal calendars;
- choose what should not be attempted today.

### End of day

- capture unfinished work;
- confirm decisions and commitments;
- schedule realistic follow-up;
- prepare tomorrow's first action;
- identify anything that needs communication;
- close or defer work without leaving every item mentally active.

These flows remain optional and configurable, not mandatory rituals.

## Return and continuity brief

After holiday, illness, travel, or another absence, LifeOS may prepare a return brief based on authorised connected sources and existing LifeOS history.

It may show:

- meetings and decisions that occurred during the absence;
- changed deadlines;
- new or unresolved commitments;
- items requiring a response;
- programs and projects affected;
- a proposed re-entry plan that does not overload the first day back.

This extends temporary life modes into a useful professional recovery workflow.

## Universal search and command access

Work information should be accessible through the same global search and command capability used by the rest of LifeOS.

Examples include:

- show decisions from the last three client calls;
- what did I promise Marco;
- prepare the agenda for tomorrow's project review;
- find the document linked to the previous meeting;
- list follow-ups without calendar time;
- why was this recurring meeting shortened;
- protect two hours of focus before Friday's review;
- simulate moving all flexible calls out of Wednesday.

Search results and actions must respect source permissions, privacy, and user confirmation rules.

## V1 boundary

### Foundation for V1

- optional work contexts and relationships;
- meeting purpose, agenda, preparation, decisions, and follow-up;
- linked action items with owners and dates;
- recurring meeting continuity;
- focus, buffer, working-hour, and time-zone constraints;
- meeting-load and fragmentation awareness;
- workday startup and shutdown reviews;
- global search across authorised professional context;
- imported summaries and transcripts with provenance;
- no silent recording or sharing.

### Progressive V1 integrations

- Google and Microsoft calendar synchronisation;
- Meet, Teams, Zoom, Slack, email, and document references;
- imported or provider-generated meeting recaps;
- safe booking links and scheduling polls;
- automatic capture of proposed actions from connected systems;
- richer return briefs and professional analytics.

### Later collaborative or business versions

- team availability coordination;
- organisational booking and routing;
- room and resource management;
- shared workspaces and permissions;
- assignment and status synchronisation across participants;
- team-level meeting and workload analytics;
- administrative policies and enterprise governance.

## Recommended product position

LifeOS should not compete with Teams, Slack, Zoom, Jira, or enterprise project-management systems by reproducing them.

It should sit above the user's authorised tools and connect professional commitments to the rest of the user's life:

- whether the meeting fits;
- what preparation it needs;
- what decision it produced;
- what the user promised;
- when the follow-up can realistically happen;
- what work is displacing personal priorities;
- how to preserve continuity without carrying the entire workday mentally.
