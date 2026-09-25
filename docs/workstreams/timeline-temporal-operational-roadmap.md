# Timeline / Temporal-Operational Vertical — Implementation Roadmap

- **Status:** CURRENT EXECUTION ROADMAP — reconciled 2026-09-25
- **Branch/workstream:** `feature/timeline-temporal-operational`
- **Vertical boundary:** Home `+` creation/configuration → canonical temporal truth → Timeline projection/actions → bounded lifecycle completion
- **Completed functional frontier:** B08 Session Runtime ✅ CLOSED / USER-REPORTED 2026-09-24
- **Current block:** B09 Responsibility / Participation 🟨 IN PROGRESS — B09-A/B closed; B09-C next, B09-D pending
- **Last proven candidate DB frontier:** B09-B / PostgreSQL 18.6 / Alembic `20260925_68` / topology `156|5|106|93|301|251|426`
- **Deferred block:** B07 UI/UX Consolidation v1 — execute only after the functional/create-completeness sequence below
- **Live execution ledger:** `docs/workstreams/timeline-temporal-operational-map.md`
- **Continuation handoff:** `docs/workstreams/timeline-temporal-operational-handoff.md`

This document is the sequencing authority for the remaining Timeline / Temporal-Operational work.

---

# 0. Execution discipline

Every functional block closes vertically:

```text
current Product / Domain / Logical / Physical authority
→ persistence / Alembic / Dictionary when required
→ backend / application
→ HTTP API / OpenAPI when public
→ generated API client when public
→ frontend / real product surface when part of the block
→ local automated proof
→ real-stack manual proof where user behavior matters
→ documentation reconciliation
→ only then advance
```

Temporary UI is acceptable before B07, but an editable product field must never silently pretend to be canonical when the owning capability does not exist yet.

Permanent rules:

```text
Domain != Logical != Physical != API DTO != frontend ViewModel
projection != canonical truth
planned/intended != happened
Activity != Event != Routine
Routine != Recurrence != Occurrence
Occurrence != Schedule
Schedule != Session != Actual
Session != Actual != Outcome
Actual != Outcome != Confirmation
Expected outcome != Outcome
Responsibility != Participation
participant != responsible actor != organizer/owner
Person != Account
Step != Activity
Plan != Activity
Dependency != hierarchy
ordering != dependency
proposal != accepted effect
current accepted state != latest row
MaterialState payload != mutable runtime record
idempotency key != Domain identity
Undo != history rewind
editable Create intent != canonical persistence
```

Documentation stays small:

```text
ROADMAP = sequence/boundaries
MAP     = live decisions/evidence
HANDOFF = exact current position and next action
```

---

# 1. Active execution order

Historical block identifiers are preserved. Execution order is intentionally non-numeric where dependencies require it.

```text
B00 Real Data Spine                              ✅ CLOSED / PROVEN
B01 Activity Core                                ✅ CLOSED / PROVEN
B02 Schedule Core                                ✅ CLOSED / PROVEN
B03 Event Core                                   ✅ CLOSED / PROVEN
PRE-B04 DB/API GOVERNANCE                        ✅ CLOSED / FROZEN
B04 Temporal Constraints + Movement Policy       ✅ CLOSED / PROVEN
B05 Product Organization                         ✅ CLOSED / PROVEN
B06 Routine / Recurrence / Occurrence Baseline   ✅ CLOSED / PROVEN

B08 Session Runtime                              ✅ CLOSED / USER-REPORTED 2026-09-24
  B08-A Session Core End-to-End                   ✅ CLOSED / USER-REPORTED
  B08-B Pause / Resume + Durations End-to-End     ✅ CLOSED / USER-REPORTED
  B08-C TC-009 Session Duration End-to-End        ✅ CLOSED / PROVEN — local automated gate 2026-09-24
  B08-D Whole-block closure                       ✅ CLOSED / USER-REPORTED — automated gate and dogfood

B09 Responsibility / Participation               🟨 IN PROGRESS
  B09-A typed persistence substrate               ✅ CLOSED / PROVEN 2026-09-25
  B09-B guarded mutation + application surface    ✅ CLOSED / PROVEN 2026-09-25
  B09-C remaining Responsibility / Participation  ⬜ NEXT — exact scope to reconcile
  B09-D B09 whole-block closure                    ⬜ AFTER B09-C — exact scope to reconcile
B10 Actual / Outcome / Confirmation / Resolution ⬜
B11 Advanced Recurrence / Conditional / Reminder ⬜
B13 Work Structure / Decomposition / Dependencies⬜
B12 Replanning / Conflict / Solver               ⬜
B14 Temporal Create Completeness Gate             ⬜
B07 UI/UX Consolidation v1                       ⏸ DEFERRED UNTIL B14
B15 Whole Vertical Closure                       ⬜
```

