# DANTE Email Platform

- **Status:** CURRENT / AUTHORITATIVE / ENGINEERING + REAL-PROVIDER UAT ACCEPTED ON `feature/access-auth`
- **Last reconciled:** 2026-09-03
- **Decision authority:** `../decisions/ADR-012-email-delivery-platform.md`
- **Persistence authority:** ADR-010, Alembic, SQLAlchemy mappings, Database Dictionary and executable PostgreSQL tests
- **Current first consumer:** Access/Auth security lifecycle
- **Platform ownership:** DANTE core infrastructure; not owned by Access/Auth
- **Real-provider acceptance evidence:** `../development/email-platform-acceptance-2026-09-03.md`

## 1. Purpose and boundary

This document defines the reusable DANTE outbound Email Platform.

The Email Platform is a shared technical subsystem. Access/Auth is its first production-intent consumer, but the platform is intentionally designed so future Account, security, notification and product workflows can reuse the same durable delivery machinery without rebuilding provider, retry, persistence, encryption, feedback or observability logic.

The permanent boundary is:

```text
DANTE feature/application transaction
        │
        ├── canonical business/security mutation
        └── durable EmailIntent
                 │
                 ▼
          PostgreSQL COMMIT
                 │
                 ▼
          durable outbox claim
                 │
                 ▼
         Email worker/orchestrator
                 │
                 ├── payload authentication/decryption
                 ├── template rendering
                 ├── bounded retry policy
                 └── provider adapter
                          │
                          ├── Amazon SES API v2
                          └── SMTP last-mile adapter for local/CI compatibility
                                   │
                                   ▼
                             Internet delivery
                                   │
                                   ▼
                     provider feedback / events
                                   │
                                   ▼
                  DANTE event/suppression state
                                   │
                                   ▼
                     operational observability
```

Core rule:

```text
DANTE owns lifecycle, intent, retry policy, ambiguity policy and canonical delivery state.
The provider owns last-mile transport only.
```

## 2. What the platform owns

The platform owns the reusable infrastructure for:

```text
durable email intent persistence
transactional coordination with caller state
idempotency and payload fingerprinting
supersession of stale work
bounded claim/lease concurrency
provider-attempt history
external provider correlation
ambiguous-outcome handling
bounded retries
sensitive payload protection and terminal wipe
template revisioning
text + HTML rendering
provider-neutral send contract
Amazon SES API v2 adapter
SMTP last-mile adapter
provider feedback normalization
hard-bounce / complaint suppression
post-restore quarantine
privacy-minimized observability
```

The platform does **not** decide product semantics such as whether a user should receive a reminder, digest, marketing campaign or account event. Those decisions remain with the feature/application consumer.

## 3. Current persistence model

Current Alembic authority:

```text
20260903_14_m5_email_platform.py
20260903_15_m5_email_platform_acl.py
```

Current platform tables:

```text
dante.email_delivery_intent
dante.email_delivery_attempt
dante.email_provider_event
dante.email_recipient_suppression
```

### 3.1 `email_delivery_intent`

Represents one durable DANTE decision to send one outbound message.

It contains:

```text
UUIDv7 intent identity
purpose / stream / template revision
recipient delivery address + comparison key
operation scope + idempotency key
supersession key
payload fingerprint
short-lived encrypted sensitive payload bundle
eligibility / expiry
claim token + lease
attempt budget
next-attempt state
accepted / terminal / wipe timestamps
```

Current dispatch states:

```text
pending
claimed
provider_accepted
retryable_failure
ambiguous
definitive_failure
expired
cancelled
recovery_quarantined
```

### 3.2 `email_delivery_attempt`

Represents one provider attempt for one intent.

It records:

```text
attempt number
provider code
started / finished timestamps
result code
provider message ID when accepted
safe error code
```

The provider message ID is correlation evidence; it is not DANTE canonical identity.

### 3.3 `email_provider_event`

Stores normalized, privacy-minimized provider evidence such as:

```text
delivered
delivery_delayed
bounced
complained
rejected
```

Raw message content and email body are not persisted here.

### 3.4 `email_recipient_suppression`

Stores DANTE's current operational projection for recipients that must not be retried after hard provider failures such as permanent bounce or complaint.

This projection is distinct from identity truth. Provider reachability does not redefine `EmailIdentity` ownership or verification semantics.

