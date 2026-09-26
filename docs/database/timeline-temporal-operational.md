# Timeline / Temporal-Operational — Candidate Database Overlay

- **Status:** CURRENT CANDIDATE DATABASE AUTHORITY — B10-C `_79` locally proven
- **Reconciled:** 2026-09-26
- **Branch:** `feature/timeline-temporal-operational`
- **Protected-main baseline:** `20260906_18` / `89|5|18|77|173|91|272|0|0|0`
- **Candidate source head:** `20260925_79`
- **Last proven candidate topology:** B10-C / `20260925_79` / `167|5|123|93|329|279|446`
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
20260925_70 B10-A guarded Actual realization authoring/read
    ↓
20260925_71 B10-A exact Activity/Event/Occurrence subject-family authority
    ↓
20260925_72 B10-A CP6 Actual/scoped-address owner-creation-order repair
    ↓
20260925_73 B10-A canonical family-aware function signatures
    ↓
20260925_74 B10-A current-history qualification + bounded receipt FK name
    ↓
20260925_75 → 20260925_78 B10-B Outcome
    ↓
20260925_79 B10-C Confirmation
```

Published migrations remain immutable. `_72`–`_74` and `_76`–`_78` are forward-only acceptance repairs. `_79` is the B10-C candidate.

## 3. Current candidate topology

```text
Alembic     20260925_79 candidate / 20260925_78 proven
Tables      167
Views       5
Routines    123
Triggers    93
Indexes     329
FKs         279
CHECKs      446
Enums       0
Domains     0
Sequences   0
Materialized/partitioned 0
RLS         0
```

User-run local PostgreSQL/application/catalog proof on 2026-09-25 passed at `_74`:

```text
14 passed in 25.06s
POSTGRES TEST EXIT: 0
```

The passing gate included B10-A realization/application/API behavior, B08 Session regression, B09 whole-block regression, current catalog reconciliation and whole-database cross-representation reconciliation.

## 4. Session persistence remains distinct

B08 reuses the existing CP6 Session identity/timing substrate:

```text
session
session_timing_state
session_timing_absolute
session_timing_elapsed
session_timing_pause
session_timing_current_history
```

Permanent boundaries remain:

```text
Schedule != Session
Session != Actual
Session != Outcome
Session END != Activity completion
Session END != Occurrence completion
planned Schedule duration != Session elapsed/active duration
```

Session START on an unplaced Activity remains valid and does not fabricate Schedule. Session END does not establish Actual or Outcome.

## 5. Existing Schedule authority remains unchanged

`dante.schedule` remains the sole accepted-placement authority. Actual realization is not a placement authority and does not mutate Schedule.

Deferred constraint families remain:

```text
TC-009 Session active-duration minimum → activated/proven in B08-C `_65`
TC-010 spacing/recovery             → later anchor-specific reopening
TC-011 relative before/after        → future bounded relation/reference review
```

## 6. Proof state

```text
B01–B06                              ✅ CLOSED / PROVEN
B08                                  ✅ CLOSED / USER-REPORTED / PROVEN SUBBLOCKS
B09-A `_66` persistence             ✅ CLOSED / PROVEN 2026-09-25
B09-B `_67`–`_68` authoring        ✅ CLOSED / PROVEN 2026-09-25
B09-C `_69` Person referents        ✅ CLOSED / PROVEN 2026-09-25
B09-D whole-block integration        ✅ CLOSED / USER-REPORTED 2026-09-25
B10-A `_70`–`_74` Actual core       ✅ CLOSED / PROVEN 2026-09-25
```

B10-A closure evidence is recorded in `../workstreams/timeline-temporal-operational-b10-a-closure-2026-09-25.md`. No B10-A real-app proof is required at this point; the integrated B10 real-app proof is deferred to B10-E.

## 7. B08-B / B08-C candidate database semantics

B08-B `_62`–`_64` reuses the CP6 Session timing substrate and returns elapsed, paused and active seconds from canonical timing and pause facts. It adds no parallel Session table.

B08-C `_65` activates `duration / session.active_duration` only for a soft minimum rule directly owned by an Activity. It reuses `temporal_constraint_state`, `temporal_constraint_duration_state`, the existing current-history envelope and the existing duration mutation capability. The evaluation is not persisted and never blocks Pause/Resume/End or creates Schedule/completion/Actual/Outcome.

## 8. B09 candidate database semantics

B09-A `_66` adds typed current relations:

```text
event_expected_participation
activity_responsibility
event_responsibility
```

B09-B `_67` keeps those tables default-deny and adds guarded mutation/read capabilities plus immutable operation receipts. `_69` admits the caller's self Person or an owner-local registered Person without creating Account identity.

```text
Responsibility != Participation
expected Participation != Actual / attendance
Person != Account
```

B09-D adds no new DB object.

## 9. B10-A Actual candidate database semantics — CLOSED / PROVEN

B10-A activates explicit realization over the existing CP6 Actual substrate rather than creating a parallel reality model.

Canonical owner/state family:

```text
actual
actual_realization_state
actual_realization_timing
actual_realization_session_basis
actual_realization_current_history
actual_current_realization
```

B10-A adds exactly one new persistent control table:

```text
actual_realization_operation
```

That table is an immutable self-scoped idempotency receipt. `operation_id` is not Actual identity.

Canonical guarded capability names at `_74`:

```text
_actual_subject_owned
_actual_subject_owned_as
record_self_actual_realization
get_self_subject_actual
list_self_actual_history
list_self_actual_session_bases
```

The Dictionary intentionally models one canonical routine per PostgreSQL `proname`. `_73` removed the hidden generic overloads introduced during the first acceptance iteration so live PostgreSQL and Dictionary remain exactly reconcilable.

### Exact subject contract

```text
Activity   → Actual subject ✅
Event      → Actual subject ✅
Occurrence → Actual subject ✅
Routine    → direct Actual subject ❌
Schedule   → Actual subject/owner ❌
Session    → Actual identity ❌
```

`_71` requires the requested family to match `native_address.owner_family` exactly before authoring or reading subject Actual.

### Actual realization contract

```text
Actual owner identity is stable per accepted subject realization context.
Realization state is append-only MaterialState truth.
Current accepted realization is explicit scoped current binding/history.
No Actual means unknown.
realization_occurred=false means known non-realization.
```

Optional realized timing is bounded to:

```text
instant
start_only
interval
```

Optional Session basis stores both:

```text
session_ref
session_timing_material_state_ref
```

and is accepted only when that exact Session timing state is evidence for the same subject.

### Runtime ACL

Runtime receives no raw mutation surface for the Actual realization family. Consequential mutation is behind `SECURITY DEFINER` capability functions. Actual realization tables/views retain only the read privileges required by the application where applicable.

### Acceptance repairs

The user-run local gate exposed and closed real database defects without weakening proof:

```text
_72  CP6 owner/scoped-address insert order
_73  exact Dictionary/live routine representation by removing hidden overloads
_74  PL/pgSQL output-column ambiguity in current-history correction
_74  canonical FK name below PostgreSQL identifier-length limit
```

Final proven B10-A topology remains:

```text
159|5|115|93|305|258|435
```

### Permanent B10-A boundaries

```text
Schedule != Session != Actual
Session END != Actual
Session evidence != Actual identity
Actual != Outcome != Confirmation
Expected outcome != Outcome
absence of Actual != known non-realization
current accepted state != latest row
provider/AI/solver != realization authority
```

## 10. B10-B Outcome — CLOSED / PROVEN

Proven chain `_75`–`_78`. Proven topology `163|5|119|93|317|268|440`.

```text
dante.outcome
dante.outcome_disposition_state
dante.outcome_disposition_current_history
dante.outcome_disposition_operation
facet: outcome.disposition
```

```text
one Outcome per Actual
disposition pinned to exact Actual realization MaterialState
current accepted Outcome state != latest row
Outcome != Confirmation
```

## 11. B10-C Confirmation — CLOSED / PROVEN

Proven revision `_79`. Proven topology `167|5|123|93|329|279|446`.

```text
dante.confirmation
dante.confirmation_attestation_state
dante.confirmation_attestation_current_history
dante.confirmation_attestation_operation
facet: confirmation.attestation
```

```text
Confirmation != Outcome
0..N Confirmation per exact Outcome disposition MaterialState
identity = (target MS, confirmer, purpose)
stance_code is contextual, not confirmed=true
Outcome correction does not transfer old Confirmation
```

## 12. Next database cursor

B10-C `_79` is locally proven. Do not start B10-D until the user approves that gate. Do not invent a generic Resolution entity.