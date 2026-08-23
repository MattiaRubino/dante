# Branching and Environments

- Status: **CURRENT**

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
-> PR + applicable validation
-> protected main
```

Short-lived prefixes may include `feature/`, `fix/`, `chore/`, `docs/`, `prototype/`. Prefix never authorizes work outside the explicit gate.

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

## 4. Protected-main integration

Before merge:

- inspect exact changed paths;
- inspect applicable real checks/statuses;
- require branch current with `main` where the ruleset requires it;
- verify no unexpected branch movement;
- verify accepted-risk/waiver state is still valid;
- verify review threads are resolved;
- preserve the repository's accepted merge/history policy.

After merge:

- reread/compare `main`;
- verify exact integration result and parentage;
- verify push-main CI where applicable;
- verify branch lifecycle/autodelete only when intentionally part of closure.

## 5. Environment vocabulary

Exactly:

```text
LOCAL
DEV
UAT
PROD
```

`TEST` may exist as automated execution context but is not a promotion environment. Preview environments may exist when useful.

Frontend/mobile provider profile/channel names map to these DANTE contexts rather than creating a second taxonomy.

## 6. Activation

```text
LOCAL   individual development / direct implementation
DEV     first shared remote integration
UAT     real release-candidate acceptance
PROD    accepted production release
```

Remote resources are not created for appearance.

## 7. LOCAL posture

Backend and frontend use one authoritative WSL-backed source tree/worktree posture on Windows systems. Windows may host JetBrains, browser and Android emulator.

```text
NO divergent Windows + WSL source clones
NO cross-OS shared node_modules
```

Backend process normally runs directly in WSL for reload/debug; Docker Compose owns LOCAL stateful dependencies. Frontend Metro/Vite/pnpm/Turbo run from the authoritative Linux/WSL tree; Windows browser/emulator are native bridge consumers.

## 8. DEV / UAT / PROD isolation

Target:

```text
DEV state     != UAT state     != PROD state
DEV identity  != UAT identity  != PROD identity
DEV secrets   != UAT secrets   != PROD secrets
```

Raw PROD -> DEV is forbidden by default. UAT uses exact release candidates and representative synthetic/sanitized data. PROD uses isolated real state/identity/secrets and accepted recovery/security/observability posture.

## 9. Artifact promotion

Server default:

```text
accepted main
-> build once
-> immutable artifact/digest
-> DEV
-> exact UAT candidate
-> exact PROD candidate
```

Web supports immutable SPA promotion with environment-specific public runtime config when that boundary activates. Mobile follows Expo/EAS native-binary/update compatibility semantics rather than pretending native binaries and OTA JS are the same artifact class.

## 10. Required status checks

A documented future job name is not a required check.

Promotion protocol:

```text
real workflow/context
+ real PR green
+ controlled deliberate red proving intended failure semantics
+ recovery green
-> separate explicit ruleset mutation
```

Current protected-main required checks:

```text
Backend CI Gate
Dependency Review
```

`Frontend CI Gate` has emitted and passed on PR #28 but is not required yet. Its deliberate-red/recovery-green calibration is the next repository-safety proof before any promotion decision.

## 11. One-developer posture

While one regular maintainer exists:

- PR + automated gates remain real;
- required approvals remain 0;
- review-thread resolution remains required;
- do not create fake independent-review ceremony;
- add CODEOWNERS/required reviewers only when real distributed ownership exists.

## 12. Current branch/workstream truth

```text
feature/backend-scaffold
CLOSED / integrated via PR #24
historical evidence branch only

feature/frontend-materialization
CLOSED / PASS — FM-00..FM-07
immutable evidence source for integration

chore/frontend-materialization-integration
ACTIVE / PR #28
created from current main
carries closed frontend history through a real merge parent
current work = reconciliation + CI gate calibration + final integration review
```

The closed frontend materialization branch is not reused as the operational integration branch.

## 13. Future capability activation

Product/infrastructure capabilities are activated by real boundary, not branch name. The durable trigger register lives in `../workstreams/frontend-materialization-integration.md` and covers first vertical, UI/design system, form, remote API, offline operation, deployment, Mobile release, security maturation, pre-PROD maturity and scale-triggered infrastructure.

## 14. Current next sequence

```text
PR #28 reconciled candidate
-> CI green
-> Frontend CI Gate deliberate red
-> recovery green
-> optional separate required-check promotion
-> final protected-main merge authorization
```

Backend Concrete Logical -> PostgreSQL remains a separate bounded workstream; product vertical work does not inherit authorization from the integration branch.