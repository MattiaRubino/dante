# PM-11 — Explicit Physical Stack Selection v1

- Status: **COMPLETE — EXPLICIT USER-APPROVED SELECTION**
- Workstream: `feature/physical-model`
- PM-10 recommendation base: `4a988b115e445c726910ef5c3da7e2629d73eaf1` plus approved Restate deployment qualification
- Selection authority: explicit user approval in the PM-11 gate
- Direct execution: **NOT STARTED**
- Verified-run benchmark score: **NOT AVAILABLE**

## 1. Selection rule

PM-11 converts the PM-10 target recommendation from `PREFERRED` to `SELECTED` without changing evidence truth.

```text
PREFERRED != SELECTED
SELECTED != DIRECT PASS
SELECTED != DEPLOYED
SELECTED != DEV-v0 ACTIVE
```

The selected stack is the target Physical architecture. Development/deployment activation is a later, separately bounded decision.

## 2. Selected canonical primary

```text
PostgreSQL 18.4
SELECTED — CANONICAL PRIMARY
```

PostgreSQL owns canonical LifeOS persistence and material history through the accepted PostgreSQL mapping. It does not create a universal Entity/EAV/generic-edge semantic kernel.

PM-09 evidence-weighted score remains `89.25 / 100`; TypeDB CE 3.12.3 remains the historical semantic runner-up at `80.00 / 100`.

## 3. Selected PostgreSQL-adjacent capabilities

```text
PostGIS 3.6.4
SELECTED — GEOSPATIAL EXTENSION

pgvector 0.8.6
SELECTED — VECTOR EXTENSION / DERIVED RETRIEVAL

PostgreSQL native FTS
pg_trgm
unaccent
SELECTED — LEXICAL SEARCH BASELINE

pg_stat_statements
SELECTED — POSTGRESQL QUERY OBSERVABILITY

PgBouncer 1.25.2
SELECTED — CONNECTION POOLER
```

These are implementation capabilities, not Domain owners or independent canonical authorities.

## 4. Selected offline / multi-device architecture

```text
PowerSync Service 1.25.0 Open Edition
SELECTED — SYNC ENGINE

encrypted SQLite
SELECTED — BOUNDED LOCAL/OFFLINE SUBSTRATE

PostgreSQL-backed PowerSync bucket storage
SELECTED — DERIVED/REBUILDABLE SYNC STORAGE
```

Hard boundaries:

- PostgreSQL remains canonical;
- SQLite remains local/noncanonical;
- only explicitly approved client-safe projections may be replicated;
- consequential offline mutations re-enter the LifeOS backend;
- expected material state, governance and authorization are revalidated before canonical commit;
- universal consequential last-write-wins is forbidden;
- Visibility/Consent/redaction/delete must propagate into sync/local copies.

## 5. Selected async / durable-execution architecture

```text
Class A bounded async
PostgreSQL transactional outbox + bounded worker
SELECTED

Class B material long-running durable execution
Restate runtime
SELECTED

Restate Python SDK 1.0.3
SELECTED SDK SUBJECT

Restate Server 1.7.2
SELECTED SELF-HOSTED/REPRODUCIBLE SUBJECT
```

### Restate deployment disposition

```text
SELF-HOSTED
ALLOWED / FIRST-CLASS

RESTATE CLOUD EU
ALLOWED / MANAGED OPTION

GLOBAL DEFAULT
NONE
```

Restate technology is selected; deployment mode is intentionally **not globally fixed**. The later operating/development/production profile chooses self-hosted or Cloud EU based on privacy, operability, availability and cost without reopening the durable-execution technology decision.

Current Restate documentation establishes that the server can run as a self-contained binary/container and that Cloud environments support an EU region. Current client-side journal encryption is documented only for the TypeScript SDK, while LifeOS currently targets Python; therefore Cloud EU is not mandatory and journal minimization is a hard boundary in either deployment mode.

Restate state is runtime state only and must not become a duplicate canonical personal-history store.

## 6. Selected object architecture

