# Timeline / Temporal-Operational — Workstream Handoff

## CURRENT HANDOFF — 2026-10-10 / live Activity Session execution

**Branch:** `feature/timeline-temporal-operational`. Approved scope: `docs/domain/decisions/activity-session-live-timeline-v1.md`. Candidate files: `20261010_136` (atomic cascading Session transition + new planned start guard), `20261010_137` (historical visual read), `20261010_138` (UUIDv7 cascade and Stop-while-paused repair), `session_panel_api.py`, `session_runtime.py`, `use-session-panel.ts`, `timeline-session-panel.tsx`, `timeline-session-reality.ts`, `timeline-surface.tsx` and `timeline-day-stream.tsx`, plus focused regressions, Dictionary and UI contract. The panel previews exact starts at -5 minutes, and the same Activity card follows real execution without mutating Schedule. **First user-local gate ran and is RED**, see `docs/workstreams/timeline-temporal-operational-map.md` for exact 3 Postgres / typecheck / single Vitest / 390px browser failures. The green components need not be repeated. **No real-app acceptance yet.** Next: the user pulls feature branch and runs `bash tooling/verify-b14-session-live-repair-local.sh`; retain uncommitted generated client artifacts for exact publication. If failing, use one coherent repair pass and repeat only affected gates, not earlier M5/Bozze suites. No CI.

The prior _135 panel, Bozze and M5 technical proof are historical context; they do not prove this newer behavior. The separately open Event-to-Bozze Move and real-app Bozze/M5 acceptance remain open and must not be marked fixed by this Session work.

- **Status:** HISTORICAL HANDOFF checkpoint (2026-10-03) — B12 CLOSED / QUALIFIED USER ACCEPTANCE — B14+B07 active as one user-guided product/UI cycle; U1 Create-entry candidate awaits user visual proof; affected B12-D rerun unreported
- **U6 continuation:** `_102` structure and the B08 Session minimum combination have focused user-run PostgreSQL proof; the combined gate and real-app walkthrough remain open. Read `timeline-temporal-operational-b14-u6-candidate-2026-10-02.md` and the approved U6 gate before work.
- **Activity interval candidate:** `_106` introduces a separate Activity `interval` role, preserves future planned Session `planned` rows, and projects each accepted interval as a distinct card. Read `docs/domain/decisions/activity-intervals-and-sessions-v2.md`; local migration/build/visual acceptance and coordinated interval editing remain open. No proof claimed.
- **Reconciled:** 2026-10-03 (U6 continuation; historical sections retain their dated checkpoints)
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
- **Current migration source head:** Alembic `20261005_106` (Activity intervals branch candidate, not locally proved)
- **Historical focused catalog topology:** `_93` / `196|5|155|100|397|344|497|0|0|0`; current Dictionary materialization is in `docs/database/dictionary/scope.json` and `_106` proof is pending.
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

The subsequent `_101` user gate reported 8 passed and two catalog test-code/Dictionary reference failures, repaired at `f453c2e82abeee9fa03331db265513343cda01ac`. `_102` at `16fe795e68a3c7662b3baf764596db4176043018` persists exact Schedule envelope/planned role and order and exposes it on readback.

The user then ran the focused `_102` atomic Activity structure and both catalog tests from `39c846d0`: **9 passed in 20.80s**. This also confirms the earlier catalog repairs on this branch. The subsequent B08 soft Session minimum in atomic U6 authoring was published at `8b9e9158`; the user ran its focused PostgreSQL test: **1 passed in 7.04s**. The agent reran 36 focused web tests and both web/API-client typechecks successfully. The combined U6/Event/catalog gate and real-stack walkthrough remain unreported; no U6 acceptance is recorded.

## B14 placement lock continuation, 2026-10-06

The current branch includes `_110` explicit user Schedule placement lock and backend/Timeline/Create candidate wiring (`9d2b6130`, reconciliation repair `84161fa5`). Distinguish it from B04 automatic movement policy. No user-run PostgreSQL migration, generated OpenAPI/client, web typecheck or real-app proof is reported; do not mark the lock closed. Existing B04 blocked policies cannot be safely reinterpreted/backfilled as user locks. The separate complete recurring-Activity inheritance vertical is still open and the Create incompatibility guard remains. See the 2026-10-06 addenda in the B14 recurring authoring contract and live map before continuing.


## B14 recurring Activity parity continuation — 2026-10-06

The recurring Activity Create candidate now carries the complete occurrence
template implemented on the current branch (intervals, planned Sessions,
Sub-Activities, Session settings, outcome review, Reminder lead and explicit
placement protection). The earlier statement that complete recurring
inheritance was not implemented is superseded by this candidate state; it is
still **unproven** until the user-run local and real-app gates pass.

The same Create Life Area contract now applies to one-off and recurring
Activities: none, existing, or create-new. The virtual Timeline unassigned
bucket is presentation-only and is not an authorable Life Area. Timeline
organization/color projection is refreshed after checkpoint/materialization so
materialized recurring Activities can resolve their accepted assignment and
appearance. Root start-time editing preserves Activity duration instead of
silently turning a same-day Activity into an overnight window.

Do not clone Activity-only interval/Session/Sub-Activity semantics into Event.
The next Event pass should share recurrence/Life-Area/color/Reminder/Timeline
infrastructure while keeping Event-specific semantics separate.


### Product correction — Sub-Activities

Sub-Activities are implementation/backward-compatibility residue, not an active
Create product surface. Do not reintroduce them while aligning Activity and
Event. Shared Event work should cover recurrence, Life Area/color, location,
description, Reminder and other genuinely shared capabilities only.

## 2026-10-06 — Create closure decision freeze

