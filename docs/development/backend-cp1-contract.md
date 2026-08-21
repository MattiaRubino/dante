# Backend CP1 Technical Contract

- Status: **CLOSED / DIRECT QA PASS**
- Workstream: `docs/workstreams/backend-scaffold.md`
- Branch: `feature/backend-scaffold`
- Product: **DANTE**
- Repository: `MattiaRubino/dante`
- Contract checkpoint: **CP1-01 + CP1-02 + CP1-03 CLOSED / IMPLEMENTED**
- Version/source verification baseline: **2026-08-19**
- Direct implementation/closure evidence: **2026-08-20**
- CP1 implementation/lock closure HEAD: `02d113d772cdb247faebb3cef4d857d125266da3`
- Implementation authority: **EVERY FUTURE WRITE STILL REQUIRES ITS OWN EXACT GATE**

## 1. Purpose

This document is the durable technical contract and closure record for **CP1 — Backend Python/process/config foundation**.

It exists so a future developer, reviewer or conversation can answer, without reconstructing chat history:

- what CP1 proves;
- why each direct dependency exists;
- what version policy is used;
- why the Python distribution name and import namespace differ;
- what each `DANTE_*` variable means;
- how LOCAL dotenv loading works;
- how the FastAPI process is created;
- what health/readiness mean at CP1;
- why there is no lifespan/database/wiring layer yet;
- which lint/type/test/coverage policies are enforced;
- what implementation findings changed earlier assumptions;
- which commands directly passed;
- what remains deliberately deferred and at which trigger it returns.

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

## 3. CP1 scope and materialized tree

CP1 materializes the smallest real DANTE backend project that can:

1. resolve/install from a committed manifest and lockfile;
2. run under the accepted Python 3.14.7 Linux/WSL environment;
3. import as an installed `src`-layout Python package;
4. create and run a FastAPI process through an application factory;
5. validate typed bootstrap configuration before accepting work;
6. expose only technical process health/readiness probes;
7. run real format/lint/type/test/build commands;
8. prove the above through automated tests and real HTTP process checks.

CP1 does **not** require PostgreSQL. PostgreSQL begins at CP2 and application persistence at CP3.

Materialized tree:

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

`apps/backend/uv.lock` is committed and remotely read back. `.coverage`, `.venv`, `.env.local`, build output and tool caches are generated/local state and are not source artifacts.

## 4. CP1-01 — dependency and version contract

### 4.1 Runtime line

