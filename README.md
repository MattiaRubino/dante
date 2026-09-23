# DANTE

DANTE is a personal operating system designed to help people understand, organize and improve real life by turning intentions, needs and possibilities into outcomes they can realistically pursue.

**Compass:** *Understand life. Shape what comes next.*

## Current repository state

Protected `main` remains the single integrated authority. The active unmerged candidate is `feature/timeline-temporal-operational`; its branch-local truth is explicitly separate from protected-main truth until integration.

```text
PRODUCT / DOMAIN / LOGICAL / PHYSICAL      CLOSED / CURRENT
ENGINEERING / FRONTEND / BACKEND CP1–CP6  CLOSED / ACCEPTED
POSTGRESQL                                 18.6

PROTECTED MAIN AT TEMPORAL SELECTION
  Access/Auth + Shared Email              CLOSED / INTEGRATED
  Recovery                                CLOSED / INTEGRATED
  Platform Observability                  CLOSED / INTEGRATED
  AI deterministic low-level foundation  CLOSED / INTEGRATED
  Home / World Focus                      CLOSED / INTEGRATED
  Pre-vertical foundation                 CLOSED / INTEGRATED
  Alembic                                 20260906_18
  DB topology                             89|5|18|77|173|91|272|0|0|0

ACTIVE TIMELINE CANDIDATE
  branch                                  feature/timeline-temporal-operational
  Alembic                                 20260923_57
  DB topology                             145|5|88|92|285|223|408|0|0|0
  B00–B06                                 CLOSED / PROVEN
  B08 Session Runtime                     NEXT
  B07 UI/UX Consolidation                 DEFERRED until after B12
```

The current Timeline/Temporal workstream is the bounded **Home `+` → canonical truth → Timeline → required lifecycle** vertical. It is not an all-DANTE roadmap.

Active sequence:

```text
B08 Session Runtime
→ B09 Responsibility / Participation
→ B10 Actual / Outcome / Confirmation / Resolution
→ B11 Advanced Recurrence / Conditional / Reminder
→ B12 Replanning / Conflict / Solver
→ B07 UI/UX Consolidation v1
→ B15 Whole Vertical Closure
```

External provider integration, native/offline/multi-device, account-to-account collaboration and broad analytics are future work outside this vertical.

## Permanent architecture rules

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
PostgreSQL is canonical persistence
provider identity != DANTE identity
no provider/network I/O inside authoritative DB transactions
applied migrations are immutable
```

## Current continuation order

For Timeline/Temporal work:

1. `docs/PROJECT-STATUS.md`
2. `docs/ROADMAP.md`
3. `docs/workstreams/timeline-temporal-operational-post-b06-scope-decision-2026-09-23.md`
4. `docs/workstreams/timeline-temporal-operational-roadmap.md`
5. `docs/workstreams/timeline-temporal-operational-map.md`
6. `docs/workstreams/timeline-temporal-operational-handoff.md`
7. `docs/database/README.md`
8. `docs/database/dictionary/README.md`
9. exact current Git/source/tests

Historical workstream/closure files preserve chronology and evidence; old `NEXT` prose in dated evidence does not override current authority.

## Documentation entry points

- `docs/README.md`
- `docs/PROJECT-STATUS.md`
- `docs/ROADMAP.md`
- `docs/database/README.md`
- `docs/database/dictionary/README.md`
- `docs/frontend/README.md`
- `docs/workstreams/README.md`
- `apps/backend/README.md`

Executable repository truth and accepted current documentation outrank conversation memory and historical handoffs.