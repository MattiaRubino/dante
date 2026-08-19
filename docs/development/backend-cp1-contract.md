# Backend CP1 Technical Contract

- Status: **APPROVED DESIGN / IMPLEMENTATION NOT STARTED**
- Workstream: `docs/workstreams/backend-scaffold.md`
- Branch: `feature/backend-scaffold`
- Product: **DANTE**
- Repository: `MattiaRubino/dante`
- Contract checkpoint: **CP1-01 + CP1-02 + CP1-03 APPROVED**
- Version/source verification date: **2026-08-19**
- Implementation authority: **NO CP1 FILE WRITE IS AUTHORIZED BY THIS DOCUMENT ALONE**

## 1. Purpose

This document is the durable technical contract for **CP1 — Backend Python/process/config foundation**.

It exists so a future developer, reviewer or conversation can answer, without reconstructing chat history:

- what CP1 is trying to prove;
- why each dependency exists;
- what version policy is used;
- why the Python distribution name and import namespace differ;
- what each `DANTE_*` variable means;
- which component consumes each variable;
- which values are allowed or forbidden;
- how LOCAL dotenv loading works;
- why remote environments do not depend on `.env.local`;
- how the FastAPI process is created;
- what health/readiness mean at CP1;
- why there is no lifespan/database/wiring layer yet;
- which lint/type/test/coverage policies are enforced;
- which commands must work;
- which tests must exist before CP1 can pass;
- what is deliberately deferred and at which trigger it returns.

The Engineering Foundation remains the parent architecture authority. This file specializes that accepted baseline for CP1; it does not reopen Domain, Logical or Physical design.

## 2. Quality rule

DANTE targets a production-grade, long-lived engineering standard suitable for future team growth.

For CP1:

```text
MAXIMUM QUALITY
!= MAXIMUM NUMBER OF FILES
!= MAXIMUM NUMBER OF ABSTRACTIONS
!= MAXIMUM NUMBER OF TOOLS
```

The quality target is instead:

- explicit responsibilities;
- reproducibility;
- strong static and runtime validation;
- secure configuration defaults;
- deterministic tests;
- observable failure at the correct boundary;
- simple local debugging;
- clean future migration paths;
- no accidental framework lock-in beyond accepted boundaries;
- no unused infrastructure or ceremonial architecture.

If two designs provide equal correctness, security, operability and future evolution, prefer the simpler one.

## 3. CP1 scope

CP1 materializes the smallest real DANTE backend project that can:

1. resolve/install from a committed manifest and lockfile;
2. run under the accepted Python 3.14.7 Linux/WSL environment;
3. import as an installed `src`-layout Python package;
4. create and run a FastAPI process through an application factory;
5. validate typed bootstrap configuration before accepting work;
6. expose only technical process health/readiness probes;
7. run real format/lint/type/test/build commands;
8. prove the above through automated tests.

CP1 does **not** require PostgreSQL. PostgreSQL starts at CP2 and application persistence at CP3.

### Approved target tree

```text
apps/backend/
├── .python-version
├── .env.example
├── pyproject.toml
├── uv.lock
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

The exact implementation write gate is still required before these files are created.

## 4. CP1-01 — dependency and version contract

### 4.1 Runtime line

```text
SUPPORTED PYTHON LINE    3.14.x
INITIAL EXACT PIN        3.14.7
PROJECT MANAGER          uv
LOCKFILE                 apps/backend/uv.lock — COMMITTED
```

`apps/backend/.python-version` records `3.14.7`.

Ubuntu's system Python is not replaced. DANTE project Python remains uv-managed.

### 4.2 Version authority model

DANTE deliberately separates:

```text
pyproject.toml
= accepted compatibility envelope / dependency intent

