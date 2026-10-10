# Timeline / Temporal-Operational — Live Execution Ledger

## Current Session panel candidate

The new Timeline control is published on this branch; refer to `docs/frontend/home/timeline-session-panel.md` and the exact scope at `docs/workstreams/timeline-session-panel-scope.md`. Candidate migration `_135` permits an explicit untimed planned start and exposes two owner-scoped read capabilities. PostgreSQL, browser and real-app gates await execution; prior B14 work remains as recorded below.

- **Status:** CURRENT LIVE STATE — U6 continuation reconciled 2026-10-03
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
- **B12 closure:** `docs/workstreams/timeline-temporal-operational-b12-closure-2026-09-30.md`
- **B14/B07 working ledger:** `docs/workstreams/timeline-temporal-operational-b14-ui-consolidation-2026-09-30.md`
- **B13-D scope:** `docs/workstreams/timeline-temporal-operational-b13-d-scope-2026-09-29.md`
- **B13-D candidate gate:** `docs/workstreams/timeline-temporal-operational-b13-d-gate-2026-09-29.md`
- **B13-D closure evidence:** `docs/workstreams/timeline-temporal-operational-b13-d-closure-2026-09-29.md`
- **DB overlay:** `docs/database/timeline-temporal-operational.md`
- **Current persistence source frontier:** `20260929_93` (B12-C focused local proof)
- **Reported current catalog topology:** `_93` / `196|5|155|100|397|344|497|0|0|0` (focused local gate)
- **Completed functional frontier:** B12 ✅ CLOSED / qualified user-reported acceptance 2026-09-30
- **Current implementation cursor:** B12-D and B12 closed on qualified user-reported acceptance; B14/B07 active as one user-guided product/UI cycle; U1 Create-entry candidate is ready for user visual proof; B13-D post-repair web rerun unreported
- **U6 cursor:** Candidate `_103` adds named future planned Schedule rows and corrects Advanced Create placement and controls after the user's real-app screenshots. The `_102` atomic/catalog gate passed 9 PostgreSQL tests at `39c846d0`; the atomic B08 minimum test passed (1) at `8b9e9158`. The `_103` PostgreSQL/catalog gate and corrected real-app acceptance are pending. Follow `timeline-temporal-operational-b14-u6-candidate-2026-10-02.md`.
- **Activity interval cursor (2026-10-05):** Candidate `_106` adds separate Activity `interval` roles and authoring while preserving `planned` for future Sessions; Timeline projects distinct intervals and hides the technical envelope for these Activities. Product decision: `docs/domain/decisions/activity-intervals-and-sessions-v2.md`. Local migration/build and real-app acceptance pending; direct coordinated interval replanning remains open.
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
B12 Replanning / Conflict / Solver                ✅ CLOSED / QUALIFIED USER ACCEPTANCE 2026-09-30
  B12-A Current-truth conflict diagnosis           ✅ CLOSED / PROVEN 2026-09-29
  B12-B Bounded candidate generation / solver      ✅ CLOSED / PROVEN 2026-09-29
  B12-C Review / governed admission                ✅ CLOSED / PROVEN 2026-09-29
  B12-D Integration / product acceptance           ✅ CLOSED / QUALIFIED USER ACCEPTANCE 2026-09-30
B14 + B07 Product / UI Consolidation              ◐ ACTIVE — USER-GUIDED
B15 Whole Vertical Closure                        ⬜
```

Sequence authority:

```text
B09 → B10 → B11 → B13-A → B13-B → B13-C → B13-D → B12 → B14+B07 → B15
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

Block and B12-A scopes are in `timeline-temporal-operational-b12-scope-2026-09-29.md` and `timeline-temporal-operational-b12-a-scope-2026-09-29.md`. B12-A is closed / proven: generated 389, both typechecks, web 4, API contract 1, Ruff, PostgreSQL/catalog 11 passed in 26.14s in the user's worktree; see `timeline-temporal-operational-b12-a-closure-2026-09-29.md`. B12-B is closed / proven on the user-run focused local gate: generated 393, both typechecks, web 3, backend 8, Ruff and PostgreSQL/catalog 11 passed in 24.63s; see `timeline-temporal-operational-b12-b-closure-2026-09-29.md`. B12-C is closed on the reported focused local gate: generated 397, both typechecks, web 4, Ruff, backend 9 and PostgreSQL 19 passed. See `timeline-temporal-operational-b12-c-closure-2026-09-29.md`. B12-D scope was approved; the original user-run gate passed on `75891447` (web 11, backend 9, PostgreSQL/catalog 20, generated 397, both typechecks and Ruff). The affected automated rerun and itemized real-app observations are unreported; the user accepted qualified closure. See `timeline-temporal-operational-b12-closure-2026-09-30.md`; proof and commands are in `timeline-temporal-operational-b12-d-implementation-2026-09-29.md` and `timeline-temporal-operational-b12-d-gate-2026-09-29.md`. The user accepted B12 closure without itemized final real-app proof; the gap is recorded in the closure. Proposal != accepted Schedule; solver UNKNOWN != INFEASIBLE; AI != scheduling authority.

## B14 + B07 — user-guided product and UI consolidation

The user directs a live list of changes while using the product. Each item can modify UI placement, interaction behavior and the owning rule or persistence layer. The Create completeness rule remains active: every editable field must be canonically supported/proven, truthfully handed off, presentation-only, or hidden. The active ledger is `timeline-temporal-operational-b14-ui-consolidation-2026-09-30.md`.

## B15 — Whole Vertical Closure

Final whole-vertical reconciliation, regressions and dogfood after all functional/create/UI blocks are complete.

## 2026-10-06 — B14 placement lock candidate

The Activity Create placement lock candidate is at `_110` / `9d2b6130` with Timeline reconciliation follow-up `84161fa5`. It separates a persisted user lock from B04 automatic movement policy and guards canonical Schedule placement history. This is **candidate / unproven**: user-run PostgreSQL, OpenAPI/generated-client, web and real-app gates are pending. Complete recurring-Activity template inheritance (intervals, planned Sessions, Sub-Activities, Reminder, outcome review, protection) is approved but **not implemented**; the explicit Create guard remains. Follow the current B14 recurring authoring contract for the product boundary.


## 2026-10-06 — B14 recurring Activity current candidate

