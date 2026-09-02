# DANTE — Temporal Create C1 Manual Acceptance

**Status:** FINAL HUMAN GATE — NOT YET EXECUTED  
**Date:** 2026-09-02  
**Branch:** `feature/home-timeline`  
**Implementation candidate under acceptance:** `7028633921d1b438bd04961a718457afd82ccc13`  
**Automated evidence:** Frontend CI `33635389124` / #632 — FULL PASS

## 1. Purpose

This is the **single coherent final manual acceptance** for C1. It is intentionally not a collection of micro-tests to run after every code change.

The goal is to verify the complete user-facing manual Create capability after automated engineering closure:

```text
manual + / contextual Timeline gesture
→ Quick
→ Expanded
→ Full
→ Activity semantics
→ Event semantics
→ Context / appearance
→ recurrence
→ external-owner seams
→ validation / Undo / focus
→ mobile
→ frozen Timeline smoke
```

Only explicit user approval closes C1.

## 2. Before starting

Sync the Timeline worktree only after the **final documentation descendant** is confirmed CI-green:

```bash
cd /home/mattia/projects/dante-timeline
git pull --ff-only
git status --short --branch
git rev-parse HEAD
```

Expected:

- branch `feature/home-timeline`;
- clean worktree;
- HEAD is the final CI-green documentation descendant of implementation candidate `7028633921d1b438bd04961a718457afd82ccc13`.

Start the normal web development environment used for this repository and open `/home`.

Do not judge backend persistence/provider behavior in this protocol: C1 intentionally stops before those runtimes.

## 3. Acceptance rule

A PASS requires all of the following:

- no visual corruption or obviously prototype-grade control;
- no raw translation/debug keys;
- no misleading fake success;
- `+` behaves as a manual authoring surface, not chat/AI/NL input;
- no Activity recurrence editor;
- no lost draft when moving Quick ↔ Expanded ↔ Full;
- no fake fixed placement for flexible Activity;
- Context and appearance override remain distinct;
- Event recurrence remains understandable despite its depth;
- focus/cancel/discard interactions feel deliberate;
- mobile Full Create is usable and contained;
- normal Timeline interactions still feel unchanged.

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

# 4. Desktop pass — manual Quick Create and Undo

Use a desktop viewport around 1360–1440 px wide.

1. Open Home.
2. Click the Timeline `+`.
3. Confirm Create opens focused on the title.
4. Confirm the Quick surface is calm and does not look like a full configuration form.
5. Confirm there is **no chat prompt, natural-language instruction box, AI command affordance, microphone/voice control or “ask DANTE” input inside Create**.
6. Enter a simple Activity title, for example `Studiare inglese`.
7. Choose a visible time and ordinary duration/Context.
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

Manual-only failure condition:

- if the `+` expects or encourages commands such as `Dentista domani alle 17`, C1 is a manual FAIL.

---

# 5. Dirty draft / discard / focus

1. Open `+` again.
2. Type a title and change at least one field.
3. Press Escape.

Expected:

- a clear discard confirmation appears;
- draft is still visible/preserved behind the confirmation;
- underlying form is not interactable while confirmation is active;
- Tab cycles only through confirmation actions.

4. Press Escape or choose `Continua a modificare`.

Expected:

- confirmation closes;
- focus returns to the control from which closing was attempted when still available;
- draft values remain unchanged.

5. Close again and choose `Scarta`.

Expected:

- composer closes;
- focus returns to the original `+` opener;
- no Create item appears.

---

# 6. Progressive disclosure / same draft

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

Use the same/new Activity and inspect its planning sections.

Verify these concepts can be represented sensibly where shown:

- fixed/timed placement;
- open / da pianificare;
- bounded window;
- deadline-constrained;
- preferred window;
- movement policy;
- indivisible vs splittable;
- minimum/max session intent;
- preparation/recovery/spacing;
- fallback policy;
- confirmation/review policy.

Then make an Activity `Da pianificare` / open or otherwise flexible and create it.

Expected:

- Create succeeds truthfully as planning intent;
- it is not fabricated into an arbitrary exact Timeline slot;
- feedback identifies it as `Da pianificare` where appropriate.

### Mandatory recurrence ownership check

Inspect Activity in Expanded and Full.

Expected:

- **there is no `Modello di ricorrenza` control for Activity**;
- UI explains that persistent repetition belongs to Routine;
- Routine appears as an owning-vertical handoff/dependency;
- there is no generic `repeat` checkbox;
- there is no generic `Tag` field pretending an unsupported owner model.

Any direct Activity recurrence editor is a manual FAIL.

---

# 8. Context and appearance non-collapse

This verifies that presentation does not silently become category/organization semantics.

1. Open a new Activity or Event.
2. Give it a distinctive title, for example `Focus colore rosso`.
3. Select Context `Focus / lavoro profondo`.
4. Observe the candidate preview before choosing an override.

Expected:

- default visual tone follows the selected Context.

5. Open Expanded and find `Aspetto`.
6. Confirm the inheritance option names the selected Context.
7. Confirm manual override choices are **color words** such as `Viola`, `Ciano`, `Verde`, `Ambra`, `Rosa`, `Rosso`, not category names such as Focus/Urgenze.
8. Choose `Rosso`.
9. Open Full, then return to Expanded.

Expected:

- red appearance survives the surface round-trip;
- title and Context remain unchanged;
- preview changes visual tone only.

10. Create the item.
11. Confirm the Timeline card still displays `Focus / lavoro profondo` as its Context while using the chosen visual tone.
12. Activate the `Urgenze` group filter.

Expected:

- the Focus item is hidden because it is **not** in the Urgenze Context merely because it is red.

13. Use `Ripristina gruppi e focus`.
14. Activate the `Focus` filter.

Expected:

- the item is visible;
- it remains visually red/custom;
- Context/filter membership remains Focus.

15. Reset and use Undo on the created item.

Any behavior where custom color changes Context/group/filter membership is a manual FAIL.

---

# 9. Owning-vertical handoff truth

In Full Create inspect `Altro tipo` / external-owner options.

Expected:

- Project, Goal, Routine, Program, World, Template, Reminder, Block and Asset are represented as unavailable/deferred owner dependencies;
- they do not navigate somewhere fake;
- clicking cannot claim that an object was created;
- wording makes ownership/dependency clear rather than looking broken.

The handoff contract itself is covered automatically; this manual step validates that the unavailable UI is understandable and product-quality.

---

# 10. Event base grammar

Open a fresh Create and switch to Event.

Verify:

- Event requires temporal placement;
- start/end behavior feels Event-specific rather than copied blindly from Activity;
- all-day can represent a multi-day Event;
- floating/local vs named-zone time semantics are understandable;
- IANA timezone field appears only when appropriate;
- location, availability and visibility are distinct concepts;
- purpose, expected outcome and agenda are grouped meaningfully in Full;
- `decision required` reads as intent, not as an executed decision.

Enter realistic data for a meeting/call.

---

# 11. Provider/collaboration truth

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

# 12. Event recurrence — four CP6 families

This is one guided inspection, not four separate acceptance sessions.

Open Event → Expanded/Full and find `Modello di ricorrenza`.

Expected family choices:

1. Calendar / ora civile;
2. Intervallo trascorso;
3. Quota per periodo;
4. Posizione ciclica;
5. plus `Non si ripete`.

## A. Calendar / wall-clock

Select calendar recurrence.

Verify frequency options include:

- daily;
- weekly;
- monthly;
- monthly by ordinal weekday;
- yearly.

For weekly, select multiple weekdays.

For monthly ordinal, configure something equivalent to `ultimo venerdì`.

For monthly/yearly anchored forms, verify UI communicates that the authored civil date is the anchor rather than presenting a mysterious DB rule.

## B. Elapsed interval

Switch to elapsed interval and enter a valid value.

Expected:

- simple elapsed duration authoring;
- no claim that browser runtime is evaluating future Occurrences.

