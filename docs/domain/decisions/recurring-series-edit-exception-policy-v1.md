# Recurring series edit: boundary and exception policy

- **Status:** Accepted decision; metadata scope implemented, structural series edit pending
- **Date:** 2026-10-19
- **Applies to:** recurring Activity (Routine source) and recurring Event

## Identity and edit scope

The selected occurrence is an instance, not the series source. Before opening
Edit, the user chooses **Solo questa istanza** or **Questa e le successive**.
When the selected instance contains factual registrations, the structural
series choice starts **Dalla prossima istanza**; the selected instance keeps
its current plan and facts. An individual edit still uses the existing
Activity/Event safety locks. A series edit revises source policy from the
chosen boundary; it does not rewrite past instances.

The completed series editor must expose the full set of applicable authoring fields, including
time, all-day precision, intervals, capture and planned Session definitions,
objectives, reminder, Life Area, description and Event agenda. A metadata-only
save must never masquerade as a full series edit. Each persisted change needs
the same owner, revision, idempotency, and transaction guarantees as a local
change. A preview is informative, not a write entitlement: acceptance must
re-read the complete source and affected instances under an authoritative
lock and reject a stale preview.

## Future instances

| State at acceptance | Outcome of a series change |
| --- | --- |
| Not yet materialized | Generated from the new policy when needed. |
| Materialized, no local edit and no factual registration | Reconciled with the revised policy. A change of cadence may replace a clean expected instance with a new one; this is an explicit planned-history transition, never a deletion of facts. |
| Individually moved, skipped, edited, or containing a registration/observation | Protected exception. Preserve its identity, existing accepted plan, and facts. Do not propagate any series fields to it. |
| Already past | Unchanged, except an explicit permitted local correction. |

A protected exception whose coordinate no longer belongs to the revised
cadence still exists and is visible as an exception of that series. Neither
silently merge it with a newly generated instance nor present it as if its
original rule still governed current future policy. The concrete reconciliation
of materialized clean occurrence identifiers, accepted Schedule history,
reminders, and already linked planning is part of the persistence vertical;
it cannot be approximated by filtering Timeline cards.

Example: a daily series is changed to Tuesdays. A future Monday instance
previously moved to Thursday remains on Thursday as a protected exception;
unmodified future expectations follow the new pattern. The preview shows that
Thursday instance before confirmation.

## Preview and feedback

Before applying **Questa e le successive**, show the boundary, new recurrence
summary, how many clean future instances will be revised/reconciled, and the
protected future instances with a reason (local change, registration, skip).
The visual treatment should match the factual-registration notice in Activity
Edit: an explicit compact row for each protected instance, not a silent
warning buried in generic text. For a large series the preview remains
bounded and must show the total plus a limited inspectable sample. A stale
change, ambiguous identity match, or incomplete authoritative inventory
blocks acceptance with a reason and retry; no partial save. A successful
confirmation reports the actual affected and preserved counts.

Session/Actual/Objective observations remain factual even when a recurring
source changes. An open or paused registration is protected just like a
completed one. A series edit never deletes a registration automatically.

## Current implementation boundary (2026-10-19)

The owner-scoped profile edit accepts title, description, location and color.
The Inspector asks for the scope in a centered modal before opening any editor,
including an Edit reached by dragging a recorded recurring Activity. It provides
a bounded materialized preview with protected exception reasons, and the server
checks its fingerprint again under the source lock. A registered selected instance uses `from_next`;
its selected profile is not changed. Materialized protected future instances
are excluded from each accepted metadata policy and preserve their effective
profile snapshot. Unmaterialized future instances inherit the accepted policy.
Only a metadata change may be saved with a series scope. The Activity editor
explicitly rejects a mixed structural/metadata series submission before any
individual writes. The Event metadata editor uses the Occurrence capability
for a selected recurring instance instead of revising the Event source
globally. Life Area and agenda editing from a recurring Event occurrence are
blocked until the structural series capability is implemented.

Dragging an unrecorded recurring Activity also asks for the scope before any
write. **Solo questa istanza** applies the local replan. **Questa e le
successive** opens the existing series editor, but does not apply the dragged
time: series Schedule changes remain outside the metadata-only capability.
The choice explains this limitation before selection; it must never silently
apply a single-instance move under a series label. A registered Activity drag
still opens scope selection before Edit, under the Session safety rules.
The scope prompt visually replaces the Inspector, and cancelling it closes
the Inspector without saving. The current-time ruler is independent of these
modals and keeps a visible line across the full day lane.

**Pending persistence vertical:** authoritative versioned Activity template
and Event structure, cadence replacements with clean-instance reconciliation,
Schedule and reminder revisions, interval, capture, planned Session, Objective,
Life Area and agenda propagation. Preview classification also needs an
immutable marker for a planned Session's local name override (the current
mutation updates its name in place), plus common source-lock serialization
for concurrent instance writes. Until these exist, do not expose those fields
as if the series scope could save them. AI authoring must use the same
authoritative preview and acceptance contract, and must not compose separate
local writes to imitate a series change.

The recurring Create transport commits the Routine/Event source, its Recurrence,
and its initial occurrence policy in one transaction. Its replay checks the
same policy intent. This removes a partial-source failure window in Create;
it does not implement revision or propagation of that policy in Edit. A series
revision still requires a versioned policy, authoritative inventory, and
atomic reconciliation of clean materialized instances before the full editor
can submit structural changes.

A completed Routine Occurrence → Activity binding is also an instance boundary.
Subsequent Timeline checkpoint reads may create an unbound occurrence Activity
or retry an incomplete materialization, but they must never replay authoring
for a bound Activity. In particular, a local date/time replan remains the
Activity's accepted plan when the user navigates to another Timeline day; the
old template must not be replayed with the same create id, and no checkpoint
may fail because that plan differs from the original template.

## Non-goals

This decision does not equate multi-day intervals with recurrence, does not
turn a local exception into a source edit, and does not authorize hard deletion
or silent fact correction. The existing metadata-only scoped edit endpoint is
not evidence that structural series editing is implemented.