uv.lock
= exact resolved dependency graph for reproducible installation
```

Rules:

- do not fill `pyproject.toml` with `==` pins merely to duplicate the lockfile;
- use bounded compatible ranges in the manifest;
- commit `uv.lock`;
- never hand-edit `uv.lock`;
- use `uv` to resolve/update the graph;
- upgrades are explicit reviewed changes;
- CI/local verification uses locked/frozen behavior;
- prereleases are not selected unless separately reviewed and approved;
- a new package release appearing upstream must not silently change an already-locked DANTE checkout.

### 4.3 CP1 runtime dependencies

Approved manifest envelope as of the 2026-08-19 source verification:

```toml
[project]
dependencies = [
    "fastapi>=0.141.1,<0.142",
    "pydantic>=2.13.4,<3",
    "pydantic-settings>=2.15.0,<3",
    "uvicorn[standard]>=0.52.1,<0.53",
]
```

Responsibilities:

| Dependency | Why it is direct | CP1 role |
|---|---|---|
| `fastapi` | DANTE imports and constructs the inbound HTTP/process host directly | application factory + technical health routes |
| `pydantic` | DANTE uses Pydantic validation primitives directly in the settings boundary | validation/cross-field rules |
| `pydantic-settings` | accepted Foundation configuration boundary | process-environment → typed immutable settings |
| `uvicorn[standard]` | accepted ASGI server for local process execution; `standard` provides the normal optimized/reload extras where supported | actual LOCAL server + reload workflow |

Do **not** use `fastapi[standard]` in CP1. The FastAPI standard bundle includes optional capabilities not currently exercised by DANTE, including template/form/email/CLI/cloud-related surface. CP1 keeps direct dependencies explicit and bounded to real responsibilities.

`uvicorn[standard]` is accepted because the server itself is exercised immediately and its standard extras include the supported file-watching/performance dependencies. Python 3.14 compatibility of relevant Linux extras such as `uvloop`/`watchfiles` was checked during the CP1 research boundary and is still validated by the actual `uv` resolution on the DANTE workstation.

### 4.4 Quality dependencies

```toml
[dependency-groups]
quality = [
    "ruff>=0.16.2,<0.17",
    "mypy>=2.3.0,<3",
]
```

Important research correction frozen here:

```text
Ruff verified stable on 2026-08-19     0.16.2
mypy verified stable on 2026-08-19     2.3.0
```

Do not use nonexistent/unverified floors such as `ruff>=0.16.3` or `mypy>=2.3.1` merely because they appeared in an earlier transient discussion. Future higher versions may of course be adopted through the normal explicit upgrade workflow after they actually exist and are reviewed.

### 4.5 Test dependencies

```toml
[dependency-groups]
test = [
    "pytest>=9.1.1,<10",
    "httpx>=0.28.1,<0.29",
    "pytest-cov>=7.1.0,<8",
]
```

Responsibilities:

| Dependency | Why it exists |
|---|---|
| `pytest` | canonical backend test runner |
| `httpx` | FastAPI/Starlette `TestClient` transport dependency; CP1 tests real ASGI routing rather than directly calling route functions |
| `pytest-cov` | coverage measurement from the first real backend tests |

HTTPX `1.0.dev*` prereleases are explicitly excluded from CP1.

### 4.6 Developer aggregate group

```toml
[dependency-groups]
dev = [
    { include-group = "quality" },
    { include-group = "test" },
]
```

The aggregate exists for developer convenience without duplicating package declarations.

### 4.7 Hypothesis posture

Hypothesis remains an accepted backend testing tool but is deliberately **not a CP1 dependency**.

```text
TOOL SELECTED                 YES
CP1 INSTALL                   NO
FIRST ACTIVATION              first meaningful property/invariant/state-space test
PLACEHOLDER PROPERTY TEST     FORBIDDEN
```

At activation, its then-current stable version and Python compatibility are reverified rather than freezing a stale version now.

### 4.8 Persistence packages

Do not install in CP1:

```text
SQLAlchemy
psycopg
Alembic
```

They remain selected by Engineering Foundation and return at CP3, after CP2 has produced a directly working DANTE PostgreSQL environment.

Their exact current versions are reverified at CP3. Avoid carrying unused persistence dependencies through CP1 merely because they are known future choices.

## 5. CP1-02 — package/build metadata contract

### 5.1 Distribution name vs import namespace

```text
PYTHON DISTRIBUTION / PROJECT NAME    dante-backend
PYTHON IMPORT NAMESPACE               dante
SOURCE ROOT                           src/dante
```

The distinction is intentional:

- `dante-backend` describes the installable backend application artifact;
- `dante` is the canonical Python namespace;
- the HTTP API is only one adapter, so the package is not named `api`;
- there is no second Python project yet, so no root uv workspace is created.

### 5.2 Initial application package version

```text
0.1.0
```

This is packaging metadata, **not production release identity**.

Operational release identity remains separate:

```text
DANTE_RELEASE_SHA
DANTE_BUILD_ID
future OCI digest
```

Do not introduce Git-derived dynamic versioning/setuptools-scm/hatch-vcs merely to manufacture a version number at CP1.

### 5.3 Build backend

Approved:

```toml
[build-system]
requires = ["uv_build>=0.12.5,<0.13"]
build-backend = "uv_build"

