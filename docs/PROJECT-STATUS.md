# DANTE — Project Status

- **Status:** CURRENT TRUTH FOR `feature/access-auth`
- **Last reconciled:** 2026-09-03
- **Protected `main`:** integrated source authority; Access/Auth remains branch-local until explicit merge gate
- **Active product workstream:** Access/Auth
- **Current macro-phase:** M5 — Multi-authenticator Account Layer — **ACTIVE / FINAL CLOSURE RECONCILIATION**
- **Current Access/Auth Alembic head:** `20260903_15`
- **Current Email Platform authority:** `architecture/email-platform.md`
- **Email Platform decision:** `decisions/ADR-012-email-delivery-platform.md`
- **Real-provider acceptance evidence:** `development/email-platform-acceptance-2026-09-03.md`

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

Email Platform architecture                ACCEPTED / SHARED DANTE SUBSYSTEM
Email Platform persistence/worker           ACCEPTED
Amazon SES API v2 adapter                   ACCEPTED
Email Platform automated acceptance         PASS
real SES signup UAT                         PASS
real SES recovery UAT                       PASS
real reset-notification UAT                 PASS
Email Platform engineering work             CLOSED

real Apple registered-domain UAT            DEFERRED / OPEN
whole M5                                    ACTIVE / FINAL CLOSURE RECONCILIATION
M6 Native Mobile                            FUTURE / OPTIONAL / ONLY IF RE-GATED
M7 Hardening/Observability/Handoff          PLANNED
```

## 2. Current evidence

Automated product-code evidence already established the Access/Auth frontend/backend contract, browser suite, local password/session flows, passkeys/Windows Hello and real Google provider flow.

Email Platform closure added the following observed evidence:

```text
uv lock --check                               PASS
Ruff format/lint                              PASS
targeted mypy src                             PASS
backend non-PostgreSQL regression             234 PASS
focused PostgreSQL Email/Auth acceptance      10 PASS
Email Platform unit/SES semantics             9 / 9 PASS
uv build                                      PASS
```

Real-provider UAT directly proved:

```text
dedicated non-root IAM user/profile
SES eu-west-3 preflight SUCCESS
DANTE signup → SES → real mailbox
received OTP → Account creation
DANTE password recovery → SES → real mailbox
recovery URL → password reset
no auto-login after reset
previous AuthSession revoked
password-reset notification → SES → real mailbox
```

Runtime emitted three SES `provider_accepted` outcomes, each on attempt 1.

Direct PostgreSQL UAT inspection observed all three corresponding intents as `provider_accepted`, each with provider MessageId present and sensitive payload material wiped.

Exact evidence and one explicit manual non-claim are recorded in `development/email-platform-acceptance-2026-09-03.md`.

## 3. Current database truth

```text
PostgreSQL          18.6
Alembic             20260903_15
tables              87
views                5
routines             15
triggers             75
physical indexes     170
foreign keys         88
CHECK constraints    267
```

The Email Platform adds four bounded technical persistence structures:

```text
dante.email_delivery_intent
dante.email_delivery_attempt
dante.email_provider_event
dante.email_recipient_suppression
```

These are delivery-control structures, not Domain identity owners and not DANTE MaterialState.

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

No Email Platform work changes these invariants.

## 5. Email Platform current truth

The shared platform is now closed as engineering infrastructure:

```text
DANTE owns email intent/lifecycle/state
PostgreSQL transactional outbox is materialized
feature mutation + EmailIntent commit atomically
provider I/O happens after commit
Amazon SES API v2 is the accepted primary external adapter
SMTP remains local/CI/generic compatibility adapter
provider accepted != recipient delivery
network ambiguity != definitely unsent
no blind retry after ambiguous outcome
short-lived sensitive payload is AEAD-protected and terminally wiped
provider feedback/suppression model is materialized and automated-test accepted
privacy-minimized observability is materialized
real signup/recovery/reset-notification SES UAT PASS
```

Access/Auth is the first consumer, not the owner of the Email Platform.

The final real UAT used `eu-west-3`/Paris. SES region is deployment configuration and no longer hard-coded in current architecture/status as “Milan preferred”.

## 6. Production email deployment — separate open gate

Email Platform closure does **not** equal production mail deployment acceptance.

Still required before production sender acceptance:

```text
DANTE-controlled sender domain/subdomain
SPF
DKIM
DMARC
production workload identity / IAM role
SES production account/quota/reputation posture
live provider feedback/event routing
production alerting/SLOs
traffic/reputation segmentation
privacy/legal/subprocessor deployment review where required
Apple Private Email Relay sender-domain compatibility where applicable
```

These tasks may configure/harden the accepted platform; they do not reopen its architecture absent defect evidence.

## 7. Real UAT precision

Observed live recovery behavior:

```text
recovery email received
recovery URL consumed successfully
password reset succeeded
prior session revoked
no auto-login
reset notification received
```

The exact same consumed recovery URL was **not manually opened a second time** in the final live run because the message had already been removed before that check. Do not report manual replay rejection as observed evidence.

## 8. Open items before whole-M5 closure

The Email Platform is no longer an M5 blocker.

Remaining closure work is bounded to:

```text
final M5 status/documentation reconciliation
Apple real registered-domain UAT disposition
  → execute when prerequisites exist, or
  → record an explicit bounded deferral accepted for M5 closure
final branch/integration gate when authorized
```

M7 continues to own later maturity work such as session/device inventory, remote revoke, new-login/security alerts, production operations/observability and final authenticated Home handoff.

## 9. Documentation authority

Current operational truth:

1. this file;
2. `ROADMAP.md`;
3. `workstreams/access-auth.md`;
4. `architecture/email-platform.md` for shared Email Platform architecture;
5. `development/email-platform-acceptance-2026-09-03.md` for observed live SES evidence;
6. `architecture/access-auth-email-delivery.md` for Access/Auth consumer integration;
7. executable code/tests/migrations/live schema.

Historical M5 handoffs and phase-time “NEXT/OPEN/not materialized” statements do not override these current authorities.
