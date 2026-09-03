# DANTE — Access/Auth Integration with the Email Platform

- **Status:** CURRENT / ACCESS-AUTH CONSUMER INTEGRATION ACCEPTED ON `feature/access-auth`
- **Last reconciled:** 2026-09-03
- **Platform authority:** `email-platform.md`
- **Decision authority:** `../decisions/ADR-012-email-delivery-platform.md`
- **Real-provider evidence:** `../development/email-platform-acceptance-2026-09-03.md`

## 1. Scope

This document is intentionally **not** the Email Platform architecture.

The reusable platform is documented independently in `email-platform.md`. This file defines only how Access/Auth consumes that shared subsystem.

```text
Email Platform = shared DANTE infrastructure
Access/Auth     = first platform consumer
```

Access/Auth must not own provider clients, process queues, retry machinery, provider-event storage or shared delivery observability.

## 2. Access/Auth email purposes

Current authorized Auth/security purposes are:

```text
signup_verification
provider_enrollment_verification
password_recovery
password_reset_notification
```

Current stream:

```text
auth_security
```

These purpose codes are intentionally bounded. Adding Account, calendar, workflow, reminder, digest or other product email does not belong in this contract; those consumers must extend the shared Email Platform explicitly.

## 3. Transaction boundary

When an Auth mutation requires delivery, the security mutation and EmailIntent are staged in the same PostgreSQL transaction.

Examples:

```text
password signup challenge
+
signup verification EmailIntent
→ one commit

password recovery challenge
+
password recovery EmailIntent
→ one commit

provider enrollment challenge/OTP mutation
+
provider enrollment EmailIntent
→ one commit
```

If EmailIntent staging conflicts/fails, the Auth mutation rolls back. Provider network I/O is never performed inside the Auth transaction.

## 4. Resend semantics

A resend creates fresh security proof material where required and stages a fresh EmailIntent in the same transaction.

The previous eligible Auth email intent is superseded/cancelled atomically through the platform supersession mechanism.

Old OTP/recovery delivery work must never remain independently claimable after the canonical Auth proof has been rotated.

## 5. Neutral recovery posture

Public password-recovery behavior remains enumeration-resistant.

A neutral/no-op recovery path does not persist a fake EmailIntent and does not cause provider delivery. The shared platform is invoked only when canonical Auth state actually authorizes delivery.

## 6. Sensitive material

Signup/provider OTP and password-recovery bearer material are security secrets.

Access/Auth supplies the compact typed payload to the Email Platform. The platform owns encryption-at-rest for the short-lived delivery payload and terminal wipe.

Auth code must not place those secrets into normal logs, metrics, traces or provider tags.

Final live UAT direct PostgreSQL inspection observed the sensitive payload bundle wiped after provider acceptance for signup verification and password recovery.

## 7. Rendering

Access/Auth owns the security-message meaning/copy requirements; the shared Email Platform owns repository rendering/versioning and provider-neutral message construction.

Current templates:

```text
auth.signup_verification
auth.provider_enrollment_verification
auth.password_recovery
auth.password_reset_notification
```

New intents currently use template revision `2` with plain-text + minimal robust HTML alternatives.

Auth/security tracking rules remain:

```text
open tracking OFF
click tracking OFF
link rewriting OFF
marketing content FORBIDDEN
```

## 8. Provider independence

Access/Auth code must never depend on SES SDK types, SMTP status syntax or provider-specific retry behavior.

The flow is:

```text
Auth lifecycle
→ shared durable EmailIntent
→ Email Platform worker
→ provider-neutral adapter
→ SES / SMTP last mile
```

Amazon SES API v2 is the accepted external provider adapter. SMTP remains a shared platform last-mile adapter for local/CI compatibility; there is no Access-owned process-memory SMTP queue in the canonical runtime.

## 9. Feedback integration

Provider feedback belongs to the Email Platform.

Access/Auth consumes only the resulting security-relevant projection where necessary. Current hard bounce/complaint handling can apply:

```text
EmailIdentity.recovery_restriction_code = provider_delivery_disabled
```

This does not redefine email verification or identity ownership. Reachability/provider suppression remains distinct from Auth identity truth.

Live AWS feedback-event ingress remains a production/deployment concern; the normalization/persistence/projection behavior is already covered by automated PostgreSQL acceptance.

## 10. Real Access/Auth consumer acceptance

Observed automated proof includes:

```text
signup challenge + EmailIntent commit together
EmailIntent staging failure rolls back signup challenge
recovery/reset intents follow canonical Auth mutations
resend/supersession behavior covered by platform tests
provider ambiguity does not create blind duplicate security mail
post-restore uncertain Auth email work is quarantined
```

Observed real SES UAT on 2026-09-03 proved:

```text
signup
→ DANTE creates signup state + EmailIntent
→ SES provider_accepted attempt 1
→ real mailbox receives verification mail
→ received OTP verifies successfully
→ Account created

password recovery
→ DANTE creates recovery state + EmailIntent
→ SES provider_accepted attempt 1
→ real mailbox receives recovery mail
→ recovery URL opens reset surface
→ password reset succeeds
→ no automatic login
→ previously authenticated AuthSession revoked

password reset notification
→ EmailIntent emitted
→ SES provider_accepted attempt 1
→ real mailbox receives security notification
```

Direct PostgreSQL inspection observed all three live intents as `provider_accepted`, all with one SES attempt, provider MessageId present, no error code and sensitive payload bundle wiped.

### Explicit non-claim

The exact same consumed recovery URL was not manually opened a second time in the final live UAT because the message had already been removed before that check. Do not label same-link replay rejection as manually observed in this final run.

## 11. Closure

For Access/Auth specifically:

```text
signup email integration                    ACCEPTED
password recovery email integration         ACCEPTED
password-reset notification integration     ACCEPTED
atomic Auth state + EmailIntent              ACCEPTED
real SES/mailbox UAT                         PASS
session revoke after reset                   PASS
no-auto-login after reset                    PASS

ACCESS/AUTH EMAIL CONSUMER INTEGRATION       CLOSED
```

This does not make production sender-domain/DNS/reputation deployment complete, and it does not make Access/Auth the owner of the shared Email Platform.

## 12. References

Shared platform:

```text
docs/architecture/email-platform.md
docs/development/email-platform-local-uat.md
docs/development/email-platform-acceptance-2026-09-03.md
```

Access/Auth architecture:

```text
docs/architecture/access-auth-architecture.md
docs/architecture/access-auth-security-contract.md
docs/architecture/access-auth-m4-contract.md
docs/architecture/access-auth-m5-contract.md
```

Decision/persistence:

```text
docs/decisions/ADR-012-email-delivery-platform.md
docs/database/access-auth.md
```
