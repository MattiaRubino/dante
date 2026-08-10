# Branching and Environments

- Status: Accepted project workflow
- Last updated: 2026-08-10

## Git model

`main` is the single integrated source of truth for accepted code, documentation and decisions.

Normal work uses short-lived branches such as:

- `feature/*` — production features or foundations;
- `fix/*` — bug fixes;
- `docs/*` — documentation/governance work;
- `prototype/*` — bounded exploratory work that is not yet production implementation.

Changes reach `main` through pull requests. A branch should not become a permanent second source of project truth.

Long-running exploratory branches may exist temporarily, but durable decisions/documentation discovered there must eventually be integrated into `main`.

Detailed source precedence, path ownership and coherence rules are defined in [`operating-rules.md`](operating-rules.md).

## Starting a branch

1. Start normal new work from current `main`.
2. Use an existing non-main branch only when the active workstream handoff explicitly identifies it as the current branch for that work.
3. Before editing overlapping/shared files, compare the active branch with current `main` and synchronize it when practical.
4. Keep one primary branch per workstream where possible.
5. If two proposed workstreams would modify the same core files heavily, sequence them or combine them instead of manufacturing avoidable merge conflicts.

For example, if Domain Model v0 is being built as part of Backend Foundation, it should normally live in `feature/backend-foundation` until the foundation boundary is stable rather than simultaneously editing the same files from `feature/domain-model`.

## Why there is no permanent `develop` branch

A permanent `develop` branch would create a second integrated state that can drift from `main`. LifeOS instead uses `main` plus short-lived branches and deployment environments.

If future release management creates a measured need for release branches, that decision can be added later. It is not the default.

## DEV / UAT / PROD

DEV, UAT and PROD are deployment environments, not Git branches.

### DEV

Purpose:

- integration testing;
- active development validation;
- test/demo data;
- non-production credentials/services.

Normal direction: deploy the latest accepted `main` build automatically or on demand. Feature branches may use isolated preview environments when useful, without becoming shared canonical DEV state.

### UAT / Staging

Purpose:

- acceptance testing;
- realistic end-to-end validation;
- migration/deployment rehearsal;
- release-candidate verification.

A UAT deployment must record the exact source commit and artifact/build identifier.

### PROD

Purpose:

- real released service/data.

Promotion should use the same immutable artifact already accepted in UAT whenever practical, with environment-specific configuration/secrets supplied externally.

Production releases should be traceable to a Git commit and later to a release tag such as `v1.0.0` when semantic release versioning begins.

## Promotion model

Conceptually:

```text
feature/fix/docs/prototype branch
          ↓ PR + validation
         main
          ↓
         DEV
          ↓ promote accepted artifact
         UAT
          ↓ approve/promote same artifact
         PROD
```

The exact CI/CD provider is intentionally not fixed yet.

## Parallel branch discipline

Parallel branches must minimize shared-file churn.

- Workstream-local progress belongs in the workstream's own code/docs/handoff paths.
- `PROJECT-STATUS.md`, root `README.md`, broad architecture docs and ADRs are global coordination files; do not modify them for every local iteration.
- A prototype branch may contain newer prototype-specific decisions without becoming authoritative for unrelated backend/domain decisions.
- Before copying files from historical branches, compare them against `main` and preserve newer accepted semantics.
- Do not force-push shared active branches or rewrite history merely to make synchronization look cleaner.

## Branch lifecycle

1. Start from current `main` unless the workstream explicitly requires another active prototype base.
2. Keep scope bounded.
3. Commit code/tests/docs for the same change together logically.
4. Open a PR early when useful; draft PRs are appropriate for work in progress.
5. Keep the branch synchronized enough to expose conflicts before merge.
6. Before merge, run the semantic/documentation coherence gate from `operating-rules.md`.
7. Merge only when implementation and required documentation/handoff are coherent.
8. After an important merge, synchronize long-running branches that share changed global files.
9. Delete or archive obsolete working branches later according to repository housekeeping policy; never delete history merely to hide prior reasoning.

## Definition of Done for a PR

As applicable:

- implementation/design change complete;
- tests/validation complete;
- migrations and rollback implications considered;
- relevant durable documentation updated;
- workstream handoff updated;
- `PROJECT-STATUS.md` updated only if global state changed;
- ADR added/updated for significant architectural decisions;
- branch compared against current `main` before merge;
- overlapping shared docs checked for semantic freshness;
- no secrets or personal production data committed;
- environment/deployment impact noted.

## Emergency production fixes

When production exists, urgent fixes should still originate from the canonical history and be merged back into `main`. Do not create permanent environment branches that require repeated manual cherry-picking.
