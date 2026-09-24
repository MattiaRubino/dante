# Timeline / Temporal-Operational Vertical — Implementation Roadmap

- **Status:** CURRENT EXECUTION ROADMAP — reconciled 2026-09-24
- **Branch/workstream:** `feature/timeline-temporal-operational`
- **Vertical boundary:** Home `+` creation/configuration → canonical temporal truth → Timeline projection/actions → bounded lifecycle completion
- **Completed frontier:** B06 ✅ CLOSED / PROVEN
- **Current block:** B08 Session Runtime 🟡 READY TO START
- **Current slice:** B08-B Pause / Resume + Durations End-to-End ← NEXT
- **Deferred block:** B07 UI/UX Consolidation v1 — execute after B08–B12
- **Current DB frontier:** PostgreSQL 18.6 / Alembic `20260924_58`
- **Proven topology:** `145|5|88|92|285|223|408|0|0|0`
- **Live execution ledger:** `docs/workstreams/timeline-temporal-operational-map.md`
- **Continuation handoff:** `docs/workstreams/timeline-temporal-operational-handoff.md`
- **Post-B06 scope authority:** `docs/workstreams/timeline-temporal-operational-post-b06-scope-decision-2026-09-23.md`

This document is the sequencing authority for the remaining Timeline / Temporal-Operational work.

---

# 0. Execution discipline — every slice is end-to-end

Every implementation slice must be completed vertically before the next slice starts:

```text
current Product / Domain / Logical / Physical authority
→ persistence / Alembic / Dictionary when required
→ backend / application
→ HTTP API / OpenAPI
→ generated API client
→ frontend / real product surface
→ local automated proof
→ real-stack manual proof where user behavior matters
→ documentation / live-ledger reconciliation
→ only then advance
```

A slice is **not** complete because one technical layer is finished. Do not create sequences such as “all DB first”, “all backend second”, or “frontend later”. Temporary UI is acceptable before B07, but the active capability must already be usable and testable end-to-end.

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

## Documentation rule

Keep documentation deliberately small:

```text
ROADMAP  = ordered plan and block boundaries
MAP      = live state, accepted decisions, implementation/test evidence
HANDOFF  = exact current position and next concrete action
```

Do not create a separate planning/freeze file for every sub-slice. Update the live map and handoff as work progresses. A historical closure record is created only when a whole major block closes and retaining immutable evidence is useful.

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

B08 Session Runtime                              🟡 READY TO START
  B08-A Session Core End-to-End                   ✅ CLOSED / PROVEN
  B08-B Pause / Resume + Durations End-to-End     ← NEXT
  B08-C TC-009 Session Duration End-to-End        ⬜
  B08-D Whole-block closure                       ⬜

