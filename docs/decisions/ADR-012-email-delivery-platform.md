# ADR-012: DANTE Email Delivery Platform

- **Status:** ACCEPTED ARCHITECTURE / IMPLEMENTED / SHARED-OWNERSHIP VERIFIED
- **Date:** 2026-09-02
- **Last reconciled:** 2026-09-04
- **Scope:** reusable outbound DANTE Email Platform; Access/Auth is the first consumer
- **Detailed authority:** `../architecture/email-platform.md`
- **Access/Auth consumer contract:** `../architecture/access-auth-email-delivery.md`
- **Accepted real-provider evidence:** `../development/email-platform-acceptance-2026-09-03.md`
- **Accepted integration-candidate proof HEAD:** `81639c61478b476c995652d0060dde8f53aef089`
- **Consumes:** ADR-010 PostgreSQL Persistence Constitution, ADR-011 Access/Auth Architecture Constitution, TD-04 Class-A transactional-outbox direction

## Context

The original Access/Auth email slice established typed security messages and bounded SMTP delivery, but process-owned queued work could not provide the required Class-A durability between canonical commit and external delivery.

The architectural question is therefore not which mail vendor DANTE uses. It is which lifecycle facts DANTE owns and which last-mile capability belongs to a specialist provider.

Security-critical delivery requires:

```text
durable intent
transactional coordination with caller state
explicit idempotency
bounded claim ownership
explicit uncertainty
no blind retry after ambiguous external effect
short-lived secret protection
provider correlation/feedback
suppression
operational observability
```

## Decision

DANTE adopts the permanent split:

```text
CONSUMER OWNS MESSAGE MEANING.
DANTE SHARED EMAIL PLATFORM OWNS DELIVERY LIFECYCLE.
SPECIALIST PROVIDER OWNS LAST-MILE INTERNET TRANSPORT.
```

The reusable boundary is:

```text
consumer application transaction
        │
        ├── canonical feature/security mutation
        └── typed consumer email intent semantics
                 │
                 ▼
          shared durable EmailIntent
                 │
                 ▼
          PostgreSQL COMMIT
                 │
                 ▼
        shared claim/lease worker
                 │
                 ├── protected payload
                 ├── injected consumer renderer port
                 ├── retry/ambiguity policy
                 └── provider-neutral adapter
                          │
                          ├── Amazon SES API v2
                          └── SMTP local/CI adapter
                                   │
                                   ▼
                           recipient infrastructure
                                   │
                                   ▼
                       provider feedback/events
                                   │
                                   ▼
                    shared suppression/evidence
                                   │
                                   └── optional typed consumer projection
```

PostgreSQL remains canonical DANTE authority. Provider dashboards/event stores are external evidence, not canonical delivery lifecycle state.

## Shared platform ownership

Reusable implementation belongs under:

```text
dante.platform.email
```

The shared package owns:

```text
provider-neutral contracts
payload crypto/fingerprint mechanics
durable outbox lifecycle
claim / lease / attempt state
retry / ambiguity policy
renderer port orchestration
SES / SMTP adapters
provider feedback persistence
recipient suppression
privacy-minimized observability
process runtime composition
```

It must not import `dante.auth` or another consumer package.

A repository architecture test enforces this dependency direction.

## Consumer ownership

A consumer owns:

```text
whether delivery should occur
semantic purpose
stream identity
recipient decision
consumer template identity/revision policy
actual message copy / text / HTML rendering
operation-specific idempotency and supersession inputs
expiry and preference/consent semantics
consumer-owned projections resulting from delivery evidence
```

Current Access/Auth owns the `auth_security` stream and its four security-message purposes/templates. The shared platform does not hardcode Auth copy or rendering.

Future Account/reminder/workflow/report consumers reuse shared mechanics and provide their own typed renderer/integration rather than creating another mail subsystem.

## Durable persistence

Current shared persistence:

```text
dante.email_delivery_intent
dante.email_delivery_attempt
dante.email_provider_event
dante.email_recipient_suppression
```

Migration history:

```text
20260903_14  first durable Email Platform materialization
20260903_15  exact runtime ACL hardening
20260904_16  forward hardening from Auth-only stream/purpose CHECKs to governed shared identifiers
```

Revisions 14 and 15 remain immutable historical evidence. Revision 16 is a normal forward correction; it does not rewrite the prior graph.

The two vocabulary checks remain bounded technical identifiers rather than unrestricted semantic payloads:

```text
lowercase ASCII identifier
starts with a letter
letters / digits / underscore only
maximum length 64
```

Consumer code remains responsible for its exact typed vocabulary. This preserves shared persistence without turning the platform into a generic event/property-bag system.

## Transactional coordination

If a consumer mutation requires durable email, canonical mutation + EmailIntent are committed atomically in one PostgreSQL transaction.

External provider I/O occurs only after commit.

```text
canonical mutation + external intent  → same DB transaction
external network effect               → after commit
```

This is the accepted Class-A side-effect boundary.

## Idempotency

Reservation identity is:

```text
operation_scope + idempotency_key
```

A same-key replay is accepted only when the existing intent matches the full immutable non-temporal delivery identity:

```text
purpose
stream
recipient address + comparison key
template code + revision
locale
supersession key
protected semantic payload fingerprint
```

Therefore:

```text
same scope/key + same immutable work       → replay existing intent
same scope/key + different immutable work  → conflict / fail closed
```

The keyed payload fingerprint protects equality of secret-bearing consumer payload. It is not the sole idempotency comparison.

