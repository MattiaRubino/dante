# LifeOS — Phase 3 Product Definition Review

## Status

Phase 3 is complete at product-definition level.

The product now has a coherent V1 domain, operating principles, user flows, safety boundaries, and future extension path. No additional major product concept is required before beginning the coded frontend prototype.

Future discoveries may refine the model, but they should not reopen completed topics without a concrete contradiction, user need, or implementation constraint.

## Product identity

LifeOS is a personal operating system that combines:

- calendar and time planning;
- independent events, activities, reminders, routines, projects, goals, and programs;
- structured user context and constraints;
- realistic capacity rather than free time alone;
- adaptive replanning and scenario comparison;
- planned-versus-actual history;
- explainable decisions and provenance;
- configurable automation;
- low-friction capture and global command access;
- professional and personal commitments in one coherent system;
- future coordination with other people without exposing private life data.

Its defining value is not the number of modules. It is the ability to understand the user's current situation, organise competing commitments, preserve history, and adapt the future under explicit user control.

## Canonical domain

The V1 product model contains:

- planning items with explicit types and type-specific behaviour;
- events, activities or tasks, reminders, and calendar blocks;
- routines as reusable recurring patterns;
- goals as desired results;
- programs as structured progression paths;
- projects as finite bodies of work and deliverables;
- milestones as meaningful checkpoints;
- calendars or life areas as organisational contexts;
- modules as specialised domain extensions;
- participants and person-related commitments;
- sources, provenance, decisions, temporary modes, and inbox items.

Calendar assignment, item type, module, source, tag, and sharing are separate dimensions.

## Calendar and daily operation

LifeOS supports:

- one-off, all-day, recurring, fixed, flexible, windowed, and deadline-constrained items;
- recurrence exceptions and occurrence-level changes;
- day, week, month, and longer-horizon planning over the same canonical data;
- Today as the main operational surface;
- direct actions and contextual natural-language changes;
- calendars or life areas such as Personal and Work, plus user-defined areas;
- unified, grouped, and focused inspection without fixing the final visual layout;
- global conflict, travel, workload, protected-time, and capacity awareness across calendars;
- independent items that do not require a parent goal, program, project, or module.

## Scheduling and adaptation

Each item may define independent rules for:

- temporal constraint;
- movement policy;
- divisibility and partial completion;
- recurrence and persistence;
- fallback behaviour;
- replanning scope;
- preparation, recovery, spacing, and dependency needs.

LifeOS applies the smallest valid replanning scope first and expands only when necessary. Hard constraints are not violated silently. Material changes show impact and require approval according to the user's autonomy settings.

Temporary life modes provide time-bounded overrides for situations such as holiday, illness, travel, exams, intense work, or reduced availability without permanently changing the normal profile.

## Execution, confirmation, and history

The model separates:

- planning and scheduling state;
- execution outcome;
- attendance or participation;
- confirmation and provenance;
- planned and actual measurements.

Postponement, rescheduling, replacement, cancellation, correction, and reopening preserve relevant history instead of rewriting what happened.

Confirmation and reminder policy is configurable globally and by module, program, routine, or item. Automatic completion is disabled by default and records its provenance when explicitly enabled.

## Goals, projects, programs, and routines

Goals describe results. Projects coordinate finite work and deliverables. Programs define structured progression. Routines define repeated patterns.

Goals and programs can be created quickly, with assistance, or by importing existing plans. Complex plans require a preview before calendar insertion.

Programs use a simple visible lifecycle:

- Draft;
- Scheduled;
- Active;
- Paused;
- Finished.

Structural changes use effective-dated versions. Past execution remains attached to the version active at the time. Pauses suspend future generated work rather than deleting it. Resumption uses a previewed replan. Replacement and continuation create linked history instead of rewriting the original program.

## User context and profile

LifeOS maintains structured, editable, scope-aware user context, including:

- explicit facts and preferences;
- availability and protected time;
- active constraints;
- current commitments and programs;
- resources, equipment, locations, and budget where relevant;
- imported professional instructions;
- temporary conditions;
- observed patterns that remain distinct from declared preferences.

Every fact can carry source, confirmation, validity, sensitivity, scope, and reuse controls.

Onboarding remains light. Information is divided into account-required, function-required, and optional enrichment. Additional data is requested progressively only when it materially affects the requested function.

## Adaptive intelligence

The V1 product direction includes:

- capacity beyond free clock time;
- scenario simulation before meaningful changes;
- balance and allocation across life areas;
- declared preference versus observed behaviour;
- configurable autonomy by scope;
- universal text-and-file inbox;
- decision rationale and provenance;
- person-related commitments;
- global search, questions, navigation, and validated commands.

These concepts belong to V1, but automation depth increases progressively. The first release may use deterministic rules, structured commands, mock providers, and manual AI-assisted workflows before a production AI API is connected.

## Professional work and meetings

LifeOS supports personal work coordination without becoming an enterprise collaboration suite.

A meeting may include:

- purpose and expected outcome;
- agenda and preparation;
- attendees, availability, time zones, buffers, and location;
- notes, imported transcript or recording references;
- decisions, unresolved questions, commitments, and follow-up;
- action items converted into normal LifeOS items;
- persistent memory across recurring meetings;
- focus protection, fragmentation analysis, and recurring-meeting review;
- optional startup, shutdown, and return-from-absence briefs.

