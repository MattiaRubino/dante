# Timeline / Temporal-Operational Vertical — Implementation Roadmap

- **Status:** CURRENT EXECUTION ROADMAP — reconciled 2026-09-23
- **Branch/workstream:** `feature/timeline-temporal-operational`
- **Vertical boundary:** Home `+` creation/configuration → canonical temporal truth → Timeline projection/actions → bounded lifecycle completion
- **Current completed frontier:** B06 ✅ CLOSED / PROVEN
- **Current block:** B08 Session Runtime ← NEXT
- **Deferred block:** B07 UI/UX Consolidation v1 — execute after B12
- **Current candidate DB source:** PostgreSQL 18.6 / Alembic `20260923_57`
- **Candidate proven topology:** `145|5|88|92|285|223|408|0|0|0`
- **Live progress ledger:** `docs/workstreams/timeline-temporal-operational-map.md`
- **Post-B06 scope/sequencing authority:** `docs/workstreams/timeline-temporal-operational-post-b06-scope-decision-2026-09-23.md`
- **B06 whole-block closure:** `docs/workstreams/timeline-temporal-operational-b06-e-closure-2026-09-23.md`

This document is the current sequencing authority. Historical snapshots and closure records preserve phase-time evidence; they do not override this roadmap.

---

# 0. Fixed execution contract

```text
semantic capability
→ current Product / Domain / Logical / Physical inspection
→ current persistence inspection
→ DDL only if a real gap exists
→ backend/application operation/query
→ API/transport when applicable
→ frontend integration sufficient for real use/proof
→ automated proof
→ manual userTest where applicable
→ live ledger update
→ documentation reconciliation
```

Permanent rules include:

```text
Domain != Logical != Physical != API DTO != frontend ViewModel
projection != canonical truth
planned/intended != happened
Activity != Event != Routine
Routine != Recurrence != Occurrence
Occurrence != Schedule
Schedule != Temporal Constraint != Movement Policy
Schedule != Session != Actual
Session != Actual != Outcome
Actual != Outcome != Confirmation
Responsibility != Participation
proposal != accepted effect
evaluation != solver decision
current accepted state != latest row
idempotency key != Domain identity
Undo != history rewind
```

A block closes only after applicable semantic, persistence, backend, API/client, frontend, proof and documentation gates are reconciled.

---

# 1. Active ordered roadmap

```text
B00 Real Data Spine                              ✅ CLOSED / PROVEN
B01 Activity Core                                ✅ CLOSED / PROVEN
B02 Schedule Core                                ✅ CLOSED / PROVEN
B03 Event Core                                   ✅ CLOSED / PROVEN
PRE-B04 DB/API GOVERNANCE                        ✅ CLOSED / FROZEN
B04 Temporal Constraints + Movement Policy       ✅ CLOSED / PROVEN
B05 Product Organization                         ✅ CLOSED / PROVEN
B06 Routine / Recurrence / Occurrence Baseline   ✅ CLOSED / PROVEN

B08 Session Runtime                              ← NEXT
B09 Responsibility / Participation
B10 Actual / Outcome / Confirmation / Resolution
B11 Advanced Recurrence / Conditional / Reminder
B12 Replanning / Conflict / Solver
B07 UI/UX Consolidation v1                       ← DEFERRED UNTIL B08–B12 EXIST
B15 Whole Vertical Closure
```

The block identifiers remain stable for historical traceability. Execution order is intentionally non-numeric after B06 because B07 has been deliberately deferred rather than renamed.

Former B13 Provider/Offline/Multi-device and B14 Analytics/Statistics/Signals are **not active blocks in this vertical**. They are future backlog work outside the bounded `+`/Timeline vertical and are not B15 closure blockers.

---

# 2. Completed foundation B00–B06

## B00 — Real Data Spine ✅

Normal runtime consumes real authenticated Web → FastAPI/application → PostgreSQL truth with real empty/error/reload behavior.

## B01 — Activity Core ✅

Canonical Activity identity, actionable intention, idempotent create/read, unplaced state and Planning Tray projection.

## B02 — Schedule Core ✅

One shared Schedule engine across accepted owners, with establish/revise/unschedule/Undo/current-history/CAS/idempotency/DST semantics.

## B03 — Event Core ✅

Event remains distinct from Activity while reusing shared Schedule authority. Agenda remains Event-internal value truth.

## B04 — Temporal Constraints + Movement Policy ✅

Typed planning constraints, deterministic hard/soft evaluation, planned-placement duration and governed movement/proposal semantics without collapsing constraint, policy, solver or accepted Schedule.

## B05 — Product Organization ✅

Actor-local Life Area + secondary Tag organization and postponed/TBD rediscovery without inventing placement truth or new Domain owners.

## B06 — Routine / Recurrence / Occurrence Baseline ✅

```text
B06-A Routine source core                        ✅
B06-B Recurrence authoring                       ✅
B06-C canonical Occurrence checkpoint            ✅
B06-D shared Schedule / Timeline / functional UI ✅
B06-E whole-block closure                        ✅
```

B06 preserves `Routine != Recurrence != Occurrence != Schedule`. Occurrences reuse the existing shared Schedule authority; expected and scheduled projections obey one-item precedence; canonical recurring state survives reload.

