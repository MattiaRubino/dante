# DANTE Access/Auth Database Reference

- **Status:** CURRENT ACCESS/AUTH REFERENCE / INTEGRATED; historical exact-head proof retained
- **Last reconciled:** 2026-09-18
- **PostgreSQL:** 18.6
- **Current protected-main Alembic head:** `20260906_18`
- **Access/Auth + Recovery integration baseline:** `20260904_17`
- **Access integration merge:** `5f76ec54ad78542f137e8730e904f805d9e59e56`
- **Accepted Access/Auth implementation proof HEAD:** `81639c61478b476c995652d0060dde8f53aef089`
- **Pre-vertical protected-main merge:** `1ecd58145860aebfaaa3dc1bd356b90f7a8eb19b`
- **Shared Email Platform:** `../architecture/email-platform.md`
- **Recovery runbook:** `../operations/postgres-recovery-runbook.md`
- **Whole-DB current authority:** `README.md`

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
Access/Auth+Recovery convergence _17   HISTORICAL EXACT INTEGRATION BASELINE
pre-vertical protected-main _18        CURRENT WHOLE-DB HEAD
CP07 enriched-baseline LOCAL recovery  PASS at historical exact head _17
real SES UAT                           PASS
real Google UAT                        PASS
real Windows Hello UAT                 PASS
Apple real external UAT                BOUNDED DEFERRED / NON-BLOCKING
post-merge Backend CI                  PASS
post-merge Frontend CI                 PASS
```

Current protected-main whole-DB catalog is owned by `docs/database/README.md` and currently equals:

```text
89 tables / 5 views / 18 routines / 77 triggers
173 physical indexes / 91 foreign keys / 272 CHECKs
Alembic 20260906_18
```

The Access/Auth exact integration proof itself remains `_17 / 88|5|16|76|172|89|270`; that historical evidence is not rewritten as if `_18` had been its exact test head.

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
20260904_17 → 20260906_18 pre-vertical foundation
```

No historical migration was rebased, renumbered or rewritten. Revision `20260904_17` performs no DDL; it joins the two accepted histories. The later pre-vertical foundation advances the whole protected-main database without invalidating the exact Access/Auth integration evidence.

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

The shared-ownership refactor is integrated; its architecture/replay/static/unit coverage and real PostgreSQL acceptance passed before merge and the exact Access/Auth merge commit passed real PostgreSQL and full frontend/backend push CI afterward.

## 6. Recovery interaction

Recovery `20260830_09` preserves the MaterialState retirement/anti-resurrection contract. Access/Auth and Email do not rewrite that history.

The 2026-09-04 CP07 rehearsal on implementation proof HEAD `81639c61478b476c995652d0060dde8f53aef089` proved the historical exact-head baseline:

```text
Alembic head                                  20260904_17
accepted topology                             88|5|16|76|172|89|270|0|0|0
A before target / B after target              PASS
old protected X physical resurrection         PROVEN
suppression-ledger reconciliation             PASS
payload reinsertion after retirement           REJECTED
DATABASE LOCAL REOPEN                         PASS
```

Remote backup provider remains `TBD / NOT ACTIVATED`; production/cloud recovery is not claimed. Current restore acceptance must additionally reconcile to the then-current whole-DB head/topology rather than treating historical `_17` as forever-current.

## 7. Cross-representation invariant

For the Access/Auth integration baseline:

```text
Access/Auth Dictionary objects
≈ SQLAlchemy mappings
≈ accepted Alembic integration baseline 20260904_17
≈ real PostgreSQL proof at that baseline
≈ Access/Auth + Email direct tests
```

For current whole-DB topology/head, `docs/database/README.md` and the current Dictionary/Alembic/catalog are authoritative. Historical CP6 and Access/Auth proof heads remain evidence, not current topology banners.

## 8. Protected-main integration disposition

The Access/Auth integration is **CLOSED / INTEGRATED / POST-MERGE CI PASS**.

```text
implementation proof HEAD                 81639c61478b476c995652d0060dde8f53aef089
final candidate HEAD                      6cee5506d404d0684b0679aca54c03f0ca433c72
PR                                        #52
Access/Auth protected-main merge          5f76ec54ad78542f137e8730e904f805d9e59e56
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
