# ADR-002: Backend Platform

- Status: **Accepted with qualification**
- Date: 2026-08-02
- Qualified: 2026-08-17

## Decision

Use Python as the backend language direction with FastAPI and Pydantic for the primary application/API boundary.

SQLAlchemy and Alembic were part of the original relational implementation choice. They are now **conditional implementation candidates**, not binding architecture commitments, because the Physical Model has not yet been selected.

## Rationale

The product requires strong API validation, scheduling/reasoning logic, document imports, AI integration and potential optimization libraries. Python fits these requirements and aligns with current development expertise.

FastAPI/Pydantic remain compatible with the current modular-monolith and governed-contract direction without deciding the persistence technology.

## Current consequences

- Python + FastAPI + Pydantic remain current backend direction.
- Domain logic stays independent from FastAPI routes.
- OpenAPI/client generation may be used where useful but does not define Domain semantics.
- CPU-heavy or long-running work must be isolated from request handling where necessary.
- SQLAlchemy + Alembic are adopted only if the accepted Physical persistence design justifies them.
- This ADR does not authorize backend implementation, API routes, schema, migrations or a Physical Model.

## Qualification reason

The original ADR predated the closed Domain and Logical Models. Whole-Logical closure leaves persistence technology open to a later benchmark, with PostgreSQL hybrid as the current preferred baseline and TypeDB as a mandatory challenger.

Therefore the backend platform decision remains valid at the language/framework boundary while its ORM/migration-tool portion is conditional on later Physical selection.
