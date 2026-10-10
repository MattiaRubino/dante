# Timeline / Temporal-Operational — Candidate Database Overlay

## B14 Session panel forward candidate — `20261009_135`

`_135` replaces the owner-scoped planned Session start admission check to allow an active untimed `planned` Schedule. It retains capture-policy enforcement, idempotent replay, linked provenance and Activity/role retirement protection. `list_self_open_activity_sessions(uuid)` reads only the actor's open Activity Sessions and their current timing, optional planned link and pause status. `list_self_session_panel_inputs(uuid)` composes owned Activity profiles, Schedules and open executions in one read. Both functions are DEFINER capabilities granting runtime EXECUTE; this migration adds no direct table grants. Candidate Dictionary topology: `237|5|220|103|484|420|593|0|0|0`. The user-local PostgreSQL gate reported 17 passed, including current catalog reconciliation, and one test failure caused by an incorrect assumption about a pre-existing runtime SELECT grant. The assertion was removed; the corrected gate remains to be rerun. See `docs/frontend/home/timeline-session-panel.md` for UI semantics and gate.

- **Status:** CURRENT CANDIDATE DATABASE OVERLAY — `_106` Activity intervals pending local proof
- **Reconciled:** 2026-10-05
- **Branch:** `feature/timeline-temporal-operational`
- **Protected-main baseline:** `20260906_18` / `89|5|18|77|173|91|272|0|0|0`
- **Current migration source head:** `20261005_106` (candidate; migration not locally proven)
- **Focused local proof frontier:** `_102` atomic/catalog 9 PostgreSQL tests and B08 minimum 1 test user-reported passed; `_103`–`_106` database gate unreported.
- **Later candidate stages:** `_94`–`_105` include B14/U6 work; `_106` extends `activity_schedule_role` with `interval` without changing table or routine counts. `planned` keeps its future Session meaning. See `../domain/decisions/activity-intervals-and-sessions-v2.md`. Current materialization totals in the Dictionary are unverified for `_106` until the user runs the local database gate.
- **Historical catalog topology:** `_93` / `196|5|155|100|397|344|497|0|0|0`. Current Dictionary counts are in `dictionary/scope.json`; `_106` has not been locally proved.
- **Whole-DB SoR:** `README.md`
- **Machine-readable authority:** `dictionary/`
- **Persistence doctrine:** `../development/backend-cp6-02-postgresql-persistence-constitution.md`
- **Current workstream map:** `../workstreams/timeline-temporal-operational-map.md`

## 1. Authority boundary

This is candidate-branch database truth, not protected-main truth. The authority chain remains:

```text
Product / Domain / Logical / Physical
→ PostgreSQL Persistence Constitution
→ candidate overlay + Dictionary
→ Alembic
→ SQLAlchemy
→ live PostgreSQL
→ direct proof
```

PostgreSQL remains canonical. API/client/frontend/provider/AI are projections and do not create a second truth model.

Published migrations are immutable. Any persistence correction is forward-only.

## 2. Candidate evolution

```text
20260906_18 protected-main baseline
    ↓
20260908_19 B01 Activity
    ↓
20260909_20 → 20260915_26 B02 Schedule
    ↓
20260916_27 → 20260917_29 B03 Event
    ↓
20260918_30 → 20260920_42 B04 Temporal Constraint + Movement Policy
    ↓
20260920_43 → 20260921_48 B05 Product Organization
    ↓
20260921_49 → 20260923_57 B06 Routine / Recurrence / Occurrence
    ↓
20260924_58 → 20260924_65 B08 Session Runtime
    ↓
20260925_66 → 20260925_69 B09 Responsibility / Participation
    ↓
20260925_70 → 20260925_74 B10-A Actual
    ↓
20260925_75 → 20260925_78 B10-B Outcome
    ↓
20260925_79 B10-C Confirmation
    ↓
20260926_80 B10-D Reconciliation
    ↓
20260926_81 B11-A advanced elapsed Recurrence
    ↓
20260927_82 → 20260927_85 B11-B conditional temporal intent/evaluation and forward-only read/qualification repairs
    ↓
20260927_86 B11-C personal Schedule Reminder candidate
    ↓
20260928_87 B13-A Plan work structure candidate
    ↓
20260928_88 B13-A replay projection and catalog check-name repair
    ↓
20260928_89 B13-A replace-current binding qualification
    ↓
20260928_90 B13-B Plan-qualified Dependency (focused PostgreSQL/catalog proven)
    ↓
20260929_91 B13-C Plan Step execution intent
    ↓
20260929_92 B13-C execution-policy CHECK-name repair (focused PostgreSQL/catalog proven)
    ↓
20260929_93 B12-C guarded reviewed candidate admission (focused local proof reported)
```

## 3. Proven frontier and topology discipline

B11-C focused functional persistence frontier is:

```text
Alembic 20260927_86
```

