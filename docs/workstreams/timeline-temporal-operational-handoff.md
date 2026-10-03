# Timeline / Temporal-Operational — Workstream Handoff

- **Status:** B12 CLOSED / QUALIFIED USER ACCEPTANCE — B14+B07 active as one user-guided product/UI cycle; U1 Create-entry candidate awaits user visual proof; affected B12-D rerun unreported
- **U6 continuation:** derived B10 Reconciliation queue candidate in `_96`; Sub-Activity, execution policy, planned slices and the remaining queue reasons are still open. Read `timeline-temporal-operational-b14-u6-candidate-2026-10-02.md` and the approved U6 gate before work.
- **Reconciled:** 2026-09-30
- **Branch:** `feature/timeline-temporal-operational`
- **Roadmap authority:** `docs/workstreams/timeline-temporal-operational-roadmap.md`
- **Live execution ledger:** `docs/workstreams/timeline-temporal-operational-map.md`
- **B13-A gate authority:** `docs/workstreams/timeline-temporal-operational-b13-a-scope-2026-09-28.md`
- **B13-A implementation checkpoint:** `docs/workstreams/timeline-temporal-operational-b13-a-implementation-2026-09-28.md`
- **B13-A closure evidence:** `docs/workstreams/timeline-temporal-operational-b13-a-closure-2026-09-28.md`
- **B11 closure evidence:** `docs/workstreams/timeline-temporal-operational-b11-closure-2026-09-28.md`
- **B13-B approved scope:** `docs/workstreams/timeline-temporal-operational-b13-b-scope-2026-09-28.md`
- **B13-B candidate checkpoint:** `docs/workstreams/timeline-temporal-operational-b13-b-implementation-2026-09-28.md`
- **B13-B closure evidence:** `docs/workstreams/timeline-temporal-operational-b13-b-closure-2026-09-29.md`
- **B13-C scope:** `docs/workstreams/timeline-temporal-operational-b13-c-scope-2026-09-29.md`
- **B13-C implementation checkpoint:** `docs/workstreams/timeline-temporal-operational-b13-c-implementation-2026-09-29.md`
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
- **B12 closure:** `docs/workstreams/timeline-temporal-operational-b12-closure-2026-09-30.md`
- **B14/B07 working ledger:** `docs/workstreams/timeline-temporal-operational-b14-ui-consolidation-2026-09-30.md`
- **B13-D scope:** `docs/workstreams/timeline-temporal-operational-b13-d-scope-2026-09-29.md`
- **B13-D candidate gate:** `docs/workstreams/timeline-temporal-operational-b13-d-gate-2026-09-29.md`
- **B13-D closure evidence:** `docs/workstreams/timeline-temporal-operational-b13-d-closure-2026-09-29.md`
- **DB overlay:** `docs/database/timeline-temporal-operational.md`
- **Current migration source head:** B12-C / Alembic `20260929_93` (focused local proof)
- **Reported current catalog topology:** `_93` / `196|5|155|100|397|344|497|0|0|0` (focused local gate)
- **B11 real-app acceptance:** USER-REPORTED PASS 2026-09-28
- **CI:** no CI/GitHub Actions unless explicitly authorized; user runs local tests

Read this first after a context reset. Repository HEAD remains the source of truth; re-fetch it before any write.

---

# 1. Exact current position