## 4. Transactional atomicity

A feature that requires an email as part of a durable mutation must stage the EmailIntent inside the **same PostgreSQL transaction** as the canonical feature state.

Example:

```text
BEGIN
  create password-signup challenge
  stage signup-verification EmailIntent
COMMIT
```

If EmailIntent staging fails, the caller mutation rolls back. If the transaction commits, admitted email work survives process loss because PostgreSQL owns it.

Provider network I/O is forbidden inside that transaction.

This is the Class-A side-effect boundary:

```text
business/security state + external intent are atomically coordinated
external network effect happens only after commit
```

## 5. Idempotency and supersession

Each intent uses:

```text
operation_scope
+
idempotency_key
+
immutable payload fingerprint
```

Same scope/key + same semantic payload is a replay and resolves to the existing intent.

Same scope/key + different semantic payload is a conflict and fails closed.

Fingerprint verification is key-rotation safe: retained retired payload keys can validate existing fingerprints without changing the semantic identity of a replay.

Supersession is explicit. When a newer proof/message replaces older pending work, stale nonterminal work is cancelled atomically instead of being left claimable.

## 6. Claiming, concurrency and leases

Workers use short PostgreSQL transactions and `FOR UPDATE SKIP LOCKED` semantics.

The model is:

```text
claim batch
→ assign exact claim token
→ durable lease
→ create provider attempt
→ COMMIT
→ verify claim ownership
→ render/send outside DB transaction
→ finalize in a new short transaction using exact claim ownership
```

This allows multiple workers/processes without double ownership of one claim.

An expired in-flight lease is not interpreted as "definitely unsent". It becomes `ambiguous` and is not blindly retried.

## 7. Provider outcome model

Provider send outcomes are normalized into:

```text
ACCEPTED
RETRYABLE_FAILURE
AMBIGUOUS
DEFINITIVE_FAILURE
```

For SES:

```text
HTTP/API success + MessageId
→ provider_accepted

known throttle / service-unavailable before acceptance
→ retryable_failure

known reject / invalid configuration
→ definitive_failure

connection loss / read timeout / uncertain transport outcome
→ ambiguous
```

`provider_accepted` does **not** mean delivered to recipient inbox.

Amazon SES API v2 is deliberately configured for one SDK wire attempt. DANTE, not the SDK, owns retry policy so a transport ambiguity cannot silently generate duplicate OTP/recovery messages.

The real UAT exposed one credential-refresh integration defect: the SES region had been supplied only to the SES client while Botocore's browser-login credential refresh needed region context at the boto3 session level. The provider now creates a region-bound `boto3.Session` and then the SES v2 client from that session. A focused test covers this behavior.

## 8. Sensitive payload protection

OTP and password-recovery bearer material are protected with a dedicated Email Platform key ring, separate from password peppers, signup OTP HMAC keys, CSRF keys and Apple grant encryption keys.

Current protection:

```text
AES-256-GCM
random nonce
purpose-separated key ring
AAD binds:
  email intent ref
  purpose
  template code
  template revision
```

The payload bundle is wiped when no longer safely needed, including terminal/unsafe states such as:

```text
provider accepted
ambiguous
expired
cancelled
definitive terminal failure
recovery quarantine
```

Secrets must never enter ordinary logs, metrics, traces or provider tags.

The final real SES UAT directly inspected PostgreSQL and observed `sensitive_key_id`, `sensitive_nonce` and `sensitive_ciphertext` cleared, with `sensitive_wiped_at` present, for signup verification, password recovery and reset notification.

## 9. Templates and rendering

Templates are repository-owned and revisioned.

Current renderer supports:

```text
plain-text body
minimal robust HTML alternative
escaped dynamic content
no tracking pixel
no click tracking
no provider link rewriting
```

Revision `1` remains renderable for compatibility. New intents currently use revision `2` with multipart text + HTML.

A template change that materially changes protected rendering semantics must advance the template revision rather than silently mutating historical intent meaning.

## 10. Provider adapters

### Amazon SES API v2

Primary external delivery adapter.

Properties:

```text
process-scoped SDK client
region-bound boto3 Session
configurable AWS region
bounded connect/read timeout
TCP keepalive
SDK retries disabled to one total wire attempt
provider MessageId required for accepted outcome
safe DANTE intent tag
Auth/security stream tag
optional SES configuration set
standard AWS credential provider chain
```