The local PostgreSQL `_86` probe measured the whole-database topology directly:

```text
184|5|144|100|370|323|480|0|0|0
```

At B11-C, Dictionary entries and current-catalog tests targeted `_86`. The first exact gate passed 8 tests and failed 2 on five CHECK names. After those names were aligned to the immutable migrations, both tests advanced to a missing registration of the five existing Outcome Reconciliation SQLAlchemy mappings. Registration at `3fe447af` completed 184 unique mappings; the user-run rerun of both exact catalog tests passed on 2026-09-27. B13-A subsequently advanced the current Dictionary/catalog target to `_89`, verified by its final local suite.

## 4. Permanent persistence boundaries

```text
Schedule != Session != Actual
Session != Actual != Outcome
Actual != Outcome != Confirmation
Confirmation != Reconciliation
current accepted state != latest row
MaterialState != mutable runtime object
idempotency operation receipt != Domain identity
```

`dante.schedule` remains accepted-placement authority. Session timing does not establish Actual. Actual does not establish Outcome. Outcome does not establish Confirmation. Confirmation does not grant reconciliation authority.

## 5. B08 Session persistence remains distinct

B08 reuses the CP6 Session timing substrate:

```text
session
session_timing_state
session_timing_absolute
session_timing_elapsed
session_timing_pause
session_timing_current_history
```

```text
START does not fabricate Schedule
END does not create Actual
END does not create Outcome
pause does not create a new Session
planned Schedule duration != Session active duration
```

## 6. B09 Responsibility / Participation persistence

Typed current relations introduced by B09:

```text
event_expected_participation
activity_responsibility
event_responsibility
```

B09-B guarded mutation keeps raw relation tables out of the runtime mutation surface. B09-C admits self or owner-local registered Person referents without collapsing Person into Account.

```text
Person != Account
Responsibility != Participation
expected Participation != Actual attendance
```

## 7. B10-A Actual — CLOSED / PROVEN

Canonical family:

```text
actual
actual_realization_state
actual_realization_timing
actual_realization_session_basis
actual_realization_current_history
actual_current_realization
actual_realization_operation
facet: actual.realization
```

Exact subject contract:

```text
Activity   → Actual ✅
Event      → Actual ✅
Occurrence → Actual ✅
Routine    → direct Actual ❌
Schedule   → Actual identity ❌
Session    → Actual identity ❌
```

```text
absence of Actual = unknown
realization_occurred=false = known non-realization
Session evidence != Actual identity
current accepted realization != latest row
```

Proven frontier:

```text
20260925_74
159|5|115|93|305|258|435
```

## 8. B10-B Outcome — CLOSED / PROVEN

Canonical family:

```text
outcome
outcome_disposition_state
outcome_disposition_current_history
outcome_disposition_operation
facet: outcome.disposition
```

```text
one stable Outcome per Actual
disposition pinned to exact Actual realization MaterialState
Actual correction does not reinterpret older Outcome disposition
current accepted Outcome state != latest row
```

The initial `_75` vocabulary/result representation is superseded by `_76`–`_78` and must not be reintroduced.

Proven frontier:

```text
20260925_78
163|5|119|93|317|268|440
```

## 9. B10-C Confirmation — CLOSED / PROVEN

Canonical family:

```text
confirmation
confirmation_attestation_state
confirmation_attestation_current_history
confirmation_attestation_operation
facet: confirmation.attestation
```

Stable identity:

```text
(outcome_disposition_material_state_ref, confirmer_person_ref, purpose_code)
```

```text
0..N Confirmation per exact Outcome disposition MaterialState
stance_code is contextual, not confirmed=true
absence of Confirmation != false
Outcome correction does not transfer Confirmation
```

Proven frontier:

```text
20260925_79
167|5|123|93|329|279|446
```

## 10. B10-D Reconciliation — CLOSED / PROVEN

Forward-only revision:

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

Resolver authority:

```text
Outcome owner is the only resolver in B10-D
Confirmation participation does not grant resolution authority
resolved_by_person_ref is state data, not owner identity
```

Exact evidence pinning:

```text
confirmation_ref
confirmation_attestation_material_state_ref
role_code = considered | selected
```

Every evidence state must belong to the exact Outcome disposition MaterialState being reconciled.

```text
Confirmation correction does not reinterpret prior reconciliation
Outcome correction does not transfer reconciliation
reconciliation correction appends a new MaterialState
prior evidence/history remains immutable
expected_material_state_ref guards current-state correction
operation receipt != reconciliation identity
```

Approved action codes:

```text
unresolved
select
accept_multiple
defer
escalate
```

B10-D local persistence/runtime/API proof:

```text
4 passed in 14.94s
```

Final generated/client/web/OpenAPI closure proof:

```text
web typecheck PASS
web controls 6/6 PASS
generated check PASS — 345 files deterministic/current
api-client typecheck PASS
backend B10-D/B10-C/OpenAPI inventory 6/6 PASS in 3.07s
```