```text
B00–B06 ✅ CLOSED / PROVEN
B08     ✅ CLOSED / USER-REPORTED 2026-09-24
B09     ✅ CLOSED / USER-REPORTED 2026-09-25
B10     ✅ CLOSED 2026-09-26
  B10-A ✅ CLOSED / PROVEN 2026-09-25
  B10-B ✅ CLOSED / PROVEN 2026-09-25
  B10-C ✅ CLOSED / PROVEN 2026-09-26
  B10-D ✅ CLOSED / PROVEN 2026-09-26
  B10-E ✅ CLOSED / USER-REPORTED ACCEPTANCE 2026-09-26
B11     ✅ CLOSED / USER-REPORTED ACCEPTANCE 2026-09-28
  B11-A ✅ CLOSED / PROVEN
  B11-B ✅ CLOSED / PROVEN
  B11-C ✅ CLOSED / PROVEN
  B11-D ✅ CLOSED / PROVEN
B13     ✅ CLOSED / USER-REPORTED ACCEPTANCE 2026-09-29
  B13-A ✅ CLOSED / PROVEN 2026-09-28
  B13-B ✅ CLOSED / PROVEN 2026-09-29
  B13-C ✅ CLOSED / PROVEN 2026-09-29
  B13-D ✅ CLOSED / USER-REPORTED ACCEPTANCE 2026-09-29
B12     ✅ CLOSED / QUALIFIED USER ACCEPTANCE 2026-09-30
  B12-A ✅ CLOSED / PROVEN 2026-09-29
  B12-B ✅ CLOSED / PROVEN 2026-09-29
  B12-C ✅ CLOSED / PROVEN 2026-09-29
  B12-D ✅ CLOSED / QUALIFIED USER ACCEPTANCE 2026-09-30
B14+B07 ◐ ACTIVE — USER-GUIDED PRODUCT / UI CONSOLIDATION
B15     ⬜ NOT STARTED
```

Execution order:

```text
B09 → B10 → B11 → B13-A → B13-B → B13-C → B13-D → B12 → B14+B07 → B15
```

---

# 2. Permanent semantic boundaries

```text
Person != Account != Actor
Activity != Event != Routine
Routine != Recurrence != Occurrence
Occurrence != Schedule
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
Resolution != deletion / rewrite of prior evidence
Responsibility != Participation
planned/intended != happened
Plan != Activity
Step != Activity
Dependency != hierarchy
ordering != dependency
decomposition != execution precedence
projection != canonical truth
current accepted state != latest row
MaterialState != mutable runtime object
idempotency key != Domain identity
Undo != history rewind
```

PostgreSQL is canonical authority. API, generated client, frontend, provider, solver and AI are projections/capabilities and may not create a second truth model.

---

# 3. Closed B10 chain

## B10-A — Actual

```text
Alembic  20260925_74
Topology 159|5|115|93|305|258|435
```

```text
Session END != Actual
absence of Actual = unknown
known realization_occurred=false != absence
current accepted realization != latest row
```

## B10-B — Outcome

```text
Alembic  20260925_78
Topology 163|5|119|93|317|268|440
facet: outcome.disposition
one stable Outcome per Actual
Outcome disposition pinned to exact Actual realization MaterialState
```

Never reintroduce the superseded `_75` vocabulary/result identity model.

## B10-C — Confirmation

```text
Alembic  20260925_79
Topology 167|5|123|93|329|279|446
facet: confirmation.attestation
identity = (Outcome disposition MaterialState, confirmer Person, purpose)
```

```text
Confirmation != Outcome
Confirmation != Authority / Verification / Decision
absence of Confirmation != false
Outcome correction does not transfer Confirmation
```

## B10-D — Reconciliation

Canonical identity:

```text
(outcome_disposition_material_state_ref, purpose_code)
```

Authority boundary:

```text
Outcome owner is the only resolver in B10-D
can confirm != can resolve
resolver identity is state data, not reconciliation identity
```

Persistence frontier:

```text
20260926_80

dante.outcome_reconciliation
dante.outcome_reconciliation_state
dante.outcome_reconciliation_evidence
dante.outcome_reconciliation_current_history
dante.outcome_reconciliation_operation
facet: outcome.reconciliation
```

Evidence pins exact Confirmation attestation MaterialStates. Confirmation correction does not reinterpret older reconciliation. Outcome correction does not transfer reconciliation.

## B10-E — Final integration + acceptance

Repository integration coverage:

```text
apps/backend/tests/integration/temporal/test_b10_e_whole_block.py
apps/web/src/features/temporal/timeline-truth-inspector.test.tsx
```

The user performed the integrated real-app walkthrough on 2026-09-26 and reported the chain working end-to-end.

Classification remains:

```text
B10-A..D = CLOSED / PROVEN
B10-E    = CLOSED / USER-REPORTED ACCEPTANCE
B10      = CLOSED
```

---

# 4. B11 closure record