Current Create/Timeline candidate now carries full per-Occurrence Activity
template inheritance (intervals, planned Sessions, Sub-Activities, Session
settings, outcome review, Reminder lead and placement protection) and restores
Life Area/color parity with one-off Activity Create. The virtual unassigned
Timeline bucket is presentation-only and non-authorable. Timeline organization
refresh is sequenced after authoritative read/checkpoint so newly materialized
Activity assignments and colors are visible. Root start-time edits preserve
duration and cannot silently manufacture an overnight first interval.

Status remains **candidate / unproven**. Event recurrence parity is a subsequent
shared-infrastructure pass; Activity-only structure semantics are not Event
semantics.

## 2026-10-06 — Create closure mini-roadmap

Use `timeline-temporal-operational-create-closure-mini-roadmap-2026-10-06.md` as the current product/UI execution cursor for Activity/Event Create. It does not reopen B01-B13 closures; it selects and composes already-proven capabilities, plus one new bounded Objectives vertical using accepted Criterion/Evaluation/Observation semantics.

## 2026-10-06 — Verification rail candidate

The B14/B07 Today rail candidate at Alembic `20261006_117` extends the shared lower edge of Timeline, Context Rail and Quick Create by 48 px and derives pending Reality/Objective/B10 Reconciliation cards from canonical state. Activity review requires a completed bounded Session; Event and Event Occurrence review uses the accepted placement end in the person's effective IANA zone, including date spans. The Reality response carries the exact Session/timing basis; Objective responses write Observation/Evaluation through the existing owner API. The branch candidate is unproven pending user-run local migration, generated-client/typecheck, focused PostgreSQL/web and real-app acceptance. The active details and gate are in `timeline-temporal-operational-b14-ui-consolidation-2026-09-30.md`.

## 2026-10-08 — Active B14 Inspector / Edit / Duplicate cursor

**This append-only checkpoint supersedes older M0/U6/B14 candidate status
paragraphs above where newer local evidence is available.** Live branch
baseline at reconciliation: `39e8ab96`. The authoritative, itemized status
and newest user-approved global edit scope are at the end of
`timeline-temporal-operational-b14-ui-consolidation-2026-09-30.md`.

Focus: Activity Inspector/editor is partially implemented and **not**
whole-block accepted. Coordinated Activity interval add/remove and planned
Session replan is focused-gate green (Ruff, 4 unit, 15 PostgreSQL,
15 web, generated/client proof; generated files published in `c22f04ae`).
New post-create Activity Objective ADD is web-gate green (typecheck,
17 Vitest). Remaining order: **M1** selected-instance edit scope
`Solo questa / Questa e le prossime`, **M2** versioned Objective
corrections and no-delete past facts, **M3** Activity residual fields
(existing planned Session names, Life Area unassign, retirement guard),
**M4** faithful Activity/Event duplication and Event Inspector parity,
**M5** user real-stack acceptance / B15 whole vertical.

A past selected instance is ALWAYS included, even when following future
instances are also selected; **other past instances are never rewritten**.
No unanchored `Le prossime` scope and no silent rewrite of current
Objective results. B14+B07 stay ACTIVE; B15 stays OPEN.

## 2026-10-08 — M1-A green / M1-B read-only inventory candidate

M1-A: focused Ruff PASS / 18 unit PASS reported by the user.
M1-B: forward-only `_122`, new self-scoped 10k bounded
materialized-Occurrence inventory function + GET read API and
PostgreSQL/catalog tests. Exact Dictionary now expects 197 routines,
unchanged 231 tables, 5 views, 103 triggers, 471 indexes, 405 FK,
572 CHECK. Status **candidate / no user local gate yet**.
Returned inventory is materialized-only, not permission to apply.
M1-C transactional CAS/scope apply, Activity/Event binding,
overrides and future source-template revision remain OPEN. Details
and user gate in the B14 UI consolidation ledger. No CI.

## 2026-10-08 — M1 _123 atomic metadata edit candidate

_122 user local green: Ruff 0, PostgreSQL 10/10, client generation/
deterministic 484, API/Web typechecks 0. New _123 source-wide
immutable revision, scope/past isolation, conflict guarded CAS,
readback in Activity and Event Timeline, Activity materialization,
Activity profile save UI and shared API are a candidate pending ONE
whole local gate. Candidate Dictionary `232|5|202|103|473|408|576`.
Global scope is `Solo questa` or `Questa e le prossime`, clicked
always included, other past never changed. Application to Objective,
Session/Scaletta, Schedule and remaining independently-governed
settings remains open under M2/M3/M4, not implicitly implemented
by the metadata endpoint.

## 2026-10-08 — M1 _124 one-off Activity read correction

The _123 unified gate returned 18 unit PASS, 21 Web PASS,
generation/check 489 PASS, API/Web typecheck PASS, and
4 PostgreSQL Activity Inspector/read failures plus 2 Ruff I001.
_124 is a forward repair with deterministic PL/pgSQL NULL
Occurrence guard in `get_self_activity_profile`, CASE guard
in Activity Timeline, import sort corrections and regression
test. Dictionary/catalog stays 232/5/202/103/473/408/576.
_124 local gate **PENDING**. Do not claim M1 whole domain or
B14 closed.

## 2026-10-08 — M1 focused technical closure on published client

After user rerun of _124: `RUFF=0`, `POSTGRES=0`, `GENERATED_CHECK=0`, `API_TYPECHECK=0`, `WEB_TYPECHECK=0`, `VITEST=0`. User published the nine generated API files in `55a017b9`, with clean `git status`. **M1 general-metadata recurrence edit vertical focused-gate CLOSED.** Preserve B06/B11 existing functional authority. _124 catalog 232 tables, 5 views, 202 functions, 103 triggers, 473 indexes, 408 FK, 576 CHECK. Final visual dogfood still B14 M5/B15. M2 Objective same-logical-identity definition/result correction and historically valid audit is OPEN; M3 remaining field/domain edits, M4 Event inspector/duplicate and M5/B15 also OPEN.

## 2026-10-08 — M2 bounded Objective edit+reality correction candidate

M1 closed only for recurring general metadata on user green gate `55a017b9`; B14 overall active. Two new forward-only migrations `20261008_125` and `20261008_126` implement same-identity Objective definition revisions, immutable result correction and deterministic evaluation, and accepted selected/future Objective definition inheritance for canonically template-generated recurring occurrences. Strict owner/CAS, source-specific idempotency, protected future facts and rollback of an entire conflicting series apply. New Activity UI controls cover definition edit, result correction and trusted Objective series scope. Existing Activity/Event Objective create/read/record are reused. No manual-result copying or past deletion. Catalog target **234/5/207/103/477/414/586**; new local whole gate **PENDING**, not claimed green. M3–M5/B15 still open.

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