Closure evidence: `../workstreams/timeline-temporal-operational-b10-d-closure-2026-09-26.md`.

## 11. B11-A Advanced Recurrence — focused local proof

Revision `_81` extends existing Routine/Event elapsed Recurrence with completion-relative Actual anchors and anchor-stream-relative provenance. It adds typed anchor state/operation relations and guarded generation functions; it does not create a second Recurrence owner, a fake Activity, or an implicit Schedule/Actual. The user reported the focused PostgreSQL/OpenAPI/web/generated-client gates passing. The whole-catalog Dictionary proof was not recorded at `_81`.

## 12. B11-B Conditional Temporal Behavior — focused local proof

Revisions `_82`–`_85` add `conditional_temporal_intent`, `conditional_temporal_evaluation`, `conditional_temporal_operation`, and guarded create/get/find/evaluate functions. `_83`–`_85` are forward-only corrections to published routines, not new Condition identities. Evaluation reads accepted-current Actual and pins the exact Actual MaterialState when known; `allow` never executes an effect. The user-run focused PostgreSQL (4), OpenAPI (6), web (3), generated check (361 files) and client/web typechecks passed; see `../workstreams/timeline-temporal-operational-b11-b-proof-2026-09-27.md`.

## 13. B11-C Reminder — proven frontier

B11-C `_86` adds a stable `schedule_reminder` owner keyed by self Person and Schedule, append-only `schedule_reminder_configuration_state` with shared MaterialState address/current binding, `schedule_reminder_current_history`, and `schedule_reminder_operation` for CAS/idempotency. Guarded PostgreSQL functions resolve self ownership, the accepted exact-start interval (absolute or resolved named-zone), and derived due/disposition. Runtime has execute grants on bounded get/configure functions and no direct table DML. Focused backend (5) and web (16) tests, generation and both typechecks passed locally; the `_86` catalog probe and both exact Dictionary/catalog tests passed with the measured tuple above. This slice creates no delivery job or Actual mutation. Whole B11 is closed with user-reported real-app acceptance.

## 14. B13-A Plan work structure — focused proof closed

Forward-only `_87` reuses the Plan NativeRef identity shell and introduces self ownership, internal Plan-owned Steps, immutable normalized structure revisions, explicit accepted-current binding/history and replay-safe operations. Step order is a presentation sequence, not Dependency. An optional link to an existing self-owned Activity preserves the Activity's separate identity and lifecycle. The runtime has execute grants on four guarded read/write functions and no direct DML grants on the seven new tables.

The `_87` local test reached the expected topology `191|5|148|100|386|334|488|0|0|0` but exposed one replay projection error and eight check identifiers that did not match the Dictionary. `_88` repaired those names and the function; forward-only `_89` qualified an ambiguous `plan_ref` in the replace-current update. Neither changes topology. The final user-run focused PostgreSQL and exact Dictionary/catalog suite passed **9 tests in 24.09s** at `_89`. See `../workstreams/timeline-temporal-operational-b13-a-closure-2026-09-28.md`.

## 15. B13-B Plan-qualified Dependency — CLOSED / PROVEN

Forward-only `_90` introduces five Plan-scoped relation/current/history/operation tables and four guarded capabilities. The relation preserves direction, immutable Step-to-Activity endpoint bindings, explicit dependent admissibility purpose and typed Actual/Outcome qualifier. Current evaluation is derived from accepted Actual/Outcome truth; stale Outcome basis is unknown. An active endpoint guard is added to the existing Plan replacement function; the scoped owner dispatcher is extended to the bounded `plan_dependency` family.

The Dictionary/catalog topology is verified at `_90`: `196|5|152|100|397|344|496|0|0|0`. The user-run focused PostgreSQL capability and exact catalog suite passed **11 tests in 41.75s** on 2026-09-29. `_90` was the B13-B persistence frontier; B13-D remains the whole-B13 integration/acceptance gate.

## 16. B13-C Plan Step execution intent — CLOSED / focused proof

Forward-only `_91` adds four nullable execution-policy columns and one coherent-tuple CHECK to the existing immutable `plan_step_in_state`. It patches guarded `get_self_plan_work` and `replace_self_plan_work` with exact anchors, retaining B13-A ownership/current-history/replay and B13-B active Dependency endpoint protection. The first user-run gate passed 10 of 13 PostgreSQL tests but exposed a duplicate naming-convention prefix on the CHECK and a stale catalog-probe revision assertion. Forward-only `_92` renames the physical CHECK to the Dictionary/ORM identifier; the probe expects `_92`. No table, routine, view, trigger, index or FK is added by the repair. The user-run complete focused PostgreSQL B13-A/B/C and exact catalog suite passed **13 tests in 29.16s** at `_92`, asserting the live schema against the Dictionary, ORM and `196|5|152|100|397|344|497|0|0|0` topology target. B13-C is closed on focused proof. See `../workstreams/timeline-temporal-operational-b13-c-closure-2026-09-29.md`; whole-B13 acceptance remains B13-D.

