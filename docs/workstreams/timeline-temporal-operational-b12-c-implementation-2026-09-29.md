# B12-C — reviewed single Schedule move — implementation checkpoint

- **Status:** IMPLEMENTED CANDIDATE / LOCAL POSTGRESQL GATE PENDING
- **Approved scope:** `timeline-temporal-operational-b12-c-scope-2026-09-29.md` (user approved 2026-09-29)
- **Source head:** Alembic `20260929_93`, forward from proven `_92`
- **Acceptance cadence:** focused automated gate now; integrated real-app walkthrough only in B12-D before B12 closure

## Effect boundary

Home offers an explicit review of one B12-B candidate against the old/current interval and its capacity limitation. The request carries an operation id and reviewed Plan/Step, Schedule, Movement Policy and candidate basis. Backend reruns B12-B search and checks membership in its supported OPTIMAL candidate set. A new definer function locks the self Plan and relevant evidence, verifies Plan/Step, sole Schedule, exact Policy, every active qualified Dependency plus Actual/Outcome state, and every subject Constraint state, then calls canonical B04-D within the same transaction. B04-D owns current placement/Policy/hard-rule checks, a direct committed move or a pending proposal, and replay receipts. The separate confirmation repeats the basis guard and delegates B04-D acceptance. Identical concurrent operation ids serialize on the Plan lock before receipt lookup; a different intent is rejected.

The `_93` migration adds three functions and no tables, views, indexes, triggers or constraints. The Dictionary has three corresponding routine entries. Expected topology is `196|5|155|100|397|344|497|0|0|0`, pending live catalog proof. Existing `_92` proof remains the latest PostgreSQL-proven head until the user runs the gate.

The authenticated API exposes request and confirmation routes and generated client models. Home uses CSRF, shows pending proposals separately from accepted Schedule state, and refreshes the selected Plan candidate after a committed effect. It continues to state that availability and capacity were not evaluated.

## Local gate and closure condition

The authoring workspace has no PostgreSQL service. Ruff, mypy, OpenAPI contract, client/web typechecks and component tests run here; their exact results belong in the handoff after publication. User runs the focused PostgreSQL integration and exact catalog suite in the worktree and reports complete output. Correct any failure forward-only, rerun the gate, then record B12-C closure. Do not substitute this checkpoint for user-run persistence proof or B12-D real-app acceptance.
