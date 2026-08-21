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
INTEGRATED IN PROTECTED main / DIRECT QA PASS
CP1 CLOSED / DIRECT QA PASS
CP2 CLOSED / DIRECT QA PASS
CP3 CLOSED / DIRECT QA PASS
CP4 CLOSED / DIRECT REMOTE QA PASS
CP5 CLOSED / DIRECT INTEGRATED QA PASS
PR #24 MERGED / POST-MERGE BACKEND CI PASS

PROTECTED-MAIN CI
Backend CI Gate REQUIRED
Dependency Review REQUIRED
branch up-to-date REQUIRED
required-check source GitHub Actions

CONCRETE LOGICAL → POSTGRESQL IMPLEMENTATION
NOT STARTED / NEXT BACKEND IMPLEMENTATION BOUNDARY

DIRECT SELECTED-STACK VALIDATION / PSV
NOT RUN BEYOND EXPLICITLY RECORDED SCAFFOLD ACCEPTANCE
```

Architecture/design closure never implies implementation PASS. Direct PASS is recorded only where the relevant artifact or scenario actually ran.

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

The materialized LOCAL PostgreSQL baseline uses:

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

Accepted frontend architecture includes feature-first Web/Mobile, thin route/navigation adapters, public-API-only acyclic dependencies, small real-consumer shared packages, a formal Data Authority Matrix, backend canonical effect authority, Mobile PowerSync local/offline posture, Web online-first posture, identity-scoped local storage and platform-specific UI implementations over shared semantic tokens.

Frontend production materialization continues independently on `feature/frontend-materialization`; no direct frontend PASS is inferred from branch activity.

## Backend CI and protected-main enforcement

CP4 materialized and directly calibrated:

```text
Backend CI
├── Backend Quality
├── Backend PostgreSQL
└── Backend CI Gate

Dependency Review
└── repository-wide dependency policy check
```

Remote PR #24 calibration directly proved:

```text
M5 GREEN
Backend Quality       SUCCESS
Backend PostgreSQL    SUCCESS
Backend CI Gate       SUCCESS
Dependency Review     SUCCESS

M6 DELIBERATE RED
Backend Quality       FAILURE
Backend PostgreSQL    SUCCESS
Backend CI Gate       FAILURE
Dependency Review     FAILURE

