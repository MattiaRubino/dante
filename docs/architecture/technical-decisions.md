# DANTE Technical Decisions

- Status: **CURRENT DECISION REGISTER**

This file summarizes current accepted technical decisions. Detailed rationale/constraints live in linked Domain/Logical/Physical/Engineering Foundation sources.

## TD-01 — Canonical persistence

**ACCEPTED**

```text
PostgreSQL 18.4
sole canonical persistence + material-history authority
```

No separate graph/vector/search/event-store database is canonical by default.

## TD-02 — PostgreSQL capability envelope

**ACCEPTED**

Selected target:

- PostGIS 3.6.4;
- pgvector 0.8.6;
- native FTS;
- pg_trgm;
- unaccent;
- pg_stat_statements;
- PgBouncer 1.25.2.

Engineering Foundation adds: the full extension envelope is installed/enabled from the first LOCAL PostgreSQL baseline so compatibility is exercised early, even before every feature uses the capability.

PgBouncer activation remains tied to concrete pooling/replication validation.

## TD-03 — Offline/sync

**ACCEPTED TARGET / NOT IMPLEMENTED**

PowerSync Open Edition + encrypted SQLite bounded local state.

```text
SQLite != canonical truth
PowerSync arrival order != conflict resolution
consequential offline mutation → backend revalidation → PostgreSQL
```

## TD-04 — Async/durable work

**ACCEPTED**

Class A:

```text
PostgreSQL transactional outbox + bounded worker
```

Class B:

```text
Restate selected
initially DORMANT
activation = first real Class-B durable workflow
```

## TD-05 — Object bytes

**ACCEPTED TARGET / NOT IMPLEMENTED**

Cloudflare R2 Standard, private, EU jurisdiction, raw bytes only.

PostgreSQL remains authority for ContentArtifact identity/metadata/provenance/visibility/retention/hash/locator semantics.

## TD-06 — Recovery

**ACCEPTED TARGET / INITIALLY DORMANT**

```text
pgBackRest 2.59.0
+ AWS S3 Standard eu-south-1
+ accepted Versioning/Object Lock GOVERNANCE posture
+ WAL/PITR
```

Activation at recovery/production boundary or real recovery rehearsal.

Recovery copies remain noncanonical and anti-resurrection obligations remain active.

## TD-07 — Solver

**ACCEPTED TARGET / NOT IMPLEMENTED**

OR-Tools CP-SAT.

`UNKNOWN != INFEASIBLE`.

Solver result remains candidate/derived until governed acceptance.

## TD-08 — Observability

**ACCEPTED TARGET**

OpenTelemetry + Grafana Alloy + Grafana Cloud EU + pg_stat_statements.

Operational telemetry is privacy-minimized and noncanonical.

## TD-09 — Repository strategy

**ACCEPTED**

One DANTE product monorepo.

```text
apps/backend
apps/web
apps/mobile
```

Keep the current repository; do **not** create a new production repository.

Repository rename from historical `lifeos` to `dante` is a separate governance action and is the recommended next small step before scaffold unless explicitly deferred.

Extract a separate repository only after a real independent ownership/security/release/scale lifecycle appears.

## TD-10 — Backend architecture

**ACCEPTED**

Capability-first modular monolith.

- no 57 owners → 57 modules mechanical translation;
- no generic CRUD `Repository[T]` semantic model;
- no BaseService/service locator/global session;
- Domain/application meaning independent of FastAPI/SQLAlchemy/provider SDK identity;
- explicit composition root;
- cross-module private implementation not a public interface;
- truthful cross-module ACID transactions allowed where semantics require them.

## TD-11 — Frontend boundary

**ACCEPTED BOUNDARY / INTERNAL ENGINEERING DEFERRED**

`apps/web` and `apps/mobile` are sibling governed clients in the monorepo.

Engineering Foundation does not freeze Node/package manager/task graph/test runners/EAS/shared UI or detailed client source structure. Those decisions belong to the frontend workstream.

## TD-12 — Backend language/runtime

**ACCEPTED**

```text
Python supported line     3.14.x
initial bootstrap pin     3.14.7
package manager           uv
source root               apps/backend/src/dante
```

Ruff, mypy strict, pytest and Hypothesis are the accepted backend quality/test baseline.

## TD-13 — Developer OS/workflow

**ACCEPTED**

Canonical backend/server semantics: Linux.

Primary Windows workflow:

```text
Windows 11
→ WSL2/Linux
→ repo in WSL filesystem
→ Python/uv/backend under Linux semantics
```

PyCharm with WSL interpreter is supported as the user's primary IDE. Repository commands remain IDE-neutral/CLI reproducible.

## TD-14 — LOCAL container model

**ACCEPTED**

Backend application process runs directly in WSL/Linux for normal reload/debug.

Docker Compose owns LOCAL stateful dependencies.

Future deployed backend uses OCI container packaging.

