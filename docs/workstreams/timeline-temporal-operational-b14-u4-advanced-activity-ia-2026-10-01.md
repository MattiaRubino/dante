# B14 + B07 — U4 Advanced Activity information architecture — 2026-10-01

- **Branch:** `feature/timeline-temporal-operational`
- **Status:** CANDIDATE after UX correction; previous operational slice is PROVEN locally
- **Latest proven gate:** `fc4ae041` — web typecheck PASS + 34/34 focused tests PASS on 2026-10-01
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

The last boundary is now explicit product policy: Create/Advanced configures which capabilities and policies an item will have; actions against real state belong to the created Activity/Event surface.

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

The Session child row now contains only Create-time configuration. The current supported setting is minimum active Session duration; it is displayed in the row settings rail. The row may be disabled/removed again before creation.

The temporary disabled runtime icons previously shown in Create were removed after user review. Their semantics were wrong even while disabled because Create is not a place from which an Activity can later be resumed.

### Runtime Session controls belong to the created item

The canonical B08 runtime remains separate and real:

```text
Start → Pause → Resume → End
```

`SessionSubjectControls` and `remote-session-data-source` remain the post-create runtime path for an existing Activity/Occurrence subject. Their commands require a real `activityRef` / `occurrenceRef` and must be mounted from the final Activity card/details destination rather than represented in Advanced Create.

### Sub-Activity remains blocked, not faked

`Sotto-attività` stays disabled because the current repository does not expose a canonical Activity → child Activity authoring contract. B13 Plan/Step is not silently reused as a substitute because `Step != Activity` is permanent.

A future slice may add a reviewed Activity decomposition relationship, but U4 does not invent one merely to make the button appear functional.

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

The B10 runtime controls (`ActualRealizationControls`, `OutcomeControls`, `ConfirmationControls`, `ReconciliationControls`) remain the real post-create implementation. They should be moved out of `Da collocare` only when the final Activity/Event card/details destination is mounted, so no capability is lost during the UI migration.

## 7. Description

Description remains the final Advanced section. Life Area stays in the primary Create controls. The historical duplicate `Organizzazione` notes panel remains removed.

## 8. U4 gate and correction history

User-local gate for the operational slice:

```text
fc4ae041
web typecheck: PASS
focused test files: 6 passed
focused tests: 34 passed
```

The focused gate covered Create U2, top U1, composer, Advanced Activity IA, B08 Session controls and B04 Create runtime.

Post-gate UX correction commits begin after `fc4ae041`:

```text
3537fc12  remove runtime Session commands from Advanced Create and keep settings only
4d3ceb49  align Session configuration in the right-side settings rail
3391b932  regress that Create exposes no Session runtime actions
```

## 9. Explicitly not claimed yet

Do not describe these as implemented capability yet:

```text
canonical Activity → sub-Activity authoring
future Session records created before execution
multi-placement `Suddivisa` authoring
placement protection / lock persistence
manual-vs-automation unlock semantics
final mounted runtime controls on every created Timeline Activity card
Create-time persistence for non-inherited outcome verification policies
Reminder notification delivery
```

## 10. Required local gate for the correction

User runs locally; no CI/GitHub Actions:

```bash
cd ~/projects/dante

git pull --ff-only origin feature/timeline-temporal-operational

pnpm --filter @dante/web typecheck

pnpm --filter @dante/web exec vitest run \
  src/features/temporal-create/ui/temporal-create-entry-u2.test.tsx \
  src/features/temporal-create/ui/temporal-create-top-u1.test.tsx \
  src/features/temporal-create/ui/temporal-create-composer.test.tsx \
  src/features/temporal-create/ui/temporal-create-advanced-activity-ia.test.tsx \
  src/features/temporal/session-subject-controls.test.tsx \
  src/features/temporal-create/application/temporal-create-b04-runtime.test.ts

git status --short
```

## 11. Next checkpoint after green gate

1. inspect the corrected Advanced Activity tree: Session row must show settings only, never runtime commands;
2. identify and mount B08 Session + B10 Reality/Outcome/Confirmation runtime controls on the final created Activity card/details destination;
3. only after that destination is proven, remove their legacy exposure from `Da collocare`;
4. decide whether canonical Activity decomposition needs a new relation or an already-approved dormant contract exists elsewhere in the model;
5. design canonical `Suddivisa` multi-placement creation and duration derivation;
6. implement placement protection for manual + Dante movement and the post-create unlock path;
7. continue with Event Advanced separately.
