# DANTE — Access/Auth M4–M7 Execution Plan

- **Status:** CURRENT EXECUTION PLAN / M4 CLOSED / M5 FINAL EXTERNAL ACCEPTANCE OPEN
- **Branch:** `feature/access-auth`
- **Worktree:** `/home/mattia/projects/dante`
- **Last reconciled:** 2026-09-02
- **Reviewed product checkpoint:** `ab2716abe40de658d99d1908ba31c5d5744e3c57`
- **Current branch checkpoint before docs reconciliation:** `9c0587af5891249d8a6e6b6a5d6e3af6934c6943`
- **Accepted Alembic head:** `20260831_13`
- **Review evidence:** `access-auth-m5-review-2026-09-02.md`

## 1. Closed implementation sequence

```text
M4 lifecycle/recovery/reauth                 CLOSED / ACCEPTED
M5.1 architecture                            COMPLETE
M5.2 persistence/API design                  COMPLETE
M5-A–D                                       COMPLETE
GROUP 1 M5-E+G                               COMPLETE
GROUP 2 M5-F                                 COMPLETE
GROUP 3 M5-H+I                               COMPLETE
GROUP 4 Web product engineering              AUTOMATED QA PASS
GROUP 4 local password/passkey UAT            PASS
GROUP 4 real Google UAT                      PASS
```

Do not restart the old Group-4 candidate QA plan; it has executed and is preserved in Git history/review evidence.

## 2. Permanent implementation boundaries

```text
Account = durable security root
EmailIdentity separate from Account
PasswordCredential optional
Principal runtime-derived
opaque PostgreSQL-backed AuthSession
Secure HttpOnly host-only Web session
session-bound CSRF + exact Origin/Fetch Metadata
provider identity = issuer + subject
provider token/assertion != DANTE AuthSession
passwordless Account valid
WebAuthn private-key/biometric material never stored by DANTE
OpenAPI → governed @dante/api-client → bounded Web remote
```

## 3. Current execution block — EMAIL ARCHITECTURE RESEARCH

Before another email-delivery code change, answer:

1. What must DANTE own canonically: message intent, security-event state, delivery attempt state, provider message ID, bounce/complaint/suppression state?
2. What should an external provider own: SMTP/HTTP transport, reputation, DKIM signing, feedback loops, global routing?
3. Does DANTE need a provider-neutral delivery port now or only when a second provider/real production requirement exists?
4. How are ambiguous SMTP/HTTP outcomes handled without duplicate security mail or silent loss?
5. Which messages are resendable (OTP/recovery) and which are notification-only?
6. Is an outbox/queue justified by the actual Class-A correctness requirement, or is the current bounded process queue sufficient for the first deployment stage?
7. What are the exact SPF/DKIM/DMARC, bounce, complaint and suppression responsibilities?
8. How do LOCAL/DEV/UAT/PROD prevent accidental delivery to real users?
9. What does Apple Private Email Relay require from sender/domain configuration?
10. Compare self-hosted SMTP operational burden with transactional providers before vendor selection.

The existing `9c0587...` real-SMTP UAT opt-in remains a transport experiment only. It is not production architecture authority.

## 4. Real email UAT after architecture selection

Once the boundary is accepted:

```text
real signup
→ real mailbox delivery
→ OTP verification
→ Account creation
→ DB inspection

real password recovery
→ neutral request
→ real recovery email
→ one-use reset
→ old sessions revoked
→ fresh signin
→ DB inspection
```

Delivery proof must include the actual external delivery path, not loopback capture.

## 5. Apple real UAT

Deferred until real Apple account + registered HTTPS domain configuration are available.

Must prove:

```text
real Apple authorization
form_post/callback
server-side code exchange
canonical issuer+subject binding
Private Email Relay handling
Account/AuthSession result
revoke/grant lifecycle as practically testable
outbound relay sender configuration
```

Current 2026 guidance requires support for both legacy `privaterelay.appleid.com` and new `private.icloud.com` Sign in with Apple relay addresses.

## 6. M5 closure gate

M5 closes only when:

```text
closed engineering proof remains green
real external email architecture selected + qualified
real signup/recovery delivery UAT passes
Apple real UAT passes or is explicitly accepted as a bounded deferred release prerequisite by the user
all current docs reconciled
explicit user acceptance
```

Do not convert an unavailable Apple account into fake PASS.

## 7. M6

Native Mobile remains future/optional and requires a deliberate gate. Do not install or materialize native Auth merely to make the roadmap look complete.

## 8. M7

Target mature account-security UX and production hardening:

```text
session/device list
per-session revoke
revoke all others / log out everywhere
new-login/security-event alerts
“this wasn't me” flow
security-event retention/observability
production operational dashboards/alerts
final accessibility/legal/release checks
final authenticated Home handoff
componentization/hardening of Security UI
```

The existing Account/AuthSession/authenticator architecture is intentionally capable of supporting this without semantic rewrite.

## 9. Safety

No merge/rebase/history rewrite/protected-main write without explicit authorization. Implementation/debug remains assistant-owned; the user supplies UAT/external-account actions and raw evidence.