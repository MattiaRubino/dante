# Timeline / Temporal-Operational — B02 Schedule Core Execution Plan

- **Status:** ACTIVE EXECUTION CONTRACT / B02-A through B02-E1 proven; B02-E2 next
- **Date:** 2026-09-14
- **Branch:** `feature/timeline-temporal-operational`
- **B02-D pre-scope branch head:** `0fa9f0a6c04ba86a466dc113f76aea0d438f8c06`
- **Roadmap block:** B02 — Schedule Core
- **Primary semantic authority:** `docs/workstreams/timeline-temporal-operational-map.md`
- **Roadmap:** `docs/workstreams/timeline-temporal-operational-roadmap.md`
- **Final precision audit:** `docs/workstreams/timeline-temporal-operational-final-pre-roadmap-audit-2026-09-07.md`
- **Purpose:** bind the current CP6/B01 repository truth into an implementation-ready Schedule plan before any B02 product/schema write.
- **Important:** this document authorizes no product code, API, DDL, frontend mutation or B03+ implementation by itself. Each implementation slice still requires its own reviewed PRE-SCOPE gate.

---

# 0. Binding objective

B02 is not a green-field Schedule design.

The accepted repository already contains the structural PostgreSQL Schedule model created during CP6. B02 must activate that model through real application/API/frontend operations without creating a competing Schedule ontology or weakening existing MaterialState/current-history semantics.

The binding implementation direction is therefore:

```text
existing CP6 Schedule owner
+
existing CP6 placement MaterialState/current/history machinery
+
B01 canonical Activity identity
+
new bounded B02 application operations/read models
=
first real accepted Activity scheduling loop
```

The following remain permanent:

```text
Activity != Schedule
Schedule != Temporal Constraint
Schedule != Session
Schedule != Actual
Schedule != proposal
scheduled != happened
estimated effort != scheduled duration
current accepted placement != newest row
no current placement != no Schedule history
Undo != history rewind
```

No implementation convenience may replace those boundaries.

---

# 1. Authority re-open result

B02 authority was re-opened before implementation against current branch truth, including:

- the frozen temporal semantic map and B02 ledger;
- the final pre-roadmap audit and its FA-03 coarse-placement correction;
- the accepted PostgreSQL/CP6 Schedule owner and placement structures;
- current SQLAlchemy mappings for Schedule and bounded current views;
- current Database Dictionary objects for Schedule/current/history/material-state addressing;
- B01 Activity persistence/application/API behavior;
- the current Timeline backend/frontend read spine;
- frozen F0/T1 interaction semantics that B02 must preserve.

## 1.1 Candidate database baseline

At B00/B01 closure the candidate database baseline is:

```text
PostgreSQL       18.6
Alembic head     20260908_19
Topology         91|5|19|77|177|95|275|0|0|0
```

`20260908_19` adds B01 Activity descriptive/idempotent-create support. It does not replace the older CP6 Schedule structures.

## 1.2 Existing Schedule owner

Current CP6 truth already has canonical `dante.schedule` with:

```text
schedule_ref       ScopedRecordRef / UUIDv7
subject_native_ref NativeRef
```

The Schedule subject family is bounded to schedulable native owners and must remain:

```text
Activity
Event
Occurrence
```

B02 activates the Activity path first. It must not broaden subject eligibility to Routine, Session, Actual, arbitrary native owners or generic entities.

## 1.3 Existing placement MaterialState family

Current CP6 truth already provides:

- `dante.schedule_placement_state` as the Schedule placement MaterialState envelope;
- typed payload families for:
  - `date_span`;
  - `floating_local`;
  - `named_zone_local`;
  - `absolute`;
- `dante.material_state_address` for immutable MaterialStateRef addressing;
- `dante.scoped_current_material_state` for explicit current binding;
- `dante.schedule_current_placement` as the bounded current-placement capability view;
- `dante.schedule_placement_current_history` as durable currentness chronology;
- database-local totality/current-history/binding validators.

Therefore B02 must consume those objects rather than create parallel tables such as:

