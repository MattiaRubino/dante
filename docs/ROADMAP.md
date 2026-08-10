# LifeOS Roadmap

- Last updated: 2026-08-10
- Purpose: delivery order, not a calendar commitment

## Completed foundation

### Phase 1–3 — Vision, architecture and V1 product definition

Completed at the level required to move into implementation and UX validation:

- product vision and scope;
- client/backend/database/storage/AI technical direction;
- core domain vocabulary;
- V1 behaviors and user flows;
- history/privacy/safety boundaries;
- confirmation and planned-versus-actual model;
- adaptive-intelligence principles.

## In progress

### Phase 4 — UX prototype and interaction validation

Primary focus:

- Home / Today information architecture;
- timeline density and progressive disclosure;
- grouped views and navigation;
- interaction behavior across complex daily scenarios;
- mobile/touch/accessibility implications.

This work can continue in parallel with backend/domain foundations. Final visual decisions must not block stable backend primitives that are already product-defined.

## Parallel technical track

### Backend Foundation

Deliverables:

- Python/FastAPI project bootstrap;
- configuration and dependency boundaries;
- PostgreSQL development infrastructure;
- SQLAlchemy + Alembic setup;
- pytest baseline;
- versioned API skeleton;
- modular-monolith boundaries;
- provider interfaces for AI, storage and integrations;
- observability/error-handling baseline appropriate for development.

### Domain Model v0

Deliverables:

- first-class domain concepts and value objects;
- ownership/workspace rules;
- invariants and lifecycle rules;
- structural versus dynamic relationships;
- source/provenance model;
- planned/actual/confirmation model;
- version/audit expectations;
- first persistence mapping proposal.

Exact complete table count is intentionally not a roadmap prerequisite.

### First vertical slice

Target conceptual slice:

`Workspace → Goal/Program → Activity → Schedule → Actual/Confirmation`

The slice should include API contracts, persistence, migrations and tests. It becomes the first end-to-end backend behavior that future web/mobile clients can consume.

## Next expansion

After the first slice is stable:

- Register / RegisterEntry and quantities;
- Asset / Subject;
- Skill and skill state;
- Requirement / Capability;
- semantic relationship layer with provenance;
- Review Queue / Inbox primitives;
- source/integration records and deduplication;
- seed/demo workspace matching UX prototype scenarios.

## Frontend/backend convergence

Phase 4 mock/simulated data is replaced gradually by versioned LifeOS APIs when a backend slice is stable. The frontend does not need to wait for the entire backend, and the backend does not need to copy unfinished visual implementation details.

## Later V1 work

- richer scheduling/replanning engine;
- real AI provider integration behind the gateway;
- Integration Hub adapters;
- notifications and device integrations;
- HealthKit / Health Connect where applicable;
- weather/maps providers where product flows require them;
- production authentication/security hardening;
- data export/deletion and privacy controls;
- staging/UAT and production deployment pipelines;
- release/versioning process.

## Explicitly deferred until justified

- permanent `dev`, `uat` or `prod` Git branches;
- microservices by default;
- Kubernetes by default;
- MongoDB as the primary domain store;
- a dedicated graph database as the primary store;
- Redis/ClickHouse/Timescale/search clusters before measured need;
- full specialist schemas for every imaginable life domain;
- V2 collaboration/social features.

## Roadmap maintenance

This file describes sequence and boundaries. [`PROJECT-STATUS.md`](PROJECT-STATUS.md) records what is actually happening now. Workstream files contain the exact operational handoff.