[tool.uv.build-backend]
module-name = "dante"
```

Why:

- the backend is pure Python at CP1;
- uv's native build backend is designed for `src/` projects and validates project structure/metadata;
- `dante-backend` would otherwise normalize to the module name `dante_backend`, which is not the accepted DANTE namespace;
- explicit `module-name = "dante"` preserves `src/dante` intentionally;
- the upper bound follows uv's build-backend compatibility/versioning recommendation.

### 5.4 Accidental PyPI publication barrier

Approved project classifier:

```toml
classifiers = [
    "Private :: Do Not Upload",
]
```

Purpose: make PyPI reject accidental publication of the internal backend distribution. This is a safety barrier, not a substitute for credential/repository controls.

### 5.5 Planned project metadata skeleton

```toml
[project]
name = "dante-backend"
version = "0.1.0"
description = "DANTE production backend"
readme = "README.md"
requires-python = ">=3.14,<3.15"
classifiers = [
    "Private :: Do Not Upload",
]
dependencies = [
    "fastapi>=0.141.1,<0.142",
    "pydantic>=2.13.4,<3",
    "pydantic-settings>=2.15.0,<3",
    "uvicorn[standard]>=0.52.1,<0.53",
]

[build-system]
requires = ["uv_build>=0.12.5,<0.13"]
build-backend = "uv_build"

[tool.uv.build-backend]
module-name = "dante"
```

This is the approved design target. `uv` still performs the real resolution and generates the authoritative lockfile during implementation.

## 6. Ruff contract

### 6.1 Baseline

```toml
[tool.ruff]
target-version = "py314"
line-length = 100
src = ["src"]
```

Reasons:

- DANTE intentionally targets Python 3.14 syntax/semantics;
- a 100-character line is a deliberate readability compromise for modern typed Python without making code excessively wide;
- `src = ["src"]` helps Ruff classify DANTE imports as first-party.

### 6.2 Lint families

Approved stable high-signal baseline:

```toml
[tool.ruff.lint]
select = [
    "A",
    "ASYNC",
    "B",
    "BLE",
    "C4",
    "DTZ",
    "E4",
    "E7",
    "E9",
    "F",
    "G",
    "I",
    "LOG",
    "N",
    "PERF",
    "PIE",
    "PT",
    "PTH",
    "RET",
    "RUF",
    "S",
    "SIM",
    "T20",
    "UP",
]

[tool.ruff.lint.per-file-ignores]
"tests/**/*.py" = [
    "S101",
]
```

Intent by family:

- `A`: avoid accidental shadowing of Python builtins;
- `ASYNC`: catch common async misuse;
- `B`: bugbear correctness traps;
- `BLE`: discourage blind/broad exception handling;
- `C4`: clearer/correct comprehensions;
- `DTZ`: timezone-aware datetime discipline;
- `E4/E7/E9` + `F`: core pycodestyle/Pyflakes correctness;
- `G/LOG`: safer/correct logging usage;
- `I`: deterministic import ordering;
- `N`: naming consistency;
- `PERF`: obvious avoidable Python performance traps;
- `PIE`: miscellaneous correctness/simplification checks;
- `PT`: pytest-specific correctness/style;
- `PTH`: prefer pathlib-style path operations;
- `RET`: clearer return-flow correctness;
- `RUF`: Ruff-native correctness checks;
- `S`: security-adjacent static checks;
- `SIM`: simplification where semantics stay clear;
- `T20`: prevent stray `print`/`pprint` in production code;
- `UP`: keep syntax aligned with the Python 3.14 target.

`S101` is ignored only in tests because ordinary `assert` is the canonical pytest assertion mechanism.

### 6.3 Explicit Ruff non-decisions

Do not enable at CP1:

```text
ALL
preview rules
unsafe automatic fixes in CI
ANN as a duplicate type-enforcement system
TC/type-checking import movement before the concrete Pydantic/SQLAlchemy graph exists
```

Mypy owns the primary static typing policy. Ruff complements it instead of duplicating every annotation rule.

## 7. mypy contract

Approved baseline:

```toml
[tool.mypy]
python_version = "3.14"
strict = true
warn_unreachable = true
show_error_codes = true
show_column_numbers = true
pretty = true
files = [
    "src",
    "tests",
]
enable_error_code = [
    "explicit-override",
    "exhaustive-match",
]
```

Rationale:

- `strict` is the global baseline; do not weaken it globally to accommodate one adapter/library;
- `warn_unreachable` surfaces impossible/dead branches;
- error codes make narrow exceptions auditable;
- `explicit-override` requires deliberate override intent as inheritance appears;
- `exhaustive-match` is valuable for DANTE's closed enums/state families and prevents silent omission of newly introduced cases;
- tests are type-checked too.

### Pydantic mypy plugin

```text
CP1 DEFAULT    OFF
```

Pydantic supports ordinary mypy usage without the plugin. Start with standard mypy strict behavior. Introduce `pydantic.mypy` only if direct CP1/next-scope evidence shows a concrete benefit that outweighs plugin-specific coupling.

A third-party typing weakness is handled with the narrowest justified adapter/path exception, never by lowering global strictness.

## 8. pytest and coverage contract

### 8.1 Pytest native TOML configuration

Pytest 9 supports native TOML configuration in `[tool.pytest]`.

Approved target:

```toml
[tool.pytest]
minversion = "9.1"
testpaths = [
    "tests",
]
addopts = [
    "-ra",
    "--import-mode=importlib",
    "--cov=dante",
    "--cov-report=term-missing",
]
strict = true
filterwarnings = [
    "error",
]
```

Reasons:

- `--import-mode=importlib` is the recommended modern mode for new pytest projects and avoids mutating `sys.path` merely to make the source tree importable;
- tests therefore exercise the installed `src`-layout package rather than relying on repository-root path accidents;
- strict mode activates pytest's strict configuration/markers/parameter-id/xfail behavior and future strictness additions will arrive only through explicit pytest lock upgrades;
- warnings are defects by default at this boundary;
- if a dependency produces an unavoidable warning, add only a narrow documented filter for that exact warning after direct evidence.

### 8.2 Coverage

Approved target:

```toml
[tool.coverage.run]
branch = true
source = [
    "dante",
]
relative_files = true

