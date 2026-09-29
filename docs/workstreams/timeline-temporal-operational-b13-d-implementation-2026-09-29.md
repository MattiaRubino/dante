# B13-D — integration candidate checkpoint

- **Status:** AUTOMATED LOCAL GATE PASS / real-app walkthrough pending
- **Date:** 2026-09-29
- **Branch:** `feature/timeline-temporal-operational`
- **Base:** `4eac3e971d50cb3c0f04d2699e35275a2dacbe9b`
- **Persistence:** existing `_92`; no schema, Dictionary or ACL change
- **CI:** not authorized

## Integrated slice

`test_b13_d_whole_block.py` puts Plan structure, two linked Activities, a qualified `actual_occurred` Dependency, a dependent Step execution policy and a hard Activity Schedule-duration rule in one migrated PostgreSQL fixture. It checks unknown/current Actual evaluation, Step reordering, active endpoint protection, hard proposed-slice count, individually admissible slices whose contiguous union violates the real Temporal Constraint, stale Plan-state rejection, Actual correction, self isolation, policy retirement and Dependency history. It invokes the existing assessment route with real runtime state; assessment remains read-only.

The Home `PlanWorkPanel` integration test drives both nested controls from one accepted Plan revision. It creates the directional Dependency, saves and reloads the Step policy, then checks that the assessment uses the revised state without a second Plan write. The existing B13-A OpenAPI contract assertion was updated for the B13-C Step policy fields and the typed assessment route; the Dependency contract remains its own B13-B test.

## Verification and next gate

In this coding workspace, the focused web suite passed **12 tests across 6 files**, including the new whole-panel integration; web typecheck passed. Ruff check and format checks passed for the two changed Python tests, and the new integration test compiled. The generated OpenAPI artifact contains the expected Plan Step and assessment fields, but the Python contract test has not run here. The local `uv` is `0.12.18` while this repository pins `==0.12.5`, so the local Python test command exits before pytest starts. There is no local PostgreSQL proof for the new integrated test. These are candidate checks, not B13-D acceptance.

The user subsequently ran the published `c7e29838` gate locally: deterministic generation (383 files), API-client and web typechecks, six web files (**12 tests**), backend contract/unit (**3 tests**), seven PostgreSQL files (**14 tests in 44.24s**), Ruff check and format all passed. The earlier workspace limitation remains a record of where these checks were run, not a pending gate. The exact commands and remaining real-app walkthrough are in `timeline-temporal-operational-b13-d-gate-2026-09-29.md`. Do not mark B13-D or parent B13 closed until the user reports the real-app walkthrough; B12 remains held.
