# DANTE Database System of Record

- **Status:** CURRENT / PRE-INTEGRATION
- **Last reconciled:** 2026-09-03
- **PostgreSQL:** 18.6
- **Protected-main Alembic head:** `20260830_09` — Recovery integrated
- **Feature/access-auth Alembic head:** `20260903_15` — Access/Auth + Email branch-local
- **Current Access/Auth reference:** `access-auth.md`
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

Permanent reconciliation invariant:

```text
CURRENT DB REFERENCE
≈ DATABASE DICTIONARY
≈ SQLALCHEMY
≈ ALEMBIC
≈ REAL POSTGRESQL
≈ DIRECT TESTS
```

A mismatch is a defect. Applied Alembic revisions are immutable historical evidence; corrections use new forward revisions.

## 2. Two accepted histories currently awaiting convergence

### Protected main

The CP6 baseline was `20260826_08`, but that is no longer the protected-main head.

Current protected main contains the closed Recovery evolution:

```text
20260826_08
└── 20260830_09 recovery_material_state_retirement
```

Current protected-main catalog:

```text
69 tables
5 views
15 routines
76 triggers
97 physical indexes
69 foreign keys
123 CHECK constraints
```

### `feature/access-auth`

The active branch independently evolved from the same `20260826_08` parent:

```text
20260826_08
└── 20260827_09 Account / Email / Password / AuthSession
    └── 20260827_10 Account security-lock capability
        └── 20260829_11 signup/recovery challenges
            └── 20260830_12 multi-authenticator persistence
                └── 20260831_13 authenticator-lifecycle ACL
                    └── 20260903_14 shared Email Platform
                        └── 20260903_15 Email Platform ACL hardening
```

Current branch catalog:

```text
87 tables
5 views
15 routines
75 triggers
170 physical indexes
88 foreign keys
267 CHECK constraints
```

These are **two branch-local accepted histories**, not one combined database yet. Recovery must not be claimed as present on `feature/access-auth` before main is merged; Access/Auth/Email must not be claimed as present on protected main before the PR lands.

## 3. Integration rule for the divergent Alembic DAG

The correct integration is forward-only:

```text
merge protected main into feature/access-auth
→ retain main Recovery revision unchanged
→ retain Access/Auth/Email revisions unchanged
→ Alembic temporarily has two heads
→ add one normal merge revision referencing both heads
→ reconcile Dictionary/reference/mappings/tests for combined truth
→ prove fresh PostgreSQL + upgrade paths
```

Forbidden:

```text
rebase migration history
renumber an applied revision
change down_revision of an existing revision
copy Recovery DDL into an Access revision
flatten one branch away
stamp over a missing history
claim combined topology before live introspection
```

The exact combined object counts are deliberately **not predicted here**. They become accepted only after the merged graph is materialized and introspected on real PostgreSQL 18.6.

## 4. Access/Auth branch persistence

Current semantic shape:

```text
Account
├── EmailIdentity 1..N
├── PasswordCredential 0..1
├── AuthSession 0..N
├── ExternalIdentity 0..N
├── WebAuthnAccount 0..1
│   └── PasskeyCredential 0..N
└── bounded lifecycle/challenge state

PasswordSignupChallenge
PasswordRecoveryChallenge
ExternalAuthTransaction
ExternalLinkChallenge
ExternalSignupChallenge
AccountProfileBootstrap
AppleAuthGrant
WebAuthnChallenge
```

Account is the durable security serialization root. Principal remains runtime-derived and is not persisted.

## 5. Shared Email Platform persistence

Exactly four bounded technical structures are currently materialized on the Access branch:

```text
dante.email_delivery_intent
dante.email_delivery_attempt
dante.email_provider_event
dante.email_recipient_suppression
```

They are shared Email Platform state, not Access/Auth semantic owners and not DANTE MaterialState.

Core doctrine:

```text
feature mutation + EmailIntent atomically coordinated
provider network I/O only after COMMIT
operation_scope + idempotency_key + fingerprint
bounded claim / lease / SKIP LOCKED
exact claim ownership to finalize
explicit ambiguous outcome
no blind retry after ambiguity
short-lived AES-256-GCM protected payload
terminal/unsafe-state sensitive wipe
provider evidence distinct from DANTE intent truth
suppression distinct from EmailIdentity verification truth
```

Access/Auth is the first consumer. Future consumers reuse this platform rather than creating another outbox/mailer lifecycle.

## 6. Security / transaction baseline

```text
PostgreSQL 18.6
READ COMMITTED baseline
short authoritative transactions
no provider/browser/network wait inside authoritative DB transactions
dante_owner      NOLOGIN owner
dante_migrator   dedicated migration identity
dante_runtime    least-privilege runtime identity
trusted search_path = pg_catalog,dante,pg_temp
Account-wide security mutation uses bounded DB serialization
constraints remain final race arbiters
no blanket transaction retry
ambiguous commit/effect requires operation-specific reconciliation
```

## 7. Database Dictionary contract

`dictionary/` is the machine-readable current database companion.

For every materialized DANTE object, same-change review must keep aligned:

```text
purpose/classification/traceability
columns + types + nullability/defaults
PK / UNIQUE / FK / CHECK
indexes / triggers
lifecycle / state-history meaning
runtime ACL
introducing Alembic revision
SQLAlchemy mapping
proof obligations
```

The CP6 stage list in `dictionary/scope.json` is a frozen CP6 materialization provenance sequence. Later object provenance belongs on each Dictionary object through `implementation.introducing_stage`, `alembic_revision` and `runtime_acl_stage`; current topology counts live separately in `current_materialization`.

## 8. Direct proof already established on the Access branch

Current PostgreSQL acceptance tests prove, among other things:

```text
fresh DB reaches one Access-branch head 20260903_15
head → base → head round trip
Alembic check reports no mapping/schema drift
migrator identity + trusted search_path
current live table/view/routine/index/constraint/trigger sets
Dictionary ↔ SQLAlchemy mapping parity
object owner = dante_owner
exact Auth runtime ACL
Email Platform migration / lifecycle / ACL behavior
```

Real SES UAT additionally proved three accepted Email intents with one SES attempt each, provider MessageId present and terminal sensitive-payload wipe.

## 9. Whole-database Blueprint lifecycle

The `dante-postgresql-database*.md` corpus contains the deep CP6 derivation, design rationale and closure chronology. It has continuing reference value, but historical phase banners such as `CP6-03 ACTIVE`, `GATE NOT EARNED`, early M3 counts or old DB-U OPEN states are **checkpoint evidence**, not current operational status.

Current routing is:

```text
this README                       → current database System of Record
access-auth.md                    → current Access/Auth + Email branch DB reference
dictionary/                       → current machine-readable object contract
Alembic + mappings + PostgreSQL   → executable/materialized truth
dante-postgresql-database*.md     → deep CP6 design/reference history and rationale
```

Where a historical Blueprint progress label conflicts with current executable/current-reference truth, it does not override this System of Record.

## 10. Same-change database rule

A structural database change is incomplete until the same reviewed slice updates all affected:

```text
semantic/security authority
Alembic forward migration
SQLAlchemy mapping/MetaData
Database Dictionary
current human DB reference
direct tests
real PostgreSQL proof
status/routing docs when phase state changes
```

## 11. Current pre-integration gate

Before main is merged into this branch:

```text
Dictionary scope/schema internally coherent
current docs no longer claim stale M5/CP6 state
no temporary branch handoff is allowed to leak to main
Access Alembic line remains single-head and green
current PostgreSQL catalog parity remains green
```

After main is merged, the database gate is repeated against the **combined** Recovery + Access/Auth + Email DAG before any PR to protected main.