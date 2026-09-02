# DANTE — Temporal Create C1 Traceability

**Status:** FINAL AUTOMATED TRACEABILITY — MANUAL ACCEPTANCE PENDING  
**Date:** 2026-09-02  
**Branch:** `feature/home-timeline`  
**Implementation candidate:** `81808814abb4e4998c7bde5b0c6cb8f5f903aa62`  
**Frontend CI:** `33613239926` / #536 — FULL PASS  
**Scope:** complete pre-backend Timeline Temporal Create C1

## 1. Purpose

This file is the closure-grade traceability record for C1. It connects the implemented frontend Create capability to the product evidence, closed semantic models, CP6 materialized database, Alembic families, frontend application boundary, UI surfaces and automated proof.

It is deliberately not a claim that browser fields are database rows. The permanent boundary remains:

```text
Product intent
→ Domain owner/invariant
→ Logical representation
→ Physical/CP6 mechanism
→ frontend application model
→ UI projection/authoring surface
→ future backend/provider adapter
```

and never:

```text
UI field == DB column
```

## 2. Source authority used

Primary authorities consumed for this traceability:

- `docs/product/product-identity-and-north-star.md`
- `docs/product/v1-scheduling-flexibility.md`
- `docs/product/v1-execution-status.md`
- `docs/product/v1-confirmation-and-reminders.md`
- `docs/product/feature-discovery-simulation-2026-08.md`
- `docs/product/multi-actor-collaboration-discovery-simulation-2026-08.md`
- `docs/domain/README.md` and accepted Domain Atlas/Language Map
- `docs/logical-model/README.md` and Whole Logical closure
- `docs/physical-model/README.md` and accepted Physical Model
- `docs/database/README.md` and current Database Dictionary/reference
- `apps/backend/migrations/versions/20260825_03_cp6_schedule_actual_session.py`
- `apps/backend/migrations/versions/20260825_04_cp6_recurrence.py`
- `apps/backend/migrations/versions/20260826_06_cp6_occurrence_generation.py`
- `apps/backend/migrations/versions/20260826_07_cp6_runtime_acl_activation.py`
- `apps/backend/migrations/versions/20260826_08_cp6_final_qa_hardening.py`
- `docs/frontend/home/temporal-f0-contract.md`
- `docs/frontend/home/timeline-t1-frozen-contract.md`
- `docs/frontend/home/temporal-create-c1-scope-amendment.md`
- code under `apps/web/src/features/temporal-create/`
- `apps/web/src/features/home/ui/timeline/timeline-create-bridge.tsx`
- `apps/web/e2e/temporal-create.spec.ts`

Current database baseline used here is the materialized CP6 system of record: PostgreSQL 18.6, Alembic head `20260826_08`, 68 DANTE tables, 5 ordinary views, 14 routines, 75 trigger attachments, 95 physical indexes, 68 foreign keys and 120 CHECK constraints.

## 3. Ownership and non-collapse matrix

| C1 capability | Product / simulation requirement | Domain / Logical invariant | Physical / CP6 evidence | Frontend representation | UI / seam | Automated evidence | Disposition |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Activity vs Event | Simple appointment may remain simple; action/planning and event semantics must not collapse | `Activity` and `Event` are separate LR-01 native owners | Separate owner tables/families; recurrence M4 has an Event owner family, not an Activity family | `TemporalCreateKind = activity | event`; normalization is kind-aware | Type control with distinct Activity/Event sections | session, enterprise and E2E suites | **Implemented** |
| Activity repetition | Repeated work needs durable routine semantics, not a convenience boolean | Routine is a native owner; Activity is not a recurrence owner | M4 calls `_create_recurrence_family` exactly for `routine` and `event` | Activity normalization forces `eventRecurrence.patternKind = none` | Activity shows truthful Routine handoff; no recurrence editor | seed, handoff, boundary, session and E2E tests | **Implemented / owner-correct** |
| Event recurrence | Repeated calendar events need recurrence source semantics | recurrence source != generated Occurrence | `event_recurrence_*` M4 family | `TemporalCreateEventRecurrenceIntent` | Event recurrence editor | model/runtime/enterprise/E2E | **Implemented** |
| Generated Occurrence | A recurrence specification must not fabricate concrete occurrence truth in the browser | Occurrence is a distinct LR-01 owner | M6 owns `occurrence_generation*`, `governing_recurrence_state_ref`, `recurrence_generated` vs `explicit_extra` | Create stores recurrence specification only | UI explicitly states backend evaluator/generation is not simulated | enterprise/runtime/E2E assertions | **Deferred to backend by design** |
| Schedule vs Session vs Actual | Planned time does not prove execution or outcome | Schedule != Session != Actual; absence != false | CP6 M3 materializes separate Schedule/Actual/Session families | placement, execution intent and confirmation intent remain distinct structures | Create authors planning policy without Session/Actual creation | F0 + Create unit/E2E | **Implemented distinction** |
| Planned vs happened | DANTE must represent reality rather than force it to match plan | planned != actual; Observation != Actual | separate current/material-state families downstream | no Create success fabricates Actual | outcome policy is configuration only | confirmation/runtime tests | **Implemented distinction** |
| Inferred outcome | Product allows provisional inference but not false certainty | provenance/confirmation != outcome | backend provenance/Actual boundary remains external | `infer-provisional` is a policy value, not Actual | copy says inferred result remains provisional/non-authoritative | E2E + i18n coverage | **Implemented seam** |

