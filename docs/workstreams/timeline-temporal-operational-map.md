# Timeline / Temporal-Operational Vertical — Semantic Work Map / Live Ledger

- **Status:** CURRENT SEMANTIC MAP + LIVE IMPLEMENTATION LEDGER — reconciled 2026-09-19
- **Branch:** `feature/timeline-temporal-operational`
- **Roadmap:** `docs/workstreams/timeline-temporal-operational-roadmap.md`
- **B03 closure:** `docs/workstreams/timeline-temporal-operational-b03-e-closure-2026-09-18.md` ✅ CLOSED / PROVEN
- **Pre-B04 governance closure:** `docs/workstreams/timeline-temporal-operational-pre-b04-governance-2026-09-18.md` ✅ CLOSED / FROZEN
- **B04 execution plan:** `docs/workstreams/timeline-temporal-operational-b04-execution-plan.md`
- **B04-A closure:** `docs/workstreams/timeline-temporal-operational-b04-a-closure-2026-09-18.md` ✅ CLOSED / PROVEN
- **B04-B closure:** `docs/workstreams/timeline-temporal-operational-b04-b-closure-2026-09-19.md` ✅ CLOSED / PROVEN
- **B04-C freeze:** `docs/workstreams/timeline-temporal-operational-b04-c-implementation-freeze.md`
- **B04-C closure:** `docs/workstreams/timeline-temporal-operational-b04-c-closure-2026-09-19.md` ✅ CLOSED / PROVEN
- **Timeline candidate DB overlay:** `docs/database/timeline-temporal-operational.md`
- **Detailed semantic freeze:** `docs/workstreams/archive/timeline-temporal-operational-map-ledger-snapshot-2026-09-15.md`

The archived semantic freeze remains the binding detailed inventory for the full vertical. This file is the live implementation/proof ledger.

---

# 1. Permanent semantic boundaries

```text
Person != Account != Principal != Actor
Goal != Plan != Activity
Activity != Event != Routine
Activity != Schedule
Event != Schedule
Routine != Recurrence
Recurrence != Occurrence
Occurrence != Schedule
Schedule != Temporal Constraint
Temporal Constraint != Movement Policy
Temporal Constraint != Recurrence
Schedule != Session
Schedule != Actual
Session != Actual
Actual != Outcome
Outcome != Confirmation
planned/intended != happened
current accepted state != latest row
idempotency key != Domain identity
provider identity != DANTE identity
projection != canonical truth
proposal != accepted effect
pending != success
unscheduled != deleted
Undo != DB/history rewind
estimated effort != scheduled duration != Session duration
floating-local != named-zone-local != absolute instant
date span != coarse local period
coarse precision != fabricated exact clock time
source wall-clock intent != resolved instant
Agenda part != Activity/Event/Occurrence/Schedule/Session/Actual by default
Event != Availability / Capacity Claim
postponed/TBD Event != Planning Tray Activity
window != placement
preference != accepted Schedule
evaluation != solver decision
violation != automatic mutation
```

These boundaries cannot be weakened by UI convenience, ORM convenience, provider shape or roadmap pressure.

---

# 2. Current roadmap position