```text
activity_schedule
current_activity_time
activity_due_at
activity_start_end
activity_status
```

## 1.4 Existing current-binding semantics

The current Schedule placement is explicit.

It is not inferred from:

- latest insert;
- highest UUID;
- latest timestamp;
- provider-most-recent value;
- frontend revision number.

A revision creates a new accepted MaterialState and moves the explicit current binding while retaining history.

## 1.5 Existing retirement/history semantics

Material-state payload retirement does not manufacture historical non-existence.

Schedule placement history and MaterialStateRef continuity remain separate from protected payload lifecycle. B02 must not use delete-and-recreate as ordinary reschedule behavior.

---

# 2. Current B01/B00 integration truth

## 2.1 Activity

B01 now provides one canonical Activity identity with bounded descriptive intention state and governed idempotent create semantics.

The Activity is not a Schedule row and does not contain placement columns.

## 2.2 Planning Tray semantic defect that becomes active in B02

Current B01 `list_unplaced()` is intentionally sufficient only while no Schedule lifecycle exists. It currently means approximately:

```text
Activity has no Schedule row at all
```

That becomes wrong as soon as B02 supports unschedule/history.

B02 must redefine the read criterion as:

```text
unplaced Activity
=
Activity has no current accepted Schedule placement
```

not:

```text
Activity never had a Schedule
```

An Activity that was scheduled, then explicitly unscheduled, must be able to return to the Planning Tray while its prior Schedule/history remains reconstructible.

## 2.3 Timeline

B00 established a truthful authenticated Timeline backend path, but its current transport/read model is intentionally empty-only.

B02 must introduce the first normalized real scheduled-Activity Timeline projection.

The target architecture remains:

```text
canonical Activity + current Schedule placement
→ temporal application query
→ normalized Timeline read model
→ frontend temporal data source
→ frozen T1 rendering/interactions
```

The Timeline card remains a projection, not a canonical Schedule/Activity row.

## 2.4 Frozen frontend interaction contract

B02 is backend integration of already-frozen interaction semantics, not permission to redesign Timeline behavior.

The protected T1 behavior includes, among other things:

- custom drag;
- deterministic focus grammar;
- move + guarded Undo;
- anchored time editor;
- compact overlap behavior;
- Firefox pointer/focus regression contract.

These interactions must progressively call real governed B02 operations while preserving their UX contract.

---

# 3. Verified reuse versus real B02 gaps

## 3.1 Reuse — do not redesign

B02 SHALL reuse:

1. canonical `Schedule` identity and subject relation;
2. existing `schedule.placement` MaterialState addressing;
3. existing typed placement payload tables;
4. explicit current placement binding;
5. currentness history;
6. existing database-local integrity validators;
7. B01 Activity identity/self-Person scope;
8. B00 temporal authenticated read spine;
9. F0 idempotency/expected-state/Undo semantics as application behavior;
10. T1 Timeline interaction behavior.

## 3.2 Proven implementation gaps

The deep read identifies these real gaps rather than a missing Schedule ontology:

### GAP-B02-01 — governed Schedule operation boundary

There is no current product-level B02 application/API operation that creates/revises/unschedules an accepted Schedule for Activity.

### GAP-B02-02 — mutation idempotency receipt

B01 has a dedicated idempotent Activity-create receipt/routine. Schedule mutations do not yet have the equivalent product operation receipt semantics required by B02.

The exact physical implementation must be proven in the code slice. The operation identity must not become Schedule identity or MaterialState identity.

### GAP-B02-03 — expected-state concurrency

Real Schedule mutations must reject/reconcile a stale current placement basis. Existing DB current/history integrity does not by itself define the product command's expected-state conflict contract.

### GAP-B02-04 — Planning Tray current-placement semantics

`list_unplaced()` must stop equating `no Schedule ever` with `no current accepted placement`.

### GAP-B02-05 — Timeline scheduled-item read model

The current B00 Timeline endpoint/TypeScript datasource exposes only a truthful empty window. B02 needs a normalized scheduled Activity projection over current accepted placement.

### GAP-B02-06 — coarse accepted placement precision

