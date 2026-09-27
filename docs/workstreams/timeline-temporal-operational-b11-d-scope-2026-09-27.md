# B11-D — Whole-block integration gate

- **Date:** 2026-09-27
- **Branch:** `feature/timeline-temporal-operational`
- **Status:** IN PROGRESS
- **Entering frontier:** B11-A/B/C CLOSED / PROVEN; Alembic `20260927_86`
- **Real-app acceptance:** reserved for final B11 closure after B11-D

## Purpose

B11-D verifies that Advanced Recurrence, `actual_realization` Condition and personal Schedule Reminder work together on the same canonical temporal chain. It adds no fourth temporal concept, generic automation engine, delivery worker or copied due-time authority. PostgreSQL remains the sole source of accepted truth.

## Integrated proof

The local automated gate exercises one self-owned Routine and its seed Occurrence. A qualifying, explicitly recorded Actual completion drives a dependent Occurrence through completion-relative Recurrence. A Condition on the dependent Occurrence is initially `indeterminate/withhold`; scheduling that Occurrence and configuring its personal Reminder changes neither the Condition nor Actual. The Reminder derives its due time from the accepted Schedule. Explicit Actual on the dependent Occurrence changes a newly evaluated Condition to `satisfied/allow` with exact MaterialState evidence, without silently changing the Schedule or Reminder. A later Actual correction leaves the older evaluation and the already materialized Occurrence history intact. Replay and reload retain stable identities and accepted-current state.

The gate also runs the B11-A anchor-stream and B11-B/C focused regressions, exact `_86` catalog tests, relevant API/OpenAPI and web tests, deterministic generated-client check, and typechecks. The user executes local tests on `~/projects/dante`; no GitHub Actions or CI are used.

## Closure boundary

B11-D is closed only after its integrated tests and the focused regressions pass locally and the results are recorded in roadmap/map/handoff. The final real-app walkthrough across A/B/C occurs **after** B11-D and immediately before closing the parent B11 block. No published Alembic revision or generated client is edited manually.
