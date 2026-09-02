# DANTE — Access/Auth Email Delivery Architecture

- **Status:** CURRENT / AUTHORITATIVE TARGET FOR `feature/access-auth` / NOT YET MATERIALIZED AS PRODUCTION EMAIL PLATFORM
- **Last reconciled:** 2026-09-02
- **Decision authority:** `../decisions/ADR-012-email-delivery-platform.md`
- **Consumes:** Access/Auth architecture/security contracts, ADR-010 PostgreSQL constitution, TD-04 Class-A durable work
- **Current implementation:** `apps/backend/src/dante/auth/email_delivery.py`
- **Current UAT tooling:** `tooling/serve-access-auth-local-uat.py`

## 1. Purpose

This document defines the current target architecture for DANTE outbound transactional/security email.

It separates three things that must not be conflated:

```text
1. application/security intent
2. DANTE-owned durable lifecycle + delivery state
3. external last-mile Internet delivery
```

The guiding rule is:

```text
DANTE owns the email lifecycle.
A specialist provider owns last-mile delivery.
```

The current SMTP dispatcher is a valid implementation slice and UAT adapter. It is not the final production authority.

## 2. Current versus target

Current executable path:

```text
Auth command
→ EmailDeliveryPort
→ typed EmailCommand
→ bounded asyncio.Queue
→ fixed SmtpEmailDispatcher workers
→ SMTP
```

Current strengths:

```text
typed signup/provider/recovery/reset-notification messages
bounded queue capacity
fixed worker count
no blind transport retry
bounded shutdown drain
TLS/STARTTLS/plain transport configuration
optional SMTP authentication
no OTP/recovery material in normal logs
neutral/no-op recovery work to preserve public response posture
```

Current limitation:

```text
process-owned queue != durable accepted email intent
SMTP send success != delivered inbox state
no durable provider message reference
no durable attempt/event history
no bounce/complaint ingestion
no suppression lifecycle
no production reputation segmentation
```

Target path:

```text
Application mutation
        │
        ├── canonical business/security state
        └── durable Email Intent
                 │
                 ▼
          PostgreSQL COMMIT
                 │
                 ▼
         Outbox claim / lease
                 │
                 ▼
      Email Delivery Orchestrator
                 │
                 ├── template/locale
                 ├── priority/stream
                 ├── deduplication
                 ├── bounded retry policy
                 └── provider adapter
                          │
                          ▼
                    Amazon SES API v2
                          │
                          ▼
                     Internet mail
                          │
                          ▼
           delivery/bounce/complaint events
                          │
                          ▼
             Event ingestion / normalization
                          │
                          ▼
        Delivery state / suppression / metrics
```

## 3. Application boundary

`EmailDeliveryPort` remains the application-facing delivery abstraction.

Feature/application code may express intents such as:

```text
signup mailbox verification
provider-enrollment mailbox verification
password recovery
password-reset security notification
future login/security event notification
future first-party DANTE notification
```

Feature/application code must not know:

```text
SES boto3/client types
SMTP response codes
AWS configuration-set names
provider message-ID wire formats
SNS/EventBridge envelopes
provider dashboards
```

Provider-specific translation remains behind infrastructure/platform adapters.

## 4. Durable lifecycle model

The exact physical schema is **not yet authorized**. A later persistence design gate must define exact tables/columns/indexes/ACLs under ADR-010.

The target logical responsibilities are:

### Email Intent / Outbox

Represents a durable DANTE decision that an email should be attempted.

Minimum semantics:

```text
stable DANTE email-intent reference
purpose / stream
recipient identity reference or bounded destination snapshot
locale/template revision
created/eligible/expiry time
delivery state
claim/lease ownership
attempt budget
idempotency/deduplication identity
security-sensitive payload handling metadata
```

### Delivery Attempt

Represents one provider-send attempt without pretending ambiguous outcomes are definitive.

Minimum semantics:

```text
attempt number
provider code
attempt timestamps
result classification
provider message reference when accepted
retry/failover eligibility
error class/code safe for operations
no OTP/recovery secret in observability fields
```

