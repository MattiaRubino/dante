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
        ↓
PR + applicable validation
        ↓
protected main
```

Short-lived branch prefixes may reflect purpose, for example:

```text
feature/
fix/
chore/
docs/
prototype/
```

The prefix does not authorize work outside the explicit write gate.

## 3. Existing repository

Production implementation continues in the current repository.

```text
NEW REPOSITORY
NO
```

The repository may be renamed from historical `lifeos` to `dante` in a separate explicit governance operation. A rename preserves Git history and is preferred to creating a new production repo.

## 4. Exact write gate

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

Immediately before first write verify branch HEAD still equals PRE-SCOPE.

If it moved: stop, inspect and re-gate.

## 5. Protected-main integration

Durable work integrates through PR.

Before merge:

- inspect exact changed paths;
- inspect applicable real checks/statuses;
- verify no unexpected branch movement;
- merge with expected head when tooling supports it;
- preserve workstream history with the repository's accepted merge strategy.

After merge:

- reread/compare `main`;
- verify exact integration result;
- verify branch lifecycle/autodelete when relevant.

## 6. Environment vocabulary

DANTE lifecycle contexts:

```text
LOCAL
DEV
UAT
PROD
```

`TEST` may exist as an automated execution context but is not a promotion environment.

Optional preview environments may exist temporarily when useful.

## 7. Activation

```text
LOCAL
first production implementation

DEV
when shared/remote integration becomes useful

UAT
when real release candidates exist

PROD
at production-readiness
```

Environment definitions are fixed now; remote resources are not created until useful.

## 8. LOCAL

LOCAL is the individual developer context.

Backend baseline:

- Linux canonical semantics;
- Windows supported through WSL2;
- backend repo/worktree in WSL filesystem;
- PyCharm WSL interpreter supported;
- backend process direct in WSL for reload/debug;
- Docker Compose for stateful infra;
- real PostgreSQL 18.4 with full selected extension envelope enabled;
- synthetic/local credentials and data.

LOCAL is disposable/rebuildable where state is not intentionally retained.

## 9. DEV

First shared remote integration environment.

- accepted-main artifact only;
- DEV-only state/credentials/secrets;
- synthetic/shared non-production data;
- remote config/network/provider integration;
- no PROD credentials;
- no raw PROD dump as convenience.

## 10. UAT

Production-like release-candidate/acceptance environment.

- exact candidate identity;
- migration/release rehearsal;
- E2E/provider compatibility;
- representative synthetic or explicitly sanitized/minimized data;
- applicable security/performance/recovery/PSV gates.

## 11. PROD

Real released service/user data.

- exact accepted candidate artifact;
- isolated production state/identity/secrets;
- controlled serialized migrations/releases where required;
- accepted recovery/observability/security posture;
- manual emergency infra changes reconciled into versioned desired state.

## 12. Environment isolation

Target:

```text
DEV state != UAT state != PROD state
DEV identity != UAT identity != PROD identity
DEV secrets != UAT secrets != PROD secrets
```

When provider is selected, prefer its strong account/project/subscription-equivalent security boundary where operationally reasonable.

Cloud provider is intentionally deferred.

## 13. GitHub Environments

When remote deployment workflows activate, use GitHub Environments:

```text
dev
uat
prod
```

They control deployment workflow/credentials/protection/history as supported. They are not the runtime/cloud environment themselves.

## 14. Artifact promotion

Future server default:

```text
accepted main
→ build once
→ immutable artifact/digest
→ DEV
→ exact UAT candidate
→ exact PROD candidate
```

Do not rebuild “the same release” separately without a platform-specific reason and explicit traceability.

Frontend/mobile artifact semantics are deferred to frontend workstream.

## 15. Required status checks

A documented future job name is not a required check.

Only after the real check exists, emits a stable context, has been observed on relevant PRs and genuinely must block merge may it become required on `main`.

## 16. One-developer posture

While there is one active developer:

- PR + automated gates remain real;
- do not create impossible/fake independent-review requirements;
- add required reviewers/CODEOWNERS only when real independent ownership exists.

## 17. Next branch after Foundation

First small scope: repository rename decision/action `lifeos → dante`, or explicit defer.

Then create a dedicated production-scaffold branch from current `main` with an exact path gate for `apps/backend` and required local infrastructure/tooling only.
