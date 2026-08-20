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

## Current lifecycle status

```text
Product/North Star                 CURRENT
Domain Model                       CLOSED
Logical Model                      CLOSED
Pre-Physical coherence             CLOSED
Physical target                    CLOSED / ACCEPTED
Engineering Foundation v0          CLOSED / ACCEPTED
Frontend Foundation Passo 1        DESIGN COMPLETE / branch-local
Frontend Foundation Passo 2        DESIGN COMPLETE / branch-local
Frontend Foundation Passo 3        CLEAN REVIEW IN PROGRESS
Production backend scaffold        NOT STARTED
Production frontend scaffold       NOT STARTED
Direct HG / frontend PSV           NOT RUN
```

## Mandatory entry points

### Project/current truth

- `../README.md`
- `PROJECT-STATUS.md`
- `ROADMAP.md`

### Development governance

- `development/agent-operating-manual.md`
- `development/operating-rules.md`
- `development/documentation-and-handoff.md`
- `development/branching-and-environments.md`
- `development/repository-engineering-safety.md`

### Engineering Foundation — closed

- `workstreams/engineering-foundation.md`
- `development/engineering-foundation-v0.md`
- `development/repository-layout-v0.md`
- `development/application-structure-v0.md`
- `development/environments-and-promotion-v0.md`
- `development/config-and-secrets-v0.md`
- `development/toolchain-and-dx-v0.md`
- `development/testing-and-ci-v0.md`

### Frontend Engineering Foundation — active branch-local

- `workstreams/frontend-foundation.md` — live save-game/current step
- `architecture/frontend-engineering-foundation.md` — Passo-1 technology specification
- `architecture/frontend-engineering-foundation-part-2.md` — Passo-2 application/package/data-authority specification
- `decisions/ADR-008-frontend-engineering-stack.md` — technology decision
- `decisions/ADR-009-frontend-architecture-boundaries.md` — structural decision

### Architecture

- `architecture/README.md`
- `architecture/system-overview.md`
- `architecture/technical-decisions.md`

### Domain / Logical / Physical

Use their indexes and accepted linked sources. Any Physical-consuming implementation also consumes the post-selection validation register.

Historical evidence remains historical.

## Current engineering direction

One product monorepo with accepted root ownership for:

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

Backend Engineering Foundation is closed. Frontend Passo 1 and Passo 2 are design-complete on the active branch and Passo 3 clean review/closure is next.

Frontend durable rules include feature-first platform-specific apps, public-API-only/acyclic dependencies, real-consumer shared packages, explicit Data Authority Matrix, backend canonical effect authority, Web online-first, mobile local/offline PowerSync posture, PWA/service-worker dormant, identity-scoped local data, shared semantic tokens with platform-specific UI and one DANTE LOCAL/DEV/UAT/PROD vocabulary.

Cloud/backend compute provider and IaC engine remain deferred until their real infrastructure boundary.

## Repository identity

Continue in the existing repository. Creating a new implementation repo is not the plan.

## Exact next handoff

```text
1. Complete Frontend Foundation Passo 3 clean review.
2. If blockers == 0, record frontend design/architecture closure.
3. Prepare/integrate through protected main only with explicit authorization.
4. After integration, open a new exact scope for production frontend materialization/direct validation.
5. Backend scaffold remains a separate not-started implementation scope.
```

No production code/direct PASS is authorized merely by design closure.
