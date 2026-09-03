# DANTE Access/Auth Database Reference

- **Status:** CURRENT / BRANCH-LOCAL / M3–M5 + EMAIL PLATFORM MATERIALIZED
- **Last reconciled:** 2026-09-03
- **Branch:** `feature/access-auth`
- **PostgreSQL:** 18.6
- **Feature branch Alembic head:** `20260903_15`
- **Protected-main Alembic head:** `20260830_09` — Recovery integrated separately
- **Historical CP6 common ancestor:** `20260826_08`
- **Database System of Record:** `README.md`
- **M5 architecture:** `../architecture/access-auth-m5-contract.md`
- **Exact M5 design:** `../architecture/access-auth-m5-persistence-api-contract.md`
- **Shared Email Platform:** `../architecture/email-platform.md`

## 1. Current evidence state

```text
M3 persistence                         MATERIALIZED / PG PROVEN / CLOSED
M4 persistence                         MATERIALIZED / PG PROVEN / CLOSED
M5 multi-authenticator persistence     MATERIALIZED / PG PROVEN
M5 application/API/Web                 ENGINEERING + UAT ACCEPTED
Email Platform 20260903_14             MATERIALIZED / PG PROVEN
Email Platform ACL 20260903_15         ACCEPTED
real SES UAT                           PASS
manual passkey/Google DB UAT           PASS
M5 whole scope                         CLOSED / ACCEPTED
Apple real external UAT                BOUNDED DEFERRED / NON-BLOCKING
```

Current branch catalog before main convergence:

```text
87 tables / 5 views / 15 routines / 75 triggers
170 physical indexes / 88 foreign keys / 267 CHECKs
```

## 2. Protected-main relationship

Protected main is **not** still at the CP6 `20260826_08` head. It independently contains the closed Recovery revision:

```text
20260826_08
└── 20260830_09 recovery_material_state_retirement
```

This Access branch independently contains:

```text
20260826_08
└── 20260827_09
    └── 20260827_10
        └── 20260829_11
            └── 20260830_12
                └── 20260831_13
                    └── 20260903_14
                        └── 20260903_15
```

Recovery objects are not claimed as branch-local materialization before main is merged. The future integration must preserve both histories and add a forward Alembic merge revision rather than rewriting either line.

## 3. Canonical Auth topology

```text
Account
├── EmailIdentity 1..N
├── PasswordCredential 0..1
├── AuthSession 0..N
├── ExternalIdentity 0..N
├── WebAuthnAccount 0..1
│   └── PasskeyCredential 0..N
└── bounded signup/recovery/provider/WebAuthn lifecycle state

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

Those four structures belong to the shared Email Platform and are not semantic Account children.

## 4. `dante.account`

Durable security root:

```text
account_ref UUIDv7 PK
status_code active | disabled
created_at
disabled_at nullable
```

Account does not embed email/password/provider/passkey/profile/device payload.

Account-wide security mutations serialize through the bounded database capability:

```text
dante.acquire_account_security_lock(uuid)
```

The routine is owner-controlled, `SECURITY DEFINER`, uses trusted `pg_catalog,dante,pg_temp` search path and exposes only the required runtime EXECUTE capability.

## 5. `dante.email_identity`

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

`verified_at` is historical direct mailbox-control evidence. Current provider delivery restrictions/suppression are separate state and never rewrite canonical ownership meaning.

Provider email is never the federated identity key.

## 6. `dante.password_credential`

```text
password_credential_ref
account_ref UNIQUE
verifier
pepper_key_id
created_at
updated_at
```

Raw password, normalized password bytes, pepper and HIBP material are never persisted. Password is optional; passwordless Accounts are first-class.

## 7. `dante.auth_session`

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

Raw bearer secrets are never persisted. All successful authentication methods converge on this canonical DANTE session rather than provider tokens becoming sessions.

Real recovery UAT observed that reset did not auto-login and revoked an existing prior AuthSession.

## 8. Signup / recovery challenges

`password_signup_challenge` owns anonymous pre-Account password signup and verifier-only OTP proof state.

`password_recovery_challenge` owns one-use high-entropy recovery proof bound to the exact Account/EmailIdentity.

When delivery is required:

```text
signup challenge mutation + signup-verification EmailIntent
→ same PostgreSQL transaction

