# Workstream — Production Backend Scaffold

- Status: **ACTIVE / CP1 CLOSED / CP2 CLOSED / CP3 CLOSED / DIRECT QA PASS / CP4 NEXT**
- Branch: `feature/backend-scaffold`
- Decision baseline PRE-SCOPE: `9f7c21857cf7a9c7300053370954c4b93f9bd96a`
- CP1 closure implementation HEAD: `02d113d772cdb247faebb3cef4d857d125266da3`
- CP2 implementation/repair HEAD before closure docs: `2d79c89d78b9031a1fe4323bbdcdb4b359fa87d6`
- CP3 original materialization PRE-SCOPE: `a09936d168de48909d948425387b168d016911e8`
- CP3 lock materialization HEAD: `17c00d2ac24d2efecfc52f7fa5f707f5b15c36cd`
- CP3 implementation/direct-QA HEAD: `35cf6440bc121a38342f6bbee72e210435a788a4`
- Product: **DANTE**
- Repository: `MattiaRubino/dante`
- Engineering Foundation v0: **CLOSED / CONSUMED / NOT REOPENED**
- Concrete Logical → PostgreSQL schema: **OUT OF SCOPE UNTIL SCAFFOLD QA**
- Detailed CP1 contract: `docs/development/backend-cp1-contract.md`
- Detailed CP2 contract: `docs/development/backend-cp2-postgres-contract.md`
- Detailed CP3 contract: `docs/development/backend-cp3-persistence-contract.md`

## 1. Purpose

This workstream turns the closed Engineering Foundation into the first real production backend scaffold.

It exists so implementation can proceed in small, directly verifiable checkpoints rather than creating the entire backend/database/CI surface in one opaque write.

The scaffold is infrastructure and application bootstrap only. It does not authorize concrete Domain/Logical persistence mapping or business vertical slices.

```text
ENGINEERING FOUNDATION v0
        CLOSED
          ↓
PRODUCTION BACKEND SCAFFOLD
        ACTIVE
          ↓
CP1 Python/backend process + typed config
        CLOSED / DIRECT QA PASS
          ↓
CP2 reproducible LOCAL PostgreSQL
        CLOSED / DIRECT QA PASS
          ↓
CP3 persistence + migrations + real PostgreSQL harness
        CLOSED / DIRECT QA PASS
          ↓
CP4 quality / CI enforcement
        NEXT
          ↓
CP5 scaffold QA / closure
          ↓
CONCRETE LOGICAL → POSTGRESQL
        NEXT WORKSTREAM BOUNDARY
```

## 2. Quality bar

DANTE targets a production-grade engineering standard suitable for a serious long-lived product and future team growth.

For this workstream, **maximum quality does not mean maximum complexity**.

The required standard is:

- explicit architecture and ownership boundaries;
- reproducible clean-machine bootstrap;
- pinned/reviewed runtime and dependency state;
- real Linux/PostgreSQL execution semantics;
- strong typing and deterministic validation;
- secure configuration and secret handling;
- migration-first schema evolution;
- tests that prove the relevant boundary rather than mocks that merely look green;
- CI checks only after the underlying command actually exists and is trustworthy;
- excellent local debugging/IDE ergonomics without IDE dependence;
- small, understandable components that can evolve without accidental coupling;
- no placeholder folders, fake abstractions or unused infrastructure merely to resemble a large-company repository.

A simpler design is preferred when it preserves the same correctness, operability, security and future migration options.

## 3. Current verified state

Repository/workstation evidence:

```text
GitHub repository                     MattiaRubino/dante
active branch                         feature/backend-scaffold
repository rename                     COMPLETE
local workspace                       /home/mattia/projects/dante

Windows 11 host                       PASS
WSL2                                  PASS
Ubuntu 24.04 LTS                      PASS
repository on Linux filesystem        PASS
Git + GitHub CLI                      PASS
uv                                    PASS
Python 3.14.7 Linux x86_64            PASS
Docker Desktop WSL2 backend           PASS
Ubuntu-24.04 Docker integration       PASS
Docker Compose                        PASS
Docker daemon access without sudo     PASS
hello-world Linux container           PASS
Docker data location on D:            PASS
```

