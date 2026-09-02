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
WL-H01..WL-H12 BINDING

PHYSICAL TARGET
CLOSED / SELECTED / ACCEPTED
PostgreSQL 18 major family = sole canonical persistence/material-history authority

ENGINEERING FOUNDATION
CLOSED / ACCEPTED

FRONTEND ENGINEERING FOUNDATION
CLOSED / INTEGRATED VIA PR #22

FRONTEND MATERIALIZATION
CLOSED / PASS / INTEGRATED VIA PR #28

PRODUCTION BACKEND SCAFFOLD
CP1–CP5 CLOSED / DIRECT QA PASS / INTEGRATED VIA PR #24

CP6 — CONCRETE POSTGRESQL DATABASE
CLOSED / DIRECT QA PASS / INTEGRATED VIA PR #42

CURRENT POSTGRESQL
18.6

CURRENT PROTECTED-MAIN DATABASE / RECOVERY BASELINE
Alembic 20260830_09
69 tables / 5 views / 15 routines / 76 triggers /
97 indexes / 69 FKs / 123 CHECKs
PostgreSQL Recovery CP01–CP07 LOCAL PASS / CLOSED
Recovery integrated via PR #47
remote backup provider TBD / NOT ACTIVATED
production/cloud recovery NOT CLAIMED

ACCESS PRE-BACKEND FRONTEND
CLOSED / ACCEPTED / RELEASE-HARDENED

FULL ACCESS/AUTH PRODUCT VERTICAL
ACTIVE UNMERGED WORKSTREAM
feature/access-auth

AI ARCHITECTURE DESIGN / REENGINEERING
CLOSED / STRUCTURALLY ACCEPTED ON feature/ai-architecture
AI-00 COMPLETE
AI-02.1 CLOSED / STRUCTURALLY ACCEPTED
AI-03 CLOSED / C01..C33 / B01..B35 / MAT-01..MAT-15
AI-04 CLOSED / A01..A30 / EV01..EV20 / RT-01..RT-31 / PA-01..PA-61 / WP-01..WP-22
PRE-AI05 CLOSED / PRE05-H01..H19
AI-05A CLOSED / BD-01..BD-41
AI-05B CLOSED / AI05B-H01..H15
AI-05 WHOLE-SYSTEM CLOSED / STRUCTURALLY ACCEPTED
POST-AI05 HARDENING CLOSED / POST05-H01..H25
MKT-001..MKT-100 PASS
C01..C20 COMPOUND PASS
REVERSE AUTHORITY PASS
PRODUCT/SIMULATION REPLAY PASS

CURRENT AI IMPLEMENTATION AUTHORITY
docs/architecture/dante-ai-implementation-baseline-final.md

NEXT AI WORK
ACTUAL AI IMPLEMENTATION WORKSTREAM
I0 repository/application ownership + architecture-test skeleton

AI BACKEND / PROVIDER / PRODUCTION ACTIVATION
NOT IMPLEMENTED / NOT CLAIMED
```

For exact current truth use `docs/PROJECT-STATUS.md`. Do not reconstruct current state from old phase documents or conversation memory.

## Repository

Production development continues in the single monorepo:

```text
MattiaRubino/dante
```

Accepted root ownership:

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
- `infra/` owns infrastructure definitions, never business logic;
- production applications do not import from `prototypes/`;
- normal product development remains in this monorepo.

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

The outer application-operation boundary owns commit/rollback. Persistence adapters may flush but never commit implicitly. No generic Repository/UoW/BaseService/service-locator architecture is introduced for uniformity.

Backend entry point: `apps/backend/README.md`.

## Concrete PostgreSQL database

Current protected-main database:

```text
PostgreSQL          18.6
Alembic head        20260830_09
tables              69
views                5
routines             15
triggers             76
physical indexes     97
foreign keys         69
CHECK constraints    123
custom enum/domain    0
sequences             0
materialized views    0
RLS policies          0
```

Database documentation begins at:

- `docs/database/README.md`;
- `docs/database/dictionary/README.md`;
- `docs/database/dictionary/scope.json`.

Permanent consistency rule:

```text
Database Architecture & Reference
≈ Database Dictionary
≈ SQLAlchemy metadata/mappings
≈ Alembic head
≈ real PostgreSQL schema
```

A later structural change is incomplete if these representations remain inconsistent.

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

Current frontend documentation starts at `docs/frontend/README.md`.

## Active bounded unmerged workstreams

```text
feature/access-auth             active full-stack product work
feature/home-react              active frontend work
feature/platform-observability  active platform work
feature/ai-architecture         architecture design CLOSED / implementation handoff ready
```

Each branch owns only its bounded newer truth until protected-main integration.

## AI architecture / implementation boundary

Current final implementation-facing authority:

```text
docs/architecture/dante-ai-implementation-baseline-final.md
```

Final independent structural acceptance:

```text
docs/architecture/dante-ai-post05-final-mega-acceptance.md
```

The post-AI05 mega pass found no need for a new Domain root, Logical/Physical reopen, PostgreSQL/Alembic change, generic AI persistence, provider preselection or agent framework.

Accepted implementation split:

```text
modules/search
→ independent deterministic Global Search/discovery
→ permission-safe bounded read projection
→ no canonical mutation authority

