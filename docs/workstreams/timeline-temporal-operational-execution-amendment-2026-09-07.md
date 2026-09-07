# Timeline / Temporal-Operational — Execution Amendment 2026-09-07

- **Status:** ACTIVE EXECUTION AMENDMENT
- **Workstream branch:** `feature/timeline-temporal-operational`
- **Protected-main SHA reverified before B00 implementation:** `981f6cf9ad985d0b811bc4172c12a7529fbc9b15`
- **Database authority:** PostgreSQL 18.6 / Alembic `20260906_18`

## 1. Branch discipline amendment

The product owner explicitly selected **one branch for the whole Timeline / Temporal-Operational vertical**.

Therefore this amendment supersedes only the branch-per-block guidance in
`timeline-temporal-operational-roadmap.md §0.7`.

Canonical execution rule from this point forward:

```text
feature/timeline-temporal-operational
└── B00 → B01 → ... → B14
```

No `feature/temporal-b00-*`, `feature/temporal-b01-*`, or equivalent implementation branches are part of the accepted execution plan.

The semantic map, block ordering, Definition-of-Done gates, no-runtime-mock rule, forward-migration rule and protected-main safety rules remain unchanged.

Reviewability is preserved through bounded commits/slices and the live implementation ledger rather than branch proliferation.

## 2. B00 first implementation slice

This slice establishes the first real transport/data-source seam without inventing product persistence:

```text
authenticated request
→ require_dante_context()
→ Account → self Person
→ effective request timezone
→ Temporal Timeline application boundary
→ bounded half-open local-date window
→ HTTP transport
→ governed web fetch
→ strict frontend temporal Timeline data source
```

B00 deliberately returns a truthful empty projection until a later block activates a semantically justified real temporal projection family.

This is not authorization for:

- generic `temporal_item` persistence;
- generic `timeline_entry` persistence;
- Activity/Event/Routine schema invented merely to create demo cards;
- frontend inference of canonical semantics;
- fake success after transport/backend failure.

## 3. B00 runtime fixture-isolation checkpoint

The accepted T1 prototype dataset is retained only as regression-test material. Its runtime exports are now guarded by one explicit mode predicate:

```text
mode == test
→ frozen prototype clock/groups/cards available

mode != test
→ real device-zone wall clock
→ zero prototype groups
→ zero prototype store rows
→ zero generated fallback cards
```

This closes the previously separate fake-card entry paths at their common source:

- `createInitialTimelineState()` can no longer seed prototype store/groups in normal runtime;
- `timelineEventsForDate()` can no longer manufacture distant-date fallback cards in normal runtime;
- `buildTimelineRenderedDays()` may still call the legacy fixture helper, but that helper is incapable of returning prototype cards outside explicit test mode;
- the Timeline surface legacy clock exports resolve to the real device-zone wall clock outside explicit test mode.

A dedicated regression test proves that `production` and `development` modes return no prototype groups/cards/store while `test` retains the frozen T1 dataset.

This checkpoint is deliberately narrower than full B00 completion. In particular, it does **not** make the existing Create in-memory workspace canonical and does not authorize local materialization as successful persistence.

## 4. Current B00 checkpoint semantics

B00 remains **IN PROGRESS**. No green-check claim is made merely because code exists; automated suites and manual acceptance still have to run under the workstream Definition of Done.

Still required before B00 can become `✅` include at minimum:

- consume the real temporal data source from the normal Timeline surface rather than merely exposing the adapter;
- retire/contain the Create in-memory workspace so normal runtime cannot present ephemeral local materialization as canonical backend success;
- establish the real PostgreSQL-backed temporal query seam at the first semantically legitimate readable family;
- define isolated `userTest`/test-data setup and cleanup;
- establish real backend + real PostgreSQL E2E harness;
- manual empty/error/real-path acceptance;
- full F0/T1 regression proof.

No checklist item may be marked green until its applicable Definition-of-Done gates have actually passed.
