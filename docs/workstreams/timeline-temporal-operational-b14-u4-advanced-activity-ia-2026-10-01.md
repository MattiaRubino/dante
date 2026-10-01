# B14 + B07 — U4 Advanced Activity information architecture — 2026-10-01

- **Branch:** `feature/timeline-temporal-operational`
- **Status:** CANDIDATE — Create/runtime boundary and B08/B10 split are PROVEN; inline Session-enabled Timeline card runtime awaits local gate
- **Latest proven gate:** `038d86d5` — web typecheck PASS + 8/8 focused tests PASS on 2026-10-01
- **Accepted direction:** Activity structure is attached directly to the title row, not rendered as a detached panel
- **CI:** not authorized; user runs local tests in `~/projects/dante`

## 1. Goal

Turn Advanced Create for Activity into a product information architecture instead of a historical collection of controls, while reusing proven vertical capabilities instead of fabricating parallel UI state.

Permanent semantic boundaries:

```text
Step != Activity
Schedule != Session
Session END != Activity completion
Actual != Outcome != Confirmation != Reconciliation
Create configuration != post-create runtime action
```

Create/Advanced configures which capabilities and policies an item will have. Commands against real state belong to the created Activity/Event surface.

## 2. Current Advanced Activity order

```text
kind
→ title + inline Activity tree / settings rail
→ placement/date/time main controls
→ Life Area / location / Reminder main controls
→ Reference time
→ Planning
→ Recurrence when applicable
→ Reality and outcome policy
→ Description
```

The old detached `Struttura`, `Esecuzione`, `Organizzazione` and duplicate Appearance treatments are not retained as parallel panels.

## 3. Title-attached Activity tree

Accepted geometry:

```text
Activity title                         [Activity settings]
│
└── + Aggiungi
    ├── Sotto-attività
    └── Sessione                      [Session settings]
```

The right side of the root and every future child row is a settings rail, not a runtime command rail. Valid Create-time controls include enablement, mode and duration/time rules. Start/Pause/Resume/End Session, record Actual, save Outcome and register Confirmation require an existing canonical subject and do not belong in Create.

### Session intent is real Create state

Selecting `Sessione` updates the supported Create execution intent:

```text
execution.sessionMode = splittable
execution.minSessionMinutes = N
```

The detached `Esecuzione` panel remains removed. The Session child row contains only Create-time configuration and may be removed again before submit.

B04 persists the currently supported Session capability as the active soft Temporal Constraint:

```text
family = duration
constrained_facet = session.active_duration
duration_kind = minimum
```

That persisted rule, rather than a new duplicate boolean, is the current source of truth for whether the created Activity should expose B08 runtime on its Timeline card.

### Sub-Activity remains blocked, not faked

`Sotto-attività` remains disabled because the repository still has no canonical Activity → child Activity authoring contract. B13 Plan/Step is not reused as a substitute because `Step != Activity` is permanent.

## 4. Reference time

Advanced uses explicit `Riferimento orario` controls over the same `timeMode/timeZoneId` state used by Quick. The compact globe is Quick-only.

## 5. Planning

Placed Activity exposes `Unica | Suddivisa`; only `Unica` is active. `Suddivisa` remains disabled until canonical multi-placement authoring exists.

Unplaced Activity keeps the supported Temporal Constraint authoring for open/window/deadline/preferred-window intent.

The legacy editable `locked | window | confirm | free` selector is not reintroduced. `Proteggi collocazione` remains a destination until it can truthfully govern accidental manual movement and Dante automation, including a post-create unlock/edit path.

## 6. Post-create Session runtime

Canonical B08 remains:

```text
Start → Pause → Resume → End
```

`SessionSubjectControls` and `remote-session-data-source` remain the single runtime implementation. U4 now adds a compact `card` presentation of the same component rather than duplicating Session lifecycle logic.

A scheduled Activity card first reads the already-existing canonical constraints endpoint for its `activityRef`. Compact runtime is mounted only when an active current rule has:

```text
family = duration
constrained_facet = session.active_duration
```

Therefore:

```text
Activity with Session configured    → compact B08 controls on Timeline card
Activity without Session configured → no Session controls
Event                               → no B08 Session controls
```

Capability discovery fails closed: an unavailable or malformed read never exposes a Start command. Duplicate reads for the same Activity are deduplicated in the current web surface. No DB column, new boolean or parallel Session truth was introduced.

