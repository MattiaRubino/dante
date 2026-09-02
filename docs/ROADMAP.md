# DANTE Roadmap

- **Status:** CURRENT FOR `feature/access-auth`
- **Last reconciled:** 2026-09-02
- **Active vertical:** Access/Auth
- **Current macro-phase:** M5 — Multi-authenticator Account Layer — **FINAL EXTERNAL ACCEPTANCE OPEN**
- **Reviewed product checkpoint:** `ab2716abe40de658d99d1908ba31c5d5744e3c57`
- **Email-UAT tooling checkpoint:** `9c0587af5891249d8a6e6b6a5d6e3af6934c6943`
- **Documentation reconciliation base:** `bbf63fe0375c52ec2c49448ae7f6e9d238b4ba74`

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
EMAIL DELIVERY ARCHITECTURE
        ACCEPTED DIRECTION
          ↓
EMAIL PROVIDER / OPERATIONS QUALIFICATION
        NEXT
          ↓
EMAIL PLATFORM EXACT PERSISTENCE + IMPLEMENTATION GATE
        OPEN
          ↓
REAL INTERNET SIGNUP / RECOVERY DELIVERY UAT
        OPEN
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

## 3. Email architecture — selected direction

Current architectural decision:

```text
DANTE owns email lifecycle
external provider owns last-mile Internet delivery
PostgreSQL transactional outbox is durable target
EmailDeliveryPort remains provider-neutral
Amazon SES API v2 is primary production adapter target
preferred initial region target: eu-south-1 Europe/Milan
SMTP remains LOCAL/UAT/compatibility transport
provider feedback returns into DANTE delivery/suppression state
```

Authorities:

- `architecture/access-auth-email-delivery.md`
- `decisions/ADR-012-email-delivery-platform.md`

This direction does **not** mean email production acceptance is closed.

## 4. Immediate next gate — provider / operational qualification

Do not start the production outbox/SES implementation until this gate produces concrete evidence.

Research and prove:

```text
AWS account / billing posture
SES sandbox and production-access requirements
SES eu-south-1 exact capability, quotas and current pricing
sender identity/domain verification flow
DKIM / SPF / DMARC mechanics
IAM role/workload identity and least privilege
SES API v2 SDK/runtime integration posture
configuration sets and traffic segmentation
provider event destinations
SNS vs EventBridge boundary for DANTE ingestion
provider retention / privacy / subprocessors
current operational limits and failure semantics
manual UAT route without committing credentials
```

Provider comparison may be reopened if this qualification reveals a material blocker. SES is selected because it fits the desired architecture, not because of a temporary free allowance.

Important current correction: the old SES-specific 3,000-message/month first-year free tier is no longer available to **new** AWS customers after July 21, 2026. Use current pricing/credits when evaluating cost.

## 5. Exact Email Platform implementation gate — after qualification

Only after Section 4 is closed, freeze the bounded implementation slice:

```text
transactional outbox logical/physical design
delivery-attempt/provider-message state
claim/lease/recovery semantics
sensitive OTP/recovery payload protection
SES API adapter
idempotency and ambiguous-send reconciliation
provider event verification + normalization
bounce/complaint suppression mapping
observability / metrics / SLOs
failure-injection matrix
ACL/migration/dictionary alignment
```

Exact table names and migrations are deliberately **not** pre-authorized by the architecture document. They must pass ADR-010/CP6 persistence discipline.

## 6. Real Internet delivery acceptance

After implementation, execute real inbox UAT:

```text
normal email/password signup
→ real verification email arrives
→ code works
→ Account/AuthSession/DB state verified

Google account with third-party mailbox
→ DANTE mailbox proof delivered for real
→ provider enrollment completes

password recovery
→ real recovery email arrives
→ bearer URL validates and scrubs correctly
→ password changes
→ existing sessions revoked
→ password-change notification arrives

provider feedback
→ delivery/bounce/complaint path proved where feasible
→ direct PostgreSQL state inspected
```

Loopback SMTP remains CI proof; real inbox proof is a separate acceptance layer.

## 7. Current email security / delivery invariants

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
SPF + DKIM + DMARC before production acceptance
Auth/security / product notifications / marketing separable
```

## 8. External benchmark conclusion

Public evidence supports the selected split without claiming undocumented internals for unrelated products:

```text
Netflix
→ retired in-house email delivery for Amazon SES
→ separates reputation by traffic class
→ consumes delivery/bounce/complaint feedback

Fanatics
→ builds/owns its email platform lifecycle
→ uses Amazon SES as scalable delivery infrastructure
→ separates transactional/marketing streams
```

This is directional validation for `DANTE platform + external delivery engine`, not permission to copy another company's internal design mechanically.

Do not claim “Notion uses provider X” or “Linear uses provider Y” without current public evidence.

## 9. Apple acceptance

Apple backend architecture is implemented. Real Web acceptance remains deferred until a usable Apple account and registered HTTPS domain configuration are available.

The implementation/documentation must continue accepting both:

```text
privaterelay.appleid.com
private.icloud.com
```

per Apple's current 2026 Sign in with Apple relay guidance.

Email sender/domain work must preserve Apple Private Email Relay compatibility.

## 10. M7 target

M7 should close the maturity gap visible in mature account/security products without changing the core Auth model:

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

The email platform created for M5 recovery/signup should later carry security-event notifications rather than creating a second mail subsystem.

## 11. Authorities

```text
docs/PROJECT-STATUS.md
docs/ROADMAP.md
docs/workstreams/access-auth.md
docs/workstreams/access-auth-m5-review-2026-09-02.md
docs/architecture/access-auth-email-delivery.md
docs/decisions/ADR-012-email-delivery-platform.md
docs/architecture/access-auth-*.md
docs/database/README.md
docs/frontend/access.md
```

The old dated M5 live-handoff from 2026-08-29 is historical/superseded. The current 2026-09-02 handoff is branch-operational only and must be consolidated/removed before protected-main integration.