The active Activity/Event Create cleanup is now governed by `timeline-temporal-operational-create-closure-mini-roadmap-2026-10-06.md`. It freezes the compact three-batch plan: existing Event/B09/common capability consolidation; shared Reality + Objectives; then cleanup and user-run closure gate. Product copy uses **Scaletta** for B03-D Agenda; Sub-Activities are not a current Create product capability; sharing one item does not imply shared calendar/free-busy access.

## 2026-10-06 — Create closure candidate

Current migration source head is now `20261006_114`.

The accepted Create product model is frozen for the closure gate:

```text
Activity/Event
├─ shared authoring: placement / Life Area / color / description / location / recurrence / Reminder
├─ Activity-only: Activity intervals / planned Sessions / placement protection
├─ Event-only: Scaletta / expected participants
├─ Reality: optional global realization-review policy
└─ Objectives 0..N: boolean / quantity / qualitative / range
```

Reality and Objectives are independent. Objective measurements are Observation-backed and evaluated; they are not B10 Outcome payloads. Raw B10 Outcome remains available as a lower-level contextual disposition capability but is not the default Create product field.

Recurring Activity materializes Reality/Objectives onto each Activity instance. Recurring Event materializes them onto each Occurrence. Sub-Activities remain non-product/internal compatibility only.

Status is **IMPLEMENTATION CANDIDATE / USER LOCAL GATE PENDING**. No CI or GitHub Actions were used for this candidate; user runs the final local gate.


## 2026-10-06 — Create closure catalog reconciliation

Create-closure persistence is now reconciled through Alembic `20261006_115`. The final candidate catalog topology is 229 tables / 5 views / 191 routines, with 103 triggers, 467 physical indexes, 401 foreign keys and 569 CHECK constraints. The 14 new persistence tables are mapped and documented; 17 new routine names are documented; the explicit Schedule placement-lock trigger is included in Dictionary truth.

The first user-run gate exposed generated drift, five stale web assertions/type-contracts, two stale catalog snapshots and one Ruff import-order failure. The source/test/catalog repairs are now published. Generated OpenAPI/Orval output still must be produced by the repository generator in the user's local worktree before the final deterministic generated check and real-stack acceptance.

## 2026-10-06 — Create closure automatic gate green

User-run final catalog verification at `6371768b01c54dcf7ae6e8800ae73e8488d7d67e` passed: current catalog + cross-representation catalog suite => **8 passed**. Together with the already-green generated/typecheck/focused web gate, the automatic Create-closure gate is complete. Next cursor: real-stack visual/product acceptance only; fix regressions found there without reopening the product model.

## 2026-10-06 — Life Area Create contract frozen

User-run Life Area regression is green at `a48eb93e41d7040aa540139efce7371b5b18ef83`: focused Create UI test **13/13**; dedicated `apps/web/e2e/auth/temporal-create-life-area-golden.spec.ts` **4 passed, 2 skipped** (Chromium + Firefox real-stack; WebKit intentionally skipped by project policy). This proves one-off and recurring Activity/Event Life Area behavior across none/existing/create-new, assignment/readback, color projection, materialized Timeline items and reload. The picker exposes only canonical Life Areas; the presentation-only unassigned bucket is not authorable and the removed create-on-Add helper must not return. Mark this slice **FROZEN**; regressions should be fixed without reopening the product model.

## 2026-10-06 — Verification rail candidate

The B14/B07 Today rail candidate at Alembic `20261006_117` extends the shared lower edge of Timeline, Context Rail and Quick Create by 48 px and derives pending Reality/Objective/B10 Reconciliation cards from canonical state. Activity review requires a completed bounded Session; Event and Event Occurrence review uses the accepted placement end in the person's effective IANA zone, including date spans. The Reality response carries the exact Session/timing basis; Objective responses write Observation/Evaluation through the existing owner API. The branch candidate is unproven pending user-run local migration, generated-client/typecheck, focused PostgreSQL/web and real-app acceptance. The active details and gate are in `timeline-temporal-operational-b14-ui-consolidation-2026-09-30.md`.

## B14 recurrence edit scope correction — 2026-10-08

**Newly user-confirmed product authority**, detailed in the final section of
`timeline-temporal-operational-b14-ui-consolidation-2026-09-30.md`:
For a selected recurring Activity/Event instance, the only save scopes are
`Solo questa` and `Questa e le prossime`. **Both always include the clicked
instance**. Following scope additionally includes future instances later than
the selected recurrence position, NEVER other past instances. Example:
past 1,2,3; NOW; future 4,5,6 — selecting 1 yields 1 or 1+4+5+6
(not 2,3); selecting 4 yields 4 or 4+5+6; selecting 5 yields 5 or 5+6.
No future-only choice without the selected instance.

This governs **all edits**, not just Objectives. Past recorded facts and
evaluated Objectives remain correctable with the user's corrected value
becoming current canonical truth; they are not deletable. Correcting an
Objective retains its logical product identity with internal immutable
history, not a required new visible Objective. Current/future planned
content can be edited/removed subject to domain rules and chosen scope.
Dependent assessments must be reconciled without inventing manual
judgments. Previous Objective versioning design gate was superseded.
**Only the rule/documentation is approved; no code or schema implements
the full scoped modification/correction lifecycle yet.**

## B14 inspector scope and implementation checkpoint — 2026-10-08

Reconciled against live branch `39e8ab96`, road map/map,
B14 consolidation ledger, current API/Activity editor/duplicate seed, and
_121 migration/DB Dictionary. **Use the complete M1–M5 status and evidence
matrix in the B14 ledger** rather than older U6 candidate descriptions.