### Provider Delivery Event

Normalizes provider feedback into DANTE semantics:

```text
accepted/sent
delivered
delivery_delayed
bounced
complained
rejected
```

Raw provider payload retention, if any, requires an explicit privacy/retention decision and must not become normal canonical product state by default.

### Recipient Suppression / Delivery Restriction

Represents current operational eligibility to send to a mailbox without redefining identity ownership.

A bounce/complaint restriction is not the same semantic as:

```text
EmailIdentity removed
Account disabled
provider identity revoked
mailbox ownership historically unverified
```

Current Access/Auth `recovery_restriction_code` direction is a natural integration point; exact extension requires the later persistence/application gate.

## 5. Transactional outbox rules

Email is a Class-A durable side effect.

When an application operation requires an email because of a committed security/business effect, the durable intent must be written in the same PostgreSQL transaction as the state that requires it whenever atomicity is semantically required.

Required property:

```text
business/security COMMIT succeeded
→ intended email work is durably represented
```

Forbidden final-production pattern:

```text
COMMIT
→ process crashes
→ required email intent disappears because it existed only in RAM
```

Worker processing should use bounded PostgreSQL claim/lease semantics suitable for queue work. `SKIP LOCKED` may be appropriate for outbox worker contention because this is work claiming, not an Account-security invariant. Exact claim/recovery semantics must be designed and tested, not copied mechanically.

## 6. Delivery state machine direction

A target state model should distinguish at least:

```text
pending
claimed
provider_accepted
retryable_failure
definitive_failure
delivered
delayed
bounced
complained
expired/cancelled
```

Exact names are not frozen here.

Important rule:

```text
provider_accepted != delivered
```

and:

```text
HTTP/SMTP timeout != definitely not sent
```

The state machine must preserve uncertainty rather than collapsing it into false success/failure.

## 7. Idempotency and ambiguous outcomes

Every email intent receives a stable DANTE reference before external I/O.

Retry policy depends on outcome class.

### Safe retry class

Examples:

```text
local validation failed before provider call
provider definitively rejected request before acceptance
provider returns explicit throttling/transient failure with no acceptance
```

A bounded retry with backoff may be allowed.

### Accepted class

Provider returns a provider message reference/acceptance.

```text
record acceptance
wait for delivery feedback
never send a second message merely because delivery feedback is not immediate
```

### Ambiguous class

Network failure/timeout occurs after request transmission and DANTE cannot prove whether provider accepted it.

```text
NO blind immediate retry
preserve ambiguous state
reconcile through provider evidence when supported
otherwise apply explicit purpose-specific policy
```

Recovery/OTP duplication can cause user confusion and security ambiguity; “retry everything” is rejected.

## 8. Sensitive Auth payload policy

Security-sensitive payload includes:

```text
signup OTP
provider-enrollment OTP
password-recovery bearer secret
other future short-lived account-recovery proof
```

It must never appear in:

```text
normal application logs
metrics labels
traces
provider tags
long-lived plaintext operational history
error reporting payloads
```

A durable outbox cannot justify indefinite plaintext secret retention.

Implementation gate must choose and prove a bounded scheme such as short-lived envelope encryption or equivalent protection with:

```text
purpose-separated key material
short TTL
least-readable scope
deletion/cryptographic erasure after provider acceptance or expiry
no frontend exposure
no accidental dump/telemetry propagation
```

## 9. Template and localization ownership

DANTE owns message semantics, templates and locale selection.

Provider-hosted templates may be used only if they do not make the provider the canonical source of security copy/versioning.

Preferred baseline:

```text
repository-reviewed DANTE template/content revision
→ application delivery model
→ provider adapter
```

Security messages remain minimal and purpose-specific.

Auth email must not contain marketing content.

## 10. Primary provider target — Amazon SES

Selected target:

```text
Amazon SES API v2
preferred initial region: eu-south-1 Europe/Milan
```

The provider target remains **not production accepted** until account/sandbox/domain/IAM/live-delivery qualification is complete.

