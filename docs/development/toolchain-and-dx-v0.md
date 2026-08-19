# Toolchain and Developer Experience v0

- Status: **CLOSED / ACCEPTED BACKEND BASELINE**
- Scope: backend runtime, package/dependency management, local development and reproducibility
- Frontend toolchain: **DEFERRED**

## 1. Goal

A clean supported workstation/CI runner can reconstruct DANTE backend development from repository-controlled declarations rather than tribal knowledge.

The backend toolchain must be:

- reproducible;
- explicit about versions;
- fast for daily inner-loop development;
- production-relevant in server/database semantics;
- small enough to understand and maintain;
- independent of one IDE.

## 2. Version policy

DANTE distinguishes:

```text
SUPPORTED RUNTIME LINE
major/minor family accepted by the project

BOOTSTRAP PIN
exact interpreter/tool version used by the scaffold/CI baseline

DEPENDENCY LOCK
exact resolved dependency graph
```

Rules:

1. production/CI does not intentionally depend on unbounded `latest`;
2. exact CI runtime/tool versions are pinned where practical;
3. lockfiles are committed;
4. upgrades are explicit reviewed changes;
5. pre-release majors are not default production baselines;
6. version-sensitive decisions are rechecked against primary documentation at upgrade/scaffold time.

## 3. Python

```text
SUPPORTED LINE       Python 3.14.x
INITIAL PIN          Python 3.14.7
```

The backend commits:

```text
apps/backend/.python-version
```

A Python major/minor migration requires compatibility review and full affected CI, especially for native/binary dependencies.

Experimental free-threaded Python is not the default simply because the runtime exposes it; activation requires measured benefit and ecosystem compatibility.

## 4. Dependency/environment manager

Use **uv**.

Backend ownership:

```text
apps/backend/pyproject.toml
apps/backend/uv.lock
apps/backend/.python-version
```

Rules:

- `pyproject.toml` declares project/dependency/tool intent;
- `uv.lock` is committed generated package-manager state;
- dependency changes go through uv/manifest workflow, not hand-edited lock internals;
- CI/deploy uses frozen/locked installation behavior;
- ad-hoc `pip install` into the project environment is not normal project workflow;
- dependency groups separate runtime/dev/test concerns when useful.

A root uv workspace is not introduced while there is only one actual Python project. Add one only when coordinated multi-project Python resolution becomes real.

## 5. Source layout

Use src layout:

```text
apps/backend/
└── src/
    └── dante/
```

Tests import the project package rather than relying on repository-root path accidents.

Canonical Python package namespace: `dante`.

## 6. Formatting/linting

Use **Ruff** for formatting/linting/import-order/selected correctness/security-adjacent rules.

```text
local format
may modify files

CI format check
never modifies files

safe autofix
allowed locally/reviewed

unsafe broad fixes
never applied blindly in CI
```

Configuration lives with the backend project unless later real multi-project Python reuse justifies centralization.

## 7. Type checking

Use **mypy** with a strict project baseline.

Principles:

- public/application boundaries typed;
- untyped defs not normal production code;
- `Any` bounded to real integration/dynamic reasons;
- ignores narrow and reasoned;
- third-party typing weaknesses isolated at adapters;
- external dynamic payloads validated into typed internal structures before meaningful use;
- path-specific exceptions documented rather than lowering global strictness.

Exact plugin/settings compatibility with the scaffolded Pydantic/FastAPI versions is reverified at implementation time.

## 8. Tests

Use **pytest** as backend runner.

Use **Hypothesis** for property/state-space/state-machine tests where invariants/lifecycle combinations justify it, not as boilerplate for trivial functions.

Detailed model: `testing-and-ci-v0.md`.

## 9. Persistence stack

```text
SQLAlchemy        2.0 stable line
psycopg           3
Alembic           migration authority
```

Use SQLAlchemy async APIs + psycopg async DB I/O at I/O boundaries where useful. Domain/application calculations remain synchronous by default.

Exact package versions are resolved/pinned in `uv.lock` during scaffold.

## 10. Windows / WSL2 / Linux boundary

Canonical server semantics: **Linux**.

Supported primary Windows workflow:

```text
Windows 11 host
        ↓
WSL2 / Linux
        ↓
repository in WSL filesystem
        ↓
Python / uv / Git / backend commands under Linux semantics
```

Do not operate one backend virtual environment alternately from Windows and WSL paths.