## 2026-10-08 — Current cursor after locally GREEN M2

**M2 is CLOSED at focused automated technical-proof level**, superseding prior candidate/failed-gate entries. The user-reported whole M2 gate ended `SYNTAX=0 RUFF=0 POSTGRES=0 GENERATE=0 GENERATED_CHECK=0 API_TYPECHECK=0 WEB_TYPECHECK=0 VITEST=0`; the generated client was pushed in `09dc26f9`, verified as remote HEAD. Objective logical identity/current accepted corrected value, append-only versions, factual Observation/Evaluation correction, deterministic assessment, Routine and Event generated Objective scopes are part of this proven bounded vertical. No original historical facts are deleted; future unobserved instances do not acquire manufactured results.

M1 recurring general-metadata remains closed; **M3 is next and OPEN** (existing planned Session title edit without historical identity replacement; null/unassign primary Life Area; missing temporal/settings editing paths; Schedule/Reminder/policy boundaries; history-safe retirement). **M4 OPEN** faithful duplicate and Event Inspector parity. **M5/B15 OPEN** true user visual/real-stack full-vertical acceptance, catalog/ACL/negative invariants. No fabricated acceptance and no GitHub CI.

## 2026-10-08 — M3 post-create Activity residual edit candidate on _127

**CURRENT STATUS: IMPLEMENTED CANDIDATE; THE USER HAS NOT RUN THE _127 LOCAL GATE.** Do not call M3 proven or B14/B15 closed. Following M2 user-green gate and generated publication `09dc26f9`, forward-only `20261008_127` adds three post-create behaviors:
- Actor-local Activity **and Event primary Life Area explicit unassignment**: four existing `life_area_ref` columns (current row + immutable operation receipts) accept NULL. The existing guarded assign functions retain self ownership, expected-revision CAS, durable operation receipt, replay/reuse rejection and monotonic revision after unassignment/reassignment; `list_self_unassigned_life_area_items` now recognizes explicitly null assignments. API/request/response/ORM, Activity editor and remote source accept NULL. No fake Life Area is created and no row deletion resets revision.
- Existing **planned Activity Session display name** can be revised through the same `activity_schedule_role` Schedule identity, using a new self-scoped `revise_self_planned_session_name` function (expected-name compare, idempotent same-target replay, validation, actor-ownership and retired guard). This is **presentation metadata**, not actual Session timing or schedule-history mutation. API, remote client, Activity editor and tests added; no history of prior *label values* is modeled in this candidate, so do not misrepresent it as a full append-only label ledger or a recurring template-wide edit.
- **Activity retirement historical-truth veto**: the existing guarded `retire_self_activity` function now rejects deletion/retirement whenever a Session (even ended), accepted Actual or recorded Objective observation/evaluation exists. The existing open-Session veto and retirement operation replay remain. Inspector explains the restriction and shows a conflict for recorded truth. Corrections to historical data continue through their own domain-owned edit endpoints.

Candidate DB topology `234 tables / 5 views / 208 routines / 103 triggers / 477 indexes / 414 FKs / 586 CHECK` at `20261008_127`; ORM, Dictionary entries, scope and exact catalog test expectations updated. The additional routine is the planned label capability; nullable columns create no new tables/constraints. Backend PostgreSQL test `test_b14_m3_residual_editor.py` checks Life Area null CAS/replay/actor isolation, Event parity, planned Schedule identity and recorded Session retirement veto; focused Web remote-contract regression added.

**Outstanding verification and scope:** no automated _127 proof yet; migrations/DB exact catalog, legacy B05/B14 and M2 regression, API generation/determinism, Web/API-client typecheck and Vitest must pass on the user local worktree before publishing canonical generated files. Remaining broad M3 questions include recurrence-template propagation for domain-owned Session name/Life Area, non-supported temporal-form UX and acceptance of historical label edits; do not claim these solved by selected-only mutations. Preserve `Solo questa`/`Questa e le prossime` for supported recurring edits with clicked included. After honest M3 gating/reconciliation, M4 faithful Activity/Event Duplica and Event Inspector and M5/B15 full product acceptance remain. No GitHub Actions or CI.

## 2026-10-08 14:42 — M3 second local gate: 21 PASS / 5 FAIL (repairs pending user verification)

The user pulled `c7206a10` and executed the M3 combined recheck; `RUFF=1` (test import ordering), `POSTGRES=1` with **21 passed, 5 failed**, while `GENERATE`, `GENERATED_CHECK`, `API_TYPECHECK`, `WEB_TYPECHECK` and `VITEST` were previously green. The failed tests were M3 Activity null Life Area, M3 Event null Life Area, legacy B05 primary reassignment, M2 Event Objective definition (which uses a scheduled Event with an assigned Life Area), and exact database cross-representation catalog. The displayed log was only `tail -n 100`, so full individual test tracebacks were not included; log path on user's WSL: `/tmp/dante-m3-recheck.LM4nCX/POSTGRES.log`.

Code review established that `20261008_127`'s `assign_self_{activity,event}_life_area` functions used unqualified `WHERE life_area_ref=requested_life_area_ref` although `life_area_ref` is also a PL/pgSQL output variable under `#variable_conflict error`. The new SQL now explicitly uses `target.life_area_ref`, `target.self_person_ref`, `target.archived` (commit `39e11193`). The B05 legacy and M2 scheduled Event tests both call these replacement Life Area functions, explaining their shared likely failure path. Ruff import placement corrected in `test_b14_m3_residual_editor.py` (commit `7ad57b87`). Exact-catalog test stale values were updated to **208 routines**, **447 standalone entries**, and to expect `B14-M3-RESIDUAL-EDITOR` in completed stages (commit `56a6e4de`). The physical topology expected remains **234 tables / 5 views / 208 routines / 103 triggers / 477 indexes / 414 FKs / 586 CHECK**.

**Latest state: _127 M3 implementation candidate, NOT verified green.** Recheck focused Ruff and PostgreSQL, then the full local gate before generated-client publication. User's uncommitted OpenAPI/Orval outputs must be preserved (do not reset/overwrite manually); no Actions or CI. If additional failure remains, collect complete pytest failure traceback rather than another `tail -n 100` summary. M1/M2 remain closed and published; M4/M5/B15 still open.

