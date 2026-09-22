# Timeline / Temporal-Operational — B06-C Occurrence Implementation Freeze

- **Status:** ✅ IMPLEMENTED / CLOSED / PROVEN
- **Date:** 2026-09-22
- **Branch:** `feature/timeline-temporal-operational`
- **Migration:** `20260922_55`
- **Proven topology:** `145|5|87|92|285|223|408|0|0|0`
- **CI / Actions:** not authorized; proof is user-run against PostgreSQL 18.6

This record freezes the proven B06-C surface. Closure evidence is recorded in `timeline-temporal-operational-b06-c-closure-2026-09-22.md`.

## 1. Delivered boundary

```text
explicit bounded checkpoint command
→ immutable Recurrence-history evaluation
→ exact effective-state selection by candidate coordinate
→ CP6 Role-13 coordinate/provenance validation
→ canonical Occurrence identity/result receipt
```

The checkpoint range is a half-open actor-zone civil range of at most 62 days. A second safety bound rejects any single checkpoint that would evaluate more than 10,000 Occurrences and rolls the transaction back; callers must narrow the horizon. Timeline/GET reads never trigger generation.

The evaluator supports the four accepted families: calendar wall-clock, elapsed interval, flexible quota-per-period and cyclic positional. Named-zone calendar gaps structurally generate nothing; overlaps resolve exactly once using the persisted `earlier | later` policy. Elapsed coordinates remain absolute. Quota coordinates remain flexible periods with no fabricated slot time or ordinal.

## 2. Mutation semantics

| Intent | Canonical result |
|---|---|
| checkpoint | Reuse/materialize typed recurrence-generated Occurrences and persist an exact replay result, including an empty result. |
| explicit extra | Create one Occurrence with `origin_code=explicit_extra`, no governing Recurrence state and no generated coordinate. |
| skip | Append one immutable non-execution disposition; do not delete the Occurrence or cancel the source. |
| structural exclusion | Prevent one not-yet-materialized calendar/elapsed/cyclic coordinate from becoming an Occurrence. |
| this and subsequent | Reuse B06-B immutable Recurrence replacement; prior materialized Occurrences retain their original governing state. |

Paused or ended Routines reject new checkpoints and explicit extras. Exact accepted-operation replay remains available after the lifecycle change. Event and Routine use distinct typed capabilities over the same Occurrence semantics.

## 3. Persistence and security

Migration `_55` adds six append-retained control/receipt tables and fourteen self-scoped `SECURITY DEFINER` functions. Runtime and migrator roles receive no direct access to the new tables. Direct runtime access to the five CP6 Occurrence-generation tables is retired, so the Role-13 historical-state repair cannot be bypassed: materialization is execute-only through the B06-C boundary.

Role-13 continues to validate source ownership, exact governing state/family, typed coordinate membership, range/count, duplicate and quota cardinality. The B06-C materializer additionally validates checkpoint receipt/range and coordinate-time precedence across immutable Recurrence history while holding the established current/generation advisory-lock namespaces.

## 4. Deliberate stop line

B06-C does not establish Schedule placement, Timeline projection, UI flows, Activity copies, Session, Actual or Outcome. Those remain owned by later slices, beginning with B06-D for shared Schedule/Timeline integration.

## 5. Closure proof

- deterministic evaluator tests, including DST, absolute-vs-civil behavior, 62-day and 10,000-Occurrence bounds — **PASS**;
- Routine/Event checkpoint replay, empty replay, collision and concurrency — **PASS**;
- future-state reconciliation with retained historical materialization — **PASS**;
- explicit extra, skip and structural exclusion separation — **PASS**;
- Routine lifecycle stop, self isolation and execute-only ACL — **PASS**;
- whole catalog/Dictionary/SQLAlchemy reconciliation at `_55` — **PASS**;
- exported OpenAPI/client generation and API-client typecheck — **PASS**.

The user-run gate passed generated/client checks, targeted Ruff/format checks, `22` selected evaluator/API/OpenAPI tests and the selected `41`-test PostgreSQL/catalog/ACL set after the cyclic projection repair and focused `3`-test rerun. B06-C is **CLOSED / PROVEN**.
