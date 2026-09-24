# Timeline / Temporal-Operational — Live Execution Ledger

- **Status:** CURRENT LIVE STATE — reconciled 2026-09-24
- **Branch:** `feature/timeline-temporal-operational`
- **Roadmap authority:** `docs/workstreams/timeline-temporal-operational-roadmap.md`
- **Continuation handoff:** `docs/workstreams/timeline-temporal-operational-handoff.md`
- **DB overlay:** `docs/database/timeline-temporal-operational.md`
- **Current candidate Alembic frontier:** `20260924_65`
- **Last proven candidate DB frontier:** B08-C / `20260924_65` / `150|5|99|93|292|236|418|0|0|0`
- **Completed functional frontier:** B08 Session Runtime ✅ CLOSED / USER-REPORTED 2026-09-24
- **Current implementation cursor:** B09 Responsibility / Participation
- **CI:** not authorized; local tests are run by the user

---

# 1. Permanent semantic boundaries

```text
Person != Account != Principal != Actor
Activity != Event != Routine
Routine != Recurrence != Occurrence
Occurrence != Schedule
Schedule != Temporal Constraint != Movement Policy
Schedule != Session != Actual
Session != Actual != Outcome
Actual != Outcome != Confirmation
Expected outcome != Outcome
Responsibility != Participation
participant != responsible actor != organizer/owner
participant != Account identity
shared Event truth != actor-specific participation truth
planned/intended != happened
Step != Activity
Plan != Activity
Dependency != hierarchy
ordering != dependency
child Schedule != parent Schedule
child Session != parent Session
proposal != accepted effect
projection != canonical truth
current accepted state != latest row
MaterialState payload != mutable runtime record
idempotency key != Domain identity
Undo != history rewind
estimated effort != scheduled duration != Session duration
editable Create intent != canonical persistence
```

---

# 2. Closed frontier

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
  B08-C TC-009 Session Duration End-to-End        ✅ CLOSED / PROVEN — local automated gate
  B08-D Whole-block closure                       ✅ CLOSED / USER-REPORTED — automated gate and dogfood
