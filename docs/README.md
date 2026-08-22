# DANTE Documentation Index

This directory is the durable documentation authority for DANTE.

## Current authority order

When sources conflict:

1. current protected-main code/migrations/tests and accepted model/ADR truth;
2. current durable product/domain/logical/architecture/engineering docs on protected `main`;
3. active bounded workstream handoff for newer unmerged work;
4. other current sources inside that workstream;
5. historical evidence/closed branches/Git history;
6. conversation memory.

Conversation instructions may clarify intent but do not silently override durable repository truth.

## Current lifecycle status

```text
Product/North Star                 CURRENT
Domain Model                       CLOSED
Logical Model                      CLOSED
Pre-Physical coherence             CLOSED
Physical target                    CLOSED / ACCEPTED
PostgreSQL architecture            18 major family / sole canonical persistence
Physical exact patch               18.4 / HISTORICAL PHASE-TIME SELECTION
Engineering Foundation v0          CLOSED / ACCEPTED
Frontend Engineering Foundation    CLOSED / ACCEPTED / FINAL REVIEW PASS
Frontend main integration          COMPLETE VIA PR #22
Frontend materialization           ACTIVE ON feature/frontend-materialization / DIRECT PASS NOT YET EARNED
Production backend scaffold        INTEGRATED IN PROTECTED main / DIRECT QA PASS
Backend CP1                        CLOSED / DIRECT QA PASS
Backend CP2                        CLOSED / DIRECT QA PASS — PostgreSQL 18.4 historical exact evidence
Backend CP3                        CLOSED / DIRECT QA PASS — PostgreSQL 18.4 historical exact evidence
Backend CP4                        CLOSED / DIRECT REMOTE QA PASS
Backend CP5                        CLOSED / DIRECT INTEGRATED QA PASS
Backend integration PR #24         MERGED / POST-MERGE BACKEND CI PASS
Backend CP6                        ACTIVE ON feature/logical-postgresql / DESIGN-FIRST
Backend CP6-01                     CLOSED / GATE 01 PASS
Backend CP6-02                     CLOSED / GATE 02 PASS
Backend CP6-03                     NEXT / NOT STARTED
Current PostgreSQL patch           18.6
PostgreSQL 18.6 regression         DIRECT REMOTE QA PASS / run 32568664940
Vertical #1 implementation         POST-CP6 / NOT STARTED
Direct business HG / blanket PSV   NOT RUN
```

Patch-level maintenance inside PostgreSQL 18 does not rewrite Physical/CP2/CP3 historical 18.4 evidence or reopen the accepted PostgreSQL architecture.

## Mandatory entry points

### Project / current truth

- `../README.md`
- `PROJECT-STATUS.md`
- `ROADMAP.md`

### Active backend CP6 — Concrete Persistence Readiness

- `workstreams/logical-postgresql.md` — durable CP6 handoff and exact resume point
- `development/backend-cp6-01-concrete-persistence-coverage.md` — exact 57/57 owner/role ledger
- `development/backend-cp6-01-concrete-persistence-coverage-part-2.md` — cross-cutting LR/WL-H/PG-R/DEFER-WL/HG/SC/PSV ledger
- `development/backend-cp6-01-concrete-persistence-coverage-closure.md` — Gate 01 closure
- `development/backend-cp6-02-postgresql-persistence-constitution.md` — closed/accepted PostgreSQL Persistence Constitution
- `development/backend-cp6-02-postgresql-persistence-constitution-closure.md` — formal Gate 02 closure evidence

CP6-02 technical evidence retained by the closed Constitution:

```text
PostgreSQL patch target                18.6
configuration refresh                  APPLIED
Backend CI run                         32568664940
executed HEAD                          ec3dc795b5e044daa3a77723c94a1b4b5b92865c
Backend Quality                        SUCCESS
fast pytest                            32 / 32 PASS
Backend PostgreSQL                     SUCCESS
PostgreSQL pytest                      18 / 18 PASS
Backend CI Gate                        SUCCESS
current test corpus                    50 / 50 covered across mandatory CI lanes
18.6 release-note impact               PASS / NO CURRENT POST-UPGRADE ACTION
```

