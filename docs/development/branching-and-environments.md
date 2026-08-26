# Branching and Environments

- **Status:** CURRENT
- **Last reconciled:** 2026-08-26

## 1. Core rule

Git branches represent source-change scope. Runtime environments represent deployed state.

```text
BRANCH != ENVIRONMENT
```

DANTE does not use permanent `develop`, `uat`, `staging` or `production` branches as environment state.

## 2. Integrated source truth

Protected `main` is the only integrated source truth.

Normal flow:

```text
bounded branch
→ PR + applicable validation
→ protected main
```

Short-lived prefixes may include `feature/`, `fix/`, `chore/`, `docs/`, `prototype/`. Prefix never authorizes work outside the explicit gate.

Do not create a permanent generic `feature/backend` or `feature/frontend` branch as a parallel integration line. Product work uses bounded branches named for the real workstream.

## 3. Exact write gate

Before remote mutation:

```text
BRANCH
<exact branch>

PRE-SCOPE
<exact SHA>

CREATE
<paths>

UPDATE
<paths>

DELETE
<paths>

PURPOSE
<bounded purpose>

EXPLICITLY OUT OF SCOPE
<non-scope>
```

Immediately before the first branch-visible write, verify branch HEAD still equals PRE-SCOPE. If it moved: stop, inspect, re-gate.

A new chat/session is not a reason to create another branch or worktree. Continue the existing bounded workstream unless its lifecycle has actually closed or the user explicitly changes scope.

## 4. Protected-main integration

Effective repository rules are owned by the live GitHub ruleset `lifeos-main-safety`.

Current enforcement includes:

```text
PR required
allowed merge method: merge commit only
strict required-status-check policy
branch must be current with main
review threads must be resolved
deletion protection
non-fast-forward protection
bypass actors: none
```

Current required checks:

```text
Backend CI Gate
Dependency Review
Frontend CI Gate
```

Before merge:

- inspect exact changed paths;
- inspect the current live ruleset when integration behavior matters;
- inspect applicable real checks/statuses on the exact current PR/head;
- require branch current with `main` when strict policy requires it;
- verify no unexpected branch movement;
- verify accepted-risk/waiver state is still valid;
- verify review threads are resolved;
- preserve merge-commit history policy;
- do not bypass with squash, rebase, force-push or synthetic status tricks.

After merge:

- reread/compare `main`;
- verify exact integration result and parentage;
- verify PR `merged=true`;
- verify the resulting protected-main tree/commit relation;
- inspect push-main CI where it actually exists and can be read;
- record unavailable/nonexistent evidence as such rather than inventing PASS;
- verify branch lifecycle/autodelete only when intentionally relevant.

## 5. Environment vocabulary

Exactly:

```text
LOCAL
DEV
UAT
PROD
```

`TEST` may exist as an automated execution context but is not a promotion environment. Preview environments may exist when useful.

Frontend/mobile provider profile/channel names map to these DANTE contexts rather than creating a second taxonomy.

## 6. Activation

```text
LOCAL   individual development / direct implementation
DEV     first shared remote integration
UAT     real release-candidate acceptance
PROD    accepted production release
```

Remote resources are not created merely for appearance.

## 7. LOCAL posture

Backend and frontend use authoritative WSL-backed worktrees on Windows systems. Windows may host JetBrains, browser and Android emulator.

Current user worktree pattern includes separate worktrees for genuinely concurrent branches, for example backend/general repository work and an independent frontend Access branch. Multiple worktrees are valid when they represent different real branches; duplicate clones of the same repository state are not the default strategy.

```text
NO divergent Windows + WSL source clones
NO cross-OS shared node_modules
NO accidental branch switch in the wrong worktree
```

Backend process normally runs directly in WSL for reload/debug; Docker Compose owns LOCAL stateful dependencies. Frontend Metro/Vite/pnpm/Turbo run from the authoritative Linux/WSL tree; Windows browser/emulator are native bridge consumers.

## 8. DEV / UAT / PROD isolation

Target:

```text
DEV state     != UAT state     != PROD state
DEV identity  != UAT identity  != PROD identity
DEV secrets   != UAT secrets   != PROD secrets
```

Raw PROD → DEV is forbidden by default. UAT uses exact release candidates and representative synthetic/sanitized data. PROD uses isolated real state/identity/secrets and accepted recovery/security/observability posture.

## 9. Artifact promotion

Server default:

```text
accepted main
→ build once
→ immutable artifact/digest
→ DEV
→ exact UAT candidate
→ exact PROD candidate
```

