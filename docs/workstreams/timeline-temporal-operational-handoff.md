# Timeline / Temporal-Operational — Workstream Handoff

- **Status:** B12 CLOSED / QUALIFIED USER ACCEPTANCE — B14+B07 active as one user-guided product/UI cycle; U1 Create-entry candidate awaits user visual proof; affected B12-D rerun unreported
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
