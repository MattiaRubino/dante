# DANTE Database System of Record

- **Status:** CURRENT / AUTHORITATIVE DATABASE REFERENCE
- **Last reconciled:** 2026-09-14
- **PostgreSQL:** 18.6
- **Protected-main Alembic head:** `20260906_18`
- **Protected-main topology:** `89|5|18|77|173|91|272|0|0|0`
- **Timeline candidate branch:** `feature/timeline-temporal-operational`
- **Timeline candidate Alembic head:** `20260914_23`
- **Timeline candidate topology:** `95|5|23|77|190|110|284|0|0|0`
- **Pre-vertical integration:** PR #66 / merge `1ecd58145860aebfaaa3dc1bd356b90f7a8eb19b`
- **Authenticated DANTE context authority:** `../architecture/authenticated-dante-context.md`
- **Access/Auth reference:** `access-auth.md`
- **Shared Email Platform authority:** `../architecture/email-platform.md`
- **Recovery operator authority:** `../operations/postgres-recovery-runbook.md`
- **Persistence doctrine:** `../development/backend-cp6-02-postgresql-persistence-constitution.md`
- **Persistence ADR:** `../decisions/ADR-010-postgresql-persistence-constitution.md`
- **Pre-vertical closure:** `../workstreams/pre-vertical-foundation-closure-2026-09-06.md`
- **Timeline workstream authority:** `../workstreams/timeline-temporal-operational-map.md`
- **B02 execution authority:** `../workstreams/timeline-temporal-operational-b02-execution-plan.md`

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

Recovery and Access/Auth originated as sibling children of `20260826_08`; both accepted histories are preserved. The pre-vertical foundation and Timeline candidate evolve only through forward revisions:

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
        20260908_19 activity_core                 [Timeline B01 candidate]
            ↓
        20260909_20 b02_schedule_establish        [Timeline B02-A candidate]
            ↓
        20260909_21 b02_schedule_acl_hardening
            ↓
        20260913_22 b02_schedule_revision
            ↓
        20260914_23 b02_schedule_unschedule_undo    [current Timeline candidate head]
```

`20260904_17` is the accepted no-DDL merge revision. `20260906_18` is current protected-main authority. `_19`, `_20`, `_21`, `_22` and `_23` are forward-only candidate descendants on `feature/timeline-temporal-operational`; they do not become protected-main authority merely by existing on this branch.

No accepted migration was rebased, renumbered or flattened. `_21` corrects the B02 runtime ACL forward rather than editing `_20`; `_22` adds the separately gated B02-C revision capability; `_23` adds the separately gated B02-D unschedule and guarded Undo capabilities.

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

### 3.2 Timeline B01 candidate delta

`20260908_19` adds exactly:

```text
dante.activity_intention
dante.activity_create_operation
dante.create_self_activity(uuid,text,text,uuid,text)
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

`dante.activity` remains the single CP6 Activity NativeRef owner. `activity_intention` is the smallest typed dependent canonical descriptor required by B01; `activity_create_operation` is immutable operation-control state; `create_self_activity` is a bounded capability surface. None authorizes a generic Task/status model or a second Activity identity.

### 3.3 Timeline B02-A candidate delta

`20260909_20` adds exactly:

```text
dante.schedule_establish_operation
dante.establish_self_floating_schedule(
  uuid,text,text,uuid,uuid,uuid,
  timestamp without time zone,
  timestamp without time zone
)
```

Exact `_19 → _20` structural delta:

```text
+1 table
+1 routine
+0 triggers
+4 indexes
+4 foreign keys
+2 CHECK constraints
```

`20260909_21` changes ACL only and therefore adds no table/view/routine/index/FK/CHECK.

### 3.4 Timeline B02-C candidate delta

`20260913_22` adds `dante.schedule_revision_operation` and `dante.revise_self_floating_schedule(...)`. Exact `_21 → _22` delta: one table, one routine, three indexes, four foreign keys and two CHECK constraints. It retains the existing Schedule owner and immutable placement history while moving explicit currentness from the exact expected MaterialStateRef to one new state.

