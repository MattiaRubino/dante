# B13-B implementation checkpoint — focused local proof obtained

- **Status:** IMPLEMENTED / FOCUSED LOCAL AUTOMATED PROOF OBTAINED; closed 2026-09-29
- **Base:** `1f7ecca73ca2816d8aa0da838734ad67daf9fba5`
- **Semantic authority:** `timeline-temporal-operational-b13-b-scope-2026-09-28.md`
- **Candidate Alembic head:** `20260928_90` (forward only)
- **Verified live head:** B13-B `20260928_90`

## Source inventory and physical decisions

1. B13-A uses `plan_intention`, `plan_step`, immutable `plan_work_state` snapshots, explicit `plan_current_work_state` and `plan_work_current_history`, and guarded self operations. The latest replacement routine is the forward repair at Alembic `20260928_89`; earlier migrations remain immutable.
2. The first relation is a Plan-owned LR-03 record with its own scoped UUIDv7 address. Registering the `plan_dependency` scoped family requires a forward alteration to `scoped_address`'s family constraint. The relation keeps both Step refs and their bound Activity refs, with direction, dependent admissibility facet and one typed qualifier. It does not become a root Domain identity or a generic graph edge.
3. Accepted qualifier revisions, explicit current binding, historical states, operation receipt and retirement must be separate from Plan work snapshots. Revising a dependency must leave Plan identity and Step order untouched. Replay checks precede current-revision CAS, but a reused operation ID with a different fingerprint is rejected.
4. The Plan owner row is the shared serialization lock for relation authoring and Plan replacement. A new forward definition of `replace_self_plan_work` must refuse removal or relinking of an active relation's endpoints before advancing current Plan state. Reorder and title changes retain both bindings. A relationship write validates both endpoints against the same current Plan snapshot and self-owned Activity links under that lock.
5. Actual evaluation reads `actual.subject_native_ref`, `actual_current_realization`, and `actual_realization_state.realization_occurred`. Outcome evaluation reads the one `outcome` for that Actual, `scoped_current_material_state` with facet `outcome.disposition`, and `outcome_disposition_state`; the Outcome's `actual_realization_material_state_ref` must equal the current Actual state. Missing basis means unknown, not unsatisfied.
6. Reject exact active duplicate claims in the guarded write. A reversed direction remains distinct. Cycle diagnostics can be derived over the bounded Plan edge set in the application read, without a DAG constraint, transitive persistence, or a global blocked field.
7. The backend uses one self-scoped guarded capability and Plan-scoped HTTP author/read/revise/retire/history routes. The web Plan panel exposes both qualifiers and per-relation evaluation; the generated API client must be regenerated deterministically. PostgreSQL/Dictionary/ORM/canonical catalog counts must be reconciled in the same implementation scope.

## Verification to obtain before closure

- Fresh forward migration on PostgreSQL 18, replay and CAS, ownership and endpoint guards, immutable history/retirement, both qualifier truth tables, stale Outcome basis and correction, duplicate/cycle behavior, and unchanged Schedule/Actual/Outcome on dependency writes.
- Exact Dictionary/live catalog/mapping/ACL reconciliation, HTTP OpenAPI inventory, deterministic API client generation, web tests and typechecks.
- Focused local test command and result supplied by the user. B13-D retains the integrated real-app walkthrough; CI is outside this workstream.

## Candidate implementation and local verification

- `_90` adds five tables, four guarded functions, a bounded `plan_dependency` scoped address, and a forward patch to the active Plan replacement function. A Plan row lock serializes relation writes with structure replacement. Active relation endpoints cannot disappear or relink; historical assertions and operation receipts remain intact.
- Self-scoped HTTP routes provide create, list, read, revise, retire and history. The generated client and Home Plan panel expose typed Actual/Outcome conditions, derived evaluation, and cycle diagnostics. The relation records purpose, direction and both Activity bindings.
- The Dictionary and ORM inventory describe 196 tables, five views, 152 routines, 100 triggers, 397 physical indexes, 344 foreign keys and 496 checks. These counts were subsequently reconciled by the exact live PostgreSQL/catalog gate. The five new tables contribute 11 indexes (five primary keys, three unique constraints and three explicit indexes).
- In this worktree, 9 OpenAPI tests and 4 static inventory tests passed; 6 focused web tests passed. Ruff lint/format, backend mypy for the new source files, web/API-client TypeScript checks and byte-identical client regeneration after Orval plus Prettier passed. The PostgreSQL suite cannot run in this workspace because no local PostgreSQL cluster/container is available. No CI/Actions ran.

After the exact implementation Git gate is approved and the candidate is published, run from a clean pull on the branch:

```bash
cd ~/projects/dante
git pull --ff-only origin feature/timeline-temporal-operational
cd apps/backend
uv run --locked pytest -q --no-cov --tb=short -m postgres \
  tests/integration/temporal/test_b13_b_plan_dependency.py \
  tests/integration/database/test_current_catalog.py \
  tests/integration/database/test_database_current_catalog.py \
  tests/integration/database/test_b11_catalog_reconciliation_probe.py
cd ../..
pnpm --filter @dante/web exec vitest run \
  src/features/temporal/plan-dependency-panel.test.tsx \
  src/features/temporal/remote-plan-dependency-data-source.test.ts \
  src/features/temporal/plan-work-panel.test.tsx
pnpm --filter @dante/web typecheck
pnpm --filter @dante/api-client typecheck
```

## Closure evidence

The user pulled the final test-only correction `e19d3b0` and ran the focused PostgreSQL/catalog gate on 2026-09-29:

```text
PostgreSQL B13-B + exact catalog reconciliation    11 passed in 41.75s
```

The candidate's earlier static/backend OpenAPI checks, Ruff/mypy, deterministic generated-client check, focused web tests (6) and web/API-client typechecks had already passed. The final correction changes only the B13-B integration test so it tests the active-Dependency relink guard without violating the independent one-Activity-per-Step invariant. No CI/Actions ran. B13-B is closed; B13-D retains whole-B13 product acceptance.

## Publication boundary

This candidate is not a remote checkpoint. The approved semantic scope did not authorize the implementation file set. Before its remote write, present the exact created and updated paths at this base SHA and obtain explicit approval under `docs/development/agent-operating-manual.md` §5. A moved branch requires re-inspection and re-gating. B13-B closure is a later evidence update after the focused PostgreSQL suite passes.
