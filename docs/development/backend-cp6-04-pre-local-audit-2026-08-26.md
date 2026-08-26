# CP6-04 PRE-LOCAL AUDIT — 2026-08-26

**Repository:** `MattiaRubino/dante`  
**Branch:** `feature/logical-postgresql`  
**Accepted implementation HEAD:** `7fb54f267e9e91512001e3ea6c7cc02630097941`  
**Status:** M1–M7 MATERIALIZED / DIRECT POSTGRESQL PASS / PERSISTENT LOCAL NEXT

## Audit conclusion

The CP6-04 database implementation is structurally and behaviorally complete through M7 and is accepted by the full direct PostgreSQL suite. No schema, migration, mapping, Dictionary or ACL defect is known at this boundary.

Final repository materialization is exactly:

```text
tables              68
views                 5
routines             14
triggers             75
  immediate          18
  deferred           57
physical indexes     95
foreign keys         68
check constraints   120
SQLAlchemy Row maps  68
Core view handles     5
Dictionary entries   87
```

## Migration DAG

The repository has one accepted chain:

```text
P0 provisioning
M1 cp6_native_identity_address
M2 cp6_scoped_material_control
M3 cp6_schedule_actual_session
M4 cp6_recurrence
M5 cp6_core_integrity_current_views
M6 cp6_occurrence_generation
M7 cp6_runtime_acl_activation
```

The final direct run proved fresh→head, head→base→head and Alembic drift consistency.

## Behavioral/security acceptance

The final direct PostgreSQL run proves the frozen integrity and security model at runtime, including:

- owner/reference/material-state family enforcement;
- current-state/current-history equivalence and one-way closure semantics;
- recurrence and occurrence-generation constraints;
- exact runtime ACL activation;
- bounded current-view mutation contract;
- direct integrity-routine EXECUTE denial;
- advisory-lock occurrence-generation boundary without fake owner UPDATE privileges;
- hardened owner/migrator/runtime role posture;
- runtime readiness/recovery behavior;
- real transaction commit, rollback, flush and savepoint behavior.

## Direct evidence

At accepted HEAD `7fb54f267e9e91512001e3ea6c7cc02630097941` the user ran:

```text
cd apps/backend
uv run pytest -m postgres -vv
```

Observed:

```text
108 collected
37 deselected
71 selected
71 passed
0 failed
51.14s
coverage 94.14%
```

## Repository consistency

The Database Dictionary final baseline and materialized surface agree on:

```text
68 tables
5 views
14 routines
75 triggers
95 physical indexes
68 foreign keys
120 CHECK constraints
87 standalone Dictionary entries
```

`scope.json` is promoted to `status=materialized` and records CP6-M01 through CP6-M07 as completed only after this direct PASS.

## Persistent LOCAL readiness

Repository infrastructure for the next step already exists:

```text
infra/compose/local.yaml
infra/local/postgres/Dockerfile
infra/local/postgres/initdb/
```

The Compose contract uses:

```text
image       dante-postgres-local:18.6
host bind   127.0.0.1:5432
volume      postgres-data:/var/lib/postgresql
DB          dante
```

The named volume is intentionally persistent across `docker compose down`; only `down --volumes` destroys it.

## Remaining closure sequence

The PostgreSQL phase is not considered fully operationally closed until the explicit LOCAL sequence succeeds:

```text
persistent LOCAL PostgreSQL start/build
→ application role provisioning
→ Alembic fresh→head against LOCAL
→ runtime/backend smoke
→ docker down/up restart
→ verify schema/data/roles persist
→ optional DBeaver inspection
→ DATABASE OPERATIVE LOCAL
→ explicit gate toward protected main
```

No merge/rebase/main mutation is authorized by this audit.