```text
SUPPORTED PYTHON LINE    3.14.x
INITIAL EXACT PIN        3.14.7
PROJECT MANAGER          uv
LOCKFILE                 apps/backend/uv.lock — COMMITTED / REMOTE VERIFIED
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
- a new upstream release must not silently change an already-locked DANTE checkout.

### 4.3 Runtime dependencies

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

| Dependency | Why direct | CP1 role |
|---|---|---|
| `fastapi` | DANTE constructs the inbound HTTP/process host directly | application factory + technical health routes |
| `pydantic` | DANTE uses validation primitives directly | validation/cross-field rules + mypy integration plugin |
| `pydantic-settings` | accepted configuration boundary | process environment → typed immutable settings |
| `uvicorn[standard]` | accepted ASGI server | actual LOCAL server + supported reload/runtime extras |

Do **not** use `fastapi[standard]` merely to acquire unrelated optional capabilities.

### 4.4 Quality dependencies

```toml
[dependency-groups]
quality = [
    "ruff>=0.16.2,<0.17",
    "mypy>=2.3.0,<3",
]
```

The manifest floors describe the accepted compatibility envelope. The final lock resolved later compatible patch releases.

### 4.5 Test dependencies

```toml
[dependency-groups]
test = [
    "pytest>=9.1.1,<10",
    "httpx2>=2.9.1,<3",
    "pytest-cov>=7.1.0,<8",
]
```

Responsibilities:

| Dependency | Why it exists |
|---|---|
| `pytest` | canonical backend test runner |
| `httpx2` | current Starlette `TestClient` transport dependency |
| `pytest-cov` | statement/branch coverage measurement |

### 4.6 Evidence-driven `httpx` → `httpx2` correction

The original CP1 design used `httpx>=0.28.1,<0.29`.

Direct execution invalidated that assumption after FastAPI resolved current Starlette behavior. `uv run pytest` failed during collection because Starlette attempted to use `httpx2`; with only `httpx` installed it emitted `StarletteDeprecationWarning`, and DANTE's intentional warnings-as-errors policy promoted the warning to an error.

DANTE deliberately did **not**:

- weaken warnings-as-errors;
- pin Starlette backward;
- bypass `TestClient`;
- hide the warning.

A temporary proof:

```text
uv run --with "httpx2==2.9.1" pytest
→ 25 collected
→ 25 passed
→ statement coverage 100.00%
→ branch coverage 100.00%
```

The manifest was then corrected to `httpx2>=2.9.1,<3`, the lock regenerated, the `.venv` synchronized from that lock and the canonical suite rerun successfully.

### 4.7 Developer aggregate group

```toml
[dependency-groups]
dev = [
    { include-group = "quality" },
    { include-group = "test" },
]
```

### 4.8 Hypothesis posture

Hypothesis remains an accepted backend testing tool but is deliberately **not a CP1 dependency**.

```text
TOOL SELECTED                 YES
CP1 INSTALL                   NO
FIRST ACTIVATION              first meaningful property/invariant/state-space test
PLACEHOLDER PROPERTY TEST     FORBIDDEN
```

### 4.9 Persistence packages

Do not install in CP1:

```text
SQLAlchemy
psycopg
Alembic
```

They return at CP3 after CP2 provides a directly working DANTE PostgreSQL environment.

### 4.10 Final exact direct graph — 2026-08-20

The final `uv lock` resolved **39 packages**. Direct project dependencies/groups:

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

Remote lock readback confirms:

```text
httpx2               2.12.0
httpcore2             2.12.0
httpx2-jsfetch         1.0
truststore             0.10.4
```

The previous direct `httpx 0.28.1` project dependency is no longer in the final DANTE graph.

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

### 5.3 Build backend

```toml
[build-system]
requires = ["uv_build>=0.12.5,<0.13"]
build-backend = "uv_build"

[tool.uv.build-backend]
module-name = "dante"
```

Why:

- the backend is pure Python at CP1;
- uv's native build backend fits `src/` projects;
- `dante-backend` would otherwise normalize to module `dante_backend`;
- explicit `module-name = "dante"` preserves the accepted namespace;
- the upper bound follows the chosen uv build-backend compatibility posture.

### 5.4 Accidental PyPI publication barrier

```toml
classifiers = [
    "Private :: Do Not Upload",
]
```

This is a safety barrier, not a substitute for credential/repository controls.

## 6. Ruff contract

### 6.1 Baseline

```toml
[tool.ruff]
target-version = "py314"
line-length = 100
src = ["src"]
```

### 6.2 Stable high-signal lint families

```text
A ASYNC B BLE C4 DTZ E4 E7 E9 F G I LOG N PERF PIE PT PTH RET RUF S SIM T20 UP
```

Test-only ignore:

```toml
[tool.ruff.lint.per-file-ignores]
"tests/**/*.py" = ["S101"]
```

`S101` is ignored only because ordinary `assert` is canonical pytest behavior.

Explicitly not enabled at CP1:

```text
ALL
preview rules
unsafe automatic fixes in CI
ANN as a duplicate type-enforcement system
TC/type-checking import movement before a concrete graph justifies it
```

### 6.3 Direct Ruff findings

The first real run found only narrow source-normalization issues:

1. formatter normalization in the `.env.local` test fixture string;
2. three `RUF043` findings requiring raw regex strings in `pytest.raises(..., match=...)`.

After narrow repairs:

```text
uv run ruff format --check .    PASS — 9 files already formatted
uv run ruff check .             PASS — All checks passed
```

The same commands passed again against the final `httpx2` locked environment.

## 7. mypy contract

Final configuration:

```toml
[tool.mypy]
plugins = ["pydantic.mypy"]
python_version = "3.14"
strict = true
warn_unreachable = true
show_error_codes = true
show_column_numbers = true
pretty = true
files = ["src", "tests"]
enable_error_code = ["explicit-override", "exhaustive-match"]