The next backend checkpoint is **CP6-03 — Concrete Relational Topology + Implementation Dependency DAG + Vertical Decomposition**. It begins read/research/design-first; Gate 02 does not authorize business DDL or Vertical #1 implementation.

### Development governance

- `development/agent-operating-manual.md`
- `development/operating-rules.md`
- `development/documentation-and-handoff.md`
- `development/branching-and-environments.md`
- `development/repository-engineering-safety.md`
- `development/github-main-ruleset.json`

### Backend scaffold — closed / integrated

- `workstreams/backend-scaffold.md` — production-backend scaffold handoff, CP1–CP5 evidence and verified main-integration record
- `development/backend-cp1-contract.md` — CP1 Python/process/config authority
- `development/backend-cp2-postgres-contract.md` — CP2 LOCAL PostgreSQL 18.4 historical direct authority
- `development/backend-cp3-persistence-contract.md` — CP3 persistence/migrations/privileges/real-PostgreSQL 18.4 historical direct authority
- `development/backend-cp4-ci-contract.md` — CP4 CI/security/calibration closure authority
- `development/local-backend-workstation-bootstrap.md` — active WSL2/Docker/PyCharm-oriented workstation/bootstrap guide with phase-time evidence distinguished from current runtime truth

CP5 did not create a new implementation contract because it was an integration-acceptance/closure checkpoint, not a new runtime architecture boundary. Its durable evidence is recorded in the workstream handoff, project status, roadmap and backend README.

### Engineering Foundation — closed

- `workstreams/engineering-foundation.md`
- `development/engineering-foundation-v0.md`
- `development/repository-layout-v0.md`
- `development/application-structure-v0.md`
- `development/environments-and-promotion-v0.md`
- `development/config-and-secrets-v0.md`
- `development/toolchain-and-dx-v0.md`
- `development/testing-and-ci-v0.md`

### Frontend Engineering Foundation — closed / integrated

- `workstreams/frontend-foundation.md`
- `architecture/frontend-engineering-foundation.md`
- `architecture/frontend-engineering-foundation-part-2.md`
- `architecture/frontend-engineering-foundation-final-review.md`
- `architecture/frontend-engineering-foundation-post-closure-qa.md`
- `decisions/ADR-008-frontend-engineering-stack.md`
- `decisions/ADR-009-frontend-architecture-boundaries.md`

The active frontend materialization handoff lives on the separate branch `feature/frontend-materialization`; do not invent a branch-local replacement here before that workstream is integrated.

### Architecture

- `architecture/README.md`
- `architecture/system-overview.md`
- `architecture/technical-decisions.md`

### Domain / Logical / Physical

Use their indexes and accepted linked sources. Physical-consuming implementation also consumes the applicable post-selection validation register.

Historical evidence remains historical. In particular, the exact Physical/CP2/CP3 PostgreSQL 18.4 records must not be rewritten as if their direct execution occurred on 18.6.

## Current engineering direction

One product monorepo with accepted ownership for:

```text
apps/backend + apps/web + apps/mobile
packages
infra
tooling
tests/system
docs
prototypes
.github
```

Paths are created only when real content exists.

Backend current truth includes Python 3.14.7, exact uv 0.12.5 project authority, Ruff, mypy strict, pytest, SQLAlchemy 2.0 stable, psycopg 3, Alembic, least-privilege application roles, a real PostgreSQL acceptance harness, calibrated CI and protected-main required checks. The accepted persistence architecture is PostgreSQL 18; the current repository-owned image is PostgreSQL 18.6 with PostGIS 3.6.4 and pgvector 0.8.6. Its technical foundation regression passed remotely in run `32568664940`.

