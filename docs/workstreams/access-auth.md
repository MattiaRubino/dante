# DANTE — Access/Auth Full-Stack Workstream

- **Status:** ACTIVE / M1–M4 CLOSED / M5 FINAL CLOSURE RECONCILIATION
- **Branch:** `feature/access-auth`
- **Intended worktree:** `/home/mattia/projects/dante`
- **Current Access/Auth Alembic head:** `20260903_15`
- **Architecture authority:** `../architecture/access-auth-m5-contract.md`
- **Exact persistence/API authority:** `../architecture/access-auth-m5-persistence-api-contract.md`
- **Shared Email Platform authority:** `../architecture/email-platform.md`
- **Access/Auth Email integration:** `../architecture/access-auth-email-delivery.md`
- **Email decision:** `../decisions/ADR-012-email-delivery-platform.md`
- **Real Email acceptance evidence:** `../development/email-platform-acceptance-2026-09-03.md`

> Continue this existing workstream. Do not restart Access/Auth, create a replacement Account/session model, or reopen accepted groups absent direct defect evidence.

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

shared Email Platform architecture          ACCEPTED
shared Email Platform persistence/worker    ACCEPTED
Amazon SES API v2 adapter                   ACCEPTED
Email Platform automated acceptance         PASS
real signup SES UAT                         PASS
real recovery SES UAT                       PASS
real reset-notification SES UAT             PASS
Email Platform engineering work             CLOSED

real Apple Web UAT                          DEFERRED / OPEN
whole M5                                    ACTIVE / FINAL CLOSURE RECONCILIATION
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

## 3. Product evidence already closed

Automated and live evidence already proved:

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
real Google passwordless signup/signin
canonical ExternalIdentity issuer + subject authority
canonical AuthSession convergence
```

The earlier UAT defects around session rotation, cross-chunk remote error identity and WebAuthn envelope shape are fixed and live-verified.

## 4. Email Platform closure

The Email Platform is **not** an Access/Auth-owned mail helper. It is a shared DANTE infrastructure subsystem and Access/Auth is the first consumer.

Accepted platform shape:

```text
Auth/feature mutation
+
durable EmailIntent
→ one PostgreSQL commit
→ durable claim/lease worker
→ protected payload + repository template
→ provider-neutral adapter
→ Amazon SES API v2 / SMTP local-CI compatibility
→ provider event/suppression model
→ privacy-minimized observability
```

Current persistence:

```text
dante.email_delivery_intent
dante.email_delivery_attempt
dante.email_provider_event
dante.email_recipient_suppression
```

Current Alembic evolution:

```text
20260831_13
→ 20260903_14 Email Platform persistence
→ 20260903_15 exact Email Platform runtime ACL hardening
```

Permanent invariants:

```text
DANTE owns lifecycle/state; provider owns last-mile transport
provider accepted != delivered
no provider network wait in caller transaction
no blind retry after ambiguous outcome
stable DANTE intent before external send
short-lived encrypted sensitive payload
terminal sensitive-payload wipe
Auth/security open tracking OFF
Auth/security click tracking/link rewriting OFF
Auth/security marketing content FORBIDDEN
```

## 5. Email automated / PostgreSQL evidence

Observed acceptance includes:

```text
Auth challenge/state + EmailIntent atomic commit          PASS
rollback when EmailIntent staging fails                   PASS
idempotency + immutable fingerprint                       PASS
supersession                                              PASS
claim/lease + SKIP LOCKED                                PASS
provider I/O outside DB transaction                       PASS
ambiguous no-blind-retry semantics                        PASS
SES one-wire-attempt configuration                        PASS
AES-GCM protected payload + terminal wipe                 PASS
feedback normalization/idempotency                        PASS
hard-bounce/complaint suppression                         PASS
post-restore quarantine                                   PASS
privacy-minimized observability                           PASS
runtime ACL least privilege                               PASS
Email unit/SES suite                                      9 / 9 PASS
focused Email/Auth PostgreSQL suite                       10 PASS
backend non-PostgreSQL regression                         234 PASS
build                                                     PASS
```

## 6. Real SES UAT — PASS

Final 2026-09-03 UAT used the repository-owned runbook, disposable PostgreSQL 18.6 and a dedicated non-root AWS UAT principal with temporary `aws login` credentials.

Directly observed:

```text
SES eu-west-3 preflight                       SUCCESS
signup EmailIntent → SES                      provider_accepted / attempt 1
real verification email                       RECEIVED
received OTP                                  VERIFIED
Account creation                              PASS

