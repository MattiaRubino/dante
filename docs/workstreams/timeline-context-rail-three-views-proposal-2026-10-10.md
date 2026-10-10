# Home Context Rail — three views and Objective confirmation (product discussion)

**Status: PROPOSAL / DISCUSSION OPEN — NOT APPROVED OR IMPLEMENTED.**
**Date:** 2026-10-10
**Source:** real-app acceptance feedback, screenshot on 2026-10-10.
**Preserve:** Schedule≠Session≠Actual≠Outcome/Confirmation; never invent completed work from the clock.

## Source-backed current behavior

`apps/backend/src/dante/modules/temporal/resolution_queue_api.py` currently returns a narrowly derived unresolved inbox (`reconciliation_open`, `realization_review`, `objective_review`). Activity reality review depends on an accepted `review_on_end` policy and a completed bounded real Session; an ended Session is not automatically an open review. `apps/web/src/features/home/ui/context-rail/context-rail.tsx` maps those items to the current **Da verificare** pane. `ObjectiveControls` presently writes an accepted ObjectiveResult immediately on Boolean click, qualitative selection or numeric `Registra`, with no separate user-confirm step. Therefore an empty review rail after a Stop is not, by itself, a backend failure.

## User-proposed product change: one rail, three switchable views

1. **Conclusi:** an actor-owned bounded, paginated recent history of finished real Sessions, ended Event instances, Activities with explicit completion/status facts, and any other truly concluded operations. Show truthful labels `Sessione conclusa` vs `Attività completata`; do **not** equate Session Stop with an Activity's final Outcome. A finished item may also have pending Objective assessment, and its history remains immutable. Date-grouping and links to Inspector, not duplicated Session cards.
2. **Da verificare:** today's accepted reconciliation/reality-review queue, plus **only explicitly governed missing-execution questions**, grouped by Activity (not one item per unused child). Clock expiry, an unstarted planned Session or dragged-to-past Schedule alone must not create a fact `non eseguita`, `saltata`, failure or Actual. Whether to offer opt-in reminders for missed sessions is an open decision.
3. **Obiettivi:** a separate overview of Objective observations/assessments awaiting input or confirmation for Activities, Events and supported Occurrences, linked to the same canonical objective records and Inspector controls. Do not silently mark objectives satisfied when a Session ends.

## Confirmation interaction: to be decided before persistence implementation

User asks for an editable value/assessment and an adjacent `Conferma` action (same flow in rail and Inspector), after which that Objective is removed from `da compilare`, while history remains available. Decide whether typing is:
- **local, uncommitted editing** until pressing Conferma (simpler, no persistent draft but unconfirmed entry lost on reload); or
- **durable provisional observation** stored as pending and separate from accepted ObjectiveResult/Assessment, preserved across refresh and devices (requires explicit new canonical persistence contract, owner ACL, replay/CAS and reconciliation).

**Do not implement an ambiguous halfway state that writes the final canonical Result and merely hides/unhides a checkmark.** A confirmed result must have exactly one accepted truth; a draft cannot masquerade as the confirmed observation. Feedback/error and keyboard confirmation must be consistent in Inspector and rail.

## Acceptance / boundaries

No immediate implementation of three views or new Objective confirmation just from this draft. First accept precise meaning of finished Activity vs finished Session, expired-but-untouched work review policy, and value-before-confirm persistence. This is separate from the **current small Session desk bugfixes** (right-aligned popup + Stop-cleared rows). Do not restructure `ContextRail` until product semantics are approved. Existing B10 resolution queue and Objective results remain authoritative during interim.