Execution sequence after B08 remains:

```text
B09 → B10 → B11 → B13 → B12 → B14 → B07 → B15
```

B13 exists before B12 because replanning/solver logic must already understand work structure and dependencies. B14 exists before B07 so final UI consolidation does not polish editable fields that are still non-canonical or unsupported.

External providers, native/offline/multi-device and account collaboration remain future backlog unless a bounded handoff is explicitly needed by one of these blocks.

---

# 2. Completed foundation B00–B08

B00–B06 and B08 are closed. Permanent temporal boundaries at the B09 entry point include:

```text
Activity may exist without Schedule
Event != Activity
Routine != Recurrence != Occurrence
Occurrence != Schedule
Schedule is the shared accepted-placement authority
Life Area / Tags are product organization, not Domain ownership
Session != Actual
Session END != completion
```

B08 proven/user-reported candidate chain ends at `20260924_65`.

---

# 3. B09 — Responsibility / Participation — IN PROGRESS

B09 adds actor/person semantics around temporal subjects without introducing account collaboration infrastructure.

Required boundaries:

```text
Person != Account
Responsibility != Participation
participant != responsible actor != organizer/owner
shared Event truth != actor-specific participation truth
expected/response Participation != Actual Participation
participation/attendance state != Event Actual
another person's participation != DANTE authority over that person's calendar/task system
```

Do not add a generic participant JSON/blob or make provider attendee identity canonical ontology.

## B09-A — typed persistence substrate — CLOSED / PROVEN

`20260925_66` adds exactly three typed direct/current relation tables:

```text
event_expected_participation(Event, Person, required|optional)
activity_responsibility(Activity, Person)
event_responsibility(Event, Person)
```

B09-A deliberately stops before guarded mutation/application/API/frontend and before Actual attendance semantics.

Local user-run proof on 2026-09-25:

```text
pytest focused B09-A persistence + both current-catalog suites
10 passed
```

Proven candidate DB frontier:

```text
Alembic  20260925_66
Topology 153|5|99|93|298|242|419
```

## B09-B — CLOSED / PROVEN

B09-B owns the guarded mutation/application layer over the B09-A substrate and the public API/OpenAPI/generated-client/Timeline surface.

It preserves:

```text
raw relation tables are not runtime mutation surfaces
Person identity is not Account identity
the public holder/participant vocabulary is only "self" in this slice
expected Participation does not establish acceptance/attendance/Actual
Responsibility does not imply Participation
participant authoring does not grant control over another person's calendar/task system
```

Home `+` required/optional participant textareas remain B14. Timeline detail is the truthful B09 authoring surface.

User-run local automated proof on 2026-09-25: generated check and both typechecks passed, web responsibility controls 4 passed, backend B09-B/B09-A/catalog/OpenAPI 18 passed. B09-B alone closes on this evidence; B09-C and B09-D remain, and real-stack testing is deferred to B15 whole-vertical closure.

## B09-C / B09-D — NOT STARTED

B09-C is the next Responsibility / Participation slice; B09-D is the subsequent whole-block closure. Their precise deliverables must be reconciled with the accepted B09 scope in `timeline-temporal-operational-post-b06-scope-decision-2026-09-23.md` and the current Product / Domain / Logical / Physical authority before implementation. The current roadmap does not define those deliverables: B09-B's bounded `self` surface must not be treated as proof that all B09 product flows are complete. Neither slice is covered by B09-B's tests. B15 retains the user's end-of-vertical real-stack test.

---

# 4. Remaining functional blocks

## B10 — Actual / Outcome / Confirmation / Resolution

B10 adds realization/reconciliation semantics while preserving:

```text
planned/intended != happened
Schedule != Session != Actual
Session END != completion
Actual != Outcome != Confirmation
Expected outcome != Outcome
no Actual != known non-realization/failure
```

B10 also owns the canonical behavior behind the existing Create confirmation policy and execution intents whose meaning depends on realized results, notably partial completion and finish-early semantics. Fast outcomes such as completed/partial/skipped/not-completed/postponed/replaced/cancelled must be represented without collapsing Actual, Outcome and Confirmation.

