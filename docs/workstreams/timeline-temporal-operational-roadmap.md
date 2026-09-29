# Timeline / Temporal-Operational Vertical — Implementation Roadmap

- **Status:** CURRENT EXECUTION ROADMAP — reconciled 2026-09-29
- **Branch/workstream:** `feature/timeline-temporal-operational`
- **Vertical boundary:** Home `+` creation/configuration → canonical temporal truth → Timeline projection/actions → bounded lifecycle completion
- **Completed functional frontier:** B13 ✅ CLOSED / user-reported B13-D real-app acceptance 2026-09-29
- **Current block:** B12 Replanning / Conflict / Solver — B12-D scope prepared
- **Current gate:** B12-A closed / proven on user-run focused gate; B12-B closed / proven; B12-C closed / focused proof; B12-D scope prepared / approval pending; whole-B12 real-app acceptance at B12-D
- **B12 block scope:** `docs/workstreams/timeline-temporal-operational-b12-scope-2026-09-29.md`
- **B12-A scope proposal:** `docs/workstreams/timeline-temporal-operational-b12-a-scope-2026-09-29.md`
- **B12-A closure:** `docs/workstreams/timeline-temporal-operational-b12-a-closure-2026-09-29.md`
- **B12-B scope proposal:** `docs/workstreams/timeline-temporal-operational-b12-b-scope-2026-09-29.md`
- **B12-B closure:** `docs/workstreams/timeline-temporal-operational-b12-b-closure-2026-09-29.md`
- **B12-C approved scope:** `docs/workstreams/timeline-temporal-operational-b12-c-scope-2026-09-29.md`
- **B13-D scope authority: `docs/workstreams/timeline-temporal-operational-b13-d-scope-2026-09-29.md`
- **B13-D candidate gate:** `docs/workstreams/timeline-temporal-operational-b13-d-gate-2026-09-29.md`
- **B13-D closure evidence:** `docs/workstreams/timeline-temporal-operational-b13-d-closure-2026-09-29.md`
- **B13-C scope authority:** `docs/workstreams/timeline-temporal-operational-b13-c-scope-2026-09-29.md`
- **B13-C closure evidence:** `docs/workstreams/timeline-temporal-operational-b13-c-closure-2026-09-29.md`
- **B13-B scope authority:** `docs/workstreams/timeline-temporal-operational-b13-b-scope-2026-09-28.md`
- **B13-B closure evidence:** `docs/workstreams/timeline-temporal-operational-b13-b-closure-2026-09-29.md`
- **B13-A scope authority:** `docs/workstreams/timeline-temporal-operational-b13-a-scope-2026-09-28.md`
- **B13-A closure evidence:** `docs/workstreams/timeline-temporal-operational-b13-a-closure-2026-09-28.md`
- **Current persistence source frontier:** B12-C / Alembic `20260929_93` (focused local proof)
- **Reported current catalog topology:** `_93` / `196|5|155|100|397|344|497|0|0|0` (focused local gate)
- **B10-D closure evidence:** `docs/workstreams/timeline-temporal-operational-b10-d-closure-2026-09-26.md`
- **B10-E closure evidence:** `docs/workstreams/timeline-temporal-operational-b10-e-closure-2026-09-26.md`
- **B11 closure evidence:** `docs/workstreams/timeline-temporal-operational-b11-closure-2026-09-28.md`
- **Deferred block:** B07 UI/UX Consolidation v1 — execute only after B14
- **Live execution ledger:** `docs/workstreams/timeline-temporal-operational-map.md`
- **Continuation handoff:** `docs/workstreams/timeline-temporal-operational-handoff.md`

This document is the sequencing authority for the remaining Timeline / Temporal-Operational work.

---

# 0. Execution discipline

Every functional block closes vertically:

```text
current Product / Domain / Logical / Physical authority
→ persistence / Alembic / Dictionary when required
→ backend / application
→ HTTP API / OpenAPI when public
→ generated API client when public
→ frontend / real product surface when part of the block
→ local automated proof
→ documentation reconciliation
→ only then advance
```

