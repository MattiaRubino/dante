# Physical Model

- Status: **AUTHORIZED / IN PROGRESS — PM-10 COMPLETE / PM-11 NEXT**
- Branch: `feature/physical-model`
- Main baseline: `3de84bb49f9cef30e88e9bde4961ed84335daa79`
- PM-00: **QA PASS**
- PM-01: **PASS-CONDITIONAL**
- PM-02: **COMPLETE**
- PM-03: **STATIC COMPLETE / 0 REJECTS**
- PM-04A: **COMPLETE / 0 EXECUTION-WORTHY GAPS**
- PM-04B: **NOT ADMITTED**
- PM-05: **COMPLETE**
- PM-06: **EVIDENCE QUALIFICATION COMPLETE / DIRECT PERFORMANCE NOT RUN**
- PM-07: **EVIDENCE QUALIFICATION COMPLETE / DIRECT DESTRUCTIVE RUNS NOT RUN**
- PM-08: **SECONDARY/SPECIALIST QUALIFICATION COMPLETE**
- PM-09: **EVIDENCE-WEIGHTED SCORING + SENSITIVITY COMPLETE**
- PM-10: **FINAL STACK RECOMMENDATION COMPLETE**
- Preferred primary: **PostgreSQL 18.4 / PASS-CONDITIONAL**
- Evidence-weighted score: **PostgreSQL 89.25 / TypeDB 80.00**
- Ranking: **ROBUST / NOT SENSITIVITY-DEPENDENT / NOT PERFORMANCE-DEPENDENT**
- Preferred companion stack: **ESTABLISHED / PASS-CONDITIONAL**
- Selected: **NONE**
- Backend Foundation: **NOT STARTED / DEFERRED**

## Purpose

Turn accepted LifeOS Domain + Logical semantics into a durable, evidence-backed Physical Model without weakening semantics or manufacturing benchmarks that cannot change the decision.

```text
DOMAIN + LOGICAL
fixed semantic authority

PHYSICAL
research
→ candidate-native mapping
→ semantic preflight
→ evidence sufficiency
→ correctness qualification
→ finalist qualification
→ specialist lanes
→ scoring/sensitivity
→ final stack audit
→ preferred recommendation
→ explicit selection
→ accepted model / clean-room QA / main integration
```

## Non-negotiable barriers

```text
SEMANTIC OWNER != IMPLEMENTATION MECHANISM
ADDRESSABILITY != DOMAIN IDENTITY
STORAGE TOKEN != MaterialStateRef
CANONICAL != PROVIDER / DERIVED / SECURITY STATE
SECONDARY != CANONICAL
LOCAL != CANONICAL
RUNTIME != DOMAIN HISTORY
MISSING != FALSE
EVIDENCE-QUALIFIED != EXECUTED PASS
EVIDENCE-WEIGHTED SCORE != VERIFIED-RUN SCORE
PUBLIC BENCHMARK != LIFEOS BENCHMARK
FINALIST != PREFERRED
PREFERRED != SELECTED
```

No universal Entity/Thing/EAV/generic-edge canonical shortcut may be introduced for implementation convenience.

## Evidence-first execution policy

```text
LOCAL EXECUTION
last-mile evidence only
```

A direct run requires a residual question that remains unresolved, is materially decision-relevant, and can actually be resolved by controlled execution.

Current direct execution state:

```text
benchmark host          HOLD / DORMANT
database deployment     NOT STARTED
fixture/harness          NOT STARTED
LOW/BASE/HIGH            NOT RUN
direct HG PASS           0
restore rehearsal        NOT RUN
migration rehearsal      NOT RUN
failure injection        NOT RUN
verified-run score       NOT AVAILABLE
```

## Two score ledgers

```text
VERIFIED-RUN BENCHMARK SCORE
requires direct applicable hard-gate PASS and execution artifacts

EVIDENCE-WEIGHTED DECISION SCORE
used by PM-09 after evidence exhaustion and 0 ranking-critical execution gaps
```

The PM-09 score is the second type only. PM-10 consumes it for recommendation without manufacturing direct PASS.

## PM-10 preferred primary

### PostgreSQL 18.4

```text
PM-09 SCORE
89.25 / 100

SENSITIVITY
ROBUST

PM-10
PREFERRED / PASS-CONDITIONAL

SELECTED
NONE
```

Why it is preferred:

- accepted mapping preserves LifeOS semantics without a universal ontology root;
- strong transaction/concurrency ergonomics and mature integrity primitives;
- WAL/PITR/backup/replication/evolution maturity;
- reporting/traversal/search ecosystem;
- PostGIS, pgvector and PostgreSQL-native search keep major accepted capabilities inside one primary database ecosystem;
- lower topology, synchronization, operational and exit burden than the TypeDB finalist path.

Performance is not a hidden reason for the lead: PM-09 deliberately scored performance `8.0 / 8.0` because LOW/BASE/HIGH were not executed.

### TypeDB CE 3.12.3

