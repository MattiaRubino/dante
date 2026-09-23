# DANTE Roadmap

- **Status:** CURRENT REPOSITORY ROADMAP — reconciled 2026-09-23
- **Pre-vertical integration merge:** `1ecd58145860aebfaaa3dc78933f4ee42698f33` via PR #66
- **Protected-main baseline at temporal selection:** PostgreSQL 18.6 / Alembic `20260906_18` / topology `89|5|18|77|173|91|272|0|0|0`
- **Active candidate workstream:** `feature/timeline-temporal-operational`
- **Candidate temporal DB authority:** PostgreSQL 18.6 / Alembic `20260923_57`
- **Candidate temporal topology:** `145|5|88|92|285|223|408|0|0|0`
- **Temporal roadmap:** `workstreams/timeline-temporal-operational-roadmap.md`
- **Temporal live map/ledger:** `workstreams/timeline-temporal-operational-map.md`
- **Post-B06 scope/sequencing decision:** `workstreams/timeline-temporal-operational-post-b06-scope-decision-2026-09-23.md`
- **Whole-B06 closure:** `workstreams/timeline-temporal-operational-b06-e-closure-2026-09-23.md`

`protected-main baseline` and `candidate branch truth` remain deliberately separate. The candidate branch is not protected-main integration until the repository integration gate actually completes.

## 1. Current sequence

```text
Product / Domain / Logical / Physical
        CLOSED / CURRENT
              ↓
Engineering + Frontend + Backend CP1–CP6
        CLOSED / ACCEPTED
              ↓
Access/Auth + Email + Recovery + Observability + AI foundation
        CLOSED / PROTECTED-MAIN INTEGRATED
              ↓
Home / World Focus + Pre-vertical Foundation
        CLOSED / PROTECTED-MAIN INTEGRATED
              ↓
TIMELINE / TEMPORAL-OPERATIONAL `+` → TIMELINE VERTICAL
        B00 Real Data Spine                         ✅ CLOSED / PROVEN
        B01 Activity Core                           ✅ CLOSED / PROVEN
        B02 Schedule Core                           ✅ CLOSED / PROVEN
        B03 Event Core                              ✅ CLOSED / PROVEN
        B04 Temporal Constraints + Movement Policy  ✅ CLOSED / PROVEN
        B05 Product Organization                    ✅ CLOSED / PROVEN
        B06 Routine / Recurrence / Occurrence       ✅ CLOSED / PROVEN

        B08 Session Runtime                         ← NEXT
        B09 Responsibility / Participation
        B10 Actual / Outcome / Confirmation
        B11 Advanced Recurrence / Reminder
        B12 Replanning / Conflict / Solver
        B07 UI/UX Consolidation v1                  ← DEFERRED
        B15 Whole Vertical Closure
```

Former B13 Provider/Offline/Multi-device and B14 Analytics/Signals are removed from the active vertical sequence. They remain future DANTE backlog concepts outside this workstream and are not B15 blockers.

## 2. Active vertical boundary

This workstream does **not** implement all of DANTE. It completes the bounded path:

```text
Home `+`
→ create/configure canonical temporal things/facets
→ backend/PostgreSQL truth
→ Timeline representation/actions
→ required Session/Actual lifecycle
→ advanced recurrence/reminders
→ replanning/conflict/solver proposals
→ final UI/UX consolidation
```

Explicitly outside the current vertical:

```text
external provider integration (Google Calendar / Outlook / sync)
native/mobile app
advanced offline / multi-device sync
account-to-account collaboration
chat/shared editing
broad analytics/statistics/signals vertical
```

## 3. Candidate database boundary

Protected-main baseline at temporal selection:

```text
Alembic  20260906_18
Topology 89|5|18|77|173|91|272|0|0|0
```

Current candidate truth after B06 closure:

```text
Alembic      20260923_57
Tables       145
Views          5
Routines       88
Triggers       92
Indexes       285
Foreign keys  223
Checks        408
```

The candidate remains unmerged branch truth. Historical migrations are immutable; later evolution is forward-only.

## 4. Completed temporal foundation

### B00 — Real Data Spine ✅

Authenticated Web → application/API → PostgreSQL truth with real reload/empty/error behavior.

### B01 — Activity Core ✅

Canonical Activity identity, create/read, unplaced state and Planning Tray behavior.

### B02 — Schedule Core ✅

One shared Schedule engine with establish/revise/unschedule/Undo/current-history/CAS/idempotency/DST semantics.

### B03 — Event Core ✅

Event remains distinct from Activity and reuses shared Schedule authority.

### B04 — Temporal Constraints + Movement Policy ✅

Typed constraints, planned-duration semantics, hard/soft deterministic evaluation and separate governed Movement Policy/proposal behavior.

### B05 — Product Organization ✅

Life Area + secondary Tag organization and postponed/TBD rediscovery without inventing placement truth.

### B06 — Routine / Recurrence / Occurrence ✅

Routine, Recurrence and Occurrence remain distinct; canonical Occurrences reuse shared Schedule; expected/scheduled Timeline precedence and persistent reload behavior are proven.

## 5. Next — B08 Session Runtime

B08 is bounded to execution/runtime state needed by the Timeline vertical.

It must preserve:

```text
Schedule != Session
Session != Actual
planned Schedule duration != Session duration
```

No migration is pre-authorized; current Product/Domain/Logical/Physical/DB authority is inspected first.

## 6. Later active blocks

### B09 — Responsibility / Participation

Role semantics around Activity/Event/Routine/Occurrence. A participant may be a Person/referent without a DANTE Account. No collaboration/chat/shared-editing system is activated.

### B10 — Actual / Outcome / Confirmation / Resolution

Completes bounded happened-reality lifecycle. Time passage does not prove execution.

### B11 — Advanced Recurrence / Conditional / Reminder

Completes recurrence/reminder capabilities needed by `+`, editors and Timeline once required anchors exist.

### B12 — Replanning / Conflict / Solver

Deterministic-first candidate generation/optimization and governed proposals. AI may assist interpretation/explanation/ranking but is not accepted-Schedule authority.

### B07 — UI/UX Consolidation v1 — DEFERRED

Executed after B08–B12 so final `+`, editor and Timeline interaction design is consolidated once the capability vocabulary is complete.

### B15 — Whole Vertical Closure

Final whole-vertical semantic/DB/API/client/frontend/real-stack/manual/documentation reconciliation for the bounded `+`/Timeline workstream.

## 7. Stable semantic boundaries

```text
Person != Account != Principal != Actor
AuthSession != DANTE Session
Activity != Event != Routine
Routine != Recurrence != Occurrence
Occurrence != Schedule
Schedule != Temporal Constraint
Schedule != Movement Policy
Schedule != Session != Actual
Session != Actual != Outcome
Actual != Outcome != Confirmation
Responsibility != Participation
planned/intended != happened
proposal != accepted effect
evaluation != solver decision
provider identity != DANTE identity
projection != canonical truth
```

PostgreSQL remains canonical persistence authority. No generic repository/UoW/EAV/Fact/Version/relationship framework is pre-authorized.