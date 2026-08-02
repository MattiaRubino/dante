# ADR-003: Primary Database

- Status: Accepted
- Date: 2026-08-02

## Decision

Use PostgreSQL as the primary source of truth.

## Rationale

The domain contains strongly related users, workspaces, goals, activities, schedules, confirmations, progress, and audit data. Transactions, constraints, indexing, and relational consistency are central requirements.

## Consequences

- MongoDB is not used as the primary domain database.
- JSONB remains available for flexible properties.
- Additional databases are introduced only for measured needs.
