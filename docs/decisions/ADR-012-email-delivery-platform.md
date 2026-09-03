# ADR-012: DANTE Email Delivery Platform

- **Status:** ACCEPTED / IMPLEMENTED / REAL-PROVIDER UAT ACCEPTED ON `feature/access-auth`
- **Date:** 2026-09-02
- **Last reconciled:** 2026-09-03
- **Scope:** reusable outbound DANTE Email Platform; Access/Auth is the first consumer
- **Detailed platform authority:** `../architecture/email-platform.md`
- **Access/Auth consumer contract:** `../architecture/access-auth-email-delivery.md`
- **Real-provider evidence:** `../development/email-platform-acceptance-2026-09-03.md`
- **Consumes:** ADR-010 PostgreSQL Persistence Constitution, ADR-011 Access/Auth Architecture Constitution, TD-04 Class-A transactional-outbox direction

## Context

The original M3/M4 email boundary used typed delivery commands and bounded SMTP tooling. That was sufficient to establish application semantics, but not sufficient as the final reliability boundary because process-owned queued work can be lost between application commit and external send.

The architecture question is therefore not “which SMTP vendor?”. It is:

```text
which lifecycle DANTE owns
vs
which last-mile delivery capability a specialist provider owns
```

Security-critical messages such as signup verification and password recovery require durable coordination, explicit ambiguity handling, bounded retries, secret minimization and provider feedback without turning provider infrastructure into DANTE canonical state.

## Decision

DANTE adopts this permanent split:

```text
DANTE OWNS THE EMAIL LIFECYCLE.
A SPECIALIST PROVIDER OWNS LAST-MILE INTERNET DELIVERY.
```

DANTE will not operate a general-purpose production MTA/mail-server fleet as the default architecture.

The reusable platform boundary is:

```text
DANTE feature/application transaction
        │
        ├── canonical mutation
        └── durable EmailIntent
                 │
                 ▼
          PostgreSQL COMMIT
                 │
                 ▼
       transactional outbox worker
                 │
                 ├── claim/lease
                 ├── protected payload
                 ├── rendering
                 ├── bounded retry/ambiguity policy
                 └── provider-neutral adapter
                          │
                          ├── Amazon SES API v2
                          └── SMTP local/CI compatibility adapter
                                   │
                                   ▼
                         recipient infrastructure
                                   │
                                   ▼
                         provider feedback/events
                                   │
                                   ▼
                     DANTE event/suppression state
```

PostgreSQL remains canonical DANTE authority. Provider dashboards and provider event stores are external evidence, not canonical lifecycle state.

## Platform ownership

The Email Platform is shared DANTE infrastructure.

```text
Email Platform = reusable technical delivery subsystem
Access/Auth     = first consumer
```

Access/Auth does not own provider clients, retry machinery, durable worker semantics, provider-event persistence, suppression infrastructure or shared email observability.

Future Account, reminder, workflow, digest or report consumers reuse the same platform and define their own semantic trigger/purpose/template/idempotency/preference policy.

The platform must not become a generic semantic event bus or an EAV/property-bag escape hatch.

## Primary external adapter

Amazon SES API v2 is the selected primary external delivery adapter.

DANTE prefers the SES HTTPS API through the AWS SDK over SES SMTP because it provides structured responses, provider MessageId, tags/configuration sets and native IAM integration while preserving a provider-neutral application boundary.

SMTP remains a valid local/CI/generic-provider compatibility adapter behind the same durable outbox. It is not a separate canonical queue and not the production lifecycle authority.

### Region posture

SES region is explicit configuration, not a semantic constant.

The accepted real-provider UAT was executed in:

```text
eu-west-3 / Europe (Paris)
```

No document should imply that `eu-south-1`/Milan is the permanent production region. Final production-region selection is a deployment decision constrained by current SES capability, account posture, legal/privacy requirements, quotas, latency and operations.

## Durable persistence

The exact accepted persistence is materialized through:

```text
dante.email_delivery_intent
dante.email_delivery_attempt
dante.email_provider_event
dante.email_recipient_suppression
```

Alembic authority:

```text
20260903_14  durable Email Platform persistence
20260903_15  exact runtime ACL hardening
```

These tables are bounded technical delivery structures, not new semantic Domain owners and not DANTE MaterialState.

An email-producing application mutation must commit the feature/security mutation and EmailIntent atomically in PostgreSQL. Provider network I/O occurs only after commit.

## Idempotency, claim and concurrency

Each durable intent uses:

```text
operation_scope
+
idempotency_key
+
immutable payload fingerprint
```

