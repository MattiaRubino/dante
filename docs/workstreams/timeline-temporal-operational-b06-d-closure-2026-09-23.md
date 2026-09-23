# Timeline / Temporal-Operational — B06-D Closure

- **Status:** ✅ CLOSED / PROVEN
- **Date:** 2026-09-23
- **Branch:** `feature/timeline-temporal-operational`
- **Application proof head:** `5abd55a2c032a1f76aa3cdc8ef15700fc7666755`
- **Database head:** `20260923_57`
- **Proven topology:** `145|5|88|92|285|223|408|0|0|0`
- **CI / Actions:** none launched; proof was user-run locally

## Delivered boundary

B06-D extends canonical B06-C Occurrences into the existing shared Schedule and Timeline surfaces without creating a second scheduling model or browser-generated recurrence state.

The delivered flow is:

```text
real Routine / recurring Event authoring
→ explicit bounded backend checkpoint
→ canonical Occurrences
→ optional existing shared Schedule per Occurrence
→ read-only bounded Timeline projection
→ one-instance Schedule revise / unschedule / Undo
→ authoritative browser refetch
```

Routine and recurring Event authoring use real backend Recurrence operations. The browser does not manufacture future Occurrences. The visible Timeline window is checkpointed explicitly before read, and Timeline `GET` remains read-only.

## Shared Schedule authority

Migration `_56` widens the existing self-scoped Schedule establish/revise/unschedule/Undo capabilities to derive Occurrence ownership through its Routine/Event source. Schedule identity, typed placement payloads, MaterialState/current/history, CAS, idempotency and monotonic Undo semantics remain the same authority used by Activity and Event.

An Occurrence with no current Schedule remains a valid expected Occurrence. Establishing a Schedule does not replace its source, governing Recurrence MaterialState or generation coordinate.

## Timeline projection and least privilege

The final projection precedence is:

```text
skipped Occurrence                    → no active Timeline item
current Occurrence Schedule           → one scheduled_occurrence item
generated calendar without Schedule   → one expected calendar item
generated elapsed without Schedule    → one expected instant item
generated quota without Schedule      → one flexible-period item
generated cyclic without Schedule     → one expected date/position item
explicit extra without coordinate     → no Timeline item
structural exclusion                  → no Occurrence / no Timeline item
```

Expected coordinate and accepted placement are not emitted as duplicate cards. Quota and cyclic expectations retain their actual precision; no fake weekday, clock time or duration is fabricated.

Local proof exposed an important ACL defect in the first Timeline implementation: runtime projection attempted direct reads from B06-C provenance tables. That implementation was rejected rather than solved with broader grants. Forward migration `_57` adds exactly one bounded, self-scoped, execute-only `SECURITY DEFINER` capability:

```text
list_self_expected_occurrences_in_window(uuid,date,date,text)
```

It validates a finite positive half-open actor-zone range of at most 62 days. Runtime retains zero direct grants on the private Occurrence provenance tables. Scheduled Occurrence provenance composes the pre-existing `get_self_occurrence` capability; Routine source metadata is read through the pre-existing `list_self_routines` capability rather than direct `routine_intention` access.

Therefore `_57` changes only the routine count:

```text
145 tables
5 views
88 routines
92 triggers
285 physical indexes
223 foreign keys
408 CHECK constraints
0 enums/domains
0 sequences/materialized/partitioned
0 RLS policies
```

Dictionary, Alembic and both whole-catalog tests reconcile at `_57`.

## Functional UI boundary

B06-D wires the existing recurrence Create intent to canonical Routine/recurring Event authoring, performs checkpoint-before-read, hydrates expected/scheduled Occurrence items, inherits source organization rather than cloning per-Occurrence organization, and provides the bounded one-instance `Pianifica` path through the existing Schedule engine.

A new Occurrence Schedule requires explicit placement information. The UI does not invent a duration. Calendar/elapsed coordinates may only seed information already contained in canonical expected truth; quota/cyclic expectations remain untimed until the user supplies a real placement. Mutations complete through authoritative invalidation/refetch rather than optimistic canonical patches.

## Direct proof

User-run locally after the final repairs:

```text
focused Occurrence Schedule PostgreSQL test        1 PASS
B06-D backend + catalog gate                       11 PASS
web TypeScript typecheck                           PASS
focused B06-D web Vitest files                     4 PASS
focused B06-D web Vitest tests                    18 PASS
```

The final `11 PASS` PostgreSQL gate included:

```text
test_b06_occurrence_schedule.py
test_b06_recurring_authoring.py
test_database_current_catalog.py
test_current_catalog.py
```

It proves shared Schedule identity/history/replay/self-scope, recurring authoring integration and `_57` Dictionary/Alembic/PostgreSQL catalog parity. The focused web proof covers Occurrence Schedule transport, Timeline parsing, expected-Occurrence scheduling and recurring Create runtime behavior.

## Semantic stop-line

B06-D adds no Session, Actual, Outcome, Responsibility/Participation, completion-relative or anchor-stream-relative recurrence, solver/replanning, provider synchronization, analytics or broad B07 UI redesign.

B06-D is therefore **CLOSED / PROVEN**. Whole-B06 reconciliation and the real-stack recurring Routine/Event walkthrough remain B06-E.

**Next:** B06-E — whole-block closure, broad direct local regression and real-stack recurring walkthrough.