## Claim, retry and ambiguity

Workers use bounded batches, `FOR UPDATE SKIP LOCKED`, exact claim tokens and leases.

Provider I/O occurs outside PostgreSQL transactions; finalization requires exact still-owned claim identity.

Normalized outcomes:

```text
provider_accepted
retryable_failure
ambiguous
definitive_failure
```

Permanent rule:

```text
ambiguous external effect → never blind retry
```

An expired in-flight lease is also conservative uncertainty, not proof that nothing was sent.

## Sensitive material

OTP/recovery payload material is protected with:

```text
AES-256-GCM dedicated Email Platform key ring
random nonce
AAD binding intent + purpose + template + revision
keyed immutable payload fingerprint
terminal/unsafe-state wipe
```

The key ring is separate from Auth password peppers, OTP HMAC keys, CSRF keys and Apple-grant encryption keys.

No secret belongs in logs, metrics, traces or provider tags.

## Primary external adapter

Amazon SES API v2 remains the selected primary external adapter.

Accepted properties:

```text
region-bound boto3 Session
structured provider response
provider MessageId required for acceptance
intent + stream tags
optional configuration set
standard AWS credential provider chain
one deliberate SDK wire attempt
```

DANTE owns retry policy rather than allowing hidden provider-SDK retry to duplicate security mail.

SMTP remains a shared local/CI/generic compatibility adapter behind the same durable lifecycle; it is not another process queue.

## Provider acceptance vs delivery

Permanent distinction:

```text
provider_accepted != mailbox delivered
```

Provider acceptance requires an explicit provider MessageId when the provider supplies one. Mailbox receipt/provider feedback is separate evidence.

## Feedback and suppression

Shared feedback currently normalizes SES:

```text
Delivery
DeliveryDelay
Bounce
Complaint
Reject
```

Provider events are persisted idempotently. Strong bounce/complaint evidence can update shared recipient suppression.

Consumer-owned consequences are applied through typed projection ports. For Access/Auth, the Auth projection may restrict recovery delivery on the matching EmailIdentity. Shared feedback code must not import or mutate Auth persistence directly.

Live cloud feedback ingress remains a production deployment concern; normalization/persistence behavior is executable application code.

## Environment / credential posture

Real-provider UAT used a dedicated non-root IAM principal with temporary browser-login credentials in `eu-west-3`.

That is UAT evidence, not permanent production topology.

Production should use workload identity/IAM role and a DANTE-controlled authenticated sender domain/subdomain with appropriate:

```text
SPF
DKIM
DMARC
quota/reputation controls
provider feedback routing
operational alerting
```

## Configuration compatibility boundary

During the first-consumer Access/Auth integration, concrete Email Platform fields remain carried inside the existing `AuthSettings` / `DANTE_AUTH__...` environment envelope.

The shared platform itself consumes only the read-only structural `EmailPlatformSettings` protocol and does not import `AuthSettings`.

This nesting is a compatibility carrier, not ownership. A later top-level `Settings.email` namespace migration is justified when independent multi-consumer/deployment composition requires it and must be performed as an explicit validated configuration migration.

## Explicit non-goals

The Email Platform is not:

```text
a universal semantic event bus
a generic JSON "send anything" API
an EAV/property-bag store
a marketing authorization mechanism
a provider dashboard as canonical state
a place for feature business state
```

Marketing/newsletter traffic requires separate product/legal/reputation policy and should remain operationally isolated from security traffic.

## Evidence status

The accepted 2026-09-03 baseline and real SES UAT proved the original durable platform behavior, including real signup/recovery/reset-notification delivery, session revocation and terminal secret wipe.

The later 2026-09-04 shared-ownership refactor changed code organization, separated consumer rendering/projection, hardened replay identity and introduced forward migration `20260904_16` without intentionally changing user-visible delivery semantics.

Current truth on exact proof HEAD `81639c61478b476c995652d0060dde8f53aef089`:

```text
architecture decision                         ACCEPTED
2026-09-03 real-provider UAT                  ACCEPTED HISTORICAL EVIDENCE
shared ownership refactor                     VERIFIED / ACCEPTED
forward shared-vocabulary migration 16        PG PROVEN / ACCEPTED
backend static + fast regression              PASS
real PostgreSQL acceptance                    PASS
combined Backend CI                           PASS
combined Frontend CI                          PASS
CP07 enriched-baseline LOCAL recovery         PASS
```

The post-refactor focused regression gate is no longer pending. The 2026-09-03 SES run remains the real-provider evidence; this ADR does not pretend the real-provider UAT was rerun after each structural refactor commit.

Production sender/domain/DNS/reputation/workload-identity and live feedback ingress remain separate deployment gates.

## Consequences

Positive:

```text
one reusable delivery lifecycle
crash-safe admitted work
explicit uncertainty
no hidden provider retry authority
consumer-specific rendering without shared back-dependencies
future consumers do not rebuild SES/SMTP/outbox/feedback machinery
persistence is no longer falsely Auth-only
```

Costs:

```text
more explicit consumer integration
consumer renderer/version governance required
provider feedback ingress still needs deployment wiring
production sender/reputation operations remain real operational work
```

## Reopen rule

Reopen this architecture only on concrete evidence that the shared lifecycle cannot preserve DANTE correctness/security/operational requirements.

Do not reopen it merely to simplify one consumer, move logic back under Auth, introduce a generic event bag, or substitute a provider SDK/dashboard for canonical lifecycle state.
