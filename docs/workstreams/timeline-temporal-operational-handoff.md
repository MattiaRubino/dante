# Timeline / Temporal-Operational — Workstream Handoff

- **Status:** B06 ✅ CLOSED / PROVEN → B08 SESSION RUNTIME NEXT
- **Reconciled:** 2026-09-23
- **Branch:** `feature/timeline-temporal-operational`
- **Current roadmap:** `docs/workstreams/timeline-temporal-operational-roadmap.md`
- **Current live map/ledger:** `docs/workstreams/timeline-temporal-operational-map.md`
- **Post-B06 scope decision:** `docs/workstreams/timeline-temporal-operational-post-b06-scope-decision-2026-09-23.md`
- **B06 whole-block closure:** `docs/workstreams/timeline-temporal-operational-b06-e-closure-2026-09-23.md`
- **Timeline candidate DB overlay:** `docs/database/timeline-temporal-operational.md`
- **CI:** no CI launch is implied or authorized

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

B08 Session Runtime                              ← NEXT
B09 Responsibility / Participation               ⬜
B10 Actual / Outcome / Confirmation / Resolution ⬜
B11 Advanced Recurrence / Conditional / Reminder ⬜
B12 Replanning / Conflict / Solver               ⬜
B07 UI/UX Consolidation v1                       ⏸ DEFERRED UNTIL B08–B12 EXIST
B15 Whole Vertical Closure                       ⬜
```

Former B13 Provider/Offline/Multi-device and B14 Analytics/Statistics/Signals are outside this vertical. Their historical identifiers are not reassigned.

Current candidate DB:

```text
PostgreSQL      18.6
Alembic source  20260923_57
Proven topology 145|5|88|92|285|223|408|0|0|0
```

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

## 6. B08 next boundary — Session Runtime

B08 must begin with authority/pre-scope reconciliation before implementation.

Questions to resolve explicitly:

```text
which canonical owner(s) can have/start a Session?
what exact Session identity/lifecycle is already defined by Domain/Logical/Physical?
what does start/pause/resume/stop mean semantically?
what is elapsed vs active duration?
what state is current/history and how is it revised?
what idempotency/CAS rules apply?
how does Session attach to Activity/Event/Routine/Occurrence/Schedule without collapse?
how does Timeline project active/paused/stopped runtime state?
which B04 TC-009/TC-010 constraints become evaluable now?
what is explicitly deferred to B10 Actual/Outcome?
```

Forbidden assumptions:

```text
scheduled start == actual Session start
Session end == Actual completion by default
Session existence == Outcome
planned duration == Session duration
```

No migration is pre-authorized. Inspect current physical/database support first and add forward-only DDL only for a proven gap.

## 7. B09 later boundary — Responsibility / Participation

B09 is role semantics around Activity/Event/Routine/Occurrence, not collaboration infrastructure.

A participant/responsible subject may exist as a Person/referent without a DANTE Account. A future account linkage can be added without changing the participation meaning.

Out of scope:

```text
account-to-account collaboration
chat
shared editing
invitation delivery
cross-account grants
```

## 8. B10 later boundary — Actual / Outcome / Confirmation / Resolution

B10 owns happened-reality semantics required to complete the Timeline lifecycle.

```text
planned/intended != happened
Session != Actual
Actual != Outcome
Outcome != Confirmation
```

Time passage never proves execution.

## 9. B11 later boundary — Advanced Recurrence / Conditional / Reminder

B11 completes recurrence/reminder semantics needed by `+`, editors and Timeline once later anchors exist. No generic RRULE ontology, opaque JSON rule bag or IFTTT-style canonical engine is authorized.

## 10. B12 later boundary — Replanning / Conflict / Solver

B12 is deterministic-first candidate generation/optimization and Proposal handling.

```text
canonical truth + constraints/preferences
→ deterministic solver/candidate generation
→ Proposal(s)
→ optional AI interpretation/explanation/ranking assistance
→ governed acceptance
→ canonical Schedule mutation
```

AI is optional support, not scheduling authority.

## 11. Current gate

```text
B06 ✅ CLOSED / PROVEN at `_57`
B07 ⏸ DEFERRED
B08 ← NEXT / NOT STARTED
```

Current action: prepare B08 pre-scope from the proven `_57` frontier. Do not start B09+ opportunistically. No CI/Actions are authorized by this handoff.