Web supports immutable SPA promotion with environment-specific public runtime config when that boundary activates. Mobile follows Expo/EAS native-binary/update compatibility semantics rather than pretending native binaries and OTA JS are the same artifact class.

## 10. Required status checks

A documented future job name is not a required check.

Promotion protocol for a new required context:

```text
real workflow/context
+ real PR green
+ controlled deliberate red proving intended failure semantics when appropriate
+ recovery green
→ separate explicit ruleset mutation
→ live ruleset readback
```

The current live ruleset directly confirms:

```text
Backend CI Gate
Dependency Review
Frontend CI Gate
```

with strict branch-up-to-date enforcement. This live remote readback supersedes older documentation that described `Frontend CI Gate` as merely owner-confirmed / connector-unverifiable.

Required-check names must match real emitted contexts exactly; never manufacture a context merely to satisfy a rule.

## 11. One-developer posture

While one regular maintainer exists:

- PR + automated gates remain real;
- required approvals remain 0 unless the live ruleset changes;
- review-thread resolution remains required;
- do not create fake independent-review ceremony;
- add CODEOWNERS/required reviewers only when real distributed ownership exists.

## 12. Current branch/workstream truth

Protected `main` current backend/database baseline includes CP1–CP6, with CP6 integrated via PR #42.

Current known active unmerged product branch:

```text
feature/access-frontend
→ Access frontend workstream
→ AF-01D / AF-02A / AF-02B PASS
→ Access vertical still OPEN
→ branch-local workstream record + temporary live handoff
→ must reconcile with current main before integration
```

The documentation lifecycle/current-truth cleanup is a bounded maintenance change, not a permanent development line. Once its reviewed policy/index changes enter `main`, future documentation maintenance uses ordinary bounded `docs/` or `chore/` branches only when real work exists.

Closed feature branches are not reusable integration lines. New work starts from current protected `main` under a fresh bounded branch unless an already-active workstream explicitly continues on its existing branch.

## 13. Worktree discipline

A worktree is tied to one checked-out branch.

Before commands that can mutate source/ref state, verify:

```text
pwd
git status -sb
git branch --show-current
git rev-parse HEAD
git worktree list
```

Do not switch a worktree onto another branch merely because a new chat begins.

If two workstreams must continue concurrently, separate worktrees are appropriate. If one workstream has closed and the worktree is being repurposed, first reconcile/close its branch lifecycle intentionally.

## 14. Documentation lifecycle at branch integration

Temporary live/session/resume handoffs are branch-operational only.

Before merging a branch into `main`:

```text
temporary handoffs
→ knowledge coverage
→ durable current truth updated
→ important evidence/rationale retained
→ optional one consolidated branch-history record
→ temporary handoffs deleted
```

Protected `main` must not contain `live-handoff`/session-resume files as current navigation.

See `documentation-lifecycle-policy.md`.

## 15. Capability activation

Product/infrastructure capabilities are activated by real boundary, not branch name.

Examples:

```text
PowerSync
→ real offline/multi-device requirement

R2
→ real ContentArtifact byte flow

Restate
→ first real Class-B durable workflow

pgBackRest
→ recovery/production boundary

CodeQL or other security controls
→ explicit repository-security workstream/gate when justified
```

No branch prefix turns a selected technology into an implemented/directly validated capability.

## 16. Current next boundaries

Backend CP6 is no longer the next branch; it is closed/integrated.

Current practical boundaries are:

```text
FRONTEND
continue existing feature/access-frontend
→ do not create another Access branch/worktree merely for a new chat
→ reconcile with current main before final integration

BACKEND
next post-CP6 product vertical
→ create only when explicitly scoped
→ branch from current protected main
→ consume the existing materialized database

DOCUMENTATION
apply the lifecycle/current-truth policy continuously
→ create a bounded maintenance branch only for real documentation work
→ never accumulate live/session handoffs on protected main
```

A genuine later DB requirement uses normal forward migration/database-documentation synchronization; it does not reopen `feature/logical-postgresql`.

## 17. Persistent rules

```text
BRANCH != ENVIRONMENT
NEW CHAT != NEW BRANCH
ACTIVE WORKSTREAM != NEW WORKTREE BY DEFAULT
UNMERGED BRANCH TRUTH != PROTECTED-main TRUTH
CLOSED BRANCH != PERMANENT DEVELOPMENT LINE
SELECTED TECHNOLOGY != IMPLEMENTED CAPABILITY
DOCUMENTED CHECK != LIVE REQUIRED CHECK
TEMPORARY HANDOFF != DURABLE main DOCUMENTATION
```