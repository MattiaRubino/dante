# Timeline / Temporal-Operational — B04-B Boundary / Deadline Closure

- **Status:** ✅ CLOSED / PROVEN
- **Branch:** `feature/timeline-temporal-operational`
- **Closure date:** 2026-09-19
- **Implementation freeze:** `docs/workstreams/timeline-temporal-operational-b04-b-implementation-freeze.md`
- **Parent authority:** `docs/workstreams/timeline-temporal-operational-b04-execution-plan.md`
- **Previous closure:** `docs/workstreams/timeline-temporal-operational-b04-a-closure-2026-09-18.md`
- **Candidate Alembic head:** `20260919_34`
- **Candidate topology:** `107|5|34|85|212|129|309|0|0|0`
- **Generated contract commit:** `3ca46c634411371d720b9ea1ed6600bce16b23da`

## 1. Closed semantic slice

B04-B extends the B04-A boundary family without collapsing Temporal Constraint into Schedule placement or generic `due_at` truth.

Accepted absolute rule matrix:

```text
earliest_start     + schedule.start       ✅
latest_start       + schedule.start       ✅
latest_completion  + schedule.completion  ✅
```

Shared bounds:

```text
subject        self-owned Activity | Event
family         boundary
strength       hard | soft
temporal form  absolute
value          finite timestamptz
```

Unsupported pairings fail closed. B04-B does not infer Actual, Outcome, failure or completion from a passed deadline.

Permanent non-collapse remains:

```text
deadline != Schedule end
passed deadline != Actual
passed deadline != Outcome / failure
constraint != placement
Temporal Constraint != Movement Policy
current accepted state != latest row
```

## 2. Persistence closure

Forward migration `20260919_34_b04_absolute_boundary_deadline.py`:

- widens `temporal_constraint_state.constrained_facet_code` from only `schedule.start` to the accepted B04-B facet set;
- widens `temporal_constraint_boundary_state.boundary_kind_code` to `earliest_start | latest_start | latest_completion`;
- keeps `temporal_form_code='absolute'` for this slice;
- strengthens deferred totality so the kind/facet matrix itself is canonical DB truth;
- adds governed `mutate_self_absolute_boundary_constraint(...)` while retaining the B04-A earliest-start routine for compatibility;
- introduces no new table, trigger, index, FK or CHECK object count.

Candidate topology at closure:

```text
107 tables
5 views
34 routines
85 triggers
212 indexes
129 foreign keys
309 CHECK constraints
0 enums/domains
0 sequence/materialized/partitioned objects
0 RLS policies
```

## 3. Application / API closure

The existing five public Temporal Constraint operations remain stable; B04-B changes the typed rule contract rather than inventing duplicate endpoints.

The public rule is now an explicit discriminated union of:

```text
AbsoluteEarliestStartRule
AbsoluteLatestStartRule
AbsoluteLatestCompletionRule
```

Each variant carries its exact `boundary_kind` and `constrained_facet`; no generic untyped rule payload was introduced. Existing explicit `temporal_*` operationIds remain unchanged.

Create/revise/retire retain:

```text
operation-id idempotency
expected-current CAS
append-only MaterialState history
retired != deleted
Activity/Event self scope
```

## 4. Proof evidence

Observed local gates:

```text
API / typed-union / Temporal inventory             13 PASS
PostgreSQL + application + API activation + DB     22 PASS / 1 deselected
OpenAPI export / inventory / API contract          21 PASS
@dante/api-client typecheck                         PASS
@dante/api-client Vitest                            11 PASS
pnpm generated:check                                PASS / 163 files deterministic
```

The generated OpenAPI / Orval client update was committed and pushed as:

```text
3ca46c634411371d720b9ea1ed6600bce16b23da
feat(temporal): generate B04-B boundary API client
```

No frontend product surface was part of the accepted B04-B slice, so no frontend manual userTest is claimed.

## 5. Representation reconciliation

B04-B closure reconciles:

```text
Domain / Logical freeze
→ Alembic _34
→ SQLAlchemy mappings
→ Dictionary object entries + scope
→ PostgreSQL catalog / owner / ACL proof
→ application / API typed union
→ exact Temporal API governance
→ OpenAPI snapshot
→ Orval-generated @dante/api-client
→ current DB references / Timeline DB overlay
→ roadmap / live map / handoff
→ this closure evidence
```

Protected-main authority remains unchanged; `_34` is Timeline candidate truth only.

## 6. Closure decision

```text
semantic freeze                         ✅ PROVEN
absolute boundary DB matrix             ✅ PROVEN
latest-start                            ✅ PROVEN
latest-completion / deadline            ✅ PROVEN
CAS / history / replay                  ✅ PROVEN
application typed rule union            ✅ PROVEN
public API compatibility                ✅ PROVEN
Dictionary / catalog / ACL              ✅ PROVEN
OpenAPI / generated client              ✅ PROVEN
deterministic generation                ✅ PROVEN
documentation reconciliation            ✅ CLOSED

B04-B Boundary / Deadline constraints   ✅ CLOSED / PROVEN
```

## 7. Next gate

B04 remains **IN PROGRESS**. The next slice is **B04-C Windows / Preferences / Evaluation**.

B04-C must be separately frozen before implementation. It must not pull in Movement Policy (B04-D), advanced duration/spacing/relative applicability (B04-E), solver/replanning ownership (B12), or B05+.
