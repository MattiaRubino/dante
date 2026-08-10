# Personal Data, Semantic Model, AI and Integration Architecture

- Status: Accepted architectural direction
- Date: 2026-08-10
- Scope: persistent personal data, extensibility, cross-domain relationships, AI interpretation, external integrations, history and scaling

## Purpose

LifeOS has an unusually broad and open-ended domain. A person may track goals, language learning, training, nutrition, projects, equipment, vehicles, documents, travel, health measurements, creative work, household tasks, agriculture, or future domains that do not exist in the product today. The application therefore cannot be designed as one rigid schema per life domain, but it also cannot become an unstructured JSON store where every user invents an incompatible model.

This document defines the architectural model that must be used when the production data model is implemented.

The key principle is:

> LifeOS owns a small, stable grammar of universal concepts. User-specific content, relationships and extensions are expressed as data inside that grammar. AI may interpret and propose semantic changes, but the backend remains the authority that validates and persists them.

## 1. Source of truth and ownership

PostgreSQL remains the canonical server-side source of truth.

LifeOS, not an AI provider and not an external integration, owns the persistent personal model. AI conversation memory may help interaction, but it is never authoritative for goals, preferences, programs, history, progress or relationships.

In V1 each person's data belongs to a personal workspace. Tables are shared across users/workspaces; the application does not create separate tables or databases per user. Ownership is represented by identifiers such as `workspace_id`, with authorization enforced by the backend and potentially reinforced later with PostgreSQL Row Level Security where useful.

## 2. Hybrid data model

LifeOS uses four complementary persistence layers inside the primary domain model.

### 2.1 Typed relational core

Concepts that are stable, central and frequently queried receive first-class relational structures and constraints. Expected examples include:

- users and workspaces;
- goals;
- programs;
- projects;
- activities and events;
- schedule entries;
- actual sessions and confirmations;
- assets;
- skills;
- registers and register entries;
- files/documents metadata;
- integrations and synchronization state;
- versions and audit events.

Relationships that are structural invariants and are used constantly should normally be represented with foreign keys or dedicated tables. Examples include an activity belonging to a program, a program contributing to a goal, or a schedule entry referring to an activity.

### 2.2 Flexible metadata and JSONB

The system must support properties that cannot reasonably be known in advance without creating a migration for every new asset type, activity subtype or custom user property.

Examples:

- a camera lens may have focal length, mount and filter diameter;
- a tractor may have power, hitch type and fuel type;
- a custom user-defined metric may have a unit and aggregation strategy;
- an integration may retain provider-specific metadata.

These properties may use metadata definitions, typed property values and/or PostgreSQL JSONB. JSONB is an extension mechanism, not a replacement for the relational model. Frequently queried or invariant fields should be promoted to typed columns/tables when justified.

### 2.3 Dynamic relationship layer

LifeOS needs relationships that are personal, emergent or uncertain and therefore cannot all be encoded as static foreign keys in advance.

Examples include:

- a particular sleep pattern may affect adherence to a particular learning program for one person;
- a specific asset may provide a capability required by an activity;
- weather may affect the feasibility of an outdoor activity;
- a skill may contribute to a user-specific goal;
- two areas of life may become related because of an observed pattern.

A graph-like relationship layer will represent these links without requiring a graph database as the primary store. The physical implementation may use an `entity_relations`-style table plus typed relation definitions and metadata.

The dynamic relationship layer is for relationships that are not already better represented by normal relational structures.

### 2.4 Version, audit and event history

LifeOS must preserve the distinction between what was planned, what actually happened and what was changed later.

Important domain changes should be traceable. Programs and other structural plans should support versioning where a change modifies future behavior. Audit/event records should explain creation, rescheduling, completion, import, recalibration and AI-assisted changes.

The past is not silently rewritten. Future state may be recalibrated by creating a new effective version or explicit change.

## 3. Universal concepts, not a table for every life domain

The production schema must not create tables such as `english_table`, `photography_table`, `farming_table` and `guitar_table` simply because those topics exist.

LifeOS should instead model a compact vocabulary such as:

- Goal: an intended outcome;
- Program: an organized strategy or ongoing structure;
- Project: a bounded body of work;
- Activity/Event: something planned or performed;
- Actual/Session: what really happened;
- Asset/Subject: an object or subject managed by the user;
- Skill: a capability that can develop over time;
- Register/Metric: a value observed over time;
- Requirement: something necessary or desirable for an action;
- Capability: something an asset, person or resource can provide;
- Dependency: ordering or blocking relationship;
- Relation: a non-core semantic link between entities.

A language-learning program may contain speaking, listening, writing, review, television/media exposure and tests. A training program may contain strength, hypertrophy, cardio, mobility or recovery sessions. These are different configurations and activity types built from shared primitives, with specialist structures added only where the data and queries justify them.

## 4. Progressive formalization

New domains begin with the generic model when possible.

Example: plants may initially be represented as assets plus properties, registers, activities and relationships. If usage later proves that plant cycles, treatments and specialized queries are important enough, native structures can be introduced and existing data migrated/promoted.

