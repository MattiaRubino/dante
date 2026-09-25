# Timeline / Temporal-Operational — B10-B alignment checkpoint

Status: **IMPLEMENTATION CANDIDATE REPAIRED / AWAITING USER LOCAL POSTGRESQL RE-PROOF — 2026-09-25**

This checkpoint records the canonical B10-B state after reconciling the branch against the published Alembic chain and repairing the first user-local acceptance failures. It is a continuation aid and candidate handoff, not closure evidence.

## Canonical persistence frontier

The published B10-B migration chain is immutable:

```text
20260925_75  initial Outcome capability
20260925_76  forward-only Outcome disposition reconciliation
20260925_77  forward-only Outcome ScopedAddress owner-dispatch repair
20260925_78  forward-only Outcome MaterialState totality-dispatch repair
```

`20260925_78` is the current B10-B persistence candidate. Do not edit `_75` through `_78`; any later persistence correction must be a new forward-only revision.

Candidate Dictionary topology:

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

## Candidate surfaces reconciled

The current branch has been reconciled through `_78` across:

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

## First local gate and repairs

The first user-local B10-B gate proved the non-PostgreSQL surfaces:

```text
API generation       PASS
API client typecheck PASS
web typecheck        PASS
web tests            14/14 PASS
OpenAPI inventory    3/3 PASS
```

The PostgreSQL gate exposed two bounded persistence defects:

```text
1. the shared CP6 ScopedAddress owner dispatcher did not yet admit scoped_family='outcome';
2. the shared MaterialState totality dispatcher did not yet admit facet='outcome.disposition'.
```

They are repaired forward-only by `_77` and `_78`. The same gate also exposed a stale Dictionary topology count (`443` CHECKs); PostgreSQL and the exact Dictionary object set materialize `440`, so scope/current-catalog snapshots are reconciled to `440` rather than inventing three constraints.

## Remaining acceptance work

The implementation candidate is coherent. The remaining work is acceptance, not more feature implementation:

```text
1. user pulls the repaired branch;
2. user reruns the focused B10-B PostgreSQL/regression/catalog gate;
3. if PostgreSQL is green, user runs the correct generated determinism command: pnpm generated:check;
4. generated artifacts already produced locally are committed only after the local gate is green;
5. only then reconcile closure docs and mark B10-B CLOSED / PROVEN.
```

Generated artifacts must be produced through repository tooling and must never be hand-edited.

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
B10-B  IMPLEMENTATION CANDIDATE REPAIRED / AWAITING USER LOCAL POSTGRESQL RE-PROOF
```

No CI/GitHub Actions are authorized or used. The user runs the acceptance gate locally.

## Exact continuation cursor

1. pull the branch;
2. rerun the focused B10-B PostgreSQL/regression/catalog gate;
3. if failures appear, repair them without starting B10-C;
4. if green, run `pnpm generated:check` against the already generated local artifacts;
5. commit generated artifacts, reconcile roadmap/map/handoff/DB closure evidence, mark B10-B CLOSED / PROVEN and prepare the B10-C modification gate;
6. do not perform the integrated real-app proof before B10-E.
