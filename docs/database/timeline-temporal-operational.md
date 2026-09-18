# Timeline / Temporal-Operational — Candidate Database Overlay

- **Status:** CURRENT CANDIDATE DATABASE AUTHORITY
- **Reconciled:** 2026-09-18
- **Branch:** `feature/timeline-temporal-operational`
- **Protected-main baseline:** `20260906_18` / `89|5|18|77|173|91|272|0|0|0`
- **Candidate head:** `20260917_29`
- **Candidate topology:** `101|5|31|78|198|119|297|0|0|0`
- **Whole-DB SoR:** `README.md`
- **Machine-readable authority:** `dictionary/`
- **Persistence doctrine:** `../development/backend-cp6-02-postgresql-persistence-constitution.md`
- **B03 closure authority:** `../workstreams/timeline-temporal-operational-b03-e-closure-2026-09-18.md`
- **Pre-B04 governance closure:** `../workstreams/timeline-temporal-operational-pre-b04-governance-2026-09-18.md`

## 1. Purpose and authority boundary

This file is the human-readable database overlay for Timeline candidate-only persistence. It exists so feature-branch schema truth is documented without rewriting candidate state as protected-main truth.

```text
protected main
  docs/database/README.md protected-main section
  + current protected-main architecture

Timeline candidate
  protected-main baseline
  + this overlay
  + Dictionary candidate tree/scope
  + candidate Alembic
  + SQLAlchemy
  + real PostgreSQL proof
```

Candidate truth becomes protected-main truth only after the applicable integration gates and protected-main merge/readback.

## 2. Candidate evolution

```text
20260906_18 protected-main baseline
    ↓
20260908_19 B01 Activity core
    ↓
20260909_20 → 20260915_26 B02 shared Schedule core/closure
    ↓
20260916_27 B03-A Event canonical core
    ↓
20260917_28 B03-B shared Event/Schedule activation
    ↓
20260917_29 B03-D Event Agenda; B03 candidate closure head
```

B03-C intentionally adds no Event-specific scheduling DDL. Event lifecycle reuses the shared Schedule capability.

## 3. Candidate objects/capabilities activated by the vertical

### Activity

```text
activity_intention
activity_create_operation
create_self_activity(...)
```

### Shared Schedule

B02 activates governed establishment, revision, current/history, unschedule and guarded Undo across the accepted placement union:

```text
date_span
floating_local
named_zone_local
absolute
coarse_local_period
```

Schedule remains a shared owner/capability; no Activity- or Event-specific placement engine is introduced.

### Event

```text
event_expectation
event_create_operation
event_agenda_part
event_agenda_current
event_agenda_mutation_operation
create_self_event(...)
create_self_event_with_agenda(...)
replace_self_event_agenda(...)
```

Event Schedule authorization is generalized against the existing shared Schedule owner. Agenda values remain Event-internal ordered content and do not receive NativeRef identity.

## 4. Non-collapse invariants

```text
Activity != Event
Activity != Schedule
Event != Schedule
Schedule != Temporal Constraint
Event != Recurrence != Occurrence
Schedule != Session != Actual
Actual != Outcome
Agenda part != Activity/Event/Occurrence/Schedule/Session/Actual
NativeRef != ScopedRecordRef != MaterialStateRef != ExternalRef
Schedule identity != placement MaterialState
current accepted state != newest row
operation/idempotency identity != Domain identity
provider identity != DANTE identity
```

## 5. Current proof state

```text
B01 ✅ CLOSED / PROVEN
B02 ✅ CLOSED / PROVEN
B03 ✅ CLOSED / PROVEN
B04 ⬜ NOT STARTED
```

The candidate structural authority is `_29` with topology `101|5|31|78|198|119|297|0|0|0`. B03 closure reconciled Dictionary, Alembic, SQLAlchemy/current catalog, ACL/direct PostgreSQL proof, API/client authority and product acceptance.

## 6. Binding same-change gate for B04+

Any Timeline change that affects persistence must update, in one reviewed slice, every affected representation:

```text
Domain / Logical / Physical authority when semantics change
→ Alembic forward revision when DDL is required
→ SQLAlchemy mappings / MetaData
→ Dictionary object entries + scope counts
→ current-catalog / owner / ACL proof
→ docs/database/README.md
→ this candidate overlay
→ direct PostgreSQL tests
→ affected map / roadmap / closure evidence
```

No slice can close with a known mismatch. No placeholder table/column/routine is added for future scope. No historical migration is rewritten. No candidate object is promoted in prose before it exists and passes its proof gate.

## 7. B04 entry condition

B04 has a frozen execution plan but has not started implementation. The entering database authority remains exactly:

```text
Alembic  20260917_29
Topology 101|5|31|78|198|119|297|0|0|0
```

The next implementation gate remains explicit: `APPROVE B04`.