# Timeline / Temporal-Operational Vertical — Implementation Roadmap

- **Status:** CURRENT EXECUTION ROADMAP — reconciled 2026-09-26
- **Branch/workstream:** `feature/timeline-temporal-operational`
- **Vertical boundary:** Home `+` creation/configuration → canonical temporal truth → Timeline projection/actions → bounded lifecycle completion
- **Completed functional frontier:** B10-C Confirmation ✅ CLOSED / PROVEN 2026-09-26
- **Current block:** B10 Actual / Outcome / Confirmation / Resolution — IN PROGRESS; B10-D not started
- **Last proven DB frontier:** B10-C / PostgreSQL 18.6 / Alembic `20260925_79` / topology `167|5|123|93|329|279|446`
- **B10-C approved scope:** `docs/workstreams/timeline-temporal-operational-b10-c-scope-2026-09-25.md`
- **Deferred block:** B07 UI/UX Consolidation v1 — execute only after the functional/create-completeness sequence below
- **Live execution ledger:** `docs/workstreams/timeline-temporal-operational-map.md`
- **Continuation handoff:** `docs/workstreams/timeline-temporal-operational-handoff.md`

This document is the sequencing authority for the remaining Timeline / Temporal-Operational work.

---

# 0. Execution discipline

Every functional block closes vertically:

```text
current Product / Domain / Logical / Physical authority
→ persistence / Alembic / Dictionary when required
→ backend / application
→ HTTP API / OpenAPI when public
→ generated API client when public
→ frontend / real product surface when part of the block
→ local automated proof
→ documentation reconciliation
→ only then advance
```

For B10 specifically, B10-A/B/C/D are each implemented as one coherent major block and tested locally by the user only after that entire block is ready. The integrated manual real-app proof is intentionally deferred until B10-E.

Temporary UI is acceptable before B07, but an editable product field must never silently pretend to be canonical when the owning capability does not exist yet.

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
Expected outcome != Outcome
Responsibility != Participation
participant != responsible actor != organizer/owner
Person != Account
Step != Activity
Plan != Activity
Dependency != hierarchy
ordering != dependency
proposal != accepted effect
current accepted state != latest row
MaterialState payload != mutable runtime record
idempotency key != Domain identity
Undo != history rewind
editable Create intent != canonical persistence
```

Documentation stays small:

```text
ROADMAP = sequence/boundaries
MAP     = live decisions/evidence
HANDOFF = exact current position and next action
```

---

# 1. Active execution order

Historical block identifiers are preserved. Execution order is intentionally non-numeric where dependencies require it.

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
  B08-C TC-009 Session Duration End-to-End        ✅ CLOSED / PROVEN — local automated gate 2026-09-24
  B08-D Whole-block closure                       ✅ CLOSED / USER-REPORTED — automated gate and dogfood

B09 Responsibility / Participation               ✅ CLOSED / USER-REPORTED 2026-09-25
  B09-A typed persistence substrate               ✅ CLOSED / PROVEN 2026-09-25
  B09-B guarded mutation + application surface    ✅ CLOSED / PROVEN 2026-09-25
  B09-C non-Account Person referents              ✅ CLOSED / PROVEN 2026-09-25
  B09-D B09 whole-block closure                   ✅ CLOSED / USER-REPORTED 2026-09-25

B10 Actual / Outcome / Confirmation / Resolution 🟨 IN PROGRESS
  B10-A Actual / realization core                 ✅ CLOSED / PROVEN 2026-09-25
  B10-B Outcome                                   ✅ CLOSED / PROVEN
  B10-C Confirmation                              ✅ CLOSED / PROVEN 2026-09-26
  B10-D Reconciliation / resolution workflow      ⬜ NEXT — not started
  B10-E Final integration + acceptance            ⬜ — includes integrated real-app proof

B11 Advanced Recurrence / Conditional / Reminder ⬜
B13 Work Structure / Decomposition / Dependencies⬜
B12 Replanning / Conflict / Solver               ⬜
B14 Temporal Create Completeness Gate             ⬜
B07 UI/UX Consolidation v1                       ⏸ DEFERRED UNTIL B14
B15 Whole Vertical Closure                       ⬜
```

Execution sequence after B08 remains:

