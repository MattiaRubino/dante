# DANTE Email Platform

- **Status:** CURRENT / AUTHORITATIVE / ARCHITECTURE ACCEPTED / SHARED-OWNERSHIP REFACTOR UNDER VERIFICATION
- **Last reconciled:** 2026-09-04
- **Decision authority:** `../decisions/ADR-012-email-delivery-platform.md`
- **Persistence authority:** ADR-010, Alembic, SQLAlchemy mappings, Database Dictionary and executable PostgreSQL tests
- **Current first consumer:** Access/Auth security lifecycle
- **Platform ownership:** DANTE shared technical infrastructure; not owned by Access/Auth
- **Accepted real-provider evidence:** `../development/email-platform-acceptance-2026-09-03.md`

## 1. Purpose and permanent boundary

The Email Platform is DANTE's reusable outbound-delivery subsystem. Access/Auth is the first consumer, not the owner.

The permanent split is:

```text
CONSUMER
semantic trigger / purpose
recipient decision
stream identity
template identity + revision policy
consumer copy / text / HTML rendering
idempotency + supersession inputs
        │
        ▼
SHARED EMAIL PLATFORM
durable EmailIntent
payload protection
claim / lease / concurrency
attempt lifecycle
retry / ambiguity policy
renderer port orchestration
provider-neutral message contract
SES / SMTP adapters
provider correlation
feedback persistence
recipient suppression
observability
        │
        ▼
LAST-MILE PROVIDER
Internet transport / delivery infrastructure
```

Core rule:

```text
DANTE owns durable delivery lifecycle and uncertainty semantics.
The consumer owns message meaning and rendering semantics.
The provider owns last-mile transport only.
```

The shared implementation lives under `dante.platform.email`. Shared modules must not import `dante.auth`; an executable architecture test guards that direction.

## 2. What the shared platform owns

The platform owns reusable technical machinery for:

```text
durable email intent persistence
transactional coordination with caller state
short-lived payload encryption + keyed fingerprinting
bounded claim/lease concurrency
provider-attempt history
external provider correlation
explicit ambiguous outcomes
bounded retry policy
terminal/unsafe-state secret wipe
renderer port / worker orchestration
provider-neutral send contract
Amazon SES API v2 adapter
SMTP local/CI adapter
provider-feedback normalization
hard-bounce / complaint suppression
post-restore quarantine
privacy-minimized observability
```

It does **not** own consumer semantics such as:

```text
whether an email should exist
what a security/reminder/report event means
consumer purpose vocabulary
consumer template copy/layout
preference / consent / legal policy
business-state transitions
```

A future consumer must provide those through explicit typed consumer integration rather than modifying shared delivery mechanics.

## 3. Current package ownership

Shared platform:

```text
apps/backend/src/dante/platform/email/
├── contracts.py
├── crypto.py
├── settings.py
├── outbox.py
├── provider.py
├── feedback.py
├── observability.py
├── worker.py
└── runtime.py
```

Access/Auth consumer integration remains under `dante.auth`, including its command types, semantic normalization, renderer and projection adapters.

Historical `dante.auth.email_*` compatibility import/adaptation paths may remain temporarily so accepted Auth code does not require a flag-day rewrite. They must delegate toward `dante.platform.email`; they are not architecture ownership.

## 4. Current persistence model

Alembic authority remains immutable:

```text
20260903_14  shared Email Platform persistence
20260903_15  exact runtime ACL hardening
```

Current tables:

```text
dante.email_delivery_intent
dante.email_delivery_attempt
dante.email_provider_event
dante.email_recipient_suppression
```

They are bounded technical delivery structures, not Domain owners, not DANTE MaterialState and not Access/Auth-owned semantic state.

### `email_delivery_intent`

One durable DANTE decision to attempt a bounded outbound message. It stores, among other technical facts:

```text
UUIDv7 intent identity
purpose / stream / template revision
recipient delivery address + comparison key
operation scope + idempotency key
supersession key
payload fingerprint
short-lived encrypted payload bundle
eligibility / expiry
claim token + lease
attempt budget / next-attempt state
accepted / terminal / wipe timestamps
```

Dispatch vocabulary:

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

### `email_delivery_attempt`

One exact provider attempt for one intent:

```text
attempt number
provider code
started / finished timestamps
result code
provider message ID when explicitly accepted
safe error code
```

Provider message ID is correlation evidence, never DANTE identity.

### `email_provider_event`

Privacy-minimized normalized provider evidence:

```text
delivered
delivery_delayed
bounced
complained
rejected
```

Raw email content/provider payload is not retained as canonical event content.

### `email_recipient_suppression`

Current technical projection preventing delivery to recipients with confirmed strong failure evidence such as permanent bounce or complaint. It is distinct from consumer identity/verification truth.

## 5. Transactional atomicity

A consumer mutation that requires durable delivery stages its canonical mutation and EmailIntent in the **same PostgreSQL transaction**.

Example:

```text
BEGIN
  create password-signup challenge
  stage signup-verification EmailIntent
COMMIT
```

If staging fails, the caller mutation fails with the transaction. If commit succeeds, admitted email work survives process loss because PostgreSQL owns it.

Provider network I/O is forbidden inside the caller transaction.

## 6. Idempotency and supersession

Persistent reservation identity is:

```text
operation_scope + idempotency_key
```

A same-key replay is valid only when the existing intent matches the complete immutable non-temporal delivery identity:

```text
purpose code
stream code
recipient delivery address
recipient comparison key
template code
template revision
locale
supersession key
protected semantic payload fingerprint
```

Therefore:

```text
same scope/key + same immutable work
→ existing EmailIntent

same scope/key + any different immutable work
→ conflict / fail closed
```

`payload_fingerprint` is a keyed equality proof for protected consumer payload. It is **not by itself** the whole replay-equality contract.

Expiry/eligibility timing is operational scheduling state rather than semantic replay identity; an exact semantic replay does not create a new intent merely because a caller recomputed a later expiration instant.

Supersession is explicit. A newer proof/message may atomically cancel older eligible nonterminal work through a consumer-supplied supersession key.

## 7. Claiming, concurrency and leases

Workers use short PostgreSQL transactions and `FOR UPDATE SKIP LOCKED`:

```text
claim batch
→ assign exact claim token
→ durable lease
→ create provider attempt
→ COMMIT
→ verify exact claim ownership
→ consumer renderer + provider I/O outside DB transaction
→ finalize in a new short transaction using exact claim ownership
```

Multiple workers/processes may operate without two owners for one live claim.

An expired in-flight lease is not interpreted as definitely unsent. It becomes `ambiguous` and is not blindly retried.

## 8. Provider outcome model

Normalized provider outcomes:

```text
ACCEPTED
RETRYABLE_FAILURE
AMBIGUOUS
DEFINITIVE_FAILURE
```

For SES:

```text
API success + MessageId
→ provider_accepted

known retryable service/throttle condition
→ retryable_failure

known definitive rejection
→ definitive_failure

connection/read/transport uncertainty
→ ambiguous
```

`provider_accepted != delivered`.

SES is configured for one deliberate SDK wire attempt. DANTE, not hidden SDK retry behavior, owns retry policy.

The 2026-09-03 real UAT exposed a Botocore browser-login credential-refresh region defect. DANTE conservatively classified that attempt `ambiguous`; the provider adapter was then fixed to construct a region-bound `boto3.Session` before the SES v2 client.

## 9. Sensitive payload protection

Current protection:

```text
AES-256-GCM
dedicated Email Platform key ring
random nonce
AAD binds:
  EmailIntent ref
  purpose
  template code
  template revision
keyed payload fingerprint
```

The Email Platform key ring remains purpose-separated from password peppers, OTP HMAC keys, CSRF keys and Apple-grant encryption keys.

Sensitive payload columns are wiped when no longer safely needed, including:

```text
provider accepted
ambiguous
expired
cancelled
definitive terminal failure
recovery quarantine
```

Secrets must never enter ordinary logs, metrics, traces or provider tags.

## 10. Rendering ownership

The **consumer owns actual message rendering semantics**.

The shared platform owns only the renderer port and orchestration needed to turn a claimed durable intent into a provider-neutral message before the provider call.

Current Access/Auth consumer owns:

```text
stream: auth_security

auth.signup_verification
auth.provider_enrollment_verification
auth.password_recovery
auth.password_reset_notification

current new-intent revision: 2
```

Its renderer produces plain text + minimal HTML, escapes dynamic content and rejects claims from another stream.

Revision `1` remains renderable for already-persisted compatibility. New Auth intents currently use revision `2`.

A consumer must not silently mutate historical template meaning. Material rendering changes advance that consumer's template revision.

## 11. Provider adapters

### Amazon SES API v2

Primary accepted external adapter:

```text
process-scoped SDK client
region-bound boto3 Session
explicit AWS region
bounded connect/read timeout
TCP keepalive
one total SDK wire attempt
provider MessageId required for accepted outcome
safe intent + stream tags
optional SES configuration set
standard AWS credential provider chain
```

Credentials are not DANTE app/front-end settings. Production should use workload identity/IAM role rather than developer IAM credentials.

### SMTP

SMTP remains a last-mile adapter behind the same durable lifecycle for local/CI/generic-provider compatibility. It is not a second canonical process queue.

## 12. Feedback, suppression and consumer projection

Shared feedback normalization supports:

```text
Delivery
DeliveryDelay
Bounce
Complaint
Reject
```

The shared layer persists provider evidence idempotently and owns recipient suppression.

A consumer may receive a typed projection hook after strong suppression evidence. The shared package must **not** import or mutate consumer persistence directly.

For current Access/Auth integration, the Auth-owned suppression projection may set:

```text
EmailIdentity.recovery_restriction_code = provider_delivery_disabled
```

That projection remains Auth-owned and does not redefine email verification/ownership.

Live AWS cloud-event ingress was not part of the real-provider UAT. Normalization/persistence/suppression were previously accepted through PostgreSQL tests; production event routing remains a deployment gate.

## 13. Recovery / PITR posture

Physical restore may resurrect historical nonterminal outbox state whose real-world provider effect is unknowable.

Required posture:

```text
email workers closed
→ physical restore
→ recovery reconciliation
→ restored uncertain nonterminal email → recovery_quarantined
→ protected payload wiped
→ reopen workers
```

Restored work is never blindly replayed merely because an older database snapshot says `pending` or `claimed`.

## 14. Observability

Operational truth is derived from durable PostgreSQL state rather than volatile counters.

Current snapshot includes low-cardinality facts such as:

```text
backlog count / oldest age
provider accepted count
ambiguous count
retryable / definitive failure counts
accepted send latency average / maximum
active hard-bounce suppressions
active complaint suppressions
```

No recipient, address, secret, payload or message content may become metric dimensions.

## 15. Current first consumer: Access/Auth

Access/Auth uses the platform for:

```text
signup verification
provider-enrollment mailbox verification
password recovery
password-reset security notification
```

The consumer contract is `access-auth-email-delivery.md`.

Future Account/reminder/workflow/digest/report consumers reuse the same delivery machinery but define their own semantic trigger, stream, purpose, renderer, template revision, idempotency inputs, supersession/expiry and preference/consent policy.

Marketing/newsletter capability is not implicitly authorized and should remain legally and reputationally isolated from security traffic.

## 16. Configuration ownership during first-consumer integration

The shared implementation consumes only the structural read-only `EmailPlatformSettings` protocol and does not import `AuthSettings`.

At the current first-consumer checkpoint, concrete environment fields are still carried inside the existing `AuthSettings` / `DANTE_AUTH__...` configuration envelope for compatibility with the already-accepted Access/Auth bootstrap and UAT tooling.

