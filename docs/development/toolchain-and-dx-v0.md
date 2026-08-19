# Toolchain and Developer Experience v0

- Status: **Engineering Foundation branch baseline — pending closure**
- Scope: runtimes, package management, formatting/types, local workflow and reproducibility

## 1. Goal

A new contributor or CI runner should be able to reconstruct a supported DANTE development environment from repository-controlled declarations rather than tribal knowledge.

The toolchain must be:

- reproducible;
- fast enough for daily use;
- explicit about versions;
- cross-platform where client development needs it;
- production-relevant where server semantics matter;
- small enough to understand and maintain.

## 2. Version policy

DANTE distinguishes:

```text
RUNTIME LINE
supported major/minor family, e.g. Python 3.14 / Node 24 LTS

BOOTSTRAP PIN
exact interpreter/package-manager version used when the production scaffold is created

DEPENDENCY LOCK
exact library dependency graph resolved by uv.lock / pnpm-lock.yaml
```

Rules:

1. production/CI never intentionally depends on an unbounded `latest` tag;
2. exact CI runtime/tool versions are pinned;
3. lockfiles are committed;
4. runtime/tool upgrades are explicit PRs;
5. pre-release majors are not default production baselines;
6. security/bugfix upgrades are kept reasonably current;
7. version-sensitive decisions are re-checked against primary documentation at upgrade time.

## 3. Python runtime

### Decision

```text
SUPPORTED PRODUCTION LINE
Python 3.14.x

INITIAL BOOTSTRAP PIN
Python 3.14.7
```

Python 3.14.7 is a stable maintenance release as of the Engineering Foundation baseline date.

The API project commits `.python-version` under `apps/api/` so uv and developer tooling resolve the intended interpreter.

A later Python minor/major migration is deliberate and runs full backend CI plus compatibility validation for binary/native dependencies.

Experimental free-threaded Python is not the production default merely because Python 3.14 supports it. It requires a separate measured benefit/compatibility decision.

## 4. Python dependency/environment manager

### Decision

Use **uv**.

API ownership:

```text
apps/api/pyproject.toml
apps/api/uv.lock
apps/api/.python-version
```

Rules:

- `pyproject.toml` is the dependency/tool configuration manifest;
- `uv.lock` is committed and treated as generated package-manager state;
- developers update dependencies through uv, not by editing lockfile internals;
- CI/deploy builds use locked/frozen installation behavior;
- ad-hoc `pip install` into the project environment is not the normal workflow;
- dependency groups separate runtime/dev/test concerns where useful.

A root uv workspace is **not** created initially because there is one Python project. If later another real Python package/application needs coordinated resolution, convert deliberately to a uv workspace with one shared lockfile.

## 5. Python source layout

Use the `src` layout:

```text
apps/api/
└── src/
    └── dante/
```

Tests import the installed/project package rather than relying on repository-root path accidents.

The application package namespace is `dante`.

## 6. Python formatting and linting

### Decision

Use **Ruff** for:

- formatting;
- linting;
- import sorting/modernization/security-adjacent lint classes where selected.

This deliberately avoids a redundant Black + isort + Flake8 stack where Ruff can enforce the same baseline coherently.

Policy:

```text
local format command
may modify files

CI format check
never modifies files

lint autofix
allowed locally for explicitly safe fixes

unsafe/broad fixes
reviewed, never applied blindly in CI
```

Ruff configuration lives in `apps/api/pyproject.toml` unless repository growth later proves a shared Python config necessary.

## 7. Python type checking

### Decision

Use **mypy** with a strict project baseline.

Pydantic's mypy integration/plugin is enabled where current supported versions require/provide value.

Principles:

- public/application boundaries are fully typed;
- untyped defs are not normal production code;
- `Any` requires a bounded integration reason, not convenience;
- `type: ignore` includes a narrow error code/reason where supported;
- third-party typing deficiencies are isolated at adapters;
- generated/provider dynamic payloads are validated into typed internal structures before meaningful use.

Strictness exceptions are path-specific and documented in config, not a global lowering of standards.

## 8. Python tests

Use **pytest** as the backend test runner.

Add purpose-specific plugins only when their real test need appears, e.g. async integration support or coverage tooling.

Use **Hypothesis** for property/state-space tests where it adds real value to invariants, parsers, temporal/recurrence logic, identifiers, state transitions or conflict behavior. It is not mandatory boilerplate for trivial functions.

## 9. Backend database stack

Implementation baseline:

```text
SQLAlchemy       2.0 stable line
PostgreSQL DBAPI psycopg 3
Migrations       Alembic
```

SQLAlchemy 2.1 pre-release/beta status is not adopted merely to be newer while 2.0 is the stable documented line.

The runtime may use SQLAlchemy async APIs with psycopg where I/O concurrency benefits the API. Pure domain/application calculations remain synchronous by default.

On Windows, canonical backend execution uses WSL2/Linux semantics; this also avoids making Windows-specific asyncio driver behavior the primary development path.

## 10. Alembic development workflow

Canonical commands are implemented during scaffold, but the workflow is fixed:

