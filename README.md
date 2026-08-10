# LifeOS

LifeOS is an adaptive personal operating system for planning goals, activities, routines, and day-to-day changes across web, Android, and iOS.

## Project status

Phase 3 product definition is closed. Phase 4 is in progress with a coded UX prototype focused on the Home/Today surface, timeline density, progressive disclosure, overlapping items, and grouped expansion.

No production application code has been committed yet. The current milestone is an interactive validation prototype with simulated data.

## Current Phase 4 milestone

- Phase 4 frontend source of truth: [`docs/phase-4/frontend-master.md`](docs/phase-4/frontend-master.md)
- Home/Today v7 decisions: [`docs/ux/today-home-v7.md`](docs/ux/today-home-v7.md)
- Prototype archive and restore instructions: [`prototypes/today/archive/README.md`](prototypes/today/archive/README.md)
- Prototype index: [`prototypes/README.md`](prototypes/README.md)

The frontend master log must be read before each Phase 4 iteration and updated after every meaningful change. It records the current implementation, rationale, regressions, open issues, handoff rules, versioning, and Git workflow.

## Product direction

LifeOS will provide:

- a central adaptive calendar;
- goals, projects, activities, routines, and progress tracking;
- optional modules such as nutrition, training, health, learning, travel, and creative work;
- web, Android, and iOS clients with equivalent functionality and platform-adapted UX;
- AI-assisted interpretation, planning and recalibration behind replaceable provider/tool interfaces;
- integrations with external apps, device data and services through a normalized Integration Hub;
- local development with a future path to portable cloud deployment.

## Initial technical direction

- Web: Next.js + TypeScript
- Mobile: Expo + React Native + TypeScript
- Backend: Python + FastAPI
- Primary database: PostgreSQL
- Data model: typed relational core + metadata/JSONB + graph-like personal relations + audit/version history
- File storage: local provider initially, replaceable by S3-compatible/cloud providers
- AI: replaceable gateway, Context Builder, structured proposals and provider-neutral Tool API / MCP-compatible direction
- Integrations: provider adapters normalized into LifeOS domain data with provenance and deduplication
- Repository: private monorepo
- Local infrastructure: Docker Compose for infrastructure dependencies

## Architecture sources of truth

Before detailed production data-model or AI/integration implementation, read:

- [`docs/architecture/system-overview.md`](docs/architecture/system-overview.md)
- [`docs/architecture/technical-decisions.md`](docs/architecture/technical-decisions.md)
- [`docs/architecture/personal-data-ai-integration.md`](docs/architecture/personal-data-ai-integration.md) — accepted detailed direction for personal data, semantic relations, AI ingestion, integrations, history and scaling
- [`docs/decisions/ADR-003-primary-database.md`](docs/decisions/ADR-003-primary-database.md)
- [`docs/decisions/ADR-005-ai-gateway.md`](docs/decisions/ADR-005-ai-gateway.md)
- [`docs/decisions/ADR-006-hybrid-personal-data-model.md`](docs/decisions/ADR-006-hybrid-personal-data-model.md)

The architecture is fixed at the level of principles and boundaries. Exact production tables, relation vocabulary, JSONB boundaries, retention rules and specialist-domain schemas are intentionally deferred until detailed domain modeling.

See [`docs/`](docs/) for the current product and architecture decisions.