Detailed clean-machine/onboarding instructions are in:

`docs/development/local-backend-workstation-bootstrap.md`

CP1 is materially implemented and directly validated:

```text
apps/backend production project       CREATED / REMOTE
backend virtual environment            CREATED BY uv sync
FastAPI process/bootstrap              CREATED / DIRECT STARTUP PASS
backend typed settings                 CREATED / TESTED
uv.lock                                COMMITTED / REMOTE VERIFIED
Ruff                                   DIRECT PASS
mypy strict                            DIRECT PASS
pytest                                 25/25 PASS
CP1 statement coverage                 100.00%
CP1 branch coverage                    100.00%
uv build                               PASS
real /health/live HTTP                 PASS
real /health/ready HTTP                PASS
```

CP2 is materially implemented and directly validated:

```text
DANTE PostgreSQL LOCAL image           CREATED / REMOTE / BUILD PASS
PostgreSQL                             18.4 / DIRECT PASS
PostGIS package                        3.6.4 exact / DIRECT PASS
pgvector package                       0.8.6 exact / DIRECT PASS
fresh initdb                           PASS
selected extension envelope            5/5 PASS
PostGIS capability                     PASS
pgvector capability                    PASS
pg_trgm capability                     PASS
unaccent capability                    PASS
native PostgreSQL FTS                  PASS
pg_stat_statements preload             PASS
pg_stat_statements real collection     PASS
named-volume persistence               PASS
destructive volume reset               PASS
fresh extension reinitialization       PASS
Windows DBeaver connectivity           PASS
```

CP3 is materially implemented and directly validated:

```text
SQLAlchemy/psycopg persistence         CLOSED / DIRECT QA PASS
Alembic migration harness              CLOSED / DIRECT QA PASS
real PostgreSQL integration harness    CLOSED / DIRECT QA PASS
runtime/migrator application roles     CLOSED / DIRECT QA PASS
CP3 transaction tests                  CLOSED / DIRECT QA PASS
CP3 DB outage/recovery tests           CLOSED / DIRECT QA PASS
PostgreSQL acceptance                  18/18 PASS
full backend pytest                    50/50 PASS
full-run coverage                      97.42% evidence only; not threshold
uv build                               PASS
backend CI workflows                   NOT CREATED
concrete business schema               NOT STARTED
```

## 4. Execution strategy

Do not create the complete scaffold in one undifferentiated write.

Use ordered checkpoints. Each checkpoint receives its own exact Git write gate, local direct validation and remote exact-delta QA before the next checkpoint is authorized.

```text
CP1  Python/backend process + typed config                       CLOSED / DIRECT QA PASS
 ↓
CP2  reproducible LOCAL PostgreSQL infrastructure                CLOSED / DIRECT QA PASS
 ↓
CP3  persistence + migration + real-PostgreSQL harness           CLOSED / DIRECT QA PASS
 ↓
CP4  repository quality/CI enforcement once real checks exist    NEXT
 ↓
CP5  full scaffold QA + closure/handoff
```

A checkpoint may be split further if implementation evidence shows that doing so improves reviewability or fault isolation.

## 5. CP1 — Backend Python/process/config foundation — CLOSED

### Goal

Materialize the smallest real backend project that can be installed reproducibly, started under Linux/WSL, configured through the accepted typed settings boundary and tested without yet depending on PostgreSQL.

### Detailed authority

The complete CP1 design and implementation evidence live in:

`docs/development/backend-cp1-contract.md`

That document is the authority for:

