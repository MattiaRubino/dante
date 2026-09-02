# DANTE — Project Status

- **Status:** CURRENT TRUTH FOR `feature/access-auth`
- **Last reconciled:** 2026-09-02
- **Protected `main`:** integrated source authority; Access/Auth remains branch-local until explicit merge gate
- **Active product vertical:** Access/Auth
- **Current macro-phase:** M5 — Multi-authenticator Account Layer — **ACTIVE / FINAL EXTERNAL ACCEPTANCE OPEN**
- **Reviewed product checkpoint:** `ab2716abe40de658d99d1908ba31c5d5744e3c57`
- **Email-UAT tooling checkpoint:** `9c0587af5891249d8a6e6b6a5d6e3af6934c6943`
- **Documentation reconciliation base:** `bbf63fe0375c52ec2c49448ae7f6e9d238b4ba74`
- **Accepted Alembic head:** `20260831_13`
- **Current review evidence:** `workstreams/access-auth-m5-review-2026-09-02.md`
- **Current email architecture:** `architecture/access-auth-email-delivery.md` + `decisions/ADR-012-email-delivery-platform.md`

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

Email delivery architecture direction      ACCEPTED
Primary production delivery target         AMAZON SES API V2 / QUALIFICATION OPEN
Durable email platform implementation       OPEN
Real Internet signup/recovery delivery      OPEN
Real Apple registered-domain UAT            DEFERRED / OPEN

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

The target email transactional outbox/delivery-state concepts are **not materialized yet** and therefore do not alter the current catalog counts.

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

## 5. Email architecture current truth

Architecture direction is now selected:

```text
DANTE owns email intent/lifecycle/state
external specialist provider owns last-mile Internet delivery
PostgreSQL transactional outbox is the durable target
EmailDeliveryPort remains provider-neutral application boundary
Amazon SES API v2 is the primary production adapter target
preferred initial SES region target: eu-south-1 Europe/Milan
SMTP remains deterministic test/UAT/compatibility transport
provider acceptance != recipient delivery
blind retry after ambiguous send outcome is forbidden
Auth/security tracking/link rewriting remain off
SPF + DKIM + DMARC required before production sender acceptance
```

This is an architecture decision, **not** production acceptance. Exact outbox schema, SES account/sandbox/IAM, sender DNS, provider event ingestion, suppression lifecycle, failure-model proof and live Internet delivery remain open.

The older SES-specific `3,000 message charges/month for the first 12 months` free-tier claim is stale for new AWS customers after July 21, 2026 and must not be used as current provider economics.

## 6. Open items before M5 closure

```text
Email Platform operational/provider qualification
→ SES account + sandbox/production-access model
→ exact regional capability/quotas and current pricing
→ IAM/workload-identity posture
→ sender domain/subdomain + SPF/DKIM/DMARC
→ privacy/retention/subprocessor review

Email Platform exact implementation gate
→ transactional outbox persistence design
→ sensitive OTP/recovery payload protection
→ SES API adapter
→ delivery-attempt/provider-message state
→ event ingestion and suppression/restriction mapping
→ retry/idempotency/ambiguous-outcome handling
→ observability/failure injection

Real Internet UAT
→ signup verification delivered to a real inbox
→ provider-mailbox verification delivered to a real inbox
→ recovery link delivered and consumed
→ password-change notification delivered
→ direct PostgreSQL + provider-event verification

Apple
→ registered HTTPS domain/provider configuration
→ real Apple account UAT when available
→ Private Email Relay sender/domain proof
```

The opt-in real-SMTP local-UAT support introduced at `9c0587...` remains useful tooling and still requires its targeted qualification before being treated as an accepted real-delivery harness path. It is not the production architecture.

## 7. M7 maturity work

Compared with mature consumer/work tools, the main post-M5 account-security maturity work remains compatible with the current model:

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

## 8. Deprecation/coherence reconciliation

2026-09-02 review:

```text
Google GIS/FedCM button path                   CURRENT
Google issuer+sub authority                    CURRENT
WebAuthn/FIDO2 direction                       CURRENT
Apple relay dual-domain handling               CURRENT
old M2/M3-not-started workstream index          STALE → RECONCILED
old pre-Access technical-decision status        STALE → RECONCILED
old SES 3,000/month new-customer free-tier      STALE → REJECTED AS CURRENT CLAIM
```

Historical phase-time progress text inside otherwise durable contracts remains evidence only where newer operational authorities supersede it.

## 9. Documentation authority

Current operational truth:

1. this file;
2. `ROADMAP.md`;
3. `workstreams/access-auth.md`;
4. `workstreams/access-auth-m5-review-2026-09-02.md`;
5. `architecture/access-auth-email-delivery.md` and `decisions/ADR-012-email-delivery-platform.md` for email;
6. current executable code/tests/migrations.

Architecture/security/API contracts remain durable semantic authority. Old phase-progress statements embedded in those contracts are historical milestone snapshots and do not override the current operational state.

The dated `workstreams/access-auth-m5-live-handoff-2026-08-29.md` is superseded/historical. While this branch remains active, the current branch-operational handoff is `workstreams/access-auth-m5-live-handoff-2026-09-02.md`; it must not merge into protected `main` without the documentation-lifecycle consolidation gate.
