# Repository Engineering Safety

- Status: **CURRENT — Phase 11 QA PASS**
- Scope: repository integration safety before and during Physical/backend production implementation
- Repository: `MattiaRubino/lifeos`
- Default branch: `main`
- Physical Model: **CLOSED / SELECTED / ACCEPTED / INTEGRATED INTO MAIN VIA PR #15**
- Direct selected-stack implementation validation: **NOT STARTED / DIRECT HG PASS 0**
- Backend Foundation: **NOT STARTED / DEFERRED**
- Development Profile v0: **NOT STARTED / NEXT SEPARATE OPERATIONAL SCOPE**

## Purpose

Make the repository enforce the Git discipline LifeOS already documents without inventing premature CI, enterprise ceremony or implementation infrastructure.

```text
DOCUMENTED REPOSITORY POLICY
!=
GITHUB SETTING ACTUALLY APPLIED
```

Phase 11 closed only because both the policy and the applicable GitHub-side protections were verified where the connector permits verification.

## Authority

This file complements, and does not replace:

- `agent-operating-manual.md`;
- `operating-rules.md`;
- `branching-and-environments.md`;
- `documentation-and-handoff.md`;
- the active workstream handoff.

Existing project rules remain authoritative:

```text
main = one integrated source of truth
normal work = bounded branch
integration = pull request
no direct main work except explicitly approved emergency repair
no force-push of shared history for cosmetic cleanup
remote evidence required before PASS / CLOSED
```

## Phase 11 verified repository state

Verified on 2026-08-17 after GitHub-side application:

```text
repository visibility              public
default branch                     main
ruleset                            lifeos-main-safety
ruleset enforcement                active
ruleset target                     ~DEFAULT_BRANCH
ruleset bypass                     none
main deletion                      blocked
main non-fast-forward / force push blocked
pull request before merge          required
required approving reviews         0
review-thread resolution           required
allowed merge method               merge
required status checks             0
GitHub Actions workflows           0
auto-delete merged head branches  enabled
confirmed accidental refs          absent
Physical Model                     NOT STARTED / NOT AUTHORIZED at Phase-11 closure
Backend Foundation                 NOT STARTED / DEFERRED
```

The ruleset was verified remotely through GitHub's repository ruleset API. The three confirmed accidental refs `__do_not_create__`, `__noop_should_fail__` and `__tmp_should_not_create__` were verified absent after cleanup. The earlier `__no-op__` ref was already absent before Phase 11 closure.

Dependabot and secret/code-scanning alert state is not readable through the connected GitHub integration because the relevant endpoints return `403 Resource not accessible by integration`. The user/admin applied the requested repository security settings, but this connector limitation is recorded rather than converted into false API evidence.

## Current safety objective

The repository is currently owner-driven. Safety prevents destructive mistakes without creating gates that require nonexistent reviewers or nonexistent CI.

Current main protection therefore is:

```text
protect main from deletion
protect main from force-push / non-fast-forward updates
require integration through pull request
require review conversations to be resolved
require zero approvals while no independent reviewer exists
require zero status checks while no stable checks exist
preserve merge commits/history
```

## Main branch ruleset

Canonical repository definition:

`github-main-ruleset.json`

Current verified identity:

```text
name        lifeos-main-safety
target      branch
enforcement active
condition   ~DEFAULT_BRANCH
bypass      none
```

Current effective rules:

```text
DELETE TARGET REF
blocked

FORCE PUSH / NON-FAST-FORWARD
blocked

PULL REQUEST BEFORE MERGE
required

APPROVING REVIEWS
0

REVIEW THREAD RESOLUTION
required

ALLOWED MERGE METHOD
merge

REQUIRED STATUS CHECKS
none until real stable checks exist
```

## Why zero approvals is intentional

A required approval adds real safety only when an independent reviewer can provide it. In the current owner-driven repository, requiring one approval would either block legitimate work or force an artificial bypass.

Reconsider the review count when:

- another regular human maintainer/reviewer exists; or
- an accepted governance process assigns independent approval responsibility.

Changing `0 → 1+` is a repository-policy change and should be gated/documented.

## Why required checks are empty now

Phase 11 verified:

```text
GitHub Actions workflows = 0
required status checks   = 0
```

A required check MUST NOT be configured merely because a future check name sounds desirable.

Activation rule:

```text
check exists
+ runs on the relevant pull-request path
+ produces a stable unique context name
+ has demonstrated successful execution
+ is materially required for integration safety
→ MAY become required
```

No required check should make `main` unmergeable because the underlying workflow does not exist.

## Future check classes

These are categories, not current workflow names or implementation authorization:

```text
backend tests
backend lint
backend type checks
backend security/static analysis

web tests/lint/types/build
mobile equivalent checks where applicable

Physical/migration validation
only when an accepted Physical implementation exists

benchmark evidence validation
only when executable benchmark tooling exists and produces stable useful checks
```

