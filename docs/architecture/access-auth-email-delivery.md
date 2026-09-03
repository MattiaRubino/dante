# DANTE — Access/Auth Integration with the Email Platform

- **Status:** CURRENT / ACCESS-AUTH CONSUMER INTEGRATION CONTRACT FOR `feature/access-auth`
- **Last reconciled:** 2026-09-03
- **Platform authority:** `email-platform.md`
- **Decision authority:** `../decisions/ADR-012-email-delivery-platform.md`

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

Amazon SES API v2 is the selected external provider adapter for real UAT/production direction. SMTP remains a shared platform last-mile adapter for local/CI compatibility; there is no Access-owned process-memory SMTP queue in the canonical runtime.

## 9. Feedback integration

Provider feedback belongs to the Email Platform.

Access/Auth consumes only the resulting security-relevant projection where necessary. Current hard bounce/complaint handling can apply:

```text
EmailIdentity.recovery_restriction_code = provider_delivery_disabled
```

This does not redefine email verification or identity ownership. Reachability/provider suppression remains distinct from Auth identity truth.

## 10. Current proof

Observed automated proof includes:

```text
signup challenge + EmailIntent commit together
EmailIntent staging failure rolls back signup challenge
recovery/reset intents follow canonical Auth mutations
resend/supersession behavior covered by platform tests
provider ambiguity does not create blind duplicate security mail
post-restore uncertain Auth email work is quarantined
```

The remaining external acceptance gate is real DANTE-originated delivery for signup and password recovery through SES to the UAT mailbox.

## 11. References

Shared platform:

```text
docs/architecture/email-platform.md
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