[tool.pydantic-mypy]
init_forbid_extra = true
init_typed = true
warn_required_dynamic_aliases = true
```

Rules:

- global `strict` is preserved;
- tests are type-checked;
- `explicit-override` and `exhaustive-match` remain enabled;
- framework typing weaknesses are handled narrowly, never by lowering global strictness.

### 7.1 Pydantic plugin — evidence-driven decision

The original design deliberately started with the plugin OFF.

Real plain strict mypy produced **21 `call-arg` errors** because it treated environment-sourced `BaseSettings` fields as mandatory explicit constructor arguments.

A temporary plugin proof reduced those to one diagnostic on the deliberate negative runtime mutation test. The plugin correctly recognized frozen `Settings.debug` as read-only.

Final posture:

```text
PYDANTIC MYPY PLUGIN       ENABLED
GLOBAL MYPY STRICTNESS     PRESERVED
SETTINGS FROZEN            PRESERVED
RUNTIME IMMUTABILITY TEST  PRESERVED
BROAD TYPE IGNORES         FORBIDDEN
```

The one intentional test line is:

```python
settings.debug = True  # type: ignore[misc]  # deliberate runtime immutability probe
```

Canonical final evidence:

```text
uv run mypy
Success: no issues found in 8 source files
```

## 8. pytest and coverage contract

Configuration principles:

- pytest 9 native TOML configuration;
- `--import-mode=importlib`;
- strict pytest behavior;
- warnings treated as errors;
- coverage includes statement and branch measurement;
- missing lines shown;
- no arbitrary percentage threshold at CP1.

Canonical final locked result:

```text
collected 25 items
25 passed
statement coverage 100.00%
branch coverage    100.00%
```

The 100% result is evidence for this **small CP1 surface only**. It does not establish a permanent global coverage target.

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

| External variable | Internal setting | Required | Secret | CP1 meaning | Consumer |
|---|---|---:|---:|---|---|
| `DANTE_ENV` | `env` | YES | NO | `local`, `dev`, `uat`, `prod` runtime identity | bootstrap/config + host behavior |
| `DANTE_RELEASE_SHA` | `release_sha` | YES | NO | source/release identity; `local` marker only in LOCAL | bootstrap metadata/future observability |
| `DANTE_BUILD_ID` | `build_id` | YES | NO | build/execution identity; `local` marker only in LOCAL | bootstrap metadata/future observability |
| `DANTE_DEBUG` | `debug` | NO | NO | FastAPI application debug behavior only | `FastAPI(debug=...)` |

### 9.3 Closed environment set

```text
local
dev
uat
prod
```

Represented by `Environment(StrEnum)`.

`TEST` is not a fifth promotion environment.

### 9.4 Identity values

`DANTE_RELEASE_SHA` and `DANTE_BUILD_ID`:

- are required;
- are stripped and reject blank values;
- permit `local` only when `DANTE_ENV=local`;
- are not automatically exposed through health/API output.

Future exact artifact/Git-SHA formatting is deferred until the release pipeline exists.

### 9.5 Debug invariant

```text
DANTE_ENV=prod + DANTE_DEBUG=true
→ BOOTSTRAP REJECT
```

`DANTE_DEBUG` controls FastAPI application debug behavior only; it does not control Uvicorn reload, host, port or workers.

### 9.6 Variables deliberately not created at CP1

```text
DANTE_HOST
DANTE_PORT
DANTE_WORKERS
DANTE_RELOAD
DB variables
```

Host/port/workers/reload belong to the ASGI server/runtime boundary. DB configuration begins only when application DB connectivity exists.

## 10. Settings implementation semantics

Conceptual shape:

```python
class Environment(StrEnum):
    LOCAL = "local"
    DEV = "dev"
    UAT = "uat"
    PROD = "prod"


