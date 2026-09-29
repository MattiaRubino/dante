# B12-A — Current-truth conflict diagnosis — implementation checkpoint

- **Status:** CLOSED / PROVEN on user-run focused local gate 2026-09-29
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
- This executor could not run PostgreSQL because Docker is not installed. The user's local worktree passed the focused PostgreSQL/catalog suite: **11 passed in 26.14s**.
- Generated-source determinism: PASS (389 files) in this executor with a temporary local uv version override, restored after generation. Repeat on the user worktree with the repository's pinned uv/pnpm versions.
- User-run proof at `db6a568`: generated check **389 files current**, both typechecks PASS, web **4 passed / 2 files**, OpenAPI contract **1 passed**, Ruff PASS, PostgreSQL/catalog **11 passed in 26.14s**. B12-A is closed on this focused automated evidence. The whole-chain real-app acceptance is deferred to B12-D before parent B12 closure.

## Deferred B12-D product walkthrough material

1. Open Home → Plan e Step and select a self-owned Plan with linked Record and Mix Activities; ensure Mix has one accepted absolute Schedule interval.
2. Click **Analizza conflitti**. Check that Record/Mix are named and that an absent Actual on the Record → Mix Dependency says `sconosciuta`.
3. If Mix already has a hard Temporal Constraint that its current absolute interval violates, click again and confirm a hard violation; the Schedule should stay in place. The PostgreSQL integration test proves this case without requiring a new manual rule authoring path.
4. Record `non avvenuto` for Record, click again and confirm `non soddisfatta` plus blocked prerequisite. Correct to `avvenuto`, click again and confirm `soddisfatta` while the hard violation remains.
5. For a linked Activity without accepted Schedule, confirm the result stays unknown. No availability/free-slot claim or automatic move appears.

These manual checks are reserved for the integrated B12-D walkthrough and will be reconciled with candidate generation and governed admission then. The B12-A automated PostgreSQL test creates the Record → Mix progression and checks Schedule/Plan immutability, self scope and stale Plan state; it passed in the user's local gate.