```text
B09 → B10 → B11 → B13 → B12 → B14 → B07 → B15
```

B13 exists before B12 because replanning/solver logic must already understand work structure and dependencies. B14 exists before B07 so final UI consolidation does not polish editable fields that are still non-canonical or unsupported.

External providers, native/offline/multi-device and account collaboration remain future backlog unless a bounded handoff is explicitly needed by one of these blocks.

---

# 2. Completed foundation B00–B10-A

B00–B06, B08, B09 and B10-A are closed. Permanent temporal boundaries at the B10-B entry point include:

```text
Activity may exist without Schedule
Event != Activity
Routine != Recurrence != Occurrence
Occurrence != Schedule
Schedule is the shared accepted-placement authority
Life Area / Tags are product organization, not Domain ownership
Person != Account != Actor
Responsibility != Participation
Session != Actual
Session END != completion
absence of Actual = unknown
Actual != Outcome != Confirmation
Expected outcome != Outcome
```

B10-A proven candidate frontier is `20260925_74` / `159|5|115|93|305|258|435`.

---

# 3. B09 — Responsibility / Participation — CLOSED / PROVEN

B09 adds actor/person semantics around temporal subjects without introducing account collaboration infrastructure.

Required boundaries:

```text
Person != Account
Responsibility != Participation
participant != responsible actor != organizer/owner
shared Event truth != actor-specific participation truth
expected/response Participation != Actual Participation
participation/attendance state != Event Actual
another person's participation != DANTE authority over that person's calendar/task system
```

Do not add a generic participant JSON/blob or make provider attendee identity canonical ontology.

## B09-A — typed persistence substrate — CLOSED / PROVEN

`20260925_66` adds exactly three typed direct/current relation tables:

```text
event_expected_participation(Event, Person, required|optional)
activity_responsibility(Activity, Person)
event_responsibility(Event, Person)
```

B09-A deliberately stops before guarded mutation/application/API/frontend and before Actual attendance semantics.

Local user-run proof on 2026-09-25:

```text
pytest focused B09-A persistence + both current-catalog suites
10 passed
```

Proven candidate DB frontier:

```text
Alembic  20260925_66
Topology 153|5|99|93|298|242|419
```

## B09-B — CLOSED / PROVEN

B09-B owns the guarded mutation/application layer over the B09-A substrate and the public API/OpenAPI/generated-client/Timeline surface.

It preserves:

```text
raw relation tables are not runtime mutation surfaces
Person identity is not Account identity
the public holder/participant vocabulary is only "self" in this slice
expected Participation does not establish acceptance/attendance/Actual
Responsibility does not imply Participation
participant authoring does not grant control over another person's calendar/task system
```

Home `+` required/optional participant textareas remain B14. Timeline detail is the truthful B09 authoring surface.

User-run local automated proof on 2026-09-25: generated check and both typechecks passed, web responsibility controls 4 passed, backend B09-B/B09-A/catalog/OpenAPI 18 passed. B09-B alone closes on this evidence; B09-C and B09-D followed before whole B09 closure.

## B09-C — CLOSED / PROVEN

B09-C introduces self-scoped Person referents without Account identity. Native Person creation includes NativeAddress and owner-local label with immutable create/rename receipts; the existing B09-B guarded role mutations admit only self or a locally registered Person. Timeline controls permit selection, creation and local-name correction for Activity/Event Responsibility and expected Event Participation. The label is local presentation, not universal human identity; no invitation, response, Actual, cross-account grant or collaboration is implied. The user-run automated proof on 2026-09-25 passed: generated:check (321 deterministic files), API-client and web typechecks, 7 web tests, 11 backend OpenAPI/API tests, and 18 PostgreSQL B09-C/B09-B/catalog regression tests. The generated client is committed at `875aaf48`; proven Alembic head is `20260925_69` and topology `158|5|109|93|303|254|433`.

## B09-D — CLOSED / PROVEN

B09-D integrates the proven A/B/C surfaces. The API/PostgreSQL gate exercises owner-local Person creation, replay, rename, Activity/Event Responsibility, expected Event Participation, removal, cross-actor isolation and absence of Actual/Session. The web gate exercises creation, local-name correction, assignment and removal. The user reported the real-app Timeline walkthrough working on 2026-09-25; the separate whole-vertical walkthrough remains in B15. Evidence and exact manual steps are recorded in `timeline-temporal-operational-b09-d-closure-2026-09-25.md`. No new persistence or collaboration semantics are introduced.

