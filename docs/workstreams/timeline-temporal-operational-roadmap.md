# Timeline / Temporal-Operational Vertical — Implementation Roadmap

- **Status:** CURRENT EXECUTION ROADMAP — U6 continuation reconciled 2026-10-03
- **Branch/workstream:** `feature/timeline-temporal-operational`
- **Vertical boundary:** Home `+` creation/configuration → canonical temporal truth → Timeline projection/actions → bounded lifecycle completion
- **Completed functional frontier:** B12 ✅ CLOSED / qualified user-reported B12-D acceptance 2026-09-30
- **Current block:** B14 + B07 user-guided product/UI consolidation
- **U6:** ACTIVE / CANDIDATE at `_103`. The user's real-app screenshots triggered Advanced Create layout and language corrections plus a canonical name for future planned Session rows. The `_102` PostgreSQL/catalog gate passed 9 tests and the atomic B08 minimum test passed (1); `_103` PostgreSQL/catalog proof and corrected real-app acceptance remain pending. See `timeline-temporal-operational-b14-u6-candidate-2026-10-02.md`.
- **Activity intervals (2026-10-05):** Branch candidate `_106` separates occupied Activity intervals (`interval`) from future planned Sessions (`planned`), replaces `Unica / Suddivisa` with `+ Aggiungi intervallo`, and projects each Activity interval as a separate Timeline card. Current semantics: `docs/domain/decisions/activity-intervals-and-sessions-v2.md`. Local migration/build/visual proof remains open; no PASS claimed.
- **Current gate:** B12-D and B12 closed on qualified user-reported acceptance; B14/B07 is a live user-directed implementation cycle
- **B14/B07 working ledger:** `docs/workstreams/timeline-temporal-operational-b14-ui-consolidation-2026-09-30.md`
- **B12 block scope:** `docs/workstreams/timeline-temporal-operational-b12-scope-2026-09-29.md`
- **B12-A scope proposal:** `docs/workstreams/timeline-temporal-operational-b12-a-scope-2026-09-29.md`
- **B12-A closure:** `docs/workstreams/timeline-temporal-operational-b12-a-closure-2026-09-29.md`
- **B12-B scope proposal:** `docs/workstreams/timeline-temporal-operational-b12-b-scope-2026-09-29.md`
- **B12-B closure:** `docs/workstreams/timeline-temporal-operational-b12-b-closure-2026-09-29.md`
- **B12-C approved scope:** `docs/workstreams/timeline-temporal-operational-b12-c-scope-2026-09-29.md`
- **B12-C closure evidence:** `docs/workstreams/timeline-temporal-operational-b12-c-closure-2026-09-29.md`
- **B12-D approved scope:** `docs/workstreams/timeline-temporal-operational-b12-d-scope-2026-09-29.md`
- **B12-D implementation checkpoint:** `docs/workstreams/timeline-temporal-operational-b12-d-implementation-2026-09-29.md`
- **B12-D local gate:** `docs/workstreams/timeline-temporal-operational-b12-d-gate-2026-09-29.md`
- **B12 closure:** `docs/workstreams/timeline-temporal-operational-b12-closure-2026-09-30.md`
- **B13-D scope authority:** `docs/workstreams/timeline-temporal-operational-b13-d-scope-2026-09-29.md`
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
- **UI consolidation:** B07 runs within the active B14 user-guided cycle
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
B12 Replanning / Conflict / Solver                ✅ CLOSED / QUALIFIED USER ACCEPTANCE 2026-09-30
  B12-A Current-truth conflict diagnosis           ✅ CLOSED / PROVEN 2026-09-29
  B12-B Bounded candidate generation / solver      ✅ CLOSED / PROVEN 2026-09-29
  B12-C Review / governed admission                ✅ CLOSED / PROVEN 2026-09-29
  B12-D Integration / product acceptance           ✅ CLOSED / QUALIFIED USER ACCEPTANCE 2026-09-30
