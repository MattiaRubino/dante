# DANTE Roadmap

- Status: **CURRENT**

## Completed foundations

```text
Product / North Star                         CURRENT
Domain Model                                 CLOSED
Logical Model                                CLOSED
Pre-Physical coherence                       CLOSED
Physical target                              CLOSED / ACCEPTED
Engineering Foundation v0                    CLOSED / ACCEPTED
Frontend Engineering Foundation              CLOSED / ACCEPTED / integrated via PR #22
Production backend scaffold CP1..CP5          CLOSED / integrated via PR #24
Frontend materialization FM-00..FM-07         CLOSED / PASS
```

Architecture closure remains distinct from implementation/direct validation.

## Active integration workstream

### Frontend materialization integration hardening — ACTIVE

Branch:

`chore/frontend-materialization-integration`

PR:

`#28` — draft

Purpose:

- integrate the already-closed frontend materialization into current protected-main truth without rewriting its evidence history;
- reconcile shared/current documentation semantically;
- close bounded hardening found during final review;
- calibrate the new aggregate `Frontend CI Gate` before any required-check promotion.

Already materialized in the integration branch:

```text
Mobile src/** explicit TypeScript scope
Expo dependency compatibility CI gate
tracked + untracked repository-mutation CI gate
Frontend CI Gate aggregate context
least-privilege Frontend CI permissions
pnpm minimumReleaseAge 24h
npm/pnpm Dependabot scope
narrow Dependency Review accepted-risk exceptions
```

Combined PR candidate `a91fbfc3dcce4ada128cd1c9ae0971eadb531e06` directly observed:

```text
Dependency Review   PASS
Backend CI          PASS
Frontend CI         PASS
Quality             PASS
Web E2E             PASS
Mobile Bundle       PASS
Frontend CI Gate    PASS
```

The current documentation-reconciliation commit must earn its own PR CI before final-candidate classification.

## Immediate sequence

### 1. Reconcile CURRENT truth — IN PROGRESS

Remove stale claims such as frontend/backend scaffold “not started”, record the closed frontend materialization, preserve backend CP1-CP5 integrated truth and qualify version-specific Frontend Foundation design text against later direct materialization evidence.

### 2. Re-prove combined candidate

Required before closure of integration hardening:

```text
Backend CI          GREEN
Dependency Review   GREEN
Frontend CI         GREEN
Frontend CI Gate    GREEN
branch current with main
unexpected paths    0
```

### 3. Calibrate Frontend CI Gate

The context has already emitted a real green on PR #28.

Still required before promotion:

```text
controlled deliberate red
-> prove mandatory upstream failure propagates to Frontend CI Gate
-> restore exact intended workflow
-> recovery green
```

The deliberate-red change must be bounded, reversible and must not introduce a real vulnerable dependency or weaken unrelated policy.

### 4. Required-check promotion — separate governance mutation

Only after green -> deliberate red -> recovery green may `Frontend CI Gate` be considered for the protected-main ruleset.

Current required checks remain:

```text
Backend CI Gate
Dependency Review
```

Do not mutate the ruleset implicitly inside implementation/docs work.

### 5. Final PR review / protected-main merge

Before merge:

- PR #28 current with `main`;
- exact changed paths reviewed;
- accepted-risk register still valid;
- applicable checks green;
- no stale CURRENT docs;
- no unresolved review threads;
- expected head verified.

Merge authorization remains separate from this roadmap.

## Backend next boundary

### Concrete Logical -> PostgreSQL

Backend scaffold is already closed and integrated. The next backend implementation boundary is a fresh bounded workstream that consumes the closed Logical owner/ref/invariant contracts plus accepted PostgreSQL posture.

```text
consume Logical authorities
-> propose concrete table/constraint/index/history mapping
-> review
-> Alembic migrations
-> real PostgreSQL tests
-> persistence/application vertical slice
```

Do not mechanically translate 57 Logical owners into 57 tables/services.

## Product vertical slices

After foundational integration, product work proceeds vertically rather than by completing every possible infrastructure layer first:

```text
user capability
-> required canonical data
-> domain/application behavior
-> persistence/migration if needed
-> API boundary if needed
-> Web/Mobile feature boundary
-> direct acceptance evidence
```

Each vertical activates only the selected capabilities it actually consumes.

## Future activation triggers

The durable activation register lives in `docs/workstreams/frontend-materialization-integration.md`.

Key triggers:

```text
first real product vertical
-> Expo/React Hooks lint qualification
-> executable feature/ui/platform boundaries
-> Web component tests / Mobile RNTL as applicable

first real UI/design-system surface
-> WCAG 2.2 AA target
-> a11y automation
-> Storybook / visual regression only when justified

first form
-> TanStack Form + Zod

first remote product API
-> FastAPI OpenAPI -> Orval
-> @dante/api-client
-> TanStack Query

first Mobile offline operation
-> PowerSync + OP-SQLite/SQLCipher
-> identity-scoped local DB lifecycle
-> accept/reject/conflict reconciliation tests

first shared DEV/Web deployment
-> versioned runtime config
-> Cloudflare delivery
-> Sentry/source-map qualification

first Mobile release candidate
-> EAS Build/Submit/Update
-> Maestro where useful
-> signed-device validation
-> iOS direct validation when activated

post frontend integration on main
-> CodeQL default setup evaluation

pre-PROD
-> broader browser matrix
-> representative performance budgets
-> SBOM/provenance where required
-> license policy
-> SECURITY.md/vulnerability intake
-> explicit privacy/security threat review

scale-triggered only
-> Turbo remote cache
-> merge queue
-> CODEOWNERS / real independent reviewers
-> generic feature flags
-> large browser/device farms
```

## Capability-triggered Physical implementation

Other selected specialist components remain dormant until real requirements:

```text
R2                  -> ContentArtifact byte flow
OR-Tools            -> solver-backed planning
Restate             -> Class-B durable workflow
pgBackRest + S3     -> recovery boundary/rehearsal
PowerSync           -> real offline/multi-device operation
```

## Environment progression

```text
LOCAL
-> current implementation boundary

DEV
-> activate when shared remote integration provides real value

UAT
-> activate for real release candidates

PROD
-> activate only at production readiness
```

## Persistent rules

```text
SELECTED != IMPLEMENTED
DOCUMENTATION PASS != DIRECT IMPLEMENTATION PASS
CLIENT LOCAL STATE != CANONICAL EFFECT AUTHORITY
ENVIRONMENT != GIT BRANCH
WORKFLOW EXISTS != TRUSTED CHECK
TRUSTED CHECK != REQUIRED CHECK UNTIL CALIBRATED
CLOSED FEATURE BRANCH != INTEGRATED MAIN UNTIL VERIFIED MERGE
```

Continue from durable contracts/handoffs instead of redesigning closed decisions from conversation memory.