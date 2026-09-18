# Timeline / Temporal-Operational Vertical — Semantic Work Map / Live Ledger

- **Status:** CURRENT SEMANTIC MAP + LIVE IMPLEMENTATION LEDGER — reconciled 2026-09-18
- **Branch:** `feature/timeline-temporal-operational`
- **Roadmap:** `docs/workstreams/timeline-temporal-operational-roadmap.md`
- **B03 closure:** `docs/workstreams/timeline-temporal-operational-b03-e-closure-2026-09-18.md` ✅ CLOSED / PROVEN
- **B03 manual acceptance:** `docs/workstreams/timeline-temporal-operational-b03-usertest.md` ✅ PASS
- **Pre-B04 governance closure:** `docs/workstreams/timeline-temporal-operational-pre-b04-governance-2026-09-18.md` ✅ CLOSED / FROZEN
- **B04 execution plan:** `docs/workstreams/timeline-temporal-operational-b04-execution-plan.md`
- **B04-A implementation freeze:** `docs/workstreams/timeline-temporal-operational-b04-a-implementation-freeze.md`
- **B04-A closure:** `docs/workstreams/timeline-temporal-operational-b04-a-closure-2026-09-18.md` ✅ CLOSED / PROVEN
- **Timeline candidate DB overlay:** `docs/database/timeline-temporal-operational.md`
- **Detailed semantic freeze:** `docs/workstreams/archive/timeline-temporal-operational-map-ledger-snapshot-2026-09-15.md`

The archived semantic freeze remains the binding detailed inventory for the full vertical. This file is the current implementation/proof ledger; compacting historical evidence here does not weaken that archived semantic contract.

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
├─ B04-B Boundary / Deadline constraints         ⬜ NEXT
├─ B04-C Windows / Preferences / Evaluation      ⬜
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
Alembic head     20260918_33
Topology         107|5|33|85|212|129|309|0|0|0
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

B03 activates Event as a distinct originating owner while keeping one shared Schedule engine:

```text
Activity ─┐
          ├── one Schedule identity/current/history capability
Event ────┘
```

Accepted Event behavior includes canonical Event expectation, idempotent self create/read, shared Schedule placement/lifecycle, all-day and multi-day truth, postponed/TBD history retention, Timeline projection and bounded ordered Agenda/internal values.

Still-deferred B03 semantic obligations remain owned by later blocks rather than fabricated as B03 completeness:

```text
preparation/follow-up Activity relation   later exact relation semantics
place/conference intent                   later relation/profile semantics
ordinary attendance != Session            B08/B09 owners
Event != Availability/Capacity Claim       later availability semantics
```

Postponed/TBD Event rediscovery remains transferred to B05 without converting Event into Activity Planning Tray truth.

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

Frozen first complete rule:

```text
subject             self-owned Activity | Event
identity            ScopedRecordRef, not NativeRef
facet               temporal_constraint.rule
family              boundary
boundary kind       earliest_start
constrained facet   schedule.start
strength            hard | soft
temporal form       absolute
boundary             finite timestamptz
```

Permanent B04-A non-collapse:

```text
Temporal Constraint != Schedule
Temporal Constraint != Movement Policy
Temporal Constraint != Recurrence
Temporal Constraint != Session / Actual
Temporal Constraint != Availability / Capacity
constraint revision != Schedule revision
proposal != accepted constraint
current accepted state != newest row
idempotency receipt != constraint identity != MaterialState identity
```

### A1 — DDL / mappings ✅ PROVEN

Candidate migration chain:

```text
20260918_30 temporal_constraint_core
20260918_31 temporal_constraint_totality_hardening
20260918_32 current_history_dispatch_hardening
20260918_33 temporal_constraint_api_activation
```

Six canonical/control tables and the governed rule/mutation routines are materialized. SQLAlchemy registers the B04-A persistence surface and shared CP6 dispatchers are extended rather than duplicated.

### A2 — direct PostgreSQL structural/integrity proof ✅ PROVEN

