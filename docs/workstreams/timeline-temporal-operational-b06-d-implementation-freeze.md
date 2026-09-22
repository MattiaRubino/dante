# Timeline / Temporal-Operational — B06-D Implementation Freeze

- **Status:** 🔒 APPROVED / IMPLEMENTATION IN PROGRESS
- **Date:** 2026-09-22
- **Branch:** `feature/timeline-temporal-operational`
- **Entering migration:** `20260922_55`
- **Entering proven topology:** `145|5|87|92|285|223|408|0|0|0`
- **CI / Actions:** not authorized; all proof is user-run locally

This record freezes B06-D before runtime changes. It extends the proven B06-C canonical Occurrence surface into the existing shared Schedule and bounded Timeline capabilities. It does not create a second scheduling model, expand recurrence in the browser or pull B07 redesign work forward.

## 1. Complete owned outcome

```text
real Routine / recurring Event authoring
→ explicit bounded backend checkpoint
→ canonical Occurrences
→ optional existing shared Schedule per Occurrence
→ read-only bounded Timeline projection
→ one-instance Schedule edit / unschedule / Undo
→ authoritative browser refetch
```

The B06-D slice is complete only when Routine and recurring Event creation/read paths reach real Occurrences, one Occurrence can enter the shared Schedule capability, and the Timeline renders canonical expected or accepted truth without duplicates.

## 2. Persistence boundary

The existing `schedule.subject_native_ref` and Schedule placement/history tables remain authoritative. CP6 already admits the `occurrence` native family; B06-D adds no Schedule table, Occurrence clone, virtual-instance table or generic polymorphic edge.

Migration `_56` is limited to the real capability gap: the four existing self-scoped Schedule mutation functions must derive ownership through

```text
Occurrence
→ occurrence_generation.source_native_ref
→ self-owned Routine or Event
```

The existing typed placement forms, MaterialState history, idempotency, CAS, unschedule and monotonic Undo semantics remain unchanged. An Occurrence with no current Schedule remains a valid Occurrence.

## 3. Public application/API boundary

B06-D adds one typed establish command for an already materialized Occurrence. It reuses the existing Schedule placement request union and returns canonical Schedule identity/current placement state. Existing generic Schedule revise, unschedule and Undo commands remain the only edit/history paths after ownership scope is widened.

The Timeline `GET` remains strictly read-only. It never checkpoints, expands a Recurrence, creates an Occurrence or establishes a Schedule. Callers explicitly checkpoint the same half-open actor-zone range before refetching the Timeline window.

## 4. Timeline projection precedence

Each canonical Occurrence produces at most one current Timeline item:

| Canonical state | B06-D Timeline result |
|---|---|
| skipped Occurrence | no active Timeline item; identity/disposition remains retained by Occurrence read |
| current Occurrence Schedule | one `scheduled_occurrence` item; expected coordinate is retained as metadata, not emitted as a second item |
| generated calendar coordinate without Schedule | one expected calendar item; date/wall-time/zone meaning retained, no invented duration |
| generated elapsed coordinate without Schedule | one expected instant item; no invented interval |
| generated quota coordinate without Schedule | one flexible period item; never a fabricated weekday or clock slot |
| generated cyclic coordinate without Schedule | one expected civil-date/position item; no invented clock time |
| explicit extra without Schedule | no Timeline item because it has no generation coordinate or accepted placement |
| structural exclusion | no Occurrence and therefore no Timeline item |

The range remains `[start_date, end_date_exclusive)` in the authenticated effective timezone and remains capped at 62 days. Current source title, Life Area and Tags are inherited for grouping; B06-D creates no per-Occurrence organization records.

## 5. Functional UI boundary

B06-D wires the existing Create recurrence handoff to real Routine/recurring Event backend operations, explicitly checkpoints the visible window, reads canonical Timeline items, and supports scheduling or moving one materialized Occurrence through the shared Schedule commands. Every mutation completes through authoritative refetch; the browser does not synthesize future instances or patch canonical truth optimistically.

Expected points and flexible periods may use a minimal B06-D presentation, but they must remain semantically distinct from accepted Schedule intervals. Broad visual consolidation, dense series-management UX and new interaction architecture remain B07.

## 6. Required proof and stop line

Required direct proof covers:

- Routine/Event Occurrence Schedule establish, replay/collision, self isolation and retained placement history;
- revise, unschedule and Undo through the already shared Schedule boundary;
- bounded expected projection for all four recurrence families;
- scheduled-over-expected precedence, skip suppression and no duplicate Timeline item;
- quota/flexible and point expectations without fabricated interval geometry;
- source organization inheritance without cloned Occurrence assignments;
- generated OpenAPI/client, frontend transport/refetch and focused browser behavior.

The user runs PostgreSQL, backend, generation, typecheck, Vitest and real-stack browser gates locally. B06-D does not add Session, Actual, Outcome, solver/replanning, provider synchronization, analytics or the broad B07 UI/UX redesign.
