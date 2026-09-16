# Timeline / Temporal-Operational Vertical — Semantic Work Map / Live Ledger

- **Status:** CURRENT SEMANTIC MAP + LIVE IMPLEMENTATION LEDGER — reconciled 2026-09-16
- **Branch:** `feature/timeline-temporal-operational`
- **Roadmap:** `docs/workstreams/timeline-temporal-operational-roadmap.md`
- **B02 closure:** `docs/workstreams/timeline-temporal-operational-b02-closure-2026-09-16.md`
- **Detailed semantic freeze:** `docs/workstreams/archive/timeline-temporal-operational-map-ledger-snapshot-2026-09-15.md`
- **Historical roadmap freeze:** `docs/workstreams/archive/timeline-temporal-operational-roadmap-freeze-2026-09-07.md`

The archived semantic freeze preserves the full pre-implementation semantic analysis, non-collapse registers, coverage audit and original checklist wording. It remains binding semantic evidence unless explicitly amended here. This file is the **current live progress authority** and current numbering authority.

---

# 1. Permanent semantic boundaries

```text
Person != Account != Principal != Actor
Goal != Plan != Activity
Activity != Event != Routine
Activity != Schedule
Event != Schedule
Routine != Recurrence
Recurrence != Occurrence
Occurrence != Schedule
Schedule != Temporal Constraint
Schedule != Session
Schedule != Actual
Session != Actual
Actual != Outcome
Outcome != Confirmation
planned/intended != happened
current accepted state != latest row
idempotency key != Domain identity
provider identity != DANTE identity
projection != canonical truth
proposal != accepted effect
pending != success
unscheduled != deleted
Undo != DB/history rewind
estimated effort != scheduled duration != Session duration
floating-local != named-zone-local != absolute instant
date span != coarse local period
coarse precision != fabricated exact clock time
source wall-clock intent != resolved instant
```

These boundaries cannot be weakened by UI convenience, ORM convenience, provider shape or roadmap pressure.

---

# 2. High-level semantic tree

```text
TIMELINE / TEMPORAL-OPERATIONAL
│
├── ORIGINATING
│   ├── Activity
│   ├── Event
│   ├── Routine
│   └── Session recording
│
├── TEMPORAL EXPECTATION
│   ├── Schedule
│   ├── Temporal Constraint
│   ├── Movement / replanning policy
│   ├── Recurrence
│   └── Occurrence
│
├── EXECUTION / REALITY
│   ├── Session
│   ├── Actual
│   └── Outcome
│
├── RESOLUTION / COMMON GROUND
│   ├── Confirmation
│   ├── Acknowledgement
│   └── Resolution Queue / review
│
├── PRODUCT ORGANIZATION
│   ├── Calendar / Life Area
│   ├── Tags
│   ├── Context / grouping
│   └── Appearance (separate)
│
├── CONDITIONAL / AUTOMATION
│   ├── Conditional Policy
│   ├── Reminder intent
│   └── bounded automatic effects
│
└── DERIVED SURFACES
    ├── Timeline
    ├── Planning Tray
    ├── Detail / History
    ├── Resolution Queue
    ├── conflict / replanning explanation
    └── Analytics / Signals
```

This is a work map, not an inheritance hierarchy and not authorization for a generic temporal mega-entity.

---

# 3. Status semantics

```text
⬜ NOT STARTED
🟨 IN PROGRESS / partially satisfied but global gate remains
✅ DONE / CLOSED for the exact checklist scope
⛔ BLOCKED
```

Rules:

1. `✅` requires all applicable gates for the checklist scope.
2. A capability that is intentionally not activated in a block may close only when the non-activation boundary itself was the required applicability gate and the future owning block is explicit.
3. No item may remain accidentally open merely because documentation was not reconciled after proof.
4. No item may be marked green merely because a future semantic concept is described in the Domain model.
5. Historical numbering before 2026-09-16 is preserved only in archive snapshots.

---

# 4. Current roadmap position

```text
B00 Real Data Spine                              ✅ CLOSED / PROVEN
B01 Activity Core                                ✅ CLOSED / PROVEN
B02 Schedule Core                                ✅ CLOSED / PROVEN
B03 Event Core                                   ⬜ NEXT
B04 Temporal Constraints + Movement Policy       ⬜
B05 Product Organization                         ⬜
B06 Routine / Recurrence / Occurrence Baseline   ⬜
B07 UI/UX Consolidation v1                       ⬜
B08 Session Runtime                              ⬜
B09 Responsibility / Participation               ⬜
B10 Actual / Outcome / Confirmation / Resolution ⬜
B11 Advanced Recurrence / Conditional / Reminder ⬜
B12 Replanning / Conflict / Solver               ⬜
B13 Provider / Offline / Multi-device             ⬜
B14 Analytics / Statistics / Signals             ⬜
B15 Whole Vertical Closure                       ⬜
```

---

# 5. Completed foundation ledgers

## 5.1 B00 — Real Data Spine ✅

All previously frozen B00 checklist IDs are closed:

```text
SPINE-001 … SPINE-012   ✅
B00-T01 … B00-T05      ✅
```

Proven outcome: normal runtime has one real temporal backend/PostgreSQL data path, truthful empty/error states, isolated test fixtures, authenticated context/timezone handling and real-stack E2E. Exact item-level historical evidence is preserved in the archived ledger snapshot.

## 5.2 B01 — Activity Core ✅

All previously frozen B01 checklist IDs are closed:

```text
ACT-001 … ACT-017      ✅
B01-T01 … B01-T08      ✅
```

The B01 applicability gates for estimated effort, sub-Activity structure and completion semantics closed through explicit non-activation: no fake effort/subtask/done semantics were introduced before their owning future blocks.

---

# 6. B02 — Schedule Core ✅ CLOSED / PROVEN

Closure authority:

```text
docs/workstreams/timeline-temporal-operational-b02-closure-2026-09-16.md
```

## 6.1 Schedule capability checklist