Reasons for API preference over SMTP in production:

```text
structured provider response
provider message IDs
message tags/configuration sets
native AWS SDK integration
IAM least-privilege/workload identity
provider event-publishing integration
cleaner operational error classification
```

SMTP remains supported for deterministic local capture, manual provider/UAT compatibility and fallback use cases that are explicitly designed.

## 11. IAM / credentials

Production DANTE should prefer workload identity / IAM role where deployment permits.

Avoid defaulting to long-lived SMTP credentials or static AWS access keys.

Least-privilege policy should restrict:

```text
SES send actions required by the adapter
approved From identity/domain
approved configuration set where appropriate
region/account scope where practical
```

Provider credentials never enter public Web/mobile runtime configuration.

## 12. Provider events

SES event publishing supports operational feedback including delivery, bounce, complaint and delay classes.

DANTE must normalize external event envelopes before they reach application policy.

Target boundary:

```text
AWS event transport
→ provider event verifier/parser
→ normalized DANTE delivery event
→ idempotent persistence/application update
```

Duplicate provider events must be tolerated. Event order must not be assumed to equal semantic lifecycle order without evidence.

Event ingestion must have:

```text
authenticity/integrity validation appropriate to transport
idempotent event identity or equivalent deduplication
bounded payload size
schema/version handling
safe unknown-event policy
privacy-minimized logging
```

## 13. Suppression and mailbox health

Hard bounce and complaint are not ordinary transient errors.

Target policy must support:

```text
hard bounce → delivery restriction/suppression
complaint   → delivery restriction/suppression
temporary delay → provider/worker monitoring, not immediate permanent invalidation
```

Re-enabling a suppressed mailbox requires an explicit evidence-based policy. Do not silently clear suppression because a later feature “needs to send”.

Provider global suppression lists are useful infrastructure but do not replace DANTE-owned canonical restriction reasoning when product/security behavior depends on it.

## 14. DNS and sender authentication

Production sender must use a DANTE-owned verified domain/subdomain.

Required baseline:

```text
SPF
DKIM
DMARC
```

Exact domain naming is not frozen yet. A likely separation is conceptually:

```text
security/auth stream
product notification stream
future marketing stream
```

The design must preserve the ability to isolate reputation and operational policy.

Production recovery/signup must not originate from a personal Gmail/Hotmail mailbox.

## 15. Tracking posture

For Auth/security email:

```text
open tracking    OFF
click tracking   OFF
link rewriting   OFF
marketing pixels OFF
```

Security mail requires deliverability/operational telemetry, not engagement surveillance.

If provider defaults enable tracking, the DANTE security configuration must explicitly override them.

## 16. Traffic/reputation segmentation

Different traffic classes carry different complaint/reputation risk.

Do not mix by default:

```text
password reset / account security
routine product notifications
future marketing/bulk campaigns
```

Netflix's public SES case study explicitly separates traffic/reputation pools. Fanatics publicly describes granular transactional/marketing segmentation. These are directional external evidence, not claims that DANTE must copy their internal topology.

At DANTE's early volume, separate dedicated IP pools are not automatically required. Logical/configuration-set/domain-stream separation should exist first; dedicated-IP decisions require later volume/deliverability evidence.

## 17. Provider failover

Secondary-provider support is a future capability.

The architecture remains provider-neutral so an adapter for Postmark, Resend, Brevo, SendGrid or another provider can be added if justified.

Failover is **not**:

```text
SES uncertain → send same recovery email through provider B immediately
```

Allowed failover requires proof that the primary did not accept, or a purpose-specific policy that safely handles uncertainty.

Circuit breaker, provider health and routing policy are application/infrastructure decisions owned by DANTE.

## 18. DEV/UAT/PROD separation

Automated tests:

```text
loopback SMTP capture
no Internet dependency
protocol/delivery semantics deterministic
```

Manual UAT:

```text
explicit opt-in real SMTP/provider config
real inbox proof where required
no secret committed to repository
```

Production:

```text
verified DANTE sender identity
provider API adapter
workload identity/secret governance
feedback event path
observability/suppression
```

