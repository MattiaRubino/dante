# Repository Layout v0

- Status: **CLOSED / ACCEPTED**
- Scope: production repository topology and path ownership
- Production scaffold: **NOT CREATED YET**

## 1. Decision

DANTE uses one product monorepo with explicit ownership by path.

The repository root is coordination space, not an application source directory.

Target topology:

```text
/
├── apps/
│   ├── backend/
│   │   ├── pyproject.toml
│   │   ├── uv.lock
│   │   ├── .python-version
│   │   ├── Dockerfile                 # when deployment packaging begins
│   │   ├── src/
│   │   │   └── dante/
│   │   ├── migrations/
│   │   │   └── versions/
│   │   └── tests/
│   │       ├── unit/
│   │       ├── application/
│   │       ├── integration/
│   │       ├── architecture/
│   │       └── contract/
│   │
│   ├── web/                           # internal structure deferred
│   └── mobile/                        # internal structure deferred
│
├── packages/                          # only genuinely shared artifacts/contracts
├── infra/
│   ├── local/
│   │   └── postgres/
│   │       ├── Dockerfile             # when scaffolded
│   │       └── config/                # exact shape implementation-owned
│   ├── compose/                       # local stateful topology
│   └── iac/                           # remote desired state; engine deferred
│       ├── modules/                   # only when reusable modules exist
│       └── environments/
│           ├── dev/
│           ├── uat/
│           └── prod/
│
├── tooling/
├── tests/
│   └── system/
├── docs/
├── prototypes/
├── .github/
│   └── workflows/
├── .editorconfig                      # when scaffolded
├── .gitignore
└── README.md
```

This is an ownership model, not an instruction to create empty ceremonial directories. Git paths are created only when real content exists.

## 2. `apps/backend`

`apps/backend` is the DANTE server/backend modular monolith.

It owns:

- Python runtime manifest/lock/pin;
- FastAPI process/bootstrap/composition;
- backend capability modules;
- database persistence mappings/adapters;
- Alembic migration history;
- backend-local tests;
- backend OCI image definition when deployment packaging begins.

It does not own:

- web/mobile UI implementation;
- frontend package-manager/task-runner decisions;
- provider infrastructure desired state;
- repository-global tooling;
- prototypes.

Naming rule:

```text
apps/backend
```

is canonical. `apps/api` is not used as the backend root because HTTP API is one adapter of the backend, not the identity of the entire server application.

## 3. `apps/web` and `apps/mobile`

The monorepo reserves sibling application boundaries:

```text
apps/web
apps/mobile
```

This foundation intentionally does **not** freeze their internal tree, Node/package-manager choices, task graph, testing stack, build profiles or shared-UI design.

Those decisions belong to the frontend workstream after current frontend design/prototype work is ready.

Production code must never depend on `prototypes/` by identity. Moving prototype ideas into production requires deliberate implementation/review.

## 4. `packages/`

`packages/` contains only artifacts/contracts with a real multi-consumer or durable-generation need.

Potential classes may include generated API contracts/types, design tokens or other platform-neutral assets, but exact package names/technology are deferred to the consumer workstream.

Forbidden generic dumping-ground conventions:

```text
packages/shared
packages/common
packages/utils
packages/helpers
```

unless a future bounded scope gives such a package a precise, non-generic responsibility.

Python backend code remains inside `apps/backend` until a genuinely independently reusable/versionable Python package exists.

## 5. `infra/`

`infra/` owns infrastructure definitions, never DANTE business logic.

### `infra/local/postgres`

Owns the reproducible LOCAL PostgreSQL build/configuration when scaffolded.

Required baseline capability:

```text
PostgreSQL 18.4
PostGIS 3.6.4
pgvector 0.8.6
pg_trgm
unaccent
pg_stat_statements + preload configuration
native full-text search
```

All selected extensions are enabled from the first LOCAL database. Application use may remain dormant until a real feature needs the capability.

