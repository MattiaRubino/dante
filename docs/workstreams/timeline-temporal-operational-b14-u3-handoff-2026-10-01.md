# B14 + B07 — U3 Create / Planning handoff — 2026-10-01

- **Branch:** `feature/timeline-temporal-operational`
- **Status:** ACTIVE — implementation candidate; latest user-local proof is `899f9260`, later changes require a new local gate
- **Current candidate HEAD before this document update:** `856d59f28894dd5aadd72cee1c1a059a639412af`
- **U2 canonical closure:** `docs/workstreams/timeline-temporal-operational-b14-u2-closure-2026-10-01.md`
- **UI ledger:** `docs/workstreams/timeline-temporal-operational-b14-ui-consolidation-2026-09-30.md`
- **CI:** not authorized; user runs tests locally in `~/projects/dante`

## 1. Proven checkpoint carried forward

User-local gate at `899f9260`:

```text
web typecheck                                  PASS
Temporal Create composer tests                 PASS
Temporal Create U2 entry tests                 PASS
Temporal Create top/U1 tests                   PASS
focused total                                  16/16 PASS
```

Earlier in the same cycle the unified planning-tray vertical was also proven locally:

```text
web focused tests                              13/13 PASS
backend Ruff                                   PASS
planning-tray PostgreSQL                       2/2 PASS
larger backend focused gate                    10/10 PASS
OpenAPI/generated planning-tray client         generated and committed at a9dbdbe2
```

Do not describe later commits as proven until the user reruns the local gate.

## 2. Product decisions frozen in U3 so far

### Quick Create

- Activity and Event both support `Orario`, `Tutto il giorno`, `Da collocare`.
- `Da collocare` hides `Ripeti` and clears any recurrence previously staged in the draft.
- `Da collocare` does not show `Ricorda`.
- `Tutto il giorno` now exposes the same explicit pair for Activity and Event: `Data inizio | Data fine`; no hour controls and no timezone control are invented for a date-span.
- `Orario` keeps the compact globe in Quick; named-zone time is the default product path so Schedule-relative Reminder can be configured before submit.
- `Ricorda` is configured before Activity/Event creation. Persistence happens after accepted Schedule authoring only because the canonical Reminder targets the resulting `schedule_ref`; that sequencing is an internal command detail, not a user-visible prerequisite.
- Reminder delivery/push/email/desktop notification execution is deliberately deferred until the rest of the product surface is settled. B11-C remains Reminder configuration, not delivery claim.
- Quick footer has `Opzioni avanzate` + `Aggiungi`; header `X` owns close/cancel behavior.

### Life Area / color

- Life Area remains optional.
- Selecting an item color before typing a new Life Area must preserve that exact visible color when the new Life Area is staged; no reset to DANTE orange.
- Color picker is one floating portal panel; popup positioning is shifted upward so the palette/picker fits visually beside the Create card rather than hanging below it.
- The old Advanced `Aspetto` panel is superseded by the canonical Quick Life Area + color controls and is removed, including its obsolete component/styles.

### Advanced

- Advanced is a central viewport surface, not an expansion of the right rail.
- Quick and Advanced share the same draft; switching surfaces must not lose entered data.
- Quick timezone = compact globe; Advanced timezone = explicit `timeMode` + `timeZoneId` controls over the same state. The Quick globe is hidden while Advanced is active.
- Reminder has one product control (`Ricorda`) in the shared/main Create fields. Advanced must not expose a second Reminder/Promemoria copy.
- `Verifica esito` is separate from Reminder. It owns `confirmation.outcomePolicy`; for now only the actually supported inherited rule is exposed. Unsupported future policies are not shown as disabled fake choices.
- Advanced recurrence and `Verifica esito` are independent sections: Event recurrence or an Activity recurrence does not suppress outcome-verification policy.
- `Verifica esito` is not canonical B10 `Confirmation`; B10 Confirmation remains an attestation on an exact Outcome MaterialState.

### Planning tray / `Da collocare`

One product container now includes:

```text
Activity with no current accepted placement
Event never placed
Event postponed with retained Schedule identity
```

The UI may unify them, but Domain identity/history remain distinct.