The card presentation hides detail-only duration/policy prose while preserving accessible runtime feedback. When another card is the active focus target, these runtime buttons are removed from tab order and disabled consistently with the Timeline's existing inline-action behavior.

A future performance consolidation may fold this capability directly into the authoritative Timeline read projection; the current candidate deliberately reuses the existing canonical constraint read instead of changing DB truth merely for presentation.

## 7. Reality and outcome

`Realtà ed esito` in Create is a policy/configuration destination, not a place where realized truth is recorded.

Runtime chain:

```text
Actual → Outcome → Confirmation → Reconciliation
```

The B08/B10 split is now PROVEN locally:

```text
Activity / Occurrence detail
├── Session runtime (B08)
└── Reality / Outcome / Confirmation / Reconciliation (B10)

Event detail
└── Reality / Outcome / Confirmation / Reconciliation (B10)
```

`SessionSubjectControls` owns only B08. B10 controls mount independently from canonical Activity/Event/Occurrence subject identity, so Event reality semantics never depend on Session UI.

Do not remove legacy B10 exposure from `Da collocare` until the final post-create destinations and cleanup are proven together.

## 8. Proven gates

### Create/runtime boundary

User-local result on `fd92c246` lineage:

```text
web typecheck: PASS
focused files: 3 passed
focused tests: 17 passed
```

### Independent B08/B10 destinations

User-local result on `038d86d5` lineage:

```text
web typecheck: PASS
focused files: 4 passed
focused tests: 8 passed
```

Covered:

```text
session-subject-controls.test.tsx
timeline-runtime-detail-controls.test.tsx
timeline-event-lifecycle-b03.test.tsx
temporal-create-advanced-activity-ia.test.tsx
```

The `react-i18next` NO_I18NEXT_INSTANCE line emitted by the focused runtime-detail test was non-blocking; the test file still passed.

## 9. Current inline-card candidate history

After the `038d86d5` proven checkpoint:

```text
be03dbbf  read canonical Session capability from Temporal Constraints
eeb71fb2  add compact Timeline-card Session styling
b4984a5e  gate card runtime by canonical capability
ed5bd855  add compact/inert presentation to the existing B08 controls
b06ed0a9  preserve card feedback accessibly without detail prose
a3db99ad  mount B08 controls on scheduled Activity cards only
9a809cd7  test canonical Session capability detection
6a2c3b18  test capability-gated card mounting
980dfbb0  test compact and inert B08 card presentation
```

## 10. Explicitly not claimed yet

Do not describe these as implemented/proven yet:

```text
canonical Activity → sub-Activity authoring
future Session records created before execution
multi-placement `Suddivisa` authoring
placement protection / lock persistence
manual-vs-automation unlock semantics
inline B08 Timeline-card runtime candidate until local gate passes
Create-time persistence for non-inherited outcome verification policies
Reminder notification delivery
```

## 11. Required local gate for inline Session cards

User runs locally; no CI/GitHub Actions:

```bash
cd ~/projects/dante

git pull --ff-only origin feature/timeline-temporal-operational

pnpm --filter @dante/web typecheck

pnpm --filter @dante/web exec vitest run \
  src/features/temporal/remote-session-capability-data-source.test.ts \
  src/features/temporal/activity-session-card-controls.test.tsx \
  src/features/temporal/session-subject-controls-card.test.tsx \
  src/features/temporal/session-subject-controls.test.tsx \
  src/features/home/ui/timeline/timeline-runtime-detail-controls.test.tsx \
  src/features/home/ui/timeline/timeline-event-lifecycle-b03.test.tsx \
  src/features/temporal-create/ui/temporal-create-advanced-activity-ia.test.tsx

git status --short
```

## 12. Next checkpoint after green gate

1. inspect a real Session-enabled Activity card and verify the compact controls fit short/normal Timeline cards cleanly;
2. verify an Activity created without `Sessione` exposes no runtime controls and Event exposes none;
3. decide whether capability discovery should be folded into the authoritative Timeline projection before broad-scale density work;
4. remove legacy B10 exposure from `Da collocare` only after the final card/details destination is proven;
5. design the canonical Activity → sub-Activity relationship rather than substituting B13 Step;
6. design canonical `Suddivisa` multi-placement creation and duration derivation;
7. implement placement protection for manual + Dante movement and post-create unlock;
8. continue Event Advanced separately.
