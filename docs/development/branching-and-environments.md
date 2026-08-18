# Branching and Environments

- Status: Accepted project workflow
- Last updated: 2026-08-18

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
3. Before editing overlapping/shared files, compare the active branch with current `main` and synchronize it when practical.
4. Keep one primary branch per workstream where possible.
5. If two proposed workstreams would modify the same core/shared files heavily, sequence them or combine them instead of manufacturing avoidable merge conflicts.
6. Before the first remote write, follow the exact PRE-SCOPE/write-gate protocol in the agent operating manual.

`chore/pre-physical-coherence` is branch-locally **DEFINITIVE CLOSED / FINAL QA PASS** and remains unmerged. Until protected integration is separately authorized and completed, no future Backend Foundation or Physical Model branch may rewrite the same current sources concurrently. Integrate/synchronize the prerequisite state or explicitly re-scope first.

Closed Domain/Logical branches are historical evidence, not starting points for new backend work. Any genuine semantic reopen requires its own explicit scope/methodology rather than reuse of a historical branch by convenience.

## Why there is no permanent `develop` branch

A permanent `develop` branch would create a second integrated state that can drift from `main`. LifeOS instead uses `main` plus bounded branches and deployment environments.

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
feature/fix/docs/chore/prototype branch
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
- `PROJECT-STATUS.md`, root `README.md`, `docs/README.md`, `docs/ROADMAP.md`, broad architecture docs and ADRs are global coordination/current-truth files; do not modify them for every local iteration.
- A prototype branch may contain newer prototype-specific decisions without becoming authoritative for unrelated backend/domain decisions.
- A model/architecture branch may contain newer bounded decisions only inside its explicit workstream scope; it does not become a second global truth.
- Before copying files from historical branches, compare them against `main` and preserve newer accepted semantics.
- Do not force-push shared active branches or rewrite history merely to make synchronization look cleaner.
- If a shared file is stale, fix it inside an explicit scope rather than opportunistically while working on unrelated code.

## Main-branch enforcement

The repository safety target for `main` is deliberately aligned with this workflow rather than a separate Git model.

The current owner-driven effective rules have been remotely verified:

```text
pull request required before merge
force-push / non-fast-forward blocked
delete protected main blocked
review-thread resolution required
required approvals = 0 while no independent reviewer exists
required status checks = none until real stable checks exist
merge commits allowed/required by current merge policy
```

Do not manufacture a required status check before the corresponding workflow/check context exists and has run successfully. When real CI is introduced, promote checks into required-main rules only after their exact stable context names and blocking value are verified.

Do not treat future repository rules/settings as active merely because their intended configuration is documented. Read back effective remote rules before claiming a changed safety milestone PASS.

## Current stage boundary

As of 2026-08-18:

- Core Domain Model / Domain Atlas is closed and integrated into `main`;
- Logical Model is closed and integrated into `main`;
- `chore/pre-physical-coherence` is **DEFINITIVE CLOSED / FINAL QA PASS** branch-locally after the independent total audit and final remote activation QA;
- Phase 12 clean-room QA is **QA PASS / CLOSED**;
- Physical readiness is established, but the Physical Model is **NOT STARTED / NOT AUTHORIZED** and requires a separate future authorization;
- Backend Foundation/production implementation is **NOT STARTED / DEFERRED**;
- Phase 4 UX continues separately on `prototype/phase-4-today-home`;
- Pre-Physical `main` integration is **PENDING / NOT PERFORMED** and requires separate protected-PR authorization.

Closure activation checkpoint: `9c53e812d13ffd1b3d3d3dc20b8b162799e13c1d`.

This stage note is a current operational baseline, not a permanent branching rule. Future agents must re-check `docs/PROJECT-STATUS.md`, the active handoff and Git refs.

## Branch lifecycle

1. Start from current `main` unless the workstream explicitly requires another active base.
2. Establish the workstream/handoff and exact PRE-SCOPE where required.
3. Keep scope bounded.
4. Commit code/tests/docs for the same change together logically where practical.
5. Open a PR early when useful; draft PRs are appropriate for work in progress.
6. Keep the branch synchronized enough to expose conflicts before merge.
7. Before merge, run the semantic/documentation coherence gate from `operating-rules.md` plus the exact post-write/compare QA required by the agent operating manual.
8. Merge only when implementation/design and required documentation/handoff are coherent.
9. After an important merge, synchronize long-running branches that share changed global files.
10. Delete or archive obsolete working branches according to repository housekeeping policy; never delete history merely to hide prior reasoning.

Repository hygiene rules:

- automatic deletion of merged head branches is currently enabled;
- unmerged active branches are never auto-classified as obsolete by age alone;
- an old/historical branch is deleted only after proving it contains no unique accepted/active work that still requires integration;
- obviously accidental refs may be deleted after ancestry/content verification shows no unique branch-only work;
- branch deletion is not a substitute for Git history/evidence retention.

## Definition of Done for a PR

As applicable:

- implementation/design/documentation scope complete;
- approved PRE-SCOPE delta matches expected paths;
- tests/validation complete;
- migrations and rollback implications considered when relevant;
- relevant durable documentation updated;
- workstream handoff updated;
- `PROJECT-STATUS.md` updated only if global state changed;
- ADR/current-baseline/supersession treatment added for significant architectural decisions;
- branch compared against current `main` before merge;
- overlapping shared docs checked for semantic freshness;
- no secrets or personal production data committed;
- environment/deployment impact noted;
- any required repository/CI checks that actually exist are passing;
- remote readback/QA supports any PASS/CLOSED claim.

## Emergency production fixes

When production exists, urgent fixes should still originate from the canonical history and be merged back into `main`. Do not create permanent environment branches that require repeated manual cherry-picking.

If an emergency direct-main repair is ever explicitly approved because normal PR flow is unavailable or would worsen an active incident, record the reason and resulting commit, then restore normal protected-branch discipline immediately after the repair. Emergency exception language must not become a standing bypass.