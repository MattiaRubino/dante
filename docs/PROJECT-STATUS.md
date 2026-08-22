# DANTE — Project Status

- Status: **CURRENT TRUTH**
- Product: **DANTE**
- Protected-main truth anchor: `fd3bc8dd918cf6aadeff4572221af68612c3cb42`
- Backend integration PR `#24`: **MERGED**
- Backend persistence-readiness workstream: `feature/logical-postgresql` — **CP6 ACTIVE / DESIGN-FIRST**
- Frontend materialization workstream: `feature/frontend-materialization`

## 1. Executive state

```text
PRODUCT / NORTH STAR
CURRENT

DOMAIN MODEL
CLOSED
Whole-Domain PASS WITH HARDENING
POST-WRITE QA PASS

LOGICAL MODEL
CLOSED
Whole-Logical PASS WITH HARDENING
REMOTE QA PASS
57 / 57 CLASSIFIED
WL-H01..WL-H12 ACTIVE

PRE-PHYSICAL COHERENCE
DEFINITIVE CLOSED / FINAL QA PASS

PHYSICAL TARGET
CLOSED / SELECTED / ACCEPTED
POSTGRESQL 18 MAJOR FAMILY
SOLE CANONICAL PERSISTENCE / MATERIAL-HISTORY AUTHORITY
PHYSICAL PHASE-TIME EXACT PATCH 18.4

ENGINEERING FOUNDATION v0
CLOSED / ACCEPTED / FINAL REVIEW PASS

FRONTEND ENGINEERING FOUNDATION
CLOSED / ACCEPTED / FINAL REVIEW PASS
INTEGRATED VIA PR #22

FRONTEND MATERIALIZATION
ACTIVE ON feature/frontend-materialization
DIRECT FRONTEND VALIDATION ONLY AS EARNED BY ITS WORKSTREAM

PRODUCTION BACKEND SCAFFOLD
INTEGRATED IN PROTECTED main / DIRECT QA PASS
CP1 CLOSED / DIRECT QA PASS
CP2 CLOSED / DIRECT QA PASS — POSTGRESQL 18.4 HISTORICAL EXACT EVIDENCE
CP3 CLOSED / DIRECT QA PASS — POSTGRESQL 18.4 HISTORICAL EXACT EVIDENCE
CP4 CLOSED / DIRECT REMOTE QA PASS
CP5 CLOSED / DIRECT INTEGRATED QA PASS
PR #24 MERGED / POST-MERGE BACKEND CI PASS

PROTECTED-MAIN CI ENFORCEMENT
Backend CI Gate REQUIRED
Dependency Review REQUIRED
branch up-to-date REQUIRED
source GitHub Actions

CP6 — CONCRETE PERSISTENCE READINESS
ACTIVE ON feature/logical-postgresql
DESIGN-FIRST
CP6-00 COMPLETE
CP6-01 CLOSED / GATE 01 PASS
CP6-02 CLOSED / GATE 02 PASS
CP6-03 NEXT / NOT STARTED
NO BUSINESS SCHEMA / MIGRATION / MAPPING / ADAPTER AUTHORIZED IN CP6

CURRENT POSTGRESQL TECHNICAL PATCH
18.6
CONFIGURATION REFRESH APPLIED
DIRECT REMOTE FOUNDATION REGRESSION PASS
RUN 32568664940
HEAD ec3dc795b5e044daa3a77723c94a1b4b5b92865c

CP6 TERMINAL TARGET
CONCRETE POSTGRESQL FOUNDATION CLOSED / READY
VERTICAL #1 SELECTED / EXACTLY DESIGNED / READY FOR IMPLEMENTATION

VERTICAL #1 BUSINESS IMPLEMENTATION
POST-CP6 / SEPARATELY AUTHORIZED

DIRECT BUSINESS-SEMANTIC HG-01..HG-12
NOT RUN / PASS 0 UNLESS A QUALIFYING BUSINESS SCENARIO IS ACTUALLY EXECUTED
```