Credentials are not DANTE application settings and never belong in frontend/public configuration.

Real UAT acceptance used a dedicated non-root IAM user/profile with temporary `aws login` credentials and least-privilege SES permissions. Production should use workload identity / IAM role rather than reproducing a developer IAM user.

### SMTP

SMTP is retained as a last-mile adapter behind the same durable outbox/worker lifecycle for local/CI compatibility and generic provider testing.

There is no longer a second process-owned SMTP queue in the canonical runtime.

## 11. Feedback and suppression

SES feedback normalization currently supports:

```text
Delivery
DeliveryDelay
Bounce
Complaint
Reject
```

Provider events are persisted idempotently by provider identity.

Permanent bounce and complaint can materialize/update recipient suppression and project the appropriate recovery-delivery restriction into the Auth email identity integration point.

Soft/transient bounce does not automatically create permanent suppression.

Feedback order must not fabricate delivery success or resurrect terminal intents.

The feedback/suppression implementation is accepted through automated PostgreSQL tests. Live AWS cloud-event ingress was not part of the final real-provider UAT and remains a deployment/operations gate rather than an Email Platform implementation blocker.

## 12. Recovery / PITR posture

Physical database restore can resurrect historical nonterminal outbox rows whose real-world provider outcome is unknowable after the restore point.

DANTE therefore requires:

```text
email workers CLOSED
→ physical restore
→ recovery reconciliation
→ uncertain restored nonterminal email work → recovery_quarantined
→ protected sensitive payload wiped
→ reopen workers
```

Restored outbox state is never blindly replayed merely because PostgreSQL shows it as pending/claimed before reconciliation.

Email intent/attempt state is technical delivery state and is **not** DANTE MaterialState semantic history.

## 13. Observability

The Email Platform exposes privacy-minimized operational truth derived from canonical PostgreSQL state rather than volatile process counters.

Current snapshot includes:

```text
backlog count
oldest backlog age
provider accepted count
ambiguous count
retryable failure count
definitive failure count
accepted send latency average
accepted send latency maximum
active hard-bounce suppressions
active complaint suppressions
```

Metric names/dimensions must never include recipient address, email address, secret, payload or provider message content.

Worker/feedback structured logs may include safe non-secret technical identifiers such as intent reference, attempt number, provider code and normalized outcome.

## 14. Current first consumer: Access/Auth

Access/Auth currently uses the platform for:

```text
signup verification
provider-enrollment mailbox verification
password recovery
password-reset security notification
```

Those are consumer-specific purpose codes; they do not make Access/Auth the owner of the Email Platform.

The Access/Auth integration contract is documented separately in `access-auth-email-delivery.md`.

## 15. Future consumers

Future DANTE capabilities may reuse the same platform, for example:

```text
Account email-change notification
new authenticator / new-device security notification
calendar/reminder delivery
workflow notifications
digests
AI-generated report delivery
```

Adding a future consumer does **not** require rebuilding the provider, worker, retry, encryption, feedback or observability layers.

A new consumer must instead define explicitly:

```text
its semantic event/trigger
stream/purpose code
template + revision
idempotency scope/key
supersession policy if any
expiry/retry policy
preference/consent policy where applicable
```

Marketing/newsletter capability is not implicitly authorized by this platform. It requires separate product/legal/reputation policy and should remain operationally isolated from security traffic.

## 16. Extension constraints

Do not turn the Email Platform into a generic semantic event bus.

Forbidden shortcuts include:

```text
universal event/property bags
EAV payload semantics
generic "send anything" JSON contract
feature-specific business state hidden inside email tables
provider SDK types leaking into application/domain contracts
provider dashboard becoming canonical lifecycle state
```

The platform is technical delivery infrastructure. Feature semantics remain in their owning bounded context.

## 17. Acceptance status

### 17.1 Automated / PostgreSQL evidence

Observed evidence on `feature/access-auth` includes:

```text
Email unit tests PASS
non-PostgreSQL backend regressions PASS
real PostgreSQL Email Platform acceptance PASS
Auth mutation + EmailIntent atomicity PASS
rollback-on-stage-failure PASS
ACL least privilege PASS
idempotency + conflict PASS
claim/lease + SKIP LOCKED PASS
ambiguous no-blind-retry PASS
sensitive payload wipe PASS
feedback idempotency PASS
hard-bounce suppression PASS
post-restore quarantine PASS
privacy-minimized observability PASS
build PASS
```