This is a **configuration-carrier compatibility boundary**, not platform ownership.

A top-level `Settings.email` / `DANTE_EMAIL__...` namespace migration is not required merely to make the architecture truthful today. It becomes justified when a second consumer or deployment configuration needs independent composition, and must then be done as an explicit validated configuration migration rather than a silent rename.

## 17. Extension constraints

Forbidden shortcuts:

```text
shared email package importing dante.auth
universal event/property bags
generic "send anything" JSON semantic API
feature-specific business state hidden in email tables
provider SDK types leaking into consumers
provider dashboard becoming canonical lifecycle truth
```

An executable test currently enforces the first rule.

## 18. Acceptance truth

### Accepted baseline evidence before the ownership refactor

The 2026-09-03 accepted implementation/UAT evidence proved:

```text
real PostgreSQL Email Platform behavior
Auth mutation + EmailIntent atomicity
ACL least privilege
claim/lease + SKIP LOCKED
ambiguous no-blind-retry
sensitive payload wipe
feedback idempotency + suppression
post-restore quarantine
real DANTE → SES signup delivery + OTP
real DANTE → SES recovery + reset
reset notification delivery
no auto-login after reset
prior AuthSession revocation
three provider_accepted attempts with MessageId and terminal wipe
```

Exact evidence remains in `../development/email-platform-acceptance-2026-09-03.md` and is historical fact.

### Current shared-ownership refactor

The subsequent ownership cleanup moved reusable implementation under `dante.platform.email`, separated consumer rendering/projection, hardened replay identity and added architecture/replay tests.

These code changes are **IMPLEMENTED BUT NOT YET RE-ACCEPTED** until the current branch executes the focused static/unit/PostgreSQL regression gate.

Do not reinterpret the prior UAT as proof that later refactor commits have already passed.

## 19. Production deployment gates

Engineering architecture closure never implied production sender acceptance. Deployment still owns, as applicable:

```text
DANTE-controlled sender domain/subdomain
SPF / DKIM / DMARC
production workload identity / IAM role
SES production access/quota/reputation posture
live provider feedback/event routing
operational alerting / SLOs
traffic/reputation segmentation
privacy/legal/subprocessor review
Apple Private Email Relay sender-domain compatibility
```

## 20. Source map

Shared platform implementation:

```text
apps/backend/src/dante/platform/email/contracts.py
apps/backend/src/dante/platform/email/crypto.py
apps/backend/src/dante/platform/email/settings.py
apps/backend/src/dante/platform/email/outbox.py
apps/backend/src/dante/platform/email/provider.py
apps/backend/src/dante/platform/email/feedback.py
apps/backend/src/dante/platform/email/observability.py
apps/backend/src/dante/platform/email/worker.py
apps/backend/src/dante/platform/email/runtime.py
apps/backend/src/dante/platform/database/mappings/email_delivery.py
```

Access/Auth consumer adapters:

```text
apps/backend/src/dante/auth/email_delivery.py
apps/backend/src/dante/auth/email_render.py
apps/backend/src/dante/auth/email_outbox.py
apps/backend/src/dante/auth/email_feedback.py
apps/backend/src/dante/auth/email_runtime.py
```

Architecture / replay guards:

```text
apps/backend/tests/test_email_platform_architecture.py
apps/backend/tests/test_auth_email_platform.py
apps/backend/tests/integration/database/test_m5_email_platform.py
apps/backend/tests/integration/database/test_email_platform_replay.py
```

Persistence:

```text
apps/backend/migrations/versions/20260903_14_m5_email_platform.py
apps/backend/migrations/versions/20260903_15_m5_email_platform_acl.py
```

Decision / evidence:

```text
docs/decisions/ADR-012-email-delivery-platform.md
docs/architecture/access-auth-email-delivery.md
docs/development/email-platform-local-uat.md
docs/development/email-platform-acceptance-2026-09-03.md
```
