# Timeline / Temporal-Operational — B02 Schedule Core Closure

- **Status:** ✅ CLOSED / PROVEN
- **Date:** 2026-09-16
- **Branch:** `feature/timeline-temporal-operational`
- **Scope:** B02 Schedule Core only
- **B03 Event Core:** NOT AUTHORIZED by this closure
- **CI:** not claimed as closure evidence; local/real-stack evidence is the accepted gate for this closure

## 1. Closure decision

B02 Schedule Core is closed and proven.

This closure does **not** claim that the separate B02-E manual protocol was executed. The user explicitly declined a redundant second manual pass on 2026-09-16 after the already-approved B02 manual acceptance from 2026-09-15. The evidence model is therefore reconciled as follows:

- the approved B02 manual `userTest` A–F from 2026-09-15 remains the manual acceptance evidence for the shared real-product interactions: create/place, governed revision, unschedule, guarded Undo, stale conflict truthfulness, reload persistence and database-failure truthfulness;
- B02-E-specific form completeness and temporal semantics are accepted from the executed automated PostgreSQL/backend/frontend/full-stack evidence below;
- Chromium and Firefox full-stack runs exercise the B02-E implementation against a disposable PostgreSQL 18.6 stack and real FastAPI/web production build;
- no second manual replay is required merely to duplicate already-proven interactions.

This is an explicit closure decision, not a fabricated `B02-E manual PASS`.

## 2. Semantic boundary preserved

B02 closes with these distinctions intact:

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
coarse precision != fabricated exact clock time
source wall-clock intent != resolved instant
operation/idempotency identity != Activity/Schedule/MaterialState identity
```

B02 activates Schedule for Activity. It does not authorize Event Core, Routine/Recurrence, Session, Actual or Outcome implementation.

## 3. Activated Schedule forms

The accepted Schedule placement union is:

```text
date_span
floating_local
named_zone_local
absolute
coarse_local_period
```

Named-zone acceptance retains source wall-clock intent separately from resolved instants and uses explicit `reject / earlier / later` disambiguation. Coarse local periods remain coarse and do not manufacture exact clock boundaries.

## 4. Database / Dictionary / migration evidence

B02-E closure reconciled Database Dictionary / SQLAlchemy / Alembic through head `20260915_26`.

Final live topology:

```text
tables          96
views            5
routines        28
triggers        78
indexes        191
foreign keys   111
checks         285
types/domains/enums 0
sequences/materialized/partitioned 0
policies         0
```

Executed evidence:

```text
current-catalog + migration PostgreSQL gate    20 / 20 PASS
repository HEAD → base → HEAD round-trip        1 / 1 PASS
Dictionary / SQLAlchemy / Alembic parity        PASS
```

The B02 migration chain remains at `_26`; no migration 27 is part of the final branch state.

## 5. Backend / PostgreSQL / web evidence

Frozen proven evidence includes:

```text
B02 PostgreSQL proof group             11 PASS / 2 deselected
Backend temporal/API targeted          41 / 41 PASS
Backend full non-PostgreSQL           495 PASS / 188 deselected
Backend Ruff                           PASS
Backend Mypy                           PASS
Web B02-E3 targeted                   104 / 104 PASS
Web helper                              5 / 5 PASS
Web full regression                   717 / 717 PASS
TypeScript typecheck                   PASS
ESLint                                 PASS
generated:check                        PASS
```

Cross-command Activity idempotency reuse is fail-closed and classified as `ActivityOperationIdReuseError`; operation identity does not become Activity or Schedule identity.

## 6. Real full-stack E2E evidence

The final B02-E full-stack spec is:

```text
apps/web/e2e/auth/temporal-b02-schedule-forms.spec.ts
```

It runs against the real auth stack, production web build, FastAPI and disposable PostgreSQL 18.6.

Final executed results on 2026-09-16:

```text
Chromium    2 / 2 PASS
Firefox     2 / 2 PASS
```

The governed-loop scenario proves:

```text
create unplaced Activity
→ real Planning Tray membership
→ establish accepted Schedule
→ exact move/revision
→ cross-form revision to coarse_local_period
→ unschedule
→ guarded Undo
→ canonical reload
→ same Schedule identity + monotonic current MaterialState
```

The form-completeness scenario proves product-exposed:

```text
date_span
coarse_local_period
named_zone_local
```

through create and canonical reload. Absolute form remains API/runtime/read-model evidence rather than a manufactured primary Create UI mode.

## 7. Manual acceptance evidence reuse

The approved manual protocol remains:

```text
docs/workstreams/timeline-temporal-operational-b02-usertest.md
```

Completed 2026-09-15:

```text
Proof A — create/place same Activity identity + reload          PASS
Proof B — governed revision + reload                           PASS
Proof C — unschedule → Planning Tray + reload                  PASS
Proof D — guarded Undo creates restored current state           PASS
Proof E — stale mutation is rejected without overwrite         PASS
Proof F — real database failure never fakes success             PASS

B02 userTest — APPROVED
```

The later `timeline-temporal-operational-b02-e-usertest.md` remains a protocol artifact, not an executed evidence claim. Its duplicated interaction checks are not rerun for closure; E-specific semantics are covered by the automated and real full-stack evidence recorded here.

## 8. Product/UI qualification

B02 closure is a semantic, persistence, application and interaction closure. It is **not** an assertion that the current Create/Timeline visual design is final or polished.

UI/visual refinement may be performed later provided it preserves the frozen B02 semantics and interaction contracts. Visual dissatisfaction with the current form layout does not reopen Schedule Core ontology or persistence behavior.

## 9. Final status

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
B03 Event Core                         ⬜ NOT AUTHORIZED
```

B02 is complete. Any subsequent B03 work requires a separate authorization/pre-scope decision.