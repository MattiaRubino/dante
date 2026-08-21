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
Frontend Engineering Foundation    DESIGN/ARCHITECTURE CLOSED / ACCEPTED / FINAL REVIEW PASS
Frontend main integration          COMPLETE VIA PR #22
Frontend materialization           ACTIVE ON feature/frontend-materialization / DIRECT PASS NOT YET EARNED
Production backend scaffold        ACTIVE
Backend CP1                        CLOSED / DIRECT QA PASS
Backend CP2                        CLOSED / DIRECT QA PASS
Backend CP3                        CLOSED / DIRECT QA PASS
Backend CP4                        MATERIALIZED / LOCAL QA PASS / MAIN RECONCILED / REGRESSION QA NEXT
Backend CP5                        NOT STARTED
Concrete PostgreSQL business map   NOT STARTED
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

### Backend scaffold — active

- `workstreams/backend-scaffold.md` — active production-backend scaffold handoff and exact resume point
- `development/backend-cp1-contract.md` — CP1 Python/process/config contract and direct evidence
- `development/backend-cp2-postgres-contract.md` — CP2 LOCAL PostgreSQL contract and direct evidence
- `development/backend-cp3-persistence-contract.md` — CP3 persistence/migrations/privileges/real-PostgreSQL contract and direct evidence
- `development/backend-cp4-ci-contract.md` — CP4 CI/security/calibration contract and current materialization evidence
- `development/local-backend-workstation-bootstrap.md` — verified WSL2/Docker/PyCharm-oriented workstation bootstrap

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

- `workstreams/frontend-foundation.md` — closure/integration handoff
- `architecture/frontend-engineering-foundation.md` — technology specification
- `architecture/frontend-engineering-foundation-part-2.md` — application/package/data-authority specification
- `architecture/frontend-engineering-foundation-final-review.md` — final review/closure evidence
- `architecture/frontend-engineering-foundation-post-closure-qa.md` — post-closure knowledge/evidence QA
- `decisions/ADR-008-frontend-engineering-stack.md` — frontend technology ADR
- `decisions/ADR-009-frontend-architecture-boundaries.md` — frontend structural ADR

The currently active frontend materialization handoff lives on the separate branch `feature/frontend-materialization`; do not invent a branch-local file here before that branch is integrated.

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

Backend current branch truth includes Python 3.14.7, exact uv 0.12.5 project authority, Ruff, mypy strict, pytest, SQLAlchemy 2.0 stable, psycopg 3, Alembic, the DANTE-owned PostgreSQL 18.4 image and real PostgreSQL acceptance harness.

Frontend durable rules include feature-first platform-specific apps, public-API-only acyclic dependencies, real-consumer shared packages, Data Authority Matrix, backend canonical effect authority, Web online-first, Mobile PowerSync local/offline posture, identity-scoped local data, shared semantic tokens with platform-specific UI and one DANTE LOCAL/DEV/UAT/PROD vocabulary.

Cloud/backend compute provider and IaC engine remain deferred until their real infrastructure boundary.

## CI truth

CP4 has materialized on `feature/backend-scaffold`:

```text
.github/workflows/backend-ci.yml
.github/workflows/dependency-review.yml
.github/dependabot.yml
```

Local QA has directly passed, but remote PR calibration has not yet run. Required status checks therefore remain **0**. No remote green/red/recovery PASS may be inferred from YAML existence.

## Exact next handoffs

```text
BACKEND
1. Current main is reconciled into feature/backend-scaffold.
2. Run post-reconciliation locked quality + real PostgreSQL regression QA.
3. Open real CP4 calibration PR only after regression PASS.
4. Observe exact emitted checks.
5. Deliberate red → recovery green.
6. Only then consider required-check repository settings.
7. Close CP4, then CP5 scaffold closure.
8. Concrete Logical → PostgreSQL mapping starts only after scaffold closure.

FRONTEND
1. Continue feature/frontend-materialization independently.
2. Execute its carried direct validations progressively.
3. Reconcile shared global docs semantically at integration time.
```

No production/direct PASS is authorized merely by design closure or workflow existence.