Recent user-run green gates: Activity interval replan Ruff 0,
backend unit **4/4**, PostgreSQL/catalog **15/15**, previous web **15/15**,
API client source-generation deterministic **483**; six generator-produced
artifacts published by the user in `c22f04ae`. Post-create Activity
Objective ADD web typecheck 0 and **17/17 Vitest**, also user run.
Focused PASS is not final real-app Inspector acceptance.

Global modification policy is approved but **not yet implemented**:
`Solo questa` or `Questa e le prossime`, always including the clicked
instance; the second targets additional *future* instances only, never other
past occurrences. Past Objective/Observation corrections become current
truth, with immutable audit; past realized facts cannot be deleted.
No inference about the user's reason for editing. Applies to ALL relevant
Activity/Event modifications, not Objectives alone.

**Next**: M1 canonical recurrence-instance scope + safe preview/CAS,
then M2 Objective definition/recorded-fact correction, M3 Activity edit
gaps and past retirement policy, M4 faithful duplication/Event parity,
M5 user local end-to-end real-stack and B15 closure. Do not implement
future-only scope, direct Objective target mutation or copy of Actual/
Observation/Evaluation into duplicates. No CI/Actions; user alone runs
local WSL tests.

## B14 M1-A selector candidate — 2026-10-08

Live GitHub contains `apps/backend/src/dante/modules/temporal/occurrence_edit_scope.py`
and `apps/backend/tests/test_b14_occurrence_edit_scope.py`, plus a detailed
scope note at the end of the B14 ledger. This is an independent,
**not-yet-user-tested** pure selection candidate. It reuses existing B06/B11
Occurrence/Recurrence identity and enforces selected-anchor plus later
future only (not other past instances), detects skipped/overridden/
recorded-fact conflicts, distinguishes future template inheritance,
and rejects unverified/incomplete following inventories. It does NOT
yet add an API, SQL function, web wiring or persist multi-instance edits;
the full M1 block is OPEN. User runs Ruff and focused pytest in WSL.
Next deliverable: guarded authoritative current occurrence inventory +
source CAS/preview/apply integration, reusing B06/B11 functions rather
than rebuilding their already-proven functionality. The user explicitly
noted that several original backlog capabilities already exist, so
avoid counting implemented individual features as missing.

## 2026-10-08 — M1-A passed; M1-B guarded inventory checkpoint

**User-local PASS** at `a62ab230`: M1-A Ruff 0; 18/18 focused
unit tests. M1-A pure selector closed. **M1 remains OPEN**.
M1-B adds forward-only `20261008_122` a bounded owner-only
materialized Occurrence read via existing B06 `get_self_occurrence`,
a Python read application and read-only HTTP
`GET /temporal/occurrences/{ref}/edit-inventory`. It includes
skipped/Scheduled/extra materialized instances for both Routine and
Event source, with 10k hard failure and no newly generated future
assumptions; no apply authorization. The database Dictionary and
exact topology probes were advanced to 231/5/**197**/103/471/405/572.
New focused integration test is
`test_b14_m1_edit_inventory.py`.

**UNPROVEN candidate** until user local PostgreSQL, catalog, Ruff,
OpenAPI/generated client and typechecks. No multi-instance mutation
or scope UI is yet implemented. Next M1-C must add authoritative
write-time CAS, override/recorded-fact conflict resolution,
Activity/Event identity linking, future template revision and one
atomic idempotent apply. User runs tests locally, no CI.

## 2026-10-08 — M1 whole-vertical candidate _123, user gate pending

User-reported _122 inventory **Ruff PASS, PostgreSQL 10/10 PASS,
OpenAPI generated/check 484 PASS, API/Web typecheck PASS**.
Generated files currently uncommitted in local user worktree.

Live branch now includes forward migration `20261008_123`,
append-only `occurrence_profile_edit`, five self-scoped read/write
functions, ORM/Database Dictionary exact target
`232|5|202|103|473|408|576`, atomic recurrence-source
metadata edit with CAS/replay/owner controls, selected-anchor/future
inheritance, Activity readback/Timeline projection/materialization,
and scoped Activity general-metadata save UI. Event Occurrence
metadata patch has backend/Timeline support; M4 Event Inspector
UI parity remains open. New PostgreSQL and Vitest tests are
in the branch but not user-run. Latest work is one combined
candidate, **not** a claim of final whole B14 acceptance.

The user explicitly requests **no further small isolated steps**:
request ONE combined local gate. Preserve generated client output
once it passes. Do not claim that scoped editing already handles
Objective facts, Session/Scaletta, Schedule or all other fields;
M2/M3/M4 will integrate those owners with the global
`Solo questa / Questa e le prossime` contract.

## 2026-10-08 — _124 fixes M1 gate regression (user proof pending)

M1 _123 local user gate results: Ruff 1 (2 I001), 18/18 unit
PASS, PostgreSQL 16 PASS / 4 FAIL; OpenAPI generation PASS,
generated 489 deterministic PASS, API/Web typecheck PASS,
Vitest 21 PASS. Four PostgreSQL failures share a single
one-off Activity Inspector profile NULL Occurrence access,
not a security failure in the strict Occurrence function.

On branch: `20261008_124_b14_scoped_activity_profile_guard.py`
forward-only existing function replacement (explicit null guard);
Timeline one-off Activity CASE guard; two import sort fixes;
Dictionary (one routine now PL/pgSQL) and _124 exact catalog
expected revision; focused one-off Activity regression test.
No new objects; topology unchanged 232|5|202|103|473|408|576.
_124 user-run local proof **PENDING**. User should run one
combined focused local gate, preserving locally generated
API client artifacts. No CI. M1 metadata candidate is NOT yet
closed until that proof.

## 2026-10-08 — _124 user local gate: PostgreSQL/Web all green; lint-only fix

