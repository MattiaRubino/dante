# Technical Decisions

## Clients

### Web

- Next.js
- React
- TypeScript

### Mobile

- Expo
- React Native
- TypeScript
- Android and iOS from the same mobile codebase where practical

Web and mobile are separate clients of the same product. They share contracts, types, validation, design tokens, and selected business rules while retaining platform-appropriate interfaces.

## Backend

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- Alembic

The backend exposes versioned APIs used by every client. Clients never connect directly to the primary database.

## Data

- PostgreSQL is the primary source of truth.
- The production data model is hybrid: typed relational core + flexible metadata/JSONB + graph-like personal relationship layer + audit/version history.
- Tables are shared across users/workspaces; LifeOS does not create per-user tables/databases.
- Stable domain invariants and high-frequency structural relationships remain relational and constrained.
- Flexible or unpredictable properties use metadata/JSONB rather than one migration per possible life-domain property.
- Personal, emergent or uncertain semantic links use the relationship layer and retain provenance/status where relevant.
- AI never invents or changes the physical database schema. Schema evolution is controlled through reviewed Alembic migrations.
- New domains should begin with the generic model when appropriate and be progressively formalized when repeated usage/query needs justify it.
- MongoDB and a dedicated graph database are not planned as primary domain stores.
- Specialized time-series, analytics, graph or cache systems are introduced only after measured workload needs.
- PostgreSQL search is used before introducing a dedicated search engine.

Detailed accepted direction: [`personal-data-ai-integration.md`](personal-data-ai-integration.md) and [`ADR-006`](../decisions/ADR-006-hybrid-personal-data-model.md).

## Data semantics and history

LifeOS explicitly separates:

- planned/canonical state;
- actual events and sessions;
- derived metrics/aggregates;
- high-frequency raw external data.

The past is not silently rewritten. Important changes are auditable, and structural plans may create new effective versions. Derived values remain reproducible where practical. Raw sensor streams are not copied indefinitely by default when summaries/provider references are sufficient.

## Files

The first implementation uses local file storage behind a provider interface. Future providers may include S3-compatible storage, Cloudflare R2, Azure Blob Storage, or similar services without changing domain logic. PostgreSQL stores file metadata/logical identifiers rather than normal large-file payloads.

## Integrations

External apps and device services are normalized behind an Integration Hub/provider interfaces. Provider-specific concepts should not leak through the core domain.

Expected provider families include weather, maps/places/routes, health, calendar, AI and future external data sources. Imported data retains provenance/external identifiers and supports deduplication/reconciliation.

HealthKit and Health Connect are preferred aggregation surfaces for supported mobile health/wearable data rather than integrating every device vendor independently at the start. Device-native sensors may be used directly when they add value, but high-frequency raw data is retained only for a justified product need.

## AI

AI access is isolated behind a replaceable AI gateway.

Initial providers/workflows may include:

1. mock provider;
2. manual/structured assistant import-export;
3. paid API providers when needed;
4. external assistants connected through a provider-neutral Tool API / MCP-compatible layer when supported.

AI produces structured semantic candidates or proposals. The backend validates permissions, versions, entity/relation types, constraints, duplicates, consequences and confirmation policy before applying changes.

LifeOS owns persistent memory/state. AI conversation memory is not authoritative.

A Context Builder provides the minimum relevant state and tool access for each request instead of sending the user's entire history to the model. Deterministic services handle routine calculations, aggregation and straightforward scheduling logic; AI is reserved for interpretation, conversation, ambiguous cross-domain planning and complex replanning.

External assistants and the internal AI must use the same LifeOS domain/tool contracts. When a client cannot write directly, it may still create an importable proposal that LifeOS validates and applies after confirmation.

See [`ADR-005`](../decisions/ADR-005-ai-gateway.md) and [`personal-data-ai-integration.md`](personal-data-ai-integration.md).

## Local development

- Web, mobile, and backend may run natively for fast development.
- PostgreSQL runs through Docker initially.
- Docker Compose is prepared for repeatable infrastructure startup.
- Production images will be added when application code begins.

## Deployment direction

The architecture must remain portable across local machines, single-server deployments, managed container platforms, and future orchestration systems. Kubernetes is not required initially.

The initial backend remains a modular monolith with clear domain boundaries. Expensive components are extracted only when measurements justify independent scaling.
