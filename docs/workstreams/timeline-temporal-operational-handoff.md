# Timeline / Temporal-Operational — Workstream Handoff

- **Status:** B02 Schedule Core ✅ CLOSED / PROVEN
- **Reconciled:** 2026-09-16
- **Branch:** `feature/timeline-temporal-operational`
- **Closure record:** `docs/workstreams/timeline-temporal-operational-b02-closure-2026-09-16.md`
- **Next roadmap block:** B03 Event Core
- **B03 authorization:** NOT AUTHORIZED by this handoff
- **CI:** not claimed as B02 closure evidence; no manual CI launch was authorized

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
B02-E4 closure evidence                ✅ PROVEN
B02 Schedule Core                      ✅ CLOSED / PROVEN
B03 Event Core                         ⬜ DO NOT START WITHOUT NEW AUTHORIZATION
```

B02-E PRE-SCOPE is complete. No Event behavior was used to make B02 pass.

## 2. Closed Schedule capability

The accepted B02 placement union preserves:

```text
date_span
floating_local
named_zone_local
absolute
coarse_local_period
```

Permanent rules carried forward:

```text
Activity != Schedule
Schedule != Actual
planned != happened
current placement != latest row
unscheduled != deleted
Undo != DB rewind
estimated effort != scheduled duration
floating local != named-zone local != absolute instant
date span != coarse local period
coarse precision != fabricated exact interval
named-zone source wall-clock intent != resolved instant
operation/idempotency identity != canonical entity/state identity
```

B02 activates the Activity subject path while preserving the shared Schedule capability for later Event/Occurrence use.

## 3. Final persistence authority

B02 closes on PostgreSQL 18.6 / Alembic head:

```text
20260915_26
```

Final reconciled topology:

```text
96 tables
5 views
28 routines
78 triggers
191 indexes
111 foreign keys
285 checks
0 types/domains/enums
0 sequences/materialized/partitioned
0 policies
```

Dictionary / SQLAlchemy / Alembic current-catalog parity is proven. The repository migration chain also passed fresh `HEAD → base → HEAD` round-trip. There is no migration 27 in the final B02 chain.

## 4. Final automated evidence

Executed evidence frozen for B02 closure:

```text
Database current-catalog + migrations        20 / 20 PASS
Migration HEAD → base → HEAD                  1 / 1 PASS
B02 PostgreSQL proof group                   11 PASS / 2 deselected
Backend temporal/API targeted                41 / 41 PASS
Backend full non-PostgreSQL                 495 PASS / 188 deselected
Backend Ruff                                 PASS
Backend Mypy                                 PASS
Web B02-E3 targeted                         104 / 104 PASS
Web helper                                    5 / 5 PASS
Web full regression                         717 / 717 PASS
TypeScript typecheck                         PASS
ESLint                                       PASS
generated:check                              PASS
B02-E real full-stack Chromium                2 / 2 PASS
B02-E real full-stack Firefox                 2 / 2 PASS
```

The final full-stack governed loop covers unplaced Activity → establish Schedule → revision → cross-form revision → unschedule → guarded Undo → canonical reload while preserving Schedule identity and monotonic MaterialState currentness.

The form-completeness full-stack scenario covers product-exposed date-span, coarse local period and named-zone authoring/reload. Absolute placement remains proven through API/runtime/read-model tests rather than being exposed as a fabricated primary Create mode.

## 5. Manual acceptance reconciliation

The real isolated full-stack manual B02 `userTest` A–F was completed and approved on 2026-09-15. It proves the shared user-visible lifecycle:

```text
create/place + reload                     PASS
governed revision + reload                PASS
unschedule → Planning Tray + reload       PASS
guarded Undo + reload                     PASS
stale two-tab mutation rejected           PASS
real database failure never fakes success PASS
```

The later B02-E manual protocol was not executed and is **not** being mislabeled as PASS. On 2026-09-16 the user explicitly declined a redundant second manual replay. B02-E-specific semantics are accepted from the executed PostgreSQL/backend/frontend and real-stack Chromium/Firefox evidence recorded in the closure document.

Canonical closure record:

```text
docs/workstreams/timeline-temporal-operational-b02-closure-2026-09-16.md
```

## 6. Product behavior frozen by B02

B02 now proves that:

- Activity Create can produce accepted exact, date-span, coarse and named-zone Schedule intent while preserving distinct temporal forms;
- unplaced Activity remains a valid state and Planning Tray membership depends on absence of current accepted placement, not absence of Schedule history;
- revisions preserve one Schedule identity while creating new accepted current MaterialStates;
- named-zone source intent is retained separately from resolved instant;
- explicit DST `reject / earlier / later` semantics are fail-closed and deterministic;
- coarse precision never manufactures exact clock boundaries;
- cross-midnight exact placement remains one canonical Schedule interval even if view rendering splits across days;
- direct planning changes remain Schedule mutations and do not create Session/Actual truth;
- unschedule is not delete;
- Undo is monotonic restoration, not history rewind;
- stale expected state and operation-id reuse do not become last-write-wins;
- browser/frontend success is reconciled from authoritative backend truth.

## 7. UI qualification

B02 closure does not freeze the current visual quality of the Create modal or Timeline presentation as final product design.

UI/visual cleanup may be performed later without reopening B02 provided it preserves the accepted semantic and interaction contracts above. Styling/layout dissatisfaction is not a reason to reopen Schedule persistence/domain semantics.

## 8. Next-step boundary

The next roadmap block is B03 Event Core, whose purpose is to exercise the shared Schedule capability with a second semantic owner.

However:

```text
B02 closure != B03 authorization
```

Do not begin B03 code, DDL, API or product implementation until the user gives a new explicit authorization/pre-scope approval.