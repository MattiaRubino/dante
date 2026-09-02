# DANTE — Temporal Create C1 Manual Acceptance

**Status:** FINAL HUMAN GATE — NOT YET EXECUTED  
**Date:** 2026-09-02  
**Branch:** `feature/home-timeline`  
**Validated implementation / harness candidate:** `2b910092ecd70de74338427924666a965938ba9f`  
**Automated evidence:** Frontend CI `33660540265` / #676 — **FULL PASS**

## 1. Purpose

This is the **single coherent final manual acceptance** for C1. It is intentionally one end-to-end human pass after automated closure, not a collection of micro-tests to repeat after every code change.

The flow under acceptance is:

```text
manual + / contextual Timeline gesture
→ Quick
→ Expanded
→ Full
→ Activity semantics
→ Da collocare / Planning Tray
→ Event semantics
→ Context / appearance
→ recurrence
→ external-owner seams
→ validation / Undo / focus
→ all-day
→ mobile
→ frozen Timeline smoke
```

Only explicit user approval closes C1.

## 2. Before starting

Sync the Timeline worktree only after the documentation descendant containing this protocol is itself confirmed CI-green:

```bash
cd /home/mattia/projects/dante-timeline
git pull --ff-only
git status --short --branch
git rev-parse HEAD
```

Expected:

- branch `feature/home-timeline`;
- clean worktree;
- HEAD is the final CI-green documentation descendant of `2b910092ecd70de74338427924666a965938ba9f`.

Start the normal web development environment used for this repository and open `/home`.

Do **not** judge backend persistence/provider execution in this protocol: C1 intentionally stops before those runtimes.

## 3. Acceptance rule

A PASS requires all of the following:

- no visual corruption or obviously prototype-grade control;
- no raw translation/debug keys;
- no misleading fake success;
- `+` behaves as a manual authoring surface, not chat/AI/NL/voice input;
- no Activity recurrence editor;
- no lost draft when moving Quick ↔ Expanded ↔ Full;
- no fake fixed placement for a flexible/unplaced Activity;
- `Da collocare`, placement, scheduling constraint and expected duration remain distinct concepts;
- Context and appearance override remain distinct;
- Event recurrence remains understandable despite its depth;
- focus/cancel/discard interactions feel deliberate;
- Planning Tray placement/delete Undo restores real prior state;
- all-day Event remains structurally outside the timed grid;
- mobile Full Create and Planning Tray are usable and contained;
- normal frozen Timeline interactions still feel unchanged.

If one material defect is observed, record exactly:

```text
surface
steps
expected
actual
viewport/browser if relevant
```

Do not compensate manually for a defect and call it PASS.

---

# 4. Desktop — manual Quick Create and Undo

Use a desktop viewport around 1360–1440 px wide.

1. Open Home.
2. Click the Timeline `+`.
3. Confirm Create opens focused on the title.
4. Confirm the Quick surface is calm and does not look like a full configuration form.
5. Confirm there is **no chat prompt, natural-language instruction box, AI command affordance, microphone/voice control or “ask DANTE” input inside Create**.
6. Enter a simple Activity title, for example `Studiare inglese`.
7. Choose a visible time, ordinary duration and Context.
8. Create it.

Expected:

- composer closes;
- placed Activity appears in the Timeline;
- created projection is revealed/focused when applicable;
- success feedback describes the actual local creation;
- Undo is available.

Use Undo.

Expected:

- created projection disappears;
- no stale card/preview remains;
- no second/fake mutation feedback appears.

Manual-only failure condition: if the `+` expects or encourages commands such as `Dentista domani alle 17`, C1 is a manual FAIL.

---

# 5. Dirty draft / discard / focus

1. Open `+` again.
2. Type a title and change at least one field.
3. Press Escape.

Expected:

- clear discard confirmation appears;
- draft remains visible/preserved behind the confirmation;
- underlying form is not interactable while confirmation is active;
- Tab cycles only through confirmation actions.

4. Press Escape or choose `Continua a modificare`.

Expected:

- confirmation closes;
- focus returns to the relevant editor control;
- draft values remain unchanged.

5. Close again and choose `Scarta`.

Expected:

- composer closes;
- focus returns to the original `+` opener;
- no Create item appears.

---

# 6. Progressive disclosure — one draft