### `infra/compose`

Owns local stateful-dependency orchestration.

Backend application process is not required to run inside Compose during the normal inner loop.

### `infra/iac`

Owns remote infrastructure desired state once remote infrastructure exists.

Conceptual environment composition:

```text
infra/iac/environments/dev
infra/iac/environments/uat
infra/iac/environments/prod
```

Exact IaC engine and provider are deferred. No placeholder Terraform/OpenTofu/Pulumi files are created merely to fill the tree.

Secrets never live in desired-state files as plaintext.

## 6. `tooling/`

`tooling/` may contain deterministic repository engineering utilities such as:

- bootstrap/validation scripts;
- fixture generation;
- migration/recovery helpers;
- contract/code generation;
- CI support tooling.

It must not become a hidden application layer or own canonical business logic.

## 7. Test ownership

Tests live with what they validate.

```text
apps/backend/tests/*
backend unit/application/integration/architecture/contract tests

apps/web/... and apps/mobile/...
frontend-specific test placement decided by frontend workstream

/tests/system/*
true black-box/cross-application/deployed-system validation only
```

Root `tests/` is not a general bucket for backend unit tests.

Test fixtures are synthetic by default and never contain ad-hoc raw production database dumps.

## 8. Documentation and prototypes

### `docs/`

Durable project memory/authority. Code changes that alter accepted architecture or operating contract update relevant documentation in the same bounded PR.

### `prototypes/`

Explicitly non-production.

Rules:

- production apps do not import prototype code;
- prototypes do not override main architecture authority;
- accepted prototype behavior is deliberately reimplemented/migrated into `apps/*` under implementation scope.

## 9. Generated artifact policy

### Generated and committed

Use only when reviewability/reproducibility/offline consumption materially benefit.

Requirements:

- deterministic generator;
- generator/tool version pinned;
- source input traceable;
- generated marker where feasible;
- CI can regenerate and prove clean diff.

### Generated locally/build-time and ignored

Examples:

```text
.venv/
coverage output
cache/build directories
local database volumes
temporary reports
IDE/machine-local state
```

Frontend-specific generated paths are deferred to the frontend workstream.

### CI/release artifacts

OCI images, test reports, SBOMs/attestations and future client binaries belong in the appropriate artifact/release store rather than ordinary Git history.

## 10. Ignore/normalization policy

Commit:

- lockfiles;
- migrations;
- durable infrastructure definitions;
- selected committed generated contracts.

Ignore:

- secrets;
- machine-local state;
- reproducible transient build/test/cache output;
- local stateful volumes.

Repository text uses LF where ecosystem/file rules permit. `.editorconfig`/Git attributes are introduced with the scaffold to prevent cross-platform line-ending churn.

## 11. Dependency direction by top-level path

```text
apps/* may consume explicitly shared packages/contracts
packages/* --X--> apps/*
infra/* may reference deployable artifact identity
infra/* --X--> application source imports
tooling/* may invoke engineering interfaces
tooling/* --X--> canonical business-logic ownership
production apps --X--> prototypes/*
```

No application imports another application's private implementation merely because it is in the same monorepo.

## 12. Ownership before team growth

The repository is currently owner-driven. `CODEOWNERS` and required independent reviewers are not manufactured while there is no independent reviewer/owner capacity.

When real maintainers/teams appear, path ownership/review requirements can be introduced at stable application/module/security boundaries.

## 13. Repository identity

The current repository is retained.

```text
NEW REPOSITORY FOR IMPLEMENTATION
NO
```

The historical GitHub repository name `lifeos` may be renamed to `dante` in a separate governance scope. Repository rename is not performed by this document.

## 14. Scaffold gate

The first production scaffold after Engineering Foundation closure must enumerate exact created/modified paths and create only real files required by the approved backend baseline.

No empty-folder forest and no placeholder architecture for future frontend/cloud work.
