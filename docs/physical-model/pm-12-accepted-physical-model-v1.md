# PM-12 — Accepted Physical Model v1

- Status: **COMPLETE — ACCEPTED PHYSICAL MODEL ESTABLISHED**
- Current product/app name: **DANTE** (`LifeOS` remains the previous working/project name in historical evidence and technical identifiers)
- Historical workstream: `feature/physical-model`
- Selection authority: `pm-11-explicit-selection-v1.md`
- Domain authority: unchanged / closed
- Logical authority: unchanged / closed / `WL-H01..WL-H12` active
- Direct execution: **NOT STARTED**
- Backend implementation: **NOT STARTED / OUT OF SCOPE**
- Subsequent lifecycle: **PM-13 QA PASS → PM-14 branch/workstream closure COMPLETE → PR #15 protected-main integration COMPLETE**

## 1. Purpose

This document is the accepted target Physical Model for DANTE. It converts the selected PM-11 technology stack into one bounded ownership/topology contract without changing Domain or Logical semantics.

```text
ACCEPTED PHYSICAL MODEL
!= DEPLOYMENT PROFILE
!= DEV-v0 ACTIVATION PLAN
!= BACKEND IMPLEMENTATION
!= DIRECT TEST PASS
```

A later Development Profile may decide which selected components are activated immediately, self-hosted, managed, free-tier or temporarily dormant. That operational profile must not silently change this target architecture.

## 2. Canonical persistence

```text
PostgreSQL 18.4
CANONICAL PRIMARY
```

PostgreSQL is the sole canonical persistence engine for accepted DANTE state and material history. The accepted PostgreSQL mapping remains authoritative for how Logical owners and references are represented.

Forbidden shortcuts remain forbidden:

```text
no universal Entity/Thing root
no generic EAV canonical kernel
no universal semantic edge root
no provider/system token as MaterialStateRef
no technical AuthZ as Domain Authority/Consent
no runtime/projection state as canonical truth
```

## 3. PostgreSQL capability envelope

```text
PostGIS 3.6.4
geospatial representation/query

pgvector 0.8.6
derived vector retrieval

native FTS + pg_trgm + unaccent
lexical/fuzzy/accent-normalized search baseline

pg_stat_statements
query telemetry

PgBouncer 1.25.2
connection pooling for compatible connection classes
```

These capabilities remain inside the PostgreSQL ecosystem but do not become independent Domain owners.

## 4. Search / retrieval model

```text
LEXICAL
PostgreSQL native FTS + pg_trgm + unaccent

SEMANTIC/VECTOR
pgvector derived state

DEDICATED SEARCH ENGINE
NONE

DEDICATED VECTOR DATABASE
NONE
```

Visibility, scope, freshness and deletion rules apply before/while producing user-visible retrieval results. Derived indexes cannot override canonical access semantics.

## 5. Geospatial model

```text
CANONICAL PLACE/LOCATION STATE
PostgreSQL

SPATIAL CAPABILITY
PostGIS

DEVICE GEOFENCING
execution mechanism only where useful
```

A device geofence event is not itself canonical DANTE consequence. Consequential behavior re-enters governed DANTE semantics where applicable.

## 6. Offline / multi-device model

```text
CANONICAL
PostgreSQL

LOCAL WORKING COPY
encrypted SQLite

SYNC ENGINE
PowerSync Service 1.25.0 Open Edition

SYNC STORAGE
PostgreSQL-backed PowerSync bucket storage
noncanonical / derived / rebuildable
```

Required flow:

```text
canonical PostgreSQL
      ↓ approved client-safe sync projections
PowerSync
      ↓
encrypted SQLite
      ↓ offline mutation
DANTE backend
      ↓ expected-state + governance + AuthZ validation
PostgreSQL canonical commit
```

Rules:

- offline capability is operation-specific;
- local arrival order does not define semantic truth;
- universal consequential LWW is forbidden;
- sync publication is explicit and bounded;
- visibility/deletion/redaction changes propagate to every affected local/projection copy;
- PowerSync bucket state is downstream/rebuildable and never recovery truth.

## 7. Async / durable-execution model

### Class A — bounded async

```text
PostgreSQL transactional outbox
+
bounded worker
```

Use for reconstructible/bounded background work where a dedicated durable workflow runtime is unnecessary.

### Class B — material durable execution

```text
Restate runtime
Restate Python SDK 1.0.3
Restate Server 1.7.2 selected self-hosted/reproducible subject
```

Use where execution must survive or explicitly model:

- long waits;
- callbacks;
- human approval/wait states;
- external unknown outcome;
- retry/replay/idempotency;
- cancellation/deadline;
- workflow version evolution;
- recovery after process/runtime failure.

### Restate deployment

```text
SELF-HOSTED
first-class selected deployment option

CLOUD EU
selected managed deployment option

GLOBAL MANDATORY DEFAULT
NONE
```

The deployment profile chooses between the two. For the current Python path, Cloud journal client-side encryption must not be assumed because current Restate documentation exposes that feature only through the TypeScript SDK. Journal payloads therefore remain minimized technical execution state, preferably IDs/references and bounded parameters rather than duplicated personal canonical payloads.

## 8. Object model

```text
RAW OBJECT BYTES
Cloudflare R2 Standard
EU jurisdiction
private

OBJECT IDENTITY / METADATA / AUTHORITY
PostgreSQL ContentArtifact mapping
```