Current planning-tray cards still expose Session / Actual / Outcome / Confirmation / Reconciliation for Activity through the historical wiring. This is acknowledged as poor product placement, but **must not be removed yet**. Move those capabilities to their intended destination first, then remove them from `Da collocare` in the same checkpoint.

## 3. Semantic distinctions that must remain intact

```text
Schedule != Session != Actual
Session != Actual != Outcome
Actual != Outcome != Confirmation
Confirmation != outcome verification policy
Reminder != outcome verification
Reminder configuration != notification delivery
Plan != Activity
Step != Activity
Event agenda/decomposition != Actual/Outcome/Confirmation/Reconciliation
```

`Verifica esito` in Create means policy for how Dante should later ask/infer/review realization/outcome. Canonical B10 `Confirmation` means contextual attestation of one exact Outcome version. Do not merge these names or models.

## 4. Candidate commits after the last proven gate

```text
480162a0  preserve selected color while staging new Life Area + lift color popup
da4d703d  Quick all-day/Reminder visibility consolidation
d4d48733  Activity all-day request uses explicit end date too
a7839d51  remove Advanced Aspetto rendering
1a6cbab8  regressions: color preservation, all-day pair, no Reminder in unplaced
9876d146  Advanced hides compact globe and uses explicit timezone section
c62d6c2c  separate Verifica esito from Reminder
a7e1888e  remove Advanced appearance dependency
edcc3b34  delete superseded appearance component
c830a9f1  delete superseded appearance styles
12f85f6a  mark explicit Advanced timeMode field
b06b5542  lock Advanced timezone / verification separation in tests
856d59f2  make recurrence and outcome verification independent sections
```

These commits are implementation candidate only until the user runs the next local gate.

## 5. Immediate next local gate

Run locally only:

```bash
cd ~/projects/dante
git pull --ff-only origin feature/timeline-temporal-operational

pnpm --filter @dante/web typecheck

pnpm --filter @dante/web exec vitest run \
  src/features/temporal-create/ui/temporal-create-entry-u2.test.tsx \
  src/features/temporal-create/ui/temporal-create-top-u1.test.tsx \
  src/features/temporal-create/ui/temporal-create-composer.test.tsx

git status --short
```

No OpenAPI regeneration is expected for this candidate because it changes only web/product organization.

## 6. Real-app checks after automated green

Verify in this order:

1. pick a non-default color, then type a new Life Area name: chosen color stays selected and is persisted with the new area;
2. color panel opens as one coherent floating panel and fits beside the Create card;
3. `Da collocare` for Activity and Event has neither `Ripeti` nor `Ricorda`;
4. `Tutto il giorno` for Activity and Event shows exactly two DANTE date pickers and no hour controls;
5. Reminder is selectable before submit for a normal named-zone timed Activity/Event;
6. Advanced opens centrally, preserves draft, hides the compact globe, and exposes explicit time reference/timezone;
7. Advanced has one `Ricorda` control only and a separate `Verifica esito` section;
8. Event/recurring Activity can show recurrence and `Verifica esito` independently;
9. `Aspetto` is absent.

## 7. Next product work after this checkpoint

Do not jump directly to deleting historical controls. Continue incrementally:

1. finish Activity vs Event Advanced information architecture;
2. place B04 temporal constraints / movement policy into the Advanced product surface;
3. decide final destination for Session runtime (`Avvia/Pausa/Riprendi/Termina`);
4. design destination for Actual / Outcome / canonical Confirmation / Reconciliation, then remove those controls from `Da collocare` in the same move;
5. integrate the remaining advanced recurrence/organization/responsibility/work-structure capabilities without collapsing their Domain distinctions;
6. only near the end define Reminder delivery channels / notification execution.

## 8. Repository discipline

- PostgreSQL remains canonical authority.
- Published migrations are immutable and fixes are forward-only.
- Generated API client is never edited manually.
- User runs all gates locally; no CI/GitHub Actions.
- Fetch branch HEAD before every write and keep frequent checkpoints.
- Do not leave superseded product panels wired in parallel when an equivalent destination has been accepted; remove dead UI code/styles in the same consolidation checkpoint.
