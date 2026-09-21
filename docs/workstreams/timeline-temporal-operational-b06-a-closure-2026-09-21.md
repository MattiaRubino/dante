# Timeline / Temporal-Operational — B06-A Closure

- **Status:** ✅ CLOSED / PROVEN
- **Date:** 2026-09-21
- **Branch:** `feature/timeline-temporal-operational`
- **Database head:** `20260921_51`
- **Expected topology:** `135|5|68|90|263|201|381|0|0|0`
- **CI / Actions:** none launched

## Delivered boundary

B06-A establishes a self-owned Routine source with guarded title/lifecycle
(`active`, `paused`, `ended`), actor-local primary Life Area and secondary
Product Tags. Source commands have immutable idempotency receipts and CAS
where a source or assignment revision is meaningful.

CP6 requires a canonical Routine to carry a current `routine.recurrence`
MaterialState. Creation therefore atomically establishes a **separate**,
caller-specified initial `daily` / `floating_local` Recurrence with start date
and optional wall time. This is not an Occurrence, Activity or Schedule and
does not materialize any future instance.

The closing forward repairs are deliberately retained as migrations:

```text
20260921_49  Routine source/product capability
20260921_50  CP6-required initial Recurrence companion
20260921_51  qualified PL/pgSQL source/Life Area commands
```

No accepted migration was rewritten. The last repair preserves
`#variable_conflict error` and qualifies relation columns instead of weakening
the database guardrail.

## Direct proof

User-run locally, with no CI/Actions:

```text
26 passed in 39.19s
```

The selection covered B06-A Routine creation/companion, self isolation,
idempotent replay/collision, lifecycle/CAS, Life Area reassignment, Tag
detach, runtime ACL and catalog reconciliation, plus affected B03–B05/B04
regressions. OpenAPI export/client generation and API-client typecheck also
completed successfully.

## Explicitly deferred

B06-A does not author or revise general Recurrence families, generate or
materialize Occurrences, create occurrence exceptions/skips, create Schedule
placements or project recurring data into Timeline. Those boundaries remain
B06-B through B06-D.

**Next:** B06-B — full guarded Routine/Event Recurrence authoring for the four
CP6 families, effective boundaries, immutable history and explicit DST policy.
