# Branching and Environments

- Status: Accepted project workflow
- Last updated: 2026-08-19

## Git model

`main` is the single integrated source of truth for accepted code, documentation and decisions.

Normal work uses bounded branches such as:

- `feature/*` — production features or foundations;
- `fix/*` — bug fixes;
- `docs/*` — documentation/governance work;
- `chore/*` — bounded repository/coherence/maintenance work;
- `prototype/*` — bounded exploratory work that is not yet production implementation.

Changes reach `main` through pull requests. A branch should not become a permanent second source of project truth.

Long-running exploratory/model branches may exist temporarily, but durable accepted decisions/documentation discovered there must eventually be integrated into `main` or explicitly closed as rejected/historical.

Detailed source precedence, path ownership, write gates and coherence rules are defined in [`agent-operating-manual.md`](agent-operating-manual.md) and [`operating-rules.md`](operating-rules.md).

Repository-level enforcement and the lifecycle for branch rules, CI checks and security settings are defined in [`repository-engineering-safety.md`](repository-engineering-safety.md). Repository settings must enforce this Git model where practical, but a documented policy is not considered applied until the remote setting is verified.

## Starting a branch

1. Start normal new work from current `main`.
2. Use an existing non-main branch only when the active workstream handoff explicitly identifies it as the current branch for that work.
3. Before editing overlapping/shared files, compare the active branch with current `main` and synchronize/review material drift when practical.
4. Keep one primary branch per workstream where possible.
5. If two proposed workstreams would modify the same core/shared files heavily, sequence them or combine them instead of manufacturing avoidable merge conflicts.
6. Before the first remote write, follow the exact PRE-SCOPE/write-gate protocol in the agent operating manual.

Historical workstream state:

```text
chore/pre-physical-coherence
DEFINITIVE CLOSED / FINAL QA PASS
integrated into main via PR #13
post-merge aligned via PR #14

feature/physical-model
PM-00..PM-14 TARGET-ARCHITECTURE WORK COMPLETE
selected canonical primary PostgreSQL 18.4
PM-13 architecture/documentation QA PASS
merged into protected main via PR #15
auto-deleted after merge
```

Current bounded engineering work:

```text
chore/engineering-foundation-v0
ACTIVE / UNMERGED
PRE-SCOPE ebc3616956faeabd99d90f5f32458b284be218e4
production code NOT STARTED
```

Closed Domain/Logical/Physical branches are historical evidence, not starting points for new backend work. Any genuine semantic or Physical reopen requires its own explicit scope/methodology rather than reuse of a historical branch by convenience.

## Why there is no permanent `develop` branch

A permanent `develop` branch would create a second integrated state that can drift from `main`. DANTE uses protected `main` plus short-lived bounded branches and deployment environments.

Engineering Foundation v0 is an **engineering-design workstream**, not a permanent Git `develop` branch.

The previously proposed standalone `Development Profile v0` is no longer the next separate phase; its useful operational concerns are captured by Engineering Foundation and resolved further at the real capability/release boundary that needs them.

If future release management creates a measured need for release branches, that decision can be added later. Release branches are not the default.

## LOCAL / DEV / UAT / PROD

These names describe execution/deployment lifecycle contexts, not Git branches.

### LOCAL

Purpose:

- individual development;
- fast inner-loop validation;
- disposable state;
- real local PostgreSQL semantics when persistence is involved.

Foundation baseline:

- Linux semantics are canonical for backend/server development;
- Windows backend development uses WSL2/Linux semantics;
- stateful selected dependencies use Docker Compose when activated;
- application processes normally run directly in the developer environment for fast reload/debug;
- synthetic/non-sensitive data and non-production credentials only.

LOCAL is not promoted. Source/artifacts are.

### DEV

Purpose:

- integration testing;
- active development validation of accepted `main` builds;
- shared synthetic/test/demo data;
- non-production credentials/services;
- early provider/environment integration.