[tool.coverage.report]
show_missing = true
precision = 2
```

Policy:

```text
statement coverage measured       YES
branch coverage measured          YES
missing lines shown               YES
coverage percentage threshold     NO at CP1
```

No arbitrary `80%`, `90%` or `100%` gate is invented before a meaningful application denominator exists. Critical behavior is required to have direct tests regardless of percentage.

A threshold may be introduced later from measured reality and explicit risk policy; once introduced it is not silently lowered to make CI green.

## 9. CP1-03 — configuration model

### 9.1 Configuration authority

The backend bootstrap boundary uses `pydantic-settings`.

CP1 creates one small immutable `Settings` object at process/application construction.

Do not create:

- a mutable global settings singleton;
- scattered `os.getenv()` calls throughout production code;
- business/domain configuration in environment variables;
- a service locator;
- repeated Settings construction per request.

### 9.2 CP1 environment-variable registry

Every CP1 variable is listed below. This registry is part of the contract.

| External variable | Internal setting | Required | Secret | CP1 meaning | Consumer |
|---|---|---:|---:|---|---|
| `DANTE_ENV` | `env` | YES | NO | promotion/runtime identity: `local`, `dev`, `uat`, `prod` | bootstrap/config + environment-derived HTTP host behavior |
| `DANTE_RELEASE_SHA` | `release_sha` | YES | NO | source/release identity associated with the running build; `local` marker allowed only in LOCAL | bootstrap metadata; future observability/release evidence |
| `DANTE_BUILD_ID` | `build_id` | YES | NO | build/execution identity associated with the artifact/process; `local` marker allowed only in LOCAL | bootstrap metadata; future observability/release evidence |
| `DANTE_DEBUG` | `debug` | NO | NO | FastAPI/application debug behavior only | `FastAPI(debug=...)`; never Uvicorn reload/workers |

### 9.3 `DANTE_ENV`

Allowed values exactly at semantic level:

```text
local
dev
uat
prod
```

Represent with a closed Python `StrEnum` (or equivalently strict closed enum semantics):

```text
Environment.LOCAL
Environment.DEV
Environment.UAT
Environment.PROD
```

Unknown values fail bootstrap before the application accepts work.

`TEST` is not a fifth promotion environment. Automated tests construct/override a valid environment context explicitly.

### 9.4 `DANTE_RELEASE_SHA`

Required in every environment.

LOCAL accepted marker:

```text
local
```

DEV/UAT/PROD:

- must be non-empty after whitespace normalization;
- must not use the `local` marker;
- exact future artifact/Git-SHA format enforcement is deferred until the real release/artifact pipeline exists;
- do not expose this value automatically through public/health endpoints.

The name is inherited from the accepted Foundation config contract. It is not the Python package version.

### 9.5 `DANTE_BUILD_ID`

Required in every environment.

LOCAL accepted marker:

```text
local
```

DEV/UAT/PROD:

- must be non-empty after whitespace normalization;
- must not use the `local` marker;
- provider/CI-specific format is intentionally deferred until the build pipeline exists;
- do not expose it automatically through public/health endpoints.

### 9.6 `DANTE_DEBUG`

Default:

```text
false
```

Meaning:

```text
DANTE_DEBUG
= application/FastAPI debug behavior
!= Uvicorn --reload
!= Uvicorn log level
!= worker count
!= developer environment identity
```

Hard safety invariant:

```text
DANTE_ENV=prod + DANTE_DEBUG=true
→ BOOTSTRAP REJECT
```

This prevents accidental production debug behavior/traceback exposure.

### 9.7 Variables deliberately not created

Do not create these DANTE variables at CP1:

```text
DANTE_HOST
DANTE_PORT
DANTE_WORKERS
DANTE_RELOAD
```

Host/port/workers/reload belong to the ASGI server/runtime boundary. Uvicorn already owns CLI/`UVICORN_*` configuration for those concerns.

Do not duplicate server configuration into the DANTE application namespace.

No database variables exist at CP1 because PostgreSQL application connectivity does not exist until CP3.

## 10. Settings implementation semantics

### 10.1 Model shape

Conceptual target:

```python
class Environment(StrEnum):
    LOCAL = "local"
    DEV = "dev"
    UAT = "uat"
    PROD = "prod"