- ✅ **[SCH-001]** Re-open Schedule authority/current CP6 placement tables/views/validators before implementation. — B02 reused the accepted CP6 Schedule/current/history machinery.
- ✅ **[SCH-002]** Preserve subject eligibility Activity/Event/Occurrence; first activate Activity path. — Physical/shared eligibility was preserved while only Activity was product-activated; Event remains B03 and Occurrence remains B06.
- ✅ **[SCH-003]** Implement/consume date-span placement correctly. — Backend/read model/web create/reload proof is green.
- ✅ **[SCH-004]** Implement/consume floating-local placement correctly. — Manual B02 A–F plus automated/full-stack proof is green.
- ✅ **[SCH-005]** Implement/consume named-zone placement correctly. — Source wall-clock intent, resolved instant and explicit DST policy remain distinct.
- ✅ **[SCH-006]** Implement/consume absolute placement correctly. — API/runtime/read-model coverage is green; absolute is intentionally not manufactured as a primary end-user Create mode.
- ✅ **[SCH-007]** Preserve coarse accepted placement precision without manufactured timestamps. — `coarse_local_period` is persisted/projected without fake exact boundaries.
- ✅ **[SCH-008]** Preserve Schedule absence as valid state. — Unschedule leaves owner/history intact and returns Activity to Planning Tray.
- ✅ **[SCH-009]** Preserve possible 0..N planned placements; do not hard-code universal 1:1. — Real PostgreSQL proof established independent Schedule owners for one Activity where semantics allow.
- ✅ **[SCH-010]** Implement accepted Schedule creation for Activity.
- ✅ **[SCH-011]** Implement Schedule MaterialState revision.
- ✅ **[SCH-012]** Implement explicit current accepted Schedule binding.
- ✅ **[SCH-013]** Preserve Schedule history/original expectation.
- ✅ **[SCH-014]** Implement expected-state concurrency check.
- ✅ **[SCH-015]** Implement Schedule mutation idempotency and changed-intent operation-id rejection.
- ✅ **[SCH-016]** Implement real Planning Tray → Timeline placement preserving Activity identity.
- ✅ **[SCH-017]** Implement real Timeline exact drag earlier/later as governed Schedule revision. — Frontend regression plus real full-stack governed move passed.
- ✅ **[SCH-018]** Implement supported duration/start/end adjustment without conflating Actual.
- ✅ **[SCH-019]** Implement anchored time editor against real Schedule mutation.
- ✅ **[SCH-020]** Implement Activity unschedule back to Planning Tray where valid.
- ✅ **[SCH-021]** Implement guarded Undo through a new monotonic accepted state/revision.
- ✅ **[SCH-022]** Preserve explicit expectation change as Schedule revision. — B02 proves planning changes remain Schedule mutations. The special case of changing expectation while a real Session is running cannot exist before B08 and is transferred there; B02 did not fake Session runtime to satisfy it.
- ✅ **[SCH-023]** Preserve early/late/overrun reality as Session/Actual, not automatic Schedule rewrite. — B02 applicability gate is satisfied by strict non-activation: Schedule operations never manufacture Session/Actual. Recording/deriving real deviation is owned by B08/B10.
- ✅ **[SCH-024]** Implement temporal range/local-day query for scheduled Activity across activated Schedule forms.

## 6.2 B02 proof checklist

- ✅ **[B02-T01]** Schedule form/validator tests across date-span, floating-local, named-zone, absolute and coarse.
- ✅ **[B02-T02]** Schedule current/history direct PostgreSQL tests.
- ✅ **[B02-T03]** Reschedule/unschedule/Undo application tests including cross-form revision.
- ✅ **[B02-T04]** Stale expected-state/idempotency/reuse-conflict tests.
- ✅ **[B02-T05]** DST/local-day tests for exposed Schedule forms. — Named-zone gap/overlap and local-day/range semantics covered by backend/web regression evidence.
- ✅ **[B02-T06]** Timeline drag/time-editor/Planning Tray frontend regressions.
- ✅ **[B02-T07]** Firefox T1 critical interaction/full-stack regression. — Final Firefox run `2 / 2 PASS`.
- ✅ **[B02-T08]** Real-stack create/unplaced → establish → move → cross-form revise → unschedule → Undo → reload test. — Final Chromium `2 / 2 PASS`; same spec Firefox `2 / 2 PASS`.
- ✅ **[B02-T09]** Manual `userTest` Schedule/Undo/conflict acceptance. — B02 A–F approved 2026-09-15. The later E-specific manual protocol was not fabricated as PASS; E-specific semantics close on PostgreSQL/backend/frontend/full-stack evidence per the explicit B02 closure decision.

## 6.3 B02 persistence/quality closure

```text
Alembic head / candidate authority              20260915_26
Dictionary / SQLAlchemy / Alembic parity        ✅
current-catalog + migration PostgreSQL gate      20 / 20 PASS
HEAD → base → HEAD round-trip                     1 / 1 PASS
B02 PostgreSQL proof group                       11 PASS / 2 deselected
Backend temporal/API targeted                    41 / 41 PASS
Backend full non-PostgreSQL                     495 PASS / 188 deselected
Web B02-E3 targeted                             104 / 104 PASS
Web full regression                             717 / 717 PASS
TypeScript / ESLint / generated:check            PASS
Chromium B02-E full-stack                         2 / 2 PASS
Firefox B02-E full-stack                          2 / 2 PASS
```

No B02 checklist item remains accidentally open.

---

# 7. B03 — Event Core ⬜ NEXT

- ⬜ **[EVT-001]** Re-open Event Domain/Logical/Physical authority before implementation.
- ⬜ **[EVT-002]** Resolve minimum meaningful Event descriptive persistence.
- ⬜ **[EVT-003]** Implement idempotent `CreateEvent`.
- ⬜ **[EVT-004]** Activate Event macro-class in `+` Create.
- ⬜ **[EVT-005]** Implement timed Event using shared B02 Schedule.
- ⬜ **[EVT-006]** Implement all-day/date-span Event in real all-day lane.
- ⬜ **[EVT-007]** Implement multi-day Event semantics/query/rendering.
- ⬜ **[EVT-008]** Implement postponed/TBD Event with identity/history and no fake placeholder Schedule.
- ⬜ **[EVT-009]** Preserve original expectation/current Schedule/Actual separation.
- ⬜ **[EVT-010]** Implement Event Agenda/internal parts at accepted product level.
- ⬜ **[EVT-011]** Preserve Agenda part `!= Activity/Event/Occurrence/Session/Actual` by default.
- ⬜ **[EVT-012]** Implement preparation/follow-up Activity relation when activated.
- ⬜ **[EVT-013]** Implement Place/conference intent only through justified relation/profile semantics.
- ⬜ **[EVT-014]** Preserve ordinary Event attendance `!= Session`.
- ⬜ **[EVT-015]** Preserve Event `!= Availability/Capacity Claim`.
- ⬜ **[B03-T01]** Event create/application tests.
- ⬜ **[B03-T02]** Timed/all-day/multi-day PostgreSQL/API tests.
- ⬜ **[B03-T03]** Postponed/TBD history/query tests.
- ⬜ **[B03-T04]** Event Agenda semantic/frontend tests.
- ⬜ **[B03-T05]** Shared Schedule regression suite rerun for Activity + Event.
- ⬜ **[B03-T06]** E2E Event create/reschedule/all-day/reload test.
- ⬜ **[B03-T07]** Manual `userTest` Event acceptance.

