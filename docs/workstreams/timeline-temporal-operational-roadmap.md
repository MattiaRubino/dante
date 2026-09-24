# Timeline / Temporal-Operational Vertical — Implementation Roadmap

- **Status:** CURRENT EXECUTION ROADMAP — reconciled 2026-09-24
- **Branch/workstream:** `feature/timeline-temporal-operational`
- **Vertical boundary:** Home `+` creation/configuration → canonical temporal truth → Timeline projection/actions → bounded lifecycle completion
- **Completed functional frontier:** B08 Session Runtime ✅ CLOSED / USER-REPORTED 2026-09-24
- **Current block:** B09 Responsibility / Participation ⬜ NOT STARTED
- **Last proven candidate DB frontier:** B08-C / PostgreSQL 18.6 / Alembic `20260924_65` / topology `150|5|99|93|292|236|418|0|0|0`
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

B09 Responsibility / Participation               ⬜ NEXT
B10 Actual / Outcome / Confirmation / Resolution ⬜
B11 Advanced Recurrence / Conditional / Reminder ⬜
B13 Work Structure / Decomposition / Dependencies⬜
B12 Replanning / Conflict / Solver               ⬜
B14 Temporal Create Completeness Gate             ⬜
B07 UI/UX Consolidation v1                       ⏸ DEFERRED UNTIL B14
B15 Whole Vertical Closure                       ⬜
```

Execution sequence after B08:

```text
B09 → B10 → B11 → B13 → B12 → B14 → B07 → B15
```

B13 exists before B12 because replanning/solver logic must already understand work structure and dependencies. B14 exists before B07 so final UI consolidation does not polish editable fields that are still non-canonical or unsupported.

External providers, native/offline/multi-device and account collaboration remain future backlog unless a bounded handoff is explicitly needed by one of these blocks.

---

# 2. Completed foundation B00–B06

B00–B06 are closed/proven. Their permanent boundary at the B08 entry point is:

```text
Activity may exist without Schedule
Event != Activity
Routine != Recurrence != Occurrence
Occurrence != Schedule
Schedule is the shared accepted-placement authority
Life Area / Tags are product organization, not Domain ownership
```

Proven B06 frontier:

```text
Alembic  20260923_57
Topology 145|5|88|92|285|223|408|0|0|0
```

---

# 3. B08 — Session Runtime — CLOSED

B08 activated execution episodes without collapsing planned Schedule or later happened-reality semantics.

```text
Activity != Session
Occurrence != Session
Schedule != Session
Session != Actual
Session != Outcome
Session END != Activity completion
Session END != Occurrence completion
planned Schedule duration != Session elapsed duration
Session elapsed duration != Session active duration
```

Implemented candidate chain:

```text
_58 typed Session subject + bounded START/READ/END
_59 exact Activity-vs-Occurrence family enforcement
_60 immutable END MaterialState transition + exact replay receipt
_62 pause/resume persistence
_63 transition replay repair
_64 runtime metrics
_65 direct Activity soft minimum on Session active duration + read-time evaluation
```

B08-D closed on 2026-09-24 from the user's local and dogfood evidence: generated/client checks passed, focused Web suite passed 58 tests, backend PostgreSQL/unit/API command passed 31 tests, the post-fix Web typecheck passed by user confirmation, and the real app confirms timed and unplaced Activity placement plus START/PAUSE/RESUME/END. Detailed repair history and observed results remain in the map and handoff.

Forbidden effects remain permanent:

```text
START does not fabricate Schedule
END does not complete Activity
END does not resolve Occurrence
END does not create Actual
END does not create Outcome
TC-009 evaluation does not block transitions or mutate Schedule/Actual/Outcome
```

---

# 4. Remaining functional blocks

## B09 — Responsibility / Participation

B09 adds actor/person semantics around temporal subjects without introducing account collaboration infrastructure.

It owns the truthful Temporal subset of participant/responsibility authoring, including the existing Event create fields where they can be represented canonically.

Required boundaries:

```text
Person != Account
Responsibility != Participation
participant != responsible actor != organizer/owner
shared Event truth != actor-specific participation truth
participation/attendance state != Event Actual
another person's participation != DANTE authority over that person's calendar/task system
```

Do not add a generic participant JSON/blob or make provider attendee identity canonical ontology.

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

The existing editable Create reminder field must leave B11 either:

```text
canonically supported by its correct owner/capability
OR
truthfully handed off to the owning vertical
OR
hidden until that capability exists
```

B14 will verify the final result; B11 must not leave a knowingly fake editable field behind.

## B13 — Work Structure / Decomposition / Dependencies

B13 is the one missing functional block identified by the create-flow audit. It is intentionally compact and must not become a generic project-management ontology.

It distinguishes three different concepts:

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

B13 also closes the temporal execution-structure foundation already exposed by Create where semantically appropriate: maximum Session count, merge compatibility, spacing, preparation/recovery and related structure rules. It does not turn those policies into Session history or completion truth.

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

B12 is deterministic-first replanning/conflict/solver and owns the still-latent planning semantics exposed by Create: preferred windows, movement policies, fallback policies and dependency-aware replanning.

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

B14 is a gate, not a new product mega-feature. It closes the mismatch discovered by auditing Home `+`.

For every editable field visible in Create, exactly one must be true:

```text
A. canonically persisted and covered by behavioral proof
B. truthful handoff to the owning vertical/capability
C. explicitly presentation/read-only
D. hidden/removed until supported
```

Forbidden state:

```text
editable field
→ value collected by UI
→ normal submit silently ignores it or rejects it only because backend support is absent
```

The gate explicitly audits the current latent surface, including:

```text
Notes
appearance override
Tags
confirmation/reminder policy
execution-structure policy
Event location / availability / visibility
Event purpose / expected outcome / decision requirement
required/optional participants
resources / pre-read / conference integration
```

B14 does **not** force every field into the Temporal kernel. Fields owned by Work, Content, provider integrations or another vertical may remain handoffs or be hidden. The requirement is truthful ownership, not maximal scope.

---

# 6. B07 — UI/UX Consolidation v1 — DEFERRED

Execute after B14 so final Home/Timeline/`+`/editors/actions/navigation are designed once against a truthful functional vocabulary. B07 does not create missing semantics; it consolidates presentation and interaction after those semantics are either implemented, handed off or removed from the editable surface.

---

# 7. B15 — Whole Vertical Closure

B15 is the final cross-block closure. It reconciles migrations/catalog/Dictionary, backend/API/client, frontend, negative invariants, local automated proof, required real-stack walkthroughs and the live documentation ledger.

B15 must include a red-team semantic audit for accidental collapses such as:

```text
Activity == Event
Routine == Recurrence
Occurrence == Schedule
Schedule == Session
Session END == completion/Actual
Expected outcome == Outcome
Step == Activity
Dependency == hierarchy
editable Create field == assumed canonical support
```

---

# 8. Current gate

```text
B00–B06 ✅ CLOSED / PROVEN
B08     ✅ CLOSED / USER-REPORTED 2026-09-24
B09     ⬜ NEXT
B10     ⬜ NOT STARTED
B11     ⬜ NOT STARTED
B13     ⬜ NOT STARTED
B12     ⬜ NOT STARTED
B14     ⬜ NOT STARTED
B07     ⏸ DEFERRED UNTIL B14
B15     ⬜ NOT STARTED
```

**Current action:** Define and implement B09 Responsibility / Participation from the B08-closed frontier.
