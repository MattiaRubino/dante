# DANTE Documentation Index

This directory is the durable documentation authority for DANTE.

## Current authority order

When sources conflict:

1. current `main` code/migrations/tests and accepted model/ADR;
2. current durable product/domain/logical/architecture/engineering docs on `main`;
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
Engineering Foundation v0          CLOSED / ACCEPTED
Frontend Engineering Foundation    CLOSED / ACCEPTED / FINAL REVIEW PASS
Frontend main integration          COMPLETE VIA PR #22
Frontend materialization           ACTIVE ON feature/frontend-materialization / DIRECT PASS NOT YET EARNED
Production backend scaffold        CLOSED ON feature/backend-scaffold / DIRECT QA PASS
Backend CP1                        CLOSED / DIRECT QA PASS
Backend CP2                        CLOSED / DIRECT QA PASS
Backend CP3                        CLOSED / DIRECT QA PASS
Backend CP4                        CLOSED / DIRECT REMOTE QA PASS
Backend CP5                        CLOSED / DIRECT INTEGRATED QA PASS
Backend integration PR #24         OPEN / MERGE NOT YET AUTHORIZED
Concrete PostgreSQL business map   NOT STARTED / NEXT AFTER SCAFFOLD INTEGRATION
Direct HG / blanket PSV            NOT RUN
```

## Mandatory entry points

### Project / current truth

- `../README.md`
- `PROJECT-STATUS.md`
- `ROADMAP.md`

### Development governance

- `development/agent-operating-manual.md`
- `development/operating-rules.md`
- `development/documentation-and-handoff.md`
- `development/branching-and-environments.md`
- `development/repository-engineering-safety.md`
- `development/github-main-ruleset.json`

### Backend scaffold — closed on feature branch / pending integration

- `workstreams/backend-scaffold.md` — production-backend scaffold handoff, CP1–CP5 evidence and exact resume point
- `development/backend-cp1-contract.md` — CP1 Python/process/config authority
- `development/backend-cp2-postgres-contract.md` — CP2 LOCAL PostgreSQL authority
- `development/backend-cp3-persistence-contract.md` — CP3 persistence/migrations/privileges/real-PostgreSQL authority
- `development/backend-cp4-ci-contract.md` — CP4 CI/security/calibration closure authority
- `development/local-backend-workstation-bootstrap.md` — verified WSL2/Docker/PyCharm-oriented workstation bootstrap

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

Historical evidence remains historical.

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

Backend closed-scaffold truth includes Python 3.14.7, exact uv 0.12.5 project authority, Ruff, mypy strict, pytest, SQLAlchemy 2.0 stable, psycopg 3, Alembic, the DANTE-owned PostgreSQL 18.4 image, least-privilege application roles, real PostgreSQL acceptance harness, calibrated CI and protected-main required checks.

Frontend durable rules include feature-first platform-specific apps, public-API-only acyclic dependencies, real-consumer shared packages, Data Authority Matrix, backend canonical effect authority, Web online-first, Mobile PowerSync local/offline posture, identity-scoped local data, shared semantic tokens with platform-specific UI and one DANTE LOCAL/DEV/UAT/PROD vocabulary.

Cloud/backend compute provider and IaC engine remain deferred until their real infrastructure boundary.

## CI truth

CP4 is closed on `feature/backend-scaffold` after direct local, remote green, deliberate-red and recovery-green evidence.

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

## CP5 closure truth

CP5 re-ran the integrated backend scaffold on the canonical WSL2/Linux workstation and directly observed:

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

## Exact next handoffs

```text
BACKEND
1. Treat CP1–CP5 as CLOSED / DIRECT QA PASS.
2. PR #24 remains the active backend integration PR and is not auto-merged.
3. Next backend action is a fresh explicit merge gate for PR #24 into protected main.
4. Revalidate required checks on the actual merge candidate and verify main after merge.
5. Concrete Logical → PostgreSQL becomes the next implementation boundary only after verified scaffold integration.
6. CodeQL remains a separate post-main activation boundary and is not implicitly authorized.

FRONTEND
1. Continue feature/frontend-materialization independently.
2. Execute its carried direct validations progressively.
3. Reconcile shared global docs semantically at integration time.
```

No production/direct PASS is authorized merely by design closure or workflow existence.