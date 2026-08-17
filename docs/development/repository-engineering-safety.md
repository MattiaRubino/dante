# Repository Engineering Safety

- Status: **CURRENT — Phase 11 content; GitHub settings application/verification pending**
- Scope: repository integration safety before Physical/backend production implementation
- Repository: `MattiaRubino/lifeos`
- Default branch: `main`
- Physical Model: **NOT STARTED / NOT AUTHORIZED**
- Backend Foundation: **NOT STARTED / DEFERRED**

## Purpose

Make the repository enforce the Git discipline LifeOS already documents without inventing premature CI, enterprise ceremony or implementation infrastructure.

This contract separates:

```text
DOCUMENTED REPOSITORY POLICY
!=
GITHUB SETTING ACTUALLY APPLIED
```

Phase 11 is not complete merely because this file or a ruleset JSON exists. Closure requires remote evidence that the applicable GitHub settings are actually active.

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

## Phase 11 observed repository state

Observed remotely on 2026-08-17 before Phase 11 writes:

```text
repository visibility              public
default branch                     main
main protected                     false
repository rulesets                0
required status checks             0
GitHub Actions workflows           0
Dependabot alerts                  disabled
pull request template              present
CODEOWNERS                          absent
.github/dependabot.yml             absent
SECURITY.md                         absent
```

Secret-scanning/code-scanning alert APIs were not readable through the connected GitHub integration, so their dashboard state was **not inferred**.

The connector exposed no mutation for repository rulesets/settings and no delete-ref action. These GitHub-side settings therefore require an authenticated user/admin action outside the connector followed by remote verification.

## Current safety objective

The repository is currently owner-driven. Safety should prevent accidental corruption without creating gates that require nonexistent reviewers or nonexistent CI.

Therefore the immediate target is:

```text
protect main from deletion
protect main from force-push
require integration through pull request
require review conversations to be resolved
require zero approvals while the repository has no independent reviewer
require zero status checks while no stable checks exist
preserve merge commits/history
```

This is deliberately strong against destructive mistakes and deliberately light on ceremony that would provide no real safety today.

# Main branch ruleset

Canonical importable definition:

`github-main-ruleset.json`

Expected ruleset identity:

```text
name        lifeos-main-safety
target      branch
enforcement active
condition   ~DEFAULT_BRANCH
bypass      none by default
```

Expected effective rules:

```text
DELETE TARGET REF
blocked

FORCE PUSH
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

A required approval only adds real safety when an independent reviewer can provide it. In the current owner-driven repository, requiring one approval would either block legitimate work or force an artificial bypass.

The review count MUST be reconsidered when:

- another regular human maintainer/reviewer exists; or
- an accepted governance process assigns independent approval responsibility.

At that point, changing `0 → 1+` is a repository-policy change and should be gated/documented.

## Why required checks are empty now

Phase 11 observed:

```text
GitHub Actions workflows = 0
commit status contexts   = 0
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

No required check should be created that makes `main` unmergeable because the underlying workflow does not exist.

## Future check classes

