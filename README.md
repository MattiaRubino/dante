# DANTE

DANTE is a personal operating system designed to help people understand, organize and improve real life by turning intentions, needs and possibilities into outcomes they can realistically pursue.

**Compass:** *Understand life. Shape what comes next.*

## Current state

```text
PRODUCT / NORTH STAR
CURRENT

DOMAIN MODEL
CLOSED / SEMANTICALLY COMPLETE FOR CURRENT SCOPE

LOGICAL MODEL
CLOSED / 57 OF 57 CLASSIFIED
WL-H01..WL-H12 REMAIN BINDING

PHYSICAL TARGET
CLOSED / SELECTED / ACCEPTED
PostgreSQL 18 major family is canonical persistence/material-history authority
Physical phase-time exact patch 18.4 / historical evidence

ENGINEERING FOUNDATION
CLOSED / ACCEPTED

FRONTEND ENGINEERING FOUNDATION
CLOSED / ACCEPTED / INTEGRATED VIA PR #22

FRONTEND MATERIALIZATION
CLOSED / PASS / INTEGRATED VIA PR #28

PRODUCTION BACKEND SCAFFOLD
CP1–CP5 CLOSED / DIRECT QA PASS / INTEGRATED VIA PR #24

CP6 — CONCRETE POSTGRESQL DATABASE
CLOSED / DIRECT QA PASS / INTEGRATED VIA PR #42

CURRENT POSTGRESQL
18.6

HISTORICAL PRE-RECOVERY CP6 DATABASE BASELINE
Alembic 20260826_08
68 tables / 5 views / 14 routines / 75 triggers /
95 physical indexes / 68 FKs / 120 CHECKs

CURRENT PROTECTED-MAIN DATABASE / RECOVERY BASELINE
Alembic 20260830_09
69 tables / 5 views / 15 routines / 76 triggers /
97 physical indexes / 69 FKs / 123 CHECKs
PostgreSQL recovery CP01–CP07 LOCAL PASS / CLOSED
Recovery integrated via PR #47
remote backup provider TBD / NOT ACTIVATED
production/cloud recovery NOT CLAIMED

ACCESS PRE-BACKEND FRONTEND
CLOSED / ACCEPTED / RELEASE-HARDENED
AF-01D PASS / AF-02A PASS / AF-02B PASS / AF-03A PASS

FULL ACCESS/AUTH PRODUCT VERTICAL
ACTIVE UNMERGED WORKSTREAM EXISTS / NOT CLAIMED CLOSED
branch-local truth lives on feature/access-auth
```

For exact current truth use `docs/PROJECT-STATUS.md`. Do not reconstruct current state from old phase documents, historical workstream continuations or conversation memory.

## Repository

Production development continues in the single monorepo:

```text
MattiaRubino/dante
```

Accepted ownership boundaries:

```text
apps/
├── backend/
├── web/
└── mobile/
packages/
infra/
tooling/
tests/system/
docs/
prototypes/
.github/
```

These are ownership boundaries, not an instruction to create empty ceremonial directories.

- `apps/backend` owns the server application;
- `apps/web` and `apps/mobile` are sibling client boundaries;
- `packages/` contains only real multi-consumer packages;
- `infra/` owns infrastructure definitions when real infrastructure exists, never business logic;
- production applications do not import from `prototypes/`;
- do not create a second implementation repository for normal product development.

## Backend baseline

```text
Python                   3.14.x
initial exact pin         3.14.7
package manager           uv
source root               apps/backend/src/dante
format/lint               Ruff
type checking             mypy strict
testing                   pytest + Hypothesis where meaningful
server semantics          Linux
Windows workflow          WSL2/Linux
IDE                       PyCharm with WSL interpreter supported
local stateful infra      Docker Compose

canonical persistence     PostgreSQL 18 major family
current patch             PostgreSQL 18.6
ORM/SQL toolkit           SQLAlchemy 2.0 stable line
driver                    psycopg 3
migrations                Alembic
```

Current database roles:

```text
dante_owner      NOLOGIN ownership identity
dante_migrator   LOGIN migration identity
dante_runtime    LOGIN application runtime identity
```

