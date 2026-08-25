# Backend CP6-04 — P0 Provisioning / Database-Security Hardening

- **Status:** IMPLEMENTATION CANDIDATE / DIRECT POSTGRESQL EXECUTION PENDING
- **Date:** 2026-08-25
- **Repository:** `MattiaRubino/dante`
- **Branch:** `feature/logical-postgresql`
- **Authorized PRE-SCOPE:** `52398cf6eb91f565edaa24f28b9a14a02b93cc79`
- **Checkpoint:** CP6-04 — Whole DANTE Database Materialization
- **Stage:** P0 — `cp6_provisioning_acl_hardening`
- **Alembic revision:** none; P0 is a non-Alembic prerequisite
- **Business DDL created by P0:** 0
- **M1 status:** NOT STARTED / BLOCKED UNTIL DIRECT P0 POSTGRESQL PROOF

## 1. Purpose

P0 implements the database-security and provisioning prerequisite frozen by CP6-03 Parts 12, 13 and 18 before any CP6 business table may be created.

The hard ordering remains:

```text
P0  cp6_provisioning_acl_hardening
MUST be effective and directly proven
        ↓
M1  cp6_native_identity_address
may then create the first 16 business tables
```

P0 does not materialize the DANTE business database. It hardens the technical PostgreSQL envelope so M1 cannot create business objects under the old CP3 blanket runtime-privilege posture.

## 2. Exact implementation surface

P0 changes only the approved technical/database-security boundary and its tests:

```text
apps/backend/src/dante/platform/database/provisioning.py
apps/backend/src/dante/platform/config/database.py
apps/backend/src/dante/platform/database/runtime.py
apps/backend/migrations/env.py
apps/backend/tests/integration/database/test_privileges.py
apps/backend/tests/integration/database/test_runtime.py
apps/backend/tests/integration/database/test_migrations.py
apps/backend/tests/integration/database/test_transactions.py
apps/backend/tests/test_settings.py
```

No CP6 M1..M7 business revision, business SQLAlchemy mapping, Dictionary object entry, API, product persistence adapter or frontend behavior is part of P0.

## 3. Runtime database identity — fail closed

`DatabaseSettings.user` is no longer an arbitrary non-empty PostgreSQL username.

The normal application runtime identity is fixed to:

```text
dante_runtime
```

Configuration using `postgres`, `dante_owner`, `dante_migrator` or another custom role is rejected before normal runtime use.

The runtime engine also verifies the real session contract during readiness:

```text
session_user = dante_runtime
current_user = dante_runtime
search_path = pg_catalog,dante,pg_temp
```

Readiness therefore proves both connectivity and the exact technical database identity/search-path envelope instead of treating `SELECT 1` alone as sufficient.

## 4. Trusted search_path

P0 replaces the old CP3 runtime/migration path:

```text
dante,public
```

with the Part-18 frozen baseline:

```text
pg_catalog,dante,pg_temp
```

This is configured for both runtime and migrator connections and reconciled at the role/database level by provisioning.

`public` is not present in the baseline DANTE runtime/migration search path.

## 5. Exact PostgreSQL role topology

P0 reconciles the three DANTE database roles to the frozen attributes:

```text
dante_owner
  NOLOGIN
  INHERIT
  NOSUPERUSER
  NOCREATEDB
  NOCREATEROLE
  NOREPLICATION
  NOBYPASSRLS
  password = NULL

dante_migrator
  LOGIN
  NOINHERIT
  NOSUPERUSER
  NOCREATEDB
  NOCREATEROLE
  NOREPLICATION
  NOBYPASSRLS

dante_runtime
  LOGIN
  NOINHERIT
  NOSUPERUSER
  NOCREATEDB
  NOCREATEROLE
  NOREPLICATION
  NOBYPASSRLS
```

P0 inspects every direct membership edge where any DANTE role is either granted role or member, removes those edges, and then recreates the only allowed edge:

```text
granting role  dante_owner
member         dante_migrator
INHERIT        FALSE
SET            TRUE
ADMIN          FALSE
```

No other direct DANTE membership edge is accepted by the final P0 verification.

## 6. Database and schema privilege envelope

P0 reconciles the database boundary to:

```text
PUBLIC
  CONNECT     NO
  TEMPORARY   NO
  CREATE      NO

dante_runtime
  CONNECT     YES
  TEMPORARY   NO
  CREATE      NO

dante_migrator
  CONNECT     YES
  TEMPORARY   NO
  CREATE      NO
```

Schema baseline:

```text
dante schema
  PUBLIC            none
  dante_runtime     USAGE only
  dante_migrator    no direct privilege
  dante_owner       owner

public schema
  PUBLIC            none
  dante_runtime     none
  dante_migrator    none
  dante_owner       USAGE only as technical owner context
```

The migrator performs DDL only after the explicitly verified `SET ROLE dante_owner` boundary.

## 7. Deny-by-default future object privileges

The CP3 broad defaults are removed before business materialization.