---

# 8. B04 — Temporal Constraints / movement policy ⬜

- ⬜ **[TC-001]** Re-open Temporal Constraint authority before persistence design.
- ⬜ **[TC-002]** Resolve first typed persistence/runtime representation; no generic `due_at`/JSON escape.
- ⬜ **[TC-003]** Implement earliest-start constraint where required.
- ⬜ **[TC-004]** Implement latest-start constraint where required.
- ⬜ **[TC-005]** Implement latest-completion/delivery Deadline semantics with explicit facet.
- ⬜ **[TC-006]** Implement hard validity window.
- ⬜ **[TC-007]** Implement preferred/soft window.
- ⬜ **[TC-008]** Implement minimum/maximum duration where required.
- ⬜ **[TC-009]** Implement minimum contiguous Session duration where required.
- ⬜ **[TC-010]** Implement spacing/recovery constraint where required.
- ⬜ **[TC-011]** Implement relative-before/after constraint where required.
- ⬜ **[TC-012]** Implement movement policy separately from Temporal Constraint.
- ⬜ **[TC-013]** Ensure hard planning violation does not block recording contradictory Actual reality.
- ⬜ **[TC-014]** Implement hard/soft conflict explanation.
- ⬜ **[B04-T01]** Constraint typed-validation tests.
- ⬜ **[B04-T02]** Constraint persistence/direct PostgreSQL tests if DDL added.
- ⬜ **[B04-T03]** Hard vs soft placement behavior tests.
- ⬜ **[B04-T04]** Deadline passage `!= Outcome` test.
- ⬜ **[B04-T05]** Manual `userTest` constraint/explanation acceptance.

---

# 9. B05 — Life Area / Calendar / Tags ⬜

- ⬜ **[ORG-001]** Re-open product/Logical organization authority before persistence design.
- ⬜ **[ORG-002]** Prove exact durable Life Area representation; no new owner by convenience.
- ⬜ **[ORG-003]** Implement Life Area create.
- ⬜ **[ORG-004]** Implement rename.
- ⬜ **[ORG-005]** Implement reorder.
- ⬜ **[ORG-006]** Implement archive.
- ⬜ **[ORG-007]** Implement hide/show.
- ⬜ **[ORG-008]** Implement icon/color appearance metadata without making color semantic truth.
- ⬜ **[ORG-009]** Implement one primary Life Area relation for applicable planning item.
- ⬜ **[ORG-010]** Implement secondary Tags separately.
- ⬜ **[ORG-011]** Preserve Life Area `!= Goal/Plan/Tag/Place/provider calendar`.
- ⬜ **[ORG-012]** Replace/reconcile prototype Timeline groups with real product organization.
- ⬜ **[ORG-013]** Preserve hidden-item relevance to authorized conflict/scheduling reasoning.
- ⬜ **[ORG-014]** Preserve future actor-local organization for shared canonical item.
- ⬜ **[ORG-015]** Ensure accessibility does not rely on color alone.
- ⬜ **[B05-T01]** Organization lifecycle tests.
- ⬜ **[B05-T02]** Item assignment/filter/grouping tests.
- ⬜ **[B05-T03]** Tags-vs-primary-area tests.
- ⬜ **[B05-T04]** Hidden-group conflict-awareness test.
- ⬜ **[B05-T05]** Accessibility/frontend grouping tests.
- ⬜ **[B05-T06]** Manual `userTest` Life Area organization acceptance.

---

# 10. B06 — Routine / Recurrence / Occurrence baseline ⬜

## Routine

- ⬜ **[ROU-001]** Re-open Routine authority/current identity shell.
- ⬜ **[ROU-002]** Resolve minimum meaningful Routine product persistence.
- ⬜ **[ROU-003]** Implement Routine create and activate Routine macro-class.
- ⬜ **[ROU-004]** Implement Routine recurrence MaterialState authoring.
- ⬜ **[ROU-005]** Implement Routine pause.
- ⬜ **[ROU-006]** Implement Routine resume.
- ⬜ **[ROU-007]** Implement Routine end.
- ⬜ **[ROU-008]** Preserve skip Occurrence `!= pause != end`.
- ⬜ **[ROU-009]** Implement composite Routine structure when required.
- ⬜ **[ROU-010]** Preserve observed pattern `!= canonical Routine intent`.

## Recurrence baseline

- ⬜ **[REC-001]** Calendar-wall-clock authoring/evaluation.
- ⬜ **[REC-002]** Elapsed-interval authoring/evaluation.
- ⬜ **[REC-003]** Quota-per-period authoring/evaluation.
- ⬜ **[REC-004]** Cyclic-positional authoring/evaluation.
- ⬜ **[REC-005]** Explicit pattern anchor/phase semantics.
- ⬜ **[REC-006]** Effective range: open/until/count.
- ⬜ **[REC-007]** Expected-count `!= successful-completion-count`.
- ⬜ **[REC-008]** Named-zone/floating/absolute recurrence timezone modes as applicable.
- ⬜ **[REC-009]** Quota period frame.
- ⬜ **[REC-010]** Stable quota identities without invented ordinal meaning.
- ⬜ **[REC-011]** Structural exclusion `!= generated then skipped`.
- ⬜ **[REC-012]** Virtual future/materialization horizon.
- ⬜ **[REC-013]** Frontend authors specification only; backend owns canonical generation.
- ⬜ **[REC-014]** Reuse recurrence capability for Event recurrence.

