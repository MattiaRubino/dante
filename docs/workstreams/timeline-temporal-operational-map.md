# Timeline / Temporal-Operational — Live Execution Ledger

- **Status:** CURRENT LIVE STATE — reconciled 2026-09-24
- **Branch:** `feature/timeline-temporal-operational`
- **Roadmap authority:** `docs/workstreams/timeline-temporal-operational-roadmap.md`
- **Continuation handoff:** `docs/workstreams/timeline-temporal-operational-handoff.md`
- **DB overlay:** `docs/database/timeline-temporal-operational.md`
- **Current Alembic frontier:** `20260923_57`
- **Current proven topology:** `145|5|88|92|285|223|408|0|0|0`
- **CI:** not authorized; local tests are run by the user

This is the single live implementation/proof ledger. Every active sub-slice is delivered **end-to-end** before the next starts.

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
TC-009 contiguous Session duration  → B08-C
TC-010 spacing/recovery             → later anchor-specific reopening
TC-011 relative before/after        → future bounded relation/reference review
```

---

# 3. Current position

```text
B08 Session Runtime                              🟡 READY TO START
  B08-A Session Core End-to-End                   ← NEXT / NOT STARTED
  B08-B Pause / Resume + Durations End-to-End     ⬜
  B08-C TC-009 Session Duration End-to-End        ⬜
  B08-D Whole-block closure                       ⬜

