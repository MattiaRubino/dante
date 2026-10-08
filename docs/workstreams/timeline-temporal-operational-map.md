# Timeline / Temporal-Operational — Live Execution Ledger

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
