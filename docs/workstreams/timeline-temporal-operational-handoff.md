# Timeline / Temporal-Operational — Workstream Handoff

- **Status:** B02 ✅ CLOSED / PROVEN → B03 PRE-SCOPE AUTHORIZED
- **Reconciled:** 2026-09-16
- **Branch:** `feature/timeline-temporal-operational`
- **Current roadmap:** `docs/workstreams/timeline-temporal-operational-roadmap.md`
- **Current live map/ledger:** `docs/workstreams/timeline-temporal-operational-map.md`
- **B02 closure:** `docs/workstreams/timeline-temporal-operational-b02-closure-2026-09-16.md`
- **Next block:** B03 Event Core
- **Authorization boundary:** user authorized moving forward to B03 on 2026-09-16; this authorizes B03 authority/deep-read/PRE-SCOPE work, not implementation before PRE-SCOPE approval
- **CI:** no CI launch is implied or authorized by this handoff

## 1. Current workstream position

```text
B00 Real Data Spine                              ✅ CLOSED / PROVEN
B01 Activity Core                                ✅ CLOSED / PROVEN
B02 Schedule Core                                ✅ CLOSED / PROVEN
B03 Event Core                                   🟨 PRE-SCOPE AUTHORIZED
B04 Temporal Constraints + Movement Policy       ⬜
B05 Product Organization                         ⬜
B06 Routine / Recurrence / Occurrence Baseline   ⬜
B07 UI/UX Consolidation v1                       ⬜ planned after B06
B08 Session Runtime                              ⬜
B09 Responsibility / Participation               ⬜
B10 Actual / Outcome / Confirmation / Resolution ⬜
B11 Advanced Recurrence / Conditional / Reminder ⬜
B12 Replanning / Conflict / Solver               ⬜
B13 Provider / Offline / Multi-device             ⬜
B14 Analytics / Statistics / Signals             ⬜
B15 Whole Vertical Closure                       ⬜
```

The B07 insertion is current numbering authority. Historical old B07–B14 numbering exists only in archived snapshots.

## 2. B02 handoff contract

B03 inherits one proven shared Schedule capability. It must reuse, not clone, the B02 machinery.

Accepted placement union:

```text
date_span
floating_local
named_zone_local
absolute
coarse_local_period
```

Permanent inherited rules:

```text
Activity != Event
Activity != Schedule
Event != Schedule
Schedule != Session
Schedule != Actual
planned != happened
current placement != latest row
unscheduled != deleted
Undo != history rewind
floating local != named-zone local != absolute instant
date span != coarse local period
coarse precision != fabricated exact clock time
source wall-clock intent != resolved instant
operation/idempotency identity != canonical entity/state identity
```

B02 proved Schedule current/history, CAS/idempotency, Timeline projection, Planning Tray placement, drag/editor revision, unschedule/Undo and temporal-form correctness on Activity. B03 must exercise that same capability with Event.

## 3. Final B02 evidence frozen

```text
Alembic candidate head                         20260915_26
Dictionary / SQLAlchemy / Alembic parity        PASS
Database current-catalog + migrations        20 / 20 PASS
Migration HEAD → base → HEAD                   1 / 1 PASS
B02 PostgreSQL proof group                    11 PASS / 2 deselected
Backend temporal/API targeted                 41 / 41 PASS
Backend full non-PostgreSQL                  495 PASS / 188 deselected
Web B02-E3 targeted                          104 / 104 PASS
Web full regression                          717 / 717 PASS
TypeScript / ESLint / generated:check         PASS
B02 manual userTest A–F                       APPROVED
B02-E Chromium full-stack                     2 / 2 PASS
B02-E Firefox full-stack                      2 / 2 PASS
```

The redundant B02-E manual extension was not executed and is not claimed as PASS; that protocol is retired as an open gate and preserved in archive.

## 4. B03 PRE-SCOPE objective

Before any B03 product/schema write, re-open current Event authority across:

1. accepted Domain Event semantics and non-collapse boundaries;
2. closed Logical model ownership/cardinality;
3. accepted Physical/PostgreSQL representation and CP6 Event/Schedule/recurrence shells;
4. current Alembic `_26`, SQLAlchemy and Database Dictionary truth;
5. current backend temporal application/API seams created by B01/B02;
6. current frontend Create/Timeline/read-model contracts;
7. B03 checklist in the live map;
8. current tests and real-stack harness that B03 must extend without weakening B02.

The PRE-SCOPE must identify exact reuse versus genuine gaps before proposing DDL or code.

## 5. B03 expected semantic surface to prove/reject during deep read

The roadmap currently expects B03 to cover, subject to authority verification:

```text
Event identity / expectation
timed Event
all-day / date-span Event
multi-day Event
postponed/TBD Event without fake placeholder Schedule
original expectation / current Schedule separation
Agenda/internal Event parts
preparation/follow-up Activity relation only where justified
Place/conference intent only through accepted relations
ordinary Event attendance != Session
Event != Availability/Capacity Claim
```

Event Schedule must use B02:

```text
Activity ─┐
          ├→ shared Schedule capability
Event ────┘
```

A separate `event_schedule` engine/table/API family is forbidden unless accepted authority proves a genuinely different concept, which current authority does not anticipate.

## 6. UI checkpoint boundary

The current Create/Timeline visuals are not final. B07 is now the explicit 60–70% UI/UX consolidation checkpoint after B06.

Until B07:

- fix real usability blockers when encountered;
- do not spend entire blocks polishing temporary layouts;
- do not allow temporary UI shape to dictate Domain/API/persistence semantics.

B03 still needs truthful usable Event UI sufficient for acceptance, but not the final visual redesign.

## 7. Next action

B03 is now authorized **for PRE-SCOPE only**.

Canonical next sequence:

```text
deep authority read
→ current repo/persistence inspection
→ exact B03 reuse/gap matrix
→ proposed B03 slices + tests + stop conditions
→ PRE-SCOPE review/approval
→ only then implementation
```

Do not launch CI and do not implement B03 code/DDL before the PRE-SCOPE is reviewed and approved.