Therefore:

- generic representation is the default for genuinely unpredictable cases;
- repeated, important and query-heavy concepts can become first-class domain structures;
- a concept is promoted because real usage justifies it, not because it can be imagined in advance.

This keeps V1 developable while preserving a path to specialist capabilities.

## 5. Assets, capabilities and requirements

Assets are not merely inventory notes. They may participate in planning.

An asset can expose capabilities. An activity can declare requirements. The planner can match available capabilities to requirements instead of hard-coding one specific object name.

Conceptual example:

```text
Activity: outdoor long-exposure photography
requires capability: stable camera support

Tripod asset
provides capability: stable camera support
```

The same model can represent machinery, tools, vehicles, kitchen equipment, musical equipment or future resource categories.

Requirements may be mandatory or optional, may have alternatives, and may be currently satisfied or unsatisfied. An unsatisfied requirement can become a prerequisite activity such as obtaining, renting, borrowing or preparing a resource.

## 6. Personal relationships and per-user meaning

The schema is shared, but the semantic graph is personal.

LifeOS does not assume that the same event has the same operational meaning for every person. The user's goal, program policy, history, preferences, constraints and current state determine whether something is relevant.

For example, a nutrition program can be strict, advisory, monitoring-only, review-oriented or a mixture of these behaviors. A deviation may require immediate replanning for one program, only be recorded for another, and be irrelevant to a third.

Similarly, sleep can affect training, study or nothing at all depending on the person's configuration and observed/confirmed relationships.

The system should store the operational policy of a program separately from its subject area. Domain type alone must not determine intervention behavior.

## 7. Relation lifecycle and provenance

A semantic relationship must not automatically become a trusted rule merely because an AI inferred it.

Relationships and important inferred facts should carry provenance and lifecycle information such as:

- source: user statement, external provider, domain rule, AI inference, statistical observation, import;
- confidence when relevant;
- status: candidate, observed, user-confirmed, system-confirmed, active, dismissed, superseded;
- created/effective timestamps;
- optional explanation/evidence references.

Examples:

```text
Sleep MAY_AFFECT learning adherence
source = observed_pattern
status = candidate
confidence = 0.68
```

versus:

```text
Avoid demanding learning sessions after poor sleep
source = user_confirmed
status = active
```

Operational rules that materially change scheduling or program behavior should normally require explicit confirmation unless the user has enabled a suitable automation policy.

## 8. AI semantic ingestion

AI does not choose SQL tables and does not modify database schema.

Natural-language input passes through a semantic interpretation boundary:

```text
user/external input
        ↓
AI semantic interpretation
        ↓
structured semantic candidates
        ↓
LifeOS domain/schema validator
        ↓
deduplication + authorization + confirmation policy
        ↓
persistent domain records
```

If a user says that they own a new tool and want to learn a related skill, AI may propose an Asset, Skill, Goal and relationships among them. The backend determines whether those entity/relation types are permitted, whether matching records already exist, whether data is duplicated, and whether confirmation is required.

AI is allowed to create or propose instances and relationships inside the supported meta-model. AI is not allowed to invent arbitrary physical tables, columns or database migrations.

If an interpretation cannot be expressed precisely with the current semantic vocabulary, it may temporarily use a generic relation/property with explanatory metadata. Repeated gaps are product evidence for extending the model through normal development and migrations.

## 9. Cross-domain reasoning and replanning

LifeOS is not a set of isolated mini-apps. Specialist domain knowledge may exist, but planning decisions can span multiple areas.

A change in one area may be relevant to several programs. The central planner/reasoning layer must be able to query the relevant state rather than having every module replan independently.

Replanning should be incremental:

```text
current plan version
+ actual event / new constraint / user decision
→ validated proposal
→ minimal future patch or new effective version
```

The system should avoid destructive full-plan regeneration when a smaller change is sufficient.

Program policy determines whether a deviation triggers no action, deterministic handling, a scheduled review, or AI-assisted reasoning.

## 10. Context builder and AI cost control

AI should not receive an entire lifetime of user data for every request.

A Context Builder selects the minimum relevant state and can expose tools that allow the AI to request additional data when necessary. A complex review may progressively fetch recent program versions, actual sessions, relevant registers, constraints, calendar availability or related domains.

Routine calculations, aggregation, conflict checks and straightforward state transitions belong in deterministic LifeOS services. AI is used for interpretation, planning, conversation and ambiguous cross-domain reasoning.

Automatic AI calls must be event-gated and may aggregate several changes before asking for a single higher-level evaluation.

## 11. Internal AI and external assistants

The AI Gateway remains provider-replaceable. LifeOS may use its own paid API providers for integrated AI features, while also exposing a provider-neutral Tool API / MCP-compatible surface for external assistants.

Conceptually:

```text
                    LifeOS Domain API
                           │
             ┌─────────────┼─────────────┐
             ↓             ↓             ↓
       Internal AI     ChatGPT-like   Other agents
        gateway         assistant      / providers
```

All clients operate through the same domain services and validation rules.