- CP1-01 dependency/version policy;
- CP1-02 `pyproject.toml`, Ruff, mypy, pytest and coverage policy;
- CP1-03 FastAPI application factory and typed Settings contract;
- the complete `DANTE_*` variable registry and meaning;
- LOCAL `.env.local` loading semantics;
- health/readiness semantics;
- OpenAPI/docs environment behavior;
- standard commands;
- test obligations;
- implementation findings and corrections;
- exact resolved dependency evidence;
- direct acceptance evidence;
- deferred-item triggers;
- permanent configuration-documentation discipline.

Do not reconstruct those decisions from conversation memory when the contract exists.

### Materialized CP1 shape

```text
apps/backend/
├── .python-version
├── pyproject.toml
├── uv.lock
├── .env.example
├── README.md
│
├── src/
│   └── dante/
│       ├── __init__.py
│       ├── bootstrap/
│       │   ├── __init__.py
│       │   └── app.py
│       └── platform/
│           ├── __init__.py
│           └── config/
│               ├── __init__.py
│               └── settings.py
│
└── tests/
    ├── test_bootstrap.py
    └── test_settings.py
```

### CP1 final state

```text
CP1-01 dependency/version policy        CLOSED / IMPLEMENTED
CP1-02 pyproject/tooling policy          CLOSED / IMPLEMENTED
CP1-03 FastAPI/settings/health policy    CLOSED / IMPLEMENTED
CP1 source/manifests                     REMOTE
CP1 uv.lock                              REMOTE / VERIFIED
CP1 direct QA                            PASS
```

Final direct project graph on 2026-08-20:

```text
fastapi             0.141.1
pydantic            2.13.4
pydantic-settings   2.15.0
uvicorn             0.52.4
httpx2               2.12.0
mypy                 2.3.1
pytest               9.1.1
pytest-cov           7.1.0
ruff                 0.16.3
```

Important evidence-driven corrections during CP1:

- Pydantic's mypy plugin was enabled after plain strict mypy produced false-positive `BaseSettings()` constructor errors;
- one narrow `type: ignore[misc]` remains only on the deliberate runtime frozen-settings mutation probe;
- `httpx` was replaced by `httpx2` after current Starlette `TestClient` behavior emitted a deprecation warning that DANTE correctly promoted to an error;
- warnings-as-errors and global mypy strictness were preserved;
- `.coverage` is ignored as a generated local artifact.

### CP1 explicitly did not create

```text
modules/ capability tree
kernel/ primitives without proven shared meaning
empty observability/security/clock/identifier layers
SQLAlchemy mappings
persistence adapters
Alembic migrations
PostgreSQL connection code
business/domain schema
business HTTP routes
backend OCI Dockerfile
PowerSync
Restate
R2
OR-Tools integration
PgBouncer runtime path
cloud/IaC/provider resources
frontend implementation
```

The accepted application structure remains the architectural target, but empty layers are not materialized for ceremony.

## 6. CP2 — Reproducible LOCAL PostgreSQL infrastructure — CLOSED

CP2 closed on 2026-08-20 after its complete approved direct acceptance contract passed on the canonical Windows 11 + WSL2 + Docker Desktop workstation.

### Detailed authority

The durable CP2 design, implementation findings, operating model and direct closure evidence live in:

`docs/development/backend-cp2-postgres-contract.md`

Do not reconstruct CP2 from chat history when that contract exists.

### Materialized CP2 shape

```text
infra/
├── local/postgres/
│   ├── Dockerfile
│   └── initdb/010-extensions.sql
└── compose/
    ├── local.yaml
    └── README.md
```

The repository also ignores the workstation-local Compose secret file through `.gitignore`.

### Final selected LOCAL database envelope

```text
Docker Compose
        ↓
DANTE-owned PostgreSQL build/config
        ↓
PostgreSQL 18.4
+ PostGIS 3.6.4
+ pgvector 0.8.6
+ pg_trgm
+ unaccent
+ pg_stat_statements preload + extension
+ native PostgreSQL FTS capability
```

