# Timeline / Temporal-Operational — Live Execution Ledger

- **Status:** CURRENT LIVE STATE — reconciled 2026-09-24
- **Branch:** `feature/timeline-temporal-operational`
- **Roadmap authority:** `docs/workstreams/timeline-temporal-operational-roadmap.md`
- **Continuation handoff:** `docs/workstreams/timeline-temporal-operational-handoff.md`
- **DB overlay:** `docs/database/timeline-temporal-operational.md`
- **Current candidate Alembic frontier:** `20260924_60`
- **Candidate topology awaiting proof:** `148|5|94|93|290|230|414|0|0|0`
- **Last proven DB frontier:** B06 / `20260923_57` / `145|5|88|92|285|223|408|0|0|0`
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
  B08-A Session Core End-to-End                   🟡 IMPLEMENTED / AWAITING PROOF
  B08-B Pause / Resume + Durations End-to-End     ⬜ BLOCKED
  B08-C TC-009 Session Duration End-to-End        ⬜ BLOCKED
  B08-D Whole-block closure                       ⬜ BLOCKED

B09 Responsibility / Participation               ⬜
B10 Actual / Outcome / Confirmation / Resolution ⬜
B11 Advanced Recurrence / Conditional / Reminder ⬜
B12 Replanning / Conflict / Solver               ⬜
B07 UI/UX Consolidation v1                       ⏸ DEFERRED
B15 Whole Vertical Closure                       ⬜
```

B08-A was previously marked closed too early. Audit found two real contract gaps; both are now repaired in source, but closure waits for the user-run proof below.

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

# 5. B08-A proof gate — NOT YET ACCEPTED

User-run automated gates:

```text
[ ] Alembic upgrade reaches `20260924_60`
[ ] test_b08_a_session_catalog.py PASS
[ ] test_b08_a_session_runtime.py PASS
[ ] test_database_current_catalog.py PASS
[ ] test_current_catalog.py PASS
[ ] relevant API tests PASS
[ ] generated:check PASS
[ ] API-client typecheck PASS
[ ] web typecheck PASS
[ ] remote-session-data-source focused Vitest PASS
[ ] relevant Timeline/Planning Tray focused Vitest PASS
```

Real-stack gate:

```text
[ ] unplaced Activity: START works while Activity stays without Schedule
[ ] F5: same running Session is rehydrated
[ ] END: Session closes
[ ] second START: new SessionRef
[ ] scheduled Activity path works
[ ] eligible Occurrence START → F5 → END works
[ ] Schedule state is unchanged by Session actions
[ ] no fabricated Activity/Occurrence completion
[ ] no Actual/Outcome fabricated
```

Only after both groups pass:

```text
B08-A → ✅ CLOSED / PROVEN
B08-B → NEXT
```

---

# 6. B08-B / C / D

B08-B remains blocked until B08-A proof. When activated it owns `RUNNING → PAUSED → RUNNING → ENDED`, same Session identity, one open pause maximum, authoritative reload, deterministic transition conflicts and durations derived from facts rather than browser state.

B08-C reopens TC-009 against truthful Session duration semantics; planned Schedule duration remains separate.

B08-D is whole-block regression/dogfood closure after A–C; it cannot be used to defer missing proof from an earlier slice.

---

# 7. Current gate

```text
B00–B06 ✅ CLOSED / PROVEN
B07     ⏸ DEFERRED
B08     🟡 IN PROGRESS
B08-A   🟡 SOURCE REPAIRED / AWAITING USER PROOF
B08-B   ⬜ BLOCKED
B08-C-D ⬜ BLOCKED
B09–B12 ⬜ NOT STARTED
B15     ⬜ NOT STARTED
```

**Next concrete action:** user pulls the branch and runs the B08-A proof bundle; then execute the real-stack walkthrough and record evidence before advancing.