Candidate persistence frontier after B06:

```text
PostgreSQL 18.6
Alembic     20260923_57
Topology    145|5|88|92|285|223|408|0|0|0
```

---

# 3. B08 — Session Runtime ← NEXT

B08 activates Session only to the extent needed by the `+`/Timeline vertical: a real execution episode connected to the planned/intended item shown in Timeline.

Expected bounded work:

```text
Session identity/lifecycle where required by current authority
start / pause / resume / stop or semantically accepted equivalent
Timeline-linked runtime state
runtime duration semantics
relevant B04 deferred Session-duration constraints
reload/current-history/idempotency as required
API/client/frontend path sufficient for real manual use
```

Permanent boundaries:

```text
Schedule != Session
Session != Actual
planned Schedule duration != Session elapsed/active duration
```

B08 is not a generic workflow/runtime platform.

---

# 4. B09 — Responsibility / Participation

B09 adds the role/participation semantics needed by Activity/Event/Routine/Occurrence creation/editing and Timeline interaction.

A participant/responsible subject may be a Person/referent without being a DANTE Account. Future account linkage may bind the same Person/referent without changing the participation meaning.

Out of scope:

```text
account-to-account collaboration
chat/messaging
shared editing
cross-account invitation/grant system
```

Permanent boundaries:

```text
Responsibility != Participation
participant != Account identity
performer change != Occurrence identity change
```

---

# 5. B10 — Actual / Outcome / Confirmation / Resolution

B10 completes the bounded Timeline lifecycle toward happened reality.

```text
intended / expected
→ optionally planned
→ optionally Session/runtime
→ Actual / realized fact where justified
→ Outcome
→ Confirmation / Observation / Evidence where applicable
```

Time passage never manufactures execution.

```text
planned/intended != happened
Session != Actual
Actual != Outcome
Outcome != Confirmation
```

---

# 6. B11 — Advanced Recurrence / Conditional / Reminder

B11 completes advanced recurrence/reminder capabilities required by `+`, structured editing and Timeline after B06 baseline.

It may reopen intentionally deferred families once their anchors exist, including completion-relative semantics where justified.

Forbidden shortcuts remain:

```text
RRULE as canonical ontology
generic JSON rule bag
generic IFTTT/automation ontology
fake Activity materialization
```

---

# 7. B12 — Replanning / Conflict / Solver

B12 owns deterministic candidate generation, conflict handling, ranking/optimization and governed replanning proposals over canonical Schedule/Constraint/Recurrence truth.

Target flow:

```text
current canonical truth + constraints/preferences
→ deterministic candidate generation / optimization
→ Proposal(s)
→ optional AI interpretation/explanation/ranking assistance
→ governed acceptance
→ canonical Schedule mutation
```

AI is not scheduling authority and never writes accepted Schedule merely because a model proposed it.

```text
evaluation != solver decision
solver proposal != accepted Schedule
AI output != accepted effect
```

The selected Physical target already names OR-Tools CP-SAT as the solver candidate; B12 decides the concrete bounded activation based on real needs.

---

# 8. B07 — UI/UX Consolidation v1 — DEFERRED

B07 is deliberately executed after B08–B12 so final interaction design sees the complete vertical vocabulary instead of being repeatedly rebuilt.

During B08–B12 the UI may be functional and visually temporary, but must remain truthful, usable and testable.

Deferred B07 consolidates at least:

```text
Home / Timeline
`+` Create
Activity/Event/Routine editors
Occurrence actions
Schedule / constraint / recurrence controls
Session / Actual lifecycle controls
Responsibility / Participation presentation
advanced recurrence/reminders
solver/replanning proposals
responsive / loading / empty / error / accessibility behavior
```

B07 changes presentation/interaction; it must not weaken Domain/Logical/Persistence semantics.

---

# 9. Explicitly outside this vertical

The following are future DANTE work, not active blocks here:

```text
external provider integration (Google Calendar / Outlook / provider sync)
native mobile app
advanced offline / multi-device synchronization
account-to-account collaboration
chat/shared editing
broad analytics / statistics / signals vertical
```

A narrowly derived read value may still be implemented if a specific active block genuinely requires it, but that does not activate a general analytics vertical.

---

# 10. B15 — Whole Vertical Closure

B15 closes only the bounded vertical:

```text
`+` creation/configuration
→ canonical backend/persistence truth
→ Timeline projection/actions
→ required Session/Actual lifecycle
→ Responsibility/Participation roles
→ advanced recurrence/reminders
→ replanning/conflict/solver proposals
→ final B07 UI/UX consolidation
```

Provider integration, native/offline, broad analytics and collaboration are explicitly not B15 blockers.

---

# 11. Current gate

```text
B00–B06 ✅ CLOSED / PROVEN
B07     ⏸ DEFERRED
B08     ← NEXT / NOT STARTED
B09–B12 ⬜ NOT STARTED
B15     ⬜ NOT STARTED
```

Current action: begin B08 pre-scope/authority reconciliation from the proven `_57` frontier. No CI or GitHub Actions are implied or authorized by this roadmap.