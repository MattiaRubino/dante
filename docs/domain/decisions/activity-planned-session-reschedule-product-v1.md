# Activity / Planned Session / Real Session — product rules v1

- **Status:** HISTORICAL PRODUCT FREEZE — Timeline card rule superseded by `activity-intervals-and-sessions-v2.md` (2026-10-05)
- **Date:** 2026-10-04
- **Workstream:** Timeline / Temporal-Operational B14/B07 consolidation
- **Scope:** normal placed Activity creation, planned Session slices, real Session execution, Timeline projection, reschedule/resize admission, Reality interaction
- **Presentation override (2026-10-10):** `activity-session-live-timeline-v1.md` now owns the main/internal Session desk, five-minute preview, one-card reality geometry and atomic cascade semantics. Historical product rules in §§11–16 on Schedule≠Session, no implicit completion and protected history remain durable. Do not read old single-envelope and generic-only controls as current UI.

For current Activity placement and Timeline projection, read `activity-intervals-and-sessions-v2.md`. The `planned` role in this historical decision still refers to future planned Sessions, while the new `interval` role represents the Activity's separate occupied periods. The single envelope-card rule in section 4.1 is historical.

## 1. Purpose

This decision freezes the product rules for the normal placed Activity flow before the separate `Da collocare` flow is consolidated.

The product must preserve the canonical boundaries:

```text
Activity != Session
Schedule != Session != Actual
planned != happened
Session END != Activity completion
```

The user-facing model for this slice is intentionally smaller than the full kernel capability set.

## 2. Product v1 surface

The normal Activity Create surface exposes:

```text
Activity
├── Activity Schedule / temporal envelope
├── Session execution capability
├── Outcome confirmation policy
├── 0..N planned Session slices
└── Placement protection   [accepted semantics; expose only after canonical wiring]
```

### 2.1 Sub-Activity authoring is not exposed

Activity decomposition remains a valid canonical kernel capability and its existing persistence/API/tests are retained.

Product v1 does **not** expose Sub-Activity authoring in Create.

Consequences:

1. `+ Sotto-attività` is removed from Create;
2. new Create drafts do not author child Activities;
3. existing decomposition persistence/migrations are not rolled back or rewritten;
4. no new product feature should depend on Sub-Activity until an explicit product reactivation decision;
5. focused kernel tests remain to prevent the dormant capability from silently rotting.

This is a product simplification, not a claim that Activity decomposition is semantically invalid.

## 3. Three distinct temporal truths

The product must always distinguish:

```text
Activity Schedule
= the accepted planned temporal envelope of the Activity

Planned Session slice
= a planned execution interval inside the Activity envelope

Real Session
= a truthful execution episode that actually happened
```

Example:

```text
Activity Schedule:        18:00 ------------------------ 21:00
Planned Session A:        18:00 ------ 19:00
Planned Session B:                       20:00 ------ 21:00
Real Session A:           18:13 ---- 18:51
Real Session B:                          20:22 ---- 20:57
```

Differences between plan and reality are valid information and must not be normalized away automatically.

## 4. Planned Session persistence and Timeline projection

A future planned Session is not a B08 Session identity.

Canonical persistence remains:

```text
planned Session in Create
= Schedule placement with Activity-owned `planned` role

real execution
= B08 Session identity
```

### 4.1 Timeline card rule

Planned Session slices must **not create independent Timeline cards**.

The Timeline owns one primary Activity card for the Activity envelope.

Planned Session slices belong to the Activity card/detail/Inspector as nested planning information, for example:

```text
┌ Activity: Studio inglese ───────────────┐
│ 18:00–21:00                             │
│                                         │
│ Sessioni pianificate                    │
│ • Teoria       18:00–19:00              │
│ • Esercizi     20:00–21:00              │
└─────────────────────────────────────────┘
```

The public Timeline projection must continue to represent the Activity envelope as the top-level scheduled item. Planned-role schedules are supporting structure/detail and are not sibling Timeline identities.

## 5. Planned Session containment

For every planned Session with an explicit placement:

```text
activity_start <= planned_session_start
planned_session_end <= activity_end
```

A planned Session outside the Activity envelope is invalid.

For the same Activity, overlapping planned Session intervals are not admitted in product v1. Gaps are allowed.

Example:

```text
Activity 18:00–21:00
Session A 18:00–19:00   ✓
Session B 20:00–21:00   ✓
```

The Activity may therefore describe one overall window while planned execution is split into multiple internal bands.

## 6. Untimed Session rows

Current canonical planned-slice persistence requires a temporal placement. Product code must not fabricate a Schedule merely to preserve a label.

If a future product slice introduces an untimed Session row, that row is an **authoring/planning draft** until it receives a valid placement; it must not be persisted as a fake B08 Session or fake Schedule.

An untimed planning draft would not block Activity movement because it has no temporal coordinate to invalidate. This behavior is accepted conceptually but is not claimed as implemented by this document.

## 7. Reschedule and resize — general rule

Changing an Activity Schedule must never silently rewrite dependent planned intervals.

The product uses a preview/admission model:

```text
user proposes Activity move/resize
→ compute affected planned Sessions
→ show proposed changes
→ highlight invalid rows
→ explicit user acceptance
→ one admitted mutation
```

No dependent planned Session is silently truncated, deleted or moved without the user seeing the resulting proposal when its placement changes.

## 8. Moving an Activity with planned Sessions

If the Activity is translated by a delta and planned Sessions have explicit placements, Dante proposes the same delta for those planned Sessions.

Example:

```text
before
Activity   18:00–21:00
Session A  18:00–19:00
Session B  20:00–21:00

proposed +1h
after
Activity   19:00–22:00
Session A  19:00–20:00
Session B  21:00–22:00
```

Even when the proposal remains valid, the changed Session times must be visible in the review panel before acceptance.

The review panel should show:

```text
Activity
18:00–21:00  →  19:00–22:00

Sessioni coinvolte
Session A  18:00–19:00 → 19:00–20:00
Session B  20:00–21:00 → 21:00–22:00

[Annulla] [Applica]
```

## 9. Invalid move/resize

If a proposed Activity move/resize would leave any planned Session outside the new envelope, the mutation is not admitted yet.

The panel must mark the invalid Session in red and keep the apply action unavailable until the user supplies a coherent placement.

Example:

```text
Activity new end: 20:30
Session B: 20:00–21:00   ✗ fuori dall'Activity
```

Dante must not automatically cut Session B to 20:30.

## 10. Moving one planned Session

A planned Session can be moved independently only while it remains inside its Activity envelope and does not overlap another planned Session.

A move outside the envelope is rejected.

A future UX may offer an explicit `Estendi anche l'Activity` action, but that is a coordinated mutation and must never happen implicitly.

## 11. Real Session execution never rewrites the plan

Pressing Play before or after the planned Activity time creates reality; it does not move the Activity Schedule.

Example:

```text
Activity Schedule: 18:00–19:00
Play:              17:42

Result:
Schedule remains   18:00–19:00
Real Session       17:42–...
```

The Inspector may later explain the deviation or offer an explicit planning correction, but execution must never silently rewrite Schedule.

Likewise, editing Schedule never rewrites a historical real Session.

## 12. Play / Pause / Resume / Stop

Within one open Session:

```text
Play
Pause
Resume
Stop
```

represents one real Session with multiple internal active/pause intervals.

Pause/Resume does not create child Sessions.

A later new `Play` after the previous Session has been ended creates a new Session identity.

## 13. Planned Session and real Session association

A real Session belongs to the Activity execution history.

Product v1 must not infer an exact planned-slice identity merely because the real Session overlaps one planned slice.

Rules:

1. Play from the Activity card starts a real Session for the Activity;
2. a future explicit action launched from a planned Session may carry an explicit planning association;
3. temporal overlap alone is not canonical proof that a real Session realizes one particular planned slice.

## 14. Passage of time does not create reality

When a planned Activity or planned Session interval passes with no real Session or Actual:

```text
not done          ❌ not inferred
skipped           ❌ not inferred
failed            ❌ not inferred
completed         ❌ not inferred
Actual(false)     ❌ not inferred
Outcome           ❌ not inferred
Confirmation      ❌ not inferred
```

The historical plan remains visible and reality remains unknown.

A future review queue may ask what happened, but the queue is a derived product projection, not reality itself.

## 15. Outcome review (`Ricordami alla fine`)

`Ricordami alla fine` is driven by real execution, not by Schedule expiration.

A concluded real Session may create a Reality review item.

Because:

```text
Session END != Activity completion
```

the review must allow the Activity to remain unresolved/not yet complete when additional execution is expected.

Planned Sessions may inform UX timing, but they do not determine truth.

## 16. Activity state and movement

### 16.1 Planned / reality unknown

An Activity whose Schedule is in the past but whose reality is still unknown remains reschedulable. Time passage alone does not lock it.

### 16.2 Real Session already exists

Historical real Sessions never move when the Activity Schedule moves.

A reschedule changes plan only.

### 16.3 Reality review already open

Moving the Activity does not delete a Reality review produced by a real Session. The review belongs to the execution evidence, not to the current Schedule.

### 16.4 Real Session currently open

Product v1 blocks Activity drag/resize while a real Session is actively open. This avoids changing the plan underneath an active execution episode.

### 16.5 Activity confirmed as occurred/completed

Once the Activity has accepted realized truth and Confirmation establishing it as occurred/completed, its normal Schedule is historically closed for product editing:

```text
no drag
no resize
no ordinary reschedule
```

The Activity remains where it happened.

A future `Duplica`, `Ripeti` or `Crea nuova da questa` command may create a new intention/Occurrence. It must not rewrite the confirmed historical Activity.

## 17. Recurrence scope

Recurring planning changes retain the established explicit scopes:

```text
questa
questa e successive
serie
```

Those scopes mutate planning for the selected/future Occurrences according to the recurrence contract.

They do not rewrite:

```text
historical real Sessions
historical Actual
historical Outcome
historical Confirmation
```

Future planned Session offsets belonging to affected Occurrences may be proposed together with the parent Schedule change and must pass the same preview/admission rules.

## 18. Placement protection

Accepted product meaning:

> `Proteggi collocazione` prevents Dante solver/AI/automations from automatically moving the Activity Schedule.

It does **not**:

1. prevent a real Session from starting earlier/later;
2. force reality to match the plan;
3. rewrite execution truth;
4. necessarily forbid an explicit manual user move.

A manual move still goes through the same preview/admission rules for planned Sessions.

### 18.1 Exposure rule

`Proteggi collocazione` must not be exposed as an enabled product checkbox until the current U2 canonical authoring/update path persists the protection together with planned Sessions.

The previous disabled `Da collegare` control is not a valid final product surface and should remain hidden.

## 19. Product implementation order

The next implementation work should follow this order:

1. keep Create Activity-only and remove Sub-Activity authoring UI;
2. stabilize planned Session authoring/readback inside the Activity;
3. keep the advanced footer anchored correctly;
4. implement a reschedule/resize preview command that computes dependent planned-Session changes;
5. refuse invalid proposals and surface red per-Session validation;
6. lock drag/resize while a real Session is open;
7. lock ordinary Schedule editing after confirmed realized truth;
8. wire canonical placement protection, then expose its checkbox;
9. integrate recurrence scopes with the same planning preview semantics;
10. render planned/real Sessions inside Activity card/Inspector without creating sibling Timeline cards.

## 20. Non-negotiable invariants

1. Planned Session is not a future B08 Session.
2. Planned Sessions do not create independent Timeline cards.
3. Real Session history is never moved by Schedule changes.
4. Schedule is never silently rewritten by Play/Stop.
5. Dependent planned-Session changes are previewed before acceptance.
6. Invalid planned Sessions block Activity move/resize until resolved.
7. A confirmed historical Activity is not ordinarily rescheduled.
8. Open live execution blocks Activity drag/resize in product v1.
9. Passage of time alone never invents reality.
10. Sub-Activity kernel capability remains intact but is not a Create product feature in v1.
