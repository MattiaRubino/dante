# Backend CP6-04 — P0 Provisioning / Database-Security Hardening

- **Status:** REPAIR CANDIDATE / DIRECT POSTGRESQL RERUN PENDING
- **Date:** 2026-08-25
- **Repository:** `MattiaRubino/dante`
- **Branch:** `feature/logical-postgresql`
- **Initial authorized PRE-SCOPE:** `52398cf6eb91f565edaa24f28b9a14a02b93cc79`
- **Initial implementation candidate HEAD:** `a691783a18794937f16c2574b8ca814936ecd45b`
- **Repair authorized PRE-SCOPE:** `a691783a18794937f16c2574b8ca814936ecd45b`
- **Checkpoint:** CP6-04 — Whole DANTE Database Materialization
- **Stage:** P0 — `cp6_provisioning_acl_hardening`
- **Alembic revision:** none; P0 is a non-Alembic prerequisite
- **Business DDL created by P0:** 0
- **M1 status:** NOT STARTED / BLOCKED UNTIL DIRECT P0 POSTGRESQL PASS

## 1. Purpose

P0 implements the database-security and provisioning prerequisite frozen by CP6-03
Parts 12, 13 and 18 before any CP6 business table may be created.

The hard ordering remains:

```text
P0  cp6_provisioning_acl_hardening
MUST be effective and directly proven
        ↓
M1  cp6_native_identity_address
may then create the first 16 business tables
```

P0 does not materialize the DANTE business database. It hardens the technical
PostgreSQL envelope so M1 cannot create business objects under the old CP3
blanket runtime-privilege posture.

## 2. Exact implementation surface

The original P0 gate changed only:

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
docs/development/backend-cp6-04-p0-provisioning-security.md
```

The repair gate after the first real PostgreSQL run is limited to:

```text
apps/backend/src/dante/platform/database/provisioning.py
apps/backend/tests/integration/database/test_privileges.py
docs/development/backend-cp6-04-p0-provisioning-security.md
```

No CP6 M1..M7 business revision, business SQLAlchemy mapping, Dictionary object
entry, API, product persistence adapter or frontend behavior is part of P0.

## 3. Runtime database identity — fail closed

`DatabaseSettings.user` is no longer an arbitrary PostgreSQL username.

The normal application runtime identity is fixed to:

```text
dante_runtime
```

Configuration using `postgres`, `dante_owner`, `dante_migrator` or another
custom role is rejected before normal runtime use.

Runtime readiness verifies the real session contract:

```text
session_user = dante_runtime
current_user = dante_runtime
search_path = pg_catalog,dante,pg_temp
```

Readiness therefore proves both connectivity and the exact technical database
identity/search-path envelope.

## 4. Trusted search_path

P0 replaces the old CP3 runtime/migration path:

```text
dante,public
```

with the frozen Part-18 baseline:

```text
pg_catalog,dante,pg_temp
```

This is configured for runtime and migrator connections and reconciled at the
role/database level by provisioning.

`public` is absent from the DANTE runtime/migration search path.

## 5. Exact PostgreSQL role topology

P0 reconciles the three DANTE database roles to:

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

The only allowed DANTE-to-DANTE membership edge is:

```text
granted role  dante_owner
member        dante_migrator
INHERIT       FALSE
SET           TRUE
ADMIN         FALSE
```

P0 inspects every direct membership where a DANTE role appears on either side.

The repair makes the reconciliation boundary explicit:

```text
unexpected DANTE ↔ DANTE edge
  -> provisioning may revoke/reconcile it to the exact frozen graph

DANTE ↔ external-role edge
  -> provisioning FAILS CLOSED
  -> the external edge is not silently mutated
  -> manual security review is required
```

This prevents provisioning from silently deleting an externally managed or
unexpected cross-boundary role relationship.

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

The migrator performs DDL only after the verified `SET ROLE dante_owner`
boundary.

## 7. Deny-by-default future object privileges

The CP3 broad defaults are removed before business materialization.

For future objects created by `dante_owner`, P0 establishes no automatic
runtime privilege on:

```text
tables
sequences
types/domains
routines
```

Runtime-specific DANTE defaults remain schema-scoped.

PostgreSQL's built-in global defaults require special treatment for PUBLIC:

```text
routines
  built-in default: PUBLIC EXECUTE
  P0: global ALTER DEFAULT PRIVILEGES REVOKE EXECUTE ON ROUTINES FROM PUBLIC

types/domains
  built-in default: PUBLIC USAGE
  P0: global ALTER DEFAULT PRIVILEGES REVOKE USAGE ON TYPES FROM PUBLIC
