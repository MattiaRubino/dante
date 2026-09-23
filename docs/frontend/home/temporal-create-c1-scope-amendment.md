# DANTE — Temporal Create C1 Scope Amendment — Historical

**Status:** HISTORICAL PRE-VERTICAL SCOPE EVIDENCE — NOT CURRENT AUTHORITY  
**Original branch:** `feature/home-timeline`  
**Original reconciliation:** 2026-09-04

This file preserves the scope decision from the old frontend-only C1 phase. At that checkpoint C1 deliberately stopped at the maximum useful pre-backend/manual Create capability and excluded real API persistence, canonical recurrence evaluation/Occurrence generation, provider execution, authoritative solver, notification delivery and AI/NL/voice runtime.

That stop line was correct for its phase. It is no longer the current workstream boundary because B00–B06 subsequently implemented real backend/PostgreSQL temporal persistence, canonical Schedule/Event/Routine/Recurrence/Occurrence behavior and backend-backed Timeline projection.

## Historical semantic value retained

The original C1 work helped establish useful distinctions that remain valid:

```text
Activity != Event != Routine
Schedule/placement != Actual
Routine-backed repeated intent != browser-generated fake Occurrences
Timeline card != canonical identity/DB row
manual structured Create != AI/NL/voice interpretation
```

## Current authority

For current scope and sequencing read:

1. `../../workstreams/timeline-temporal-operational-post-b06-scope-decision-2026-09-23.md`;
2. `../../workstreams/timeline-temporal-operational-roadmap.md`;
3. `../../workstreams/timeline-temporal-operational-map.md`;
4. `current-checkpoint.md`.

Current vertical boundary is the real `+ → canonical truth → Timeline → required lifecycle` implementation path. B08 is next; B07 is deferred until after B12. External provider integration, native/offline, account collaboration and broad analytics are outside this vertical.