## 4. Temporal placement traceability

| C1 form | Semantic meaning | F0/application representation | Backend/physical relation | C1 behavior |
| --- | --- | --- | --- | --- |
| Timed floating | local wall-clock intent without named-zone binding | `floating-local` placement | compatible with CP6 local/date temporal payloads | accepted local deterministic projection |
| Timed zoned | local civil time bound to IANA zone | `zoned` placement | named-zone semantics remain distinct from instant/provider revision | DST-aware duration/end arithmetic uses real Instants |
| Absolute | exact Instant representation | F0 supports `absolute` | CP6 recurrence boundaries/calendar frames support absolute forms | **not exposed as manual C1 control**; reserved for adapter/import/interop |
| All-day | date span, not midnight timed hack | `date-span`, exclusive end | date semantics remain first-class | multi-day Event supported and validated |
| Unscheduled Activity | valid planning intent with no accepted exact placement | placement `null` plus structured scheduling intent | future Schedule persistence/solver boundary | no fake Timeline card at an arbitrary time |
| Event unscheduled | semantically invalid for current Event Create grammar | normalized/rejected away | Event remains time-centred | UI cannot silently create an unscheduled Event |

C1 intentionally does not expose every substrate representation merely because F0 or PostgreSQL can encode it. The UI exposes the representations justified by the current manual authoring contract; richer interop remains available at adapter level.

## 5. Activity scheduling and execution traceability

Product source `v1-scheduling-flexibility.md` explicitly rejects a single fixed/flexible flag. C1 therefore supports structured Activity intent for:

- fixed placement;
- open/unscheduled;
- bounded window;
- deadline constrained;
- preferred window;
- earliest start / deadline boundaries where applicable;
- locked, window-bound, confirmation-required or freely replannable movement;
- indivisible vs splittable execution;
- minimum session duration;
- maximum session count where meaningful;
- preparation/recovery/spacing;
- partial completion, early finish and compatible merge intent;
- fallback such as skip, same-window, next valid date, shorten/split and dependency replan.

These are **planning/application specifications**. They do not construct Session rows, Actual rows or solver output.

Frontend owners:

- `model/temporal-create-session.ts`
- `ui/temporal-create-activity-fields.tsx`
- `application/temporal-create-runtime.ts`

Primary automated evidence:

- `model/temporal-create-session.test.ts`
- `application/temporal-create-enterprise.test.ts`
- `application/temporal-create-runtime.test.ts`
- `e2e/temporal-create.spec.ts`

## 6. Event recurrence family traceability

Alembic M4 defines exactly four recurrence `family_code` values:

```text
calendar_wall_clock
elapsed_interval
quota_per_period
cyclic_positional
```

C1 exposes the same four semantic families for Event without mirroring tables directly.

### Calendar / wall-clock

CP6 supports calendar pattern codes including daily, weekly weekdays, monthly month-days, monthly ordinal weekdays, yearly month-days and anchor stepping, with floating-local / named-zone / absolute-UTC clock bases.

C1 manual authoring currently exposes:

- daily;
- weekly + selected weekdays;
- monthly anchored to the authored civil date;
- monthly ordinal weekday with ordinal `-5..-1, 1..5`;
- yearly anchored to the authored civil date;
- recurrence interval;
- end open / until date / occurrence count.

This preserves the important calendar semantics without presenting database vocabulary as UI.

### Elapsed interval

