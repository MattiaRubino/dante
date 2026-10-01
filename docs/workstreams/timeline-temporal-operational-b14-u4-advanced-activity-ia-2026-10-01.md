# B14 + B07 — U4 Advanced Activity information architecture — 2026-10-01

- **Branch:** `feature/timeline-temporal-operational`
- **Status:** CANDIDATE — Session intent moved into the title-attached tree; user-local gate still required
- **Previous proven gate:** `779fa723` — web typecheck PASS + 17/17 focused tests PASS
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
```

## 2. Current Advanced Activity order

```text
kind
→ title + inline Activity tree / action rail
→ placement/date/time main controls
→ Life Area / location / Reminder main controls
→ Reference time
→ Planning
→ Recurrence when applicable
→ Reality and outcome
→ Description
```

The old detached `Struttura`, `Esecuzione`, `Organizzazione` and duplicate Appearance treatments are not retained as parallel panels.

## 3. Title-attached Activity tree

The accepted geometry is:

```text
Activity title                         [root actions]
│
└── + Aggiungi
    ├── Sotto-attività
    └── Sessione                      [row actions]
```

The right side of the title and every future child row is reserved for row-specific actions. This geometry is now implemented in the Advanced Activity tree rather than as a separate `Struttura` panel.

### Session intent is now real draft state

`Sessione` is no longer a disabled visual destination. Selecting it updates the existing canonical Create execution intent:

```text
execution.sessionMode = splittable
execution.minSessionMinutes = N
```

The previous detached `Esecuzione` panel that edited the same state has been removed, so there is one authoring surface rather than two competing controls.

The Session row exposes the already-supported minimum active Session duration and reserves compact runtime actions on the right:

```text
▶ start
⏸ pause
▶ resume
■ end
```

Those four buttons are intentionally disabled before the Activity exists: a canonical B08 Session cannot be started against a subject that has no `activityRef` yet. This is not a fake limitation; `planned/intended != happened` remains authoritative.

The real B08 runtime remains end-to-end and is reused for existing Activity subjects through `SessionSubjectControls` and `remote-session-data-source`. Its real card controls were compacted to icon buttons while keeping their accessible names and the proven Start/Pause/Resume/End commands.

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

`Realtà ed esito` remains the Create policy destination:

```text
Actual → Outcome → Confirmation → Reconciliation
```

Create does not fabricate future Actual/Outcome/Confirmation/Reconciliation records. The existing B10 runtime continues to own realized truth after the subject exists.

Unresolved work from this family is intended to feed the derived `Da risolvere` queue without collapsing every unresolved state into canonical Reconciliation.

## 7. Description

Description remains the final Advanced section. Life Area stays in the primary Create controls. The historical duplicate `Organizzazione` notes panel remains removed.

## 8. U4 commit history

Initial visual/IA pass and title-inline correction remain part of the history. The current operational Session slice adds:

```text
07478e49  make Advanced Activity Session structure operational
944cfdbc  wire Advanced Activity Session intent into draft
0016c83c  move Session execution intent into Activity tree
907cbf2f  reuse compact B08 Session controls in Activity cards
```

## 9. Explicitly not claimed yet

Do not describe these as implemented capability yet:

```text
canonical Activity → sub-Activity authoring
future Session records created before execution
multi-placement `Suddivisa` authoring
placement protection / lock persistence
manual-vs-automation unlock semantics
Session linkage across multiple Activities
Reminder notification delivery
```

## 10. Required local gate

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
  src/features/temporal/session-subject-controls.test.tsx

git status --short
```

## 11. Next checkpoint after green gate

1. inspect the real Advanced Activity tree and compact Session row;
2. decide whether canonical Activity decomposition needs a new relation or an already-approved dormant contract exists elsewhere in the model;
3. move B10 runtime controls out of `Da collocare` only after their final post-create Activity destination is mounted;
4. design canonical `Suddivisa` multi-placement creation and duration derivation;
5. implement placement protection for manual + Dante movement and the post-create unlock path;
6. continue with Event Advanced separately.
