# DANTE Access/Auth Database Reference

- **Status:** CURRENT / BRANCH-LOCAL / M3–M5 MATERIALIZED
- **Last reconciled:** 2026-09-02
- **Branch:** `feature/access-auth`
- **PostgreSQL:** 18.6
- **Current accepted Alembic head:** `20260831_13`
- **Protected-main CP6 baseline:** `20260826_08`
- **Database System of Record:** `README.md`
- **M5 architecture:** `../architecture/access-auth-m5-contract.md`
- **Exact M5 design:** `../architecture/access-auth-m5-persistence-api-contract.md`
- **Security:** `../architecture/access-auth-security-contract.md`

## 1. Current evidence state

```text
M3 persistence                    MATERIALIZED / PG PROVEN / CLOSED
M4 persistence                    MATERIALIZED / PG PROVEN / CLOSED
M5.1 / M5.2                       COMPLETE
M5-A persistence                  MATERIALIZED / PG PROVEN
M5-B–D + Groups 1–3               APPLICATION/API ENGINEERING PASS
20260831_13 lifecycle ACL          ACCEPTED
Group-4 Web                       NO DB TOPOLOGY DELTA
manual passkey/Google DB UAT       PASS
```

Current catalog:

```text
83 tables / 5 views / 15 routines / 75 triggers
156 physical indexes / 85 foreign keys / 233 CHECKs
103 standalone Dictionary entries
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

Passwordless Accounts are first-class. Group 1 lifecycle now supports add/remove password under recent-auth + anti-lockout policy; this is no longer future-only behavior.

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

## 7. Signup / recovery challenges

`password_signup_challenge` owns anonymous/pre-Account password signup state and verifier-only OTP evidence.

`password_recovery_challenge` owns one-use high-entropy recovery proof bound to the exact Account/EmailIdentity. Recovery can create the first PasswordCredential for a passwordless Account or replace an existing credential, revokes prior sessions and requires fresh signin.

## 8. `dante.external_identity`

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

## 9. Provider transaction/collision state

`external_auth_transaction` is the bounded server-authoritative sign-in/link/reauth transaction with verifier-only state/nonce and optional exact AuthSession bearer snapshot.

`external_link_challenge` prevents silent email merge and carries bounded explicit link continuation.

`external_signup_challenge` carries provider evidence that still requires direct DANTE mailbox proof before Account creation.

No Account is created before the accepted proof set.

## 10. `dante.account_profile_bootstrap`

One-shot, non-canonical provider bootstrap staging for useful first-account data such as name/locale/picture hint. Later provider login does not continuously overwrite DANTE-owned profile values.

## 11. `dante.apple_auth_grant`

Durable encrypted Apple server-side grant lifecycle:

```text
pending → active → revocation_pending → revoked
```

Refresh-token material is application-layer AEAD encrypted with key material outside PostgreSQL/Git/logs. Local provider revoke precedes remote revoke so provider outage does not keep local authentication active.

## 12. WebAuthn persistence

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

## 13. Runtime ACL / `20260831_13`

`20260831_13` grants only the bounded runtime operations required by the accepted authenticator lifecycle. It does not change the 83-table M5 topology and does not relax the general deny-by-default runtime posture.

## 14. Transaction/race doctrine

```text
READ COMMITTED
short authoritative transactions
network/provider/browser ceremony outside DB transaction
Account security lock for Account-wide mutation
constraints as final race arbiters
no blanket SERIALIZABLE
no blind mutation retry
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
```

Personal email/provider subject values are intentionally excluded from repository documentation.

## 16. Current source relationship

Detailed exact constraint/FK/ACL rationale remains recoverable in the M5 persistence/API contract, Dictionary, SQLAlchemy mappings, Alembic and direct tests. Where an older milestone section says `M5-B NEXT` or `20260830_12 current`, that is historical progress metadata; this file owns current Access/Auth DB reference state.