# Branching and Environments

- **Status:** CURRENT
- **Last reconciled:** 2026-09-05

## 1. Core rule

Git branches represent bounded source-change scope. Runtime environments represent deployed state.

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

Allowed short-lived prefixes include `feature/`, `fix/`, `chore/`, `docs/`, `prototype/`. A prefix never authorizes work outside the explicit gate.

Do not create permanent generic `feature/backend` or `feature/frontend` integration lines. Product/platform work uses bounded branches named for the real workstream.

A new chat/session is not a reason to create another branch or worktree. Continue the existing bounded workstream unless its lifecycle is actually closed or the user explicitly changes scope.

## 3. Exact write gate

Before branch-visible mutation:

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

Immediately before the first remote mutation verify that local/remote branch state still satisfies the gate. If the ref moved: stop, inspect and re-gate. Do not silently rewrite or force through concurrent movement.

## 4. Protected-main integration

Effective repository rules are owned by the live GitHub ruleset `lifeos-main-safety`; live enforcement outranks prose snapshots.

Current integration contract includes:

```text
PR required
merge method: merge commit only
strict required-status-check policy
branch current with main
review threads resolved
deletion protection
non-fast-forward protection
bypass actors: none
```

Current required checks documented by the repository:

```text
Backend CI Gate
Dependency Review
Frontend CI Gate
```

Before merge:

- inspect exact changed paths;
- inspect the live ruleset when integration behavior matters;
- inspect real checks/statuses on the exact current PR/head;
- require branch current with `main` when strict policy requires it;
- verify no unexpected branch movement;
- verify accepted-risk/waiver state is still valid;
- resolve review threads;
- preserve merge-commit history policy;
- do not bypass with squash, rebase, force-push or synthetic status tricks.

After merge:

- reread/compare `main`;
- verify PR `merged=true`;
- verify exact merge parentage/tree relation;
- inspect push-main CI where it exists and can be read;
- reconcile any candidate-state/current-document wording to the actual protected-main state;
- repair references to temporary/workstream overlays deliberately removed before integration;
- record unavailable/nonexistent evidence as unavailable rather than inventing PASS;
- close/archive/delete the feature branch only after the integration result is verified.

## 5. Environment vocabulary

Exactly:

```text
LOCAL
DEV
UAT
PROD
```

`TEST` may exist as automated execution context but is not a promotion environment. Preview environments may exist when useful.

## 6. Activation

```text
LOCAL   individual development / direct implementation
DEV     first shared remote integration
UAT     real release-candidate acceptance
PROD    accepted production release
```

Remote resources are not created merely to complete a diagram.

## 7. LOCAL posture

Backend and frontend use authoritative Linux/WSL-backed worktrees on Windows systems. Windows may host JetBrains, browser and Android emulator.

Multiple worktrees are valid when they represent different real concurrent branches. Duplicate divergent Windows + WSL source clones are not the default strategy.

```text
NO divergent Windows + WSL source clones
NO cross-OS shared node_modules
NO accidental branch switch in the wrong worktree
```

Backend process normally runs directly in WSL for reload/debug; Docker Compose owns LOCAL stateful dependencies. Frontend tooling runs from the authoritative Linux/WSL tree while Windows browser/emulator act as consumers.

## 8. DEV / UAT / PROD isolation

```text
DEV state     != UAT state     != PROD state
DEV identity  != UAT identity  != PROD identity
DEV secrets   != UAT secrets   != PROD secrets
```

Raw PROD → DEV is forbidden by default. UAT uses exact release candidates and representative synthetic/sanitized data. PROD uses isolated real state, identity and secrets plus accepted security/recovery/observability posture.

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

Web/mobile promotion follows platform-specific immutable artifact/config compatibility rules rather than pretending every surface has identical deployment semantics.

## 10. Required status checks

A documented future job name is not a required check.

Promotion protocol for a new required context:

```text
real workflow/context
+ real PR green
+ controlled deliberate red where appropriate
+ recovery green
→ separate explicit ruleset mutation
→ live ruleset readback
```

Required-check names must match emitted contexts exactly. Never manufacture a status to satisfy a rule.

## 11. One-developer posture

While one regular maintainer exists:

- PR + automated gates remain real;
- required approvals remain 0 unless live policy changes;
- review-thread resolution remains required;
- do not create fake independent-review ceremony;
- add CODEOWNERS/required reviewers only when real distributed ownership exists.

## 12. Current branch/workstream truth

Protected `main` contains the integrated CP1–CP6 backend/database baseline, the closed LOCAL PostgreSQL Recovery evolution, Access/Auth M1–M5, the Shared Email Platform, the forward Recovery↔Email reopen hardening and Platform Observability:

```text
CP6                              integrated via PR #42
PostgreSQL Recovery              CP01–CP07 LOCAL PASS / CLOSED / integrated via PR #47
Access/Auth + Shared Email       CLOSED / integrated via PR #52
Recovery↔Email application gate  CP08 PASS / integrated via PR #55
Platform Observability           CLOSED / integrated via PR #58
current Alembic                  20260904_17
current topology                 88|5|16|76|172|89|270|0|0|0
```

Platform Observability source work is closed and protected-main integration completed via PR `#58`, merge commit `b74a806deed68b2729dd04678c0a5674cd572e8a`. `feature/platform-observability` is closed source history; `integration/platform-observability-v2` is the closed accepted integration line; `integration/platform-observability` is the abandoned reconstruction attempt and must never be resumed or merged.

`feature/access-auth`, `feature/postgres-recovery` and `feature/access-frontend` are closed/integrated historical branch state. Their accepted results remain current protected-main/baseline evidence where applicable, but those branches are not current resume/integration lines.

Closed feature/integration branches are not reusable development lines. New work starts from current protected `main` under a fresh bounded branch unless an already-active workstream explicitly continues on its existing branch.

Exact branch truth must be reread from live Git before writes.

## 13. Worktree discipline

Before commands that can mutate source/ref state verify:

```text
pwd
git status -sb
git branch --show-current
git rev-parse HEAD
git worktree list
```

Do not switch a worktree to another branch merely because a new chat begins. If concurrent workstreams are real, separate worktrees are appropriate. If a workstream closes, reconcile its branch lifecycle intentionally before repurposing/removing the worktree.

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

After merge:

```text
protected-main readback
→ candidate-state wording reconciled to merged state
→ deleted-overlay references repaired
→ historical branch record remains non-authoritative
```

Protected `main` must not contain live/session handoff files as current navigation.

See `documentation-lifecycle-policy.md` and `../archive/README.md`.

## 15. Capability activation

Product/infrastructure capabilities are activated by real boundaries, not by branch names.

```text
PowerSync
→ real offline/multi-device implementation

R2
→ real ContentArtifact byte flow

Restate
→ first real Class-B durable workflow

pgBackRest LOCAL
→ already activated and directly rehearsed for LOCAL PostgreSQL recovery; integrated via PR #47

remote backup provider
→ real production deployment boundary + provider-specific direct proof

CodeQL / additional security controls
→ explicit repository-security workstream/gate when justified
```

Selected technology != implemented capability.

## 16. Current next boundaries

```text
ACCESS/AUTH
CLOSED / INTEGRATED VIA PR #52
→ do not resume feature/access-auth as an active workstream
→ future M6/M7 work is a new bounded scope from current protected main when explicitly activated

HOME
continue/resume frontend work only according to its own current bounded authority and live branch state
→ Access closure does not silently mutate or redefine that separate workstream

OBSERVABILITY
CLOSED / INTEGRATED VIA PR #58
→ source closure + true merge + source verification + PostgreSQL/ACL + runtime/Grafana smoke PASS
→ documentation lifecycle and protected-main CI/merge PASS
→ do not resume feature/platform-observability or either integration branch
→ future vertical metrics/tuning are new bounded scopes from current protected main when explicitly activated

POSTGRESQL RECOVERY
CLOSED / INTEGRATED VIA PR #47
→ CP08 application/Email reopen hardening integrated via PR #55
→ do not resume feature/postgres-recovery
→ permanent bootstrap/runner/runbook remain reusable from current protected main
→ remote provider remains TBD until production deployment creates the real boundary

DOCUMENTATION
apply lifecycle/current-truth cleanup before every integration
→ no live/session handoff on protected main
→ retain at most one useful non-authoritative branch-history record
→ perform a post-merge current-state/read-link reconciliation before declaring the integration fully closed
```

A genuine later database requirement uses a normal forward migration plus same-change database reconciliation. It does not reopen CP6, PostgreSQL Recovery or `feature/logical-postgresql`.

## 17. Persistent rules

```text
BRANCH != ENVIRONMENT
NEW CHAT != NEW BRANCH
ACTIVE WORKSTREAM != NEW WORKTREE BY DEFAULT
UNMERGED BRANCH TRUTH != PROTECTED-main TRUTH
MERGED BRANCH CANDIDATE STATE != CURRENT protected-main STATUS
CLOSED BRANCH != PERMANENT DEVELOPMENT LINE
SELECTED TECHNOLOGY != IMPLEMENTED CAPABILITY
DOCUMENTED CHECK != LIVE REQUIRED CHECK
TEMPORARY HANDOFF != DURABLE main DOCUMENTATION
```
