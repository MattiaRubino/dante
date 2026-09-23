# Timeline / Temporal-Operational — Live Execution Ledger

- **Status:** CURRENT LIVE STATE — reconciled 2026-09-23
- **Branch:** `feature/timeline-temporal-operational`
- **Roadmap authority:** `docs/workstreams/timeline-temporal-operational-roadmap.md`
- **Continuation handoff:** `docs/workstreams/timeline-temporal-operational-handoff.md`
- **DB overlay:** `docs/database/timeline-temporal-operational.md`
- **Current Alembic frontier:** `20260923_57`
- **Current proven topology:** `145|5|88|92|285|223|408|0|0|0`
- **CI:** not authorized; local tests are run by the user

This is the **single live work ledger**. It records only current progress, accepted decisions, implementation notes and proof evidence. Do not create a new planning/freeze document for every sub-slice.

---

# 1. Permanent semantic boundaries

```text
Person != Account != Principal != Actor
Goal != Plan != Activity
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
pending != success
projection != canonical truth
current accepted state != latest row
idempotency key != Domain identity
Undo != history rewind
estimated effort != scheduled duration != Session duration
planned Schedule duration != Actual duration
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

B06 final state:

```text
B06-A Routine source core                        ✅ at `_51`
B06-B Recurrence authoring                       ✅ at `_54`
B06-C canonical Occurrence checkpoint            ✅ at `_55`
B06-D shared Schedule / Timeline / functional UI ✅ at `_57`
B06-E whole-block closure                        ✅ at `_57`
```

Accepted B06 evidence:

```text
generated:check                             PASS
API-client typecheck                        PASS
web typecheck                               PASS
focused B06/runtime Vitest                  6 files / 37 tests PASS
persistent local dogfood real-stack        accepted
created Timeline/Event/recurring state      survives F5
remaining B06 blocker                       none
```

B04 deferred families carried forward:

```text
TC-009 contiguous Session duration  → B08-E
TC-010 spacing/recovery             → later anchor-specific reopening
TC-011 relative before/after        → future bounded relation/reference review
```

---

# 3. Current position

```text
B08 Session Runtime                              🟡 READY TO START
  B08-A Authority reconciliation + freeze         DECISIONS RECORDED / LOCAL PROOF PENDING
  B08-B Start / Read / End core                   ⬜
  B08-C Pause / Resume + duration                 ⬜
  B08-D Timeline runtime integration              ⬜
  B08-E TC-009 Session-duration reopening         ⬜
  B08-F Whole-block closure                       ⬜

B09 Responsibility / Participation               ⬜
B10 Actual / Outcome / Confirmation / Resolution ⬜
B11 Advanced Recurrence / Conditional / Reminder ⬜
B12 Replanning / Conflict / Solver               ⬜
B07 UI/UX Consolidation v1                       ⏸ DEFERRED
B15 Whole Vertical Closure                       ⬜
```

No B08 runtime slice has been started. B08-A decisions are recorded below and stay open until local proof is recorded in this ledger.

---

# 4. B08 semantic boundary

B08 activates actual execution episodes only where required by the Timeline vertical.

```text
Activity != Session
Occurrence != Session
Schedule != Session
Session != Actual
Session != Outcome
Session end != Activity completion
Session end != Occurrence completion
planned Schedule duration != Session elapsed duration
Session elapsed duration != Session active duration
```

Existing CP6 Session substrate to inspect before authorizing new DDL:

```text
session
session_timing_state
session_timing_absolute
session_timing_elapsed
session_timing_pause
session_timing_current_history
```

Candidate execution targets to verify in B08-A rather than assume:

```text
Activity     ✅ candidate
Occurrence   ✅ candidate
Routine      ❌ direct target
Event        ❌ ordinary baseline target
Schedule     ❌ owner/target
```

---

# 5. B08-A — Authority reconciliation + freeze

**Status:** DECISIONS RECORDED / LOCAL PROOF PENDING

Inspection used `docs/domain/concepts/session.md`, Logical Time/Reality Session disposition, CP6-M03 Session materialization, Dictionary `session` plus `session_timing_*`, SQLAlchemy `identity.SessionRow` and `mappings/session.py`, and the current Temporal OpenAPI inventory. No separate B08-A document is added.

B08-A adds no migration, API route, generated client, or frontend behavior. Alembic stays `20260923_57`.

## Accepted B08-A decisions

### Eligible execution targets

```text
Activity      baseline Session subject     yes
Occurrence    baseline Session subject     yes
Routine       direct Session subject       no
Event         ordinary baseline subject    no
Schedule      Session owner or subject     no
```

Authority: Session is an execution episode of Activity or Occurrence (`docs/domain/concepts/session.md` core model; Logical slice Time/Reality §7). A Routine stays the policy; execution belongs to an Occurrence. An ordinary Event stays Schedule → Actual, and does not receive a Session merely because it occupies time. Schedule remains planned placement.

Spontaneous Session without a prior Activity remains Domain-true and is not a B08 baseline command. B08 must not invent an Activity to host one.

One Activity or Occurrence may have many Sessions. Ending a Session does not complete either subject.

### Representation

```text
identity     dante.session.session_ref          existing NativeRef shell
timing       session.timing MaterialState      existing
subject edge Session → Activity | Occurrence   ABSENT — the only DDL gap
```

`dante.session` stays an identity shell with only `session_ref`. Do not add a subject column to that shell. Do not store the subject on Schedule. Do not use a `(kind, id)` pair.

B08-B may add one typed association only:

```text
session_ref          → dante.session
subject_native_ref   → native_address
owner_family         activity | occurrence
cardinality          exactly one subject per Session
```

The family check uses `native_address.owner_family`, the same discriminator Schedule already uses for Activity, Event, and Occurrence.

### Lifecycle

The Domain defers a lifecycle enum. B08 does not add one. Open, paused, and ended are the existing timing rows.

```text
START    new session_ref
         + current absolute session.timing
         + started_at set, ended_at NULL
