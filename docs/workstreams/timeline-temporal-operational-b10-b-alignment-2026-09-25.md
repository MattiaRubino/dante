# Timeline / Temporal-Operational — B10-B alignment checkpoint

Status: **IMPLEMENTATION CANDIDATE READY / AWAITING USER LOCAL PROOF — 2026-09-25**

This checkpoint records the canonical B10-B state after reconciling the branch against the published Alembic chain. It is a continuation aid and candidate handoff, not closure evidence.

## Canonical persistence frontier

The published B10-B migration chain is immutable:

```text
20260925_75  initial Outcome capability
20260925_76  forward-only Outcome disposition reconciliation
```

`20260925_76` is the binding B10-B persistence contract. Do not edit `_75` or `_76`; any later persistence correction must be a new forward-only revision.

Candidate Dictionary topology:

```text
163|5|119|93|317|268|443
```

The canonical model after `_76` is:

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

The current branch has been reconciled to `_76` across:

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

## Remaining acceptance work

The implementation candidate is coherent. The remaining work is acceptance, not more feature implementation:

```text
1. user pulls the current branch;
2. user runs pnpm api:generate locally so OpenAPI/Orval reflect the current Outcome API;
3. generated determinism + API-client/web typechecks run locally;
4. focused B10-B web/OpenAPI/PostgreSQL tests and B10-A/B09/B08/catalog regressions run locally;
5. generated artifacts are committed only after the local gate is green;
6. only then reconcile closure docs and mark B10-B CLOSED / PROVEN.
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
B10-B  IMPLEMENTATION CANDIDATE READY / AWAITING USER LOCAL PROOF
```

No CI/GitHub Actions are authorized or used. The user runs the acceptance gate locally.

## Exact continuation cursor

1. pull the branch;
2. regenerate OpenAPI/client locally with repository tooling;
3. run the single B10-B local automated gate;
4. if failures appear, repair them without starting B10-C;
5. if green, commit generated artifacts, reconcile roadmap/map/handoff/DB closure evidence, mark B10-B CLOSED / PROVEN and prepare the B10-C modification gate;
6. do not perform the integrated real-app proof before B10-E.
