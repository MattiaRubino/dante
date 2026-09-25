# Timeline / Temporal-Operational — Live Execution Ledger

- **Status:** CURRENT LIVE STATE — reconciled 2026-09-25
- **Branch:** `feature/timeline-temporal-operational`
- **Roadmap authority:** `docs/workstreams/timeline-temporal-operational-roadmap.md`
- **Continuation handoff:** `docs/workstreams/timeline-temporal-operational-handoff.md`
- **DB overlay:** `docs/database/timeline-temporal-operational.md`
- **Current candidate Alembic frontier:** `20260925_71`
- **Last proven candidate DB frontier:** B09-C / `20260925_69` / `158|5|109|93|303|254|433`
- **Completed functional frontier:** B09 Responsibility / Participation ✅ CLOSED / USER-REPORTED 2026-09-25
- **Current implementation cursor:** B10-A Actual / realization core — candidate prepared; generated client + user-run local gate pending
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
B09 Responsibility / Participation               ✅ CLOSED / USER-REPORTED 2026-09-25
  B09-A typed persistence substrate               ✅ CLOSED / PROVEN 2026-09-25
  B09-B guarded mutation + application surface    ✅ CLOSED / PROVEN 2026-09-25
  B09-C non-Account Person referents              ✅ CLOSED / PROVEN 2026-09-25
  B09-D B09 whole-block closure                   ✅ CLOSED / USER-REPORTED 2026-09-25
```

B10-A is not part of the closed frontier until the user-run local acceptance gate passes.

---

# 3. Remaining execution order

```text
B10 Actual / Outcome / Confirmation / Resolution 🟨 IN PROGRESS
  B10-A Actual / realization core                 🟨 CANDIDATE PREPARED — local gate pending
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

B13 and B14 are compact blocks added by the post-B08 Create audit. Existing gaps stay assigned to B09–B12 rather than being exploded into micro-verticals.

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

Raw local test logs are not committed; do not upgrade user-reported items to repository-captured evidence retroactively.

---

# 5. B09 closure record — Responsibility / Participation

B09 adds the smallest coherent actor/person layer needed by the temporal vertical, without introducing account collaboration infrastructure.

## B09-A — typed persistence substrate — CLOSED / PROVEN

Implemented by Alembic `20260925_66`:

```text
event_expected_participation
  Event → Person
  requirement_code ∈ {required, optional}

activity_responsibility
  Activity → responsible Person

event_responsibility
  Event → responsible Person
```

B09-A proves:

```text
[x] Person-backed relations work without Account identity
[x] Responsibility and Participation are separate typed relations
[x] required/optional expected Event participation is bounded explicitly
[x] Activity Responsibility and Event Responsibility remain separate typed owners
[x] invalid participation requirement values are rejected by PostgreSQL
[x] one current simple responsible Person per Activity/Event in this B09-A subset
[x] runtime has no raw SELECT/INSERT/UPDATE/DELETE privilege on the new relation tables
[x] Alembic ↔ SQLAlchemy ↔ Dictionary/scope ↔ catalog remain reconciled
[x] local PostgreSQL gate supplied by user: 10 passed on 2026-09-25
```

Proven B09-A candidate frontier:

```text
Alembic  20260925_66
Topology 153|5|99|93|298|242|419
```

B09-A deliberately does **not** implement:

```text
invitation workflow / response history
accepted / declined / tentative semantics
Actual Participation / attendance
attendance intervals
Responsibility transfer / claim / hand-off workflow
public API authoring
Home + / Timeline authoring UI
provider attendee identity or calendar control
```

Those omissions are intentional semantic boundaries, not failed B09-A requirements.

## B09-B — CLOSED / PROVEN

B09-B owns guarded mutation/application behavior over the B09-A substrate. It does not expose the new tables as direct runtime mutation surfaces.

Implemented on `20260925_67`/`_68`:

```text
[x] bounded guarded operations for current Responsibility and expected Event Participation
[x] exact authorization/self-context rules without Person=Account collapse
[x] idempotency/replay behavior where mutation is public/consequential
[x] backend/application service
[x] HTTP/OpenAPI/generated client
[x] Timeline detail authoring for self Responsibility / self expected Participation
[x] negative automated proof: expected Participation does not establish Actual attendance
[x] user-run local automated proof 2026-09-25: web 4 passed; backend 18 passed
```

Home `+` required/optional participant textareas remain B14. They are free-text emails, not Person refs. B09-B does not invent email-to-Person identity.

## B09-C — CLOSED / PROVEN