The user runs local tests. Do not use GitHub Actions/CI unless explicitly authorized.

Published migrations are immutable. Generated API-client artifacts come only from repository generation tooling and are never hand edited.

Permanent boundaries:

```text
Domain != Logical != Physical != API DTO != frontend ViewModel
projection != canonical truth
planned/intended != happened
Activity != Event != Routine
Routine != Recurrence != Occurrence
Occurrence != Schedule
Schedule != Session != Actual
Session != Actual != Outcome
Actual != Outcome != Confirmation
Confirmation != Authority / Verification / Decision
Reconciliation != universal truth
Expected outcome != Outcome
Responsibility != Participation
Person != Account
Step != Activity
Plan != Activity
Dependency != hierarchy
ordering != dependency
decomposition != execution precedence
proposal != accepted effect
current accepted state != latest row
MaterialState payload != mutable runtime record
idempotency key != Domain identity
Undo != history rewind
editable Create intent != canonical persistence
```

---

# 1. Active execution order

Historical block identifiers are preserved. Execution order is intentionally non-numeric where dependencies require it.

```text
B00 Real Data Spine                              ✅ CLOSED / PROVEN
B01 Activity Core                                ✅ CLOSED / PROVEN
B02 Schedule Core                                ✅ CLOSED / PROVEN
B03 Event Core                                   ✅ CLOSED / PROVEN
PRE-B04 DB/API GOVERNANCE                        ✅ CLOSED / FROZEN
B04 Temporal Constraints + Movement Policy       ✅ CLOSED / PROVEN
B05 Product Organization                         ✅ CLOSED / PROVEN
B06 Routine / Recurrence / Occurrence Baseline   ✅ CLOSED / PROVEN
B08 Session Runtime                              ✅ CLOSED / USER-REPORTED 2026-09-24
B09 Responsibility / Participation               ✅ CLOSED / USER-REPORTED 2026-09-25

B10 Actual / Outcome / Confirmation / Resolution ✅ CLOSED 2026-09-26
  B10-A Actual / realization core                 ✅ CLOSED / PROVEN 2026-09-25
  B10-B Outcome                                   ✅ CLOSED / PROVEN 2026-09-25
  B10-C Confirmation                              ✅ CLOSED / PROVEN 2026-09-26
  B10-D Reconciliation / resolution workflow      ✅ CLOSED / PROVEN 2026-09-26
  B10-E Final integration + acceptance            ✅ CLOSED / USER-REPORTED ACCEPTANCE 2026-09-26

B11 Advanced Recurrence / Conditional / Reminder ✅ CLOSED / USER-REPORTED ACCEPTANCE 2026-09-28
  B11-A Advanced Recurrence                       ✅ CLOSED / PROVEN (user-run local gates)
  B11-B Conditional Temporal Behavior             ✅ CLOSED / PROVEN (focused and `_86` catalog gates)
  B11-C Schedule-relative personal Reminder       ✅ CLOSED / PROVEN (focused and `_86` catalog gates)
  B11-D Whole-block integration gate              ✅ CLOSED / PROVEN; real-app acceptance ✅

B13 Work Structure / Decomposition / Dependencies ✅ CLOSED / USER-REPORTED ACCEPTANCE
  B13-A Work Structure Core                       ✅ CLOSED / PROVEN 2026-09-28
  B13-B Qualified Dependencies                    ✅ CLOSED / PROVEN 2026-09-29
  B13-C Execution Structure Constraints           ✅ CLOSED / PROVEN 2026-09-29
  B13-D Whole-block Integration / Proof / Acceptance ✅ CLOSED / USER-REPORTED 2026-09-29
B12 Replanning / Conflict / Solver                ◐ B12-D APPROVAL PENDING
  B12-A Current-truth conflict diagnosis           ✅ CLOSED / PROVEN 2026-09-29
  B12-B Bounded candidate generation / solver      ✅ CLOSED / PROVEN 2026-09-29
  B12-C Review / governed admission                ✅ CLOSED / PROVEN 2026-09-29
  B12-D Integration / product acceptance           ⬜ SCOPE PREPARED / APPROVAL PENDING
B14 Temporal Create Completeness Gate             ⬜
B07 UI/UX Consolidation v1                        ⏸ DEFERRED UNTIL B14
B15 Whole Vertical Closure                        ⬜
```