## Occurrence

- ⬜ **[OCC-001]** Backend recurrence evaluator/checkpoint consumption.
- ⬜ **[OCC-002]** Materialize stable Occurrence identity when justified.
- ⬜ **[OCC-003]** Bind exact governing Recurrence MaterialState for generated Occurrence.
- ⬜ **[OCC-004]** Persist compatible generation coordinate.
- ⬜ **[OCC-005]** Implement `explicit_extra` without fake governing recurrence state.
- ⬜ **[OCC-006]** Preserve Occurrence Schedule optionality.
- ⬜ **[OCC-007]** One-off occurrence-specific Schedule exception.
- ⬜ **[OCC-008]** This-occurrence-only change scope.
- ⬜ **[OCC-009]** This-and-future source recurrence revision scope.
- ⬜ **[OCC-010]** Preserve historical generating state after source revision.
- ⬜ **[OCC-011]** Preserve materialized future history when new rule no longer derives it.
- ⬜ **[OCC-012]** Preserve Occurrence identity through reschedule.

## Tests

- ⬜ **[B06-T01]** Four CP6 recurrence-family tests.
- ⬜ **[B06-T02]** Recurrence direct PostgreSQL/current-state tests.
- ⬜ **[B06-T03]** DST wall-clock recurrence tests.
- ⬜ **[B06-T04]** Quota frame/no-exact-time tests.
- ⬜ **[B06-T05]** Pattern anchor/effective-range tests.
- ⬜ **[B06-T06]** Structural exclusion vs skip.
- ⬜ **[B06-T07]** `explicit_extra` invariant tests.
- ⬜ **[B06-T08]** This-occurrence vs this-and-future.
- ⬜ **[B06-T09]** Historical generating-state preservation.
- ⬜ **[B06-T10]** Virtual vs materialized future reconciliation.
- ⬜ **[B06-T11]** Event + Routine shared recurrence regression.
- ⬜ **[B06-T12]** Frontend no-canonical-browser-expansion test.
- ⬜ **[B06-T13]** E2E recurring items → Timeline.
- ⬜ **[B06-T14]** Manual recurrence acceptance.

---

# 11. B07 — UI/UX Consolidation v1 ⬜

This is the new explicit 60–70% product-quality checkpoint. It changes presentation/information architecture, not canonical semantics.

- ⬜ **[UIX-001]** Inventory current temporal UI surfaces/components and identify duplication/inconsistent hierarchy.
- ⬜ **[UIX-002]** Define coherent temporal information architecture for Create, Timeline, Planning Tray and detail affordances.
- ⬜ **[UIX-003]** Implement progressive disclosure so common Create paths do not expose all advanced controls at once.
- ⬜ **[UIX-004]** Preserve distinct Activity/Event/Routine authoring while reusing only semantically shared components.
- ⬜ **[UIX-005]** Consolidate exact/date-span/coarse/named-zone temporal editors into a coherent interaction family without flattening forms.
- ⬜ **[UIX-006]** Redesign Timeline visual hierarchy/density while preserving canonical projection semantics.
- ⬜ **[UIX-007]** Redesign Planning Tray usability while preserving unplaced-reason semantics and identity.
- ⬜ **[UIX-008]** Consolidate card/detail/editor affordances and interaction hierarchy.
- ⬜ **[UIX-009]** Establish/clean typography, spacing, layout and reusable component tokens.
- ⬜ **[UIX-010]** Consolidate button/input/select/modal/drawer patterns.
- ⬜ **[UIX-011]** Implement responsive/mobile behavior for activated temporal surfaces.
- ⬜ **[UIX-012]** Preserve deterministic keyboard/focus/pointer grammar.
- ⬜ **[UIX-013]** Ensure accessibility labels/state and no color-only semantics.
- ⬜ **[UIX-014]** Consolidate truthful loading/empty/pending/error/conflict states.
- ⬜ **[UIX-015]** Preserve F0/T1 governed-operation contracts; no frontend-only canonical success.
- ⬜ **[UIX-016]** Ensure ViewModel/presentation fields do not become new canonical meaning.
- ⬜ **[UIX-017]** Reconcile frontend UI registry/component documentation after consolidation.
- ⬜ **[B07-T01]** Create/editor component regression suite.
- ⬜ **[B07-T02]** Timeline/Planning Tray interaction regression suite.
- ⬜ **[B07-T03]** Temporal-form presentation regression suite.
- ⬜ **[B07-T04]** Responsive/mobile automated checks.
- ⬜ **[B07-T05]** Accessibility/keyboard/focus automated checks.
- ⬜ **[B07-T06]** Chromium + Firefox critical interaction pass.
- ⬜ **[B07-T07]** Manual UI/UX acceptance proving the intended 60–70% quality checkpoint.

---

# 12. B08 — Session Runtime ⬜

- ⬜ **[SES-001]** Re-open Session Domain/CP6 timing authority.
- ⬜ **[SES-002]** Resolve typed Session execution-context relation persistence.
- ⬜ **[SES-003]** Direct manual retrospective Session recording.
- ⬜ **[SES-004]** Spontaneous Session without fake Activity/Schedule.
- ⬜ **[SES-005]** Timer start.
- ⬜ **[SES-006]** Pause as same Session.
- ⬜ **[SES-007]** Resume.
- ⬜ **[SES-008]** End/close.
- ⬜ **[SES-009]** Activity contextual start.
- ⬜ **[SES-010]** Occurrence contextual start.
- ⬜ **[SES-011]** Ordinary Event attendance `!= Session`.
- ⬜ **[SES-012]** Absolute timing.
- ⬜ **[SES-013]** Elapsed-only/uncertain-boundary timing where required.
- ⬜ **[SES-014]** Timing precision/provenance.
- ⬜ **[SES-015]** Derived elapsed/paused/active durations.
- ⬜ **[SES-016]** Timing correction preserving Session identity.
- ⬜ **[SES-017]** Context correction preserving lineage.
- ⬜ **[SES-018]** Session split with lineage.
- ⬜ **[SES-019]** Session merge with lineage.
- ⬜ **[SES-020]** False-data deletion/invalidation boundary.
- ⬜ **[SES-021]** Semantically compatible overlapping Sessions.
- ⬜ **[SES-022]** One Session related to multiple intentions without duplicate capture.
- ⬜ **[SES-023]** Stale-running detection/review without fabricated end.
- ⬜ **[SES-024]** Idempotent Session controls.
- ⬜ **[SES-025]** Expected-state conflict on concurrent controls.
- ⬜ **[SES-026]** Session end `!= Activity/Occurrence completion`.
- ⬜ **[SES-027]** During active execution, explicit changed expectation revises Schedule while mere temporal deviation does not.
- ⬜ **[B08-T01]** Manual/spontaneous Session tests.
- ⬜ **[B08-T02]** Start/pause/resume/end tests.
- ⬜ **[B08-T03]** Session timing/current-state PostgreSQL tests.
- ⬜ **[B08-T04]** Precision/correction tests.
- ⬜ **[B08-T05]** Split/merge/lineage tests.
- ⬜ **[B08-T06]** Overlap/multi-intention tests.
- ⬜ **[B08-T07]** Stale-running tests.
- ⬜ **[B08-T08]** Concurrent/idempotent control tests.
- ⬜ **[B08-T09]** Schedule-vs-actual-deviation boundary tests.
- ⬜ **[B08-T10]** E2E Activity/Occurrence → Session timer.
- ⬜ **[B08-T11]** Manual Session lifecycle acceptance.

