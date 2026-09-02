# ADR-012: DANTE Email Delivery Platform

- **Status:** ACCEPTED ARCHITECTURAL DIRECTION ON `feature/access-auth` / PRIMARY PROVIDER TARGET SELECTED / IMPLEMENTATION + PROVIDER QUALIFICATION OPEN
- **Date:** 2026-09-02
- **Scope:** outbound transactional/security email lifecycle for Access/Auth and later first-party DANTE notifications
- **Detailed authority:** `../architecture/access-auth-email-delivery.md`
- **Consumes:** ADR-010 PostgreSQL Persistence Constitution, ADR-011 Access/Auth Architecture Constitution, TD-04 Class-A transactional-outbox direction
- **Active workstream:** `../workstreams/access-auth.md`

## Context

M3/M4 materialized a correct first executable email boundary for signup verification, provider mailbox verification, recovery and password-change notification:

```text
EmailDeliveryPort
→ typed email commands
→ bounded process-owned queue
→ fixed workers
→ SMTP dispatcher
```

That implementation is intentionally safe for the current product slice: bounded admission, no blind retry after ambiguous SMTP outcomes, shutdown drain, typed security messages and logs that omit OTP/recovery proof material.

It is not yet the final production email platform. A process-owned in-memory queue can lose an accepted email intent if the process terminates after the application transaction commits but before delivery becomes durable. SMTP success also does not represent recipient delivery, bounce, complaint or later suppression state.

The architecture question is therefore not “which SMTP vendor?”. It is:

```text
which lifecycle DANTE owns
vs
which last-mile delivery capability a specialist provider owns
```

## Decision

DANTE adopts this boundary:

```text
DANTE OWNS THE EMAIL LIFECYCLE.
A SPECIALIST PROVIDER OWNS LAST-MILE INTERNET DELIVERY.
```

DANTE will not operate a general-purpose production MTA/mail-server fleet as the default product architecture.

### Primary production target

Amazon SES API v2 is the selected **primary production delivery-adapter target**, subject to the remaining operational/provider qualification gate before production acceptance.

Preferred initial region target is `eu-south-1` (Europe/Milan) where Amazon SES exposes regional API/SMTP endpoints. Region selection does not by itself close privacy, retention, subprocessors or legal/compliance review; those remain explicit deployment gates.

Production integration should prefer the SES HTTP API through the AWS SDK over SMTP because it provides structured provider responses, message identifiers/tags/configuration sets and native IAM integration. SMTP remains a valid compatibility/UAT adapter, not the primary production contract.

### Provider-neutral application boundary

`EmailDeliveryPort` remains the application-facing abstraction. Domain/application code must not depend on SES SDK types, SMTP response syntax or provider-specific message IDs.

The target flow is:

```text
Auth / DANTE feature transaction
        │
        ▼
Email Intent
        │
        ▼
PostgreSQL Transactional Outbox
        │
        ▼
Email Worker / Delivery Orchestrator
        │
        ├── template + locale resolution
        ├── deterministic deduplication/idempotency
        ├── bounded claim/lease
        ├── retry/failure policy
        └── provider adapter
                 │
                 ▼
          Amazon SES API v2
                 │
                 ▼
        recipient mail infrastructure
                 │
                 ▼
 delivery/bounce/complaint/delay events
                 │
                 ▼
 Provider Event Ingestion
                 │
                 ▼
 DANTE delivery state / suppression / metrics
```

PostgreSQL remains canonical DANTE authority. SES is delivery infrastructure, not canonical lifecycle state.

## Durable outbox direction

Email becomes a Class-A durable-work consumer under TD-04.

The later exact persistence gate must materialize only the minimum schema required to represent concepts equivalent to:

```text
EmailIntent / OutboxItem
DeliveryAttempt
ProviderMessageRef
DeliveryEvent
RecipientSuppression / DeliveryRestriction
```

Those are conceptual responsibilities, not pre-authorized table names. Exact table/column/index/ACL design requires a separate reviewed persistence migration gate under ADR-010.

An email-producing application mutation must be able to commit the business/security effect and durable email intent atomically in PostgreSQL. A process crash after commit must not silently erase the intent.

## Sensitive Auth material

OTP codes and password-recovery bearer material are security secrets.

The durable design must not persist them indefinitely in clear text merely because an outbox exists.

Accepted direction:

```text
short TTL
minimum exposure
no secrets in logs/metrics/traces
no long-lived plaintext outbox payload
provider acceptance → erase no-longer-required sensitive delivery material
```

The exact implementation may use short-lived envelope encryption or another bounded design that preserves crash-safe delivery without turning PostgreSQL into a permanent plaintext recovery-secret archive. The implementation gate must prove the threat model and cleanup semantics.

## Retry / ambiguity / idempotency

Email sending is an external side effect. DANTE must distinguish:

```text
definitive pre-send/provider rejection
→ retry/failover may be allowed by policy

provider accepted with provider_message_id
→ do not send another copy merely because downstream delivery is pending

network timeout / ambiguous provider outcome
→ never blind-retry into duplicate OTP/recovery messages
→ reconcile when provider evidence permits
→ otherwise follow an explicit bounded ambiguous-outcome policy
```

Every durable email intent requires a stable DANTE non-secret reference usable for reconciliation and observability.

Provider failover is future capability, not automatic double-send. A secondary provider adapter may be added later only with deterministic routing, circuit-breaker policy and duplicate-prevention semantics.

## Feedback and suppression

Production acceptance requires normalized ingestion for at least:

```text
accepted/sent
delivered
delivery_delayed
bounced
complained
rejected
```

A hard bounce or complaint must be able to influence future DANTE delivery eligibility without redefining `EmailIdentity` as provider state. Current Access/Auth recovery-delivery restriction semantics are the integration point; the exact mapping requires the persistence/application implementation gate.

