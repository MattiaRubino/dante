# Timeline / Temporal-Operational — B06-B Closure

- **Status:** ✅ CLOSED / PROVEN
- **Date:** 2026-09-22
- **Branch:** `feature/timeline-temporal-operational`
- **Application proof head:** `e1f7101194f6d6445d7be906e2cd274827c6388e`
- **Database head:** `20260922_54`
- **Expected topology:** `139|5|73|92|269|209|389|0|0|0`
- **CI / Actions:** none launched

## Delivered boundary

B06-B establishes guarded self-scoped Recurrence authoring for exactly two
source owners—Routine and Event—and all four CP6 families:

```text
calendar_wall_clock
elapsed_interval
quota_per_period
cyclic_positional
```

Each accepted mutation creates an immutable owner-bound MaterialState, closes
and opens current-history atomically, moves the bounded current facet under
expected-state CAS and records an actor-local idempotency receipt. Replaying the
same operation returns the accepted state; changed intent and stale state fail.

Named-zone calendar truth persists the IANA zone plus explicit immutable DST
policy: nonexistent civil candidates are structurally skipped and ambiguous
civil candidates resolve to exactly one declared `earlier | later` instant.
Floating-local, named-zone and absolute/elapsed semantics remain distinct.

## Persistence authority

```text
20260922_52  immutable Routine/Event Recurrence authoring,
             owner-specific receipts and explicit DST policy
20260922_53  forward-only current-state reader repair
20260922_54  forward-only selector-validation repair
Topology     139|5|73|92|269|209|389|0|0|0
```

Runtime retains execute-only self-scoped capability access. Raw CP6 and B06-B
tables remain unavailable to the runtime role. Dictionary, SQLAlchemy mapping,
Alembic head and database catalog are reconciled.

## Direct proof

User-run locally:

```text
2 passed in 0.58s    Pydantic/API positional non-zero contract
1 passed in 0.45s    canonical Decimal-safe idempotency fingerprint
28 passed in 41.66s PostgreSQL authoring/catalog/ACL/regression selection
API-client typecheck PASS
```

The PostgreSQL selection proves Routine/Event ownership, all four families,
named-zone DST persistence, open/until/count ranges, CAS, replay/collision,
current/history, self isolation, execute-only ACL, catalog exactness and
affected B03–B06 regressions.

## Semantic stop-line

B06-B creates no Occurrence, fake Activity, Event instance, Schedule, Session,
Actual or Timeline expansion. One-occurrence exception/skip, explicit extra,
bounded generation checkpoint, structural exclusion and this-vs-future
reconciliation remain B06-C. Shared Occurrence Schedule, Timeline projection
and functional recurring UI remain B06-D.

**Next:** B06-C — canonical bounded Occurrence checkpoint and scope.
