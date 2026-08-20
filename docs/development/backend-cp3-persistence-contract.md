# DANTE Backend CP3 — Persistence, migrations and real PostgreSQL contract

- Status: **CLOSED / DIRECT QA PASS**
- Workstream: `feature/backend-scaffold`
- Scope: technical persistence boundary only
- Implementation/direct-QA HEAD: `35cf6440bc121a38342f6bbee72e210435a788a4`
- Concrete Logical → PostgreSQL business mapping: **OUT OF SCOPE**

## 1. Purpose

CP3 activates the first real DANTE application persistence boundary on the already accepted PostgreSQL 18.4 LOCAL stack.

It establishes:

```text
typed database configuration
        ↓
one process-scoped AsyncEngine
        ↓
one process-scoped async_sessionmaker
        ↓
one AsyncSession per application operation/task
        ↓
explicit transaction boundary
        ↓
PostgreSQL 18.4
```

It also establishes Alembic as deployed-schema authority, the `dante` application schema, the owner/migrator/runtime privilege split and a real PostgreSQL acceptance harness.

CP3 deliberately does **not** create business/domain tables or persistence adapters for Logical owners.

## 2. Resolved dependency contract

Compatibility policy in `apps/backend/pyproject.toml`:

```text
SQLAlchemy[asyncio]  >=2.0.51,<2.1
psycopg[binary]      >=3.3.4,<3.4
Alembic              >=1.19.1,<1.20
pytest-asyncio       >=1.4.0,<2
```

The lock was generated with `uv` on the canonical WSL workstation. Current exact CP3 resolution:

```text
SQLAlchemy       2.0.52
psycopg          3.3.4
Alembic          1.19.1
pytest-asyncio   1.4.0
```

`uv.lock` is generated state and must never be hand-edited.

## 3. Database configuration

Runtime database configuration is nested, typed and immutable:

```text
DANTE_DATABASE__HOST
DANTE_DATABASE__PORT
DANTE_DATABASE__NAME
DANTE_DATABASE__USER
DANTE_DATABASE__PASSWORD
DANTE_DATABASE__CONNECT_TIMEOUT_SECONDS
DANTE_DATABASE__POOL_SIZE
DANTE_DATABASE__MAX_OVERFLOW
DANTE_DATABASE__POOL_TIMEOUT_SECONDS
DANTE_DATABASE__READINESS_TIMEOUT_SECONDS
```

Rules:

- password is a `SecretStr`;
- no canonical raw DSN string is accepted as the DANTE configuration model;
- SQLAlchemy URLs are built through `URL.create()`;
- runtime, migration and provisioning credentials are separate boundaries;
- `.env.example` contains runtime configuration only;
- admin and migrator secrets must not be added to the normal backend runtime environment.

## 4. Engine and lifecycle

One `AsyncEngine` exists per backend process and is owned by the FastAPI lifespan.

Accepted engine posture:

```text
postgresql+psycopg
pool_pre_ping=True
pool_size=configured
max_overflow=configured
pool_timeout=configured
pool_recycle=not forced
hide_parameters=True
echo=False
echo_pool=False
```

The engine is lazy: PostgreSQL unavailability does not make engine construction itself crash the process.

Shutdown performs `await engine.dispose()`.

No global `Session` or `async_scoped_session` is used.

## 5. Session and transaction architecture

Accepted session posture:

```text
one async_sessionmaker per process
one AsyncSession per application operation/task
expire_on_commit=False
autobegin=False
autoflush=True
```

Transaction authority belongs to the outer application-operation boundary.

Persistence adapters may flush when required but must not commit implicitly.

Conceptual shape:

```text
HTTP / MOBILE / AI / WORKER / WORKFLOW
                  ↓
        application operation
                  ↓
          one transaction
                  ↓
     persistence adapters
                  ↓
       same AsyncSession
                  ↓
          PostgreSQL
```

There is no generic `Repository[T]` or generic Unit of Work in CP3.

Nested transactions are not the default composition model. `SAVEPOINT` / `session.begin_nested()` is allowed only when partial-failure semantics genuinely require it.

Default PostgreSQL isolation remains `READ COMMITTED`; stronger locking/isolation is selected later per concrete invariant.

No hidden statement retry or automatic transaction retry is introduced in CP3.

## 6. Readiness and failure semantics

`GET /health/live` is process-only and does not depend on PostgreSQL.

`GET /health/ready` performs a bounded real database probe:

```text
SELECT 1 success        → 200 {"status":"ready"}
DB unavailable/timeout  → 503 {"status":"not_ready"}
```

