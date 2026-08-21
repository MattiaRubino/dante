# DANTE — Project Status

- Status: **CURRENT TRUTH**
- Product: **DANTE**
- Branch-local current work: `feature/backend-scaffold`
- Protected-main truth reconciled from: `ff46eb16b971b1fde96eef9047b09faa02e1a5db`

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
WL-H01..WL-H12 ACTIVE

PRE-PHYSICAL COHERENCE
DEFINITIVE CLOSED / FINAL QA PASS

PHYSICAL TARGET
CLOSED / SELECTED / ACCEPTED
PM-11 COMPLETE
PM-12 COMPLETE
PM-13 QA PASS
PM-14 CLOSURE COMPLETE

ENGINEERING FOUNDATION v0
CLOSED / ACCEPTED / FINAL REVIEW PASS

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
CP4-M1 CLOSED
CP4-M2 MATERIALIZED / REMOTE READBACK PASS
CP4-M3 CLOSED / DIRECT LOCAL QA PASS
CP4-M4 MAIN RECONCILIATION MATERIALIZED
POST-MERGE REGRESSION QA NEXT
CP4 REMOTE GREEN/RED/RECOVERY CALIBRATION NOT RUN
CP5 NOT STARTED

CONCRETE LOGICAL → POSTGRESQL IMPLEMENTATION
NOT STARTED

DIRECT HG-01..HG-12
NOT RUN / PASS 0
```

Architecture/design closure does not imply implementation PASS. Branch-local implementation evidence outranks older `main` status text only for this still-unmerged backend workstream.

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
- idempotency != semantic identity;
- client local state != canonical accepted effect.

WL-H01..WL-H12 remain active and constrain implementation.

## 3. Logical / Physical authority

The Logical Model remains closed. 57/57 owners are classified and implementation must not mechanically translate owners into one-table/one-service assumptions.

Canonical persistence remains:

```text
PostgreSQL 18.4
sole canonical persistence + material-history authority
```

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

Accepted baseline includes:

```text
Node 24 LTS
TypeScript 6.0.x strict
pnpm 11
Turborepo 2.x
React 19.2 / Vite 8 / TanStack Router
React Native 0.86 / Expo SDK 57 / Expo Router
PowerSync + encrypted SQLite
TanStack Query 5
TanStack Form
Zod 4
Orval 8
```

Structural rules include feature-first Web/Mobile, public-API-only acyclic dependencies, small real-consumer shared packages, a Data Authority Matrix, backend canonical effect authority, feature data firewall, Mobile local/offline capability, Web online-first posture, identity-scoped local data and platform-specific UI implementations over shared semantic tokens.

The separate `feature/frontend-materialization` workstream is active. Its existence is not direct frontend validation PASS.

## 6. Backend CP1 — CLOSED / DIRECT QA PASS

Implementation/closure HEAD:

`02d113d772cdb247faebb3cef4d857d125266da3`

Direct evidence includes:

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

CP1 coverage 100% was evidence for that small surface only, never a permanent threshold.

## 7. Backend CP2 — CLOSED / DIRECT QA PASS

Direct LOCAL PostgreSQL evidence includes:

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

The accepted DANTE-owned image is `dante-postgres-local:18.4`.

## 8. Backend CP3 — CLOSED / DIRECT QA PASS

Implementation/direct-QA HEAD:

`35cf6440bc121a38342f6bbee72e210435a788a4`

Materialized boundaries include SQLAlchemy async runtime, psycopg 3, Alembic technical baseline, typed database settings, FastAPI DB lifespan/readiness, `dante` schema metadata authority, owner/migrator/runtime provisioning and the real PostgreSQL acceptance harness.

Direct closure evidence:

```text
uv lock --check                         PASS
uv sync --locked                        PASS
Ruff                                    PASS
mypy                                    PASS
fast pytest                             32/32 PASS
PostgreSQL pytest                       18/18 PASS in 15.61s
full pytest                             50/50 PASS in 24.72s
full-run coverage                       97.42% evidence only
uv build / sdist / wheel                PASS
Alembic fresh/head/round-trip/drift     PASS
privilege matrix                        PASS
runtime identity/search_path            PASS
stale-connection recovery               PASS
DB stop/start outage recovery           PASS
transaction semantics                   PASS
```

The frozen/blackholed-peer readiness behavior remains an explicit hardening finding, not a claimed CP3 PASS.

## 9. Backend CP4 — Quality / CI enforcement

Detailed authority:

`docs/development/backend-cp4-ci-contract.md`

### M1 — evidence freeze — CLOSED

```text
canonical workstation uv              0.12.5
Python authority                       apps/backend/.python-version = 3.14.7
uv Linux x86_64 SHA-256                68a509da24b06b4223a1c0175fb5eb5bc79342b76cbeff0cfe51ac3f5b17b6b2
```

Pinned Actions:

```text
actions/checkout v7.0.1
3d3c42e5aac5ba805825da76410c181273ba90b1

