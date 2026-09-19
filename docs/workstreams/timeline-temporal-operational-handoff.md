# Timeline / Temporal-Operational — Workstream Handoff

- **Status:** B03 ✅ CLOSED / PROVEN + pre-B04 governance ✅ FROZEN + B04-A ✅ CLOSED / PROVEN + B04-B ✅ CLOSED / PROVEN → B04-C NEXT
- **Reconciled:** 2026-09-19
- **Branch:** `feature/timeline-temporal-operational`
- **Current roadmap:** `docs/workstreams/timeline-temporal-operational-roadmap.md`
- **Current live map/ledger:** `docs/workstreams/timeline-temporal-operational-map.md`
- **B04 execution authority:** `docs/workstreams/timeline-temporal-operational-b04-execution-plan.md`
- **B04-A closure:** `docs/workstreams/timeline-temporal-operational-b04-a-closure-2026-09-18.md`
- **B04-B freeze:** `docs/workstreams/timeline-temporal-operational-b04-b-implementation-freeze.md`
- **B04-B closure:** `docs/workstreams/timeline-temporal-operational-b04-b-closure-2026-09-19.md`
- **Timeline candidate DB overlay:** `docs/database/timeline-temporal-operational.md`
- **CI:** no CI launch is implied or authorized

## 1. Current workstream position

```text
B00 Real Data Spine                              ✅ CLOSED / PROVEN
B01 Activity Core                                ✅ CLOSED / PROVEN
B02 Schedule Core                                ✅ CLOSED / PROVEN
B03 Event Core                                   ✅ CLOSED / PROVEN
PRE-B04 DB/API GOVERNANCE                        ✅ CLOSED / FROZEN
B04 Temporal Constraints + Movement Policy       🟡 IN PROGRESS
├─ B04-A Temporal Constraint canonical core      ✅ CLOSED / PROVEN
├─ B04-B Boundary / Deadline                     ✅ CLOSED / PROVEN
├─ B04-C Windows / Preferences / Evaluation      ⬜ NEXT
├─ B04-D Movement Policy                         ⬜
├─ B04-E Advanced-family applicability           ⬜
└─ B04-F Whole-B04 closure                       ⬜
B05 Product Organization                         ⬜
B06 Routine / Recurrence / Occurrence Baseline   ⬜
B07 UI/UX Consolidation v1                       ⬜
B08 Session Runtime                              ⬜
B09 Responsibility / Participation               ⬜
B10 Actual / Outcome / Confirmation / Resolution ⬜
B11 Advanced Recurrence / Conditional / Reminder ⬜
B12 Replanning / Conflict / Solver               ⬜
B13 Provider / Offline / Multi-device             ⬜
B14 Analytics / Statistics / Signals             ⬜
B15 Whole Vertical Closure                       ⬜
```

Current candidate DB:

```text
PostgreSQL 18.6
Alembic     20260919_34
Topology    107|5|34|85|212|129|309|0|0|0
```

## 2. Closed foundation

B03 remains fully CLOSED / PROVEN. Event is distinct from Activity and reuses one shared Schedule authority. Agenda remains Event-internal value truth. Postponed/TBD Event rediscovery remains explicitly transferred to B05 rather than collapsed into Planning Tray Activity semantics.

The pre-B04 governance closure remains binding:

```text
DB:
Alembic
≈ SQLAlchemy
≈ Dictionary + scope
≈ live catalog / owner / ACL
≈ current DB SoR
≈ Timeline DB overlay
≈ direct PostgreSQL proof
≈ workstream closure docs

API:
route/model
→ explicit stable semantic operationId for every new Temporal endpoint
→ exact Temporal inventory
→ OpenAPI snapshot
→ Orval / @dante/api-client
→ affected API/frontend tests
→ workstream docs
```

The 13 pre-B04 Temporal operationIds remain frozen compatibility baseline.

## 3. B04-A closure carried forward

B04-A established Temporal Constraint as a stable `ScopedRecordRef` LR-05 dependent, not NativeRef and not Schedule placement.

Its first complete rule remains valid inside the broader B04-B union:

```text
subject             self-owned Activity | Event
family              boundary
boundary kind       earliest_start
constrained facet   schedule.start
strength            hard | soft
temporal form       absolute
boundary             finite timestamptz
```

A1–A5 are CLOSED / PROVEN. Closure authority: `timeline-temporal-operational-b04-a-closure-2026-09-18.md`.

## 4. B04-B semantic closure

