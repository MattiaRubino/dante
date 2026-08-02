# LifeOS V1 — Global Search and Command

## Principle

LifeOS should provide one cross-cutting way to find information, understand history, and request actions without forcing the user to remember where each object is stored.

This capability is broader than a chat screen. It is a permission-aware search, question, navigation, and command layer over the user's authorised LifeOS data and connected sources.

The final visual entry point is deferred to the frontend phase.

## Searchable domains

The global capability may search across:

- events, activities, routines, reminders, and calendar blocks;
- goals, programs, projects, milestones, and progress;
- calendars and life areas;
- people, participants, organisations, clients, and commitments;
- notes, attachments, imported plans, and source documents;
- meeting agendas, decisions, recaps, and follow-up actions;
- user preferences, active constraints, temporary modes, and reusable rules;
- execution history, actual results, postponements, replacements, and confirmations;
- decision history and recorded rationale;
- authorised external calendars, files, messages, and integrations.

Search must remain scope-aware. Sensitive or unrelated data is not exposed merely because it exists.

## Question examples

The user may ask questions such as:

- how much did I run last month;
- why was my language program reduced;
- which commitments to Marco are still open;
- where is the physiotherapy plan I imported;
- which days are overloaded next week;
- what repeatedly displaces my personal time;
- what was decided in the last three client calls;
- which activities are awaiting confirmation;
- which goals have received no time recently.

Answers must distinguish confirmed records, imported information, calculated results, and uncertain inference.

## Command examples

The same surface may accept actions such as:

- create an appointment tomorrow at 16:00;
- pause training for one week;
- activate holiday mode from 10 to 24 August;
- protect two hours of focus before Friday's review;
- move flexible work calls away from Wednesday;
- prepare an agenda from unresolved items in the previous meeting;
- create three scenarios for adding Japanese study;
- show and then cancel low-priority items affected by this change.

## Action handling

A request is converted into a structured domain command or proposal.

LifeOS then:

1. resolves the intended objects and scope;
2. checks permissions, current versions, constraints, conflicts, and consequences;
3. asks one focused clarification only when a material ambiguity cannot be resolved safely;
4. shows a preview for broad, destructive, shared, sensitive, or structurally meaningful changes;
5. applies direct low-risk actions only when unambiguous and allowed by the user's autonomy settings;
6. records provenance, rationale, and affected objects;
7. provides undo or recovery where supported.

Natural language never bypasses backend validation.

## Search result quality

Results should prioritise:

- direct title and content matches;
- active and recent items when the query implies current relevance;
- semantically related records;
- linked objects and decisions;
- user-selected calendars, people, projects, or time periods;
- authoritative sources over unconfirmed inference.

The user can narrow by date, calendar, type, person, source, status, program, project, or sensitivity scope.

The system must not fabricate a missing record. When it cannot find the requested information, it should say so and show the closest relevant evidence if useful.

## Navigation and inspection

Search results may open the canonical object rather than creating a disconnected copy.

From a result, the user may inspect:

- current details;
- linked history;
- source and provenance;
- related items;
- decisions and changes;
- permissions and sharing state;
- available actions.

## Privacy and connected sources

Connected-source search uses only sources authorised by the user and only the permissions granted by the provider.

LifeOS must:

- identify the source of retrieved information;
- avoid exposing sensitive profile context in ordinary search results;
- respect separation between personal, work, shared, and external data;
- prevent private notes from leaking into shared outputs;
- obtain confirmation before sending, sharing, deleting, or broadly modifying external content;
- keep provider retention and AI-processing rules visible where relevant.

## V1 boundary

### First usable release

- keyword and structured filtering over native LifeOS objects;
- natural-language questions over LifeOS data through deterministic or mock/manual AI flows;
- creation and modification commands for common items;
- preview, validation, provenance, and undo for supported actions;
- direct navigation to canonical objects.

### Progressive V1

- semantic search;
- questions over decision history and long-term analytics;
- file and attachment content search;
- connected calendar, email, meeting, and messaging sources;
- richer multi-object commands and scenario simulation;
- proactive suggestions based on saved searches or unresolved patterns.

## Product requirement

Global search and command is a shared product capability, not a feature owned only by Today, Calendar, Work, or the assistant. Every major domain object must be discoverable and actionable through the same validated model.
