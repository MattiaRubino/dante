# Timeline / Temporal-Operational — Live Execution Ledger

- **Status:** CURRENT LIVE STATE — reconciled 2026-09-25
- **Branch:** `feature/timeline-temporal-operational`
- **Roadmap authority:** `docs/workstreams/timeline-temporal-operational-roadmap.md`
- **Continuation handoff:** `docs/workstreams/timeline-temporal-operational-handoff.md`
- **DB overlay:** `docs/database/timeline-temporal-operational.md`
- **Current / last proven candidate Alembic frontier:** `20260925_74`
- **Current / last proven candidate DB topology:** `159|5|115|93|305|258|435`
- **Completed functional frontier:** B10-A Actual / realization core ✅ CLOSED / PROVEN 2026-09-25
- **Current implementation cursor:** B10-B Outcome — gate approval pending
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
  B08-C TC-009 Session Duration End-to-End        ✅ CLOSED / PROVEN
  B08-D Whole-block closure                       ✅ CLOSED / USER-REPORTED
B09 Responsibility / Participation               ✅ CLOSED / USER-REPORTED 2026-09-25
  B09-A typed persistence substrate               ✅ CLOSED / PROVEN 2026-09-25
  B09-B guarded mutation + application surface    ✅ CLOSED / PROVEN 2026-09-25
  B09-C non-Account Person referents              ✅ CLOSED / PROVEN 2026-09-25
  B09-D B09 whole-block closure                   ✅ CLOSED / USER-REPORTED 2026-09-25
B10-A Actual / realization core                  ✅ CLOSED / PROVEN 2026-09-25
```

B10-A closure evidence: `timeline-temporal-operational-b10-a-closure-2026-09-25.md`.

---

# 3. Remaining execution order

```text
B10 Actual / Outcome / Confirmation / Resolution 🟨 IN PROGRESS
  B10-A Actual / realization core                 ✅ CLOSED / PROVEN
  B10-B Outcome                                   ⬜ NEXT — gate approval pending
  B10-C Confirmation                              ⬜
  B10-D Reconciliation / resolution workflow      ⬜
  B10-E Final integration + acceptance            ⬜ — manual real-app proof here
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

Within B10:

```text
B10-A Actual
→ B10-B Outcome
→ B10-C Confirmation
→ B10-D reconciliation workflow
→ B10-E final integration + user real-app proof
```

A/B/C/D are each implemented as one coherent block. The user runs one local automated gate only after the whole major block is ready. No CI/GitHub Actions. No manual real-app proof until B10-E.

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

---

# 5. B09 closure record — Responsibility / Participation

B09 adds the smallest coherent actor/person layer needed by the temporal vertical, without introducing account collaboration infrastructure.

## B09-A — typed persistence substrate — CLOSED / PROVEN

Implemented by Alembic `20260925_66`:

```text
event_expected_participation(Event, Person, required|optional)
activity_responsibility(Activity, Person)
event_responsibility(Event, Person)
```

Local user-run proof on 2026-09-25: 10 focused PostgreSQL tests passed.

## B09-B — CLOSED / PROVEN

B09-B owns guarded mutation/application behavior over the B09-A substrate. It preserves Person != Account, Responsibility != Participation and expected Participation != Actual attendance. Home `+` free-text participant fields remain B14.

User-run local automated proof on 2026-09-25: web 4 passed; backend B09-B/B09-A/catalog/OpenAPI 18 passed.

## B09-C — CLOSED / PROVEN

B09-C closed at `20260925_69`: guarded creation/list/local label correction for owner-local native Persons without Accounts. User-run proof passed generated/client checks, both typechecks, 7 web tests, 11 backend OpenAPI/API tests and 18 PostgreSQL B09-C/B09-B/catalog regressions. Proven topology `158|5|109|93|303|254|433`; generated client commit `875aaf48`.

## B09-D — CLOSED / USER-REPORTED

B09-D integrated proof covers Person creation and correction, Responsibility, expected Event Participation, removal, isolation and absence of Actual/Session. User real-app walkthrough passed on 2026-09-25. Evidence: `timeline-temporal-operational-b09-d-closure-2026-09-25.md`.

Permanent B09 boundaries:

