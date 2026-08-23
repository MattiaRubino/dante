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
PostgreSQL 18 major family is the canonical persistence architecture
Physical phase-time exact patch: PostgreSQL 18.4

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
CP2 CLOSED / DIRECT QA PASS — original PostgreSQL 18.4 evidence
CP3 CLOSED / DIRECT QA PASS — original PostgreSQL 18.4 evidence
CP4 CLOSED / DIRECT REMOTE QA PASS
CP5 CLOSED / DIRECT INTEGRATED QA PASS
PR #24 MERGED / POST-MERGE BACKEND CI PASS

PROTECTED-MAIN CI
Backend CI Gate REQUIRED
Dependency Review REQUIRED
branch up-to-date REQUIRED
required-check source GitHub Actions

CP6 — CONCRETE POSTGRESQL DATABASE
ACTIVE ON feature/logical-postgresql
CP6-00 COMPLETE
CP6-01 CLOSED / GATE 01 PASS
CP6-02 CLOSED / GATE 02 PASS
CP6-03 ACTIVE — CHECKPOINT J / DB-U23 CLOSED
NEXT DESIGN BLOCK — FINAL ACTUAL POSTGRESQL OBJECT INVENTORY
DB-U08 / DB-U15 / DB-U21 OPEN
GATE 03 NOT YET EARNED

CURRENT POSTGRESQL TECHNICAL PATCH
PostgreSQL 18.6
configuration refresh APPLIED
foundation regression DIRECT REMOTE QA PASS
Backend CI run 32568664940 @ ec3dc795b5e044daa3a77723c94a1b4b5b92865c

CURRENT DANTE BUSINESS DATABASE
NOT YET MATERIALIZED

FIRST PRODUCT VERTICAL
POST-CP6 / NOT STARTED / SEPARATELY AUTHORIZED

DIRECT BUSINESS-SEMANTIC HG / blanket PSV
NOT RUN BEYOND EXACTLY RECORDED QUALIFYING EVIDENCE
```

Architecture/design closure never implies implementation PASS. Direct PASS is recorded only where the relevant artifact or scenario actually ran. PostgreSQL 18.4 remains the exact historical Physical/CP2/CP3 evidence patch; the current CP6 technical patch is 18.6. Patch maintenance inside PostgreSQL 18 does not rewrite historical evidence or reopen the selected persistence architecture.

## Current CP6 execution boundary

CP6 now has one concrete job: turn the closed Domain + Logical + Physical model into the real DANTE PostgreSQL database before the first product vertical begins.

```text
CP6-03
WHOLE DANTE DATABASE BLUEPRINT
CURRENT: CHECKPOINT J COMPLETE
NEXT: FINAL ACTUAL POSTGRESQL OBJECT INVENTORY
        ↓
CP6-04
WHOLE DANTE DATABASE MATERIALIZATION
Alembic + tables + constraints + indexes + SQLAlchemy mappings + DB tests
        ↓
CP6-05
WHOLE DATABASE DIRECT QA + CP6 CLOSURE
        ↓
POST-CP6
FIRST PRODUCT VERTICAL APPLICATION PHASE
```

Earlier process language that prohibited all business schema/migrations/mappings anywhere in CP6 is superseded. CP6-01 and CP6-02 themselves correctly created none; later CP6 stages may materialize every database structure already determinable from the closed model. First-product-vertical application behavior, product persistence adapters, APIs and frontend remain post-CP6.

Current execution authority: `docs/workstreams/logical-postgresql.md`.

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
Python                   3.14.x
current scaffold pin      3.14.7
package manager           uv 0.12.5 exact project requirement
source root               apps/backend/src/dante
format/lint               Ruff
type checking             mypy strict
unit/integration runner   pytest
property testing          Hypothesis where meaningful

server semantics          Linux
Windows workflow          WSL2/Linux
primary user IDE          PyCharm with WSL interpreter supported
local stateful infra      Docker Compose

canonical persistence     PostgreSQL 18 major family
current technical patch   PostgreSQL 18.6
ORM/SQL toolkit           SQLAlchemy 2.0 stable line
driver                    psycopg 3
migrations                Alembic
```

