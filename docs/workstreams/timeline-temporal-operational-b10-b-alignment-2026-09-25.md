# Timeline / Temporal-Operational — B10-B alignment checkpoint

Status: **CLOSED / PROVEN — 2026-09-25**

This checkpoint records the canonical B10-B state after reconciling the branch against the published Alembic chain, repairing the first user-local acceptance failures, completing the user-local PostgreSQL re-proof, and committing deterministic generated API artifacts.

Closure evidence: `docs/workstreams/timeline-temporal-operational-b10-b-closure-2026-09-25.md`.

## Canonical persistence frontier

The published B10-B migration chain is immutable:

```text
20260925_75  initial Outcome capability
20260925_76  forward-only Outcome disposition reconciliation
20260925_77  forward-only Outcome ScopedAddress owner-dispatch repair
20260925_78  forward-only Outcome MaterialState totality-dispatch repair
```

`20260925_78` is the proven B10-B persistence frontier. Do not edit `_75` through `_78`; any later persistence correction must be a new forward-only revision.

Proven Dictionary topology:

```text
163|5|119|93|317|268|440
```

`_77` and `_78` replace shared integrity routine bodies only; they do not add standalone objects or change this topology.

The canonical model after `_78` is:

```text
Actual != Outcome
one stable Outcome identity per Actual
Outcome disposition != Outcome identity
Outcome disposition is append-only MaterialState
Outcome disposition is pinned to one exact Actual realization MaterialState
current accepted Outcome state != latest row
idempotency receipt != Outcome identity
Outcome != Confirmation
absence of Outcome != success/failure
```

Canonical physical names:

```text
dante.outcome
dante.outcome_disposition_state
dante.outcome_disposition_current_history
dante.outcome_disposition_operation
facet: outcome.disposition
```

Each disposition state carries:

```text
outcome_ref
actual_realization_material_state_ref
disposition_code
material_state_ref
```

`disposition_code` is contextual. B10-B does not introduce one universal completed/failed/skipped/etc. Outcome enum.

## Proven surfaces

The proven vertical is reconciled across:

```text
apps/backend/src/dante/platform/database/mappings/outcome.py
apps/backend/src/dante/platform/database/mappings/addressing.py
apps/backend/src/dante/platform/database/mappings/__init__.py
apps/backend/src/dante/modules/temporal/outcome_runtime.py
apps/backend/src/dante/modules/temporal/outcome_api.py
apps/backend/tests/integration/temporal/test_b10_b_outcome.py
apps/backend/tests/integration/temporal/test_b10_b_outcome_api.py
apps/backend/tests/test_temporal_openapi_inventory.py
apps/web/src/features/temporal/remote-outcome-data-source.ts
apps/web/src/features/temporal/outcome-controls.tsx
apps/web/src/features/temporal/outcome-controls.test.tsx
docs/database/dictionary/**
docs/database/dictionary/scope.json
packages/api-client/openapi/dante-v1.openapi.json
packages/api-client/src/generated/**
```

The runtime/API contract uses:

```text
actual_ref
actual_realization_material_state_ref
expected_material_state_ref
disposition_code
```

and public reads expose the exact Actual realization basis so a later Actual correction cannot retroactively reinterpret an older Outcome.

Current public route shape:

```text
POST /api/v1/temporal/actuals/{actual_ref}/outcome
GET  /api/v1/temporal/actuals/{actual_ref}/outcome
GET  /api/v1/temporal/outcomes/{outcome_ref}/history
```

History ordering is canonical oldest-to-newest (`current_from_at ASC`), matching the focused B10-B application/API proof.

## Local automated proof

The first user-local B10-B gate proved the non-PostgreSQL surfaces:

```text
API generation       PASS
API client typecheck PASS
web typecheck        PASS
web tests            14/14 PASS
OpenAPI inventory    3/3 PASS
```

The PostgreSQL gate then exposed two bounded persistence defects:

```text
1. the shared CP6 ScopedAddress owner dispatcher did not yet admit scoped_family='outcome';
2. the shared MaterialState totality dispatcher did not yet admit facet='outcome.disposition'.
```

They were repaired forward-only by `_77` and `_78`. The same gate also exposed a stale Dictionary topology count (`443` CHECKs); PostgreSQL and the exact Dictionary object set materialize `440`, so scope/current-catalog snapshots were reconciled to `440` rather than inventing three constraints.

The user-local PostgreSQL re-proof after `_77/_78` is green:

```text
13 passed in 26.18s
POSTGRES TEST EXIT: 0
```

The re-proof covered focused B10-B Outcome application/API, B10-A Actual regression, B09 whole-block regression, and both current-catalog checks.

Generated determinism was then re-run locally by the user:

```text
PASS: generated sources are deterministic and current (335 files)
GENERATED CHECK EXIT: 0
```

Generated OpenAPI/Orval Outcome artifacts were committed and pushed at:

```text
58757fbb  feat(api-client): generate B10-B Outcome contracts
```

## Deferred by B10-B

Still explicitly out of scope:

```text
Confirmation
B10-D reconciliation / resolution workflow
a generic Resolution ontology entity
automatic Session -> Actual
automatic Actual -> Outcome
automatic Outcome -> Confirmation
provider or AI authority over canonical result truth
integrated real-app B10 walkthrough (belongs to B10-E)
```

## Proof status

```text
B10-A  CLOSED / PROVEN
B10-B  CLOSED / PROVEN
B10-C  NEXT — Confirmation
```

No CI/GitHub Actions were authorized or used. The user ran the acceptance gates locally.

## Exact continuation cursor

1. B10-B is closed; do not reopen Outcome semantics without new evidence;
2. prepare the B10-C modification gate against current Product / Domain / Logical / Physical authority for Confirmation;
3. do not implement B10-C until the user approves that gate;
4. do not perform the integrated real-app proof before B10-E.