Direct closure evidence includes:

```text
Compose config validation                 PASS
immutable postgres:18.4-trixie digest     PASS
clean/no-cache image build                PASS
exact PostGIS/pgvector package pins       PASS
fresh cluster init                        PASS
010-extensions.sql                        PASS
five selected extensions                  PASS
functional capability probes              PASS
pg_stat_statements actual collection      PASS
normal down/up persistence                PASS
down --volumes destructive reset          PASS
fresh post-reset reinitialization          PASS
Windows DBeaver 127.0.0.1:5432            PASS
```

The first clean build exposed a real TLS trust-store prerequisite: the pinned PostgreSQL base contained the PGDG signing key but did not have Debian `ca-certificates` installed in the final filesystem. The accepted repair installs the Debian trust store before using the PGDG historical archive over HTTPS and preserves both TLS verification and PGDG signed-repository verification. The repaired no-cache build passed directly.

PgBouncer remains selected but is not forced into every day-one LOCAL connection. Its activation belongs to the concrete pooling/compatibility validation boundary.

### CP2 final state

```text
DANTE PostgreSQL image       PASS
PostgreSQL 18.4              PASS
PostGIS 3.6.4                PASS
pgvector 0.8.6               PASS
pg_trgm                      PASS
unaccent                     PASS
pg_stat_statements           PASS
native FTS                   PASS
named-volume persistence     PASS
explicit reset               PASS
Windows GUI connectivity     PASS
CP2                          CLOSED / DIRECT QA PASS
```

CP2 does not imply application persistence, Alembic, privilege separation, Logical mapping, restore/PITR or Physical HG/PSV PASS.

## 7. CP3 — Persistence, migrations and real PostgreSQL harness — CLOSED / DIRECT QA PASS

### Detailed authority

The complete accepted CP3 design, materialized boundary and closure evidence live in:

`docs/development/backend-cp3-persistence-contract.md`

Do not reconstruct CP3 from conversation history when that contract exists.

### Accepted architecture

```text
Settings / DatabaseSettings
        ↓
one AsyncEngine per process
        ↓
one async_sessionmaker per process
        ↓
one AsyncSession per application operation/task
        ↓
explicit transaction boundary
        ↓
PostgreSQL 18.4
```

Key rules:

- `postgresql+psycopg` async SQLAlchemy boundary;
- `pool_pre_ping=True`;
- `autobegin=False`, `expire_on_commit=False`, `autoflush=True`;
- outer application operation owns commit/rollback;
- persistence adapters never commit implicitly;
- no generic `Repository[T]` / generic Unit of Work;
- liveness is process-only;
- readiness performs a bounded real PostgreSQL probe for the CP3 outage model;
- no hidden SQL/transaction retry;
- no long external/AI I/O while holding an unnecessary DB transaction.

### Alembic/schema governance

```text
application schema     dante
version table          dante.alembic_version
one canonical DAG/head
technical baseline     20260820_01
```

Alembic authenticates as `dante_migrator`, explicitly performs `SET ROLE dante_owner`, governs only the `dante` schema and does not treat `public` extension/provider objects as DANTE-owned schema.

`metadata.create_all()` is not deployment authority.

### PostgreSQL identity model

```text
dante_owner      NOLOGIN object owner
dante_migrator   LOGIN / NOINHERIT / SET dante_owner allowed / ADMIN denied
dante_runtime    LOGIN / NOINHERIT / no owner membership / DML-only posture
```

The runtime has no default DDL, TRUNCATE, TEMP, owner escalation, migration-history access or routine EXECUTE capability.

### Materialized dependency resolution

```text
SQLAlchemy       2.0.52
psycopg          3.3.4
Alembic          1.19.1
pytest-asyncio   1.4.0
```

The lock was generated directly with `uv` on the canonical WSL workstation and pushed at:

