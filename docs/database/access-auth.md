# DANTE Access/Auth Database Reference

- **Status:** CURRENT / BRANCH-LOCAL / M3–M5 + EMAIL PLATFORM MATERIALIZED
- **Last reconciled:** 2026-09-03
- **Branch:** `feature/access-auth`
- **PostgreSQL:** 18.6
- **Current accepted Alembic head:** `20260903_15`
- **Protected-main CP6 baseline:** `20260826_08`
- **Database System of Record:** `README.md`
- **M5 architecture:** `../architecture/access-auth-m5-contract.md`
- **Exact M5 design:** `../architecture/access-auth-m5-persistence-api-contract.md`
- **Shared Email Platform:** `../architecture/email-platform.md`
- **Access/Auth Email integration:** `../architecture/access-auth-email-delivery.md`

## 1. Current evidence state

```text
M3 persistence                         MATERIALIZED / PG PROVEN / CLOSED
M4 persistence                         MATERIALIZED / PG PROVEN / CLOSED
M5.1 / M5.2                            COMPLETE
M5-A persistence                       MATERIALIZED / PG PROVEN
M5-B–D + Groups 1–3                    APPLICATION/API ENGINEERING PASS
20260831_13 lifecycle ACL               ACCEPTED
Email Platform 20260903_14              MATERIALIZED / PG PROVEN
Email Platform ACL 20260903_15          ACCEPTED
Email Platform real SES UAT             PASS
manual passkey/Google DB UAT            PASS
```

Current catalog:

```text
87 tables / 5 views / 15 routines / 75 triggers
170 physical indexes / 88 foreign keys / 267 CHECKs
```

## 2. Canonical Auth topology

```text
Account
├── EmailIdentity 1..N
├── PasswordCredential 0..1
├── AuthSession 0..N
├── ExternalIdentity 0..N
├── WebAuthnAccount 0..1
│   └── PasskeyCredential 0..N
└── recovery lifecycle

PasswordSignupChallenge
PasswordRecoveryChallenge
ExternalAuthTransaction
ExternalLinkChallenge
ExternalSignupChallenge
AccountProfileBootstrap
AppleAuthGrant
WebAuthnChallenge
```

Shared technical delivery infrastructure used by Auth:

```text
EmailDeliveryIntent
EmailDeliveryAttempt
EmailProviderEvent
EmailRecipientSuppression
```

Those four structures are not children in the semantic Account identity model; they are bounded shared technical delivery state.

## 3. `dante.account`

Durable Access/security root:

```text
account_ref UUIDv7 PK
status_code active | disabled
created_at
disabled_at nullable
```

It does not directly store password/email/provider/passkey/profile/device payload.

Account-wide security mutation serializes through the bounded database capability `dante.acquire_account_security_lock(uuid)` rather than broad runtime UPDATE authority.

## 4. `dante.email_identity`

Canonical contact/login/recovery email identity:

```text
email_identity_ref
account_ref
address
comparison_key UNIQUE
created_at
verified_at
recovery_restriction_code nullable
recovery_restriction_observed_at nullable
```

`verified_at` is historical mailbox-control evidence. Provider reachability restrictions are separate current state.

EmailIdentity is not Account and is never the federated-provider identity key.

Email provider suppression/reachability state does not rewrite `verified_at`; the shared Email Platform projects only the bounded recovery-delivery restriction when current hard-bounce/complaint policy requires it.

## 5. `dante.password_credential`

Optional current credential:

```text
password_credential_ref
account_ref UNIQUE
verifier
pepper_key_id
created_at
updated_at
```

Raw password, normalized password bytes, pepper and HIBP material are never persisted.

Passwordless Accounts are first-class. Group 1 lifecycle supports add/remove password under recent-auth + anti-lockout policy.

## 6. `dante.auth_session`

Canonical independent server-authoritative session:

```text
auth_session_ref
account_ref
secret_verifier UNIQUE
created_at
authenticated_at
recent_auth_at
last_user_activity_at
expires_at
revoked_at nullable
revocation_reason_code nullable
```

Raw session secrets are never persisted. Provider/passkey success always converges here rather than turning provider tokens into DANTE sessions.

Final live recovery UAT directly observed that reset did not auto-login and an existing prior session was revoked.

## 7. Signup / recovery challenges

`password_signup_challenge` owns anonymous/pre-Account password signup state and verifier-only OTP evidence.

`password_recovery_challenge` owns one-use high-entropy recovery proof bound to the exact Account/EmailIdentity. Recovery can create the first PasswordCredential for a passwordless Account or replace an existing credential, revokes prior sessions and requires fresh signin.

When real delivery is required, challenge mutation and the corresponding durable EmailIntent are staged in the same PostgreSQL transaction.

```text
signup challenge + signup-verification EmailIntent
→ one commit

recovery challenge + password-recovery EmailIntent
→ one commit
```

Provider network I/O happens only after commit.

## 8. Shared Email Platform persistence

### `dante.email_delivery_intent`

Durable technical decision to send one message.

Key responsibilities:

```text
UUIDv7 intent
purpose / stream / template revision
recipient address + comparison key
operation_scope + idempotency_key
supersession key
payload fingerprint
short-lived protected payload bundle
eligibility / expiry
claim token + lease
attempt budget / next-attempt state
accepted / terminal / wipe timestamps
```

Current Auth purpose vocabulary:

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

Dispatch states:

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

### `dante.email_delivery_attempt`

One row per provider attempt:

```text
email_attempt_ref
email_intent_ref
attempt_number
provider_code smtp | ses
started_at
finished_at
result_code
provider_message_id
error_code
```