Provider-specific scheduling, meeting, email, and messaging integrations remain progressive V1 work.

## Privacy, safety, and user authority

LifeOS uses purpose limitation, data minimisation, user-controlled retention, export, deletion, provenance, and stronger protection for sensitive data.

The user remains authoritative over their own reported results and profile updates. AI-generated or inferred content does not silently become confirmed truth.

Health, dietary, rehabilitation, and accessibility context can be used for compatibility and personal organisation, but V1 is positioned as a lifestyle, wellbeing, and organisation product rather than a diagnostic or clinical system.

Before public launch, privacy, security, consent, retention, processor, legal-copy, and medical-device-boundary review remain mandatory.

## Release slicing

The product definition is intentionally broader than the first deployable build.

### V1.0 — first usable personal release

The first usable release should prioritise:

- account and lightweight profile;
- native calendars or life areas;
- events, activities, reminders, routines, projects, goals, and basic programs;
- recurrence, scheduling constraints, direct editing, and basic replanning;
- Today and core calendar horizons;
- execution outcomes, confirmation, reminders, and history;
- manual or deterministic program creation with preview;
- text-and-file inbox;
- keyword and structured global search;
- common validated commands;
- manual meeting agenda, decision, and follow-up support;
- basic temporary modes, capacity fields, autonomy settings, and scenario preview;
- privacy controls, provenance, export foundations, and safe deletion;
- mock or manual AI gateway instead of mandatory production AI.

### Progressive V1.x

Later V1 iterations can add:

- production AI providers;
- richer simulations and behavioural learning;
- semantic search and long-term question answering;
- stronger capacity estimation;
- Google and Microsoft calendar synchronisation;
- email, Teams, Meet, Zoom, Slack, file, and meeting-recap integrations;
- voice, image, screenshot, and broader inbox capture;
- booking links, scheduling polls, and safe external availability;
- advanced professional analytics and return briefs;
- deeper modules such as learning, training, nutrition, travel, finance, or creative workflows.

### V2 and later

Deferred beyond personal V1:

- full account-to-account shared editing;
- invitations and participant coordination;
- small private social groups and activity discovery;
- safe free/busy matching;
- shared trips, activities, and responsibilities;
- team workspaces, assignments, roles, and enterprise governance;
- organisational routing, rooms, resources, and team analytics.

## Decisions intentionally deferred to Phase 4 or implementation

The following are not missing product decisions:

- final navigation;
- final web and mobile layout;
- timeline, card, lane, column, or grouped-calendar presentation;
- visual design system, colours, typography, spacing, and animation;
- exact analytics screens and metric presentation;
- detailed interaction design for the global command surface;
- precise responsive behaviour;
- provider-specific OAuth, webhook, polling, sync, and conflict algorithms;
- database schema and API contracts;
- production AI provider and model selection;
- final pricing, product name, domain, and public positioning;
- final legal wording and consent copy.

These decisions require prototypes, technical investigation, user testing, provider constraints, or launch preparation.

## Audit findings and corrections

The final review found no unresolved contradiction in the main product direction after these corrections:

1. `Project` is now explicitly separated from goal, program, and routine.
2. Scheduling state, execution outcome, attendance, confirmation, and actual values are separate dimensions.
3. Global search and command is a cross-cutting capability rather than a chat owned by one screen.
4. Calendar or life area remains separate from sharing, item type, module, source, and tags.
5. Work support is limited to personal coordination in V1; enterprise collaboration remains later.
6. Visual examples discussed during planning are not fixed frontend requirements.
7. Full V1 product architecture is separated from the smaller V1.0 implementation slice.

## Primary risks

### Scope inflation

The model is intentionally rich. Release slicing and progressive automation are required. V1.0 must not attempt every integration and advanced module at once.

### Interface overload

The backend model may be complex, but ordinary use must remain quick. Progressive disclosure, sensible defaults, contextual questions, and realistic prototype testing are mandatory.

### AI reliability

AI produces structured proposals, not unchecked database writes. Backend validation, provenance, preview, permissions, and undo remain mandatory.

### Sensitive-data exposure

Scope-aware retrieval, separate sensitive controls, minimised provider prompts, and privacy review are required before connected AI or public use.

### Integration complexity

External calendars, meetings, messages, and documents require provider abstractions and incremental delivery. Native LifeOS behaviour must remain useful without every integration.

## Phase 4 entry criteria

Phase 4 may begin because the following are now defined:

- V1 product identity and boundaries;
- core domain vocabulary;
- primary planning and execution behaviour;
- goals, projects, routines, and program lifecycle;
- Today and first-run capabilities;
- grouped and focused calendar requirements;
- adaptive intelligence principles;
- profile, history, privacy, and safety rules;
- global command and work-meeting requirements;
- release slicing and deferred decisions.

Phase 4 should build a coded UX prototype using realistic light and dense sample data. It should validate discoverability, speed, information density, progressive disclosure, and consistency across web and mobile before backend implementation expands.

## Closure decision

Phase 3 is closed.

The next project activity is Phase 4: coded frontend and interaction prototyping. New product concepts should enter through a recorded change or backlog item rather than reopening the complete definition process.
