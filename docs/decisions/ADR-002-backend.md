# ADR-002: Backend Platform

- Status: Accepted
- Date: 2026-08-02

## Decision

Use Python with FastAPI, Pydantic, SQLAlchemy, and Alembic.

## Rationale

The product requires strong API validation, scheduling logic, document imports, AI integration, and potential optimization libraries. Python fits these requirements and aligns with current development expertise.

## Consequences

- OpenAPI contracts can generate TypeScript clients.
- CPU-heavy work must be isolated from request handling when necessary.
- Domain logic should remain independent from FastAPI routes.
