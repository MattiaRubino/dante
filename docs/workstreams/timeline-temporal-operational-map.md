# Timeline / Temporal-Operational — Live Execution Ledger

- **Status:** CURRENT LIVE STATE — reconciled 2026-09-23
- **Branch:** `feature/timeline-temporal-operational`
- **Roadmap authority:** `docs/workstreams/timeline-temporal-operational-roadmap.md`
- **Continuation handoff:** `docs/workstreams/timeline-temporal-operational-handoff.md`
- **DB overlay:** `docs/database/timeline-temporal-operational.md`
- **Current Alembic frontier:** `20260923_57`
- **Current proven topology:** `145|5|88|92|285|223|408|0|0|0`
- **CI:** not authorized; local tests are run by the user

This is the **single live work ledger**. It records only current progress, accepted decisions, implementation notes and proof evidence. Do not create a new planning/freeze document for every sub-slice.

---

# 1. Permanent semantic boundaries

```text
Person != Account != Principal != Actor
Goal != Plan != Activity
Activity != Event != Routine
Routine != Recurrence != Occurrence
Occurrence != Schedule
Schedule != Temporal Constraint != Movement Policy
Schedule != Session != Actual
Session != Actual != Outcome
Actual != Outcome != Confirmation
Responsibility != Participation
participant != Account identity
planned/intended != happened
proposal != accepted effect
pending != success
projection != canonical truth
current accepted state != latest row
idempotency key != Domain identity
Undo != history rewind
estimated effort != scheduled duration != Session duration
planned Schedule duration != Actual duration
```

---

# 2. Proven frontier

```text
B00 Real Data Spine                              ✅ CLOSED / PROVEN
B01 Activity Core                                ✅ CLOSED / PROVEN
B02 Schedule Core                                ✅ CLOSED / PROVEN
B03 Event Core                                   ✅ CLOSED / PROVEN
PRE-B04 DB/API GOVERNANCE                        ✅ CLOSED / FROZEN
B04 Temporal Constraints + Movement Policy       ✅ CLOSED / PROVEN
B05 Product Organization                         ✅ CLOSED / PROVEN
B06 Routine / Recurrence / Occurrence Baseline   ✅ CLOSED / PROVEN
```

B06 final state:

```text
B06-A Routine source core                        ✅ at `_51`
B06-B Recurrence authoring                       ✅ at `_54`
B06-C canonical Occurrence checkpoint            ✅ at `_55`
B06-D shared Schedule / Timeline / functional UI ✅ at `_57`
B06-E whole-block closure                        ✅ at `_57`
```

Accepted B06 evidence:

```text
generated:check                             PASS
API-client typecheck                        PASS
web typecheck                               PASS
focused B06/runtime Vitest                  6 files / 37 tests PASS
persistent local dogfood real-stack        accepted
created Timeline/Event/recurring state      survives F5
remaining B06 blocker                       none
```

B04 deferred families carried forward:

```text
TC-009 contiguous Session duration  → B08-E
TC-010 spacing/recovery             → later anchor-specific reopening
TC-011 relative before/after        → future bounded relation/reference review
```

---

# 3. Current position

```text
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
B07 UI/UX Consolidation v1                       ⏸ DEFERRED
B15 Whole Vertical Closure                       ⬜
```

No B08 implementation slice has been started yet. The next session may be implemented by ChatGPT, Cursor, or another coding tool; this ledger remains the shared authority for what was actually accepted.

---

# 4. B08 semantic boundary

B08 activates actual execution episodes only where required by the Timeline vertical.

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

Existing CP6 Session substrate to inspect before authorizing new DDL:

```text
session
session_timing_state
session_timing_absolute
session_timing_elapsed
session_timing_pause
session_timing_current_history
```

Candidate execution targets to verify in B08-A rather than assume:

```text
Activity     ✅ candidate
Occurrence   ✅ candidate
Routine      ❌ direct target
Event        ❌ ordinary baseline target
Schedule     ❌ owner/target
```

---

# 5. B08-A — Authority reconciliation + freeze ← CURRENT NEXT STEP

Nothing below is marked accepted until it has been checked against current Domain/Logical/Physical/DB/application authority.

```text
[ ] inspect Session Domain authority
[ ] inspect Activity / Occurrence / Schedule / Event / Actual boundaries
[ ] inspect Logical Session/reference contracts
[ ] inspect Physical PostgreSQL Session mapping
[ ] inspect current `session*` dictionary/schema objects
[ ] inspect ORM mappings / runtime ACLs / DB capabilities
[ ] inspect application/API/OpenAPI/frontend insertion points
[ ] freeze eligible Session execution targets
[ ] freeze Session → execution-context representation
[ ] freeze START / PAUSE / RESUME / END legal transitions
[ ] freeze current/history mutation model
[ ] freeze concurrent-open policy
[ ] freeze idempotency/replay and CAS requirements
[ ] identify real DDL gaps, if any
[ ] freeze API operation inventory
[ ] classify TC-009 reopening
[ ] keep TC-010 deferred unless authority requires it
[ ] freeze explicit non-goals
[ ] freeze proof matrix
```

**Exit:** mark B08-A `CLOSED / FROZEN` directly in this ledger, record the accepted decisions below, update handoff, then proceed to B08-B. No separate B08-A document is required.

## Accepted B08-A decisions

_Not started yet._

## B08-A evidence

_Not started yet._

---

# 6. Later B08 slices

These are deliberately not expanded into separate planning documents. The roadmap defines their scope; when each becomes active, its decisions and evidence are added here.

```text
B08-B  Start / Read / End core
B08-C  Pause / Resume + truthful duration
B08-D  Timeline runtime integration
B08-E  TC-009 Session-duration reopening
B08-F  Whole-block automated + real-stack closure
```

B08-F manual target:

```text
START
→ F5 still running
→ PAUSE
→ F5 still paused
→ RESUME
→ END
→ second START = new SessionRef
→ eligible Occurrence path works
→ Schedule unchanged
→ no fabricated completion / Actual / Outcome
→ no duplicate runtime state after reload/navigation
```

Only after this may B08 become `CLOSED / PROVEN`.

---

# 7. Documentation / chat-saturation rule

At a meaningful checkpoint:

```text
1. update this ledger with accepted decisions/evidence
2. update handoff with exact next action
3. update roadmap only if sequencing or scope changed
4. update DB overlay/dictionary in the same change when persistence changes
5. push code/docs frequently
```

Fresh-chat recovery order:

```text
1. timeline-temporal-operational-handoff.md
2. timeline-temporal-operational-roadmap.md
3. timeline-temporal-operational-map.md
4. docs/database/timeline-temporal-operational.md only if the active slice touches DB work
```

A whole-block closure document may be created when B08 closes; intermediate sub-slices stay in this live ledger.

---

# 8. Current gate

```text
B00–B06 ✅ CLOSED / PROVEN
B07     ⏸ DEFERRED
B08     🟡 READY TO START
B08-A   ← NEXT / NOT STARTED
B09–B12 ⬜ NOT STARTED
B15     ⬜ NOT STARTED
```

**Next concrete action:** B08-A authority reconciliation. No code or B08-A decision has been accepted yet.