Concrete workflow names, runners, language versions and tool selections belong to the future implementation scope that creates them.

Direct selected-stack validation may later create bounded tests/harnesses under exact gated paths. Their existence does not automatically justify a required `main` status check; promotion still requires the stable-context protocol below.

## Required-check promotion protocol

Before adding a status check to the main ruleset:

1. create the real workflow/check in an approved scope;
2. run it on a real branch/PR;
3. confirm the exact emitted context name;
4. confirm it does not depend on unavailable production secrets for normal PR validation;
5. confirm its failure means integration should actually stop;
6. update this contract/ruleset only if the check should become mandatory;
7. re-read effective branch rules after applying the change.

## Merge/history posture

LifeOS preserves workstream PRE-SCOPEs, checkpoint SHAs and intermediate evidence in Git history.

The current ruleset therefore allows only merge commits for protected-main pull-request integration. A future merge-policy change requires explicit evaluation of evidence/history consequences.

# Security posture

## Secrets

Repository rules prohibit secrets and personal production data in commits.

Secret scanning / push protection should remain enabled where available for this public repository. Their dashboard/API state could not be independently read through the current connector, so future security audits should re-check them using an API/session with sufficient permissions.

Do not place production secrets in repository files, real example credentials, Actions workflow source, CI logs/artifacts or benchmark fixtures.

Physical/direct-validation fixtures must be synthetic/non-sensitive. Raw validation artifacts committed or durably referenced must not contain real personal production data or credentials.

## Dependabot

Dependabot alerts were disabled at the initial Phase 11 inventory. The requested admin action was applied by the repository owner, but the connector cannot independently verify the resulting state because the vulnerability-alerts endpoint is inaccessible to the integration.

Do not create `.github/dependabot.yml` merely to populate the repository. Dependency-update scheduling belongs when actual package ecosystems/manifests exist.

## Code scanning

No code-scanning workflow is created by Phase 11.

Code scanning / CodeQL becomes relevant when actual source code/harness code exists and the concrete language/build topology is known. A future code-scanning gate must produce real results before becoming a required main check.

Benchmark/direct-validation harness code is not production backend code by identity; security/static analysis requirements must be chosen according to the actual code introduced and its risk.

## CODEOWNERS

`CODEOWNERS` is intentionally not created now. A single owner naming himself as code owner does not create independent review safety. Introduce CODEOWNERS when ownership/reviewer responsibility becomes meaningfully distributed.

## SECURITY.md

Phase 11 does not create a public vulnerability-reporting policy before a production/released security process exists. Revisit before public production release or when external vulnerability reporting becomes operationally meaningful.

# Branch hygiene

## Active branches

Do not delete branches merely because they look old.

Known active bounded branches relevant to current project work include:

```text
prototype/phase-4-today-home
```

The former `feature/physical-model` branch is no longer active. It was merged into protected `main` via PR #15 at merge commit `e6f191bad947388a44defe2c15f4939345084f58` and auto-deleted after successful merge. Its accepted result is now part of `main`; Git/PR history preserves its evidence.

`chore/pre-physical-coherence` is **not active**: it was merged into protected `main` via PR #13 and auto-deleted after successful merge. Its accepted result is now part of `main`; Git/PR history preserves its evidence.

The prototype branch has an open draft pull request and must not be removed while active.

## Historical branches

Historical/model/documentation branches may be deleted only after proving:

```text
unique accepted work not integrated       0
current active work owned by branch       0
required evidence available elsewhere     PASS
```

Deletion is hygiene, not a way to hide project history.

## Confirmed accidental refs

Phase 11 classified and cleaned:

```text
__do_not_create__          absent
__noop_should_fail__       absent
__tmp_should_not_create__  absent
__no-op__                  already absent before closure
```

Each confirmed accidental ref that still existed was an ancestor of `main`, so no unique branch-only project history was lost.

## Automatic merged-branch cleanup

Verified repository setting:

```text
Automatically delete head branches after merge = enabled
```

This reduces stale working-branch accumulation without deleting unmerged active branches. PR #13, post-merge alignment PR #14 and Physical integration PR #15 all exercised the merged-head cleanup path.

# Phase 11 verification evidence

Core repository-safety verification:

```text
ruleset lifeos-main-safety present                 PASS
ruleset enforcement active                        PASS
ruleset target ~DEFAULT_BRANCH                    PASS
bypass actors none                                PASS
main deletion protection                          PASS
main non-fast-forward/force-push protection       PASS
pull request required                             PASS
required approvals = 0                            PASS
review-thread resolution required                 PASS
allowed merge method = merge                      PASS
required status checks = 0                        PASS / expected today
auto-delete merged branches = true                PASS
__do_not_create__                                 404 / PASS
__noop_should_fail__                              404 / PASS
__tmp_should_not_create__                          404 / PASS
main SHA unchanged during settings application    PASS
```

