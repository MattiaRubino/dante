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
AF-01D / AF-02A / AF-02B / AF-03A PASS

FULL ACCESS/AUTH PRODUCT VERTICAL
ACTIVE UNMERGED WORKSTREAM
feature/access-auth

AI ARCHITECTURE
ACTIVE UNMERGED DESIGN / REENGINEERING WORKSTREAM
feature/ai-architecture
AI-02.1 v0.5 CANDIDATE STRUCTURAL FREEZE
ALL FOUR MEGA/PRESSURE TEST ROUNDS COMPLETE
TARGETED v0.5 CONSISTENCY VERIFICATION COMPLETE
NO MORE MEGA TESTS
NOT CLOSED
ADDITIONAL PRE-AI-03 REVIEW STILL PENDING
AI-03 NOT STARTED / BLOCKED
NO AI BACKEND / DB / PROVIDER IMPLEMENTATION CLAIMED
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
local stateful infra      Docker Compose

canonical persistence     PostgreSQL 18 major family
current patch             PostgreSQL 18.6
ORM/SQL toolkit           SQLAlchemy 2.0 stable line
driver                    psycopg 3
migrations                Alembic
current Alembic head      20260830_09
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

Current protected-main database:

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

custom enum/domain    0
sequences             0
materialized views    0
RLS policies          0
```

The pre-Recovery `20260826_08 / 68|5|14|75|95|68|120` shape remains historical evidence only.

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

A later structural database change is incomplete if these representations remain inconsistent.

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

Accepted architecture includes feature-first Web/Mobile boundaries, thin route/navigation adapters, public-API-only acyclic feature dependencies, selective shared packages, backend/PostgreSQL canonical accepted-effect authority, Web online-first, bounded Mobile local/offline state as noncanonical, identity-scoped local data and production isolation from prototypes.

Current protected-main frontend docs start at `docs/frontend/README.md`.

## Active bounded unmerged workstreams

At the 2026-09-01 reconciliation, bounded unmerged work includes:

```text
feature/access-auth             active full-stack product work
feature/home-react              active frontend work
feature/platform-observability  active platform work
feature/ai-architecture         active AI architecture design/reengineering work
```

Each unmerged branch owns only its bounded newer truth until protected-main integration. Do not infer one branch's implementation state from another branch.

PostgreSQL Recovery is not an active branch boundary: CP01–CP07 are closed and the accepted LOCAL recovery implementation is integrated into `main` via PR #47.

## AI architecture checkpoint

Current branch-local AI authority is layered:

```text
docs/architecture/dante-ai-foundation.md
→ AI-00 semantic / architectural baseline

docs/architecture/ai-production-engineering-state-of-the-art-2026.md
→ production-engineering research / NON-DANTE-DECISION

docs/architecture/dante-ai-02-1-intelligence-reengineering.md
→ AI-02.1 v0.5 CANDIDATE STRUCTURAL FREEZE / NOT CLOSED
```

The v0.5 candidate incorporates all completed simulation/kill-test rounds and the final isolation/runtime hardening. It preserves:

```text
DANTE != model/provider/chat transcript
PostgreSQL = sole canonical persistence/material-history authority
MODEL OUTPUT != PUBLISHABLE OUTPUT
DISPLAY NAME != EFFECT TARGET
Interaction Session != Run != Worker
SUPERSEDE != CANCEL != ROLLBACK != RECONCILE
Context access != disclosure permission
Scenario state != canonical current state
ChangeSet != bypass of individual effect governance
DANTE representation != external System-of-Record authority
SENT != DELIVERED != SEEN != ACKNOWLEDGED != ACCEPTED
Execution Environment != mandatory sandbox/container
```

AI-02.1 is not an implementation claim. Exact model/provider/SDK, runtime technology, sandbox implementation and AI-03 Context/Retrieval/Memory design remain later evidence-driven work.

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
→ implemented and directly rehearsed; integrated via PR #47

remote backup provider
→ TBD; activate and prove only at a real production deployment boundary

AI Execution Environment isolation
→ activate only for workloads/threat models that require it
```

Selected architecture is not the same thing as activated implementation or direct PASS.

## Protected `main`

Protected-main policy is repository-enforced. Use the live GitHub ruleset as authority rather than a stale documentation snapshot. Integration remains PR-based and must respect required checks and branch protection.

## Environment model

Exactly:

```text
LOCAL
DEV
UAT
PROD
```

Environment != Git branch.

## Documentation lifecycle

Current specifications describe current truth directly. Historical evidence remains explicitly historical; temporary live/session handoffs do not merge into protected `main`; Git preserves complete chronology; frozen split specifications may be compacted only when lossless knowledge coverage is proven.

Normative lifecycle source:

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

Persistent truth rules:

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
