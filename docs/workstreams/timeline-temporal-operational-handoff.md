# Timeline / Temporal-Operational — Workstream Handoff

- **Status:** B08 SESSION RUNTIME 🟡 ACTIVE — B08-A AUTHORITY RECONCILIATION NEXT
- **Reconciled:** 2026-09-23
- **Branch:** `feature/timeline-temporal-operational`
- **Exact known remote frontier at handoff update:** `a00555a95661f345c3bfcb57cd1c55cd74a26934`
- **Current roadmap:** `docs/workstreams/timeline-temporal-operational-roadmap.md`
- **Current live map/ledger:** `docs/workstreams/timeline-temporal-operational-map.md`
- **B08 detailed execution plan:** `docs/workstreams/timeline-temporal-operational-b08-execution-plan.md`
- **Post-B06 scope decision:** `docs/workstreams/timeline-temporal-operational-post-b06-scope-decision-2026-09-23.md`
- **B06 whole-block closure:** `docs/workstreams/timeline-temporal-operational-b06-e-closure-2026-09-23.md`
- **Timeline candidate DB overlay:** `docs/database/timeline-temporal-operational.md`
- **Current Alembic frontier:** `20260923_57`
- **Current proven DB topology:** `145|5|88|92|285|223|408|0|0|0`
- **CI:** no CI/GitHub Actions launch is implied or authorized

This handoff is the first document a fresh chat should read. It records the exact workstream position and next concrete action; detailed B08 sequencing lives in the B08 execution plan.

## 1. Current position

