# Timeline / Temporal-Operational Vertical — Implementation Roadmap

- **Status:** CURRENT EXECUTION ROADMAP — reconciled 2026-09-24
- **Branch/workstream:** `feature/timeline-temporal-operational`
- **Vertical boundary:** Home `+` creation/configuration → canonical temporal truth → Timeline projection/actions → bounded lifecycle completion
- **Completed frontier:** B06 ✅ CLOSED / PROVEN
- **Current block:** B08 Session Runtime 🟡 IN PROGRESS
- **Current slice:** B08-A Session Core End-to-End — repaired, awaiting local + real-stack proof
- **Deferred block:** B07 UI/UX Consolidation v1 — execute after B08–B12
- **Current candidate DB frontier:** PostgreSQL 18.6 / Alembic `20260924_60`
- **Candidate topology awaiting proof:** `148|5|94|93|290|230|414|0|0|0`
- **Live execution ledger:** `docs/workstreams/timeline-temporal-operational-map.md`
- **Continuation handoff:** `docs/workstreams/timeline-temporal-operational-handoff.md`

This document is the sequencing authority for the remaining Timeline / Temporal-Operational work.

---

# 0. Execution discipline

Every slice closes vertically:

```text
current Product / Domain / Logical / Physical authority
→ persistence / Alembic / Dictionary when required
→ backend / application
→ HTTP API / OpenAPI
→ generated API client
→ frontend / real product surface
→ local automated proof
→ real-stack manual proof where user behavior matters
→ documentation reconciliation
→ only then advance
```

Temporary UI is acceptable before B07, but the active capability must already be truthful, usable and testable end-to-end.

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
Responsibility != Participation
proposal != accepted effect
current accepted state != latest row
MaterialState payload != mutable runtime record
idempotency key != Domain identity
Undo != history rewind
```

Documentation stays small:

```text
ROADMAP = sequence/boundaries
MAP     = live decisions/evidence
HANDOFF = exact current position and next action
```

---

# 1. Active ordered roadmap

```text
B00 Real Data Spine                              ✅ CLOSED / PROVEN
B01 Activity Core                                ✅ CLOSED / PROVEN
B02 Schedule Core                                ✅ CLOSED / PROVEN
B03 Event Core                                   ✅ CLOSED / PROVEN
PRE-B04 DB/API GOVERNANCE                        ✅ CLOSED / FROZEN
B04 Temporal Constraints + Movement Policy       ✅ CLOSED / PROVEN
B05 Product Organization                         ✅ CLOSED / PROVEN
B06 Routine / Recurrence / Occurrence Baseline   ✅ CLOSED / PROVEN

B08 Session Runtime                              🟡 IN PROGRESS
  B08-A Session Core End-to-End                   🟡 IMPLEMENTED / AWAITING PROOF
  B08-B Pause / Resume + Durations End-to-End     ⬜ BLOCKED BY B08-A
  B08-C TC-009 Session Duration End-to-End        ⬜
  B08-D Whole-block closure                       ⬜

B09 Responsibility / Participation               ⬜
B10 Actual / Outcome / Confirmation / Resolution ⬜
B11 Advanced Recurrence / Conditional / Reminder ⬜
B12 Replanning / Conflict / Solver               ⬜
B07 UI/UX Consolidation v1                       ⏸ DEFERRED UNTIL B08–B12 EXIST
B15 Whole Vertical Closure                       ⬜
```

B07 keeps its historical identifier but executes late. External providers, native/offline/multi-device and account collaboration remain future backlog outside this bounded vertical.

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

# 3. B08 — Session Runtime

B08 activates execution episodes without collapsing planned Schedule or later happened-reality semantics.

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

Existing CP6 substrate is reused:

```text
session
session_timing_state
session_timing_absolute
session_timing_elapsed
session_timing_pause
session_timing_current_history
```

## B08-A — Session Core End-to-End — CURRENT

Required product path:

```text
Activity   → START Session → authoritative read/reload → END Session
Occurrence → START Session → authoritative read/reload → END Session
```

B08-A implementation now includes:

```text
_58 typed Session subject + bounded START/READ/END
_59 exact Activity-vs-Occurrence family enforcement
_60 immutable END MaterialState transition + exact replay receipt
backend/application boundary
HTTP API / OpenAPI / generated client
Timeline controls for scheduled Activity/Occurrence
Planning Tray controls for unplaced Activity
focused backend/database/frontend proof
```

The repaired END contract is:

```text
S1 = current open session.timing MaterialState
END(expected=S1)
→ create immutable ended S2
→ close S1 current-history
→ bind S2 current
→ receipt(expected=S1, resulting=S2)
```

Forbidden effects:

```text
START does not fabricate Schedule
END does not complete Activity
END does not resolve Occurrence
END does not create Actual
END does not create Outcome
```

### B08-A closure gate

B08-A is **not** closed merely because code is pushed. Before B08-B:

```text
1. migration/catalog/Dictionary/backend focused tests PASS locally
2. generated client + web typecheck/focused tests PASS locally
3. real-stack Activity START → reload → END works
4. unplaced Activity START works without creating Schedule
5. eligible Occurrence START → reload → END works
6. second START creates a distinct SessionRef
7. no fabricated Schedule / completion / Actual / Outcome
8. docs/map/handoff receive the proven evidence
```

Only then mark `B08-A ✅ CLOSED / PROVEN` and advance to B08-B.

## B08-B — Pause / Resume + Durations End-to-End

After B08-A closure:

```text
RUNNING → PAUSED → RUNNING → ENDED
```

Must preserve Session identity, enforce one open pause, reject invalid/concurrent transitions deterministically, rehydrate running/paused state after reload, and derive duration only from captured facts. Browser timers are presentation only.

## B08-C — TC-009 Session Duration End-to-End

Reopen TC-009 against truthful Session facts. Never alias planned Schedule duration to Session elapsed/active duration. Evaluation is not automatic mutation.

## B08-D — Whole-block closure

Whole B08 regression/dogfood closure after A–C. It adds no half-capability and cannot compensate for an unproven earlier slice.

---

# 4. B09–B12

B09 adds semantic Responsibility / Participation without making participant identity equal to a DANTE account and without introducing collaboration infrastructure.

B10 adds Actual / Outcome / Confirmation / Resolution while preserving `planned != happened`, `Session != Actual`, `Actual != Outcome`.

B11 extends recurrence/conditional/reminder behavior without RRULE-as-ontology or fake Activity materialization.

B12 is deterministic-first replanning/conflict/solver:

```text
canonical truth + constraints/preferences
→ deterministic candidate generation / optimization
→ Proposal(s)
→ optional AI interpretation/ranking assistance
→ governed acceptance
→ canonical Schedule mutation
```

`proposal != accepted Schedule`; AI is never scheduling authority.

---

# 5. B07 — UI/UX Consolidation v1 — DEFERRED

Execute after B08–B12 so final Home/Timeline/`+`/editors/actions/navigation are designed once against stable functional vocabulary. Interim UI only needs to be truthful, functional and testable.

---

# 6. Current gate

```text
B00–B06 ✅ CLOSED / PROVEN
B07     ⏸ DEFERRED
B08     🟡 IN PROGRESS
B08-A   🟡 IMPLEMENTED / AWAITING USER LOCAL + MANUAL PROOF
B08-B   ⬜ BLOCKED
B08-C-D ⬜ BLOCKED
B09–B12 ⬜ NOT STARTED
B15     ⬜ NOT STARTED
```

**Current action:** prove the repaired B08-A at Alembic `_60`; do not start B08-B first.
