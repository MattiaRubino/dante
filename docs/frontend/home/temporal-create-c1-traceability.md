# DANTE — Temporal Create C1 Traceability — Historical

**Status:** HISTORICAL PRE-VERTICAL TRACEABILITY — NOT CURRENT IMPLEMENTATION LEDGER  
**Original date:** 2026-09-04  
**Original branch:** `feature/home-timeline`

This file preserves the semantic traceability established during the earlier frontend-only C1 phase. It is retained as phase-time evidence, not as current Timeline sequencing or capability status.

## Historical semantic mapping retained

| Product concept | DANTE ownership | Non-collapse rule |
| --- | --- | --- |
| Activity | native Activity | not Event; not Routine |
| Event | native Event | not Activity; recurrence may be Event-owned |
| Routine | native Routine | persistent repeated policy/source |
| Schedule | accepted temporal placement | not Activity/Event/Routine/Occurrence identity |
| Recurrence | recurrence policy/state | not Routine; not Occurrence |
| Occurrence | expected instance identity | not Schedule; not fake Activity |
| Session | execution runtime | not Schedule; not Actual |
| Actual | realization | planned/intended != happened |
| Timeline card | read/ViewModel projection | not DTO/DB row/canonical identity |

Those distinctions remain compatible with current authority, but the old `AUTOMATED GREEN / MANUAL OPEN` status is historical only.

## Current authority

Current semantic/proof traceability is owned by:

1. `../../workstreams/timeline-temporal-operational-map.md`;
2. `../../workstreams/timeline-temporal-operational-roadmap.md`;
3. `../../workstreams/timeline-temporal-operational-post-b06-scope-decision-2026-09-23.md`;
4. current Product / Domain / Logical / Physical references;
5. current DB Dictionary/Alembic/OpenAPI/generated client/source/tests.

Current frontier:

```text
B00–B06 ✅ CLOSED / PROVEN
B08 Session Runtime ← NEXT
B07 UI/UX Consolidation ⏸ DEFERRED until after B12
```

Do not use this historical C1 file to reintroduce local/browser canonical recurrence generation, old Context semantics, provider assumptions or obsolete sequencing.