The following are categories, not current check names or implementation authorization:

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
only when executable benchmark tooling exists
```

Concrete workflow names, runners, language versions and tool selections belong to the future implementation scope that creates them.

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

LifeOS currently preserves workstream PRE-SCOPEs, checkpoint SHAs and intermediate evidence in Git history.

Therefore the current ruleset permits only:

```text
merge commits
```

for protected-main pull-request integration.

This avoids silently destroying intermediate evidence through mandatory squash/rebase. A future change to merge policy requires explicit evaluation of evidence/history consequences.

# Security posture

## Secrets

Repository rules already prohibit secrets and personal production data in commits.

GitHub secret scanning / push protection SHOULD be enabled where available for this public repository. Phase 11 closure must verify their repository/security setting state manually or through an API with sufficient permissions; absence of connector visibility is not proof of either enabled or disabled state.

Do not place production secrets in:

- repository files;
- example config values that are real credentials;
- Actions workflow source;
- CI logs/artifacts;
- benchmark fixtures.

## Dependabot

Observed current state:

```text
Dependabot alerts = disabled
```

Phase 11 target:

```text
Dependabot alerts = enabled
```

Do **not** create `.github/dependabot.yml` yet merely to populate the repository. Dependency-update scheduling belongs when actual package ecosystems/manifests exist.

## Code scanning

No code-scanning workflow is created by Phase 11.

Code scanning / CodeQL becomes relevant when actual production source code exists and the concrete language/build topology is known. Any future code-scanning gate must first produce real results before it can be made a required main check.

## CODEOWNERS

`CODEOWNERS` is intentionally not created now. A single owner naming himself as code owner does not create independent review safety.

Introduce CODEOWNERS when ownership/reviewer responsibility becomes meaningfully distributed.

## SECURITY.md

Phase 11 does not create a public security-contact/vulnerability policy before a production/released security process exists. Revisit before a public production release or when external vulnerability reporting becomes operationally meaningful.

# Branch hygiene

## Active branches

Do not delete branches merely because they are old-looking.

Known active bounded branches at Phase 11 inventory include:

```text
chore/pre-physical-coherence
prototype/phase-4-today-home
```

The active prototype also has an open draft pull request and must not be removed.

## Historical branches

Historical/model/documentation branches may be deleted only after proving that:

```text
unique accepted work not integrated       0
current active work owned by branch       0
required evidence available elsewhere     PASS
```

Deletion is hygiene, not a way to hide project history.

## Confirmed accidental refs

Phase 11 inventory found these accidental branches:

```text
__do_not_create__
__noop_should_fail__
__tmp_should_not_create__
```

For each, remote comparison showed its tip is an ancestor of `main`; no unique branch-only project history must be preserved.

Disposition:

```text
SAFE TO DELETE
```

The earlier accidental `__no-op__` ref is already absent at Phase 11 inventory time.

The available connector cannot delete refs, so deletion of the three remaining accidental branches is a required external/manual repository-hygiene step before Phase 11 closure.

## Automatic merged-branch cleanup

Target repository setting:

```text
Automatically delete head branches after merge = enabled
```

This reduces stale working-branch accumulation without deleting unmerged active branches.

# GitHub-side application checklist

Phase 11 remains **PENDING SETTINGS VERIFICATION** until all applicable items below are checked.

## A — import main ruleset

Import:

`docs/development/github-main-ruleset.json`

Expected result:

```text
lifeos-main-safety
active
~DEFAULT_BRANCH
PR required
0 approvals
review-thread resolution required
deletion blocked
force-push blocked
merge only
no required status checks yet
```

## B — repository branch cleanup setting

Enable automatic deletion of merged head branches.

## C — dependency alerts

Enable Dependabot alerts.

## D — secret security

Verify secret scanning and push protection in repository security settings; enable where available/applicable for the public repository.

## E — delete confirmed accidental refs

Delete exactly:

```text
__do_not_create__
__noop_should_fail__
__tmp_should_not_create__
```

Do not bulk-delete other branches as part of this action.

# Phase 11 verification contract

After the settings are applied, verify remotely where possible:

```text
repository rulesets contains lifeos-main-safety     PASS
ruleset enforcement active                          PASS
main effective rules include PR/deletion/force-push PASS
required status checks                              0 expected today
Dependabot alerts enabled                           PASS
accidental ref __do_not_create__                    404
accidental ref __noop_should_fail__                  404
accidental ref __tmp_should_not_create__             404
auto-delete merged branches                         true
main SHA/content                                     unchanged by settings
```

Secret scanning / push protection may require UI evidence if the connector lacks permission to read their state; record the limitation truthfully rather than inferring it.

Only after this verification may repository/global current state say:

```text
PHASE 11
QA PASS
```

# Future production readiness

Before production backend work begins, repository safety must evolve with the codebase rather than remain frozen at this documentation-only stage.

Expected progression:

```text
now
main ruleset + PR discipline + security alerts

first implementation
real tests/lint/types/security workflows

stable workflow contexts
promote material checks into required main rules

Physical/migrations exist
add real Physical/migration checks

release/deployment exists
add environment/release protections based on actual promotion design
```

Release tags, deployment environments, merge queues and environment approvals are intentionally premature today.

# Phase 11 acceptance

Content readiness requires:

```text
repository inventory complete                 PASS
ruleset definition complete                   PASS
future-check activation policy complete       PASS
security-setting plan complete                PASS
branch-hygiene classification complete        PASS
manual/external settings steps explicit       PASS
```

Final Phase 11 closure additionally requires GitHub-side application and remote verification.

Until then:

```text
PHASE 11
CONTENT READY / SETTINGS VERIFICATION PENDING

PHYSICAL MODEL
NOT STARTED / NOT AUTHORIZED

BACKEND FOUNDATION
NOT STARTED / DEFERRED
```
