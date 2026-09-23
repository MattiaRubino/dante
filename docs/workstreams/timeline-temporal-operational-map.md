# Timeline / Temporal-Operational Vertical — Semantic Work Map / Live Ledger

- **Status:** CURRENT SEMANTIC MAP + LIVE IMPLEMENTATION LEDGER — reconciled 2026-09-23
- **Branch:** `feature/timeline-temporal-operational`
- **Roadmap:** `docs/workstreams/timeline-temporal-operational-roadmap.md`
- **Post-B06 scope decision:** `docs/workstreams/timeline-temporal-operational-post-b06-scope-decision-2026-09-23.md`
- **B06 whole-block closure:** `docs/workstreams/timeline-temporal-operational-b06-e-closure-2026-09-23.md`
- **Timeline candidate DB overlay:** `docs/database/timeline-temporal-operational.md`

This file is the live implementation/proof ledger. Historical snapshots and closure records preserve chronology; they do not compete with current authority.

---

# 1. Vertical boundary

```text
Home `+`
→ create/configure Activity / Event / Routine and later-owned bounded facets
→ canonical backend / PostgreSQL truth
→ Timeline projection
→ Schedule / recurrence / runtime / lifecycle actions
→ bounded completion of the Timeline experience
```

This is not an all-DANTE roadmap.

Explicit future/out-of-scope work:

```text
external provider integration
native/mobile app
advanced offline / multi-device sync
account-to-account collaboration
chat/shared editing
broad analytics/statistics/signals vertical
```

---

# 2. Permanent semantic boundaries

```text
Person != Account != Principal != Actor
Goal != Plan != Activity
Activity != Event != Routine
Routine != Recurrence != Occurrence
Occurrence != Schedule
Schedule != Temporal Constraint
Schedule != Movement Policy
Temporal Constraint != Movement Policy
Movement Policy != Authority itself
Movement Policy != solver result
Schedule != Session
Schedule != Actual
Session != Actual
Actual != Outcome
Outcome != Confirmation
Responsibility != Participation
participant != Account identity
planned/intended != happened
proposal != accepted effect
pending != success
current accepted state != latest row
idempotency key != Domain identity
provider identity != DANTE identity
projection != canonical truth
unscheduled != deleted
Undo != DB/history rewind
estimated effort != scheduled duration != Session duration
planned Schedule duration != Actual duration
floating-local != named-zone-local != absolute instant
date span != coarse local period
coarse precision != fabricated exact clock time
Agenda part != Activity/Event/Occurrence/Schedule/Session/Actual by default
Event != Availability / Capacity Claim
postponed/TBD Event != Planning Tray Activity
window != placement
preference != accepted Schedule
evaluation != solver decision
violation != automatic mutation
policy revision != Schedule revision
constraint revision != Schedule revision
solver proposal != accepted Schedule
AI output != accepted effect
```

---