TypeDB remains the semantic runner-up with the strongest direct relation/role/n-ary fit, but it is not PM-10 preferred because its advantages do not outweigh the accepted whole-system costs under LifeOS priorities.

## Recommended stack

```text
CANONICAL
PostgreSQL 18.4

POSTGRESQL CAPABILITIES
PostGIS 3.6.4
pgvector 0.8.6
native FTS
pg_trgm
unaccent
pg_stat_statements
PgBouncer 1.25.2

BOUNDED ASYNC
PostgreSQL transactional outbox + bounded worker

DURABLE CLASS-B PROCESS
Restate Cloud EU
Restate Python SDK 1.0.3
Restate Server 1.7.2 reproducible local/self-hosted subject

OFFLINE / SYNC
PowerSync Service 1.25.0 Open Edition
encrypted SQLite
PostgreSQL-backed PowerSync bucket storage
explicit client-safe sync projections only

OBJECT BYTES
Cloudflare R2 Standard
EU jurisdiction
private

BACKUP
pgBackRest 2.59.0 -> AWS S3 Standard eu-south-1
R2 object backup -> separate AWS S3 eu-south-1 bucket

SOLVER
OR-Tools 9.15 CP-SAT

OBSERVABILITY
OpenTelemetry
Grafana Alloy 1.18.0
Grafana Cloud EU
pg_stat_statements
```

## Offline semantics

Offline capability is required but operation-specific.

```text
SQLite
bounded encrypted local working copy

PowerSync
transport/synchronization

LifeOS backend
semantic expected-state / governance / AuthZ / conflict authority

PostgreSQL
canonical truth
```

No global last-write-wins rule is accepted. A local mutation made while offline may be rejected or enter reconciliation when its material basis is stale or governance changed.

## Object semantics

`ContentArtifact` identity, metadata, provenance, visibility, retention and locator state remain in PostgreSQL. R2 stores raw bytes only. Private object access is governed; public R2 buckets/public permanent URLs are not part of the accepted recommendation.

## Durable execution semantics

Short/reconstructible background work uses the PostgreSQL outbox/worker baseline. Long-running recoverable work with human/external waits uses Restate. Runtime state never replaces Domain Actual/Decision/Confirmation/history.

## Solver semantics

OR-Tools outputs are candidates. `OPTIMAL`, `FEASIBLE`, `INFEASIBLE` and `UNKNOWN` are technical solver outcomes; they cannot silently become canonical LifeOS Decisions or semantic truth.

## Technology exclusions

The proposed PM-11 stack intentionally excludes:

```text
TypeDB/XTDB/SurrealDB primary
Neo4j
Qdrant
OpenSearch
TimescaleDB
Redis/Valkey
Kafka
RabbitMQ
NATS
Debezium
dedicated event store / universal event sourcing
Temporal
DBOS
Celery + broker
Zero
Electric as full mutation/sync engine
CRDT/local-first canonical authority
MongoDB for PowerSync
large bytea object store
public R2
separate vector/graph/search servers
data lake/Spark/Hudi
pg_cron as workflow engine
Object Lock Compliance as default
```

See `recommendation/technology-exclusion-register-v1.md` for rationale.

## PM-10 supporting records

```text
pm-10-recommendation-v1.md
final-stack-audit-v1.md
final-stack-capability-matrix-v1.md
final-stack-simulation-v1.md
recommendation/postgresql-18.4-v1.md
recommendation/companion-stack-v1.md
recommendation/technology-exclusion-register-v1.md
recommendation/post-selection-validation-register-v1.md
```

## Post-selection validation

Scoring/recommendation does not waive direct selected-stack validation.

Core obligations still include:

```text
SC-011 old-backup anti-resurrection
SC-030 actual LifeOS V1→V2 mapping evolution
SC-031 semantic backup/restore verification
SC-032 capacity/backpressure
WL-H12 non-interference
search/vector/projection deletion/freshness
PowerSync offline/replication/local-encryption
Restate crash/replay/governance/versioning
R2/S3 object recovery
PostGIS/PgBouncer compatibility
OR-Tools status/governance corpus
observability privacy
```

The full register is `recommendation/post-selection-validation-register-v1.md`.

## Roadmap

```text
PM-00  PASS
PM-01  PASS-CONDITIONAL
PM-02  COMPLETE
PM-03  COMPLETE
PM-04A COMPLETE
PM-04B NOT ADMITTED
PM-05  COMPLETE
PM-06  COMPLETE
PM-07  COMPLETE
PM-08  COMPLETE
PM-09  COMPLETE
PM-10  COMPLETE
PM-11  NEXT
PM-12  NOT STARTED
PM-13  NOT STARTED
PM-14  NOT STARTED
```

## Current exact next step

```text
PM-11
explicit user-approved stack selection
fresh exact write gate required

PREFERRED
PostgreSQL 18.4 / PASS-CONDITIONAL

PREFERRED COMPANION STACK
ESTABLISHED / PASS-CONDITIONAL

SELECTED NONE
BACKEND NOT STARTED / DEFERRED
```