CP6 M4 stores a positive elapsed interval with explicit anchor semantics. C1 captures a positive elapsed interval in minutes as authoring intent; authoritative evaluator anchoring/execution remains backend work.

### Quota per period

CP6 M4 explicitly supports:

- quota count;
- period unit `day | week | month | year`;
- positive period span;
- frame `floating_local | named_zone | absolute_utc`;
- `zone_id` only for named-zone frame;
- `week_start` only for weekly periods.

C1 now exposes that same meaningful authoring depth in Full Create:

- quota count;
- day/week/month/year;
- every N periods;
- floating-local / named-zone / absolute-UTC frame;
- week start when period is weekly;
- IANA period timezone when frame is named-zone.

### Cyclic positional

CP6 M4 stores cycle length/unit plus multiple `cycle_position` rows using `position_index` and `generates_expected`.

C1 exposes a human-friendly **1-based active-position list** and translates the conceptual meaning rather than exposing the technical 0-based index. Multiple active positions are supported; values are normalized, unique, ordered and bounded by cycle length.

## 7. Recurrence state/history and M6 boundary

C1 does not flatten recurrence into a repeat flag. CP6 binds recurrence to material state and current-history structures. M6 then allows each recurrence-generated Occurrence to bind to the exact `governing_recurrence_state_ref` that generated it.

Therefore:

```text
Create recurrence draft
!= recurrence material state persisted by backend
!= evaluator checkpoint
!= generated Occurrence
```

A later backend adapter must preserve this separation. A later C5/Detail flow owns source revision/scope editing; C1 only authors the initial specification.

## 8. Confirmation, reminders and provider seams

`v1-confirmation-and-reminders.md` allows ask-now/later, daily/weekly review, silent-unconfirmed, explicit automatic policies and provisional inference. C1 captures these as structured policy intent.

Real notification delivery is deliberately absent.

For Event collaboration/integration C1 captures:

- required participants;
- optional participants;
- rooms/resources;
- pre-read/material;
- conference intent;
- location;
- availability;
- visibility.

It does **not** claim:

- invitation delivery;
- room booking;
- conferencing link creation;
- external calendar synchronization;
- sharing/ACL changes.

These remain future backend/provider seams.

## 9. External owning-vertical handoff

Create is not a universal CRUD factory.

Application file:

`application/temporal-create-handoff.ts`

Typed targets:

```text
project
goal
routine
program
world
template
reminder
block
asset
```

Current registry state for all targets is `deferred`.

`prepareTemporalCreateHandoff()` produces an immutable, normalized draft snapshot and deliberately contains no route, href, CRUD callback or success effect. This means a future owning vertical can consume the snapshot without requiring Create to duplicate its model or silently lose the user's context.

The Routine target is also the owner-correct escape hatch for persistent Activity repetition.

Automated proof: `application/temporal-create-handoff.test.ts`.

## 10. Manual / Timeline / future DANTE input convergence

Application file:

`application/temporal-create-seed.ts`

`TemporalCreateFieldSeed` is intentionally source-neutral. It may be supplied by:

- Timeline gesture;
- future global Create;
- future keyboard command;
- import;
- a governed future DANTE interpretation.

`TemporalCreateInvocation` already accepts `seed`, and `TemporalCreateEntry` applies it before opening the same session used by manual UI.

The future architecture is therefore:

```text
manual input ───────────────┐
Timeline context ───────────┤
keyboard/global Create ─────┤
import ─────────────────────┼→ structured seed → SAME CREATE SESSION
future DANTE interpretation ┘                         ↓
                                      normalize → validate → preview
                                                   ↓
                                           explicit commit
                                                   ↓
                                              F0 command
```

DANTE will not need to script fields or click controls. C1 does not implement AI interpretation/runtime itself.

Automated proof: `application/temporal-create-seed.test.ts` plus invocation wiring in `ui/temporal-create-entry.tsx`.

## 11. Draft, progressive disclosure and preview

Quick, Expanded and Full are one session/draft, not separate form engines.

Required preserved behavior:

- Quick is title-first and low-friction;
- Expanded reveals common structured planning;
- Full reveals deep owner-specific authoring;
- round-trips preserve values;
- candidate preview stays visually/state-wise separate from accepted projection;
- validation never requires partially committing a real item.

The Timeline bridge accepts preview separately from applied effects.

Automated proof: session tests and `e2e/temporal-create.spec.ts`.

## 12. Command boundary, idempotency and snapshot integrity

F0 owns the minimal temporal command/result boundary and exact operation idempotency.

