# DANTE Architecture Index

- **Status:** CURRENT / AUTHORITATIVE NAVIGATION FOR `feature/access-auth`
- **Last reconciled:** 2026-09-03

## 1. Current architecture state

```text
Domain Model                         CLOSED
Logical Model                        CLOSED / 57 OF 57
Physical target                      CLOSED / ACCEPTED
Engineering Foundation               CLOSED / ACCEPTED
Frontend Foundation                  CLOSED / ACCEPTED
Backend CP1–CP6                      CLOSED / ACCEPTED
PostgreSQL                           18.6 / sole canonical persistence

Access/Auth M1–M4                    CLOSED / ACCEPTED
M5.1 architecture freeze             COMPLETE
M5.2 persistence/API freeze          COMPLETE
M5-A–D                               COMPLETE
Groups 1–3                           COMPLETE / ENGINEERING PASS
Group 4 product engineering          AUTOMATED QA PASS
local password/passkey UAT           PASS
real Google UAT                      PASS

Email Platform architecture          ACCEPTED / SHARED DANTE SUBSYSTEM
Email Platform implementation        ACCEPTED
Email Platform automated acceptance  PASS
primary external delivery adapter    AMAZON SES API V2
real DANTE → SES signup UAT           PASS
real DANTE → SES recovery UAT         PASS
real reset-notification UAT          PASS
Email Platform engineering           CLOSED

real Apple registered-domain UAT     DEFERRED / OPEN
whole M5                             ACTIVE / FINAL CLOSURE RECONCILIATION

Access/Auth Alembic head             20260903_15
Access/Auth DB topology              87 tables / 5 views / 15 routines /
                                     75 triggers / 170 indexes / 88 FKs /
                                     267 CHECKs
```

Protected `main` remains integrated authority for closed shared foundations. Newer Access/Auth and Email Platform truth is branch-local until explicit integration.

## 2. Current architecture entry points

- `system-overview.md` — system/component/authority overview
- `technical-decisions.md` — architecture decision register
- `email-platform.md` — standalone reusable DANTE Email Platform architecture
- `access-auth-architecture.md` — identity/authenticator/session architecture
- `access-auth-security-contract.md` — security/session/password/email/provider/passkey policy
- `access-auth-api-contract.md` — `/api/v1`, RFC 9457, OpenAPI/generated-client contract
- `access-auth-testing-contract.md` — proof layers and real-boundary contract
- `access-auth-m4-contract.md` — closed lifecycle authority
- `access-auth-m5-contract.md` — durable M5 multi-authenticator semantics
- `access-auth-m5-persistence-api-contract.md` — exact M5 persistence/API design and milestone reconciliation
- `access-auth-email-delivery.md` — Access/Auth consumer integration with the shared Email Platform
- `../development/email-platform-local-uat.md` — reproducible SES UAT runbook
- `../development/email-platform-acceptance-2026-09-03.md` — observed real-provider acceptance evidence
- `../workstreams/access-auth.md` — current operational state
- `../workstreams/access-auth-m5-review-2026-09-02.md` — review/UAT evidence before final Email closure
- `../database/README.md` and `../database/access-auth.md`
- `../frontend/access.md`

Important ADRs:

- `../decisions/ADR-007-domain-model-informed-persistence-boundaries.md`
- `../decisions/ADR-008-frontend-engineering-stack.md`
- `../decisions/ADR-009-frontend-architecture-boundaries.md`
- `../decisions/ADR-010-postgresql-persistence-constitution.md`
- `../decisions/ADR-011-access-auth-architecture.md`
- `../decisions/ADR-012-email-delivery-platform.md`

## 3. Permanent Auth architecture

```text
Person != Account != Principal != Actor
AuthSession != DANTE Session
EmailIdentity != Account
PasswordCredential optional
Principal request-runtime only
Account → 0..N AuthSessions
Account → 0..N ExternalIdentities
Account → 0..N PasskeyCredentials
provider identity key = issuer + subject
provider email != identity/link authority
provider authentication != provider-data authorization
provider assertion != DANTE AuthSession
passwordless Account valid
method != factor != assurance
```

Authenticator-specific code verifies evidence. Canonical DANTE policy/session creation remains a shared application/security boundary.

## 4. Browser security posture

```text
opaque high-entropy server-authoritative session
Secure + HttpOnly + host-only cookie direction
no JWT/localStorage/sessionStorage Auth authority
session-bound synchronizer CSRF
exact same-origin posture
Origin + Fetch Metadata
no broad credentialed CORS
recent reauthentication for sensitive mutations
same-session bearer rotation after reauth/security-context change
```

## 5. Provider architecture

Google:

```text
official Google Identity Services
DANTE transaction + nonce first
Google ID token = evidence only
backend signature/JWK/issuer/audience/nonce verification
issuer + sub canonical external identity
third-party mailbox → additional DANTE mailbox proof where current control matters
```

Apple:

```text
DANTE begin → Apple authorization → form_post/code exchange
issuer + subject authority
encrypted server grant lifecycle
server notifications
Private Email Relay semantics
```

Sign-in authorization remains separate from future Gmail/Calendar/iCloud data-integration grants.

## 6. Passkey architecture

```text
WebAuthn / FIDO2, not custom crypto
resident/discoverable credential required
user verification required
attestation none
exact RP/origin policy
opaque random user_handle
multiple passkeys
synced/device-bound/security-key compatible
DANTE stores credential public material, never biometric/PIN/private key
```

Frontend owns only browser ceremony conversion/interaction; backend `python-fido2` owns cryptographic/RP verification.

## 7. Email Platform architecture

The Email Platform is a **shared DANTE infrastructure subsystem**, not an Access/Auth-owned implementation detail.

Canonical platform authority:

```text
docs/architecture/email-platform.md
```

Current shape:

```text
DANTE feature/application mutation
        │
        ├── canonical state
        └── durable EmailIntent
                 ▼
PostgreSQL transactional outbox
                 ▼
claim / lease / worker
                 ▼
template + protected payload
                 ▼
provider-neutral adapter
        ├── Amazon SES API v2
        └── SMTP local/CI last mile
                 ▼
provider feedback
                 ▼
DANTE delivery-event / suppression state
                 ▼
privacy-minimized observability
```

Permanent rules:

```text
DANTE owns lifecycle/state; provider owns last-mile transport
PostgreSQL remains canonical authority
provider accepted != delivered
network timeout != definitely not sent
no blind retry after ambiguous outcome
no provider I/O in caller DB transaction
OTP/recovery proof excluded from logs/metrics/traces
short-lived encrypted sensitive payload + terminal wipe
Auth/security open tracking OFF
Auth/security click tracking/link rewriting OFF
future product consumers reuse platform rather than rebuilding delivery machinery
```

Access/Auth is currently the first consumer and is documented separately in `access-auth-email-delivery.md`.

## 8. Email Platform real-provider evidence

Final 2026-09-03 evidence directly proved:

```text
AWS non-root UAT principal + SES preflight       PASS
signup EmailIntent → SES → real mailbox         PASS
received OTP → Account creation                  PASS
password recovery → SES → real mailbox          PASS
recovery URL → reset                             PASS
no auto-login after reset                        PASS
prior AuthSession revoked                        PASS
reset security notification → real mailbox       PASS
```

Runtime emitted three SES `provider_accepted` outcomes, each on attempt 1.

Direct PostgreSQL inspection observed the three corresponding intents with provider MessageId present and the short-lived sensitive payload bundle wiped.

The first live attempt also proved the ambiguous failure path when Botocore temporary-credential refresh lacked region context. That defect was fixed by propagating `ses_region` through a boto3 Session and is now unit-covered.

The exact same consumed recovery link was not manually replayed in the final run; that one specific manual claim remains unasserted.

## 9. Current standards/deprecation review

Current Google/WebAuthn primitives remain accepted:

- Google uses current GIS and canonical `issuer + sub` identity authority.
- WebAuthn/FIDO2 remains the accepted passwordless/passkey direction.
- Apple semantics accept both `privaterelay.appleid.com` and `private.icloud.com` relay domains.

Email provider economics and deployment settings are not architectural constants. Production region, quotas and pricing must be checked at deployment time.

## 10. Progress metadata inside frozen contracts

The M5 contracts contain detailed milestone-time reconciliation sections. Statements such as `M5-F NEXT`, `email outbox later` or `public routes later` are historical for the slice when written if they conflict with current status/workstream/executable truth.

Current progress is owned by `PROJECT-STATUS`, `ROADMAP`, the active workstream and the current subsystem/evidence docs.

## 11. Current architecture gaps — deliberate, not hidden

Email Platform engineering is no longer an architecture gap.

Remaining deliberate gaps are:

```text
controlled production sender/domain
SPF + DKIM + DMARC production posture
production SES account/quota/reputation posture
production workload identity / IAM role
live cloud feedback/event routing when deployment requires it
production alerting / SLO / traffic segmentation
real Apple registered-domain UAT
M7 session/device management UX
M7 new-login/security-event response
final authenticated Home handoff
```

These are deployment, product-maturity or Apple-specific gates. No current evidence requires replacing the accepted Email Platform or Account/AuthSession/authenticator architecture.