The outer application-operation boundary owns commit/rollback. Persistence adapters may flush but never commit implicitly. No generic `Repository[T]`, generic Unit of Work, BaseService or service-locator architecture is introduced merely for uniformity.

Backend entry point:

- `apps/backend/README.md`

## Concrete PostgreSQL database

CP6 is complete and integrated into protected `main` through PR #42. PostgreSQL Recovery was subsequently integrated through PR #47 without reopening CP6.

The historical pre-recovery CP6 baseline was:

```text
PostgreSQL          18.6
Alembic head        20260826_08

tables              68
views                5
routines             14
triggers             75
physical indexes    95
foreign keys         68
CHECK constraints   120

custom enum/domain    0
sequences             0
materialized views    0
RLS policies          0
```

The current protected-main database after Recovery integration is:

```text
PostgreSQL          18.6
Alembic head        20260830_09

tables              69
views                5
routines             15
triggers             76
physical indexes    97
foreign keys         69
CHECK constraints   123
```

PR #47 integrated the Recovery evolution into protected `main` with merge commit `bdd2b2370d41423dbaecd00fde86bb2bf2466f2b`. The Recovery branch is historical after integration; current database truth is the protected-main contract above.

Final CP6 acceptance included:

```text
Ruff format/check                    PASS
mypy strict                          PASS
non-PostgreSQL tests                 37 / 37 PASS
real PostgreSQL tests                76 / 76 PASS
build                                PASS
Dictionary JSON-Schema               PASS
Dictionary ↔ SQLAlchemy              PASS
Dictionary ↔ Alembic                 PASS
Dictionary ↔ live PostgreSQL         PASS
persistent LOCAL upgrade/restart     PASS
security / ACL posture               PASS
GET /health/live                     200
GET /health/ready                    200
```

Current database documentation starts at:

- `docs/database/README.md`
- `docs/database/dictionary/README.md`
- `docs/database/dictionary/scope.json`

Permanent consistency rule:

```text
Database Architecture & Reference
≈ Database Dictionary
≈ SQLAlchemy metadata / mappings
≈ Alembic head
≈ real PostgreSQL schema
```

A later schema change is incomplete if these representations remain inconsistent.

Historical exact PostgreSQL 18.4 evidence for the Physical/CP2/CP3 phases remains historical truth. Current patch 18.6 does not rewrite what executed on 18.4.

## Frontend baseline

```text
Node 24 LTS
TypeScript 6.0.x strict
pnpm 11
Turborepo 2.x

Web
React 19.2 + React DOM
Vite 8
TanStack Router

Mobile
React Native 0.86
Expo SDK 57
Expo Router

Data / forms / validation
PowerSync + encrypted SQLite when activated
TanStack Query 5
TanStack Form
Zod 4
Orval 8 when real OpenAPI exists
```

Accepted architecture includes:

- feature-first Web/Mobile applications;
- thin route/navigation adapters;
- public-API-only acyclic feature dependencies;
- shared packages only for real multi-consumer value;
- backend + PostgreSQL as canonical accepted-effect authority;
- Web online-first baseline;
- Mobile bounded local/offline state as noncanonical;
- identity-scoped local data;
- platform-specific UI implementations over shared semantic tokens;
- production code never importing prototypes.

Current protected-main frontend docs start at:

- `docs/frontend/README.md`

## Access frontend baseline

The completed pre-backend Access frontend materialization is the accepted Web baseline consumed by the active unmerged full-stack Access/Auth workstream.

Accepted checkpoints:

```text
AF-01D  shell completion / professional polish      PASS
AF-02A  complete pre-backend frontend state graph   PASS
AF-02B  downstream surface hardening                PASS
AF-03A  release-hardening viewport matrix           PASS
```

Current durable Access frontend authority:

- `docs/frontend/access.md`
- `apps/web/src/features/access/`
- `apps/web/e2e/access.spec.ts`

The frontend deliberately stops backend-authoritative transitions rather than fabricating account/session/authentication success.

The whole Access/Auth product vertical is **not claimed closed here**. An active unmerged `feature/access-auth` workstream exists; its branch-local docs, code and tests own the newer Auth state. This global file must not freeze its sub-checkpoints.

## Post-CP6 product direction