## 2026-10-08 — M3 _127 green technical subvertical (supersedes previous red status)

The user's complete M3 gate returned eight zeros (`SYNTAX/RUFF/POSTGRES/GENERATE/GENERATED_CHECK/API_TYPECHECK/WEB_TYPECHECK/VITEST`). Generated API client pushed `6fdda05f`, now remote HEAD. _127 canonical model includes nullable primary Life Area with monotonic assignment revisions, unchanged-ID planned Session label corrections, and retirement refusal when Activity recorded facts exist; B05, B14, M2 regressions and exact physical/Dictionary catalog were within passing PostgreSQL suite. Catalog 234/5/208/103/477/414/586, standalone total 447. **M3-A technically accepted (focused automated), not final M3-wide approval.**

Remaining M3 frontier is source/template propagation and temporal edit-surface parity: current new Life Area/planned Session name edits permit only selected-instance changes and explicitly reject selected+following in the UI; broader recurrence behavior needs authoritative domain design and test. Existing editing paths must be inventoried to avoid duplicate behavior. M4 Event inspector/duplicate, M5 UI dogfood and B15 remain open. No CI.

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

## 2026-10-08 — M4 integrated technical gate accepted

The user reran `bash tooling/verify-b14-m4-local.sh` after the consolidated repair `06e4b7a7`: all ten stages (`PULL`, `SYNTAX`, `RUFF`, `UNIT`, `POSTGRES`, `GENERATE`, `GENERATED_CHECK`, `API_TYPECHECK`, `WEB_TYPECHECK`, `VITEST`) returned zero. Evidence `/tmp/dante-m4-whole.5cpYvA`. The script committed and pushed seven verified generated client files as `77968de6`; GitHub branch readback confirmed. M4's implemented Inspector/edit and supported duplication technical paths are green; real-app M5 visual acceptance, guarded unsupported duplication and B14 following-source parity debt remain explicit. Next: one integrated M5 click-through, collect visible defects and then review B15 closure. No repeat M4 micro-gates or CI.

## 2026-10-09 — M5 Session editor, validation and Objective Inspector repair candidate

User real-app screenshots exposed three defects after the green M4 technical gate: Edit's planned-Session clock controls inherited broad Timeline input/button styling, Create showed an English range paragraph with a misplaced section-wide red outline, and entering a numeric Objective observation in Inspector opened the error boundary. The Web candidate excludes the shared Session clock controls from those broad editor selectors, removes the Edit-only offset, localizes the bounded structure message, and targets the invalid Session's date/time row. Numeric Objective input now snapshots the DOM value before React's deferred state updater. A dedicated Inspector regression records `8 km`; targeted Create validation checks outside-range and reversed Session times, and a form test confirms the inline Italian error and precise invalid row.

Coding-workspace proof: Web typecheck, changed runtime/new-test ESLint and four focused Vitest files (54 tests) pass. The older Create entry test file has pre-existing ESLint violations and was excluded from this lint command; its tests are included. No user WSL run, real-app visual proof, or PostgreSQL proof is claimed for this candidate. Alembic `_129/_130` untimed planned-Session persistence and Docker-assigned acceptance port are already on branch HEAD `ec648022`, but their user-local PostgreSQL/catalog gate remains pending. M4 stays technically green, M5 remains open, and B15 parity debt for `Questa e le prossime` Life Area/planned Session labels remains unchanged. Run one consolidated affected gate after publication; no CI or extra M4 gate.

## 2026-10-09 — User-local M5/untimed acceptance gate, Ruff repair pending

After pulling `b1b74c6d`, the user's WSL gate reported 13/13 PostgreSQL integration and exact-catalog tests passing on `_130`, Web typecheck passing, and 54/54 focused Vitest tests passing. Ruff alone reported four style violations in `test_b14_u2_authoring.py`: literal dict, compound assertion, and two intentionally naive datetimes for floating-local placement. The focused repair preserves test semantics and marks those two datetimes with `DTZ001` exemptions. This repair is not yet user-local Ruff verified; no second PostgreSQL/Web run is needed solely for this test-style change. The Create entry test also emitted an existing React cross-component setState warning while all tests passed; track separately from this blocking Ruff gate. M5 visual acceptance remains open; B14 source-following Life Area/planned Session naming remains guarded.

## 2026-10-09 — M5/untimed focused technical gate GREEN

The user pulled `0754ba1e` in WSL and reran the exact focused Ruff selection; **All checks passed**. The preceding run on `b1b74c6d` had already passed 13/13 PostgreSQL integration and exact-catalog tests, Web typecheck, and 54/54 focused Vitest tests. The intervening commit changed only test lint/syntax and documentation, so this completes the bounded technical gate without repeating green PostgreSQL/Web checks. The React cross-component update warning seen in an existing Create-entry test remains a non-failing follow-up observation. Next: the user inspects planned Session clock layout in Activity Edit, the localized precise range validation in Create, and numeric Objective input/recording in Inspector in the real app. M5 visual acceptance and B14 source-following `Questa e le prossime` parity debt remain open; no CI/Actions.

## 2026-10-09 — M5 Activity Edit follow-up candidate

The current candidate includes `_132` planned Session retirement distinct from removing its time, the first placement-lock CAS fix, Session control cache invalidation, new Life Area creation in Edit, Inspector title controls, and Activity Edit layout corrections. It requires a single user-local migration/backend/Web gate and real UI acceptance. The renewed Objective crash needs the actual `Show Error` trace; do not claim it resolved. M5 and B15 remain open; no CI.

### 2026-10-09 — M5 generated contract and whole-block gate

Source generation now covers `_129`–`_132` OpenAPI/Orval shapes, including `delete_planned_sessions`, and is deterministic in the coding workspace. The consolidated user-local gate is `bash tooling/verify-b14-m5-local.sh`; it includes focused PostgreSQL/catalog, Objective, Activity Edit and Web checks. No PostgreSQL or real-app PASS is claimed. The Objective white-page recurrence remains unconfirmed without the boundary detail. M5/B15 remain open.

### 2026-10-09 — Activity Edit planned time and Timeline runtime candidate

The Activity Edit `Orario` switch now adds or withdraws a planned Session time through coordinated preview/apply. A new guarded `_131` placement capability preserves the Schedule identity when timing an unplaced planned row, including after a previous unschedule; the edit snapshot keeps untimed planned rows visible. New planned rows may be saved without a time. Core Edit requests have bounded database and web timeouts with an Italian retry error instead of an endless spinner. Timeline Activity cards show a combined Play/Pausa button and Stop. Workspace web typecheck and 40/40 focused Vitest tests pass; Python syntax and diff checks pass. PostgreSQL/Ruff and real-app acceptance await the user's local gate. No CI/Actions.