User confirmed after pulling `14b38334`:
`POSTGRES=0`, `GENERATED_CHECK=0`, `API_TYPECHECK=0`,
`WEB_TYPECHECK=0`, `VITEST=0`. The previous four B14 Activity
Inspector failures are gone and the new one-off profile regression
test passed. Ruff found exactly one new test-only rule `DTZ011`
(`date.today()` in
`tests/integration/temporal/test_b14_m1_activity_profile_guard.py`).
Commit `62c18771` replaces it with
`datetime.now(ZoneInfo("Europe/Rome")).date()`.
**Only focused Ruff rerun remains** for _124 technical gate.
Generated client OpenAPI/TypeScript artifacts pass deterministic
check but are still modified/untracked in the user's local worktree;
they are NOT yet published to the remote branch. Preserve them and
reconcile their commit before marking M1 metadata delivery closed.
No CI. B14 domain M2–M5 remain open.

## 2026-10-08 — M1 recurring general-metadata vertical closed, all artifacts on GitHub

User completed final local `set -e` gate at _124 and published `55a017b9` to `feature/timeline-temporal-operational`. Ruff **All checks passed!**, earlier _124 PostgreSQL/Generated Check/API Typecheck/Web Typecheck/Vitest all exit **0**. User-produced commit adds nine generated OpenAPI/Orval files (1,013 insertions), push succeeds, and `git status --short` is clean. M1-A 18 unit and M1-B 10 PostgreSQL were separately proven. **Mark M1 CLOSED only for recurring Activity/Event general metadata,** with the user-run focused gate. No hidden claim of visual acceptance or other domain edits. Revision _124 exact catalog unchanged 232/5/202/103/473/408/576. Resume M2 complete Objective definition/reality correction with stable logical Objective identity (retain old accepted snapshots/Observations/Evaluation for audit; newest corrected values canonical), no deleting recorded historical facts, correct deterministic re-evaluation, actor-scope, CAS and operation replay. The product rule for ALL edits remains selected included in either of exactly two scopes; future-only excludes the other already-past Occurrences. M3/M4/M5/B15 open. The dependency advisory shown by GitHub upon push (34 on default branch) is not a result of this gate and was not investigated; treat independently, not as B14 blocker. No CI/Actions.

## 2026-10-08 — M2 complete Objective correction candidate (_125/_126), local proof open

Latest M1 general metadata: published generated `55a017b9`, user Ruff+PostgreSQL+Web+client all green, exact _124 catalog. M2 newly committed on branch: `20261008_125_b14_objective_corrections.py` adds append-only `temporal_objective_definition_revision` and 3 self-scoped capability functions, replacing effective list/result readers; `20261008_126_b14_scoped_objective_definition.py` adds append-only `temporal_objective_series_edit` and 2 new self-scoped functions, replacing effective definition read to apply selected+later future source-template policies. SQLAlchemy mappings and exact Dictionary now 234/5/207/103/477/414/586. Changes never delete Observations, Evaluation states or previous definitions. User-corrected past definitions become current truth under same `objective_ref`, with deterministic quantitative/boolean reassessment; manual qualitative assessment cannot be fabricated.

Objective series scope uses trusted `b14:objective:{kind}:{subject_ref}:{slot}` materializer provenance and current source/Recurrence CAS, *not* name or `presentation_order`. Both scope choices include clicked instance; other past excluded. Skip, Actual, locally corrected future Objective and prior Observation block all-or-nothing series update. Future newly materialized Objective inherits read-side source policy; its own recorded result is never copied. Manual one-off Objective edits work with selected scope only and the UI makes limitations explicit. New Objective definition/result correction API, typed Web data source and Activity editor (existing Objective edit and result correction) plus focused PostgreSQL and Vitest tests are committed.

**Status: CANDIDATE, USER LOCAL GATE NOT RUN.** One whole test pass required (Ruff, _125/_126 migration/DB exact catalog, Objective correction and recurring-scope PostgreSQL + prior M1/Objective regression, generated/check, TypeScript, Vitest). Publish canonical generated files after the gate. Do not mark M2 or B14 closed before user gate. Do not reopen previous B06/B11, no CI or Actions. M3/M4/M5/B15 still open.

## 2026-10-08 — First local M2 gate: syntax blocker repaired, focused rerun required

User local first M2 gate at branch `4f7c90d3`: `RUFF=1` (malformed ORM mapping and Objective audit test), `POSTGRES=2` (seven collection errors from ORM SyntaxError), `GENERATE=1` (FastAPI cannot import), `GENERATED_CHECK=1` (TSX malformed), `API_TYPECHECK=0`, `WEB_TYPECHECK=2`, `VITEST=1` (11 other tests green; Activity editor TSX failed to parse). **No passing DB functional assessment was reached**.

Fixes since gate: rebuilt `b14_create_closure.py` from pre-M2 stable mapping and added exactly one immutable Objective definition row and one series row with exact named constraints and complete fingerprint regex; repaired test's `asyncio` audit count closure; repaired `activity-edit-panel.tsx` JSX handler. Additionally tightened historical recorded-result replay to precede current definition type/shape validation, and made result correction require an actual previous Evaluation state under CAS in SQL, FastAPI and the Web UI/data source. No Alembic revision/count changes; catalog target remains `20261008_126`, `234/5/207/103/477/414/586`.

**Status remains M2 CANDIDATE, NOT GATE-GREEN**. User must run ONE complete new local gate for Ruff, Postgres, generation/check, typecheck and Vitest. Generated OpenAPI/Orval files are not published yet. M3/M4/M5/B15 remain open; no Actions/CI.

## 2026-10-08 — Second user local M2 gate, remaining blockers fixed in branch