### 3.5 Timeline B02-D candidate delta

`20260914_23` adds `dante.schedule_unschedule_operation`, `dante.schedule_unschedule_undo_operation`, `dante.unschedule_self_schedule(...)` and `dante.undo_self_schedule_unschedule(...)`. Exact `_22 → _23` delta: two tables, two routines, six physical indexes, seven foreign keys and five CHECK constraints. Unschedule removes only explicit currentness and closes the open history episode; guarded Undo creates a new immutable placement state and a new history episode only while absence is still current and no later episode exists.

Current candidate topology is therefore:

```text
95 tables
5 views
23 routines
77 triggers
190 physical indexes
110 foreign keys
284 CHECK constraints
0 enums/domains
0 sequences
0 materialized views
0 partitioned tables
0 RLS policies
```

B02-A reuses the existing CP6 `schedule` owner, `schedule.placement` MaterialState structures, typed floating-local interval payload, explicit scoped-current binding and current-history. It does not create a second Schedule owner, generic calendar object, Session, Actual or Temporal Constraint.

Permanent boundaries remain:

```text
Activity != Schedule
Schedule != Temporal Constraint != Session != Actual
Schedule identity != placement MaterialState
current accepted placement != newest state row
operation receipt != Schedule identity != MaterialState identity
```

Platform Observability adds no DANTE business table/view/routine/Alembic revision/SQLAlchemy business mapping; its database contribution remains a provisioning-owned operational observer identity described below.

## 4. Acceptance boundary

### 4.1 Protected-main accepted boundary

Current protected-main database acceptance remains:

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

### 4.2 Timeline B01/B02-A/B02-C/B02-D candidate boundary

At this reconciliation slice the current `_23` candidate carries the following obligations; B02-D evidence is pending because its test gate is deliberately deferred:

```text
single repository Alembic head = 20260914_23
Dictionary object tree/counts = live PostgreSQL catalog
SQLAlchemy mappings = all 95 DANTE tables
candidate topology = 95|5|23|77|190|110|284|0|0|0
runtime table ACL = Dictionary
create_self_activity owner/security/search_path/EXECUTE = exact
establish_self_floating_schedule owner/security/search_path/EXECUTE = exact
schedule_establish_operation direct runtime table privileges = none
revise_self_floating_schedule exact expected-state/history/replay proof = PENDING
schedule_revision_operation direct runtime table privileges = none
unschedule_self_schedule exact withdrawal/history/replay proof = PENDING
undo_self_schedule_unschedule exact receipt/absence/chronology proof = PENDING
B02-D operation receipt direct runtime table privileges = none
fresh DB → head = PENDING FOR _23
head → base → head = PENDING FOR _23
canonical B01 Activity intention → _19→_18 downgrade = REJECTED
canonical B02-A Schedule history → _20→_19 downgrade = REJECTED
B00/B01/B02-A real PostgreSQL integration = HISTORICAL PASS
full backend PostgreSQL marked suite = PENDING FOR _23
frontend B02-D operation/reconciliation tests = AUTHORED, NOT YET RUN
```

These are obligations until an exact-head run actually succeeds. Updating the candidate reference is not itself acceptance evidence, and automated green does not replace applicable manual `userTest` approval.

## 5. Application role model

Application roles remain explicitly separated:

```text
dante_owner      NOLOGIN ownership identity
dante_migrator   LOGIN migration identity
dante_runtime    LOGIN application runtime identity
dante_observer   LOGIN statistics-only collector identity
```

Ownership, migration and runtime privileges remain independently tested. Application runtime does not inherit migration/owner authority.

`20260906_18` does not grant generic runtime `INSERT` on Person. Runtime receives only the bounded capability needed to establish an absent authenticated Account application context; direct Person DML remains governed by the existing CP6 posture.

B01 `_19` grants no generic runtime Activity mutation. Runtime receives:

```text
SELECT  dante.activity_intention
EXECUTE dante.create_self_activity(uuid,text,text,uuid,text)
```

and no direct table privilege on `activity_create_operation`.