B11 is historical closed scope. Do not describe any B11 walkthrough as pending.

B11-A completion-relative and anchor-stream-relative recurrence uses `_81`. B11-B bounded `actual_realization` Condition uses `_82`–`_85`. B11-C Schedule-relative self Reminder uses `_86`. The shared `_86` catalog probe measured `184|5|144|100|370|323|480|0|0|0` and the exact catalog tests passed after the CHECK-name and mapping-registration repairs.

B11-D integrated A/B/C. The full user-run local gate reported OpenAPI 7, PostgreSQL 14, deterministic generation 364, both typechecks, web 24 and final Ruff pass. The first real-app attempt exposed recurring Create `Senza Life Area` validation and Advanced Recurrence read transaction defects; both were repaired. The final isolated B11-D PostgreSQL rerun passed (`1 passed in 6.81s`) and the user reported the restarted integrated real-app walkthrough working.

Closure authority:

```text
docs/workstreams/timeline-temporal-operational-b11-closure-2026-09-28.md
```

B11 is `CLOSED / USER-REPORTED ACCEPTANCE`.

---

# 5. Closed gate — B13-A Work Structure Core

Scope authority:

```text
docs/workstreams/timeline-temporal-operational-b13-a-scope-2026-09-28.md
```

Immediate semantic target:

```text
canonical Plan
→ Plan-owned internal work decomposition
→ structural Step semantics
→ optional reference to a real Activity without identity collapse
→ explicit ordering separate from decomposition
→ deterministic accepted/current-state + history behavior
→ bounded author/read proof
```

Frozen boundaries:

```text
Plan != Activity
Step != Activity
Dependency != hierarchy
ordering != dependency
decomposition != execution precedence
```

Treat Step as internal work-structure semantics unless stronger current repository authority requires promotion to a universal root semantic identity. Do not create generic `work_item`, `node` or `edge` abstractions merely to defer the decision.

The B13-A discovery checkpoint resolved the implementation choices before `_87` DDL:

1. whether existing Plan identity/address primitives are sufficient or a dedicated Plan state family is required;
2. whether this gate is `Plan -> Step` only or needs recursive structural nesting;
3. the smallest semantic decomposition representation;
4. the ordering representation and correction/reordering history semantics;
5. how an optional Activity reference remains referential without identity collapse;
6. which existing identity/material/current-history primitives can be reused correctly;
7. database versus guarded-operation boundaries for cross-Plan, duplicate-link and cycle invariants;
8. the minimum public API/client/UI slice required for author/read proof.

The decision is flat `Plan -> Step`, reusing Plan NativeRef and giving Step an internal Plan-owned reference. Normalized revision snapshots hold membership, title, presentation order and optional same-self Activity link. Guarded functions enforce ownership, duplicate links and expected-current revision; current/history bindings remain explicit. `_88` repaired replay and catalog names; `_89` qualified the accepted-current update. OpenAPI, web/API typechecks, deterministic client generation and the UI test passed. The final user-run PostgreSQL/catalog suite passed **9 tests in 24.09s** at `_89`; B13-A is **closed**. Evidence: `timeline-temporal-operational-b13-a-closure-2026-09-28.md`.

B13-A non-goals:

```text
B13-B Dependency semantics
B13-C maximum Session / merge / spacing / preparation / recovery constraints
B12 solver/replanning
auto-Schedule
proposal acceptance semantics
AI scheduling authority
generic graph ontology
B07 UI consolidation
```

B13-A focused automated closure does not claim whole B13 real-app acceptance; that remains B13-D.

---

# 6. B13 continuation