## 2026-10-09 — M5 PostgreSQL gate failures repaired, user-local rerun pending

After the candidate commit `2a30359`, the user-local `bash tooling/verify-b14-m5-local.sh` run reported green `PULL`, `SYNTAX`, `RUFF`, `UNIT`, `GENERATE`, `GENERATED_CHECK`, `API_TYPECHECK`, `WEB_TYPECHECK`, and `VITEST` (75 focused Web tests). `POSTGRES` remained red for two verified source defects: `activity_replan_api.py` zipped all free planned-Schedule order slots against fewer new Sessions with `strict=True`; `test_database_current_catalog.py` still expected pre-_131/_132 Dictionary totals and omitted their two completed-stage markers. Both are fixed on the same feature branch by commits `604459a9` and `677ea8d1`, respectively. The first change takes exactly as many free slots as newly requested planned Sessions; the second aligns exact assertions to Alembic `20261009_132` and Dictionary `236 tables / 5 views / 214 routines / 103 triggers / 482 indexes / 420 FKs / 589 CHECK`, including `B14-PLANNED-SESSION-TIME-EDIT` and `B14-M5-PLANNED-RETIREMENT`. No database migration or generated client artifacts were modified during this repair. The `_131` `DECLARE prior record;` correction was already present on the remote branch.

**Status: REPAIR PUBLISHED / POSTGRES RERUN PENDING; NOT GREEN, NOT M5 CLOSED.** Next: the user pulls the latest feature branch and reruns the single affected PostgreSQL selection from `tooling/verify-b14-m5-local.sh` (Activity replan, U2 authoring, Activity edit snapshot, M2 objectives, current catalogs), plus the selected Ruff file check if desired. Preserve any local worktree edits before pulling; never reset or overwrite user changes. If PostgreSQL is green, accept the consolidated M5 technical candidate without rerunning unrelated previously green Web/API gates, then complete real-app visual/keyboard acceptance (including the unresolved Objective white-page report if reproducible). B14 source-following `Questa e le prossime` for Life Area and planned-Session names remains guarded and not implemented; B15 remains open. No CI/Actions.


## 2026-10-09 — M5 Objective editor one-save candidate; local verification required

The user requested direct editing of existing Objectives by expanding their row, a single **Salva modifiche** after adding/changing/removing Objectives (no intermediate confirmation), and an **×** removal affordance per row. The branch candidate implements these in `apps/web/src/features/home/ui/timeline/activity-objective-row.tsx`, `activity-edit-panel.tsx` and their style/tests. The previously separate Objective definition actions were folded into Activity Edit submit. Draft additions have no server side effects until the final Save; removal is staged and undoable. Recorded-result correction remains a separate factual-history operation and was not silently rewritten as a definition edit.

The new **Objective-only** `PUT /api/v1/temporal/activities/{subject_ref}/objective-edits` API uses a *single SERIALIZABLE database transaction* to apply all newly authored, revised and retired Objective definitions. It uses existing owner-scoped Objective create/revision/source-policy functions; the new forward-only `20261009_133_b14_objective_retirement.py` adds a retirement tombstone and an owner-scoped function with definition CAS, replay and veto of any recorded Observation/Evaluation or template-generated recurring Objective. Retired Objectives remain in historical storage, but active read/definition capabilities no longer return them. The database Dictionary, SQLAlchemy mapping and exact-catalog expectations have been reconciled to `20261009_133`: **236 tables / 5 views / 215 routines / 103 triggers / 482 indexes / 420 FKs / 589 CHECK**, standalone **456**. New Objective batch command and precise veto response are in `reality_objective_api.py`.

The remote Web Objective batch call has a bounded 20s timeout, stable per-row operation IDs and retained CAS basis for retries. The general Activity Save visually drives the Objective batch without extra buttons. **Important domain boundary:** the batch is atomic *among Objective changes*; other domain-owned edits on the same Activity continue using their established guarded commands and are **not a single cross-domain database transaction**. Do not claim a global atomic Activity save. Unsupported source-wide deletion is refused, and a recorded Objective cannot be erased. Existing selected/following Objective definition scopes remain available only with verified template provenance; the unrelated Life Area/planned Session following-source parity debt remains open.

**Current status: CODE/TEST/DOCUMENTATION CANDIDATE ONLY; ZERO NEW USER-LOCAL PROOF.** The preceding `_132` M5 PostgreSQL selection passed **26/26** in the user's WSL, but this new `_133` candidate is not covered by those 26 tests. Run **one complete local gate** via `bash tooling/verify-b14-m5-objectives-local.sh` on `~/projects/dante` (Ruff, syntax, PostgreSQL new Objective batch/history and existing regression/catalog, deterministic generated API, API/Web typechecks and focused Vitest). The script does not commit/push and does not trigger CI/Actions. A new OpenAPI/Orval client artifact is expected from `pnpm api:generate` and must be published only after a green gate; never hand-edit generated files. Follow with real-app visual/keyboard acceptance including the earlier Objective white-page report. Neither M5 nor B15 is closed.


### 2026-10-09 — M5 Objective editor first user-local gate: PostgreSQL GREEN / Web parse + Ruff repairs published

The user's first `bash tooling/verify-b14-m5-objectives-local.sh` run returned **PULL=0, SYNTAX=0, POSTGRES=0, GENERATE=0, API_TYPECHECK=0** at Alembic `20261009_133` (covering new Objective batch/retirement tests, prior M2, Activity edit snapshot and exact Dictionary/catalog). **RUFF=1** for exactly two reported issues: `RUF001` right-curly apostrophe in the new backend error text and `PT018` combined tombstone assertion in the new test. **GENERATED_CHECK=1, WEB_TYPECHECK=2 and VITEST=1** because the Activity editor had one unmatched JSX `</div>` after the Objective correction block (at the formerly reported line 1245); Vite/OXC could not parse that source. The separate unaffected Web test files passed 12 tests. User log `/tmp/dante-m5-objectives.CAzpn9`.