B04-B adds truthful latest bounds while preserving exact facet meaning.

Closed rule matrix:

```text
earliest_start     → schedule.start
latest_start       → schedule.start
latest_completion  → schedule.completion
```

Each rule is:

```text
family         boundary
strength       hard | soft
temporal form  absolute
value          finite timestamptz
subject        self-owned Activity | Event
```

Binding non-collapse:

```text
earliest_start != latest_start
latest_completion/deadline != Schedule end
passed deadline != Actual
passed deadline != Outcome / failure
constraint != placement
Temporal Constraint != Movement Policy
```

Date-only, floating-local, named-zone-local and coarse-local-period boundary forms remain unsupported in B04-B and must not be silently converted to absolute instants.

## 5. B04-B persistence authority

Candidate chain now continues:

```text
20260917_29 B03 closure
    ↓
20260918_30 B04-A Temporal Constraint core
    ↓
20260918_31 MaterialState totality hardening
    ↓
20260918_32 current-history dispatcher hardening
    ↓
20260918_33 Temporal Constraint API activation hardening
    ↓
20260919_34 B04-B absolute boundary / deadline
```

`_34`:

```text
widens constrained_facet_code to schedule.start | schedule.completion
widens boundary_kind_code to earliest_start | latest_start | latest_completion
keeps temporal_form_code = absolute
requires exact kind↔facet pairing in deferred totality
adds mutate_self_absolute_boundary_constraint(...)
preserves mutate_self_absolute_earliest_start_constraint(...) compatibility
```

No new table/view/trigger/index/FK/CHECK count is introduced. Current candidate topology:

```text
107 tables
5 views
34 routines
85 triggers
212 indexes
129 FK
309 CHECK
0 enums/domains
0 sequence/materialized/partitioned
0 RLS
```

## 6. B04-B application / API / generated contract

The same five Temporal Constraint operations remain public:

```text
Get Temporal Constraint
List Temporal Constraints by subject
Create Temporal Constraint
Revise Temporal Constraint rule
Retire Temporal Constraint
```

Existing explicit `temporal_*` operationIds remain stable. The request/response rule contract is a typed discriminated union:

```text
AbsoluteEarliestStart
AbsoluteLatestStart
AbsoluteLatestCompletion
```

CAS, idempotency, append-only rule history, current-vs-retired semantics and Activity/Event self scope remain unchanged.

Generated OpenAPI/client commit:

```text
3ca46c634411371d720b9ea1ed6600bce16b23da
feat(temporal): generate B04-B boundary API client
```

## 7. B04-B proof

Observed local proof:

```text
API / typed union / inventory                 13 PASS
PostgreSQL/application/catalog                22 PASS / 1 deselected
OpenAPI export/inventory/API                  21 PASS
@dante/api-client typecheck                   PASS
@dante/api-client Vitest                      11 PASS
pnpm generated:check                          PASS / 163 deterministic files
```

No frontend product surface was part of B04-B; no manual frontend userTest is claimed.

Closure decision:

```text
B04-B Boundary / Deadline constraints ✅ CLOSED / PROVEN
```

Closure authority: `timeline-temporal-operational-b04-b-closure-2026-09-19.md`.

## 8. Next slice — B04-C Windows / Preferences / Evaluation

B04-C is the next implementation slice and requires a new semantic/implementation freeze before any write.

Candidate territory:

```text
hard windows
soft preferred windows
start-within
completion-within
full-contained
overlaps
evaluation / violation explanation
```

Do not collapse:

```text
window != placement
preference != accepted Schedule
evaluation != solver decision
violation != automatic mutation
```

B04-C must decide exactly which temporal forms are supported. Lossless representation rules remain binding; unsupported forms fail closed.

## 9. Remaining B04 before B05

```text
B04-A canonical core                    ✅ CLOSED / PROVEN
B04-B Boundary / Deadline constraints   ✅ CLOSED / PROVEN
B04-C Windows / Preferences             NEXT
B04-D Movement Policy                   later
B04-E advanced-family applicability     later
B04-F whole-B04 closure                 later
```

B05 Product Organization starts only after B04-F closes.

## 10. Current gate

```text
B04
├─ B04-A ✅ CLOSED / PROVEN
├─ B04-B ✅ CLOSED / PROVEN
└─ B04-C ⬜ NEXT
```

**Immediate action:** re-open Domain / Logical / Physical / B04 execution authority for Windows / Preferences / Evaluation semantics and freeze the exact B04-C first slice before implementation.

CI remains separately authorized.