Execution sequence:

```text
B09 → B10 → B11 → B13-A → B13-B → B13-C → B13-D → B12 → B14 → B07 → B15
```

B13 precedes B12 so replanning/solver logic already understands canonical work structure, dependencies and execution-structure constraints. B14 precedes B07 so final UI consolidation does not polish unsupported editable intent.

---

# 2. Proven foundation through B09

B00–B06, B08 and B09 are closed. Their permanent boundaries remain active in all later work.

```text
Activity may exist without Schedule
Event != Activity
Routine != Recurrence != Occurrence
Occurrence != Schedule
Schedule is accepted-placement authority
Life Area / Tags are product organization, not Domain ownership
Person != Account != Actor
Responsibility != Participation
Session != Actual
Session END != completion
```

B09 adds typed Person/Responsibility/expected Participation behavior without collapsing Person into Account or expected Participation into Actual attendance.

---

# 3. B10 — Actual / Outcome / Confirmation / Reconciliation — CLOSED

B10 added realized/reconciled truth while preserving:

```text
planned/intended != happened
Schedule != Session != Actual
Session END != completion
Actual != Outcome != Confirmation
Confirmation != Authority / Verification / Decision
Reconciliation != universal truth
Expected outcome != Outcome
no Actual != known non-realization/failure
```

## B10-A — Actual / realization core — CLOSED / PROVEN

Closure evidence: `docs/workstreams/timeline-temporal-operational-b10-a-closure-2026-09-25.md`.

```text
Alembic  20260925_74
Topology 159|5|115|93|305|258|435
```

```text
Session END != Actual
absence of Actual = unknown
known realization_occurred=false != absence
Session evidence != Actual identity
current accepted realization != latest row
```

## B10-B — Outcome — CLOSED / PROVEN

Closure evidence: `docs/workstreams/timeline-temporal-operational-b10-b-closure-2026-09-25.md`.

```text
Alembic  20260925_78
Topology 163|5|119|93|317|268|440
facet: outcome.disposition
```

```text
one stable Outcome per Actual
Outcome disposition pinned to exact Actual realization MaterialState
Actual correction does not reinterpret older Outcome disposition
```

The temporary `_75` vocabulary/result identity model is superseded and must not return.

## B10-C — Confirmation — CLOSED / PROVEN

Closure evidence: `docs/workstreams/timeline-temporal-operational-b10-c-closure-2026-09-26.md`.

```text
Alembic  20260925_79
Topology 167|5|123|93|329|279|446
facet: confirmation.attestation
```

```text
identity = (target Outcome MaterialState, confirmer Person, purpose)
0..N confirmations per exact Outcome disposition MaterialState
absence of Confirmation != false
Outcome correction does not transfer Confirmation
```

The post-closure public-contract hardening is closed: OpenAPI/generated truth includes `201` creation, `200` replay and bounded ProblemDetails failures.

## B10-D — Reconciliation / resolution workflow — CLOSED / PROVEN

Scope: `docs/workstreams/timeline-temporal-operational-b10-d-scope-2026-09-26.md`.
Closure evidence: `docs/workstreams/timeline-temporal-operational-b10-d-closure-2026-09-26.md`.

Persistence frontier:

```text
20260926_80
```

Canonical family:

```text
outcome_reconciliation
outcome_reconciliation_state
outcome_reconciliation_evidence
outcome_reconciliation_current_history
outcome_reconciliation_operation
facet: outcome.reconciliation
```

Stable identity:

```text
(outcome_disposition_material_state_ref, purpose_code)
```

Authority boundary:

```text
Outcome owner is the only resolver in B10-D
can confirm != can resolve
resolver identity is state data
```