---

# 13. B09 — Responsibility / Participation / actor relations ⬜

- ⬜ **[REL-001]** Re-open Responsibility/Participation/Actor authority.
- ⬜ **[REL-002]** Preserve Person/Account/Principal/Actor separation.
- ⬜ **[REL-003]** Bounded requester relation.
- ⬜ **[REL-004]** Responsible/accountable Actor relation.
- ⬜ **[REL-005]** Expected performer separate where required.
- ⬜ **[REL-006]** Actual performer separate where required.
- ⬜ **[REL-007]** No ambiguous `assigned_to` persistence.
- ⬜ **[PAR-001]** Event intended/invited Participation.
- ⬜ **[PAR-002]** Accepted response.
- ⬜ **[PAR-003]** Tentative response.
- ⬜ **[PAR-004]** Declined response.
- ⬜ **[PAR-005]** No-response remains unknown.
- ⬜ **[PAR-006]** Actual attendance separately.
- ⬜ **[PAR-007]** Actual attendance without prior invitation where valid.
- ⬜ **[PAR-008]** Accepted `!= attended`; declined `!= proven absence`.
- ⬜ **[ACK-001]** Acknowledgement remains separate common-ground act.
- ⬜ **[B09-T01]** Responsibility role-separation tests.
- ⬜ **[B09-T02]** Participation response/history tests.
- ⬜ **[B09-T03]** Actual attendance independence tests.
- ⬜ **[B09-T04]** Unexpected participant test.
- ⬜ **[B09-T05]** No generic-role persistence review/test.
- ⬜ **[B09-T06]** Manual actor/participant acceptance.

---

# 14. B10 — Actual / Outcome / Confirmation / Resolution ⬜

## Actual

- ⬜ **[ACTUAL-001]** Re-open Actual Domain/CP6 realization authority.
- ⬜ **[ACTUAL-002]** Activity Actual subject path.
- ⬜ **[ACTUAL-003]** Event Actual subject path.
- ⬜ **[ACTUAL-004]** Occurrence Actual subject path.
- ⬜ **[ACTUAL-005]** No Actual remains unknown.
- ⬜ **[ACTUAL-006]** Known non-realization distinctly.
- ⬜ **[ACTUAL-007]** Partial realization where required.
- ⬜ **[ACTUAL-008]** Differently-realized/replacement context.
- ⬜ **[ACTUAL-009]** 0..N Session basis where applicable.
- ⬜ **[ACTUAL-010]** Event Actual without Session.
- ⬜ **[ACTUAL-011]** Observation/Measurement remains external fact semantics.
- ⬜ **[ACTUAL-012]** Current accepted realization/history/correction.
- ⬜ **[ACTUAL-013]** Competing assertion/reconciliation boundary.
- ⬜ **[ACTUAL-014]** Early/late/overrun reality derives from Session/Actual against accepted Schedule and never silently rewrites Schedule.

## Outcome

- ⬜ **[OUT-001]** Re-open Outcome authority and prove first persistence shape.
- ⬜ **[OUT-002]** Context-specific Activity result vocabulary.
- ⬜ **[OUT-003]** Context-specific Event result vocabulary.
- ⬜ **[OUT-004]** Context-specific Occurrence result vocabulary.
- ⬜ **[OUT-005]** No Outcome `!= negative`.
- ⬜ **[OUT-006]** Outcome `!= lifecycle status/Observation/Artifact/Milestone`.
- ⬜ **[OUT-007]** Outcome correction/history.

## Confirmation / Acknowledgement

- ⬜ **[CNF-001]** Re-open Confirmation authority and persistence shape.
- ⬜ **[CNF-002]** Confirmer Actor.
- ⬜ **[CNF-003]** Exact target/material-state binding.
- ⬜ **[CNF-004]** Purpose/context where required.
- ⬜ **[CNF-005]** Confirmation S1 remains historical after target S2 correction.
- ⬜ **[CNF-006]** Conflicting actor Confirmations where required.
- ⬜ **[CNF-007]** Retraction/supersession where required.
- ⬜ **[CNF-008]** No Confirmation `!= false/rejected/not-performed`.
- ⬜ **[ACK-002]** Implement Acknowledgement only where real common-ground workflow requires it.
- ⬜ **[ACK-003]** Sent/delivered/read `!= acknowledged`.

## Resolution Queue

- ⬜ **[RES-001]** Actual unknown reason.
- ⬜ **[RES-002]** Outcome required/absent reason.
- ⬜ **[RES-003]** Confirmation required/absent reason.
- ⬜ **[RES-004]** Session anomaly reason.
- ⬜ **[RES-005]** Real `Fatto` mapping.
- ⬜ **[RES-006]** Real `Parziale` mapping.
- ⬜ **[RES-007]** Real `Saltato` mapping.
- ⬜ **[RES-008]** Real `Posticipato` mapping.
- ⬜ **[RES-009]** Real `Sostituito` mapping.
- ⬜ **[RES-010]** `Conferma` mapping.
- ⬜ **[RES-011]** `Correggi` path.
- ⬜ **[RES-012]** Batch/review workflow where activated.
- ⬜ **[RES-013]** Resolution Queue `!= Notification feed/status table`.
- ⬜ **[RES-014]** Atomic multi-effect operation where one UX action needs Actual+Outcome+Confirmation.