Architecture/design closure does not imply implementation PASS. CP2/CP3 directly prove the technical PostgreSQL 18.4 substrate at their historical checkpoint; CP6 has now directly re-proved the same technical foundation on PostgreSQL 18.6. Neither technical result retroactively discharges business-semantic HG/PSV obligations.

CP6-01 closure authority:

`docs/development/backend-cp6-01-concrete-persistence-coverage-closure.md`

CP6-02 closed Constitution:

`docs/development/backend-cp6-02-postgresql-persistence-constitution.md`

CP6-02 closure authority:

`docs/development/backend-cp6-02-postgresql-persistence-constitution-closure.md`

## 2. Product and semantic invariants

DANTE is a personal operating system designed to help people understand, organize and improve their real life by turning intentions, needs and possibilities into outcomes they can realistically pursue.

Compass: **Understand life. Shape what comes next.**

Persistent invariants include:

- life central, not task/calendar centric;
- planned vs actual preserved;
- user authority and authorship;
- historical/material truth;
- privacy and provenance;
- honest uncertainty;
- progressive complexity;
- personal-first, not personal-only;
- AI is not product authority;
- possibility != action/decision/preference;
- Effort != Execution != Outcome != Goal Progress;
- Person != Account != Principal != Actor;
- provider state != canonical DANTE state;
- derived projection != canonical truth;
- absence/unknown != false;
- MaterialStateRef != ETag/MVCC/provider revision;
- idempotency != semantic identity;
- client local state != canonical accepted effect.

`WL-H01..WL-H12` remain active and constrain implementation.

## 3. Logical / Physical authority

The Logical Model remains closed. 57/57 Domain concepts are classified and implementation must not mechanically translate them into one-table/one-service assumptions.

Canonical persistence architecture remains:

```text
PostgreSQL 18 major family
sole canonical persistence + material-history authority
```

Version truth is deliberately split:

```text
Physical exact phase-time selection      PostgreSQL 18.4
CP2 / CP3 original direct evidence       PostgreSQL 18.4 / HISTORICAL EXACT
current CP6 technical patch              PostgreSQL 18.6
current 18.6 foundation regression       DIRECT REMOTE QA PASS
```

Patch maintenance inside PostgreSQL 18 is lifecycle maintenance and does not reopen Domain, Logical or Physical architecture.

Accepted PostgreSQL mapping thesis remains:

```text
owner-specific canonical families
+ owner-specific material-state/history families
+ specific typed relation families
+ bounded technical anchors only where genuinely heterogeneous addressing requires them
+ separate provider/derived/runtime concerns
```

Forbidden canonical shortcuts remain universal Entity/Thing, universal Relationship/edge, EAV/property-bag kernel, universal event ontology and JSONB required-semantic escape hatches.

Selected PostgreSQL capabilities:

- PostGIS 3.6.4;
- pgvector 0.8.6;
- native full-text search;
- `pg_trgm`;
- `unaccent`;
- `pg_stat_statements`;
- PgBouncer 1.25.2 selected, activation bounded.

Other selected targets remain bounded and noncanonical where applicable: PowerSync + encrypted SQLite, PostgreSQL transactional outbox, Restate, R2, pgBackRest + AWS S3 `eu-south-1`, OR-Tools CP-SAT and OpenTelemetry/Grafana.

No specialist target is implicitly active merely because it is selected.

## 4. Engineering Foundation and repository

Repository identity governance is complete:

```text
historical repository   MattiaRubino/lifeos
current repository      MattiaRubino/dante
```

Accepted monorepo ownership includes:

```text
apps/backend
apps/web
apps/mobile
packages
infra
tooling
tests/system
docs
prototypes
.github
```

Paths are created only for real content.

Backend architecture remains a capability-first modular monolith with Domain/application/adapters separated, explicit transaction ownership and no universal generic Repository/BaseService/service locator/global DB session.

## 5. Frontend Engineering Foundation

The Frontend Engineering Foundation is integrated into protected `main` via PR #22 and remains closed in design/architecture.

Accepted baseline includes Node 24 LTS, TypeScript 6.0.x strict, pnpm 11, Turborepo 2.x, React 19.2/Vite 8/TanStack Router, React Native 0.86/Expo SDK 57/Expo Router, PowerSync + encrypted SQLite, TanStack Query/Form, Zod 4 and Orval 8.