## B12-C reviewed candidate admission checkpoint

Forward-only `_93` adds three owner-controlled, security-definer functions: an internal current-evidence guard, a self-scoped B04-D request delegate, and a self-scoped B04-D confirmation delegate. The guard serializes Plan/Dependency changes on the Plan row, locks current Policy and relevant Actual/Outcome/Constraint evidence, and checks exact Schedule, Plan Step and evidence state before calling B04-D in the same transaction. No new table, view, index, trigger or constraint is introduced; Dictionary/catalog target is `196|5|155|100|397|344|497|0|0|0`. The user reported a passing focused local PostgreSQL gate (19 tests in 39.83s); the pasted transcript does not echo the exact final file selection. See the qualified closure evidence in `../workstreams/timeline-temporal-operational-b12-c-closure-2026-09-29.md`. See `../workstreams/timeline-temporal-operational-b12-c-implementation-2026-09-29.md`.
# B14-U6 candidate read projection (2026-10-02)

Forward revision `20261002_96` adds only `dante.list_self_resolution_queue(uuid)`.
It exposes current unresolved B10 Reconciliations for self-owned Activity/Event
through a bounded SECURITY DEFINER read. It creates no queue table and does not
infer skipped or failed execution from elapsed Schedule time. This is a candidate
until the user reports the local PostgreSQL gate. The rest of U6 persistence is
not claimed by this revision.

## B14 M1-B recurring edit inventory read (2026-10-08)

Forward-only candidate `20261008_122` adds
`dante.list_self_recurrence_edit_occurrences(uuid,uuid)`: selected
Occurrence ownership through B06 `get_self_occurrence`, all
already-materialized same-source Occurrences (including current
Schedules, skip states and explicit extras), and a hard 10,000 row
cap that **raises** instead of truncating. This is a SECURITY DEFINER
STABLE read, grant-only EXECUTE to `dante_runtime`; no table grants,
no new stored history, no source rewrite. The API is read-only and
marks both its materialized-only coverage and lack of apply authority.
Dictionary/canonical catalog candidate: `231|5|197|103|471|405|572`.
Implementation is not PostgreSQL-proven until the user's local gate;
M1-C atomic CAS/apply remains open.

## B14 M1 _123 scoped occurrence metadata edit (2026-10-08)

New **candidate** forward revision `20261008_123` has one
append-only, owner-keyed `occurrence_profile_edit` ledger table
and five SECURITY DEFINER functions. Owner/Source row locks,
Recurrence-current state row lock, edit CAS revision, idempotent
operation replay, fixed accepted_at and typed Occurrence coordinates
govern the selected anchor and additional future only. Already-past
neighbors never enter effective policy. Accepted Actual and Objective
observations on future materialized instances are conflict guarded;
no historical recorded facts are deleted. Effective Activity metadata
and Event/Activity Timeline titles are derived from the log; new
Routine-derived Activity instances inherit applicable future metadata.
Runtime gets function EXECUTE, no ledger table DML.

Dictionary/canonical catalog target is
`232 tables / 5 views / 202 routines / 103 triggers / 473 indexes /
408 FK / 576 CHECK`, ORM adds one table mapping. Existing
`get_self_activity_profile` function is replaced with the same
return signature and PARALLEL RESTRICTED effective projection.
_123 and client generation/whole user local gate are pending.
Metadata edit semantics are not a license to overwrite other
domain owners' Session, Objective, Schedule, Event agenda or
Reality histories.

## B14 M1 _124 guarded Activity Inspector read (2026-10-08)

_123 local gate showed four B14 Activity profile read/edit
failures because a planner-inlineable LATERAL WHERE guard
did not prevent calling the strict self-Occurrence accessor
with a NULL Occurrence on one-off Activities. The function
correctly rejected missing ownership; the caller was
incorrect. Forward _124 replaces existing
`get_self_activity_profile(uuid,uuid)` with a branch-executed
PL/pgSQL owner read that only invokes the scoped patch
accessor on a real canonical materialized Routine Occurrence.
Returns no row for non-self, missing or retired Activity.
Activity Timeline uses a CASE guard on the analogous path.
No new database objects: physical topology remains
232 tables, 5 views, 202 routines, 103 triggers, 473 indexes,
408 foreign keys, 576 CHECK. Dictionary reflects the
existing profile function language change SQL -> PL/pgSQL.
User-run _124 gate pending. No previous materialized
Occurrence/Actual history changes.

## B14 M2 canonical Objective revision/correction and generated series scope (_125/_126)