Normal direction: deploy the latest accepted `main` artifact automatically or on demand once stable workflows exist. Feature branches may use isolated preview environments when useful, without becoming shared canonical DEV state.

DEV does not receive production data/credentials by design.

Selected Physical components are activated when their implemented capability requires them. Restate and pgBackRest/AWS S3 retain their already-fixed dormant initial-DEV posture.

### UAT / Staging

Purpose:

- acceptance testing;
- realistic end-to-end validation;
- migration/deployment rehearsal;
- supported-client compatibility verification;
- release-candidate verification.

A UAT deployment records at minimum the exact source commit and artifact/build identity and, where applicable, artifact digest and migration revision.

UAT should resemble PROD behavior/topology as far as practical without using PROD credentials or an ad-hoc copy of production personal data.

### PROD

Purpose:

- real released service/data.

Promotion should use the same immutable server/web artifact already accepted in UAT whenever the platform permits, with environment-specific configuration/secrets supplied externally.

Mobile is an explicit exception where different signed/environment-specific binaries may be required; each build remains traceable to the same reviewed source/locked dependency graph and an explicit build profile.

Production releases are traceable to a Git commit and later to a release tag such as `v1.0.0` when semantic public release versioning begins.

## Promotion model

Conceptually:

```text
feature/fix/docs/chore/prototype branch
          ↓ PR + validation
protected main
          ↓ build exact artifact
         DEV
          ↓ select/promote exact candidate
         UAT
          ↓ acceptance + release gates
         PROD
```

GitHub Actions is the Engineering Foundation baseline for primary repository CI/CD orchestration. GitHub Environments are the intended privileged deployment boundaries for `dev`, `uat` and `prod` once real deployment workflows exist.

This selects the orchestration layer; it does **not** select the compute hosting provider, artifact registry or IaC engine, which remain deferred until real remote infrastructure is implemented.

## Artifact/promotion discipline

A release candidate is not “whatever `main` points to now”. It has exact identity.

Where applicable record:

```text
source Git SHA
build ID
artifact/image digest
migration revision
application version/release tag
mobile build identity/profile
```

If a fix is required after UAT selection, produce a new commit/artifact and re-promote it. Do not patch deployable binaries/containers in place.

Database schema changes are controlled release operations. Application replicas do not independently run Alembic migrations at startup. Risky schema changes use backward-compatible expand/migrate/contract sequencing where required.

## Environment isolation

DEV, UAT and PROD use separate state and credentials where the provider supports meaningful isolation.

Default:

```text
DEV DB != UAT DB != PROD DB
DEV credentials != UAT credentials != PROD credentials
DEV object namespace != UAT != PROD
```

A lower environment must not hold broad production credentials “for convenience”. Production database copies are not the default source of DEV/UAT fixtures.

## Preview environments

Preview environments are optional, ephemeral and noncanonical.

When used:

- isolate credentials/data;
- no PROD secrets;
- clean up automatically where practical;
- do not replace shared DEV;
- no durable personal test data without a purpose/lifecycle;
- failure/cleanup must not mutate DEV/UAT/PROD.

## Parallel branch discipline

Parallel branches must minimize shared-file churn.

- Workstream-local progress belongs in the workstream's own code/docs/handoff paths.
- `PROJECT-STATUS.md`, root `README.md`, `docs/README.md`, `docs/ROADMAP.md`, broad architecture docs and ADRs are global coordination/current-truth files; do not modify them for every local iteration.
- A prototype branch may contain newer prototype-specific decisions without becoming authoritative for unrelated backend/domain decisions.
- An architecture/engineering branch may contain newer bounded decisions only inside its explicit workstream scope; it does not become a second global truth.
- Before copying files from historical branches, compare them against `main` and preserve newer accepted semantics.
- Do not force-push shared active branches or rewrite history merely for cosmetic cleanliness.
- If a shared file is stale, fix it inside an explicit scope rather than opportunistically while working on unrelated code.

## Main-branch enforcement

