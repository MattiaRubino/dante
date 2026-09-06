# DANTE Database System of Record

- **Status:** CURRENT / AUTHORITATIVE DATABASE REFERENCE
- **Last reconciled:** 2026-09-06
- **PostgreSQL:** 18.6
- **Protected-main Alembic head:** `20260906_18`
- **Protected-main topology:** `89|5|18|77|173|91|272|0|0|0`
- **Pre-vertical integration:** PR #66 / merge `1ecd58145860aebfaaa3dc1bd356b90f7a8eb19b`
- **Authenticated DANTE context authority:** `../architecture/authenticated-dante-context.md`
- **Access/Auth reference:** `access-auth.md`
- **Shared Email Platform authority:** `../architecture/email-platform.md`
- **Recovery operator authority:** `../operations/postgres-recovery-runbook.md`
- **Persistence doctrine:** `../development/backend-cp6-02-postgresql-persistence-constitution.md`
- **Persistence ADR:** `../decisions/ADR-010-postgresql-persistence-constitution.md`
- **Pre-vertical closure:** `../workstreams/pre-vertical-foundation-closure-2026-09-06.md`

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

Protected `main` is the integration authority. Candidate truth becomes protected-main truth only after its applicable exact-head recovery/integration gates and protected-main merge/readback.

## 2. Current migration graph

Recovery and Access/Auth originated as sibling children of `20260826_08`; both accepted histories are preserved. The pre-vertical foundation evolved forward from their protected-main merge head without rewriting either history:

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
            ↓
        20260906_18 account_application_context   [current protected-main head]