class Settings(BaseSettings):
    env: Environment
    release_sha: IdentityValue
    build_id: IdentityValue
    debug: bool = False
```

Configuration:

```text
env_prefix   DANTE_
extra        forbid
frozen       true
```

Cross-field invariants directly tested:

```text
missing DANTE_ENV                         REJECT
unknown DANTE_ENV                         REJECT
missing/blank DANTE_RELEASE_SHA           REJECT
missing/blank DANTE_BUILD_ID              REJECT
prod + debug=true                         REJECT
dev/uat/prod + release_sha=local          REJECT
dev/uat/prod + build_id=local             REJECT
mutation after bootstrap                  REJECT
```

## 11. `.env.local` and configuration source model

Committed safe example:

```dotenv
DANTE_ENV=local
DANTE_RELEASE_SHA=local
DANTE_BUILD_ID=local
DANTE_DEBUG=false
```

Developer convenience file:

```text
apps/backend/.env.local
```

is ignored by Git.

Critical rule: `Settings` does **not** configure `env_file=".env.local"`.

LOCAL flow:

```text
.env.local
  ↓ explicit uv --env-file
process environment
  ↓
Settings()
  ↓
create_app()
```

Remote flow:

```text
DEV / UAT / PROD deployment configuration
  ↓
process environment / runtime injection
  ↓
Settings()
  ↓
create_app()
```

A direct test proves that `Settings()` does not auto-load `.env.local`.

## 12. FastAPI application factory contract

Public technical bootstrap shape:

```python
def create_app(settings: Settings | None = None) -> FastAPI:
    ...
```

Behavior:

```text
create_app(None)
→ Settings() from current process environment
→ validate/fail fast
→ construct FastAPI

create_app(explicit_settings)
→ use already-validated settings
→ construct FastAPI
```

No module-level `settings = Settings()` and no `@lru_cache` are introduced merely because they appear in common examples. CP1 constructs settings once at bootstrap.

## 13. Lifespan/wiring decision

CP1 intentionally creates neither:

```text
bootstrap/lifespan.py
bootstrap/wiring.py
```

There is no long-lived DB/provider resource or sufficiently large concrete component graph yet.

When a real application-wide resource exists, FastAPI lifespan is the preferred startup/shutdown mechanism. CP3 is the likely first trigger.

## 14. Technical HTTP surface

CP1 creates no product API.

Only:

```text
GET /health/live
GET /health/ready
```

### 14.1 Liveness

```text
200
{"status":"ok"}
```

Meaning: process is alive and can answer HTTP.

Liveness must not later depend on external dependency availability.

### 14.2 Readiness

```text
200
{"status":"ready"}
```

CP1 meaning: application construction/bootstrap configuration completed successfully.

Because CP1 has no database/resource dependency, readiness performs no fake DB/provider check. Its semantics must be revisited when required runtime dependencies appear.

### 14.3 Exposure

Both routes use `include_in_schema=false` and expose no:

- environment identity;
- release SHA;
- build ID;
- hostname;
- dependency versions;
- configuration values;
- secret/resource identifiers.

## 15. OpenAPI/docs environment behavior

```text
LOCAL    /docs ON    /openapi.json ON    /redoc OFF
DEV      /docs ON    /openapi.json ON    /redoc OFF
UAT      /docs ON    /openapi.json ON    /redoc OFF
PROD     /docs OFF   /openapi.json OFF   /redoc OFF
```

No extra environment variable controls this at CP1.

## 16. Canonical LOCAL server command

From `apps/backend`:

```bash
uv run --env-file .env.local \
  uvicorn dante.bootstrap.app:create_app \
  --factory \
  --reload