Environment is not Git branch.

## 19. Observability / SLO direction

DANTE needs operational visibility into at least:

```text
outbox backlog/age
claim/processing latency
provider acceptance latency
provider rejection rate
delivery latency
bounce rate
complaint rate
delayed delivery rate
suppression count
ambiguous send outcomes
worker/provider circuit state
```

Do not put raw recipient address, OTP or recovery secret into high-cardinality metrics labels.

Use stable internal references/request correlation where needed.

Potential later SLOs should distinguish:

```text
DANTE accepted email intent
provider accepted message
recipient server accepted delivery
```

Those are different boundaries.

## 20. Failure modes to prove before production closure

The final implementation must test at least:

```text
process crash after DB COMMIT before worker sees intent
worker crash after claim
claim lease expiry/recovery
provider deterministic rejection
provider throttle/transient failure
network timeout/ambiguous send
provider accepted but feedback delayed
hard bounce
complaint
duplicate provider event
out-of-order provider event
suppressed recipient
expired OTP/recovery before delivery
shutdown with queued/claimed work
provider credentials revoked
DNS/sender identity invalid
```

No production PASS is valid without proving the relevant failure model.

## 21. Current live state

As of 2026-09-02:

```text
EmailDeliveryPort                         IMPLEMENTED
SmtpEmailDispatcher                      IMPLEMENTED
bounded process queue                    IMPLEMENTED
no blind SMTP retry                      IMPLEMENTED
loopback SMTP capture                    IMPLEMENTED / CI
opt-in real SMTP local-UAT config         IMPLEMENTED at 9c0587af...

transactional email outbox               NOT MATERIALIZED
production SES API adapter               NOT MATERIALIZED
provider message state                   NOT MATERIALIZED
feedback event ingestion                 NOT MATERIALIZED
suppression management                   NOT MATERIALIZED
sender DNS/domain                        NOT MATERIALIZED
real Internet signup/recovery UAT         OPEN
```

Do not mislabel the existing SMTP path as the completed production Email Platform.

## 22. Current next gate

Before writing the production implementation, perform a bounded operational/provider qualification covering:

```text
AWS/SES account creation and billing posture
SES sandbox vs production access
Milan region exact capability/quotas
verified identity/domain setup
DKIM/SPF/DMARC mechanics
IAM/workload identity
API v2 SDK/runtime choice
configuration-set/event-destination design
SNS/EventBridge ingestion boundary
provider retention/privacy/subprocessor review
cost at DANTE expected volumes
local DEV/UAT strategy
exact outbox + sensitive-payload design
```

Then freeze the exact persistence/implementation slice and implement it under normal PRE-SCOPE/write/race/post-scope gates.

## 23. Current external evidence

Reviewed 2026-09-02:

- AWS SES API sending — `https://docs.aws.amazon.com/ses/latest/dg/send-email-api.html`
- AWS SES endpoints — `https://docs.aws.amazon.com/general/latest/gr/ses.html`
- AWS SES event publishing — `https://docs.aws.amazon.com/ses/latest/dg/monitor-using-event-publishing.html`
- AWS SES configuration sets — `https://docs.aws.amazon.com/ses/latest/dg/using-configuration-sets.html`
- AWS SES IAM — `https://docs.aws.amazon.com/ses/latest/dg/control-user-access.html`
- AWS SES pricing — `https://aws.amazon.com/ses/pricing/`
- AWS SES pricing-plan update — `https://aws.amazon.com/blogs/messaging-and-targeting/introducing-amazon-simple-email-service-ses-pricing-plans/`
- Netflix SES case study — `https://aws.amazon.com/ses/netflix-ses-case-study/`
- Fanatics SES platform case study — `https://aws.amazon.com/blogs/messaging-and-targeting/how-fanatics-commerce-built-a-scalable-email-platform-on-amazon-ses/`

The old SES-specific 3,000-message/month first-year free-tier claim is not current for new customers after July 21, 2026. Provider economics must use current pricing at the time of deployment.