PAUSE    one session_timing_pause with resumed_at NULL
         Session identity stays open
RESUME   set resumed_at on that open pause
         same Session, same timing state
END      set ended_at on the current absolute timing
         later START is a new session_ref
```

`elapsed_only` stays the existing manual retrospective form. Pause rows reference absolute timing, so the timer path does not write `elapsed_only`. A pause duration never splits a Session. END does not write Actual, Outcome, Activity completion, Occurrence completion, or a Schedule change.

Illegal transitions, already enforced or required of B08-B:

```text
two open pauses on one timing state          reject
pause or resume on elapsed_only              reject
pause or resume after ended_at is set        reject
resume without an open pause                 reject
second END                                   reject
```

### Current history, concurrency, CAS

Current timing is `session_timing_current_history`, one open row per `session_ref` (`ux_session_timing_current_history_open`). Corrections are later MaterialStates. B08-B does not implement split/merge.

Overlap of two Sessions is not a database prohibition (`docs/domain/concepts/session.md`). B08 does not add “one open Session per subject”.

B08-B mutations use the existing temporal pattern: self-scope, expected current timing state, operation id distinct from `session_ref`, and an immutable receipt. B08-A adds no receipt table.

### API inventory — not published in B08-A

Later slices publish these operationIds and no others for the baseline timer:

```text
temporal_start_activity_session
temporal_start_occurrence_session
temporal_list_activity_sessions
temporal_list_occurrence_sessions
temporal_get_session
temporal_pause_session
temporal_resume_session
temporal_end_session
```

Subject reads return every Session for that subject, including more than one open Session. They do not invent a single current Session.

### TC-009 and non-goals

TC-009 minimum contiguous Session duration stays B08-E. It is not planned Schedule duration. TC-010 and TC-011 stay deferred.

Out of B08-A, and out of the baseline timer unless a later slice owns them: Actual, Outcome, Confirmation, completion, Schedule mutation, Event Sessions, Routine as subject, spontaneous Session commands, provider import, split/merge, a status enum, pause-threshold splitting, solver, reminders, B07 visual consolidation, and CI.

### Proof owned by B08-A

```text
dictionary + SQLAlchemy + OpenAPI freeze lock
live PostgreSQL: revision _57, six Session tables,
  identity shell unchanged, absolute|elapsed_only,
  open-pause and open-history uniqueness,
  no subject edge, no start/pause/resume/end capability
```

B08-B owns behavioral proof of START/END. B08-C owns pause/resume duration. B08-F owns the real-stack walkthrough.

## B08-A evidence

_Local proof has not been executed in this session. B08-A is not CLOSED / FROZEN until that proof is recorded here._

---

# 6. Later B08 slices

These are deliberately not expanded into separate planning documents. The roadmap defines their scope; when each becomes active, its decisions and evidence are added here.

```text
B08-B  Start / Read / End core
B08-C  Pause / Resume + truthful duration
B08-D  Timeline runtime integration
B08-E  TC-009 Session-duration reopening
B08-F  Whole-block automated + real-stack closure
```

B08-F manual target:

```text
START
→ F5 still running
→ PAUSE
→ F5 still paused
→ RESUME
→ END
→ second START = new SessionRef
→ eligible Occurrence path works
→ Schedule unchanged
→ no fabricated completion / Actual / Outcome
→ no duplicate runtime state after reload/navigation
```

Only after this may B08 become `CLOSED / PROVEN`.

---

# 7. Documentation / chat-saturation rule

At a meaningful checkpoint:

```text
1. update this ledger with accepted decisions/evidence
2. update handoff with exact next action
3. update roadmap only if sequencing or scope changed
4. update DB overlay/dictionary in the same change when persistence changes
5. push code/docs frequently
```

Fresh-chat recovery order:

```text
1. timeline-temporal-operational-handoff.md
2. timeline-temporal-operational-roadmap.md
3. timeline-temporal-operational-map.md
4. docs/database/timeline-temporal-operational.md only if the active slice touches DB work
```

A whole-block closure document may be created when B08 closes; intermediate sub-slices stay in this live ledger.

---

# 8. Current gate

```text
B00–B06 ✅ CLOSED / PROVEN
B07     ⏸ DEFERRED
B08     🟡 READY TO START
B08-A   DECISIONS RECORDED / LOCAL PROOF PENDING
B09–B12 ⬜ NOT STARTED
B15     ⬜ NOT STARTED
```

**Next concrete action:** run the B08-A local proof. Do not start B08-B and do not mark B08-A `CLOSED / FROZEN` until that proof is recorded in this ledger.