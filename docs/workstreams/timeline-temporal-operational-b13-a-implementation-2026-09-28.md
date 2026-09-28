# B13-A Work Structure Core — implementation checkpoint

- **Branch:** `feature/timeline-temporal-operational`
- **Status:** CANDIDATE — local PostgreSQL, API, web, generated-client and catalog gates pending
- **Migration source head:** `20260928_87`
- **Prior proven persistence frontier:** B11-C / `20260927_86`

## Discovery decisions

The CP6 `dante.plan` identity shell and `native_address` owner family are sufficient. Plan needs its own intention/owner, accepted work revision, current binding and history; it is never an Activity wrapper. B13-A uses a flat `Plan -> Step` structure. Recursive hierarchy and cycle semantics are deferred because no accepted B13-A authority requires nesting.

Each Step has an internal UUIDv7 reference owned by exactly one Plan. A normalized, immutable revision snapshot records membership, Step title, zero-based presentation position and an optional real Activity reference. The Step does not receive a generic root `work_item` identity. An Activity link must refer to an Activity owned by the same self Person and does not change the Activity's lifecycle or Schedule. Duplicate Step membership, duplicate linked Activity in a revision and cross-Plan Step reuse are rejected.

The API replaces a complete bounded snapshot with expected-current CAS and a replay-safe operation receipt. Earlier snapshots remain queryable as historical rows; reads join the explicit current binding and open history episode. Positions are consecutive by guarded write, not inferred Dependency edges. The UI supports creating a Plan, adding/removing/reordering Steps and attaching/detaching an existing Activity reference. This gate creates no Dependency, solver proposal, Session constraint or implicit Schedule mutation.

## Candidate surfaces

```text
_87 forward-only migration
seven typed Plan work tables + four guarded self-scoped functions
SQLAlchemy mapping inventory + Dictionary entries
Plan application / HTTP OpenAPI routes
Home Plan/Step panel + governed web data source
focused PostgreSQL, OpenAPI and web tests
```

The expected `_87` topology derived from the migration delta is `191|5|148|100|386|334|488|0|0|0`. This is **not yet a measured PostgreSQL result**. The user-run catalog gate must verify it before B13-A can be marked PROVEN.

## Exit gate

Run the B13-A PostgreSQL test, the exact current catalog tests, the OpenAPI contract and inventory, web tests and typechecks, then deterministic API client generation/check. Record actual outputs; repair any discrepancy with a new forward migration if `_87` has been applied/published. Only after all applicable gates pass should the roadmap, map and handoff advance to B13-B.
