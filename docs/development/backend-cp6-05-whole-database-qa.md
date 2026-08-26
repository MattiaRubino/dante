# DANTE Backend CP6-05 — Whole Database Direct QA / Final Closure

**Status:** IMPLEMENTED CANDIDATE / DIRECT LOCAL ACCEPTANCE REQUIRED  
**Branch:** `feature/logical-postgresql`  
**PRE-SCOPE:** `6972852d0b62066f2e00f20f6e24a0f2e1cbd8da`  
**Accepted materialization before CP6-05:** CP6-M01..M07 + persistent LOCAL PostgreSQL 18.6  

## Purpose

CP6-05 is the mandatory whole-database clean-room gate. It does not add product semantics. It reconciles the final accepted database across architecture/reference, Dictionary, SQLAlchemy, Alembic, real PostgreSQL and executable proof.

## Audit disposition

```text
DB topology defect                           0
ACL topology defect                          0
Role-13 concurrency-defense defect           1 → repaired by 20260826_08
historical stage-scope test defect           1 → repaired stage-relatively
mapping filename documentation drift         1 → narrowly superseded by Part 19
Dictionary final proof-trace gap              occurrence-generation family → final QA proof added
whole-head cross-representation proof gap     → test_cp6_final.py
```

## Corrective revision

`20260826_08_cp6_final_qa_hardening.py` is forward-only from M7 and changes no frozen object count. It replaces only the body of existing `dante.enforce_occurrence_generation_integrity()` so Role-13 independently acquires the exact occurrence-generation advisory lock before final validation.

The advisory digest is changed at the technical lock-key layer from the pre-closure BLAKE2b planning contract to the cross-language SHA-256 v2 contract frozen by Part 19. No persisted identifier or business data changes.

## Final proof composition

Existing P0/M1..M7 tests remain required. `test_cp6_final.py` adds final-head evidence for:

- exact PostgreSQL 18.6 environment and zero forbidden object families;
- exact 68/5/14/75/95/68/120 topology;
- semantic Dictionary internal integrity;
- Dictionary ↔ SQLAlchemy mapping import/symbol reconciliation;
- Dictionary ↔ Alembic revision/head reconciliation;
- Dictionary ↔ live PostgreSQL relation/column/constraint/index/trigger reconciliation;
- Python ↔ PostgreSQL advisory golden vectors for namespaces 1..7;
- real AsyncSession transaction-lock acquisition/release and deduplication;
- Role-13 final definition proof;
- real two-connection quota race without application locks;
- real two-connection elapsed duplicate race without application locks.

Draft 2020-12 structural validation is intentionally test-tool-only and uses pinned `check-jsonschema==0.37.4`; it is not an application dependency.

## Direct acceptance command

From repository root after pulling the candidate HEAD:

```bash
set -euo pipefail

cd apps/backend
uvx --from check-jsonschema==0.37.4 check-jsonschema --check-metaschema \
  ../../docs/database/dictionary/schema/scope-v1.schema.json \
  ../../docs/database/dictionary/schema/object-v1.schema.json
uvx --from check-jsonschema==0.37.4 check-jsonschema \
  --schemafile ../../docs/database/dictionary/schema/scope-v1.schema.json \
  ../../docs/database/dictionary/scope.json
uvx --from check-jsonschema==0.37.4 check-jsonschema \
  --schemafile ../../docs/database/dictionary/schema/object-v1.schema.json \
  ../../docs/database/dictionary/tables/*.json \
  ../../docs/database/dictionary/views/*.json \
  ../../docs/database/dictionary/routines/*.json

uv run ruff check src tests migrations
uv run mypy
uv run pytest -vv
```

The ordinary full pytest includes the real PostgreSQL-marked suite and therefore requires Docker plus `dante-postgres-local:18.6`.

## LOCAL upgrade after disposable acceptance

Only after the disposable/full suite is green:

```text
persistent LOCAL current head 20260826_07
→ provisioning idempotent rerun
→ alembic upgrade head
→ expected 20260826_08
→ verify unchanged topology
→ docker down/up without --volumes
→ verify head/topology survive
→ backend /health/live + /health/ready
```

## Closure rule

CP6-05 and CP6 remain OPEN until the user-executed direct acceptance on the exact final candidate HEAD is green. No protected-main integration is authorized by this candidate.
