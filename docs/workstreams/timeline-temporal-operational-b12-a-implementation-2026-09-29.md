# B12-A — Current-truth conflict diagnosis — implementation checkpoint

- **Status:** CANDIDATE / local PostgreSQL and real-app acceptance pending
- **Date:** 2026-09-29
- **Branch:** `feature/timeline-temporal-operational`
- **Scope:** `timeline-temporal-operational-b12-a-scope-2026-09-29.md`
- **DB source head:** `20260929_92`; no migration or new canonical tables

## Delivered slice

The selected Plan in Home → Plan e Step has an explicit **Analizza conflitti** control. The authenticated read-only endpoint `GET /api/v1/temporal/plans/{plan_ref}/conflicts` requires the Plan's current state reference and returns bounded Step-level diagnoses. The server rereads the self-owned Plan, active qualified Dependencies and current accepted Schedule placement; for an absolute interval it evaluates the Activity's current Temporal Constraints with the existing B04 evaluator. It checks that Plan, Dependencies and placement have not changed during the read. The endpoint never writes or searches a replacement time.

The API exposes Plan/Step/Activity references, Schedule MaterialState, active Dependency states and source Actual/Outcome MaterialStates, individual constraint results and the hard-set result. The Home panel shows names and typed reasons rather than technical identifiers. It distinguishes a known hard violation, unsatisfied prerequisite, unknown prerequisite, unplaced/unsupported placement, multiple current placements, cycle and no known conflict within supported rules. Availability and capacity are explicitly not evaluated; simple overlap is not treated as a conflict.

Limits: at most 20 Steps, 40 active Dependencies and 40 current Schedules; only a single current absolute Schedule interval per linked Activity is evaluated. Schedule/constraint/Dependency truth is read on each click. A Plan state mismatch yields HTTP 409; another self Person receives 404. No new persistence or migration was needed.

## Evidence and remaining gate

- Python compilation and Ruff for changed backend paths: PASS.
- Focused OpenAPI contract test: 1 passed.
- OpenAPI and generated client produced through repository tooling; web and API-client typechecks: PASS.
- Focused web component tests: 4 passed across two files.
- This executor cannot run the PostgreSQL integration test because Docker is not installed. User worktree must run the full local gate and report results.
- Generated-source determinism: PASS (389 files) in this executor with a temporary local uv version override, restored after generation. Repeat on the user worktree with the repository's pinned uv/pnpm versions.
- Real-app acceptance is pending. Do not close B12-A or advance to B12-B until the user reports the complete result.

## Product walkthrough

1. Open Home → Plan e Step and select a self-owned Plan with linked Record and Mix Activities; ensure Mix has one accepted absolute Schedule interval.
2. Click **Analizza conflitti**. Check that Record/Mix are named and that an absent Actual on the Record → Mix Dependency says `sconosciuta`.
3. With a hard duration rule that Mix's current interval violates, click again and confirm a hard violation; the Schedule should stay in place.
4. Record `non avvenuto` for Record, click again and confirm `non soddisfatta` plus blocked prerequisite. Correct to `avvenuto`, click again and confirm `soddisfatta` while the hard violation remains.
5. For a linked Activity without accepted Schedule, confirm the result stays unknown. No availability/free-slot claim or automatic move appears.

The automated PostgreSQL test creates this exact Record → Mix progression and checks Schedule/Plan immutability, self scope and stale Plan state. Its outcome is pending the user's local run.