```text
17c00d2ac24d2efecfc52f7fa5f707f5b15c36cd
```

### Real PostgreSQL acceptance harness

PostgreSQL-marked tests use the exact CP2-built image:

```text
dante-postgres-local:18.4
```

They start one disposable loopback-only cluster per pytest PostgreSQL session, then create fresh provisioned/migrated databases inside that isolated cluster.

This is intentionally stronger than using the ordinary LOCAL cluster because PostgreSQL roles are cluster-global. Acceptance provisioning must not change the developer's real `dante_runtime` / `dante_migrator` credentials.

The harness therefore proves the same DANTE image/envelope while keeping the ordinary LOCAL database and roles untouched.

The cluster readiness predicate uses `SHOW server_version_num = 180004`, avoiding package/distribution suffixes while retaining an exact PostgreSQL 18.4 assertion.

Outage/recovery acceptance uses stop/start of the same disposable container. This closes live connections while preserving the database state needed to prove readiness recovery without restarting the backend process.

### CP3 final state

```text
CP3-01 stack/version design              CLOSED / MATERIALIZED / DIRECT QA PASS
CP3-02 connection/config/lifecycle       CLOSED / MATERIALIZED / DIRECT QA PASS
CP3-03 transaction architecture          CLOSED / MATERIALIZED / DIRECT QA PASS
CP3-04 Alembic/schema governance         CLOSED / MATERIALIZED / DIRECT QA PASS
CP3-05 PostgreSQL privileges             CLOSED / MATERIALIZED / DIRECT QA PASS
CP3-06 real PostgreSQL harness/matrix    CLOSED / MATERIALIZED / DIRECT QA PASS
CP3 uv.lock                              REMOTE / GENERATED BY uv / VERIFIED
CP3 direct QA                            PASS
```

No concrete Logical owner/table mapping is authorized by CP3. The technical probe objects created by tests exist only inside disposable acceptance databases and are not canonical schema.

### Direct closure evidence

Implementation/direct-QA HEAD:

```text
35cf6440bc121a38342f6bbee72e210435a788a4
```

Directly recorded on the canonical WSL/Docker workstation on 2026-08-20:

```text
uv lock --check                         PASS
uv tree --locked --depth 1              PASS
uv sync --locked                         PASS
ruff format --check .                    PASS — 23 files already formatted
ruff check .                             PASS
mypy                                    PASS — 20 source files
pytest -m "not postgres"                PASS — 32/32
pytest -m postgres                       PASS — 18/18 in 15.61s
full pytest                              PASS — 50/50 in 24.72s
full-run coverage                        97.42% evidence only; not threshold
uv build                                 PASS
sdist + wheel                            PASS
fresh DB → Alembic head                  PASS
head → base → head                       PASS
alembic check / no DANTE drift           PASS
privilege allow/deny matrix              PASS
runtime identity/search_path             PASS
stale pooled-connection recovery         PASS
real DB outage live 200 / ready 503      PASS
DB recovery ready 200, no app restart    PASS
commit / rollback / flush / SAVEPOINT    PASS
```

Remote exact-scope QA from the original CP3 PRE-SCOPE to the executable QA HEAD:

```text
PRE-SCOPE       a09936d168de48909d948425387b168d016911e8
QA HEAD         35cf6440bc121a38342f6bbee72e210435a788a4
ahead_by        45
behind_by       0
changed paths   27
expected paths  27
unexpected      0
deleted         0
```

The 97.42% coverage figure is run evidence, not a permanent arbitrary project threshold.

### Evidence-driven hardening finding

`docker pause` was directly shown to represent a stronger frozen/blackholed-peer condition: TCP may remain open while PostgreSQL cannot respond, and driver cancellation/cleanup may exceed the Python-level readiness timeout.

CP3 therefore does not claim a bounded wall-clock readiness result for a frozen/blackholed peer. That stronger scenario remains a separate hardening item; it is not hidden by the accepted stop/start outage test.