B09 Responsibility / Participation               ⬜
B10 Actual / Outcome / Confirmation / Resolution ⬜
B11 Advanced Recurrence / Conditional / Reminder ⬜
B12 Replanning / Conflict / Solver               ⬜
B07 UI/UX Consolidation v1                       ⏸ DEFERRED
B15 Whole Vertical Closure                       ⬜
```

No B08 implementation slice is currently closed. Work resumes from B08-A only.

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

Existing CP6 Session substrate to reuse wherever truthful:

```text
session
session_timing_state
session_timing_absolute
session_timing_elapsed
session_timing_pause
session_timing_current_history
```

Baseline product subjects to validate at the start of B08-A:

```text
Activity      Session subject     yes
Occurrence    Session subject     yes
Routine       direct subject      no
Event         ordinary subject    no baseline
Schedule      Session owner       no
```

Spontaneous Session without prior Activity remains a possible Domain capability but is outside the B08 baseline product path. B08 must not invent an Activity merely to host one.

---

# 5. B08-A — Session Core End-to-End ← NEXT

**Status:** NOT STARTED

Target product capability:

```text
Activity   → START Session → authoritative read → END Session
Occurrence → START Session → authoritative read → END Session
```

This is one vertical slice. The authority/schema inspection is the first step of the same slice, not a separate phase.

## B08-A live checklist

### Semantics / authority

```text
[ ] reconcile Session Domain/Logical/Physical authority
[ ] confirm Activity + Occurrence eligible subjects
[ ] confirm Routine/Event/Schedule exclusions for baseline
[ ] freeze START / READ / END semantics
[ ] confirm END has no completion/Actual/Outcome side effect
```

### Persistence / database

```text
[ ] inspect current `session*` substrate against the accepted capability
[ ] choose typed Session → Activity/Occurrence execution-context representation
[ ] add forward-only Alembic only for real gaps
[ ] reconcile SQLAlchemy mapping
[ ] reconcile Dictionary + DB overlay + expected topology
[ ] self-scope / integrity / current-history behavior proven
[ ] idempotency / receipt / expected-current / concurrency behavior proven
```

### Backend / API / generated client

```text
[ ] Activity START operation
[ ] Occurrence START operation
[ ] authoritative Session read/list required by product path
[ ] END operation
[ ] stable operationIds / error-conflict contract
[ ] OpenAPI generated-current
[ ] generated API client typechecks
```

### Frontend / Timeline

```text
[ ] functional START control for eligible Activity
[ ] functional START control for eligible Occurrence
[ ] authoritative running/open representation
[ ] functional END control
[ ] F5/navigation rehydrates canonical state
[ ] no browser-owned canonical Session state
[ ] no implicit Schedule mutation
```

### Proof / closure

```text
[ ] relevant backend/PostgreSQL local tests PASS
[ ] relevant web/unit/typecheck gates PASS
[ ] generated:check PASS when applicable
[ ] manual Activity START → F5 → END PASS
[ ] manual Occurrence START → F5 → END PASS
[ ] second START after END creates a new SessionRef
[ ] Schedule remains unchanged
[ ] no Activity/Occurrence completion fabricated
[ ] no Actual/Outcome fabricated
[ ] map/handoff/DB docs reconciled
```

Only when every applicable item above is accepted may B08-A become `✅ CLOSED / PROVEN` and B08-B start.

---

# 6. B08-B — Pause / Resume + Durations End-to-End

**Status:** BLOCKED BY B08-A

Target extension of the proven B08-A path:

```text
RUNNING → PAUSED → RUNNING → ENDED
```

Live checklist when activated:

```text
[ ] authority semantics reconciled
[ ] persistence/current-history changes complete
[ ] PAUSE backend/API/client/frontend complete
[ ] RESUME backend/API/client/frontend complete
[ ] same SessionRef across pause/resume
[ ] at most one open pause
[ ] invalid transition conflicts/fails closed
[ ] elapsed duration truthful
[ ] paused duration truthful
[ ] active duration only from supported facts
[ ] browser timer remains presentation only
[ ] F5 while running/paused authoritative
[ ] concurrency/replay proof
[ ] automated gates PASS
[ ] real-stack manual path PASS
[ ] docs/ledger reconciled
```

B08-B closes only as a complete end-to-end capability.

---

# 7. B08-C — TC-009 Session Duration End-to-End

**Status:** BLOCKED BY B08-B

TC-009 is reopened only after real Session runtime exists.

```text
[ ] exact contiguous Session-duration semantics frozen
[ ] elapsed-vs-active applicability frozen
[ ] typed persistence added only if needed
[ ] deterministic hard/soft evaluation complete
[ ] backend/API/client complete where required
[ ] functional product exposure complete where required
[ ] violation != automatic mutation preserved
[ ] automated proof PASS
[ ] manual proof where applicable PASS
[ ] docs/ledger reconciled
```

TC-010 remains deferred unless a direct authority dependency is proven.

---

# 8. B08-D — Whole-block closure

**Status:** BLOCKED BY B08-A/B/C

No new half-feature belongs here. B08-D is whole-block regression, reconciliation and persistent real-stack proof:

```text
[ ] DB catalog/integrity/topology reconciled
[ ] B08 backend regression PASS
[ ] cross-user/fail-closed PASS
[ ] idempotency/concurrency PASS
[ ] generated:check PASS
[ ] API-client typecheck PASS
[ ] web typecheck PASS
[ ] focused Session/Timeline Vitest PASS
[ ] touched B01/B02/B04/B06 regressions PASS
[ ] Activity START → F5 → PAUSE → F5 → RESUME → END PASS
[ ] second START → new SessionRef PASS
[ ] Occurrence path PASS
[ ] Schedule unchanged PASS
[ ] no fabricated completion / Actual / Outcome PASS
[ ] no duplicate state after reload/navigation PASS
[ ] final docs/handoff reconciled
```

Only B08-D may mark the whole B08 block `✅ CLOSED / PROVEN`.

---

# 9. Later blocks

B09–B12 follow the same discipline: each sub-capability must travel through semantics → persistence → backend/API/client → real frontend → automated/manual proof → documentation before the next sub-capability starts.

B07 remains deferred until B08–B12 exist; it consolidates presentation rather than rescuing half-implemented capabilities.

---

# 10. Documentation / chat-saturation rule

At a meaningful checkpoint:

```text
1. update this ledger checkboxes + accepted evidence
2. update handoff with exact next action
3. update roadmap only if scope/order changes
4. update DB overlay/dictionary in the same change when persistence changes
5. push code/docs frequently
```

Fresh-chat recovery order:

```text
1. timeline-temporal-operational-handoff.md
2. timeline-temporal-operational-roadmap.md
3. timeline-temporal-operational-map.md
4. docs/database/timeline-temporal-operational.md only if active work touches DB
```

---

# 11. Current gate

```text
B00–B06 ✅ CLOSED / PROVEN
B07     ⏸ DEFERRED
B08     🟡 READY TO START
B08-A   ← NEXT / NOT STARTED / END-TO-END
B08-B–D ⬜ BLOCKED BY PRECEDING SLICE
B09–B12 ⬜ NOT STARTED
B15     ⬜ NOT STARTED
```

**Next concrete action:** start B08-A Session Core as one complete end-to-end slice. Do not treat authority, DB, API or frontend as separate roadmap phases.