Provider MessageId is correlation evidence, not canonical DANTE identity.

### `dante.email_provider_event`

Normalized asynchronous SES evidence:

```text
delivered
delivery_delayed
bounced
complained
rejected
```

Provider event identity is idempotent and raw message body/content is not persisted.

### `dante.email_recipient_suppression`

Current operational projection for hard-bounce/complaint suppression. It is separate from EmailIdentity verification truth.

## 9. Email Platform DB doctrine

```text
Auth/business state + EmailIntent atomically coordinated
provider network wait forbidden inside DB transaction
READ COMMITTED baseline
claim/lease uses short transactions + FOR UPDATE SKIP LOCKED
exact claim token required for finalize
same operation_scope/idempotency_key + same fingerprint = replay
same idempotency identity + different fingerprint = conflict
expired/uncertain in-flight work can become ambiguous
ambiguous is not blindly retried
sensitive delivery payload uses dedicated AES-256-GCM ring
terminal/unsafe state wipes sensitive payload
restored uncertain nonterminal work is recovery_quarantined before workers reopen
```

The Email Platform is technical delivery state and is **not** MaterialState.

## 10. `dante.external_identity`

Durable lifetime provider binding:

```text
external_identity_ref
account_ref
email_identity_ref nullable
provider_code google | apple
issuer
subject
provider_email_address nullable
provider_email_private nullable
status_code active | revoked
created/status/last-auth/revocation timestamps
```

Hard identity authority:

```text
UNIQUE(issuer, subject)
```

No `UNIQUE(account_ref, provider_code)` is imposed. Normal unlink is logical revoke, preserving lifetime identity uniqueness.

Live Google UAT verified an active ExternalIdentity keyed by canonical Google issuer + provider subject while the corresponding Account had zero PasswordCredential.

## 11. Provider transaction/collision state

`external_auth_transaction` is the bounded server-authoritative sign-in/link/reauth transaction with verifier-only state/nonce and optional exact AuthSession bearer snapshot.

`external_link_challenge` prevents silent email merge and carries bounded explicit link continuation.

`external_signup_challenge` carries provider evidence that still requires direct DANTE mailbox proof before Account creation.

No Account is created before the accepted proof set.

## 12. `dante.account_profile_bootstrap`

One-shot, non-canonical provider bootstrap staging for useful first-account data such as name/locale/picture hint. Later provider login does not continuously overwrite DANTE-owned profile values.

## 13. `dante.apple_auth_grant`

Durable encrypted Apple server-side grant lifecycle:

```text
pending → active → revocation_pending → revoked
```

Refresh-token material is application-layer AEAD encrypted with key material outside PostgreSQL/Git/logs. Local provider revoke precedes remote revoke so provider outage does not keep local authentication active.

## 14. WebAuthn persistence

### `dante.webauthn_account`

```text
account_ref PK/FK
user_handle bytea(32) UNIQUE
```

The user handle is opaque random state, not AccountRef/email/PersonRef.

### `dante.passkey_credential`

```text
passkey_credential_ref
account_ref
credential_id UNIQUE
credential_public_key
cose_algorithm
sign_count
backup_eligible
backup_state
transports
label
status_code active | revoked
created/updated/last-used/revocation timestamps
```

DANTE stores no biometric template, device PIN or private key. Passkey removal is logical revoke; lifetime credential-id uniqueness remains.

### `dante.webauthn_challenge`

Bounded verifier-only ceremony state for registration/authentication/reauthentication with exact Account/AuthSession/user-handle binding where applicable. Raw browser challenge is not persisted.

## 15. Runtime ACL through `20260903_15`

`20260831_13` grants only bounded runtime operations required by authenticator lifecycle.

`20260903_14` materializes Email Platform persistence and initial runtime capabilities.

`20260903_15` hardens Email Platform runtime access to exact lifecycle columns, preserving deny-by-default/least-privilege posture.

Applied revisions are historical evidence and must not be rewritten.

## 16. Transaction/race doctrine

```text
READ COMMITTED
short authoritative transactions
network/provider/browser ceremony outside DB transaction
Account security lock for Account-wide mutation
constraints as final race arbiters
bounded claim/lease for email work
no blanket SERIALIZABLE
no blind mutation/send retry
```

## 17. Live UAT database evidence

Manual UAT observed coherent durable state for:

```text
passkey create/use/rename
password remove/re-establish
anti-lockout rejection
session rotation/login
Google passwordless Account
verified EmailIdentity
Google ExternalIdentity
active AuthSession
```

Final Email Platform real SES UAT observed three accepted intents:

```text
signup_verification
password_recovery
password_reset_notification
```

For each:

```text
dispatch_state_code = provider_accepted
attempt_count = 1
accepted_at present
sensitive bundle NULL
sensitive_wiped_at present
```

Corresponding attempts:

```text
provider_code = ses
attempt_number = 1
result_code = provider_accepted
provider_message_id present
error_code NULL
```

Personal email/provider subject values are intentionally excluded from repository documentation.

Exact real-provider evidence: `../development/email-platform-acceptance-2026-09-03.md`.

## 18. Current source relationship

Detailed exact constraint/FK/ACL rationale remains recoverable in the M5 persistence/API contract, Email Platform architecture, Dictionary, SQLAlchemy mappings, Alembic and direct tests.

Where older milestone sections say `M5-B NEXT`, `20260830_12 current`, `Email Platform not materialized` or show 83-table counts, those are historical progress metadata. This file plus `README.md`, executable migrations/Dictionary and direct PostgreSQL proof own current database-reference state.