1. Open a new Activity.
2. Enter a distinctive title.
3. Go from Quick to `Dettagli e pianificazione`.
4. Change expected duration to a non-preset exact value, for example `195` minutes.
5. Set a planning constraint and execution structure.
6. Open `Editor completo`.
7. Set a deeper fallback/session/confirmation/reminder value.
8. Return to Expanded and then back to Full.

Expected:

- title and every modified value survive each surface transition;
- no second draft is created;
- layout remains grouped by meaning rather than becoming a giant settings wall;
- exact 195-minute duration remains intact.

---

# 7. Activity semantic truth

Inspect a new Activity in Expanded/Full and verify these concepts can be represented sensibly where shown:

- fixed/timed placement;
- open / without accepted placement;
- bounded window;
- deadline-constrained;
- preferred window;
- movement policy;
- indivisible vs splittable;
- minimum/max session intent;
- preparation/recovery/spacing;
- fallback policy;
- confirmation/review/reminder policy.

Then create an Activity using `Aperta, senza collocazione` or another flexible scheduling constraint.

Expected:

- creation succeeds truthfully as planning intent;
- no arbitrary exact Timeline slot is fabricated;
- the Activity becomes available in `Da collocare`;
- feedback remains truthful about the unplaced state.

### Mandatory recurrence ownership

Inspect Activity in Expanded and Full.

Expected:

- **there is no `Modello di ricorrenza` control for Activity**;
- UI explains that persistent repetition belongs to Routine;
- Routine is represented as an owning-vertical handoff/dependency;
- there is no generic `repeat` checkbox;
- there is no generic `Tag` field pretending an unsupported owner model.

Any direct Activity recurrence editor is a manual FAIL.

---

# 8. `Da collocare` / Planning Tray — one coherent pass

Create two unplaced Activities with visibly different titles and durations, for example:

```text
Preparare portfolio — 60 min
Rivedere note — 30 min
```

Open `Da collocare` using the Timeline action `Apri attività da collocare`.

Expected:

- badge/count reflects pending unplaced Activities;
- tray clearly explains that these Activities exist but have no accepted slot;
- each item shows useful Context/tone/duration/planning information;
- search is available;
- nothing is silently materialized in the timed Timeline.

## A. Search

Search for one title fragment.

Expected:

- list filters predictably;
- clearing search restores the full list;
- no Activity identity changes.

## B. Quick placement → Undo

For `Preparare portfolio`, use the explicit `Colloca` action or double-click the item, choose a valid date/time and confirm `Colloca nella Timeline`.

Expected:

- the item leaves `Da collocare`;
- the same Activity appears at the chosen Timeline slot;
- its identity/state transition feels like placement, not delete-and-recreate;
- Undo is available.

Use Undo.

Expected:

- placed card disappears from the Timeline;
- **the same Activity returns to `Da collocare`**;
- badge/count is restored;
- no duplicate is created.

## C. Drag placement → live preview → Undo

Drag `Preparare portfolio` from the tray onto a visible Timeline area.

Expected during drag:

- Timeline enters an obvious planning foreground mode;
- a live drop preview appears;
- preview says `Rilascia qui` and shows a snapped start/end time;
- the preview follows valid Timeline geometry;
- no native browser drag ghost appears.

Drop it.

Expected:

- exactly one placement mutation occurs;
- item leaves tray and appears in Timeline;
- Undo is available.

Use Undo and confirm it returns to the tray again.

## D. Drag cancellation with Escape

Start dragging `Rivedere note` into the Timeline but press Escape before dropping.

Expected:

- planning foreground mode clears;
- preview disappears;
- releasing the pointer afterwards does not commit placement;
- `Rivedere note` remains in `Da collocare`;
- no Undo/fake mutation is emitted.

## E. Explicit delete → Undo

Use the item overflow/delete action on an unplaced Activity.

Expected:

- explicit confirmation asks whether to delete the Activity;
- copy makes clear this is local workspace behavior and does not simulate backend deletion.

Confirm delete.

Expected:

- item disappears;
- Undo is available.

Use Undo.

Expected:

- the same unplaced Activity returns;
- no duplicate or fabricated placement appears.

Manual FAIL conditions include any of these:

- an unplaced Activity is silently placed at an arbitrary time;
- placement creates a second Activity instead of moving state of the same one;
- Undo after placement does not restore unplaced state;
- Escape still allows a dragged item to commit;
- delete has no explicit confirmation;
- tray language collapses `Da collocare`, `Collocazione`, `Vincolo temporale` and `Durata prevista` into one vague concept.

---

# 9. Context creation and appearance non-collapse

## A. Page-local Context creation

Open Create and use the Context picker to create a distinctive local Context, for example `Studio`, choosing a visible tone.

Expected:

- newly created Context becomes selectable immediately;
- Timeline group/filter representation is created consistently;
- creating the same normalized name again does not produce a duplicate Context;
- existing Context tone/identity wins rather than silently creating a conflicting duplicate.

## B. Appearance override

1. Create/edit a draft with Context `Focus / lavoro profondo`.
2. Observe the candidate preview before choosing an appearance override.
3. Open Expanded and find `Aspetto`.
4. Confirm inheritance names the selected Context.
5. Choose a manual color override, for example `Rosso`.
6. Open Full, return to Expanded, then create.

Expected:

- appearance override survives surface transitions;
- title and Context remain unchanged;
- preview/card changes presentation only;
- Timeline card still belongs to `Focus / lavoro profondo`;
- activating `Urgenze` does **not** include the card merely because it is red;
- activating `Focus` still includes it while preserving the red/custom appearance.

Any behavior where custom color changes Context/group/filter membership is a manual FAIL.

---

# 10. Owning-vertical handoff truth

In Full Create inspect external-owner options.

Expected targets:

`Project`, `Goal`, `Routine`, `Program`, `World`, `Template`, `Reminder`, `Block`, `Asset`.

Expected behavior:

- all are visibly unavailable/deferred owner dependencies;
- they do not navigate somewhere fake;
- clicking cannot claim an object was created;
- wording makes owner responsibility clear rather than looking accidentally broken.

---

# 11. Event base grammar

Open a fresh Create and switch to Event.

Verify:

- Event cannot be `unscheduled`;
- start/end/duration behavior is Event-specific;
- all-day can represent a multi-day Event;
- floating-local vs named-zone semantics are understandable;
- IANA timezone field appears when appropriate;
- location, availability and visibility are distinct;
- purpose, expected outcome and agenda are grouped meaningfully in Full;
- `decision required` is intent, not an executed decision.

Enter realistic meeting/call data.

---

# 12. Provider/collaboration truth

In Full Event fill some of:

- required participant;
- optional participant;
- room/resource;
- pre-read;
- conference provider intent.

Expected:

- UI clearly says these are preserved intents/seams;
- no invitation is reported sent;
- no room is reported booked;
- no conference link is fabricated;
- visibility is not presented as product ACL/sharing authority.

Any fake provider success is a manual FAIL.

---

# 13. Event recurrence — four CP6 families

This is one guided inspection, not four separate acceptance sessions.

Open Event → Expanded/Full and find `Modello di ricorrenza`.

Expected choices:

1. `Non si ripete`;
2. Calendar / wall-clock;
3. elapsed interval;
4. quota per period;
5. cyclic positional.

## A. Calendar / wall-clock

Verify frequency options include:

- daily;
- weekly;
- monthly;
- monthly by ordinal weekday;
- yearly.

For weekly, select multiple weekdays.

For monthly ordinal, configure something equivalent to `ultimo venerdì`.

For monthly/yearly anchored forms, verify UI communicates that authored civil date remains the recurrence anchor.

## B. Elapsed interval

Switch to elapsed interval and enter a valid elapsed duration.

Expected: recurrence specification only; no claim that browser runtime is evaluating future Occurrences.

## C. Quota per period

Switch to quota and verify:

- count;
- day/week/month/year period;
- every N periods;
- Full allows period frame;
- frame choices include local, named-zone and UTC/absolute basis;
- weekly period exposes week start;
- named-zone frame exposes period timezone;
- explanatory copy says period boundaries do not silently follow device timezone.

## D. Cyclic positional

Set cycle length 4 and add at least two active positions, for example 1 and 3.

Expected:

- multiple active positions can coexist;
- positions are human-readable 1-based values;
- invalid/duplicate/out-of-range additions are not accepted as valid state;
- removing a position behaves predictably;
- at least one active position remains.

## E. Termination and surface round-trip

