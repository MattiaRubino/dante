# B13-D — Whole-block Integration / Acceptance closure

- **Date:** 2026-09-29
- **Branch:** `feature/timeline-temporal-operational`
- **Status:** CLOSED / USER-REPORTED REAL-APP ACCEPTANCE
- **Parent B13:** CLOSED on the same qualified acceptance
- **Persistence frontier:** existing Alembic `20260929_92`; no B13-D schema change
- **CI:** not used; the user runs tests locally

## Scope delivered

The integrated candidate exercises Plan and linked Steps, a qualified directional Dependency, a Plan Step execution policy and read-only proposed-slice assessment against Activity Temporal Constraints. The Home panel now opens from an Activity title, carries the selected Activity and can link an existing same-title Step or add a new linked Step with a visible button. It no longer asks the user to copy a browser UUID.

The B13-A/B/C identities and boundaries remain distinct: Plan/Step structure is not Activity identity; ordering is not a Dependency; proposed segments are not accepted Schedule or Session; Actual is recorded separately. B13-D added no new migration or Dictionary topology.

## Evidence and limits

The initial user-run local gate on `c7e298384a2dacc8e7a8dc64405e20a1951f0879` passed generated check (383 files), API-client and web typechecks, six web files (12 tests), backend contract/unit (3 tests), seven PostgreSQL files (14 tests in 44.24s), Ruff check and format. That run preceded the direct Activity-to-Step UX repair.

The first seven-file rerun after the initial repair reported 14 passing and one failing web test, with a jsdom scroll error. The text matcher and optional scroll call were repaired at `92bb5a92f173abac7040ff4931c441380ebd7902`; the existing-Step destination repair was published at `be4359690a2b2f2c0ff5023abbc63d00704b4ddb`. A final post-repair web rerun was requested and expected to collect 16 tests, but no result was supplied. **Do not claim the final web suite passed.**

In the user's real app, screenshots showed the `B13D Album` Plan with linked `B13D Record` and `B13D Mix` Steps. A later screenshot showed the `B13D Record → B13D Mix` Dependency, qualifier `Actual avvenuto`, evaluated `sconosciuta` before recording Actual. The complete remaining walkthrough (reorder/reload and endpoint protection, Mix policy persistence, three-slice assessment, Actual correction, retirement) was provided in one message. The user then reported `ok va chiudiamo`, accepted here as overall real-app acceptance. No separate observations for each remaining check or 90-minute Temporal Constraint setup were supplied; those individual outcomes are not asserted as independently observed.

## Closure and continuation

B13-D and parent B13 are closed as **user-reported acceptance**, not as a fully rerun post-repair automated proof. The final seven-file web rerun remains a documented verification gap. B12 is the next workstream gate and needs its own scoped approval before implementation; it must use B13's canonical Plan, Dependency and execution-policy truth. No CI/GitHub Actions were used.