For future objects created by `dante_owner`, P0 sets the baseline to no automatic runtime privilege on:

```text
tables
sequences
types/domains
routines
```

PUBLIC routine EXECUTE and DANTE type USAGE defaults are also revoked.

P0 deliberately does not issue blanket `GRANT ... ON ALL TABLES` or equivalent business-object reconciliation.

Exact runtime business privileges remain migration-owned and are activated only by M7 according to the frozen DB-U21 / Part-17 matrix.

A later provisioning rerun must therefore not broaden an exact object ACL already established by migrations.

## 8. SCRAM-SHA-256 credential path

P0 removes the former cleartext-password-bearing SQL construction.

The implementation:

```text
SET password_encryption = 'scram-sha-256'
SHOW password_encryption
require exact scram-sha-256
then use psycopg/libpq PGconn.change_password()
for dante_migrator and dante_runtime
```

The application code does not construct an `ALTER ROLE ... PASSWORD <original-cleartext>` SQL statement.

`dante_owner` is explicitly reconciled to:

```text
NOLOGIN
rolpassword = NULL
```

The login roles remain the only DANTE roles with credentials.

## 9. Alembic migration identity preflight

Alembic remains online-only and now fails closed on database identity.

Before elevation it requires:

```text
session_user = dante_migrator
current_user = dante_migrator
search_path = pg_catalog,dante,pg_temp
```

Only then may it execute the static:

```text
SET ROLE dante_owner
```

After elevation it requires:

```text
session_user = dante_migrator
current_user = dante_owner
search_path = pg_catalog,dante,pg_temp
```

An injected Alembic URL whose username is not exactly `dante_migrator` is rejected.

The existing CP3 technical Alembic revision remains the repository head at this P0 stage because P0 is not an Alembic revision.

## 10. Regression-test adaptation

The old CP3 transaction acceptance probe previously inherited broad default runtime CRUD privileges.

That is no longer valid under P0.

The transaction test now gives its disposable probe only the explicit test-local capabilities required to exercise transaction semantics:

```text
SELECT
INSERT
```

This preserves commit/rollback/flush/savepoint proof without restoring broad production defaults.

## 11. Direct P0 proof encoded in the test suite

The P0 test changes require real PostgreSQL 18.6 to prove at least:

```text
runtime user is exactly dante_runtime
runtime trusted search_path is exact
migrator pre-elevation identity is exact
migrator post-elevation current_user is dante_owner
owner/migrator/runtime attributes are exact
only the owner -> migrator membership edge exists
membership options are exact
owner password is NULL
migrator/runtime verifiers are SCRAM-SHA-256
runtime/migrator TEMP and database CREATE are denied
runtime public-schema USAGE/CREATE is denied
migrator direct dante/public USAGE is denied
new dante_owner objects are deny-by-default to runtime
runtime cannot SET ROLE owner/migrator
runtime cannot create TEMP/schema objects or read migration history
provisioning removes an injected unexpected DANTE membership edge
provisioning rerun does not broaden a migration-owned SELECT-only ACL
Alembic rejects a non-migrator injected login identity
existing transaction semantics still pass under explicit test ACLs
```

## 12. Execution honesty

At the time this implementation record is written:

```text
P0 CODE / TEST IMPLEMENTATION
WRITTEN

PYTHON PATCH SYNTAX REVIEW
COMPLETE

REAL POSTGRESQL 18.6 P0 EXECUTION
NOT YET RUN IN THIS CP6-04 STAGE

REAL DOCKER ACCEPTANCE
PENDING

P0 DIRECT PASS
NOT YET EARNED

M1
NOT STARTED
```

No result from the earlier CP3 PostgreSQL 18.6 foundation run is reused as proof that these new P0 changes pass. The P0 implementation changed provisioning/runtime/migration security behavior and therefore requires fresh direct execution.

## 13. Next mandatory operation

Before authoring or executing M1:

```text
1. build/verify the repository PostgreSQL 18.6 Docker image;
2. start a disposable real PostgreSQL acceptance boundary;
3. run fresh provisioning with this P0 implementation;
4. execute the real PostgreSQL test lane;
5. inspect any failure as a P0 implementation finding;
6. repair and rerun until clean;
7. record exact PostgreSQL/Docker/test evidence;
8. only then open the separate M1 implementation gate.
```

M1 remains blocked if P0 has only static/code review evidence.

## 14. Explicit exclusions

P0 does not authorize or create:

```text
CP6-M01..CP6-M07 Alembic business revisions
68 DANTE business tables
5 current views
14 integrity routines
75 trigger attachments
95 final physical indexes
68 final business FKs
120 final CHECK constraints
68 business SQLAlchemy Row mappings
5 Core-only business view handles
87 Dictionary object entries
product persistence adapters
application use cases
business APIs
frontend/mobile changes
production TLS/network/secret-manager topology
protected-main merge/rebase/realignment
```

Those remain in their already-frozen later stages.