A replay with identical semantic payload resolves to the existing intent. Same idempotency identity with different payload fails closed.

Workers use bounded claim/lease ownership and `FOR UPDATE SKIP LOCKED`. Provider I/O occurs outside database transactions, and finalization requires exact claim ownership.

## Sensitive material

OTP codes and password-recovery bearer material are security secrets.

Accepted protection:

```text
AES-256-GCM dedicated Email Platform key ring
random nonce
AAD binds intent + purpose + template + revision
short-lived protected payload
terminal/unsafe-state wipe
no secret in logs/metrics/traces/provider tags
```

The Email Platform key ring is separate from password peppers, signup OTP HMAC keys, CSRF keys and Apple-grant encryption keys.

Real UAT direct PostgreSQL inspection proved that protected payload columns were wiped after provider acceptance for signup, password recovery and reset notification.

## Provider retry / ambiguity doctrine

Email sending is an external side effect. DANTE distinguishes:

```text
known retryable pre-acceptance/service condition
→ bounded DANTE retry may be allowed

known definitive rejection
→ terminal definitive failure

provider success + MessageId
→ provider_accepted
→ no duplicate send merely because downstream delivery is unknown

network timeout / connection loss / uncertain provider result
→ ambiguous
→ never blind retry
```

SES SDK retry configuration is deliberately bounded to one total wire attempt. DANTE owns retry policy.

The first real SES UAT exposed a Botocore temporary-credential refresh region defect. The resulting send was correctly classified `ambiguous` rather than blindly retried. The adapter was fixed to create a region-bound boto3 Session and a focused unit test now guards that behavior.

## Provider acceptance vs delivery

Permanent distinction:

```text
provider_accepted != delivered to mailbox
```

Provider acceptance requires a provider MessageId.

Mailbox receipt is a separate UAT/operational observation. Provider delivery events may later provide additional asynchronous evidence.

## Feedback and suppression

The platform normalizes at least:

```text
Delivery
DeliveryDelay
Bounce
Complaint
Reject
```

Provider events are persisted idempotently. Permanent bounce and complaint can project recipient suppression and security-relevant reachability restrictions without redefining `EmailIdentity` verification/ownership truth.

Live cloud feedback ingress was not part of the final real-provider UAT. The normalization/persistence/suppression implementation is accepted through automated PostgreSQL proof; cloud event routing is a production deployment gate.

## Sender identity and reputation

Production Auth/security email requires a DANTE-controlled authenticated domain/subdomain with operational DNS/reputation posture including:

```text
SPF
DKIM
DMARC
```

Auth/security traffic, ordinary product notifications and any future marketing traffic must remain logically and operationally separable.

For Auth/security messages:

```text
open tracking        OFF
click tracking       OFF
link rewriting       OFF
marketing content    FORBIDDEN
```

The final local UAT used a verified mailbox identity, not the future production DANTE domain. Mail landing in spam/junk during that UAT therefore does not close or fail production deliverability.

## Environment posture

```text
LOCAL/CI automated tests
→ deterministic local provider/capture + PostgreSQL

manual real-provider UAT
→ explicit SES opt-in
→ disposable PostgreSQL 18.6
→ dedicated non-root IAM principal
→ temporary aws login credentials

PRODUCTION
→ workload identity / IAM role preferred
→ DANTE-controlled sender/domain
→ provider event routing + operations
```

No provider credential belongs in frontend/public runtime or repository configuration.

## Local UAT IAM decision

For reproducible local SES UAT the accepted topology is:

```text
IAM user:   dante-uat
IAM group:  dante-local-uat
no Access Key
browser-based aws login temporary credentials
```

Group policies:

```text
SignInLocalDevelopmentAccess
DanteUatSesVerifiedIdentity
```

The custom SES policy grants only:

```text
ses:GetEmailIdentity
ses:SendEmail
```

scoped to the verified UAT identity.

Root may be used only for one-time account administration/bootstrap when necessary; the repository preflight fails closed if the runtime profile resolves to root.

Production does not copy this IAM-user model; it should use workload identity/role.

## Recovery / PITR

A physical restore can resurrect historical nonterminal outbox state whose real-world provider outcome is unknowable.

Required sequence:

```text
email workers CLOSED
→ physical restore
→ recovery reconciliation
→ uncertain restored nonterminal email work → recovery_quarantined
→ sensitive payload wiped
→ reopen workers
```

Restored pending/claimed email work is never blindly replayed after PITR.

## Observability

Operational metrics derive from canonical PostgreSQL lifecycle state and exclude recipient/secret dimensions.

Current accepted signals include backlog, oldest backlog age, provider acceptance/failure/ambiguity counts, provider latency and active hard-bounce/complaint suppression counts.