B09-C closed and proven at `20260925_69`: guarded creation, list and label correction for owner-local native Persons without Accounts. The admissibility seam accepts self or a Person in this owner's catalog. Timeline role controls select that Person explicitly; expected participation remains an intention only. Dictionary and mappings cover two default-deny tables, three capabilities and the widened helper. User-run proof on 2026-09-25: generated:check PASS (321 files), both typechecks PASS, web 7 passed, backend OpenAPI/API 11 passed, PostgreSQL B09-C/B09-B/catalog regressions 18 passed; physical topology `158|5|109|93|303|254|433` proven. Generated client commit `875aaf48`.

## B09-D — CLOSED / USER-REPORTED

B09-D integrated proof covers Person creation and label correction, both Responsibility owners, expected Event Participation, removal, isolation and no Actual/Session. The user's local run passed: web typecheck, 8 focused web tests, and 18 focused PostgreSQL tests. The user reported the real-app walkthrough working on 2026-09-25; the closure evidence lives in `timeline-temporal-operational-b09-d-closure-2026-09-25.md`.

Permanent B09 boundaries:

```text
Person != Account
Responsibility != Participation
participant != responsible actor != organizer/owner
shared Event truth != actor-specific participation truth
expected/response Participation != Actual Participation
participation/attendance != Event Actual
another person's participation != DANTE authority over that person's calendar/task system
provider attendee != canonical Person identity by default
```

---

# 6. B10 live contract — Actual / Outcome / Confirmation / Resolution

Scope authority for the active slice: `docs/workstreams/timeline-temporal-operational-b10-scope-freeze.md`.

## B10-A — Actual / realization core — CANDIDATE PREPARED

Candidate database chain:

```text
20260925_70 guarded self-scoped Actual realization authoring/current/history
20260925_71 exact Activity/Event/Occurrence family hardening at PostgreSQL boundary
```

Candidate capability:

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

Implemented candidate evidence now in the branch:

```text
[x] PostgreSQL guarded capability over canonical CP6 Actual substrate
[x] exact subject-family enforcement at PostgreSQL boundary
[x] public-write idempotency receipts
[x] append-only state/current-history behavior
[x] backend application current/history surface
[x] Activity/Event/Occurrence POST+GET Actual routes
[x] Actual history route
[x] OpenAPI inventory frozen for all seven operations
[x] Timeline minimal Actual authoring for Activity/Event/Occurrence
[x] absence rendered as unknown, not false/non-realization
[x] focused PostgreSQL/application test committed
[x] focused Event public API test committed
[x] focused web Actual test committed
[ ] generated OpenAPI/Orval client regenerated locally through repository generator
[ ] user-run local automated acceptance gate
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

The assistant does not run this gate. The user runs it locally; CI/GitHub Actions remain unauthorized. A passing gate is required before B10-A enters the closed frontier.

Later B10 work remains deliberately unimplemented here:

```text
[ ] Outcome semantics
[ ] Confirmation semantics
[ ] canonical partial/completed/skipped/not-completed/postponed/replaced/cancelled result vocabulary
[ ] finish-early behavior
[ ] confirmation policy behind Home +
[ ] integrated reconciliation/resolution behavior
```

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

Every editable Create field must be one of:

```text
[ ] canonically persisted + behaviorally proven
[ ] truthful handoff to owning vertical/capability
[ ] explicitly presentation/read-only
[ ] hidden/removed until supported
```

Forbidden:

```text
editable UI → collected value → silently ignored or routinely rejected because capability is absent
```

---

# 7. Current gate

```text
B00–B06 ✅ CLOSED / PROVEN
B08     ✅ CLOSED / USER-REPORTED 2026-09-24
B09     ✅ CLOSED / USER-REPORTED 2026-09-25
  B09-A ✅ CLOSED / PROVEN 2026-09-25
  B09-B ✅ CLOSED / PROVEN 2026-09-25
  B09-C ✅ CLOSED / PROVEN 2026-09-25
  B09-D ✅ CLOSED / USER-REPORTED 2026-09-25
B10     🟨 IN PROGRESS
  B10-A 🟨 CANDIDATE PREPARED — generated client + user local gate pending
B11     ⬜ NOT STARTED
B13     ⬜ NOT STARTED
B12     ⬜ NOT STARTED
B14     ⬜ NOT STARTED
B07     ⏸ DEFERRED UNTIL B14
B15     ⬜ NOT STARTED
```

**Next concrete action:** user runs the B10-A local acceptance command. It regenerates OpenAPI/Orval through `pnpm api:generate`, then validates generated/client, backend PostgreSQL/API/OpenAPI and focused web regressions. Only after the user reports a passing gate does B10-A close.