```text
B00 Real Data Spine                              ✅ CLOSED / PROVEN
B01 Activity Core                                ✅ CLOSED / PROVEN
B02 Schedule Core                                ✅ CLOSED / PROVEN
B03 Event Core                                   ✅ CLOSED / PROVEN
PRE-B04 DB/API GOVERNANCE                        ✅ CLOSED / FROZEN
B04 Temporal Constraints + Movement Policy       ✅ CLOSED / PROVEN
B05 Product Organization                         ✅ CLOSED / PROVEN
B06 Routine / Recurrence / Occurrence Baseline   ✅ CLOSED / PROVEN

B08 Session Runtime                              🟡 ACTIVE
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

Former B13 Provider/Offline/Multi-device and B14 Analytics/Statistics/Signals are outside this vertical. Their historical identifiers are not reassigned.

## 2. Workstream boundary

This workstream completes the bounded vertical:

```text
Home `+`
→ create/configure canonical temporal things and facets
→ backend/PostgreSQL truth
→ Timeline projection/actions
→ required runtime/reality lifecycle
→ advanced recurrence/reminders
→ replanning/conflict/solver proposals
→ final UI/UX consolidation
```

It does not own external providers, native/offline, account collaboration or broad analytics.

## 3. Binding distinctions carried forward

```text
Domain != Logical != Physical != API DTO != ViewModel
Person != Account != Principal != Actor
Activity != Event != Routine
Routine != Recurrence != Occurrence
Occurrence != Schedule
Schedule != Temporal Constraint
Schedule != Movement Policy
Temporal Constraint != Movement Policy
Movement Policy != solver result
proposal != accepted effect
Schedule != Session != Actual
Session != Actual != Outcome
Actual != Outcome != Confirmation
Responsibility != Participation
participant != Account identity
planned/intended != happened
planned Schedule duration != Session duration
Session elapsed duration != Session active duration
Session end != Activity completion
Session end != Occurrence completion
planned Schedule duration != Actual duration
projection != canonical truth
current accepted state != latest row
Undo != history rewind
```

Pre-B04 DB/API same-change governance remains binding for all later blocks.

## 4. B06 closed authority

```text
B06-A Routine source core                         ✅ CLOSED / PROVEN at `_51`
B06-B Recurrence authoring                        ✅ CLOSED / PROVEN at `_54`
B06-C canonical Occurrence checkpoint             ✅ CLOSED / PROVEN at `_55`
B06-D shared Schedule / Timeline / functional UI  ✅ CLOSED / PROVEN at `_57`
B06-E whole-block closure                         ✅ CLOSED / PROVEN at `_57`
B06 whole block                                   ✅ CLOSED / PROVEN
```

B06 reuses existing Schedule authority for materialized Occurrences. It does not create a second Schedule owner, rewrite provenance, or materialize repeated Activity copies. Expected and scheduled Occurrence projections obey one-item precedence; source organization is inherited rather than cloned.

Final B06 evidence includes:

```text
generated:check                             PASS
API-client typecheck                        PASS
web typecheck                               PASS
focused B06/runtime Vitest                  6 files / 37 tests PASS
persistent local dogfood real-stack        accepted
created Timeline/Event/recurring state      survives F5
remaining B06 blocker                       none
```

## 5. Why B07 is deferred

B07 is deliberately postponed until B08–B12 are implemented. The goal is to avoid repeatedly redesigning `+`, Timeline and editors while their capability vocabulary is still expanding.

During B08–B12, temporary UI is acceptable if it is truthful, accessible enough for the feature, real-stack testable and does not create fake semantics.

B07 later consolidates the complete interaction surface once all vertical capabilities are visible together.

## 6. B08 execution authority

Detailed plan:

`docs/workstreams/timeline-temporal-operational-b08-execution-plan.md`

B08 activates actual execution episodes while preserving:

```text
Activity != Session
Occurrence != Session
Schedule != Session
Session != Actual
Session != Outcome
```

Existing CP6 persistence to inspect/reuse before adding DDL:

```text
session
session_timing_state
session_timing_absolute
session_timing_elapsed
session_timing_pause
session_timing_current_history
```

Candidate baseline to verify in B08-A:

```text
Activity     candidate Session target ✅
Occurrence   candidate Session target ✅
Routine      direct target            ❌
Event        ordinary baseline target ❌
Schedule     Session owner/target     ❌
```

Schedule is not required for actual execution; B08 must not invent retroactive Schedule truth for an unscheduled execution episode.

## 7. Current slice — B08-A Authority reconciliation + implementation freeze

No major B08 runtime implementation should begin until this slice is frozen.

Required inspection:

```text
[ ] Session Domain authority in full
[ ] Activity / Occurrence / Schedule / Event / Actual related boundaries
[ ] Logical Session/reference contracts
[ ] Physical PostgreSQL Session mapping
[ ] every current `session*` dictionary object
[ ] current ORM mappings / runtime ACLs / DB capabilities
[ ] current application/API/OpenAPI/frontend insertion points
```

Required decisions:

```text
[ ] exact eligible Session execution targets
[ ] typed Session → Activity / Occurrence execution-context representation
[ ] exact START / PAUSE / RESUME / END semantics and legal transitions
[ ] current/history mutation model
[ ] concurrent-open Session policy
[ ] idempotency/replay contract
[ ] expected-current/CAS contract
[ ] API operation inventory
[ ] real DDL gap list
[ ] B04 TC-009 reopening boundary
[ ] TC-010 deferral confirmation
[ ] proof matrix
[ ] explicit B08 exclusions
```

Exit artifact:

```text
dated B08-A implementation-freeze record
B08-A CLOSED / FROZEN
```

Only then advance to B08-B.

## 8. Ordered remaining B08 slices

```text
B08-B Start / Read / End core
B08-C Pause / Resume + truthful runtime duration
B08-D Timeline runtime integration
B08-E TC-009 Session-duration reopening
B08-F Whole-block automated + real-stack closure
```

B08-F manual target includes:

```text
START
→ F5 still running
→ PAUSE
→ F5 still paused
→ RESUME
→ END
→ second START = new SessionRef
→ eligible Occurrence path
→ Schedule unchanged
→ no fabricated completion / Actual / Outcome
→ no duplicate state after reload/navigation
```

The user runs local tests. Do not launch CI/Actions.

## 9. Explicit B08 non-goals currently carried forward

```text
Actual / Outcome / Confirmation semantics                 → B10
automatic completion from Session end                     → forbidden
ordinary Event actual-occurrence duplication as Session    → excluded baseline
spontaneous context-free Session product flow              → deferred
Session split / merge UX                                   → deferred
provider/import reconciliation                             → future provider work
native/mobile background timer                             → outside vertical
advanced offline/multi-device runtime sync                 → outside vertical
cross-account shared execution                             → outside vertical
analytics/productivity statistics                          → outside vertical
final visual polish                                        → B07
TC-010 spacing/recovery                                     → later reopening
```

Deferred does not mean semantically prohibited.

## 10. Documentation continuity / chat saturation

At every meaningful checkpoint:

```text
update live map checkbox/status
update B08 execution plan if scope/order changes
create dated freeze/closure record for semantic milestones
update this handoff with exact next action and accepted evidence
reconcile DB overlay/dictionary in the same change as schema changes
push code/docs frequently
```

Fresh-chat recovery order:

```text
1. this handoff
2. timeline-temporal-operational-map.md
3. timeline-temporal-operational-b08-execution-plan.md
4. latest dated B08 freeze/closure record
5. docs/database/timeline-temporal-operational.md when persistence is involved
```

## 11. Current gate / exact next action

```text
B06 ✅ CLOSED / PROVEN at `_57`
B07 ⏸ DEFERRED
B08 🟡 ACTIVE
B08-A ← NEXT
```

**Next concrete action:** inspect and reconcile current Session authority/persistence/application surfaces, resolve the B08-A decision list, then publish the dated B08-A implementation freeze. Do not start B08-B or B09+ opportunistically. No CI/Actions are authorized by this handoff.