## Sender identity and reputation

Production Auth/security email requires a DANTE-owned authenticated domain/subdomain with:

```text
SPF
DKIM
DMARC
```

Auth/security traffic, ordinary product notifications and any future marketing traffic must be logically and operationally separable. They must not become one reputation pool merely for convenience.

For Auth/security messages:

```text
open tracking        OFF
click tracking       OFF
link rewriting       OFF
marketing content    FORBIDDEN
```

Configuration sets/event streams must preserve security-traffic isolation and privacy-minimized telemetry.

## Environment posture

```text
LOCAL automated tests
→ deterministic loopback SMTP capture

manual UAT
→ explicit real-provider adapter/config only when intentionally enabled

DEV/UAT/PROD
→ separate credentials/configuration/identities as appropriate
→ no secret in frontend/public runtime config
```

The opt-in real-SMTP tooling introduced at `9c0587af...` remains useful for UAT/provider qualification. It does not become production architecture by inertia.

## Authentication / IAM posture

When DANTE runs on AWS-capable infrastructure, production SES API authorization should prefer workload identity / IAM role with least privilege over long-lived SMTP passwords or static access keys.

The sending identity and allowed SES actions should be policy-bounded. Provider credentials never belong in Web/client configuration.

## Why SES is the primary target

The selection is architectural, not based on a temporary free allowance.

Relevant current evidence reviewed on 2026-09-02:

- Amazon SES exposes API v2 and regional endpoints, including Europe/Milan.
- SES configuration sets can publish delivery, bounce and complaint telemetry to AWS event destinations.
- IAM can restrict allowed SES actions and sender identities.
- Netflix publicly describes retiring its in-house delivery infrastructure for SES and separating transactional/marketing reputation pools.
- Fanatics publicly describes an internal scalable email platform using SES as delivery infrastructure while retaining application-side platform control and traffic segmentation.

Important pricing correction: the older SES-specific `3,000 message charges/month for the first 12 months` offer is no longer available to **new** customers as of July 21, 2026. Current new-account economics use AWS pricing plans / general AWS Free Tier credits. DANTE must therefore never encode the obsolete 3,000/month claim as a reason for this architecture.

## Rejected defaults

Not selected as the default architecture:

```text
self-hosted production SMTP/MTA fleet
SMTP transport as DANTE's canonical lifecycle authority
provider dashboard as canonical DANTE delivery state
in-memory queue as final durable production queue
blind retry after ambiguous send outcome
OTP/recovery secret in normal logs/traces
long-lived plaintext sensitive outbox payload
silent double-send provider failover
marketing + Auth/security reputation mixed by default
provider SDK types crossing into Domain/application contracts
```

Turnkey providers such as Postmark, Resend, Brevo or SendGrid remain possible future secondary adapters or evidence-based replacement candidates. They are not selected as canonical application architecture.

## Consequences

Positive:

```text
DANTE keeps provider portability and canonical lifecycle authority
crash-safe intent becomes possible through PostgreSQL outbox
provider delivery telemetry can become first-class operational evidence
Auth/security semantics stay independent of SMTP/provider implementation
IAM/workload identity fits future AWS deployment
traffic/reputation isolation is explicit
```

Costs:

```text
additional durable persistence and worker lifecycle
provider-event ingestion and verification
suppression/reconciliation policy
DNS/domain operations
observability/SLO work
provider-specific infrastructure adapter
more nuanced handling of ambiguous external side effects
```

Those costs are accepted because reliable password recovery/account-security email is a security-critical product capability, not incidental notification plumbing.

## Acceptance boundary

This ADR closes the **architecture direction**, not the implementation or production provider acceptance.

Still open:

```text
exact outbox/delivery persistence contract
SES account/sandbox/production-access qualification
exact IAM policy + credential posture for target deployment
sender domain/subdomain selection
SPF/DKIM/DMARC materialization and verification
SES API adapter implementation
provider event-ingestion implementation
suppression/restriction implementation
real Internet signup/recovery/reset-notification UAT
failure-injection / ambiguous-outcome proof
privacy/legal/subprocessor review
secondary-provider/failover decision
```

M5 must not claim real Internet email closure until the relevant bounded implementation and live delivery proof are complete.

## Reopen rule

Reopen the provider target or lifecycle split when concrete evidence shows SES, AWS deployment posture, privacy constraints, deliverability, cost, regulatory requirements or operational complexity cannot satisfy DANTE requirements without unacceptable coupling or risk.

A free-tier promotion, developer preference or vendor marketing alone is not reopen evidence.

## External references reviewed 2026-09-02

- AWS SES API sending: `https://docs.aws.amazon.com/ses/latest/dg/send-email-api.html`
- AWS SES endpoints/regions: `https://docs.aws.amazon.com/general/latest/gr/ses.html`
- AWS SES event publishing: `https://docs.aws.amazon.com/ses/latest/dg/monitor-using-event-publishing.html`
- AWS SES configuration sets: `https://docs.aws.amazon.com/ses/latest/dg/using-configuration-sets.html`
- AWS SES IAM: `https://docs.aws.amazon.com/ses/latest/dg/control-user-access.html`
- AWS SES pricing: `https://aws.amazon.com/ses/pricing/`
- AWS SES pricing-plan change: `https://aws.amazon.com/blogs/messaging-and-targeting/introducing-amazon-simple-email-service-ses-pricing-plans/`
- Netflix SES case study: `https://aws.amazon.com/ses/netflix-ses-case-study/`
- Fanatics SES platform case study: `https://aws.amazon.com/blogs/messaging-and-targeting/how-fanatics-commerce-built-a-scalable-email-platform-on-amazon-ses/`
