# Timeline / Temporal-Operational — Candidate Database Overlay

- **Status:** CURRENT CANDIDATE DATABASE AUTHORITY — B10-D `_80` locally proven
- **Reconciled:** 2026-09-26
- **Branch:** `feature/timeline-temporal-operational`
- **Protected-main baseline:** `20260906_18` / `89|5|18|77|173|91|272|0|0|0`
- **Candidate source head / proven persistence frontier:** `20260926_80`
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
```

## 3. Proven frontier and topology discipline

B10-D functional persistence frontier is:

```text
Alembic 20260926_80
```

The B10-D closure proof did not include a newly recorded whole-database topology tuple. Therefore this overlay does **not** invent one. The last explicitly recorded whole-topology tuple remains the B10-C `_79` value:

```text
167|5|123|93|329|279|446
```

When a later catalog/topology gate records the `_80` tuple, update this document from evidence rather than arithmetic inference.

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

## 11. Current database cursor

B10-D `_80` is locally proven and closed. **B10-E is integration/acceptance**, not a planned new persistence family.

Do not add a generic Resolution, Decision, Verification or Provenance database owner merely to complete B10-E.

If the integrated B10-E proof exposes a real persistence defect, repair it with a new forward-only migration and re-run the affected database/catalog gates.
