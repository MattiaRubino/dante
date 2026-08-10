# ADR-003: Primary Database

- Status: Accepted
- Date: 2026-08-02
- Updated: 2026-08-10

## Decision

Use PostgreSQL as the primary source of truth.

The primary domain follows the hybrid model defined by ADR-006:

- typed relational structures for stable domain concepts and invariants;
- metadata/JSONB for genuinely flexible properties;
- a graph-like relationship layer for personal/emergent semantic links;
- version/audit/event history for traceability.

## Rationale

The domain contains strongly related users, workspaces, goals, programs, activities, schedules, confirmations, assets, skills, registers, progress and audit data. Transactions, constraints, indexing and relational consistency are central requirements.

At the same time LifeOS must support user-specific concepts and relationships that cannot all be known in advance. PostgreSQL provides the required relational foundation while allowing controlled JSONB extensibility and graph-like relationship tables without introducing multiple primary databases prematurely.

## Consequences

- MongoDB is not used as the primary domain database.
- A dedicated graph database is not used as the initial primary domain database.
- Tables are shared across users/workspaces rather than created per user.
- JSONB complements rather than replaces the relational model.
- Specialized analytics, time-series, graph, cache or search stores are introduced only for measured needs.
- PostgreSQL remains authoritative even if later systems receive derived projections/caches.
- Schema changes remain controlled by application migrations; AI cannot create per-user schema.

See [`ADR-006-hybrid-personal-data-model.md`](ADR-006-hybrid-personal-data-model.md) and [`../architecture/personal-data-ai-integration.md`](../architecture/personal-data-ai-integration.md).