The goal is to make LOCAL server behavior closer to CI/production and avoid Windows-specific filesystem/async/native-library behavior becoming canonical accidentally.

## 11. PyCharm workflow

PyCharm is supported as the primary user workflow.

Recommended arrangement:

```text
PyCharm on Windows
        ↓
WSL project/interpreter
        ↓
apps/backend/.venv Python managed through uv
```

Run/debug/breakpoint/test integration may be driven from PyCharm while Python actually executes under Linux/WSL semantics.

Repository correctness never depends on PyCharm. Every authoritative format/lint/type/test/migration operation has a CLI form usable by CI and another supported IDE.

IDE-specific files are committed only if they provide durable team value and contain no personal paths/secrets.

## 12. Docker / Compose

Use current Docker Compose v2/specification conventions for LOCAL stateful infrastructure.

Normal inner loop:

```text
FastAPI/backend process
→ direct WSL/Linux process for reload/debug

PostgreSQL and other stateful infra
→ Docker Compose
```

This preserves simple debugging without sacrificing reproducible infrastructure.

Rules:

- explicit image/build versions, never canonical `latest`;
- DANTE-scoped resource names;
- synthetic LOCAL passwords;
- health checks where startup dependency matters;
- configurable ports where useful;
- local volumes disposable unless explicitly documented;
- no production secrets in Compose files.

## 13. Reproducible LOCAL PostgreSQL

DANTE owns the canonical local PostgreSQL build/configuration.

Required from first persistence scaffold:

```text
PostgreSQL          18.4
PostGIS             3.6.4
pgvector            0.8.6
pg_trgm             enabled
unaccent            enabled
pg_stat_statements  enabled
native FTS          available
```

`pg_stat_statements` receives required server preload configuration.

Do not use an unpinned generic community “all extensions” image as the canonical baseline.

The same DANTE database image/envelope is used by backend PostgreSQL integration/migration tests where practical so local/CI capability does not silently diverge.

## 14. PgBouncer

PgBouncer 1.25.2 remains selected Physical target.

It is not required between every first LOCAL query. Activate/provide an explicit profile when connection-pooling behavior is implemented/tested.

Validation must preserve direct PostgreSQL paths for migration/replication classes that require them and exercise the accepted PowerSync/logical-replication compatibility obligations when those capabilities activate.

## 15. Migration developer workflow

Canonical logical sequence:

```text
change reviewed SQLAlchemy/schema intent
→ generate candidate revision when useful
→ manually inspect/complete migration
→ migration risk classification
→ run migration/static checks
→ create clean DANTE PostgreSQL
→ base → head
→ integration tests
→ metadata/schema drift check
→ release-transition tests where applicable
```

Autogenerate never equals approval.

## 16. Standard backend developer operations

The scaffold must expose/document straightforward commands for:

```text
bootstrap backend dependencies
run backend
debug backend
format
format check
lint
typecheck
unit/application tests
property tests
PostgreSQL integration tests
architecture tests
migration base→head
schema drift check
create candidate migration
apply migration
reset LOCAL DB safely
logical dump/restore for approved use
full local CI-equivalent backend validation
build future OCI backend artifact
```

A developer should not need undocumented command sequences for routine operations.

## 17. Line endings / text normalization

Canonical repository text uses LF unless a file/tool format explicitly requires another representation.

`.editorconfig`/Git attributes introduced with scaffold prevent Windows/macOS/Linux line-ending churn. Shell scripts use LF and correct executable mode.

## 18. Dependency update policy

Routine dependency updates:

- bounded reviewed PR/change;
- update lockfile through package manager;
- run affected CI;
- include migration/config/release implications when relevant.

Major runtime/framework upgrades:

- review official migration/release notes;
- verify ecosystem compatibility;
- run full affected test matrix;
- update pins/docs together;
- avoid mixing unrelated architecture refactors unless required.

Dependency automation is configured only for package-manager/ecosystem versions actually supported by the chosen GitHub tooling at implementation time. No false claim that a bot supports a manifest/lock format until verified.

## 19. Reproducibility boundary

Supported backend setup is reconstructible from:

```text
source commit
+ pinned runtime/tool versions
+ committed pyproject/uv.lock/.python-version
+ committed DANTE PostgreSQL/container definitions
+ external LOCAL secrets/config
+ documented commands
```

“Works on my machine” is not sufficient evidence.

## 20. Frontend toolchain

Not selected by this document.

Node/package-manager/task-graph/lint/format/test/mobile-build choices are explicitly deferred to the frontend workstream.