Frontend durable rules include feature-first platform-specific apps, public-API-only acyclic dependencies, real-consumer shared packages, Data Authority Matrix, backend canonical effect authority, Web online-first, Mobile PowerSync local/offline posture, identity-scoped local data, shared semantic tokens with platform-specific UI and one DANTE LOCAL/DEV/UAT/PROD vocabulary.

Cloud/backend compute provider and IaC engine remain deferred until their real infrastructure boundary.

## CI truth

CP4 is closed and integrated into protected `main` via PR #24 after direct local, remote green, deliberate-red and recovery-green evidence.

Materialized:

```text
.github/workflows/backend-ci.yml
.github/workflows/dependency-review.yml
.github/dependabot.yml
```

Observed on real PR #24:

```text
Backend Quality
Backend PostgreSQL
Backend CI Gate
Dependency Review
```

Protected `main` requires:

```text
Backend CI Gate
Dependency Review
```

Both were selected in the GitHub ruleset UI from source **GitHub Actions**, and the branch must be up to date before merge. Required checks are enforced through the `lifeos-main-safety` repository ruleset; classic branch-protection context output is not the ruleset authority.

Repository owner also enabled full-length Action SHA enforcement. The connected GitHub integration cannot directly read that setting, so documentation records it as owner-applied / connector-unverifiable rather than false API PASS.

No arbitrary coverage threshold was introduced.

## Historical CP5 closure truth

CP5 re-ran the integrated backend scaffold on the canonical WSL2/Linux workstation against the then-current PostgreSQL 18.4 envelope and directly observed:

```text
uv 0.12.5 / Python 3.14.7                 PASS
locked bootstrap                          PASS
Ruff + mypy                               PASS
fast pytest                               32/32 PASS
canonical PostgreSQL image rebuild        PASS
PostgreSQL acceptance                     18/18 PASS
full pytest                               50/50 PASS
wheel + sdist                             PASS
LOCAL PostgreSQL healthy                  PASS
explicit DB provisioning                  PASS
real Uvicorn startup                      PASS
/health/live                              200 PASS
/health/ready                             200 PASS
```

A single intervening Docker Desktop/WSL `/forwards/expose` 500 was isolated to local port-forwarding state; the subsequent clean full suite passed 50/50. No backend source change was required.

## Backend scaffold protected-main integration

Verified integration record:

```text
PR #24                                  MERGED
pre-merge main                          ff46eb16b971b1fde96eef9047b09faa02e1a5db
feature/backend-scaffold final HEAD     46b775bfbfc4747daff341d973df133646dbd0c8
merge commit / protected main           41680497c94b0c2f4830679b93f8eb6f1d543f8d
Backend CI push-main run                32502330955 SUCCESS
```

The merge commit has exactly the expected two parents. The merge gate did not delete the feature branch, activate CodeQL, mutate frontend, alter the ruleset or start concrete business-schema implementation.

## Exact next handoffs

```text
BACKEND
1. Treat CP1–CP5 and backend scaffold integration as CLOSED / DIRECT QA PASS.
2. Preserve their exact PostgreSQL 18.4 historical evidence.
3. Treat CP6-01 as CLOSED / GATE 01 PASS.
4. Treat CP6-02 as CLOSED / GATE 02 PASS.
5. Preserve PostgreSQL 18.6 direct technical evidence at run 32568664940 / HEAD ec3dc795....
6. Start CP6-03 read/research/design-first from the closed Constitution and full CP6-01 coverage ledger.
7. Do not create business DDL merely to materialize topology or obtain proof.
8. Do not implement Vertical #1 anywhere inside CP6.
9. CodeQL remains a separate activation boundary and is not implicitly authorized.

FRONTEND
1. Continue feature/frontend-materialization independently.
2. Execute its carried direct validations progressively.
3. Reconcile shared global docs semantically at integration time.
```

No production/direct PASS is authorized merely by design closure or workflow existence.