Second user gate at `7b3f1df1`: `RUFF=1`, `POSTGRES=2` (collection aborted), `GENERATE=1` and `GENERATED_CHECK=1`, all cascading from **two remaining orphan trailing ORM CheckConstraint snippets** in `b14_create_closure.py` (lines 223, 302). `WEB_TYPECHECK=2` reported nullable `objective.evaluationStateRef` at Activity editor line 313. `API_TYPECHECK=0`, **`VITEST=0`** with the prior TSX syntax already fixed.

Branch repairs: surgically removed both malformed orphan fragments after legitimate class `__table_args__` (commit `302a74ac`, readback confirms 16 unique classes and no orphan line), added explicit non-null Evaluation guard at correction call site before submitting required correction state (commit `96b3ecf6`). These changes are syntax/call-site corrections, not a migration revision bump. Current expected catalog remains `20261008_126`, `234/5/207/103/477/414/586`. Source readbacks verified correct base classes, legacy Objective methods and template-generated Event/Activity origin contract.

**M2 NOT GREEN: functional PostgreSQL tests still have not executed, and generated OpenAPI/Orval files have not been committed.** Rerun one complete local gate before claiming any M2 closure; avoid CI.

Additional pre-gate static review: corrected all three M2 recurring test queries that had incorrectly read `generated_date` from `dante.occurrence_generation`; generated calendar dates live in `dante.occurrence_generation_calendar` and are now joined explicitly. No effect on runtime schema, extra migration or dictionary topology.

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

## 2026-10-08 — AUTHORITATIVE LATEST HANDOFF: M2 GATE GREEN, generated client published

This entry **supersedes earlier M2 pending/failing status lines**; preserve them solely as historical investigation. On the user's final WSL `~/projects/dante` gate after pulling `b1599c19`:
```text
SYNTAX=0
RUFF=0
POSTGRES=0
GENERATE=0
GENERATED_CHECK=0
API_TYPECHECK=0
WEB_TYPECHECK=0
VITEST=0
LOG_DIR=/tmp/dante-m2-gate.ZTDo2Z
TUTTI I GATE VERDI
CLIENT_API_PUBLISH_EXIT=0
```
The user then committed/pushed canonical generated OpenAPI/Orval client in `09dc26f9` (ten changed files); verified remote `feature/timeline-temporal-operational` HEAD `09dc26f9e7140698856461d8e1b7652eadc93404` and generated Objective model file availability. `20261008_126` Dictionary/catalog expected topology 234/5/207/103/477/414/586 is included in the successful focused tests. **M2 CLOSED for automated technical scope only**, not an assertion of visual or full-stack usage acceptance. M1 already closed for scoped general metadata. No fresh independent assistant-side PostgreSQL run was performed.

**Next action, M3:** inspect already working Activity Inspector/Edit/Replan and domain-owned B08 Session, B05 Life Area, B02/B04 Schedule/Reminder, and B14 retirement to avoid redundant implementations. Finish remaining existing planned Session display-name mutation; null/unassign primary Life Area; outstanding temporal forms/settings and Schedule/Reminder/policy edits; history-aware Activity retirement. Design authoritative scoped edits for recurrence-derived instances without changing unrelated past facts. One complete bounded M3 backend/DB/Dictionary/API/Web integration and one user-local combined gate; no micro-gates, no CI. Thereafter M4 faithful Activity/Event Duplicate + Event Inspector, M5 product dogfood, B15 whole vertical. User runs tests from local worktree `~/projects/dante`; do not use GitHub Actions.

## 2026-10-08 — M3 post-create Activity residual edit candidate on _127

**CURRENT STATUS: IMPLEMENTED CANDIDATE; THE USER HAS NOT RUN THE _127 LOCAL GATE.** Do not call M3 proven or B14/B15 closed. Following M2 user-green gate and generated publication `09dc26f9`, forward-only `20261008_127` adds three post-create behaviors:
- Actor-local Activity **and Event primary Life Area explicit unassignment**: four existing `life_area_ref` columns (current row + immutable operation receipts) accept NULL. The existing guarded assign functions retain self ownership, expected-revision CAS, durable operation receipt, replay/reuse rejection and monotonic revision after unassignment/reassignment; `list_self_unassigned_life_area_items` now recognizes explicitly null assignments. API/request/response/ORM, Activity editor and remote source accept NULL. No fake Life Area is created and no row deletion resets revision.
- Existing **planned Activity Session display name** can be revised through the same `activity_schedule_role` Schedule identity, using a new self-scoped `revise_self_planned_session_name` function (expected-name compare, idempotent same-target replay, validation, actor-ownership and retired guard). This is **presentation metadata**, not actual Session timing or schedule-history mutation. API, remote client, Activity editor and tests added; no history of prior *label values* is modeled in this candidate, so do not misrepresent it as a full append-only label ledger or a recurring template-wide edit.
- **Activity retirement historical-truth veto**: the existing guarded `retire_self_activity` function now rejects deletion/retirement whenever a Session (even ended), accepted Actual or recorded Objective observation/evaluation exists. The existing open-Session veto and retirement operation replay remain. Inspector explains the restriction and shows a conflict for recorded truth. Corrections to historical data continue through their own domain-owned edit endpoints.

Candidate DB topology `234 tables / 5 views / 208 routines / 103 triggers / 477 indexes / 414 FKs / 586 CHECK` at `20261008_127`; ORM, Dictionary entries, scope and exact catalog test expectations updated. The additional routine is the planned label capability; nullable columns create no new tables/constraints. Backend PostgreSQL test `test_b14_m3_residual_editor.py` checks Life Area null CAS/replay/actor isolation, Event parity, planned Schedule identity and recorded Session retirement veto; focused Web remote-contract regression added.