The three verified source failures have been corrected directly on the feature branch: remove exactly the orphan closing `</div>`, replace the ambiguous apostrophe with a straight apostrophe and split the tombstone test assertion. **These repairs have no new PostgreSQL business/schema changes** and do not justify repeating the already passing  `_133` PostgreSQL gate. No Web PASS is claimed: perform one focused **Ruff + generated/check + Web typecheck + focused Vitest** local rerun after pull, then close the technical gate only if green and publish the generated API client separately. The first generation modified two preexisting files and created four new Orval model files locally; preserve these user files and never reset/clean the worktree. Real-app acceptance/old Objective error boundary, M5 and B15 remain open; no CI.

### 2026-10-09 — M5 Objective editor second user-local gate: Web/TS tests repair published

The user pulled `b213aa7d` and ran the **focused** follow-up. **Ruff PASS**; **generated:check PASS** (OpenAPI/Orval generated files deterministic, 508 files); Vite production build PASS (chunk-size warning only). Web typecheck reported precisely **three TS2552 references** to `objective` in two new tests under the `Activity Inspector` suite: the fixture had been declared inside the preceding `Objective correction in Activity Editor` suite. Focused Vitest reported **45 passed / 3 failed**: two fixture-scope ReferenceErrors, plus an accessible-button-name mismatch (UI is `＋ Aggiungi obiettivo` while the test required exactly `Aggiungi obiettivo`). The untouched Web settings/control tests passed.

Commit `330fc5a0` moves the shared Objective fixture to module scope and adjusts the add-button query to match the visible accessible name. These are **test-only** changes; no backend/migration/business code altered. **Awaiting one focused user-local rerun of Web typecheck and focused Vitest; do not repeat already-green PostgreSQL (previous gate), Ruff or generated:check.** The generated client files remain only in the user's local worktree, pending publication; never remove them with reset/clean. Full B14 M5 and B15 closure remains dependent on real-app acceptance and previously documented scope parity.

### 2026-10-09 — Objective editor M5 focused technical gate GREEN (user WSL)

The user pulled `0d2c71c2` and reran the exact focused Web gate. **Web typecheck: PASS (exit 0); focused Vitest: 3/3 files, 48/48 tests PASS.** The preceding user-local gates on the same `_133` Objective editor candidate already proved PostgreSQL integration/catalog PASS, Ruff PASS, API typecheck PASS, and deterministic OpenAPI/Orval `generated:check` PASS (508 files). The test-only repairs `330fc5a0` do not alter backend/domain behavior. This **closes the bounded Objective-editor technical gate**; do not rerun completed PostgreSQL/Ruff/TypeScript/Vitest checks just to repeat the same evidence.

**Publication still outstanding:** Generated API artifacts exist in the user's WSL worktree, not on GitHub: tracked modifications to `packages/api-client/openapi/dante-v1.openapi.json`, `packages/api-client/src/generated/dante.ts`, `packages/api-client/src/generated/model/index.ts`; new `packages/api-client/src/generated/model/{activityObjectiveBatchCommand,objectiveBatchRetirement,objectiveBatchRevision,temporalApplyActivityObjectiveEditsBody}.zod.ts`. The client is deterministically source-generated and already checked. Publish **exactly these seven files** without resetting/cleaning any local worktree data. The GitHub connector cannot access the user's uncommitted WSL bytes. No CI. Then real-app acceptance of Objective editing (inline expansion, new, edit, X/remove/undo, Save, error/retry) remains; larger M5/B15 closure and recurring source-following parity debts remain open.


### 2026-10-09 — M5 Objective API generated artifacts PUBLISHED

The user completed the exact seven-file Orval/OpenAPI publication on the feature branch in commit `f950d22f7d51d432a02b7527dc6ee322fe06d3de` (`chore(api-client): publish B14 M5 Objective API [skip ci]`). GitHub comparison against `c44e9a0b` confirms **one commit ahead, exactly seven generated API client files**, with no other changes in that publication. The user-local command ended with no `git status --short` entries, consistent with a clean worktree at that point. **The Objective editor bounded technical gate is green, and source-generated API publication is complete.** No more migrations, Ruff, PostgreSQL, code generation, typechecks or repeated Vitest are required solely for this accepted technical gate. Next: inspect the running app and manually validate new Objective rows, direct editing, removal/reinstatement, Save, recorded-history veto and error feedback; report concrete defects before marking M5 visually accepted. The remaining B14 source-following parity and B15 close-out remain explicitly open; no CI/Actions.


### 2026-10-09 — M5 real-app visual feedback: sessions, Title, Objectives, Life Area color (candidate)

Real-app screenshots after the green `_133` Objective editor gate and published Orval client `f950d22f` exposed four remaining issues: adding timed or untimed planned Sessions reports a generic planning conflict when the Activity has placement protection enabled; Activity Edit's Title has a second nested rectangular border; existing Objectives are collapsed and show their name twice (row header plus input); newly created Life Areas from Activity Edit display a color briefly, then Timeline falls back to gray.

The bounded follow-up candidate (no schema migration or generated API changes) changes `activity_replan_api.py` so **new planned Sessions within an unchanged, already accepted Activity envelope** are authorable while the envelope is locked. Movement of *existing* Schedule coordinates, removals and interval edits continue to require unlocking; open execution/recorded Actual veto remains. New PostgreSQL regression covers a locked Activity with one new untimed and one new timed Session, verifies the envelope state is unchanged and a subsequent move still conflicts. The existing user screenshot had an enabled “Sblocca spostamenti” control; this is the identified root guard rather than a UI-only error.

The Activity Edit Title CSS now removes its nested label/input borders while preserving one controlled outer border and responsive layout. Every Objective (new and existing) shows a **single editable name field** and all its other definition controls immediately; no duplicate static heading or extra expand step. Series-origin lookup is deferred until focus, and the same Object definition CAS/one-button Save/history veto semantics remain unchanged. Activity Edit Life Area choices carry canonical revision/appearance metadata; creating a new Life Area now sets its canonical area appearance color with owner-scoped revision before assignment, and an explicitly selected color for an existing Life Area is persisted through the same capability rather than changing only the item's color. A colorless existing Life Area shows a neutral gray swatch instead of misleading orange. Failed appearance writes retain pending draft and error for retry. **Create authoring already routes new-Life-Area color through `resolve_authoring_life_area` in the existing backend; its reported real-app color behavior still needs confirmation after this fix, not a made-up backend change.**