The semantic authority explicitly accepts states such as:

```text
Tuesday afternoon
```

and requires:

```text
coarse accepted placement
!= exact timed block
!= all-day/date span automatically
!= unplaced
```

Current CP6 placement payload families do not, by themselves, prove a dedicated representation for every coarse product precision.

B02 must not manufacture exact timestamps such as `14:00-18:00` merely because the current UI renderer prefers an interval.

The exact physical representation is a blocking design/proof point for the later B02 form-completeness slice. If current accepted Logical/Physical authority cannot represent the required precision losslessly, a narrow forward physical extension must be separately gated.

### GAP-B02-07 — frontend real-operation integration

Planning Tray placement, Timeline drag, anchored time edit and Undo are not yet bound to a canonical Schedule backend operation.

---

# 4. B02 operation semantics

B02 operations are semantic effects over Schedule/current placement, not generic CRUD/status writes.

Names below describe operation families; exact API route/function names are fixed only in the implementation slice after code inspection.

## 4.1 Establish accepted Schedule

Conceptual command:

```text
EstablishActivitySchedule
```

Inputs must include enough bounded information to establish:

- target Activity identity;
- new Schedule identity where this is a new Schedule owner;
- exact placement temporal form/payload;
- operation identity/idempotency fingerprint;
- authenticated self-Person/DanteContext scope;
- acceptance/source context required by the activated product path.

Effect:

```text
same Activity identity
+
one Schedule owner
+
placement MaterialState
+
explicit current binding
+
open current-history episode
```

No duplicate Activity is created.

## 4.2 Revise accepted placement

Conceptual command:

```text
ReviseSchedulePlacement
```

Required semantics:

- target existing Schedule;
- exact expected current placement MaterialState/revision basis;
- new placement MaterialState;
- same Schedule identity;
- previous current-history episode closed;
- new current-history episode opened;
- explicit current binding moved;
- operation idempotency preserved.

A revision must not overwrite the old placement payload in place merely to simplify querying.

## 4.3 Unschedule

Conceptual command:

```text
UnscheduleActivity
```

Effect:

- same Activity identity remains;
- prior Schedule/history remains reconstructible;
- no current accepted placement remains for the applicable subject state;
- Activity becomes eligible for the Planning Tray projection again where no other current accepted placement applies.

`unschedule` is not:

- delete Activity;
- cancel Activity;
- delete all Schedule history;
- create a fake all-day placeholder;
- establish Actual non-realization.

## 4.4 Guarded Undo

Undo reverses a recent supported Schedule mutation only when the current state still matches the exact state produced by that mutation.

Required behavior:

```text
original operation
→ current placement S2

Undo with expected current S2
→ new monotonic accepted state/effect
→ prior semantic placement restored as current where valid
→ history retained
```

If newer truth exists:

```text
Undo expected S2
current = S3
→ conflict/rejected
→ no blind overwrite
```

Undo must never rewind MaterialState/current-history chronology or technical revision counters.

## 4.5 No-op

A semantically equivalent requested placement may resolve to an explicit no-op rather than manufacturing a redundant material revision, provided the equality/materiality rule is exact and tested.

Idempotent replay and semantic no-op remain distinguishable concepts even if both produce no second mutation.

---

# 5. Idempotency and concurrency contract

## 5.1 Operation identity

B02 mutation operation identity SHALL be separate from:

```text
Activity NativeRef
Schedule ScopedRecordRef
MaterialStateRef
HTTP request id
frontend component id
```

Same operation identity + same material command intent may replay safely.

Same operation identity + materially different command intent must conflict/reject.

## 5.2 Expected state

Consequential revisions/unschedule/Undo must bind to an expected current accepted placement state.

The preferred canonical basis is the relevant current MaterialStateRef/current binding semantics rather than an invented independent version counter unless implementation evidence proves a separate projection revision is required.

The implementation slice must show how transport-level expected revision maps losslessly to canonical state.

## 5.3 Serialization

Concurrency protection may use application transaction ownership plus bounded database locking/advisory serialization where justified.

It must not rely on:

