# DANTE Database System of Record

- **Status:** CURRENT / INTEGRATION CANDIDATE / COMBINED QA PASS
- **Last reconciled:** 2026-09-04
- **PostgreSQL:** 18.6
- **Protected-main Alembic head:** `20260830_09`
- **Integration-candidate Alembic head:** `20260904_17`
- **Accepted candidate proof HEAD:** `81639c61478b476c995652d0060dde8f53aef089`
- **Access/Auth reference:** `access-auth.md`
- **Shared Email Platform authority:** `../architecture/email-platform.md`
- **Recovery operator authority:** `../operations/postgres-recovery-runbook.md`
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

Protected `main` remains Recovery-only until PR #52 lands. The accepted integration candidate is the current forward database contract for the pending protected-main integration; candidate truth must not be mislabeled as already merged main truth.

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

## 3. Accepted candidate topology

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
68 tables / 5 views / 14 routines / 75 triggers
95 indexes / 68 FKs / 120 CHECKs
```

Protected-main Recovery-only historical/current-before-merge topology remains:

```text
20260830_09
69 tables / 5 views / 15 routines / 76 triggers
97 indexes / 69 FKs / 123 CHECKs
```

That Recovery-only topology is not the accepted integration-candidate topology.

## 4. Combined acceptance proof

On exact candidate proof HEAD `81639c61478b476c995652d0060dde8f53aef089`:

```text
Backend Quality         PASS
Backend PostgreSQL      PASS
Backend CI Gate         PASS
Frontend CI             PASS
Dependency Review       PASS
```

The 2026-09-04 CP07 whole LOCAL operator recovery rehearsal independently observed during restore acceptance:

```text
PostgreSQL              18.6
Alembic                 20260904_17
topology                88|5|16|76|172|89|270|0|0|0
A present / B absent    PASS
old X resurrection      PROVEN
ledger reconciliation  PASS
payload reinsertion    REJECTED
DATABASE LOCAL REOPEN   PASS
```

Derived/object gates were `NOT_ACTIVATED / NO FALSE PASS`. Remote backup provider remained `TBD / NOT ACTIVATED`; production/cloud recovery was not claimed.

Durable evidence: `../workstreams/access-auth-integration-acceptance-2026-09-04.md`.

## 5. Integration rule

Forbidden:

```text
rebase applied migration history
renumber applied revisions
change historical down_revision
copy one sibling branch's DDL into old migrations
stamp over missing history
flatten an accepted branch away
```

Accepted proof on the candidate includes:

```text
fresh DB → 20260904_17
20260904_16 → 20260904_17
20260830_09 → 20260904_17
head → base → head
Alembic check
Dictionary ↔ SQLAlchemy ↔ live catalog
owners / ACL
Recovery + Auth + Email behavior together
CP07 enriched-baseline recovery acceptance
```

If protected `main` changes before merge, this acceptance must be re-evaluated against the new base. Any database/recovery-contract delta requires the affected real-PostgreSQL gates and CP07 to be rerun.

## 6. Access/Auth persistence

Account is the durable security serialization root. Principal is runtime-derived. Provider identity authority is issuer+subject, never provider email. Password is optional; passkeys and external authenticators converge on canonical DANTE AuthSession.

## 7. Shared Email Platform persistence

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

The shared-ownership refactor and forward shared-vocabulary migration `20260904_16` are accepted on the current candidate through static/unit/PostgreSQL regression and exact-HEAD CI.

## 8. Dictionary contract

`dictionary/scope.json` keeps the CP6 `expected_baseline` frozen and uses `current_materialization` for the accepted combined candidate inventory. `completed_stages` remains CP6 provenance only; post-CP6 provenance lives on each object entry.

The Dictionary currently describes the candidate contract `20260904_17 / 88|5|16|76|172|89|270`. After PR #52 lands, only the lifecycle label changes from integration-candidate truth to protected-main truth; object semantics/counts do not change unless the merge result itself differs and is revalidated.

## 9. Blueprint lifecycle

`dante-postgresql-database-part-*.md` retains detailed design/reference history. Historical banners such as `CP6-03 ACTIVE`, `GATE NOT EARNED` or early object counts are checkpoint evidence and do not override this System of Record or `dante-postgresql-database.md` current sections.

## 10. Same-change rule

A structural database change is incomplete until the reviewed slice aligns semantic authority, forward Alembic, SQLAlchemy, Dictionary, current human reference, direct tests and real PostgreSQL proof.

A branch integration is incomplete until the accepted candidate state is also reflected consistently in the current DB reference, recovery runbook and project/workstream status without rewriting historical evidence.