recovery challenge mutation + password-recovery EmailIntent
→ same PostgreSQL transaction
```

Provider network I/O occurs only after commit.

Recovery reset replaces/creates PasswordCredential, revokes existing sessions and requires fresh normal signin.

## 9. External provider persistence

### `dante.external_identity`

```text
external_identity_ref
account_ref
email_identity_ref nullable
provider_code google | apple
issuer
subject
provider email metadata nullable
status active | revoked
lifecycle timestamps
```

Hard external identity authority:

```text
UNIQUE(issuer, subject)
```

Email coincidence never silently links Accounts.

### `external_auth_transaction`

Short-lived server-authoritative provider transaction with verifier-only state/nonce and exact AuthSession binding where required.

### `external_link_challenge`

Bounded explicit provider collision/link continuation; prevents provider-email auto-merge.

### `external_signup_challenge`

Provider evidence that still requires direct DANTE mailbox proof when current mailbox authority is not provider-established.

### `account_profile_bootstrap`

One-shot non-canonical provider bootstrap staging; later provider login does not continuously overwrite DANTE-owned profile state.

### `apple_auth_grant`

Encrypted minimal Apple server grant lifecycle:

```text
pending → active → revocation_pending → revoked
```

Encryption keys remain outside PostgreSQL/Git/logs.

## 10. WebAuthn persistence

### `dante.webauthn_account`

```text
account_ref PK/FK
user_handle bytea(32) UNIQUE
```

User handle is random opaque state, not AccountRef/email/PersonRef.

### `dante.passkey_credential`

```text
passkey_credential_ref
account_ref
credential_id UNIQUE
credential_public_key
cose_algorithm
sign_count
backup_eligible / backup_state
transports
label
status active | revoked
created/updated/last-used/revocation timestamps
```

DANTE stores no private key, biometric template or device PIN. Removal is logical revoke so credential identity cannot be silently recycled.

### `dante.webauthn_challenge`

Bounded verifier-only ceremony state for registration/authentication/reauthentication with exact Account/AuthSession/user-handle binding where applicable.

## 11. Shared Email Platform persistence

The Email Platform is reusable DANTE infrastructure; Access/Auth is its first current consumer.

### `dante.email_delivery_intent`

Owns the durable decision to send one bounded message:

```text
UUIDv7 intent
purpose / stream / template revision
recipient snapshot + comparison key
operation_scope + idempotency_key
supersession key
payload fingerprint
short-lived protected payload bundle
eligibility / expiry
claim token + lease
attempt budget / retry schedule
accepted / terminal / wipe timestamps
```

Current Auth-security purposes:

```text
signup_verification
provider_enrollment_verification
password_recovery
password_reset_notification
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

One exact external attempt:

```text
email_attempt_ref
email_intent_ref
attempt_number
provider_code smtp | ses
started_at / finished_at
result_code
provider_message_id
error_code
```

Provider MessageId is correlation evidence, not canonical DANTE identity.

### `dante.email_provider_event`

Privacy-minimized normalized SES evidence:

```text
delivered
delivery_delayed
bounced
complained
rejected
```

Provider events are idempotent evidence rows; raw message content/provider payload is not retained.

### `dante.email_recipient_suppression`

Current operational hard-bounce/complaint suppression projection. It does not redefine EmailIdentity verification/ownership truth.

## 12. Email Platform DB doctrine

```text
feature state + EmailIntent atomically coordinated
provider network wait forbidden inside authoritative DB transaction
READ COMMITTED baseline
claim/lease uses short transactions + FOR UPDATE SKIP LOCKED
exact claim token required for finalize
same operation_scope/idempotency_key + same fingerprint = replay
same idempotency identity + different fingerprint = conflict
ambiguous external outcome is preserved explicitly
ambiguous outcome is not blindly retried
sensitive payload uses dedicated AES-256-GCM ring
terminal/unsafe state wipes sensitive payload
restored uncertain nonterminal work becomes recovery_quarantined before workers reopen
```

Email Platform state is technical delivery state and is **not MaterialState**.

## 13. Runtime ACL through `20260903_15`

Post-CP6 migrations own the exact runtime privileges required by their objects.

`20260903_15` specifically replaces broad Email lifecycle UPDATE capability with exact reviewed column-level UPDATE grants.

Applied revisions are immutable. Any future privilege correction uses a new forward migration.

## 14. Transaction / race doctrine

```text
READ COMMITTED
short authoritative transactions
network/provider/browser ceremony outside DB transaction
Account row serialization for Account-wide security mutation
constraints as final race arbiters
bounded claim/lease for email work
no blanket SERIALIZABLE
no blind mutation/send retry
ambiguous commit/effect handled by explicit reconciliation
```

## 15. Live UAT database evidence

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
post-reset session revocation
```

Final Email UAT observed three accepted intents:

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
provider_code = ses
result_code = provider_accepted
provider_message_id present
error_code NULL
sensitive bundle NULL
sensitive_wiped_at present
```

Personal mailbox/provider-subject values are intentionally excluded from repository documentation.

## 16. Cross-representation invariant

Current branch database acceptance requires:

```text
Dictionary
≈ SQLAlchemy mappings
≈ Alembic 20260903_15
≈ real PostgreSQL catalog
≈ this human reference
≈ direct tests
```

`apps/backend/tests/integration/database/test_current_catalog.py` proves current object-set/mapping/head parity against real PostgreSQL. Historical CP6 tests independently prove the frozen `20260826_08` baseline.

## 17. Pre-integration rule

Before main is merged, this document describes only branch-local Access/Auth + Email truth plus the exact protected-main divergence.

After main is merged:

```text
preserve Recovery revision
preserve Access/Auth/Email revisions
add forward Alembic merge revision
reconcile combined Dictionary/reference
re-run real PostgreSQL acceptance
```

Combined topology/counts are not accepted until that merged live proof exists.