## B11 — Advanced Recurrence / Conditional / Reminder

B11 extends recurrence and conditional/reminder behavior without RRULE-as-ontology, fake Activity materialization or an unjustified universal Reminder owner.

The existing editable Create reminder field must leave B11 either canonically supported, truthfully handed off, or hidden until that capability exists.

## B13 — Work Structure / Decomposition / Dependencies

B13 distinguishes:

```text
1. INTERNAL STEP
   ordered/internal execution structure of one Activity
   Step != Activity

2. COMPOSITE WORK
   Plan or other legitimate composition containing real Activities
   each Activity keeps its own identity/lifecycle/Schedule/Session

3. DEPENDENCY
   typed relationship between independently meaningful work
   Dependency != hierarchy
   ordering != dependency
```

Examples such as `English lesson → speaking/writing/grammar` must be representable either as internal steps or as independently meaningful Activities; the UI must not force both cases into one generic `sub_item` model.

B13 also closes the temporal execution-structure foundation already exposed by Create where semantically appropriate: maximum Session count, merge compatibility, spacing, preparation/recovery and related structure rules.

Permanent boundaries:

```text
Step != Activity
Plan != Activity
Dependency != hierarchy
ordering != dependency
child Schedule != parent Schedule
child Session != parent Session
all children resolved != parent Actual unless an explicit policy establishes that meaning
```

## B12 — Replanning / Conflict / Solver

B12 is deterministic-first replanning/conflict/solver and owns preferred windows, movement policies, fallback policies and dependency-aware replanning.

```text
canonical truth + constraints/preferences + B13 dependencies
→ deterministic candidate generation / optimization
→ Proposal(s)
→ optional AI interpretation/ranking assistance
→ governed acceptance
→ canonical Schedule mutation
```

Hard constraints are never violated silently.

```text
proposal != accepted Schedule
preferred window != accepted Schedule
fallback policy != automatic hidden mutation
solver UNKNOWN != INFEASIBLE
AI != scheduling authority
```

---

# 5. B14 — Temporal Create Completeness Gate

For every editable field visible in Create, exactly one must be true:

```text
A. canonically persisted and covered by behavioral proof
B. truthful handoff to the owning vertical/capability
C. explicitly presentation/read-only
D. hidden/removed until supported
```

Forbidden:

```text
editable field
→ value collected by UI
→ normal submit silently ignores it or rejects it only because backend support is absent
```

The gate audits Notes, appearance override, Tags, confirmation/reminder policy, execution-structure policy, Event location/availability/visibility, Event purpose/expected outcome/decision requirement, required/optional participants, resources/pre-read and conference/provider fields.

B14 does not force every field into the Temporal kernel. Truthful ownership matters more than maximal scope.

---

# 6. B07 — UI/UX Consolidation v1 — DEFERRED

Execute after B14 so final Home/Timeline/`+`/editors/actions/navigation are designed once against a truthful functional vocabulary. B07 does not create missing semantics.

---

# 7. B15 — Whole Vertical Closure

B15 reconciles migrations/catalog/Dictionary, backend/API/client, frontend, negative invariants, local automated proof, required real-stack walkthroughs and the live documentation ledger.

B15 must include a red-team semantic audit for accidental collapses such as:

```text
Activity == Event
Routine == Recurrence
Occurrence == Schedule
Schedule == Session
Session END == completion/Actual
Expected outcome == Outcome
Responsibility == Participation
Participant == Account
Step == Activity
Dependency == hierarchy
editable Create field == assumed canonical support
```

---

# 8. Current gate

```text
B00–B06 ✅ CLOSED / PROVEN
B08     ✅ CLOSED / USER-REPORTED 2026-09-24
B09     🟨 IN PROGRESS
  B09-A ✅ CLOSED / PROVEN 2026-09-25
  B09-B ✅ CLOSED / PROVEN 2026-09-25
  B09-C ⬜ NEXT — scope to reconcile
  B09-D ⬜ AFTER B09-C — scope to reconcile
B10     ⬜ NOT STARTED
B11     ⬜ NOT STARTED
B13     ⬜ NOT STARTED
B12     ⬜ NOT STARTED
B14     ⬜ NOT STARTED
B07     ⏸ DEFERRED UNTIL B14
B15     ⬜ NOT STARTED
```

**Current action:** reconcile the exact B09-C/B09-D scope against the accepted authority, then proceed with B09-C. B10 follows B09-D; the user's real-stack test remains B15 scope.