C1 adds rich specification metadata that must not be lost merely because the visible Timeline projection is minimal.

### Rich idempotency

C1 fingerprints canonical rich metadata by operation ID:

- exact prepared replay is idempotent;
- same operation ID with changed rich intent is rejected as `operation-id-reused`;
- rejected collision is side-effect free.

### Prepared-snapshot ownership

At implementation candidate `81808814...`, `runtime.prepare()` re-normalizes and deeply freezes its own specification before validation, placement/capability projection and execution.

This closes a prepare/execute TOCTOU class of bug: a future importer/adapter cannot mutate its original object after preparation and silently create a command/specification mismatch.

Automated proof:

- `application/temporal-create-runtime.test.ts`
- `application/temporal-create-boundary.test.ts`

## 13. Undo and local runtime truth

Current C1 executes against the deterministic in-memory F0 adapter only.

On applied Create:

- the projection is added;
- the rich local record is retained separately;
- reveal/focus can target the placed projection;
- Undo uses the F0 undo token;
- successful Undo removes both the projection and its C1 rich local record.

This is truthful local application behavior, not a persistence claim.

## 14. Interaction, accessibility and responsive proof

C1 protects:

- opener focus;
- contextual focus return to Timeline grid;
- dirty draft discard confirmation as named modal `alertdialog`;
- contained Tab order;
- exact previous-control focus restoration when continuing editing;
- native `inert` background while discard confirmation is active;
- unambiguous accessible names;
- automated Axe WCAG A/AA checks on advanced surfaces;
- mobile Full Create at 390×844 with strict no-horizontal-overflow invariant;
- Timeline double-click and Shift-drag contextual entry;
- virtualized Timeline gesture test anchored to a stable visible day/date instead of unstable DOM index;
- frozen Timeline pointer/focus/drag behavior in Firefox.

## 15. Performance / architecture proof

Current accepted design deliberately avoids speculative framework work.

Relevant guarantees:

- Create projections prepare layout in O(n) with cached group/day lookup and slot counters;
- local runtime is lazily initialized once per mounted entry;
- no component direct HTTP;
- no localStorage fake persistence;
- no ORM/DB-row-shaped frontend model;
- no duplicate Create engine per surface;
- no UI component dependency cycles;
- listener/RAF/observer cleanup remains covered by existing Timeline architecture/tests.

CI #536 architecture result:

```text
199 modules
477 dependencies cruised
0 dependency violations
```

## 16. Final automated evidence

Implementation candidate:

`81808814abb4e4998c7bde5b0c6cb8f5f903aa62`

Frontend CI:

`33613239926` / #536

Result:

- Quality — PASS
- Mobile Bundle — PASS
- Chromium full Web E2E — PASS
- Firefox frozen Timeline interaction contract — PASS
- Frontend CI Gate — PASS

Quality evidence:

- frontend contract drift PASS;
- active Home format PASS;
- lint PASS;
- typecheck 5/5 PASS;
- architecture 199 modules / 477 dependencies / zero violations;
- generated-source drift PASS;
- web unit suite 28 files / 168 tests PASS plus package suites;
- production build PASS;
- diff check PASS;
- repository mutation check PASS.

Production Home route on this candidate:

```text
252.22 kB raw
86.38 kB gzip
```

No dynamic split is added solely to recover a small amount of gzip at the cost of asynchronous draft/focus/error complexity. Route splitting remains a measured future performance decision, not a ceremonial optimization.

## 17. Backend stop line / disposition

The following remain intentionally outside C1:

- API transport;
- PostgreSQL writes/transactions;
- canonical server IDs;
- durable server idempotency;
- product auth/ACL enforcement;
- provider/calendar synchronization;
- invitations and room/resource booking;
- conferencing creation;
- notification delivery;
- authoritative solver;
- recurrence evaluator/checkpoints;
- Occurrence generation;
- Session runtime;
- Actual/outcome execution runtime;
- multi-device reconciliation;
- AI interpretation/runtime;
- voice runtime.

These are **deferred integration/runtime responsibilities**, not missing C1 fields.

## 18. Closure state

Automated engineering and traceability gates are satisfied on the implementation candidate.

C1 remains:

```text
AUTOMATED PASS
MANUAL ACCEPTANCE PENDING
NOT YET FROZEN / CLOSED
```

Only explicit user acceptance after the final manual protocol may transition C1 to `FROZEN / CLOSED` and authorize C2.