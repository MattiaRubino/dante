# DANTE — Project Status

- **Status:** CURRENT PROTECTED-MAIN TRUTH + ACTIVE CANDIDATE POINTER
- **Last reconciled:** 2026-09-23
- **Pre-vertical integration merge:** `1ecd58145860aebfaaa3dc1bd356b90f7a8eb19b` via PR #66
- **AI protected-main merge:** `431fb34029baeacc9ef9f721e9626b39ca10dd39` via PR #63
- **Home/World Focus protected-main merge:** `5258452d7bd4e7a2797922b00035a9068ba41167` via PR #65
- **Protected-main Alembic:** `20260906_18`
- **Protected-main topology:** `89|5|18|77|173|91|272|0|0|0`
- **Active candidate workstream:** `feature/timeline-temporal-operational`
- **Candidate Alembic:** `20260923_57`
- **Candidate topology:** `145|5|88|92|285|223|408|0|0|0`
- **Candidate frontier:** B06 ✅ CLOSED / PROVEN → B08 NEXT; B07 deferred until after B12

Protected `main` remains integration authority. Candidate truth below is explicitly branch-local and must not be relabeled as protected-main truth before integration.

## 1. Protected-main state

```text
Product / North Star                         CURRENT
Domain / Logical / Physical                  CLOSED / CURRENT
Engineering + Frontend + Backend CP1–CP6    CLOSED / ACCEPTED
PostgreSQL                                   18.6

Access/Auth M1–M5                            CLOSED / INTEGRATED
Shared Email Platform                        CLOSED / INTEGRATED
PostgreSQL Recovery                          CLOSED / INTEGRATED
Platform Observability                       CLOSED / INTEGRATED
AI deterministic low-level foundation        CLOSED / INTEGRATED VIA PR #63
Home / World Focus reconciliation            CLOSED / INTEGRATED VIA PR #65
Pre-vertical foundation                      CLOSED / INTEGRATED VIA PR #66

Protected-main Alembic                       20260906_18
Protected-main topology                      89|5|18|77|173|91|272|0|0|0

AI production/private-data qualification     NOT CLAIMED
Apple registered-domain real UAT             BOUNDED DEFERRED / NON-BLOCKING
remote backup provider                       NOT ACTIVATED
production/cloud recovery                    NOT CLAIMED
```

## 2. Active branch candidate

```text
Branch                                       feature/timeline-temporal-operational
PostgreSQL                                   18.6
Alembic                                      20260923_57
Topology                                     145|5|88|92|285|223|408|0|0|0

B00 Real Data Spine                          ✅ CLOSED / PROVEN
B01 Activity Core                            ✅ CLOSED / PROVEN
B02 Schedule Core                            ✅ CLOSED / PROVEN
B03 Event Core                               ✅ CLOSED / PROVEN
B04 Constraints + Movement Policy            ✅ CLOSED / PROVEN
B05 Product Organization                     ✅ CLOSED / PROVEN
B06 Routine / Recurrence / Occurrence        ✅ CLOSED / PROVEN

B08 Session Runtime                          ← NEXT
B09 Responsibility / Participation           ⬜
B10 Actual / Outcome / Confirmation          ⬜
B11 Advanced Recurrence / Reminder           ⬜
B12 Replanning / Conflict / Solver           ⬜
B07 UI/UX Consolidation                      ⏸ DEFERRED
B15 Whole Vertical Closure                   ⬜
```

Former B13 provider/offline/multi-device and B14 broad analytics are outside the active `+`/Timeline vertical and remain future backlog work.

## 3. Active vertical boundary

Current candidate work is deliberately bounded to:

```text
Home `+`
→ canonical create/configuration
→ Timeline representation/actions
→ required Session/Actual lifecycle
→ Responsibility/Participation roles
→ advanced recurrence/reminders
→ replanning/conflict/solver proposals
→ final deferred UI/UX consolidation
```

Not current vertical scope:

```text
external provider integration
native/mobile/offline/multi-device
account-to-account collaboration/chat/shared editing
broad analytics/statistics/signals
```

Current authority:

- `ROADMAP.md`
- `workstreams/timeline-temporal-operational-post-b06-scope-decision-2026-09-23.md`
- `workstreams/timeline-temporal-operational-roadmap.md`
- `workstreams/timeline-temporal-operational-map.md`
- `workstreams/timeline-temporal-operational-handoff.md`
- `database/timeline-temporal-operational.md`

## 4. Permanent distinctions

```text
Person != Account != Principal != Actor
AuthSession != DANTE Session
Activity != Event != Routine
Routine != Recurrence != Occurrence
Occurrence != Schedule
Schedule != Temporal Constraint != Movement Policy
Schedule != Session != Actual
Session != Actual != Outcome
Actual != Outcome != Confirmation
Responsibility != Participation
planned/intended != happened
proposal != accepted effect
projection != canonical truth
```

UUID ordering is never semantic chronology/currentness authority.

## 5. Protected-main pre-vertical acceptance evidence

The integrated pre-vertical foundation supplied authenticated Account → admitted Principal → DANTE context → self Person, reusable UUIDv7/Clock/timezone primitives, persistent LOCAL/DEV dogfood and deterministic scale/convergence proof.

Its historical final acceptance evidence remains in `workstreams/pre-vertical-foundation-closure-2026-09-06.md`; those exact PASS counts are evidence for that checkpoint and are not reinterpreted as current candidate test results.

## 6. Recovery disposition

Current protected-main Recovery authority remains `operations/postgres-recovery-runbook.md`.

```text
LOCAL exact-head recovery capability         integrated/proven for its recorded scope
remote backup provider                       NOT ACTIVATED
production/cloud recovery                    NOT CLAIMED
```

Candidate Timeline migrations are forward-only descendants of the protected-main baseline; no accepted migration history is rewritten.

## 7. Documentation lifecycle

Durable current references include:

- `README.md`
- `ROADMAP.md`
- `database/README.md`
- active Timeline workstream authority listed above
- executable source, migrations, tests and tooling

Dated closure/evidence and archived records preserve phase-time truth. They must not override current authority when their `NEXT` or status prose is older.

## 8. Next development boundary

The active candidate next block is **B08 Session Runtime**, starting with Product/Domain/Logical/Physical/DB pre-scope reconciliation from `_57`.

No migration, generic runtime framework, Actual semantics, collaboration system, provider sync or broad analytics is pre-authorized by that label.

## 9. Permanent safety rules

```text
protected main is integration authority
unmerged candidate truth != protected-main truth
applied migration history is immutable
no PASS without executed evidence
no schema claim without Dictionary/mapping/migration/PG/test parity
AI/model output != canonical DANTE truth
telemetry != canonical DANTE state
LOCAL recovery PASS != production/cloud recovery PASS
```

## 10. Authority order

1. executable code / migrations / tests / real PostgreSQL
2. Product / Domain / Logical / Physical / constitutions / ADRs
3. current subsystem references
4. this status + current roadmap/workstream authority
5. durable closure/evidence + Git/PR chronology
6. conversation memory
