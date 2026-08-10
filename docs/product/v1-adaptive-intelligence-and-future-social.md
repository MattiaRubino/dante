# LifeOS V1 — Adaptive Intelligence and Future Social Direction

## Principle

LifeOS should not behave like a calendar with a chat layer. Its distinctive value is the ability to maintain a structured model of the user's current situation, evaluate what is realistically sustainable, explain trade-offs, and adapt plans without destroying history or user control.

The following capabilities are part of the product direction. They are all important, but they do not all need to be fully automated in the first technical release. V1 must establish the domain model and user flows so that progressively stronger automation can be added without redesigning the product.

## 1. Temporary life modes

Users can activate temporary conditions that change how LifeOS plans without permanently rewriting their normal profile.

Examples include:

- holiday;
- illness or recovery;
- travel;
- intense work period;
- exams;
- moving home;
- reduced availability;
- guest or family period;
- temporary pause from one or more life areas.

A temporary mode may affect availability, sleep and quiet hours, workload limits, location, equipment, priorities, routines, notifications, and selected programs.

Every mode has a start, optional end, affected scopes, and an explicit restoration or review policy. When it ends, LifeOS restores previous defaults or proposes an updated continuation rather than silently keeping temporary settings forever.

## 2. Capacity beyond free time

LifeOS should distinguish available clock time from realistic capacity.

Relevant dimensions may include:

- mental energy;
- physical energy;
- concentration;
- emotional load;
- recovery needs;
- stress reported by the user;
- transition and context-switching cost;
- difficulty and intensity of the planned activity;
- recent workload and sleep information when available and authorised.

These factors may initially be user-declared or rule-based. They must not pretend to be medical measurements.

The scheduler can therefore recognise that a two-hour free window is not automatically suitable for two hours of demanding work. It may propose a lighter activity, a shorter session, recovery, or movement to a more suitable period.

## 3. Scenario simulation

Before applying a meaningful new goal, program, routine, or structural change, LifeOS can simulate alternatives.

A simulation may compare:

- required time;
- expected workload;
- affected sleep or protected time;
- conflicts with current commitments;
- deadlines and milestones;
- equipment, location, travel, or budget constraints when relevant;
- activities that would need to be reduced, moved, paused, or removed;
- practical sustainability based on the user's declared rules and past behaviour.

The result is a set of understandable scenarios rather than a false numerical certainty. Nothing is applied until the user selects or approves a proposal.

## 4. Balance and allocation across life areas

LifeOS tracks how time, attention, workload, and repeated postponements are distributed across user-defined life areas such as Work, Personal, Family, Study, Health, Social, or custom calendars.

The system does not impose a universal ideal balance. It surfaces patterns and trade-offs, for example:

- one area consistently displacing another;
- important goals receiving no practical time;
- rest being repeatedly sacrificed;
- social commitments being postponed more often than work;
- low-value routines consuming capacity needed by a declared priority.

These observations remain explainable and tied to actual history.

## 5. Declared preferences versus observed behaviour

LifeOS distinguishes among:

- what the user explicitly says;
- what completed history appears to show;
- temporary exceptions;
- confirmed reusable rules;
- uncertain hypotheses.

Observed behaviour does not silently override the user's statement. When there is a meaningful difference, LifeOS can ask whether the declared preference should be updated or whether the observed period was exceptional.

Every learned preference keeps provenance, confidence, validity period, scope, and user control.

## 6. Configurable autonomy

AI and automatic planning should not use one universal permission level.

The user can define autonomy by calendar, item type, program, routine, or individual item. Suggested levels are:

1. suggestions only;
2. propose changes and require confirmation;
3. apply minor changes automatically within approved limits;
4. manage a defined scope autonomously within explicit constraints.

Examples:

- never move medical appointments;
- move training within a two-day window;
- redistribute study sessions inside the same week;
- replace a lightweight routine automatically;
- propose meal substitutions but never apply them without approval.

