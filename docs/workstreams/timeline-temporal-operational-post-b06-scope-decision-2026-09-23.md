# Timeline / Temporal-Operational — Post-B06 Scope and Sequencing Decision

- **Status:** CURRENT / ACCEPTED SEQUENCING AUTHORITY
- **Date:** 2026-09-23
- **Branch:** `feature/timeline-temporal-operational`
- **Prior completed frontier:** B06 ✅ CLOSED / PROVEN
- **Next implementation block:** B08 Session Runtime
- **Candidate DB frontier:** PostgreSQL 18.6 / Alembic `20260923_57`
- **Candidate proven topology:** `145|5|88|92|285|223|408|0|0|0`

## 1. Vertical boundary

This workstream is the implementation vertical for the Home `+` creation surface and the Timeline semantics/actions that originate from or complete that surface.

A capability belongs in this vertical only when it is required to:

```text
create/configure something through `+`
→ represent it truthfully in Timeline
→ operate on its temporal/lifecycle state from Timeline
→ complete the bounded lifecycle needed by that Timeline experience
```

This vertical is **not** a mandate to implement all of DANTE.

## 2. Accepted post-B06 sequence

The active execution order is:

```text
B08 Session Runtime                              ← NEXT
B09 Responsibility / Participation
B10 Actual / Outcome / Confirmation / Resolution
B11 Advanced Recurrence / Conditional / Reminder
B12 Replanning / Conflict / Solver
B07 UI/UX Consolidation v1                       ← DEFERRED UNTIL CAPABILITIES EXIST
B15 Whole Vertical Closure
```

B07 keeps its historical block identifier but is deliberately executed after B12. The purpose is to avoid repeatedly redesigning `+`, editors and Timeline while their capability vocabulary is still incomplete.

The implementation UI during B08–B12 may be functional and deliberately unpolished. It must remain truthful, testable and accessible enough for real-stack/manual proof, but final visual/interaction consolidation is owned by deferred B07.

## 3. B08 bounded scope — Session Runtime

B08 activates Session only as needed by this vertical: a Timeline-linked execution episode for something the user intends/plans to do.

Expected bounded capabilities include start/pause/resume/stop or equivalent runtime lifecycle where justified by current Product/Domain/Logical authority.

Permanent distinctions:

```text
Schedule != Session
Session != Actual
planned duration != Session elapsed/active duration
```

B08 does not become a generic runtime/workflow platform.

## 4. B09 bounded scope — Responsibility / Participation

B09 models roles/participation around Activity/Event/Routine/Occurrence where needed by `+`, editors and Timeline.

It does **not** activate collaboration between DANTE accounts.

A participant/responsible subject may be represented as a Person/referent according to existing authority without requiring that subject to own a DANTE Account. A future capability may link an existing Person/referent to a real DANTE Account without changing the original participation meaning.

Explicitly out of scope for B09:

```text
account-to-account collaboration
chat/messaging
shared object editing
invitation delivery
cross-account grants/authorization model
social notifications
```

Permanent distinctions:

```text
Responsibility != Participation
participant != Account identity
performer change != Occurrence identity change
```

## 5. B10 bounded scope — Actual / Outcome / Confirmation / Resolution

B10 completes the Timeline lifecycle from intention/planning toward happened reality without collapsing the stages.

```text
intended / expected
→ optionally planned
→ optionally Session/runtime
→ Actual / realized fact where justified
→ Outcome
→ Confirmation / Observation / Evidence where applicable
```

Permanent rule:

```text
planned/intended != happened
time passage != execution proof
Actual != Outcome
Outcome != Confirmation
```

## 6. B11 bounded scope — Advanced Recurrence / Conditional / Reminder

B11 completes the recurrence/reminder semantics needed by `+`, structured editing and Timeline after the B06 baseline.

It may reopen families intentionally deferred by B06 when their required anchors now exist, including completion-relative or other bounded advanced recurrence semantics.

It must not introduce a generic automation/IFTTT ontology or use RRULE/JSON as the canonical semantic model.

## 7. B12 bounded scope — Replanning / Conflict / Solver

B12 owns candidate generation, conflict handling and replanning proposals over the canonical planning model already built by B02/B04/B06 and later blocks.

The solver is **deterministic-first**. The accepted target may use deterministic constraint/optimization tooling such as the already selected OR-Tools CP-SAT physical target where appropriate.

AI is optional as an interpretation/explanation/ranking layer. It is not canonical scheduling authority.

```text
constraints/preferences/current Schedule truth
→ deterministic candidate generation / optimization
→ Proposal(s)
→ optional AI explanation/intent assistance
→ explicit governed acceptance path
→ canonical Schedule mutation
```

Permanent distinctions:

```text
evaluation != solver decision
solver proposal != accepted Schedule
AI output != accepted effect
```

## 8. B07 deferred UI/UX consolidation

B07 is not cancelled. It is deliberately deferred until B08–B12 capabilities are implemented so final consolidation can see the complete `+`/Timeline vocabulary.

B07 will then consolidate at least:

```text
Home / Timeline
`+` Create
Activity/Event/Routine editors
Occurrence actions
Schedule / constraint / recurrence interaction
Session / Actual lifecycle interaction
Responsibility / Participation presentation
Reminder / advanced recurrence controls
solver/replanning proposals
loading / empty / error / responsive / accessibility states
```

It must consolidate presentation and interaction without weakening Domain/Logical/Persistence boundaries.

## 9. Removed from this vertical

The former roadmap placeholders B13 and B14 are removed from the active vertical sequence.

### External provider integration — FUTURE / OUTSIDE THIS VERTICAL

Examples: Google Calendar, Outlook, provider import/export/sync, provider conflict resolution.

These capabilities add OAuth/token/webhook/provider-state complexity but are not required to complete DANTE's own `+`/Timeline vertical. They remain future backlog work.

### Analytics / statistics / general signals — FUTURE / OUTSIDE THIS VERTICAL

General analytics/read-model work is also outside this vertical unless a narrowly derived value is strictly required to operate a specific `+`/Timeline capability.

### Native/mobile/offline/multi-device — FUTURE / OUTSIDE THIS VERTICAL

No native app, offline-first database or advanced multi-device reconciliation is activated by this workstream.

The historical identifiers B13/B14 are not reassigned to new semantics; historical documents may continue to mention their former planned meaning as phase-time evidence.

## 10. Whole-vertical closure

B15 remains the stable final closure label for this workstream.

It closes only the bounded vertical described here:

```text
`+` creation/configuration
→ canonical backend/persistence truth
→ Timeline projection/operations
→ required execution/reality lifecycle
→ advanced recurrence/reminders
→ replanning/conflict/solver proposals
→ final UI/UX consolidation
```

Provider integrations, general analytics, native/offline and account collaboration are not B15 blockers.

## 11. Permanent non-collapse set carried forward

```text
Domain != Logical != Physical != API DTO != ViewModel
Person != Account != Principal != Actor
Activity != Event != Routine
Routine != Recurrence != Occurrence
Occurrence != Schedule
Schedule != Temporal Constraint != Movement Policy
Schedule != Session != Actual
Session != Actual != Outcome
Actual != Outcome != Confirmation
Responsibility != Participation
planned/intended != happened
proposal != accepted effect
current accepted state != latest row
projection != canonical truth
idempotency key != Domain identity
provider identity != DANTE identity
Undo != history rewind
```

No implementation block may collapse these distinctions merely to simplify UI or persistence.