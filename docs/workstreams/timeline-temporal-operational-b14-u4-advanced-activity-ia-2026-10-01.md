# B14 + B07 — U4 Advanced Activity information architecture — 2026-10-01

- **Branch:** `feature/timeline-temporal-operational`
- **Status:** CANDIDATE — Create/runtime boundary is PROVEN; B08/B10 post-create split now awaits local gate
- **Latest proven gate:** `fd92c246` — web typecheck PASS + 17/17 focused tests PASS on 2026-10-01
- **Accepted direction:** Activity structure is attached directly to the title row, not rendered as a detached panel
- **CI:** not authorized; user runs local tests in `~/projects/dante`

## 1. Goal

Turn Advanced Create for Activity into a product information architecture instead of a historical collection of controls, while reusing proven vertical capabilities instead of fabricating parallel UI state.

The permanent semantic boundaries remain:

```text
Step != Activity
Schedule != Session
Session END != Activity completion
Actual != Outcome != Confirmation != Reconciliation
Create configuration != post-create runtime action
```

The last boundary is explicit product policy: Create/Advanced configures which capabilities and policies an item will have; actions against real state belong to the created Activity/Event surface.

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

The accepted geometry is:

```text
Activity title                         [Activity settings]
│
└── + Aggiungi
    ├── Sotto-attività
    └── Sessione                      [Session settings]
```

The right side of the title and every future child row is reserved for configuration/settings belonging to that node. It is not a runtime command rail.

Examples of valid Create-time controls in that rail are enablement, mode, duration/time rules and other properties that must exist on the item after creation.

Examples that do **not** belong there are Start/Pause/Resume/End Session, record Actual, save Outcome or register Confirmation. Those require an existing canonical subject and belong on the post-create card/details surface.

### Session intent is real Create draft state

Selecting `Sessione` updates the existing supported Create execution intent:

```text
execution.sessionMode = splittable
execution.minSessionMinutes = N
```

The previous detached `Esecuzione` panel that edited the same state remains removed, so there is one authoring surface rather than two competing controls.

The Session child row contains only Create-time configuration. The current supported setting is minimum active Session duration; it is displayed in the row settings rail. The row may be disabled/removed again before creation.

The temporary disabled runtime icons previously shown in Create were removed after user review. Their semantics were wrong even while disabled because Create is not a place from which an Activity can later be resumed.

### Runtime Session controls belong to the created item

The canonical B08 runtime remains separate and real:

```text
Start → Pause → Resume → End
```

`SessionSubjectControls` and `remote-session-data-source` remain the post-create runtime path for an existing Activity/Occurrence subject. Their commands require a real `activityRef` / `occurrenceRef` and must be mounted from the final Activity card/details destination rather than represented in Advanced Create.

## 4. Reference time

Advanced uses explicit `Riferimento orario` controls over the same `timeMode/timeZoneId` state used by Quick. The compact globe is Quick-only.

## 5. Planning

Placed Activity currently exposes `Unica | Suddivisa`; only `Unica` is active. `Suddivisa` stays disabled until canonical multi-placement authoring exists.

Unplaced Activity keeps the existing supported Temporal Constraint authoring for open/window/deadline/preferred-window intent.

The legacy editable `locked | window | confirm | free` movement selector is not reintroduced. `Proteggi collocazione` remains a disabled destination until it can truthfully govern both accidental manual movement and Dante automation, with post-create unlock/edit semantics explicitly defined.

## 6. Reality and outcome

`Realtà ed esito` is a Create-time **policy/configuration** destination, not a place where realized truth is recorded.

The conceptual runtime chain remains:

```text
Actual → Outcome → Confirmation → Reconciliation
```

Create may configure supported behavior/policies for that future chain. The actual operations happen only after the Activity/Event exists, on its post-create card/details surface.

The current Create runtime only truthfully supports the inherited outcome-verification policy. Other model enum values must not be made selectable merely because the TypeScript type contains them; they require a canonical persistence/authoring path first.

### B08/B10 runtime split candidate

After the proven Create gate, the post-create runtime was corrected so B10 is no longer owned by B08:

```text
Activity / Occurrence detail
├── Session runtime (B08)
└── Reality / Outcome / Confirmation / Reconciliation (B10)

Event detail
└── Reality / Outcome / Confirmation / Reconciliation (B10)
```

`SessionSubjectControls` now owns only Session runtime and duration evaluation. `ActualRealizationControls` is mounted independently by Timeline subject detail from the canonical Activity/Event/Occurrence basis.

This matters because Event has B10 reality semantics even though current Session runtime supports Activity/Occurrence only. B10 must therefore never depend on the presence of a Session UI.

The new focused test `timeline-runtime-detail-controls.test.tsx` covers canonical Activity/Event/Occurrence B10 subject derivation and verifies that Reality controls mount without Session controls.

## 7. Description

Description remains the final Advanced section. Life Area stays in the primary Create controls. The historical duplicate `Organizzazione` notes panel remains removed.

## 8. Proven gates and candidate history

### Proven Create/runtime-boundary gate

User-local result on `fd92c246` lineage:

```text
web typecheck: PASS
focused test files: 3 passed
focused tests: 17 passed
```

Covered:

```text
temporal-create-advanced-activity-ia.test.tsx
session-subject-controls.test.tsx
temporal-create-b04-runtime.test.ts
```

This proves the correction that Advanced Create exposes Session settings but no Start/Pause/Resume/End controls.

### Current B08/B10 split candidate

```text
f61fcbb0  decouple B10 reality controls from Session runtime
61e50968  mount B10 reality controls directly on canonical subject detail
89f271d5  add focused Activity/Event/Occurrence runtime-destination tests
```

## 9. Explicitly not claimed yet

Do not describe these as implemented/proven capability yet:

```text
canonical Activity → sub-Activity authoring
future Session records created before execution
multi-placement `Suddivisa` authoring
placement protection / lock persistence
manual-vs-automation unlock semantics
inline B08 runtime buttons directly on every Timeline card
Create-time persistence for non-inherited outcome verification policies
Reminder notification delivery
```

The current B08 runtime remains available in the created item detail; direct compact Timeline-card buttons are still a separate UI move and must not be confused with Create-time configuration.

## 10. Required local gate for B08/B10 split

User runs locally; no CI/GitHub Actions:

```bash
cd ~/projects/dante

git pull --ff-only origin feature/timeline-temporal-operational

pnpm --filter @dante/web typecheck

pnpm --filter @dante/web exec vitest run \
  src/features/temporal/session-subject-controls.test.tsx \
  src/features/home/ui/timeline/timeline-runtime-detail-controls.test.tsx \
  src/features/home/ui/timeline/timeline-event-lifecycle-b03.test.tsx \
  src/features/temporal-create/ui/temporal-create-advanced-activity-ia.test.tsx

git status --short
```

## 11. Next checkpoint after green gate

1. mount compact B08 Start/Pause/Resume/End directly on eligible created Timeline Activity/Occurrence cards, while keeping Create free of runtime commands;
2. only show those card controls when canonical persisted capability/policy says Session tracking is enabled — do not show Session runtime on every Activity merely because the endpoint exists;
3. remove legacy B10 exposure from `Da collocare` only after the final card/details destination is proven;
4. decide whether canonical Activity decomposition needs a new relation or an already-approved dormant contract exists elsewhere in the model;
5. design canonical `Suddivisa` multi-placement creation and duration derivation;
6. implement placement protection for manual + Dante movement and the post-create unlock path;
7. continue with Event Advanced separately.