```

`20260904_17` is the accepted no-DDL merge revision. `20260906_18` is the current protected-main DDL head for authenticated DANTE application context. No accepted migration was rebased, renumbered or flattened.

## 3. Current topology

Current protected-main topology:

```text
89 tables
5 views
18 routines
77 triggers
173 physical indexes
91 foreign keys
272 CHECK constraints
0 enums/domains
0 sequences
0 materialized views
0 partitioned tables
0 RLS policies
```

The pre-vertical delta over the former `20260904_17 / 88|5|16|76|172|89|270|0|0|0` baseline is exactly one `account_application_context` table, two routines, one trigger, one PK-backed index, two foreign keys and two CHECK constraints.

Dictionary, SQLAlchemy and Alembic are aligned against `20260906_18 / 89|5|18|77|173|91|272|0|0|0`.

Platform Observability does **not** add a DANTE business table, view, routine, Alembic revision or SQLAlchemy business mapping. Its database contribution is a provisioning-owned operational observer identity described below.

## 4. Acceptance boundary

Current protected-main database acceptance includes:

```text
fresh/current migration paths                      PASS
head → base → head where semantically valid        PASS
Alembic currentness / drift checks                 PASS
Dictionary ↔ SQLAlchemy ↔ live catalog             PASS
live topology 89|5|18|77|173|91|272               PASS
owners / ACL                                       PASS
runtime ACL: generic Person INSERT remains denied  PASS
bounded ensure_account_application_context         PASS
concurrent first-use/idempotence                    PASS
timezone policy integrity                           PASS
full PostgreSQL 18.6 marked suite                  PASS — 165 tests
exact-head pre-vertical LOCAL Recovery             PASS
Backend CI Gate                                    PASS
Dependency Review                                  PASS
Frontend CI Gate                                   PASS
protected-main merge/readback                      PASS
```

The exact recovery candidate was `21353469464f1371f9913dc78933f4ee42698f33`; PR #66 integrated it through merge `1ecd58145860aebfaaa3dc1bd356b90f7a8eb19b`.

Historical CP6, Recovery and Access/Auth checkpoints remain evidence in Git, archived branch records and dated validation records. They do not override current protected-main truth.

## 5. Application role model

Application roles remain explicitly separated:

```text
dante_owner      NOLOGIN ownership identity
dante_migrator   LOGIN migration identity
dante_runtime    LOGIN application runtime identity
dante_observer   LOGIN statistics-only collector identity
```

Ownership, migration and runtime privileges remain independently tested. Application runtime does not inherit migration/owner authority.

`20260906_18` does not grant generic runtime `INSERT` on `Person`. `dante_runtime` receives only the bounded capability needed to establish an absent authenticated Account application context; direct Person DML remains governed by the existing CP6 posture.

## 6. Platform Observability observer role

<!-- DANTE-OBSERVABILITY-OBSERVER-README-ROUTING v1 -->

`dante_observer` is a provisioning-owned technical role for aggregate PostgreSQL operational statistics. It is not an Account, Principal, Actor, business entity, SQLAlchemy model or Alembic-managed application object.

Exact posture:

```text
LOGIN / NOINHERIT
NOSUPERUSER / NOCREATEDB / NOCREATEROLE / NOREPLICATION / NOBYPASSRLS
CONNECT dante
NO database CREATE / TEMP
search_path = pg_catalog
pg_read_all_stats membership only (INHERIT TRUE / SET FALSE / ADMIN FALSE)
NO dante/public schema usage
NO DANTE business-object privileges
NO DANTE application-role membership
```

The canonical detailed contract is in `dante-postgresql-database-part-12.md`, Section 46, marked by:

```text
<!-- DANTE-OBSERVABILITY-OBSERVER-CONTRACT v1 -->
```

Provisioning, live PostgreSQL tests and the Alloy/Postgres-exporter configuration must remain aligned with that contract. The observer credential is secret even though its authority is read-only statistics access.

## 7. Access/Auth and authenticated DANTE context persistence

Account is the durable security serialization root. Principal is runtime-derived. Provider identity authority is issuer+subject, never provider email. Password is optional; passkeys and external authenticators converge on canonical DANTE AuthSession.

The permanent distinction remains:

```text
Person != Account != Principal != Actor
AuthSession != DANTE Session
```

`dante.account_application_context` is the explicit application-facing bridge from one authenticated Account to its `self_person_ref` plus user/default timezone policy. It is not a generic user/profile/preferences framework and does not make Account a Domain native owner.

Detailed authority: `../architecture/authenticated-dante-context.md`.

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

Current materialization is `20260906_18 / 89|5|18|77|173|91|272`. The former protected-main `20260904_17 / 88|5|16|76|172|89|270` is retained only as historical integration context.

Operational cluster roles such as `dante_observer` are deliberately not fake business objects; their security contract is carried by technical-role/provisioning references and live ACL tests.

## 10. Recovery boundary

The accepted LOCAL recovery model keeps database-local proof distinct from application/Email reopen and from future production/cloud recovery.

```text
historical CP07 database-local reopen              PASS FOR EXECUTED HISTORICAL SCOPE
historical CP08 Email/application reopen            PASS FOR EXECUTED HISTORICAL SCOPE
pre-vertical exact-head database-local recovery     PASS @ 21353469464f1371f9913dc78933f4ee42698f33
remote backup provider                              TBD / NOT ACTIVATED
production/cloud recovery                           NOT CLAIMED
```

The final pre-vertical rehearsal proved the current `20260906_18` database-local Recovery contract, including observer provisioning, structural/security acceptance, deterministic PITR, MaterialState anti-resurrection reconciliation and database-local reopen. It did **not** silently relabel historical CP08 application/Email reopen evidence as newly executed.

Current operator authority is `../operations/postgres-recovery-runbook.md`; executable recovery truth lives under `../../infra/local/postgres/recovery/`.

## 11. Same-change rule

A structural database change is incomplete until the reviewed slice aligns semantic authority, forward Alembic, SQLAlchemy, Dictionary, current human reference, direct tests and real PostgreSQL proof.

For operational-role changes, the equivalent same-change rule applies to the database reference, provisioning, collector configuration and live privilege tests.

No future vertical may bypass these contracts merely because its data is “technical” or “observability” data.

## 12. Reachability rule

`20260906_18` is reachable from protected `main` through PR #66 and is current protected-main truth. Future candidate schema changes remain candidates until their own reviewed integration/recovery obligations are complete.
