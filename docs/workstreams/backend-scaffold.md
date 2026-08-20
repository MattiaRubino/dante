# Workstream — Production Backend Scaffold

- Status: **ACTIVE / CP1 CLOSED / CP2 CLOSED / CP3 NEXT**
- Branch: `feature/backend-scaffold`
- Decision baseline PRE-SCOPE: `9f7c21857cf7a9c7300053370954c4b93f9bd96a`
- CP1 closure implementation HEAD: `02d113d772cdb247faebb3cef4d857d125266da3`
- CP2 implementation/repair HEAD before closure docs: `2d79c89d78b9031a1fe4323bbdcdb4b359fa87d6`
- Product: **DANTE**
- Repository: `MattiaRubino/dante`
- Engineering Foundation v0: **CLOSED / CONSUMED / NOT REOPENED**
- Concrete Logical → PostgreSQL schema: **OUT OF SCOPE UNTIL SCAFFOLD QA**
- Detailed CP1 contract: `docs/development/backend-cp1-contract.md`
- Detailed CP2 contract: `docs/development/backend-cp2-postgres-contract.md`

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
        NEXT
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

Still not implemented:

```text
SQLAlchemy/psycopg persistence         NOT CREATED
Alembic migration harness              NOT CREATED
real PostgreSQL integration harness    NOT CREATED
runtime/migrator application roles     NOT CREATED
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
CP3  persistence + migration + real-PostgreSQL harness           NEXT
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

## 7. CP3 — Persistence, migrations and real PostgreSQL harness — NEXT

CP3 is the active next checkpoint now that the DANTE PostgreSQL image/environment is directly operational.

It introduces the first real technical persistence boundary using the accepted stack:

```text
SQLAlchemy 2.x stable line
psycopg 3
async DB I/O boundary
Alembic migration authority
```

Expected responsibilities include, once exact current design/version research is approved:

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

CP3 requires its own READ-ONLY design/research, exact decisions and exact Git write gate before implementation.

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

A new conversation must not redesign Engineering Foundation, repeat CP1/CP2 implementation work or jump directly into concrete PostgreSQL schema mapping.

Resume in this exact order:

```text
1. Read current project truth, this handoff, `backend-cp1-contract.md` and `backend-cp2-postgres-contract.md`.
2. Verify `feature/backend-scaffold`, current remote/local HEAD and clean tree.
3. Treat CP1 and CP2 as CLOSED / DIRECT QA PASS unless new concrete evidence contradicts them.
4. Start CP3 READ-ONLY design/research for persistence, migrations and the real PostgreSQL harness.
5. Re-check current official version/compatibility evidence for SQLAlchemy 2.x, psycopg 3 and Alembic.
6. Decide typed DB configuration, async engine/session lifecycle, transaction ownership, migration authority and test-database lifecycle.
7. Decide the minimum real runtime/migrator privilege split that CP3 can honestly exercise.
8. Define direct CP3 acceptance evidence, including clean base → head migration and real PostgreSQL integration.
9. Present a fresh exact CP3 Git write gate before any CP3 repository write.
10. Only after explicit approval, materialize CP3 and run direct validation.
11. Proceed to CP4 only after CP3 PASS.
12. Keep concrete Logical → PostgreSQL owner/table mapping deferred until scaffold closure.
```

### Immediate next action

**Begin CP3 READ-ONLY design/research. No CP3 repository write is authorized by this handoff alone.**
