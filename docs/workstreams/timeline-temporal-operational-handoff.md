# Timeline / Temporal-Operational — Workstream Handoff

- **Status:** B08 SESSION RUNTIME ✅ CLOSED — B09 Responsibility / Participation is next
- **Reconciled:** 2026-09-24
- **Branch:** `feature/timeline-temporal-operational`
- **Roadmap authority:** `docs/workstreams/timeline-temporal-operational-roadmap.md`
- **Live execution ledger:** `docs/workstreams/timeline-temporal-operational-map.md`
- **DB overlay:** `docs/database/timeline-temporal-operational.md`
- **Current candidate Alembic frontier:** `20260924_65`
- **Last proven candidate DB frontier:** B08-C / `20260924_65` / `150|5|99|93|292|236|418|0|0|0`
- **CI:** no CI/GitHub Actions unless explicitly authorized; user runs local tests

Read this first after a context reset.

---

# 1. Exact current position

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

Execution order after B08 is deliberately:

```text
B09 → B10 → B11 → B13 → B12 → B14 → B07 → B15
```

Historical identifiers are not renumbered. B13 and B14 are the only new compact blocks introduced by the post-B08 Create audit; all other missing Create behavior belongs to existing B09–B12 ownership.

---

# 2. B08 closure truth

B08 closed from the user's local automated output and real-app walkthrough on 2026-09-24.

Migration chain:

```text
_58 typed Session subject + START/READ/END
_59 exact Activity/Occurrence subject-family enforcement
_60 immutable END MaterialState + exact replay receipt
_62 pause/resume
_63 transition replay repair
_64 runtime metrics
_65 Activity TC-009 soft minimum on one Session active duration
```

Recorded evidence:

```text
generated/client checks PASS
focused Web suite: 58 PASS
backend PostgreSQL/unit/API command: 31 PASS
follow-up Web typecheck: user-confirmed PASS
real app: START / PAUSE / RESUME / END confirmed
real app: timed splittable Activity remains timed and scheduled
real app: genuinely unplaced Activity remains in Da collocare
real app: whole-minute Schedule duration accepted without 26/31 step bug
```

Raw local output is not committed; retain the distinction between user-reported proof and repository-captured evidence.

Permanent B08 boundaries:

```text
START does not create fake Schedule
END does not complete Activity
END does not resolve Occurrence
END does not create Actual or Outcome
pause does not create a new Session
Session elapsed != active duration
TC-009 does not aggregate Sessions, count pauses, block transitions or mutate Schedule/Actual/Outcome
```

---

# 3. Roadmap amendment after Create audit

The Home `+` audit found two structural omissions, not a reason to create many extra phases.

## B13 — Work Structure / Decomposition / Dependencies

Needed for cases such as:

```text
English lesson → speaking / writing / grammar
work item → internal steps
Plan → several independently meaningful Activities
Activity A → dependency → Activity B
```

B13 must distinguish:

```text
internal Step != Activity
composite work != generic sub-item hierarchy
Dependency != hierarchy
ordering != dependency
child Schedule != parent Schedule
child Session != parent Session
```

It also owns the temporal execution-structure foundation already latent in Create where appropriate: maximum Session count, merge compatibility, spacing and preparation/recovery rules.

B13 executes before B12 so replanning/solver logic sees real dependency structure rather than inventing it later.

## B14 — Temporal Create Completeness Gate

B14 is a gate, not a new feature vertical.

Every editable Home `+` field must be exactly one of:

```text
A. canonically persisted and behaviorally proven
B. truthful handoff to the owning vertical/capability
C. explicitly presentation/read-only
D. hidden/removed until supported
```

Never leave:

```text
editable field → value collected → silently ignored or normally rejected because implementation is absent
```

B14 audits Notes, appearance override, Tags, confirmation/reminder, execution policy and rich Event fields. It does not pull Work/Content/provider functionality into the Temporal kernel merely because the UI once exposed a field.

---

# 4. B09 start contract — Responsibility / Participation

B09 starts now. The goal is the smallest coherent actor/person layer needed by the temporal vertical, not collaboration infrastructure.

Permanent boundaries:

```text
Person != Account
Responsibility != Participation
participant != responsible actor != organizer/owner
shared Event truth != actor-specific participation truth
participation/attendance != Event Actual
another person's state != something DANTE controls by default
provider attendee != canonical Person identity by default
```

Before implementing persistence, inspect and reuse the existing Product / Domain / Logical / Physical authority for Person, Responsibility and Participation. Do not create a generic participant JSON/blob or a polymorphic shortcut when typed ownership/relations already exist.

B09 must also reconcile the existing Home `+` required/optional participant fields: if B09 owns their semantics they become truthful canonical authoring; otherwise they must be deferred/hidden rather than pretending to persist.

B09 closes only when the same-change obligations are satisfied where applicable:

```text
Logical/Physical authority
→ forward-only Alembic
→ SQLAlchemy
→ Dictionary + scope.json
→ direct PostgreSQL proof
→ backend/application
→ HTTP/OpenAPI/generated client if public
→ frontend Create/Timeline surface if part of B09
→ user-run local proof
→ roadmap/map/handoff evidence
```

---

# 5. Reserved ownership after B09

```text
B10
  Actual / Outcome / Confirmation / Resolution
  confirmation policy
  partial completion / finish-early realization semantics
  Expected outcome != Outcome

B11
  advanced recurrence / conditional behavior
  truthful resolution of the Create reminder field

B13
  internal steps / composition / dependencies
  execution-structure policy foundation

B12
  preferred windows / movement / fallback
  conflict detection and dependency-aware replanning
  deterministic solver proposals

B14
  field-by-field Create truthfulness gate

B07
  final UI/UX consolidation only after B14

B15
  whole-vertical regression + semantic red-team closure
```

---

# 6. Collaboration discipline

- user runs tests locally; assistant prepares exact commands
- no CI/GitHub Actions unless explicitly authorized
- push changes frequently
- do not edit historical migrations; use forward-only repair
- distinguish candidate truth from proven/protected-main truth
- generated API client is generated from OpenAPI, never manually edited
- B07 is presentation consolidation, not a place to invent missing semantics

---

# 7. Fresh-chat recovery

```text
1. this handoff
2. timeline-temporal-operational-roadmap.md
3. timeline-temporal-operational-map.md
4. docs/database/timeline-temporal-operational.md
5. current Logical Model / PostgreSQL blueprint sections relevant to B09
```

**Exact next action:** Inspect existing Responsibility / Participation / Person authority and persistence substrate, freeze the smallest coherent B09 contract, then implement it vertically.