PostgreSQL owns identity, provenance, hashes, MIME/type, Visibility, retention semantics and object locator. R2 owns bytes only.

No public R2 bucket or permanent public object URL is accepted by default.

## 9. Recovery model

```text
POSTGRESQL BACKUP
pgBackRest 2.59.0
→ AWS S3 Standard eu-south-1
→ Versioning
→ Object Lock GOVERNANCE
→ finite policy-bound retention

R2 OBJECT BACKUP
→ separate AWS S3 eu-south-1 bucket/repository
```

Recovery copies never become canonical state.

Anti-resurrection rule:

1. restore canonical PostgreSQL under accepted recovery procedure;
2. apply/verify deletion-redaction suppression/anti-resurrection state;
3. verify canonical semantic state;
4. rebuild/discard stale derived sync/search/vector state as required;
5. reconcile object backup state before reopening affected traffic.

`Object Lock Compliance` is not the default because irreversible retention must not structurally defeat accepted privacy/deletion policy.

## 10. Solver model

```text
OR-Tools 9.15 CP-SAT
```

Solver output is candidate/derived state. Required semantic barrier:

```text
OPTIMAL / FEASIBLE / INFEASIBLE / UNKNOWN
= technical solver status
!= accepted DANTE Decision
```

`UNKNOWN != INFEASIBLE`.

## 11. Observability model

```text
OpenTelemetry
→ Grafana Alloy 1.18.0
→ Grafana Cloud EU

PostgreSQL
→ pg_stat_statements
```

Observability collects privacy-minimized operational telemetry such as latency, error rate, backlog, replication lag, workflow failures, backup health and query behavior.

Telemetry is not canonical DANTE history and must not become a shadow personal-data store.

## 12. State ownership matrix

| State | Physical owner / mechanism | Canonical? |
|---|---|---|
| DANTE current truth | PostgreSQL | YES |
| Material history | PostgreSQL | YES |
| Semantic relations | PostgreSQL explicit mappings | YES |
| Geospatial query | PostGIS over PostgreSQL | capability over canonical data |
| Lexical search | PostgreSQL FTS/pg_trgm/unaccent | derived/query |
| Vector retrieval | pgvector | derived |
| Local/offline copy | encrypted SQLite | NO |
| Sync buckets/projections | PowerSync | NO / rebuildable |
| Bounded async runtime | PG outbox/worker | NO |
| Durable workflow runtime | Restate | NO |
| Raw object bytes | R2 | object bytes only |
| Object authority/metadata | PostgreSQL | YES |
| DB/object backups | pgBackRest/S3 | NO / recovery only |
| Solver result | OR-Tools | NO / candidate |
| Telemetry | OTel/Alloy/Grafana | NO / operational |

## 13. Excluded initial target technologies

The accepted Physical Model does not include the PM-10 exclusion set, including TypeDB/XTDB/SurrealDB as primary, Neo4j, Qdrant, OpenSearch, TimescaleDB, Redis/Valkey, Kafka, RabbitMQ, NATS, Debezium, universal event sourcing, Temporal, DBOS, Celery+broker, Zero, Electric as full mutation authority, CRDT canonical authority, MongoDB for PowerSync, separate graph/vector/search databases, data lake/Spark/Hudi and pg_cron as workflow system.

A later material requirement can reopen a technology decision only through an explicit architecture change.

## 14. Direct evidence truth

The accepted target architecture is evidence-backed but not directly deployed/tested yet.

```text
DATABASE DEPLOYMENT      NOT STARTED
FIXTURE/HARNESS           NOT STARTED
DIRECT HG PASS            0
LOW/BASE/HIGH            NOT RUN
RESTORE                   NOT RUN
MIGRATION                 NOT RUN
FAILURE INJECTION         NOT RUN
POWERSYNC                  NOT RUN
RESTATE                    NOT RUN
OBJECT RECOVERY            NOT RUN
SOLVER                     NOT RUN
VERIFIED-RUN SCORE        NOT AVAILABLE
```

No line in this Accepted Physical Model overrides that truth.

## 15. Mandatory implementation validation

`recommendation/post-selection-validation-register-v1.md` remains authoritative. PM-12 accepts the Physical architecture while carrying those obligations into implementation/release gates.

A failed applicable validation can reopen the affected Physical decision; it cannot be papered over by weakening Domain/Logical semantics.

## 16. DEV-v0 boundary

A later bounded `Development Profile v0` should answer operational questions such as:

- which selected services are active immediately;
- self-hosted vs managed deployment where the Physical Model allows both;
- free-tier/local development choices;
- credentials/accounts and environment setup;
- initial backup/observability activation;
- upgrade/production triggers.

That profile is intentionally **not** defined by PM-12.

## 17. PM-12 verdict

```text
PM-12
COMPLETE

ACCEPTED PHYSICAL MODEL
ESTABLISHED

CANONICAL PRIMARY
PostgreSQL 18.4

TARGET COMPANION ARCHITECTURE
SELECTED / BOUNDED

RESTATE DEPLOYMENT
SELF-HOSTED OR CLOUD EU / PROFILE DECISION

DIRECT EXECUTION
NOT STARTED
```

Historical progression after PM-12:

```text
PM-13 independent clean-room QA   PASS
PM-14 branch/workstream closure   COMPLETE
PR #15 protected-main integration COMPLETE
```

Current next project boundary is **Development Profile v0**, not PM-13.
