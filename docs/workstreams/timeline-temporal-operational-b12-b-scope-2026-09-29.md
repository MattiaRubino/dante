# B12-B — Bounded absolute-time candidate generation — scope proposal

- **Status:** APPROVED; implementation candidate awaiting focused user-run PostgreSQL gate
- **Date:** 2026-09-29
- **Branch:** `feature/timeline-temporal-operational`
- **Entry:** B12-A closed / proven; `20260929_92` remains DB source head
- **Parent:** `timeline-temporal-operational-b12-scope-2026-09-29.md`
- **Acceptance cadence:** focused user-run local automated proof for B12-B; one integrated real-app walkthrough at B12-D before closing B12

## 1. Supported planning question

For one selected Step of one authenticated self-owned Plan, whose linked Activity has exactly one current accepted absolute Schedule interval, find up to three nearby *candidate* intervals of the same duration. The Plan/Step selection comes from the existing Home panel, not copied UUIDs. Start with a 24-hour absolute horizon centered on the accepted start, at 15-minute increments: at most 97 start instants. Keep the accepted duration fixed, so this gate does not silently shorten, split or merge work. Candidates may include the original interval only as a marked current baseline; only different intervals count as alternatives.

The candidate may satisfy the **supported current hard Temporal Constraints** yet still have unknown real-world availability/capacity. It must be labeled accordingly. B12-A's known hard duration violation may remain unresolved when the existing duration is fixed; this is a truthful modeled failure, not proof that no broader replan can work. B12-B solves no generic overlap, resource allocation, recurrence, multi-actor or group replan problem.

## 2. Evidence and semantics

The request carries the Plan state and selected Step reference. The server rereads the guarded Plan/Dependency truth, current accepted Schedule MaterialState and current Activity Temporal Constraints; it rejects an unlinked Step, unsupported/non-absolute/multiple Schedule, stale Plan or unresolved/unsatisfied prerequisite with a typed result. It takes only current accepted absolute inputs. Qualified Dependency `unknown` remains unknown and does not become a precedence time inequality. Step presentation order is never a dependency.

Candidate evaluation reuses B04's existing absolute Temporal Constraint evaluator for each grid interval. Hard violations are excluded. A not-evaluable applicable hard rule makes the result incomplete/unknown; it cannot certify a candidate as valid. Soft-rule evaluations are surfaced individually and never silently hardened or relaxed. The same supported-rule limitations as B12-A apply. A final self-scoped current-basis reread invalidates results if Plan/Dependency/Schedule/constraint evidence changes during computation. Include exact relevant MaterialState references, horizon, fixed duration, grid size, model/solver version, time limit and status in the typed result; do not persist a candidate as canonical truth.

The existing Movement Policy is not authorization for a B12-B effect. If its current state can be read within the present self-scoped API, carry its MaterialState and any blocking condition as an explicit review limitation. B12-C must independently revalidate policy and every effect precondition; B12-B never sends a move request.

## 3. Deterministic solver boundary

Use the selected Physical target OR-Tools 9.15 CP-SAT as a backend-only bounded adapter for this finite candidate set. Pin and lock the dependency through project tooling after approval; validate the actual installed API and deterministic repeatability locally. One integer grid-index variable selects an allowed interval after B04 rule evaluation; the objective minimizes absolute displacement from the accepted start, with earlier start as a stable tie-breaker. Enumerate at most three distinct solutions with deterministic settings and a bounded time limit. Do not invent a universal priority weight or capacity cost.

Keep technical solver status `OPTIMAL`, `FEASIBLE`, `INFEASIBLE`, `MODEL_INVALID`, `UNKNOWN` distinct. A timeout/limit or incomplete hard input returns `UNKNOWN`/incomplete, never `INFEASIBLE`. `INFEASIBLE` means only that **no grid interval within this 24-hour fixed-duration model** satisfies the supported hard rules; it is not a claim about other dates, changed durations or capacity. A solver candidate is a derived preview, not an accepted Schedule, Proposal act, Decision or authority.

## 4. API, product and non-effects

Expose one authenticated, bounded read-only candidate endpoint and deterministic OpenAPI/generated client. Add a contextual Home action next to the B12-A diagnosis for a linked Step with a supported current absolute Schedule. Display up to three candidate intervals and concise reasons/status, including unsupported or unknown input and an explicit message that availability/capacity are **not assessed**. The product cannot accept/apply a candidate in B12-B; B12-C owns user review and governed admission. Do not add a button that appears to commit a move.

No new canonical candidate/solver table or migration is planned. No Schedule, Plan, Dependency, Actual, Outcome, Movement Policy or Temporal Constraint may be changed by candidate generation. If inventory discovers that the current self-scoped material basis cannot be obtained without new DDL or that this bounded model is unsound, revise the gate before broadening it.

## 5. Focused local acceptance

1. A Plan with a linked Activity, accepted absolute Schedule and supported hard window/boundary produces deterministic nearby alternatives with exact current basis; no accepted placement or history changes.
2. Every returned interval passes the existing hard evaluator. Soft evaluations remain visible; candidates never claim resource/free-capacity proof.
3. Repeated calls with the same material basis and solver config return the same ordered candidates. A conflicting Schedule, Plan, constraint or Dependency correction invalidates a stale basis.
4. Unknown/unsatisfied prerequisites, unsupported/unplaced/multiple Schedules, hard not-evaluable rules and another self Person produce bounded typed outcomes without leaking private data.
5. A fixed-duration hard violation with no allowed grid slot produces only model-scoped infeasibility. A solver timeout/unknown status never becomes infeasibility; invalid model status stays distinct.
6. Backend unit/solver status corpus, guarded PostgreSQL/API, OpenAPI/generated client, web component, typechecks, Ruff and current catalog regression pass in the user's local worktree. No CI/GitHub Actions.

B12-B closes on focused automated proof. B12-C will review/submit effects with fresh policy/state checks. B12-D will run the integrated end-to-end real-app walkthrough once, immediately before parent B12 closure.

**Approval:** The user approved B12-B within this one-Activity, fixed-duration, 24-hour candidate scope. B12-C admission and whole-Plan automation remain separate gates.
