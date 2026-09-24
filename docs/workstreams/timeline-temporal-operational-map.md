# Timeline / Temporal-Operational — Live Execution Ledger

- **Status:** CURRENT LIVE STATE — reconciled 2026-09-24
- **Branch:** `feature/timeline-temporal-operational`
- **Roadmap authority:** `docs/workstreams/timeline-temporal-operational-roadmap.md`
- **Continuation handoff:** `docs/workstreams/timeline-temporal-operational-handoff.md`
- **DB overlay:** `docs/database/timeline-temporal-operational.md`
- **Current candidate Alembic frontier:** `20260924_65`
- **Candidate topology B08-C local proof recorded:** `150|5|99|93|292|236|418|0|0|0`
- **Last proven candidate DB frontier:** B08-C / `20260924_65` / `150|5|99|93|292|236|418|0|0|0` (raw local proof logs not committed)
- **Protected-main baseline:** `20260906_18`; see `docs/database/README.md`
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
Responsibility != Participation
participant != Account identity
planned/intended != happened
proposal != accepted effect
projection != canonical truth
current accepted state != latest row
MaterialState payload != mutable runtime record
idempotency key != Domain identity
Undo != history rewind
estimated effort != scheduled duration != Session duration
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

Accepted B06 evidence remains the last fully proven frontier. B08 candidate work does not rewrite that evidence.

---

# 3. Current position

```text
B08 Session Runtime                              🟡 IN PROGRESS
  B08-A Session Core End-to-End                   ✅ CLOSED / USER-REPORTED
  B08-B Pause / Resume + Durations End-to-End     ✅ CLOSED / USER-REPORTED
  B08-C TC-009 Session Duration End-to-End        ✅ CLOSED / PROVEN — local automated gate 2026-09-24
  B08-D Whole-block closure                       🟡 USER WALKTHROUGH FAILED / FIX AWAITS LOCAL REPRO

B09 Responsibility / Participation               ⬜
B10 Actual / Outcome / Confirmation / Resolution ⬜
B11 Advanced Recurrence / Conditional / Reminder ⬜
B12 Replanning / Conflict / Solver               ⬜
B07 UI/UX Consolidation v1                       ⏸ DEFERRED
B15 Whole Vertical Closure                       ⬜
```

The user reported B08-B closed on 2026-09-24. This implies its B08-A prerequisite was accepted. Earlier local proof output was not committed to the repository; the B08-D closure record must preserve the full proof evidence.

---

# 4. B08-A repaired implementation

Target:

```text
Activity   → START Session → authoritative read/reload → END Session
Occurrence → START Session → authoritative read/reload → END Session
```

Implemented candidate chain:

```text
20260924_58
  typed Session → Activity/Occurrence subject persistence
  START / READ / END bounded capabilities

20260924_59
  DB receives requested subject family
  actual native_address.owner_family must match exactly
  Activity endpoint cannot start Occurrence and vice versa

20260924_60
  END no longer UPDATEs session_timing_absolute in place
  new immutable ended MaterialStateRef is created
  native current binding + current-history advance atomically
  end receipt records expected + resulting MaterialStateRef
  idempotent replay returns the exact produced state
  legacy candidate `_58` ended payloads are repaired forward-only
```

Application/API/client/frontend state:

```text
[x] backend Session application START/LIST/GET/END
[x] HTTP Activity START route
[x] HTTP Occurrence START route
[x] HTTP Session read/list/end routes
[x] OpenAPI/generated client path already present
[x] scheduled Timeline Activity/Occurrence Session controls
[x] unplaced Activity Planning Tray Session controls
[x] START on unplaced Activity requires no Schedule
[x] remote Session datasource focused coverage
[x] PostgreSQL Activity/Occurrence behavioral proof added
[x] wrong-family / cross-self / replay / conflict checks added
[x] immutable timing-history proof added
```

Forbidden effects remain:

```text
START does not fabricate Schedule
END does not complete Activity
END does not resolve Occurrence
END does not create Actual
END does not create Outcome
```

---

# 5. B08-A / B08-B closure evidence — USER-REPORTED

The user reported B08-B closed on 2026-09-24. That sequencing implies B08-A’s required automated and real-stack gates were accepted. The exact command output and walkthrough observations are not present in the repository; B08-D must record the consolidated evidence.

```text
B08-A: closed for sequencing by user-reported B08-B completion
B08-B: closed per user report; code frontier `_64`
B08-C: `_65` closed/proven by user-run local automated gate on 2026-09-24
```

# 6. B08-B / C / D

B08-B is closed per user report. `_62` implements Pause/Resume transitions, `_63` repairs replay, and `_64` derives elapsed/paused/active metrics from facts.

B08-C `_65` is closed/proven by the user-run local automated gate: generated/client checks, web typecheck/Vitest, backend unit/API and PostgreSQL catalog/integration proof all passed on 2026-09-24. Its freeze contract is `timeline-temporal-operational-b08-c-implementation-freeze.md`; it adds only the direct Activity soft-minimum Session active-duration subset, with read-time evaluation and no outcome or Schedule side effects.

B08-D is whole-block regression/dogfood closure after A–C. The prepared PostgreSQL test crosses unplaced Activity Session START → PAUSE → reload → RESUME → END → second START with TC-009 per Session, immutable timing history and no fabricated Schedule/Actual; it also checks an unscheduled Occurrence Session through the same transitions without inherited Activity TC-009. The prepared browser controls test checks reload while paused, exact expected timing state on commands, the pending/violated display and separate subsequent start. These tests have not yet been reported as run by the user. The real-stack walkthrough showed START succeed, then PAUSE and END fail with HTTP 422 even after the soft five-minute minimum was satisfied. The HTTP command's strict UUID validation rejected the JSON string `expected_material_state_ref` before Session execution. The candidate fix accepts valid UUID strings for this field and lets users author positive whole-minute minima without a five-minute step (for example, 1, 26 or 31). Repeat the full local gate and real-stack walkthrough; see handoff. B08-D remains open.

---

# 7. Current gate

```text
B00–B06 ✅ CLOSED / PROVEN
B07     ⏸ DEFERRED
B08     🟡 IN PROGRESS
B08-A   ✅ CLOSED / USER-REPORTED VIA B08-B
B08-B   ✅ CLOSED / USER-REPORTED
B08-C   ✅ CLOSED / PROVEN — local automated gate 2026-09-24
B08-D   🟡 REAL-STACK 422 OBSERVED — FIX AWAITS LOCAL REPRO
B09–B12 ⬜ NOT STARTED
B15     ⬜ NOT STARTED
```

**Next concrete action:** User pulls the candidate HTTP and authoring fix, runs B08-D automated regression and repeats the real-stack walkthrough; then record actual evidence and decide closure.
