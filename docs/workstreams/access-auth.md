# DANTE — Access/Auth Full-Stack Vertical Workstream

- **Status:** ACTIVE VERTICAL / M1–M4 CLOSED / M5 FINAL EXTERNAL ACCEPTANCE OPEN
- **Branch:** `feature/access-auth`
- **Intended worktree:** `/home/mattia/projects/dante`
- **Reviewed product checkpoint:** `ab2716abe40de658d99d1908ba31c5d5744e3c57`
- **Real-SMTP UAT tooling checkpoint:** `9c0587af5891249d8a6e6b6a5d6e3af6934c6943`
- **Accepted Alembic head:** `20260831_13`
- **Current review:** `access-auth-m5-review-2026-09-02.md`
- **Architecture authority:** `../architecture/access-auth-m5-contract.md`
- **Exact persistence/API authority:** `../architecture/access-auth-m5-persistence-api-contract.md`
- **Email architecture:** `../architecture/access-auth-email-delivery.md`
- **Email decision:** `../decisions/ADR-012-email-delivery-platform.md`

> Continue this existing vertical. Do not restart Access/Auth, create a replacement Account/session model, or reopen accepted Groups 1–3 absent direct defect evidence.

## 1. Current state

```text
M1–M4                                      CLOSED / ACCEPTED
M5.1 / M5.2                                COMPLETE
M5-A persistence                           COMPLETE / PG PROVEN
M5-B provider/crypto/WebAuthn               COMPLETE / ENGINEERING PASS
M5-C Google backend                        COMPLETE / ENGINEERING PASS
M5-D Apple backend                         COMPLETE / ENGINEERING PASS
GROUP 1 lifecycle/passwordless             COMPLETE / ENGINEERING PASS
GROUP 2 passkeys                           COMPLETE / ENGINEERING PASS
GROUP 3 public API/generated client         COMPLETE / ENGINEERING PASS
GROUP 4 product engineering                AUTOMATED QA PASS
GROUP 4 local manual UAT                    PASS
GROUP 4 real Google UAT                    PASS

email-delivery architecture                ACCEPTED DIRECTION
primary production provider target         AMAZON SES API V2 / QUALIFICATION OPEN
durable Email Platform                     NOT MATERIALIZED
real Internet email delivery               OPEN
real Apple Web UAT                         DEFERRED / OPEN
whole M5                                   ACTIVE / NOT CLOSED
```

## 2. Frozen Auth constitution

