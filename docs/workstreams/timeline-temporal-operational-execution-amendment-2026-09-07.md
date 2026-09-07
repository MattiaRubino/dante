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

B00 deliberately returns a truthful empty projection until a later block activates a semantically justified real temporal product projection family.

This is not authorization for:

- generic `temporal_item` persistence;
- generic `timeline_entry` persistence;
- Activity/Event/Routine schema invented merely to create demo cards;
- frontend inference of canonical semantics;
- fake success after transport/backend failure.

The B00 exit condition is **not** that Activity/Event product rows already exist. B00 closes when the shared real-data spine is proven ready for B01. The first real temporal product read is intentionally activated by B01 together with the first legitimate persistent Activity projection.

## 3. B00 runtime fixture-isolation checkpoint

The accepted T1 prototype dataset is retained only as regression-test material. Its runtime exports are guarded by one explicit mode predicate:

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

The existing backend integration harness already provides disposable PostgreSQL 18.6 clusters, fresh provisioned databases and Alembic-to-head migration. B00 reuses that accepted harness rather than creating a second testing architecture.

A temporal integration suite exists under `apps/backend/tests/integration/temporal/` to exercise the complete request spine against a real migrated PostgreSQL database:

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

## 6. B00 browser → web → API → PostgreSQL E2E checkpoint

B00 reuses the already accepted Access/Auth full-stack Playwright harness instead of introducing a second browser stack.

The existing harness owns:

- a disposable `dante-postgres-local:18.6` container;
- fresh database provisioning and Alembic upgrade to head;
- real `dante_runtime` FastAPI;
- same-origin HTTPS Vite production preview;
- synthetic isolated accounts;
- browser execution across Chromium, Firefox and WebKit;
- teardown of the disposable stack after the run.

`apps/web/e2e/auth/temporal-b00-runtime-spine.spec.ts` now carries three vertical proofs.

### Proof A — real empty Timeline read

```text
browser in Europe/Rome
→ real UI sign-in
→ real AuthSession cookie
→ /home
→ createWebFetch()
→ X-Dante-Time-Zone: Europe/Rome
→ GET /api/v1/temporal/timeline/window
→ FastAPI / DanteContext / PostgreSQL
→ truthful empty response
→ Timeline ready
→ zero prototype cards
```

### Proof B — Create write stop-line before B01

```text
production Home
→ Timeline +
→ author valid Activity draft
→ submit
→ temporal.create.backend_unavailable
→ draft remains visible
→ zero Timeline cards materialized
```

### Proof C — database outage is an error, not empty success

```text
healthy Timeline read
→ controlled disposable PostgreSQL stop
→ force fresh temporal window request
→ backend failure visible in UI
→ zero fake Timeline cards
→ controlled PostgreSQL restart
→ explicit Riprova
→ fresh successful temporal request
→ ready/empty truthful state
```

The outage proof uses the already accepted scoped `access-auth-e2e-control.py` harness control and always attempts to restart the disposable database in test cleanup if the proof aborts while it is stopped.

The browser tests use dedicated synthetic account slots per browser and per proof so bounded sign-in rate controls cannot create cross-test coupling.

These tests are committed but have not yet been executed in this connector-only session. They establish the real browser/full-stack harness coverage structurally, but do not yet make `B00-T04` or any execution gate green.

## 7. B00 isolated manual `userTest` checkpoint

The manual setup/cleanup flow is now defined in:

`docs/workstreams/timeline-temporal-operational-b00-usertest.md`

It deliberately reuses the same disposable full-stack harness rather than a developer's normal account/database.

The manual protocol covers:

1. real authenticated empty Timeline behavior with no prototype cards;
2. Create fail-closed behavior before B01;
3. real PostgreSQL outage → visible error → database restart → explicit Retry recovery;
4. deterministic scoped cleanup of the exact disposable container/control id.

The protocol is **READY TO RUN — NOT YET APPROVED**.

Manual approval remains distinct from automated proof and requires the explicit approval token recorded after inspection of the current candidate:

```text
B00 userTest — APPROVED
```

## 8. Current B00 checkpoint semantics

B00 remains **IN PROGRESS**. No green-check claim is made merely because code/tests/protocols exist; applicable automated suites and manual acceptance still have to run under the workstream Definition of Done.

Implemented/defined boundaries now include:

- authenticated backend temporal read/API boundary;
- strict frontend remote temporal read adapter;
- Home/Timeline consumption of that real read boundary;
- truthful loading/error/retry behavior;
- normal-runtime prototype card/clock isolation;
- normal-runtime Create fake-success retirement;
- PostgreSQL integration proof for AuthSession → DanteContext → self Person → timezone → temporal endpoint;
- browser → production web → API → PostgreSQL E2E coverage;
- controlled PostgreSQL outage/recovery browser proof;
- isolated manual `userTest` setup/cleanup protocol.

Still required before B00 can become `✅`:

- execute the full frontend/backend automated quality suites;
- execute the real PostgreSQL integration suite against the certified image;
- execute the full-stack browser proofs across the configured browser projects;
- run and approve the isolated manual `userTest` protocol;
- confirm the complete F0/T1 regression suite remains green after the real-data cutover;
- update the primary live ledger with executed evidence before declaring B00 closed.

The first real PostgreSQL-backed **temporal product** projection is a B01 responsibility, not a circular B00 prerequisite. B00's job is to prove that B01 can activate that read/write capability without inventing a second application/data-source architecture.

No checklist item may be marked green until its applicable Definition-of-Done gates have actually passed.