Evidence includes:

```text
focused B04-A core                            4 PASS
shared current-history legacy-family proof    4 PASS
Temporal + CP6 final regression              32 PASS / 2 deselected
B04-A structural catalog / owner / ACL        3 PASS
```

Accepted structural topology remains:

```text
107|5|33|85|212|129|309|0|0|0
```

### A3 — create / revise / retire CAS + idempotency ✅ PROVEN

```text
create establishes stable constraint + scoped address + immutable complete rule state
same operation id + same material intent replays accepted canonical result
same key + changed intent conflicts
revise requires expected current MaterialStateRef
stale expected state conflicts
revision appends state and moves currentness
retire requires expected current state
retire removes only current binding and closes history
stable constraint identity/history survive retirement
```

### A4 — DB / Dictionary / docs ✅ PROVEN

Dictionary object entries/scope, Alembic/SQLAlchemy, live catalog, owners/ACL, DB SoR and Timeline overlay are reconciled. The whole-DB A4 gate passed locally, and the later `_33` activation expectations were reconciled again.

Final current-catalog/DB/B04 activation reconciliation:

```text
13 PASS
```

### A5 — application / API ✅ PROVEN

Public B04-A operations:

```text
Get Temporal Constraint by TemporalConstraintRef
List Temporal Constraints by self-owned subject
Create absolute earliest-start constraint
Revise current absolute earliest-start rule
Retire Temporal Constraint
```

A5 preserves accepted-current semantics, expected-state CAS, operation-id idempotency, retired-not-deleted semantics and Activity/Event subject scope. `_33` makes mutation replay safe with server-generated UUIDs and grants only the narrow runtime read surface needed by Get/List; history/receipt internals remain private and direct writes remain governed.

API governance evidence includes:

```text
focused API + Temporal inventory             10 PASS
B04-A PostgreSQL/application activation       12 PASS
OpenAPI export/inventory/API parity           18 PASS
@dante/api-client typecheck                   PASS
@dante/api-client Vitest                      11 PASS
pnpm generated:check                          PASS / 159 files deterministic
```

No frontend product surface was part of the accepted A5 scope, so no manual frontend acceptance is claimed.

### B04-A closure decision

```text
A1 ✅ CLOSED / PROVEN
A2 ✅ CLOSED / PROVEN
A3 ✅ CLOSED / PROVEN
A4 ✅ CLOSED / PROVEN
A5 ✅ CLOSED / PROVEN

B04-A Temporal Constraint canonical core ✅ CLOSED / PROVEN
```

Closure authority: `timeline-temporal-operational-b04-a-closure-2026-09-18.md`.

## 5.2 B04-B — Boundary / Deadline constraints ⬜ NEXT

B04-B expands truthful boundary semantics beyond the B04-A earliest-start absolute rule. Before implementation, the exact slice must be frozen from Domain/Logical/Physical authority.

Candidate semantic territory includes:

```text
earliest-start
latest-start
latest-completion / deadline
hard | soft boundary semantics
lossless temporal representation appropriate to each accepted rule
```

Do not assume these are aliases. In particular:

```text
deadline != Schedule end
passed deadline != Actual
passed deadline != Outcome/failure
constraint != placement
coarse/date precision != fabricated exact instant
```

The first B04-B implementation slice must be explicitly selected rather than materializing every candidate family at once.

## 5.3 B04-C — Windows / Preferences / Evaluation ⬜

Hard windows, soft preferred windows and explicit relation semantics such as start-within, completion-within, full-contained and overlaps. Evaluation/explanation is allowed; solver ownership remains B12.

## 5.4 B04-D — Movement Policy ⬜

Activate movement policy separately from constraint truth and solver output. Accepted movement/override remains explicit and governed.

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
└─ B04-B                   ⬜ NEXT
```

Immediate gate: freeze the exact B04-B Boundary / Deadline semantic and implementation scope before any B04-B write.

CI remains separately authorized and is not implicitly launched.
