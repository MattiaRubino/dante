# Branching and Environments

- Status: **CURRENT**

## 1. Core rule

```text
BRANCH != ENVIRONMENT
```

Branches represent source-change scope. DANTE does not use permanent develop/uat/staging/production branches as environment state.

## 2. Integrated source truth

Protected `main` is the only integrated source truth.

```text
bounded branch
→ PR + applicable validation
→ protected main
```

Branch prefixes never authorize work outside the explicit gate.

## 3. Existing repository

Production continues in the current repository. **NEW REPOSITORY: NO.** Repository identity/name governance is separate from feature/architecture implementation.

## 4. Exact write gate

Before remote mutation state exact branch, PRE-SCOPE, CREATE/UPDATE/DELETE, purpose and explicit out-of-scope. Immediately before first write verify HEAD == PRE-SCOPE; if moved, stop/inspect/re-gate.

## 5. Protected-main integration

Before merge inspect exact paths/checks/branch movement and use expected-head protection where supported. After merge reread/compare main and verify branch lifecycle.

## 6. Environment vocabulary

Exactly:

```text
LOCAL
DEV
UAT
PROD
```

`TEST` may be an automated context, not a promotion environment. Temporary previews may exist. Frontend/mobile provider names map to these DANTE contexts.

## 7. Activation

```text
LOCAL   first production implementation
DEV     shared/remote integration when useful
UAT     real release candidates
PROD    production readiness
```

Remote resources are not created for appearance.

## 8. LOCAL

Backend: Linux canonical semantics, Windows through WSL2, one authoritative WSL-backed worktree, PyCharm WSL supported, backend direct in WSL, Docker Compose stateful infra, real PostgreSQL when materialized, synthetic data.

Frontend selected posture shares the authoritative checkout. WSL↔Windows Android/ADB/Metro is validated during materialization.

## 9. DEV

Accepted-main artifacts only; DEV-only state/credentials/secrets; synthetic non-production data; no PROD credentials/raw dumps. Frontend deployment profiles map explicitly to DEV.

## 10. UAT

Exact release candidate, migration/release rehearsal, E2E/provider compatibility, representative synthetic/sanitized data, applicable security/performance/recovery/PSV gates; signed/device validation for activated mobile targets.

## 11. PROD

Exact accepted candidate/artifact, isolated production state/identity/secrets, controlled releases/migrations, accepted recovery/observability/security posture; mobile store/update gates only for activated targets.

## 12. Isolation

```text
DEV state != UAT state != PROD state
DEV identity != UAT identity != PROD identity
DEV secrets != UAT secrets != PROD secrets
```

Backend compute/cloud provider remains deferred until its real boundary.

## 13. GitHub Environments

When deployment workflows activate, GitHub Environments such as `dev`, `uat`, `prod` govern credentials/protection/history; they are not the runtime environments themselves.

## 14. Artifact promotion

Server default: accepted main → build once → immutable artifact/digest → DEV → exact UAT → exact PROD.

Web supports an immutable SPA artifact promoted where platform permits with versioned environment-specific **public** runtime config.

Mobile binary/OTA semantics follow Expo/EAS runtime compatibility; native binary and OTA update are distinct artifact classes.

## 15. Required status checks

A future job name is not a required check. Require only real stable observed contexts whose failure genuinely must block merge.

## 16. One-developer posture

PR + automated gates remain real; no fake independent reviewer requirement; add CODEOWNERS/required reviewers only when real ownership exists.

## 17. Current Frontend Foundation continuation

```text
feature/frontend-foundation
DESIGN / ARCHITECTURE CLOSED / ACCEPTED / FINAL REVIEW PASS
PENDING MAIN INTEGRATION
```

PR creation and merge require explicit authorization. After protected-main integration, open a fresh materialization/direct-validation branch/gate.

Backend production scaffold remains a separate NOT STARTED workstream.