```

Uvicorn owns host/port/workers/reload semantics; do not duplicate them into `DANTE_*` application configuration.

## 17. CP1 standard commands

```bash
uv sync --locked
uv lock --check
uv run ruff format --check .
uv run ruff check .
uv run mypy
uv run pytest
uv build
```

Local formatting may use:

```bash
uv run ruff format .
```

Do not create a decorative project script merely to shorten the Uvicorn invocation.

## 18. CP1 test contract

### 18.1 Settings tests

Directly prove:

```text
valid LOCAL environment variables                       PASS
valid explicit Settings construction                    PASS
missing DANTE_ENV                                       REJECT
unknown DANTE_ENV                                       REJECT
missing/blank release identity                          REJECT
missing/blank build identity                            REJECT
PROD + debug=true                                       REJECT
remote + local identity markers                         REJECT
settings mutation after bootstrap                       REJECT
.env.local is not auto-loaded                           PASS
```

### 18.2 Bootstrap/HTTP tests

Directly prove:

```text
create_app(explicit settings)                           PASS
GET /health/live                                        200 + exact body
GET /health/ready                                       200 + exact body
health routes absent from OpenAPI                       PASS
LOCAL/DEV/UAT docs + OpenAPI                            PASS
PROD docs + OpenAPI disabled                            PASS
ReDoc disabled                                          PASS
FastAPI debug reflects validated settings               PASS
```

Tests use FastAPI/Starlette `TestClient` with `httpx2`; calling route functions directly is not accepted as HTTP proof.

### 18.3 No fake tests

Do not add:

- meaningless Hypothesis properties;
- empty architecture tests before a meaningful dependency graph exists;
- database mocks in CP1;
- placeholder provider tests;
- fake coverage targets.

## 19. CP1 direct acceptance — FINAL EVIDENCE

Every CP1 acceptance obligation was run directly on the real WSL/Linux workstation against the final locked environment.

```text
uv lock                                    PASS — 39 packages resolved
uv lock --check                            PASS
uv tree --locked --depth 1                 PASS
uv sync --locked                           PASS
Python project interpreter                 PASS — 3.14.7
installed `dante` src-layout import        PASS
uv run ruff format --check .               PASS — 9 files already formatted
uv run ruff check .                        PASS — All checks passed
uv run mypy                                PASS — no issues in 8 source files
uv run pytest                              PASS — 25/25
statement coverage                         PASS — 100.00% on CP1 surface
branch coverage                            PASS — 100.00% on CP1 surface
uv build                                   PASS
source distribution                        PASS — dante_backend-0.1.0.tar.gz
wheel                                      PASS — dante_backend-0.1.0-py3-none-any.whl
actual Uvicorn factory process startup     PASS
GET /health/live over real HTTP            PASS — 200 / {"status":"ok"}
GET /health/ready over real HTTP           PASS — 200 / {"status":"ready"}
remote CP1 lock commit/readback             PASS
```

Uvicorn real-process evidence included:

```text
127.0.0.1:8000
WatchFiles reloader started
server process started
application startup complete
```

CP1 is therefore **CLOSED / DIRECT QA PASS**.

This does not imply PostgreSQL, HG/PSV, recovery, migration or failure-injection validation.

## 20. File responsibility map

| Path | Primary responsibility |
|---|---|
| `apps/backend/.python-version` | exact initial Python interpreter pin |
| `apps/backend/pyproject.toml` | project metadata, dependency intent, build/tool configuration |
| `apps/backend/uv.lock` | exact resolved dependency graph |
| `apps/backend/.env.example` | safe LOCAL configuration contract/example |
| `apps/backend/README.md` | executable developer/operator commands + variable reference |
| `src/dante/__init__.py` | canonical installed package marker |
| `src/dante/bootstrap/app.py` | FastAPI application factory + CP1 technical routes/host behavior |
| `src/dante/platform/config/settings.py` | environment enum + typed immutable settings + safety validation |
| `tests/test_settings.py` | settings source/validation/immutability contract |
| `tests/test_bootstrap.py` | real ASGI application/route/docs behavior |

## 21. Configuration documentation discipline — permanent rule

No new backend `DANTE_*` variable is complete unless the same change records, at minimum:

```text
NAME
OWNER / DOMAIN
TYPE
REQUIREDNESS
DEFAULT
SECRET CLASS
SOURCE
CONSUMER
EFFECT
INVALID COMBINATIONS
EXPOSURE
ROTATION / LIFECYCLE where applicable
TEST EVIDENCE
DOCUMENTATION
```

Operational truth is intentionally represented in complementary forms:

```text
Settings model
= executable validation truth