## Tests

- ⬜ **[B10-T01]** Unknown vs known non-realization.
- ⬜ **[B10-T02]** Multiple Sessions → one Actual.
- ⬜ **[B10-T03]** Event Actual without Session.
- ⬜ **[B10-T04]** Partial/different realization.
- ⬜ **[B10-T05]** Context-specific Outcome.
- ⬜ **[B10-T06]** Confirmation exact-state/correction.
- ⬜ **[B10-T07]** No-response/unresolved.
- ⬜ **[B10-T08]** Multi-effect transaction atomicity.
- ⬜ **[B10-T09]** Resolution Queue projection.
- ⬜ **[B10-T10]** E2E expected item → resolve → history.
- ⬜ **[B10-T11]** Manual Fatto/Parziale/Saltato/Conferma acceptance.

---

# 15. B11 — Advanced Recurrence / Conditional Policy / reminders ⬜

- ⬜ **[REC-ADV-001]** Dedicated persistence/runtime need for completion-relative recurrence.
- ⬜ **[REC-ADV-002]** Completion-relative qualifying Actual anchor.
- ⬜ **[REC-ADV-003]** Sequential chain/no-future-anchor behavior.
- ⬜ **[REC-ADV-004]** Dedicated persistence/runtime need for anchor-stream-relative recurrence.
- ⬜ **[REC-ADV-005]** Qualifying Session/anchor-stream mapping.
- ⬜ **[REC-ADV-006]** Advanced recurrence `!= generic Trigger/workflow`.
- ⬜ **[POL-001]** Re-open Conditional Policy authority.
- ⬜ **[POL-002]** Transition-based activation.
- ⬜ **[POL-003]** Persistent-state activation where required.
- ⬜ **[POL-004]** Per-new-qualifying-fact activation where required.
- ⬜ **[POL-005]** Semantic dedup/idempotency.
- ⬜ **[POL-006]** Competing policy handling without universal newest-wins.
- ⬜ **[POL-007]** Loop/cycle safeguards.
- ⬜ **[POL-008]** Activation `!= response success`.
- ⬜ **[REM-001]** Immediate review/confirmation policy.
- ⬜ **[REM-002]** Later/end-of-day review policy.
- ⬜ **[REM-003]** Weekly review policy.
- ⬜ **[REM-004]** Silent-unresolved policy.
- ⬜ **[REM-005]** Explicitly authorized bounded automatic Outcome.
- ⬜ **[REM-006]** Automatic effect provenance/no fake human Confirmation.
- ⬜ **[REM-007]** Reminder intent separate from delivery.
- ⬜ **[REM-008]** Shared Email Platform reuse where configured.
- ⬜ **[REM-009]** Durable intent/commit-before-provider-I/O.
- ⬜ **[REM-010]** Ambiguous provider result without blind resend.
- ⬜ **[REM-011]** Notification controls/quiet hours/repetition.
- ⬜ **[B11-T01]** Completion-relative anchor tests.
- ⬜ **[B11-T02]** Anchor-stream duplicate/qualification tests.
- ⬜ **[B11-T03]** Conditional activation-mode tests.
- ⬜ **[B11-T04]** Policy conflict/loop safeguards.
- ⬜ **[B11-T05]** Automatic Outcome provenance tests.
- ⬜ **[B11-T06]** Reminder intent/outbox/provider ambiguity tests.
- ⬜ **[B11-T07]** Daily/weekly review aggregation tests.
- ⬜ **[B11-T08]** Manual review/reminder acceptance.

---

# 16. B12 — Replanning / conflict / solver ⬜

- ⬜ **[RPL-001]** Re-open movement/replanning/solver Physical authority.
- ⬜ **[RPL-002]** Candidate input from canonical current Schedule/constraints.
- ⬜ **[RPL-003]** Hard constraints.
- ⬜ **[RPL-004]** Soft constraints/preferences.
- ⬜ **[RPL-005]** Movement policy.
- ⬜ **[RPL-006]** Relevant hidden Life Area commitments under visibility rules.
- ⬜ **[RPL-007]** Candidate `!= accepted Schedule`.
- ⬜ **[RPL-008]** Explain affected items/trade-offs without hidden-data leakage.
- ⬜ **[RPL-009]** Smallest useful replan scope.
- ⬜ **[RPL-010]** Move fallback.
- ⬜ **[RPL-011]** Postpone fallback.
- ⬜ **[RPL-012]** Skip fallback.
- ⬜ **[RPL-013]** Shorten fallback where valid.
- ⬜ **[RPL-014]** Split fallback where valid.
- ⬜ **[RPL-015]** Replacement preserving original intention/history.
- ⬜ **[RPL-016]** Scope expansion only when required.
- ⬜ **[RPL-017]** This-occurrence vs future-source scope.
- ⬜ **[RPL-018]** Expected-state revalidation before apply.
- ⬜ **[RPL-019]** Solver failure leaves canonical state unchanged.
- ⬜ **[B12-T01]** Hard/soft solver tests.
- ⬜ **[B12-T02]** Candidate-vs-accepted.
- ⬜ **[B12-T03]** Stale candidate conflict.
- ⬜ **[B12-T04]** Minimal scope/fallback.
- ⬜ **[B12-T05]** Hidden-conflict privacy/non-interference.
- ⬜ **[B12-T06]** Manual proposal/explanation/apply acceptance.

---

# 17. B13 — Provider / Offline / Multi-device ⬜

