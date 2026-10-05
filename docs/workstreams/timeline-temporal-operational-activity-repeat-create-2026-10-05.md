# Activity Repeat — manual Create product boundary

- **Status:** ACCEPTED / CURRENT PRODUCT DECISION
- **Date:** 2026-10-05
- **Workstream:** B14 + B07 Product / UI Consolidation
- **Branch:** `feature/timeline-temporal-operational`
- **Scope:** manual creation of an `Activity`; post-create series editing is explicitly out of scope here

## Why this decision exists

The previous Advanced Create surface exposed the full recurrence engine directly to a user creating an Activity. That surface mixed three different concerns:

1. the user-facing act of making the current Activity repeat;
2. the reusable Recurrence engine and its advanced pattern families;
3. Outcome / Reminder controls that are not part of recurrence at all.

That was technically expressive but product-incorrect. Internal engine vocabulary such as `calendar-wall-clock`, elapsed interval, quota frame and cyclic positions must not define the normal Create information architecture.

This decision narrows the **manual scheduled-Activity Create surface** without weakening the Domain or deleting supported recurrence semantics.

## Permanent semantic boundaries

The existing domain rules remain authoritative:

```text
Activity != Routine
Routine != Recurrence
Recurrence != Occurrence
Occurrence != Schedule
Routine policy != concrete Schedule
planned/intended != happened
```

For an Activity that repeats:

```text
Activity authoring intent
        ↓
Routine-owned recurring policy
        ↓
Recurrence rule
        ↓
Occurrence candidates
        ↓
accepted Schedule(s), when applicable
```

The UI may simply say **Ripeti**. It does not need to expose the internal Routine ownership selector.

For Activity recurrence, the recurrence owner remains canonically `routine`. For Event recurrence, the owner remains `event`.

## Accepted manual Activity Create surface

When the user is manually creating an Activity with a concrete time/date, `Ripeti` exposes the familiar calendar-based family only:

```text
Non si ripete
Ogni giorno
Ogni settimana
Ogni mese
Ogni anno
Personalizza…
```

The quick choices map to canonical `calendar-wall-clock` recurrence with interval `1`.

`Personalizza…` remains calendar-based and exposes only human-facing controls:

```text
Ripeti ogni [N] [giorno | settimana | mese | anno]

weekly  -> Giorni [L M M G V S D]
monthly -> giorno del mese | posizione nel mese

Termina -> Mai | Data | Dopo [N] occorrenze
```

The Activity date remains the calendar anchor for ordinary monthly/yearly repetition. Monthly positional repetition may use ordinal + weekday.

The UI must not expose the engine label `calendar-wall-clock`.

### Placement and expansion rule

The detailed Activity repeat editor belongs **directly to the `Ripeti` control**.

When Advanced Create is open and a calendar recurrence is active, the repeat detail block is rendered immediately below the `Ripeti` selector, before Life Area, Location, Reminder and the remaining Advanced sections. It must not be moved to the bottom of the form or separated from the selector by unrelated controls.

This is both a visual and DOM-order rule: keyboard/focus order must follow the same information architecture shown on screen. No CSS-only visual reordering or detached fallback panel is accepted for this relationship.

### End-of-series vocabulary and interaction

The end policy is not a dropdown. Advanced has enough space to expose all three choices directly in DANTE styling:

```text
Mai
Data
Dopo [N] occorrenze
```

The choices use direct radio-style selection. `Data` reveals the DANTE date picker; `Dopo` reveals the numeric occurrence count.

The user-facing term is **occorrenze**, not “numero di volte”. The persisted meaning remains the canonical recurrence count; this is a product-language decision, not a Domain rename.

## What is deliberately NOT exposed here

The following recurrence families remain valid canonical capabilities but are not normal controls for manual creation of a scheduled Activity:

### Quota per period

Example:

```text
Train 3 times per week
```

This is a flexible Routine expectation. It does not specify the three concrete placements. It belongs to a Routine/DANTE/scheduler authoring flow where placement can be decided separately.

It must not be presented beside a manually selected Activity timestamp as if the timestamp alone defined all required occurrences.

### Elapsed interval

Example:

```text
Take medicine every 12 elapsed hours
```

This is semantically different from `every day at 08:00`, especially across DST/timezone changes, and may naturally create multiple Occurrences per civil day.

The capability remains in the recurrence engine but is deferred to a dedicated Routine/DANTE advanced authoring flow rather than the normal scheduled-Activity `Ripeti` control.

### Cyclic positional recurrence

Examples include shift cycles and other repeated positional sequences. This remains an advanced Routine capability and is not part of the normal scheduled-Activity Create surface.

### Completion-relative and anchor-stream-relative recurrence

Examples:

```text
replace filter 30 days after the previous Actual replacement
backup after every qualifying photography Session
```

These remain advanced canonical recurrence semantics and are not flattened into calendar repeat controls.

## Multiple fixed times in the same civil day

A future Routine may legitimately express one repeated policy with multiple fixed wall-clock times, for example:

```text
Medication
08:00
20:00
```

This must **not** be faked by inventing unrelated Activity identities merely to fit the current editor.

The manual Activity Create surface does not implement multi-time-per-day Routine authoring in this slice. The capability is explicitly deferred for a dedicated Routine editor / DANTE authoring flow.

## Outcome and Reminder are not recurrence

The previous generic recurrence panel also rendered `Conferma e promemoria`.

That placement is superseded for Activity Create.

```text
Recurrence != Outcome policy
Recurrence != Reminder configuration
Outcome != Reminder
```

Activity Create already exposes the relevant Outcome verification and Reminder controls in their own product locations. They must not be duplicated inside the repeat editor.

## Code/UI consequence

Activity Advanced Create uses a focused Activity repeat surface for calendar recurrence.

The focused repeat surface is injected into the core Create flow immediately after the shared `Ripeti` selector. It is no longer owned by the lower generic Advanced-fields block. This prevents Life Area / Location / Reminder from splitting the selector from its detailed recurrence configuration.

The legacy generic recurrence surface is retained only for Event while Event authoring is reviewed separately. This is intentional compatibility, not an Activity fallback.

The underlying `TemporalCreateEventRecurrenceIntent` remains broader than the Activity manual Create surface. Keeping the broader model is deliberate because quota, elapsed, cyclic and later advanced families remain legitimate domain/runtime capabilities.

Therefore:

> **Hidden from this UI != deprecated in the domain.**

and:

> **No advanced recurrence family may be deleted merely because the normal Activity Create surface does not expose it.**

## Post-create editing boundary

This decision covers **creation only**.

Series mutation semantics such as:

```text
this occurrence
this and future occurrences
whole series
skip occurrence
pause Routine
end Routine
```

must be designed against the canonical Routine / Recurrence / Occurrence boundaries before being exposed. They are not implicitly defined by this Create UI change.

## Product intent

The manual surface should feel familiar and low-friction for common repetition while DANTE keeps stronger semantics behind it.

Normal user mental model:

```text
Create Activity
choose when it happens
choose whether it repeats
optionally customize the calendar pattern
```

Advanced intent such as flexible quotas, elapsed cadence, cycles, completion-relative generation or relation-anchored generation belongs to a dedicated Routine/DANTE authoring experience where the system can truthfully represent and schedule that intent.
