# B14 + B07 — U4 Advanced Activity information architecture — 2026-10-01

- **Branch:** `feature/timeline-temporal-operational`
- **Status:** CANDIDATE — visual/product checkpoint; user-local gate still required
- **Previous proven gate:** `779fa723` — web typecheck PASS + 17/17 focused tests PASS
- **Candidate head before this document commit:** `681f88993520cb17fa4384bf83650d4193736005`
- **CI:** not authorized; user runs local tests in `~/projects/dante`

## 1. Goal

Turn Advanced Create for Activity into a product information architecture instead of a historical collection of controls. The candidate is intentionally conservative about persistence: controls that are not yet connected to a canonical authoring path are shown only as disabled visual destinations and do not collect silently ignored data.

## 2. Product decisions represented in the candidate

Advanced Activity now follows this visible order:

```text
kind
→ title
→ placement/date/time main controls
→ Life Area / location / Reminder main controls
→ Reference time
→ Structure
→ Planning
→ Execution
→ Recurrence when applicable
→ Reality and outcome
→ Description
```

Quick remains compact and keeps its prior ordering.

### Reference time

The former verbose `Tempo e fuso` treatment is reduced to one compact `Riferimento orario` section with only:

```text
Modalità = Ora locale | Fuso specifico
Fuso orario = explicit zone when zoned
```

No duplicate Quick globe is mounted in Advanced.

### Structure

The candidate introduces the intended Activity structure destination:

```text
Activity root
└── + Aggiungi
    ├── Sotto-attività
    └── Sessione
```

Both child options are deliberately disabled in this checkpoint. They are visual IA only until a reviewed atomic Create path exists. B13 Plan/Step must not be silently reused as `sub-Activity`; `Step != Activity` remains permanent. A future Session row created before execution must also not fabricate a canonical performed Session; `planned/intended != happened` and `Schedule != Session` remain authoritative.

### Planning

Placed Activity shows `Unica | Suddivisa`; only `Unica` is currently active. `Suddivisa` is disabled until Create has a canonical atomic multi-placement authoring path. This avoids allowing a user to enter a parent duration that contradicts hidden child placements.

Unplaced Activity keeps the existing supported Temporal Constraint authoring for open/window/deadline/preferred-window intent.

The legacy editable `locked | window | confirm | free` movement select has been removed from this Advanced Activity candidate. B04 already superseded that prototype vocabulary by separating Temporal Constraint from Movement Policy.

A visual `Proteggi collocazione` destination is shown for placed Activity and is disabled. The accepted product direction is one user-facing protection concept that must eventually govern both accidental manual movement and Dante automation while preserving separate internal authority/effect paths. Post-create unlock/edit UX is explicitly still TODO.

### Execution / Session

The previous Advanced panel exposed maximum Session count, spacing, preparation/recovery, partial completion, early finish and merge compatibility even though the current Create path does not persist all of them truthfully.

U4 removes those editable controls from Activity Create. The candidate keeps only the existing Session minimum-duration authoring seam:

```text
Durata minima per Sessione
→ minimum active Session duration
```

This preserves `Session != Activity`, `Session != Schedule`, and `Session END != completion`.

### Reality and outcome

The former standalone `Verifica esito` panel becomes a collapsible `Realtà ed esito` destination. The currently supported authoring remains the inherited outcome-verification policy. The visual flow is:

```text
Actual → Outcome → Confirmation → Reconciliation
```

This is product organization only; Create does not fabricate future Actual/Outcome/Confirmation records. Policy may be configured before execution; realized records arise only from reality.

Unresolved work from this family is intended to feed the derived `Da risolvere` / Resolution Queue, without collapsing every unresolved case into canonical Reconciliation.

### Description / Organization

The historical Advanced `Organizzazione` panel contained only a duplicate Notes textarea and is removed, including the obsolete component file. Description now has one explicit Advanced section at the end while Quick keeps its compact description field. Life Area remains in the primary Create controls.

## 3. Commits in this candidate

```text
5e4249ce  shape Advanced Create information architecture
6067dba0  simplify Activity Advanced planning and execution
A84bbb38  place outcome verification under reality section
630cc035  compose Advanced Activity workspace styling
6f914e37  remove superseded Advanced organization panel
1dea8272  keep reality section visible in initial Advanced pass
681f8899  add focused Advanced Activity IA regression
```

## 4. Explicitly not claimed yet

Do not describe these as implemented capability yet:

```text
atomic sub-Activity authoring from Create
future/planned Session persistence
multi-placement `Suddivisa` authoring
placement protection / lock persistence
manual-vs-automation unlock semantics
Session linkage across multiple Activities
post-create unlock UX
Reminder notification delivery
```

The candidate only gives those capabilities a truthful visual destination where useful.

## 5. Required local gate

User runs locally; no CI/GitHub Actions:

```bash
cd ~/projects/dante

git pull --ff-only origin feature/timeline-temporal-operational

pnpm --filter @dante/web typecheck

pnpm --filter @dante/web exec vitest run \
  src/features/temporal-create/ui/temporal-create-entry-u2.test.tsx \
  src/features/temporal-create/ui/temporal-create-top-u1.test.tsx \
  src/features/temporal-create/ui/temporal-create-composer.test.tsx \
  src/features/temporal-create/ui/temporal-create-advanced-activity-ia.test.tsx

git status --short
```

## 6. Next checkpoint after green gate

Open Advanced Activity in the real app and judge the visual hierarchy. Based on that screenshot/check:

1. decide whether `Sessione` becomes a top-level Create kind (`Registra sessione`) in addition to being an Activity execution child/context;
2. wire Structure authoring only after choosing the exact canonical representation for sub-Activity versus Session intent;
3. design canonical `Suddivisa` multi-placement creation and duration derivation;
4. implement placement protection against both manual accidental moves and Dante automation, then define post-create unlock/edit UX;
5. continue with Event Advanced separately so Activity-specific execution semantics do not leak into Event.