_125 adds append-only `temporal_objective_definition_revision` and grants owner-validated SECURITY DEFINER functions for current same-`objective_ref` definition, optimistic-CAS/idempotent revision and corrected-result Observation/Evaluation. New definition re-evaluates existing factual numeric/boolean Observation with the accepted target, appends a new Evaluation only when changed, and preserves the historic observation and previous Evaluation states. Qualitative manual judgments are never invented. Replacing the existing Objective result function ensures subsequent results use the current corrected definition, not an obsolete target.

_126 adds append-only `temporal_objective_series_edit` keyed by immutable materializer template slot and recurrence source revision. Owner/source-lock CAS, acceptance instant and selected-anchor coordinate target the selected generated Objective plus later future; other already-past instances remain unchanged. Overrides, skipped Occurrences, Actual and future Observations are conflict guarded before apply. New instances inherit the accepted definition by effective read. Unlike template definition inheritance, recorded Observation is never propagated to an unobserved future Objective. One-off/individual Objective edit is selected-only, avoiding unsupported implicit lineage. Runtime gets only function EXECUTE, never direct ledger DML. Exact _126 catalog candidate: **234/5/207/103/477/414/586**. Both migrations are forward-only; user-run focused PostgreSQL, canonical Dictionary and Web/API gate PENDING.

## 2026-10-08 — _126 live local catalog gate remains failing

The user's third M2 combined local gate **successfully migrated PostgreSQL through `20261008_125` and `20261008_126`** and ran 20 focused PostgreSQL tests: **16 passed / 4 failed**. One failure is `tests/integration/database/test_database_current_catalog.py::test_current_database_cross_representation_is_exact`; the other three are new Objective correction and Routine/Event recurring series integration tests. Therefore `234 tables / 5 views / 207 routines / 103 triggers / 477 indexes / 414 FK / 586 CHECK` is still an **expected Dictionary topology, not locally confirmed exact parity**. The shared log omitted the failure tracebacks; read the existing full `/tmp/dante-m2-final.2m48YP/POSTGRES.log` before making a schema or Dictionary correction. Ruff I001 for the Objective ORM import block was corrected separately in GitHub `1ff3e500` and awaits local confirmation. API generation, deterministic generated-source check, both TypeScript typechecks and Vitest all passed, with generated source still local/unpublished. Do not add arbitrary forward migrations, relax owner/CAS invariants or declare `_126` catalog verified without the complete exact mismatch report.

## 2026-10-08 — M2 third PostgreSQL failure forensics and four-source fixes

The user supplied the **full `FAILURES` section** from `/tmp/dante-m2-final.2m48YP/POSTGRES.log`. Concrete root causes were confirmed, rather than guessed:
1. `test_objective_definition_and_result_corrections_are_canonical_without_deletion`: all actual HTTP recording/definition/replay/CAS checks reached their expected status; the last assertion incorrectly expected JSON numeric `6` instead of the contract's Decimal serialization string `"6"`. Test now uses `Decimal(str(...))`. The same test's subsequent internal-audit query was also preemptively repaired to use the **isolated test administrator**; `dante_runtime` must not gain raw Observation/Evaluation table SELECT.
2. `test_generated_routine_objective_scope_selected_past_and_later_future`: test setup generated a `floating_local` recurrence, but the real recurring-Activity template materializer requires an actual `named_zone` wall time and zone. Test now uses a named-zone daily recurrence (`Europe/Rome`, explicit DST policies); production materializer unchanged.
3. `test_generated_event_objectives_share_future_scope_without_copying_results`: the test attempted direct SELECT on `dante.temporal_objective` under `dante_runtime` and correctly received `InsufficientPrivilege`. Both Event and Routine tests now read **replayable B06 checkpoint identities**, linked Activity refs via `dante.list_self_routine_occurrence_activities`, and Objective refs through `dante.list_self_temporal_objectives`. Removed all raw protected-table SELECTs from the routine/event Objective-scope test; production owner ACL unchanged.
4. `test_current_database_cross_representation_is_exact`: the final ORM registry count assertion still expected 232 tables even though mapping, dictionary and live catalog all enumerate **234**. Changed only stale test literal to 234.

All fixes committed/pushed on `feature/timeline-temporal-operational` (not CI): `fae4dcbf`, `b72d7f2b`, `470fde9d`, `61dd6913`, `b5c55489`. Post-edit branch readback verified single Objective mapping classes, correct fingerprints, no test table-policy bypass, and all four corrections. **These edits have not yet been subjected to the next user-run local gate; M2 is NOT closed.** DB expected revision `20261008_126` and topology `234/5/207/103/477/414/586` remain unchanged; no speculative migrations and no role grants. Rerun the whole focused Ruff + PostgreSQL/catalog + generated API/check + API/Web TS typechecks + Vitest gate once. If green, stage and publish only deterministic generated client files, then record M2 closure. M3/M4/M5/B15 remain open.

## 2026-10-08 — M2 _126 Dictionary and PostgreSQL exact-catalog gate GREEN

