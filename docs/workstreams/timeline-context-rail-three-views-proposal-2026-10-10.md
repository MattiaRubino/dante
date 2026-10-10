# Home Context Rail — three views and Objective confirmation (approved product decision)

**Status: APPROVED by user 2026-10-10; implementation candidate published, local PostgreSQL/frontend gate and real-app acceptance PENDING.**
**Date:** 2026-10-10
**Source:** real-app acceptance feedback, screenshot on 2026-10-10.
**Preserve:** Schedule≠Session≠Actual≠Outcome/Confirmation; never invent completed work from the clock.

## Source-backed current behavior

`apps/backend/src/dante/modules/temporal/resolution_queue_api.py` currently returns a narrowly derived unresolved inbox (`reconciliation_open`, `realization_review`, `objective_review`). Activity reality review depends on an accepted `review_on_end` policy and a completed bounded real Session; an ended Session is not automatically an open review. `apps/web/src/features/home/ui/context-rail/context-rail.tsx` maps those items to the current **Da verificare** pane. `ObjectiveControls` presently writes an accepted ObjectiveResult immediately on Boolean click, qualitative selection or numeric `Registra`, with no separate user-confirm step. Therefore an empty review rail after a Stop is not, by itself, a backend failure.

## User-proposed product change: one rail, three switchable views

1. **Conclusi:** an actor-owned bounded, paginated recent history of finished real Sessions, ended Event instances, Activities with explicit completion/status facts, and any other truly concluded operations. Show truthful labels `Sessione conclusa` vs `Attività completata`; do **not** equate Session Stop with an Activity's final Outcome. A finished item may also have pending Objective assessment, and its history remains immutable. Date-grouping and links to Inspector, not duplicated Session cards.
2. **Da verificare:** today's accepted reconciliation/reality-review queue, plus **only explicitly governed missing-execution questions**, grouped by Activity (not one item per unused child). Clock expiry, an unstarted planned Session or dragged-to-past Schedule alone must not create a fact `non eseguita`, `saltata`, failure or Actual. Whether to offer opt-in reminders for missed sessions is an open decision.
3. **Obiettivi:** a separate overview of Objective observations/assessments awaiting input or confirmation for Activities, Events and supported Occurrences, linked to the same canonical objective records and Inspector controls. Do not silently mark objectives satisfied when a Session ends.

## Confirmed input semantics: durable provisional value, then explicit accepted result

The user selected **durable persisted provisional input**. Entering a value saves an actor-owned versioned `temporal_objective_input_draft` without creating an Observation or Result. The separate adjacent `✓ Conferma` invokes owner/CAS/idempotent `confirm_self_objective_input_draft`, which atomically records the canonical ObjectiveResult and the confirmation receipt. Inspector and Home call the same client and API; accepted results are never rewritten by drafting. Existing Result correction remains the only accepted correction path. New PostgreSQL migration `_139` and current `ObjectiveControls` share this contract; pending user-local gate.

**Do not implement an ambiguous halfway state that writes the final canonical Result and merely hides/unhides a checkmark.** A confirmed result must have exactly one accepted truth; a draft cannot masquerade as the confirmed observation. Feedback/error and keyboard confirmation must be consistent in Inspector and rail.

## Acceptance / boundaries

**Code candidate is published:** `_139`–`_141`, three-tab `ContextRail`, bounded history/objective reads and shared confirm UI. Acceptance is NOT yet proven: user will run `tooling/verify-b14-session-home-workspace-local.sh` and perform real-app walkthrough. Expired-but-never-started work remains unknown without an explicit B10 review policy. This file is the dated decision record; the current UX and migration authority remain the domain decision and database overlay.