# 3. Current roadmap position

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
B09 Responsibility / Participation               ⬜
B10 Actual / Outcome / Confirmation / Resolution ⬜
B11 Advanced Recurrence / Conditional / Reminder ⬜
B12 Replanning / Conflict / Solver               ⬜
B07 UI/UX Consolidation v1                       ⏸ DEFERRED UNTIL B08–B12 EXIST
B15 Whole Vertical Closure                       ⬜
```

Former B13 Provider/Offline/Multi-device and B14 Analytics/Statistics/Signals are removed from the active vertical sequence and retained only as future backlog concepts outside this workstream. Their historical identifiers are not reassigned.

Current candidate persistence authority:

```text
PostgreSQL       18.6
Alembic source   20260923_57
Proven topology  145|5|88|92|285|223|408|0|0|0
```

---

# 4. Completed foundation B00–B06

## B00–B03 ✅

Real Data Spine, Activity Core, shared Schedule Core and Event Core are established. Event remains distinct from Activity while reusing shared Schedule authority; Agenda remains Event-internal value truth.

## Pre-B04 governance ✅

DB same-change reconciliation and Temporal API inventory/operationId/OpenAPI generation rules remain binding for all later slices.

## B04 ✅

Temporal Constraint boundary/window/planned-duration semantics plus separate Movement Policy are proven. Deterministic evaluation remains derived and does not search for candidates or mutate Schedule by itself.

Deferred B04 families carried forward:

```text
TC-009 contiguous Session duration  → B08
TC-010 spacing/recovery             → later anchor-specific reopening
TC-011 relative before/after        → reviewed bounded relation/reference persistence required
```

## B05 ✅

Life Area catalog/lifecycle, typed primary assignment, separate secondary Tags and real Timeline organization are proven. Life Area/Tag remain product organization rather than new Domain roots.

## B06 ✅

```text
B06-A Routine source core                        ✅ CLOSED / PROVEN at `_51`
B06-B Recurrence authoring                       ✅ CLOSED / PROVEN at `_54`
B06-C canonical Occurrence checkpoint            ✅ CLOSED / PROVEN at `_55`
B06-D shared Schedule / Timeline / functional UI ✅ CLOSED / PROVEN at `_57`
B06-E whole-block closure                        ✅ CLOSED / PROVEN at `_57`
```

B06 preserves `Routine != Recurrence != Occurrence != Schedule`; expected/scheduled Timeline projection does not duplicate one canonical Occurrence; source organization is inherited rather than cloned.

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

---

# 5. B08 ownership — Session Runtime ← NEXT

B08 activates only the Session semantics required by the Timeline vertical.

Required questions before implementation:

```text
which owner(s) can open a Session?
what is the exact Session lifecycle?
what is active vs elapsed duration?
how does pause/resume behave?
what survives reload?
which current/history/idempotency rules apply?
how does Timeline expose the runtime state without collapsing Schedule or Actual?
which B04 TC-009/TC-010 semantics become evaluable now?
```

Forbidden collapse:

```text
Schedule timestamp == actual Session start
Session completion == Actual/Outcome by default
planned duration == Session duration
```

---

# 6. B09 ownership — Responsibility / Participation

B09 is role semantics, not collaboration infrastructure.

Possible bounded relationships are reviewed against Product/Domain/Logical authority before persistence is selected. A Person/referent may participate without owning a DANTE Account; future account linkage is separate.

Out of scope:

```text
cross-account collaboration
chat
shared edit grants
account invitation flow
```

---

# 7. B10 ownership — Actual / Outcome / Confirmation / Resolution

B10 owns happened-reality semantics required to complete the Timeline lifecycle.

```text
planned/intended != happened
Session != Actual
Actual != Outcome
Outcome != Confirmation
```

Time passage never proves execution.

---

# 8. B11 ownership — Advanced Recurrence / Conditional / Reminder

B11 completes advanced recurrence/reminder authoring and Timeline behavior after B06 baseline and after later anchors exist.

It does not authorize a generic IFTTT engine, RRULE ontology or opaque JSON recurrence root.

---

# 9. B12 ownership — Replanning / Conflict / Solver

B12 is deterministic-first candidate search/optimization and governed Proposal handling.

```text
canonical Schedule + constraints/preferences
→ deterministic candidate generation / optimization
→ Proposal(s)
→ optional AI interpretation/explanation/ranking assistance
→ governed acceptance
→ canonical Schedule mutation
```

AI is optional support, not canonical scheduling authority.

---

# 10. B07 ownership — UI/UX Consolidation v1 — DEFERRED

B07 executes only after B08–B12 exist. Until then UI may be deliberately utilitarian but must remain truthful, usable and testable.

B07 consolidates `+`, Timeline, editors, lifecycle controls, responsibility/participation, advanced recurrence/reminders and replanning proposals without changing canonical semantics for visual convenience.

---

# 11. B15 ownership — Whole Vertical Closure

B15 closes the bounded `+`/Timeline vertical only. Provider integration, native/offline, general analytics and account collaboration are not closure blockers.

---

# 12. Current gate

```text
B00–B06 ✅ CLOSED / PROVEN
B07     ⏸ DEFERRED
B08     ← NEXT / NOT STARTED
B09–B12 ⬜ NOT STARTED
B15     ⬜ NOT STARTED
```

Next action: B08 pre-scope and authority reconciliation from `_57`. No CI/Actions are launched by this ledger.