B13-B is closed / proven at `_90`; its closure evidence is `timeline-temporal-operational-b13-b-closure-2026-09-29.md`. B13-C is closed / focused proof at `_92`: the user-run B13-A/B/C and exact Dictionary/catalog suite passed **13 tests in 29.16s** after the forward CHECK-name repair. The earlier web suite passed **11 tests**, deterministic client generation and both typechecks passed. See `timeline-temporal-operational-b13-c-closure-2026-09-29.md`. B13-D whole-block automated gate initially passed on the user's local worktree: generated check (383 files), both typechecks, web **12**, backend contract/unit **3**, PostgreSQL **14 in 44.24s**, and Ruff. Acceptance preparation exposed the UUID copy/paste Activity-link path; the direct card-to-linked-Step repair was published and used in the real app. Screenshots confirmed linked Record/Mix Steps and the `Actual avvenuto` Record → Mix Dependency in `sconosciuta`; after receiving the complete walkthrough the user reported “ok va chiudiamo”. B13-D/B13 are closed on user-reported acceptance, while the final seven-file web rerun and itemized remaining manual observations are not recorded. See `docs/workstreams/timeline-temporal-operational-b13-d-closure-2026-09-29.md`. See its scope, implementation checkpoint and gate documents. Do not merge Dependency truth into execution-structure constraints.

```text
B13-B — Qualified Dependencies
B13-C — Execution Structure Constraints
B13-D — Whole-block Integration / Proof / Acceptance
```

B13-B owns real dependency semantics. B13-C owns execution-structure constraints only where current Domain/Logical authority supports them. B13-D proves the complete B13 chain and real product behavior.

B12 block scope and B12-A diagnosis scope are published in `timeline-temporal-operational-b12-scope-2026-09-29.md` and `timeline-temporal-operational-b12-a-scope-2026-09-29.md`. B12-A is closed / proven on the user-run focused local gate at `db6a568`: generated 389, both typechecks, web 4, API contract 1, Ruff and PostgreSQL/catalog 11 passed in 26.14s. See `timeline-temporal-operational-b12-a-closure-2026-09-29.md`. Its read-only Home diagnosis distinguishes known hard violations, blocked prerequisites and unknown/unsupported bases without generating placements. B12-B is closed / proven on the user-run focused local gate: generated 393, both typechecks, web 3, backend 8, Ruff and PostgreSQL/catalog 11 passed in 24.63s; see `timeline-temporal-operational-b12-b-closure-2026-09-29.md`. B12-C is closed on the reported focused local gate: generated 397, both typechecks, web 4, Ruff, backend 9 and PostgreSQL 19 passed. See `timeline-temporal-operational-b12-c-closure-2026-09-29.md`. The original B12-D candidate passed the user-run gate on `75891447` (generated 397, web 11, backend 9, PostgreSQL/catalog 20, both typechecks and Ruff). The hard-rule and Movement Policy click path was repaired, and placement-zone authoring was moved to Colloca. The user accepted qualified B12 closure; the affected automated rerun and itemized real-app observations are unreported. See `timeline-temporal-operational-b12-closure-2026-09-30.md` and `timeline-temporal-operational-b12-d-gate-2026-09-29.md`. Replanning/solver behavior consumes canonical structure/dependency truth.

---

# 7. Collaboration discipline

- user runs tests locally; assistant does not use CI/GitHub Actions
- push coherent checkpoints frequently with `[skip ci]`
- published migrations are immutable; persistence fixes are forward-only
- generated API client comes only from repository generator
- PostgreSQL remains canonical truth
- distinguish proven persistence/domain semantics from user-reported product acceptance
- repository HEAD is source of truth before any write

## B14-U6 continuation, 2026-10-03

Branch `feature/timeline-temporal-operational` implementation checkpoint `64916cf2882323b7e4dd29ac5e9e42b551565273` follows the `_101` manual Session and execution-policy CHECK-name repair at `c7fa7209faa6e36b8b1a3c21ae52c68e73c6e7c6`. The user-run `_100` gate reported 12 passed and two exact-catalog failures caused by `_97` CHECK naming expansion. The `_101` forward rename is published but not yet PostgreSQL-proven. Follow the U6 candidate checkpoint for scope, verification and open acceptance.

The subsequent `_101` user gate reported 8 passed and two catalog test-code/Dictionary reference failures, repaired at `f453c2e82abeee9fa03331db265513343cda01ac`; the rerun is unreported. `_102` at `16fe795e68a3c7662b3baf764596db4176043018` persists exact Schedule envelope/planned role and order and exposes it on readback. Its PostgreSQL gate is pending. No real-stack U6 acceptance is recorded.