The separate `feature/frontend-materialization` workstream remains independent from backend CP6. Its existence is not a blanket direct frontend PASS.

## 6. Backend CP1 — CLOSED / DIRECT QA PASS

Implementation/closure HEAD:

```text
02d113d772cdb247faebb3cef4d857d125266da3
```

Direct evidence:

```text
Python 3.14.7 project interpreter      PASS
uv locked bootstrap                    PASS
Ruff format/lint                       PASS
mypy strict                            PASS
pytest                                 25/25 PASS
uv build                               PASS
real Uvicorn factory startup           PASS
/health/live                           200 PASS
/health/ready                          200 PASS
```

## 7. Backend CP2 — CLOSED / DIRECT QA PASS

This section is historical direct evidence and remains tied to the exact patch actually executed.

```text
PostgreSQL                             18.4 PASS
PostGIS                                3.6.4 PASS
pgvector                               0.8.6 PASS
pg_trgm                                PASS
unaccent                               PASS
pg_stat_statements preload/query       PASS
fresh init                             PASS
named-volume persistence               PASS
destructive reset                      PASS
Windows DBeaver host connection        PASS
```

Historical accepted image: `dante-postgres-local:18.4`.

## 8. Backend CP3 — CLOSED / DIRECT QA PASS

Implementation/direct-QA HEAD:

```text
35cf6440bc121a38342f6bbee72e210435a788a4
```

Materialized boundaries include SQLAlchemy async runtime, psycopg 3, Alembic technical baseline, typed database settings, FastAPI DB lifespan/readiness, `dante` schema metadata authority, owner/migrator/runtime provisioning and the real PostgreSQL acceptance harness.

Original direct closure on PostgreSQL 18.4:

```text
uv lock --check                         PASS
uv sync --locked                        PASS
Ruff                                    PASS
mypy                                    PASS
fast pytest                             32/32 PASS
PostgreSQL pytest                       18/18 PASS
full pytest                             50/50 PASS
full-run coverage                       97.42% evidence only
uv build / sdist / wheel                PASS
Alembic acceptance                      PASS
privilege matrix                        PASS
stale-connection recovery               PASS
DB outage recovery                      PASS
transaction semantics                   PASS
```

The frozen/blackholed-peer readiness behavior remains an explicit hardening finding, not a claimed CP3 PASS.

CP3 deliberately contains no business owner/history/relation schema. Therefore CP3 technical QA is not a semantic HG/PSV PASS.

## 9. Backend CP4 — CLOSED / DIRECT REMOTE QA PASS

Detailed authority: `docs/development/backend-cp4-ci-contract.md`.

### M1–M4

```text
uv authority                      0.12.5
Python authority                  3.14.7
workflow/config materialization   PASS
local fast suite                  32/32 PASS
local PostgreSQL suite            18/18 PASS
protected-main reconciliation     PASS
post-merge regression             PASS
main behind_by                    0 after reconciliation
```

### M5 — real PR green

```text
HEAD               bf9d364c59f02857125e228c6b223c13650ab78f
Backend CI          32477974221 SUCCESS
Dependency Review   32477974220 SUCCESS
```

Observed:

```text
Backend Quality       SUCCESS
Backend PostgreSQL    SUCCESS
Backend CI Gate       SUCCESS
Dependency Review     SUCCESS
```

### M6 — deliberate red

```text
HEAD                  739680d11fe5c33a4974f069c2fdcce9e71a4fe0
Backend Quality       FAILURE — intentional calibration step
Backend PostgreSQL    SUCCESS
Backend CI Gate       FAILURE
Dependency Review     FAILURE — intentional deny-packages policy
```

No vulnerable package was added.

### M7 — recovery green

```text
HEAD               df0a7c4fd3c7fe844fe56052fe7999732f186ee5
Backend CI          32478852443 SUCCESS
Dependency Review   32478852454 SUCCESS
```

All intended checks/jobs returned green.

### M8 — protected-main promotion

Existing ruleset `lifeos-main-safety` requires:

```text
Backend CI Gate
Dependency Review
```

The canonical ruleset definition is `docs/development/github-main-ruleset.json`.

```text
CP4
CLOSED / DIRECT REMOTE QA PASS
```

## 10. Backend CP5 — CLOSED / DIRECT INTEGRATED QA PASS

CP5 PRE-SCOPE:

```text
35eca3a6b1fc9bbc691672e29ac975e640a49bf4
```

Canonical WSL2/Linux workstation evidence against the then-current PostgreSQL 18.4 envelope:

```text
branch synchronized to PRE-SCOPE             PASS
uv 0.12.5                                    PASS
Python 3.14.7                                 PASS
uv lock --check                              PASS
uv sync --locked                             PASS
uv tree --locked                             PASS
Ruff format --check                          PASS
Ruff lint                                    PASS
mypy strict                                  PASS
fast pytest                                  32/32 PASS
uv build wheel + sdist                       PASS
canonical PostgreSQL image rebuild           PASS
PostgreSQL acceptance                        18/18 PASS
full backend pytest                          50/50 PASS
full-run coverage                            97.42% evidence only
LOCAL Compose PostgreSQL                     HEALTHY
explicit owner/migrator/runtime provisioning PASS
real Uvicorn factory startup                 PASS
GET /health/live                             200 {"status":"ok"}
GET /health/ready                            200 {"status":"ready"}
```

One immediate full-suite invocation after a dedicated PostgreSQL run hit a transient Docker Desktop/WSL `/forwards/expose` HTTP 500. The diagnostic container was removed and the next clean full suite passed 50/50, so no backend/test-harness change was justified.

CP5 added no business schema, backend source, tests, dependency, migration or CI changes.

```text
CP5
CLOSED / DIRECT INTEGRATED QA PASS
```

## 11. Backend scaffold protected-main integration — VERIFIED / PASS

Approved merge candidate:

```text
pre-merge protected main              ff46eb16b971b1fde96eef9047b09faa02e1a5db
feature/backend-scaffold final HEAD   46b775bfbfc4747daff341d973df133646dbd0c8
```

PR #24 merged using the accepted merge-commit method:

```text
merge commit                          41680497c94b0c2f4830679b93f8eb6f1d543f8d
parent 1                              ff46eb16b971b1fde96eef9047b09faa02e1a5db
parent 2                              46b775bfbfc4747daff341d973df133646dbd0c8
Backend CI push-main run 32502330955 SUCCESS
```

Later protected-main documentation reconciliation is included in the current main anchor recorded at the top of this file.

Final scaffold integration decision:

```text
PRODUCTION BACKEND SCAFFOLD
CLOSED / INTEGRATED IN PROTECTED main / DIRECT QA PASS
```

## 12. PostgreSQL 18.6 CP6 technical refresh — DIRECT REMOTE QA PASS

CP6 retained PostgreSQL major 18 and performed a maintenance-patch refresh only:

```text
18.4 → 18.6
```

Operational pins were updated in the repository-owned Docker base, Compose image, PostgreSQL acceptance harness and Backend CI. PostGIS `3.6.4` and pgvector `0.8.6` remained unchanged.

Direct remote evidence:

```text
Backend CI run                         32568664940
workflow event                         workflow_dispatch
executed HEAD                          ec3dc795b5e044daa3a77723c94a1b4b5b92865c

PostgreSQL base                        18.6-trixie
base OCI index digest                  sha256:ae6c78831cbc35fa3a4aaf4d763ddacf6183d6004774cc2dc28b3920410d1d1a
PostGIS                                3.6.4 PASS
pgvector                               0.8.6 PASS

Backend Quality                        SUCCESS
Ruff format/lint                       PASS
mypy strict                            PASS
fast pytest                            32/32 PASS
wheel + sdist                          PASS

Backend PostgreSQL                     SUCCESS
PostgreSQL acceptance                  18/18 PASS
Alembic fresh → head                   PASS
Alembic head/base/head                 PASS
Alembic drift check                    PASS
owner/migrator/runtime privilege tests PASS
runtime/search_path                    PASS
stale connection recovery              PASS
DB outage/readiness recovery           PASS
transaction semantics                  PASS

Backend CI Gate                        SUCCESS
complete current test corpus           50/50 covered across two mandatory CI lanes
```

