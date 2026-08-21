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

FRONTEND MATERIALIZATION
ACTIVE ON feature/frontend-materialization
DIRECT FRONTEND VALIDATION NOT YET EARNED

PRODUCTION BACKEND SCAFFOLD
ACTIVE
CP1 CLOSED / DIRECT QA PASS
CP2 CLOSED / DIRECT QA PASS
CP3 CLOSED / DIRECT QA PASS
CP4 DESIGN CLOSED
CP4 M1/M2/M3 COMPLETE
CP4 MATERIALIZED / DIRECT LOCAL QA PASS
CURRENT MAIN RECONCILED
POST-MERGE REGRESSION QA NEXT
REMOTE PR CALIBRATION NOT RUN

CONCRETE LOGICAL → POSTGRESQL IMPLEMENTATION
NOT STARTED

DIRECT SELECTED-STACK VALIDATION / PSV
NOT RUN BEYOND EXPLICITLY RECORDED SCAFFOLD ACCEPTANCE
```

Architecture/design closure never implies implementation PASS. Direct PASS is recorded only where the relevant artifact or scenario has actually run.

## Production repository direction

DANTE continues in this repository as one product monorepo.

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

These are ownership boundaries, not an instruction to create empty directories.

- `apps/backend` is the server-side application boundary;
- `apps/web` and `apps/mobile` are sibling client boundaries;
- `infra/` owns infrastructure definitions when materialized, never business logic;
- production apps do not import from `prototypes/`;
- do **not** create a second implementation repository.

Repository identity governance is complete: `MattiaRubino/lifeos` is historical identity and production implementation continues in `MattiaRubino/dante`.

## Backend engineering baseline

```text
Python                 3.14.x
current scaffold pin    3.14.7
package manager         uv 0.12.5 exact project requirement
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

The materialized LOCAL PostgreSQL baseline uses the accepted extension envelope:

- PostGIS 3.6.4;
- pgvector 0.8.6;
- `pg_trgm`;
- `unaccent`;
- `pg_stat_statements` with preload configuration;
- native PostgreSQL full-text search.

PostgreSQL remains the sole canonical persistence and material-history authority.

## Frontend engineering baseline — closed design / integrated

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

Accepted frontend architecture includes feature-first Web/Mobile, thin route/navigation adapters, public-API-only acyclic dependencies, small real-consumer shared packages, a formal Data Authority Matrix, a feature data firewall, Mobile PowerSync local/offline posture, Web online-first posture, identity-scoped local storage, separate Web/Native UI implementations with shared semantic tokens, React-free shared i18n, Temporal-based time handling and versioned fail-fast Web runtime public config.

Frontend Foundation authorities were integrated into protected `main` via PR #22. Production frontend materialization continues independently on `feature/frontend-materialization`; no direct frontend PASS is inferred from its active status.

## Environment model

```text
LOCAL
DEV
UAT
PROD
```

Environments are not Git branches. Activation remains progressive and provider-specific infrastructure is selected only when the real boundary requires it.

## Persistence / selected Physical posture

Selected targets remain unchanged:

- PostgreSQL 18.4 canonical persistence;
- PostGIS / pgvector / native FTS / pg_trgm / unaccent / pg_stat_statements;
- PgBouncer 1.25.2 selected, not forced into every day-one path;
- PowerSync + encrypted SQLite for bounded noncanonical local/offline state when activated;
- PostgreSQL transactional outbox for Class-A async work when required;
- Restate for Class-B durable work, initially dormant;
- Cloudflare R2 for private ContentArtifact bytes when activated;
- pgBackRest + AWS S3 `eu-south-1` for recovery, initially dormant;
- OR-Tools CP-SAT for solver capability when activated;
- OpenTelemetry + Grafana Alloy + Grafana Cloud EU observability target.

No specialist component becomes active merely because it is selected.

## Testing and delivery

Backend CP1–CP3 commands have direct WSL/Linux evidence. CP4 has materialized repository CI on `feature/backend-scaffold`:

```text
Backend CI
├── Backend Quality
├── Backend PostgreSQL
└── Backend CI Gate

Dependency Review
└── separate repository-wide workflow
```

The workflows use explicit `ubuntu-24.04`, least-privilege permissions, immutable Action SHAs, exact uv 0.12.5 with checksum verification, locked installs and the real DANTE PostgreSQL image/harness. Required status checks remain **0** until a real PR proves green, deliberate red and recovery-green behavior and the exact emitted contexts are observed.

No arbitrary coverage threshold is introduced.

## Direct evidence truth

Current branch-local evidence includes:

```text
CP1 BACKEND PROCESS / CONFIG            DIRECT QA PASS
CP2 LOCAL POSTGRESQL                    DIRECT QA PASS
CP3 PERSISTENCE / MIGRATIONS            DIRECT QA PASS
CP3 POSTGRESQL ACCEPTANCE               18/18 PASS
CP3 FULL BACKEND PYTEST                 50/50 PASS
CP4 LOCAL QUALITY RE-RUN                32/32 FAST PASS
CP4 LOCAL POSTGRESQL RE-RUN             18/18 PASS
CP4 BACKEND PACKAGE BUILD               PASS
CP4 REMOTE PR GREEN                     NOT RUN
CP4 DELIBERATE RED                      NOT RUN
CP4 RECOVERY GREEN                      NOT RUN
REQUIRED STATUS CHECKS                  0
CONCRETE BUSINESS DB SCHEMA             NOT STARTED
DIRECT HG-01..HG-12                     NOT RUN
RESTORE/PITR REHEARSAL                  NOT RUN
POWERSYNC DIRECT TEST                   NOT RUN
RESTATE DIRECT TEST                     NOT RUN
PRODUCTION DEPLOYMENT                   NOT STARTED
```

The CP4 local PostgreSQL re-run completed 18/18 tests in 15.59s on Python 3.14.7 after rebuilding `dante-postgres-local:18.4`. Coverage percentages remain evidence only, not quality thresholds.

## Where to continue

Read before the next backend write:

1. `docs/README.md`
2. `docs/PROJECT-STATUS.md`
3. development operating/safety/handoff rules
4. `docs/workstreams/backend-scaffold.md`
5. `docs/development/backend-cp4-ci-contract.md`
6. CP1/CP2/CP3 contracts as needed
7. accepted Physical sources/register for any Physical-consuming scope.

### Exact active boundaries

```text
FRONTEND
feature/frontend-materialization
→ continue its own bounded materialization/direct-validation workstream

BACKEND
feature/backend-scaffold
→ run post-main-reconciliation regression QA
→ real CP4 calibration PR green
→ deliberate red
→ recovery green
→ only then consider required-check repository settings
→ CP4 closure
→ CP5 scaffold closure
→ concrete Logical → PostgreSQL mapping
```

Do not reopen closed Product/Domain/Logical/Physical/Engineering/Frontend Foundation decisions by default.