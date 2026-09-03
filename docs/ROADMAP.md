# DANTE Roadmap

- **Status:** CURRENT FOR `feature/access-auth`
- **Last reconciled:** 2026-09-03
- **Active workstream:** Access/Auth
- **Current macro-phase:** M5 — Multi-authenticator Account Layer — **FINAL CLOSURE RECONCILIATION**
- **Current Access/Auth Alembic head:** `20260903_15`
- **Email Platform acceptance evidence:** `development/email-platform-acceptance-2026-09-03.md`

## 1. Current sequence

```text
Product / North Star
        CURRENT
          ↓
Domain / Logical / Physical
        CLOSED
          ↓
Engineering + Frontend + Backend CP1–CP6
        CLOSED / ACCEPTED
          ↓
Access M1–M4
        CLOSED / ACCEPTED
          ↓
M5.1 / M5.2 / M5-A–D
        COMPLETE
          ↓
GROUP 1 / GROUP 2 / GROUP 3
        COMPLETE / ENGINEERING PASS
          ↓
GROUP 4 PRODUCT ENGINEERING
        AUTOMATED QA PASS
          ↓
LOCAL PASSWORD/PASSKEY UAT
        PASS
          ↓
REAL GOOGLE UAT
        PASS
          ↓
SHARED EMAIL PLATFORM
        ARCHITECTURE + IMPLEMENTATION ACCEPTED
          ↓
REAL DANTE → SES SIGNUP/RECOVERY UAT
        PASS
          ↓
EMAIL PLATFORM ENGINEERING WORKSTREAM
        CLOSED
          ↓
REAL APPLE REGISTERED-DOMAIN UAT
        DEFERRED / OPEN
          ↓
M5 FINAL CLOSURE RECONCILIATION
        CURRENT
          ↓
M6 Native Mobile
        FUTURE / OPTIONAL / ONLY IF RE-GATED
          ↓
M7 Security Hardening / Observability / Authenticated Handoff
        PLANNED
```

## 2. What is already proved

```text
password + opaque AuthSession
signup / verification / recovery / reset / reauth
Google backend + official GIS Web integration
Apple backend/grant/notification lifecycle
passkeys / WebAuthn with real fido2 verification
passwordless Accounts
provider linking/unlinking
safe authenticator lifecycle + anti-lockout
public FastAPI/OpenAPI/generated-client contract
/security management Web surface
real Windows Hello passkey UAT
real Google provider UAT + direct PostgreSQL inspection
shared durable Email Platform
real SES signup verification
real SES password recovery
real SES password-reset notification
post-reset no-auto-login
post-reset prior-session revocation
Email Platform provider correlation + secret wipe in real PostgreSQL UAT
```

Do not reopen closed implementation blocks absent direct defect evidence.

## 3. Email Platform — closed engineering direction

Current accepted architecture and implementation:

```text
DANTE owns email lifecycle
external provider owns last-mile Internet delivery
PostgreSQL transactional outbox is materialized
feature mutation + EmailIntent are atomically coordinated
provider I/O stays outside caller transaction
Amazon SES API v2 is accepted primary external adapter
SMTP remains LOCAL/CI/compatibility transport behind same durable worker
provider feedback returns into DANTE delivery/suppression state
sensitive delivery payload uses dedicated AEAD protection + terminal wipe
no blind retry after ambiguous outcome
```

Authorities:

- `architecture/email-platform.md`
- `decisions/ADR-012-email-delivery-platform.md`
- `development/email-platform-local-uat.md`
- `development/email-platform-acceptance-2026-09-03.md`

Access/Auth integration is intentionally separate in `architecture/access-auth-email-delivery.md`.

## 4. Real Internet delivery acceptance — completed for current Auth consumer

Observed final UAT:

```text
normal email/password signup
→ real verification email arrived
→ received code worked
→ Account created

password recovery
→ real recovery email arrived
→ bearer URL opened reset surface
→ password changed
→ no auto-login
→ existing session revoked
→ password-change notification arrived
```

Runtime showed three `provider_accepted` SES attempts, all attempt 1.

Direct PostgreSQL inspection showed provider MessageId for all three accepted attempts and terminal sensitive-payload wipe for the corresponding intents.

One precise manual non-claim remains recorded: the same consumed recovery URL was not manually reopened in the final run because the message had already been deleted. This does not reopen the Email Platform workstream.

## 5. Production email deployment — future operational gate

Do not confuse the closed Email Platform with production sender deployment.

Before production email is called accepted, materialize and prove as applicable:

```text
DANTE-controlled sender domain/subdomain
SPF / DKIM / DMARC
production workload identity / IAM role
SES production account, quota and reputation posture
live provider event-ingress wiring
production alerting/SLOs
traffic/reputation segmentation
privacy/legal/subprocessor deployment review
Apple Private Email Relay sender-domain requirements when Apple is enabled
```

SES region is explicit deployment configuration. The accepted local real-provider UAT used `eu-west-3` (Paris); the architecture no longer hardcodes a preferred Milan production region.

## 6. Immediate next gate — whole M5 closure

The Email Platform is no longer the blocker.

The immediate next gate is:

```text
1. final documentation/branch coherence check
2. decide Apple real-UAT disposition
   - execute when real Apple + registered HTTPS domain prerequisites exist, OR
   - explicitly accept a bounded deferral for M5 closure
3. close M5 if no other direct defect evidence is open
4. proceed to M7 / authenticated Home handoff according to project priority
```

Do not invent an additional email milestone after this closure.

## 7. Apple acceptance

Apple backend architecture is implemented. Real Web acceptance remains deferred until a usable Apple account and registered HTTPS domain configuration are available.

The implementation/documentation must continue accepting both:

```text
privaterelay.appleid.com
private.icloud.com
```

per the accepted relay semantics.

Production Email sender/domain work must preserve Apple Private Email Relay compatibility.

## 8. M7 target

M7 should close the maturity gap visible in mature account/security products without changing the core Auth model:

```text
session/device inventory
per-session revoke
revoke all other sessions / log out everywhere
new-login/security-event alerts
“this wasn't me” response
production observability/alerting
final accessibility/release/legal review
final authenticated Home handoff
bounded componentization of the large Security UI
```

The shared Email Platform should carry future security-event notifications instead of creating a second mail subsystem.

## 9. Permanent email invariants

```text
OTP/recovery proof never in logs/metrics/traces
no long-lived plaintext sensitive outbox payload
provider accepted != delivered
network timeout != definitely not sent
no blind retry after ambiguous outcome
stable DANTE intent reference before external send
Auth/security tracking OFF
Auth/security link rewriting OFF
Auth/security marketing content FORBIDDEN
production SPF + DKIM + DMARC required before sender acceptance
Auth/security / product notifications / marketing separable
```

## 10. Authorities

```text
docs/PROJECT-STATUS.md
docs/ROADMAP.md
docs/workstreams/access-auth.md
docs/architecture/email-platform.md
docs/architecture/access-auth-email-delivery.md
docs/development/email-platform-local-uat.md
docs/development/email-platform-acceptance-2026-09-03.md
docs/decisions/ADR-012-email-delivery-platform.md
docs/database/README.md
docs/database/access-auth.md
```

Historical handoffs remain evidence only and must not override current executable or current-reference truth.