Evidence pins exact Confirmation attestation MaterialStates. Confirmation correction does not reinterpret older reconciliation; Outcome correction does not transfer reconciliation.

Approved contextual actions:

```text
unresolved
select
accept_multiple
defer
escalate
```

Generated client commit:

```text
cebfb557196d3fc0f412262a1d12feae9291b875
```

User-run proof:

```text
PostgreSQL/runtime/API + direct B10-C regression    4 passed in 14.94s
web typecheck                                       PASS
Confirmation + Reconciliation web controls         6 passed / 2 files
generated check                                     PASS — 345 files deterministic/current
api-client typecheck                                PASS
B10-D/B10-C/OpenAPI inventory backend gate          6 passed
```

No CI/GitHub Actions were used.

## B10-E — Final integration + acceptance — CLOSED / USER-REPORTED ACCEPTANCE

Closure evidence: `docs/workstreams/timeline-temporal-operational-b10-e-closure-2026-09-26.md`.

B10-E integrated the chain:

```text
Session → Actual → Outcome → Confirmation → Reconciliation
```

Repository integration coverage was added in:

```text
apps/backend/tests/integration/temporal/test_b10_e_whole_block.py
apps/web/src/features/temporal/timeline-truth-inspector.test.tsx
```

The B10 truth inspector is mounted from the canonical Home timeline runtime. The user performed the requested integrated real-app walkthrough and reported the flow working, including correction boundaries and reload persistence.

The B10-E-specific automated tests were added but were not separately reported as user-run at closure time; closure therefore records B10-E precisely as `USER-REPORTED ACCEPTANCE`, while B10-A through B10-D retain their `PROVEN` classifications.

Whole B10 is now CLOSED.

---

# 4. B11 — Advanced Recurrence / Conditional / Reminder — CLOSED

B11 extends recurrence and conditional/reminder behavior without RRULE-as-ontology, fake Activity materialization or an unjustified universal Reminder owner.

The editable Create reminder intent must leave B11 either:

```text
canonically supported
truthfully handed off
or hidden until supported
```

B11-A extends the B06 elapsed recurrence baseline with completion-relative and anchor-stream-relative provenance at `_81`. The user reported the focused PostgreSQL, OpenAPI, generated-client and web gates passing; generated client checkpoint `6d4c6188`. B11-B implements the bounded `actual_realization` condition at `_82`–`_85`. Its local automated gate passed (PostgreSQL 4, OpenAPI 6, web 3, generated check 361 files, both typechecks) and its generated client is at `e79f6870`; see `timeline-temporal-operational-b11-b-proof-2026-09-27.md`.

The local PostgreSQL probe measured `_86` at `184|5|144|100|370|323|480|0|0|0`. Dictionary entries and catalog tests target `_86`. The first exact gate passed 8 tests and failed 2 on CHECK names; after their repair, both tests exposed five unregistered B10-D mappings. Commit `3fe447af` registered them, and the user-run rerun passed both exact tests. B11-B is `CLOSED / PROVEN`; see its proof checkpoint and the B11-C closure record.

B11-C is a narrow self-personal Reminder configuration on an accepted Schedule with an exact start instant; see `timeline-temporal-operational-b11-c-scope-2026-09-27.md`. `_86` persistence/backend/API was published at `9878b441`; existing-Schedule and Create web checkpoints at `9d806355` and `e9a0f760`; generated client at `d0378e17`. The focused local gate passed backend 5 and web 16 tests, generation and client/web typechecks. The `_86` probe and both exact catalog tests passed; B11-C is `CLOSED / PROVEN` with evidence in `timeline-temporal-operational-b11-c-closure-2026-09-27.md`. Integrated real-app acceptance remains the whole-B11 gate. Delivery and generic automation remain excluded.

B11-D is the closed whole-block automated integration gate; scope is `timeline-temporal-operational-b11-d-scope-2026-09-27.md`, with closure evidence in `timeline-temporal-operational-b11-d-closure-2026-09-27.md`. It verifies A/B/C together on one canonical chain and then runs focused regressions. The integrated real-app walkthrough is performed after D, immediately before whole-B11 closure.