## TD-15 — Persistence toolkit

**ACCEPTED**

```text
SQLAlchemy 2.0 stable line
psycopg 3
Alembic
```

Async DB I/O at technical boundaries; Domain/application logic synchronous/pure by default.

One AsyncSession per concurrent task/use-case. Application boundary owns transaction.

ORM != Domain.

## TD-16 — Migration governance

**ACCEPTED**

- Alembic revisions are deployment schema authority;
- autogenerate candidate only;
- applied revisions immutable;
- no unrepresented manual remote DDL;
- base→head and schema drift CI;
- migration risk classification;
- PostgreSQL online/staged techniques where appropriate;
- expand → migrate → contract;
- large backfills bounded/resumable/idempotent;
- separate DB owner/migrator/runtime/replication/backup privilege classes.

`alembic downgrade` is not assumed to be universal production rollback.

## TD-17 — DB copy/recovery separation

**ACCEPTED**

```text
pg_dump / pg_restore
logical copy/clone/migration-test use

pgBackRest + WAL/PITR
recovery-grade use at activation boundary
```

Raw PROD → DEV is forbidden by default. Production-derived lower-environment data requires explicit sanitization/minimization/authorization.

PostgreSQL major upgrade is a separate platform operation, not an ordinary DANTE migration.

## TD-18 — Environment model

**ACCEPTED**

```text
LOCAL
DEV
UAT
PROD
```

Environment != Git branch.

Remote environment activation is progressive; provider-native security/isolation boundaries are required where practical.

## TD-19 — Cloud/IaC

**DEFERRED INTENTIONALLY**

Compute provider, IaC engine, registry and remote sizing are not selected until first remote infrastructure.

Existing AWS/R2 selections for bounded recovery/object roles do not imply backend compute hosting provider.

## TD-20 — Configuration/secrets

**ACCEPTED**

- pydantic-settings typed/fail-fast immutable backend configuration;
- `.env.local` LOCAL only + safe committed `.env.example`;
- separate non-secret config / secret / build identity / domain configuration;
- remote posture: minimize secret → workload identity → provider secret manager → least privilege → rotation/revocation/audit;
- GitHub OIDC preferred for CI-to-cloud;
- independent environment/workload credentials;
- secrets never baked/committed/logged.

## TD-21 — Backend testing

**ACCEPTED**

Risk-layered testing:

- unit/domain;
- application/use-case;
- Hypothesis property/state-machine;
- architecture;
- real DANTE PostgreSQL integration;
- migration/drift;
- concurrency/expected-state/idempotency/multi-owner/outbox;
- provider/API contract;
- privacy/non-interference;
- release/recovery/PSV at applicable boundary.

SQLite is not PostgreSQL correctness evidence.

No arbitrary coverage threshold before first real vertical slice.

## TD-22 — CI/CD

**ACCEPTED**

GitHub Actions primary CI/CD.

- protected `main`;
- explicit least-privilege permissions;
- protected workflow Actions pinned to immutable full commit SHAs;
- normal PRs receive no PROD/deployment identity;
- OIDC future cloud deployment;
- real emitted check verified before required-check activation;
- GitHub-hosted runners initially;
- fake independent human-review requirement not introduced while there is one active developer;
- merge queue/self-hosted runners deferred until measured need.

## TD-23 — Supply chain

**ACCEPTED ACTIVATION POLICY**

As corresponding artifacts exist:

- dependency review;
- CodeQL Python;
- secret scanning/push protection where available;
- container/IaC scanning;
- immutable artifact promotion;
- production artifact provenance/attestation;
- SBOM/dependency inventory at production release boundary.

Security tooling execution is evidence of that tool, not proof of complete security.

## TD-24 — Selected technologies not to reintroduce casually

Closed Physical selection excluded or did not select as default canonical mechanisms, among others:

- TypeDB/XTDB/SurrealDB as primary persistence;
- Neo4j;
- Qdrant;
- OpenSearch;
- TimescaleDB;
- Redis/Valkey;
- Kafka/RabbitMQ/NATS;
- Debezium;
- dedicated event store/universal event sourcing;
- Temporal/DBOS/Celery as default durable workflow stack;
- Zero/Electric/CRDT local-first canonical authority;
- MongoDB for PowerSync;
- large `bytea` object store;
- public R2;
- separate vector/graph/search servers;
- pg_cron as workflow engine;
- Object Lock Compliance as default recovery posture.

Do not reintroduce them without a materially changed requirement/evidence and explicit architecture reopen.

## TD-25 — Current next boundary

**ACCEPTED HANDOFF**

```text
1. Keep current repository.
2. Decide/execute recommended `lifeos → dante` rename or explicitly defer.
3. Fresh exact write gate for production apps/backend scaffold.
4. Scaffold QA.
5. Concrete Logical → PostgreSQL implementation.
```

Engineering Foundation v0 is closed and is not the next thing to redesign.