class Settings(BaseSettings):
    env: Environment
    release_sha: str
    build_id: str
    debug: bool = False

    model_config = SettingsConfigDict(
        env_prefix="DANTE_",
        frozen=True,
        extra="forbid",
    )
```

The implementation may use narrow validators/types to trim/reject blank identity strings and enforce cross-field invariants. It must preserve the external variable names and semantics frozen above.

Canonical external spelling is uppercase `DANTE_*`, as documented in `.env.example` and backend README.

### 10.2 Cross-field bootstrap invariants

At minimum:

```text
missing DANTE_ENV
→ REJECT

unknown DANTE_ENV
→ REJECT

missing/blank DANTE_RELEASE_SHA
→ REJECT

missing/blank DANTE_BUILD_ID
→ REJECT

prod + debug=true
→ REJECT

dev/uat/prod + release_sha=local
→ REJECT

dev/uat/prod + build_id=local
→ REJECT
```

LOCAL may use:

```text
DANTE_ENV=local
DANTE_RELEASE_SHA=local
DANTE_BUILD_ID=local
DANTE_DEBUG=false
```

### 10.3 Immutability

`frozen=True` is required so validated process settings cannot be silently mutated after bootstrap.

If runtime behavior needs to change later, use governed application state/config or restart/redeploy with new deployment configuration as appropriate; do not mutate the bootstrap settings object in place.

## 11. `.env.local` and configuration source model

### 11.1 Committed safe contract

CP1 commits:

```text
apps/backend/.env.example
```

Initial safe contents/shape:

```dotenv
DANTE_ENV=local
DANTE_RELEASE_SHA=local
DANTE_BUILD_ID=local
DANTE_DEBUG=false
```

It contains no secret.

### 11.2 Local-only file

Developer convenience file:

```text
apps/backend/.env.local
```

is ignored by Git under the existing repository ignore policy.

### 11.3 Critical loading rule

The `Settings` class does **not** configure `env_file=".env.local"`.

The application reads the real process environment. LOCAL explicitly asks `uv` to load `.env.local` before the process starts:

```bash
uv run --env-file .env.local \
  uvicorn dante.bootstrap.app:create_app \
  --factory \
  --reload
```

Flow:

```text
LOCAL
.env.local
  ↓ explicit `uv run --env-file`
process environment
  ↓
Settings()
  ↓
create_app()
```

Remote flow:

```text
DEV / UAT / PROD
platform/deployment configuration + future secret manager/workload identity
  ↓
process environment / runtime injection
  ↓
Settings()
  ↓
create_app()
```

Why this separation matters:

- `.env.local` remains a developer convenience, not application configuration authority;
- DEV/UAT/PROD cannot accidentally start reading a local dotenv merely because one happens to be present in a filesystem/image;
- test configuration can be injected explicitly;
- the same Settings model consumes the process environment regardless of source.

A CP1 test must directly prove that `Settings()` does not automatically discover/read `.env.local`.

## 12. FastAPI application factory contract

### 12.1 Factory

Approved public technical bootstrap shape:

```python
def create_app(settings: Settings | None = None) -> FastAPI:
    ...