## 8. CP4 — Quality, architecture and CI enforcement

CI is introduced after the commands it runs are real and stable.

Expected classes as applicable:

- frozen/locked dependency bootstrap;
- Ruff format check/lint;
- mypy strict;
- pytest backend tests;
- architecture dependency checks once a meaningful package graph exists;
- real PostgreSQL integration/migration checks;
- repository text/line-ending normalization required by the scaffold;
- GitHub Actions with explicit least-privilege permissions;
- third-party and, where practical, official Actions pinned to immutable full SHAs;
- no deployment/PROD identity in ordinary PR validation.

No GitHub check becomes required on protected `main` until its real emitted context has run remotely, its name is stable and a deliberate failure is confirmed to block the merge correctly.

CodeQL/dependency/security automation activates only when the corresponding real source/manifest/capability exists and current GitHub support is verified.

## 9. CP5 — Scaffold QA and closure

Before the scaffold workstream can close, directly prove at minimum:

```text
exact changed paths                            PASS
clean locked backend dependency bootstrap      PASS
Python 3.14.7 project interpreter              PASS
backend process starts under Linux/WSL         PASS
typed config tests                             PASS
Ruff/mypy/pytest actual commands                PASS
DANTE PostgreSQL image builds                  PASS
PostgreSQL 18.4 starts/health                   PASS
selected extension envelope                    PASS
pg_stat_statements preload/extension            PASS
basic psycopg/SQLAlchemy async connection       PASS
Alembic base → head                             PASS
real PostgreSQL integration harness             PASS
initial CI emitted contexts observed remotely   PASS where activated
```

Do not convert this into false blanket validation. Direct Physical HG/PSV obligations remain NOT RUN unless the specific required scenario is actually exercised.

After CP5 closure, the next bounded scope is concrete Logical → PostgreSQL implementation.

## 10. Persistent non-goals for this workstream

Until explicitly reopened by a later boundary, do not add:

- concrete 57-owner table mapping;
- business capability modules merely to reserve names;
- product HTTP/API surface;
- AuthN/AuthZ implementation;
- frontend internals/toolchain;
- cloud provider/IaC engine;
- DEV/UAT/PROD infrastructure;
- PowerSync implementation;
- Restate activation;
- R2 implementation;
- OR-Tools implementation;
- pgBackRest/AWS recovery activation;
- production deployment pipeline;
- event sourcing, Redis, Kafka or other already-excluded infrastructure by convenience.

## 11. Exact resume point for the next chat

A new conversation must not redesign Engineering Foundation, repeat CP1/CP2 work, redesign CP3-01..CP3-06 or jump directly into concrete PostgreSQL business schema mapping.

Resume in this exact order:

```text
1. Read current project truth, this handoff and backend-cp3-persistence-contract.md.
2. Verify feature/backend-scaffold, remote/local HEAD and clean tree.
3. Treat CP1, CP2 and CP3 as CLOSED / DIRECT QA PASS.
4. Preserve CP3 implementation/direct-QA HEAD 35cf6440bc121a38342f6bbee72e210435a788a4 as executable closure evidence.
5. Begin CP4 quality/architecture/CI enforcement as a new bounded checkpoint.
6. First inspect the real repository checks/workflows/protected-main state and current GitHub support before selecting CP4 writes.
7. Define the CP4 command/check matrix only from commands already proven real and stable.
8. Open a new exact Git write gate before any CP4 mutation.
9. Do not make a GitHub check required until its real remote context has emitted, its name is stable and a deliberate failure is confirmed to block correctly.
10. After CP4 direct QA, proceed to CP5 full scaffold QA/closure.
11. Keep concrete Logical → PostgreSQL owner/table mapping deferred until scaffold closure.
```

### Immediate next action

**Begin CP4 read-only inspection/design. Do not create CI workflows or change protected-main requirements until the CP4 gate is explicitly approved.**