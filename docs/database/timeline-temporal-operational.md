# Timeline / Temporal-Operational — Candidate Database Overlay

- **Status:** CURRENT CANDIDATE DATABASE OVERLAY — B13-C `_92` repair pending PostgreSQL retest; B13-B `_90` proven
- **Reconciled:** 2026-09-29
- **Branch:** `feature/timeline-temporal-operational`
- **Protected-main baseline:** `20260906_18` / `89|5|18|77|173|91|272|0|0|0`
- **Current migration source head:** `20260929_92` (B13-C repair candidate, unverified)
- **Focused local proof frontier:** B13-B `_90` (11 PostgreSQL/catalog tests passed in 41.75s)
- **Catalog-verified whole-topology count:** `_90` / `196|5|152|100|397|344|496|0|0|0`
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
20260929_91 B13-C Plan Step execution intent (candidate, unverified)
    ↓
20260929_92 B13-C execution-policy CHECK-name repair (candidate, unverified)
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

The Dictionary/catalog topology is verified at `_90`: `196|5|152|100|397|344|496|0|0|0`. The user-run focused PostgreSQL capability and exact catalog suite passed **11 tests in 41.75s** on 2026-09-29. `_90` is the current persistence frontier; B13-D remains the whole-B13 integration/acceptance gate.

## 16. B13-C Plan Step execution intent — candidate, PostgreSQL proof pending

Forward-only `_91` adds four nullable execution-policy columns and one coherent-tuple CHECK to the existing immutable `plan_step_in_state`. It patches guarded `get_self_plan_work` and `replace_self_plan_work` with exact anchors, retaining B13-A ownership/current-history/replay and B13-B active Dependency endpoint protection. The user-run gate at `_91` passed 10 of 13 PostgreSQL tests, including B13-C behavior, but exposed a duplicate naming-convention prefix on the CHECK and a stale catalog-probe revision assertion. Forward-only `_92` renames the physical CHECK to the Dictionary/ORM identifier; the probe now expects `_92`. No table, routine, view, trigger, index or FK is added by the repair. The Dictionary predicts `196|5|152|100|397|344|497|0|0|0`; this is not a measured catalog tuple. Exact catalog proof and closure remain pending the `_92` retest. The last fully verified PostgreSQL frontier remains `_90`. See `../workstreams/timeline-temporal-operational-b13-c-implementation-2026-09-29.md` for the proposed-slice basis, capability ledger and measured gate.