The response must never expose database host, database name, credentials, DSN, SQL or stack details.

A stale connection returned to the SQLAlchemy pool must be recoverable on a later checkout through `pool_pre_ping`.

A disconnect during an active transaction is not hidden or retried; the transaction fails.

## 7. Canonical SQLAlchemy metadata

DANTE owns one technical metadata graph and one declarative base.

Application schema:

```text
dante
```

Extension/provider objects remain outside DANTE schema authority, currently in `public`.

Naming convention:

```text
PK     pk_<table>
FK     fk_<table>_<columns>_<referred_table>
UNIQUE uq_<table>_<columns>
INDEX  ix_<table>_<columns>
CHECK  ck_<table>_<semantic-name>
```

SQLAlchemy persistence mappings remain persistence models, not Domain identity.

## 8. Alembic governance

Alembic lives under:

```text
apps/backend/migrations/
```

Configuration is owned by `[tool.alembic]` in `apps/backend/pyproject.toml`; there is no duplicate credential-bearing `alembic.ini`.

Rules:

```text
one canonical PostgreSQL database
one Alembic environment
one migration DAG
one canonical head on integrated main
version table = dante.alembic_version
```

`env.py`:

- authenticates with the dedicated migrator credential;
- performs `SET ROLE dante_owner` before migration DDL;
- uses `include_schemas=True` with a strict `dante` schema allow-list;
- compares types and server defaults;
- excludes `public` extension/provider objects from DANTE autogenerate authority;
- rejects offline migration execution;
- revokes runtime access to `dante.alembic_version`.

`metadata.create_all()` is not a deployment mechanism.

Autogenerate output is a candidate only and always requires review.

Merged/applied migration history is immutable; corrections use new revisions.

CP3 begins with one empty technical baseline revision:

```text
20260820_01
```

It proves migration machinery without inventing business schema.

## 9. PostgreSQL identity and privilege model

Database/platform administrator remains outside application ownership.

Application roles:

```text
dante_owner
  NOLOGIN
  owns schema dante and DANTE-created objects

dante_migrator
  LOGIN
  NOINHERIT
  member of dante_owner with:
    INHERIT FALSE
    SET TRUE
    ADMIN FALSE

dante_runtime
  LOGIN
  NOINHERIT
  no dante_owner membership
  runtime DML only
```

The migrator authenticates as `dante_migrator` and deliberately executes `SET ROLE dante_owner`; therefore migration-created objects are owned by `dante_owner`, not by the login role.

Runtime receives:

```text
database CONNECT
schema dante USAGE
future tables SELECT/INSERT/UPDATE/DELETE
future sequences USAGE
future DANTE types USAGE
```

Runtime does not receive by default:

```text
schema CREATE
DDL
TRUNCATE
TEMP
owner membership
migration-history access
routine EXECUTE
```

The database and `public` schema are explicitly hardened against broad `PUBLIC` privileges.

Owner default privileges are configured while `SET ROLE dante_owner` is active.

Important PostgreSQL 18 correction incorporated during CP3 review:

```sql
ALTER DEFAULT PRIVILEGES
REVOKE EXECUTE ON ROUTINES FROM PUBLIC;
```

The revoke is intentionally global for objects created by `dante_owner`; a per-schema revoke would not remove the global default PUBLIC grant.

## 10. Provisioning boundary

Role/database security provisioning is separate from Alembic because Alembic requires the migrator identity before it can run.

`dante.platform.database.provisioning` is an explicit administrative command/tool boundary, not a server startup action.

It owns:

- application role creation/reconciliation;
- membership options;
- credential assignment for login roles;
- `dante` schema creation/ownership;
- database/schema hardening;
- default privileges;
- reconciliation of existing runtime object privileges.

Normal FastAPI startup never receives the admin or migrator secret.

## 11. Real PostgreSQL acceptance harness

The CP3 PostgreSQL tests never use SQLite and never mock PostgreSQL behavior.

The harness uses the exact CP2-built image:

```text
dante-postgres-local:18.4
```

A single disposable Docker container is created for the pytest PostgreSQL session. It has its own PostgreSQL cluster, generated admin/migrator/runtime secrets and loopback-only random host port.

This is an evidence-driven correction to the initial idea of creating only ephemeral databases inside the ordinary LOCAL cluster. PostgreSQL roles are cluster-global; testing provisioning there would mutate the real LOCAL `dante_runtime` / `dante_migrator` credentials. The isolated acceptance cluster therefore guarantees:

```text
ordinary LOCAL dante database untouched
ordinary LOCAL application roles untouched
same CP2 PostgreSQL image/envelope exercised
no second PostgreSQL implementation
no container per individual test
```

Within the disposable acceptance cluster, tests create fresh databases, install the exact selected extension envelope, apply CP3 provisioning and destroy each database after use.

The readiness probe for the acceptance cluster verifies the machine-readable PostgreSQL version with `SHOW server_version_num` and requires `180004`. This avoids depending on distribution/package suffixes while still proving exact PostgreSQL 18.4.

DB outage/recovery acceptance uses `docker stop` / `docker start` on the same disposable cluster rather than `docker pause` / `docker unpause`. Stop/start represents a real dependency outage, closes live connections, preserves the same acceptance database for recovery and still leaves final unconditional container removal to the session fixture.

If the CP2 image is missing, PostgreSQL tests fail explicitly; they are not silently skipped.

### Hardening finding retained after closure

A deliberately frozen PostgreSQL peer created with `docker pause` can leave an existing TCP connection open but non-responsive. Direct QA showed that in this blackholed/frozen-peer condition the Python-level readiness timeout can be exceeded while driver cancellation/cleanup itself waits on the unreachable peer.

CP3 does **not** claim bounded wall-clock readiness for that stronger blackhole/frozen-peer scenario. It remains a separate hardening item and must not be silently converted into a CP3 PASS claim.

## 12. CP3 direct acceptance evidence — PASS

CP3 direct QA was completed on the canonical Windows 11 + WSL2/Linux + Docker Desktop workstation on 2026-08-20 against implementation/direct-QA HEAD:

```text
35cf6440bc121a38342f6bbee72e210435a788a4
```

Directly recorded evidence:

```text
DEPENDENCIES
uv lock --check                         PASS
uv tree --locked --depth 1              PASS
uv sync --locked                         PASS

QUALITY
ruff format --check .                    PASS — 23 files already formatted
ruff check .                             PASS
mypy                                    PASS — 20 source files
pytest -m "not postgres"                PASS — 32/32
pytest -m postgres                       PASS — 18/18 in 15.61s
full pytest                              PASS — 50/50 in 24.72s
full-run coverage                        97.42% evidence only; not a threshold
uv build                                 PASS
source distribution                      PASS
typed wheel                              PASS

ALEMBIC / SCHEMA
fresh database → repository head         PASS
single repository head                   PASS
head → base → head                        PASS
alembic check / no DANTE drift           PASS
public extension objects preserved       PASS

POSTGRESQL PRIVILEGES
owner NOLOGIN                             PASS
migrator explicit SET ROLE               PASS
runtime expected DML/default grants       PASS
runtime DDL/escalation denial             PASS
runtime TEMP/TRUNCATE denial              PASS
alembic_version runtime denial            PASS
object owner = dante_owner                PASS
default routine EXECUTE denial            PASS

RUNTIME / FAILURE / RECOVERY
runtime dedicated identity/search_path    PASS
pool_pre_ping stale-connection recovery   PASS
live 200 during real DB outage            PASS
ready 503 during real DB outage           PASS
ready 200 after DB restart                PASS — no backend restart
readiness response secret/detail redaction PASS
engine dispose after real use             PASS

TRANSACTIONS
autobegin=False behavior                  PASS
real commit persistence                   PASS
exception whole-transaction rollback      PASS
flush != commit                           PASS
SAVEPOINT outer-transaction preservation  PASS
```

Remote repository evidence after the executable QA:

```text
original CP3 PRE-SCOPE   a09936d168de48909d948425387b168d016911e8
implementation QA HEAD   35cf6440bc121a38342f6bbee72e210435a788a4
ahead_by                 45
behind_by                0
changed paths            27
expected paths           27
unexpected               0
deleted                  0
remote branch vs QA HEAD identical
```

The 97.42% full-run coverage is recorded only as evidence for this run. CP3 does not introduce an arbitrary permanent global coverage percentage.

CP3 is therefore:

```text
CLOSED / DIRECT QA PASS
```

## 13. Explicit non-claims

CP3 does not prove or implement:

```text
concrete Logical → PostgreSQL business schema
business repositories/adapters
business concurrency invariants
automatic deadlock/serialization retry
ambiguous commit reconciliation
transactional outbox implementation
PowerSync
PgBouncer activation
Restate
backup/PITR activation
production deployment
blackholed/frozen-peer readiness wall-clock bound
Physical HG/PSV blanket PASS
```

Those remain separate bounded work.