```text
Person != Account
Responsibility != Participation
expected Participation != Actual Participation
participation/attendance != Event Actual
owner-local Person label != universal identity
provider attendee != canonical Person identity by default
```

---

# 6. B10 live contract — Actual / Outcome / Confirmation / Resolution

Scope authority: `docs/workstreams/timeline-temporal-operational-b10-scope-freeze.md`.

## B10-A — Actual / realization core — CLOSED / PROVEN

Final database chain:

```text
20260925_70 guarded self-scoped Actual realization authoring/current/history
20260925_71 exact Activity/Event/Occurrence family hardening
20260925_72 CP6 Actual/scoped-address owner creation order repair
20260925_73 canonical family-aware write/read signatures
20260925_74 current-history qualification + canonical receipt FK name
```

Proven capability:

```text
Activity    → explicit Actual current realization
Event       → explicit Actual current realization
Occurrence  → explicit Actual current realization

Actual owner                = stable scoped owner for subject_native_ref
Actual realization state    = append-only MaterialState
current accepted state      = explicit scoped current binding/history
optional timing             = instant | start_only | interval
optional Session evidence   = exact Session + exact Session timing MaterialState
```

Closure evidence:

```text
[x] PostgreSQL guarded capability over canonical CP6 Actual substrate
[x] exact subject-family enforcement
[x] public-write idempotency receipts
[x] append-only state/current-history behavior
[x] backend application current/history surface
[x] Activity/Event/Occurrence POST+GET Actual routes
[x] Actual history route
[x] OpenAPI inventory for all seven operations
[x] Timeline minimal Actual authoring for Activity/Event/Occurrence
[x] absence rendered as unknown, not false/non-realization
[x] generated OpenAPI/Orval committed at 780c612d
[x] final user-run PostgreSQL/application/catalog gate: 14 passed / exit 0
```

Proven frontier:

```text
Alembic  20260925_74
Topology 159|5|115|93|305|258|435
```

Permanent B10-A boundaries:

```text
Session END != Actual
Session evidence != Actual identity
absence of Actual = unknown
absence of Actual != realization_occurred=false
Actual != Outcome != Confirmation
current accepted state != latest row
idempotency key != Actual identity
provider/AI/solver != canonical realization authority
```

No manual real-app proof was performed for B10-A; by explicit execution policy it belongs to B10-E.

## B10-B — Outcome — NEXT

B10-B has not started. Its gate must first freeze only the planned modification surface. The implementation must derive the Outcome model from existing Product/Domain/Logical/Physical authority before adding schema.

Required boundaries entering the gate:

```text
Actual != Outcome
Expected outcome != Outcome
Outcome != Confirmation
absence of Outcome != success/failure
Session END != Outcome
```

Result vocabulary such as completed/partial/skipped/not-completed/postponed/replaced/cancelled and any finish-early interaction belongs to B10-B only if the repository authority supports that exact representation. Do not invent generic status semantics merely from UI labels.

Later B10:

```text
B10-C Confirmation
B10-D reconciliation / resolution workflow
B10-E final integration + automated regression + single real-app B10 walkthrough
```

---

# 7. Later blocks

## B11 — Advanced Recurrence / Conditional / Reminder

```text
[ ] advanced recurrence/conditional behavior
[ ] resolve Home + reminder field through canonical support, truthful handoff or hiding
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

Every editable Create field must be canonically persisted/proven, truthfully handed off, presentation-only, or hidden until supported.

---

# 8. Current gate

```text
B00–B06 ✅ CLOSED / PROVEN
B08     ✅ CLOSED / USER-REPORTED 2026-09-24
B09     ✅ CLOSED / USER-REPORTED 2026-09-25
B10     🟨 IN PROGRESS
  B10-A ✅ CLOSED / PROVEN 2026-09-25
  B10-B ⬜ NEXT — gate approval pending
  B10-C ⬜
  B10-D ⬜
  B10-E ⬜ — user real-app proof here
B11     ⬜ NOT STARTED
B13     ⬜ NOT STARTED
B12     ⬜ NOT STARTED
B14     ⬜ NOT STARTED
B07     ⏸ DEFERRED UNTIL B14
B15     ⬜ NOT STARTED
```

**Next concrete action:** review and approve the B10-B Outcome change/file gate. After approval, B10-B is implemented completely before the user runs its single local automated test command.