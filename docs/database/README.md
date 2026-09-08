# DANTE Database System of Record

- **Status:** CURRENT / AUTHORITATIVE DATABASE REFERENCE
- **Last reconciled:** 2026-09-08
- **PostgreSQL:** 18.6
- **Protected-main Alembic head:** `20260906_18`
- **Protected-main topology:** `89|5|18|77|173|91|272|0|0|0`
- **Timeline candidate branch:** `feature/timeline-temporal-operational`
- **Timeline candidate Alembic head:** `20260908_19`
- **Timeline candidate topology:** `91|5|19|77|177|95|275|0|0|0`
- **Pre-vertical integration:** PR #66 / merge `1ecd58145860aebfaaa3dc1bd356b90f7a8eb19b`
- **Authenticated DANTE context authority:** `../architecture/authenticated-dante-context.md`
- **Access/Auth reference:** `access-auth.md`
- **Shared Email Platform authority:** `../architecture/email-platform.md`
- **Recovery operator authority:** `../operations/postgres-recovery-runbook.md`
- **Persistence doctrine:** `../development/backend-cp6-02-postgresql-persistence-constitution.md`
- **Persistence ADR:** `../decisions/ADR-010-postgresql-persistence-constitution.md`
- **Pre-vertical closure:** `../workstreams/pre-vertical-foundation-closure-2026-09-06.md`
- **Timeline workstream authority:** `../workstreams/timeline-temporal-operational-map.md`

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

Protected `main` is the integration authority. Candidate truth becomes protected-main truth only after its applicable exact-head workstream/recovery/integration gates and protected-main merge/readback.

Therefore this document intentionally carries both:

```text
protected-main truth
!=
current unmerged Timeline candidate truth
```

The candidate overlay is recorded so the checked-out feature branch can remain internally coherent without falsely rewriting protected-main status.

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
            ↓
        20260908_19 activity_core                 [Timeline candidate only]
```

`20260904_17` is the accepted no-DDL merge revision. `20260906_18` is the current protected-main DDL head for authenticated DANTE application context. `20260908_19` is a forward-only candidate child on `feature/timeline-temporal-operational`; it has not become protected-main authority.

No accepted migration was rebased, renumbered or flattened.

## 3. Current topology

### 3.1 Protected-main truth

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

Protected-main Dictionary, SQLAlchemy and Alembic remain aligned against `20260906_18 / 89|5|18|77|173|91|272|0|0|0`.

### 3.2 Timeline B01 candidate truth

The checked-out workstream candidate adds exactly:

```text
dante.activity_intention
dante.activity_create_operation
dante.create_self_activity(uuid,text,text,uuid,text)
```

Candidate topology:

```text
91 tables
5 views
19 routines
77 triggers
177 physical indexes
95 foreign keys
275 CHECK constraints
0 enums/domains
0 sequences
0 materialized views
0 partitioned tables
0 RLS policies
```

Exact `_18 → _19` delta:

```text
+2 tables
+1 routine
+0 triggers
+4 indexes
+4 foreign keys
+3 CHECK constraints
```

`dante.activity` remains the single CP6 Activity NativeRef owner. `activity_intention` is the smallest typed B01 dependent canonical descriptor required by the product slice; `activity_create_operation` is immutable operation-control state; `create_self_activity` is a bounded capability surface. None authorizes a generic Task/status model or a second Activity identity.

Platform Observability does **not** add a DANTE business table, view, routine, Alembic revision or SQLAlchemy business mapping. Its database contribution is a provisioning-owned operational observer identity described below.

## 4. Acceptance boundary

### 4.1 Protected-main accepted boundary

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

### 4.2 Timeline B01 candidate boundary

At this reconciliation slice the `_19` candidate must prove, before formal B01 green:

```text
single repository Alembic head = 20260908_19
Dictionary object tree/counts = live PostgreSQL catalog
SQLAlchemy mappings = all 91 DANTE tables
candidate topology = 91|5|19|77|177|95|275|0|0|0
runtime table ACL = Dictionary
create_self_activity owner/security/search_path/EXECUTE = exact
fresh DB → head = PASS
head → base → head = PASS when no canonical B01 data exists
canonical Activity intention → downgrade to _18 = REJECTED
B00/B01 real PostgreSQL integration = PASS
full backend PostgreSQL marked suite = PASS
```

The one-shot candidate workflow created in this workstream is temporary QA infrastructure only. Until that exact-head run succeeds, the statements above are obligations, not claimed evidence.

Automated candidate green also does not replace B00/B01 manual `userTest` approval.

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

The B01 `_19` candidate likewise grants no generic runtime INSERT/UPDATE/DELETE on Activity persistence. Runtime receives:

```text
SELECT  dante.activity_intention
EXECUTE dante.create_self_activity(uuid,text,text,uuid,text)
```

and no direct table privilege on `activity_create_operation`. The SECURITY DEFINER function is owned by `dante_owner`, uses trusted `search_path = pg_catalog, dante, pg_temp`, and is the only B01 Activity creation write surface granted to runtime.

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

On protected `main`, materialization remains `20260906_18 / 89|5|18|77|173|91|272`.

On the current Timeline candidate branch, checked-out Dictionary materialization is `20260908_19 / 91|5|19|77|177|95|275`. The candidate entries for `activity_intention`, `activity_create_operation` and `create_self_activity` must match SQLAlchemy/Alembic/live PostgreSQL exactly before this slice can close.

Operational cluster roles such as `dante_observer` are deliberately not fake business objects; their security contract is carried by technical-role/provisioning references and live ACL tests.

## 10. Recovery boundary

The accepted LOCAL recovery model keeps database-local proof distinct from application/Email reopen and from future production/cloud recovery.

```text
historical CP07 database-local reopen              PASS FOR EXECUTED HISTORICAL SCOPE
historical CP08 Email/application reopen            PASS FOR EXECUTED HISTORICAL SCOPE
pre-vertical exact-head database-local recovery     PASS @ 21353469464f1371f9913dc78933f4ee42698f33
Timeline B01 _19 recovery-specific rerun             NOT CLAIMED BY THIS SLICE
remote backup provider                              TBD / NOT ACTIVATED
production/cloud recovery                           NOT CLAIMED
```

The final pre-vertical rehearsal proved the protected-main `20260906_18` database-local Recovery contract, including observer provisioning, structural/security acceptance, deterministic PITR, MaterialState anti-resurrection reconciliation and database-local reopen. It did **not** silently relabel historical CP08 application/Email reopen evidence as newly executed.

B01 adds two canonical/control tables and one bounded routine but no new MaterialState retirement facet, outbox family or provider/object-store state. Whole-vertical recovery closure remains B14; no new recovery proof is fabricated here.

Current operator authority is `../operations/postgres-recovery-runbook.md`; executable recovery truth lives under `../../infra/local/postgres/recovery/`.

## 11. Same-change rule

A structural database change is incomplete until the reviewed slice aligns semantic authority, forward Alembic, SQLAlchemy, Dictionary, current human reference, direct tests and real PostgreSQL proof.

For operational-role changes, the equivalent same-change rule applies to the database reference, provisioning, collector configuration and live privilege tests.

No future vertical may bypass these contracts merely because its data is “technical” or “observability” data.

## 12. Reachability rule

`20260906_18` is reachable from protected `main` through PR #66 and remains current protected-main truth.

`20260908_19` is reachable only on the unmerged Timeline workstream branch at this point. It is candidate truth, not protected-main truth, until workstream validation and normal repository integration complete.
