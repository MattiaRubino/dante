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

Short-lived prefixes may include `feature/`, `fix/`, `chore/`, `docs/`, `prototype/`. Prefix never authorizes work outside the explicit gate.

## 3. Existing repository

Production implementation continues in the current repository.

```text
NEW REPOSITORY
NO
```

Repository identity/name governance is separate from feature/architecture implementation and does not create a second production repository.

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

Immediately before first write verify branch HEAD still equals PRE-SCOPE. If moved: stop, inspect, re-gate.

## 5. Protected-main integration

Durable work integrates through PR.

Before merge:

- inspect exact changed paths;
- inspect applicable real checks/statuses;
- verify no unexpected branch movement;
- merge with expected head when tooling supports it;
- preserve accepted repository merge/history policy.

After merge:

- reread/compare `main`;
- verify exact integration result;
- verify branch lifecycle/autodelete when relevant.

## 6. Environment vocabulary

Exactly:

```text
LOCAL
DEV
UAT
PROD
```

`TEST` may exist as automated execution context but is not a promotion environment. Temporary preview environments may exist when useful.

Frontend/mobile provider profile/channel names map to these DANTE contexts rather than creating a second taxonomy.

## 7. Activation

```text
LOCAL   first production implementation
DEV     when shared/remote integration is useful
UAT     when real release candidates exist
PROD    production readiness
```

Environment definitions are fixed; remote resources are not created merely for appearance.

## 8. LOCAL

LOCAL is the individual developer context.

Backend baseline:

- Linux canonical semantics;
- Windows supported through WSL2;
- one authoritative WSL-backed repository/worktree;
- PyCharm WSL supported;
- backend direct in WSL for reload/debug;
- Docker Compose for stateful infra;
- real PostgreSQL 18.4 with accepted extension envelope when materialized;
- synthetic/local credentials/data.

Frontend selected posture shares the same authoritative checkout. WSL↔Windows Android/ADB/Metro details are directly validated during materialization.

LOCAL state is disposable/rebuildable where it is not intentionally retained.

## 9. DEV

First shared remote integration environment.

- accepted-main artifacts only;
- DEV-only state/credentials/secrets;
- synthetic/shared non-production data;
- remote config/network/provider integration;
- no PROD credentials;
- no raw PROD dump as convenience.

Frontend Web/mobile technical deployment profiles/channels must map explicitly to DANTE DEV semantics.

## 10. UAT

Production-like release-candidate/acceptance environment.

- exact candidate identity;
- migration/release rehearsal;
- E2E/provider compatibility;
- representative synthetic or explicitly sanitized/minimized data;
- applicable security/performance/recovery/PSV gates;
- activated mobile targets use signed/device validation appropriate to that platform.

## 11. PROD

Real released service/user data.

- exact accepted candidate/artifact identity;
- isolated production state/identity/secrets;
- controlled serialized migrations/releases where required;
- accepted recovery/observability/security posture;
- emergency infra changes reconciled into versioned desired state;
- mobile store/update gates apply only to activated release targets.

## 12. Environment isolation

Target:

```text
DEV state != UAT state != PROD state
DEV identity != UAT identity != PROD identity
DEV secrets != UAT secrets != PROD secrets
```

When provider is selected, prefer strong account/project/subscription-equivalent boundaries where operationally reasonable.

Backend compute/cloud provider remains intentionally deferred until its real remote boundary.

## 13. GitHub Environments

When remote deployment workflows activate, use GitHub Environments such as:

```text
dev
uat
prod
```

They govern deployment credentials/protection/history as supported. They are not runtime/cloud environments themselves.

## 14. Artifact promotion

Server default:

```text
accepted main
→ build once
→ immutable artifact/digest
→ DEV
→ exact UAT candidate
→ exact PROD candidate
```

Do not rebuild “the same release” separately without a platform-specific reason and explicit traceability.

Frontend Web posture supports an immutable SPA artifact promoted across environments where the delivery platform permits, with versioned environment-specific **public** runtime configuration.

Mobile artifact/update semantics follow Expo/EAS runtime-compatibility rules rather than pretending a native binary and OTA JS update are the same artifact class.

## 15. Required status checks

A documented future job name is not a required check.

Only after a real check exists, emits a stable context, has been observed on relevant PRs and genuinely must block merge may it become required on `main`.

## 16. One-developer posture

While there is one active developer:

- PR + automated gates remain real;
- do not create fake independent-review requirements;
- add CODEOWNERS/required reviewers only when real ownership exists.

## 17. Current branch/workstream continuation

Current frontend design work is on `feature/frontend-foundation`.

```text
Passo 1 technology design     COMPLETE
Passo 2 architecture design   COMPLETE
Passo 3 clean review          ACTIVE
```

If Passo 3 passes, record closure and prepare protected-main integration. PR/merge still require explicit authorization.

Only after frontend Foundation integration should a fresh branch/gate materialize production Web/Mobile/workspace artifacts and execute direct validations.

Backend production scaffold remains a separate not-started workstream with its own future gate.