- frontend-only mutexes;
- last-write-wins;
- timestamp ordering;
- newest UUID;
- provider ordering.

## 5.4 Transaction outcome

A user-visible successful placement/revision must not be reported before all canonical effects required for that operation are committed.

For the first local PostgreSQL-only B02 path:

```text
operation receipt/current state/history/payload
```

must not end in a product-visible partial-success state.

External provider application remains a later boundary and is not part of B02 local acceptance.

---

# 6. Persistence strategy

## 6.1 Do not mutate historical CP6 migrations

B02 must use forward migration only if a real new persistence gap is proven.

Do not rewrite:

- `20260825_02_cp6_scoped_material_control.py`;
- `20260825_03_cp6_schedule_actual_session.py`;
- `20260825_05_cp6_core_integrity_current_views.py`;
- later accepted recovery hardening.

## 6.2 Existing rows that an accepted Schedule operation must coordinate

The concrete implementation is expected to coordinate the existing owner/state/control families, including as applicable:

```text
scoped_address
schedule
material_state_address
schedule_placement_state
one typed schedule placement payload
schedule_current_placement / scoped_current_material_state
schedule_placement_current_history
```

The exact insert/update order must respect current deferred/nondeferred integrity contracts and current runtime ACLs.

## 6.3 Forward DDL gate

A future `_20` is justified only for a proven B02 gap such as:

- bounded idempotency/operation receipt state;
- a required lossless coarse-placement physical representation not expressible by accepted current structures;
- another exact integrity/runtime capability demonstrated by current authority/code inspection.

A `_20` must not introduce generic `status`, `due_at`, `repeat`, generic JSON relation or a competing Schedule table.

## 6.4 Runtime ACL rule

Any new mutation route must use the narrowest existing or newly justified capability surface.

Do not grant broad direct runtime UPDATE/DELETE merely to make application code easier.

---

# 7. Planning Tray semantics after B02

The Planning Tray query becomes a projection over current accepted placement, not historical existence.

The required conceptual predicate is:

```text
Activity belongs to authenticated self Person
AND
there is no applicable current accepted Schedule placement for it
```

Historical Schedule rows do not exclude an Activity from the Tray after unschedule.

If later semantics permit several simultaneous planned placements for one subject, the Tray criterion must remain based on the presence/absence of applicable current accepted placement rather than `COUNT(schedule)=0`.

This slice must preserve:

```text
unplaced Activity
!= postponed Event
!= flexible Occurrence awaiting exact placement
```

Only Activity is activated in B02.

---

# 8. Timeline read-model contract

## 8.1 First B02 projection

The first scheduled Activity Timeline item must derive from:

- canonical Activity identity/descriptive state;
- Schedule identity;
- explicit current accepted placement;
- exact typed placement payload;
- authenticated self-Person scope;
- requested bounded Timeline window/effective timezone.

The frontend normalized item needs stable owner identity and enough temporal form information to render correctly without becoming the canonical DTO.

## 8.2 Query window

The existing authenticated half-open local-date window remains the starting query contract.

B02 must make scheduled Activity inclusion correct for the activated placement forms and must not assume every local day is exactly 24 elapsed hours.

## 8.3 Current versus history

Ordinary Timeline current view renders current accepted placement.

Schedule history remains available for future/detail/history operations and test proof; historical placements must not render as duplicate current cards.

## 8.4 Truthful failures

If Timeline/Schedule canonical reads fail:

- no fake card is introduced;
- no previous optimistic local card is silently reclassified as canonical success;
- retry/refetch must return server truth.

---

# 9. Coarse placement resolution gate

Coarse accepted precision is a deliberate B02 design stop, not something to solve with fake timestamps.

Before `SCH-007` may become green, the implementation must answer with accepted authority/evidence:

1. What exact logical/product state distinguishes `Tuesday afternoon` from date-only and exact time?
2. Can current CP6 placement structures encode it losslessly?
3. If not, what is the narrowest forward representation that preserves the accepted semantic precision?
4. How is it queried in a local-date range?
5. How is it rendered without claiming false exactness?
6. How does moving/editing it change precision intentionally rather than accidentally?
7. How does provider export degrade or reject it later without weakening DANTE semantics?

