# Timeline / Temporal-Operational — Live Execution Ledger

- **Status:** CURRENT LIVE STATE — reconciled 2026-09-29
- **Branch:** `feature/timeline-temporal-operational`
- **Roadmap authority:** `docs/workstreams/timeline-temporal-operational-roadmap.md`
- **Continuation handoff:** `docs/workstreams/timeline-temporal-operational-handoff.md`
- **B10-D closure evidence:** `docs/workstreams/timeline-temporal-operational-b10-d-closure-2026-09-26.md`
- **B10-E closure evidence:** `docs/workstreams/timeline-temporal-operational-b10-e-closure-2026-09-26.md`
- **B11 closure evidence:** `docs/workstreams/timeline-temporal-operational-b11-closure-2026-09-28.md`
- **B13-A gate authority:** `docs/workstreams/timeline-temporal-operational-b13-a-scope-2026-09-28.md`
- **B13-A implementation checkpoint:** `docs/workstreams/timeline-temporal-operational-b13-a-implementation-2026-09-28.md`
- **B13-A closure evidence:** `docs/workstreams/timeline-temporal-operational-b13-a-closure-2026-09-28.md`
- **B13-B scope authority:** `docs/workstreams/timeline-temporal-operational-b13-b-scope-2026-09-28.md`
- **B13-B closure evidence:** `docs/workstreams/timeline-temporal-operational-b13-b-closure-2026-09-29.md`
- **B13-C scope:** `docs/workstreams/timeline-temporal-operational-b13-c-scope-2026-09-29.md`
- **B13-C closure evidence:** `docs/workstreams/timeline-temporal-operational-b13-c-closure-2026-09-29.md`
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
- **B13-D scope:** `docs/workstreams/timeline-temporal-operational-b13-d-scope-2026-09-29.md`
- **B13-D candidate gate:** `docs/workstreams/timeline-temporal-operational-b13-d-gate-2026-09-29.md`
- **B13-D closure evidence:** `docs/workstreams/timeline-temporal-operational-b13-d-closure-2026-09-29.md`
- **DB overlay:** `docs/database/timeline-temporal-operational.md`
- **Current persistence source frontier:** `20260929_93` (B12-C focused local proof)
- **Reported current catalog topology:** `_93` / `196|5|155|100|397|344|497|0|0|0` (focused local gate)
- **Completed functional frontier:** B13 ✅ CLOSED / user-reported acceptance 2026-09-29
- **Current implementation cursor:** B12-A closed / proven; B12-B closed / proven; B12-C closed / focused proof; B12-D implementation candidate / local gate pending; whole-B12 real-app acceptance reserved for B12-D; B13-D post-repair web rerun unreported
- **CI:** not authorized; local tests are run by the user

---

# 1. Permanent semantic boundaries

```text
Person != Account != Principal != Actor
Activity != Event != Routine
Routine != Recurrence != Occurrence
Occurrence != Schedule
Schedule != Temporal Constraint != Movement Policy
Schedule != Session != Actual
Session != Actual != Outcome
Actual != Outcome != Confirmation
Expected outcome != Outcome
Outcome != Observation
Outcome != lifecycle / operational state
Confirmation != Authority != Verification
Confirmation != Decision / Approval
Reconciliation != universal truth
Reconciliation != Confirmation != Outcome
Responsibility != Participation
participant != responsible actor != organizer/owner
planned/intended != happened
Step != Activity
Plan != Activity
Dependency != hierarchy
ordering != dependency
decomposition != execution precedence
proposal != accepted effect
projection != canonical truth
current accepted state != latest row
MaterialState payload != mutable runtime record
idempotency key != Domain identity
Undo != history rewind
```

---