```text
B00 Real Data Spine                              ✅ CLOSED / PROVEN
B01 Activity Core                                ✅ CLOSED / PROVEN
B02 Schedule Core                                ✅ CLOSED / PROVEN
B03 Event Core                                   ✅ CLOSED / PROVEN
PRE-B04 DB/API GOVERNANCE                        ✅ CLOSED / FROZEN
B04 Temporal Constraints + Movement Policy       🟡 IN PROGRESS
├─ B04-A Temporal Constraint canonical core      ✅ CLOSED / PROVEN
├─ B04-B Boundary / Deadline constraints         ✅ CLOSED / PROVEN
├─ B04-C Windows / Preferences / Evaluation      ✅ CLOSED / PROVEN
├─ B04-D Movement Policy                         ⬜ NEXT
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

Current candidate persistence authority:

```text
PostgreSQL       18.6
Alembic head     20260919_36
Topology         109|5|35|87|214|131|312|0|0|0
```

Governance baseline remains binding:

```text
DB same-change gate          ✅ FROZEN
candidate DB overlay         ✅ ESTABLISHED
pre-B04 Temporal inventory   ✅ 13 operations frozen
new API operationId rule     ✅ explicit stable semantic IDs required
OpenAPI → Orval/client gate  ✅ BINDING
```

---

# 3. Completed foundation

## B00 — Real Data Spine ✅

Authenticated frontend → backend/application → DanteContext/self Person → PostgreSQL truth, truthful empty/error behavior and isolated real-stack proof are established.

## B01 — Activity Core ✅

Canonical Activity identity, self-owned actionable-intention descriptor, idempotent create, Planning Tray/read path and reload identity are established.

## B02 — Schedule Core ✅

All accepted Schedule forms and lifecycle behavior are proven at B02 scope: date-span, floating-local, named-zone-local, absolute, coarse-local-period, establish/revision/current/history/CAS/idempotency/unschedule/guarded Undo/DST and product integration.

## B03 — Event Core ✅ CLOSED / PROVEN

Event is a distinct originating owner while reusing one shared Schedule engine. Agenda remains Event-internal value truth. Postponed/TBD Event rediscovery remains transferred to B05 rather than collapsed into Activity Planning Tray truth.

---

# 4. Pre-B04 DB/API governance ✅ CLOSED / FROZEN

- ✅ Whole DB SoR and Timeline candidate overlay separated from protected-main truth.
- ✅ Dictionary/current-catalog same-change closure rule frozen for B04+.
- ✅ Exact pre-B04 Temporal public API inventory frozen at 13 operations.
- ✅ Existing verbose operationIds retained as compatibility contract.
- ✅ Every new B04+ Temporal endpoint requires explicit stable semantic `temporal_*` operationId plus same-change OpenAPI/Orval/client/tests reconciliation.

Authority: `timeline-temporal-operational-pre-b04-governance-2026-09-18.md`.

---

# 5. B04 — Temporal Constraints + Movement Policy 🟡 IN PROGRESS

B04 establishes Temporal Constraint truth distinct from Schedule placement and later activates Movement Policy without collapsing policy, proposal, solver result or accepted effect.

## 5.1 B04-A — Temporal Constraint canonical core ✅ CLOSED / PROVEN

B04-A established:

```text
stable self-owned Activity/Event Temporal Constraint identity
ScopedRecordRef ownership
temporal_constraint.rule MaterialState history
absolute earliest_start / schedule.start rule
hard | soft strength
expected-state CAS
idempotent create/revise/retire
current-vs-retired reads
5 explicit temporal_* public operations
OpenAPI / Orval / deterministic generated client
```

Candidate migration chain through A closure:

```text
20260918_30 temporal_constraint_core
20260918_31 temporal_constraint_totality_hardening
20260918_32 current_history_dispatch_hardening
20260918_33 temporal_constraint_api_activation
```

Closure authority: `timeline-temporal-operational-b04-a-closure-2026-09-18.md`.

## 5.2 B04-B — Boundary / Deadline constraints ✅ CLOSED / PROVEN

Closed boundary matrix:

```text
earliest_start     + schedule.start       ✅
latest_start       + schedule.start       ✅
latest_completion  + schedule.completion  ✅
```

Shared limits:

```text
subject        self-owned Activity | Event
family         boundary
strength       hard | soft
temporal form  absolute
value          finite timestamptz
```

Migration authority:

```text
20260919_34 b04_absolute_boundary_deadline
```

Accepted topology through B04-B:

```text
107|5|34|85|212|129|309|0|0|0
```

Observed closure gates:

```text
API / typed-union / Temporal inventory             13 PASS
PostgreSQL + application + API activation + DB     22 PASS / 1 deselected
OpenAPI export / inventory / API contract          21 PASS
@dante/api-client typecheck                         PASS
@dante/api-client Vitest                            11 PASS
pnpm generated:check                                PASS / 163 files deterministic
```

Closure authority: `timeline-temporal-operational-b04-b-closure-2026-09-19.md`.

## 5.3 B04-C — Windows / Preferences / Evaluation ✅ CLOSED / PROVEN

B04-C activates the typed absolute-window family plus deterministic derived evaluation/explanation while preserving Temporal Constraint as independent canonical truth.

Accepted relationship matrix:

```text
start_within              + schedule.start       ✅
completion_within         + schedule.completion  ✅
full_placement_contained  + schedule.placement   ✅
placement_overlaps        + schedule.placement   ✅
```

Shared limits:

```text
subject        self-owned Activity | Event
family         window
strength       hard | soft
temporal form  absolute
range          finite starts_at < ends_at
```

Frozen semantics:

```text
start_within / completion_within use inclusive point membership
full_placement_contained requires full interval containment
placement_overlaps requires positive overlap; endpoint-only touching is not overlap
hard = validity constraint
soft = preference
```

Derived evaluation distinguishes:

```text
per rule: satisfied | violated | not_evaluable
overall:  admissible | admissible_with_soft_violations | inadmissible | not_evaluable
hard set: feasible | infeasible | undetermined
```

Evaluation is derived and non-persistent. It neither mutates Schedule nor creates Actual/Outcome truth, and performs no solver/candidate search.

Persistence authority:

```text
20260919_35 b04_absolute_window_constraints
20260919_36 b04_window_runtime_read_acl
Topology      109|5|35|87|214|131|312|0|0|0
```

New typed persistence/capability:

```text
temporal_constraint_window_state
temporal_constraint_window_absolute_state
mutate_self_absolute_window_constraint(...)
```

Public API adds exactly:

```text
POST /api/v1/temporal/constraints/evaluate
temporal_evaluate_constraints
```

Observed closure gates:

```text
PostgreSQL / application evaluation             9 PASS / 2 deselected
current catalog / Dictionary / ACL             12 PASS
OpenAPI / Temporal API contract                24 PASS
@dante/api-client typecheck                    PASS
@dante/api-client Vitest                       11 PASS
pnpm generated:check                           PASS / 177 deterministic files
```

Generated contract commit:

```text
5268d9dd239ab344337cadd1dfdf312dd46ffe42
```

Closure authority: `timeline-temporal-operational-b04-c-closure-2026-09-19.md`.

## 5.4 B04-D — Movement Policy ⬜ NEXT

Movement Policy remains separate from constraint truth and solver output. Accepted movement/override must remain explicit and governed.

B04-D requires its own semantic/implementation freeze before any write. B04-C closure does not authorize persistence, enum shape, mutation path, API, frontend behavior or solver coupling for Movement Policy.

## 5.5 B04-E — Advanced-family applicability ⬜

Min/max duration, spacing and relative constraints only where truthful anchors already exist. Dependencies on Routine/Session/Actual/Solver remain deferred to their owning blocks where semantics are not yet available.

## 5.6 B04-F — Whole-B04 closure ⬜

Whole-B04 regression, DB/docs/API consistency, applicable product/manual acceptance and final closure evidence.

B05 begins only after B04-F closes.

---

# 6. B05–B15 ownership register

```text
B05  Calendar / Life Area / Tags / product organization
     + postponed/TBD Event rediscovery/replanning surface transferred from B03
B06  Routine + Recurrence + Occurrence baseline
B07  UI/UX Consolidation v1
B08  Session Runtime
B09  Responsibility / Participation / actor relations
B10  Actual + Outcome + Confirmation + Resolution Queue
B11  advanced recurrence + conditional policy + reminders
B12  replanning/conflict/solver
B13  provider integration + offline/multi-device reconciliation
B14  analytics/statistics/Signals
B15  whole-vertical closure/recovery/cross-cutting proof
```

The detailed functionality lists remain binding in the archived semantic freeze.

---

# 7. Current gate

```text
B03 Event Core             ✅ CLOSED / PROVEN
Pre-B04 governance         ✅ CLOSED / FROZEN
B04                        🟡 IN PROGRESS
├─ B04-A                   ✅ CLOSED / PROVEN
├─ B04-B                   ✅ CLOSED / PROVEN
├─ B04-C                   ✅ CLOSED / PROVEN
└─ B04-D                   ⬜ NEXT
```

Immediate gate: re-open Domain / Logical / Physical / B04 execution authority and freeze the exact B04-D Movement Policy scope before any B04-D write.

CI remains separately authorized and is not implicitly launched.