```

B08 is the completed functional frontier. B08-C `_65` remains the latest candidate DB/catalog proof explicitly recorded in this ledger; that distinction must not be blurred.

---

# 3. Remaining execution order

```text
B09 Responsibility / Participation               ⬜ NEXT
B10 Actual / Outcome / Confirmation / Resolution ⬜
B11 Advanced Recurrence / Conditional / Reminder ⬜
B13 Work Structure / Decomposition / Dependencies⬜
B12 Replanning / Conflict / Solver               ⬜
B14 Temporal Create Completeness Gate             ⬜
B07 UI/UX Consolidation v1                       ⏸ DEFERRED UNTIL B14
B15 Whole Vertical Closure                       ⬜
```

Sequence authority:

```text
B09 → B10 → B11 → B13 → B12 → B14 → B07 → B15
```

B13 and B14 are the only new compact blocks added by the post-B08 Create audit. Existing gaps are assigned to B09–B12 rather than exploded into additional micro-blocks.

---

# 4. B08 closure record

Target path proven/accepted for B08:

```text
Activity   → START Session → authoritative read/reload → PAUSE/RESUME → END
Occurrence → START Session → authoritative read/reload → PAUSE/RESUME → END
```

Implemented migration chain:

```text
20260924_58 typed Session subject + START/READ/END
20260924_59 exact Activity/Occurrence subject-family enforcement
20260924_60 immutable END MaterialState + exact replay receipt
20260924_62 pause/resume persistence
20260924_63 transition replay repair
20260924_64 runtime metrics
20260924_65 Activity-owned soft minimum on Session active duration
```

Application/API/client/frontend state:

```text
[x] backend Session START/LIST/GET/END
[x] Activity and Occurrence subject routes
[x] exact subject-family enforcement at DB boundary
[x] immutable END timing history
[x] pause/resume on same Session identity
[x] elapsed/paused/active duration from canonical facts
[x] Timeline Session controls for scheduled Activity/Occurrence
[x] Planning Tray Session controls for unplaced Activity
[x] START on unplaced Activity requires no Schedule
[x] B08-C direct Activity TC-009 soft-minimum evaluation
[x] whole-minute Schedule duration controls after dogfood repair
[x] timed splittable Activity keeps accepted placement
[x] genuinely unplaced Activity remains in Da collocare
```

Permanent forbidden effects:

```text
START does not fabricate Schedule
END does not complete Activity
END does not resolve Occurrence
END does not create Actual
END does not create Outcome
pause does not create a new Session
TC-009 does not aggregate separate Sessions
TC-009 excludes pauses
TC-009 does not block transition or mutate Schedule/Actual/Outcome
```

B08-D evidence recorded from the user's local run on 2026-09-24:

```text
generated/client checks PASS
focused Web suite: 58 PASS
backend PostgreSQL/unit/API command: 31 PASS
follow-up Web typecheck: user-confirmed PASS
real app: START / PAUSE / RESUME / END confirmed
real app: timed/unplaced placement semantics confirmed
```

Raw local test logs are not committed; do not upgrade those user-reported items to repository-captured evidence retroactively.

---

# 5. B09 live contract — Responsibility / Participation

B09 starts from existing Product/Domain/Logical/Physical authority; no new universal collaboration ontology is allowed.

Capabilities to prove before B09 receives `[x]`:

```text
[ ] identify exact existing Responsibility / Participation owners and relations
[ ] preserve Person != Account and participant != account identity
[ ] preserve Responsibility != Participation
[ ] preserve shared Event truth != actor-specific participation truth
[ ] model the smallest useful Activity/Event temporal subset without generic JSON/polymorphic shortcuts
[ ] make Home `+` required/optional participant fields truthful where B09 owns them, or remove/defer them
[ ] keep another person's state outside DANTE authority unless explicitly represented/authorized
[ ] align migration → SQLAlchemy → Dictionary/scope → API/OpenAPI/client → frontend where applicable
[ ] user-run local automated proof
[ ] map/roadmap/handoff closure evidence
```

B09 must not infer Event Actual, attendance truth or completion merely from invitation/participation state.

---

# 6. Reserved contracts for B10–B14

These are scope anchors, not implementation checkmarks.

## B10 — Actual / Outcome / Confirmation / Resolution

```text
[ ] Actual/Outcome/Confirmation/Resolution semantics
[ ] confirmation policy behind Home `+`
[ ] partial completion / finish-early realization semantics
[ ] Expected outcome != Outcome
[ ] Session END != completion/Actual
```

## B11 — Advanced Recurrence / Conditional / Reminder

```text
[ ] advanced recurrence/conditional behavior
[ ] resolve Home `+` reminder field through canonical support, truthful handoff or hiding
[ ] no universal fake Reminder owner merely to satisfy UI
```

## B13 — Work Structure / Decomposition / Dependencies

```text
[ ] internal Step != Activity
[ ] composite work uses real independent Activities where they have independent lifecycle
[ ] typed Dependency != hierarchy / ordering
[ ] max Session count / merge / spacing / preparation-recovery structure policy where temporal
[ ] no generic SubActivity/GenericItem ontology
```

## B12 — Replanning / Conflict / Solver

```text
[ ] preferred-window semantics
[ ] movement policy semantics
[ ] fallback policy semantics
[ ] dependency-aware replanning using B13
[ ] Proposal != accepted Schedule
[ ] solver UNKNOWN != INFEASIBLE
```

## B14 — Temporal Create Completeness Gate

Every editable Create field must be one of:

```text
[ ] canonically persisted + behaviorally proven
[ ] truthful handoff to owning vertical/capability
[ ] explicitly presentation/read-only
[ ] hidden/removed until supported
```

The gate audits at least Notes, appearance override, Tags, confirmation/reminder, execution structure, Event location/availability/visibility, purpose/expected outcome/decision requirement, participants, resources/pre-read and conference/provider fields.

Forbidden:

```text
editable UI → collected value → silently ignored or routinely rejected because capability is absent
```

---

# 7. Current gate

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

**Next concrete action:** Begin B09 Responsibility / Participation from the B08-closed frontier.
