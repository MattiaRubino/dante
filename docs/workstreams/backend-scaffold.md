# Workstream — Production Backend Scaffold

- Status: **ACTIVE / CP1 CLOSED / CP2 NEXT**
- Branch: `feature/backend-scaffold`
- Decision baseline PRE-SCOPE: `9f7c21857cf7a9c7300053370954c4b93f9bd96a`
- CP1 closure implementation HEAD: `02d113d772cdb247faebb3cef4d857d125266da3`
- Product: **DANTE**
- Repository: `MattiaRubino/dante`
- Engineering Foundation v0: **CLOSED / CONSUMED / NOT REOPENED**
- Concrete Logical → PostgreSQL schema: **OUT OF SCOPE UNTIL SCAFFOLD QA**
- Detailed CP1 contract: `docs/development/backend-cp1-contract.md`

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
        NEXT
          ↓
CP3 persistence + migrations + real PostgreSQL harness
          ↓
CP4 quality / CI enforcement
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

CP1 is now materially implemented and directly validated:

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

Still not implemented:

```text
PostgreSQL 18.4 LOCAL image            NOT CREATED
selected extension envelope            NOT DIRECTLY VERIFIED
SQLAlchemy/psycopg persistence         NOT CREATED
Alembic migration harness              NOT CREATED
real PostgreSQL integration harness    NOT CREATED
backend CI workflows                   NOT CREATED
concrete business schema               NOT STARTED
```

## 4. Execution strategy

Do not create the complete scaffold in one undifferentiated write.

Use ordered checkpoints. Each checkpoint receives its own exact Git write gate, local direct validation and remote exact-delta QA before the next checkpoint is authorized.

```text
CP1  Python/backend process + typed config                       CLOSED / PASS
 ↓
CP2  reproducible LOCAL PostgreSQL infrastructure                NEXT
 ↓
CP3  persistence + migration + real-PostgreSQL harness
 ↓
CP4  repository quality/CI enforcement once real checks exist
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

## 6. CP2 — Reproducible LOCAL PostgreSQL infrastructure — NEXT

CP2 is now the active next checkpoint because CP1 direct QA has passed and its lockfile is remotely verified.

Goal:

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

Requirements:

- explicit/pinned component versions;
- trusted PostgreSQL 18.4 base;
- DANTE-owned reproducible build rather than an unpinned generic all-extensions image;
- Linux container semantics;
- deterministic initialization/bootstrap;
- DANTE-scoped resource names;
- synthetic LOCAL credentials only;
- health check;
- persistent LOCAL data through a Docker-managed volume unless an explicitly disposable test database is being used;
- explicit reset/destruction procedure;
- no production credentials;
- host connection suitable for DBeaver/PyCharm Database Tools over the published LOCAL port;
- extension installation, activation and version/capability queries directly verified;
- `pg_stat_statements` preload configuration directly verified.

Likely ownership boundary from the closed repository layout:

```text
infra/local/postgres/
infra/compose/
```

Exact files, image base, extension installation strategy, compose topology, volume naming, ports, credentials and initialization semantics must be researched/reviewed before the CP2 write gate rather than guessed here.

PgBouncer remains selected but is not forced into every day-one LOCAL connection. Its activation belongs to the concrete pooling/compatibility validation boundary.

## 7. CP3 — Persistence, migrations and real PostgreSQL harness

CP3 starts only after the DANTE PostgreSQL image/environment is directly operational.

It introduces the first real technical persistence boundary using the accepted stack:

```text
SQLAlchemy 2.0 stable line
psycopg 3
async DB I/O boundary
Alembic migration authority
```

Expected responsibilities include, once exact design is approved:

- typed DB configuration;
- async engine/session lifecycle;
- one `AsyncSession` per use-case/task scope;
- no global/shared concurrent session;
- transaction ownership at application/use-case boundary;
- Alembic environment/bootstrap;
- clean database base → head migration proof;
- real PostgreSQL connection/integration test;
- migration/drift harness suitable for future schema work;
- runtime/migrator privilege separation where the concrete harness activates those identities.

No concrete Logical owner/table mapping is authorized by CP3. An empty/technical migration baseline may exist only if it is the cleanest truthful way to prove the migration machinery.

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

A new conversation must not redesign Engineering Foundation, repeat CP1 implementation work or jump directly into PostgreSQL/schema code.

Resume in this exact order:

```text
1. Read current project truth, this handoff, and `docs/development/backend-cp1-contract.md`.
2. Verify `feature/backend-scaffold`, current remote/local HEAD and clean tree.
3. Treat CP1 as CLOSED / DIRECT QA PASS; do not reopen it without concrete evidence.
4. Start CP2 READ-ONLY design/research for reproducible LOCAL PostgreSQL infrastructure.
5. Re-check current official source/version evidence for PostgreSQL 18.4, PostGIS 3.6.4, pgvector 0.8.6 and the selected built-in extensions.
6. Decide the DANTE-owned image/build strategy, extension installation path, Compose topology, volume/persistence semantics, healthcheck, port and synthetic LOCAL credential model.
7. Define direct CP2 acceptance evidence, including persistence across container recreation/restart and host GUI connectivity.
8. Present a fresh exact CP2 Git write gate before creating any PostgreSQL/Compose file.
9. Only after explicit approval, materialize CP2 and run direct validation.
10. Proceed to CP3 only after CP2 PASS.
```

### Immediate next action

**Begin CP2 READ-ONLY design/research. No PostgreSQL/Compose repository write is authorized by this handoff alone.**
