# Companion Stack Recommendation v1

- Status: **PM-10 RECOMMENDED COMPANION ARCHITECTURE**
- Primary dependency: PostgreSQL 18.4 preferred primary
- Selection: **NOT SELECTED UNTIL PM-11**

## Recommended stack

### PostgreSQL-adjacent

```text
PostGIS 3.6.4
pgvector 0.8.6
native FTS
pg_trgm
unaccent
pg_stat_statements
PgBouncer 1.25.2
```

### Offline / sync

```text
PowerSync Service 1.25.0 Open Edition
encrypted SQLite local database
PostgreSQL-backed PowerSync bucket storage
explicit sync_projection publication only
```

Rules:

- local SQLite is a bounded encrypted working copy;
- PostgreSQL remains canonical;
- broad canonical publication is not the default;
- consequential mutations re-enter the LifeOS backend;
- expected material state, governance and authorization are revalidated;
- universal LWW is forbidden;
- Visibility/Consent/redaction changes must invalidate/update/reset affected client copies.

### Async / workflow

```text
Class A bounded async
PostgreSQL transactional outbox + bounded worker

Class B material durable process
Restate runtime
Restate Python SDK 1.0.3
Restate Server 1.7.2 self-hosted/reproducible subject
Restate Cloud EU allowed as managed deployment
```

`Restate runtime` is the technology recommendation. Deployment is deliberately conditional rather than hard-coded to Cloud EU:

```text
SELF-HOSTED
first-class option when privacy/data-control or Python journal-encryption constraints dominate

CLOUD EU
managed option when operational value is preferred and the privacy assessment accepts the journal posture
```

Current Restate documentation supports a self-contained server binary/container. Current client-side journal encryption for Restate Cloud is documented only for the TypeScript SDK; the LifeOS target path is Python. Therefore Cloud EU must not be treated as mandatory merely for managed convenience.

Restate journal payloads must be minimized and should normally carry technical execution identifiers plus bounded references rather than duplicate full personal canonical payloads. Runtime state is never Domain history.

### Object storage

```text
Cloudflare R2 Standard
EU jurisdiction
private bucket
```

No public bucket or permanent public URL is part of the accepted design. Raw bytes belong in R2; `ContentArtifact` authority and metadata remain in PostgreSQL.

### Recovery

```text
pgBackRest 2.59.0
-> AWS S3 Standard eu-south-1
-> versioning
-> Object Lock GOVERNANCE
-> finite policy-bound retention

R2 raw object backup
-> separate S3 eu-south-1 bucket
```

Database and object backup repositories remain logically separated.

### Solver

```text
OR-Tools 9.15 CP-SAT
```

Solver results remain candidates until accepted by applicable LifeOS semantics.

### Observability

```text
OpenTelemetry
Grafana Alloy 1.18.0
Grafana Cloud EU
pg_stat_statements
```

Operational telemetry must be privacy-minimized.

## PowerSync hardening condition

Current PowerSync evidence includes an open replication-liveness failure mode where source replication can stall while a basic health endpoint remains healthy. Therefore production acceptance requires:

```text
independent replication/checkpoint lag metric
stall detection
alerting
controlled reconnect/restart
half-open source-connection destructive test
client reconciliation validation after recovery
```

The component is recommended because its mutation path preserves server authority better than the current alternatives reviewed; the known risk is not ignored.

## Topology principle

The companion stack must not become a mesh of authorities:

```text
PostgreSQL = canonical
PowerSync/SQLite = local/sync projection
Restate = execution runtime
R2 = raw bytes
S3 = recovery copy
OR-Tools = solver candidate engine
Grafana stack = telemetry
```

## Verdict

```text
COMPANION STACK
RECOMMENDED / PASS-CONDITIONAL

RESTATE TECHNOLOGY
RECOMMENDED

RESTATE DEPLOYMENT
CONDITIONAL: SELF-HOSTED OR CLOUD EU

SECOND CANONICAL AUTHORITY
NONE
```
