# DANTE Documentation Index

This directory is the durable documentation authority for DANTE.

## Authority order

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
Product / North Star                 CURRENT
Domain Model                         CLOSED
Logical Model                        CLOSED
Pre-Physical coherence               CLOSED
Physical target                      CLOSED / ACCEPTED
Engineering Foundation v0            CLOSED / ACCEPTED
Frontend Engineering Foundation      CLOSED / ACCEPTED / integrated via PR #22
Production backend scaffold          CLOSED / DIRECT QA PASS / integrated via PR #24
Frontend materialization             CLOSED / PASS — FM-00..FM-07
Frontend integration hardening       CLOSED / INTEGRATED VIA PR #28
Frontend CI Gate calibration         COMPLETE
Frontend CI Gate promotion           OWNER-CONFIRMED APPLIED / DIRECT API READBACK UNAVAILABLE
Concrete PostgreSQL business map     NOT STARTED
Product vertical implementation      NOT STARTED
Production deployment                NOT STARTED
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

### Backend scaffold — closed / integrated

- `workstreams/backend-scaffold.md`
- `development/backend-cp1-contract.md`
- `development/backend-cp2-postgres-contract.md`
- `development/backend-cp3-persistence-contract.md`
- `development/backend-cp4-ci-contract.md`
- `development/local-backend-workstation-bootstrap.md`

### Frontend Foundation — closed

- `workstreams/frontend-foundation.md`
- `architecture/frontend-engineering-foundation.md`
- `architecture/frontend-engineering-foundation-part-2.md`
- `architecture/frontend-engineering-foundation-final-review.md`
- `architecture/frontend-engineering-foundation-post-closure-qa.md`
- `decisions/ADR-008-frontend-engineering-stack.md`
- `decisions/ADR-009-frontend-architecture-boundaries.md`

### Frontend materialization — closed / direct evidence

- `workstreams/frontend-materialization.md` — FM-00..FM-07 detailed evidence authority
- `development/frontend-local-development.md` — verified local development/runtime runbook

### Frontend integration — closed / integrated

- `workstreams/frontend-materialization-integration.md` — closed PR #28 integration-hardening record, accepted-risk lifecycle and durable future-activation register

### Architecture

- `architecture/README.md`
- `architecture/system-overview.md`
- `architecture/technical-decisions.md`

## Current engineering truth

The repository is one DANTE product monorepo. Real materialized roots currently include backend, Web, Mobile, shared packages, tooling, infrastructure definitions, tests, docs, prototypes and GitHub automation according to their accepted ownership boundaries.

Backend scaffold truth is integrated into protected `main` and includes Python 3.14.7, uv 0.12.5, Ruff, mypy strict, pytest, SQLAlchemy 2.0, psycopg 3, Alembic, DANTE-owned PostgreSQL 18.4 LOCAL image, least-privilege roles, real PostgreSQL acceptance and calibrated `Backend CI Gate`.

Frontend materialization is CLOSED / PASS and directly proved the Node/pnpm/Turbo/TypeScript workspace, Web React/Vite/TanStack Router application, Expo/React Native Android path, shared design-token/i18n/time packages, architecture enforcement, deterministic generated sources, unit tests, Web E2E, Android Hermes bundle smoke, Android emulator runtime and GitHub-hosted Frontend CI.

Frontend materialization integration is also CLOSED / integrated through PR #28. Final PR head `a6607ceabd35f874dc9e5f63fe8f57f71a92bf80` merged to protected `main` as `f1aacb0724088e0b4b086008a5219c2fba5ce0cf`; the merge commit has the expected two parents and the merged main tree has zero file delta from the final PR head.

The final PR head passed Dependency Review, Backend CI and Frontend CI including both aggregate gates. The available connector does not expose push-triggered workflow-run lookup for the merge SHA, so push-main CI remains **DIRECT READBACK UNAVAILABLE** rather than inferred PASS.

## Materialization qualification rule

The Frontend Foundation records the design-time technology selection. Later direct materialization evidence qualifies the implemented baseline without reopening the whole architecture.

Current qualified examples:

```text
@dante/time implementation       temporal-polyfill 1.0.4
Mobile Gesture Handler           2.32.0 / Expo SDK 57-qualified
Web E2E location                 apps/web/e2e/
Mobile React                     19.2.3 / Expo compatibility PASS
Web React + React DOM            19.2.8 / 19.2.8
```

Older version-specific design wording does not override later directly validated implementation evidence.

## CI / repository safety truth

The canonical protected-main ruleset definition contains:

```text
Backend CI Gate
Dependency Review
Frontend CI Gate
```

with strict branch-up-to-date policy, PR-before-merge, review-thread resolution, merge-commit-only policy, and deletion/non-fast-forward protection.

`Frontend CI Gate` completed real-green, controlled deliberate-red, mandatory failure propagation, exact restore and recovery-green calibration. The repository owner confirmed applying its protected-main promotion. Direct ruleset API readback is unavailable in the connector, therefore the administrative setting is recorded as **OWNER-CONFIRMED APPLIED / DIRECT API READBACK UNAVAILABLE** rather than independently API-verified.

Dependency Review remains `moderate+` fail-closed. The exact temporary GHSA exceptions and review deadline are documented in the closed integration handoff; no global suppression is authorized.

## Future activation register

Do not install infrastructure merely because a large application might eventually use it. Trigger-based future capabilities are recorded in `workstreams/frontend-materialization-integration.md`, including:

- React/Expo lint hardening and app-local feature boundary enforcement at the first real product vertical;
- component/RNTL/a11y/Storybook/visual testing when real UI exists;
- TanStack Form + Zod at the first real form;
- Orval/API client + TanStack Query at the first real remote product API;
- PowerSync/SQLCipher path at the first real offline operation;
- runtime config/Cloudflare/Sentry at shared DEV/Web deployment;
- EAS/Maestro/signed-device/iOS validation at Mobile release activation;
- CodeQL after integrated TypeScript + Python source is on `main`;
- performance, browser matrix, SBOM/provenance/license/security intake before production maturity;
- remote Turbo cache, merge queue, CODEOWNERS, feature flags and large device farms only when scale justifies them.

## Exact next handoff

```text
REPOSITORY SECURITY NEXT CANDIDATE
CodeQL default setup evaluation under a fresh explicit gate

BACKEND NEXT
Concrete Logical -> PostgreSQL through a fresh bounded workstream/gate

PRODUCT NEXT
first real vertical slice
-> activate only capabilities actually consumed
```

No production/direct PASS is inferred merely from design closure, selected technology or workflow existence.