An external assistant may read state, discuss a problem and create a structured proposal. If its platform permits trusted write tools, it can submit that proposal through LifeOS APIs. If the platform only permits reading, the same proposal can be imported/opened in LifeOS and applied after validation and confirmation.

This avoids making LifeOS dependent on one AI vendor or one consumer subscription model.

## 12. Integration Hub

External apps and device sources are normalized through an Integration Hub rather than leaking provider-specific concepts throughout the domain.

Provider abstractions may include:

- weather provider;
- maps/places/routes provider;
- health provider;
- calendar provider;
- learning/content provider;
- AI provider;
- future finance, media or productivity providers.

External records retain provenance such as provider, external identifier, observed timestamp, import timestamp and source device where relevant. Synchronization must support deduplication and reconciliation so that overlapping providers are not naively summed or duplicated.

For example, multiple devices may report steps for the same period. LifeOS must preserve sources and select/reconcile authoritative values rather than adding every imported total.

## 13. Planned, actual, derived and raw data

LifeOS distinguishes four kinds of data:

1. Planned/canonical state: what the user intends and the current authoritative configuration.
2. Actual/event data: what really happened.
3. Derived data: summaries, trends, planned-vs-actual comparisons and other reproducible calculations.
4. Raw high-frequency data: sensor samples or external detail that may not need permanent duplication inside LifeOS.

Derived metrics should remain reproducible from canonical facts where practical. Cached/materialized summaries may be stored for performance but are not treated as independent truth.

High-frequency raw streams such as GPS points, heart-rate samples or accelerometer data should not be copied indefinitely by default. Prefer useful summaries/session facts, provider references and explicit retention policies. Raw detail may remain in HealthKit/Health Connect or another source unless LifeOS has a clear product reason to retain it.

## 14. Files and large objects

Large files do not belong in normal relational rows. PostgreSQL stores file metadata and logical identifiers. Actual bytes live behind the StorageProvider, initially local filesystem and later potentially S3-compatible/object storage.

## 15. Scaling strategy

The architecture is designed to scale by evolution rather than by installing every specialized database on day one.

Initial production direction:

- PostgreSQL for relational, JSONB, relationship and register data;
- object/file storage through the StorageProvider;
- application-level caching only when measured needs justify it.

Potential later optimizations, introduced only from real workload evidence, include:

- indexes and query-specific denormalization;
- PostgreSQL table partitioning for very large histories/registers;
- materialized aggregates;
- archival/retention tiers;
- Redis or equivalent cache;
- analytics/time-series stores for extreme volumes;
- graph projections or a graph store if graph traversal becomes a dominant measured workload;
- sharding only at scale where a single primary topology is no longer sufficient.

PostgreSQL remains the primary system of record unless a future ADR explicitly changes that decision.

## 16. Schema governance

Database structure is controlled by application development and Alembic migrations.

The AI may discover evidence that the semantic vocabulary is insufficient, but schema evolution is an engineering decision. New first-class concepts are introduced through reviewed code/migrations, with migration paths for data previously represented through generic properties or relations.

This prevents per-user schema fragmentation and keeps all LifeOS installations compatible.

## 17. What is fixed by this decision

The following are architectural commitments:

- PostgreSQL is the primary source of truth.
- Shared schema/workspace ownership is used instead of per-user tables/databases.
- Stable domain invariants use typed relational structures.
- Flexible/unpredictable properties use metadata/JSONB rather than endless migrations.
- Personal/emergent relationships use a graph-like relation layer inside the primary store.
- Core high-frequency relationships remain normal relational relations/FKs.
- Important inferred relationships retain provenance and lifecycle/status.
- AI interprets into structured semantic candidates and never writes arbitrary SQL/schema.
- Backend validation, authorization, versioning and confirmation policy remain authoritative.
- External sources are normalized through an Integration Hub with provenance and deduplication.
- Planned state, actual events, derived metrics and raw sensor data remain distinct concepts.
- Specialist databases are added only after measured need.

## 18. What is intentionally not fixed yet

The following must be decided during detailed domain modeling and implementation rather than guessed prematurely:

- exact table count and column layout;
- final list of universal entity types;
- final relation vocabulary;
- exact JSONB versus typed-property boundaries;
- which specialist domains deserve dedicated tables in V1;
- retention periods for each raw data class;
- exact AI routing/model policies;
- exact MCP/tool schemas;
- partitioning/caching strategy before real workload measurements exist.

These are implementation details within the architecture, not reasons to reopen the architecture itself.

## 19. Implementation rule of thumb

When introducing a new piece of data, ask in this order:

1. Is this already a first-class LifeOS concept? Use the relational core.
2. Is it a flexible property of an existing concept? Use typed metadata/JSONB.
3. Is it a personal or emergent link between existing concepts? Use the relationship layer with provenance.
4. Is it a repeated, important, query-heavy concept poorly represented by the generic model? Propose formal promotion through a reviewed schema migration.
5. Is it derived from existing facts? Prefer calculation/materialization rather than duplicating truth.
6. Is it high-frequency raw external data? Retain only when the product actually needs it.

This rule is the default handoff for future data-model work.