```text
Person != Account != Principal != Actor
AuthSession != DANTE Session
EmailIdentity != Account
PasswordCredential optional
Principal runtime-derived, never persisted
multiple AuthSessions normal
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

Forbidden without a new architecture gate: JWT/localStorage browser Auth, persisted Principal, silent provider-email merge, provider token as DANTE session, provider-specific Account authority, ad-hoc raw Auth fetch clients, hand-written WebAuthn crypto, biometric/PIN/device-fingerprint persistence.

## 3. Current product evidence

Automated gate at `ab2716...`:

```text
format/typecheck/lint/architecture PASS
68 / 68 Web unit/component PASS
60 / 60 Auth Playwright PASS
Chromium / Firefox / WebKit through canonical HTTPS suite
```

Live local UAT proved:

```text
password signin/logout
session/reload authority
password reauth + rotated bearer persistence
real Windows Hello passkey registration
passkey reauth
passwordless passkey signin
passkey rename persistence
password removal with alternate authenticator
last-authenticator anti-lockout
password restore + fresh signin
direct PostgreSQL coherence
```

Real Google UAT proved official GIS → real Google token → backend verification → third-party mailbox proof → passwordless DANTE Account → canonical AuthSession. Direct DB inspection proved `ExternalIdentity(provider=google, issuer=https://accounts.google.com)`, zero PasswordCredential and an active AuthSession.

See `access-auth-m5-review-2026-09-02.md` for the full evidence and defect history.

## 4. UAT defects closed

```text
AuthSession rotation/read race            FIXED + LIVE VERIFIED
cross-chunk remote-error identity         FIXED
WebAuthn options.publicKey envelope       FIXED + WINDOWS HELLO LIVE VERIFIED
```

These defects justify retaining manual UAT as a separate proof layer.

The first real Google attempt's `401 invalid_client` was an external/UAT configuration transcription error: one character of the public OAuth Client ID had been typed incorrectly. Exact-copying the Client ID fixed the flow without a DANTE code change. The GIS ID-token flow does not require the OAuth client secret in the browser.

## 5. Database truth

```text
PostgreSQL          18.6
Alembic             20260831_13
83 tables / 5 views / 15 routines / 75 triggers
156 physical indexes / 85 FKs / 233 CHECKs
103 standalone Dictionary entries
```

Group-4 product work did not create a new DB topology. `20260831_13` is the bounded runtime ACL required by authenticator lifecycle.

The target email transactional outbox/delivery-state model is **not materialized yet** and therefore is not included in these catalog counts.

## 6. Current next work

### 6.1 Email architecture — CLOSED AS DIRECTION

The research question is no longer “SMTP provider or self-hosted?” The selected architecture is:

```text
DANTE owns email intent/lifecycle/state
external specialist provider owns last-mile Internet delivery
PostgreSQL transactional outbox is durable target
EmailDeliveryPort remains provider-neutral application boundary
Amazon SES API v2 is primary production adapter target
preferred initial SES region target: eu-south-1 Europe/Milan
SMTP remains deterministic LOCAL/UAT/compatibility transport
provider feedback returns into DANTE delivery/suppression state
```

See ADR-012 and `../architecture/access-auth-email-delivery.md`.

The current `SmtpEmailDispatcher` is retained; it is a good bounded implementation/UAT adapter, not the final durable production platform.

### 6.2 Email provider / operational qualification — NEXT

Do **not** implement the production outbox/SES adapter before this gate is complete.

Research with current official evidence:

```text
AWS account/billing posture
SES sandbox vs production-access requirements
SES eu-south-1 exact availability, quotas and current pricing
sender identity/domain setup
SPF / DKIM / DMARC
IAM role/workload identity + least privilege
SES API v2 SDK/runtime boundary
configuration sets / traffic segmentation
event destinations and SNS vs EventBridge ingestion
provider retention/privacy/subprocessors
failure semantics / provider limits
manual UAT route without committing credentials
```

Important correction: the former SES-specific 3,000-message/month first-year allowance is not available to **new** AWS customers after July 21, 2026. Current pricing/credits must be checked at qualification/deployment time. Provider selection is architectural, not based on an obsolete promotion.

If qualification reveals a material blocker, reopen the provider target narrowly and compare viable alternatives. Do not reopen the DANTE-owned lifecycle/provider-neutral boundary without evidence.

### 6.3 Email Platform exact implementation gate — OPEN AFTER QUALIFICATION

Freeze the smallest complete slice for:

```text
transactional outbox persistence
claim/lease/recovery semantics
delivery attempt + provider message reference
sensitive OTP/recovery payload protection
SES API adapter
idempotency / retry / ambiguous-send handling
provider event verification + normalization
bounce/complaint suppression/restriction mapping
observability / metrics / failure injection
Dictionary / SQLAlchemy / Alembic / PostgreSQL / ACL alignment
```

Exact table names and migrations are not pre-authorized by ADR-012. They require a normal ADR-010/CP6 persistence write gate.

Email security invariants:

```text
provider accepted != delivered
network timeout != definitely not sent
no blind retry after ambiguous send
OTP/recovery proof not in logs/metrics/traces
no indefinite plaintext sensitive outbox payload
Auth/security tracking OFF
click tracking/link rewriting OFF
marketing content FORBIDDEN in Auth/security mail
SPF + DKIM + DMARC before production sender acceptance
Auth/security / product notifications / future marketing separable
```

### 6.4 Real Internet email UAT — OPEN

After the bounded production-capable implementation exists, prove with a real mailbox:

```text
normal email/password signup verification
third-party provider mailbox verification
password recovery link
password reset
all-session revocation
password-change notification
direct PostgreSQL state
provider acceptance/delivery feedback where available
```

Loopback capture remains CI proof. It must never be mislabeled real Internet delivery.

The opt-in real-SMTP support at `9c0587...` remains useful UAT tooling and still requires targeted format/lint/compile + real-provider qualification before being called accepted as a real-delivery harness path.

### 6.5 Apple real UAT — OPEN / DEFERRED

Requires a real Apple account plus registered-domain setup. Do not fake a production acceptance claim.

Current Apple relay semantics must support both:

```text
privaterelay.appleid.com
private.icloud.com
```

Sender/domain work for the Email Platform must preserve Apple Private Email Relay requirements.

### 6.6 M7 — planned maturity hardening

Session/device management, remote revoke, security-event alerts, production observability and final authenticated Home handoff belong here unless a correctness defect forces earlier work.

The M5 Email Platform should later carry security-event notifications rather than creating a second notification-mail subsystem.

## 7. Maintainability note

The current security surface is functionally proved, but `access-security-page.tsx` has accumulated substantial orchestration/rendering responsibility. Before adding much more account-security UX, split it by bounded password/provider/passkey/reauth ownership while preserving the accepted application/platform boundaries. This is a maintainability hardening, not a reason to reopen Auth semantics.

## 8. External benchmark / deprecation conclusions

Current reviewed conclusions:

```text
Google GIS/FedCM button path               current
Google issuer+sub identity authority       current
WebAuthn/FIDO2 direction                   current
Apple dual relay-domain handling           current
NIST password direction                    aligned
GitHub/Notion/Linear security UX           confirms M7 maturity gaps, not an Auth redesign
Netflix/Fanatics email evidence            supports internal lifecycle + external delivery engine
```

Do not claim undocumented provider choices for Notion, Linear or other products without current public evidence.

## 9. Documentation authority

Current operational status lives here plus:

```text
../PROJECT-STATUS.md
../ROADMAP.md
access-auth-m5-review-2026-09-02.md
../architecture/access-auth-email-delivery.md
../decisions/ADR-012-email-delivery-platform.md
```

The old 2026-08-29 dated live handoff is superseded/historical. The 2026-09-02 handoff is temporary branch-operational continuity only; before merge it must be consolidated/removed under the documentation lifecycle policy.

M5 architecture/persistence contracts remain semantic authority, but phase-progress text inside them is historical where it conflicts with these current operational documents.

## 10. Branch/worktree safety

```text
repo:      MattiaRubino/dante
branch:    feature/access-auth
worktree:  /home/mattia/projects/dante
```

Do not touch `main`, `feature/home-react`, `feature/access-frontend` or `/home/mattia/projects/dante-frontend` without explicit topology authorization. No merge/rebase/history rewrite/force push/protected-main write without explicit authorization.

Before every write:

```text
state branch + exact remote HEAD
state exact file scope / purpose / out-of-scope
race-check remote HEAD immediately before write
write only bounded paths
post-scope compare
```

No PASS without executed evidence. `SELECTED != IMPLEMENTED != DIRECT PASS`.