B02-A `_20/_21` likewise grants no generic runtime Schedule mutation and no direct receipt-table privilege. Runtime receives:

```text
EXECUTE dante.establish_self_floating_schedule(
  uuid,text,text,uuid,uuid,uuid,
  timestamp without time zone,
  timestamp without time zone
)
```

plus the existing/current read privileges on CP6 Schedule and placement projections required by the Timeline query. `_21` explicitly removes the direct `SELECT` on `schedule_establish_operation` introduced by `_20`.

Both bounded functions are owned by `dante_owner`, use `SECURITY DEFINER` with trusted `search_path = pg_catalog, dante, pg_temp`, and expose only the operation capability required by the vertical.

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

The canonical detailed contract is in `dante-postgresql-database-part-12.md`, Section 46, marked by `DANTE-OBSERVABILITY-OBSERVER-CONTRACT v1`. Provisioning, live PostgreSQL tests and the Alloy/Postgres-exporter configuration must remain aligned with that contract. The observer credential is secret even though its authority is read-only statistics access.

## 7. Access/Auth and authenticated DANTE context persistence

Account is the durable security serialization root. Principal is runtime-derived. Provider identity authority is issuer+subject, never provider email. Password is optional; passkeys and external authenticators converge on canonical DANTE AuthSession.

Permanent distinction:

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

On the current Timeline candidate branch, checked-out Dictionary materialization is `20260914_23 / 95|5|23|77|190|110|284`. Candidate entries include B01 Activity objects, B02-A Schedule establishment objects, B02-C revision objects, and B02-D unschedule/Undo receipt tables plus bounded capabilities. They must match SQLAlchemy/Alembic/live PostgreSQL exactly before this slice can close.

Operational cluster roles such as `dante_observer` are deliberately not fake business objects; their security contract is carried by technical-role/provisioning references and live ACL tests.

## 10. Recovery boundary

The accepted LOCAL recovery model keeps database-local proof distinct from application/Email reopen and from future production/cloud recovery.

```text
historical CP07 database-local reopen              PASS FOR EXECUTED HISTORICAL SCOPE
historical CP08 Email/application reopen            PASS FOR EXECUTED HISTORICAL SCOPE
pre-vertical exact-head database-local recovery     PASS @ 21353469464f1371f9913dc78933f4ee42698f33
Timeline B01/B02-A/B02-C/B02-D _23 recovery-specific rerun       NOT CLAIMED BY THIS SLICE
remote backup provider                              TBD / NOT ACTIVATED
production/cloud recovery                           NOT CLAIMED
```

The final pre-vertical rehearsal proved the protected-main `20260906_18` database-local Recovery contract, including observer provisioning, structural/security acceptance, deterministic PITR, MaterialState anti-resurrection reconciliation and database-local reopen. It did not silently relabel historical CP08 application/Email reopen evidence as newly executed.

B01 adds dependent canonical/control persistence. B02-A and B02-C each add one operation-control table. B02-D adds two operation receipts; unschedule creates no state, while guarded Undo creates an ordinary immutable CP6 placement state through a bounded capability. None introduces a new MaterialState retirement facet, outbox family or provider/object-store state. Whole-vertical recovery closure remains B14; no new recovery proof is fabricated here.

Current operator authority is `../operations/postgres-recovery-runbook.md`; executable recovery truth lives under `../../infra/local/postgres/recovery/`.

## 11. Same-change rule

A structural database change is incomplete until the reviewed slice aligns semantic authority, forward Alembic, SQLAlchemy, Dictionary, current human reference, direct tests and real PostgreSQL proof.

For operational-role changes, the equivalent same-change rule applies to the database reference, provisioning, collector configuration and live privilege tests.

No future vertical may bypass these contracts merely because its data is “technical” or “observability” data.

## 12. Reachability rule

`20260906_18` is reachable from protected `main` through PR #66 and remains current protected-main truth.

`20260914_23` is reachable only on the unmerged Timeline workstream branch at this point. It is candidate truth, not protected-main truth, until workstream validation and normal repository integration complete.