```

Behavior:

```text
create_app(None)
→ construct Settings() from current process environment
→ validate/fail fast
→ construct FastAPI

create_app(explicit_settings)
→ use already-validated explicit Settings
→ construct FastAPI
```

This allows tests to inject settings without monkeypatching a global singleton.

### 12.2 No global application/settings singleton as architecture

Do not create a module-level `settings = Settings()`.

Do not add `@lru_cache` merely because it appears in common FastAPI settings examples. That pattern is useful when settings are resolved repeatedly as a request dependency. CP1 constructs settings once at bootstrap, so repeated request-level construction/caching is unnecessary.

The application factory is the composition boundary.

### 12.3 `FastAPI(debug=...)`

`settings.debug` controls FastAPI's application debug flag.

Again:

```text
FastAPI debug flag
!= Uvicorn reload
```

Production debug is rejected by Settings validation before app creation.

## 13. Lifespan/wiring decision

CP1 intentionally creates neither:

```text
bootstrap/lifespan.py
bootstrap/wiring.py
```

Reason:

- there is no long-lived DB/provider/resource to acquire and clean up yet;
- there are not enough concrete implementations to justify a wiring module;
- empty files/layers would be ceremony rather than architecture.

When a real application-wide resource exists, FastAPI's current recommended startup/shutdown mechanism is the `lifespan` context manager. CP3 is a likely first point because the database engine/session infrastructure may create a real process-lifetime resource.

Do not use deprecated/legacy startup/shutdown event handlers as the default future design when `lifespan` is applicable.

## 14. Technical HTTP surface

CP1 creates no product API.

Only:

```text
GET /health/live
GET /health/ready
```

### 14.1 Liveness

```text
GET /health/live
200
{"status":"ok"}
```

Meaning at CP1:

```text
FastAPI process is alive and can answer HTTP
```

Liveness must not become dependent on PostgreSQL/provider availability later; external dependency failure should not make the process itself appear dead.

### 14.2 Readiness

```text
GET /health/ready
200
{"status":"ready"}
```

Meaning at CP1:

```text
application construction/bootstrap configuration completed successfully
```

Because CP1 has no database/resource dependency, readiness performs no fake DB/provider check.

Readiness semantics must be explicitly revisited at the boundary where real required runtime dependencies appear. Do not silently redefine it by accident.

### 14.3 Probe exposure

Both routes:

```text
include_in_schema = false
```

They must not appear in the product OpenAPI contract.

Responses remain deliberately minimal. Do not expose:

- environment identity;
- release SHA;
- build ID;
- hostname;
- dependency versions;
- configuration values;
- secret/resource identifiers.

## 15. OpenAPI/docs environment behavior

CP1 policy:

```text
LOCAL    /docs ON    /openapi.json ON    /redoc OFF
DEV      /docs ON    /openapi.json ON    /redoc OFF
UAT      /docs ON    /openapi.json ON    /redoc OFF
PROD     /docs OFF   /openapi.json OFF   /redoc OFF
```

No new environment variable controls this at CP1. It is deterministic technical host behavior derived from the validated `DANTE_ENV`.

This is transport-host configuration, not business logic.

Future generated-client/release-contract workflows must use build/repository artifacts rather than depending on a production interactive documentation endpoint.

## 16. LOCAL server command

Canonical CP1 developer command from `apps/backend`:

```bash
uv run --env-file .env.local \
  uvicorn dante.bootstrap.app:create_app \
  --factory \
  --reload
```

Meaning of each part:

| Segment | Meaning |
|---|---|
| `uv run` | execute inside the locked DANTE backend project environment |
| `--env-file .env.local` | LOCAL-only explicit dotenv injection into the process environment |
| `uvicorn` | ASGI server process |
| `dante.bootstrap.app:create_app` | import the DANTE application factory |
| `--factory` | tell Uvicorn the target is a callable returning an ASGI app |
| `--reload` | LOCAL developer file reload; not controlled by `DANTE_DEBUG` |

Uvicorn host/port can remain its defaults initially. If a developer needs a different bind/port, use Uvicorn CLI/`UVICORN_*` semantics rather than adding DANTE application variables.

## 17. CP1 standard commands

The backend README must document these once implementation exists.

From `apps/backend`:

```bash
# Resolve/bootstrap from the committed lockfile
uv sync --locked