**Outstanding verification and scope:** no automated _127 proof yet; migrations/DB exact catalog, legacy B05/B14 and M2 regression, API generation/determinism, Web/API-client typecheck and Vitest must pass on the user local worktree before publishing canonical generated files. Remaining broad M3 questions include recurrence-template propagation for domain-owned Session name/Life Area, non-supported temporal-form UX and acceptance of historical label edits; do not claim these solved by selected-only mutations. Preserve `Solo questa`/`Questa e le prossime` for supported recurring edits with clicked included. After honest M3 gating/reconciliation, M4 faithful Activity/Event Duplica and Event Inspector and M5/B15 full product acceptance remain. No GitHub Actions or CI.


## 2026-10-08 14:28 — M3 first user-local gate: blocked by _127 migration, repair published

User pulled M3 candidate `4ed4497e` and ran consolidated `/tmp/dante-m3-gate.scSaU4`. Reported `SYNTAX=0 RUFF=1 POSTGRES=1 GENERATE=0 GENERATED_CHECK=0 API_TYPECHECK=0 WEB_TYPECHECK=0 VITEST=0`. The reported `26 PostgreSQL errors` were **all migration setup failures**, not 26 individually executed/failing assertions. Primary blocker: Psycopg treats SQL `dante.activity_intention%ROWTYPE` inside unescaped raw `exec_driver_sql` as an invalid `%R` placeholder. The M3 _127 migration was never applied successfully in that gate. Ruff listed three findings: SQL interpolated function string, import order in `test_b14_m3_residual_editor.py`, and PT018 compound assertion. All eight gate results have not been reverified after the repairs. Client API generated files exist **only as local user worktree changes**, not on remote; do not delete or hand-edit them.

**Repair pushed on the same branch after failed migration gate:** replace PL/pgSQL `%ROWTYPE` local variable with `record` (equivalent `SELECT * INTO` behavior without driver placeholder); scope `# noqa: S608` to the *closing Python triple-string line* so the literal SQL contains no Python comment; sort tests imports and split compound assertion. Last repair commit `4dfd046f`, branch advanced since original `4ed4497e`. No local user retest has been reported. Next gate should run Ruff, PostgreSQL and exact catalog with existing suite, then TypeScript/Orval determinism as needed; one consolidated command. Fix actual subsequent failures together, never count setup failures as passing domain tests, no CI. **M3 remains OPEN, not proven.**

## 2026-10-08 14:42 — M3 second local gate: 21 PASS / 5 FAIL (repairs pending user verification)

The user pulled `c7206a10` and executed the M3 combined recheck; `RUFF=1` (test import ordering), `POSTGRES=1` with **21 passed, 5 failed**, while `GENERATE`, `GENERATED_CHECK`, `API_TYPECHECK`, `WEB_TYPECHECK` and `VITEST` were previously green. The failed tests were M3 Activity null Life Area, M3 Event null Life Area, legacy B05 primary reassignment, M2 Event Objective definition (which uses a scheduled Event with an assigned Life Area), and exact database cross-representation catalog. The displayed log was only `tail -n 100`, so full individual test tracebacks were not included; log path on user's WSL: `/tmp/dante-m3-recheck.LM4nCX/POSTGRES.log`.

Code review established that `20261008_127`'s `assign_self_{activity,event}_life_area` functions used unqualified `WHERE life_area_ref=requested_life_area_ref` although `life_area_ref` is also a PL/pgSQL output variable under `#variable_conflict error`. The new SQL now explicitly uses `target.life_area_ref`, `target.self_person_ref`, `target.archived` (commit `39e11193`). The B05 legacy and M2 scheduled Event tests both call these replacement Life Area functions, explaining their shared likely failure path. Ruff import placement corrected in `test_b14_m3_residual_editor.py` (commit `7ad57b87`). Exact-catalog test stale values were updated to **208 routines**, **447 standalone entries**, and to expect `B14-M3-RESIDUAL-EDITOR` in completed stages (commit `56a6e4de`). The physical topology expected remains **234 tables / 5 views / 208 routines / 103 triggers / 477 indexes / 414 FKs / 586 CHECK**.

**Latest state: _127 M3 implementation candidate, NOT verified green.** Recheck focused Ruff and PostgreSQL, then the full local gate before generated-client publication. User's uncommitted OpenAPI/Orval outputs must be preserved (do not reset/overwrite manually); no Actions or CI. If additional failure remains, collect complete pytest failure traceback rather than another `tail -n 100` summary. M1/M2 remain closed and published; M4/M5/B15 still open.

## 2026-10-08 — AUTHORITATIVE M3 LOCAL GATE RESULT: GREEN, client in 6fdda05f

The previous first and second failing M3 logs below/above are **superseded**. User's WSL local worktree `~/projects/dante` pulled `d09af8a0` and ran the complete 8-part gate:
```text
SYNTAX=0
RUFF=0
POSTGRES=0
GENERATE=0
GENERATED_CHECK=0
API_TYPECHECK=0
WEB_TYPECHECK=0
VITEST=0
PUBLISH_EXIT=0
LOG_DIR=/tmp/dante-m3-final.rAAiah
```
GitHub received `6fdda05f`: 10 generated OpenAPI/Orval artifacts (343 insertions, 10 deletions), including planned Session name models and Life Area nullable response/request changes. GitHub branch `feature/timeline-temporal-operational` was independently read back at `6fdda05feb0035a66274dfbbf1723aad495b6637`. The focused PG suite includes M3 tests, B05 existing Life Area tests, Activity inspector/replan/snapshot, M2 Objective regression, current schema/catalog assertions; green. Exact _127 Dictionary target 234 tables/5 views/208 routines/103 triggers/477 indexes/414 FK/586 CHECK, standalone 447; green within the user's tested suite.