```text
change SQLAlchemy mapping/schema intent
→ generate candidate Alembic revision when useful
→ manually inspect/complete migration
→ run migration lint/checks
→ create empty PostgreSQL
→ migrate base -> head
→ run schema/integration tests
→ verify no unrepresented metadata drift
```

`alembic revision --autogenerate` is assistance, never migration approval.

`alembic check` or an equivalent deterministic drift check becomes CI evidence once metadata/migrations exist.

## 11. Node.js runtime

### Decision

```text
SUPPORTED PRODUCTION LINE
Node.js 24 LTS

INITIAL BOOTSTRAP PIN
Node.js 24.18.0
```

Node Current releases are not the default production baseline while an LTS line is available.

The exact Node runtime used in CI/EAS/development bootstrap is recorded in ecosystem-standard manifests/configuration when the JS scaffold is created.

The repository does not depend on Corepack being bundled by future Node releases. Package-manager setup must remain explicit because Corepack distribution changes across Node versions.

## 12. JavaScript package manager

### Decision

Use **pnpm**.

```text
BASELINE MAJOR
pnpm 11 stable

INITIAL BOOTSTRAP PIN
pnpm 11.20.0
```

pnpm 12 pre-release/RC is not selected for the initial production baseline.

Root files:

```text
package.json
pnpm-workspace.yaml
pnpm-lock.yaml
```

Rules:

- root `package.json` is `private`;
- `packageManager` pins the exact pnpm version;
- workspace internal dependencies use `workspace:` protocol where appropriate;
- workspace cycles are prohibited;
- CI uses `pnpm install --frozen-lockfile` or current equivalent;
- `node_modules/` is never committed.

## 13. TypeScript baseline

All production TypeScript projects run strict type checking.

Baseline configuration should include `strict: true` plus additional soundness flags where ecosystem compatibility permits, such as unchecked-index/optional-property hardening.

Exceptions are localized and justified.

Generated API types do not eliminate runtime validation at untrusted boundaries.

## 14. JavaScript lint/format

### Decision

Use:

```text
ESLint
for semantic/ecosystem-aware linting

Prettier
for deterministic formatting
```

Rationale: mature Next.js/React/Expo ecosystem integration and low surprise outweigh replacing the stack for novelty.

Shared config packages are introduced only because web + mobile create a real multi-project need.

Framework-specific rules may extend the base while preserving common security/type/import standards.

## 15. JS workspace task graph

### Decision

Use **Turborepo** for JavaScript/TypeScript workspace task dependency/caching.

Scope:

- web/mobile/packages lint/type/test/build task graph;
- local caching from the start once configured;
- cache inputs/outputs explicitly declared;
- generated artifacts participate deterministically.

Non-scope:

- Python API is not disguised as a Node package merely so Turbo can own it;
- remote Turbo cache is not required initially;
- Turbo is not a deployment orchestrator.

Root CI can invoke both native ecosystem commands independently.

## 16. Root command philosophy

Engineering Foundation intentionally does **not** select another mandatory root task-runner binary solely to alias `uv`, `pnpm` and `docker compose`.

At scaffold:

- ecosystem-native commands remain authoritative;
- a thin `tooling/scripts/` facade may be introduced only for repeated cross-ecosystem orchestration;
- if a future task runner such as `just` is added, it is a convenience facade and CI still uses/understands the underlying commands.

This avoids creating a bootstrap dependency whose only purpose is hiding three well-defined tools.

## 17. Standard logical developer operations

Regardless of exact script names created during scaffold, the repository must expose/document straightforward operations for:

```text
bootstrap dependencies
run API
run web
run mobile
typecheck
format
lint
unit tests
integration tests
full local CI-equivalent validation
start/stop local stateful dependencies
create migration
apply migration
reset LOCAL database safely
generate API client
build production artifacts
```

A new developer should not need to know undocumented command sequences to accomplish these tasks.

## 18. Docker / container development

Use current **Docker Compose v2 / Compose specification** conventions for local stateful dependencies.

Rules:

- compose project/resource names are DANTE-scoped;
- persistent volumes are local/disposable only unless explicitly documented;
- ports are configurable enough to avoid common workstation conflicts;
- health checks gate dependent integration startup where useful;
- image versions are explicit, not `latest`;
- local passwords are synthetic and clearly non-production;
- selected extensions are built/pinned into the PostgreSQL dev image when implementation begins.

## 19. Local PostgreSQL profile

Once persistence scaffold starts, LOCAL provides real PostgreSQL 18.4 with the selected extension envelope required by the implemented slice.

The local image/build must make version provenance inspectable.

Do not silently use an unpinned community “all extensions” image whose update can change PostgreSQL/PostGIS/pgvector compatibility underneath the project.

Prefer a DANTE-owned Dockerfile/build definition based on official/trusted upstream packages when the extension combination is implemented.

## 20. PgBouncer development

PgBouncer is selected Physical target but does not have to sit between every local API query from first line of code.

When pooling behavior becomes implemented/testable:

- provide a separate connection path/profile;
- exercise PSV-38/39 compatibility, especially PowerSync logical replication vs transaction pooling;
- keep direct PostgreSQL connectivity available for migration/replication classes that require it.