# Prove the lockfile is current
uv lock --check

# Format locally (modifies files)
uv run ruff format .

# Format check (does not modify)
uv run ruff format --check .

# Lint
uv run ruff check .

# Typecheck
uv run mypy

# Tests + coverage according to pyproject configuration
uv run pytest

# Build source distribution + wheel
uv build

# LOCAL server
uv run --env-file .env.local \
  uvicorn dante.bootstrap.app:create_app \
  --factory \
  --reload
```

Do not create a decorative `[project.scripts]` command merely to shorten the Uvicorn invocation at CP1. Add a stable entrypoint only when it has a durable application/release purpose.

## 18. CP1 test contract

### 18.1 `test_settings.py`

Must directly prove at least:

```text
valid LOCAL environment variables                       PASS
valid explicit Settings construction for test injection PASS
missing DANTE_ENV                                       REJECT
unknown DANTE_ENV                                       REJECT
missing/blank DANTE_RELEASE_SHA                         REJECT
missing/blank DANTE_BUILD_ID                            REJECT
PROD + DANTE_DEBUG=true                                 REJECT
DEV/UAT/PROD + release_sha=local                        REJECT
DEV/UAT/PROD + build_id=local                           REJECT
settings mutation after bootstrap                       REJECT
.env.local is not auto-loaded by Settings               PASS
```

Use pytest's environment-isolation facilities such as `monkeypatch`/temporary paths where appropriate; tests must not depend on the developer's actual shell environment.

### 18.2 `test_bootstrap.py`

Must directly prove at least:

```text
create_app(explicit valid settings)                     PASS
GET /health/live                                        200 + exact minimal body
GET /health/ready                                       200 + exact minimal body
health routes absent from OpenAPI                       PASS
LOCAL docs/OpenAPI available                            PASS
DEV/UAT docs/OpenAPI available                          PASS as parametrized behavior
PROD docs/OpenAPI disabled                              PASS
ReDoc disabled                                          PASS
FastAPI debug reflects validated settings               PASS
```

Tests use FastAPI/Starlette `TestClient`/HTTPX transport behavior. Calling route functions directly is not accepted as HTTP proof.

### 18.3 No fake tests

Do not add:

- a meaningless Hypothesis property;
- empty architecture tests before a meaningful dependency graph exists;
- database mocks in CP1;
- placeholder provider tests;
- a fake coverage target.

## 19. CP1 direct acceptance commands

Before CP1 is called PASS, execute directly on the real WSL/Linux workstation:

```text
uv sync --locked                            PASS
uv lock --check                             PASS
Python resolved as 3.14.7                   PASS
import installed `dante` package            PASS
uv run ruff format --check .                PASS
uv run ruff check .                         PASS
uv run mypy                                 PASS
uv run pytest                               PASS
uv build                                    PASS
actual Uvicorn factory process startup       PASS
/health/live over HTTP                       PASS
/health/ready over HTTP                      PASS
```

`PASS` here is earned only after execution; this document itself proves none of them.

## 20. File responsibility map

When CP1 is materialized:

| Path | Single primary responsibility |
|---|---|
| `apps/backend/.python-version` | exact initial Python interpreter pin |
| `apps/backend/pyproject.toml` | project metadata, dependency intent, build/tool configuration |
| `apps/backend/uv.lock` | exact resolved dependency graph |
| `apps/backend/.env.example` | safe LOCAL configuration contract/example |
| `apps/backend/README.md` | executable developer/operator commands + current variable reference |
| `src/dante/__init__.py` | canonical installed package marker/minimal package metadata only |
| `src/dante/bootstrap/app.py` | FastAPI application factory + CP1 technical routes/host configuration |
| `src/dante/platform/config/settings.py` | environment enum + typed immutable settings + safety validation |
| `tests/test_settings.py` | settings source/validation/immutability contract |
| `tests/test_bootstrap.py` | real ASGI application/route/docs behavior |

Do not hide unrelated responsibilities in these files to avoid creating a justified future file. Conversely, do not split a tiny cohesive responsibility into extra modules merely to make the tree look larger.

## 21. Configuration documentation discipline — permanent rule

This section exists specifically to prevent future unexplained variables.

No new backend `DANTE_*` variable is considered complete unless the same change records, at minimum:

```text
NAME
canonical external spelling

OWNER / DOMAIN
which technical/application boundary owns it

TYPE
validated runtime type

REQUIREDNESS
which environments require it

DEFAULT
if any, and why it is safe

SECRET CLASS
secret / non-secret / user-governed application data

