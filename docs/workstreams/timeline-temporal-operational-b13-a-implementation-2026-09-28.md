# B13-A Work Structure Core — implementation checkpoint

- **Branch:** `feature/timeline-temporal-operational`
- **Status:** CANDIDATE — local PostgreSQL, API, web, generated-client and catalog gates pending
- **Migration source head:** `20260928_89`
- **Prior proven persistence frontier:** B11-C / `20260927_86`

## Discovery decisions

The CP6 `dante.plan` identity shell and `native_address` owner family are sufficient. Plan needs its own intention/owner, accepted work revision, current binding and history; it is never an Activity wrapper. B13-A uses a flat `Plan -> Step` structure. Recursive hierarchy and cycle semantics are deferred because no accepted B13-A authority requires nesting.

Each Step has an internal UUIDv7 reference owned by exactly one Plan. A normalized, immutable revision snapshot records membership, Step title, zero-based presentation position and an optional real Activity reference. The Step does not receive a generic root `work_item` identity. An Activity link must refer to an Activity owned by the same self Person and does not change the Activity's lifecycle or Schedule. Duplicate Step membership, duplicate linked Activity in a revision and cross-Plan Step reuse are rejected.

The API replaces a complete bounded snapshot with expected-current CAS and a replay-safe operation receipt. Earlier snapshots remain queryable as historical rows; reads join the explicit current binding and open history episode. Positions are consecutive by guarded write, not inferred Dependency edges. The UI supports creating a Plan, adding/removing/reordering Steps and attaching/detaching an existing Activity reference. This gate creates no Dependency, solver proposal, Session constraint or implicit Schedule mutation.

## Candidate surfaces

```text
_87 forward-only migration
_88 forward-only replay and catalog-identifier repair
_89 forward-only replace-current binding qualification
seven typed Plan work tables + four guarded self-scoped functions
SQLAlchemy mapping inventory + Dictionary entries
Plan application / HTTP OpenAPI routes
Home Plan/Step panel + governed web data source
focused PostgreSQL, OpenAPI and web tests
```

The expected topology is `191|5|148|100|386|334|488|0|0|0`. The first user-run PostgreSQL gate reached `_87` and matched the topology, but exposed a replay SQL column error and eight check-constraint names that differed from the Dictionary. The follow-up `_88` corrected both without changing data or topology. Its first published source used the reserved SQL alias `constraint` and failed transactionally during fixture migration setup; no `_88` application was observed. The alias was corrected in the same unapplied revision so the migration chain could run. The next local run reached Plan replacement and exposed an ambiguous unqualified `plan_ref`; `_89` qualifies the accepted-current binding with a table alias. OpenAPI tests, web/API typechecks, the UI test and deterministic client generation passed; the generated client was committed as `96f2f7b9`. The focused PostgreSQL test and exact catalog still need a local rerun.

## Exit gate

Run the B13-A PostgreSQL test and exact current catalog tests at `_89`; record actual outputs. Only after all applicable gates pass should the roadmap, map and handoff advance to B13-B.