```text
Cloudflare R2 Standard
EU jurisdiction
private
SELECTED — OPERATIONAL OBJECT STORE
```

R2 owns raw object bytes only. PostgreSQL owns `ContentArtifact` identity, metadata, provenance, Visibility, retention semantics, hashes and object locators.

No public bucket/permanent public object URL is part of the selected design.

## 7. Selected recovery architecture

```text
pgBackRest 2.59.0
SELECTED — POSTGRESQL BACKUP/RESTORE ORCHESTRATOR

AWS S3 Standard eu-south-1
SELECTED — PRODUCTION OFF-SITE BACKUP REPOSITORY TARGET

S3 Versioning
SELECTED

S3 Object Lock GOVERNANCE
SELECTED — FINITE POLICY-BOUND RETENTION MODE
```

Database backups and raw-object backups use logically separate repositories/buckets. S3 is recovery state, never canonical or normal application object storage.

`Object Lock Compliance` is not the default because irreversible retention must not structurally override accepted privacy/deletion policy.

## 8. Selected solver architecture

```text
OR-Tools 9.15 CP-SAT
SELECTED — CONSTRAINT SOLVER
```

Solver output remains candidate/derived state. `UNKNOWN != INFEASIBLE`; no solver outcome silently becomes an accepted LifeOS Decision or consequential effect.

## 9. Selected observability architecture

```text
OpenTelemetry
SELECTED — TELEMETRY STANDARD

Grafana Alloy 1.18.0
SELECTED — COLLECTION/PIPELINE

Grafana Cloud EU
SELECTED — TARGET MANAGED OBSERVABILITY SERVICE

pg_stat_statements
SELECTED — DATABASE QUERY TELEMETRY
```

Telemetry is privacy-minimized operational state and is never canonical LifeOS history/audit ontology.

## 10. Explicit non-selection register

The PM-10 exclusion register remains active. In particular, the selected target does **not** include:

```text
TypeDB / XTDB / SurrealDB as primary
Neo4j
Qdrant
OpenSearch
TimescaleDB
Redis / Valkey
Kafka / RabbitMQ / NATS
Debezium
dedicated event store / universal event sourcing
Temporal
DBOS
Celery + broker
Zero
Electric as full LifeOS mutation/sync engine
CRDT/local-first canonical authority
MongoDB for PowerSync
large bytea standard object repository
public R2
separate vector / graph / search servers
data lake / Spark / Hudi
pg_cron as workflow engine
Object Lock Compliance as default
```

Any reintroduction requires a later explicit architecture reopen based on materially changed requirements/evidence.

## 11. Direct-execution truth preserved

```text
DATABASE DEPLOYMENT      NOT STARTED
FIXTURE/HARNESS           NOT STARTED
DIRECT HG-01..HG-12      NOT RUN
DIRECT HG PASS            0
LOW/BASE/HIGH            NOT RUN
RESTORE REHEARSAL         NOT RUN
MIGRATION REHEARSAL       NOT RUN
FAILURE INJECTION         NOT RUN
POWERSYNC DIRECT TEST     NOT RUN
RESTATE DIRECT TEST       NOT RUN
OBJECT RECOVERY TEST      NOT RUN
SOLVER DIRECT TEST        NOT RUN
VERIFIED-RUN SCORE        NOT AVAILABLE
```

Selection does not manufacture execution evidence.

## 12. Mandatory carry-forward

`docs/physical-model/recommendation/post-selection-validation-register-v1.md` remains mandatory. Applicable obligations are implementation/release gates at their stated boundary and must not be erased by PM-11 selection.

## 13. PM-11 verdict

```text
PM-11
COMPLETE

TARGET PHYSICAL STACK
SELECTED

CANONICAL PRIMARY
PostgreSQL 18.4

RESTATE TECHNOLOGY
SELECTED

RESTATE DEPLOYMENT
CONDITIONAL: SELF-HOSTED OR CLOUD EU

DIRECT EXECUTION
NOT STARTED

NEXT
PM-12 Accepted Physical Model
```
