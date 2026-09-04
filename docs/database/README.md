# DANTE Database System of Record

- **Status:** CURRENT / INTEGRATION CANDIDATE
- **Last reconciled:** 2026-09-04
- **PostgreSQL:** 18.6
- **Protected-main Alembic head:** `20260830_09`
- **Integration-candidate Alembic head:** `20260904_17`
- **Access/Auth reference:** `access-auth.md`
- **Shared Email Platform authority:** `../architecture/email-platform.md`
- **Persistence doctrine:** `../development/backend-cp6-02-postgresql-persistence-constitution.md`
- **Persistence ADR:** `../decisions/ADR-010-postgresql-persistence-constitution.md`

## 1. Authority model

```text
Product / Domain / Logical / Physical
→ PostgreSQL Persistence Constitution / ADR-010
→ current human DB reference + Dictionary semantic contract
→ Alembic forward evolution
→ SQLAlchemy mappings/MetaData
→ real PostgreSQL catalog
→ direct tests / recovery proof
```

Permanent invariant:

```text
CURRENT DB REFERENCE
≈ DATABASE DICTIONARY
≈ SQLALCHEMY
≈ ALEMBIC
≈ REAL POSTGRESQL
≈ DIRECT TESTS
```

## 2. Current migration graph

Protected main and Access/Auth originated as sibling children of `20260826_08`. The candidate preserves both histories:

```text
20260826_08
├── 20260830_09 recovery_material_state_retirement
└── 20260827_09 Account/Auth
    → 20260827_10 security lock
    → 20260829_11 signup/recovery
    → 20260830_12 multi-authenticator
    → 20260831_13 lifecycle ACL
    → 20260903_14 shared Email Platform
    → 20260903_15 Email ACL
    → 20260904_16 shared Email vocabulary

20260830_09 + 20260904_16
            ↓
        20260904_17
```

`20260904_17` is forward-only and performs no DDL.

## 3. Current candidate topology

```text
88 tables
5 views
16 routines
76 triggers
172 physical indexes
89 foreign keys
270 CHECK constraints
```

Frozen CP6 baseline remains:

```text
68 tables / 5 views / 14 routines
75 triggers / 95 indexes / 68 FKs / 120 CHECKs
```

## 4. Integration rule

Forbidden:

```text
rebase applied migration history
renumber applied revisions
change historical down_revision
copy one sibling branch's DDL into old migrations
stamp over missing history
flatten an accepted branch away
```

Required proof:

```text
fresh DB → 20260904_17
20260904_16 → 20260904_17
20260830_09 → 20260904_17
head → base → head
Alembic check
Dictionary ↔ SQLAlchemy ↔ live catalog
owners / ACL
Recovery + Auth + Email behavior together
```

## 5. Access/Auth persistence

Account is the durable security serialization root. Principal is runtime-derived. Provider identity authority is issuer+subject, never provider email. Password is optional; passkeys and external authenticators converge on canonical DANTE AuthSession.

## 6. Shared Email Platform persistence

```text
dante.email_delivery_intent
dante.email_delivery_attempt
dante.email_provider_event
dante.email_recipient_suppression
```

These are shared technical delivery structures, not Account semantic children and not MaterialState.

Core doctrine:

```text
feature mutation + EmailIntent atomically coordinated
provider network I/O after COMMIT
bounded idempotency / claim / lease
explicit ambiguous outcome
no blind retry after ambiguity
short-lived AES-256-GCM protected payload
terminal/unsafe-state wipe
provider evidence distinct from DANTE intent truth
suppression distinct from EmailIdentity ownership/verification
```

## 7. Dictionary contract

`dictionary/scope.json` keeps the CP6 `expected_baseline` frozen and uses `current_materialization` for the current combined inventory. `completed_stages` remains CP6 provenance only; post-CP6 provenance lives on each object entry.

## 8. Blueprint lifecycle

`dante-postgresql-database*.md` remains deep design/history/reference. Historical banners such as `CP6-03 ACTIVE`, `GATE NOT EARNED` or early object counts are checkpoint evidence and do not override this System of Record.

## 9. Same-change rule

A structural database change is incomplete until the reviewed slice aligns semantic authority, forward Alembic, SQLAlchemy, Dictionary, current human reference, direct tests and real PostgreSQL proof.
