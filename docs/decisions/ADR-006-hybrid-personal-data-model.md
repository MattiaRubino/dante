# ADR-006: Hybrid Personal Data and Semantic Relationship Model

- Status: Accepted
- Date: 2026-08-10

## Context

LifeOS must represent a personal domain that is broad, user-specific and impossible to enumerate exhaustively in advance. It also requires strong consistency for scheduling, programs, progress, permissions and history. A purely rigid relational schema would require constant migrations for unpredictable user concepts; a purely schemaless/document or graph model would weaken constraints, queryability and transactional domain rules.

## Decision

Use PostgreSQL as the primary system of record with a hybrid model:

1. a typed relational core for stable LifeOS concepts and structural relationships;
2. metadata and JSONB for genuinely flexible or provider-specific properties;
3. a graph-like relationship layer for personal, emergent or uncertain semantic links;
4. provenance/status for AI-inferred or observed facts and relationships;
5. version/audit/event history that preserves planned state, actual outcomes and later changes.

The schema is shared across users/workspaces. LifeOS never creates a table or database per user or per newly discovered life domain.

Stable, frequently used relationships remain normal foreign keys/dedicated relational structures. The dynamic relationship layer is not a replacement for ordinary relational modeling.

AI may create structured semantic candidates inside the supported model, but may not invent physical tables, columns, SQL or migrations. The backend validates entity/relation types, ownership, duplicates, constraints and confirmation requirements before persistence.

New domains should use the generic model first where appropriate. Repeated, important and query-heavy concepts may later be promoted to first-class structures through reviewed migrations. Specialized databases are introduced only when measured workloads justify them.

## Rationale

This gives LifeOS the required combination of:

- relational consistency and transactions;
- user-specific extensibility;
- AI-assisted semantic discovery;
- cross-domain relationships;
- evolvability without per-user schema fragmentation;
- a realistic V1 implementation path using one primary database;
- a clean path to later partitioning, analytics stores, graph projections or other specialized infrastructure if real scale requires them.

## Consequences

- Detailed schema design must follow the architecture in `docs/architecture/personal-data-ai-integration.md`.
- Exact table count, relation vocabulary and JSONB boundaries are intentionally deferred to detailed domain modeling.
- Generic representation is not an excuse to store the entire product as arbitrary JSON.
- Domain concepts that become important enough must be formalized rather than remaining permanently generic.
- AI inference must retain provenance and must not silently become an operational rule when confirmation is appropriate.
- PostgreSQL remains authoritative unless a later ADR explicitly supersedes this decision.
