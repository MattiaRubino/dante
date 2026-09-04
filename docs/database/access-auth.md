# DANTE Access/Auth Database Reference

- **Status:** CURRENT / INTEGRATION CANDIDATE / M3–M5 + EMAIL + RECOVERY MATERIALIZED
- **Last reconciled:** 2026-09-04
- **PostgreSQL:** 18.6
- **Candidate Alembic head:** `20260904_17`
- **Protected-main Alembic head:** `20260830_09`
- **Shared Email Platform:** `../architecture/email-platform.md`

## 1. Evidence state

```text
M3 persistence                         MATERIALIZED / PG PROVEN / CLOSED
M4 persistence                         MATERIALIZED / PG PROVEN / CLOSED
M5 multi-authenticator persistence     MATERIALIZED / PG PROVEN / CLOSED
M5 application/API/Web                 CLOSED / ACCEPTED
Shared Email Platform                  CLOSED / ACCEPTED
shared-ownership refactor              PRE-INTEGRATION STATIC + PG PASS
Email vocabulary hardening 16          PG PROVEN
Recovery 20260830_09                   MERGED INTO CANDIDATE
Alembic convergence 20260904_17        IMPLEMENTED / COMBINED QA ACTIVE
real SES UAT                           PASS
real Google UAT                        PASS
real Windows Hello UAT                 PASS
Apple real external UAT                BOUNDED DEFERRED / NON-BLOCKING
```

Current candidate catalog:

```text
88 tables / 5 views / 16 routines / 76 triggers
172 physical indexes / 89 foreign keys / 270 CHECKs
```

## 2. Migration relationship

```text
20260826_08
├── 20260830_09 Recovery
└── 20260827_09
    → 20260827_10
    → 20260829_11
    → 20260830_12
    → 20260831_13
    → 20260903_14
    → 20260903_15
    → 20260904_16 Access/Auth + Email

20260830_09 + 20260904_16 → 20260904_17
```

No historical migration was rebased, renumbered or rewritten.

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
```

Shared delivery infrastructure:

```text
EmailDeliveryIntent
EmailDeliveryAttempt
EmailProviderEvent
EmailRecipientSuppression
```

Those four structures are shared Email Platform state, not semantic Account children.

## 4. Frozen security rules

```text
Account != Person
provider identity = issuer + subject
provider email never silently links Accounts
opaque DANTE AuthSession bearer; verifier only in DB
reset revokes sessions and does not auto-login
password is optional
passkey private key / biometric / PIN never stored by DANTE
Account-wide security mutation serializes on the Account security root
```

## 5. Shared Email persistence doctrine

```text
feature mutation + EmailIntent in one PostgreSQL transaction
provider I/O only after commit
READ COMMITTED baseline
bounded claim/lease + FOR UPDATE SKIP LOCKED
exact claim token to finalize
full immutable idempotency identity on replay
ambiguous provider outcome explicitly preserved
no blind retry after ambiguity
AES-256-GCM dedicated Email key ring + AAD
terminal/unsafe-state sensitive wipe
restored uncertain work → recovery_quarantined
```

The persistence layer admits bounded shared stream/purpose identifiers; Access/Auth's own adapter owns the `auth_security` vocabulary and four current Auth purposes.

## 6. Cross-representation invariant

```text
Dictionary
≈ SQLAlchemy mappings
≈ Alembic 20260904_17
≈ real PostgreSQL catalog
≈ current human DB references
≈ Recovery + Access/Auth + Email direct tests
```

Historical CP6 tests independently prove the frozen `20260826_08` baseline.

## 7. Current acceptance gate

```text
fresh DB → merged head
Access head → merged head
Recovery head → merged head
head → base → head
Alembic drift
Dictionary/mapping/catalog/ACL parity
Recovery regression
Access/Auth regression
Email Platform regression
```

No M6/M7 feature scope belongs in this integration candidate.