Until this is resolved, B02 may activate an exact subset of already-lossless Schedule forms, but may not mark form-completeness or coarse-placement requirements done.

---

# 10. B02 implementation slices

B02 is intentionally split into evidence-sized slices. A slice may be further narrowed if inspection reveals a larger-than-expected persistence or frontend boundary.

## B02-A — first canonical scheduled Activity loop

Goal:

```text
Create Activity with supported exact placement
→ canonical Activity + Schedule/current placement
→ real Timeline item
→ reload preserves one identity/item
```

Expected work classes:

- first governed accepted-Schedule operation;
- minimum required operation receipt/idempotency support;
- Activity+Schedule atomic authoring path where the Create surface supplies an accepted supported placement;
- first real scheduled-Activity backend Timeline read model;
- frontend remote datasource normalization;
- exact initial placement form(s) proven by current physical representation;
- backend/PostgreSQL/frontend/E2E proof.

B02-A must not claim all Schedule forms complete unless they are actually activated and tested.

## B02-B — Planning Tray → Timeline

Goal:

```text
existing unplaced Activity
→ user places it
→ same Activity identity acquires accepted Schedule
→ leaves Planning Tray
→ appears once in Timeline
```

Required correction:

- replace B01 `no Schedule row ever` unplaced logic with current accepted placement semantics.

Placement duration, when explicitly authored, is Schedule placement data. It is not inferred from Activity estimated effort.

## B02-C — revision through drag/time editor/duration adjustment

Goal:

```text
real Timeline interaction
→ governed Schedule revision
→ old placement retained in history
→ new explicit current placement
→ stale basis rejected
→ reload shows current truth once
```

Includes activated supported operations for:

- move earlier/later;
- anchored time editor;
- duration/start/end adjustment where represented losslessly.

Reality semantics remain out of scope:

```text
dragging Schedule != recording Actual
```

## B02-D — unschedule and guarded Undo

Goal:

```text
scheduled Activity
→ unschedule
→ no current placement
→ same Activity returns to Planning Tray
→ history remains
→ guarded Undo may restore previous accepted placement through a new monotonic state/effect
```

Newer truth must cause Undo conflict instead of overwrite.

Implemented candidate contract:

- unschedule accepts the stable ScheduleRef plus exact current placement MaterialStateRef;
- the database closes the open placement-history episode and deletes only the explicit current binding;
- Activity, Schedule, placement state, payload and history are retained; absence is represented by no current binding, never by a fake MaterialState;
- Undo accepts the exact unschedule receipt, requires continued absence and rejects any later placement-history episode;
- successful Undo copies the retained floating-local interval into a newly issued MaterialStateRef and opens a new current-history episode;
- operation identity is idempotent only for the same normalized material intent;
- Timeline removal/restoration occurs only after one authoritative reload; stale/conflict failures leave the displayed canonical state unchanged;
- unschedule/Undo invalidates the Planning Tray read so the same Activity identity returns or leaves after canonical refresh.

## B02-E — form completeness / precision / DST / closure

Goal:

- prove/activate date-span semantics;
- prove/activate floating-local semantics;
- prove/activate named-zone semantics;
- prove/activate absolute semantics;
- resolve coarse accepted placement losslessly;
- verify local-day/DST behavior;
- run B02 full regression/E2E/manual acceptance;
- reconcile Dictionary/docs/live PostgreSQL where DDL changed;
- close all B02 ledger entries only with executed evidence.

---

# 11. Test obligations

B02 closure requires the roadmap's tests at minimum:

```text
B02-T01 Schedule form/validator tests
B02-T02 current/history direct PostgreSQL tests
B02-T03 reschedule/unschedule/Undo application tests
B02-T04 stale revision/idempotency conflict tests
B02-T05 DST/local-day tests for exposed forms
B02-T06 Timeline drag/time-editor/Planning Tray frontend regressions
B02-T07 Firefox T1 critical interaction regressions
B02-T08 real E2E create→place→move→unschedule/reload/history
B02-T09 manual userTest Schedule/Undo/conflict acceptance
```

