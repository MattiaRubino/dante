# DANTE Roadmap

- **Status:** CURRENT FOR `feature/access-auth`
- **Last reconciled:** 2026-09-02
- **Active vertical:** Access/Auth
- **Current macro-phase:** M5 — Multi-authenticator Account Layer — **FINAL EXTERNAL ACCEPTANCE OPEN**
- **Reviewed product checkpoint:** `ab2716abe40de658d99d1908ba31c5d5744e3c57`
- **Current branch checkpoint before docs reconciliation:** `9c0587af5891249d8a6e6b6a5d6e3af6934c6943`

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
EMAIL DELIVERY ARCHITECTURE + REAL DELIVERY UAT
        NEXT
          ↓
REAL APPLE REGISTERED-DOMAIN UAT
        DEFERRED / OPEN
          ↓
M5 closure
        BLOCKED ON REMAINING EXTERNAL ACCEPTANCE
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
68 Web unit/component tests
60 Auth browser tests across Chromium/Firefox/WebKit
real Windows Hello passkey UAT
real Google provider UAT + direct PostgreSQL inspection
```

Do not reopen closed implementation blocks absent direct defect evidence.

## 3. Immediate next gate — email delivery architecture

Do **not** select an SMTP vendor first and rationalize later.

The next research must decide the durable boundary:

```text
DANTE application responsibility
vs
external transactional-email delivery responsibility
```

Evaluate at least:

```text
SMTP vs provider HTTP API boundary
provider portability / adapter ownership
sender/domain strategy
SPF / DKIM / DMARC
bounce / complaint / suppression handling
ambiguous delivery outcome + retry/idempotency
rate limits and backpressure
queue/outbox need based on real failure model
observability and security logging
secret rotation
privacy/data residency
DEV/UAT/PROD separation
Apple Private Email Relay compatibility
cost/limits/operational burden
self-hosted SMTP deliverability burden
```

Only after that research may DANTE qualify a provider or self-hosted strategy and run real signup/recovery delivery UAT.

`9c0587...` merely provides an explicit opt-in SMTP transport path for local UAT; it is not an architecture/provider decision.

## 4. Apple acceptance

Apple backend architecture is implemented. Real Web acceptance remains deferred until a usable Apple account and registered HTTPS domain configuration are available.

The implementation/documentation must continue accepting both:

```text
privaterelay.appleid.com
private.icloud.com
```

per Apple's current 2026 Sign in with Apple relay guidance.

## 5. M7 target

M7 should close the maturity gap visible in products such as GitHub, Notion, Linear and Microsoft account management without changing the core Auth model:

```text
session/device inventory
per-session revoke
revoke all other sessions / log out everywhere
new-login/security-event alerts
“this wasn't me” response
production observability
final accessibility/release/legal review
final authenticated Home handoff
bounded componentization of the large Security UI
```

## 6. Authorities

```text
docs/PROJECT-STATUS.md
docs/ROADMAP.md
docs/workstreams/access-auth.md
docs/workstreams/access-auth-m5-review-2026-09-02.md
docs/architecture/access-auth-*.md
docs/database/README.md
docs/frontend/access.md
```

The old dated M5 live-handoff is historical/superseded.