```

The first P0 implementation incorrectly placed those two PUBLIC revokes under
`IN SCHEMA dante`. PostgreSQL per-schema default privileges are additive to
global defaults and cannot negate a global grant. The repair therefore moves
these two PUBLIC revokes to the global owner default-privilege layer.

P0 deliberately does not issue blanket `GRANT ... ON ALL TABLES` or equivalent
business-object reconciliation.

Exact runtime business privileges remain migration-owned and are activated only
by M7 according to the frozen DB-U21 / Part-17 matrix.

A later provisioning rerun must not broaden or erase an exact object ACL already
established by migrations.

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

Application code does not construct an
`ALTER ROLE ... PASSWORD <original-cleartext>` SQL statement.

`dante_owner` is explicitly reconciled to:

```text
NOLOGIN
rolpassword = NULL
```

The login roles remain the only DANTE roles with credentials.

## 9. Alembic migration identity preflight

Alembic remains online-only and fails closed on database identity.

Before elevation:

```text
session_user = dante_migrator
current_user = dante_migrator
search_path = pg_catalog,dante,pg_temp
```

Only then may it execute:

```text
SET ROLE dante_owner
```

After elevation:

```text
session_user = dante_migrator
current_user = dante_owner
search_path = pg_catalog,dante,pg_temp
```

An injected Alembic URL whose username is not exactly `dante_migrator` is
rejected.

The CP3 technical Alembic revision remains repository head at P0 because P0 is
not an Alembic revision.

## 10. Regression-test adaptation

The old CP3 transaction acceptance probe previously inherited broad default
runtime CRUD privileges.

Under P0 the disposable transaction probe receives only:

```text
SELECT
INSERT
```

This preserves commit/rollback/flush/savepoint proof without restoring broad
production defaults.

## 11. Direct P0 proof encoded in the test suite

The PostgreSQL 18.6 lane proves at least:

```text
runtime user is exactly dante_runtime
runtime trusted search_path is exact
migrator pre-elevation identity is exact
migrator post-elevation current_user is dante_owner
owner/migrator/runtime attributes are exact
only the owner -> migrator DANTE-internal membership edge remains
membership options are exact
owner password is NULL
migrator/runtime verifiers are SCRAM-SHA-256
runtime/migrator TEMP and database CREATE are denied
runtime public-schema USAGE/CREATE is denied
migrator direct dante/public USAGE is denied
new dante_owner table/sequence privileges are deny-by-default to runtime
new dante_owner routine EXECUTE is denied to runtime
new dante_owner type/domain USAGE is denied to runtime
runtime cannot SET ROLE owner/migrator
runtime cannot create TEMP/schema objects or read migration history
unexpected DANTE-internal membership is reconciled
external-role membership involving DANTE fails closed and remains untouched
provisioning rerun does not broaden a migration-owned SELECT-only ACL
Alembic rejects a non-migrator injected login identity
existing transaction semantics pass under explicit test ACLs
```

The repair adds direct `has_function_privilege(..., 'EXECUTE')` and
`has_type_privilege(..., 'USAGE')` assertions so the PUBLIC-default behavior is
proved explicitly rather than inferred from unrelated DML failures.

## 12. First real PostgreSQL 18.6 execution — finding

The first CP6-04 P0 execution was run locally on the repository's real
`dante-postgres-local:18.6` Docker image.

Observed result:

```text
pytest command
uv run pytest -m postgres -vv

selected
21

PASS
20

FAIL
1

failing test
tests/integration/database/test_privileges.py::
test_new_owner_objects_are_deny_by_default_for_runtime

failing operation
SELECT dante.cp3_probe_function()

observed problem
runtime execution succeeded when InsufficientPrivilege was required
```

All migration, role-topology, runtime, transaction and the other privilege tests
passed in that run.

This run is evidence of a real P0 finding, not a P0 PASS.

Root cause:

```text
PUBLIC EXECUTE on routines is a PostgreSQL global default privilege.
A per-schema default REVOKE cannot negate that global default.
```

Review of the same PostgreSQL default-privilege rule exposed the analogous
`PUBLIC USAGE` risk for future types/domains. That second issue was found by
analysis before it produced a separate red test.

The repair addresses both.

## 13. Repair validation state

At repair-write time:

```text
P0 ORIGINAL CODE / TEST IMPLEMENTATION
WRITTEN

FIRST REAL POSTGRESQL 18.6 RUN
20 PASS / 1 FAIL

P0 FINDING
CONFIRMED

REPAIR PYTHON SYNTAX REVIEW
COMPLETE

REPAIR REAL POSTGRESQL 18.6 RERUN
PENDING

P0 DIRECT PASS
NOT YET EARNED

M1
NOT STARTED
```

No earlier CP3 CI result is reused as proof for P0.

## 14. Next mandatory operation

Before authoring or executing M1:

```text
1. fast-forward the existing backend worktree to the repair HEAD;
2. verify no disposable pytest PostgreSQL container was left behind;
3. rerun `uv run pytest -m postgres -vv`;
4. require the full PostgreSQL P0 lane to pass;
5. verify the disposable acceptance container is gone after the run;
6. record exact Docker/PostgreSQL/test evidence;
7. only then open the separate M1 implementation gate.
```

No new worktree is required.

The PostgreSQL acceptance harness remains disposable and isolated from the
normal persistent LOCAL Compose database.

## 15. Explicit exclusions

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
new worktrees
additional persistent databases
```

Those remain in their already-frozen later stages.
