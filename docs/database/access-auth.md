# DANTE Access/Auth Database Reference

- **Status:** CURRENT / PROTECTED MAIN / M3–M5 + EMAIL + RECOVERY INTEGRATED
- **Last reconciled:** 2026-09-04
- **PostgreSQL:** 18.6
- **Protected-main Alembic head:** `20260904_17`
- **Access integration merge:** `5f76ec54ad78542f137e8730e904f805d9e59e56`
- **Accepted implementation proof HEAD:** `81639c61478b476c995652d0060dde8f53aef089`
- **Shared Email Platform:** `../architecture/email-platform.md`
- **Recovery runbook:** `../operations/postgres-recovery-runbook.md`

## 1. Evidence state

```text
M3 persistence                         MATERIALIZED / PG PROVEN / INTEGRATED
M4 persistence                         MATERIALIZED / PG PROVEN / INTEGRATED
M5 multi-authenticator persistence     MATERIALIZED / PG PROVEN / INTEGRATED
M5 application/API/Web                 CLOSED / INTEGRATED
Shared Email Platform                  CLOSED / INTEGRATED
shared-ownership refactor              STATIC + UNIT + PG + CI PASS
Email vocabulary hardening 16          PG PROVEN / INTEGRATED
Recovery 20260830_09                   INTEGRATED
Alembic convergence 20260904_17        CURRENT PROTECTED-MAIN HEAD
CP07 enriched-baseline LOCAL recovery  PASS
real SES UAT                           PASS
real Google UAT                        PASS
real Windows Hello UAT                 PASS
Apple real external UAT                BOUNDED DEFERRED / NON-BLOCKING
post-merge Backend CI                  PASS
post-merge Frontend CI                 PASS
```

Current protected-main catalog:

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

No historical migration was rebased, renumbered or rewritten. Revision `20260904_17` performs no DDL; it joins the two accepted histories.

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

The persistence layer admits bounded shared stream/purpose identifiers; Access/Auth's adapter owns the `auth_security` vocabulary and four current Auth purposes.

The shared-ownership refactor is integrated on protected `main`; its architecture/replay/static/unit coverage and real PostgreSQL acceptance passed before merge and the exact protected-main merge commit passed real PostgreSQL and full frontend/backend push CI afterward.

## 6. Recovery interaction

Recovery `20260830_09` preserves the MaterialState retirement/anti-resurrection contract. Access/Auth and Email do not rewrite that history.

The 2026-09-04 CP07 rehearsal on implementation proof HEAD `81639c61478b476c995652d0060dde8f53aef089` proved:

```text
Alembic head                                  20260904_17
accepted topology                             88|5|16|76|172|89|270|0|0|0
A before target / B after target              PASS
old protected X physical resurrection         PROVEN
suppression-ledger reconciliation             PASS
payload reinsertion after retirement          REJECTED
DATABASE LOCAL REOPEN                         PASS
```

Remote backup provider remains `TBD / NOT ACTIVATED`; production/cloud recovery is not claimed.

## 7. Cross-representation invariant

```text
Dictionary
≈ SQLAlchemy mappings
≈ Alembic 20260904_17
≈ real PostgreSQL catalog
≈ current human DB references
≈ Recovery + Access/Auth + Email direct tests
```

Historical CP6 tests independently prove the frozen `20260826_08` baseline.

## 8. Protected-main integration disposition

The integration is **CLOSED / INTEGRATED / POST-MERGE CI PASS**.

```text
implementation proof HEAD                 81639c61478b476c995652d0060dde8f53aef089
final candidate HEAD                      6cee5506d404d0684b0679aca54c03f0ca433c72
PR                                        #52
protected-main merge                      5f76ec54ad78542f137e8730e904f805d9e59e56
merge tree                                identical to final candidate
post-merge Backend Quality                PASS
post-merge Backend PostgreSQL             PASS
post-merge Backend CI Gate                PASS
post-merge Frontend Quality               PASS
post-merge Web E2E                        PASS
post-merge Mobile Bundle                  PASS
post-merge Frontend CI Gate               PASS
```

There is no remaining Access/Auth database integration procedure. No M6/M7 feature scope belongs in this closed workstream; future work starts from then-current protected `main`.
