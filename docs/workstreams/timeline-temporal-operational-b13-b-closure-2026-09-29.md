# B13-B — Qualified Dependencies closure

- **Date:** 2026-09-29
- **Branch:** `feature/timeline-temporal-operational`
- **Status:** CLOSED / focused local automated proof
- **Persistence frontier:** Alembic `20260928_90`
- **Catalog-verified topology:** `196|5|152|100|397|344|496|0|0|0`
- **Whole-B13 real-app acceptance:** reserved for B13-D

## Scope closed

B13-B adds self-owned, Plan-scoped qualified Dependency records between two distinct current Plan Steps that each bind a distinct real Activity. The relation preserves direction, immutable endpoint bindings, qualifier revision history, explicit current binding and operation receipts. It is neither Plan containment nor Step ordering.

The supported prerequisite qualifiers are:

```text
actual_occurred
outcome_code (exact disposition)
```

Evaluation derives from accepted current Actual/Outcome truth:

```text
satisfied | unsatisfied | unknown
```

Missing Actual/Outcome basis and a stale Outcome-to-Actual basis remain `unknown`; no dependency write creates or changes a Schedule, Actual or Outcome. Active duplicate claims are rejected, reverse claims remain distinct and cycles are explicitly visible rather than silently converted into a scheduling constraint. Plan replacement rejects removal or relinking of an endpoint used by an active Dependency, while title changes and reordering remain valid.

## Local proof reported by the user

```text
PostgreSQL B13-B + exact catalog reconciliation    11 passed in 41.75s
```

The suite covers fresh forward migration, self ownership, replay/CAS, endpoint guards, immutable revision history and retirement, both Actual/Outcome truth tables, correction/stale-basis behavior, duplicate/reverse/cycle behavior, and the exact Dictionary/live-catalog/mapping/ACL reconciliation.

Earlier in the published candidate, the focused web gate passed **6 tests** across the Dependency data source and Plan panels; web and API-client typechecks passed. Backend OpenAPI/inventory tests, Ruff, mypy and deterministic generated-client regeneration also passed. The final commit `e19d3b0` changes only the integration test: it introduces a third Activity so the relink guard is tested without violating the separate B13-A unique Activity-per-Step invariant.

No CI/GitHub Actions were used.

## Continuation

B13-C is next. It may add only execution-structure constraints supported by the current Product/Domain/Logical authority; it must not reinterpret or duplicate B13-B Dependency semantics. B13-D remains responsible for the complete B13 A/B/C integration gate and real-app acceptance. B12 stays held until B13-D closes.
