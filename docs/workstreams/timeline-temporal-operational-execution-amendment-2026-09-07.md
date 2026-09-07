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

## 4. B00 Create fake-success retirement checkpoint

The C1-era Create runtime previously defaulted to an `InMemoryTemporalWorkspace`. In normal runtime this allowed a prepared Create command to receive `applied`, materialize a local Timeline card and close the draft even though no backend persistence had occurred.

That behavior is now forbidden at the runtime factory boundary:

```text
explicit authoritative workspace injected
→ use that workspace

mode == test and no workspace injected
→ InMemoryTemporalWorkspace allowed

mode != test and no workspace injected
→ fail closed with temporal.create.backend_unavailable
→ no applied effect
→ no local Timeline materialization
→ draft remains available to the user through the existing failure lifecycle
```

The unavailable workspace is not a persistence substitute. It exists only to make unsupported normal-runtime writes fail truthfully until B01 activates the first real `CreateActivity` backend operation.

A dedicated boundary test covers production/development fail-closed behavior, test-mode in-memory behavior and explicit workspace injection.

This preserves the required distinction:

```text
Create draft / preview
!= canonical Activity/Event

frontend prepared command
!= accepted backend effect

local in-memory projection
!= persistence

pending / unavailable
!= applied
```

## 5. B00 real PostgreSQL runtime-spine proof checkpoint

The existing backend integration harness already provides disposable PostgreSQL 18.6 clusters, fresh provisioned databases and Alembic-to-head migration. B00 now reuses that accepted harness rather than creating a second testing architecture.

A temporal integration suite has been added under `apps/backend/tests/integration/temporal/` to exercise the complete request spine against a real migrated PostgreSQL database:

```text
synthetic isolated account
→ real password sign-in
→ real AuthSession cookie
→ GET /api/v1/temporal/timeline/window
→ require_dante_context()
→ lazy AccountApplicationContext establishment
→ self Person creation
→ X-Dante-Time-Zone resolution
→ truthful empty temporal response
```

The proof also verifies the negative bootstrap rule:

```text
follow-device account + missing device timezone
→ 400 context.device_timezone_required
→ no AccountApplicationContext row created
→ no malformed bootstrap side effect
```

The public Timeline response continues not to expose `self_person_ref`; that reference remains an internal application-context concern.

This integration suite is committed but has not yet been executed in this connector-only session. Therefore it is evidence of implemented test coverage, not evidence that the PostgreSQL gate has passed.

## 6. Current B00 checkpoint semantics

B00 remains **IN PROGRESS**. No green-check claim is made merely because code or tests exist; automated suites and manual acceptance still have to run under the workstream Definition of Done.

Implemented boundaries now include:

- authenticated backend temporal read/API boundary;
- strict frontend remote temporal read adapter;
- Home/Timeline consumption of that real read boundary;
- truthful loading/error/retry behavior;
- normal-runtime prototype card/clock isolation;
- normal-runtime Create fake-success retirement;
- real PostgreSQL integration proof for AuthSession → DanteContext → self Person → timezone → temporal endpoint.

Still required before B00 can become `✅` include at minimum:

- execute the full frontend/backend automated quality suites;
- execute the real PostgreSQL integration suite against the certified image;
- define/confirm the isolated manual `userTest` setup and deterministic cleanup flow without conflating it with automated synthetic fixtures;
- manual empty/error/real-path acceptance through the actual product surface;
- full F0/T1 regression proof under the executed test suite;
- activate a real PostgreSQL-backed temporal product read when B01 introduces the first semantically legitimate persistent temporal product family.

No checklist item may be marked green until its applicable Definition-of-Done gates have actually passed.