**Status:** M1, M2 and **M3-A owner-domain residual edit implementation** technically proven and generated code published. M3 as entire roadmap block **remains open**, because generated Routine/Event recurrence source template propagation for newly edited Life Area/planned Session label and all Create/Edit temporal policy settings parity have not been demonstrated. Current UI safely restricts these new domain edits to selected-only, and explicitly refuses `Questa e le prossime`; no hidden propagation. Do not turn off the guard as a workaround or call M3/M4/B14/B15 completely closed.

**Next action:** inspect actual source/template Life Area and planned Session naming ownership, established M1/M2 guarded scope machinery, Schedule/Reminder policy editor read/write surfaces, existing tests and Domain/Logical/Physical/Dictionary before choosing a bounded implementation. Preserve invariant `Solo questa` includes clicked, `Questa e le prossime` includes clicked plus later future only and never other past; no implicit copying of recorded truth. Implement a full coherent chunk, then request one user-local gate, no GitHub Actions/CI. Then M4 Activity/Event faithful Duplica + Event Inspector, M5 real-stack visual acceptance, B15 closure.

## 2026-10-08 — M3-B owner-domain scope integrity candidate (no migration)

After M3-A user-green `_127` gate and published generated client `6fdda05f`, M3-B review of the actual Domain/Logical/Physical contracts, `routine_occurrence_materialization.py`, M1 `_123` and M2 `_126` established **no canonical following-series policy for Life Area or planned Session labels**. Routine materializer reads the owner's Life Area from `list_self_routines`; planned Session labels are copied from `routine_occurrence_policy.activity_template.planned_slices[].name`. Following edits cannot be safely implemented as a loop over already materialized Activity/Schedule rows: that misses future checkpoint instances and breaks owner/source CAS and historical exceptions. Routine/Event source semantics differ; do not imply parity without proof. The detailed negative-scope acceptance plan is in `docs/workstreams/timeline-temporal-operational-m3-b-owner-scope-2026-10-08.md`.

**Implemented on GitHub, newly UNTESTED:** the Activity editor now treats pending planned Session names as dirty and blocks general save and replan preview/apply until individually saved; after successful replanning it rebuilds the planned-name baseline. The recurring scope controls are visible even for Life Area/name-only drafts but disable `Questa e le prossime` when there is no supported metadata change, with explicit owner-domain-only guidance. Unsupported temporal Schedule forms are left untouched, with a non-conversion explanation. The remote Activity Inspector displays the recorded-truth retirement veto specifically instead of a generic stale conflict. Focused Vitest cases were added for draft loss, replan coexistence, recurring Life Area and Session name scopes, unsupported absolute temporal form, and retirement error/invalidation.

**State:** M3-A remains technically green; **M3-B candidate UI/guard implementation needs a fresh user-local Web typecheck and focused Vitest gate**. M3-B following-source implementation remains open: a new source policy must protect original selected Occurrence, future not-yet-generated occurrences, stable planned-template slot identity, independent per-instance edits, skip/Actual/recorded Session/Observation, owner and recurrence CAS; no such source policy is claimed or silently emulated. No new migrations or Dictionary topology changes: still `20261008_127` and `234/5/208/103/477/414/586`. M4/M5/B15 remain open. No GitHub Actions/CI; user runs local gate.

### M3-B extra integration proof added after UI audit (pending local run)

The new test `apps/backend/tests/integration/temporal/test_b14_m3_b_instance_scope_boundary.py` creates a canonical daily Routine with a named root planned Session, materializes two Occurrences, edits only the first generated Activity's Life Area and first planned Session display name, then checkpoints a third future Occurrence. It asserts the selected Activity/label change preserves Schedule identity, and the other materialized and newly generated Activities retain the **source** Life Area (unassigned) and template planned name, with no covert following-series propagation. It reads exact checkpoint IDs and links through existing owner-scoped capabilities rather than raw runtime table grants. This test and newly added UI tests **have not yet run in the user's local PostgreSQL/Web harness**; do not treat the negative assertion as proven until the gate. The consolidated M3-B gate must include this new test plus the B14 M3-A/M2 owner regression, Web typecheck and two focused Vitest files. Schema/catalog unchanged _127; no generated client publication needed for this UI/negative-test-only change.

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

## 2026-10-08 — M4 first user gate, focused repair pending complete rerun

User-local gate at `244ecaef` returned green `PULL/SYNTAX/UNIT/POSTGRES/GENERATE/GENERATED_CHECK/API_TYPECHECK`, red `RUFF=1`, `WEB_TYPECHECK=2`, `VITEST=1` (66/67). The reported failures were two import blocks, three TypeScript test errors and one stale Italian Event Agenda accessible-name assertion. The consolidated repair formats those imports, uses valid Testing Library exact-name regexes, guards optional fetch-init access, and checks Agenda actions across the two existing Italian label variants. Local Ruff, Web typecheck and all 67 selected Web tests now pass. Only source/test/docs changed; the first gate's generated client was intentionally not published. Await a **single whole-block user-local rerun** via `bash tooling/verify-b14-m4-local.sh` after pulling the repair. M4 remains unverified until that rerun and M5/B15 visual acceptance remains separate.

## 2026-10-08 — M4 integrated technical gate GREEN; client published

**This supersedes the preceding M4 pending-gate checkpoint.** The user's WSL `bash tooling/verify-b14-m4-local.sh` returned zero for all ten stages: `PULL`, `SYNTAX`, `RUFF`, `UNIT`, `POSTGRES`, `GENERATE`, `GENERATED_CHECK`, `API_TYPECHECK`, `WEB_TYPECHECK`, `VITEST`. Log directory `/tmp/dante-m4-whole.5cpYvA`. The verified seven-file Event profile OpenAPI/Orval output was committed and pushed by the gate as `77968de6` (`M4_CLIENT_PUBLISH=OK`); remote branch readback matches. M4's implemented Inspector/edit and supported duplicate paths are technically user-verified, with the explicit refusals for unsupported complex duplication intact. **Next:** one real-app M5 visual/keyboard walkthrough and defects, then B15 parity/closure review. No additional M4 micro-gates. `Questa e le prossime` for owner-domain Life Area/planned Session labels remains guarded, unimplemented global B14 debt, and the automated gate is not visual acceptance. Read `docs/workstreams/timeline-temporal-operational-m4-delivery.md` for the M5 journey. No CI/Actions.