## C. Quota per period

Switch to quota.

Verify:

- count;
- day/week/month/year period;
- every N periods;
- Full surface allows period frame;
- frame choices include local, named-zone and UTC/absolute basis;
- weekly period exposes week start;
- named-zone frame exposes period timezone;
- explanatory copy makes clear period boundaries do not silently follow device timezone.

## D. Cyclic positional

Switch to cyclic.

Set a cycle length such as 4 and add at least two active positions, for example 1 and 3.

Expected:

- multiple active positions can coexist;
- positions are human-readable 1-based values;
- invalid/duplicate/out-of-range values are not accepted as valid state;
- removing a position behaves predictably.

## Surface round-trip

After configuring a deep recurrence:

1. return from Full to Expanded;
2. open Full again.

Expected:

- family and deep values remain intact;
- no recurrence state silently resets.

The browser must not show generated Occurrences merely because a recurrence specification exists.

---

# 13. Zoned time sanity

Create a zoned Event using `Europe/Rome`.

Change start/end/duration in a normal date first.

Expected:

- end and duration remain coherent;
- timezone remains attached to Event intent.

No need to manually reproduce DST transition math; spring-forward/fall-back arithmetic is already a blocking automated unit contract. This manual step checks UI presentation and editing path only.

---

# 14. All-day multi-day Event vs unscheduled Activity

### Event

Create an all-day Event spanning more than one date.

Expected:

- it behaves as a true date span;
- it does not look like a timed midnight event.

### Activity

Create an unscheduled Activity.

Expected:

- it remains valid without exact placement;
- no arbitrary slot is invented.

These two cases must feel semantically different.

---

# 15. Contextual manual Timeline creation

These gestures are manual entry shortcuts. They must prefill known temporal context, not turn into interpretation/AI input.

## Double-click

On an empty visible Timeline area, double-click a sensible time.

Expected:

- Create opens with contextual date/time defaults;
- normal manual fields remain editable;
- cancelling a clean contextual Create returns focus to Timeline, not the global `+`.

## Shift-drag range

On an empty visible Timeline area, Shift-drag a meaningful vertical range.

Expected:

- Create opens;
- duration reflects selected range at a sensible snapped value;
- no existing card is accidentally captured;
- no native drag ghost appears.

This interaction must work after previously opening/closing Create as well; Timeline virtualization and page scrolling must not make the second gesture dead.

The final automated candidate explicitly hardens this scenario by resolving an actually visible Timeline interaction band across the Timeline viewport and browser viewport before exercising the gestures.

---

# 16. Validation/recovery

Create an Activity with an obviously invalid advanced relationship, for example expected duration 60 minutes but minimum session 120 minutes.

Submit.

Expected:

- composer stays open;
- meaningful validation appears;
- focus moves to the actual invalid control;
- title and other draft values remain intact;
- no partial projection is committed.

Correct it and verify the same draft can continue successfully.

---

# 17. Mobile Full Create

Use a 390×844-equivalent viewport/devtools device.

Open Create → Expanded → Full.

Expected:

- Full becomes a usable mobile full-screen editor;
- no horizontal page overflow;
- fields/actions remain reachable;
- deep Event recurrence controls remain understandable and do not overflow disastrously;
- appearance controls remain usable;
- close/discard remains operable;
- no desktop-only floating geometry blocks the flow;
- no AI/NL/voice affordance appears in the mobile version either.

---

# 18. Frozen Timeline smoke

After Create testing, do a short normal Timeline interaction smoke:

- click/focus an existing card;
- move/edit time using an already accepted interaction;
- Undo;
- use `Ora`/Now;
- open/close calendar/time controls if convenient.

Expected:

- established T1 behavior feels unchanged;
- first drag is not swallowed;
- no native drag ghost;
- Undo corresponds to a real mutation;
- Create has not re-authored Timeline interaction grammar.

Firefox's critical interaction contract is already automated and PASS on CI #632; this is only a human regression feel-check.

---

# 19. Final decision

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