This is a direct technical-foundation PASS, not a business-semantic HG/PSV PASS.

PostgreSQL 18.6 release-note impact review is also complete. Current DANTE has no custom logical-decoding output plugin, `pgcrypto`, business GIN index, `btree_gist` or `ltree` object requiring a post-upgrade action. Result:

```text
18.6 RELEASE-NOTE IMPACT
PASS / NO CURRENT POST-UPGRADE ACTION
```

Future PowerSync/logical-replication activation must re-check `output_plugin_libraries` and then-current PostgreSQL maintenance requirements.

## 13. Current direct-validation non-claims

Do not extrapolate technical-foundation evidence into blanket Physical or production validation:

```text
DIRECT BUSINESS HG-01..HG-12           NOT RUN / PASS 0
RESTORE/PITR REHEARSAL                 NOT RUN
POWERSYNC DIRECT TEST                  NOT RUN
RESTATE DIRECT TEST                    NOT RUN
OBJECT RECOVERY TEST                   NOT RUN
SOLVER DIRECT TEST                     NOT RUN
PRODUCTION DEPLOYMENT                  NOT STARTED
CONCRETE BUSINESS DB SCHEMA            NOT IMPLEMENTED
VERTICAL #1 BUSINESS IMPLEMENTATION    NOT STARTED
```

The PostgreSQL technical substrate is real and current on 18.6; the business persistence layer is not.

## 14. Active branches / workstreams

```text
feature/backend-scaffold
→ CLOSED historical implementation branch
→ CP1–CP5 accepted
→ integrated into protected main via PR #24

feature/logical-postgresql
→ ACTIVE backend CP6 Concrete Persistence Readiness
→ design-first / no business implementation in CP6
→ CP6-00 COMPLETE
→ CP6-01 CLOSED / GATE 01 PASS
→ CP6-02 CLOSED / GATE 02 PASS
→ CP6-03 NEXT / NOT STARTED
→ PostgreSQL 18.6 refresh DIRECT REMOTE QA PASS

feature/frontend-materialization
→ independent frontend production materialization workstream
```

Frontend and backend work may proceed in parallel. Shared global documentation must preserve the newest reconciled truth rather than letting one workstream restore stale status from another.

## 15. Exact current backend action

```text
1. Treat Product/Domain/Logical/Physical/Engineering and CP1–CP5 as closed accepted authority.
2. Treat CP6-01 as CLOSED / GATE 01 PASS; do not redo the 57/57 or cross-cutting coverage census.
3. Treat CP6-02 as CLOSED / GATE 02 PASS; consume the closed PostgreSQL Persistence Constitution rather than re-deciding its global rules.
4. Preserve PostgreSQL 18.6 technical refresh + remote regression as DIRECT REMOTE QA PASS.
5. Keep PostgreSQL 18.4 Physical/CP2/CP3 evidence historical and exact; do not rewrite it.
6. Start CP6-03 read/research/design-first: Concrete Relational Topology + Implementation Dependency DAG + Vertical Decomposition.
7. Preserve the closed Constitution decisions on UUIDv7, NativeRef anchors, MaterialStateRef address/control, idempotency, constraints, transactions, migrations, security and QA.
8. Do not create business DDL merely to materialize topology or obtain proof.
9. CP6-04 selects Vertical #1 by evidence.
10. CP6-05 designs Vertical #1 exactly.
11. CP6-06 proves only genuinely materialized/non-speculative PostgreSQL foundation behavior.
12. CP6-07 closes whole persistence readiness.
13. Only after CP6 closure does a separately authorized phase implement Vertical #1.
```

CP6 terminal boundary:

```text
CONCRETE POSTGRESQL FOUNDATION
CLOSED / READY

VERTICAL #1
SELECTED
EXACTLY DESIGNED
READY FOR IMPLEMENTATION
```

Do not reopen closed decisions without concrete contradictory evidence.
