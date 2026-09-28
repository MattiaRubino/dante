# B13-A Work Structure Core — implementation checkpoint

- **Branch:** `feature/timeline-temporal-operational`
- **Status:** CANDIDATE — local PostgreSQL, API, web, generated-client and catalog gates pending
- **Migration source head:** `20260928_88`
- **Prior proven persistence frontier:** B11-C / `20260927_86`

## Discovery decisions

The CP6 `dante.plan` identity shell and `native_address` owner family are sufficient. Plan needs its own intention/owner, accepted work revision, current binding and history; it is never an Activity wrapper. B13-A uses a flat `Plan -> Step` structure. Recursive hierarchy and cycle semantics are deferred because no accepted B13-A authority requires nesting.

Each Step has an internal UUIDv7 reference owned by exactly one Plan. A normalized, immutable revision snapshot records membership, Step title, zero-based presentation position and an optional real Activity reference. The Step does not receive a generic root `work_item` identity. An Activity link must refer to an Activity owned by the same self Person and does not change the Activity's lifecycle or Schedule. Duplicate Step membership, duplicate linked Activity in a revision and cross-Plan Step reuse are rejected.

The API replaces a complete bounded snapshot with expected-current CAS and a replay-safe operation receipt. Earlier snapshots remain queryable as historical rows; reads join the explicit current binding and open history episode. Positions are consecutive by guarded write, not inferred Dependency edges. The UI supports creating a Plan, adding/removing/reordering Steps and attaching/detaching an existing Activity reference. This gate creates no Dependency, solver proposal, Session constraint or implicit Schedule mutation.

## Candidate surfaces

```text
_87 forward-only migration
_88 forward-only replay and catalog-identifier repair
seven typed Plan work tables + four guarded self-scoped functions
SQLAlchemy mapping inventory + Dictionary entries
Plan application / HTTP OpenAPI routes
Home Plan/Step panel + governed web data source
focused PostgreSQL, OpenAPI and web tests
```

The expected topology is `191|5|148|100|386|334|488|0|0|0`. The first user-run PostgreSQL gate reached `_87` and matched the topology, but exposed a replay SQL column error and eight check-constraint names that differed from the Dictionary. The follow-up `_88` corrects both without changing data or topology. OpenAPI tests, web/API typechecks and deterministic client generation passed; the focused PostgreSQL test, exact catalog and one UI test must be rerun after this repair.

## Exit gate

Run the B13-A PostgreSQL test, exact current catalog tests and repaired UI test at `_88`; record actual outputs. The generated API client remains on the user's local worktree and must be committed from the deterministic generator. Only after all applicable gates pass should the roadmap, map and handoff advance to B13-B.
