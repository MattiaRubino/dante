# DANTE Database System of Record

- **Status:** CURRENT / CP6 CLOSED ON `main` / ACCESS-AUTH DB MATERIALIZED THROUGH M5
- **Last reconciled:** 2026-09-02
- **PostgreSQL:** 18.6
- **Current accepted Access/Auth Alembic head:** `20260831_13`
- **Protected-main CP6 baseline:** `20260826_08`
- **Current Access/Auth reference:** `access-auth.md`
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

M3:

```text
20260827_09  Account / EmailIdentity / PasswordCredential / AuthSession
20260827_10  bounded Account security-lock capability
```

M4:

```text
20260829_11  signup/recovery challenges + lifecycle ACL
```

M5:

```text
20260830_12  ExternalIdentity/provider/Apple/WebAuthn/passkey persistence
20260831_13  bounded authenticator-lifecycle runtime ACL follow-up
```

Current branch catalog:

```text
PostgreSQL          18.6
Alembic             20260831_13
83 tables
5 views
15 routines
75 triggers
156 physical indexes
85 foreign keys
233 CHECK constraints
103 standalone Dictionary entries
```

`20260831_13` changes bounded runtime ACL capability and does not change the M5-A topology counts.

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

## 4. Security/ownership rules

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
```

## 5. Transaction doctrine

```text
READ COMMITTED
short authoritative transactions
network/provider/WebAuthn wait outside DB transaction
Account lock only for Account-wide security mutation
no blanket SERIALIZABLE
no blind mutation retry
ambiguous commit handled by operation-specific reconciliation
```

## 6. Same-change database rule

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

## 7. Current proof

M5 persistence/API/backend suites previously closed against real PostgreSQL. Group-4 Web/UAT introduced no new schema topology. Live UAT direct DB inspection additionally confirmed passkey lifecycle state and a passwordless Google-created Account with verified EmailIdentity, active ExternalIdentity and active AuthSession.

## 8. Documentation

- `access-auth.md` — current Access/Auth object semantics
- `dictionary/README.md` — structured Dictionary contract
- `../architecture/access-auth-m5-persistence-api-contract.md` — detailed exact M5 design/milestone reconciliation
- `../workstreams/access-auth-m5-review-2026-09-02.md` — current UAT/review evidence

Old `M5-B NEXT`/`20260830_12 current` progress labels in historical snapshots are superseded by this current reference.