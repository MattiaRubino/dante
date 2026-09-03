# DANTE Database System of Record

- **Status:** CURRENT / CP6 CLOSED ON `main` / ACCESS-AUTH + EMAIL PLATFORM MATERIALIZED ON `feature/access-auth`
- **Last reconciled:** 2026-09-03
- **PostgreSQL:** 18.6
- **Current accepted Access/Auth Alembic head:** `20260903_15`
- **Protected-main CP6 baseline:** `20260826_08`
- **Current Access/Auth reference:** `access-auth.md`
- **Shared Email Platform authority:** `../architecture/email-platform.md`
- **Persistence doctrine:** `../development/backend-cp6-02-postgresql-persistence-constitution.md`
- **ADR:** `../decisions/ADR-010-postgresql-persistence-constitution.md`

## 1. Authority model

```text
Domain / Logical / Physical semantics
→ persistence constitution / ADR-010
→ Alembic evolution
→ SQLAlchemy mappings
→ Database Dictionary
→ human reference
→ real PostgreSQL introspection + tests
```

A mismatch is a defect.

Permanent rule:

```text
human reference
≈ Dictionary
≈ SQLAlchemy
≈ Alembic
≈ real PostgreSQL
≈ direct tests
```

## 2. Baseline progression

Protected-main CP6:

```text
Alembic             20260826_08
68 tables / 5 views / 14 routines / 75 triggers
95 indexes / 68 FKs / 120 CHECKs
```

Access/Auth evolution:

```text
20260827_09  Account / EmailIdentity / PasswordCredential / AuthSession
20260827_10  bounded Account security-lock capability
20260829_11  signup/recovery challenges + lifecycle ACL
20260830_12  ExternalIdentity/provider/Apple/WebAuthn/passkey persistence
20260831_13  bounded authenticator-lifecycle runtime ACL follow-up
```

Shared Email Platform evolution:

```text
20260903_14  durable Email Platform persistence
20260903_15  exact Email Platform runtime ACL hardening
```

Current branch catalog:

```text
PostgreSQL          18.6
Alembic             20260903_15
87 tables
5 views
15 routines
75 triggers
170 physical indexes
88 foreign keys
267 CHECK constraints
```

The exact Dictionary count is governed by `dictionary/scope.json` and the current Dictionary tree; stale historical “103 entries” counts must not be treated as current after Email Platform materialization.

## 3. Current Access/Auth shape

```text
Account
├── EmailIdentity 1..N over lifecycle
├── PasswordCredential 0..1
├── AuthSession 0..N
├── ExternalIdentity 0..N
├── WebAuthnAccount 0..1
│   └── PasskeyCredential 0..N
└── current recovery state

PasswordSignupChallenge
PasswordRecoveryChallenge
ExternalAuthTransaction
ExternalLinkChallenge
ExternalSignupChallenge
AccountProfileBootstrap
AppleAuthGrant
WebAuthnChallenge
```

No generic auth-token/proof god-table exists.

## 4. Shared Email Platform persistence

The reusable outbound Email Platform adds exactly four bounded technical structures:

```text
dante.email_delivery_intent
dante.email_delivery_attempt
dante.email_provider_event
dante.email_recipient_suppression
```

They represent technical delivery lifecycle, not new Domain semantic owners.

They are **not** DANTE MaterialState and must not be routed through generic MaterialState semantics.

### `email_delivery_intent`

Owns durable DANTE send intent, including:

```text
UUIDv7 identity
purpose/stream/template revision
recipient + comparison key
operation scope + idempotency key
supersession key
payload fingerprint
short-lived protected sensitive bundle
eligibility/expiry
claim token + lease
attempt budget / retry scheduling
accepted / terminal / wipe state
```

### `email_delivery_attempt`

Owns each exact provider attempt:

```text
attempt number
provider code
start/finish
normalized result
provider MessageId
safe error code
```

### `email_provider_event`

Owns normalized asynchronous provider evidence:

```text
delivered
delivery_delayed
bounced
complained
rejected
```

### `email_recipient_suppression`

Owns current operational hard-bounce/complaint suppression projection. It does not redefine `EmailIdentity` verification or ownership truth.

## 5. Email Platform DB invariants

```text
feature/Auth mutation + EmailIntent commit atomically
provider I/O never inside caller DB transaction
operation_scope + idempotency_key is unique
payload fingerprint makes replay semantics immutable
claim/lease ownership is exact
workers use short transactions + SKIP LOCKED
ambiguous in-flight work is not blindly replayed
sensitive payload uses dedicated AEAD protection
terminal/unsafe state wipes sensitive payload
post-PITR uncertain nonterminal email work is recovery_quarantined
runtime ACL remains least privilege
```

Recovery order:

```text
email workers CLOSED
→ physical restore
→ reconciliation
→ quarantine uncertain restored nonterminal email work
→ wipe sensitive payload
→ reopen workers
```

## 6. Security/ownership rules

```text
Account is the durable security root
EmailIdentity is separate
PasswordCredential is optional
ExternalIdentity authority = issuer + subject
provider email is metadata/evidence, never link key
AuthSession stores verifier, not raw session secret
WebAuthn stores public credential material, not private key/biometric/PIN
passkey credential IDs remain lifetime-unique
runtime role remains least-privilege
Account-wide security mutation uses bounded DB-owned serialization
Email Platform technical rows do not become semantic identity owners
```

## 7. Transaction doctrine

```text
READ COMMITTED
short authoritative transactions
network/provider/WebAuthn wait outside DB transaction
Account lock only for Account-wide security mutation
email work claim uses bounded row ownership / SKIP LOCKED
no blanket SERIALIZABLE
no blind mutation retry
ambiguous commit/send handled by operation-specific reconciliation
```

## 8. Same-change database rule

A structural DB change is incomplete unless the same reviewed slice updates affected:

```text
semantic/security contract
Alembic forward migration
SQLAlchemy mapping/metadata
Dictionary
human current DB reference
direct tests
real PostgreSQL proof
status/workstream docs when milestone state changes
```

Applied migrations are immutable historical evidence.

## 9. Current proof

M5 persistence/API/backend suites closed against real PostgreSQL. Live Auth UAT additionally confirmed passkey lifecycle, passwordless Google Account state and session coherence.

Email Platform PostgreSQL acceptance proved:

```text
migration/head correctness
exact runtime ACL
atomic Auth state + EmailIntent
rollback on staging failure
idempotency/conflict
claim/lease concurrency
ambiguous no-blind-retry
secret wipe
feedback idempotency
suppression projection
post-restore quarantine
privacy-minimized observability
```

Final real SES UAT direct PostgreSQL inspection observed three accepted intents — signup verification, password recovery and password-reset notification — each with one SES attempt, provider MessageId present and sensitive payload bundle wiped.

Exact evidence: `../development/email-platform-acceptance-2026-09-03.md`.

## 10. Documentation

- `access-auth.md` — current Access/Auth + Email consumer DB semantics
- `../architecture/email-platform.md` — shared Email Platform architecture
- `dictionary/README.md` — structured Dictionary contract
- `../architecture/access-auth-m5-persistence-api-contract.md` — detailed exact M5 design/milestone reconciliation
- `../development/email-platform-acceptance-2026-09-03.md` — final real-provider + DB evidence

The large `dante-postgresql-database.md` blueprint contains historical CP6 and early Access/Auth reconciliation sections. Where its old branch-progress labels or counts conflict with this System of Record, this file plus executable Alembic/Dictionary/live PostgreSQL own current truth.