Supersedes the earlier `_126 live local catalog gate remains failing` status (retained as historical investigation). User local consolidated M2 gate after pulling `b1599c19` reported `POSTGRES=0` and all syntax/Ruff/generated/API-client/web/Vitest checks `=0`. The focused suite includes `test_current_catalog.py` and `test_database_current_catalog.py`, which no longer fail after the corrected ORM count expectation and ownership-respecting test setups. Therefore the **focused exact-catalog verification passed** for revision `20261008_126`, expected physical topology `234 tables / 5 views / 207 routines / 103 triggers / 477 indexes / 414 FKs / 586 CHECK`. Objective correction/series append-only history and callable self-scope remain intact; no runtime raw-table grants or schema workaround was added. Canonical API client generated deterministically and successfully pushed in `09dc26f9`. Do not misstate this as independent full B15 database/security or real-app proof. M3 must inspect existing B08 Session / B05 Life Area / Schedule and Reminder owners before any forward migration; no new schema solely to mirror already-existing capabilities.

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

## 2026-10-08 — _127 canonical catalogue green on M3 user-local focused gate

The prior `21 PASS / 5 FAIL` record is historical only. User reran the consolidated complete M3 WSL gate after pulling `d09af8a0`: `SYNTAX=0 RUFF=0 POSTGRES=0 GENERATE=0 GENERATED_CHECK=0 API_TYPECHECK=0 WEB_TYPECHECK=0 VITEST=0`, and published the generated client in `6fdda05f` (`PUBLISH_EXIT=0`). The PostgreSQL suite includes the exact `test_current_catalog.py` and `test_database_current_catalog.py` checks and legacy B05 / B14 / M2 regressions. Thus revision `20261008_127` **passes focused exact DB catalog** at expected 234 tables / 5 views / 208 routines / 103 triggers / 477 indexes / 414 FK / 586 CHECK (standalone 447). The new nullable Life Area has owner/CAS/idempotent receipt semantics; planned Session name change preserves Schedule identity; retiring an Activity refuses already recorded truth. **No claim of independent B15/full production DB review or broad recurring-template inherited field acceptance.**

## 2026-10-08 — M3-B owner-domain scope integrity candidate (no migration)

After M3-A user-green `_127` gate and published generated client `6fdda05f`, M3-B review of the actual Domain/Logical/Physical contracts, `routine_occurrence_materialization.py`, M1 `_123` and M2 `_126` established **no canonical following-series policy for Life Area or planned Session labels**. Routine materializer reads the owner's Life Area from `list_self_routines`; planned Session labels are copied from `routine_occurrence_policy.activity_template.planned_slices[].name`. Following edits cannot be safely implemented as a loop over already materialized Activity/Schedule rows: that misses future checkpoint instances and breaks owner/source CAS and historical exceptions. Routine/Event source semantics differ; do not imply parity without proof. The detailed negative-scope acceptance plan is in `docs/workstreams/timeline-temporal-operational-m3-b-owner-scope-2026-10-08.md`.

**Implemented on GitHub, newly UNTESTED:** the Activity editor now treats pending planned Session names as dirty and blocks general save and replan preview/apply until individually saved; after successful replanning it rebuilds the planned-name baseline. The recurring scope controls are visible even for Life Area/name-only drafts but disable `Questa e le prossime` when there is no supported metadata change, with explicit owner-domain-only guidance. Unsupported temporal Schedule forms are left untouched, with a non-conversion explanation. The remote Activity Inspector displays the recorded-truth retirement veto specifically instead of a generic stale conflict. Focused Vitest cases were added for draft loss, replan coexistence, recurring Life Area and Session name scopes, unsupported absolute temporal form, and retirement error/invalidation.

**State:** M3-A remains technically green; **M3-B candidate UI/guard implementation needs a fresh user-local Web typecheck and focused Vitest gate**. M3-B following-source implementation remains open: a new source policy must protect original selected Occurrence, future not-yet-generated occurrences, stable planned-template slot identity, independent per-instance edits, skip/Actual/recorded Session/Observation, owner and recurrence CAS; no such source policy is claimed or silently emulated. No new migrations or Dictionary topology changes: still `20261008_127` and `234/5/208/103/477/414/586`. M4/M5/B15 remain open. No GitHub Actions/CI; user runs local gate.

## 2026-10-08 — M3-B UI/negative-scope guard subvertical locally GREEN

**Latest acceptance supersedes earlier M3-B "pending Web recheck" entries.** The user pulled `b03d8aa4` into WSL `~/projects/dante` and ran the focused Web recheck: `WEB_TYPECHECK=0`, `VITEST=0`, 4 test files / **36 tests passed** (Activity Inspector UI 23, Remote Inspector 3, Remote Activity Settings 7, Remote Recurring Profile 3). Log directory `/tmp/dante-m3b-web-final.L8HfvO`. The preceding combined M3-B gate had already passed `SYNTAX=0`, `RUFF=0`, `POSTGRES=0` (including the new negative future-checkpoint Routine test and prior M3-A/M2 regression), `GENERATED_CHECK=0`, `API_TYPECHECK=0`; after these, **all bounded M3-B guard checks are proven green locally**. No schema/client change after the original backend green run; final Web fix was test-only `23daae86`. No new API generation or client publication required.