.env.example
= safe LOCAL contract/discoverability

apps/backend/README.md
= developer/operator usage

durable development docs
= rationale/architecture/governance
```

A variable must not exist only in chat/tribal knowledge.

## 22. Deferred items and return triggers

| Deferred item | Why absent now | Return trigger |
|---|---|---|
| `lifespan.py` | no real process-lifetime resource | first real shared acquire/release resource, likely CP3 DB engine |
| `wiring.py` | no meaningful concrete component graph yet | real composition root becomes large enough to extract |
| `platform/database` | no app DB connectivity in CP1 | CP3 |
| SQLAlchemy/psycopg/Alembic | unused before real PostgreSQL environment | CP3 |
| Hypothesis dependency | no meaningful CP1 property/state space | first real invariant/property candidate |
| architecture import tooling | package graph too small | CP4 or earlier only if real enforceable value appears |
| backend OCI Dockerfile | deployment packaging not active | artifact/deployment packaging boundary |
| observability package | no fake telemetry scaffold | first real service observability boundary |
| auth/security package | no Auth implementation authorized | Auth workstream/vertical slice |
| business `modules/` | capability implementation not yet selected | real vertical slice after scaffold QA |
| PostgreSQL | separate infrastructure checkpoint | CP2 |
| concrete schema/domain mappings | scaffold must pass first | post-CP5 Logical → PostgreSQL workstream |

## 23. Source-verification record

Research was refreshed on 2026-08-19 before design freeze and version-sensitive evidence was refreshed again on 2026-08-20 during real implementation.

Primary/official source families used:

- uv official documentation;
- FastAPI official documentation;
- Starlette official documentation/release notes;
- Uvicorn official documentation;
- Pydantic/Pydantic Settings official documentation, including mypy integration;
- pytest official documentation;
- authoritative package release metadata for the direct dependency set.

Initial observed versions explained the compatibility floors. The final exact implementation authority is the committed `uv.lock`.

Important closure fact:

```text
httpx initial assumption      historical / superseded
httpx2 manifest envelope      >=2.9.1,<3
httpx2 final locked version   2.12.0
```

## 24. Exact resume point

CP1 is closed. A future conversation must not replay CP1 setup by default.

```text
CP1-01 dependency/version policy       CLOSED / IMPLEMENTED
CP1-02 pyproject/tooling design         CLOSED / IMPLEMENTED
CP1-03 FastAPI/settings design          CLOSED / IMPLEMENTED
CP1 source/manifests                    REMOTE
CP1 uv.lock                             REMOTE / VERIFIED
Ruff                                    DIRECT PASS
mypy strict                             DIRECT PASS
pytest                                  DIRECT PASS — 25/25
CP1 coverage                            100% statement/branch evidence
uv build                                DIRECT PASS
real Uvicorn + HTTP probes              DIRECT PASS
CP1                                     CLOSED / DIRECT QA PASS
PostgreSQL / CP2                        NOT STARTED / NEXT
```

Next sequence:

```text
1. Read this contract + `docs/workstreams/backend-scaffold.md` + current project truth.
2. Verify `feature/backend-scaffold`, current remote/local HEAD and clean tree.
3. Treat CP1 as CLOSED unless new concrete evidence proves a contradiction.
4. Start CP2 READ-ONLY design/research.
5. Re-check current official evidence for PostgreSQL 18.4, PostGIS 3.6.4, pgvector 0.8.6 and selected built-in extensions.
6. Decide the DANTE-owned PostgreSQL image/build strategy and Compose topology.
7. Define volume/persistence/reset semantics, healthcheck, published port, LOCAL credentials and extension activation.
8. Define direct CP2 acceptance evidence including restart/recreation persistence and host GUI connectivity.
9. Present an exact CP2 Git write gate before creating PostgreSQL/Compose files.
10. Proceed to CP3 only after CP2 direct PASS.
```

No PostgreSQL/schema/business implementation is authorized by this CP1 contract.