Every automatic action remains traceable and reversible according to the product's history rules.

## 7. Universal inbox and capture

LifeOS provides a low-friction capture point for information that the user has not yet classified.

Supported inputs may progressively include:

- free text;
- voice notes or transcription;
- screenshots and photos;
- files and PDFs;
- forwarded or connected messages;
- plans created elsewhere;
- vague ideas;
- activities without dates;
- reminders to revisit something later.

LifeOS proposes whether the input represents an event, activity, goal, program, constraint, personal fact, document, note, or unresolved item.

Ambiguous inputs may remain safely in the inbox or require one focused clarification. The system must not force immediate classification or silently turn uncertain content into active commitments.

## 8. Decision history and rationale

LifeOS records not only what changed but why it changed.

A meaningful decision may include:

- previous and new value;
- affected scope;
- date of effect;
- reason;
- source or evidence used;
- whether the proposal came from the user, LifeOS, an imported plan, or another integration;
- who approved it;
- related scenarios or rejected alternatives.

This allows the user to later ask why a program was reduced, extended, paused, or replaced and receive an answer grounded in actual history rather than reconstructed speculation.

## 9. Commitments involving other people

Even in a personal V1, LifeOS should distinguish between a purely private task and a commitment involving another person.

Examples include:

- calling someone;
- replying to a message;
- delivering something to a colleague;
- buying something for a family member;
- organising a shared activity;
- remembering an important date;
- completing something that was promised.

An item may therefore be personal, related to another person, or fully shared. This distinction can affect priority, reminders, postponement warnings, and later collaboration features without turning V1 into a social network.

## V1 implementation boundary

The concepts above belong to the V1 product model, but the first usable release should implement them in stages.

### Foundation required in the first release

- temporary modes with basic scoped overrides;
- capacity fields and user-declared energy or workload constraints;
- a simple scenario preview for meaningful plan changes;
- life-area allocation and postponement history;
- explicit separation of declared preferences and observed patterns;
- per-scope autonomy settings;
- a text-and-file inbox;
- decision provenance and rationale;
- person-related commitments without account-to-account collaboration.

### Progressive intelligence

Later V1 iterations may improve:

- stronger behavioural learning;
- more detailed capacity estimation;
- richer simulations;
- voice, image, email, and broader capture integrations;
- increasingly autonomous planning inside user-defined limits;
- proactive but controlled balance and sustainability insights.

This prevents V1 from becoming an endless all-at-once implementation while preserving the correct architecture from the beginning.

## Future social and coordination direction — V2

A later version may add a social and coordination layer. The goal is not to build a dating app or a general social feed. The focus is helping people organise real activities, commitments, and shared plans.

Possible directions include:

- invite another LifeOS user to an event or activity;
- coordinate availability and propose suitable times;
- create small private groups for friends, family, travel, study, hobbies, or recurring activities;
- suggest activities based on shared interests, location, availability, and explicit preferences;
- publish an activity to a limited circle and allow others to join;
- organise trips, dinners, games, training, study sessions, or local events;
- coordinate shared responsibilities and follow-ups;
- discover opt-in local activities without exposing the user's private calendar;
- allow each participant to keep personal notes, reminders, and calendar placement while sharing canonical event facts.

Privacy and consent are central. LifeOS must never expose a user's detailed availability, private goals, health context, personal history, or full calendar merely to calculate coordination. Availability should be represented through safe abstractions such as free/busy windows or explicit user-approved options.

## Product identity

LifeOS is not defined by the number of modules it contains. Its identity is the combination of:

- structured personal context;
- realistic capacity;
- adaptive programs;
- explainable decisions;
- scenario comparison;
- historical integrity;
- configurable autonomy;
- low-friction capture;
- coordination that respects personal boundaries.

The system should become more useful as it learns, while remaining understandable, editable, reversible, and under the user's authority.