M7 RECOVERY GREEN
Backend Quality       SUCCESS
Backend PostgreSQL    SUCCESS
Backend CI Gate       SUCCESS
Dependency Review     SUCCESS
```

The deliberate red did not introduce a vulnerable package: Dependency Review temporarily denied the already-visible FastAPI dependency and failed for that policy violation. Backend CI Gate independently proved fail-closed behavior when a mandatory upstream job failed.

Protected `main` requires:

```text
Backend CI Gate
Dependency Review
```

Both are bound in the ruleset UI to **GitHub Actions**. The branch must be up to date before merge. Zero approvals remains intentional while one regular maintainer exists; PR-before-merge, review-thread resolution, deletion protection and force-push protection remain in place.

Repository owner also enabled the Actions setting requiring full-length Action SHAs. The connected API cannot directly read that setting, so it is recorded as owner-applied rather than falsely API-verified.

No arbitrary coverage threshold is introduced.

## CP5 final integrated scaffold acceptance

CP5 re-proved the complete scaffold on the canonical WSL2/Linux workstation without adding business schema or changing backend implementation.

Direct evidence:

```text
remote PRE-SCOPE / branch relation        PASS
main ancestry / behind_by=0               PASS
uv 0.12.5                                 PASS
Python 3.14.7                              PASS
uv lock --check / sync --locked           PASS
Ruff format + lint                        PASS
mypy strict                               PASS
fast pytest                               32/32 PASS
canonical PostgreSQL image rebuild        PASS
PostgreSQL acceptance                     18/18 PASS
full backend pytest                       50/50 PASS
full-run coverage                         97.42% evidence only
wheel + sdist build                       PASS
LOCAL PostgreSQL Compose health           PASS
explicit DB security provisioning         PASS
real Uvicorn factory startup              PASS
GET /health/live                          200 {"status":"ok"}
GET /health/ready                         200 {"status":"ready"}
CP4 required remote workflows             SUCCESS on PRE-SCOPE
```

One immediate full-suite rerun after the dedicated PostgreSQL suite encountered a Docker Desktop/WSL port-forwarding `/forwards/expose` HTTP 500 while Docker held a newly created container on an otherwise unused loopback port. After removing that diagnostic container, the clean full suite passed 50/50. This is recorded as a transient local Docker forwarding event, not as a backend/database test failure.

## Backend scaffold protected-main integration

PR #24 merged the closed CP1–CP5 scaffold into protected `main` using the accepted merge-commit method.

```text
pre-merge main                         ff46eb16b971b1fde96eef9047b09faa02e1a5db
feature/backend-scaffold HEAD          46b775bfbfc4747daff341d973df133646dbd0c8
merge commit / protected main          41680497c94b0c2f4830679b93f8eb6f1d543f8d
Backend CI push-main run               32502330955 SUCCESS
```

The merge commit has the expected two parents: the prior protected-main SHA and the final scaffold feature HEAD. PR #24 is closed/merged. No branch deletion, CodeQL activation, ruleset mutation, frontend mutation or concrete business-schema implementation was part of the merge gate.

## Direct evidence truth

```text
CP1 BACKEND PROCESS / CONFIG             DIRECT QA PASS
CP2 LOCAL POSTGRESQL                     DIRECT QA PASS
CP3 PERSISTENCE / MIGRATIONS             DIRECT QA PASS
CP3 POSTGRESQL ACCEPTANCE                18/18 PASS
CP3 FULL BACKEND PYTEST                  50/50 PASS
CP4 LOCAL FAST QA                        32/32 PASS
CP4 LOCAL POSTGRESQL QA                  18/18 PASS
CP4 POST-MAIN REGRESSION                 PASS
CP4 REMOTE PR GREEN                      PASS
CP4 DELIBERATE RED                       PASS
CP4 RECOVERY GREEN                       PASS
CP4 REQUIRED-CHECK PROMOTION             APPLIED
CP4                                      CLOSED / DIRECT REMOTE QA PASS
CP5 FAST QA                              32/32 PASS
CP5 POSTGRESQL QA                        18/18 PASS
CP5 FULL BACKEND QA                      50/50 PASS
CP5 REAL STARTUP + LIVE + READY          PASS
CP5                                      CLOSED / DIRECT INTEGRATED QA PASS
BACKEND SCAFFOLD MAIN INTEGRATION        PASS
POST-MERGE BACKEND CI                    PASS
CONCRETE BUSINESS DB SCHEMA              NOT STARTED
DIRECT HG-01..HG-12                      NOT RUN
RESTORE/PITR REHEARSAL                   NOT RUN
POWERSYNC DIRECT TEST                    NOT RUN
RESTATE DIRECT TEST                      NOT RUN
PRODUCTION DEPLOYMENT                    NOT STARTED
```

Coverage values recorded during scaffold tests remain evidence only, not project thresholds.

## Environment model

```text
LOCAL
DEV
UAT
PROD
```

Environments are not Git branches. Activation remains progressive and provider-specific infrastructure is selected only when the real boundary requires it.

## Selected Physical posture

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

## Where to continue

Read before the next backend write:

1. `docs/README.md`
2. `docs/PROJECT-STATUS.md`
3. development operating/safety/handoff rules
4. closed `docs/workstreams/backend-scaffold.md` for scaffold evidence
5. closed Logical Model owner/ref/invariant authorities
6. applicable Physical target/validation authorities.

Exact active boundaries:

```text
FRONTEND
feature/frontend-materialization
→ continue its independent bounded materialization/direct-validation workstream

BACKEND
protected main contains the complete CP1–CP5 production backend scaffold
→ backend scaffold integration VERIFIED / PASS
→ Concrete Logical → PostgreSQL is the next backend implementation boundary
→ start it only through a fresh bounded workstream/gate
```

Do not reopen closed Product/Domain/Logical/Physical/Engineering/Frontend Foundation or CP1–CP5 decisions by default.