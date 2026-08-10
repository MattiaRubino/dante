# LifeOS

LifeOS is an adaptive personal operating system for connecting goals and intentions to programs, routines, projects, real calendar time, actual observed/confirmed behavior, progress and adaptive future planning across web, Android and iOS.

## Project status

V1 product definition and the main architecture foundation are sufficiently mature to support parallel work.

Current tracks:

- **Phase 4 Home/Today UX prototype:** in progress on `prototype/phase-4-today-home` (PR #2).
- **Backend Foundation:** ready to start from current `main`.
- **Core Domain Model v0:** ready to start in parallel with the backend foundation.

No production application code has been committed yet.

For the exact current state, always read [`docs/PROJECT-STATUS.md`](docs/PROJECT-STATUS.md).

## How to resume work

Any human or AI agent continuing the project should read:

1. this README;
2. [`docs/PROJECT-STATUS.md`](docs/PROJECT-STATUS.md);
3. [`docs/development/operating-rules.md`](docs/development/operating-rules.md);
4. the relevant [`docs/workstreams/`](docs/workstreams/) handoff;
5. the product/architecture documents and ADRs linked by that handoff;
6. relevant current code/tests before changing implementation.

Repository documentation on current `main` is the canonical project memory when chat history or old branches are incomplete, stale or contradictory. An active workstream branch may contain newer unmerged work only inside that workstream's scope.

## Product direction

LifeOS will provide:

- a central adaptive calendar and Today experience;
- goals, programs, projects, activities, events, routines, reminders and progress tracking;
- planned-versus-actual execution and user-controlled confirmation;
- registers/measurements, assets/subjects, skills, requirements/capabilities and extensible cross-domain relationships;
- optional specialist capabilities such as nutrition, training, health, learning, travel and creative work without turning each life topic into an isolated product silo;
- web, Android and iOS clients with equivalent functionality and platform-adapted UX;
- AI-assisted interpretation, planning and recalibration behind replaceable provider/tool interfaces;
- integrations with external apps, device data and services through a normalized Integration Hub;
- explainable, traceable and reversible significant changes.

V1 is personal-first. Collaboration/social capabilities are deferred.

## Technical direction

- Web: Next.js + React + TypeScript
- Mobile: Expo + React Native + TypeScript
- Backend: Python + FastAPI + Pydantic + SQLAlchemy + Alembic
- Primary database: PostgreSQL
- Data model: typed relational core + metadata/JSONB + graph-like personal relations + audit/version history
- File storage: local provider initially, replaceable by S3-compatible/cloud providers
- AI: replaceable gateway + Context Builder + structured proposals + provider-neutral tool/MCP-compatible direction
- Integrations: provider adapters normalized into LifeOS domain data with provenance and deduplication
- Architecture: modular monolith first; extract specialized infrastructure only when measured needs justify it
- Repository: private monorepo

## Git and environments

- `main` is the single integrated source of truth.
- Work happens on bounded `feature/*`, `fix/*`, `docs/*` or `prototype/*` branches and returns through PRs.
- New production work starts from current `main` unless its workstream handoff explicitly names an active prototype branch.
- Before merge, compare against current `main` and check semantic/documentation coherence, not only Git conflicts.
- DEV, UAT and PROD are deployment environments, not permanent Git branches.

See [`docs/development/operating-rules.md`](docs/development/operating-rules.md) and [`docs/development/branching-and-environments.md`](docs/development/branching-and-environments.md).

## Architecture sources of truth

Before detailed production data-model, AI or integration implementation, read:

- [`docs/architecture/system-overview.md`](docs/architecture/system-overview.md)
- [`docs/architecture/technical-decisions.md`](docs/architecture/technical-decisions.md)
- [`docs/architecture/personal-data-ai-integration.md`](docs/architecture/personal-data-ai-integration.md)
- [`docs/decisions/ADR-003-primary-database.md`](docs/decisions/ADR-003-primary-database.md)
- [`docs/decisions/ADR-005-ai-gateway.md`](docs/decisions/ADR-005-ai-gateway.md)
- [`docs/decisions/ADR-006-hybrid-personal-data-model.md`](docs/decisions/ADR-006-hybrid-personal-data-model.md)

The architecture is fixed at the level of principles and boundaries. Exact production tables, relation vocabulary, JSONB boundaries, retention rules and specialist-domain schemas remain implementation decisions to be made through detailed domain modeling.

## Documentation

Start from [`docs/README.md`](docs/README.md). Significant work is not considered complete until its relevant documentation/handoff is updated.