SOURCE
LOCAL dotenv, deployment config, secret manager, workload identity, etc.

CONSUMER
exact subsystem that reads the validated setting

EFFECT
what behavior it changes

INVALID COMBINATIONS
cross-field/environment safety rules

EXPOSURE
whether it may appear in logs/health/metrics/API

ROTATION / LIFECYCLE
where applicable

TEST EVIDENCE
validation/default/cross-field/redaction tests

DOCUMENTATION
.env.example + backend README + durable architecture/config doc when material
```

At implementation time, the operational source of truth for existing variables is intentionally redundant in useful ways:

```text
Settings model
= executable validation truth

.env.example
= safe LOCAL contract/discoverability

apps/backend/README.md
= developer/operator explanation and commands

docs/development/* contract
= durable rationale/architecture/governance
```

A variable must not appear only in tribal knowledge/chat history.

## 22. Deferred CP1 items and return triggers

| Deferred item | Why absent now | Return trigger |
|---|---|---|
| `lifespan.py` | no real process-lifetime resource | first real shared resource requiring acquire/release, likely CP3 DB engine |
| `wiring.py` | no meaningful concrete component graph yet | composition root becomes clearer by extracting real wiring |
| `platform/database` | no app DB connectivity until CP3 | CP3 |
| SQLAlchemy/psycopg/Alembic | unused before real PostgreSQL harness | CP3 |
| Hypothesis dependency | no meaningful CP1 property/state space | first real invariant/property candidate |
| architecture import tooling | too little package graph to justify a tool | CP4 or earlier if CP1 graph already provides real enforceable value |
| backend OCI Dockerfile | normal inner loop runs directly in WSL; deployment packaging not active | artifact/deployment packaging boundary |
| observability package | no fake telemetry scaffold | first real service observability implementation boundary |
| auth/security package | no Auth implementation authorized | Auth workstream/vertical slice |
| business `modules/` | concrete capability map not yet selected | real vertical slice after scaffold QA |
| PostgreSQL | separate fault-isolated infrastructure checkpoint | CP2 |
| schema/domain mappings | scaffold must pass first | post-CP5 Logical → PostgreSQL workstream |

## 23. Source-verification record

Research was refreshed on **2026-08-19** before freezing this contract.

Primary/official sources used include:

- uv build backend/config/dependency documentation: `https://docs.astral.sh/uv/`
- FastAPI official documentation: `https://fastapi.tiangolo.com/`
- Uvicorn official settings documentation: `https://www.uvicorn.org/settings/`
- Pydantic/Pydantic Settings documentation: `https://docs.pydantic.dev/`
- pytest official documentation: `https://docs.pytest.org/`
- authoritative package release metadata on PyPI for FastAPI, Pydantic, pydantic-settings, Uvicorn, Ruff, mypy, pytest, pytest-cov, HTTPX and relevant Uvicorn extras.

Release observations used to choose the manifest floor on that date:

```text
FastAPI stable                 0.141.1
Pydantic stable                2.13.4
pydantic-settings stable       2.15.0
Uvicorn stable                 0.52.1
Ruff stable                    0.16.2
mypy stable                    2.3.0
pytest stable                  9.1.1
pytest-cov stable              7.1.0
HTTPX stable                   0.28.1
```

These observations explain the approved compatibility ranges. They are **not** a promise that those remain the latest versions forever. Once CP1 is implemented, the committed `uv.lock` becomes exact implementation evidence; future upgrades re-check current official release/migration information.

## 24. Exact resume point

A future conversation resuming CP1 must start here:

```text
CP1-01 dependency/version policy     APPROVED
CP1-02 pyproject/tooling design       APPROVED
CP1-03 FastAPI/settings design        APPROVED
CP1 implementation files              NOT CREATED
CP1 direct QA                         NOT RUN
```

Next sequence:

```text
1. Read this document + `docs/workstreams/backend-scaffold.md`.
2. Verify `feature/backend-scaffold`, remote/local HEAD and clean tree.
3. Re-check only if version-sensitive evidence materially changed since 2026-08-19.
4. Present the exact CP1 implementation Git write gate with every path.
5. After explicit approval, create CP1 only.
6. Generate `uv.lock` through uv; never hand-write it.
7. Run all CP1 local direct acceptance commands.
8. Prove exact remote delta/readback.
9. Update CP1 status/documentation with actual resolved versions and evidence.
10. Proceed to CP2 only after CP1 PASS.
```

No PostgreSQL/schema/business implementation is authorized by this contract.
