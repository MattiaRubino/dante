# B11-B — Conditional Temporal Behavior — Local proof checkpoint

- **Date:** 2026-09-27
- **Branch:** `feature/timeline-temporal-operational`
- **Scope:** `timeline-temporal-operational-b11-b-scope-2026-09-27.md`
- **Persistence head:** `20260927_85` (forward-only after `_82`–`_84`)
- **Implementation checkpoint:** `1f0af49c6c218e9c67a51b1ffae0c4a9bdf81af8`
- **Generated client checkpoint:** `e79f68702c7a6ad6d1a41b4fc92b4a6cdf646a11`
- **Classification:** LOCAL AUTOMATED GATE PROVEN; documentation/catalog reconciliation still open

## User-run local proof

After pulling `1f0af49c`, the user ran the repository generator and the focused tests in `~/projects/dante`. Reported results:

```text
pnpm api:generate                             completed
pnpm generated:check                         PASS, 361 files deterministic/current
@dante/api-client typecheck                  PASS
@dante/web typecheck                         PASS
conditional controls / truth inspector      3 passed, 2 files
B11-A + B11-B OpenAPI contract               6 passed
B11-A + B11-B PostgreSQL integration        4 passed
```

The generated OpenAPI/client diff (four files) was committed and pushed by the user at `e79f6870`; it was not manually edited. The `react-i18next` test warning did not fail the gate. No GitHub Actions/CI were used. The real-app walkthrough is reserved for the complete B11 block.

## Truth boundaries exercised

The `actual_realization` Condition is self-scoped for Activity/Event/Occurrence; Routine is not a direct Actual subject. The absence of accepted Actual yields `indeterminate/withhold`, not false reality. Evaluation pins accepted Actual plus exact MaterialState when present, does not mutate other canonical owners, and remains historical after later correction. The added read-by-typed-subject API prevents reload from treating an existing Condition as a new intent. Creation/evaluation operation ids are not Condition/Evaluation identities.

## Reconciliation outstanding before formal vertical closure

The live roadmap/map/handoff still declare B11 as next and the candidate DB overlay ends at `_80`; Dictionary `scope.json` still reports B10-C `_79`. These declarations are stale relative to the published `_81`–`_85` migrations. A focused test pass is not a whole-catalog tuple. Reconcile the current DB reference and Dictionary against the actual Alembic/SQLAlchemy/PostgreSQL catalog, record the measured topology rather than an inferred count, and update the workstream ledger before marking B11-B `CLOSED / PROVEN`.