The B11-D backend integration test passed its first isolated local run (`1 passed in 7.20s`); the complete gate is recorded in `timeline-temporal-operational-b11-d-gate-2026-09-27.md`. The Timeline inspector routes Routine/Event Recurrence through the selected Occurrence's source while Actual/Condition remain on the Occurrence, and Reminder retry uses its existing canonical operation contract.

The user-run full gate passed OpenAPI 7, PostgreSQL 14, deterministic generation 364, both typechecks and web 24. Ruff found one import-order error in the new B11-D test, corrected at `c685d519`; the user pulled `37ce469a` and reported the Ruff rerun passing. The first B11 real-app attempt on 2026-09-28 exposed two product defects: recurring Create allowed `Senza Life Area` through to a generic failure, and Advanced Recurrence read failed with `autobegin=False`. Both repairs were published; the final isolated B11-D PostgreSQL rerun passed (`1 passed in 6.81s`) and the user reported the restarted integrated real-app walkthrough working. B11 is CLOSED / USER-REPORTED ACCEPTANCE; see `timeline-temporal-operational-b11-closure-2026-09-28.md`.

---

# 5. B13 — Work Structure / Decomposition / Dependencies — IN PROGRESS

B13 is now the functional frontier. Gate authority for the current slice is `docs/workstreams/timeline-temporal-operational-b13-a-scope-2026-09-28.md`.

B13 permanently distinguishes:

```text
1. INTERNAL STRUCTURE
   Step != Activity
   Plan != Activity

2. COMPOSITE WORK
   real Activities retain independent identity/lifecycle/Schedule/Session

3. DECOMPOSITION / ORDERING
   decomposition != execution precedence
   ordering != dependency

4. DEPENDENCY
   Dependency != hierarchy
```

B13 is intentionally split into four coherent gates:

## B13-A — Work Structure Core — CLOSED / PROVEN 2026-09-28

Introduce the minimum canonical Plan-owned decomposition foundation: internal structural Step semantics, optional references to real Activities, explicit ordering distinct from decomposition, accepted/current-state plus history behavior, and only the API/UI needed to prove the canonical path.

Forbidden in B13-A:

```text
generic work_item/node/edge ontology
hidden dependency semantics
auto-Schedule
solver/proposal behavior
maximum Session / merge / spacing / preparation / recovery constraints
promotion of Step to universal root identity without model authority
```

The discovery checkpoint selected flat `Plan -> Step`, normalized immutable structure revisions and explicit position. Existing Plan identity is reused; optional Activity references are same-self validated without identity collapse. OpenAPI, web/API typechecks, generated client and UI test passed locally. `_88` repaired replay and catalog naming; forward `_89` qualified the accepted-current update. The final user-run focused PostgreSQL/catalog suite passed **9 tests in 24.09s** at `_89`. See `timeline-temporal-operational-b13-a-closure-2026-09-28.md`.

## B13-B — Qualified Dependencies — CLOSED / PROVEN 2026-09-29

Scope authority: `timeline-temporal-operational-b13-b-scope-2026-09-28.md`. Forward-only `_90` implements Plan-scoped typed Actual/Outcome prerequisites, immutable qualifier history, current binding, replay/CAS receipts and bounded cycle diagnostics. The user-run focused PostgreSQL/catalog suite passed **11 tests in 41.75s**. The earlier focused web gate passed **6 tests** and both web/API-client typechecks. Dependency remains separate from containment and Step ordering; B13-D retains the whole-block real-app acceptance. See `timeline-temporal-operational-b13-b-closure-2026-09-29.md`.

## B13-C — Execution Structure Constraints