New/refocused tests: `test_b14_activity_replan.py` locked new Session acceptance/protection veto; `activity-inspector-actions.test.tsx` always-visible Objective inputs, timed/untimed Session edits, newly created Life Area appearance and existing Life Area color change; `remote-activity-edit-settings.test.ts` appearance revision persistence/CSRF and catalog metadata. **CANDIDATE, NOT VERIFIED**: the previously green Objective gate does not prove this new behavior. One user-local affected gate should include Ruff, the new PostgreSQL test, Web typecheck and both focused Vitest files; no need to rerun earlier broad suites or regenerate the API client. Then real-app visual and persistence acceptance; M5/B15 remain open and recurring owner-field `Questa e le prossime` parity is unchanged. No CI/Actions.

### 2026-10-09 — M5 four real-app fixes: USER-LOCAL GATE GREEN, visual acceptance pending

User pulled branch to `497e8b1a` and ran `bash tooling/verify-b14-m5-ui-acceptance-local.sh` in WSL. The reported consolidated result is **PULL=0, SYNTAX=0, RUFF=0, POSTGRES=0, WEB_TYPECHECK=0, VITEST=0**; full logs at `/tmp/dante-m5-ui.xsV9uI`. The new locked-Activity timed/untimed Session regression, always-open Objective editor and Life Area appearance path are covered by this affected gate. **The M5 follow-up technical gate is VERIFIED GREEN**; do not rerun it unnecessarily.

**What is still open:** real-app manual acceptance of (1) adding both timed and untimed planned Sessions while keeping locked placement unchanged, (2) the single, correctly aligned Activity Title field, (3) always-open Objectives with only one editable name and one general Save, and (4) persistent Life Area colors after saving, Timeline refresh and reopening, including new area creation. Existing protection of historical truths and source-scoped editing rules must remain intact. Product/UI acceptance, M5 and B15 overall are **NOT YET CLOSED**, despite automated green results. User will report visual outcomes. No database revision, Orval regeneration or CI was needed for the four-defect fix.

GitHub workflow: assistant publishes docs/code to `feature/timeline-temporal-operational`; user does **explicit `git pull --ff-only origin feature/timeline-temporal-operational`** in WSL. Always provide the pull command separately before any local action.


### 2026-10-09 — B14 Draft Vault («Bozze») whole-block implementation CANDIDATE

User-approved product shift: retire “Da collocare” as an *authoring choice*; introduce an actor-owned inert Draft Vault for possible future Activity and Event, with full Quick/Advanced Create field snapshots (including uncommitted Session/Objectives/recurrence settings). `Salva bozza` beside `Aggiungi` in both Create surfaces; discard dialog now offers Save draft. Explicit Add authors accepted subject through the existing path; the original draft is removed only after success. Resume and Duplicate reopen the same Create editor; Delete removes inert snapshot. Drafts do **not** establish Activity/Event/Schedule/Session/Actual/reminders or recurrence: see `docs/domain/concepts/draft-vault.md`.

New *forward-only* PostgreSQL `20261009_134` adds `dante.temporal_draft_vault` owner-only table and 3 SECURITY DEFINER CAS/replay/list/delete functions with dante_runtime EXECUTE but no direct table privileges. New `/api/v1/temporal/drafts` authenticated API, TypeScript remote source, Home vault panel, Create integration and tests. Updated Dictionary/SQLAlchemy/catalog to **candidate 237 tables, 5 views, 218 routines, 103 triggers, 484 indexes, 420 FKs, 593 CHECK constraints** (new table + 3 funcs + 1 PK index + 4 CHECK). **Counts are expectations, not user-proven until PostgreSQL gate.** OpenAPI/Orval generated API client files must be published separately after deterministic generation. Local full affected gate scripted in `tooling/verify-b14-draft-vault-local.sh`, no CI or automatic push.

**Historical protection and gaps, explicitly OPEN:** the old planning tray holds *real* canonical unplaced/postponed Activity/Event identities. These remain distinct legacy canonical records, not silently moved or deleted as drafts; the vault exposes an explicit **Gestisci elementi già creati** handoff to the unchanged B01 placement/replan controls under a separately titled **Elementi già creati** panel (its old trigger is hidden). Inspector “Sposta in Bozze” for Activity uses existing canonical retirement guard, preserving history; moving real Event is **not yet supported** because Event has no matching safe retirement capability, so the Event Inspector visibly says “Copia in Bozze” and keeps the original. Do not treat this as Move or mark the full legacy transition accepted. Full Event move needs explicit follow-up owner-retirement capability without corrupting accepted facts. User visual and end-to-end acceptance remains **NOT VERIFIED**, including real app, keyboard interactions, and previous M5 regression checks. No new Timer/Alarm operational functionality. Avoid claiming B14/B15 or Bozze closed.

**User workflow:** Assistant writes and updates `feature/timeline-temporal-operational`; user performs explicitly displayed `git pull --ff-only origin feature/timeline-temporal-operational` in WSL. User runs a SINGLE COMPLETE local gate; do not request CI. User is not asked to push source changes except genuinely local generated OpenAPI artifacts that cannot be read by the connector.


### 2026-10-09 — Draft Vault first user-local gate FAILED; focused repair pending recheck

After pulling `16fdb7ed`, the user ran the single `tooling/verify-b14-draft-vault-local.sh` gate (log directory `/tmp/dante-draft-vault.dBVhHO`). Results: **SYNTAX=1, RUFF=1, POSTGRES=1, GENERATE=0, GENERATED_CHECK=1, API_TYPECHECK=0, WEB_TYPECHECK=2, WEB_VITEST=1**. Precisely observed root blockers: unterminated `_RETIRE` Python SQL literal in migration `20261009_134` (all 10 PostgreSQL cases could not load Alembic); misordered `draft_vault` / `confirmation` imports; incorrect `../../platform/api/web-fetch` reference from `features/temporal-create/application` (Vite build and 5 Vitest suites failed during module import). Four Web suites **ran and passed 11 tests**; the 5 unresolved suites **have not yet been verified**. Fixes were pushed in GitHub commits `dbfa1a89`, `01cf064b`, `20e5c351` respectively. This was NOT a green Draft Vault gate, and these focused fixes still need a new user-local gate. 

Seven generated API files were produced in the user's WSL (`packages/api-client/openapi/dante-v1.openapi.json`, `src/generated/dante.ts`, `model/index.ts`, plus four new `draftVaultResponse.zod.ts`, `draftVaultSaveRequest.zod.ts`, `temporalRetireDraftParams.zod.ts`, `temporalSaveDraftBody.zod.ts`). **Preserve the local modifications, do not reset them.** They are not yet published to the branch; assistant cannot read uncommitted WSL bytes through GitHub. Next: user performs explicit `git pull --ff-only origin feature/timeline-temporal-operational` (new commits do not touch generated files), then reruns the one local `bash tooling/verify-b14-draft-vault-local.sh` gate. Evaluate any newly exposed failures as one coherent repair round, not micro-gates. Overall Bozze candidate remains open, with Event Move parity and real-app visual acceptance pending.