- ⬜ **[EXT-001]** Re-open ExternalRef/provider authority.
- ⬜ **[EXT-002]** Provider Event identity mapping separate from DANTE Event.
- ⬜ **[EXT-003]** Provider recurring-series/instance mapping separate from DANTE Occurrence.
- ⬜ **[EXT-004]** Import/update assertion path.
- ⬜ **[EXT-005]** Provider deletion/tombstone handling.
- ⬜ **[EXT-006]** Provider Schedule `!= accepted DANTE Schedule`.
- ⬜ **[EXT-007]** Detached recurring-instance reconciliation.
- ⬜ **[EXT-008]** Explicit unsupported/lossy recurrence mapping.
- ⬜ **[EXT-009]** Preserve user correction against blind provider overwrite.
- ⬜ **[EXT-010]** Truthful external apply pending/success/failure/ambiguous state.
- ⬜ **[EXT-011]** Imported Session provider/source/device provenance.
- ⬜ **[EXT-012]** Duplicate imported Session reconciliation.
- ⬜ **[SYNC-001]** Activate selected local-sync technology only through Physical gate.
- ⬜ **[SYNC-002]** Local/synced copy remains noncanonical.
- ⬜ **[SYNC-003]** Truthful pending/offline mutation state.
- ⬜ **[SYNC-004]** Reconnect/replay idempotency.
- ⬜ **[SYNC-005]** Expected-state reconciliation after offline period.
- ⬜ **[SYNC-006]** Web/Mobile concurrent Session reconciliation.
- ⬜ **[SYNC-007]** Device clock drift handling.
- ⬜ **[SYNC-008]** No silent last-write-wins.
- ⬜ **[B13-T01]** Provider Event/Occurrence identity tests.
- ⬜ **[B13-T02]** Provider tombstone tests.
- ⬜ **[B13-T03]** Unsupported recurrence mapping tests.
- ⬜ **[B13-T04]** User-correction vs provider-update tests.
- ⬜ **[B13-T05]** Imported Session duplicate/reconciliation tests.
- ⬜ **[B13-T06]** Offline replay/idempotency tests.
- ⬜ **[B13-T07]** Concurrent Web/Mobile Session race tests.
- ⬜ **[B13-T08]** Device clock drift tests.
- ⬜ **[B13-T09]** Provider ambiguous-result tests.
- ⬜ **[B13-T10]** Manual provider/offline acceptance.

---

# 18. B14 — Analytics / Statistics / Signals ⬜

- ⬜ **[ANA-001]** Scheduled-duration metric.
- ⬜ **[ANA-002]** Session elapsed-duration metric.
- ⬜ **[ANA-003]** Session active-duration metric.
- ⬜ **[ANA-004]** Paused-duration metric.
- ⬜ **[ANA-005]** Early/late start against correct Schedule state.
- ⬜ **[ANA-006]** Early/late finish.
- ⬜ **[ANA-007]** Overrun/underrun.
- ⬜ **[ANA-008]** Schedule revision/reschedule statistics.
- ⬜ **[ANA-009]** Postpone/cancel/skip patterns without generic status ontology.
- ⬜ **[ANA-010]** Expected Occurrence counts.
- ⬜ **[ANA-011]** Actual coverage.
- ⬜ **[ANA-012]** Context-specific Outcome distributions.
- ⬜ **[ANA-013]** Confirmation coverage where required.
- ⬜ **[ANA-014]** Time allocation by Life Area.
- ⬜ **[ANA-015]** Tag/context aggregation.
- ⬜ **[ANA-016]** Day/week/month/year trends with correct timezone boundaries.
- ⬜ **[ANA-017]** Routine adherence from Occurrence+Actual+Outcome+Confirmation basis.
- ⬜ **[ANA-018]** Streak only as defined derived metric.
- ⬜ **[ANA-019]** Raw Session sum vs unique wall-clock coverage.
- ⬜ **[ANA-020]** Intentional overlapping multi-domain contribution.
- ⬜ **[ANA-021]** Corrected current accepted truth for ordinary analytics.
- ⬜ **[ANA-022]** Deleted/redacted source cannot survive as hidden undeletable derived copy.
- ⬜ **[ANA-023]** Product analytics `!=` OTel/Grafana observability.
- ⬜ **[ANA-024]** No universal productivity/success/performance score without explicit semantics.
- ⬜ **[B14-T01]** Planned-vs-actual calculations.
- ⬜ **[B14-T02]** Overlap/unique-wall-clock.
- ⬜ **[B14-T03]** Routine adherence.
- ⬜ **[B14-T04]** Corrected-history analytics.
- ⬜ **[B14-T05]** Timezone/DST period boundaries.
- ⬜ **[B14-T06]** Life Area/tag aggregation.
- ⬜ **[B14-T07]** Privacy/deletion/non-interference analytics.
- ⬜ **[B14-T08]** Manual statistics acceptance.

---

# 19. Cross-cutting gates

These remain global gates and therefore are not marked fully green merely because B00–B02 have proven their activated subset.

- 🟨 **[HIST-001]** Owner identity separate from MaterialState. — Proven for Activity/Schedule; must remain true for future mutable facets.
- 🟨 **[HIST-002]** Explicit current accepted state; no latest-row inference. — Proven for Schedule; future facets pending.
- 🟨 **[HIST-003]** Correction/revision preserves lineage. — Proven for Schedule; Session/Actual/etc. pending.
- ⬜ **[HIST-004]** Material change invalidates Confirmation/Acknowledgement applicability where required.
- 🟨 **[PROV-001]** Consequential source/actor/device/provider provenance preserved. — Context/source foundations exist; future provider/session facets pending.
- ✅ **[PROV-002]** Provenance is not treated as truth by itself in activated B00–B02 semantics; this remains a permanent invariant.
- ⬜ **[RECON-001]** Competing assertions can remain unresolved across future Actual/provider flows.
- 🟨 **[AUTH-001]** DanteContext/Account/self-Person boundary respected. — Proven for B00–B02; future operations must inherit it.
- ✅ **[AUTH-002]** Person `!=` Account `!=` Principal `!=` Actor remains preserved by activated temporal APIs/persistence; future relation work cannot collapse it.
- ⬜ **[AUTH-003]** Consequential Authority/Visibility/Consent basis where applicable.
- ⬜ **[PRIV-001]** Safe busy/free projection without leaking hidden details.
- ⬜ **[PRIV-002]** Counts/explanations/analytics respect non-interference.
- ⬜ **[PRIV-003]** Retention/deletion/redaction distinct from semantic correction.
- ⬜ **[PRIV-004]** Derived user-linked data honors deletion/retention.
- 🟨 **[RECOV-001]** New canonical temporal state covered by recovery considerations; whole-vertical proof remains future.
- 🟨 **[RECOV-002]** Anti-resurrection doctrine preserved for B02 MaterialState; future facets pending.
- ⬜ **[RECOV-003]** Future outbox/provider recovery behavior.
- 🟨 **[OBS-001]** Temporal operations instrumented where currently activated; future blocks pending.
- ✅ **[OBS-002]** Observability outage cannot change canonical operation truth as a platform invariant.

