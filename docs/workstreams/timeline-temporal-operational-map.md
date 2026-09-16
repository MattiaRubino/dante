# Timeline / Temporal-Operational Vertical — Semantic Work Map / Live Ledger

- **Status:** CURRENT SEMANTIC MAP + LIVE IMPLEMENTATION LEDGER — reconciled 2026-09-16
- **Branch:** `feature/timeline-temporal-operational`
- **Roadmap:** `docs/workstreams/timeline-temporal-operational-roadmap.md`
- **B02 closure:** `docs/workstreams/timeline-temporal-operational-b02-closure-2026-09-16.md`
- **B03 execution plan:** `docs/workstreams/timeline-temporal-operational-b03-execution-plan.md`
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
B03 Event Core                                   🟨 PRE-SCOPE COMPLETE / IMPLEMENTATION PENDING
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

# 7. B03 — Event Core 🟨 PRE-SCOPE COMPLETE / IMPLEMENTATION PENDING

- ✅ **[EVT-001]** Re-open Event Domain/Logical/Physical authority before implementation. — Deep-read completed 2026-09-16 across Event Domain, Whole Logical, CP6/Alembic `_26`, SQLAlchemy, Dictionary, backend B01/B02 seams, frontend Create/Timeline and test harness. Frozen in `timeline-temporal-operational-b03-execution-plan.md`.
- ⬜ **[EVT-002]** Resolve minimum meaningful Event descriptive persistence. — PRE-SCOPE identifies a real gap and recommends typed `event_expectation`; implementation proof/DDL still pending.
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

## 7.1 PRE-SCOPE findings

```text
Event NativeRef / EventRow                          EXISTS
Schedule physical Event eligibility                EXISTS
shared Schedule MaterialState/current/history      EXISTS / B02 PROVEN
Event typed expectation descriptor                 MISSING
Event idempotent create receipt/capability         MISSING
B02 Schedule runtime self-scope                    ACTIVITY-DESCRIPTOR BOUND
Timeline backend/API                               ACTIVITY-ONLY
frontend Timeline protocol                         ACTIVITY-ONLY
frontend Event authoring prototype                 EXISTS
normal-runtime Event create                        FAIL-CLOSED BY DESIGN
Event Agenda canonical persistence                 MISSING
```

No `event_schedule` table/engine is authorized. B03 must boundedly generalize the one Schedule capability to typed Activity/Event ownership.

Rich prototype fields remain fail-closed when owned by later blocks: recurrence B06, constraints B04, product organization B05, Session B08, Participation B09, Actual/Outcome/Confirmation B10, reminder policy B11, provider/conference integration B13.

## 7.2 Planned implementation slices

```text
B03-A  Event canonical core
       typed Event expectation + create operation/capability + ownership

B03-B  Shared Schedule + Event Timeline
       typed Activity/Event self-scope + atomic scheduled Event + timed/all-day/multi-day

B03-C  Event placement lifecycle
       reschedule + postponed/TBD + Event read/detail + guarded Undo

B03-D  Agenda/internal parts
       bounded ordered Event-internal persistence + real frontend integration

B03-E  closure
       PG/API/frontend/E2E/manual + DB/Dictionary/docs reconciliation
```

Next gate is explicit `APPROVE B03-A`. PRE-SCOPE completion does not authorize implementation by itself.

---

# 8. B04 — Temporal Constraints / movement policy ⬜

The detailed B04 checklist remains unchanged and binding in the previous live-map revision and archived semantic map. No B04 capability is activated by B03 PRE-SCOPE.

---

# 9. B05 — Life Area / Calendar / Tags ⬜

The detailed B05 checklist remains unchanged and binding in the previous live-map revision and archived semantic map. No B05 capability is activated by B03 PRE-SCOPE.

---

# 10. B06 — Routine / Recurrence / Occurrence baseline ⬜

The detailed B06 checklist remains unchanged and binding in the previous live-map revision and archived semantic map. In particular Event recurrence remains B06-owned; B03 must not materialize canonical recurring Event Occurrences.

---

# 11. B07 — UI/UX Consolidation v1 ⬜

The explicit 60–70% product-quality checkpoint remains scheduled after B06. B03 may fix usability blockers but must not allow temporary UI shape to dictate persistence/domain semantics.

Stable checklist family remains `UIX-001 … UIX-017` and `B07-T01 … B07-T07` as frozen in the prior live-map revision.

---

# 12. B08 — Session Runtime ⬜

Stable checklist family remains `SES-001 … SES-027` and `B08-T01 … B08-T11`. Event attendance remains distinct from Session.

---

# 13. B09 — Responsibility / Participation / actor relations ⬜

Stable checklist families remain `REL-*`, `PAR-*`, `ACK-001`, and `B09-T*`. B03 does not activate participants/invitations merely because the prototype Event form displays them.

---

# 14. B10 — Actual / Outcome / Confirmation / Resolution ⬜

Stable checklist families remain `ACTUAL-*`, `OUT-*`, `CNF-*`, `ACK-002/003`, `RES-*`, and `B10-T*`. B03 does not create Actual/Outcome/Confirmation from Event passage or Schedule state.

---

# 15. B11 — Advanced Recurrence / Conditional Policy / reminders ⬜

Stable checklist families remain `REC-ADV-*`, `POL-*`, `REM-*`, and `B11-T*`. Event reminder/confirmation prototype fields stay fail-closed in B03.

---

# 16. B12 — Replanning / conflict / solver ⬜

Stable checklist families remain `RPL-*` and `B12-T*`. No solver/replanning candidate becomes accepted Event Schedule without the later governed block.

---

# 17. B13 — Provider / Offline / Multi-device ⬜

Stable checklist families remain `EXT-*`, `SYNC-*`, and `B13-T*`. Event provider identity/conference execution is explicitly deferred.

---

# 18. B14 — Analytics / Statistics / Signals ⬜

Stable checklist families remain `ANA-*` and `B14-T*`. No analytics shortcut is introduced in B03.

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

The full `CLOSE-001 … CLOSE-027` checklist remains unchanged and binding from the preceding live-map revision. B03 PRE-SCOPE does not promote any final closure gate.

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

Semantic stable IDs remain unchanged. Historical files under `docs/workstreams/archive/` preserve old numbering only as historical evidence.

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
B03 EVENT CORE PRE-SCOPE                        ✅ COMPLETE
B03 EVENT CORE IMPLEMENTATION                   ⬜ NOT AUTHORIZED YET
B03 EVT-001 AUTHORITY RE-OPEN                   ✅ DONE
B03 EVT-002+ / B03-T*                           ⬜ PENDING IMPLEMENTATION/PROOF
B07 UI/UX CONSOLIDATION v1                      ⬜ scheduled after B06
NEXT EXECUTION GATE                             APPROVE B03-A
```

No B03 product code, API mutation or DDL is authorized by PRE-SCOPE completion alone.