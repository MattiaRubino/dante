# Timeline / Temporal-Operational Vertical — Implementation Roadmap

- **Status:** CURRENT EXECUTION ROADMAP — reconciled 2026-09-23
- **Branch/workstream:** `feature/timeline-temporal-operational`
- **Vertical boundary:** Home `+` creation/configuration → canonical temporal truth → Timeline projection/actions → bounded lifecycle completion
- **Completed frontier:** B06 ✅ CLOSED / PROVEN
- **Current block:** B08 Session Runtime 🟡 READY TO START
- **Current slice:** B08-A Authority reconciliation + implementation freeze ← NEXT
- **Deferred block:** B07 UI/UX Consolidation v1 — execute after B08–B12
- **Current DB frontier:** PostgreSQL 18.6 / Alembic `20260923_57`
- **Proven topology:** `145|5|88|92|285|223|408|0|0|0`
- **Live execution ledger:** `docs/workstreams/timeline-temporal-operational-map.md`
- **Continuation handoff:** `docs/workstreams/timeline-temporal-operational-handoff.md`
- **Post-B06 scope authority:** `docs/workstreams/timeline-temporal-operational-post-b06-scope-decision-2026-09-23.md`

This document is the single sequencing authority for the remaining Timeline / Temporal-Operational work. It defines **what comes next and in what order**. Detailed discoveries, decisions, implementation evidence and test results are recorded incrementally in the live map/ledger rather than creating a new planning document for every sub-slice.

---

# 0. Execution discipline

For every slice:

```text
inspect current authority/code/schema
→ decide the smallest truthful change
→ implement that slice only
→ user runs the requested local tests
→ reconcile docs/evidence
→ advance to the next slice
```

Rules:

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

No later slice starts opportunistically while the current one still has unresolved semantic or proof gaps.

## Documentation rule

Keep documentation deliberately small:

```text
ROADMAP  = ordered plan and block boundaries
MAP      = live state, accepted decisions, implementation/test evidence
HANDOFF  = exact current position and next concrete action
```

Do **not** create a separate planning/freeze file for every A/B/C sub-slice. Update the live map and handoff as work progresses. A historical closure record is created only when a whole major block closes and retaining immutable closure evidence is useful.

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
  B08-A Authority reconciliation + freeze         ← NEXT
  B08-B Start / Read / End core                   ⬜
  B08-C Pause / Resume + duration                 ⬜
  B08-D Timeline runtime integration              ⬜
  B08-E TC-009 Session-duration reopening         ⬜
  B08-F Whole-block closure                       ⬜

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
TC-009 contiguous Session duration  → B08-E
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

Existing CP6 substrate must be inspected/reused before new schema is authorized:

```text
session
session_timing_state
session_timing_absolute
session_timing_elapsed
session_timing_pause
session_timing_current_history
```

## B08-A — Authority reconciliation + implementation freeze ← NEXT

Before implementation, inspect current Domain/Logical/Physical/DB/application/API/frontend authority and freeze only what is needed for B08-B–E:

```text
eligible Session execution targets
Session → execution-context representation
START / PAUSE / RESUME / END lifecycle and legal transitions
current/history mutation model
concurrent-open Session policy
idempotency/replay and CAS requirements
real DDL gaps, if any
API operation inventory
TC-009 exact reopening boundary
explicit non-goals
proof matrix
```

Candidate baseline to verify, not assume:

```text
Activity     Session target ✅ candidate
Occurrence   Session target ✅ candidate
Routine      direct target  ❌
Event        ordinary target ❌ baseline
Schedule     Session owner  ❌
```

**Exit:** B08-A decisions are recorded in the live map; there is no separate B08-A planning/freeze document.

## B08-B — Start / Read / End core

Implement the smallest canonical vertical:

```text
Activity/Occurrence → START Session
read authoritative open/current Session
END Session
reload preserves canonical state
new START after END → new Session identity
```

Must include self-scope, idempotency, conflict/concurrency protection and truthful persistence. START/END must not fabricate Schedule, Activity/Occurrence completion, Actual or Outcome.

## B08-C — Pause / Resume + truthful duration

Implement one continuous Session identity across:

```text
RUNNING → PAUSED → RUNNING → ENDED
```

Prove at-most-one open pause, invalid-transition conflicts, truthful elapsed/paused/active derivation and reload/concurrency behavior.

## B08-D — Timeline runtime integration

Expose functional START/PAUSE/RESUME/END behavior for eligible Activity/Occurrence surfaces. Canonical runtime truth remains backend/PostgreSQL; browser timers are presentation only. F5/navigation must rehydrate without changing Schedule or fabricating lifecycle results.

## B08-E — TC-009 Session-duration reopening

Reopen only the B04-deferred contiguous Session-duration family after Session timing semantics exist. Do not alias Session duration to planned Schedule duration. TC-010 remains deferred unless authority requires otherwise.

## B08-F — Whole-block closure

Run applicable local automated gates and the persistent real-stack walkthrough:

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

Only B08-F may mark B08 `CLOSED / PROVEN`. At that point update roadmap/map/handoff and, if useful for immutable history, create **one B08 whole-block closure record**.

---

# 4. B09 — Responsibility / Participation

Add the role/participation semantics required by Activity/Event/Routine/Occurrence and Timeline interaction without equating participant identity with a DANTE Account.

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

Time passage never manufactures execution.

---

# 6. B11 — Advanced Recurrence / Conditional / Reminder

Complete advanced recurrence/reminder capabilities after B06 baseline and once later anchors exist. No RRULE-as-ontology, generic JSON rule bag, generic IFTTT ontology or fake Activity materialization.

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

AI is support, never scheduling authority.

---

# 8. B07 — UI/UX Consolidation v1 — DEFERRED

Execute after B08–B12 so the final interaction design sees the complete vertical vocabulary. During B08–B12 UI may be temporary but must remain truthful, usable and testable.

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

The handoff says where work stopped. The roadmap says what comes next. The map contains the accepted decisions and evidence produced so far.

---

# 11. Current gate

```text
B00–B06 ✅ CLOSED / PROVEN
B07     ⏸ DEFERRED
B08     🟡 READY TO START
B08-A   ← NEXT
B09–B12 ⬜ NOT STARTED
B15     ⬜ NOT STARTED
```

**Current action:** none has started yet inside B08-A. The next implementation/review session begins with B08-A and proceeds one slice at a time.