---

# 4. B10 — Actual / Outcome / Confirmation / Resolution — IN PROGRESS

B10 adds realization/reconciliation semantics while preserving:

```text
planned/intended != happened
Schedule != Session != Actual
Session END != completion
Actual != Outcome != Confirmation
Expected outcome != Outcome
no Actual != known non-realization/failure
```

B10 also owns the canonical behavior behind the existing Create confirmation policy and execution intents whose meaning depends on realized results, notably partial completion and finish-early semantics. Fast outcomes such as completed/partial/skipped/not-completed/postponed/replaced/cancelled must be represented without collapsing Actual, Outcome and Confirmation.

## B10-A — Actual / realization core — CLOSED / PROVEN

Scope authority: `docs/workstreams/timeline-temporal-operational-b10-scope-freeze.md`.
Closure evidence: `docs/workstreams/timeline-temporal-operational-b10-a-closure-2026-09-25.md`.

B10-A closes explicit self-scoped Actual realization for Activity, Event and Occurrence over the canonical CP6 substrate.

Migration chain:

```text
20260925_70 guarded Actual realization authoring/read + immutable operation receipt
20260925_71 exact Activity/Event/Occurrence family binding
20260925_72 forward repair for CP6 Actual/scoped-address creation order
20260925_73 canonical family-aware write/read signatures; hidden overloads removed
20260925_74 qualify current-history correction + canonical bounded FK name
```

Proven database frontier:

```text
Alembic  20260925_74
Topology 159|5|115|93|305|258|435
```

Permanent B10-A boundaries:

```text
Session END != Actual
absence of Actual = unknown
known realization_occurred=false != absence of Actual
current accepted realization != latest row
Session evidence does not share Actual identity
Actual != Outcome != Confirmation
```

The final user-run local PostgreSQL/application/catalog gate passed on 2026-09-25:

```text
14 passed in 25.06s
POSTGRES TEST EXIT: 0
```

The earlier generation/client/web/OpenAPI parts of the same B10-A gate were also green. Generated OpenAPI/Orval artifacts are committed at `780c612d` (`feat(api-client): generate B10-A Actual contracts`). No CI/GitHub Actions were used.

Manual real-app B10 validation remains intentionally deferred to B10-E.

## B10-B — Outcome — CLOSED / PROVEN

Closure evidence: `docs/workstreams/timeline-temporal-operational-b10-b-closure-2026-09-25.md`.

```text
Alembic  20260925_78
Topology 163|5|119|93|317|268|440
```

## B10-C — Confirmation — CLOSED / PROVEN

Closure evidence: `docs/workstreams/timeline-temporal-operational-b10-c-closure-2026-09-26.md`.

```text
Alembic  20260925_79
Topology 167|5|123|93|329|279|446
```

Confirmation attests a specific Outcome MaterialState for a purpose. It does not collapse into Actual, Outcome, Authority, Verification or universal truth. No manual real-app proof until B10-E.

## B10-D — Reconciliation / resolution workflow

B10-D owns the governed reconciliation workflow among realized facts/results/confirmation. Do not invent a generic `Resolution` ontology entity unless the repository/domain authority explicitly requires one.

## B10-E — Final integration + acceptance

B10-E integrates A/B/C/D, runs the final automated regressions and then performs the single real-app B10 proof. Only then is the whole B10 block closed.

## B11 — Advanced Recurrence / Conditional / Reminder

B11 extends recurrence and conditional/reminder behavior without RRULE-as-ontology, fake Activity materialization or an unjustified universal Reminder owner.

The existing editable Create reminder field must leave B11 either canonically supported, truthfully handed off, or hidden until that capability exists.

## B13 — Work Structure / Decomposition / Dependencies

B13 distinguishes:

```text
1. INTERNAL STEP
   ordered/internal execution structure of one Activity
   Step != Activity

2. COMPOSITE WORK
   Plan or other legitimate composition containing real Activities
   each Activity keeps its own identity/lifecycle/Schedule/Session

3. DEPENDENCY
   typed relationship between independently meaningful work
   Dependency != hierarchy
   ordering != dependency
```

