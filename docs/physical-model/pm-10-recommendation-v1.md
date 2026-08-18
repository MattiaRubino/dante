# PM-10 — Final Physical Stack Recommendation v1

- Status: **COMPLETE — PREFERRED RECOMMENDATION ESTABLISHED / PM-11 NEXT**
- Workstream: `feature/physical-model`
- PRE-SCOPE: `016e4df07df9756d2c03d5582b489eed607aaecc`
- Recommendation basis: PM-01 through PM-09 + final stack audit + product simulations + current primary-source technology evidence
- Direct execution: **NOT STARTED**
- Preferred primary: **PostgreSQL 18.4 / PASS-CONDITIONAL**
- Selected: **NONE**

## 1. Recommendation

LifeOS SHOULD use PostgreSQL 18.4 as canonical primary persistence.

```text
PREFERRED PRIMARY
PostgreSQL 18.4

PM-09 EVIDENCE-WEIGHTED SCORE
89.25 / 100

RUNNER-UP
TypeDB CE 3.12.3
80.00 / 100

RANKING
ROBUST
NOT SENSITIVITY-DEPENDENT
NOT PERFORMANCE-DEPENDENT
```

This recommendation does not convert evidence qualification into a direct hard-gate PASS and does not create `SELECTED` status. PM-11 remains the explicit selection gate.

## 2. Why PostgreSQL wins

PostgreSQL is preferred because it preserves the accepted LifeOS Logical Model while giving the strongest whole-system balance across:

- semantic fidelity without a generic Entity/EAV kernel;
- native integrity constraints and mature transactional semantics;
- concurrency ergonomics for consequential expected-state and multi-owner invariants;
- current-state plus explicit material-history mapping;
- reporting, recursive traversal and lexical search;
- mature backup/PITR/replication/evolution paths;
- strong Python/tooling ecosystem and low exit risk;
- ability to add bounded geospatial and vector capabilities inside the same database boundary;
- lower topology/synchronization burden than TypeDB plus additional search/vector infrastructure.

TypeDB retains the strongest pure relation/role/n-ary semantic fit. That advantage is real but does not outweigh the permanent concurrency-discipline, CE topology, self-hosted backup and broader stack costs under accepted LifeOS priorities.

## 3. Recommended companion stack

### PostgreSQL-native extensions and facilities

```text
PostGIS 3.6.4
pgvector 0.8.6
native Full Text Search
pg_trgm
unaccent
pg_stat_statements
PgBouncer 1.25.2
```

These are technical capabilities, not Domain owners.

### Async and durable execution

```text
BOUNDED ASYNC
PostgreSQL transactional outbox + bounded worker

MATERIAL LONG-RUNNING DURABLE PROCESS
Restate runtime
Restate Python SDK 1.0.3
Restate Server 1.7.2 self-hosted/reproducible deployment subject
Restate Cloud EU allowed as managed deployment when privacy/operability review accepts it
```

Restate is the recommended Class-B durable-execution technology; **Cloud EU is not a globally mandatory deployment mode**. Restate can run self-hosted as a single binary/container and can also run as a managed EU cloud environment. The deployment choice is an operational/privacy decision and must preserve the same LifeOS runtime boundary.

For the current Python path, do not assume client-side journal encryption available on Restate Cloud: current Restate documentation exposes client-side journal encryption through the TypeScript SDK only. Therefore journal payload minimization is a hard rule regardless of deployment, and self-hosting remains a first-class production option when data-control/privacy considerations dominate managed convenience.

Runtime workflow state remains technical and must not replace LifeOS canonical or material history.

### Offline / multi-device

```text
PowerSync Service 1.25.0 Open Edition
+ encrypted SQLite local state
+ PostgreSQL-backed PowerSync bucket storage
```

Offline is operation-specific. A local write is never canonical truth merely because it happened later. Consequential mutation must return through the LifeOS backend and revalidate expected material state, governance and authorization before PostgreSQL commit.

PowerSync replication must be limited to explicitly approved client-safe projections rather than broad publication of canonical tables.

