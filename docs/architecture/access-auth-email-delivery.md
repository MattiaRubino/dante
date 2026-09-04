# DANTE — Access/Auth Integration with the Email Platform

- **Status:** CURRENT / ACCESS-AUTH CONSUMER CONTRACT / OWNERSHIP REFACTOR UNDER VERIFICATION
- **Last reconciled:** 2026-09-04
- **Platform authority:** `email-platform.md`
- **Decision authority:** `../decisions/ADR-012-email-delivery-platform.md`
- **Accepted real-provider evidence:** `../development/email-platform-acceptance-2026-09-03.md`

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

## 11. Accepted UAT evidence vs current refactor

The accepted 2026-09-03 real SES UAT proved the pre-refactor behavior end to end:

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

That evidence remains valid historical acceptance evidence.

The later ownership refactor moves reusable mechanics under `dante.platform.email`, introduces renderer/projection ports and hardens replay identity. Those changes are implemented but **must pass the current regression gate before being called re-accepted**.

Do not treat the older UAT as proof that later refactor commits have already passed.

## 12. Closure boundary

The accepted Auth email capability is not being redesigned. The current task is structural pre-integration hardening.

After the focused static/unit/PostgreSQL gate returns green:

```text
Access/Auth consumer semantics       remain CLOSED
shared Email Platform ownership      VERIFIED
real SES UAT evidence                remains ACCEPTED historical evidence
production sender/domain deployment  still separate
```

## 13. References

```text
docs/architecture/email-platform.md
docs/decisions/ADR-012-email-delivery-platform.md
docs/development/email-platform-local-uat.md
docs/development/email-platform-acceptance-2026-09-03.md
docs/database/access-auth.md
```
