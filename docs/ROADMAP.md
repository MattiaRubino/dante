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
Frontend integration hardening                CLOSED / integrated via PR #28
Frontend CI Gate calibration                  COMPLETE
Frontend CI Gate promotion                    OWNER-CONFIRMED APPLIED / DIRECT API READBACK UNAVAILABLE
```

Architecture closure remains distinct from implementation/direct validation.

## Frontend integration closure

PR #28 integrated the already-closed frontend materialization into protected `main` while preserving evidence history and applying bounded integration hardening.

Integrated scope:

```text
Mobile src/** explicit TypeScript scope
Expo dependency compatibility CI gate
tracked + untracked repository-mutation CI gate
Frontend CI Gate aggregate context
least-privilege Frontend CI permissions
pnpm minimumReleaseAge 24h
npm/pnpm Dependabot scope
narrow Dependency Review accepted-risk exceptions
CURRENT documentation reconciliation
Frontend CI Gate green/red/recovery calibration
canonical three-check protected-main ruleset definition
```

Final integration evidence:

```text
final PR head        a6607ceabd35f874dc9e5f63fe8f57f71a92bf80
prior main           fd3bc8dd918cf6aadeff4572221af68612c3cb42
merge commit         f1aacb0724088e0b4b086008a5219c2fba5ce0cf
PR #28               MERGED
merge parentage      PASS — exactly prior main + final PR head
merged tree identity PASS — 0 file delta from PR head to merged main tree
```

The final PR head directly passed Dependency Review, Backend Quality, Backend PostgreSQL, Backend CI Gate, Frontend Quality, Web E2E, Mobile Bundle and Frontend CI Gate.

The available connector does not expose push-triggered workflow-run lookup for the merge SHA, therefore push-main CI is recorded as **DIRECT READBACK UNAVAILABLE**, not inferred PASS.

The integration branch was observed absent after merge; no manual branch deletion was performed during the merge operation.

## Frontend CI Gate calibration — COMPLETE

Directly proved:

```text
real green
controlled deliberate red
mandatory upstream failure propagation
exact workflow restore
recovery green
```

The deliberate-red change was bounded and reversible and did not introduce a vulnerable dependency or weaken unrelated policy.

## Required-check promotion — OWNER-CONFIRMED APPLIED

The canonical repository ruleset definition contains:

```text
Backend CI Gate
Dependency Review
Frontend CI Gate
```

with strict branch-up-to-date policy preserved.

The repository owner confirmed applying the `Frontend CI Gate` promotion in GitHub. The available connector does not expose direct ruleset readback, so this administrative state remains **OWNER-CONFIRMED APPLIED / DIRECT API READBACK UNAVAILABLE**, not independently API-verified.

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
-> CodeQL default setup evaluation under a fresh explicit gate

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