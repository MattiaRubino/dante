# Timeline / Temporal-Operational — B06-C Closure

- **Status:** ✅ CLOSED / PROVEN
- **Date:** 2026-09-22
- **Branch:** `feature/timeline-temporal-operational`
- **Application proof head:** `ff92caf52245937f38ee91bf0bebd916fc854f79`
- **Database head:** `20260922_55`
- **Proven topology:** `145|5|87|92|285|223|408|0|0|0`
- **CI / Actions:** none launched

## Delivered boundary

B06-C establishes the bounded self-scoped Occurrence checkpoint for Routine and
Event over immutable Recurrence history. It supports all four accepted families,
selects the exact governing MaterialState at each coordinate, and reuses or
materializes one canonical Occurrence identity under deterministic locks.

The checkpoint uses a half-open actor-zone civil range of at most 62 days and
rejects more than 10,000 evaluated Occurrences atomically. Named-zone gaps do
not generate a coordinate; overlaps resolve exactly once using the persisted
policy. Elapsed coordinates remain absolute and quota coordinates remain
flexible periods without invented slot times or ordinals.

Explicit extra, immutable skip and pre-generation structural exclusion remain
distinct operations. Accepted operations replay exactly, including empty
checkpoint results and replay after a Routine lifecycle change. Concurrent
checkpoints converge on the same canonical identities.

## Persistence authority

```text
20260922_55  bounded checkpoint receipts/results,
             explicit-extra receipts, immutable skips and exclusions,
             fourteen self-scoped SECURITY DEFINER capabilities
Topology     145|5|87|92|285|223|408|0|0|0
```

Runtime and migrator roles have no direct access to the six B06-C control
tables. Runtime direct writes to the five CP6 Occurrence-generation tables are
retired; materialization is execute-only through the governed B06-C boundary.
Dictionary, SQLAlchemy, Alembic and the live PostgreSQL catalog reconcile.

## Direct proof

User-run locally:

```text
generated sources deterministic/current             PASS (271 files)
API-client typecheck                                 PASS
targeted Ruff check                                  PASS
targeted Ruff format check                           PASS (4 files)
selected evaluator/API/OpenAPI tests                 22 PASS
post-fix evaluator rerun                             16 PASS
selected PostgreSQL/catalog/ACL regressions          41 proven
post-fix Occurrence PostgreSQL rerun                  3 PASS
```

The first PostgreSQL run passed 40 tests and exposed one real cyclic-read
projection defect: the shared Occurrence reader returned only the calendar
`generated_date`. The repair projects the calendar or cyclic date according to
the populated typed coordinate; the complete three-test Occurrence PostgreSQL
file then passed. The final proof also includes all-family evaluation,
revision-zone boundaries, concurrency, replay/collision, lifecycle stop,
self-isolation, Role-13 provenance and execute-only ACL.

## Semantic stop-line

B06-C creates no Schedule placement, Timeline projection, recurring UI flow,
Activity copy, Session, Actual or Outcome. Shared Occurrence Schedule and
Timeline integration remain B06-D; whole-block reconciliation remains B06-E.

**Next:** B06-D — shared Schedule, bounded Timeline projection and functional UI.