Examples such as `English lesson → speaking/writing/grammar` must be representable either as internal steps or as independently meaningful Activities; the UI must not force both cases into one generic `sub_item` model.

B13 also closes the temporal execution-structure foundation already exposed by Create where semantically appropriate: maximum Session count, merge compatibility, spacing, preparation/recovery and related structure rules.

Permanent boundaries:

```text
Step != Activity
Plan != Activity
Dependency != hierarchy
ordering != dependency
child Schedule != parent Schedule
child Session != parent Session
all children resolved != parent Actual unless an explicit policy establishes that meaning
```

## B12 — Replanning / Conflict / Solver

B12 is deterministic-first replanning/conflict/solver and owns preferred windows, movement policies, fallback policies and dependency-aware replanning.

```text
canonical truth + constraints/preferences + B13 dependencies
→ deterministic candidate generation / optimization
→ Proposal(s)
→ optional AI interpretation/ranking assistance
→ governed acceptance
→ canonical Schedule mutation
```

Hard constraints are never violated silently.

```text
proposal != accepted Schedule
preferred window != accepted Schedule
fallback policy != automatic hidden mutation
solver UNKNOWN != INFEASIBLE
AI != scheduling authority
```

---

# 5. B14 — Temporal Create Completeness Gate

For every editable field visible in Create, exactly one must be true:

```text
A. canonically persisted and covered by behavioral proof
B. truthful handoff to the owning vertical/capability
C. explicitly presentation/read-only
D. hidden/removed until supported
```

Forbidden:

```text
editable field
→ value collected by UI
→ normal submit silently ignores it or rejects it only because backend support is absent
```

The gate audits Notes, appearance override, Tags, confirmation/reminder policy, execution-structure policy, Event location/availability/visibility, Event purpose/expected outcome/decision requirement, required/optional participants, resources/pre-read and conference/provider fields.

B14 does not force every field into the Temporal kernel. Truthful ownership matters more than maximal scope.

---

# 6. B07 — UI/UX Consolidation v1 — DEFERRED

Execute after B14 so final Home/Timeline/`+`/editors/actions/navigation are designed once against a truthful functional vocabulary. B07 does not create missing semantics.

---

# 7. B15 — Whole Vertical Closure

B15 reconciles migrations/catalog/Dictionary, backend/API/client, frontend, negative invariants, local automated proof, required real-stack walkthroughs and the live documentation ledger.

B15 must include a red-team semantic audit for accidental collapses such as:

```text
Activity == Event
Routine == Recurrence
Occurrence == Schedule
Schedule == Session
Session END == completion/Actual
Expected outcome == Outcome
Responsibility == Participation
Participant == Account
Step == Activity
Dependency == hierarchy
editable Create field == assumed canonical support
```

---

# 8. Current gate

```text
B00–B06 ✅ CLOSED / PROVEN
B08     ✅ CLOSED / USER-REPORTED 2026-09-24
B09     ✅ CLOSED / USER-REPORTED 2026-09-25
  B09-A ✅ CLOSED / PROVEN 2026-09-25
  B09-B ✅ CLOSED / PROVEN 2026-09-25
  B09-C ✅ CLOSED / PROVEN 2026-09-25
  B09-D ✅ CLOSED / USER-REPORTED 2026-09-25
B10     🟨 IN PROGRESS
  B10-A ✅ CLOSED / PROVEN 2026-09-25
  B10-B ✅ CLOSED / PROVEN 2026-09-25
  B10-C ✅ CLOSED / PROVEN 2026-09-26
  B10-D ⬜ NEXT — not started
  B10-E ⬜ — integrated manual proof at end
B11     ⬜ NOT STARTED
B13     ⬜ NOT STARTED
B12     ⬜ NOT STARTED
B14     ⬜ NOT STARTED
B07     ⏸ DEFERRED UNTIL B14
B15     ⬜ NOT STARTED
```

**Current action:** the B10-C local gate is green. Commit the generated client only when the user asks. Do not start B10-D until the user approves that gate. Do not hand-edit generated artifacts. Do not use CI/GitHub Actions.