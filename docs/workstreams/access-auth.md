# DANTE — Access/Auth Full-Stack Workstream

- **Status:** **M1–M5 CLOSED / ACCEPTED — COMBINED INTEGRATION QA ACTIVE**
- **Original feature branch:** `feature/access-auth`
- **Current integration candidate:** `integration/access-auth-main-20260904`
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
Shared Email Platform                      CLOSED / ACCEPTED
Real SES signup/recovery/reset notification PASS
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

## 4. Shared Email Platform

Email is shared DANTE infrastructure. Access/Auth owns security-message meaning/rendering; the platform owns durable delivery lifecycle and provider mechanics. Future consumers reuse this platform.

## 5. Current work

Only combined integration acceptance:

```text
Alembic DAG / migration paths
Dictionary + SQLAlchemy + live catalog
Recovery regression
Auth regression
Email regression
backend/Web/generated-client/build QA
Recovery whole-rehearsal recheck
current documentation coherence
```

## 6. Integration sequence

```text
combined QA
→ protected-main PR
→ enriched main into feature/platform-observability
→ observability release rechecks
→ observability PR to protected main
→ future bounded branches
```

No rebase, history rewrite, force push or direct protected-main write.

## 7. Deliberately later

```text
M6 Native Mobile
session/device inventory
remote session management
security event center / "this wasn't me"
future Access polish
Apple real UAT until prerequisites exist
production email sender deployment
```
