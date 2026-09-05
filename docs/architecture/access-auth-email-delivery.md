# DANTE — Access/Auth Integration with the Email Platform

- **Status:** CURRENT / ACCESS-AUTH CONSUMER CONTRACT / OWNERSHIP VERIFIED / INTEGRATED
- **Last reconciled:** 2026-09-04
- **Platform authority:** `email-platform.md`
- **Decision authority:** `../decisions/ADR-012-email-delivery-platform.md`
- **Accepted real-provider evidence:** `../development/email-platform-acceptance-2026-09-03.md`
- **Accepted implementation proof HEAD:** `81639c61478b476c995652d0060dde8f53aef089`
- **Protected-main integration:** PR #52 / `5f76ec54ad78542f137e8730e904f805d9e59e56`

## 1. Scope

This file defines only the Access/Auth consumer integration.

```text
Email Platform = shared DANTE technical infrastructure
Access/Auth     = first consumer
```

Access/Auth must not own provider clients, generic worker mechanics, retry/ambiguity policy, platform provider-event persistence, shared recipient suppression or shared delivery observability.

Access/Auth **does** own the meaning of its messages, its typed commands, its stream/purpose/template vocabulary and its actual security-message rendering.

## 2. Current Auth email vocabulary

Current stream:

```text
auth_security
```

Current purposes:

```text
signup_verification
provider_enrollment_verification
password_recovery
password_reset_notification
```

Current templates:

```text
auth.signup_verification
auth.provider_enrollment_verification
auth.password_recovery
auth.password_reset_notification
```

Current new-intent template revision:

```text
2
```

These are Auth consumer values. They are not the complete shared-platform vocabulary.

## 3. Consumer adapter boundary

Current Auth integration is intentionally split:

```text
Auth lifecycle / provider flow
→ typed Auth EmailCommand
→ Auth email_intent_spec(...)
→ shared EmailIntentSpec
→ shared DurableEmailOutbox
```

The Auth adapter supplies:

```text
purpose
stream = auth_security
template code
template revision
recipient
payload
operation scope / idempotency key
supersession key where required
expiry
```

The shared platform supplies durable admission, payload protection, claim/lease, attempts, retry/ambiguity policy and provider delivery.

## 4. Transaction boundary

When Auth requires email, canonical Auth state and EmailIntent are staged in the same PostgreSQL transaction.

Examples:

```text
password signup challenge
+ signup verification EmailIntent
→ one commit

password recovery challenge
+ password recovery EmailIntent
→ one commit

provider enrollment challenge
+ enrollment verification EmailIntent
→ one commit
```

If EmailIntent staging conflicts/fails, the Auth mutation fails with the transaction. Provider network I/O never occurs inside that transaction.

## 5. Idempotency and supersession

Auth chooses operation-specific idempotency and supersession identities; the platform arbitrates them durably.

Same operation scope/key is a replay only if all immutable intent dimensions still match, including recipient, stream, purpose, template/revision, locale, supersession identity and protected payload fingerprint.

A changed Auth proof/message under the same idempotency identity is a conflict, not a silent replay.

Resend/rotation flows create fresh proof material and supersede stale eligible work so an older OTP/recovery message cannot remain independently claimable after canonical proof rotation.

## 6. Neutral recovery posture

Public password recovery remains enumeration-resistant.

A neutral/no-op path does not create a fake durable EmailIntent and does not send external mail. Shared delivery is invoked only when canonical Auth state authorizes delivery.

## 7. Sensitive material

Signup/provider OTP and password-recovery bearer material remain Auth/security secrets.

Access/Auth constructs only the typed consumer payload. The shared platform owns short-lived AES-256-GCM persistence protection, keyed fingerprinting and terminal/unsafe-state wipe.

Auth must never put these secrets into normal logs, metrics, traces or provider tags.

## 8. Rendering ownership

Access/Auth owns the actual repository security renderer:

```text
AuthSecurityEmailRenderer
```

It is injected through the shared platform `EmailRendererPort`.

The renderer:

```text
accepts only stream = auth_security
authenticates/decrypts the claimed payload through the shared cipher
selects Auth purpose/template copy
produces provider-neutral text + optional HTML
escapes dynamic HTML content
preserves revision compatibility
```

Revision `1` remains supported for already-persisted compatibility. New Auth intents use revision `2` with plain text + minimal HTML.

Security-message policy remains:

```text
open tracking      OFF
click tracking     OFF
link rewriting     OFF
marketing content  FORBIDDEN
```

The shared package must not import this renderer or any other `dante.auth` module.

## 9. Provider independence

Auth does not depend on SES SDK types, SMTP status codes or provider-specific retry behavior.

```text
Auth consumer
→ shared durable platform
→ provider-neutral adapter
→ SES / SMTP
```

SES API v2 is the accepted external adapter. SMTP is a shared local/CI compatibility adapter, not an Auth process-memory queue.

## 10. Feedback projection

Provider feedback and recipient suppression are shared Email Platform state.

Auth receives only the consumer projection required by Auth semantics. Current strong hard-bounce/complaint suppression can project:

```text
EmailIdentity.recovery_restriction_code = provider_delivery_disabled
```

That write is performed by the Auth-owned `AuthEmailSuppressionProjection`, injected into the shared feedback store. Therefore shared `dante.platform.email.feedback` does not import or mutate Auth persistence directly.

This projection does not redefine email verification or ownership truth.

## 11. Acceptance evidence

The accepted 2026-09-03 real SES UAT proved the original durable behavior end to end:

```text
signup verification delivery + OTP use
password recovery delivery + link use
password reset
no automatic login after reset
prior AuthSession revocation
password-reset security notification delivery
three provider_accepted attempts with provider MessageId
terminal sensitive-payload wipe
```

That remains valid historical real-provider evidence.

The later ownership refactor moved reusable mechanics under `dante.platform.email`, introduced renderer/projection ports, hardened replay identity and added forward migration `20260904_16` for shared bounded stream/purpose vocabulary.

Those later changes were accepted on implementation proof HEAD `81639c61478b476c995652d0060dde8f53aef089` through:

```text
architecture/dependency guard              PASS
fast/static regression                      PASS
real PostgreSQL acceptance                  PASS
shared replay/idempotency coverage          PASS
combined Backend CI                         PASS
combined Frontend CI                        PASS
CP07 enriched-baseline LOCAL recovery       PASS
```

PR #52 then integrated that exact accepted capability into protected `main`. Post-merge CI on `5f76ec54ad78542f137e8730e904f805d9e59e56` passed Backend Quality, real PostgreSQL, Backend CI Gate, Frontend Quality, Web E2E, Mobile Bundle and Frontend CI Gate.

The real SES UAT was not rerun after every structural refactor commit and is not represented as if it were. Production sender/domain deployment remains separate.

## 12. Closure boundary

The accepted Auth email capability and shared platform ownership are **CLOSED / INTEGRATED** on protected `main`.

Current disposition:

```text
Access/Auth consumer semantics       CLOSED / INTEGRATED
shared Email Platform ownership      VERIFIED / INTEGRATED
real SES UAT evidence                ACCEPTED HISTORICAL EVIDENCE
production sender/domain deployment  SEPARATE FUTURE GATE
```

There is no remaining protected-main Access/Email integration step. Future Email work is activated only by a real consumer/deployment requirement.

## 13. References

```text
docs/architecture/email-platform.md
docs/decisions/ADR-012-email-delivery-platform.md
docs/development/email-platform-local-uat.md
docs/development/email-platform-acceptance-2026-09-03.md
docs/database/access-auth.md
docs/workstreams/access-auth-integration-acceptance-2026-09-04.md
```
