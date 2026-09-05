# DANTE Database System of Record

- **Status:** CURRENT / AUTHORITATIVE DATABASE REFERENCE
- **Last reconciled:** 2026-09-05
- **PostgreSQL:** 18.6
- **Alembic head:** `20260904_17`
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

## 2. Current migration graph

Recovery and Access/Auth originated as sibling children of `20260826_08`; both accepted histories are preserved:

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

`20260904_17` is forward-only and performs no DDL. No accepted migration was rebased, renumbered or flattened.

## 3. Current topology

```text
88 tables
5 views
16 routines
76 triggers
172 physical indexes
89 foreign keys
270 CHECK constraints
```

The Dictionary, SQLAlchemy, Alembic and real PostgreSQL acceptance agree on this contract.

Platform Observability does **not** add a DANTE business table, view, routine, Alembic revision or SQLAlchemy business mapping. Its database contribution is a provisioning-owned operational observer identity described below.

## 4. Current acceptance boundary

Accepted database evidence includes:

```text
fresh DB → 20260904_17
20260904_16 → 20260904_17
20260830_09 → 20260904_17
head → base → head
Alembic check
Dictionary ↔ SQLAlchemy ↔ live catalog
owners / ACL
Recovery + Auth + Email behavior together
CP07 database-local recovery acceptance
CP08 Email/application reopen acceptance
Platform Observability PostgreSQL/ACL suite 155/155 PASS
```

Historical CP6, Recovery and Access/Auth topology checkpoints remain evidence in Git, archived branch records and dated validation records. They do not override the current topology above.

## 5. Application role model

Application roles remain explicitly separated:

```text
dante_owner      NOLOGIN ownership identity
dante_migrator   LOGIN migration identity
dante_runtime    LOGIN application runtime identity
```

Ownership, migration and runtime privileges remain independently tested. Application runtime does not inherit migration/owner authority.

## 6. Platform Observability observer role

<!-- DANTE-OBSERVABILITY-OBSERVER-README-ROUTING v1 -->

`dante_observer` is a provisioning-owned technical role for aggregate PostgreSQL operational statistics. It is not an Account, Principal, Actor, business entity, SQLAlchemy model or Alembic-managed application object.

Exact posture:

```text
LOGIN / INHERIT
NOSUPERUSER / NOCREATEDB / NOCREATEROLE / NOREPLICATION / NOBYPASSRLS
CONNECT dante
NO database CREATE / TEMP
search_path = pg_catalog
pg_read_all_stats membership only
NO dante/public schema usage
NO DANTE business-object privileges
NO DANTE application-role membership
```

The canonical detailed contract is in `dante-postgresql-database-part-12.md`, Section 46, marked by:

```text
<!-- DANTE-OBSERVABILITY-OBSERVER-CONTRACT v1 -->
```

Provisioning, live PostgreSQL tests and the Alloy/Postgres-exporter configuration must remain aligned with that contract. The observer credential is secret even though its authority is read-only statistics access.

## 7. Access/Auth persistence

Account is the durable security serialization root. Principal is runtime-derived. Provider identity authority is issuer+subject, never provider email. Password is optional; passkeys and external authenticators converge on canonical DANTE AuthSession.

## 8. Shared Email Platform persistence

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

## 9. Dictionary contract

`dictionary/scope.json` keeps the frozen CP6 baseline separate from `current_materialization`. Post-CP6 provenance lives on object entries rather than inventing fictitious CP6 stages.

The Dictionary describes the current business schema contract `20260904_17 / 88|5|16|76|172|89|270`. Operational cluster roles such as `dante_observer` are deliberately not fake business objects; their security contract is carried by the technical-role/provisioning references and live ACL tests.

## 10. Recovery boundary

The accepted LOCAL recovery model keeps database-local proof distinct from application/Email reopen and from future production/cloud recovery.

```text
CP07 database-local reopen                  PASS FOR EXECUTED SCOPE
CP08 Email/application reopen after PITR   PASS
remote backup provider                     TBD / NOT ACTIVATED
production/cloud recovery                  NOT CLAIMED
```

Current operator authority is `../operations/postgres-recovery-runbook.md` and executable recovery truth lives under `../../infra/local/postgres/recovery/`.

## 11. Same-change rule

A structural database change is incomplete until the reviewed slice aligns semantic authority, forward Alembic, SQLAlchemy, Dictionary, current human reference, direct tests and real PostgreSQL proof.

For operational-role changes, the equivalent same-change rule applies to the database reference, provisioning, collector configuration and live privilege tests.

No future vertical may bypass these contracts merely because its data is “technical” or “observability” data.
