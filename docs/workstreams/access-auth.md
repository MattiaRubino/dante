# DANTE — Access/Auth Full-Stack Workstream

- **Status:** **M1–M5 CLOSED / ACCEPTED / INTEGRATED VIA PR #52 / POST-MERGE CI PASS**
- **Original feature branch:** `feature/access-auth` — historical only
- **Former integration branch:** `integration/access-auth-main-20260904` — historical only
- **Protected-main integration merge:** `5f76ec54ad78542f137e8730e904f805d9e59e56`
- **Current Alembic head:** `20260904_17`

> Access/Auth M1–M5 is closed on protected `main`. No M6/M7 scope belongs to the completed integration workstream.

## 1. Closure state

```text
M1 Visual / UX                              CLOSED / INTEGRATED
M2 Auth architecture                        CLOSED / INTEGRATED
M3 Signin + AuthSession                     CLOSED / INTEGRATED
M4 Signup/recovery/reset/reauth             CLOSED / INTEGRATED
M5 Multi-authenticator Account              CLOSED / INTEGRATED
Google                                      REAL UAT PASS
Apple backend/grant/notifications           ENGINEERING PASS
Apple real registered-domain UAT            BOUNDED DEFERRED / NON-BLOCKING
Passkeys / Windows Hello                    REAL UAT PASS
Shared Email Platform                       CLOSED / INTEGRATED / OWNERSHIP VERIFIED
Real SES signup/recovery/reset notification PASS
CP07 whole LOCAL recovery rehearsal         PASS
post-merge Backend CI                       PASS
post-merge Frontend CI                      PASS
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

## 3. Current protected-main database

```text
PostgreSQL          18.6
Alembic             20260904_17
88 tables / 5 views / 16 routines
76 triggers / 172 indexes / 89 FKs / 270 CHECKs
```

Recovery `20260830_09` and Access/Auth/Email `20260904_16` remain distinct accepted histories below the no-DDL merge revision `20260904_17`.

The accepted CP07 rehearsal on implementation proof HEAD `81639c61478b476c995652d0060dde8f53aef089` re-proved this integrated head/topology during restore acceptance and earned `DATABASE LOCAL REOPEN = PASS`. Remote backup provider and production/cloud recovery remain outside the accepted scope.

## 4. Shared Email Platform

Email is shared DANTE infrastructure. Access/Auth owns security-message meaning/rendering; the platform owns durable delivery lifecycle and provider mechanics. Future consumers reuse this platform.

The shared-ownership refactor, replay hardening and migration `20260904_16` are integrated on protected `main`. Historical real SES UAT remains valid real-provider evidence for the accepted delivery behavior.

## 5. Protected-main integration evidence

Implementation proof:

```text
81639c61478b476c995652d0060dde8f53aef089
```

Final documentation/evidence candidate:

```text
6cee5506d404d0684b0679aca54c03f0ca433c72
```

Protected-main merge:

```text
PR #52
merge commit  5f76ec54ad78542f137e8730e904f805d9e59e56
old main      fe87d3c8a71f0c56d9acf5e8acbcdb274b18f282
merge tree    b610ece4fbfa0049749bb8454345a96a0385e6e5
```

The merge tree is identical to the final candidate tree. Push CI on the exact merge commit passed Backend Quality, real PostgreSQL acceptance, Backend CI Gate, Frontend Quality, Web E2E, Mobile Bundle and Frontend CI Gate.

Durable detailed evidence: `access-auth-integration-acceptance-2026-09-04.md`.

## 6. Current work

This workstream has no remaining integration task. Protected `main` is the current authority.

Next bounded integration:

```text
enriched protected main
→ feature/platform-observability
→ observability release/integration rechecks
→ protected-main Observability PR
```

The former Access/Auth feature/integration branches are historical Git evidence, not continuation authorities.

## 7. Deliberately later

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

No rebase, history rewrite, force push or direct protected-main write is authorized by this closure.