B14 + B07 Product / UI Consolidation              ◐ ACTIVE — USER-GUIDED
B15 Whole Vertical Closure                        ⬜
```

Execution sequence:

```text
B09 → B10 → B11 → B13-A → B13-B → B13-C → B13-D → B12 → B14+B07 → B15
```

B13 precedes B12 so replanning/solver logic already understands canonical work structure, dependencies and execution-structure constraints. B14 and B07 now run together so field truth, product rules and UI placement are corrected in the same user-directed delivery cycle.

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

# 6. B12 — Replanning / Conflict / Solver — CLOSED / QUALIFIED ACCEPTANCE

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

B12 may not invent work structure, dependency truth or B13 execution constraints. The block scope is `timeline-temporal-operational-b12-scope-2026-09-29.md`: B12-A current-truth diagnosis → B12-B bounded solver candidates → B12-C governed admission → B12-D whole-block acceptance. B12-A is closed / proven on the user's focused automated gate: generated 389, both typechecks, web 4, contract 1, Ruff and PostgreSQL/catalog 11 passed. See `timeline-temporal-operational-b12-a-closure-2026-09-29.md`. The whole-chain real-app walkthrough is B12-D, before closing B12. B12-B is closed / proven on the user-run focused local gate: generated 393, both typechecks, web 3, backend 8, Ruff and PostgreSQL/catalog 11 passed in 24.63s; see `timeline-temporal-operational-b12-b-closure-2026-09-29.md`. B12-C is closed on the reported focused local gate: generated 397, both typechecks, web 4, Ruff, backend 9 and PostgreSQL 19 passed. See `timeline-temporal-operational-b12-c-closure-2026-09-29.md`. B12-D scope was approved; the original user-run gate passed on `75891447` (web 11, backend 9, PostgreSQL/catalog 20, generated 397, both typechecks and Ruff). The user accepted closure without an itemized post-repair real-app report; the affected automated rerun is also unreported. The qualified closure is in `timeline-temporal-operational-b12-closure-2026-09-30.md`; proof and commands are in `timeline-temporal-operational-b12-d-implementation-2026-09-29.md` and `timeline-temporal-operational-b12-d-gate-2026-09-29.md`.

---

# 7. B14 + B07 — user-guided product and UI consolidation

The user directs the backlog while using the application. The active ledger is `timeline-temporal-operational-b14-ui-consolidation-2026-09-30.md`. Every change can include UI placement, interaction rules and the owning application/persistence work required to make it real.

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

# 8. B15 — Whole Vertical Closure

Final whole-vertical reconciliation across migrations/catalog/Dictionary, backend/API/client, frontend, negative invariants, local automated proof and dogfood.

B15 does not reopen closed semantic boundaries without explicit evidence.


## 2026-10-06 — B14 recurring Activity candidate update

The current branch now carries the complete recurring-Activity template candidate
for Create: Activity intervals, planned Sessions, Sub-Activities, Session
settings, outcome review, Reminder lead and explicit placement protection are
inherited per materialized Occurrence. Life Area authoring is aligned with
one-off Activity Create (none / existing / create-new), the virtual unassigned
Timeline bucket is non-authorable, Timeline organization refresh follows
authoritative checkpoint/materialization, and root start-time edits preserve
duration instead of silently manufacturing an overnight interval.

This remains **candidate / unproven** until the user-run local gate and real-app
acceptance pass. Event recurrence parity is a subsequent shared-infrastructure
pass; Activity-only structure semantics must not be copied into Event.

## 2026-10-08 — B14/B07 post-create consolidation cursor

Active B14 authority: latest section of
`timeline-temporal-operational-b14-ui-consolidation-2026-09-30.md`.
Following successful focused Activity interval replan (Ruff/4 unit/
15 PostgreSQL/15 web + deterministic 483 generated output published
in `c22f04ae`) and post-create Objective ADD (web typecheck,
17/17 focused web), Inspector/Edit/Duplicate is **not** yet closed.
User-approved recurrence edit scopes are **Solo questa** and
**Questa e le prossime** only; the selected instance is always
included, other already-past instances excluded. Past factual
correction is allowed and becomes canonical; deletion of recorded
past facts is not.

Work order: M1 recurrence-instance scope targeting/preview/CAS;
M2 logical Objective definition/reality correction with immutable
history; M3 Activity residual edit surfaces; M4 faithful duplicate
and Event parity; M5 product dogfood and B15 exact whole-vertical
acceptance. These M1–M5 are OPEN; B01–B13 closures retain their
previously qualified evidence, not an invented fresh full suite.

## 2026-10-08 — M1-A green / M1-B read candidate

M1-A pure selected-instance targeting **CLOSED ON FOCUSED LOCAL PROOF**:
Ruff PASS and 18/18 unit tests reported by the user. M1 overall
remains OPEN. M1-B is a new `20261008_122` self-scoped,
non-truncating, maximum-10,000 **materialized** Occurrence inventory
read, delivered via a read-only API for Routine/Event source parity.
`materialized_only=true` and `apply_authorized=false` are explicit;
it is not a hidden bulk-edit or a guarantee that future unmaterialized
Occurrences have been updated. Database Dictionary and catalog
target 231/5/197/103/471/405/572. M1-B user-run local tests and
generated-client reconciliation remain pending. M1-C still needs
save-time CAS, future-template update, exception handling, and atomic
application for all editable Activity/Event fields. Scope truth:
`Solo questa` or `Questa e le prossime`, clicked always included,
other already-past instances never touched.

## 2026-10-08 — M1 metadata end-to-end candidate; full domain integration remains

M1-A (18 unit, Ruff) and M1-B (_122; 10 PostgreSQL,
generation/484 deterministic, API/Web typecheck) are proven
by user local output. Consolidated _123 M1 metadata integration
is published in one branch candidate with append-only edit history,
server owner/CAS/replay targeting, selected/past/future split,
future materialization and Inspector/Timeline readback, Activity
metadata scope choice, Event backend/Timeline parity and tests.
User-run gate for _123 and canonical generated artifacts remains
pending; **do not mark full B14/B07 closed**. Follow the accepted
two-scope semantics throughout M2 Objective, M3 remaining Activity
settings and M4 Event Inspector/Duplica, then M5/B15 real UX acceptance.

## 2026-10-08 — M1 _124 corrective gate, existing domain stages intact

The _123 user-run gate exposed a shared one-off Activity
profile read regression (4 failing PostgreSQL B14 tests)
and two Ruff I001; all 18 unit, 21 Web, generation 489,
API/Web typecheck passed. New _124 adds an explicit safe
one-off Activity branch and Timeline guard, with a PostgreSQL
regression case; no new object, same database topology.
M1 metadata candidate now awaits one _124 user-run whole
gate. Domain stages M2–M5 remain open by design, no
separate micro-step churn.

## 2026-10-08 — M1 metadata implementation: verified local gate / published

M1 is **CLOSED for the explicitly limited Activity/Event recurring general-metadata vertical**, not for all Activity/Event modifications. User-run proof: M1-A pure selector 18/18 unit + Ruff, M1-B 10/10 PostgreSQL + client check, _124 whole focused PostgreSQL/Vitest/API/Web/generated gates all PASS, corrective Ruff PASS. The user then committed and pushed all nine generated OpenAPI/Orval artifacts in `55a017b9`; `git status --short` printed no changes. Current DB revision _124 and exact catalog 232/5/202/103/473/408/576. Local proof is focused automated proof, **not** real-app visual acceptance.

The two scopes remain `Solo questa` and `Questa e le prossime` with clicked Occurrence included. The second also affects later future, not other already-past instances; inherited future changes use immutable source-wide profile edit revisions, owner/CAS, replay and protected conflict behavior. In M1 the edited fields are only general metadata (title, description, location, color), with Activity editor and Event API/Timeline support. M1 is NOT yet an implementation of scoped Objective, Session, Schedule, Reality policy, Life Area, Event Inspector UI or duplication changes. Continue with complete M2 Objective definition/current recorded-result correction under stable logical Objective identity, internal audit, and deterministic assessment reevaluation; then M3, M4, M5 and B15. No CI.

## 2026-10-08 — M2 whole-vertical Objective corrections candidate (_125 + _126)

M1 metadata technical closure remains backed by user local tests and published generated client. **M2 implementation candidate** is now on the branch (NOT YET USER-TESTED): append-only definition revision for the *same* logical `objective_ref`, owner/CAS/replay and immutable original Evaluation receipt; past numerical/boolean Observations can be re-evaluated deterministically after a definition correction without overwriting observations; qualitative manual judgments are never synthesized. Correcting a recorded result appends a new Observation and current Evaluation instead of deleting the historical fact.

For generated recurring Objective definitions the original materializer operation ID establishes stable template-slot provenance distinct from the mutable display order. `Solo questa` always includes selected. `Questa e le prossime` includes the selected plus only later future generated instances; other already-past instances remain unchanged. New _126 source-policy revisions cover as-yet-unmaterialized future instances, with owner/source CAS, bounded inventory, future skip/Actual/Observation/individual-revision conflict rejection and idempotent replay. Activity Objective editor now permits modifying current definitions and correcting results and shows both scopes only for verified generated Objective lineage. Manually added per-instance Objectives remain individual-only, never silently mapped to a different Objective.

_125 + _126 Database Dictionary candidate: **234 tables, 5 views, 207 routines, 103 triggers, 477 indexes, 414 FKs, 586 CHECK**. Backend, typed HTTP/API, Activity UI, and PostgreSQL/Vitest coverage are present; **one consolidated local gate is PENDING**. Generated OpenAPI/Orval client still needs local generation and eventual publication if gate passes. M3/M4/M5 and B15 remain open; no CI.

## 2026-10-08 — M2 third user local gate: actual PostgreSQL frontier (supersedes earlier "pending" notes)

User local gate on `2e5028df` reached `SYNTAX=0`, `POSTGRES=1` (**16 passed, 4 failed**), `GENERATE=0`, `GENERATED_CHECK=0`, `API_TYPECHECK=0`, `WEB_TYPECHECK=0`, `VITEST=0`. The sole Ruff failure `RUFF=1` was an import-format `I001` in `mappings/b14_create_closure.py`; the source was corrected on GitHub in `1ff3e500` but still needs local verification. Unlike the two earlier M2 gates, migrations through `20261008_126` ran and PostgreSQL executed the functional suite, so this is **not** a collection/syntax failure.

The **four remaining failures** are exactly:
1. `test_b14_m2_objective_corrections.py::test_objective_definition_and_result_corrections_are_canonical_without_deletion`
2. `test_b14_m2_objective_scope.py::test_generated_routine_objective_scope_selected_past_and_later_future`
3. `test_b14_m2_objective_scope.py::test_generated_event_objectives_share_future_scope_without_copying_results`
4. `test_database_current_catalog.py::test_current_database_cross_representation_is_exact`

The pasted gate output included the final summary and only the last 100 lines of the PostgreSQL log; the **individual failure tracebacks are not available** in the shared excerpt. Do not invent diagnoses or mark M2/test catalog green. The user's full traceback source is `/tmp/dante-m2-final.2m48YP/POSTGRES.log` in their local worktree. Read it **without re-running the suite**. `pnpm api:generate` created modified/untracked canonical OpenAPI/Orval files in the local working tree; deterministic generated check passed locally, **but these files are not yet committed/pushed**.

**Current frontier:** M1 general-metadata recurring scope is user-proven and published in `55a017b9`. M2 Objective corrections, immutable history and template-derived selected/future policy are implemented as **candidate only** on `_125/_126`; clear four PostgreSQL failures and exact Dictionary/catalog comparison, rerun one consolidated user-local gate, then publish generated client and record closure. M3 remaining Activity/Session/Life Area/Schedule edits, M4 Event Inspector and faithful Activity/Event Duplica, M5 real app/visual acceptance, and B15 whole-vertical closure remain open. Preserve approved semantics: only `Solo questa` / `Questa e le prossime`, clicked always included, other past unaffected, no deleting factual history or fabricating future Observations. User runs tests in `~/projects/dante`; no Actions/CI; no extra micro-gates.

## 2026-10-08 — M2 third PostgreSQL failure forensics and four-source fixes

The user supplied the **full `FAILURES` section** from `/tmp/dante-m2-final.2m48YP/POSTGRES.log`. Concrete root causes were confirmed, rather than guessed:
1. `test_objective_definition_and_result_corrections_are_canonical_without_deletion`: all actual HTTP recording/definition/replay/CAS checks reached their expected status; the last assertion incorrectly expected JSON numeric `6` instead of the contract's Decimal serialization string `"6"`. Test now uses `Decimal(str(...))`. The same test's subsequent internal-audit query was also preemptively repaired to use the **isolated test administrator**; `dante_runtime` must not gain raw Observation/Evaluation table SELECT.
2. `test_generated_routine_objective_scope_selected_past_and_later_future`: test setup generated a `floating_local` recurrence, but the real recurring-Activity template materializer requires an actual `named_zone` wall time and zone. Test now uses a named-zone daily recurrence (`Europe/Rome`, explicit DST policies); production materializer unchanged.
3. `test_generated_event_objectives_share_future_scope_without_copying_results`: the test attempted direct SELECT on `dante.temporal_objective` under `dante_runtime` and correctly received `InsufficientPrivilege`. Both Event and Routine tests now read **replayable B06 checkpoint identities**, linked Activity refs via `dante.list_self_routine_occurrence_activities`, and Objective refs through `dante.list_self_temporal_objectives`. Removed all raw protected-table SELECTs from the routine/event Objective-scope test; production owner ACL unchanged.
4. `test_current_database_cross_representation_is_exact`: the final ORM registry count assertion still expected 232 tables even though mapping, dictionary and live catalog all enumerate **234**. Changed only stale test literal to 234.

All fixes committed/pushed on `feature/timeline-temporal-operational` (not CI): `fae4dcbf`, `b72d7f2b`, `470fde9d`, `61dd6913`, `b5c55489`. Post-edit branch readback verified single Objective mapping classes, correct fingerprints, no test table-policy bypass, and all four corrections. **These edits have not yet been subjected to the next user-run local gate; M2 is NOT closed.** DB expected revision `20261008_126` and topology `234/5/207/103/477/414/586` remain unchanged; no speculative migrations and no role grants. Rerun the whole focused Ruff + PostgreSQL/catalog + generated API/check + API/Web TS typechecks + Vitest gate once. If green, stage and publish only deterministic generated client files, then record M2 closure. M3/M4/M5/B15 remain open.

## 2026-10-08 — M2 Objective vertical CLOSED on complete user-local focused gate

**This latest closure supersedes the earlier M2 candidate, 16/4 failing gate and four-source repair notes above; keep those sections as historical diagnosis, not as current status.** User pulled `b1599c19` and ran the whole consolidated M2 gate in `~/projects/dante`. Reported results: `SYNTAX=0`, `RUFF=0`, `POSTGRES=0`, `GENERATE=0`, `GENERATED_CHECK=0`, `API_TYPECHECK=0`, `WEB_TYPECHECK=0`, `VITEST=0`. This is locally proven *focused automated* technical closure of logical Objective definition revisions, recorded result corrections, Routine/Event generated-series selected/future inheritance, immutable audit and the exact _126 catalog comparison; it does **not** establish full product dogfood or B14/B15 closure. Generated API client was committed and successfully pushed by the user in `09dc26f9` (10 OpenAPI/Orval files; 1534 additions/23 deletions); remote branch HEAD and generated models verified after push. Canonical revision `20261008_126`; catalog expectation `234 tables / 5 views / 207 routines / 103 triggers / 477 indexes / 414 FK / 586 CHECK`, now included in a passing exact-catalog focused gate.

**New current frontier: M3** complete remaining Activity post-create edits and owner-domain integrations: rename existing planned Session display names preserving Schedule/execution identity/history; explicitly unassign/null primary Life Area with correct ownership semantics; resolve still-unhandled Create settings/temporal forms and Schedule/Reminder/policy edit paths; guard Activity retirement against past recorded-fact deletion. Apply the agreed `Solo questa` / `Questa e le prossime` scope wherever a recurring edit is supported (clicked always included, no alteration of other past instances). Inventory what already works first; no duplicate capability. After M3, M4 Event Inspector/edit and faithful Activity/Event duplication; M5 user real-stack/UI acceptance; B15 whole-vertical parity and closure. User runs local tests; no CI/Actions; consolidate complete owner-domain implementation before asking for one test gate.

## 2026-10-08 — M3 post-create Activity residual edit candidate on _127

**CURRENT STATUS: IMPLEMENTED CANDIDATE; THE USER HAS NOT RUN THE _127 LOCAL GATE.** Do not call M3 proven or B14/B15 closed. Following M2 user-green gate and generated publication `09dc26f9`, forward-only `20261008_127` adds three post-create behaviors:
- Actor-local Activity **and Event primary Life Area explicit unassignment**: four existing `life_area_ref` columns (current row + immutable operation receipts) accept NULL. The existing guarded assign functions retain self ownership, expected-revision CAS, durable operation receipt, replay/reuse rejection and monotonic revision after unassignment/reassignment; `list_self_unassigned_life_area_items` now recognizes explicitly null assignments. API/request/response/ORM, Activity editor and remote source accept NULL. No fake Life Area is created and no row deletion resets revision.
- Existing **planned Activity Session display name** can be revised through the same `activity_schedule_role` Schedule identity, using a new self-scoped `revise_self_planned_session_name` function (expected-name compare, idempotent same-target replay, validation, actor-ownership and retired guard). This is **presentation metadata**, not actual Session timing or schedule-history mutation. API, remote client, Activity editor and tests added; no history of prior *label values* is modeled in this candidate, so do not misrepresent it as a full append-only label ledger or a recurring template-wide edit.
- **Activity retirement historical-truth veto**: the existing guarded `retire_self_activity` function now rejects deletion/retirement whenever a Session (even ended), accepted Actual or recorded Objective observation/evaluation exists. The existing open-Session veto and retirement operation replay remain. Inspector explains the restriction and shows a conflict for recorded truth. Corrections to historical data continue through their own domain-owned edit endpoints.

Candidate DB topology `234 tables / 5 views / 208 routines / 103 triggers / 477 indexes / 414 FKs / 586 CHECK` at `20261008_127`; ORM, Dictionary entries, scope and exact catalog test expectations updated. The additional routine is the planned label capability; nullable columns create no new tables/constraints. Backend PostgreSQL test `test_b14_m3_residual_editor.py` checks Life Area null CAS/replay/actor isolation, Event parity, planned Schedule identity and recorded Session retirement veto; focused Web remote-contract regression added.

**Outstanding verification and scope:** no automated _127 proof yet; migrations/DB exact catalog, legacy B05/B14 and M2 regression, API generation/determinism, Web/API-client typecheck and Vitest must pass on the user local worktree before publishing canonical generated files. Remaining broad M3 questions include recurrence-template propagation for domain-owned Session name/Life Area, non-supported temporal-form UX and acceptance of historical label edits; do not claim these solved by selected-only mutations. Preserve `Solo questa`/`Questa e le prossime` for supported recurring edits with clicked included. After honest M3 gating/reconciliation, M4 faithful Activity/Event Duplica and Event Inspector and M5/B15 full product acceptance remain. No GitHub Actions or CI.

## 2026-10-08 — M3 _127 owner-domain edit vertical: user-local focused gate GREEN, client published

**This new entry supersedes all older _127 candidate/pending and 21-pass/5-fail notes; those remain historical diagnostics only.** The user pulled `d09af8a0` and ran the complete M3 WSL gate on `~/projects/dante`: `SYNTAX=0 RUFF=0 POSTGRES=0 GENERATE=0 GENERATED_CHECK=0 API_TYPECHECK=0 WEB_TYPECHECK=0 VITEST=0`. The user committed and pushed the deterministic OpenAPI/Orval artifacts in `6fdda05f` (`PUBLISH_EXIT=0`, ten generated files, 343 additions/10 deletions); verified as current remote HEAD.

M3-A **focused technical closure**: Activity/Event primary Life Area explicit unassignment with retained CAS revision/receipt; guarded planned Activity Session display-name correction on the same Schedule identity (no execution reconstruction); Activity retirement veto on already recorded Session/Actual/Objective factual truth; API/Web/client and backwards B05, B14, M2 regression + exact `20261008_127` catalog included in green gate. Canonical _127 topology `234 tables / 5 views / 208 routines / 103 triggers / 477 indexes / 414 FKs / 586 CHECK` (scope standalone total 447). No assistant-side local DB execution or manual UI acceptance claimed.

**M3-A is proven, broader M3 is NOT declared closed.** M3 remaining decision/implementation frontier: determine canonical scoped/future behavior for **new** Life Area and planned Session name edits originating from recurring templates and inspect any actual missing Schedule/Reminder/policy editing surfaces; currently following-scope on these new owner-domain edits is explicitly *disabled*, not silently performed. Evaluate applicability and protect nonselected past facts, potentially keep the domain-specific per-instance-only semantics only if explicitly accepted. Once bounded, progress to M4 faithful Activity/Event duplicate + Event Inspector, M5 real product visual/usage acceptance, B15 whole-vertical closure. Preserve no CI and user-local test authority.

## 2026-10-08 — M3-B owner-domain scope integrity candidate (no migration)

After M3-A user-green `_127` gate and published generated client `6fdda05f`, M3-B review of the actual Domain/Logical/Physical contracts, `routine_occurrence_materialization.py`, M1 `_123` and M2 `_126` established **no canonical following-series policy for Life Area or planned Session labels**. Routine materializer reads the owner's Life Area from `list_self_routines`; planned Session labels are copied from `routine_occurrence_policy.activity_template.planned_slices[].name`. Following edits cannot be safely implemented as a loop over already materialized Activity/Schedule rows: that misses future checkpoint instances and breaks owner/source CAS and historical exceptions. Routine/Event source semantics differ; do not imply parity without proof. The detailed negative-scope acceptance plan is in `docs/workstreams/timeline-temporal-operational-m3-b-owner-scope-2026-10-08.md`.

**Implemented on GitHub, newly UNTESTED:** the Activity editor now treats pending planned Session names as dirty and blocks general save and replan preview/apply until individually saved; after successful replanning it rebuilds the planned-name baseline. The recurring scope controls are visible even for Life Area/name-only drafts but disable `Questa e le prossime` when there is no supported metadata change, with explicit owner-domain-only guidance. Unsupported temporal Schedule forms are left untouched, with a non-conversion explanation. The remote Activity Inspector displays the recorded-truth retirement veto specifically instead of a generic stale conflict. Focused Vitest cases were added for draft loss, replan coexistence, recurring Life Area and Session name scopes, unsupported absolute temporal form, and retirement error/invalidation.

**State:** M3-A remains technically green; **M3-B candidate UI/guard implementation needs a fresh user-local Web typecheck and focused Vitest gate**. M3-B following-source implementation remains open: a new source policy must protect original selected Occurrence, future not-yet-generated occurrences, stable planned-template slot identity, independent per-instance edits, skip/Actual/recorded Session/Observation, owner and recurrence CAS; no such source policy is claimed or silently emulated. No new migrations or Dictionary topology changes: still `20261008_127` and `234/5/208/103/477/414/586`. M4/M5/B15 remain open. No GitHub Actions/CI; user runs local gate.

## 2026-10-08 — M3-B user local gate and Web test repair (pending rerun)

User pulled `71117ae5` and ran consolidated `/tmp/dante-m3b-gate.qlpPBc` on `~/projects/dante`. **Verified green locally:** `SYNTAX=0`, `RUFF=0`, `POSTGRES=0` (including the new negative-future-checkpoint test plus M2/M3-A regressions and exact DB catalog), `GENERATED_CHECK=0`, `API_TYPECHECK=0`. **Two Web-only failures:** `WEB_TYPECHECK=2` (`activity-inspector-actions.test.tsx:662`: array index `getAllByLabelText('Inizio')[0]` typed `HTMLElement | undefined` under strict no-unsafe-index) and `VITEST=1` (35 passed, one test failed at :717 because selected-only Life Area was *already* correctly preventing `this_and_following` and showing the general "Life Area e nomi delle Session pianificate si salvano soltanto per questa istanza" explanatory paragraph, whereas the test incorrectly expected the conditional warning shown only after an unsupported scope selection). This is **not** a PostgreSQL/schema regression.

**Code correction published:** `23daae86`, only `apps/web/src/features/home/ui/timeline/activity-inspector-actions.test.tsx`. Add explicit nonnull array index for first `Inizio` input (the Testing Library `getAllBy...` contract throws if there are zero elements) and assert the exact, reachable selected-only scope guidance. The guarded UI behavior, persistence, recurring source policy and DB code are unchanged. Remote HEAD verified at `23daae86029462c33213070ca855cb72e2e44aa8` before this documentation update. **Next action:** user runs just `pnpm --filter @dante/web typecheck` and the four M3-B focused Vitest files after `git pull --ff-only`. No reason to re-run passing PG and generated-client checks for this test-only change; no regenerated client needed. **M3-B guard subvertical NOT closed until local Web recheck passes.** This does not close the separate, unimplemented source/template `Questa e le prossime` policy for Life Area/planned Session names; full M3, M4/M5 and B15 still OPEN. No CI/Actions.

## 2026-10-08 — M3-B UI/negative-scope guard subvertical locally GREEN

**Latest acceptance supersedes earlier M3-B "pending Web recheck" entries.** The user pulled `b03d8aa4` into WSL `~/projects/dante` and ran the focused Web recheck: `WEB_TYPECHECK=0`, `VITEST=0`, 4 test files / **36 tests passed** (Activity Inspector UI 23, Remote Inspector 3, Remote Activity Settings 7, Remote Recurring Profile 3). Log directory `/tmp/dante-m3b-web-final.L8HfvO`. The preceding combined M3-B gate had already passed `SYNTAX=0`, `RUFF=0`, `POSTGRES=0` (including the new negative future-checkpoint Routine test and prior M3-A/M2 regression), `GENERATED_CHECK=0`, `API_TYPECHECK=0`; after these, **all bounded M3-B guard checks are proven green locally**. No schema/client change after the original backend green run; final Web fix was test-only `23daae86`. No new API generation or client publication required.

**CLOSED as bounded technical work:** M3-B editor safeguards, explicit individual-only mode, unsaved planned-name replan/save protection, truthful incompatible temporal-form UI, recorded-fact retirement reporting, and negative no-implicit-following provenance proof. **NOT CLOSED:** M3 following-source policy for optional Life Area or planned Session names of recurrence-derived Activity/Event Occurrences. `Questa e le prossime` remains explicitly disabled for these owner-domain fields. Future and already materialized later instances require an owner-authoritative policy, source CAS, immutable operation replay and template slot provenance. M1, M2 and M3-A remain green; broader M3 open. M4 (Event Inspector / faithful Activity/Event duplication), M5 product UI acceptance and B15 closure open. Next work: read actual Routine/Event Domain/Logical/Physical and M1/M2 source policy implementations and implement bounded canonical source policy, then one user-local gate. No CI/Actions.

## 2026-10-08 — M3 delivered scope consolidated; no more micro-stages; M4 begun

Per user priority, **stop splitting the already user-proven M3 editor implementation** and advance to one combined **M4 Inspector/Edit/Duplicate** workstream (requirements and current candidate in `docs/workstreams/timeline-temporal-operational-m4-delivery.md`). M3 delivered/proven scope: Activity/Event nullable primary Life Area owner CAS, Activity planned Session renaming without Schedule/execution identity replacement, historic-fact retirement guard, supported core policy/Reminder and replan paths, clear selected-only recurring edit guards, and safe nonconverting temporal forms. _127 exact DB catalog + generated client `6fdda05f` and M3-B 36/36 Web regression are user-verified. **M3 implementation is accepted as delivered for this bounded scope; this does NOT waive or falsely close the global source-following feature.** The missing future source policy for Life Area and planned Session names remains **explicit B14 global-scope parity debt before B15**, with `Questa e le prossime` still disabled; never silently claim it works. No user-requested additional micro-gates.

**M4 underway (NOT green):** new Event duplicate seed from persisted canonical Timeline Schedule + Agenda/Life Area/expected participants; Event Inspector duplicate action that validates participants; explicit refusal of unrepresentable absolute Schedule and Activity duplicates with visible child content, plus focused tests. This is **not full Event Inspector/Edit/Duplicate parity**: still requires Event metadata modification, full Activity hierarchy/recurrent-template fidelity, other stored Event fields and full acceptance. Defer all validation requests until a coherent M4 block is complete, then one consolidated user-local gate. M5/B15 remain open. No GitHub Actions/CI.

## 2026-10-08 — M4 whole-block candidate assembled; ONE user-local gate outstanding

The M4 Event post-create edit/duplicate vertical is assembled on the GitHub branch. This entry **supersedes the earlier incomplete-M4 candidate cursor**; no local tests are claimed for the newly added code. New canonical `20261008_128_b14_m4_event_profile.py` (only one Alembic `_128` revision) owns immutable Event metadata revision history, actor/CAS/replay, with an explicit no-unscoped-recurring-source edit veto. The Event read exposes a canonical profile revision. `event_api.py` accepts guarded Event metadata edits. Event Inspector now supports metadata Title/Description/Location/Color, existing B03 Agenda, B05 Life Area and B09 Participation owners without forging replacements for them. One new integration test `test_b14_m4_event_profile.py` covers owner, CAS, replay, history and current read.

Event Duplica uses canonical persisted Schedule placement and per-Event details, Life Area and expected participants. The Event DST disambiguation now retains the resolved earlier/later fold; cross-fold, invalid clock precision and absolute forms without faithful Create representation are rejected, never silently normalized. A new owner-scoped `remote-event-recurrence-guard.ts` checks the authoritative Event Recurrence before Duplicate, and explicitly blocks unfaithful template-to-one-off conversion; unresolved participants likewise block. Activity Duplica checks authoritative persisted child count and occurrence provenance, not just displayed subitems, and refuses structures/series that cannot be fully reconstructed, preserving all existing Actual/Observation/Evaluation/Session history. These refusals are **known capability limits**, not claims of full copying of complex trees or series.

**Canonical DB target _128:** 235 tables, 5 views, 210 routines, 103 triggers, 479 indexes, 416 FKs, 587 CHECK. Dictionary scope/routine/table and exact current catalog expectations are updated. Backend+Web tests added/extended; OpenAPI/Orval generation for the new Event profile endpoint still needs publication from user-local checkout, not a manually authored generated client.

**Single consolidated verification:** user runs `bash tooling/verify-b14-m4-local.sh` in `~/projects/dante`, with PostgreSQL, Ruff, unit, API export/client determinism, TS and relevant Vitest. Logs and concise result codes remain visible; the script conditionally publishes **only** verified generated client files after all gates pass, with no CI/Actions. If red, fix all real failures before another whole-block gate; no micro-gates. M4 is **candidate / awaiting this one local gate**, not green. Then perform M5/B15 real-UI click-through; the separate M3 global `Questa e le prossime` owner-source policy for Life Area and planned Session labels remains an explicit B14 parity debt before B15. No misleading "fully complete" claim.

## 2026-10-08 — M4 technical gate GREEN, advance to M5

The user ran the one complete M4 local gate on the repaired branch: all ten stage results zero, including PostgreSQL/catalog and deterministic API client generation, backend/Web typechecks and focused Vitest. Evidence `/tmp/dante-m4-whole.5cpYvA`; the gate published seven generated API files as `77968de6`. M4 implemented Inspector/edit and supported duplicate paths are technically verified. The current execution frontier is one integrated M5 real-app visual/keyboard acceptance followed by B15 parity review. The source-wide `Questa e le prossime` behavior for primary Life Area and planned Session labels remains guarded and unimplemented, and unsupported complex/recurring duplication explicitly refuses rather than silently losing data. Neither limitation is erased by a green gate. No extra technical micro-gates or CI.

## 2026-10-09 — M5 Session editor, validation and Objective Inspector repair candidate

User real-app screenshots exposed three defects after the green M4 technical gate: Edit's planned-Session clock controls inherited broad Timeline input/button styling, Create showed an English range paragraph with a misplaced section-wide red outline, and entering a numeric Objective observation in Inspector opened the error boundary. The Web candidate excludes the shared Session clock controls from those broad editor selectors, removes the Edit-only offset, localizes the bounded structure message, and targets the invalid Session's date/time row. Numeric Objective input now snapshots the DOM value before React's deferred state updater. A dedicated Inspector regression records `8 km`; targeted Create validation checks outside-range and reversed Session times, and a form test confirms the inline Italian error and precise invalid row.

Coding-workspace proof: Web typecheck, changed runtime/new-test ESLint and four focused Vitest files (54 tests) pass. The older Create entry test file has pre-existing ESLint violations and was excluded from this lint command; its tests are included. No user WSL run, real-app visual proof, or PostgreSQL proof is claimed for this candidate. Alembic `_129/_130` untimed planned-Session persistence and Docker-assigned acceptance port are already on branch HEAD `ec648022`, but their user-local PostgreSQL/catalog gate remains pending. M4 stays technically green, M5 remains open, and B15 parity debt for `Questa e le prossime` Life Area/planned Session labels remains unchanged. Run one consolidated affected gate after publication; no CI or extra M4 gate.

## 2026-10-09 — User-local M5/untimed acceptance gate, Ruff repair pending

After pulling `b1b74c6d`, the user's WSL gate reported 13/13 PostgreSQL integration and exact-catalog tests passing on `_130`, Web typecheck passing, and 54/54 focused Vitest tests passing. Ruff alone reported four style violations in `test_b14_u2_authoring.py`: literal dict, compound assertion, and two intentionally naive datetimes for floating-local placement. The focused repair preserves test semantics and marks those two datetimes with `DTZ001` exemptions. This repair is not yet user-local Ruff verified; no second PostgreSQL/Web run is needed solely for this test-style change. The Create entry test also emitted an existing React cross-component setState warning while all tests passed; track separately from this blocking Ruff gate. M5 visual acceptance remains open; B14 source-following Life Area/planned Session naming remains guarded.

## 2026-10-09 — M5/untimed focused technical gate GREEN

The user pulled `0754ba1e` in WSL and reran the exact focused Ruff selection; **All checks passed**. The preceding run on `b1b74c6d` had already passed 13/13 PostgreSQL integration and exact-catalog tests, Web typecheck, and 54/54 focused Vitest tests. The intervening commit changed only test lint/syntax and documentation, so this completes the bounded technical gate without repeating green PostgreSQL/Web checks. The React cross-component update warning seen in an existing Create-entry test remains a non-failing follow-up observation. Next: the user inspects planned Session clock layout in Activity Edit, the localized precise range validation in Create, and numeric Objective input/recording in Inspector in the real app. M5 visual acceptance and B14 source-following `Questa e le prossime` parity debt remain open; no CI/Actions.

### 2026-10-09 — Activity Edit planned time and Timeline runtime candidate

The Activity Edit `Orario` switch now adds or withdraws a planned Session time through coordinated preview/apply. A new guarded `_131` placement capability preserves the Schedule identity when timing an unplaced planned row, including after a previous unschedule; the edit snapshot keeps untimed planned rows visible. New planned rows may be saved without a time. Core Edit requests have bounded database and web timeouts with an Italian retry error instead of an endless spinner. Timeline Activity cards show a combined Play/Pausa button and Stop. Workspace web typecheck and 40/40 focused Vitest tests pass; Python syntax and diff checks pass. PostgreSQL/Ruff and real-app acceptance await the user's local gate. No CI/Actions.
