# Timeline / Temporal-Operational — Candidate Database Overlay

- **Status:** CURRENT CANDIDATE DATABASE OVERLAY — B11-B `_85` source head; catalog reconciliation open
- **Reconciled:** 2026-09-27
- **Branch:** `feature/timeline-temporal-operational`
- **Protected-main baseline:** `20260906_18` / `89|5|18|77|173|91|272|0|0|0`
- **Candidate migration source head:** `20260927_85`
- **Focused local proof frontier:** B11-B `_85` (not a whole-catalog count)
- **Last explicitly recorded whole-topology count:** B10-C `_79` / `167|5|123|93|329|279|446`
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
```

## 3. Proven frontier and topology discipline

B11-B focused functional persistence frontier is:

```text
Alembic 20260927_85
```

Neither the B10-D nor B11-A/B closure proof recorded a newly measured whole-database topology tuple. Therefore this overlay does **not** invent one. The last explicitly recorded whole-topology tuple remains the B10-C `_79` value:

```text
167|5|123|93|329|279|446
```

The Dictionary and catalog-test revision still point at `_79`; reconcile all real objects and ACLs through `_85` (and the following B11-C migration) before claiming whole-catalog agreement. Update this document from measured evidence rather than arithmetic inference.

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

## 13. Current database cursor

B11-C is the approved next forward-only persistence step after `_85`. Reconcile the Dictionary and current catalog with the actual B10-D/B11-A/B/C objects and their PostgreSQL ACLs. Do not promote the `_79` topology to a later revision without a direct catalog measurement.
