# System Overview

## Logical architecture

```text
Web client (Next.js) ----------------------\
                                            \
Mobile client (Expo/RN) ---------------------> Versioned HTTPS API (FastAPI)
                                                |-- authentication / authorization
                                                |-- calendar / scheduling / recalibration
                                                |-- goals / programs / progress
                                                |-- domain services and validation
                                                |-- semantic model / relationship services
                                                |-- Integration Hub
                                                |-- AI Gateway + Context Builder
                                                |-- Tool API / MCP-compatible surface
                                                |-- synchronization / audit / versioning
                                                          |
                                                          v
                                                   PostgreSQL
                                                source of truth
                                                          |
                                                   StorageProvider
```

External providers and assistants never become alternate sources of truth. They interact through LifeOS APIs, adapters and validated proposals.

## Client responsibilities

Clients handle:

- presentation and navigation;
- local interaction state;
- offline-capable caches and queued changes where appropriate;
- secure session storage;
- platform integrations such as notifications, location, HealthKit, or Health Connect;
- collection of user confirmation when a proposed change requires it.

Clients do not hold database credentials and do not enforce critical authorization or business rules.

## Backend responsibilities

The backend handles:

- authentication and authorization;
- data validation and schema/domain constraints;
- domain rules;
- scheduling and recalibration;
- semantic entity/relation validation;
- synchronization and conflict detection;
- provenance, deduplication and reconciliation of external records;
- audit and version checks;
- Integration Hub orchestration;
- AI context construction, routing and proposal validation;
- tool contracts used by internal AI and external assistants.

## Data responsibility

PostgreSQL is the official server-side state. Device-local storage is a cache and offline operation queue, not an independent source of truth.

The persistent model combines:

- typed relational core for stable domain concepts;
- metadata/JSONB for genuinely flexible properties;
- graph-like dynamic relations for personal/emergent links;
- version/audit/event history;
- planned versus actual state;
- registers/measurements and reproducible derived summaries.

Important AI-inferred relationships retain provenance and lifecycle/status. AI may propose semantic candidates but cannot create arbitrary physical schema or bypass backend validation.

Detailed model: [`personal-data-ai-integration.md`](personal-data-ai-integration.md).

## Integration responsibility

External apps and services are normalized through provider adapters. LifeOS stores canonical domain meaning rather than making the rest of the application depend on Google-, Apple-, OpenAI- or vendor-specific payloads.

External records retain identifiers/provenance sufficient for synchronization, deduplication and reconciliation. High-frequency raw sensor data is not duplicated indefinitely by default when useful summaries or source references are sufficient.

## AI responsibility

The AI Gateway is replaceable and may route work among mock, internal API and future providers. AI is not required for deterministic calculations or simple state transitions.

The Context Builder selects the relevant state for a request and can expose read/proposal tools so models fetch more context only when needed. Replanning is expressed as structured proposals and validated future changes rather than direct database mutation.

The same domain/tool surface can be used by LifeOS-integrated AI and external assistants. Direct write support depends on the client/provider; a structured proposal import flow remains the universal fallback.

## Scalability direction

The initial backend is a modular monolith. Modules have clear boundaries so expensive or independently scaled components can be extracted later only when measurements justify it.

The initial persistence stack intentionally stays small: PostgreSQL plus the StorageProvider. Indexing, partitioning, materialized aggregates, caches, analytics/time-series systems, graph projections, sharding or other specialized infrastructure are added only when real workload evidence requires them.