There is no remaining CP6 design/materialization step. Post-CP6 work proceeds through bounded product/platform workstreams and normal forward schema evolution when genuinely required.

PostgreSQL Recovery is no longer an active branch boundary: CP01–CP07 are closed and the accepted LOCAL recovery implementation is integrated into protected `main` via PR #47.

At the 2026-08-31 reconciliation, active unmerged workstreams include:

```text
feature/access-auth
feature/home-react
feature/platform-observability
```

Each unmerged branch owns only its bounded newer truth. Protected `main` remains the integrated authority; live Git refs determine later movement.

A product vertical consumes the existing database and evolves it only through reviewed forward migrations plus the same-change Database System-of-Record rule. CP6 is not reopened.

## Capability-triggered components

Selected specialist components remain dormant until a real consuming boundary exists:

```text
PowerSync + encrypted SQLite
→ real offline/multi-device capability

PostgreSQL transactional outbox
→ real Class-A async requirement

R2
→ real ContentArtifact byte flow

OR-Tools
→ solver-backed capability

Restate
→ first real Class-B durable workflow

PgBouncer
→ demonstrated connection-management need

pgBackRest LOCAL recovery
→ implemented and directly rehearsed; integrated into main via PR #47

remote backup provider
→ TBD; activate and prove only at the real production deployment boundary
```

Selected architecture is not the same thing as activated implementation or direct PASS.

## Protected `main`

The effective `lifeos-main-safety` ruleset requires:

```text
PR before integration
normal merge commit only
branch up to date with main
review threads resolved
non-fast-forward protection
no bypass actor

required checks:
Backend CI Gate
Dependency Review
Frontend CI Gate
```

Do not use squash, rebase or force-push as a shortcut around protected-main policy.

The live GitHub ruleset is enforcement authority; a documentation snapshot is informative only and must not override live remote state.

## Environment model

Exactly:

```text
LOCAL
DEV
UAT
PROD
```

Environment != Git branch.

Activation remains progressive. Provider-specific infrastructure is selected/materialized only when the real deployment or operational boundary requires it.

## Documentation lifecycle

DANTE documentation is part of the implementation, but the working tree is not a chat transcript.

Rules:

```text
current specifications describe current truth directly
historical evidence is clearly labelled
active branch handoffs stay branch-local
temporary live/session handoffs do not merge into main
completed workstreams retain at most one useful branch-history narrative
Git remains complete recoverable history
frozen split documents may be compacted only losslessly
```

Normative policy:

- `docs/development/documentation-lifecycle-policy.md`

Historical archive boundary:

- `docs/archive/README.md`

## Where to start

General continuation order:

1. `README.md`
2. `docs/README.md`
3. `docs/PROJECT-STATUS.md`
4. `docs/ROADMAP.md`
5. `docs/development/agent-operating-manual.md`
6. `docs/development/operating-rules.md`
7. `docs/development/documentation-and-handoff.md`
8. `docs/development/documentation-lifecycle-policy.md`
9. `docs/development/branching-and-environments.md`
10. `docs/development/repository-engineering-safety.md`
11. the current subsystem/workstream authority
12. current branch/ref and relation to protected `main`

Backend/database continuation:

- `apps/backend/README.md`
- `docs/database/README.md`
- `docs/database/dictionary/README.md`
- `docs/development/backend-cp6-05-whole-database-qa.md`

Access frontend baseline:

- `docs/frontend/access.md`
- `apps/web/src/features/access/`
- `apps/web/e2e/access.spec.ts`

## Persistent truth rules

```text
SELECTED ARCHITECTURE != IMPLEMENTED COMPONENT
DOCUMENTATION PASS != DIRECT IMPLEMENTATION PASS
UNMERGED BRANCH TRUTH != PROTECTED-main TRUTH
HISTORICAL 18.4 EVIDENCE != CURRENT 18.6 EXECUTION CLAIM
CLIENT LOCAL STATE != CANONICAL ACCEPTED EFFECT
DATABASE MATERIALIZATION != PRODUCT APPLICATION IMPLEMENTATION
ENVIRONMENT != GIT BRANCH
TEMPORARY HANDOFF != DURABLE DOCUMENTATION
```

The goal is a repository a new developer or agent can understand from current sources without reconstructing obsolete operational chronology.
