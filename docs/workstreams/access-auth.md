# DANTE — Access/Auth Full-Stack Workstream

- **Status:** **M1–M5 CLOSED / ACCEPTED — COMBINED INTEGRATION QA PASS / READY FOR PROTECTED-MAIN MERGE**
- **Original feature branch:** `feature/access-auth`
- **Current integration candidate:** `integration/access-auth-main-20260904`
- **Accepted candidate proof HEAD:** `81639c61478b476c995652d0060dde8f53aef089`
- **Candidate Alembic head:** `20260904_17`
- **Protected-main Alembic head:** `20260830_09`

> Access/Auth feature development remains frozen until this foundation returns to protected main. No M6/M7 scope belongs in the integration candidate.

## 1. Closure state

```text
M1 Visual / UX                             CLOSED / ACCEPTED
M2 Auth architecture                       CLOSED / ACCEPTED
M3 Signin + AuthSession                    CLOSED / ACCEPTED
M4 Signup/recovery/reset/reauth            CLOSED / ACCEPTED
M5 Multi-authenticator Account             CLOSED / ACCEPTED
Google                                     REAL UAT PASS
Apple backend/grant/notifications          ENGINEERING PASS
Apple real registered-domain UAT           BOUNDED DEFERRED / NON-BLOCKING
Passkeys / Windows Hello                   REAL UAT PASS
Shared Email Platform                      CLOSED / ACCEPTED / OWNERSHIP VERIFIED
Real SES signup/recovery/reset notification PASS
Combined candidate CI                      PASS
CP07 whole LOCAL recovery rehearsal        PASS
```

## 2. Frozen constitution

```text
Person != Account != Principal != Actor
AuthSession != DANTE Session
EmailIdentity != Account
PasswordCredential optional
provider identity = issuer + subject
provider email != Account/link authority
passwordless Account valid
PasskeyCredential != Account
WebAuthn user_handle = opaque Account binding
reauthentication != signin
```

## 3. Current database candidate

```text
PostgreSQL          18.6
Alembic             20260904_17
88 tables / 5 views / 16 routines
76 triggers / 172 indexes / 89 FKs / 270 CHECKs
```

Recovery `20260830_09` and Access/Auth/Email `20260904_16` remain distinct accepted histories below the no-DDL merge revision `20260904_17`.

The accepted CP07 rehearsal on exact proof HEAD `81639c61478b476c995652d0060dde8f53aef089` re-proved this integrated head/topology during restore acceptance and earned `DATABASE LOCAL REOPEN = PASS`. Remote backup provider and production/cloud recovery remain outside the accepted scope.

## 4. Shared Email Platform

Email is shared DANTE infrastructure. Access/Auth owns security-message meaning/rendering; the platform owns durable delivery lifecycle and provider mechanics. Future consumers reuse this platform.

The shared-ownership refactor, replay hardening and migration `20260904_16` have passed the candidate static/unit/PostgreSQL gate and exact-HEAD CI. Historical real SES UAT remains valid real-provider evidence for the accepted delivery behavior.

## 5. Current work

Feature implementation and combined integration acceptance are complete for the declared branch scope. Remaining work is integration procedure only:

```text
final current-document reconciliation
→ fresh CI on the documentation-only acceptance commit
→ recheck protected main ref / candidate ancestry
→ mark PR #52 ready
→ merge through protected-main PR flow
→ verify resulting main tree + CI + Alembic/current documentation
→ retire integration branch only after post-merge acceptance
```

If `main` advances before merge, stop and integrate that delta forward before proceeding. Re-run every affected gate, including CP07 if the database/recovery contract changes.

## 6. Integration evidence

Durable acceptance record:

`access-auth-integration-acceptance-2026-09-04.md`

It records the exact candidate proof HEAD, GitHub Actions evidence, combined database contract and CP07 LOCAL recovery result without upgrading LOCAL evidence into production/cloud claims.

## 7. Integration sequence

```text
accepted candidate
→ protected-main PR #52
→ post-merge main verification/reconciliation
→ enriched main into feature/platform-observability
→ observability release rechecks
→ observability PR to protected main
→ future bounded branches
```

No rebase, history rewrite, force push or direct protected-main write.

## 8. Deliberately later

```text
M6 Native Mobile
session/device inventory
remote session management
security event center / "this wasn't me"
future Access polish
Apple real UAT until prerequisites exist
production email sender deployment
remote/cloud backup-provider deployment and production recovery acceptance
```
