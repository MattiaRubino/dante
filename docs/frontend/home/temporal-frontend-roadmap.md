# DANTE — Temporal Frontend Production-Depth Roadmap — Historical

**Status:** HISTORICAL PRE-VERTICAL FRONTEND ROADMAP — SUPERSEDED AS CURRENT SEQUENCING AUTHORITY  
**Original phase:** `feature/home-timeline`, reconciled through 2026-09-05  
**Superseded for present-tense Timeline sequencing:** 2026-09-23

This document preserves the earlier frontend-only C1/T1 roadmap that existed before the real Timeline / Temporal-Operational product vertical materialized canonical backend/PostgreSQL behavior.

It must **not** be used to infer current `NEXT`, current persistence capability, current recurrence materialization state or current product closure.

## Historical phase summary

The original roadmap froze/advanced:

```text
H0 Home structure
T1 Timeline engine
F0 typed local temporal application seam
C1 Manual Temporal Create — then OPEN
C2 Structured Detail — then BLOCKED behind C1
```

At that phase, recurrence materialization, canonical Occurrences, backend temporal range reads, Session runtime, Actual/outcome, provider integration and solver capability were still future work. That statement is phase-time evidence only.

## Current authority

For current Timeline/Temporal truth read, in order:

1. `../../workstreams/timeline-temporal-operational-post-b06-scope-decision-2026-09-23.md`;
2. `../../workstreams/timeline-temporal-operational-roadmap.md`;
3. `../../workstreams/timeline-temporal-operational-map.md`;
4. `../../workstreams/timeline-temporal-operational-handoff.md`;
5. `../../database/timeline-temporal-operational.md`;
6. executable code/tests/current OpenAPI/generated client.

Current frontier is:

```text
B00–B06 ✅ CLOSED / PROVEN
B08 Session Runtime ← NEXT
B07 UI/UX Consolidation ⏸ DEFERRED until after B12
```

The former B13 provider/offline block and B14 broad analytics block are outside the active `+`/Timeline vertical.

## Historical semantic value retained

The following distinctions from the original frontend phase remain compatible with current authority:

```text
Activity != Event != Routine
Routine != Recurrence != Occurrence
Occurrence != Schedule
Schedule != Session != Actual
planned/intended != happened
Timeline ViewModel != application model != DTO != DB row
manual Create != AI/NL/voice
```

Where old phase wording conflicts with current executable/workstream truth, current authority wins.