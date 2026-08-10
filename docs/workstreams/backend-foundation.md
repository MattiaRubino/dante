# Workstream — Backend Foundation

- Status: **READY TO START**
- Intended branch: `feature/backend-foundation`
- Base: current canonical `main`
- Work type: production technical foundation

## Purpose

Create the backend skeleton that can support LifeOS without prematurely freezing every specialist-domain table or API.

## Required reading before implementation

1. [`../PROJECT-STATUS.md`](../PROJECT-STATUS.md)
2. [`../development/operating-rules.md`](../development/operating-rules.md)
3. [`../architecture/system-overview.md`](../architecture/system-overview.md)
4. [`../architecture/technical-decisions.md`](../architecture/technical-decisions.md)
5. [`../architecture/personal-data-ai-integration.md`](../architecture/personal-data-ai-integration.md)
6. [`../product/v1-core-domain-glossary.md`](../product/v1-core-domain-glossary.md)
7. [`../product/v1-execution-status.md`](../product/v1-execution-status.md)
8. [`../product/v1-data-history-and-privacy.md`](../product/v1-data-history-and-privacy.md)
9. accepted ADRs under [`../decisions/`](../decisions/)

## Where to work

Create `feature/backend-foundation` from the latest `main` immediately before implementation begins.

During the initial foundation phase, Domain Model v0 should preferably be developed as a bounded sub-scope on this same branch if it would otherwise modify the same backend/domain files. Split it into a separate `feature/domain-model` branch only after there is a clean file/ownership boundary or after Backend Foundation has merged.

Normal incremental status goes in this handoff. Do not update `PROJECT-STATUS.md` for every backend commit; update global status when the workstream actually starts, blocks, reaches an integrated milestone or finishes.

## Initial deliverables

- Python project/package structure;
- FastAPI application bootstrap;
- Pydantic settings/configuration;
- SQLAlchemy setup;
- Alembic initialization;
- PostgreSQL local development configuration through Docker/Docker Compose;
- pytest baseline;
- versioned API routing skeleton;
- modular-monolith package boundaries;
- error-handling/logging baseline;
- provider interfaces/stubs for Storage, AI Gateway and Integration Hub where useful;
- development health/readiness endpoint where appropriate.

## Boundary

Do **not** begin by creating the complete final database for nutrition, training, learning, finance, travel and every other imaginable module.

Backend Foundation should provide infrastructure and enough domain support for the first vertical slice while preserving the accepted hybrid-data architecture.

Do not make backend schema decisions from temporary Phase 4 visual details. Phase 4 is allowed to continue independently with simulated data until stable contracts exist.

## First vertical slice target

After bootstrap, support a narrow end-to-end flow around:

`Workspace → Goal/Program → Activity → Schedule → Actual/Confirmation`

The exact persistence mapping follows Domain Model v0, not the temporary needs of one frontend screen.

## Tests / validation expected

At minimum:

- application starts in development;
- database connection/config can be tested without hard-coded secrets;
- migrations can be created/applied/rolled back in development;
- unit tests run independently of production services;
- critical domain logic is testable without requiring FastAPI request handling;
- API and persistence layers do not become the domain model itself.

## Do not change without an ADR or explicit review

- PostgreSQL as primary source of truth;
- FastAPI/Pydantic/SQLAlchemy/Alembic stack direction;
- modular monolith first;
- clients never connect directly to the database;
- AI never bypasses domain validation;
- no per-user database/table creation;
- DEV/UAT/PROD are environments rather than permanent Git branches.

## Next exact step

1. Re-read current `main` and this handoff immediately before starting.
2. Create `feature/backend-foundation` from current `main`.
3. Update this handoff to **IN PROGRESS** with the actual branch/PR and starting commit.
4. Bootstrap the backend with no specialist-domain schema beyond what the first coherent slice requires.
5. Develop Domain Model v0 inside the same branch initially unless a clean independent boundary has already emerged.

## Handoff maintenance

Once implementation starts, add:

- last validated commit;
- actual package/file paths;
- commands to run/test/migrate;
- completed tasks;
- current task;
- known issues;
- next exact steps.
