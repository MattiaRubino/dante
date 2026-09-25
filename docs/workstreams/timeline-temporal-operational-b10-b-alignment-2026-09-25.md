# Timeline / Temporal-Operational — B10-B alignment checkpoint

Status: **IN PROGRESS / NOT YET PROVEN — 2026-09-25**

This checkpoint records the canonical B10-B state after reconciling the branch against the published Alembic chain. It is a continuation aid, not closure evidence.

## Canonical persistence frontier

The published B10-B migration chain is immutable:

```text
20260925_75  initial Outcome capability
20260925_76  forward-only Outcome disposition reconciliation
```

`20260925_76` is the binding B10-B persistence contract. Do not edit `_75` or `_76`; any later persistence correction must be a new forward-only revision.

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

## Reconciliation completed in this checkpoint

The branch had drifted back toward the transient `_75` vocabulary/result representation even though `_76` was already the published forward repair. The following implementation surfaces were realigned to `_76` without rewriting published migrations:

```text
apps/backend/src/dante/platform/database/mappings/outcome.py
apps/backend/src/dante/platform/database/mappings/addressing.py
apps/backend/src/dante/platform/database/mappings/__init__.py
apps/backend/src/dante/modules/temporal/outcome_runtime.py
apps/backend/src/dante/modules/temporal/outcome_api.py
```

The runtime/API contract now uses:

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

## Still open before B10-B can be called complete

The following surfaces may still reflect the old transient `_75` vocabulary/result model and must be reconciled against this checkpoint before B10-B closure:

```text
OpenAPI export / snapshots
packages/api-client generated output — generator only, never hand-edit
web Outcome remote data source
web Outcome author/correct/read controls
B10-B backend/API/web/PostgreSQL tests
Database Dictionary / scope / database overlay
roadmap/map status ledger
```

Do not infer that those surfaces are correct merely because files already exist. Compare them to `_76` and this checkpoint first.

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

No acceptance claim is made by this checkpoint. The user explicitly did not request a local test cycle during this alignment pass. Therefore:

```text
B10-A  CLOSED / PROVEN
B10-B  IN PROGRESS / UNPROVEN
```

No CI/GitHub Actions were used.

## Exact continuation cursor

On the next continuation:

1. read this checkpoint and the approved B10-B scope;
2. re-fetch branch HEAD before any write;
3. treat `20260925_76` as the canonical B10-B persistence contract;
4. reconcile OpenAPI/generated client through the repository generator, never by hand;
5. reconcile the web Outcome surface from vocabulary/result to disposition + exact Actual realization basis;
6. reconcile Dictionary/database docs and B10-B focused tests;
7. only after the full candidate is coherent may a user-run local gate be proposed;
8. do not mark B10-B CLOSED / PROVEN without that later evidence.