## 2026-10-09 — M5 Session editor, validation and Objective Inspector repair candidate

User real-app screenshots exposed three defects after the green M4 technical gate: Edit's planned-Session clock controls inherited broad Timeline input/button styling, Create showed an English range paragraph with a misplaced section-wide red outline, and entering a numeric Objective observation in Inspector opened the error boundary. The Web candidate excludes the shared Session clock controls from those broad editor selectors, removes the Edit-only offset, localizes the bounded structure message, and targets the invalid Session's date/time row. Numeric Objective input now snapshots the DOM value before React's deferred state updater. A dedicated Inspector regression records `8 km`; targeted Create validation checks outside-range and reversed Session times, and a form test confirms the inline Italian error and precise invalid row.

Coding-workspace proof: Web typecheck, changed runtime/new-test ESLint and four focused Vitest files (54 tests) pass. The older Create entry test file has pre-existing ESLint violations and was excluded from this lint command; its tests are included. No user WSL run, real-app visual proof, or PostgreSQL proof is claimed for this candidate. Alembic `_129/_130` untimed planned-Session persistence and Docker-assigned acceptance port are already on branch HEAD `ec648022`, but their user-local PostgreSQL/catalog gate remains pending. M4 stays technically green, M5 remains open, and B15 parity debt for `Questa e le prossime` Life Area/planned Session labels remains unchanged. Run one consolidated affected gate after publication; no CI or extra M4 gate.

## 2026-10-09 — User-local M5/untimed acceptance gate, Ruff repair pending

After pulling `b1b74c6d`, the user's WSL gate reported 13/13 PostgreSQL integration and exact-catalog tests passing on `_130`, Web typecheck passing, and 54/54 focused Vitest tests passing. Ruff alone reported four style violations in `test_b14_u2_authoring.py`: literal dict, compound assertion, and two intentionally naive datetimes for floating-local placement. The focused repair preserves test semantics and marks those two datetimes with `DTZ001` exemptions. This repair is not yet user-local Ruff verified; no second PostgreSQL/Web run is needed solely for this test-style change. The Create entry test also emitted an existing React cross-component setState warning while all tests passed; track separately from this blocking Ruff gate. M5 visual acceptance remains open; B14 source-following Life Area/planned Session naming remains guarded.

## 2026-10-09 — M5/untimed focused technical gate GREEN

The user pulled `0754ba1e` in WSL and reran the exact focused Ruff selection; **All checks passed**. The preceding run on `b1b74c6d` had already passed 13/13 PostgreSQL integration and exact-catalog tests, Web typecheck, and 54/54 focused Vitest tests. The intervening commit changed only test lint/syntax and documentation, so this completes the bounded technical gate without repeating green PostgreSQL/Web checks. The React cross-component update warning seen in an existing Create-entry test remains a non-failing follow-up observation. Next: the user inspects planned Session clock layout in Activity Edit, the localized precise range validation in Create, and numeric Objective input/recording in Inspector in the real app. M5 visual acceptance and B14 source-following `Questa e le prossime` parity debt remain open; no CI/Actions.

## 2026-10-09 — M5 Edit follow-up candidate, local gate pending

Real-app feedback after `5fcbe7e` reports inability to remove an existing planned Session, a stuck placement lock save, stale runtime Session controls, creation-only type choices in Edit, duplicate/misaligned Description, missing new Life Area creation, and renewed Objective crash. This candidate adds `_132` owner-scoped planned-role retirement (history retained, recorded execution veto, active-role filtering), fixes the first-lock CAS basis `0 → null` and finite request wait, invalidates card capability after capture-policy save, positions Inspector runtime controls by the title, removes the type selector from Activity Edit, simplifies Description, and creates then assigns a new Life Area from Edit. New backend and Web regressions cover the main changed paths. Static Web typecheck and Python compilation passed in the coding workspace; **the user-local Ruff/PostgreSQL/Vitest gate, migration, generated API contract publication, and real-app visual checks remain pending**. The renewed Objective white page has no `Show Error` trace, so its cause is unconfirmed and it remains open. M5/B15 stay open. No CI.

## 2026-10-09 — M5 whole-block technical candidate assembled

The source-generated OpenAPI/Orval client now includes the `_129`–`_132` Activity planning request and snapshot shapes, including distinct `delete_planned_sessions`; two consecutive source generations produced identical file hashes. `_131`'s unproven candidate PL/pgSQL record declaration matches the user's earlier local correction. `_132` rejects placement of a retired planned row; a PostgreSQL regression now asserts this guard. The Web request expectation includes the delete field, and deferred React input updaters in Activity planned names and Event metadata snapshot values before scheduling state. Workspace evidence: Ruff on changed backend files, Python compilation, 23 backend unit tests, 75 focused Web tests, API/Web typechecks, and generated determinism passed. PostgreSQL/catalog and real-app acceptance remain user-local and unproven. Run **one** gate: `bash tooling/verify-b14-m5-local.sh`; it performs no commit, push or CI. The renewed Objective report has only a generic boundary screenshot; numeric Inspector entry is guarded and regression-tested, but a further crash requires its `Show Error` detail. M5/B15 and source-following Life Area/planned-name parity remain open.

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