B09 Responsibility / Participation               ⬜
B10 Actual / Outcome / Confirmation / Resolution ⬜
B11 Advanced Recurrence / Conditional / Reminder ⬜
B12 Replanning / Conflict / Solver               ⬜
B07 UI/UX Consolidation v1                       ⏸ DEFERRED UNTIL B08–B12 EXIST
B15 Whole Vertical Closure                       ⬜
```

The non-numeric execution order is intentional: B07 stays historically stable but is deferred until the capability vocabulary from B08–B12 exists.

Former B13 Provider/Offline/Multi-device and B14 Analytics/Statistics/Signals are future backlog outside this bounded vertical and are not B15 blockers.

---

# 2. Completed foundation B00–B06

## B00 — Real Data Spine ✅
Real authenticated Web → FastAPI/application → PostgreSQL truth with real empty/error/reload behavior.

## B01 — Activity Core ✅
Canonical Activity identity, actionable intention, idempotent create/read, unplaced state and Planning Tray projection.

## B02 — Schedule Core ✅
One shared Schedule engine across accepted owners with establish/revise/unschedule/Undo/current-history/CAS/idempotency/DST semantics.

## B03 — Event Core ✅
Event remains distinct from Activity while reusing shared Schedule authority. Agenda remains Event-internal value truth.

## B04 — Temporal Constraints + Movement Policy ✅
Typed planning constraints, deterministic hard/soft evaluation, planned-placement duration and governed movement/proposal semantics without collapsing constraint, policy, solver or accepted Schedule.

Deferred families carried forward:

```text
TC-009 contiguous Session duration  → B08-C
TC-010 spacing/recovery             → later anchor-specific reopening
TC-011 relative before/after        → bounded relation/reference review when activated
```

## B05 — Product Organization ✅
Actor-local Life Area + secondary Tags and real Timeline organization without turning organization into Domain ownership.

## B06 — Routine / Recurrence / Occurrence Baseline ✅

```text
B06-A Routine source core                        ✅
B06-B Recurrence authoring                       ✅
B06-C canonical Occurrence checkpoint            ✅
B06-D shared Schedule / Timeline / functional UI ✅
B06-E whole-block closure                        ✅
```

B06 preserves `Routine != Recurrence != Occurrence != Schedule`; expected/scheduled projections do not duplicate one canonical Occurrence; recurring state survives reload.

Frontier after B06:

```text
PostgreSQL 18.6
Alembic     20260923_57
Topology    145|5|88|92|285|223|408|0|0|0
```

---

# 3. B08 — Session Runtime

B08 activates actual execution episodes for the Timeline vertical without collapsing planned Schedule or later happened-reality semantics.

Permanent boundaries:

```text
Activity != Session
Occurrence != Session
Schedule != Session
Session != Actual
Session != Outcome
Session end != Activity completion
Session end != Occurrence completion
planned Schedule duration != Session elapsed duration
Session elapsed duration != Session active duration
```

Existing CP6 substrate is reused wherever truthful:

```text
session
session_timing_state
session_timing_absolute
session_timing_elapsed
session_timing_pause
session_timing_current_history
```

## B08-A — Session Core End-to-End ← NEXT

Deliver one complete real product capability before moving on:

```text
Activity   → START Session → authoritative read → END Session
Occurrence → START Session → authoritative read → END Session
```

The slice starts by reconciling current Domain/Logical/Physical/DB authority and freezing only the decisions needed for this capability. Then it continues through every required layer in the same slice.

B08-A owns, where required:

```text
typed Session → Activity / Occurrence execution-context persistence
forward-only Alembic + Dictionary/DB overlay reconciliation
Session creation/start/end current-history semantics
self-scope / fail-closed ownership
idempotency and materially-different replay conflict
expected-current/CAS and concurrency behavior
backend/application operations
HTTP API + stable operationIds
OpenAPI + generated client
functional Timeline/product controls for eligible Activity/Occurrence
F5/navigation authoritative rehydration
backend/database integration tests
frontend focused tests/typecheck/generated-current checks
real-stack manual START → reload → END proof   deferred to B08-D
documentation/map/handoff update
```

Forbidden effects:

```text
START does not fabricate Schedule
END does not complete Activity
END does not resolve Occurrence
END does not create Actual
END does not create Outcome
```

B08-A is `CLOSED / PROVEN` on the local automated proof. No B08-B work starts from an unproven catalog, but the manual walkthrough waits until B08-D.

## B08-B — Pause / Resume + Durations End-to-End

Extend the already proven B08-A product path end-to-end:

```text
RUNNING → PAUSED → RUNNING → ENDED
```

The same slice owns all required persistence/backend/API/client/frontend changes plus proof for:

```text
PAUSE preserves Session identity
RESUME preserves Session identity
at most one open pause
invalid transition conflicts/fails closed
truthful elapsed duration
truthful paused duration
active duration only when supported by captured facts
F5 while running/paused rehydrates authoritative state
concurrent transitions are deterministic/conflict-safe
browser timer is presentation only
```

B08-B closes only after the real product path is manually usable and the applicable local automated gates pass.

## B08-C — TC-009 Session Duration End-to-End

Reopen the B04-deferred contiguous Session-duration capability as one complete slice.

First freeze the exact Session fact/facet and elapsed-vs-active semantics; then implement every required layer together:

```text
semantic contract
→ typed persistence only if a real gap exists
→ deterministic hard/soft evaluation
→ backend/API/client
→ functional product exposure where required by the vertical
→ automated proof
→ manual proof where applicable
→ docs/ledger reconciliation
```

Do not alias Session duration to planned Schedule duration. A violation remains an evaluation result, not an automatic mutation. TC-010 remains deferred unless current authority establishes a direct dependency.

## B08-D — Whole-block closure

B08-D does not add a new half-capability. It hardens and closes the already end-to-end B08-A/B/C work with regression, catalog/integrity reconciliation and the persistent real-stack walkthrough:

```text
START
→ F5 still running
→ PAUSE
→ F5 still paused
→ RESUME
→ END
→ second START gives new SessionRef
→ eligible Occurrence path works
→ Schedule unchanged
→ no fabricated completion / Actual / Outcome
→ no duplicate state on reload/navigation
```

The user runs local tests. No CI/GitHub Actions unless separately authorized.

Only B08-D may mark the whole B08 block `CLOSED / PROVEN`.

---

# 4. B09 — Responsibility / Participation

B09 is also implemented as end-to-end capability slices, not by technical layer. It adds only the role/participation semantics required by Activity/Event/Routine/Occurrence and Timeline interaction without equating participant identity with a DANTE Account.

Out of scope: cross-account collaboration, chat/messaging, shared editing and invitation/grant infrastructure.

---

# 5. B10 — Actual / Outcome / Confirmation / Resolution

Complete the bounded Timeline lifecycle toward happened reality while preserving:

```text
planned/intended != happened
Session != Actual
Actual != Outcome
Outcome != Confirmation
```

Time passage never manufactures execution. Each sub-capability is delivered end-to-end before the next one begins.

---

# 6. B11 — Advanced Recurrence / Conditional / Reminder

Complete advanced recurrence/reminder capabilities after B06 baseline and once later anchors exist. No RRULE-as-ontology, generic JSON rule bag, generic IFTTT ontology or fake Activity materialization. Each accepted family is implemented end-to-end.

---

# 7. B12 — Replanning / Conflict / Solver

Implement deterministic candidate generation/conflict handling/optimization and governed Proposal acceptance over canonical Schedule/Constraint/Recurrence truth.

```text
canonical truth + constraints/preferences
→ deterministic candidate generation / optimization
→ Proposal(s)
→ optional AI interpretation/ranking assistance
→ governed acceptance
→ canonical Schedule mutation
```

AI is support, never scheduling authority. Solver slices must themselves be complete end-to-end product paths.

---

# 8. B07 — UI/UX Consolidation v1 — DEFERRED

Execute after B08–B12 so the final interaction design sees the complete vertical vocabulary. During B08–B12 UI may be visually temporary, but every capability must already be truthful, usable and testable end-to-end.

B07 consolidates Home/Timeline, `+`, editors, Occurrence actions, Schedule/constraints/recurrence, Session/Actual lifecycle, Responsibility/Participation, reminders and solver/replanning proposals without weakening canonical semantics for visual convenience.

---

# 9. B15 — Whole Vertical Closure

B15 closes only the bounded vertical:

```text
`+` creation/configuration
→ canonical persistence/backend truth
→ Timeline projection/actions
→ Session/Actual lifecycle
→ Responsibility/Participation
→ advanced recurrence/reminders
→ replanning/conflict/solver proposals
→ final B07 UI/UX consolidation
```

External providers, native/offline, broad analytics and account collaboration are not B15 blockers.

---

# 10. Recovery when a chat saturates

Read only:

```text
1. timeline-temporal-operational-handoff.md
2. timeline-temporal-operational-roadmap.md
3. timeline-temporal-operational-map.md
4. docs/database/timeline-temporal-operational.md only when the current slice touches persistence
```

The handoff says where work stopped. The roadmap says what comes next. The map contains accepted decisions, checkboxes and evidence.

---

# 11. Current gate

```text
B00–B06 ✅ CLOSED / PROVEN
B07     ⏸ DEFERRED
B08     🟡 READY TO START
B08-A   ✅ CLOSED / PROVEN
B08-B   ← NEXT
B08-C–D ⬜ BLOCKED UNTIL PRECEDING END-TO-END SLICE CLOSES
B09–B12 ⬜ NOT STARTED
B15     ⬜ NOT STARTED
```

**Current action:** start B08-B. The Session manual walkthrough is B08-D.