The repository safety target for `main` is deliberately aligned with this workflow rather than a separate Git model.

The last remotely verified owner-driven effective rules include:

```text
pull request required before merge
force-push / non-fast-forward blocked
delete protected main blocked
review-thread resolution required
required approvals = 0 while no independent reviewer exists
required status checks = none until real stable checks exist
merge commits allowed/required by current merge policy
```

Do not manufacture a required status check before the corresponding workflow/check context exists and has run successfully. Engineering Foundation may define future check classes, but checks are promoted into required-main rules only after exact emitted context names and blocking value are remotely verified.

Do not treat intended future repository settings as active merely because documented. Read back effective remote rules before claiming a changed safety milestone PASS.

## Current stage boundary

As of 2026-08-19:

- Core Domain Model / Domain Atlas is **CLOSED / integrated**;
- Logical Model is **CLOSED / integrated / WL-H01..WL-H12 active**;
- Pre-Physical Repository & Architecture Coherence is **DEFINITIVE CLOSED / FINAL QA PASS / integrated / post-merge verified**;
- Physical Model target architecture is **CLOSED / SELECTED / ACCEPTED / integrated**, with PostgreSQL 18.4 canonical primary;
- direct selected-stack implementation validation remains **NOT STARTED / DIRECT HG PASS 0**;
- Engineering Foundation v0 is **ACTIVE / UNMERGED** on `chore/engineering-foundation-v0`;
- backend/production application implementation is **NOT STARTED**;
- standalone Development Profile v0 is **no longer the next separate scope**;
- Phase 4 UX continues separately on `prototype/phase-4-today-home`.

Restate remains selected but dormant in initial DEV until the first real Class-B durable-workflow need; self-hosted vs Cloud EU is decided only at that activation boundary. pgBackRest/AWS S3 remain dormant in initial DEV until recovery/production boundary or a real recovery rehearsal.

## Branch lifecycle

1. Start from current `main` unless an active workstream explicitly requires another base.
2. Establish the workstream/handoff and exact PRE-SCOPE where required.
3. Keep scope bounded.
4. Commit code/tests/docs for the same change together logically where practical.
5. Open a PR early when useful; draft PRs are appropriate for work in progress.
6. Keep the branch synchronized enough to expose conflicts before merge.
7. Before merge, run semantic/documentation/engineering coherence plus exact post-write/compare QA.
8. Merge only when scope and required validation are coherent.
9. After an important merge, synchronize long-running branches that share changed global files.
10. Delete/archive obsolete working branches according to repository housekeeping policy; never delete history merely to hide prior reasoning.

Repository hygiene:

- automatic deletion of merged head branches is enabled based on last verified repository state;
- unmerged active branches are never auto-classified as obsolete by age alone;
- historical branch deletion requires proof no unique accepted/active work is lost;
- branch deletion is not a substitute for Git history/evidence retention.

## Definition of Done for a PR

As applicable:

- implementation/design/documentation scope complete;
- approved PRE-SCOPE delta matches expected paths;
- tests/validation complete at the scope actually claimed;
- migrations and rollback implications considered when relevant;
- relevant durable documentation updated;
- workstream handoff updated;
- global status updated only if globally meaningful;
- ADR/current-baseline/supersession treatment added for significant architectural decisions;
- branch compared against current `main` before merge;
- overlapping shared docs checked for semantic freshness;
- no secrets or personal production data/local artifacts committed;
- environment/deployment impact noted;
- required repository/CI checks that actually exist are passing;
- blocking review conversations resolved where policy requires;
- remote readback/QA supports any PASS/CLOSED claim.

## Emergency production fixes

When production exists, urgent fixes still originate from canonical history and are merged back into `main`. Do not create permanent environment branches requiring repeated cherry-picks.

If an emergency direct-main repair is ever explicitly approved because normal PR flow is unavailable or would worsen an active incident, record the reason/resulting commit and restore normal protected-branch discipline immediately afterward. Emergency exception language must never become a standing bypass.
