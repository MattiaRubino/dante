# Timeline / Temporal-Operational Vertical — Semantic Work Map / Live Ledger

- **Status:** CURRENT SEMANTIC MAP + LIVE IMPLEMENTATION LEDGER — reconciled 2026-09-19
- **Branch:** `feature/timeline-temporal-operational`
- **Roadmap:** `docs/workstreams/timeline-temporal-operational-roadmap.md`
- **B03 closure:** `docs/workstreams/timeline-temporal-operational-b03-e-closure-2026-09-18.md` ✅ CLOSED / PROVEN
- **Pre-B04 governance closure:** `docs/workstreams/timeline-temporal-operational-pre-b04-governance-2026-09-18.md` ✅ CLOSED / FROZEN
- **B04 execution plan:** `docs/workstreams/timeline-temporal-operational-b04-execution-plan.md`
- **B04-A closure:** `docs/workstreams/timeline-temporal-operational-b04-a-closure-2026-09-18.md` ✅ CLOSED / PROVEN
- **B04-B freeze:** `docs/workstreams/timeline-temporal-operational-b04-b-implementation-freeze.md`
- **B04-B closure:** `docs/workstreams/timeline-temporal-operational-b04-b-closure-2026-09-19.md` ✅ CLOSED / PROVEN
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

Current candidate persistence authority:

```text
PostgreSQL       18.6
Alembic head     20260919_34
Topology         107|5|34|85|212|129|309|0|0|0
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

B04-B extends the boundary family with an explicit absolute discriminated union.

Closed matrix:

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

No semantic aliases were introduced:

```text
earliest_start != latest_start
latest_completion/deadline != Schedule end
passed deadline != Actual
passed deadline != Outcome / failure
constraint != placement
```

### B04-B persistence ✅ PROVEN

Migration:

```text
20260919_34 b04_absolute_boundary_deadline
```

`_34` widens the accepted kind/facet check sets and makes the exact kind↔facet matrix a deferred totality invariant. It adds `mutate_self_absolute_boundary_constraint(...)` while preserving `mutate_self_absolute_earliest_start_constraint(...)` for compatibility.

No new table, view, trigger, index, FK or CHECK count was introduced. Routine count moves from 33 to 34.

Accepted topology:

```text
107|5|34|85|212|129|309|0|0|0
```

### B04-B application / API ✅ PROVEN

The same five public Temporal Constraint endpoints remain canonical. Request/response rule contracts are now typed variants for:

```text
AbsoluteEarliestStart
AbsoluteLatestStart
AbsoluteLatestCompletion
```

Existing explicit `temporal_*` operationIds remain stable. CAS, idempotency, append-only history and retirement semantics are preserved.

### B04-B proof ✅ PROVEN

Observed closure gates:

```text
API / typed-union / Temporal inventory             13 PASS
PostgreSQL + application + API activation + DB     22 PASS / 1 deselected
OpenAPI export / inventory / API contract          21 PASS
@dante/api-client typecheck                         PASS
@dante/api-client Vitest                            11 PASS
pnpm generated:check                                PASS / 163 files deterministic
```

Generated OpenAPI/client commit:

```text
3ca46c634411371d720b9ea1ed6600bce16b23da
```

No frontend product surface was part of the B04-B slice, so no frontend manual userTest is claimed.

Closure authority: `timeline-temporal-operational-b04-b-closure-2026-09-19.md`.

## 5.3 B04-C — Windows / Preferences / Evaluation ⬜ NEXT

B04-C is not implicitly opened by B04-B closure. Before write, re-open Domain/Logical/Physical/B04 authority and freeze exact first-slice semantics.

Candidate semantic territory:

```text
hard windows
soft preferred windows
start-within
completion-within
full-contained
overlaps
evaluation / violation explanation
```

Permanent boundary:

```text
window != placement
preference != accepted Schedule
evaluation != solver decision
violation != automatic replanning
```

Lossless temporal representation rules remain binding; unsupported date/floating/named-zone/coarse forms must fail closed rather than be silently converted.

## 5.4 B04-D — Movement Policy ⬜

Movement Policy remains separate from constraint truth and solver output. Accepted movement/override remains explicit and governed.

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
└─ B04-C                   ⬜ NEXT
```

Immediate gate: freeze the exact B04-C Windows / Preferences / Evaluation semantic and implementation scope before any B04-C write.

CI remains separately authorized and is not implicitly launched.
