# Timeline / Temporal-Operational — B02-E manual userTest

- **Status:** READY / NOT YET EXECUTED
- **Workstream branch:** `feature/timeline-temporal-operational`
- **Scope:** B02-E form completeness, precision, DST-facing authoring, rendering, direct Schedule interaction and closure acceptance
- **Data class:** disposable synthetic test data only
- **CI:** deliberately excluded; CI remains separately authorized
- **Important:** this protocol extends the already-approved B02-A/B/C/D userTest. It does not replace that evidence and it does not authorize B03/Event Core.

## 1. Acceptance boundary

This protocol judges the real product surface against canonical backend/PostgreSQL truth:

```text
production web build
→ HTTPS preview
→ real FastAPI
→ dante_runtime
→ fresh migrated PostgreSQL 18.6
→ synthetic account only
```

The semantic boundaries under test remain:

```text
Activity != Schedule
Schedule != Actual
planned != happened
current placement != latest row
unscheduled != deleted
Undo != DB rewind
floating local != named-zone local != absolute instant
date span != coarse local period
coarse precision != fabricated clock time
```

Absolute placement is intentionally not exposed as a primary end-user Create mode in B02-E. Its API/runtime/read-model behavior is automated evidence, not a hidden UI mode to manufacture for this manual protocol.

## 2. Preconditions

From repository root:

```bash
git status -sb
git branch --show-current
git rev-parse HEAD
```

Expected branch:

```text
feature/timeline-temporal-operational
```

The run must use a clean worktree and a disposable full-stack database.

Start the isolated stack with one control id:

```bash
export DANTE_E2E_CONTROL_ID=temporal-b02-e-usertest
uv run --project apps/backend python tooling/run-access-auth-stack.py
```

Open:

```text
https://127.0.0.1:4173
```

Use the synthetic account only:

```text
email: synthetic.user@example.com
password: correct horse battery staple
```

Set the product locale to Italian and use Europe/Rome as the browser/effective timezone. After every mutation, wait for the authoritative Timeline/Planning Tray reread before judging the result.

## 3. Proof A — exact floating-local `Da / A`

1. Open `+` and keep `Attività` selected.
2. Choose `Orario`.
3. Keep `Riferimento orario = Ora locale`.
4. Choose a visible date in the current Timeline window.
5. Set `Da 11:30` and `A 12:15`.
6. Verify the UI shows the derived duration `(45 min)` rather than asking for a primary duration value.
7. Submit once.
8. Wait for canonical reload.

Expected:

- exactly one Activity/Schedule card appears;
- rendered start/end are 11:30–12:15;
- reload preserves the same card once;
- no Activity estimated-effort field becomes Schedule duration;
- no Actual/Session fact is created by placement.

## 4. Proof B — date-span / all-day

1. Create a second unique Activity.
2. Choose `Tutto il giorno` and one date in the visible window.
3. Submit once and wait for canonical reload.

Expected:

- the Activity renders in the date/all-day lane;
- it does not receive a fabricated timed-grid position;
- no clock interval is presented as canonical truth;
- reload preserves it exactly once.

## 5. Proof C — coarse accepted precision

1. Create a third unique Activity.
2. Choose `Fascia`.
3. Choose a visible date and `Pomeriggio`.
4. Submit once and wait for canonical reload.

Expected:

- the Activity renders in the date/coarse lane;
- the card exposes `Pomeriggio`/coarse meaning;
- there is no fabricated `14:00–18:00` or other exact clock geometry/text;
- reload preserves the coarse period exactly once.

Then use `Riporta nel Planning Tray` on this coarse item.

Expected:

- removal is immediate; there is no confirmation dialog;
- the same Activity returns to Planning Tray after canonical refresh;
- the visible `Annulla` action restores a new accepted current placement;
- the restored item remains coarse `Pomeriggio` after reload.

## 6. Proof D — named-zone authoring retains source intent

1. Create a fourth unique Activity.
2. Choose `Orario`.
3. Set `Riferimento orario = Fuso specifico`.
4. Set `Fuso orario = Europe/Rome`.
5. Use an unambiguous local interval, for example 10:10–10:40 on a visible date.
6. Submit once and wait for canonical reload.