### 2026-10-09 — B14 Draft Vault second local gate: all Web and generation GREEN, 3 PostgreSQL fixes pending

User-local run at `/tmp/dante-draft-vault.4KmEkB` after pulling `e65be88c`: `SYNTAX=0`, `RUFF=0`, `POSTGRES=1` (**7 passed, 3 failed**), `GENERATE=0`, `GENERATED_CHECK=0`, `API_TYPECHECK=0`, `WEB_TYPECHECK=0`, `WEB_VITEST=0`. All tested front-end suites, OpenAPI generation, deterministic source checks and lint pass; do not rerun them merely to prove these backend-only corrections. Two PostgreSQL failures were caused by missing explicit `session.begin()` in `draft_vault_api.list_drafts` and two read sessions of `test_b14_draft_vault.py`; this runtime has autobegin disabled. Third failure was stale hard-coded `(236,5,215)` assertions in `test_database_current_catalog.py`; other counts and the `B14-DRAFT-VAULT` stage assertion in that file would also have been stale. GitHub commits `2e12ddb8`, `6c9854f4`, `7f61a076` respectively fix all three files and all stale hard-coded catalog assertions (expect 237 tables, 5 views, 218 routines, 484 indexes, 593 checks, 237 SQLAlchemy mappings). Code review confirms the read sessions now begin explicit transactions and no old count literals remain in the focused catalog test. **Not yet re-run locally; do not mark PostgreSQL gate green.** Next: user performs *separate explicit* `git pull --ff-only origin feature/timeline-temporal-operational`, preserving the existing seven locally generated API artifacts, then runs just `cd apps/backend && uv run --locked pytest -q --no-cov --tb=short -m postgres tests/integration/temporal/test_b14_draft_vault.py tests/integration/database/test_current_catalog.py tests/integration/database/test_database_current_catalog.py`. If green, publish seven generated API client artifacts from the user's WSL and manually verify Bozze. Event Move parity and existing-items legacy handling remain open; no CI.


### 2026-10-09 — B14 Draft Vault TECHNICAL GATE GREEN (user-local WSL)

After pulling GitHub branch head `59547421`, user ran `uv run --locked ruff check` on the three amended backend files (**All checks passed!**) and `uv run --locked pytest -q --no-cov --tb=short -m postgres` across `test_b14_draft_vault.py`, `test_current_catalog.py`, `test_database_current_catalog.py`: **10 passed in 23.76 seconds**. This completes the PostgreSQL repair gate. The immediately preceding full Draft Vault gate had **SYNTAX=0, RUFF=0, GENERATE=0, GENERATED_CHECK=0, API_TYPECHECK=0, WEB_TYPECHECK=0 and WEB_VITEST=0**; the only failing component was PostgreSQL, now green. **Technical candidate gate is GREEN based on those combined user-local results.** Do not request redundant full reruns for unchanged Web/source.

**Release handoff NOT YET COMPLETE:** Orval/OpenAPI generator created **seven local uncommitted artifacts in user's WSL**, not yet in GitHub feature branch: `packages/api-client/openapi/dante-v1.openapi.json`, `packages/api-client/src/generated/dante.ts`, `packages/api-client/src/generated/model/index.ts`, `packages/api-client/src/generated/model/draftVaultResponse.zod.ts`, `packages/api-client/src/generated/model/draftVaultSaveRequest.zod.ts`, `packages/api-client/src/generated/model/temporalRetireDraftParams.zod.ts`, `packages/api-client/src/generated/model/temporalSaveDraftBody.zod.ts`. Preserve and publish **only** these generated files with `[skip ci]`; they are the deterministic result of the passing generator and are not GitHub-accessible until user uploads or pushes them. Avoid reset/clean of user worktree. Assistant documents green gate on remote, then user explicitly pulls docs (pull does not overlap the seven generated paths); user can push precisely those seven files or supply the generated artifacts for assistant to publish. Once generated artifacts are published, manually accept Create Quick+Advanced Save, durable vault reload, Resume, Duplicate, explicit Add/consume, Delete, legacy existing-item placement, guarded Activity move. Real-app user acceptance **PENDING**; Event canonical Move is not supported (Copy into Bozze preserves original). This does not close overall B14/B15 or previous M5 visual acceptance.


### 2026-10-09 — B14 Draft Vault generated client PUBLISHED; TECHNICAL GATE COMPLETE, visual acceptance OPEN

The user successfully rebased their local `chore(b14-drafts): publish generated API client [skip ci]` commit onto GitHub `3f25c130` and pushed it as **`a3271cf9`** to `feature/timeline-temporal-operational`. GitHub comparison confirms this was precisely **one commit containing seven generated client files**: OpenAPI `dante-v1.openapi.json`, generated `dante.ts`, `model/index.ts`, and four newly generated draft Zod models. The user's `git status` reported **clean and aligned with origin**. Together with prior user-local proof (**10 PostgreSQL tests passed, Ruff green, full Draft Vault Web/Typecheck/Generate gates green**), **Draft Vault candidate technical verification and generated artifact publication are COMPLETE**. Do not repeatedly ask for old gates, commits or CI.

**NEXT: real-app acceptance, NOT YET CLAIMED**. Ensure the actual local DANTE database is migrated to `20261009_134` before running the app (the previous PostgreSQL pytest gate created temporary migrated databases, not necessarily the persistent local instance). Check Quick and Advanced Create → Save draft without operational persistence; refresh/reopen saved drafts; Resume full configuration; Duplicate retains original; Add explicit confirm consumes only source draft after accepted creation; Delete requires confirmation; locked inert Session/notification/recurrence behavior; and legacy canonical ‘Elementi già creati’ remain distinct, safely placeable. Retire an existing Activity only where history guard permits. Existing Events currently support **Copia in Bozze**, not canonical Move; Event retirement parity and prior M5 real-app verification remain open. No Timeline/Home H0 cosmetic refactor, no CI. Assistant source/docs pushes require user-visible, standalone `cd ~/projects/dante && git pull --ff-only origin feature/timeline-temporal-operational` before local app check.