Test at least one recurrence end mode (`until date` or `count`), then:

1. return Full → Expanded;
2. open Full again.

Expected:

- family, deep values and termination remain intact;
- no recurrence state silently resets;
- browser still does not show recurrence-generated Occurrences merely because a specification exists.

---

# 14. Zoned time sanity

Create a zoned Event using `Europe/Rome`.

Change start/end/duration on a normal date.

Expected:

- end and duration remain coherent;
- timezone stays attached to Event intent.

No need to manually reproduce DST transition math; that is already covered by blocking automated time contracts. This step checks UI presentation/editing only.

---

# 15. All-day multi-day Event vs unplaced Activity

## Event

Create an all-day Event spanning more than one date.

Expected:

- it behaves as a true date span;
- it appears in the dedicated all-day strip in the Timeline header;
- the all-day strip is visually separate from the timed grid;
- it does not look like a midnight timed card;
- range continuation across dates feels coherent.

Use Undo if convenient and confirm it disappears cleanly.

## Activity

Create an unplaced Activity.

Expected:

- it remains valid without exact placement;
- no arbitrary slot is invented;
- it belongs in `Da collocare`, not the all-day Event strip.

These two states must feel semantically different.

---

# 16. Contextual manual Timeline creation

These gestures are manual structured prefill. They must not become interpretation/AI input.

## Double-click

On an empty visible Timeline area, double-click a sensible time.

Expected:

- Create opens with contextual date/time defaults;
- fields remain manually editable;
- cancelling a clean contextual Create returns focus to Timeline rather than global `+`.

## Shift-drag range

On an empty visible Timeline area, Shift-drag a meaningful vertical range.

Expected:

- Create opens;
- duration reflects selected range at a sensible snapped value;
- no existing card is accidentally captured;
- no native drag ghost appears.

Repeat after previously opening/closing Create once. Timeline virtualization/browser scrolling must not make the second gesture dead.

---

# 17. Validation / recovery

Create an Activity with an invalid advanced relationship, for example expected duration 60 minutes but minimum session 120 minutes.

Submit.

Expected:

- composer stays open;
- meaningful validation appears;
- focus moves to the actual invalid control;
- title and other draft values remain intact;
- no partial projection is committed.

Correct it and continue with the same draft.

For Event recurrence, also try one obviously invalid deep value if convenient, such as an invalid named-zone timezone or invalid termination date/count.

Expected: same non-destructive recovery behavior.

---

# 18. Mobile — Full Create + Planning Tray

Use a 390×844-equivalent viewport/devtools device.

## Full Create

Open Create → Expanded → Full.

Expected:

- Full becomes a usable mobile full-screen editor;
- no horizontal page overflow;
- fields/actions remain reachable;
- recurrence controls do not overflow disastrously;
- appearance controls remain usable;
- close/discard remains operable;
- no desktop-only floating geometry blocks the flow;
- no AI/NL/voice affordance appears.

## Planning Tray

Ensure at least one unplaced Activity exists, then open `Da collocare`.

Expected:

- tray is a bounded bottom sheet within the viewport;
- no horizontal page overflow;
- unplaced item remains visible/reachable;
- search/placement actions remain usable;
- tray does not obscure the application in an obviously broken way.

Pointer drag placement is not required as a mobile-specific human gate; its semantics are already validated in desktop/manual and automated tests.

---

# 19. Frozen Timeline smoke

After Create testing, do a short normal Timeline interaction smoke:

- click/focus an existing card;
- move/edit time using an already accepted interaction;
- Undo;
- use `Ora` / Now;
- open/close calendar/time controls if convenient.

Expected:

- established T1 behavior feels unchanged;
- first drag is not swallowed;
- no native drag ghost;
- Undo corresponds to a real mutation;
- Create/Planning Tray have not re-authored Timeline interaction grammar.

Firefox's critical frozen Timeline interaction contract is already automated and PASS on CI #676; this is only a human regression feel-check.

---

# 20. Final decision

If a material issue exists, report it precisely and do **not** approve C1.

If the complete flow is accepted, send exactly or equivalently:

```text
C1 MANUAL PASS — APPROVED
```

Only then may repository status transition to:

```text
C1 TEMPORAL CREATE
FROZEN / CLOSED
```

and only then may work begin on:

```text
C2 — Card → structured Detail
```