The materialized current LOCAL PostgreSQL baseline uses:

- PostgreSQL 18.6;
- PostGIS 3.6.4;
- pgvector 0.8.6;
- `pg_trgm`;
- `unaccent`;
- `pg_stat_statements` with preload configuration;
- native PostgreSQL full-text search.

PostgreSQL remains the sole canonical persistence and material-history authority.

The current 18.6 technical envelope was directly re-proved on GitHub Actions run `32568664940` against HEAD `ec3dc795b5e044daa3a77723c94a1b4b5b92865c`: Backend Quality, Backend PostgreSQL and Backend CI Gate all succeeded; the fast lane passed 32/32 tests and the PostgreSQL lane passed 18/18 tests, covering the current 50-test corpus across the two mandatory lanes.

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

## Historical CP5 final integrated scaffold acceptance

CP5 re-proved the complete scaffold on the canonical WSL2/Linux workstation without adding business schema or changing backend implementation. This evidence used the then-current PostgreSQL 18.4 envelope and remains historically exact.

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
CP2 LOCAL POSTGRESQL 18.4                DIRECT QA PASS / HISTORICAL EXACT
CP3 PERSISTENCE / MIGRATIONS 18.4        DIRECT QA PASS / HISTORICAL EXACT
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
POSTGRESQL 18.6 FOUNDATION REGRESSION    DIRECT REMOTE QA PASS
18.6 FAST LANE                           32/32 PASS
18.6 POSTGRESQL LANE                     18/18 PASS
18.6 BACKEND CI GATE                     SUCCESS
CP6-01                                   CLOSED / GATE 01 PASS
CP6-02                                   CLOSED / GATE 02 PASS
CP6-03                                   ACTIVE / CHECKPOINT J COMPLETE / FINAL ACTUAL POSTGRESQL OBJECT INVENTORY NEXT
CONCRETE DANTE BUSINESS DB               NOT YET MATERIALIZED
DIRECT BUSINESS HG-01..HG-12             NOT RUN / PASS 0
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

The Physical target remains unchanged. Its exact phase-time PostgreSQL patch was 18.4; current patch maintenance within selected major line 18 is lifecycle-managed downstream.

- PostgreSQL 18 major family — sole canonical persistence/material-history authority; Physical phase-time patch 18.4; current CP6 technical patch 18.6;
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
3. `docs/ROADMAP.md`
4. `docs/workstreams/logical-postgresql.md`
5. `docs/development/backend-cp6-02-postgresql-persistence-constitution.md`
6. `docs/development/backend-cp6-02-postgresql-persistence-constitution-closure.md`
7. development operating/safety/handoff rules
8. closed `docs/workstreams/backend-scaffold.md` for scaffold evidence
9. closed Logical Model owner/ref/invariant authorities
10. applicable Physical target/validation authorities.

Exact active boundaries:

```text
FRONTEND
feature/frontend-materialization
→ continue its independent bounded materialization/direct-validation workstream

BACKEND
feature/logical-postgresql
→ CP6 Concrete PostgreSQL Database ACTIVE
→ CP6-01 CLOSED / GATE 01 PASS
→ CP6-02 CLOSED / GATE 02 PASS
→ PostgreSQL 18.6 technical refresh + direct remote regression PASS
→ CP6-03 ACTIVE / CHECKPOINT J COMPLETE
→ FINAL ACTUAL POSTGRESQL OBJECT INVENTORY NEXT
→ DB-U08 / DB-U15 / DB-U21 remain OPEN until inventory freeze
→ CP6-04 only after Gate 03 / REAL DATABASE MATERIALIZATION
→ CP6-05 / WHOLE DATABASE DIRECT QA + CP6 CLOSURE
→ first product vertical only after CP6 closes
```

Do not reopen closed Product/Domain/Logical/Physical/Engineering/Frontend Foundation or CP1–CP5 decisions by default. Do not implement the first product vertical application inside CP6.