### 17.2 Real SES UAT — observed PASS

On 2026-09-03 the repository-owned UAT flow directly proved:

```text
non-root dedicated AWS UAT principal
SES eu-west-3 preflight SUCCESS
real DANTE signup
→ SES provider_accepted attempt 1
→ real mailbox receipt
→ OTP verification
→ Account creation

real DANTE password recovery
→ SES provider_accepted attempt 1
→ real mailbox receipt
→ recovery URL consumed
→ password reset succeeds
→ no auto-login
→ prior AuthSession revoked

password reset notification
→ SES provider_accepted attempt 1
→ real mailbox receipt
```

Direct PostgreSQL inspection observed exactly these three UAT intents with:

```text
dispatch_state_code = provider_accepted
attempt_count = 1
accepted_at present
secret bundle wiped
sensitive_wiped_at present
provider_code = ses
result_code = provider_accepted
provider_message_id present
error_code NULL
```

Exact live evidence is preserved in `../development/email-platform-acceptance-2026-09-03.md`.

### 17.3 Explicit non-claim

The exact same consumed recovery URL was **not manually replayed a second time in the final live UAT**, because the message had already been removed before that check. The live claim is therefore one successful consumption, not manually re-observed replay rejection.

### 17.4 Closure

```text
Email Platform architecture                    ACCEPTED
Email Platform implementation                  ACCEPTED
Automated/PostgreSQL acceptance                PASS
Amazon SES API v2 adapter                      ACCEPTED
Real DANTE → SES signup UAT                    PASS
Real DANTE → SES recovery UAT                  PASS
Real reset-notification UAT                    PASS
Local UAT reproducibility                      MATERIALIZED

EMAIL PLATFORM ENGINEERING WORKSTREAM          CLOSED
```

Production deployment remains separate and is **not** implied by this closure.

## 18. Production deployment gates — separate from platform closure

Before calling production email accepted, deployment must materialize and verify as applicable:

```text
DANTE-controlled sender domain/subdomain
SPF
DKIM
DMARC
production workload identity / IAM role
SES production-access/quota/reputation posture
live provider feedback/event routing
operational alerting and traffic/reputation segmentation
privacy/legal/subprocessor review for the deployed configuration
Apple Private Email Relay sender-domain requirements where Apple is enabled
```

These gates may harden or configure the platform; they do not reopen the accepted durable Email Platform architecture absent concrete defect evidence.

## 19. Source map

Primary implementation:

```text
apps/backend/src/dante/auth/email_contracts.py
apps/backend/src/dante/auth/email_crypto.py
apps/backend/src/dante/auth/email_outbox.py
apps/backend/src/dante/auth/email_render.py
apps/backend/src/dante/auth/email_provider.py
apps/backend/src/dante/auth/email_worker.py
apps/backend/src/dante/auth/email_feedback.py
apps/backend/src/dante/auth/email_observability.py
apps/backend/src/dante/auth/email_runtime.py
apps/backend/src/dante/platform/database/mappings/email_delivery.py
```

Persistence:

```text
apps/backend/migrations/versions/20260903_14_m5_email_platform.py
apps/backend/migrations/versions/20260903_15_m5_email_platform_acl.py
```

Executable acceptance:

```text
apps/backend/tests/test_auth_email_platform.py
apps/backend/tests/integration/auth/test_m5_email_lifecycle.py
apps/backend/tests/integration/database/test_m5_email_platform.py
apps/backend/tests/integration/database/test_m5_email_observability.py
```

Reproducible external UAT:

```text
tooling/bootstrap-aws-cli-local.sh
tooling/email-platform-aws-preflight.py
tooling/serve-access-auth-local-uat.py
tooling/aws/dante-uat-ses-policy.template.json
docs/development/email-platform-local-uat.md
docs/development/email-platform-acceptance-2026-09-03.md
```

Database Dictionary:

```text
docs/database/dictionary/tables/email_delivery_intent.json
docs/database/dictionary/tables/email_delivery_attempt.json
docs/database/dictionary/tables/email_provider_event.json
docs/database/dictionary/tables/email_recipient_suppression.json
```

Decision record:

```text
docs/decisions/ADR-012-email-delivery-platform.md
```