# 2. Closed frontier

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
B10 Actual / Outcome / Confirmation / Reconciliation ✅ CLOSED 2026-09-26
  B10-A Actual / realization core                ✅ CLOSED / PROVEN 2026-09-25
  B10-B Outcome                                  ✅ CLOSED / PROVEN 2026-09-25
  B10-C Confirmation                             ✅ CLOSED / PROVEN 2026-09-26
  B10-D Reconciliation / resolution workflow     ✅ CLOSED / PROVEN 2026-09-26
  B10-E Final integration + acceptance           ✅ CLOSED / USER-REPORTED ACCEPTANCE 2026-09-26
B11 Advanced Recurrence / Conditional / Reminder ✅ CLOSED / USER-REPORTED ACCEPTANCE 2026-09-28
  B11-A Advanced Recurrence                      ✅ CLOSED / PROVEN
  B11-B Conditional Temporal Behavior            ✅ CLOSED / PROVEN
  B11-C Schedule-relative personal Reminder      ✅ CLOSED / PROVEN
  B11-D Whole-block integration gate             ✅ CLOSED / PROVEN
```

B10 closure evidence:

```text
B10-A timeline-temporal-operational-b10-a-closure-2026-09-25.md
B10-B timeline-temporal-operational-b10-b-closure-2026-09-25.md
B10-C timeline-temporal-operational-b10-c-closure-2026-09-26.md
B10-D timeline-temporal-operational-b10-d-closure-2026-09-26.md
B10-E timeline-temporal-operational-b10-e-closure-2026-09-26.md
```

B11 closure evidence:

```text
timeline-temporal-operational-b11-closure-2026-09-28.md
```

---

# 3. Active execution order

```text
B13 Work Structure / Decomposition / Dependencies ✅ CLOSED / USER-REPORTED ACCEPTANCE
  B13-A Work Structure Core                       ✅ CLOSED / PROVEN 2026-09-28
  B13-B Qualified Dependencies                    ✅ CLOSED / PROVEN 2026-09-29
  B13-C Execution Structure Constraints           ✅ CLOSED / PROVEN 2026-09-29
  B13-D Whole-block Integration / Proof / Acceptance ✅ CLOSED / USER-REPORTED 2026-09-29
B12 Replanning / Conflict / Solver                ◐ B12-D LOCAL GATE PENDING
  B12-A Current-truth conflict diagnosis           ✅ CLOSED / PROVEN 2026-09-29
  B12-B Bounded candidate generation / solver      ✅ CLOSED / PROVEN 2026-09-29
  B12-C Review / governed admission                ✅ CLOSED / PROVEN 2026-09-29
  B12-D Integration / product acceptance           ◐ IMPLEMENTED CANDIDATE / LOCAL GATE PENDING