This is activation by implementation need, not technology reopen.

## 21. Web development

Next.js application follows the pnpm workspace.

Developer flow requires:

- fast local dev server;
- strict type/lint checks independent of dev server;
- deterministic production build in CI;
- no reliance on developer-global npm packages;
- generated API client dependency resolved from workspace;
- server/browser environment boundary validated.

## 22. Mobile development

Expo application follows the pnpm workspace.

Production-grade development uses **Expo development builds**, not Expo Go as the canonical runtime.

Local platform expectations:

- Android development supported from Windows/macOS/Linux according to current Expo/Android tooling;
- local iOS simulator/native builds require macOS, while cloud EAS builds may supply another path;
- native build profile/toolchain versions are explicit and reproducible enough to relate a binary back to source/config.

No engineer is required to commit generated native platform directories unless the selected Expo workflow explicitly changes to managed-native ownership that requires them.

## 23. Mobile E2E

Use **Maestro** as the selected native E2E flow language/runner when mobile E2E activates.

EAS-hosted Maestro workflow support may be used where stable and appropriate, but current hosted feature maturity is not allowed to make the test suite vendor-trapped. Flow files remain repository-owned and runnable against suitable local/CI simulator/emulator builds.

## 24. IDE/editor policy

No single IDE is mandatory.

Repository-level configuration should provide portable behavior through:

- `.editorconfig`;
- language manifests;
- formatter/linter configs;
- type configs;
- documented environment setup.

IDE-specific files are committed only when they provide clear team value and do not encode personal paths/secrets.

## 25. WSL2 boundary

For Windows backend work:

```text
repository checkout used by server toolchain
prefer WSL2 filesystem

Python/uv/Docker CLI/server commands
run under Linux/WSL2 semantics

Windows editor
may attach to WSL workspace
```

Avoid routinely operating one backend virtualenv from both Windows and WSL paths.

Web/mobile may use native Windows tooling where needed; shared generated/source files remain Git-normalized through `.editorconfig` and repository settings.

## 26. Line endings and text normalization

Repository text uses LF as canonical line ending unless a file format/tool explicitly requires otherwise.

`.editorconfig` / Git attributes should prevent Windows/macOS/Linux contributors from creating noisy whole-file line-ending diffs.

Executable shell scripts use LF and executable mode where applicable.

## 27. Dependency vulnerability/update automation

When manifests exist:

- GitHub dependency graph/review are used for supported ecosystems;
- Dependabot version/security updates are configured for ecosystems/versions GitHub actually supports at that time;
- pnpm 11 support is re-verified before claiming automated Dependabot update coverage;
- unsupported package-manager automation is handled by a scheduled controlled update process or another explicitly selected tool rather than downgrading the package manager silently.

No dependency bot PR is auto-merged merely because tests are green unless later governance explicitly authorizes that risk class.

## 28. Local bootstrap documentation

The production scaffold must make a clean-machine setup explicit.

Expected shape:

1. install Git;
2. install supported Docker/Compose runtime;
3. install uv;
4. install/use pinned Python;
5. install supported Node 24 LTS;
6. install pinned pnpm explicitly;
7. clone repository;
8. install locked dependencies;
9. create safe local env files from examples;
10. start stateful dependencies;
11. apply migrations/seed when those exist;
12. run local validation/smoke.

No hidden global package install should be required beyond explicitly documented toolchain prerequisites.

## 29. Reproducibility boundary

“Works on my machine” is not sufficient evidence.

A supported developer setup is reproduced by:

```text
source commit
+ pinned runtime/package-manager versions
+ committed lockfiles
+ committed container/dependency definitions
+ external local secrets/config
+ documented commands
```

CI validates the same repository-controlled contracts under Linux.

## 30. Upgrade policy

Routine upgrades:

- patch/minor dependency updates in bounded PRs;
- run all affected CI;
- regenerate committed generated code if generator changes;
- include migration/config release implications where relevant.

Major runtime/framework upgrades:

- review release/migration notes;
- verify ecosystem compatibility;
- run full affected test matrix;
- update exact runtime pins and durable docs when the supported line changes;
- do not mix unrelated architectural refactors into the upgrade unless required.

## 31. Primary-source basis

Current baseline facts were checked against official sources on 2026-08-19:

- Python 3.14.7: `https://www.python.org/downloads/release/python-3147/`
- uv: `https://docs.astral.sh/uv/`
- Ruff: `https://docs.astral.sh/ruff/`
- Node release policy: `https://nodejs.org/en/about/previous-releases`
- pnpm workspaces/releases: `https://pnpm.io/workspaces` / official pnpm releases
- SQLAlchemy 2.0: `https://docs.sqlalchemy.org/en/20/`
- Alembic: `https://alembic.sqlalchemy.org/en/latest/`
- Psycopg: `https://www.psycopg.org/psycopg3/docs/`
- Expo: `https://docs.expo.dev/`

Runtime/library facts must be revalidated when scaffold/upgrade work occurs; this document's architecture does not rely on a stale “latest” label.