modules/intelligence
→ Work/Context/Reference/SemanticQuery/Retrieval orchestration
→ optional governed ModelAccess
→ Verification / Result Maturity / explicit NO_EFFECT / Safe Publication
→ no raw database/canonical business ownership

provider SDK/protocol
→ private admitted outbound adapter behind ModelAccessPort
```

Binding examples:

```text
GLOBAL SEARCH != INTELLIGENCE
SEARCH RESULT / CURSOR / TARGET REF != AUTHORIZATION
SEMANTIC QUERY GATEWAY != INTELLIGENCE-OWNED CROSS-CAPABILITY SQL
Context != Retrieval != Memory
RetrievalCandidate != ContextFragment
DATA != INSTRUCTION
MASKING / REDACTION != SEMANTIC EQUIVALENCE
MODEL OUTPUT != PUBLISHABLE OUTPUT
PROVIDER COMPLETED != VERIFIED != PUBLISHABLE
PROVIDER FAILURE != DISCLOSURE DID NOT HAPPEN
AUXILIARY MODEL CALL != FREE PROVIDER CALL
CANDIDATE ADMISSION != PRODUCTION QUALIFICATION
DEFAULT NONCANONICAL PERSISTENCE = NO
BUILD-READY != INTEGRATION-READY != ACTIVATION-READY
```

First implementation target:

```text
Global Search subset
+ read-only Ask DANTE

private authenticated in-app
single-turn
inline/request-owned
READ_ONLY
public streaming OFF
background/durable resume OFF
consequential mutation OFF
```

No provider/model/SDK is selected yet.

## Capability-triggered components

Remain dormant until real consumers/proofs exist:

```text
PowerSync + encrypted SQLite
PostgreSQL transactional outbox
R2
OR-Tools
Restate
PgBouncer
FTS / pg_trgm
pgvector / ANN / embeddings
MCP / A2A
AI Execution Environment
cross-Run prior-disclosure accounting
AI memory persistence
external result streaming
multi-provider hedging
```

Selected target != implemented/activated component.

## Environment model

Exactly:

```text
LOCAL
DEV
UAT
PROD
```

Environment != Git branch.

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
11. current subsystem/workstream authority
12. current branch/ref relation

For AI implementation, continue through:

- `docs/architecture/dante-ai-implementation-baseline-final.md`;
- `docs/architecture/dante-ai-post05-final-mega-acceptance.md`;
- `docs/workstreams/ai-architecture.md`.

Current exact AI next action:

```text
I0
→ repository/application ownership + architecture-test skeleton
```

Persistent truth rules:

```text
SELECTED != IMPLEMENTED
DOCUMENTATION PASS != RUNTIME PASS
UNMERGED BRANCH TRUTH != PROTECTED-main TRUTH
CLIENT LOCAL STATE != CANONICAL ACCEPTED EFFECT
MODEL TARGET != PROVIDER != MODEL != DEPLOYMENT
HARNESSPROFILE != PROVIDERBINDING
BUILD-READY != ACTIVATION-READY
TEMPORARY HANDOFF != DURABLE DOCUMENTATION
```