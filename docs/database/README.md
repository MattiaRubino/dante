# DANTE Database System of Record

- **Status:** CURRENT / AUTHORITATIVE DATABASE REFERENCE / PRE-VERTICAL FINAL CANDIDATE
- **Last reconciled:** 2026-09-06
- **PostgreSQL:** 18.6
- **Protected-main Alembic head:** `20260904_17`
- **Pre-vertical candidate head:** `20260906_18`
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

A feature candidate may be newer than protected `main`, but candidate truth does not become protected-main truth until the exact candidate passes its applicable recovery/integration gates and is merged through the protected-main path.

## 2. Current migration graph

Recovery and Access/Auth originated as sibling children of `20260826_08`; both accepted histories are preserved. The pre-vertical foundation evolves forward from their protected-main merge head without rewriting either history:

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
        20260906_18 account_application_context   [pre-vertical candidate]
```

`20260904_17` is the protected-main no-DDL merge revision. `20260906_18` is the forward DDL candidate for authenticated DANTE application context. No accepted migration is rebased, renumbered or flattened.

## 3. Current topology

Protected-main baseline:

```text
88 tables
5 views
16 routines
76 triggers
172 physical indexes
89 foreign keys
270 CHECK constraints
```

Pre-vertical candidate:

```text
89 tables
5 views
18 routines
77 triggers
173 physical indexes
91 foreign keys
272 CHECK constraints
```

The candidate delta is exactly one `account_application_context` table, two routines, one trigger, one PK-backed index, two foreign keys and two CHECK constraints. It does not add enums/domains, sequences, materialized views, partitioning or RLS.

Dictionary, SQLAlchemy and Alembic on this candidate are authored against `20260906_18 / 89|5|18|77|173|91|272|0|0|0`.

Platform Observability does **not** add a DANTE business table, view, routine, Alembic revision or SQLAlchemy business mapping. Its database contribution is a provisioning-owned operational observer identity described below.

## 4. Acceptance boundary

Protected-main accepted database evidence remains:

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
Platform Observability PostgreSQL/ACL acceptance
```

The pre-vertical candidate has now passed the local real-PostgreSQL acceptance obligations for `20260906_18`:

```text
fresh/current migration paths                      PASS
Alembic currentness / drift checks                 PASS
Dictionary ↔ SQLAlchemy ↔ live catalog             PASS
live topology 89|5|18|77|173|91|272               PASS
runtime ACL: generic Person INSERT remains denied  PASS
bounded ensure_account_application_context         PASS
concurrent first-use/idempotence                    PASS
timezone policy integrity                           PASS
full PostgreSQL 18.6 marked suite                  PASS — 165 tests
```

The remaining database closure obligation is the **exact-head pre-vertical Recovery rehearsal under PV-03 C**, followed by protected-main PR gates and merge/readback. There is no PV-04.

Historical CP6, Recovery and Access/Auth checkpoints remain evidence in Git, archived branch records and dated validation records. They do not override either the protected-main baseline or the explicitly marked candidate above.

## 5. Application role model

Application roles remain explicitly separated:

```text
dante_owner      NOLOGIN ownership identity
dante_migrator   LOGIN migration identity
dante_runtime    LOGIN application runtime identity
```

Ownership, migration and runtime privileges remain independently tested. Application runtime does not inherit migration/owner authority.

The pre-vertical change does not grant generic runtime `INSERT` on `Person`. `dante_runtime` receives only the bounded capability needed to establish an absent authenticated Account application context; direct Person DML remains governed by the existing CP6 posture.

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

The candidate adds `dante.account_application_context` as the explicit application-facing bridge from one authenticated Account to its `self_person_ref` plus user/default timezone policy. It is not a generic user/profile/preferences framework and does not make Account a Domain native owner.

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

On the pre-vertical candidate the Dictionary describes `20260906_18 / 89|5|18|77|173|91|272`; protected-main accepted truth remains `20260904_17 / 88|5|16|76|172|89|270` until integration completes.

Operational cluster roles such as `dante_observer` are deliberately not fake business objects; their security contract is carried by technical-role/provisioning references and live ACL tests.

## 10. Recovery boundary

The accepted LOCAL recovery model keeps database-local proof distinct from application/Email reopen and from future production/cloud recovery.

```text
historical CP07 database-local reopen              PASS FOR EXECUTED HISTORICAL SCOPE
historical CP08 Email/application reopen            PASS FOR EXECUTED HISTORICAL SCOPE
pre-vertical candidate exact-head recovery          PENDING
remote backup provider                              TBD / NOT ACTIVATED
production/cloud recovery                           NOT CLAIMED
```

The historical PASS labels are not automatically inherited by `20260906_18`. Current operator authority is `../operations/postgres-recovery-runbook.md`; executable recovery truth lives under `../../infra/local/postgres/recovery/`.

## 11. Same-change rule

A structural database change is incomplete until the reviewed slice aligns semantic authority, forward Alembic, SQLAlchemy, Dictionary, current human reference, direct tests and real PostgreSQL proof.

For operational-role changes, the equivalent same-change rule applies to the database reference, provisioning, collector configuration and live privilege tests.

No future vertical may bypass these contracts merely because its data is “technical” or “observability” data.

## 12. Reachability rule

Until `20260906_18` is reachable from protected `main`, describe it as the pre-vertical candidate. After merge/readback, the same schema becomes current protected-main truth without rewriting historical acceptance evidence.