## Read-model/global projection gates

- ✅ **[READ-001]** Timeline uses the real normalized backend/application read model in normal runtime.
- ✅ **[READ-002]** Activated Activity/Schedule Timeline projection preserves stable owner/Schedule identity.
- ✅ **[READ-003]** Timeline card `!= DB row/backend DTO` boundary maintained.
- ✅ **[READ-004]** Planning Tray represents unplaced Activity from absence of current accepted placement, not absence of history.
- ⬜ **[READ-005]** Future unified no-placement UI distinguishes postponed Event/flexible Occurrence from unplaced Activity.
- ⬜ **[READ-006]** Resolution Queue from exact unresolved reason.
- ⬜ **[READ-007]** Detail/History future surface.
- ✅ **[READ-008]** Range query supports user-local day semantics for activated Schedule forms.
- ✅ **[READ-009]** Range query supports date-span/all-day semantics.
- ✅ **[READ-010]** Range query supports coarse placement semantics.
- ⬜ **[READ-011]** Paging/cursor/horizon when dataset/window requires it.
- 🟨 **[READ-012]** Current/history/visibility filtering proven for activated B02 path; cancellation/future owners pending.
- ⬜ **[READ-013]** Recurrence materialization output integration.
- ✅ **[READ-014]** DST/local-day handling includes non-24h day semantics for the activated named-zone/range path.
- 🟨 **[READ-015]** Frozen T1 behavior preserved through B02 Chromium/Firefox; must remain green through future integrations.

---

# 20. B15 — Whole-vertical closure ⬜

- ⬜ **[CLOSE-001]** Full master `!=` sweep.
- ⬜ **[CLOSE-002]** No generic Task/Status/done/repeat/due_at/assigned_to shortcuts.
- ⬜ **[CLOSE-003]** No runtime fake Timeline/mock repository.
- ⬜ **[CLOSE-004]** Every live-ledger item green or explicitly scope-amended.
- ⬜ **[CLOSE-005]** Re-run final adversarial scenario set.
- ⬜ **[CLOSE-006]** Full backend suite.
- ⬜ **[CLOSE-007]** Full PostgreSQL acceptance.
- ⬜ **[CLOSE-008]** Full API/integration.
- ⬜ **[CLOSE-009]** Full frontend suite.
- ⬜ **[CLOSE-010]** Full T1/F0/Create regression.
- ⬜ **[CLOSE-011]** Full real-backend E2E.
- ⬜ **[CLOSE-012]** Full timezone/DST.
- ⬜ **[CLOSE-013]** Full idempotency/concurrency.
- ⬜ **[CLOSE-014]** Full recurrence/Occurrence history.
- ⬜ **[CLOSE-015]** Full Session multi-device/offline for activated surfaces.
- ⬜ **[CLOSE-016]** Full privacy/non-interference.
- ⬜ **[CLOSE-017]** Full provider/reconciliation for activated providers.
- ⬜ **[CLOSE-018]** Recovery/PITR anti-resurrection.
- ⬜ **[CLOSE-019]** Timeline/range/review/analytics performance/query-plan review.
- ⬜ **[CLOSE-020]** Alembic/SQLAlchemy/Dictionary/live PostgreSQL alignment.
- ⬜ **[CLOSE-021]** Runtime ACL/owner/migrator/observer proof.
- ⬜ **[CLOSE-022]** Desktop whole-vertical manual acceptance.
- ⬜ **[CLOSE-023]** Mobile/responsive whole-vertical manual acceptance.
- ⬜ **[CLOSE-024]** Accessibility acceptance.
- ⬜ **[CLOSE-025]** Documentation drift audit.
- ⬜ **[CLOSE-026]** Branch closure/integration rules satisfied.
- ⬜ **[CLOSE-027]** Final visual/UI polish after B07/B10 product surfaces have stabilized.

---

# 21. Numbering migration

The B07 UI/UX checkpoint was inserted after B06 on 2026-09-16. Current numbering is authoritative:

```text
old B07 Session Runtime                   → B08
old B08 Responsibility/Participation      → B09
old B09 Actual/Outcome/Confirmation       → B10
old B10 Advanced Recurrence/Conditional   → B11
old B11 Replanning/Solver                 → B12
old B12 Provider/Offline/Multi-device     → B13
old B13 Analytics/Signals                 → B14
old B14 Whole Vertical Closure            → B15
```

Accordingly the not-yet-executed block-prefixed test IDs were renumbered (`B07-T*` old Session → `B08-T*`, etc.). Semantic stable IDs such as `SES-*`, `ACTUAL-*`, `RPL-*`, `EXT-*`, `ANA-*` are unchanged.

Historical files under `docs/workstreams/archive/` preserve the old numbering only as historical evidence and are not current execution authority.

---

# 22. Current execution state

```text
SEMANTIC AUTHORITY / ARCHIVE                    ✅ PRESERVED
CURRENT ROADMAP                                 ✅ RECONCILED 2026-09-16
CURRENT LIVE MAP / LEDGER                       ✅ RECONCILED 2026-09-16
B00 REAL DATA SPINE                             ✅ CLOSED / PROVEN
B01 ACTIVITY CORE                               ✅ CLOSED / PROVEN
B02 SCHEDULE CORE                               ✅ CLOSED / PROVEN
B02 DATABASE / DICTIONARY                       ✅ Alembic _26 reconciled
B02 MANUAL userTest                             ✅ APPROVED 2026-09-15
B02-E Chromium                                  ✅ 2 / 2 PASS
B02-E Firefox                                   ✅ 2 / 2 PASS
B03 EVENT CORE                                  ⬜ NEXT / NOT STARTED
B07 UI/UX CONSOLIDATION v1                      ⬜ scheduled after B06
NEXT EXECUTION GATE                             B03 PRE-SCOPE / authority re-open
```

Nothing in this reconciliation authorizes B03 implementation by itself.