password recovery EmailIntent                 provider_accepted / attempt 1
real recovery email                           RECEIVED
recovery URL                                  CONSUMED
password reset                                PASS
no automatic signin after reset               PASS
prior AuthSession revoked                     PASS

password reset notification                   provider_accepted / attempt 1
real security notification                    RECEIVED
```

Direct PostgreSQL inspection before disposable DB shutdown observed exactly three live accepted intents:

```text
signup_verification
password_recovery
password_reset_notification
```

For all three:

```text
dispatch_state_code = provider_accepted
attempt_count = 1
accepted_at present
provider_code = ses
result_code = provider_accepted
provider_message_id present
error_code NULL
sensitive payload bundle wiped
sensitive_wiped_at present
```

Exact evidence is preserved in `../development/email-platform-acceptance-2026-09-03.md`.

### Precision / non-claim

The exact same consumed recovery link was not manually opened a second time in the final live run because the message had already been removed before that check. Do not report that specific replay rejection as manually observed.

## 7. Real-UAT defect closed

The first live SES signup exposed a Botocore browser-login credential-refresh region defect:

```text
NoRegionError during temporary-credential refresh
→ DANTE outcome = ambiguous
→ no blind retry
```

Root cause: region was supplied only to the SES client; Botocore's internal `signin` credential-refresh client also required session-level region context.

Fix: SES provider now creates a region-bound `boto3.Session` and derives the SES client from it. A focused unit test guards region propagation. The final live UAT passed after the fix.

## 8. Current database truth

```text
PostgreSQL          18.6
Alembic             20260903_15
87 tables / 5 views / 15 routines / 75 triggers
170 physical indexes / 88 FKs / 267 CHECKs
```

The Email Platform structures are bounded technical delivery persistence, not Domain semantic owners and not DANTE MaterialState.

## 9. Email production deployment — deliberately separate

The Email Platform workstream is closed, but production sender deployment is not automatically accepted.

Separate deployment gates:

```text
DANTE-controlled sender domain/subdomain
SPF / DKIM / DMARC
production workload identity / IAM role
SES production account/quota/reputation posture
live cloud provider-feedback ingress
production alerting/SLOs
traffic/reputation segmentation
privacy/legal/subprocessor review where required
Apple Private Email Relay sender-domain compatibility when Apple is enabled
```

These are deployment/operations requirements, not permission to create a second Email subsystem.

SES region is deployment configuration. The accepted local real-provider UAT used `eu-west-3`/Paris; no current authority hardcodes Milan as the production region.

## 10. Current next work

Email is no longer the next work item.

The bounded sequence is now:

```text
final M5 documentation/branch coherence
→ decide Apple real-UAT disposition
   execute when prerequisites exist
   OR explicitly accept bounded deferral for M5 closure
→ close M5 if no other direct defect evidence is open
→ M7 hardening / authenticated Home handoff according to project priority
```

Do not invent another email milestone or rebuild the platform for future consumers. New consumers extend the shared subsystem through explicit purpose/template/idempotency/preference semantics.

## 11. Apple real UAT — OPEN / DEFERRED

Requires a real Apple account plus registered-domain setup. Do not fake a production acceptance claim.

Current Apple relay semantics must support both:

```text
privaterelay.appleid.com
private.icloud.com
```

Production Email sender/domain work must preserve Apple Private Email Relay requirements.

## 12. M7 maturity work

Session/device management, remote revoke, new-login/security alerts, production operations/observability and final authenticated Home handoff belong here unless a correctness defect forces earlier work.

The shared Email Platform should carry future security-event notifications rather than creating a second notification-mail subsystem.

## 13. Documentation authority

Current operational truth lives here plus:

```text
../PROJECT-STATUS.md
../ROADMAP.md
../architecture/email-platform.md
../architecture/access-auth-email-delivery.md
../decisions/ADR-012-email-delivery-platform.md
../development/email-platform-local-uat.md
../development/email-platform-acceptance-2026-09-03.md
../database/README.md
../database/access-auth.md
```

Old dated handoffs and milestone-time `NEXT/OPEN/NOT MATERIALIZED` statements are historical where they conflict with current executable/current-reference truth.

## 14. Branch/worktree safety

```text
repo:      MattiaRubino/dante
branch:    feature/access-auth
worktree:  /home/mattia/projects/dante
```

Do not touch protected `main` or unrelated feature branches without explicit authorization. No merge/rebase/history rewrite/force push/protected-main write without explicit authorization.

No PASS without executed evidence. `SELECTED != IMPLEMENTED != AUTOMATED PASS != REAL UAT != PRODUCTION DEPLOYED`.
