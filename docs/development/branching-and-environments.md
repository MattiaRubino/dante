> **CURRENT MAIN + CP6 RECONCILIATION — 2026-08-26**
> Protected `main` anchor imported by this alignment is `87fe668c2ade78b17e0326d635e4d7a67920ae8a`. Its post-merge truth is preserved: frontend materialization/integration is **CLOSED / INTEGRATED via PR #28**, deterministic Frontend CI compatibility repair is integrated via PR #37, and the clean Home B2 v27 React handoff is integrated via PR #36. The main-only frontend contracts, fixtures, tokens and pre-production guard remain byte-identical to that protected-main anchor.
> Backend CP6 is independently **CLOSED / CONCRETE POSTGRESQL DATABASE PASS**. Accepted implementation HEAD is `22bbc078391d52c43665474bf465593d6225106e`; closure-documentation branch anchor before this alignment is `8c33c897ff57cfff9130fe00db1854470aa06bb5`; persistent LOCAL PostgreSQL 18.6 is at Alembic `20260826_08`; verified topology remains `68 tables / 5 views / 14 routines / 75 triggers / 95 indexes / 68 FKs / 120 CHECKs`.
> This overlay supersedes only contradictory **current status, routing, branch and next-step prose** later in this file. Historical evidence, accepted architecture, frontend product contracts, failed-run/repair evidence and phase-time records remain historical truth and are not rewritten. The aligned feature branch is only a candidate for protected-main integration: **no final merge into `main` is authorized by this overlay**. Protected-main integration still requires the normal PR, current-head required checks and a separate final merge gate.

> **CURRENT INTEGRATION RECONCILIATION — 2026-08-24**  
> PR #28 is **MERGED** into protected `main` at `f1aacb0724088e0b4b086008a5219c2fba5ce0cf`. `feature/frontend-materialization` remains CLOSED/PASS historical evidence; `chore/frontend-materialization-integration` is no longer an active/pending integration boundary. Any later section below that still says PR #28 READY or awaiting merge is preserved pre-merge history and is superseded on current branch status only. Backend `feature/logical-postgresql` has incorporated current `main` and remains the active CP6 branch.  

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
- verify push-main CI where the available interface permits direct readback;
- record readback limitations instead of inventing PASS;
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

For `Frontend CI Gate`, that protocol is complete: real green, controlled deliberate red, mandatory failure propagation, exact restore and recovery green were directly observed. The repository owner confirmed applying the promotion to protected `main`; direct ruleset API readback is unavailable through the current connector, so the administrative setting remains **OWNER-CONFIRMED APPLIED / DIRECT API READBACK UNAVAILABLE**.

The canonical repository ruleset definition contains:

```text
Backend CI Gate
Dependency Review
Frontend CI Gate
```

with strict branch-up-to-date enforcement preserved.

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
historical evidence source

chore/frontend-materialization-integration
CLOSED / integrated via PR #28
final PR head        a6607ceabd35f874dc9e5f63fe8f57f71a92bf80
protected-main merge f1aacb0724088e0b4b086008a5219c2fba5ce0cf
branch observed absent after merge
manual deletion performed during merge operation: NO
```

The closed frontend materialization and integration branches are not reused for new product/security/backend work. New work starts from current `main` under a fresh bounded branch and gate.

## 13. Future capability activation

Product/infrastructure capabilities are activated by real boundary, not branch name. The durable trigger register lives in `../workstreams/frontend-materialization-integration.md` and covers first vertical, UI/design system, form, remote API, offline operation, deployment, Mobile release, security maturation, pre-PROD maturity and scale-triggered infrastructure.

## 14. Current next sequence

```text
REPOSITORY SECURITY NEXT CANDIDATE
CodeQL default setup evaluation
-> fresh explicit branch/write gate

BACKEND NEXT
Concrete Logical -> PostgreSQL
-> fresh bounded branch/workstream/gate

PRODUCT NEXT
first real vertical slice
-> fresh bounded branch/workstream/gate
```

Frontend PR #28 final head passed its applicable hosted CI before merge. The protected-main merge has the expected parentage and zero file delta from that head. Push-main CI on the merge SHA remains **DIRECT READBACK UNAVAILABLE** through the current connector and is not inferred PASS.