**CLOSED as bounded technical work:** M3-B editor safeguards, explicit individual-only mode, unsaved planned-name replan/save protection, truthful incompatible temporal-form UI, recorded-fact retirement reporting, and negative no-implicit-following provenance proof. **NOT CLOSED:** M3 following-source policy for optional Life Area or planned Session names of recurrence-derived Activity/Event Occurrences. `Questa e le prossime` remains explicitly disabled for these owner-domain fields. Future and already materialized later instances require an owner-authoritative policy, source CAS, immutable operation replay and template slot provenance. M1, M2 and M3-A remain green; broader M3 open. M4 (Event Inspector / faithful Activity/Event duplication), M5 product UI acceptance and B15 closure open. Next work: read actual Routine/Event Domain/Logical/Physical and M1/M2 source policy implementations and implement bounded canonical source policy, then one user-local gate. No CI/Actions.

## 2026-10-08 — M4 whole-block candidate assembled; ONE user-local gate outstanding

The M4 Event post-create edit/duplicate vertical is assembled on the GitHub branch. This entry **supersedes the earlier incomplete-M4 candidate cursor**; no local tests are claimed for the newly added code. New canonical `20261008_128_b14_m4_event_profile.py` (only one Alembic `_128` revision) owns immutable Event metadata revision history, actor/CAS/replay, with an explicit no-unscoped-recurring-source edit veto. The Event read exposes a canonical profile revision. `event_api.py` accepts guarded Event metadata edits. Event Inspector now supports metadata Title/Description/Location/Color, existing B03 Agenda, B05 Life Area and B09 Participation owners without forging replacements for them. One new integration test `test_b14_m4_event_profile.py` covers owner, CAS, replay, history and current read.

Event Duplica uses canonical persisted Schedule placement and per-Event details, Life Area and expected participants. The Event DST disambiguation now retains the resolved earlier/later fold; cross-fold, invalid clock precision and absolute forms without faithful Create representation are rejected, never silently normalized. A new owner-scoped `remote-event-recurrence-guard.ts` checks the authoritative Event Recurrence before Duplicate, and explicitly blocks unfaithful template-to-one-off conversion; unresolved participants likewise block. Activity Duplica checks authoritative persisted child count and occurrence provenance, not just displayed subitems, and refuses structures/series that cannot be fully reconstructed, preserving all existing Actual/Observation/Evaluation/Session history. These refusals are **known capability limits**, not claims of full copying of complex trees or series.

**Canonical DB target _128:** 235 tables, 5 views, 210 routines, 103 triggers, 479 indexes, 416 FKs, 587 CHECK. Dictionary scope/routine/table and exact current catalog expectations are updated. Backend+Web tests added/extended; OpenAPI/Orval generation for the new Event profile endpoint still needs publication from user-local checkout, not a manually authored generated client.

**Single consolidated verification:** user runs `bash tooling/verify-b14-m4-local.sh` in `~/projects/dante`, with PostgreSQL, Ruff, unit, API export/client determinism, TS and relevant Vitest. Logs and concise result codes remain visible; the script conditionally publishes **only** verified generated client files after all gates pass, with no CI/Actions. If red, fix all real failures before another whole-block gate; no micro-gates. M4 is **candidate / awaiting this one local gate**, not green. Then perform M5/B15 real-UI click-through; the separate M3 global `Questa e le prossime` owner-source policy for Life Area and planned Session labels remains an explicit B14 parity debt before B15. No misleading "fully complete" claim.


## 2026-10-09 — M5 Objective editor one-save candidate; local verification required

The user requested direct editing of existing Objectives by expanding their row, a single **Salva modifiche** after adding/changing/removing Objectives (no intermediate confirmation), and an **×** removal affordance per row. The branch candidate implements these in `apps/web/src/features/home/ui/timeline/activity-objective-row.tsx`, `activity-edit-panel.tsx` and their style/tests. The previously separate Objective definition actions were folded into Activity Edit submit. Draft additions have no server side effects until the final Save; removal is staged and undoable. Recorded-result correction remains a separate factual-history operation and was not silently rewritten as a definition edit.

