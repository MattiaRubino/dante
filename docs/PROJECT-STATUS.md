# DANTE — Project Status

- **Status:** CURRENT TRUTH FOR `feature/access-auth`
- **Last reconciled:** 2026-09-02
- **Protected `main`:** integrated source authority; Access/Auth remains branch-local until explicit merge gate
- **Active product vertical:** Access/Auth
- **Current macro-phase:** M5 — Multi-authenticator Account Layer — **ACTIVE / FINAL EXTERNAL ACCEPTANCE OPEN**
- **Reviewed product checkpoint:** `ab2716abe40de658d99d1908ba31c5d5744e3c57`
- **Current branch checkpoint before docs reconciliation:** `9c0587af5891249d8a6e6b6a5d6e3af6934c6943`
- **Accepted Alembic head:** `20260831_13`
- **Current review evidence:** `workstreams/access-auth-m5-review-2026-09-02.md`

## 1. Current state

```text
Product / North Star                       CURRENT
Domain / Logical / Physical                CLOSED
Engineering + Frontend + Backend CP1–CP6  CLOSED / ACCEPTED
Access pre-backend Web materialization     CLOSED / ACCEPTED

M1 Visual / UX Freeze                      CLOSED / ACCEPTED
M2 Auth Architecture Freeze                CLOSED / ACCEPTED
M3 Email/Password + AuthSession            CLOSED / ACCEPTED
M4 Lifecycle / Recovery / Reauth           CLOSED / ACCEPTED

M5.1 architecture/external authority       COMPLETE
M5.2 persistence/API design                COMPLETE
M5-A persistence                           COMPLETE / POSTGRESQL PROVEN
M5-B provider/crypto/WebAuthn infra         COMPLETE / ENGINEERING PASS
M5-C Google backend                        COMPLETE / ENGINEERING PASS
M5-D Apple backend/grants/notifications    COMPLETE / ENGINEERING PASS
GROUP 1 M5-E+G lifecycle/passwordless      COMPLETE / ENGINEERING PASS
GROUP 2 M5-F passkeys                      COMPLETE / ENGINEERING PASS
GROUP 3 M5-H+I FastAPI/OpenAPI/client      COMPLETE / ENGINEERING PASS
GROUP 4 Access Web engineering QA          PASS
GROUP 4 local password/passkey UAT          PASS
GROUP 4 real Google UAT                    PASS
GROUP 4 real Internet email delivery       OPEN
GROUP 4 real Apple registered-domain UAT    DEFERRED / OPEN

Whole M5                                    ACTIVE / NOT FORMALLY CLOSED
M6 Native Mobile                           FUTURE / OPTIONAL / ONLY IF RE-GATED
M7 Hardening/Observability/Handoff         PLANNED
```

## 2. Current evidence

Automated product-code gate at `ab2716...`:

```text
Prettier                     PASS
TypeScript                   PASS
ESLint                       PASS
architecture                 PASS
Web unit/component           68 / 68 PASS
Auth Playwright HTTPS        60 / 60 PASS
Chromium/Firefox/WebKit      PASS through canonical suite
```

Manual UAT directly proved password/session rotation, Windows Hello passkey registration/signin/reauth, rename persistence, passwordless state, authenticator anti-lockout, password restore and direct PostgreSQL coherence.

Real Google UAT directly proved official GIS interaction, real Google ID-token verification, third-party-mailbox verification policy, passwordless Account creation, ExternalIdentity `issuer + subject` authority and canonical AuthSession creation. Direct DB inspection showed no PasswordCredential for the Google-created Account.

Detailed evidence and repaired UAT defects are recorded in `workstreams/access-auth-m5-review-2026-09-02.md`.

## 3. Current database truth

```text
PostgreSQL          18.6
Alembic             20260831_13
tables              83
views                5
routines             15
triggers             75
physical indexes     156
foreign keys         85
CHECK constraints    233
standalone Dictionary entries 103
```

Revision `20260831_13` is the bounded authenticator-lifecycle runtime ACL follow-up; it does not change the M5-A topology counts.

## 4. Current Auth constitution

```text
Person != Account != Principal != Actor
AuthSession != DANTE Session
EmailIdentity != Account
PasswordCredential optional
Principal runtime-derived
provider identity = issuer + subject
provider email != Account/link authority
provider auth != provider-data authorization
provider token/assertion != DANTE AuthSession
passwordless Account valid
PasskeyCredential != Account
WebAuthn user_handle = opaque Account binding
method != factor != assurance
reauthentication != signin
frontend/provider/browser completion != backend-authoritative success
```

## 5. Open items before M5 closure

```text
email-delivery architecture/research
→ decide internal responsibility vs external delivery service boundary
→ deliverability/DNS/bounce/complaint/retry/observability/privacy design
→ qualify provider-neutral implementation
→ real signup/recovery delivery UAT

Apple
→ registered HTTPS domain/provider configuration
→ real Apple account UAT when available
→ Private Email Relay sender/domain proof
```

The opt-in real-SMTP local-UAT support introduced at `9c0587...` is **not** a provider selection and has not yet completed its targeted tooling/real-delivery qualification.

## 6. M7 maturity work

Compared with mature consumer/work tools, the main post-M5 account-security maturity work is already compatible with the current model:

```text
session/device inventory
revoke one / revoke all others / log out everywhere
new-login/security-event notifications
“this wasn't me” response
production observability/alerting
final authenticated Home handoff
security-page component hardening
```

No Auth redesign is required to add these surfaces.

## 7. Documentation authority

Current operational truth:

1. this file;
2. `ROADMAP.md`;
3. `workstreams/access-auth.md`;
4. `workstreams/access-auth-m5-review-2026-09-02.md`;
5. current executable code/tests/migrations.

Architecture/security/API contracts remain durable semantic authority. Old phase-progress statements embedded in those contracts are historical milestone snapshots and do not override the current operational state.

The dated `workstreams/access-auth-m5-live-handoff-2026-08-29.md` is superseded and historical.