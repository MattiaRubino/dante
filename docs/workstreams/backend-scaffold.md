# Workstream — Production Backend Scaffold

- Status: **ACTIVE / CHECKPOINT PLAN APPROVED / IMPLEMENTATION NOT STARTED**
- Branch: `feature/backend-scaffold`
- Decision baseline PRE-SCOPE: `9f7c21857cf7a9c7300053370954c4b93f9bd96a`
- Product: **DANTE**
- Repository: `MattiaRubino/dante`
- Engineering Foundation v0: **CLOSED / CONSUMED / NOT REOPENED**
- Concrete Logical → PostgreSQL schema: **OUT OF SCOPE UNTIL SCAFFOLD QA**

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
SCAFFOLD QA
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

## 3. Current verified starting state

Repository/workstation evidence already completed before scaffold implementation:

```text
GitHub repository                     MattiaRubino/dante
active branch                         feature/backend-scaffold
repository rename                     COMPLETE
local workspace                       /home/mattia/projects/dante
local/remote branch sync              PASS at decision baseline
working tree                          CLEAN at decision baseline

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

Still not implemented:

```text
apps/backend production project       NOT CREATED
backend virtual environment            NOT CREATED BY REPOSITORY SCAFFOLD
FastAPI process/bootstrap              NOT CREATED
backend typed settings                 NOT CREATED
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
CP1  Python/backend process + typed config
 ↓
CP2  reproducible LOCAL PostgreSQL infrastructure
 ↓
CP3  persistence + migration + real-PostgreSQL harness
 ↓
CP4  repository quality/CI enforcement once real checks exist
 ↓
CP5  full scaffold QA + closure/handoff
```

A checkpoint may be split further if implementation evidence shows that doing so improves reviewability or fault isolation.

## 5. CP1 — Backend Python/process/config foundation — APPROVED DESIGN

### Goal

Materialize the smallest real backend project that can be installed reproducibly, started under Linux/WSL, configured through the accepted typed settings boundary and tested without yet depending on PostgreSQL.

### Approved target shape

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
│           └── config/
│               ├── __init__.py
│               └── settings.py
│
└── tests/
    ├── test_bootstrap.py
    └── test_settings.py
```

The exact file set remains subject to the CP1 write gate. A file is removed from the gate if implementation research shows it has no real purpose; additional files require explicit discussion/gate expansion.

### CP1 runtime/tool intent

Already accepted by Engineering Foundation:

```text
Python supported line       3.14.x
initial interpreter pin     3.14.7
package/environment manager uv
FastAPI                     inbound HTTP/process host
pydantic-settings           typed configuration boundary
Ruff                        format/lint
mypy                        strict baseline
pytest                      test runner
Hypothesis                  available where meaningful
```

**Exact package versions are not yet approved.**

Before `pyproject.toml` is written, re-check current primary/official sources for compatibility with Python 3.14.7 and with each other. Resolve/pin the actual graph through `uv`; never hand-edit `uv.lock`.

### CP1 behavior

CP1 should prove only real bootstrap concerns:

- package imports through src layout;
- FastAPI application can be constructed and started;
- a minimal technical smoke/health surface can prove process bootstrap without becoming a premature product API contract;
- settings use `pydantic-settings`;
- environment identity is typed/closed;
- required/invalid settings fail fast where applicable;
- settings are treated as immutable runtime state;
- secret-bearing values are not exposed through unsafe representations/logging;
- `.env.example` is safe and contains no real secret;
- routine format/lint/type/test commands are documented and CLI-capable.

### CP1 test posture

Create tests only for behavior that actually exists.

`pytest` tests should cover application construction/smoke and settings validation.

Hypothesis may be installed/declared as part of the accepted backend testing baseline, but **do not manufacture a meaningless property test** merely to prove that Hypothesis is present. Its first real use appears when a meaningful invariant/state space exists.

### CP1 explicitly does not create

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

## 6. CP2 — Reproducible LOCAL PostgreSQL infrastructure

CP2 starts only after CP1 direct QA passes.

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
- disposable local state unless explicitly documented otherwise;
- no production credentials;
- extension installation, activation and version/capability queries directly verified;
- `pg_stat_statements` preload configuration directly verified.

Likely ownership boundary from the closed repository layout:

```text
infra/local/postgres/
infra/compose/
```

Exact files/config/init strategy are decided before the CP2 write gate rather than guessed here.

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

A new conversation must not redesign Engineering Foundation or jump directly into PostgreSQL/schema code.

Resume in this exact order:

```text
1. Read current project truth and this workstream handoff.
2. Verify Git branch/HEAD/local clean state.
3. CP1 is the active approved design boundary; no CP1 files exist yet.
4. Research current official package releases and Python 3.14.7 compatibility for the CP1/backend stack.
5. Decide exact dependency/version ranges/pins and pyproject/tool configuration.
6. Present the exact CP1 Git write gate.
7. Only after approval, materialize CP1.
8. Run local direct QA + remote exact-delta QA.
9. Proceed to CP2 only after CP1 PASS.
```

### Immediate next action

**Research/version-selection only. No scaffold write is authorized by this handoff itself.**

Check current primary/official sources for at least:

- FastAPI;
- Pydantic;
- pydantic-settings;
- Ruff;
- mypy;
- pytest;
- Hypothesis;
- SQLAlchemy;
- psycopg;
- Alembic;
- relevant Python 3.14 compatibility constraints.

CP1 only needs the dependencies it truly exercises; persistence dependencies can be locked at CP3 if delaying them improves clarity and avoids unused packages. Decide this explicitly from current compatibility/evolution evidence rather than assuming all Foundation-selected libraries belong in the first manifest commit.