The new **Objective-only** `PUT /api/v1/temporal/activities/{subject_ref}/objective-edits` API uses a *single SERIALIZABLE database transaction* to apply all newly authored, revised and retired Objective definitions. It uses existing owner-scoped Objective create/revision/source-policy functions; the new forward-only `20261009_133_b14_objective_retirement.py` adds a retirement tombstone and an owner-scoped function with definition CAS, replay and veto of any recorded Observation/Evaluation or template-generated recurring Objective. Retired Objectives remain in historical storage, but active read/definition capabilities no longer return them. The database Dictionary, SQLAlchemy mapping and exact-catalog expectations have been reconciled to `20261009_133`: **236 tables / 5 views / 215 routines / 103 triggers / 482 indexes / 420 FKs / 589 CHECK**, standalone **456**. New Objective batch command and precise veto response are in `reality_objective_api.py`.

The remote Web Objective batch call has a bounded 20s timeout, stable per-row operation IDs and retained CAS basis for retries. The general Activity Save visually drives the Objective batch without extra buttons. **Important domain boundary:** the batch is atomic *among Objective changes*; other domain-owned edits on the same Activity continue using their established guarded commands and are **not a single cross-domain database transaction**. Do not claim a global atomic Activity save. Unsupported source-wide deletion is refused, and a recorded Objective cannot be erased. Existing selected/following Objective definition scopes remain available only with verified template provenance; the unrelated Life Area/planned Session following-source parity debt remains open.

**Current status: CODE/TEST/DOCUMENTATION CANDIDATE ONLY; ZERO NEW USER-LOCAL PROOF.** The preceding `_132` M5 PostgreSQL selection passed **26/26** in the user's WSL, but this new `_133` candidate is not covered by those 26 tests. Run **one complete local gate** via `bash tooling/verify-b14-m5-objectives-local.sh` on `~/projects/dante` (Ruff, syntax, PostgreSQL new Objective batch/history and existing regression/catalog, deterministic generated API, API/Web typechecks and focused Vitest). The script does not commit/push and does not trigger CI/Actions. A new OpenAPI/Orval client artifact is expected from `pnpm api:generate` and must be published only after a green gate; never hand-edit generated files. Follow with real-app visual/keyboard acceptance including the earlier Objective white-page report. Neither M5 nor B15 is closed.


### 2026-10-09 — B14 Draft Vault («Bozze») whole-block implementation CANDIDATE

User-approved product shift: retire “Da collocare” as an *authoring choice*; introduce an actor-owned inert Draft Vault for possible future Activity and Event, with full Quick/Advanced Create field snapshots (including uncommitted Session/Objectives/recurrence settings). `Salva bozza` beside `Aggiungi` in both Create surfaces; discard dialog now offers Save draft. Explicit Add authors accepted subject through the existing path; the original draft is removed only after success. Resume and Duplicate reopen the same Create editor; Delete removes inert snapshot. Drafts do **not** establish Activity/Event/Schedule/Session/Actual/reminders or recurrence: see `docs/domain/concepts/draft-vault.md`.

New *forward-only* PostgreSQL `20261009_134` adds `dante.temporal_draft_vault` owner-only table and 3 SECURITY DEFINER CAS/replay/list/delete functions with dante_runtime EXECUTE but no direct table privileges. New `/api/v1/temporal/drafts` authenticated API, TypeScript remote source, Home vault panel, Create integration and tests. Updated Dictionary/SQLAlchemy/catalog to **candidate 237 tables, 5 views, 218 routines, 103 triggers, 484 indexes, 420 FKs, 593 CHECK constraints** (new table + 3 funcs + 1 PK index + 4 CHECK). **Counts are expectations, not user-proven until PostgreSQL gate.** OpenAPI/Orval generated API client files must be published separately after deterministic generation. Local full affected gate scripted in `tooling/verify-b14-draft-vault-local.sh`, no CI or automatic push.

**Historical protection and gaps, explicitly OPEN:** the old planning tray holds *real* canonical unplaced/postponed Activity/Event identities. These remain distinct legacy canonical records, not silently moved or deleted as drafts; the vault exposes an explicit **Gestisci elementi già creati** handoff to the unchanged B01 placement/replan controls under a separately titled **Elementi già creati** panel (its old trigger is hidden). Inspector “Sposta in Bozze” for Activity uses existing canonical retirement guard, preserving history; moving real Event is **not yet supported** because Event has no matching safe retirement capability, so the Event Inspector visibly says “Copia in Bozze” and keeps the original. Do not treat this as Move or mark the full legacy transition accepted. Full Event move needs explicit follow-up owner-retirement capability without corrupting accepted facts. User visual and end-to-end acceptance remains **NOT VERIFIED**, including real app, keyboard interactions, and previous M5 regression checks. No new Timer/Alarm operational functionality. Avoid claiming B14/B15 or Bozze closed.

**User workflow:** Assistant writes and updates `feature/timeline-temporal-operational`; user performs explicitly displayed `git pull --ff-only origin feature/timeline-temporal-operational` in WSL. User runs a SINGLE COMPLETE local gate; do not request CI. User is not asked to push source changes except genuinely local generated OpenAPI artifacts that cannot be read by the connector.