Closed / focused proof at `_92`. The supported Plan-contextual Step policy governs proposed planning-slice count and compatible union assessment, using the existing Activity Temporal Constraint evaluator. Spacing, preparation and recovery remain unsupported and not editable. The user-run B13-A/B/C and exact catalog suite passed **13 tests in 29.16s**; focused web, generated-client and typecheck gates passed on the published implementation. See `timeline-temporal-operational-b13-c-closure-2026-09-29.md`. Whole-B13 real-app acceptance remains B13-D.

## B13-D — Whole-block Integration / Proof / Acceptance

Scope and gate: `timeline-temporal-operational-b13-d-scope-2026-09-29.md` and `timeline-temporal-operational-b13-d-gate-2026-09-29.md`. The new whole-block PostgreSQL test and Home panel integration test bring A/B/C into one Plan chain. The initial user-run local gate passed: generated check (383 files), both typechecks, web **12**, backend contract/unit **3**, PostgreSQL **14**, and Ruff. Acceptance preparation then exposed the UUID copy/paste Activity-link flow. The direct Activity-to-linked-Step repair was used in the real app. Screenshots confirmed linked Record/Mix Steps and an `Actual avvenuto` Record → Mix Dependency evaluated as `sconosciuta`; the user then reported “ok va chiudiamo” after receiving the full walkthrough. This is user-reported acceptance, not itemized proof of every remaining manual check. The post-repair seven-file web rerun (expected 16 tests) has not been reported; do not claim it passed. See `docs/workstreams/timeline-temporal-operational-b13-d-closure-2026-09-29.md`. B13 is closed on that qualified evidence, and B12 is next for a separately approved scope gate.

---

# 6. B12 — Replanning / Conflict / Solver — B12-D SCOPE PREPARED

Deterministic-first replanning/conflict/solver:

```text
canonical truth + constraints/preferences + B13 dependencies
→ deterministic candidate generation / optimization
→ Proposal(s)
→ optional AI interpretation/ranking assistance
→ governed acceptance
→ canonical Schedule mutation
```

```text
proposal != accepted Schedule
preferred window != accepted Schedule
fallback policy != hidden mutation
solver UNKNOWN != INFEASIBLE
AI != scheduling authority
```

B12 may not invent work structure, dependency truth or B13 execution constraints. The block scope is `timeline-temporal-operational-b12-scope-2026-09-29.md`: B12-A current-truth diagnosis → B12-B bounded solver candidates → B12-C governed admission → B12-D whole-block acceptance. B12-A is closed / proven on the user's focused automated gate: generated 389, both typechecks, web 4, contract 1, Ruff and PostgreSQL/catalog 11 passed. See `timeline-temporal-operational-b12-a-closure-2026-09-29.md`. The whole-chain real-app walkthrough is B12-D, before closing B12. B12-B is closed / proven on the user-run focused local gate: generated 393, both typechecks, web 3, backend 8, Ruff and PostgreSQL/catalog 11 passed in 24.63s; see `timeline-temporal-operational-b12-b-closure-2026-09-29.md`. B12-C is closed on the reported focused local gate: generated 397, both typechecks, web 4, Ruff, backend 9 and PostgreSQL 19 passed. See `timeline-temporal-operational-b12-c-closure-2026-09-29.md`. B12-D scope is prepared in `timeline-temporal-operational-b12-d-scope-2026-09-29.md` for separate approval.

---

# 7. B14 — Temporal Create Completeness Gate

For every editable field visible in Create, exactly one must be true:

```text
A. canonically persisted and behaviorally proven
B. truthful handoff to owning capability
C. explicitly presentation/read-only
D. hidden/removed until supported
```

Forbidden:

```text
editable UI value
→ collected
→ silently ignored by normal submit
```

---

# 8. B07 — UI/UX Consolidation v1

Execute after B14 so final Home/Timeline/`+`/editors/actions/navigation are designed once against truthful functional vocabulary. B07 does not create missing semantics.

---

# 9. B15 — Whole Vertical Closure

Final whole-vertical reconciliation across migrations/catalog/Dictionary, backend/API/client, frontend, negative invariants, local automated proof and dogfood.

B15 does not reopen closed semantic boundaries without explicit evidence.
