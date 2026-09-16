# Timeline / Temporal-Operational — Workstream Handoff

- **Status:** B02-E3 PROVEN / B02-E4 CLOSURE IN PROGRESS
- **Reconciled:** 2026-09-16
- **Branch:** `feature/timeline-temporal-operational`
- **E3 proven code head:** `e7086ec04276ae48a6c573c8d6eb34fa63387656`
- **Next block:** B03 Event Core — **NOT AUTHORIZED TO START UNTIL B02 CLOSES**
- **CI:** not executed; requires separate user authorization

## 1. Current workstream position

```text
B00 Real Data Spine                    ✅ PROVEN
B01 Activity Core                      ✅ PROVEN
B02-A first scheduled Activity loop    ✅ PROVEN
B02-B Planning Tray → Timeline         ✅ PROVEN
B02-C governed revision                ✅ PROVEN
B02-D unschedule + guarded Undo        ✅ PROVEN
B02-E1 placement union / coarse DDL    ✅ PROVEN
B02-E2 Timeline forms / DST projection ✅ PROVEN
B02-E3 web authoring / rendering       ✅ PROVEN
B02-E4 closure evidence                🟨 IN PROGRESS
B02 overall                            🟨 NOT CLOSED
B03 Event Core                         ⬜ DO NOT START
```

B02-E PRE-SCOPE is the active implementation authority for E1–E4. No B03 behavior is implied by the B02 Schedule capability.

## 2. B02-E3 evidence frozen at handoff

Executed evidence on the final E3 implementation lineage:

```text
Web targeted B02-E3                 104 / 104 PASS
Web full regression                 717 / 717 PASS
TypeScript typecheck                PASS
ESLint                              PASS
generated:check                     PASS
Generated OpenAPI/API client        committed
Backend Ruff                        PASS
Backend Mypy                        259 source files / no issues
Backend temporal/API targeted        41 / 41 PASS
Backend full non-PostgreSQL         495 PASS / 188 deselected
B02 PostgreSQL proof group           11 PASS / 2 deselected
```

The final PostgreSQL fix classifies reuse of one Activity operation id across incompatible unplaced-create versus scheduled-create commands as `ActivityOperationIdReuseError`; it does not reinterpret operation identity as Activity or Schedule identity.

## 3. Activated Schedule forms

B02 Schedule placement now preserves these distinct accepted forms:

```text
date_span
floating_local
named_zone_local
absolute
coarse_local_period
```

Permanent rules:

```text
floating-local wall clock != named-zone wall clock
named-zone source intent != resolved instant
absolute instant != local wall-clock intent
date span != coarse local period
coarse precision != fabricated exact interval
Schedule != Actual
```

Named-zone source wall-clock coordinates are retained independently from resolved instants. Explicit `reject / earlier / later` disambiguation is part of the acceptance boundary. Browser rendering must not re-resolve an already accepted decision.

## 4. E3 product behavior now proven automatically

- Activity Create supports `Orario`, `Tutto il giorno`, `Fascia`, `Da collocare`.
- Exact Activity authoring uses explicit `Data / Da / A`; duration is derived.
- Named-zone authoring accepts an IANA zone and explicit DST disambiguation.
- Coarse local-period authoring does not invent clock boundaries.
- Timeline hydration consumes all five canonical forms.
- date-span and coarse placements render outside the exact time grid.
- exact named-zone/absolute coordinates render in the effective viewing zone while retaining canonical source/instant semantics.
- cross-midnight exact intervals may split only at the view layer while preserving one Schedule identity.
- direct exact drag revises Schedule and preserves form; it does not create Session/Actual.
- `Riporta nel Planning Tray` remains immediate and non-destructive.
- guarded `Annulla` creates a new accepted monotonic state rather than rewinding history.
- stale expected state and operation-id reuse fail closed.
- generated OpenAPI/client expose the five-form discriminated contract.

## 5. B02-E4 open closure work

B02 is deliberately **not** marked closed yet. E4 still requires:

1. Database Dictionary/current-catalog/topology reconciliation through Alembic `20260915_26`.
2. Real full-stack B02-E local E2E proof.
3. Firefox critical T1 interaction proof on the B02-E implementation.
4. Manual `docs/workstreams/timeline-temporal-operational-b02-e-usertest.md` approval.
5. Final live map/roadmap/execution-plan reconciliation only after those proofs exist.

CI is not part of the above local closure unless separately authorized.

## 6. Known Dictionary drift entering E4

The checked-out Dictionary currently predates B02-E:

- Dictionary README/current-catalog constants still describe candidate head `20260914_23`.
- `schedule_placement_coarse_local_period_state` exists in migration `20260915_25` but has no Dictionary table entry yet.
- named-zone Dictionary text still describes strict round-trip resolution, while migration `20260915_26` permits only the two explicit supported DST-gap resolutions in addition to exact round-trip coordinates.

Do not mark Database Dictionary reconciliation complete until live PostgreSQL/current-catalog tests prove exact object counts and parity.

## 7. E4 manual acceptance authority

Use:

```text
docs/workstreams/timeline-temporal-operational-b02-e-usertest.md
```

The older `timeline-temporal-operational-b02-usertest.md` remains valid evidence for B02-A/B/C/D floating-local behavior only. It must not be cited as manual proof of date-span, named-zone, absolute, coarse precision or B02-E form completeness.

## 8. Stop conditions

Stop rather than improvise if any closure proof reveals:

- Dictionary/live PostgreSQL drift that cannot be explained by migrations 24–26;
- one Schedule form being flattened into another;
- named-zone source intent lost after acceptance/reload;
- coarse precision gaining invented exact times;
- drag/unschedule/Undo producing Activity identity replacement or Actual truth;
- stale conflict becoming last-write-wins;
- Event behavior being required to make B02 pass.

## 9. Closure transition

Only after all E4 gates pass may the handoff become:

```text
B02 Schedule Core ✅ CLOSED / PROVEN
next authorized planning target: B03 Event Core
```

Until then, B03 remains untouched.