### Object bytes

```text
Cloudflare R2 Standard
EU jurisdiction
PRIVATE
```

PostgreSQL owns `ContentArtifact` identity, metadata, provenance, visibility, retention semantics, hashes and object locators. R2 owns raw bytes only.

### Recovery

```text
PostgreSQL backup
pgBackRest 2.59.0
-> AWS S3 Standard eu-south-1
-> Versioning
-> Object Lock GOVERNANCE
-> finite policy-bound retention

R2 object backup
-> separate AWS S3 eu-south-1 backup bucket
```

Object Lock Compliance is not the default because immutable retention must not make accepted privacy/deletion policy structurally impossible.

### Solver

```text
OR-Tools 9.15 CP-SAT
```

Solver outputs remain candidate/derived state until accepted through applicable LifeOS decision/governance semantics.

### Observability

```text
OpenTelemetry
Grafana Alloy 1.18.0
Grafana Cloud EU
pg_stat_statements
```

Telemetry is privacy-minimized operational state, not canonical truth, audit ontology or personal-history storage.

## 4. Explicit exclusions from the accepted initial stack

The PM-10 recommendation does not include:

```text
TypeDB primary
XTDB primary
SurrealDB primary
Neo4j
Qdrant
OpenSearch
TimescaleDB
Redis / Valkey
Kafka
RabbitMQ
NATS
Debezium
dedicated event store
universal event sourcing
Temporal
DBOS
Celery + broker
Zero sync
Electric as full LifeOS mutation/sync engine
CRDT/local-first canonical authority
MongoDB for PowerSync
large bytea as standard object storage
public R2 bucket
separate vector DB
separate graph DB
separate search engine
data lake / Spark / Hudi
pg_cron as LifeOS workflow system
Object Lock Compliance as default backup policy
```

These are not hidden future dependencies. Reintroduction requires a later explicit architecture decision backed by a material requirement change.

## 5. Canonical ownership

```text
canonical LifeOS truth         PostgreSQL
material history               PostgreSQL
semantic relations             PostgreSQL explicit mappings
geospatial data/query          PostgreSQL + PostGIS
lexical search                 PostgreSQL FTS / pg_trgm / unaccent
vector retrieval               pgvector derived state
local/offline copy             encrypted SQLite / noncanonical
sync buckets/projections       PowerSync / derived and rebuildable
bounded async                  PostgreSQL outbox/worker
long durable execution         Restate runtime only
raw object bytes               Cloudflare R2
object metadata/authority      PostgreSQL
DB backup repository           pgBackRest -> AWS S3
object backup repository       R2 -> separate AWS S3 bucket
solver result                  OR-Tools candidate/derived state
telemetry                      OTel/Grafana operational state
```

No companion becomes a second canonical source of truth.

## 6. Pass conditions

`PREFERRED / PASS-CONDITIONAL` means selection/implementation must still satisfy the post-selection validation register, including at minimum:

- old-backup anti-resurrection;
- actual LifeOS V1 -> V2 mapping evolution;
- destructive restore + semantic verification;
- capacity/backpressure safe degradation;
- system-level non-interference;
- search/vector filtering and deletion propagation;
- PowerSync replication-liveness and offline-conflict validation;
- encrypted local-storage validation;
- object deletion/restore/reconciliation;
- durable workflow crash/replay/versioning/governance validation;
- Restate deployment-mode privacy/operability validation and journal minimization;
- solver corpus and status handling.

None of these is declared directly executed today.

## 7. Final PM-10 verdict

```text
PM-10
COMPLETE

PREFERRED PRIMARY
PostgreSQL 18.4
PASS-CONDITIONAL

PREFERRED COMPANION ARCHITECTURE
ESTABLISHED

RESTATE DEPLOYMENT
CONDITIONAL / SELF-HOSTED OR CLOUD EU

DIRECT HG PASS
0

VERIFIED-RUN SCORE
NOT AVAILABLE

SELECTED
NONE

NEXT
PM-11 explicit stack selection
```