Safe technical logs may contain intent reference, provider code, attempt number and normalized outcome. They must not contain OTP/recovery secrets or message payloads.

## Real-provider acceptance

The final 2026-09-03 UAT directly observed:

```text
SES preflight with non-root dedicated IAM user      PASS
real DANTE signup → SES → mailbox                   PASS
received OTP → DANTE verification → Account         PASS
real password recovery → SES → mailbox              PASS
recovery URL consumed → reset                       PASS
reset produces no auto-login                        PASS
prior session revoked                               PASS
password-reset notification → SES → mailbox         PASS
```

Runtime evidence showed three `provider_accepted` sends, all on attempt 1.

Direct PostgreSQL inspection showed for signup verification, password recovery and reset notification:

```text
dispatch_state_code = provider_accepted
attempt_count = 1
accepted_at present
provider_code = ses
result_code = provider_accepted
provider_message_id present
error_code NULL
sensitive payload bundle NULL
sensitive_wiped_at present
```

Exact observed evidence lives in `../development/email-platform-acceptance-2026-09-03.md`.

The same consumed recovery link was not manually replayed a second time in this final live run; that specific manual claim remains deliberately unasserted.

## Acceptance boundary

This ADR now closes:

```text
architecture direction
shared platform ownership
exact durable persistence
SES API v2 adapter
SMTP compatibility adapter
transactional integration model
retry/ambiguity policy
secret protection/wipe
feedback normalization/suppression implementation
observability model
reproducible local SES UAT posture
real DANTE signup/recovery/reset-notification UAT
```

Therefore:

```text
EMAIL PLATFORM ENGINEERING WORKSTREAM = CLOSED
```

This does **not** equal production deployment acceptance.

Still separate/open for deployment:

```text
DANTE production sender domain/subdomain
SPF/DKIM/DMARC verification
production SES account/quota/reputation posture
production workload identity / IAM role
live cloud provider-event ingress
production alerting/SLOs/traffic segmentation
privacy/legal/subprocessor deployment review where required
Apple Private Email Relay production-domain proof when Apple is enabled
secondary-provider/failover decision if ever required
```

## Rejected defaults

Not selected:

```text
self-hosted production SMTP/MTA fleet
SMTP transport as canonical lifecycle authority
provider dashboard as canonical DANTE state
in-memory queue as final durable queue
blind retry after ambiguous send outcome
OTP/recovery secret in logs/traces
long-lived plaintext sensitive outbox payload
silent double-send provider failover
marketing + Auth/security reputation mixed by default
provider SDK types crossing into Domain/application contracts
generic semantic event bus hidden inside email persistence
```

## Consequences

Positive:

```text
DANTE keeps provider portability and canonical lifecycle authority
crash-safe intent through PostgreSQL
feature mutation + external intent are atomically coordinated
provider ambiguity is explicit
security secrets are bounded and wiped
provider delivery telemetry can become first-class evidence
IAM/workload identity fits production deployment
future DANTE consumers can reuse one delivery subsystem
```

Costs:

```text
durable persistence and worker lifecycle
provider-event ingestion/operations
suppression/reconciliation policy
DNS/domain operations
observability/SLO work
provider-specific last-mile adapter
more nuanced ambiguous-side-effect handling
```

These costs are accepted because reliable account/security email is security-critical infrastructure.

## Reopen rule

Reopen the platform architecture only when concrete evidence shows that the accepted lifecycle split, PostgreSQL durability model or provider-neutral boundary cannot satisfy DANTE requirements.

Reopen the primary external adapter separately if SES becomes unsuitable due to deliverability, deployment posture, cost, regulation, privacy or operational constraints.

A free-tier promotion, developer preference or vendor marketing alone is not reopen evidence.

## External references originally reviewed 2026-09-02

- AWS SES API sending: `https://docs.aws.amazon.com/ses/latest/dg/send-email-api.html`
- AWS SES endpoints/regions: `https://docs.aws.amazon.com/general/latest/gr/ses.html`
- AWS SES event publishing: `https://docs.aws.amazon.com/ses/latest/dg/monitor-using-event-publishing.html`
- AWS SES configuration sets: `https://docs.aws.amazon.com/ses/latest/dg/using-configuration-sets.html`
- AWS SES IAM: `https://docs.aws.amazon.com/ses/latest/dg/control-user-access.html`
- AWS SES pricing: `https://aws.amazon.com/ses/pricing/`

Current operational behavior is governed by executable code/tests plus the current runbook/evidence, not by stale provider assumptions in the original research snapshot.