Connector-limited security verification:

```text
Dependabot alerts API           403 / connector-unverifiable
secret scanning alert API       403 / connector-unverifiable
code scanning alert API         403 / connector-unverifiable
```

These connector permission limits do not invalidate the verified branch-integration protections; they remain explicit future audit items rather than inferred PASS/FAIL values.

## Later protected-integration evidence

The closed Pre-Physical and Physical workstreams exercised the accepted repository-safety posture through PR #13, current-truth alignment PR #14 and Physical integration PR #15:

```text
PR #13 mergeable before merge               PASS
review threads                              0
required / emitted status checks            0 / expected under current policy
expected head SHA lock                      used
merge method                                merge
merged                                      PASS
main merge commit                           74593ae283ce5a1d22335502480ee3fa54be0436
final branch tree vs merged main tree       0 file differences
merged head branch auto-delete              PASS

PR #14 current-truth alignment              MERGED / PASS
main after alignment                        3de84bb49f9cef30e88e9bde4961ed84335daa79
alignment branch tree vs merged main        0 file differences
alignment head branch auto-delete           PASS

PR #15 Physical Model integration           MERGED / PASS
main after Physical merge                   e6f191bad947388a44defe2c15f4939345084f58
former feature/physical-model branch         AUTO-DELETED
```

This later integration evidence does not change the Phase 11 policy; it demonstrates that the effective controls worked as designed.

# Physical/direct-validation repository safety

The closed Physical Model and its carried-forward direct implementation validation add execution/evidence risks that must be treated explicitly.

```text
BENCHMARK / VALIDATION HARNESS
!= production backend automatically

RAW VALIDATION ARTIFACT
!= current repository specification

OFFICIAL PRODUCT CLAIM
!= direct execution evidence

SELECTED
!= DIRECT PASS
```

Physical/direct-validation-specific safety rules:

1. every new mapping/schema/harness/evidence path requires an exact separately approved write gate;
2. do not commit real production credentials or personal data into selected-stack databases/fixtures;
3. record exact selected component version/edition/deployment and hardware for reproducibility where material;
4. retain or durably reference raw evidence with hashes/reproduction metadata;
5. do not rely on ephemeral Actions artifacts alone for final direct-validation evidence;
6. validation infrastructure must not silently become production architecture;
7. an unexecuted tier/test remains `NOT RUN`;
8. insufficient/contradictory evidence remains `HOLD`;
9. PM-11 selection and PM-12 acceptance do not create direct PASS;
10. Physical closure/integration does not authorize Backend Foundation.

# Future production readiness

Repository safety must evolve with the codebase rather than remain frozen at this documentation-first stage.

```text
now
main ruleset + PR discipline + branch hygiene/security settings
+ closed/integrated Physical target
+ Development Profile v0 next

selected-stack direct validation / backend implementation
real tests/harness validation as appropriate

stable useful workflow contexts
optionally promote material checks into required main rules

accepted Physical implementation/migrations exist
add real Physical/migration checks

backend implementation begins
real backend tests/lint/types/security workflows

release/deployment exists
add environment/release protections based on actual promotion design
```

Release tags, deployment environments, merge queues and environment approvals are intentionally premature today.

# Phase 11 acceptance and current downstream state

```text
repository inventory complete                 PASS
ruleset definition complete                   PASS
ruleset applied and remotely verified         PASS
future-check activation policy complete       PASS
branch-hygiene classification complete        PASS
confirmed accidental refs removed             PASS
auto-delete merged branches                   PASS
security-setting connector limits recorded    PASS
Domain reopen required                        0
Logical reopen required                       0
```

Current state:

```text
PHASE 11
QA PASS

PRE-PHYSICAL COHERENCE
DEFINITIVE CLOSED / FINAL QA PASS
INTEGRATED / POST-MERGE VERIFIED

PHYSICAL MODEL
CLOSED / SELECTED / ACCEPTED
INTEGRATED INTO MAIN VIA PR #15
selected canonical primary PostgreSQL 18.4
former feature/physical-model MERGED / AUTO-DELETED

DIRECT SELECTED-STACK IMPLEMENTATION VALIDATION
NOT STARTED
DIRECT HG PASS 0

BACKEND FOUNDATION
NOT STARTED / DEFERRED

DEVELOPMENT PROFILE v0
NOT STARTED / NEXT SEPARATE OPERATIONAL SCOPE
```

The next repository risk gate is the separately bounded Development Profile v0 scope. Any later direct selected-stack validation, backend schema/API implementation, CI promotion or repository-policy change requires its own exact authorization rather than inheriting permission from Physical closure.