B14 Temporal Create Completeness Gate             ⬜
B07 UI/UX Consolidation v1                        ⏸ DEFERRED UNTIL B14
B15 Whole Vertical Closure                        ⬜
```

Sequence authority:

```text
B09 → B10 → B11 → B13-A → B13-B → B13-C → B13-D → B12 → B14 → B07 → B15
```

No CI/GitHub Actions. The user runs local automated gates.

---

# 4. B10 closed chain

## B10-A — Actual

```text
20260925_74
159|5|115|93|305|258|435
```

```text
Session END != Actual
absence of Actual = unknown
known realization_occurred=false != absence
Session evidence != Actual identity
```

## B10-B — Outcome

```text
20260925_78
163|5|119|93|317|268|440
facet: outcome.disposition
one Outcome per Actual
```

Outcome disposition is pinned to one exact Actual realization MaterialState. The temporary `_75` vocabulary/result identity is superseded and must not return.

## B10-C — Confirmation

```text
20260925_79
167|5|123|93|329|279|446
facet: confirmation.attestation
```

```text
identity = (target Outcome MaterialState, confirmer Person, purpose)
absence of Confirmation != false
Confirmation != Authority / Verification / Decision
```

## B10-D — Reconciliation

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

Canonical identity:

```text
(outcome_disposition_material_state_ref, purpose_code)
```

Authority:

```text
Outcome owner is resolver
can confirm != can resolve
resolver identity is state data
```

Evidence pins exact Confirmation attestation MaterialStates. Corrections are append-only/current-history transitions and do not reinterpret older evidence.

Actions:

```text
unresolved
select
accept_multiple
defer
escalate
```

Generated client:

```text
cebfb557196d3fc0f412262a1d12feae9291b875
345 generated files deterministic/current
```

Final user-run B10-D gate:

```text
web typecheck PASS
web controls 6/6 PASS
api-client typecheck PASS
generated check PASS
backend B10-D/B10-C/OpenAPI inventory 6/6 PASS
```

Earlier PostgreSQL/runtime/API proof:

```text
4 passed in 14.94s
```

## B10-E — Integration / acceptance

Repository integration coverage:

```text
apps/backend/tests/integration/temporal/test_b10_e_whole_block.py
apps/web/src/features/temporal/timeline-truth-inspector.test.tsx
```

The real Home timeline runtime mounts the B10 truth inspector. The user performed the integrated walkthrough and reported the chain working, including Outcome correction without implicit transfer of old Confirmation/Reconciliation.

Classification:

```text
B10-E CLOSED / USER-REPORTED ACCEPTANCE
B10   CLOSED
```

---

# 5. B11 closure record

B11 is CLOSED / USER-REPORTED ACCEPTANCE 2026-09-28.

B11-A completion-relative and anchor-stream-relative recurrence uses `_81` and is locally proven. B11-B bounded `actual_realization` Condition uses `_82`–`_85`; its focused local gate passed at generated client `e79f6870` (PostgreSQL 4, OpenAPI 6, web 3, deterministic generation 361 files, client/web typechecks). The shared `_86` catalog probe measured `184|5|144|100|370|323|480|0|0|0`; both exact cross-representation tests passed after the CHECK-name and mapping-registration repairs.

B11-C has the approved narrow Schedule-relative self Reminder scope at `timeline-temporal-operational-b11-c-scope-2026-09-27.md`. Commit `9878b441` publishes forward-only `_86`, guarded self functions, mapping, API, OpenAPI inventory and focused tests. Commits `9d806355` and `e9a0f760` add existing-Schedule controls and the Create two-command partial retry path. Generated client `d0378e17` and focused local backend 5/web 16 gate passed; the `_86` topology probe and exact catalog tests passed.

B11-D verifies A/B/C together through `timeline-temporal-operational-b11-d-scope-2026-09-27.md`. The full local gate reported OpenAPI 7, PostgreSQL 14, generated check 364, both typechecks, web 24 and final Ruff pass after import-order repair. The first real-app attempt exposed recurring Create `Senza Life Area` validation and Advanced Recurrence `autobegin=False` read defects; both were repaired. The final isolated B11-D PostgreSQL rerun passed (`1 passed in 6.81s`) and the user reported the restarted integrated walkthrough working.

Closure authority is `timeline-temporal-operational-b11-closure-2026-09-28.md`. B11 is historical closed scope; do not describe its walkthrough as pending.

---

# 6. Closed frontier — B13-A Work Structure Core

Gate authority:

```text
docs/workstreams/timeline-temporal-operational-b13-a-scope-2026-09-28.md
```

Frozen distinctions:

```text
Plan != Activity
Step != Activity
Dependency != hierarchy
ordering != dependency
decomposition != execution precedence
```

Current goal:

```text
canonical Plan
→ Plan-owned internal work structure
→ structural Step semantics
→ optional reference to a real Activity without identity collapse
→ explicit ordering separate from decomposition
→ deterministic accepted/current-state + history behavior
→ bounded author/read proof
```

The discovery checkpoint chose flat `Plan -> Step`, existing Plan NativeRef, Plan-owned internal Step references, normalized immutable structure revisions, explicit presentation position and same-self Activity references. `_88` repaired replay and catalog names; `_89` qualified the accepted-current binding. OpenAPI, web/API typechecks, generated client and the UI test passed. The final focused PostgreSQL/catalog suite passed **9 tests in 24.09s** at `_89`; see `timeline-temporal-operational-b13-a-closure-2026-09-28.md`.

Forbidden in B13-A:

```text
generic work_item/node/edge ontology
Dependency semantics
B13-C execution constraints
B12 solver/replanning
automatic Schedule mutation
proposal acceptance semantics
```

---

# 7. Later gates

## B13-B — Qualified Dependencies

Closed / proven at forward-only `_90`. The user-run PostgreSQL/catalog gate passed **11 tests in 41.75s**; the focused web gate previously passed **6 tests** and both typechecks. See `timeline-temporal-operational-b13-b-closure-2026-09-29.md`. Whole-B13 acceptance remains B13-D.

## B13-C — Execution Structure Constraints

Closed / focused proof at forward-only `_92`. Immutable Plan Step revisions carry Plan-contextual divisibility, optional maximum proposed-slice count and bounded proposed-slice merge permission. Read-only assessment counts explicit proposed slices and reuses the Activity Temporal Constraint evaluator. Spacing, preparation and recovery remain unsupported and not editable. The user-run B13-A/B/C plus exact catalog suite passed **13 tests in 29.16s**; the earlier web suite passed **11 tests**, with generated-client determinism and both typechecks. See `timeline-temporal-operational-b13-c-closure-2026-09-29.md`. Whole-B13 real-app acceptance remains B13-D.

## B13-D — Whole-block Integration / Proof / Acceptance

The candidate integrates B13-A/B/C on one Plan in a PostgreSQL test and one Home panel test. Its scope and executable local gate are `timeline-temporal-operational-b13-d-scope-2026-09-29.md` and `timeline-temporal-operational-b13-d-gate-2026-09-29.md`. The initial user-run gate passed: generated check (383 files), both typechecks, web **12**, backend contract/unit **3**, PostgreSQL **14**, and Ruff. The direct Activity-to-Step repair removed manual UUID linking. Screenshots confirmed both linked Steps and the Record → Mix `Actual avvenuto` Dependency in `sconosciuta`; the user then reported overall acceptance with “ok va chiudiamo” after the full walkthrough. The final seven-file web rerun was not reported, so its expected 16 tests are unverified. B13-D and B13 are closed on user-reported real-app acceptance with this explicit verification gap; see `docs/workstreams/timeline-temporal-operational-b13-d-closure-2026-09-29.md`.

## B12 — Replanning / Conflict / Solver

Block and B12-A scopes are in `timeline-temporal-operational-b12-scope-2026-09-29.md` and `timeline-temporal-operational-b12-a-scope-2026-09-29.md`. B12-A is closed / proven: generated 389, both typechecks, web 4, API contract 1, Ruff, PostgreSQL/catalog 11 passed in 26.14s in the user's worktree; see `timeline-temporal-operational-b12-a-closure-2026-09-29.md`. B12-B is closed / proven on the user-run focused local gate: generated 393, both typechecks, web 3, backend 8, Ruff and PostgreSQL/catalog 11 passed in 24.63s; see `timeline-temporal-operational-b12-b-closure-2026-09-29.md`. B12-C is closed on the reported focused local gate: generated 397, both typechecks, web 4, Ruff, backend 9 and PostgreSQL 19 passed. See `timeline-temporal-operational-b12-c-closure-2026-09-29.md`. B12-D scope was approved; integrated candidate proof and local gate are in `timeline-temporal-operational-b12-d-implementation-2026-09-29.md` and `timeline-temporal-operational-b12-d-gate-2026-09-29.md`. Real-app proof runs once in B12-D before parent B12 closure. Proposal != accepted Schedule; solver UNKNOWN != INFEASIBLE; AI != scheduling authority.

## B14 — Temporal Create Completeness Gate

Every editable Create field must be canonically supported/proven, truthfully handed off, presentation-only, or hidden.

## B07 — UI/UX Consolidation v1

Deferred until B14 so final UI consolidation operates over truthful functional vocabulary.

## B15 — Whole Vertical Closure

Final whole-vertical reconciliation, regressions and dogfood after all functional/create/UI blocks are complete.