Additional required proof discovered by the deep read:

- `list_unplaced()` regression after prior Schedule history;
- one canonical Activity projected exactly once after reload/refetch;
- no historical placement duplicates in current Timeline;
- same operation id + same intent replay;
- same operation id + different intent conflict;
- stale current placement conflict;
- no current placement after unschedule while history remains;
- no fake exact timestamp for coarse intent;
- Activity estimated effort never silently becomes scheduled duration;
- failure/retry never creates fake canonical Timeline state.

---

# 12. Manual `userTest` result

The manual protocol was executed on 2026-09-15 against the isolated synthetic full stack. The user explicitly approved the result:

~~~text
B02 userTest — APPROVED
A/B/C/D/E/F — PASS
~~~

The evidence covers only the supported same-day `floating_local` Activity Schedule slice. It does not activate date-span, named-zone, absolute, coarse-precision, DST, Event/Occurrence or B02-E form-completeness behavior.


# 13. Explicitly out of scope for B02

Unless a later separately approved B02 scope amendment proves otherwise, B02 does not implement:

- Event Core;
- Routine;
- Recurrence generation;
- Occurrence generation;
- Temporal Constraint persistence;
- Session runtime;
- Actual;
- Outcome;
- Confirmation/Acknowledgement;
- Life Area/Calendar persistence;
- solver/replanning engine;
- provider writes/import reconciliation;
- offline/multi-device sync;
- product analytics;
- generic completion/done state;
- Access/Auth idle-activity repair discovered during B00/B01 manual testing.

B02 may preserve interfaces/semantic boundaries needed by those later blocks; it must not silently implement them through shortcuts.

---

# 14. Stop conditions

Stop and re-gate rather than improvise if implementation inspection reveals any of the following:

1. current CP6 Schedule structures cannot represent the intended activated operation losslessly;
2. current runtime ACLs force broad privileges instead of a bounded capability;
3. creating/revising one Schedule cannot satisfy current deferred integrity invariants transactionally;
4. coarse placement requires a new logical/physical decision beyond the already accepted semantic requirement;
5. one subject/current-placement assumption would accidentally erase accepted 0..N Schedule cardinality;
6. frontend integration would require changing frozen T1 behavior rather than adapting data/operations;
7. expected-state semantics cannot map to canonical MaterialState/current binding without inventing a conflicting revision model;
8. a proposed shortcut collapses Schedule with Activity/Session/Actual/Constraint;
9. protected/main or branch authority changes underneath the reviewed scope.

---

# 15. Ledger activation result

Current reconciled implementation state:

~~~text
B02 block                  🟨 IN PROGRESS
SCH-001 authority reopen   ✅ DONE
B02-A candidate            ✅ PROVEN — automated + manual evidence
B02-B candidate            ✅ PROVEN — automated + manual evidence
B02-C candidate            ✅ PROVEN — automated + manual evidence
B02-D candidate            ✅ PROVEN — automated + manual evidence
B02-E exact PRE-SCOPE      ✅ APPROVED — 2026-09-15
B02-E1 placement union     ✅ PROVEN — unit/value + real PostgreSQL evidence
~~~

B02-A through B02-D are proven only for the supported same-day floating-local Activity path. Evidence includes targeted PostgreSQL proof (2 passed), application/frontend regressions, the isolated real browser A-F acceptance and the fixed viewport Undo toast behavior.

B02-E PRE-SCOPE was explicitly approved. B02-E1 activates the five-form backend placement union, lossless coarse local-period payload, form-generic establish/revise/Undo, and preserved 0..N Schedule cardinality. Evidence passed locally (`29 passed`) and on real PostgreSQL (`4 passed, 2 deselected in 9.66s`). Timeline consumption/DST, web behavior and final closure remain open. CI remains deferred by the user’s instruction.

Next required execution gate:

~~~text
B02-E2 Timeline read projection and DST
→ discriminated current placements + form-specific half-open window evidence
~~~
