# Final Stack Capability Matrix v1

- Status: **PM-10 SUPPORTING RECORD — COMPLETE**

| LifeOS pressure | Physical mechanism | Canonical? | Key guardrail |
|---|---|---|---|
| Native owners / typed relations | PostgreSQL 18.4 | YES | explicit owner-specific mapping; no universal Entity root |
| Material state/history | PostgreSQL history/current bindings | YES | MVCC/version token != MaterialStateRef |
| Referential/invariant integrity | PostgreSQL constraints + transactions | YES | semantic invariant > storage convenience |
| Effective/world time | PostgreSQL temporal/range primitives + explicit model | YES where semantic state | effective time != knowledge chronology |
| Place/proximity/location queries | PostGIS 3.6.4 | underlying semantic data YES | geometry/geography != Place identity |
| Lexical search | native FTS + pg_trgm + unaccent | derived/query | search result != canonical truth |
| Semantic/vector retrieval | pgvector 0.8.6 | derived | visibility/scoping before consequential use |
| Relationship traversal | relational mappings + recursive SQL | query | no generic graph ontology |
| Device-local state | encrypted SQLite | NO | local != canonical; data minimized |
| Offline synchronization | PowerSync 1.25.0 | NO | mutations re-enter governed backend; no consequential LWW |
| Client-safe projection | explicit sync projection | NO | purpose/visibility bounded; rebuildable |
| Bounded publication/background work | transactional outbox + worker | NO | transport delivery != semantic effect |
| Long durable process | Restate | NO | runtime state != Domain history; delayed governance revalidation |
| Binary objects | Cloudflare R2 private EU | bytes only | ContentArtifact authority remains PostgreSQL |
| DB backup/PITR | pgBackRest 2.59.0 + S3 | recovery copy | restored bytes require semantic verification |
| Object backup | R2 -> separate S3 bucket | recovery copy | object restore coordinated with canonical metadata/deletion state |
| Constraint planning | OR-Tools 9.15 CP-SAT | NO | feasible/optimal candidate != accepted Decision |
| Connection management | PgBouncer 1.25.2 | NO | replication/admin/session-sensitive paths bypass inappropriate pooling |
| Query telemetry | pg_stat_statements | NO | privacy-minimized operational data |
| Distributed telemetry | OpenTelemetry + Alloy + Grafana Cloud EU | NO | telemetry != audit/canonical history |

## Non-functional coverage

### Multi-device/offline

Covered by encrypted SQLite + PowerSync + governed server reconciliation. Offline permission remains operation-specific.

### Provider/external partial effects

Covered by explicit PostgreSQL integration state plus outbox/Restate according to operation class. No exactly-once external-effect claim is permitted.

### Privacy/deletion

Canonical deletion/redaction starts in PostgreSQL and propagates to R2, search/vector projections, PowerSync buckets and device-local copies. Delayed propagation must remain explicit and testable.

### Recovery

PostgreSQL and object bytes have separate protected backup paths. Derived sync/search/vector state is not a recovery authority and may be purged/rebuilt after restore.

### Capacity/backpressure

PostgreSQL connection/lock pressure, worker backlog, Restate backlog, PowerSync lag, object-copy lag and solver timeouts must produce explicit degraded/pending behavior rather than silent loss.

## Matrix verdict

```text
CAPABILITY OWNER COVERAGE
COMPLETE

CANONICAL AUTHORITIES
1 — PostgreSQL

UNRESOLVED TECHNOLOGY CLASS REQUIRED FOR ACCEPTED CAPABILITY
0
```