astral-sh/setup-uv v9.0.0
c771a70e6277c0a99b617c7a806ffedaca235ff9

actions/dependency-review-action v5.0.0
a1d282b36b6f3519aa1f3fc636f609c47dddb294
```

### M2 — materialization — REMOTE READBACK PASS

Executable/config HEAD before main reconciliation:

`eb8d33fa85d6409dfcc60eba663cb32b64d65aee`

Exactly materialized:

```text
.github/workflows/backend-ci.yml
.github/workflows/dependency-review.yml
.github/dependabot.yml
apps/backend/pyproject.toml
```

`apps/backend/uv.lock` was untouched.

Backend CI structure:

```text
Backend Quality
Backend PostgreSQL
        ↓
Backend CI Gate
PASS iff both mandatory upstream jobs == success
```

Dependency Review is separate and repository-wide. Required checks remain **0** pending calibration.

### M3 — direct local QA — CLOSED / PASS

At exact HEAD `eb8d33fa85d6409dfcc60eba663cb32b64d65aee`:

```text
uv 0.12.5                              PASS
uv lock --check                         PASS
uv sync --locked                        PASS
Ruff format                             PASS — 23 files
Ruff lint                               PASS
mypy strict                             PASS — 20 source files
pytest -m "not postgres"                PASS — 32/32 in 0.69s
uv build                                PASS
sdist + wheel                           PASS
canonical PostgreSQL image rebuild      PASS
pytest -m postgres -vv                  PASS — 18/18 in 15.59s
final worktree                          CLEAN
```

77.84% fast-suite and 91.75% PostgreSQL-slice coverage are evidence only.

### M4 — protected-main reconciliation — MATERIALIZED

Pre-reconciliation facts:

```text
backend PRE-SCOPE      eb8d33fa85d6409dfcc60eba663cb32b64d65aee
current main           ff46eb16b971b1fde96eef9047b09faa02e1a5db
merge base             7a1600c2167f68c9281d3ed77b32a3d954fbd061
backend vs main        92 ahead / 28 behind
```

Only four paths had independent changes on both sides:

```text
README.md
docs/PROJECT-STATUS.md
docs/README.md
docs/ROADMAP.md
```

Fourteen other changed `main` paths were imported byte-identically. The two-parent reconciliation commit is:

`6a8122249f13f9b8553f511c47b4185c6e3e6540`

After that merge, `main` is an ancestor of the backend branch (`behind_by = 0`). The four global documents are being semantically reconciled to preserve both newer frontend/main truth and newer backend/workstream truth.

**Post-merge backend regression QA has not yet run and is not claimed PASS.**

## 10. Direct-validation non-claims

Do not extrapolate scaffold evidence into blanket Physical validation:

```text
CP4 REMOTE PR GREEN                    NOT RUN
CP4 DELIBERATE RED                     NOT RUN
CP4 RECOVERY GREEN                     NOT RUN
DEPENDENCY REVIEW uv DELTA PROOF       NOT RUN
REQUIRED STATUS CHECK PROMOTION        NOT RUN
CODEQL POST-MAIN ACTIVATION            NOT RUN
DIRECT HG-01..HG-12                    NOT RUN
DIRECT HG PASS                         0
RESTORE/PITR REHEARSAL                 NOT RUN
POWERSYNC DIRECT TEST                  NOT RUN
RESTATE DIRECT TEST                    NOT RUN
OBJECT RECOVERY TEST                   NOT RUN
SOLVER DIRECT TEST                     NOT RUN
PRODUCTION DEPLOYMENT                  NOT STARTED
```

## 11. Active branches / workstreams

```text
feature/backend-scaffold
→ backend production scaffold
→ CP4 post-main regression QA next

feature/frontend-materialization
→ frontend production materialization
→ separate worktree/workstream
```

The workstreams are allowed to proceed in parallel. Shared global documentation must be reconciled semantically when integrating the second branch; branch-local work must not overwrite newer protected-main truth.

## 12. Exact next backend action

```text
1. Pull the reconciled feature/backend-scaffold HEAD.
2. Verify clean worktree and exact remote/local HEAD.
3. Re-run locked backend quality QA after main reconciliation.
4. Rebuild dante-postgres-local:18.4 and run PostgreSQL 18/18 acceptance.
5. If green, record M4 regression PASS.
6. Open the real CP4 calibration PR against current main.
7. Observe Backend Quality / Backend PostgreSQL / Backend CI Gate / Dependency Review remotely.
8. Perform bounded deliberate-red calibration.
9. Restore recovery green.
10. Only then consider a separate required-check/settings gate.
11. Close CP4 only after truthful acceptance evidence.
12. Proceed to CP5, then concrete Logical → PostgreSQL mapping.
```

Do not reopen closed Product/Domain/Logical/Physical/Engineering/Frontend Foundation/CP1/CP2/CP3 decisions without concrete contradictory evidence.