Expected:

- the item renders once at the effective viewing coordinates;
- `Europe/Rome` remains available as source-zone metadata where the card exposes it;
- reload does not re-resolve or drift the accepted instant;
- editing/moving the item does not silently convert it to floating-local.

## 7. Proof E — explicit DST gap decision

Use the Europe/Rome spring-forward date `2026-03-29`.

1. Open a new Activity with `Orario` + `Fuso specifico` + `Europe/Rome`.
2. Set a source wall-clock interval beginning at `02:30`, which is nonexistent in Europe/Rome on that date.
3. Keep `Ora ambigua/non esistente = Chiedi correzione` and submit.

Expected:

- the operation is rejected truthfully;
- no canonical Timeline success/card is fabricated.

Repeat with a new unique title and choose `Usa la soluzione successiva`.

Expected:

- the operation may be accepted using the explicit supported DST decision;
- the source wall-clock intent remains `02:30`; it is not rewritten in canonical source semantics to the normalized resolved wall time;
- after reload, accepted rendering is stable.

This proof is about explicit source-intent/disambiguation behavior; it is not permission to reinterpret a DST gap silently.

## 8. Proof F — overlap decision remains explicit

Use the Europe/Rome fall-back date `2026-10-25` and local time around `02:30`.

1. Create one named-zone Activity with `Usa la soluzione precedente`.
2. Create a second uniquely titled named-zone Activity using `Usa la soluzione successiva`.

Expected:

- both choices are explicit user decisions;
- acceptance does not collapse them into one inferred instant;
- reload keeps each accepted result stable;
- the original source local coordinate remains distinguishable from the resolved instant.

## 9. Proof G — direct exact drag is a Schedule revision

Use a currently scheduled exact Activity.

1. Drag it to a different exact time using the normal Timeline gesture.
2. Wait for the governed mutation and authoritative reread.
3. Reload.

Expected:

- the same Activity identity and Schedule identity remain;
- a new accepted placement becomes current;
- the old placement remains history;
- the temporal form is preserved;
- no Session/Actual is recorded;
- no optimistic fake success remains if the mutation fails.

## 10. Proof H — cross-midnight exact interval

Create an exact Activity whose explicit `Da / A` crosses midnight, for example 23:30 → 00:30 on the following date.

Expected:

- authoring accepts one exact Schedule interval rather than two canonical Schedules;
- Timeline may split rendering view-side across days, but both rendered pieces refer to the same Schedule identity;
- reload preserves one canonical interval without duplication.

## 11. Proof I — stale/conflict truthfulness after B02-E

Repeat the already-approved two-tab stale-state pattern using an item created through one of the B02-E forms.

Expected:

- stale revision/unschedule is rejected;
- no local success is fabricated;
- authoritative reread wins;
- operation id reuse never becomes identity reuse or last-write-wins.

## 12. Firefox critical interaction pass

Run the same full-stack browser acceptance in Firefox for the critical Timeline interaction subset:

- open/focus scheduled card;
- exact drag;
- anchored time editor;
- `Riporta nel Planning Tray`;
- visible guarded `Annulla`;
- reload reconciliation.

Expected: no pointer/focus regression versus the frozen T1 interaction contract.

## 13. Approval record

Do not edit this section to PASS before the real run.

```text
Proof A — floating-local Da/A + reload                     PENDING
Proof B — date-span lane + reload                          PENDING
Proof C — coarse precision + unschedule/Undo + reload      PENDING
Proof D — named-zone source intent + reload                PENDING
Proof E — DST gap reject/later                             PENDING
Proof F — DST overlap earlier/later                        PENDING
Proof G — direct exact drag + reload                       PENDING
Proof H — cross-midnight same Schedule identity            PENDING
Proof I — stale/conflict truthfulness                      PENDING
Firefox critical interaction pass                         PENDING

B02-E userTest — PENDING
```

B02 may be marked CLOSED only after the required E4 automated/local-E2E/Firefox/manual evidence is executed and the live ledger/handoff are reconciled. CI remains a separate authorization gate.