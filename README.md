# DANTE

DANTE is a personal operating system designed to help people understand, organize and improve their real life by turning intentions, needs and possibilities into outcomes they can realistically pursue.

**Compass:** *Understand life. Shape what comes next.*

## Current state

```text
PRODUCT / NORTH STAR
CURRENT

DOMAIN MODEL
CLOSED

LOGICAL MODEL
CLOSED
WL-H01..WL-H12 ACTIVE

PHYSICAL TARGET
CLOSED / SELECTED / ACCEPTED

ENGINEERING FOUNDATION v0
CLOSED / ACCEPTED

FRONTEND ENGINEERING FOUNDATION
DESIGN / ARCHITECTURE CLOSED / ACCEPTED / FINAL REVIEW PASS
INTEGRATED VIA PR #22
PRODUCTION FRONTEND CODE NOT STARTED
DIRECT FRONTEND VALIDATION NOT RUN

PRODUCTION BACKEND SCAFFOLD
NOT STARTED

DIRECT SELECTED-STACK VALIDATION / PSV
NOT RUN
```

Architecture/design closure never implies implementation PASS.

## Production repository direction

DANTE continues in this repository as one product monorepo.

Accepted conceptual root ownership:

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

These are ownership reservations, not an instruction to create empty directories.

- `apps/backend` is the server-side application boundary;
- `apps/web` and `apps/mobile` are sibling client boundaries;
- `infra/` owns infrastructure definitions when materialized, never business logic;
- production apps do not import from `prototypes/`;
- do **not** create a new implementation repository.

## Backend engineering baseline

```text
Python                 3.14.x
initial pin             3.14.7
package manager         uv
source root             apps/backend/src/dante
format/lint             Ruff
type checking           mypy strict
unit/integration runner pytest
property testing        Hypothesis where meaningful

server semantics        Linux
Windows workflow        WSL2/Linux
primary user IDE        PyCharm with WSL interpreter supported
local stateful infra    Docker Compose

canonical persistence   PostgreSQL 18.4
ORM/SQL toolkit         SQLAlchemy 2.0 stable line
driver                  psycopg 3
migrations              Alembic
```

First LOCAL PostgreSQL baseline includes the full accepted extension envelope when materialized.

## Frontend engineering baseline — closed design / integrated

Technology direction:

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

Data
PowerSync + encrypted SQLite
TanStack Query 5
TanStack Form
Zod 4
Orval 8
```

Architecture direction:

- feature-first Web/Mobile;
- thin route/navigation adapters;
- public-API-only and acyclic dependencies;
- small shared packages only with real consumers;
- framework-free shared client cores by default;
- formal Data Authority Matrix;
- backend/PostgreSQL retains canonical accepted-effect authority;
- feature data firewall isolates API/Query/PowerSync/storage mechanics;
- Mobile PowerSync local/offline path when materialized;
- Web online-first; PowerSync Web dormant;
- browser PWA/service worker dormant;
- identity-scoped local database lifecycle;
- separate Web/Native DANTE UI implementations with shared semantic tokens;
- React-free shared i18n core;
- Temporal-based time boundary;
- versioned/fail-fast Web runtime public config;
- GitHub Actions primary CI/CD;
- one authoritative WSL-backed checkout posture.

Frontend authorities integrated on `main` via PR #22:

- `docs/architecture/frontend-engineering-foundation.md`;
- `docs/architecture/frontend-engineering-foundation-part-2.md`;
- `docs/architecture/frontend-engineering-foundation-final-review.md`;
- `docs/decisions/ADR-008-frontend-engineering-stack.md`;
- `docs/decisions/ADR-009-frontend-architecture-boundaries.md`;
- `docs/workstreams/frontend-foundation.md`.

## Environment model

```text
LOCAL
DEV
UAT
PROD
```

Environments are not Git branches. Frontend/mobile provider profiles map to these contexts.

## Selected Physical target remains unchanged

PostgreSQL remains canonical. PowerSync/SQLite is bounded noncanonical local/sync state. Class-A async uses transactional outbox when needed; Restate remains selected/dormant until real Class-B work; R2, recovery, solver and observability targets retain their accepted activation boundaries.

## Testing and delivery

GitHub Actions is repository-wide primary CI/CD. Required checks activate only after real stable emitted contexts exist.

Frontend direct validation is intentionally **NOT RUN** until the closed Foundation is materialized under a new bounded scope.

## Direct evidence truth

```text
DATABASE DEPLOYMENT      NOT STARTED
BACKEND SCAFFOLD         NOT STARTED
FRONTEND SCAFFOLD        NOT STARTED
CONCRETE DB SCHEMA       NOT STARTED
MIGRATION IMPLEMENTATION NOT STARTED
DIRECT HG                NOT RUN
FRONTEND DIRECT TEST     NOT RUN
PSV                      NOT RUN
PRODUCTION DEPLOYMENT    NOT STARTED
```

## Where to continue

Read before the next write:

1. `docs/README.md`
2. `docs/PROJECT-STATUS.md`
3. development operating/safety/handoff rules
4. `docs/workstreams/frontend-foundation.md`
5. both frontend engineering specs + final review + ADR-008/ADR-009
6. closed Engineering Foundation/repository layout
7. accepted Physical sources/register as applicable.

### Exact next boundary

```text
FRONTEND
open a fresh bounded materialization/scaffold/direct-validation workstream
→ materialize only accepted real workspace/app/package artifacts
→ execute carried direct validations progressively

BACKEND
production scaffold remains separate and NOT STARTED
```

Do not reopen closed Product/Domain/Logical/Physical/Engineering/Foundation decisions by default.
