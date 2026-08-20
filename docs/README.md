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
Frontend Engineering Foundation    DESIGN/ARCHITECTURE CLOSED / ACCEPTED / FINAL REVIEW PASS
Frontend main integration          COMPLETE VIA PR #22
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

### Frontend Engineering Foundation — closed in design / integrated via PR #22

- `workstreams/frontend-foundation.md` — closure/integration handoff
- `architecture/frontend-engineering-foundation.md` — Passo-1 technology specification
- `architecture/frontend-engineering-foundation-part-2.md` — Passo-2 application/package/data-authority specification
- `architecture/frontend-engineering-foundation-final-review.md` — Passo-3 final review/closure evidence
- `architecture/frontend-engineering-foundation-post-closure-qa.md` — post-closure knowledge/evidence QA
- `decisions/ADR-008-frontend-engineering-stack.md` — technology decision
- `decisions/ADR-009-frontend-architecture-boundaries.md` — structural decision

### Architecture

- `architecture/README.md`
- `architecture/system-overview.md`
- `architecture/technical-decisions.md`

### Domain / Logical / Physical

Use their indexes and accepted linked sources. Physical-consuming implementation also consumes the applicable post-selection validation register.

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

Frontend durable rules include feature-first platform-specific apps, public-API-only/acyclic dependencies, real-consumer shared packages, Data Authority Matrix, backend canonical effect authority, Web online-first, Mobile PowerSync local/offline posture, PWA/service-worker dormant, identity-scoped local data, shared semantic tokens with platform-specific UI and one DANTE LOCAL/DEV/UAT/PROD vocabulary.

Cloud/backend compute provider and IaC engine remain deferred until their real infrastructure boundary.

## Exact next handoff

```text
1. Frontend Foundation design/architecture is CLOSED / ACCEPTED / integrated via PR #22.
2. Open a fresh exact frontend materialization/scaffold/direct-validation scope.
3. Materialize only real artifacts required by the accepted Foundation.
4. Execute direct validations progressively; do not manufacture PASS.
5. Backend scaffold remains a separate not-started implementation scope.
```

No production code/direct PASS is authorized merely by design closure.
